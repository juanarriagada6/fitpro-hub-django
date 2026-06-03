from django.db import models
from django.contrib.auth.models import User

class Rutina(models.Model):
    titulo = models.CharField(max_length=200)
    ejercicios = models.TextField()
    fecha_asignada = models.DateTimeField(auto_now_add=True)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_rutinas')

    def __str__(self):
        return f"Rutina: {self.titulo} | Alumno: {self.alumno.username}"
    
