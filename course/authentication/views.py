from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, viewsets
from rest_framework import status, views
from rest_framework.response import Response

from authentication.models import Account
from authentication.serializers import AccountSerializer
from authentication.permissions import IsOwner


class AccountViewSet(viewsets.ModelViewSet):
    """ Account resource. """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
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
        Return a list of accountss.

        """
        return super(AccountViewSet, self).list(request, *args, **kwargs)


class LoginView(views.APIView):
    permission_classes = ()

    def post(self, request, format=None):
        data = request.DATA

        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account,
                                               context={'request': request})

                return Response(serialized.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)
