from rest_framework import serializers
from .models import Article

class ArticleSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title','author']