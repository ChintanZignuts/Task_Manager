from rest_framework import status,viewsets,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,TaskSerializer
from .models import Task

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        self.perform_destroy(task) 
        return Response({"message": "Task deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)