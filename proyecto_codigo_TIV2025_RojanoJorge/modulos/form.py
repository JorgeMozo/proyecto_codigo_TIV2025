import pandas as pd
import streamlit as st
import datetime as dt
from pathlib import Path

def mostrar_formulario():
    st.title("Registro de Paros")
    st.write("Por favor, rellene los siguientes datos:")

    # Cargar datos desde CSV
    base_path = Path("datos")
    df_estaciones = pd.read_csv(base_path / "estaciones.csv")
    df_paros = pd.read_csv(base_path / "paros_comunes.csv")
    df_fase_linea = pd.read_csv(base_path / "fase_linea_cliente.csv")

    # Crear diccionario dinámico de líneas por fase
    lineas_por_fase = {
        fase: dict(zip(grupo["linea"], grupo["cliente"]))
        for fase, grupo in df_fase_linea.groupby("fase")
    }

    # Sección superior: Fecha y Fase
    colu1, colu2 = st.columns(2)
    with colu1:
        fecha = st.date_input("📅 Fecha de registro", value=dt.date.today())
        semana = fecha.isocalendar().week
        st.write(f"📆 Semana del año: {semana}")
    with colu2:
        fase = st.radio("Fase:", list(lineas_por_fase.keys()))

    colu1, colu2 = st.columns(2)
    # Obtener líneas y clientes según la fase seleccionada
    with colu1:
        lineas = lineas_por_fase.get(fase, {})
        linea = st.selectbox("Selecciona una línea:", list(lineas.keys()))
        cliente = lineas.get(linea, "")
        # Mostrar cliente de forma reactiva
        if linea:
            st.write(f"🏷️ Cliente asociado: {cliente}")

    with colu2:
        # Lado y estación (fuera del formulario para que sea reactivo)
        lados = [" ", "RH", "LH", "FR RH", "FR LH", "RR RH", "RR LH"]
        lado = st.selectbox("Selecciona el lado:", lados)
        estaciones = df_estaciones["estaciones"].dropna().tolist()
        estacion = st.selectbox("Selecciona la estación:", estaciones)

    # Vista previa reactiva
    if linea and lado and estacion:
        st.info(f"Seleccionaste la {linea} en el lado {lado}, estación {estacion}.")

    # Formulario principal
    with st.form("form_registro"):
        colu1, colu2 = st.columns(2)
        with colu1:
            turno = st.radio("Turno:", ["1", "2"])
            trip = st.radio("Tripulación:", ["A", "B"])
        with colu2:
            min = st.slider("Min:", min_value=1, max_value=350, step=1)
            paros_comunes = df_paros["paros_comunes"].dropna().tolist()
            problema = st.selectbox("Paros Comunes:", paros_comunes)
            descripcion = st.text_input("Descripción", placeholder="Describe el Paro...")

        guardar = st.form_submit_button("Guardar Formulario")

    # Guardar datos si se envía el formulario
    if guardar:
        paro = f"{lado} {linea} {problema}"
        capturista = f"{min} min {lado} {linea} {problema} {descripcion}"

        nuevo_paro = {
            "Fecha": fecha, "Semana": semana,
            "Turno": turno, "Tripulacion": trip,
            "Fase": fase, "Linea": linea,
            "Cliente": cliente, "Lado": lado,
            "Estación": estacion, "Min": min,
            "Problema": problema, "Paro": paro, "Capturista": capturista
        }

        if "paros" not in st.session_state:
            st.session_state.paros = []

        st.session_state.paros.append(nuevo_paro)
        st.success(f"Paro registrado: {paro}")
        st.success(f"Dato completo: {capturista}")

        st.session_state.df = pd.DataFrame(st.session_state.paros)
        output_path = base_path / "datos_Paros.csv"
        st.session_state.df.to_csv(output_path, index=False, encoding="utf-8-sig")
        st.success("Archivo CSV guardado exitosamente.")