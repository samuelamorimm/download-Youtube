from django.urls import path
from .views import YouTubeDownloadView

urlpatterns = [
    path('download/', YouTubeDownloadView.as_view(), name='youtube-download'),
]
