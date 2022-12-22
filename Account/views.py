# Create your views here.

# ========================================================= Authentication =====================================================
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from Account.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages, auth
import uuid
from django.conf import settings
from django.core.mail import send_mail


# admin authentication 
# username = admin, 
# password = sharjeel

#  Test User
# username = test, 
# password = 1234

# =========== Token Page ================= 
def token(request):
    return render(request, "token.html")


# =========== Error Page ================= 
def error(request):
    return render(request, "error.html")


# ================================================== Accoount Creation Sign Up ============================================================-->
	                        
# =========== Sign Up User ===============
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            try:
                # =========== Check Username is available ===============
                if User.objects.filter(username = username).first():
                    return render(request,"signup.html", {'error': "User Name alraedy exist"}) 

                # =========== Check Email is available ===============
                if User.objects.filter(email = email).first():
                    return render(request,"signup.html", {'error': "Email Address alraedy exist"})  

                # =========== Check Password are Match ===============
                if password != confirm_password:
                    return render(request,"signup.html", {'error': "Password Not Match"})           
                
                user_obj = User.objects.create(username = username, email = email)
                user_obj.set_password(password)
                user_obj.save()

                auth_token = str(uuid.uuid4())
                profile = Profile.objects.create(user = user_obj, auth_token = auth_token)
                profile.save()

                send_email(email, auth_token)
                messages.success(request, "Token is Sent to your email address and check your mail")
                return redirect('/token')
            
            except Exception as e:
                print(e)
                return render(request, "error.html", {'error': "There is something Wroung Try Again"} )

        return render(request, "signup.html")

    else:
        return redirect('/')

# =========== Send Email With Uuid token ================= 
def send_email(email, auth_token):
    subject="your token is verifies"
    message=f'Hi User, Click link to verify your account http://127.0.0.1:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]

    send_mail(subject,message, email_from,recepient_list)


# =========== Verify User Uuid token ==================== 
def verify(request, auth_token):
    try:
        profile = Profile.objects.filter(auth_token = auth_token).first()
        if profile:
            profile.is_verified = True
            profile.save()
            messages.success(request, "Email is verified")
            print("Email is verified")
            print("Email is verified")
            return redirect('/login')
        else:
            return render(request,"error.html", {'error': "There is Something Wroung"}) 
    except Exception as e:
        print(e)
        return HttpResponse("page not found")


# ================================================= Login And Logout Authenticated User ===================================================-->
	                        
# ============= Login User ===================
def login(request):
    # ==== Prevent user to access Log In Page After Authenticate ====   
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username = username).first()

        # ============= Check Username Exists Or Not ===========
        if user_obj is None:
            messages.error(request, "Username Do Not Exist Sign Up Here")
            return redirect('/signup')

        profile = Profile.objects.filter(user = user_obj).first()
    
        if not profile.is_verified:
            messages.error(request, "Profile is not verified")
            return redirect('/login')

        user = authenticate(request, username = username, password = password)
        if user is None:
            messages.error(request, "Invalid email or password")
            return redirect('/login')

        auth.login(request, user)
        return redirect('/')

    return render(request, "login.html")

# ============= Log Out User ===================
def logout(request):
    auth.logout(request)
    return redirect('/login')

    

# ====================================================  # Forget User Password ==============================================================-->

# =========== Email For Forget Password ================= 
def forget(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']

            # ============ checking email Exists or not ===========
            if not User.objects.filter(email = email).first():
                return render(request,"sign.html", {'error': "User Do not Exists Please Sign Up Here"})      

            user_obj = User.objects.get(email = email)
            auth_token = str(uuid.uuid4())
            profile = Profile.objects.update(auth_token = auth_token)
            send_email_forget_password(email, auth_token)
            messages.success(request, "Token is sent to your Email ")
            return render(request,"token.html")

        except Exception as e:
            print(e)
            return render(request,"error.html",{'error': "There is something wroung"})

    return render(request, "forget.html")


# =========== Send Email With Uuid token ================= 
def send_email_forget_password(email, auth_token):
    subject="Reset Account Password"
    message=f'Hi User, Click link to Reset your password http://127.0.0.1:8000/change_password/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recepient_list = [email]

    send_mail(subject,message, email_from,recepient_list)


# =========== Forget Password =================
def change_password(request, auth_token):
    context = {} 

    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        messages.success(request, "Now You can change your password")
        
        context = { 'user_id': profile_obj.user.id }
        # ============ Reset New password here =============
        if request.method == "POST":
            new_password = request.POST['new_password']
            match_password = request.POST['confirm_password']
            user_id = request.POST.get('user_id')

            # ============ User Id Dont Exist =============
            if user_id is None:
                messages.info(request, "No user id Found")
                return redirect(f'/change_password/{auth_token}')
            
            # ============== Password not Match ================
            if new_password != match_password:
                messages.success(request, "Password Not Match")
                return redirect('/change_password')

            user_obj = User.objects.get(id= user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login')

    except Exception as e:
        print(e)
        return redirect('/error')
    
    return render(request,"change_password.html", context)
    