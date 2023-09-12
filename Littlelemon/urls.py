"""
URL configuration for BookList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
# Week 3 Lesson 2 Video 5
#(Remove for video 5) from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/',include('BookListAPI.urls')),
    #DJANGO DEBUG TOOLBAR
    path('__debug__/', include('debug_toolbar.urls')),
    path('api/',include('LittlelemonAPI.urls')),
    #ENABLE DJOSER ENDPOINTS
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # Week 3 Lesson 2 Video 5
    #(Remove for video 5) path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

]
