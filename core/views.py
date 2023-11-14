from django.shortcuts import render
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
import pandas as pd
from geopandas.tools import geocode
# Create your views here.

@api_view(['GET'])
def get_data(request):
   address =request.GET.get('address', '')
   # person =  {'name':'Dennis', 'age':28}
   coordinate_data = geocode(address, provider="nominatim",
                          user_agent="aryaanand", timeout=5)
   return Response({'coordinates':str(coordinate_data.geometry.values[0])})

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        print(request.FILES)
        file_obj = request.FILES['file']
        df = pd.read_csv(file_obj)
        print(df.shape)
        jsonData = []
        for index, row in df.iterrows():
            #print(index)
            #print(row)
            information = geocode(row[0], provider="nominatim",
                                 user_agent="aryaanand", timeout=5)
            #print(information.geometry.values[0])
            jsonData.append({'Address':row['Monuments'] + ' ' + row['City'], 'Coordinates':str(information.geometry.values[0])})
        return Response(jsonData)
        # return Response({'details': "File Saved Succesfully"}, status=204)

