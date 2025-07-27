from django.contrib.auth.models import User
from django.db import models

class Comment(models.Model):
    # 关联到 User 模型，使用外键，当用户删除时，对应评论也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # 父级评论（自关联）
    parent = models.ForeignKey(
        'self',     # 关联模型自身
        on_delete=models.CASCADE,       # 父评论被删除后，子评论一并删除
        null=True,      # 允许为空，即代表顶级评论
        blank=True,
        related_name='replies'  # 通过comment.replies.all()获取所有回复
    )

    # 获取所有子回复（递归）
    def get_all_replies(self):
        replies = []
        for reply in self.replies.all():
            replies.append(reply)
            replies.extend(reply.get_all_replies())
        return replies

    # 获取父评论的用户名,用于显示回复的指向信息
    def get_parent_username(self):
        if self.parent:
            return self.parent.user.username
        return None