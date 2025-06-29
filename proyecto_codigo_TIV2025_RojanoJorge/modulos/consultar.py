import streamlit as st
import pandas as pd
import streamlit as st
import os 


def mostrar_consulta():

    # Sidebar para selección
    st.session_state.paros = st.session_state.df.to_dict(orient="records")
    st.success("Paros recuperados exitosamente del Archivo")
    opcion_vista = st.selectbox(
        "¿Qué deseas visualizar?",
        ("Tipos de Datos", "Tabla", "Ambos")
    )
    # Cargar el archivo
    try:
        st.session_state.df = pd.DataFrame(st.session_state.paros)
        path = "datos/datos_Paros.csv"
        st.session_state.df.to_csv(path, index=False, encoding="utf-8-sig")
        st.success("Archivo CSV guardado exitosamente.")
        
        # Transformar 'Fecha' a solo la parte de fecha
        if 'Fecha' in st.session_state.df.columns:
            st.session_state.df['Fecha'] = pd.to_datetime(st.session_state.df['Fecha']).dt.date
    except FileNotFoundError:
        st.session_state.paros = []
        st.session_state.df = pd.DataFrame()

    # Mostrar resultados según la selección
    if opcion_vista == "Tipos de Datos":
        st.subheader("🔍 Tipos de Datos")
        st.dataframe(
            st.session_state.df.dtypes.reset_index().rename(
                columns={"index": "Columna", 0: "Tipo de Dato"}
            )
        )
    elif opcion_vista == "Tabla":
        st.subheader("📊 Mostrar datos con DataFrame")
        st.dataframe(st.session_state.df)
    elif opcion_vista == "Ambos":
        st.subheader("🔍 Tipos de Datos")
        st.dataframe(
            st.session_state.df.dtypes.reset_index().rename(
                columns={"index": "Columna", 0: "Tipo de Dato"}
            )
        )
        st.subheader("📊 Mostrar datos con DataFrame")
        st.dataframe(st.session_state.df)

    # Actualización del archivo

    st.session_state.df = pd.DataFrame(st.session_state.paros)
    st.session_state.df.to_csv(path, index=False, encoding="utf-8-sig")
    st.success("Archivo CSV guardado exitosamente.")