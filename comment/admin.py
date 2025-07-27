from django.contrib import admin

from comment.models import Comment, User


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = '用户名'

    list_display = ('get_username', 'content', 'created_at')

