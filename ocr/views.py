import os
import json
import datetime
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse

from os.path import isfile, join, dirname, realpath
from subprocess import Popen, PIPE


file_store_path = 'ocrimage.jpg';
file_path = '../ocrimage.jpg';

def handle_uploaded_file(f):
    destination = open(file_store_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def index(request):
    number_plate = None
    mypath = dirname(realpath(__file__))
    
    if request.method == 'POST':
        
        x = request.FILES['file']
        handle_uploaded_file(x)
        
        ocr_service_cmd = str("alpr -c eu -n 1 '%s' -j" % join(mypath, file_path))
        processed_ocr_info = Popen(ocr_service_cmd, shell=True, stdout=PIPE).stdout.read()
        response = json.loads(processed_ocr_info) 
        
        if bool(response['results']):
            number_plate = response['results'][0]['plate']
        else:
            ocr_service_cmd = str("alpr -c us -n 1 '%s' -j" % join(mypath,file_path))
            processed_ocr_info = Popen(ocr_service_cmd, shell=True, stdout=PIPE).stdout.read()
            response = json.loads(processed_ocr_info) 
            
            if bool(response['results']):
                number_plate = response['results'][0]['plate']
            
    return HttpResponse(number_plate)
    
