from pygc import * # distance in meters
from shapely.geometry import Point
import numpy as np
import geopandas as gpd
import math

def vincenty_angle(prev:object, current:list, land:object):
    
    P1 = Point(float(land.latt), float(land.long))
    P2 = Point(float(current[0]),float(current[1]))
    interP = Point(float(prev.latt),float(prev.long))
    
    dx = P1.x-interP.x
    dy = P1.y-interP.y

    P2az = great_distance(start_latitude=P2.y, start_longitude=P2.x,    end_latitude=interP.y,end_longitude=interP.x)['reverse_azimuth']
    P1az = great_distance(start_latitude=P1.y, start_longitude=P1.x,    end_latitude=interP.y,end_longitude=interP.x)['reverse_azimuth']
    
    azimuth = P2az-P1az
    
    
    if dx>0 and dy>0 :
        return azimuth
    
    elif dx<0 and dy>0:
        return 180-azimuth
    
    elif dx<0 and dy<0:
        return 180+azimuth
    
    elif dx>0 and dy<0:
        return 360-azimuth
    
    
def angle_using_distance(prev:object, current:list, land:object):
    
    geom = [Point(xy) for xy in zip([float(current[0]),float(land.latt)], [float(current[1]),float(land.long)])]
    gdf = gpd.GeoDataFrame(geometry=geom, crs={'init':'epsg:4326'})
    gdf.to_crs(epsg=3310, inplace=True)
    
    l1 = gdf.distance(gdf.shift())
    l1 = l1.iloc[1].item()
    
    geom = [Point(xy) for xy in zip([float(prev.latt),float(current[0])], [float(prev.long),float(current[1])])]
    gdf = gpd.GeoDataFrame(geometry=geom, crs={'init':'epsg:4326'})
    gdf.to_crs(epsg=3310, inplace=True)
    
    l2 = gdf.distance(gdf.shift())
    l2 = l2.iloc[1].item()
    
    geom = [Point(xy) for xy in zip([float(land.latt),float(prev.latt)], [float(land.long),float(prev.long)])]
    gdf = gpd.GeoDataFrame(geometry=geom, crs={'init':'epsg:4326'})
    gdf.to_crs(epsg=3310, inplace=True)
    
    l3 = gdf.distance(gdf.shift())
    l3 = l3.iloc[1].item()
    
    
    frac = ((l2**2) + (l3**2) - (l1**2))/(2*l2*l3)
    
    result = math.acos(frac) * (180.0 / math.pi)
    
    return result
    
    
    
    


# if dx>0 & dy>0 : final azimith=azimuth
# if dx<0 & dy>0 : final azimuth=180-azimuth
# if dx<0 & dy<0: final azimuth=180+azimuth
# if dx>0 & dy<0 final azimuth=360-azimuth