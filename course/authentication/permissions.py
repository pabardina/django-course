from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to use it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'auth_token') and hasattr(request.auth, 'key') and not request.method == "GET":
            return obj.auth_token.key == request.auth.key
        elif request.method == 'POST' or request.method == "GET":
            return permissions.AllowAny(),