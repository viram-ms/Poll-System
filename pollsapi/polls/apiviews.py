from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer

class PollList(generics.ListCreateAPIView):
    # def get(self,request):
        # polls = Poll.objects.all()[:20]
        # data = PollSerializer(polls,many=True).data
        # return Response(data)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
    # def get(self,request,pk):
        # poll = get_object_or_404(Poll,pk=pk)
        # data = PollSerializer(poll).data
        # return Response(data)
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ChoiceList(generics.ListCreateAPIView):
    # def get(self,request,pk):
        # poll = get_object_or_404(Poll,pk=pk)
        # data = PollSerializer(poll).data
        # return Response(data)
    # queryset = Choice.objects.all()
    # serializer_class = ChoiceSerializer
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id = self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

class CreateVote(generics.CreateAPIView):

    def post(self,request, pk, choice_pk):
        print(request.data)
        voted_by = request.data.get('voted_by')
        print(voted_by)
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        # return Response(status = status.HTTP_201_CREATED)
    serializer_class = VoteSerializer

