from django.urls import path

from .views import ProjectCreateView, ProjectListView, project_detail

urlpatterns = [
    path("", ProjectListView.as_view(), name="list"),
    path("add", ProjectCreateView.as_view(), name="add"),
    path("<slug:project_slug>", project_detail, name="detail"),
]
