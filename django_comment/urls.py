from django.contrib import admin
from django.urls import path
from comment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', views.comment, name='comment'),
    path('reply/<int:comment_id>/', views.reply, name='reply'),
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
]
