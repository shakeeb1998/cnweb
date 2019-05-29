from  . import views
from django.urls import path
from django.conf.urls import url
from notification_sender import notify
import notification_sender
urlpatterns=[
    url(r'^enterdata$',views.enterDatatodb),
    url(r'^enterlocationdata$', views.enterlocationdata),
    url(r'^addparent', views.addParent),
    url(r'^getusers', views.getUsers),
    url(r'^getuserdetails', views.getuserdetails),
    url(r'^notify', notification_sender.notifier),
    url(r'^updatefcm', views.updateFcm),

]