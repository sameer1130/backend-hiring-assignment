from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .serializers import ProjectSerializer, TaskSerializer
from .models import Project, Task
from .forms import UserRegistrationForm, ProjectForm, TaskForm


User = get_user_model()  # Ensure we reference the correct user model

# --- User Registration ---
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        else:
            print(form.errors)  # Debugging: Print form errors in terminal
            messages.error(request, "Error in form submission.")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


# --- Home Page ---
def home(request):
    """Displays the project and task forms."""
    projects = Project.objects.all()
    tasks = Task.objects.all()
    project_form = ProjectForm()
    task_form = TaskForm()

    return render(
        request,
        "home.html",
        {
            "projects": projects,
            "tasks": tasks,
            "project_form": project_form,
            "task_form": task_form,
        },
    )


# --- Create and Update Forms ---
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()  # Save to DB

            # Serialize the newly created project
            serializer = ProjectSerializer(project)
            return redirect("home")  # ✅ Redirect back to home

        else:
            # If form is invalid, print errors (for debugging)
            print(form.errors)

    else:
        form = ProjectForm()

    projects = Project.objects.all()  # Fetch existing projects (like ProjectListCreateView)
    serialized_projects = ProjectSerializer(projects, many=True).data

    return render(request, "create_project.html", {
        "project_form": form,
        "projects": serialized_projects,  # Send data to template
    })


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()  # Save to DB

            # Serialize the newly created task
            serializer = TaskSerializer(task)
            return redirect("home")  # ✅ Redirect back to home

        else:
            # If form is invalid, print errors (for debugging)
            print(form.errors)

    else:
        form = TaskForm()

    tasks = Task.objects.all()  # Fetch existing tasks (like ProjectListCreateView)
    serialized_tasks = TaskSerializer(tasks, many=True).data

    return render(request, "create_task.html", {
        "task_form": form,
        "tasks": serialized_tasks,  # Send data to template
    })


def all_projects_tasks(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    return render(request, "all_projects_tasks.html", {"projects": projects, "tasks": tasks})

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("all_projects_tasks")
    else:
        form = ProjectForm(instance=project)
    
    return render(request, "edit_project.html", {"form": form})

def delete_project(request, pk):
    if request.method == "POST":
        project = get_object_or_404(Project, pk=pk)
        project.delete()
    return redirect("all_projects_tasks")

def delete_task(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect("all_projects_tasks")
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("all_projects_tasks")
    else:
        form = TaskForm(instance=task)
    
    return render(request, "edit_task.html", {"form": form})

def delete_task(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect("all_projects_tasks")


# --- Authentication Views ---
class LoginView(APIView):
    """Handles user login using Django's AuthenticationForm."""

    def post(self, request):
        form = AuthenticationForm(data=request.data)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Debugging messages
            print(f"✅ Login successful for: {user.username}")
            messages.success(request, "Login successful!")

            return Response({"message": "Login successful", "redirect_url": "/"}, status=status.HTTP_200_OK)

        else:
            # Debugging messages
            print("❌ Login failed!")
            print("Errors:", form.errors)  # Prints form validation errors

            messages.error(request, "Invalid credentials. Please try again.")

            return Response(
                {"error": "Invalid credentials", "details": form.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    """Logs out the user and returns a response."""

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# --- Project API Views ---
class ProjectListCreateView(generics.ListCreateAPIView):
    """Lists and creates projects."""

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()  # Remove filtering if you want to show all projects


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, or deletes a project."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


# --- Task API Views ---
class TaskListCreateView(generics.ListCreateAPIView):
    """Lists and creates tasks."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        """Fetch tasks optionally filtered by project_id"""
        project_id = self.request.query_params.get("project_id")
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return Task.objects.all()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves, updates, or deletes a task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
