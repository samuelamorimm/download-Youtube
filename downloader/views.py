from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
import os

from .serializers import YouTubeDownloadSerializer

class YouTubeDownloadView(APIView):
    def post(self, request):
        serializer = YouTubeDownloadSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            file_format = serializer.validated_data['format']

            try:
                yt = YouTube(url)

                # Escolher o formato do download
                if file_format == 'audio':
                    stream = yt.streams.filter(only_audio=True).first()
                else:
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

                if not stream:
                    return Response(
                        {'error': f'No {file_format} stream available for the given video.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Realizar o download
                file_path = stream.download()
                return Response({
                    'message': f'{file_format.capitalize()} downloaded successfully!',
                    'file_name': os.path.basename(file_path)
                })

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
