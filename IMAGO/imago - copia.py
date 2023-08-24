import webbrowser
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, Qgis, QgsFeatureRequest, QgsGeometry
from qgis.utils import iface
from qgis.gui import QgsMapTool

class SelectFeatureTool(QgsMapTool):
    def __init__(self, iface, plugin_instance):
        super().__init__(iface.mapCanvas())
        self.iface = iface
        self.plugin_instance = plugin_instance

    def distance_to_line(self, point, line_geom):
        point = QgsGeometry.fromPointXY(point)
        return point.distance(line_geom)

    def canvasReleaseEvent(self, event):
        selected_layer = self.iface.activeLayer()
        if selected_layer:
            try:
                map_point = self.toMapCoordinates(event.pos())
                distance_threshold = 0.1001  # Ajusta este valor según la escala de tu mapa

                features = selected_layer.getFeatures(QgsFeatureRequest())
                for feature in features:
                    geom = feature.geometry()
                    distance = self.distance_to_line(map_point, geom)
                    if distance < distance_threshold:
                        self.plugin_instance.openLink(feature)
                        break
            except Exception as e:
                self.iface.messageBar().pushMessage("Error", f"An error occurred: {str(e)}", level=Qgis.Warning)

class IMAGO:
    def __init__(self, iface):
        self.iface = iface
        self.select_tool = SelectFeatureTool(self.iface, self)  # Inicializa la herramienta de selección

    def initGui(self):
        # Crea una QAction con un icono o logotipo
        icon_path = 'C:/Users/josevazquez/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/IMAGO/icon.png'
        self.select_action = QAction(QIcon(icon_path), "Abrir enlace de capa seleccionada", self.iface.mainWindow())
        self.select_action.triggered.connect(self.activateSelectTool)
        self.iface.addToolBarIcon(self.select_action)

    def unload(self):
        self.iface.removeToolBarIcon(self.select_action)

    def openLink(self, feature):
        try:
            link_field = "Link"  # Nombre del campo de enlace
            link = feature[link_field]
            if link:
                webbrowser.open(link)
            else:
                self.iface.messageBar().pushMessage("Error", "No se encontró un enlace en el atributo seleccionado", level=Qgis.Warning)
        except Exception as e:
            self.iface.messageBar().pushMessage("Error", f"An error occurred: {str(e)}", level=Qgis.Warning)

    def activateSelectTool(self):
        self.iface.mapCanvas().setMapTool(self.select_tool)

def classFactory(iface):
    return IMAGO(iface)
