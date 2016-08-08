from django.db import models
from django.conf import settings
from carts.models import Cart

# Create your models here.
class UserCheckout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)  # required
    email = models.EmailField(unique=True)

    def __unicode__(self):  # when python 3, __str__(self):
        return self.email


ADDRESS_TYPE = (
    ('billing', 'Billing'),  # firstin database second code
    ('shipping', 'Shipping'),
)


class UserAddress(models.Model):
    user = models.ForeignKey(UserCheckout)
    type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)

    def __unicode__(self):
        return self.street


class Order(models.Model):
    cart = models.ForeignKey(Cart)
    user = models.ForeignKey(UserCheckout)
    billing_address = models.ForeignKey(UserAddress, related_name='billing_address')
    shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address')
    shipping_total_price = models.DecimalField(max_digits=50,decimal_places=2,default=5.99)
    order_total = models.DecimalField(max_digits=50,decimal_places=2)

    def __unicode__(self):
        return str(self.cart.id)
# class Order(models.Model):
# cart
# usercheckout --> required
# shipping address
# billing address
# shipping total price
# order total (cart total + shipping)
# order_id --> custom id
