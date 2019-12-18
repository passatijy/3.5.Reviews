from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm, NoReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    print('****************** FIRST METHOD ',request.method, ' *********************')
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    session = request.session.session_key
    print('Session id:', session)
    form = ReviewForm(request.POST)
    #print('Form type:', type(form), 'Form content:', form)
    is_reviewed = False

    def print_and_review(request, pk):
        print('----------------')
        print('Req session:', request.session)
        print('Req sess reviewed_products:', request.session['reviewed_products'])
        print('No review from this session on product', pk)
        review = Review()
        review.text = form.cleaned_data['text']
        review.product = product
        review.save()
        saved_list = request.session['reviewed_products']
        saved_list.append(pk)
        request.session['reviewed_products'] = saved_list

    if request.method == 'GET':
        print('WE IN GET!!')
        if not ('reviewed_products' in request.session):
            print('*** WE in First IF ***')
            form = ReviewForm(request.POST)
            reviews = Review.objects.all()
            is_reviewed = False
            context = {
            'form': form,
            'product': product,
            'reviews': reviews,
            'is_review_exist': is_reviewed,
            }
        else:
            if not (pk in request.session['reviewed_products']):
                print('*** WE in Second IF ***')
                form = ReviewForm(request.POST)
                reviews = Review.objects.all()
                is_reviewed = False
                context = {
                'form': form,
                'product': product,
                'reviews': reviews,
                'is_review_exist': is_reviewed,
                }
            else:
                print('You in GET method, and you reviewed this product')
                is_reviewed = True
                reviews = Review.objects.all()
                form = ReviewForm(request.POST)
                context = {
                'form': form,
                'product': product,
                'reviews': reviews,
                'is_review_exist': is_reviewed,
                }


    if request.method == 'POST':
        if form.is_valid():
            if not ('reviewed_products' in request.session):
                request.session['reviewed_products'] = []
                print_and_review(request, pk)

            else:
                if not (pk in request.session['reviewed_products']):
                    print_and_review(request, pk)
                else:
                    print('!!!!You reviewed this product!!!!')
                    is_reviewed = True
        reviews = Review.objects.all()
        for k in reviews:
            print('Reviews we have:', k.text)

        if is_reviewed:
            form = NoReviewForm(request.POST)
        else:
            form = ReviewForm(request.POST)

        context = {
            'form': form,
            'product': product,
            'reviews': reviews,
            'is_review_exist': is_reviewed,
        }



    return render(request, template, context)
