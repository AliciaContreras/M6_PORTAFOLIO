from django import forms
from .models import Pedido
from .models import Perfil

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['descripcion_pedido']
        widgets = {
            'descripcion_pedido': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalla aquí tus requerimientos especiales...'})
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia', 'foto']
        widgets = {
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }