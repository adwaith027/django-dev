from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from django.contrib.auth.forms import UserCreationForm
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from products.forms import ProductForm
from rest_framework import status
from products.models import product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404

@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def simpleapi(request):
    return Response({'text': 'Hello , This is your api call'},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user=form.save()
        return Response('account created successfully', status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
def createProduct(request):
    form=ProductForm(request.POST)
    if form.is_valid():
        product=form.save()
        return Response({'id':product.id},status=status.HTTP_201_CREATED)
    return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((AllowAny,))
def listProduct(request):
    products=product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes((AllowAny,))
def updateProduct(request, pk):
    pdt=get_object_or_404(product,pk=pk)
    form=ProductForm(request.data,instance=pdt)
    if form.is_valid():
        form.save()
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    else:
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def deleteProduct(request,pk):
    try:
        pdt=product.objects.get(pk=pk)
    except product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    
    pdt.delete()
    return Response("Deleted Successfully")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createwithlogin(request):
    form=ProductForm(request.POST)
    if form.is_valid():
        product=form.save()
        return Response({'id':product.id},status=status.HTTP_201_CREATED)
    return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)