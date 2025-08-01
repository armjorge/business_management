
import os 
from datetime import datetime
import yaml
import pandas as pd

def add_to_gitignore(root_directory, path_to_add):
    gitignore_path = os.path.join(root_directory, ".gitignore")
    
    # La ruta que queremos ignorar, relativa al root
    
    #relative_output = "Output/"
    #relative_output = f"{os.path.basename(path_to_add)}\\"
    relative_output = f"{os.path.basename(path_to_add)}/"
    #print(relative_output)

    # Verifica si ya está en .gitignore, si no, lo agrega
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            lines = f.read().splitlines()
    else:
        lines = []

    if relative_output not in lines:
        with open(gitignore_path, 'a') as f:
            f.write(f"\n{relative_output}\n")
        print(f"'{relative_output}' agregado a .gitignore.")
    else:
        print(f"'{relative_output}' ya está listado en .gitignore.")

def message_print(message): 
    message_highlights= '*' * len(message)
    message = f'\n{message_highlights}\n{message}\n{message_highlights}\n'
    return message

def yaml_creation(download_folder): 
    output_yaml = os.path.join(download_folder, "passwords.yaml")
    yaml_exists = os.path.exists(output_yaml)

    if yaml_exists:
        # Abrir y cargar el contenido YAML en un diccionario
        with open(output_yaml, 'r', encoding='utf-8') as f:
            data_access = yaml.safe_load(f)
        print(f"Archivo cargado correctamente: {os.path.basename(output_yaml)}")
        return data_access

    else: 
        print(message_print("No se localizó un yaml válido, vamos a crear uno con: "))
        platforms = ["1st_item"] # Los items
        fields    = ["url", "user", "password", "ACTIONS"] # Cada variable de los bancos
        
        lines = []
        for platform in platforms:
            for field in fields:
                # clave = valor vacío
                lines.append(f"{platform}_{field}: ")
            lines.append("")  # línea en blanco entre bloques
        
        # Escribe el archivo YAML (aunque use "=" tal como en tu ejemplo)
        with open(output_yaml, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def create_directory_if_not_exists(path_or_paths):
    """Creates a directory if it does not exist and prints in Jupyter."""
    message_create_directory_if_not_exists = 'Confirmando que los folders necesarios existen'
    print(message_print(message_create_directory_if_not_exists))
    if isinstance(path_or_paths, str):
        paths = [path_or_paths]
    elif isinstance(path_or_paths, list):
        paths = path_or_paths
    else:
        raise TypeError("El argumento debe ser un string o una lista de strings.")

    for path in paths:
        if not os.path.exists(path):
            print(f"\n\tNo se localizó el folder {os.path.basename(path)}, creando.", flush=True)
            os.makedirs(path)
            print(f"\tFolder {os.path.basename(path)} creado.", flush=True)
        else:
            print(f"\tFolder {os.path.basename(path)} encontrado.", flush=True)

def genera_partidas_presupuestales(egresos_path, ingresos_path): 
    # Preguntar al usuario hasta que dé una entrada válida
    while True:
        user_input = input("¿Quieres dar de alta un 1) ingreso o un 2) egreso?: ").strip()
        if user_input == "1":
            folder_elegido = ingresos_path
            break
        elif user_input == "2":
            folder_elegido = egresos_path
            break
        else:
            print("Entrada no válida. Por favor, escribe 1 o 2.")

    print(f"Has elegido: {os.path.basename(folder_elegido)}")
    columnas_comunes = ['fecha dd mm yyyy', 'Concepto', f"{os.path.basename(folder_elegido)}", 'Código Renglón'] 
    # Nombre del archivo
    nombre_presupuesto = input("Escribe el nombre que llevará el archivo: ").strip()
    # Crear DataFrame vacío
    df_empty = pd.DataFrame(columns=columnas_comunes)
    # Construir la ruta completa para guardar el Excel
    path_excel = os.path.join(folder_elegido, f"{nombre_presupuesto}.xlsx")
    # Guardar DataFrame como archivo Excel
    df_empty.to_excel(path_excel, index=False)
    print("Archivo generado:", path_excel)


def generador_validador_renglones(folder, columnas_folder):
    print(message_print(f'Iniciando el generador de cashflows para {os.path.basename(folder)}'))
    print("\nEste script va a leer los archivos xlsx en Ingresos y Egresos, si la columna fecha y la columna importe son válidas, les asignará un código único al renglón\n")
    

    for filename in os.listdir(folder):
        counter = 0
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder, filename)
            try:
                df_file = pd.read_excel(file_path)
            except Exception as e:
                print(f"❌ Error leyendo {filename}: {e}")
                continue

            # Verifica columnas
            if list(df_file.columns) != columnas_folder:
                print(f"⚠️ Columnas no válidas en {filename}. Se esperaban: {columnas_folder}")
                continue

            # Procesar filas
            updated_rows = 0
            for i, row in df_file.iterrows():
                fecha = row.get('fecha dd mm yyyy')
                monto = row.get(f"{os.path.basename(folder)}")

                if isinstance(fecha, datetime) and isinstance(monto, (float, int)):
                    counter += 1
                    df_file.at[i, 'Código Renglón'] = f"{os.path.splitext(filename)[0]}_{counter}"
                    updated_rows += 1
                else:
                    df_file.at[i, 'Código Renglón'] = ""        
            if updated_rows > 0:
                df_file.to_excel(file_path, index=False)
                print(f"✅ {filename} actualizado con {updated_rows} renglones.")
            else:
                print(f"ℹ️ {filename} sin filas válidas para actualizar.")

def generador_cash_flow(path_column_dict, columnas_ordenadas):
    df_total = pd.DataFrame()

    for path, expected_columns in path_column_dict.items():
        for filename in os.listdir(path):
            if filename.endswith(".xlsx"):
                file_path = os.path.join(path, filename)
                try:
                    df_file = pd.read_excel(file_path)
                except Exception as e:
                    print(f"❌ Error al leer {filename}: {e}")
                    continue

                # Validar columnas exactas
                if list(df_file.columns) != expected_columns:
                    print(f"⚠️ El archivo {filename} no tiene las columnas esperadas.")
                    continue

                # Eliminar filas con 'Código Renglón' vacío o NaN
                df_file = df_file.dropna(subset=['Código Renglón'])

                # Agregar al DataFrame total
                df_total = pd.concat([df_total, df_file], ignore_index=True)
    df_total = df_total[columnas_ordenadas]

    return df_total

def accumulative_cash_flow(df_total, columnas_acumulativas):
    print(message_print('Iniciando la generación del flujo de caja acumulativo'))
    fecha_col = columnas_acumulativas['Fecha']
    ingresos_col = columnas_acumulativas['Ingresos']
    egresos_col = columnas_acumulativas['Egresos']
    
    df_total[fecha_col] = pd.to_datetime(df_total[fecha_col], dayfirst=True, errors='coerce')
    
    df_agrupado = df_total.groupby(fecha_col).agg({
        ingresos_col: 'sum',
        egresos_col: 'sum'
    }).rename(columns={ingresos_col: 'Ingresos', egresos_col: 'Egresos'}).fillna(0).sort_index(ascending=True)
    
    df_agrupado['Balance'] = df_agrupado['Ingresos'] - df_agrupado['Egresos']
    df_agrupado['Acumulativo'] = df_agrupado['Balance'].cumsum()
    df_agrupado = df_agrupado.reset_index()
    
    return df_agrupado

def save_dfs_to_excel(path, sheet_to_df):
    """
    Guarda los DataFrames en hojas de un archivo Excel.
    - Si el archivo no existe, lo crea.
    - Si existe, sobreescribe las hojas indicadas.
    """
    mode = 'a' if os.path.exists(path) else 'w'
    if mode == 'a':
        # Añadir y sobreescribir hojas en archivo existente
        with pd.ExcelWriter(path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet, df in sheet_to_df.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
    else:
        # Crear nuevo archivo
        with pd.ExcelWriter(path, engine='openpyxl', mode='w') as writer:
            for sheet, df in sheet_to_df.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
                
def business_management(folder_root): 
    print('\nMódulo del repositorio privado https://github.com/armjorge/business_management\n')
    working_folder = os.path.join(folder_root, "Implementación")
    #add_to_gitignore(folder_root, working_folder)
    not os.path.exists(working_folder) and create_directory_if_not_exists(working_folder)
    #data_access = yaml_creation(working_folder) 
    print(message_print('Vamos a generar archivos presupuestales e ingresos'))
    presupuestos_path = os.path.join(working_folder, "Presupuesto")
    not os.path.exists(presupuestos_path) and create_directory_if_not_exists(presupuestos_path)
    egresos_path = os.path.join(presupuestos_path, "Egresos")
    not os.path.exists(egresos_path) and create_directory_if_not_exists(egresos_path)
    ingresos_path = os.path.join(presupuestos_path, "Ingresos")
    not os.path.exists(ingresos_path) and create_directory_if_not_exists(ingresos_path)    
    print(message_print('Script de Administración de Negocios'))
    columnas_egresos = ['fecha dd mm yyyy', 'Concepto', f"{os.path.basename(egresos_path)}", 'Código Renglón']  
    columnas_ingresos = ['fecha dd mm yyyy', 'Concepto', f"{os.path.basename(ingresos_path)}", 'Código Renglón'] 
    columnas_ordenadas = ['fecha dd mm yyyy', 'Concepto', f"{os.path.basename(ingresos_path)}", f"{os.path.basename(egresos_path)}", 'Código Renglón'] 
    columnas_acumulativas = {'Fecha': 'fecha dd mm yyyy', 'Ingresos': f"{os.path.basename(ingresos_path)}", 'Egresos': f"{os.path.basename(egresos_path)}"}
    while True:
        user_input = input("¿Quieres 1) generar archivos de ingreso y egresos o 2) generar el flujo de caja?: ").strip()
        if user_input == "1":
            genera_partidas_presupuestales(egresos_path, ingresos_path)
            
        elif user_input == "2":
            generador_validador_renglones(egresos_path, columnas_egresos)
            generador_validador_renglones(ingresos_path, columnas_ingresos)
            path_column_dict = {egresos_path: columnas_egresos, ingresos_path: columnas_ingresos}
            df_total = generador_cash_flow(path_column_dict, columnas_ordenadas)
            df_agrupado = accumulative_cash_flow(df_total, columnas_acumulativas)

            #path_excel = os.path.join(presupuestos_path, "Presupuesto.xlsx")
            path_excel = os.path.join(presupuestos_path, "Presupuesto.xlsx")
            sheet_to_df = {'Flujo de caja': df_agrupado, 'Desglose': df_total}
            # Guardar DataFrame como archivo Excel
            save_dfs_to_excel(path_excel, sheet_to_df)

            print(message_print(f"Se generó el archivo {os.path.basename(path_excel)} con la información de ingresos y egresos"))
            
        else:
            print("Entrada no válida. Por favor, escribe 1 o 2.")    
    



if __name__ == "__main__":
    folder_root = os.getcwd()
    # 1) Añade al path la carpeta donde está df_multi_match.py
    #libs_dir = os.path.join(folder_root, "Library")
    #sys.path.insert(0, libs_dir)
    # 2) Ahora importa la función directamente
    #from chrome_driver_load import load_chrome
    # 3) Llama a tu función pasándola como parámetro
    business_management(folder_root)
    