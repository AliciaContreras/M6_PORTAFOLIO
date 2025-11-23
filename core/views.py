from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Servicio, Perfil, Pedido
from .forms import PedidoForm, PerfilForm

# --- Vista de Inicio (Muestra los Servicios) ---
class ListaServicios(ListView):
    model = Servicio
    template_name = 'core/inicio.html'
    context_object_name = 'servicios'

# --- Vista del Equipo (Muestra Jefes y Trabajadores) ---
class ListaEquipo(ListView):
    model = Perfil
    template_name = 'core/equipo.html'
    context_object_name = 'equipo'

    def get_queryset(self):
        return Perfil.objects.exclude(tipo='CLIENTE')

# --- Vista de Registro de Clientes ---
def registro_cliente(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user, tipo='CLIENTE', biografia="Cliente del laboratorio")
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


# --- Vista para realizar un pedido ---
class CrearPedido(LoginRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'core/crear_pedido.html'
    success_url = reverse_lazy('mis_pedidos')

    def form_valid(self, form):
        # Asignamos el cliente automáticamente (usuario logueado)
        form.instance.cliente = self.request.user
        # Asignamos el servicio según la URL (obtenemos el ID)
        servicio_id = self.kwargs['servicio_id']
        form.instance.servicio = get_object_or_404(Servicio, id=servicio_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Pasamos el servicio al template para mostrar el título/foto
        context = super().get_context_data(**kwargs)
        context['servicio'] = get_object_or_404(Servicio, id=self.kwargs['servicio_id'])
        return context

# --- Vista para ver mis pedidos ---
class MisPedidos(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = 'core/mis_pedidos.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        # Solo mostrar los pedidos del usuario actual
        return Pedido.objects.filter(cliente=self.request.user).order_by('-fecha_solicitud')
    
# --- Función de comprobación: ¿Es personal del laboratorio? ---
def es_personal(user):
    return user.is_authenticated and user.perfil.tipo in ['TRABAJADOR', 'JEFE']

# --- Vista del Panel de Laboratorio (Solo personal) ---
class PanelLaboratorio(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Pedido
    template_name = 'core/panel_laboratorio.html'
    context_object_name = 'pedidos_pendientes'

    def test_func(self):
        # Solo deja pasar si es TRABAJADOR o JEFE
        return es_personal(self.request.user)

    def get_queryset(self):
        # Muestra pedidos pendientes ORDENADOS por fecha (los más viejos primero)
        return Pedido.objects.filter(estado='PENDIENTE').order_by('fecha_solicitud')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # También pasamos los pedidos que el usuario YA tomó (En proceso)
        context['mis_trabajos'] = Pedido.objects.filter(trabajador_asignado=self.request.user, estado='EN_PROCESO')
        return context

# --- Acción para tomar un pedido ---
from django.contrib.auth.decorators import user_passes_test # Importar esto

@user_passes_test(es_personal)
def tomar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Solo si está pendiente
    if pedido.estado == 'PENDIENTE':
        pedido.trabajador_asignado = request.user
        pedido.estado = 'EN_PROCESO'
        pedido.save()
    
    return redirect('panel_laboratorio')

# --- Acción para finalizar un pedido ---
@user_passes_test(es_personal)
def finalizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Solo si es el trabajador asignado
    if pedido.trabajador_asignado == request.user:
        pedido.estado = 'TERMINADO'
        pedido.save()
        
    return redirect('panel_laboratorio')

# --- Vista para editar mi propio perfil ---
class EditarPerfil(LoginRequiredMixin, UpdateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'core/editar_perfil.html'
    success_url = reverse_lazy('equipo') # Al terminar, nos manda a ver el equipo

    def get_object(self):
        # Devuelve el perfil del usuario actual, sin importar la URL
        return self.request.user.perfil