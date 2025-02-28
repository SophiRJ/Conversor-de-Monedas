import pytest
import sys
import os

from PySide6.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ConversorMonedas import ConversorMonedas


@pytest.fixture(scope="session")## vamos a utilizar esta instancia para todos los test
def app_instance():
    app=QApplication([])##Creamos una instancia de QAplication
    yield app#proporciona la aplicacion para todos los test
    app.quit()# Cierra la aplicacion despues de todos los test

@pytest.fixture()
def window(app_instance):
    #Crear una instancia de task manager para cada test
    window= ConversorMonedas()
    window.show()
    return window

def test_conversion_misma_moneda(window):
    window.cantidad_input.setText("100")
    window.moneda_origen.setCurrentText("USD")
    window.moneda_destino.setCurrentText("USD")
    window.calcular()
    assert window.resultado.text() == "Elija una moneda diferente para cambiar."

def test_conversion_usd_a_eur(window):
    window.cantidad_input.setText("100")
    window.moneda_origen.setCurrentText("USD")
    window.moneda_destino.setCurrentText("EUR")
    window.calcular()
    assert window.resultado.text() == "Resultado 92.00 EUR"


def test_conversion_mxn_a_gbp(window):
    window.cantidad_input.setText("170")
    window.moneda_origen.setCurrentText("MXN")
    window.moneda_destino.setCurrentText("GBP")
    window.calcular()
    assert window.resultado.text() == "Resultado 7.80 GBP"

def test_entrada_invalida_no_numerica(window):
    window.cantidad_input.setText("hola")
    window.calcular()
    assert window.resultado.text() == ""


def test_entrada_invalida_vacia(window):
    window.cantidad_input.setText("")
    window.calcular()
    assert window.resultado.text() == ""

def test_valores_combo_box(window):
    assert window.moneda_origen.count() == 5
    assert window.moneda_destino.count() == 5
    assert window.moneda_origen.itemText(0) == "USD"
    assert window.moneda_destino.itemText(1) == "EUR"

def test_menu_archivo(window):
    assert window.menu.title() == "Archivo"
    assert window.menu.actions()[0].text() == "Salir"


def test_menu_ayuda(window):
    assert window.menuAyuda.title() == "Ayuda"
    assert window.menuAyuda.actions()[0].text() == "Acerca de"


def test_barra_estado(window):
    assert window.status_bar is not None