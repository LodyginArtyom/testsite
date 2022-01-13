from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Время изменения')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/', verbose_name='Photo', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Статус опубликации')
    category = models.ForeignKey(
        'CategoryNews', verbose_name='Категория', on_delete=models.PROTECT, blank=True)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        # строит новую ссылку
        return reverse('view_news', kwargs={"pk": self.pk})


    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class CategoryNews(models.Model):
    title = models.CharField(
        max_length=150, db_index=True, verbose_name='Категория новости')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория новостей'
        verbose_name_plural = 'Категории новостей'
        ordering = ['title']
