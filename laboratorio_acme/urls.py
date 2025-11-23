from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # <--- Verifica que esto esté
from django.contrib.auth import views as auth_views # <--- Verifica que esto esté

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ListaServicios.as_view(), name='inicio'),
    path('equipo/', views.ListaEquipo.as_view(), name='equipo'),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('registro/', views.registro_cliente, name='registro'),
    path('pedido/nuevo/<int:servicio_id>/', views.CrearPedido.as_view(), name='crear_pedido'),
    path('mis-pedidos/', views.MisPedidos.as_view(), name='mis_pedidos'),
    path('laboratorio/', views.PanelLaboratorio.as_view(), name='panel_laboratorio'),
    path('laboratorio/tomar/<int:pedido_id>/', views.tomar_pedido, name='tomar_pedido'),
    path('laboratorio/finalizar/<int:pedido_id>/', views.finalizar_pedido, name='finalizar_pedido'),
    path('perfil/editar/', views.EditarPerfil.as_view(), name='editar_perfil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)