from django import template
from django.db.models import Count, F
from news.models import CategoryNews
from django.core.cache import cache


register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return CategoryNews.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    #categories = CategoryNews.objects.all()
    # categories = cache.get('categories')
    # if not categories :
    #     categories = CategoryNews.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)
    categories = CategoryNews.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    return {"category": categories}
