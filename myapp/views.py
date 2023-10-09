from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,orderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe,json
from .forms import ProductForm
from django.urls import reverse
from django.http import JsonResponse,HttpResponseNotFound

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request,'myapp/index.html',{'products':products})


def detail(request,id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request,'myapp/detail.html',{'product':product,'stripe_publishable_key':stripe_publishable_key})

@csrf_exempt
def create_checkout_session(request,id):
    request_data = json.loads(request.body)
    product = Product.objects.get(id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = request_data['email'],
        payment_method_types = ['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'usd',
                    'product_data':{
                        'name':product.name,
                    },
                    'unit_amount':int(product.price * 100)
                },
                'quantity':1,
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) +
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
        
    )
    
    order = orderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price)
    order.save()
    
    return JsonResponse({'sessionId':checkout_session.id})

#temporary payment success view.
def payment_success_view(request):

    # temporary view:

    order = orderDetail.objects.get(id=2)

    return render(request, 'myapp/payment_success.html', {'order': order})

#major payment success view
# def payment_success_view(request):
#     session_id = request.GET.get('session_id')
#     if session_id is None:
#         return HttpResponseNotFound()
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     session = stripe.checkout.Session.retrieve(session_id)
#     order = get_object_or_404(orderDetail,stripe_payment_intent= session.payment_intent)
#     order.has_paid = True
#     order.save()
    
#     return render(request,'myapp/payment_success.html',{'order':order})

def payment_failed_view(request):
    return render(request,'myapp/payment_failed.html')


#form to create product
def create_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
        
    product_form = ProductForm()
    
    return render(request,'myapp/create_product.html',{'product_form':product_form})


def product_edit(request,id):
    product = Product.objects.get(id=id)
    product_form = ProductForm(request.POST or None,request.FILES or None,instance=product)
    
    if request.method == 'POST':
        if product_form.is_valid():
            product_form.save()
            return redirect('index')
    return render(request,'myapp/edit_product.html',{'product_form':product_form})