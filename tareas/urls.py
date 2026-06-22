from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas públicas y de alumnos
    path("", views.index, name="index"),
    path("panel/", views.dashboard, name="dashboard"),
    path("registro/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    
    # 🚨 LA LÍNEA MÁGICA QUE HACE EL PUENTE 🚨
    path("redireccion-login/", views.redireccion_login, name="redireccion_login"),
    
    # Panel del admin 
    path("panel-admin/", views.panel_administracion, name="panel_administracion"),
    path("panel-admin/crear/", views.crear_rutina, name="crear_rutina"),
    path("panel-admin/editar/<int:id>/", views.editar_rutina, name="editar_rutina"),
    path("panel-admin/eliminar/<int:id>/", views.eliminar_rutina, name="eliminar_rutina"),
]
