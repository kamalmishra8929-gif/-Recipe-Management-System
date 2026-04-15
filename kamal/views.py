from django.shortcuts import render, redirect
from .models import *

def recipe(request):
    if request.method == "POST":
        data = request.POST

        recipe_name = data.get('recipe_name')
        description = data.get('description')
        image = request.FILES.get('image')

        Recipe.objects.create(
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

def delete_recipe(request, id):
    recipe =  Recipe.objects.get(id=id)
    recipe.delete()
    return redirect('/')

def delete_all(request):
    recipe= Recipe.objects.all().delete()
    return redirect('/')
def update_recipe(request, id):
    recipe = Recipe.objects.get(id=id)

    if request.method == "POST":
        data = request.POST

        recipe.recipe_name = data.get('recipe_name')
        recipe.description = data.get('description')

        if request.FILES.get('image'):
            recipe.image = request.FILES.get('image')

        recipe.save()  

        return redirect('/') 

    return render(request, 'update_recipe.html', {'recipe': recipe})