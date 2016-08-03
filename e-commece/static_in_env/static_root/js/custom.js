/**
 * Created by pms on 2016. 8. 3..
 */

function showFlashMessage(message) {
    var template = '{% include "alert.html" with message="' + message + '" %}';
    $('body').append(template);
    $('.container-alert-flash').fadeIn();
    setTimeout(function () {
        $('.container-alert-flash').fadeOut();
    }, 2500);
}
