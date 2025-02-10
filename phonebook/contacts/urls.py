from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Show all contacts
    path('admin/', views.admin_panel, name='admin_panel'),  # Manage contacts in one place
    path('download/', views.download_contacts, name='download_contacts'),  
    path("admin/login/", views.editor_login, name="editor_login"),  # Custom Login Page
    path("admin/logout/", views.editor_logout, name="editor_logout"),  # Logout
]
