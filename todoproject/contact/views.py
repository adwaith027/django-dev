from django.shortcuts import render

# Create your views here.
def abc(request):
    return render(request,'./contact/contactus.html')