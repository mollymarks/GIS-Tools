import datetime
import numpy as np
import pandas as pd
from arcgis.gis import GIS
from arcgis.features import FeatureCollection
gis = GIS("home")

#search for the feature layer/service
featureLayer_item = gis.content.search('type: "Feature Service" AND title:"Sanitary Septic Tank"')

#access the item's feature layers
feature_layers = featureLayer_item[0].layers
flayer = feature_layers[0]

#query all the features and get the spatial dataframe
fset = feature_layers[0].query()
flayer_rows = fset.sdf

#logic to update attributes
today = datetime.datetime.today()

for index, row in flayer_rows.iterrows():
    pumpDate = row['LastPumpDate']
    checkDate = row['LastCheckDate']
    
    
    if pd.isnull(pumpDate):
        TSP = -999999
    else:
        TSP = (today-pumpDate).total_seconds()/2628000
        
 
        
    TSC = (today-checkDate).total_seconds()/2628000
    active = row['Active']
    freq = row['CheckFrequency']
    check = row['LastCheckStatus']
    
    if active == 'No':
        fset.features[index].attributes['Status'] = 'Not Active'
    
    elif active == "Yes" and freq == "Every Three Years":
        if (TSP>36.0) or (TSP==-999999):
            fset.features[index].attributes['Status'] = 'Needs to be Pumped'
        elif TSP<36.0:
            fset.features[index].attributes['Status'] = 'Pumping Complete'
        else:
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
            
    elif active =="Yes" and freq == "Every Two Years":
        if TSP>36.0:
            fset.features[index].attributes['Status'] = 'Needs to be Pumped' 
        elif (TSP<36.0 and TSC>24) or (TSP==-999999 and TSC>24):
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
        elif ((TSP<36.0 and TSC<24 and check == "Pump Needed") or (TSP==-999999 and TSC<24 and check == "Pump Needed")):
            fset.features[index].attributes['Status'] = 'Checked - Needs Pump'
        elif (TSP<36.0 and TSC<24 and check == "No Pump Needed") or (TSP==-999999 and TSC<24 and check == "No Pump Needed"):
            fset.features[index].attributes['Status'] = 'Checked - Pump Not Needed'
        elif (TSP<36.0 and TSC<24 and check == "N/A") or (TSP==-999999 and TSC<24 and check == "N/A"):
            fset.features[index].attributes['Status'] = 'Pumping Complete'
        else:
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
            
    elif active =="Yes" and freq == "Every Year":
        if TSP>36.0:
            fset.features[index].attributes['Status'] = 'Needs to be Pumped'
        elif (TSP<36.0 and TSC>12) or (TSP==-999999 and TSC>12):
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
        elif (TSP<36.0 and TSC<12 and check == "Pump Needed") or (TSP==-999999 and TSC<12 and check == "Pump Needed"):
            fset.features[index].attributes['Status'] = 'Checked - Needs Pump'
        elif (TSP<36.0 and TSC<12 and check == "No Pump Needed") or (TSP==-999999 and TSC<12 and check == "No Pump Needed"):
            fset.features[index].attributes['Status'] = 'Checked - Pump Not Needed'
        elif (TSP<36.0 and TSC<12 and check == "N/A") or (TSP==-999999 and TSC<12 and check == "N/A"):
            fset.features[index].attributes['Status'] = 'Pumping Complete'
        else:
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
            
    elif active =="Yes" and freq == "Twice Per Year":
        if TSP>36.0:
            fset.features[index].attributes['Status'] = 'Needs to be Pumped'
        elif (TSP<36.0 and TSC>6) or (TSP==-999999 and TSC>6):
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
        elif (TSP<36.0 and TSC<6 and check == "Pump Needed") or (TSP==-999999 and TSC<6 and check == "Pump Needed"):
            fset.features[index].attributes['Status'] = 'Checked - Needs Pump'
        elif (TSP<36.0 and TSC<6 and check == "No Pump Needed") or (TSP==-999999 and TSC<6 and check == "No Pump Needed"):
            fset.features[index].attributes['Status'] = 'Checked - Pump Not Needed'
        elif (TSP<36.0 and TSC<6 and check == "N/A") or (TSP==-999999 and TSC<6 and check == "N/A"):
            fset.features[index].attributes['Status'] = 'Pumping Complete'
        else:
            fset.features[index].attributes['Status'] = 'Needs to be Checked'
            
#convert fset to fcollection
fColl = FeatureCollection.from_featureset(fset)

#append fCollection, using upsert to update existing features, not append new ones
flayer.append(

  upload_format = 'featureCollection', 
  edits = fColl.properties, 
  skip_updates = False, 
  skip_inserts = True, 
  update_geometry=False, 
  upsert_matching_field = 'GlobalID'

  )
