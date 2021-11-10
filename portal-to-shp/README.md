This is an example of a custom tool I made with ArcGIS Model Builder. See model below:

![image](https://user-images.githubusercontent.com/69057057/141152703-6ccc7f20-0a60-4945-ad7e-8272ed385f38.png)

<strong>Background: </strong>Our field crews collect data with Field Maps and an Eos GNSS receiver, which collects all elevations in meters. 
This data is collected to our Enterprise Portal and housed in an SDE database. For delivery to clients, or use internally by other GIS or CAD techs, we 
extract portions of that data and adjust the z values of the points from meters to feet (which is what our engineers require). We will both calculate an elevation in feet field
and adjust the intrinsic Z value of the point.
<br><br>
The tool does the following:
<br>
<ol>
  <li> Exports a shapefile of selected data (we choose shapefiles as our cad conversion software requires it. </li>
  <li> Adds XYZ coordinate information to the attribute table of the shapefile (we will need this to do our calculations).</li>
  <li> Adds a new field and calculates elevation in feet from the Z value. </li>
  <li> Adjusts the Z geometry value to feet and re-adds the XYZ information to the attribute table. </li>
