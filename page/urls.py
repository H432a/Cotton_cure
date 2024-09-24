from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("",views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('blog/',views.blog_view,name='blog'),
    path('blogsub/', views.blogsub_view, name='blogsub'),
    path('choose/', views.choose_view, name='choose'),
    path('page3/', views.page3_view, name='page3'),
    path('page1/', views.page1_view, name='page1'),
    path('payment/', views.payment_view, name='payment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)