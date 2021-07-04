from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'short_text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'author', 'created')
    search_fields = ('text',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    search_fields = ('user__username', 'following__username')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
