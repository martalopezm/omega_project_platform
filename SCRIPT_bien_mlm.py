# -*- coding: utf-8 -*-

"""
Created on Fri Feb 19 11:01:25 2021
Input data: date (YY,MM,DD)
            type of section (map, zonal, meridional) (map, zonaltransect, meridionaltransect)
            if section != map, latitude and longitud input is required (transects)
            property to display
@author: marta.lopez.mozos, martalopezm@tecnico.ulisboa.pt
"""

#pip install GEOS, Cython, Shapely, pyshp, six
# if problems with cartopy: conda install -c conda-forge cartopy
# if problems with mpl_toolkits..: conda install basemap

import h5py
import numpy as np

#############################################################
#                 Read user information                     
#############################################################

input_file = 'omega_input.dat'

fin = open(input_file)
print('Reading input from file...')
for lin in fin:    
    aux_line = lin.split(':',1)
    keyword = aux_line[0]    
    
    if keyword == 'DATE':            
       date = aux_line[1].replace('\n','')   
       date = date.replace(" ", "")       
       print('Date = ', date)
       
    elif keyword == 'SECTION': 
       section = aux_line[1].replace('\n','')        
       section = section.replace(" ", "")              
       print('Section =', section) 
       
    elif keyword == 'PROPERTY': 
       propert = aux_line[1].replace('\n', '')  
       propert = propert.replace(" ", "") 
       print('Property =', propert)  
       
    elif keyword == 'LATITUDE':
       input_lat = aux_line[1].replace('\n', '')  
       input_lat = float(input_lat.replace(" ", ""))
       print('Latitude input =', input_lat) 
       
    elif keyword == 'LONGITUDE':
       input_lon = aux_line[1].replace('\n', '')  
       input_lon= float(input_lon.replace(" ", ""))
       print('longitude input =', input_lon)    
       
fin.close()  


#############################################################
#           Search and open hdf5 file in PC 
#############################################################
filename = '//ML22/Ricardo/MARANHAO/Results/HDF/' + date + '/WaterProperties_1.hdf5'
#filename = '//ML22/Ricardo/FUNCIONA/MONTARGIL_2019/Results/HDF/' + date + '/WaterProperties_1.hdf5'
f = h5py.File(filename, 'r')
print('File opened successfully...')

#############################################################
#           Extract location and set units
#############################################################

lat = f['Grid']['Latitude'][0,:]
lat = lat[:-1]    
lon = f['Grid']['Longitude'][:,0]
lon = lon[:-1] 

   
if propert == 'temperature':
     units = '(°C)'
elif propert == 'oxygen':
     units = '(mgO2/L)'   
elif (propert == 'ammonia') or (propert == 'nitrate') or \
     (propert == 'nitrite') or (propert == 'particulateorganicnitrogen'):
     units = '(mgN/L)'
elif (propert == 'phytoplankton') or (propert == 'zooplankton'):  
     units = '(mgC/L)'   
elif (propert == 'inorganicphosphorus') or (propert == 'particulateorganicphosphorus'):
     units = '(mgP/L)'


############################################################
#             Surface map or section          
#############################################################


if section == 'map' : #surface map

   prop_surf_values = f['Results'][propert][propert + '_00001'][:,:,:]
   toplayer, lon_dim, lat_dim = prop_surf_values.shape
   toplayer = toplayer - 1 #index wherein first layer is
   prop_surf_values = f['Results'][propert][propert + '_00001'][toplayer,:,:]
   central_lat = np.mean(lat)
   central_lon = np.mean(lon)  
     
   for i in range(prop_surf_values.shape[0]):
    for j in range(prop_surf_values.shape[1]):
        
        if prop_surf_values[i,j] < -10000:  #land mask values
           prop_surf_values[i,j] = np.nan   
   
   import folium
   from folium import plugins
   import matplotlib.pyplot as plt
   import webbrowser
   import geojsoncontour    
   import branca
   
   x, y  = np.meshgrid(lon, lat)   
   levels = np.linspace(np.nanmin(prop_surf_values), 0.01 + np.nanmax(prop_surf_values))
   geomap1= folium.Map(location=[central_lat, central_lon], zoom_start=12, tiles="Stamen Terrain")
   m2 = plt.contourf(x,y,np.transpose(prop_surf_values), cmap = 'jet', levels=levels, alpha = 1) 
    
   geojson = geojsoncontour.contourf_to_geojson(
             contourf=m2,
             min_angle_deg=3.0,
             ndigits=10,            
             stroke_width=0.1,
             fill_opacity = 1)  
   
     
   # Plot the contour on Folium map. Several times due to colors saturation... 
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],
                                  #'fill_opacity':  x['properties']['fill-opacity'],
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)
   
   
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                               
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)
      
      
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],
                                  #'fill_opacity':  x['properties']['fill-opacity'],
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)
   
   
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],
                                  #'fill_opacity':  x['properties']['fill-opacity'],
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)
   
   
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                                 
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)
   
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                                 
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)

   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': 0.1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                                 
                                  'opacity': 1,
                                  'fill_opacity': 1
                  }).add_to(geomap1)   
   
   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': -1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                                 
                                  'opacity': 0,
                                  'fill_opacity': 1
                  }).add_to(geomap1)

   folium.GeoJson(geojson,
                  overlay=True,  
                  control = True, 
                  show = True,
                  name = propert,
                  style_function=lambda x: {
                                  'color':         x['properties']['stroke'],
                                  'weight':         x['properties']['stroke-width'],
                                  'stroke_opacity': -1, #x['properties']['stroke-opacity'],
                                  'fillColor':     x['properties']['fill'],                                 
                                  'opacity':-1,
                                  'fill_opacity': -11
                  }).add_to(geomap1)      
   
   
   
   # Add plugins. Fullscreen button, coordinates...
   plugins.Fullscreen(position='topright', force_separate_button=True).add_to(geomap1)
   plugins.MousePosition().add_to(geomap1)
   
   
   # Add the legend to the map  
   listacolores = ['blue', 'cyan', 'yellow', 'red']
   cm = branca.colormap.LinearColormap(listacolores, vmin = np.nanmin(prop_surf_values), 
                                       vmax=  np.nanmax(prop_surf_values)).to_step(len(levels))   
   cm.caption = 'Surface ' + propert + ' ' + units
   geomap1.add_child(cm)


   #Save and plot
   filepath = 'C:/Users/administrator/Desktop/mapita.html'
   geomap1.save(filepath)   
   webbrowser.open('file://' + filepath)   
   print('Surface map done..')
   
      

   
elif section == 'zonal':
    
    import pandas as pd  
    import matplotlib.pyplot as plt
    
    #Idx of the closest latitude to user's input latitude
    idx_lat = (np.abs(lat - input_lat)).argmin()
    #Extract the property and depth zonal transect, and flip them to put upper layer as first row
    prop_lattransect_values = np.flipud(f['Results'][propert][propert + '_00001'][:,:,idx_lat])
    depth = np.flipud(f['Grid']['VerticalZ']['Vertical_00001'][:,:,idx_lat])    
    #Replace land values to NaN 
    for i in range(prop_lattransect_values.shape[0]):
     for j in range(prop_lattransect_values.shape[1]):        
        if prop_lattransect_values[i,j] < -10000:  #land mask values
           prop_lattransect_values[i,j] = np.nan            
    #Convert property matrix into dataFrame        
    prop_lattransect_values_df = pd.DataFrame(prop_lattransect_values)    
    #Delete columns and rows wherein all values are NaN
    prop_lattransect_values_df = prop_lattransect_values_df.dropna(axis = 1, how='all')
    prop_lattransect_values_df = prop_lattransect_values_df.dropna(axis = 0, how='all') 
    #Find indexes wherein depth and longitude have the first and last values 
    indices_lon = prop_lattransect_values_df.columns
    indices_depth = prop_lattransect_values_df.index
    #Store longitudes and depths, including only nan rows and columns which are between first and last no-Nan value
    lon_transect = lon[indices_lon.min():indices_lon.max()]  
    depth_transect = depth[indices_depth.min():(indices_depth.max()+1), indices_lon.min():indices_lon.max()]    
    #Replace land values to NaN in new depth array
    for i in range(depth_transect.shape[0]):
     for j in range(depth_transect.shape[1]):        
        if depth_transect[i,j] < -10000:  #land mask values
           depth_transect[i,j] = np.nan 
    #Store the property array including only cells with values, or NaN rows/columns if they contain values, or are inside first and last value
    prop_lattransect_values = prop_lattransect_values[indices_depth.min():(indices_depth.max()+1), indices_lon.min():indices_lon.max()]
    
    #Generate a matrix with each depth, longitude, and property value      
    matriz = np.zeros((len(lon_transect)*(prop_lattransect_values.shape[0]), 3)) 
    k = 0  
    for i in range(prop_lattransect_values.shape[0]):
      for j in range(len(lon_transect)):   
            matriz[k, 0] = -depth_transect[i,j]  #with a minus to convert values into real depth values
            matriz[k, 1] = lon[j]
            matriz[k, 2] = prop_lattransect_values[i,j]
            k = k + 1
    
    #Grid the data. 
    numcols, numrows = len(lon_transect), prop_lattransect_values.shape[0]
    xi = np.linspace(np.nanmin(matriz[:,1]),np.nanmax(matriz[:,1]), numcols) #longitudes
    yi = np.linspace(np.nanmin(matriz[:,0]),np.nanmax(matriz[:,0]), numrows) #depth
    xi, yi = np.meshgrid(xi, yi)

    #Plot the results 
    plt.figure(figsize=(15,10)) 
    levels = np.linspace(np.nanmin(prop_lattransect_values), 0.01 + np.nanmax(prop_lattransect_values))
    plt.gca().patch.set_color('.25') #plot background grey (as land)
    im = plt.contourf(xi, np.flipud(yi), prop_lattransect_values, len(levels), cmap = 'jet')
    plt.ylabel('Depth (m)')
    plt.xlabel('Longitude')
    plt.title(label = ('Zonal section'), fontsize = 15) #, fontweight='bold')
    cbar = plt.colorbar(im, format='%.1f') 
    cbar.set_label(propert + ' ' + units, family = 'times new roman', style='italic', 
                  size = 22, rotation=-90, labelpad=40 )   
    #line_colors = ['black' for l in im.levels]
    #im2 = plt.contour(xi, np.flipud(yi), prop_lattransect_values, levels=10, colors=line_colors) #add black contour lines
    #plt.clabel(im2, inline=True, fontsize=10, fmt = '%2.1f')
    
    #Save plot
    plt.savefig('Transectozonal.jpeg', format='png', dpi=1200)     
    print('Zonal transect figure done..')

elif section == 'meridional':
    
    import pandas as pd
    import matplotlib.pyplot as plt
    
    idx_lon = (np.abs(lon - input_lon)).argmin()
    prop_lontransect_values = np.flipud(f['Results'][propert][propert + '_00001'][:,idx_lon,:])
    depth = np.flipud(f['Grid']['VerticalZ']['Vertical_00001'][:,idx_lon,:])   
    for i in range(prop_lontransect_values.shape[0]):
     for j in range(prop_lontransect_values.shape[1]):
        
        if prop_lontransect_values[i,j] < -10000:  #land mask values
           prop_lontransect_values[i,j] = np.nan 
           
          
    prop_lontransect_values_df = pd.DataFrame(prop_lontransect_values)     
    prop_lontransect_values_df = prop_lontransect_values_df.dropna(axis = 1, how='all')
    prop_lontransect_values_df = prop_lontransect_values_df.dropna(axis = 0, how='all')    
    indices_lat = prop_lontransect_values_df.columns
    indices_depth = prop_lontransect_values_df.index   
    lat_transect = lat[indices_lat.min():indices_lat.max()]  
    depth_transect = depth[indices_depth.min():(indices_depth.max()+1), indices_lat.min():indices_lat.max()]   

    for i in range(depth_transect.shape[0]):
     for j in range(depth_transect.shape[1]):        
        if depth_transect[i,j] < -10000:  
           depth_transect[i,j] = np.nan     
    prop_lontransect_values = prop_lontransect_values[indices_depth.min():(indices_depth.max()+1), indices_lat.min():indices_lat.max()]
    
    #Generate a matrix with each depth, longitude, and property value      
    matriz = np.zeros((len(lat_transect)*(prop_lontransect_values.shape[0]), 3)) 
    k = 0  
    for i in range(prop_lontransect_values.shape[0]):
      for j in range(len(lat_transect)):   
            matriz[k, 0] = -depth_transect[i,j]  #with a minus to convert values into real depth values
            matriz[k, 1] = lat[j]
            matriz[k, 2] = prop_lontransect_values[i,j]
            k = k + 1
    
    #Grid the data
    numcols, numrows = len(lat_transect), prop_lontransect_values.shape[0]
    xi = np.linspace(np.nanmin(matriz[:,1]),np.nanmax(matriz[:,1]), numcols) #longitudes
    yi = np.linspace(np.nanmin(matriz[:,0]),np.nanmax(matriz[:,0]), numrows) #depth
    xi, yi = np.meshgrid(xi, yi)

    #Plot the results 
    plt.figure(figsize=(15,10)) 
    levels = np.linspace(np.nanmin(prop_lontransect_values), 0.01 + np.nanmax(prop_lontransect_values))
    plt.gca().patch.set_color('.25')
    im = plt.contourf(xi, np.flipud(yi), prop_lontransect_values, len(levels), cmap = 'jet')
    plt.ylabel('Depth (m)')
    plt.xlabel('Latitude')
    plt.title(label = ('Meridional section'), fontsize = 15) #, fontweight='bold')
    cbar = plt.colorbar(im, format='%.1f') 
    cbar.set_label(propert + ' ' + units, family = 'times new roman', style='italic', 
                  size = 22, rotation=-90, labelpad=40 )   
    #line_colors = ['black' for l in im.levels]
    #im2 = plt.contour(xi, np.flipud(yi), prop_lontransect_values, levels=10, colors=line_colors)
    #plt.clabel(im2, inline=True, fontsize=10, fmt = '%2.1f')    
    #Save plot
    plt.savefig('Trasencto_meridional.jpeg', format='png', dpi=1200) 
    print('Meridional transect done.')

