from rest_framework import serializers

class YouTubeDownloadSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
    format = serializers.ChoiceField(choices=['audio', 'video'], required=True)
