from typing import Optional
from pathlib import Path

import pandas as pd

from filtrador_tareas.alumnos import ALUMNOS_POR_AYUDANTE


def filtrar_tareas(ayudante: str, tareas: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra las tareas de un ayudante en particular.

    Args:
        ayudante (str): Nombre del ayudante.
        tareas (pd.DataFrame): DataFrame con las tareas.
    Returns:
        pd.DataFrame: DataFrame con las tareas del ayudante.
    """
    if ayudante not in ALUMNOS_POR_AYUDANTE:
        raise ValueError(f"{ayudante} no es un ayudante válido.")

    tareas.rename(columns={"Unnamed: 2": "estudiante"}, inplace=True)
    tareas_filtradas = tareas[tareas["estudiante"].isin(ALUMNOS_POR_AYUDANTE[ayudante])]
    return tareas_filtradas.reset_index(drop=True)


def filtrar_archivos(
    ayudante: str,
    input_path: Optional[Path] = None,
    output_path: Optional[Path] = None,
) -> None:
    """
    Filtra las tareas de un ayudante en particular y guarda el resultado
    en un archivo.

    Args:
        ayudante (str): Nombre del ayudante.
        input_path (Path): Ruta al archivo de entrada.
        output_path (Path): Ruta al archivo de salida.
    """
    if input_path is None:
        input_path = Path("lista_tareas.ods")
    if not input_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo {input_path}")
    if input_path.suffix != ".ods":
        raise ValueError("El archivo de entrada debe ser un archivo .ods")

    if output_path is None:
        output_path = Path(f"tareas_{ayudante}.xlsx")

    tareas = pd.read_excel(input_path, engine="odf")
    tareas_filtradas = filtrar_tareas(ayudante, tareas)
    tareas_filtradas.to_excel(output_path, index=False)
    print(f"Archivo guardado en {output_path}")
