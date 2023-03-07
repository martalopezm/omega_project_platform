# omega_project_platform
Simple script behind OMEGA platform, for displaying HDF5 results in a map and sections

This python script has been programmed for OMEGA project, which aim is to provide water quality real-time, and forecast, status of two portuguese reservoirs (albufeira de Montargil and albufeira de Maranhão). In this, MOHID Water Modelling System will provide daily results of several properties (as temperature, nitrate or dissolved oxygen). This scripts will serve as intermediate between OMEGA platform users and model results. http://omega.maretec.org/

The user will be able to choose in the platform:
 - DATE
 - PROPERTY to display
 - TYPE OF VISUALIZATION (surface map or zonal/meridional reservoir transects). In case of transect, an user input longitude or latitude will be required. 

This selection will be stored in an input.dat file, which this script will open and read. Regarding user's selection, the script will search the corresponding hdf5 (internal script path) and display the graph.

Quick summary of the script: 
- Read user info
- Search and open the hdf5 file
- Extract coordinates and set units
- Surface map: make a map of the property projected into a google map layer (folium package) and display as a html
- Sections: select the transect and show only rows and columns with values, or at least one value (include only nan rows and columns which are between first and last no-nan value).

HOW TO RUN AN EXAMPLE?
- Place omega_input.dat file in the same path of the scrip (SCRIPT_bien_mlm.py)
- Install required python packages
- Change inside the script the path in line 62 where you will place the WaterProperties.hdf5 file. In addition choose whatever path you want in line 280 

SURFACE MAP: 
![image](https://user-images.githubusercontent.com/60937576/114426441-fd880a80-9bb1-11eb-908d-daa3f3bf8adf.png)



MERIDIONAL SECTION (with contour lines)
![maranhão_meridional](https://user-images.githubusercontent.com/60937576/114425251-ccf3a100-9bb0-11eb-849e-141556df3a82.png)



MERIDIONAL SECTION (without contour lines)
![Trasencto_meridional](https://user-images.githubusercontent.com/60937576/114426577-1e506000-9bb2-11eb-975c-1f15b8bb0284.png)



ZONAL SECTION (changing property to display to oxygen)
![Transectozonal](https://user-images.githubusercontent.com/60937576/114426704-3d4ef200-9bb2-11eb-83b7-96abdbeef9fe.png)


