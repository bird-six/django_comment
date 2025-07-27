from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Comment


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(
            username=username,
            password=password,
        )
        return redirect('user_login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('comment')
        else:
            messages.error(request, '用户名或密码错误')
    return render(request, 'login.html')

def comment(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = "访客"
    if request.method == 'POST':
        # 登录状态验证
        if not request.user.is_authenticated:
            messages.error(request, '请先登录再发表评论')
            return redirect('user_login')
        # 获取表单数据
        content = request.POST.get('content')
        # 数据验证
        if not content.strip():
            messages.error(request, '评论内容不能为空')
            return redirect('comment')
        # 创建评论
        Comment.objects.create(content=content, user=request.user)
        return redirect('comment')
    # 查询数据库中评论列表
    comments = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    return render(request, 'comment.html', {
        'username': username,
        'comments': comments,
    })

def reply(request, comment_id):
    # 获取被回复的评论对象
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        # 登录状态验证
        if not request.user.is_authenticated:
            messages.error(request, '请先登录再发表回复')
            return redirect('user_login')

        # 获取回复表单数据
        reply_content = request.POST.get('reply_content')
        # 数据验证
        if not reply_content.strip():
            messages.error(request, '回复内容不能为空')
            return redirect('comment')
        # 创建回复
        Comment.objects.create(
            content=reply_content,
            user=request.user,
            parent=comment
        )
        return redirect('comment')
    return render(request, 'comment.html', {
        'comment': comment,
    })
