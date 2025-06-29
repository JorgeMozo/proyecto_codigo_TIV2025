from modulos import form, graficas, consultar
import pandas as pd
import streamlit as st
import os 

#Class
class App_Paros:
    def __init__(self):
        st.set_page_config(page_title="Registro de Paros", page_icon="🦖")

        path = "datos/datos_Paros.csv"

        # Leer archivo CSV si existe
        try:
            df = pd.read_csv(path, encoding="utf-8")
            if "Fecha" in df.columns:
                df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.date

            st.session_state.df = df
            st.session_state.paros = df.to_dict(orient="records")
            st.success("Paros cargados desde archivo CSV.")
        except FileNotFoundError:
            st.warning("Archivo CSV no encontrado. Se inicia con un dataframe vacio.")
            st.session_state.df = pd.DataFrame()
            st.session_state.paros = []

    def vista_formulario_de_paros(self):
        form.mostrar_formulario()

    def vista_visualizacion_de_registros(self):
        graficas.mostrar_visualizaciones()

    def vista_consultar_registros(self):
        consultar.mostrar_consulta()

    def run_py(self):
        st.sidebar.title("☰ Menú")
        opcion = st.sidebar.radio("Ir a:", ["Registro", "Visualizacion", "Consultar"])
        if opcion == "Registro":
            self.vista_formulario_de_paros()
        elif opcion == "Visualizacion":
            self.vista_visualizacion_de_registros()
        elif opcion == "Consultar":
            self.vista_consultar_registros()
        else:
            st.error("ERROR #404")

app = App_Paros()
app.run_py()





