from django.urls import path
from . import views


urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/comments/', views.CommentListCreateAPIView.as_view(), name='comment_list'),
    path('posts/<slug:post_slug>/comments/', views.PostCommentListAPIView.as_view(), name='post_comments'),
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('categories/<slug:slug>/posts/', views.CategoryPostListAPIView.as_view(), name='category_posts'),
    path('tags/', views.TagListAPIView.as_view(), name='tag_list'),
    path('tags/<slug:slug>/posts/', views.TagPostListAPIView.as_view(), name='tag_posts'),
]