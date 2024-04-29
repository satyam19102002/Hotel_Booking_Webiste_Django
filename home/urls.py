
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_booking/' , check_booking),
    path("",home,name = 'home'),
    path("login_page/",login_page,name = 'login_apge'),
    path("register/",register,name = 'register'),
    path("hotel-detail/<uid>",hotel_detail , name = 'hotel_detail')
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()