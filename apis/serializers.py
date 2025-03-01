from rest_framework import serializers
from .models import *


class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'email', 'bio')

    def validate_email(self, value):
        if "@" not in value or "." not in value:
            raise serializers.ValidationError("Noto‘g‘ri email formati!")
        return value


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'post_count')
        extra_kwargs = {'slug': {'read_only': True}}

    def get_post_count(self, obj):
        return Post.objects.filter(category=obj).count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class TagsSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Tags
        fields = ('id', 'name', 'slug', 'post_count')
        extra_kwargs = {'slug': {'read_only': True}}

    def get_post_count(self, obj):
        return Post.objects.filter(tags=obj).count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'created_at', 'author_email', 'content', 'parent_comment', 'replies')

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True).data

    def validate_author_email(self, value):
        if not value or "@" not in value:
            raise serializers.ValidationError("Email manzili to‘g‘ri formatda bo‘lishi kerak.")
        return value

    def validate_parent_comment(self, value):
        if value:
            level = 1
            parent = value
            while parent.parent_comment:
                level += 1
                parent = parent.parent_comment
                if level >= 3:
                    raise serializers.ValidationError("Komment faqat 3-darajaga qadar joylashtirilishi mumkin.")
        return value


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    author = AuthorModelSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'author', 'category', 'tags',
                  'created_at', 'updated_at', 'status', 'comments_count')
        extra_kwargs = {'slug': {'read_only': True}}

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)
