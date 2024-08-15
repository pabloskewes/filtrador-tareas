from io import BytesIO

import pandas as pd
import streamlit as st

from filtrador_tareas.filtrador import filtrar_tareas
from filtrador_tareas.alumnos import ALUMNOS_POR_AYUDANTE


def cargar_tareas(uploaded_file) -> pd.DataFrame:
    """Carga el archivo .ods de tareas y lo convierte a un DataFrame."""
    return pd.read_excel(uploaded_file, engine="odf")


def seleccionar_ayudante() -> str:
    """Muestra un dropdown con los ayudantes disponibles y
    devuelve la selección."""
    return st.selectbox(
        "Selecciona un ayudante",
        options=list(ALUMNOS_POR_AYUDANTE.keys()),
    )


def generar_archivo_filtrado(tareas: pd.DataFrame, ayudante: str) -> BytesIO:
    """Filtra las tareas y genera un archivo Excel en memoria."""
    tareas_filtradas = filtrar_tareas(ayudante, tareas)
    output = BytesIO()
    tareas_filtradas.to_excel(output, index=False)
    output.seek(0)
    return output


def descargar_archivo(archivo: BytesIO, ayudante: str):
    """Provee un botón de descarga para el archivo filtrado."""
    st.download_button(
        label="Descargar tareas filtradas",
        data=archivo,
        file_name=f"tareas_{ayudante}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def main():
    """Función principal de la aplicación."""
    st.title("Filtrador de Tareas por Ayudante")

    # Subir archivo
    uploaded_file = st.file_uploader(
        "Sube el archivo de tareas (.ods)",
        type=["ods"],
    )

    if uploaded_file:
        tareas = cargar_tareas(uploaded_file)
        ayudante = seleccionar_ayudante()

        if st.button("Filtrar Tareas"):
            try:
                archivo_filtrado = generar_archivo_filtrado(tareas, ayudante)
                descargar_archivo(archivo_filtrado, ayudante)
                st.success(f"Tareas filtradas para {ayudante} generadas con éxito.")
            except Exception as e:
                st.error(f"Hubo un error al filtrar las tareas: {e}")


if __name__ == "__main__":
    main()
