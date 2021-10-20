
import sys
import io
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtWidgets

"""
Folium in PyQt5
"""


''''''

class googleMaps(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (55.68379619892188, 12.571606455699344)
        m = folium.Map(tiles='OpenStreetMap', zoom_start=14, location=coordinate)


        # Virta charging stations
        folium.Marker([55.6838445898742, 12.583314340269386], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.682843024903356, 12.581981919550408], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67859794248827, 12.561335623193628], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67859794248827, 12.561335623193628], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67859794248827, 12.561335623193628], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68515841593509, 12.556147066838536], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.66928203191013, 12.571081602915246], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.66928203191013, 12.571081602915246], popup="Virta", icon=folium.Icon(color='orange', icon="car", prefix='fa')).add_to(m)

        #Tesla
        folium.Marker([55.68544624096336, 12.564730132042083], popup="Tesla", icon=folium.Icon(color='red', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68588171106987, 12.564901793417032], popup="Tesla", icon=folium.Icon(color='red', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.681427519032525, 12.571939906095839], popup="Tesla", icon=folium.Icon(color='red', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68549213577168, 12.565073451097822], popup="Tesla", icon=folium.Icon(color='red', icon="car", prefix='fa')).add_to(m)

        # Clever A/S
        folium.Marker([55.69119625977196, 12.571510745149984], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.685632310882, 12.558979464778604], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68316456708772, 12.56601758115157], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68122897279602, 12.5676483642136], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67716391296998, 12.56224103090266], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67716391296998, 12.56224103090266], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67716391296998, 12.56224103090266], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67513122462981, 12.570824099650181], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67319523277522, 12.573570681649388], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67256601479463, 12.57048077690028], popup="Clever", icon=folium.Icon(color='green', icon="car", prefix='fa')).add_to(m)

        #E.ON
        folium.Marker([55.69270593357997, 12.560610262587245], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.68012592804444, 12.572969881733883], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.672237168273924, 12.578033892294918], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67997825916832, 12.573399031477077], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.686413945725754, 12.58653112666078], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.69013938548993, 12.573399031477077], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.69284857329237, 12.560610259043273], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)
        folium.Marker([55.67237988270961, 12.577776396538312], popup="E.ON", icon=folium.Icon(color='darkblue', icon="car", prefix='fa')).add_to(m)



        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)



app = QApplication(sys.argv)
x=googleMaps()
widget = QtWidgets.QStackedWidget()
widget.addWidget(x)
widget.setFixedWidth(500)
widget.setFixedHeight(800)
widget.show()
app.exec()


