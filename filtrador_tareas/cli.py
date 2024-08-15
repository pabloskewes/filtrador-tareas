import argparse
from pathlib import Path

from filtrador_tareas.filtrador import filtrar_archivos


def parse_args():
    """
    Parse the command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Filtra las tareas de un ayudante y guarda el resultado en un archivo."
    )

    # Agregar el argumento ayudante, que es obligatorio pero puede ser llamado con --ayudante
    parser.add_argument(
        "--ayudante",
        type=str,
        required=True,
        help="Nombre del ayudante para filtrar las tareas.",
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Ruta al archivo .ods de entrada. (Por defecto: lista_tareas.ods)",
        default="lista_tareas.ods",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Ruta al archivo .xlsx de salida. (Por defecto: tareas_<ayudante>.xlsx)",
        default=None,
    )

    return parser.parse_args()


def main():
    """
    Main function that is executed when the script is run.
    """
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    try:
        filtrar_archivos(
            ayudante=args.ayudante,
            input_path=input_path,
            output_path=output_path,
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
