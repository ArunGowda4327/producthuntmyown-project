from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

def homepage(request):
    product = Product.objects
    return render(request, 'products/home.html', {'product':product})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url'] and request.POST['body'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title']
            product.url = request.POST['url']
            product.body = request.POST['body']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))

        else:
            return render(request, 'products/create.html', {'error':'all fields required'})



    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    return render(request, 'products/detail.html', {'product':product})

@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    product = get_object_or_404(Product, pk = product_id)
    product.total_votes += 1
    product.save()
    return redirect('/products/' + str(product.id))
