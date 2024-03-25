from django.contrib.auth.decorators import login_required
from .models import News, Rating
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import NewsForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EditorLoginForm, ViewerLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import EditorRegistrationForm, ViewerRegistrationForm, EditorLoginForm, ViewerLoginForm
from .models import News, Category
from .models import News
from .models import Rating
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Avg
from .models import News, Category, Rating


def home(request):
    categories = Category.objects.all()
    top_articles_by_category = {}
    for category in categories:
        top_articles_by_category[category] = News.objects.filter(category=category).annotate(
            avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:2]

    return render(request, 'home1.html', {'top_articles_by_category': top_articles_by_category})


# def home(request):
#     return render(request, 'base1.html')


def detail(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    # Get the existing rating for the news article, if it exists
    rating = Rating.objects.filter(news=news).first()

    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))

        # If a rating already exists, update it; otherwise, create a new one
        if rating:
            rating.rating = rating_value
            rating.save()
        else:
            Rating.objects.create(news=news, rating=rating_value, comment='')

        return redirect('detail', news_id=news_id)

    # Get all ratings for the article
    ratings = Rating.objects.filter(news=news)

    # Get related news from the same category (excluding the current article)
    related_news = News.objects.filter(
        category=news.category).exclude(id=news_id)[:3]

    return render(request, 'detail1.html', {'news': news, 'ratings': ratings, 'related_news': related_news})


def all_news(request):
    all_news = News.objects.all()
    return render(request, 'all-news1.html', {
        'all_news': all_news
    })


def all_category(request):
    cats = Category.objects.all()
    return render(request, 'category1.html', {
        'cats': cats
    })


def category_detail(request, category_id):
    category = Category.objects.get(pk=category_id)
    # Get all news articles in the given category
    articles = News.objects.filter(category=category)

    # Calculate average ratings for each article
    for article in articles:
        article.avg_rating = Rating.objects.filter(
            news=article).aggregate(Avg('rating'))['rating__avg'] or 0

    # Sort articles by average rating in descending order
    articles = sorted(articles, key=lambda x: x.avg_rating, reverse=True)

    return render(request, 'category1detail.html', {'category': category, 'articles': articles})


def userlogin(request):
    categories = Category.objects.all()
    top_articles_by_category = {}
    for category in categories:
        top_articles_by_category[category] = News.objects.filter(category=category).annotate(
            avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:2]

    return render(request, 'userlogin.html', {'top_articles_by_category': top_articles_by_category})


def editor_login(request):
    if request.method == 'POST':
        form = EditorLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_editor:
                login(request, user)
                # Redirect to editor dashboard or specific page
                return redirect('profile2')
    else:
        form = EditorLoginForm()
    return render(request, 'login.html', {'form': form})


def profi2(request):
    all_news = News.objects.all()
    return render(request, 'profile2.html', {
        'all_news': all_news
    })


def viewer_login(request):
    if request.method == 'POST':
        form = ViewerLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_viewer:
                login(request, user)
                # Redirect to viewer dashboard or specific page
                return redirect('profile')
    else:
        form = ViewerLoginForm()
    return render(request, 'login.html', {'form': form})


def profi(request):
    categories = Category.objects.all()
    top_articles_by_category = {}
    for category in categories:
        top_articles_by_category[category] = News.objects.filter(category=category).annotate(
            avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:2]

    return render(request, 'profile1.html', {'top_articles_by_category': top_articles_by_category})


def userregistration(request):
    categories = Category.objects.all()
    top_articles_by_category = {}
    for category in categories:
        top_articles_by_category[category] = News.objects.filter(category=category).annotate(
            avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:2]

    return render(request, 'userregistration.html', {'top_articles_by_category': top_articles_by_category})


def editor_register(request):
    if request.method == 'POST':
        form = EditorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_editor')
    else:
        form = EditorRegistrationForm()
    return render(request, 'edit.html', {'form': form})


def viewer_register(request):
    if request.method == 'POST':
        form = ViewerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_viewer')
    else:
        form = ViewerRegistrationForm()
    return render(request, 'edit.html', {'form': form})


def create_article(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to home page after article creation
            return redirect('home')
    else:
        form = NewsForm()
    return render(request, 'create_article.html', {'form': form})


def edit_article(request, article_id):
    article = get_object_or_404(News, pk=article_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page after article edit
    else:
        form = NewsForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})


def delete_article(request, article_id):
    article = get_object_or_404(News, pk=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('home')  # Redirect to home page after article deletion
    return render(request, 'delete_article.html', {'article': article})
