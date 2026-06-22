from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Rutina
from .forms import RutinaForm

# --- VISTAS PÚBLICAS Y DE ALUMNOS ---

def index(request):
    imc = None
    clasificacion = ""
    error_mensaje = None

    if request.method == 'POST' and 'calcular_imc' in request.POST:
        try:
            peso = float(request.POST.get('peso', 0))
            altura_cm = float(request.POST.get('altura', 0)) # Recibe centímetros

            if peso <= 0 or altura_cm <= 0:
                error_mensaje = "El peso y la altura deben ser mayores a cero."
            elif peso > 300 or altura_cm > 250:
                error_mensaje = "Por favor, ingresa valores reales (ej: máximo 300 kg y 250 cm)."
            else:
                # Transformamos cm a metros para la fórmula del IMC
                altura_m = altura_cm / 100
                imc = round(peso / (altura_m ** 2), 1)
                
                if imc < 18.5:
                    clasificacion = "Bajo peso"
                elif 18.5 <= imc < 25:
                    clasificacion = "Peso normal (Saludable)"
                elif 25 <= imc < 30:
                    clasificacion = "Sobrepeso"
                else:
                    clasificacion = "Obesidad"
        except ValueError:
            error_mensaje = "Por favor, ingresa números válidos."

    return render(request, 'tareas/index.html', {
        'imc': imc, 
        'clasificacion': clasificacion, 
        'error_mensaje': error_mensaje
    })

@login_required
def dashboard(request):
    rutinas = Rutina.objects.filter(alumno=request.user)
    return render(request, 'tareas/dashboard.html', {'rutinas': rutinas})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- VISTAS PRIVADAS DE ADMINISTRACIÓN / GESTIÓN (CRUD DEL COACH) ---

def es_admin(user):
    return user.is_staff

@login_required
@user_passes_test(es_admin)
def panel_administracion(request):
    rutinas = Rutina.objects.all()
    return render(request, 'tareas/panel_administracion.html', {'rutinas': rutinas})

@login_required
@user_passes_test(es_admin)
def crear_rutina(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_administracion')
    else:
        form = RutinaForm()
    return render(request, 'tareas/rutina_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin)
def editar_rutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)
    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            return redirect('panel_administracion')
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'tareas/rutina_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin)
def eliminar_rutina(request, id):
    rutina = get_object_or_404(Rutina, id=id)
    if request.method == 'POST':
        rutina.delete()
        return redirect('panel_administracion')
    return render(request, 'tareas/rutina_eliminar.html', {'rutina': rutina})

@login_required
def redireccion_login(request):
    if request.user.is_staff:
        return redirect('panel_administracion')
    else:
        return redirect('dashboard')