from django.shortcuts import render, redirect
from django.contrib import messages
from arrow.models import Landing, Drop, Skydive
from .calculate_angle import vincenty_angle, angle_using_distance

# Create your views here.

from django.http import HttpResponse,JsonResponse


def index(request):
    return render(request, 'landing_site.html', {})

def landing(request):
    if request.method == 'POST':
        
        lat = request.POST['latitude']
        lng = request.POST['longitude']
        
        obj = Landing.objects.all()[0]
        obj.latt = lat
        obj.long = lng
        
        obj.save()

        context = {
            'latt' : lat,
            'long' : lng
        }
        
        return render(request, 'drop_location.html', context)
    
    elif request.method == 'GET':
        
        if request.GET.get('latitude'):
        
            lat = request.GET.get('latitude')
            lng = request.GET.get('longitude')
            
            obj = Landing.objects.all()[0]
            obj.latt = lat
            obj.long = lng
            
            obj.save()
        
            return render(request, 'drop_location.html')
        
        else:
            
            obj = Landing.objects.all()[0]


            context = {
                'latt' : obj.latt,
                'long' : obj.long
            }
            
            return render(request, 'drop_location.html', context)
        
def drop(request):
    if request.method == 'POST':
        
        drop_lat = request.POST['latitude']
        drop_lng = request.POST['longitude']
        
        obj = Drop.objects.all()[0]
        obj.latt = drop_lat
        obj.long = drop_lng
        obj.save()
        
        obj = Landing.objects.all()[0]

        context = {
            'drop_latt' : drop_lat,
            'drop_long' : drop_lng,
            'land_latt': obj.latt,
            'land_long': obj.long,
            
        }
        
        return render(request, 'direction.html', context)
    
    elif request.method == 'GET':
        
        if request.GET.get('latitude'):
        
            lat = request.GET.get('latitude')
            lng = request.GET.get('longitude')
            
            obj = Drop.objects.all()[0]
            obj.latt = lat
            obj.long = lng
            
            obj.save()
        
            return render(request, 'direction.html')
        
        else:
            
            obj_drop = Drop.objects.all()[0]
            obj_land = Landing.objects.all()[0]

            context = {
                'drop_latt' : obj_drop.latt,
                'drop_long' : obj_drop.long,
                'land_latt': obj_land.latt,
                'land_long': obj_land.long,
                
            }
            
            return render(request, 'direction.html', context)
        
def skydive_path(request):    
    
    if request.method == 'GET':
    
        if request.GET.get('latitude'):
            
                current_lat = request.GET.get('latitude')
                current_lng = request.GET.get('longitude')
                
                current = [current_lat, current_lng]
                
                obj = Skydive(latt= current_lat, long= current_lng) 
                obj.save()
                
                if len(Skydive.objects.all()) == 1:
                    return render(request, 'direction.html')
                
                else:
                    
                    prev= Skydive.objects.all().order_by('-id')[1]
                    
                    land = Landing.objects.all()[0]

                    angle = angle_using_distance(prev, current, land)
                    
                    print(angle)
                    
                    return JsonResponse({
                        "prev_latt": prev.latt,
                        "prev_long": prev.long,
                        "angle": angle,
                    })

            
def reset_path(request):
    
    Skydive.objects.all().delete()
    
    return redirect('drop')