import sys
import pandas as pd
import altair as alt
import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication, QFormLayout, QLineEdit, QComboBox, \
    QPushButton, QLabel, QMessageBox, QStatusBar, QMenuBar, QMenu


class ConversorMonedas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de Divisas")

        # Estilos CSS para la ventana
        estilos = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QStatusBar {
                background-color: #e0e0e0;
                color: #333333;
                font-size: 12px;
            }
            QMenuBar {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #45a049;
            }
            QMenu {
                background-color: #ffffff;
                color: #333333;
                font-size: 14px;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """

        # Aplicar estilos a la ventana
        self.setStyleSheet(estilos)

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self)
        self.label.setText("Conversor de Divisas")
        self.label.setStyleSheet("background-color: rgb(206, 255, 217);")
        self.layout.addWidget(self.label)

        self.imagen = QLabel(self)
        self.imagen.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("moneda.png")
        if not pixmap.isNull():
            imagen_escalada = pixmap.scaled(250, 200)
            self.imagen.setPixmap(imagen_escalada)
        else:
            self.imagen.setText("No se pudo cargar la imagen.")
        self.layout.addWidget(self.imagen)

        self.form_layout = QFormLayout()
        self.cantidad_input = QLineEdit()
        self.form_layout.addRow("Cantidad:", self.cantidad_input)

        self.moneda_origen = QComboBox()
        self.moneda_origen.addItems(["USD", "EUR", "MXN", "GBP", "JPY"])
        self.form_layout.addRow("Moneda Origen:", self.moneda_origen)

        self.moneda_destino = QComboBox()
        self.moneda_destino.addItems(["USD", "EUR", "MXN", "GBP", "JPY"])
        self.form_layout.addRow("Moneda Destino:", self.moneda_destino)

        self.layout.addLayout(self.form_layout)

        self.resultado = QLabel("")
        self.layout.addWidget(self.resultado)

        self.botonCalcular = QPushButton("Convertir")
        self.layout.addWidget(self.botonCalcular)
        self.botonCalcular.clicked.connect(self.calcular)

        self.botonGrafico = QPushButton("Evolucion de monedas frente al Euro. Mostrar Gráfico")
        self.layout.addWidget(self.botonGrafico)
        self.botonGrafico.clicked.connect(self.mostrar_grafico)

        self.vista_web = QWebEngineView()
        self.vista_web.setMinimumSize(300, 120)  # Ajusta el tamaño mínimo del área del gráfico
        self.layout.addWidget(self.vista_web)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.menu = QMenu("Archivo", self)
        self.menu_bar.addMenu(self.menu)
        self.menu.addAction("Salir", self.close)

        self.menuAyuda = QMenu("Ayuda", self)
        self.menu_bar.addMenu(self.menuAyuda)
        self.menuAyuda.addAction("Acerca de", self.mostrar_info)

        self.tasas_cambio = {
            "USD": 1.0,
            "EUR": 0.92,
            "MXN": 17.0,
            "GBP": 0.78,
            "JPY": 150.0
        }

    def calcular(self):
        try:
            cantidad = float(self.cantidad_input.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese una cantidad válida.")
            return

        origen = self.moneda_origen.currentText()
        destino = self.moneda_destino.currentText()

        if origen == destino:
            self.resultado.setText("Elija una moneda diferente para cambiar.")
            return

        cantidad_usd = cantidad / self.tasas_cambio[origen]
        resultado = cantidad_usd * self.tasas_cambio[destino]

        self.resultado.setText(f"Resultado {resultado:.2f} {destino}")
        self.status_bar.showMessage("Conversión realizada con éxito", 3000)

    def mostrar_grafico(self):
        try:
            if not os.path.exists("evolucion_monedas.csv"):
                QMessageBox.warning(self, "Error", "El archivo evolucion_monedas.csv no existe.")
                return

            datos = pd.read_csv("evolucion_monedas.csv")
            print(datos.head())  # Depuración para ver las primeras filas

            datos["DateTime"] = pd.to_datetime(datos["DateTime"], format="%Y-%m-%d")
            datos = datos.melt(id_vars=["DateTime"], var_name="Moneda", value_name="Valor")

            grafico = alt.Chart(datos).mark_line().encode(
                x="DateTime:T",
                y="Valor:Q",
                color="Moneda:N"
            ).properties(
                title="Evolución de las monedas frente al Euro",
                width=180,
                height=90
            ).interactive()

            ruta = "grafico_monedas.html"
            grafico.save(ruta)

            ruta_absoluta = os.path.abspath(ruta)
            if os.path.exists(ruta_absoluta):
                with open(ruta_absoluta, "r",encoding='UTF-8') as f:
                    html_content = f.read()
                    self.vista_web.setHtml(html_content)
            else:
                QMessageBox.warning(self, "Error", "No se pudo encontrar el archivo HTML generado.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo generar el gráfico: {str(e)}")

    def mostrar_info(self):
        QMessageBox.information(self, "Info", "Conversor de Monedas v1.0\nHecho con PySide6.")


if __name__ == "__main__":
    app = QApplication([])
    ventana = ConversorMonedas()
    ventana.show()
    sys.exit(app.exec())