from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    TaskListCreateView, 
    TaskDetailView,
    create_project,
    create_task,
    all_projects_tasks,
     delete_project,
     edit_task,
     delete_task,
     edit_project,
     )



urlpatterns = [
   
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name = 'project-detail'),
    path('projects/create/', create_project, name='create_project'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', create_task, name='create_task'),
    path("all-projects-tasks/", all_projects_tasks, name="all_projects_tasks"),
    path("projects/<int:pk>/edit/", edit_project, name="edit_project"),
    path("projects/<int:pk>/delete/", delete_project, name="delete_project"),
    path("tasks/<int:pk>/edit/", edit_task, name="edit_task"),  # Edit Task URL
    path("tasks/<int:pk>/delete/", delete_task, name="delete_task"),
]