from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
# Create your views here.

from .models import Product, Variation, Category
from .forms import VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
import random


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
        object = self.get_object()
        product_set = object.product_set.all()
        default_products = object.default_category.all()
        products = (product_set | default_products).distinct()
        context["products"] = products
        return context


class VariationListView(LoginRequiredMixin, ListView):
    model = Variation
    queryset = Variation.objects.all()

    def get_context_data(self, **kwargs):
        context = super(VariationListView, self).get_context_data()
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get('pk')
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product=product)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        print request.POST
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                try:
                    product_pk = self.kwargs.get('pk')
                    product = get_object_or_404(Product, pk=product_pk)
                    new_item.product = product
                    new_item.save()
                except:
                    pass
            messages.success(request, "Your inventory and pricing has been updated")
            return redirect("products")
        raise Http404


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")  # None
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            queryset = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query)
            )
            try:
                queryset2 = self.model.objects.filter(
                    Q(price=query)
                )
                queryset = (queryset | queryset2).distinct()
            except:
                pass

        return queryset


class ProductDetailView(DetailView):
    model = Product

    # template_name = "product.html"
    # template_name = "<appname>/<modelname>_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        # order_by('-title")
        context['related'] = sorted(Product.objects.get_related(instance)[:6], key=lambda x: random.random())
        return context


"""
def product_detail_view_func(request, id):
    # product_instance = Product.objects.get(id=id)
    product_instance = get_object_or_404(Product, id=id)
    try:
        product_instance = Product.objects.get(id=id)
    except Product.DoseNotExist:
        raise Http404
    except:
        raise Http404
    template = "products/product_detail.html"
    context = {
        "object": product_instance
    }
    return render(request, template, context)
"""
