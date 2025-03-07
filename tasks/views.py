from rest_framework import generics
from .serializers import ProjectSerializer,TaskSerializer
from .models import Project,Task



# Create your views here.


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(end_date__isnull=True)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.object.all()
    serializer = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

