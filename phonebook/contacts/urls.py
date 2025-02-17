from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Show all contacts
    path('contacts-admin/', views.admin_panel, name='admin_panel'),  # Manage contacts in one place
    path('download/', views.download_contacts, name='download_contacts'),  
    path("contacts-admin/login/", views.editor_login, name="editor_login"),  # Custom Login Page
    path("contacts-admin/logout/", views.editor_logout, name="editor_logout"),  # Logout
]
