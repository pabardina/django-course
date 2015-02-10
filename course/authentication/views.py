from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, viewsets, authentication
from rest_framework import status, views
from rest_framework.response import Response

from authentication.models import Account
from authentication.serializers import AccountSerializer
from authentication.permissions import IsOwner


class AccountViewSet(viewsets.ModelViewSet):
    """ Account resource. """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = authentication.TokenAuthentication,
    permission_classes = IsOwner,

    def create(self, request):
        """
        Create an account

        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            account = Account.objects.create_user(**serializer.validated_data)
            serializer_with_token = AccountSerializer(
                account, context={'request': request})
            return Response(serializer_with_token.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        """
        Return a list of accounts.

        """
        return super(AccountViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update an object with all fields required

        """
        return super(AccountViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update an object with specific field

        """
        return super(AccountViewSet, self).partial_update(request, *args,
                                                          **kwargs)


class LoginView(views.APIView):
    """
    Login Ressource

    """
    permission_classes = permissions.AllowAny,

    def post(self, request, format=None):
        """
        Two arguments needed:
        username & password
        """
        data = request.DATA

        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    """
    Logout Ressource
    """

    def post(self, request, format=None):
        """
        Simple Call on /logout in post. No arguments

        """
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
