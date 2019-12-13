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

    form = ReviewForm(request.POST)
    #print('Form type:', type(form), 'Form content:', form)
    if request.method == 'POST':
        #if form.is_valid():
        review = Review()
        review.text = form.cleaned_data['text']
        review.product = product
        # логика для добавления отзыва
        review.save()
    reviews = Review.objects.all()
    for k in reviews:
        print(k.text)
    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
    }

    return render(request, template, context)
