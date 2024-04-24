from django.urls import path
from . import views
from .views import post_detail

urlpatterns = [
    path('',views.home,name='home'),
    path('blogadmin/',views.blogadmin,name='blogadmin'),
    path('signin/',views.signin,name='signin'),
    path('signup/',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
