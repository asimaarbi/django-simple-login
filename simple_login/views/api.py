from rest_framework import status
from rest_framework.response import Response

from simple_login.serializers import (
    ActivationKeyRequestSerializer,
    PasswordResetRequestSerializer,
    PasswordChangeSerializer,
    StatusSerializer,
    ActivationValidationSerializer,
    LoginSerializer,
    RetrieveUpdateDestroyProfileValidationSerializer,
)
from simple_login.views.base import (
    BaseAPIView,
    ProfileBaseAPIView,
    AuthenticatedRequestBaseAPIView,
)


class ActivationAPIView(ProfileBaseAPIView):
    validation_class = ActivationValidationSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.activate()
        return Response(
            data=self.get_user_profile_data_with_token(),
            status=status.HTTP_200_OK
        )


class ActivationKeyRequestAPIView(BaseAPIView):
    validation_class = ActivationKeyRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_account_activation_key()
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(ProfileBaseAPIView):
    validation_class = LoginSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return Response(
            data=self.get_user_profile_data_with_token(),
            status=status.HTTP_200_OK
        )


class PasswordResetRequestAPIView(BaseAPIView):
    validation_class = PasswordResetRequestSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.generate_and_send_password_reset_key()
        return Response(status=status.HTTP_200_OK)


class PasswordChangeAPIView(BaseAPIView):
    validation_class = PasswordChangeSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        self.user_account.change_password(
            self.serializer.data.get('new_password')
        )
        return Response(status=status.HTTP_200_OK)


class StatusAPIView(BaseAPIView):
    validation_class = StatusSerializer

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class RetrieveUpdateDestroyProfileAPIView(AuthenticatedRequestBaseAPIView):
    validation_class = RetrieveUpdateDestroyProfileValidationSerializer
    http_method_names = ['put', 'get', 'delete']

    def get(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.get_auth_user())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        self.get_auth_user().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        serializer = self.update_fields_with_request_data()
        self.ensure_password_hashed()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
