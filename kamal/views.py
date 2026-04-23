from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 

@login_required (login_url='/login/')
def recipe(request):
    if request.method == "POST":
        data = request.POST

        recipe_name = data.get('recipe_name')
        description = data.get('description')
        image = request.FILES.get('image')

        Recipe.objects.create(
         user=request.user,
         recipe_name= recipe_name,
         description=description,
         image= image,
       )

        return redirect('/')  
    queryset = Recipe.objects.all()
    search_query = request.GET.get('search')
    print("Search Query:", search_query)
    if search_query:
        queryset = queryset.filter(recipe_name__icontains=search_query)

    return render(request, 'recipe.html', {'recipe': queryset})

@login_required(login_url='/login/')
def delete_recipe(request, id):

    recipe = Recipe.objects.filter(id=id).first()

    if recipe is None:
        messages.error(request, "Recipe not found")
        return redirect('/')

    if recipe.user == request.user or request.user.is_superuser:
        recipe.delete()
        messages.success(request, "Deleted successfully")
    else:
        messages.error(request, "No permission")

    return redirect('/')

@login_required(login_url='/login/')
def delete_all(request):

    if request.user.is_superuser:
        Recipe.objects.all().delete()
        messages.success(request, "All recipes deleted")
    else:
        Recipe.objects.filter(user=request.user).delete()
        messages.success(request, "Your recipes deleted")

    return redirect('/')

@login_required(login_url='/login/')
def update_recipe(request, id):

    recipe = Recipe.objects.filter(id=id).first()

    if recipe is None:
        messages.error(request, "Recipe not found")
        return redirect('/')

    if recipe.user != request.user and not request.user.is_superuser:
        messages.error(request, "No permission")
        return redirect('/')

    if request.method == "POST":
        recipe.recipe_name = request.POST.get('recipe_name')
        recipe.description = request.POST.get('description')

        if request.FILES.get('image'):
            recipe.image = request.FILES.get('image')

        recipe.save()
        messages.success(request, "Updated successfully")
        return redirect('/')

    return render(request, 'update_recipe.html', {'recipe': recipe})

   
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Wrong password")
            return render(request, 'login.html')

        login(request, user)
        return redirect('/')

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST)
        
        user = User.objects.filter(username=username)
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exist !")
            return render(request, 'register.html')

                
        user=User.objects.create_user(
           
            first_name = first_name,
            last_name = last_name,
            username = username, 
           
        )
        user.set_password(password)
        user.save()
        messages.success(request, "account created successfully")
        return redirect('http://127.0.0.1:8000/register_page/')
       
    return render(request,'register.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")