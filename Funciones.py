
from IPython.display import display
import pandas as pd


def cargar_datos(ruta, n_filas=None, tipos=None):
    """
    Carga un archivo CSV y muestra sus dimensiones.

    Parámetros
    ----------
    ruta : str
        Ruta del archivo CSV.
    n_filas : int, opcional
        Número máximo de filas que se cargarán.
    tipos : dict, opcional
        Tipos de datos que queremos conservar.

    Devuelve
    --------
    pd.DataFrame
        Datos cargados.
    """

    datos = pd.read_csv(
        ruta,
        nrows=n_filas,
        dtype=tipos
    )

    print(f"Filas: {datos.shape[0]:,}")
    print(f"Columnas: {datos.shape[1]}")

    return datos


def resumen_calidad(datos):
    """
    Genera un resumen de la calidad de los datos.

    Devuelve una tabla con tipos de datos,
    valores nulos y porcentajes de ausencia.
    """

    resumen = pd.DataFrame({
        "Tipo de dato": datos.dtypes.astype(str),
        "Valores nulos": datos.isnull().sum(),
        "Porcentaje nulos (%)": (
            datos.isnull().mean() * 100
        ).round(2),
        "Valores únicos": datos.nunique()
    })

    return resumen


def preparar_transacciones(datos):
    """
    Prepara las variables temporales de transacciones.

    Convierte la fecha y crea columnas de año,
    mes y año-mes para facilitar el análisis.

    No elimina filas ni modifica el DataFrame original.
    """

    datos = datos.copy()

    datos["t_dat"] = pd.to_datetime(
        datos["t_dat"],
        errors="coerce"
    )

    datos["anio"] = datos["t_dat"].dt.year
    datos["mes"] = datos["t_dat"].dt.month
    datos["anio_mes"] = (
        datos["t_dat"].dt.strftime("%Y-%m")
    )

    return datos


def filtrar_transacciones_csv(
    ruta_entrada,
    ruta_salida,
    fecha_inicio,
    fecha_fin,
    tamano_bloque=500_000
):
    """
    Filtra un CSV de transacciones por fechas.

    Procesa el archivo por bloques para evitar
    cargar todos los registros en memoria.

    Guarda el resultado en un nuevo CSV.
    """

    from pathlib import Path

    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    total_guardado = 0
    primera_escritura = True

    for bloque in pd.read_csv(
        ruta_entrada,
        dtype={"article_id": "string"},
        chunksize=tamano_bloque
    ):
        # Convertir fechas
        bloque["t_dat"] = pd.to_datetime(
            bloque["t_dat"]
        )

        # Filtrar periodo
        filtro = bloque["t_dat"].between(
            fecha_inicio,
            fecha_fin
        )

        seleccion = bloque.loc[filtro].copy()

        if seleccion.empty:
            continue

        # Crear variables temporales
        seleccion = preparar_transacciones(
            seleccion
        )

        # Guardar sin sobrescribir bloques anteriores
        seleccion.to_csv(
            ruta_salida,
            mode="w" if primera_escritura else "a",
            header=primera_escritura,
            index=False
        )

        primera_escritura = False
        total_guardado += len(seleccion)

    print("Transacciones guardadas:",
          f"{total_guardado:,}")

    print("Archivo creado:", ruta_salida)

    return total_guardado


def preparar_clientes(datos):
    """
    Prepara el dataset de clientes para el análisis.

    - Conserva los identificadores originales.
    - Estandariza las categorías.
    - Identifica valores desconocidos.
    - Crea segmentos de edad.
    - No elimina registros.
    """

    datos = datos.copy()

    # Estandarizar categorías
    columnas_categoricas = [
        "club_member_status",
        "fashion_news_frequency"
    ]

    for columna in columnas_categoricas:
        datos[columna] = (
            datos[columna]
            .astype("string")
            .str.strip()
            .str.upper()
            .fillna("UNKNOWN")
        )

    # Convertir edad a numérico
    datos["age"] = pd.to_numeric(
        datos["age"],
        errors="coerce"
    )

    # Crear segmentos de edad
    datos["grupo_edad"] = pd.cut(
        datos["age"],
        bins=[0, 24, 34, 44, 54, 64, float("inf")],
        labels=[
            "16-24",
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65+"
        ]
    )

    # Identificar edades desconocidas
    datos["grupo_edad"] = (
        datos["grupo_edad"]
        .cat.add_categories("UNKNOWN")
        .fillna("UNKNOWN")
    )

    return datos


def preparar_articulos(datos):
    """
    Prepara el dataset de artículos de H&M.

    - Conserva los identificadores originales.
    - Estandariza espacios en variables de texto.
    - Gestiona descripciones ausentes.
    - No elimina artículos ni categorías.
    """

    datos = datos.copy()

    # Conservar article_id como texto
    datos["article_id"] = datos["article_id"].astype("string")

    # Limpiar espacios en columnas de texto
    columnas_texto = datos.select_dtypes(
        include=["object", "string"]
    ).columns

    for columna in columnas_texto:
        datos[columna] = (
            datos[columna]
            .astype("string")
            .str.strip()
        )

    # Identificar descripciones ausentes
    datos["detail_desc"] = (
        datos["detail_desc"]
        .fillna("DESCRIPTION NOT AVAILABLE")
    )

    return datos
