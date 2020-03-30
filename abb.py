import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import folium
import os
import webbrowser
dirpath = os.getcwd()
filepath = dirpath + "\\index.html"

abb_total = pd.read_csv(dirpath +"\\final_total.csv")
abb = abb_total[(abb_total['room_type']=='Entire home/apt') | (abb_total['room_type']=='Hotel room')].copy()

# grouped = trnd.groupby(['TOR_F_SCALE','SOURCE'])
# df = pd.DataFrame(columns=['bins','count','scenario'])
#
# for group in grouped:
#     a = int(group[1]['TOR_LENGTH'].max()) - int(group[1]['TOR_LENGTH'].max()) % 5 + 10
#     bins = range(0, a, 5)
#     count, edges = np.histogram(group[1]['TOR_LENGTH'], bins=bins)
#     c = pd.Series(count, name='count')
#     e = pd.Series(edges[1:], name = 'bins')
#     dfex = pd.concat([e,c], axis=1)
#     dfex['scenario'] = str(group[0])
#     df = df.append(dfex)
# print(df)





endmap = folium.Map(location=[abb['longitude'].mean(),abb['latitude'].mean()], tiles='cartodbdark_matter', zoom_start = 5)


layers = ["av_mar19", "av_Feb2020", "av_mar20"]
descriptions = {0: "Month before Easter 2020",
                1: "2 months before Easter 2020",
                2:  "1.5 month before Easter 2019"}

for y in range (0,3):
    fg=folium.FeatureGroup(name=descriptions.get(y))
    for i in range(0,len(abb)):
        if abb[layers[y]].iloc[i] == 'f':
            abb.at[i, 'COLOR'] = 'grey'
        else:
            abb.at[i, 'COLOR'] = 'green'
        text = folium.Html('<b>Room type: </b>'+str(abb.iloc[i]['room_type'])+
                            '<br><b>Price: </b>'+str(abb.iloc[i]['price'])+
                            '<br><b>Neighbourhood: </b>'+str(abb.iloc[i]['neighbourhood'])+
                           '<br>', script=True)
        popup = folium.Popup(text, max_width=300, min_width=100)
        fg.add_child(folium.Circle(
          location=[abb.iloc[i]['latitude'], abb.iloc[i]['longitude']],
          radius=100,
          popup=popup,
          color=abb.iloc[i]['COLOR'],
          fill=True,
          fill_color=abb.iloc[i]['COLOR']))
    endmap.add_child(fg)

endmap.add_child(folium.LayerControl())

legend_html =   '''
                <div style="position: fixed; 
                            bottom: -5px; left: -18px; width: 280px; height: 360px; margin: 30px; padding: 8px;
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
