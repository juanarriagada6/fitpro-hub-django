from django import forms
from .models import Rutina

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['alumno', 'titulo', 'ejercicios']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Ej: Rutina de Piernas - Hipertrofia'}),
            'ejercicios': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 4, 'placeholder': 'Escribe los ejercicios, series y repeticiones...'}),
        }