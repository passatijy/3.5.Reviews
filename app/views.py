from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    session = request.session.session_key
    print('Session id:', session)
    form = ReviewForm(request.POST)
    #print('Form type:', type(form), 'Form content:', form)
    if 'reviewed_products' in request.session.keys():
        reviewed = request.session.get('reviewed_products')
        print('Reviewed items:', reviewed)
    else:
        request.session['reviewed_products'] = []
    print('req session keys:', request.session.keys())

    if request.method == 'POST':
        #if form.is_valid():
        if pk not in reviewed:
            print('Product id:', pk, ', ... you are in not_revieved selection')
            review = Review()
            #review.text = form.cleaned_data['text']
            review.product = product
            # логика для добавления отзыва
            review.save()
            request.session['reviewed_products'].append(pk)
            print('Reviewed items:', request.session.get('reviewed_products'))
        else:
            print('you review to this product allways exist')

    reviews = Review.objects.all()
    for k in reviews:
        print(k.text)
    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
    }

    return render(request, template, context)
