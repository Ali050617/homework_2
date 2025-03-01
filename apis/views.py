from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from .models import Post, Comment, Category, Tags
from .serializers import (
    PostSerializer, CommentSerializer, CategorySerializer, TagsSerializer
)


class PostListCreateView(APIView):
    def get(self, request):
        queryset = Post.objects.filter(status="published").order_by('-created_at')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = PostSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        data = request.data.copy()
        data['slug'] = slugify(data.get('title', post.title))
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        return Response({'detail': 'Post o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCommentListAPIView(APIView):
    def get(self, request, post_slug):
        post = get_object_or_404(Post, slug=post_slug)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryPostListAPIView(APIView):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(category=category)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class TagListAPIView(APIView):
    def get(self, request):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data)


class TagPostListAPIView(APIView):
    def get(self, request, slug):
        tag = get_object_or_404(Tags, slug=slug)
        posts = Post.objects.filter(tags=tag)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
