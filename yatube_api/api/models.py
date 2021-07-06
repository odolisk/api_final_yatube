from slugify import slugify

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Group(models.Model):
    title = models.CharField(verbose_name='Наименование', max_length=200,
                             help_text='Введите название группы')
    slug = models.SlugField(verbose_name='Идентификатор URL',
                            unique=True,
                            blank=True,
                            help_text='Укажите идентификатор URL')
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        help_text='Введите описание группы')

    class Meta:
        verbose_name = 'Группа записей'
        verbose_name_plural = 'Группы записей'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts_author'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts_group',
        verbose_name='Группа',
        blank=True,
        null=True,
        help_text='Выберите группу для записи')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Запись'
    )
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows_i_read',
        verbose_name='Кто подписан',
        help_text='Кто подписан')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follows_i_author',
        verbose_name='На кого подписан',
        help_text='На кого подписан')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='follows-users'),
            models.CheckConstraint(
                check=~Q(user=F('following')),
                name='prevent_self_follow'),
        )

    def __str__(self):
        return f'{self.user.username} to {self.following.username}'
