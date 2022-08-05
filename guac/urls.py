from django.urls import re_path
from guac import views


urlpatterns = [
    re_path(r"^(?P<label>\w+)/(?P<session_id>\w+)/$", views.index, name="index"),
]
