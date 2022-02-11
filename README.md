# WebMap


## Description
This module creates an HTML map based on given loaction and year. The map shows the nearest locations where films were shot.
<br><br>
Libraries used in this module:
 + **argparse**
 + **csv**
 + **pandas**
 + **folium**
 + **geopy**
 + **functools**
## USAGE
[main.py](https://github.com/mchlgmnk03/WebMap/blob/main/main.py) is launched from command line.
```python
python3 main.py 2016 40.7410861 -73.9896297241625 new.txt
```
There are 4 postional arguments:
 + **year**(str)
 + **latitude**(float)
 + **longitude**(float)
 + **path to dataset**(str)
## Output
The program creates such [map](https://github.com/mchlgmnk03/WebMap/blob/main/FilmMap.html)
<br><br>
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/92575176/153588609-6e4cdbb0-a9ce-4226-8985-e3800908f76a.png">
<br><br>
The color of flags indicates how far the location of the scene is to your location. Green <img width="18" alt="image" src="https://user-images.githubusercontent.com/92575176/153589508-effbf27b-4994-42e2-8fd8-0e617497cd68.png">
: within 1500km; Yellow <img width="18" alt="image" src="https://user-images.githubusercontent.com/92575176/153589582-dc137080-2e0a-417f-9b0d-0ca56c1afe19.png">
: within 3000km; Red <img width="18" alt="image" src="https://user-images.githubusercontent.com/92575176/153589623-51104f65-64b3-4968-8f52-b71d1acb1640.png">
: even further.
## TOOLS:
 + **MiniMap**: is used to see your location on larger scale and move your position on the map <img width="100" align="center" alt="image" src="https://user-images.githubusercontent.com/92575176/153590891-ef09f25c-9eca-4ad9-a227-9b00e0f1ae7d.png">

 + **Zoom Toggler**: is used to change the scale of the map <img width="26" align="center" alt="image" src="https://user-images.githubusercontent.com/92575176/153590381-00c775d1-25f1-4c8e-a54e-e1160b785240.png">

 + **FullScreen Button**: is used to enter FullScreen mode <img width="26" align="center" alt="image" src="https://user-images.githubusercontent.com/92575176/153590767-7c93db58-234e-4d4a-9d20-406dc818571a.png">

 + **LayerControl Button**: is used to switch layers <img width="35" alt="image" align="center" src="https://user-images.githubusercontent.com/92575176/153590284-fc5e403d-2d88-462a-8bb8-07c567320a5c.png">
 
