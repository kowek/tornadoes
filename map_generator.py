import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import folium
import os
import webbrowser
dirpath = os.getcwd()
filepath = dirpath + "\\map.html"

trnd = pd.read_csv(dirpath +"\\tornadoes.csv", dtype=object)
trnd['BEGIN_DATE']= trnd['BEGIN_DATE'].apply(pd.to_datetime)
trnd['TOR_LENGTH']=trnd['TOR_LENGTH'].apply(pd.to_numeric)
ind = trnd['INJURIES_DIRECT'] = trnd['INJURIES_DIRECT'].apply(pd.to_numeric)
trnd['YEAR'] = trnd['BEGIN_DATE'].dt.year

for i in range(0,len(ind)):
    if ind.iloc[i] == 0:
        trnd.at[i, 'COLOR'] = 'grey'
    elif 0 < ind.iloc[i] < 5:
        trnd.at[i, 'COLOR'] = 'green'
    elif 5 <= ind.iloc[i] < 20:
        trnd.at[i, 'COLOR'] = 'yellow'
    elif 20 <= ind.iloc[i] < 90:
        trnd.at[i, 'COLOR']= 'orange'
    else:
        trnd.at[i, 'COLOR']= 'crimson'

endmap = folium.Map(location=[trnd['BEGIN_LAT'].apply(pd.to_numeric).mean(),trnd['BEGIN_LON'].apply(pd.to_numeric).mean()],
                    tiles='cartodbdark_matter', zoom_start = 5)
#38.2942989,-101.5782557
for y in range (2015,2020):
    trnd_sub = trnd[trnd.YEAR == y]
    fg=folium.FeatureGroup(name=str(y))
    for i in range(0,len(trnd_sub)):
        text = folium.Html('<b>'+str(trnd_sub.iloc[i]['BEGIN_DATE'].date())+
                           ', '+str(trnd_sub.iloc[i]['BEGIN_LOCATION'])+
                            '<br><br>Length: </b>'+str(trnd_sub.iloc[i]['TOR_LENGTH'])+
                            ' mi<br><b>Width: </b>'+str(trnd_sub.iloc[i]['TOR_WIDTH'])+
                            ' ft<br><b>Direct injuries: </b>'+str(trnd_sub.iloc[i]['INJURIES_DIRECT'])+
                           '<br><br>'+str(trnd_sub.iloc[i]['EVENT_NARRATIVE']).split("||")[0], script=True)
        popup = folium.Popup(text, max_width=300, min_width=100)
        fg.add_child(folium.Circle(
          location=[trnd_sub.iloc[i]['BEGIN_LAT'], trnd_sub.iloc[i]['BEGIN_LON']],
          radius=int(trnd_sub.iloc[i]['TOR_LENGTH'])*3000,
          popup=popup,
          color=trnd_sub.iloc[i]['COLOR'],
          weight=int(trnd_sub.iloc[i]['TOR_WIDTH'])/400,
          fill=True,
          fill_color=trnd_sub.iloc[i]['COLOR']))
    endmap.add_child(fg)

endmap.add_child(folium.LayerControl())

legend_html =   '''
                <div style="position: fixed; 
                            bottom: 1%; left: 1%; width: 280px; height: 360px; margin: 30px; padding: 8px;
                            border:3px solid grey; background-color: rgb(255,255,255,0.8); z-index:9999; font-size:13px;
                            text-align:justify;">
                            <h4><b><center>US TORNADOES 2015-2019</b></h4>
                            <p>
                            The map depicts 5 years of class 3 and higher tornadoes in US. 
                            You can select each year using a handle in the top right corner.
                            Click on the marker to read each tornado's history.
                            </p>
                            <p><u>Description:</u></p>
                            <p>The <b>bigger</b> the circle the <b>longer</b> the tornado</b></p>
                            <p>The <b>thicker</b> the circle the <b>wider</b> the tornado</b></p>
                            Colours represent direct injuries:
                            <ul>
                            <li><span style="color: grey">grey: </span>0</li>
                            <li><span style="color: green">green: </span>1 to 4</li>
                            <li><span style="color: yellow">yellow: </span>5 to 19</li>
                            <li><span style="color: orange">orange: </span>20 to 89</li>
                            <li><span style="color: crimson">crimson: </span>90 and more</li>
                            </ul>
                </div>
                '''

endmap.get_root().html.add_child(folium.Element(legend_html))

endmap.save(filepath)
webbrowser.open('file://' + filepath)
