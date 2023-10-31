# serializers.py
from rest_framework import serializers

class FollowerSerializer(serializers.Serializer):
    username = serializers.CharField()

class FollowingSerializer(serializers.Serializer):
    username = serializers.CharField()

class Follower_Following_Serializer(serializers.Serializer):
    username = serializers.CharField()

class Following_Followers_Serializer(serializers.Serializer):
    username = serializers.CharField()