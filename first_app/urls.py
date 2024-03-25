# urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='base'),
    path('registration/', views.userregistration, name='registration'),
    path('editor/', views.editor_register, name='editor'),
    path('viewer/', views.viewer_register, name='viewer'),
    path('login/', views.userlogin, name='login'),
    path('login_editor/', views.editor_login, name='login_editor'),
    path('login_viewer/', views.viewer_login, name='login_viewer'),
    path('detail/<int:news_id>', views.detail, name='detail'),
    path('all-news', views.all_news, name='all-news'),
    path('all-category', views.all_category, name='all-category'),
    path('category/<int:category_id>/', views.category_detail, name='category-d'),
    path('profile/', views.profi, name='profile'),
    path('profile2/', views.profi2, name='profile2'),
    path('create/', views.create_article, name='create_article'),
    path('edit/<int:article_id>/', views.edit_article, name='Edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article')
    # path('logout/', views.user_logout, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
