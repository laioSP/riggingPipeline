from PySide2 import QtCore, QtGui, QtWidgets

class MangoItem(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QtCore.QRectF(-100, -150, 200, 300)

    def paint(self, painter, option, widget):
        self.drawMango(painter)

    def drawMango(self, painter):
        # Define mango body shape
        mangoPath = QtGui.QPainterPath()
        mangoPath.addEllipse(QtCore.QRectF(-100, -150, 200, 300))

        # Set up mango gradient
        mangoGradient = QtGui.QLinearGradient(mangoPath.boundingRect().topRight(),
                                            mangoPath.boundingRect().bottomLeft())
        mangoGradient.setColorAt(0, QtGui.QColor(255, 255, 0))  # yellow
        mangoGradient.setColorAt(1, QtGui.QColor(255, 105, 200))  # pink 

        # Create a painter path for the mango with the gradient as its fill
        filledMangoPath = QtGui.QPainterPath()
        filledMangoPath.addEllipse(QtCore.QRectF(-100, -150, 200, 300))
        filledMangoPath.addPath(mangoPath)
        filledMangoPath.setFillRule(QtCore.Qt.WindingFill)

        # Move the filled mango path and the text together
        painter.translate(200, 200)  # Adjust the translation values as needed

        # Draw the filled mango path
        painter.save()
        painter.rotate(45)
        painter.fillPath(filledMangoPath, QtGui.QBrush(mangoGradient))
        painter.restore()

        # Draw "mango" text in the center of the mango shape
        self.drawText(painter, "mango", [-80, -40, 250, 80])
        self.drawText(painter, "rig", [-80, 0, 250, 80])

    def drawText(self, painter, txt, position):
        textFont = QtGui.QFont("Helvetica", 40, QtGui.QFont.Bold)
        textRect = QtCore.QRectF(*position)
        painter.rotate(15)
        painter.setFont(textFont)
        painter.setPen(QtCore.Qt.black)
        painter.drawText(textRect, QtCore.Qt.AlignCenter, txt)

"""
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.view)
        self.mangoItem = MangoItem()
        self.scene.addItem(self.mangoItem)

app = QtWidgets.QApplication([])
widget = MyWidget()
widget.show()
app.exec_()
"""