from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerialzier
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

# Create a article list
@api_view (['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        #serialize all the requested article
        serializer = ArticleSerialzier(articles, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        #first parse the data 
        #data = JSONParser().parse(request)
        
        serializer = ArticleSerialzier(data=request.data)
        # if our serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) #201 is creates status
        #if the json response is not valid, return serializer error
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
        

@api_view (['GET', 'PUT', 'DELETE'])
def article_detail(request, pk) : #pk - primary key
    try: 
        article = Article.objects.get(pk=pk)

    except Article.DoesNotExist : 
        return HttpResponse(status= status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = ArticleSerialzier(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        #data = JSONParser().parse(request)
        serializer = ArticleSerialzier(article, data=request.data)
        #if serializer is valid it saves the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) #201 is creates status
        #if the json response is not valid, return serializer error
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        article.delete()
        return Response(status = status.HTTP_200_OK)

