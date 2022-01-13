from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from .models import News, CategoryNews
from .forms import *
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешло зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
        # messeges.error(request, 'Ошибка')

    return render(request, 'news/register.html', {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
            form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})



def user_logout(request):
    logout(request)
    return redirect('login')

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'news.blogs.test@gmail.com', ['articrafter123@mail.ru'], fail_silently=True )
            if mail :
                messages.success(request, 'Письмо отправлено!')
                return redirect('contacts')
            else:
                messages.error(request, 'Ошибка ')
        else:
            messages.error(request, 'Ошибка ')
    else:
        form = ContactForm()
    return render(request,'news/contacts.html', {'form': form})


class HomeNews(ListView,MyMixin):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    #extra_context = {'title': 'Главная'}
    # mixin_prop = 'hello world!!!'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin,ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False  # 404 errors в случае перехода на несуществующую категорию
    paginate_by = 3
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(CategoryNews.objects.get(
            pk=self.kwargs['category_id']))
        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    #template_name = 'news/news_detail.html' # указание другого шаблона
    #pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # login_url = '/admin/'
    raise_excetion = True


#def index(request):
#    news = News.objects.order_by('-created_at')
#    context = {
#        'news': news,
#        'title': 'Список новостей',
#    }
#    return render(request, 'news/index.html', context)


#def get_category_news(request, category_id):
#    news = News.objects.filter(category_id=category_id)
#    categoryNow = CategoryNews.objects.get(pk=category_id)
#    return render(request, 'news/category.html', {'news': news, 'categories': categoryNow, 'title': 'Список новостей'})


#def view_news(request, news_id):
#    #news_item = News.objects.get(pk=news_id)
#    news_item = get_object_or_404(News, pk=news_id)
#    return render(request, 'news/view_news.html', {"news_item": news_item})


#def add_news(request):
#    if request.method == 'POST':
#        form = NewsForm(request.POST)
#        if form.is_valid():
#            #print(form.cleaned_data)
    #news = News.objects.create(**form.cleaned_data)
#            news = form.save()
#            return redirect(news)
##    else:
##        form = NewsForm()
#    return render(request, 'news/add_news.html', {'form': form})
#    return render(request, 'news/add_news.html', {'form': form})
#    return render(request, 'news/add_news.html', {'form': form})
