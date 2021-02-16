from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views




app_name = 'feed'
urlpatterns = [
    path('',views.feed,name='feed'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/<str:user>',views.profile,name='profile'),
    path('profile/edit/<str:user>',views.profileEdit,name='profile_edit'),
    #path('posts/delete/<str:author>/<str:hour>/<str:day>/<str:month>/<str:year>/',views.postDelete),
    #path('posts/delete/<str:author>/<str:hour>/<str:day>/<str:month>/<str:year>/<str:result>/',views.postDelete)
    path('posts/delete/<str:author>/<str:publish>/',views.postDelete),
    path('posts/delete/<str:author>/<str:publish>/<str:result>/',views.postDelete)
  
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)