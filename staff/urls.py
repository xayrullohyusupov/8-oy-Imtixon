from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/',include('api.urls')),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('populate-db/', views.populate_db, name='populate_db'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff_attendance/<int:pk>/update/', views.update_staff_attendance, name='update_staff_attendance'),
    path('staff_attendance/<int:pk>/delete/', views.delete_staff_attendance, name='delete_staff_attendance'),
]
