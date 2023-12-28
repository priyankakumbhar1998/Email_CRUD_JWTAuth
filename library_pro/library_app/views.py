from .models import Library
from .serializers import LibrarySerializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from library_pro.utils import send_email

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')


class LibraryAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(Self, request):
        try:
            library= Library.objects.all()
            serializer = LibrarySerializers(library, many=True)
            success_logger.info(f'all books fetched successfully!!!')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            error_logger.error(f'There is an error in fetching all books')
            return Response(data={'detail': 'There is an error fetching books'}, status=status.HTTP_400_BAD_REQUEST)
    
        
    def post(self, request):
        try:
            serializer = LibrarySerializers(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            body = "Hello %s, You have just created a book %s"%(request.user.username, serializer.data.get)
            subject = "book created successfully!!!"
            recipient_list = [request.user.email]
            send_email(subject=subject, body=body, recipient_list=recipient_list)
            success_logger.info(f'Book created successfully!!!with id {serializer.data.get("id")}')
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            error_logger.error(f'failed to create book {serializer.errors}')
            return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
        
class LibraryDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            library = get_object_or_404(Library, pk=pk)
            serializer = LibrarySerializers(library)
            success_logger.info(f'book details are retrieved: {serializer.data}')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f'There is an error retrieving books')
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk=None):
        try:
            library = get_object_or_404(Library, pk=pk)
            serializer = LibrarySerializers(library, data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                body = "Hello %s, You have just updated a book %s"%(request.user.username, serializer.data.get)
                subject = "book updated successfully!!!"
                recipient_list = [request.user.email]
                send_email(subject=subject, body=body, recipient_list=recipient_list)
                success_logger.info(f"Book updated successfully!!! : {instance}")
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f"Failed to update Book data: {pk} : {serializer.errors}")
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def patch(self, request, pk=None):
        try:
            library = get_object_or_404(Library, pk=pk)
            serializer = LibrarySerializers(data=request.data, instance=library, partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                success_logger.info(f'Book data partially updated successfully!!! {instance}')
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error(f'There is an error fetching student {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            library = get_object_or_404(Library, pk=pk)
            library.delete()
            success_logger.info(f"Book deleted successfully!!! {pk}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_logger.error(f'Failed to delete Book')
            return Response(data={'datail': 'Error in deleting Book'}, status=status.HTTP_400_BAD_REQUEST)

        




