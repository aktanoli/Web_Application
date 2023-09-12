from django.urls import path
from . import views

#Week 3 Lesson 2 Video 1
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
#path('books/',views.books),
#to map a whole class as a view
#path('books',views.BookList.as_view()),
#path('books/<int:pk>',views.Book.as_view()),
#Week 2 Restuarant Menu API
path('menu-items', views.MenuItemsView.as_view()), #include this in the project urls.py
path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
path('category_items',views.CategoryView.as_view()),
path('secret/',views.secret),
#path('menu-itemsc', views.MenuItemsCView.as_view())
path('api-token-auth/', obtain_auth_token), # add this URL pattern for token generation
path('manager-view/', views.manager_view),
#path('roles/', views.roles),
path('api-token-auth/', obtain_auth_token),
path('throttle-check/', views.throttle_check),
path('throttle-check-auth/', views.throttle_check_auth),
#path('me/', views.me),
path('manager-view/', views.manager_view),
path('groups/manager/users', views.managers)
]