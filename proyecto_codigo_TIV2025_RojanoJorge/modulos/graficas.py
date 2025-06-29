import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import os 
import plotly.express as px

def mostrar_visualizaciones():

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
            st.plotly_chart(fig_bar)

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
            st.plotly_chart(fig_scatter)

            st.markdown("---")
            st.write("Configuración de mapa de calor de densidad")

            # Selección de variables para los ejes
            colu1, colu2 = st.columns(2)
            with colu1: #todo lo que este identado va en la columna 1
                heatmap_x = st.selectbox("Eje X:", variables, key="heatmap_x")
                heatmap_y = st.selectbox("Eje Y:", variables, key="heatmap_y")
            with colu2: #todo lo que este identado va en la columna 2
                color_options = ["Min", "Semana"]
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
            st.plotly_chart(fig_heatmap)

            st.session_state.df = pd.DataFrame(st.session_state.paros)
            path = "datos/datos_Paros.csv"
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
