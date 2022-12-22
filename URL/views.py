from tkinter import EXCEPTION
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import url_user
import random, string



@login_required(login_url="/login")
def dashboard(request):
    return render(request, 'dashboard.html')
    
# =============================== Function to generate random URL ==========
def randomnum():
    return ''.join(random.choice(string.ascii_lowercase)for _ in range(6))

@login_required(login_url="/login")
def home(request):
    return render(request,"index.html")

            
@login_required(login_url="/login")
def generate(request):
    if request.method == 'POST':
        if request.POST['original'] and request.POST['short']:
            # =========================== Generate On url user value =================
            user = request.user
            originalurl = request.POST['original']
            short = request.POST['short']
            check = url_user.objects.filter(short_url = short)
            if not check:
                newurl= url_user(
                    user = user,
                    original_url = originalurl,
                    short_url = short,
                )
                newurl.save()
                return redirect(dash)
            else:
                messages.error(request, "Url already Exists")
                return redirect(dash)
        elif request.POST['original']:
            # ============================= Generate On url random value ================
            user = request.user
            originalurl = request.POST['original']
            generate = False
            while not generate:
                short = randomnum() # function for random value 
                check = url_user.objects.filter(short_url = short)
                if not check:
                    newurl= url_user(
                        user = user,
                        original_url = originalurl,
                        short_url = short,
                    )
                    newurl.save()
                    generate = True
                    return redirect(dash)
                else:
                    continue
        else:
            messages.error(request, "Empty Field")
            return redirect(dash)
    else:
        return redirect(dash)


def go(request, query=None):    
    if not query or query is None:
        return render(request,"dash.html")
    else:
        try:
            check = url_user.objects.get(short_url = query) # === query is vlaue to redirect
            check.visit = check.visit + 1 
            check.save()
            url_to = check.original_url
            return redirect(url_to)
        except url_user.DoesNotExist:
            auth.logout(request)
            return render(request,"login.html")
        except Exception as e:
            return render(request,"error.html", {'error': 'error'})


@login_required(login_url="/login")
def dash(request):
    user = request.user
    user_url = url_user.objects.filter(user = user)
    url = url_user.objects.all()
    return render(request, 'dash.html', {'url': url})
    