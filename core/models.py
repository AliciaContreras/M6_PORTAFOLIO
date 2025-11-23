from django.db import models
from django.contrib.auth.models import User

# --- 1. Perfil Extendido (Para Jefes, Trabajadores y Clientes) ---
class Perfil(models.Model):
    # Tipos de usuario
    TIPO_USUARIO = [
        ('JEFE', 'Jefe de Laboratorio'),
        ('TRABAJADOR', 'Trabajador'),
        ('CLIENTE', 'Cliente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='CLIENTE')
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_display()}"

# --- 2. Servicios del Laboratorio Acme ---
class Servicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    precio_aproximado = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.titulo

# --- 3. Pedidos (Clientes piden servicios) ---
class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('TERMINADO', 'Terminado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos_realizados')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    descripcion_pedido = models.TextField(help_text="Detalles específicos de lo que necesita")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    # Trabajador que toma el pedido (puede ser nulo al principio)
    trabajador_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trabajos_asignados')

    def __str__(self):
        return f"Pedido de {self.cliente.username}: {self.servicio.titulo}"