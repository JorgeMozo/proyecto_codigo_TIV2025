import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
import datetime as dt
import os 
import plotly.express as px



class App_Paros:
    def __init__(self):
        st.set_page_config(page_title="Registro de Paros", page_icon="🦖")

        path = os.path.join(os.getcwd(), "datos", "datos_Paros.csv")

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

        st.title("Registro de Paros")
        st.write("Por favor, rellene los siguientes datos:")
        colu1, colu2 = st.columns(2)
        with colu1:
         # Selector de fecha
            fecha = st.date_input("📅 Fecha de registro", value=dt.date.today())
            # Cálculo reactivo de la semana
            semana = fecha.isocalendar().week
            st.write(f"📆 Semana del año: {semana}")
        with colu2:
            # Selector de fase (¡esto va ANTES!)
            fase = st.radio("Fase:", ["Fase1", "Fase2"])

            # Diccionario de líneas por fase y cliente
            lineas_por_fase = {
                "Fase1": {
                    "GA Main": "NISSAN", "GA Cable A RH": "NISSAN", "GA Cable A LH": "NISSAN",
                    "GA Cable B LH": "NISSAN", "GA Cable B RH": "NISSAN", "Hinge Autom": "NISSAN",
                    "Hinge P02F": "NISSAN", "Check link P02F": "NISSAN", "Check link L02D": "NISSAN",
                    "Check link XDC": "NISSAN", "AC6": "STELLANTIS", "AC9 Power": "STELLANTIS",
                    "AC9 Cinch": "STELLANTIS", "M2 FR RH": "NISSAN", "M2 FR LH": "NISSAN",
                    "M2 RR RH": "NISSAN", "M2 RR LH": "NISSAN", "GC2 MAIN": "STELLANTIS",
                    "GC2 BACK PLATE": "STELLANTIS", "GC2 ACTUADOR": "STELLANTIS",
                    "Hood Lock P71A": "NISSAN", "Bell crank": "NISSAN", "Sub Procesos": "NISSAN"
                },
                "Fase2": {
                    "Conveyor": "HONDA", "M16 A RH": "HONDA", "M16 A LH": "HONDA",
                    "M16 B RH": "HONDA", "M16 B LH": "HONDA", "M18 RH": "HONDA",
                    "M18 LH": "HONDA", "M11 Final FR RH": "HONDA", "M11 Final FR LH": "HONDA",
                    "M11 Final RR RH": "HONDA", "M11 Final RR LH": "HONDA", "ODYSSEY LH": "HONDA",
                    "ODYSSEY RH": "HONDA", "C5": "HONDA", "Pass Through": "HONDA"
                }
            }

        colu1, colu2 = st.columns(2)
        with st.form("form_registro"):
            colu1, colu2 = st.columns(2)
            with colu1: #todo lo que este identado va en la columna 1
                # Selector de turno y tripulación
                turno = st.radio("Turno:", ["1", "2"])
                trip = st.radio("Tripulación:", ["A", "B"])
                # Ahora sí puedes acceder al diccionario correctamente
                lineas = lineas_por_fase.get(fase, {})
                linea = st.selectbox("Selecciona una línea:", list(lineas.keys()))

                # Mostrar cliente
                if linea:
                    cliente = lineas[linea]
                    st.write(f"🏷️ Cliente asociado: {cliente}")
                # Mostrar cliente correspondiente
                cliente = lineas[linea]


                # Opciones de lado posibles
                lados = [" ","RH", "LH", "FR RH", "FR LH", "RR RH", "RR LH"]

                lado = st.selectbox("Selecciona el lado:", lados)

                # Lista de líneas
                estaciones = [
                    "LINEA","A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A1", "A1.1", "A1.2",
                    "A10", "A11", "A12", "A13", "A13.1", "A14", "A14.1", "A15", "A16", "A17", "A18", "A19",
                    "A2", "A20", "A21", "A22", "A23", "A24", "A25", "A26", "A27", "A28", "A3", "A3.1", "A30",
                    "A31", "A32", "A33", "A34", "A35", "A36", "A37", "A38", "A39", "A4", "A40", "A5", "A5.1",
                    "A5.2", "A5.3", "A5.4", "A6", "A7", "A8", "A9", "B01", "B02", "B03", "B04", "B05", "B06",
                    "B07", "B08", "B09", "B1", "B10", "B11", "B12", "B12.1", "B13", "B14", "B15", "B16",
                    "B17", "B18", "B19", "B2", "B20", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "C01", "C02",
                    "C03", "C1", "C2", "C3", "C4", "C5", "J01", "J02", "J03", "J04", "J05", "K01", "K02", "K03",
                    "K04", "K05", "K06", "K07", "K08", "K09", "K10", "K11", "K12", "K13", "K14", "K15", "K16",
                    "K17", "K18", "K19", "K20", "K21", "K22", "K23", "K24", "K25", "K26", "K27", "K28", "K29",
                    "K30", "K31", "K32", "K33", "K34", "K35", "K36", "K37", "K38", "K39", "K40", "S01", "S02",
                    "S03", "S04", "S06", "S07", "S08", "S09", "S1", "S10", "S2", "S3", "S4", "S5", "S6", "S7",
                    "S8", "S9", "SA01", "SA02", "SA03", "SA04", "SA05", "SA06", "SA07", "SA08", "SA09",
                    "SA10", "SA11", "SA12", "SA13", "SA14", "SA15", "SA16", "SA17", "SA18", "SA19", "SA20"
                ]
                estacion = st.selectbox("Selecciona la estación:", estaciones)

                st.info(f"Seleccionaste la {linea} en el lado {lado}, estación {estacion}.")

            with colu2: #todo lo que este identado va en la columna 2
                min = st.slider("Min:", min_value=1, max_value=350, step=1)

                # Lista de paros comunes
                paros_comunes = [
                    "Abastecimiento", "Abastecimiento por Inventario", "Acomodo de Personal",
                    "Acomodo de Secuencia", "Ajar Switch", "Ajuste de Bomba de Grasa"
                ]

                # Selectbox para elegir un paro
                problema = st.selectbox("Paros Comunes:", paros_comunes)
                descripcion = st.text_input("Descripción", placeholder="Describe el Paro...")
                paro = f"{lado} {linea} {problema}"
                capturista = f"{min} min {lado} {linea} {problema} {descripcion}"




            guardar = st.form_submit_button("Guardar Formulario")
    

        if guardar:
            nuevo_paro = {
                "Fecha":fecha, 
                "Semana":semana, 
                "Turno":turno, 
                "Tripulacion":trip, "Fase": fase,
                "Linea":linea, "Cliente":cliente,
                "Lado":lado, "Estación":estacion,
                "Min":min, "Problema": problema,
                "Paro":paro, "Capturista": capturista
                }
        
            st.session_state.paros.append(nuevo_paro)
                # Mostrar resultado final
            st.success(f"Paro registrado: {paro}")
            st.success(f"Dato completo: {capturista}")


            st.session_state.df = pd.DataFrame(st.session_state.paros)
            path = os.path.join(os.getcwd(), "datos", "datos_Paros.csv")
            st.session_state.df.to_csv(path, index=False, encoding="utf-8-sig")
            st.success("Archivo CSV guardado exitosamente.")


    def vista_visualizacion_de_registros(self):
            if not st.session_state.df.empty:
                st.session_state.df = pd.DataFrame(st.session_state.paros) #actualizo el dataframe
                # Lista de variables disponibles
                variables = st.session_state.df.columns.tolist()

                st.write("Configuración de gráfica de barras")
                colu1, colu2 = st.columns(2)
                with colu1: #todo lo que este identado va en la columna 1
                    x_bar = st.selectbox("Eje X:", variables, key="x_bar")
                with colu2: #todo lo que este identado va en la columna 2
                    y_bar = st.radio("Eje Y:", ["Min"], key="y_bar")
                color_bar = st.selectbox("Color:", [None] + variables, key="color_bar")


                st.subheader("📊 Gráfica de Barras")
                fig_bar = px.bar(
                    st.session_state.df,
                    x=x_bar,
                    y=y_bar,
                    color=color_bar if color_bar else None,
                    barmode="group",
                    title=f"{y_bar} por {x_bar}",
                    labels={x_bar: x_bar, y_bar: y_bar}, )
                st.plotly_chart(fig_bar, use_container_width=True)

                st.markdown("---")
                st.write("Configuración de gráfica de dispersión")
                colu1, colu2 = st.columns(2)
                with colu1: #todo lo que este identado va en la columna 1
                    x_disp = st.selectbox("Eje X:", variables, key="x_disp")
                with colu2: #todo lo que este identado va en la columna 2
                    y_disp = st.selectbox("Eje Y:", variables, key="y_disp")
                color_disp = st.selectbox("Color:", [None] + variables, key="color_disp")

                st.subheader("🎯 Gráfica de Dispersión")
                fig_scatter = px.scatter(
                    st.session_state.df,
                    x=x_disp,
                    y=y_disp,
                    color=color_disp if color_disp else None,
                    title=f"{y_disp} vs {x_disp}",
                    labels={x_disp: x_disp, y_disp: y_disp}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

                st.markdown("---")
                st.write("Configuración de mapa de calor de densidad")

                # Selección de variables para los ejes
                heatmap_x = st.selectbox("Eje X:", variables, key="heatmap_x")
                heatmap_y = st.selectbox("Eje Y:", variables, key="heatmap_y")

                color_options = ["Min", "Num de Semana"]
                heatmap_color = st.selectbox("Color (valor agregado):", [None] + color_options, key="heatmap_color")

                st.subheader("🔥 Mapa de Calor")

                fig_heatmap = px.density_heatmap(
                    st.session_state.df,
                    x=heatmap_x,
                    y=heatmap_y,
                    z=heatmap_color if heatmap_color else None,
                    histfunc="avg" if heatmap_color else "count",
                    title=f"Densidad de {heatmap_y} vs {heatmap_x}",
                    nbinsx=20,
                    nbinsy=20,
                    labels={heatmap_x: heatmap_x, heatmap_y: heatmap_y},)
                st.plotly_chart(fig_heatmap, use_container_width=True)


                

                st.session_state.df = pd.DataFrame(st.session_state.paros)
                path = os.path.join(os.getcwd(), "datos", "datos_Paros.csv")
                st.session_state.df.to_csv(path, index=False, encoding="utf-8-sig")
                st.success("Archivo CSV guardado exitosamente.")





                with st.form("form_exportar"):

                    st.write("📝 Especifica el nombre del archivo y la carpeta de destino")

                    nombre_archivo = st.text_input("Nombre del archivo (sin extensión)", value="Paros")
                    carpeta_destino = st.text_input("Ruta de la carpeta", value=os.getcwd())

                    exportar = st.form_submit_button("Guardar ")
                    if not st.session_state.df.empty: 

                        if exportar:
                            # Asegurarse de que la carpeta exista
                            if not os.path.isdir(carpeta_destino):
                                st.error("❌ La carpeta especificada no existe.")
                            else:
                                ruta_completa = os.path.join(carpeta_destino, f"{nombre_archivo}.csv")
                                st.session_state.df.to_csv(ruta_completa, index=False)
                                st.success(f"✅ Registros guardados en: {ruta_completa}")



                    else: 
                        st.error("No hay paros registrados ⚠️ ☹️ ") 


    def vista_consultar_registros(self):

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
            path = os.path.join(os.getcwd(), "datos", "datos_Paros.csv")
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

        # Actualización del archivo (si lo deseas realizar aquí también)
        path_guardado = os.path.join(os.getcwd(), "datos", "datos_Paros.xlsx")
        st.session_state.df = pd.DataFrame(st.session_state.paros)
        st.session_state.df.to_excel(path_guardado, index=False, engine="openpyxl")
        

    def run_py(self):
        st.sidebar.title("☰ Menú")
        opcion = st.sidebar.radio("Ir a: ", ["Registro", "Visualizacion","Consultar"])
        if opcion == "Registro":
            self.vista_formulario_de_paros()
        elif opcion == "Visualizacion":
            self.vista_visualizacion_de_registros()
        elif opcion == "Consultar":
            self.vista_consultar_registros()
        else:
            print("ERROR #404")

app = App_Paros()
app.run_py()


