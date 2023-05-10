from django.urls import path
from . import views


urlpatterns = [

    path("home/",views.index, name = "index"),
    path("profiles",views.profile_list, name = "profile_list"),
    path("account/<int:pk>",views.profile, name = "account"),
    path("detail/<int:video_id>",views.video_details, name = "video_detail"),
    path("aboutus/",views.aboutus, name = 'aboutus'),
    path("login/",views.login, name = 'signin'),
    path("signup/",views.signup, name = 'signup'),
    # path('like-video/<int:video_id>/', views.like_video, name='like_video'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('logout/', views.logout_view, name = 'logout'),


]
