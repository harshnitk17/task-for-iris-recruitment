from django.urls import path

from . import views
from django.conf.urls import url

app_name = 'market'
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('myprofile/myadds', views.myadds, name='myadds'),
    path('updateprofile/', views.update_profile, name='update_profile'),
    path('post/', views.add, name='add'),
    path('home/', views.market, name='market'),
    path('sell/', views.sell, name='sell'),
    path('rent/', views.rent, name='rent'),
    path('search/<slug:keyword>/', views.search, name='search'),
    url(r'^show_add/(\d+)/$', views.show_add, name="show_add"),
    url(r'^edit_add/(\d+)/$', views.edit_add, name="edit_add"),
]
