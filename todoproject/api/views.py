from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from django.contrib.auth.forms import UserCreationForm
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@api_view(["GET",""])
@permission_classes((AllowAny,))
def simpleapi(request):
    return Response({'text': 'Hello world, This is your first api call'},status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    form = UserCreationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        return Response({'message':"account created successfully",
                         'data':form.data}, status=HTTP_201_CREATED)
    return Response(form.errors, status=HTTP_400_BAD_REQUEST)


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
@permission_classes((IsAuthenticated,))
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response({"message": "Logged out successfully"}, status=HTTP_200_OK)