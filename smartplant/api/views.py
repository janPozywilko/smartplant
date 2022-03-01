from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .utils import get_devices, get_minutes, get_range, create_device_application_server, create_device_identity_server, create_device_join_server, create_device_network_server, delete_device_application_server, delete_device_identity_server, delete_device_join_server, delete_device_network_server

# Create your views here.

class Test(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = Token.objects.get(key=request.auth.key).user_id # Get's id of the user from the token that was used
            user = User.objects.get(id=user_id) # Get's user objects from the coresponding token
            return Response({"current user": user.username}, status=status.HTTP_200_OK)
        except:
            return Response({"test": "can't get user from token"}, status=status.HTTP_200_OK)

class Devices(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            devices = get_devices()
            return Response(devices, status=status.HTTP_200_OK)
        except:
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class Minutes(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, minutes, dev_eui):
        try:
            json_minutes = get_minutes(minutes=minutes, dev_eui=dev_eui)
            return Response(json_minutes, status=status.HTTP_200_OK)
        except:
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class Range(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, start_timestamp, stop_timestamp, dev_eui):
        try:
            json_minutes = get_range(start=start_timestamp, stop=stop_timestamp, dev_eui=dev_eui)
            return Response(json_minutes, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class CreateDevice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # name = request.data['name']
            # dev_eui = request.data['dev_eui']
            dev_eui = "A8610A32372F6C08"
            ttn_name = "testing"
            

            create_IS_status = create_device_identity_server(ttn_name, dev_eui)
            create_JS_status = create_device_join_server(ttn_name, dev_eui)
            create_NS_status = create_device_network_server(ttn_name, dev_eui)
            create_AS_status = delete_device_application_server(ttn_name, dev_eui)

            return Response({"IS": create_IS_status, "JS": create_JS_status, "NS": create_NS_status, "AS": create_AS_status}, status=status.HTTP_201_CREATED)
            # if create_IS_status == 200:
            #     create_JS_status = create_device_join_server(ttn_name, dev_eui)
            # else:
            #     return Response({"message": "there was problem when creating your device please try again 1"}, status=status.HTTP_400_BAD_REQUEST)

            # if create_JS_status == 200:
            #     create_NS_status = create_device_network_server(ttn_name, dev_eui)
            # else:   
            #     delete_IS_status = delete_device_identity_server(ttn_name)
            #     return Response({"message": "there was problem when creating your device please try again 2"}, status=status.HTTP_400_BAD_REQUEST)
            
            # if create_NS_status == 200:
            #     create_AS_status = delete_device_application_server(ttn_name, dev_eui)
            # else:
            #     delete_JS_status = delete_device_join_server(ttn_name)
            #     delete_IS_status = delete_device_identity_server(ttn_name)
            #     return Response({"message": "there was problem when creating your device please try again 3"}, status=status.HTTP_400_BAD_REQUEST)

            # if create_AS_status == 200:
            #     return Response({"message": "Created device succesfully"}, status=status.HTTP_201_CREATED)
            # else:
            #     delete_NS_status = delete_device_network_server(ttn_name)
            #     delete_JS_status = delete_device_join_server(ttn_name)
            #     delete_IS_status = delete_device_identity_server(ttn_name)
            #     return Response({"message": "there was problem when creating your device please try again 4"}, status=status.HTTP_400_BAD_REQUEST)
            


        except:
            return Response({"error": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        