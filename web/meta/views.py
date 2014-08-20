from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.core import serializers
import meta.models
import tasks

def index(request):
    return render(request, 'meta/html/index.html')

def imageIngest(request):
    return render(request, 'meta/html/imageIngest.html')

def tiePointCreator(request):
    return render(request, 'meta/html/tiePointCreator.html')

def voxelCreator(request):
    return render(request, 'meta/html/voxelCreator.html')

def voxelWorldViewer(request):
    return render(request, 'meta/html/voxelWorldViewer.html')

#
# API for grabbing data in the database
#
def fetchVideoList(request):
    imgs = meta.models.ImageCollection.objects.all()
    return HttpResponse( serializers.serialize('geojson', imgs) , content_type="application/json")

def fetchImages(request):
    print("Requested images for video collection id ", request.REQUEST["videoId"])
    videoId = request.REQUEST["videoId"]
    video = meta.models.ImageCollection.objects.get(id=videoId)
#    return HttpResponse( serializers.serialize('geojson', video.images.all(), fields=('name',)), 
#                         content_type="application/json")
    return HttpResponse( serializers.serialize('geojson', video.images.all()), 
                         content_type="application/json")
    #based off of video_list_example.ipynb
    
def fetchControlPointList(request):    
    geoPoints = meta.models.ControlPoint.objects.all()    
    return HttpResponse( serializers.serialize('geojson', geoPoints) , content_type="application/json")
  
def fetchTiePoints(request):    
    print("Requested tie points for image id ", request.REQUEST["imageId"])
    imageId = request.REQUEST["imageId"]
    tiePoints = meta.models.TiePoint.objects.filter(image_id=imageId)
    serializers.serialize('geojson', tiePoints, fields=('name', 'point', 'geoPoint'))
    return HttpResponse( serializers.serialize('geojson', tiePoints, fields=('name', 'point', 'geoPoint')) , content_type="application/json")
     
#  API for updating data in the database
def createTiePoint(request):
    imageId = request.REQUEST["imageId"];
    if 'controlPointId' in request.REQUEST:
      controlPointId = request.REQUEST["controlPointId"];
    else:
      controlPointId = None;
    x = request.REQUEST["x"];
    y = request.REQUEST["y"];
    tasks.addTiePoint.apply(kwargs={'point':'POINT(%s %s)' % (x,y), 
                               'image_id':imageId, 
                               'geoPoint_id':controlPointId,
                               'name':'User Generated by Web UI'});
    return HttpResponse('');

def updateTiePoint(request):
    print("Requested to update a tie point with id ", request.REQUEST["tiePointId"],           
          " with x=", request.REQUEST["x"], " and y=", request.REQUEST["y"])    

    tasks.updateTiePoint.apply(args=(request.REQUEST["tiePointId"], request.REQUEST["x"], request.REQUEST["y"]))
    #Eventually when the REAL update function is written, it may be EASIEST to say
    #"POINT(%s %s)" % (x, y), but until this is complete, it does not matter to me.
          
    return HttpResponse('');