
from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('',views.index),
  path('thanks/<str:id>/<str:format>',views.thx),
  path('error/',views.error),
  path('download/<str:id>/<str:format>', views.download_client)
]