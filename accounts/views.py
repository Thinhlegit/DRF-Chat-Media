from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.views import APIView

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

from rest_framework import generics, permissions

# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Sending Mail
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def sendmail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)        
        # email = request.POST.get('email')
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            # print(form.cleaned_data['email'])
            email = form.cleaned_data['email']
            html = render_to_string('contactform.html',{
                'name':name,
                'email':email,
                'content':content
            })
            print('valid')
            send_mail('subject','message','lehaquangthinh@gmail.com',[email],html_message=html,fail_silently=False)
            # send_mail('subject','message','noreply@lehaquangthinh.com',[email],html_message=html)

            return render(request, 'contactform.html',
            {
                'form':form
            })
    else:
        form = ContactForm()
    return render(request, 'contactform.html',
    {
        'form':form
    })
    