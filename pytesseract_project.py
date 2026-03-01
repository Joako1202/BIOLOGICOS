import cv2
import pytesseract
import re
import os

# 1. CONFIGURACIÓN DEL MOTOR (Ruta obligatoria en Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extraer_coordenadas_gps(ruta_imagen):
    """
    Carga una imagen, la procesa y extrae variables Este (mE) y Norte (mN).
    """
    # Verificamos si el archivo existe para evitar errores
    if not os.path.exists(ruta_imagen):
        return None, None, f"Error: No se encuentra el archivo en {ruta_imagen}"

    # 2. LECTURA Y PREPROCESAMIENTO
    # Cargamos la imagen original
    imagen = cv2.imread(ruta_imagen)
    
    # La convertimos a escala de grises para que el OCR lea mejor los números
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # 3. EJECUCIÓN DEL OCR
    # Usamos lang='spa' si lo tienes instalado, si no, puedes quitar ese parámetro
    try:
        texto_extraido = pytesseract.image_to_string(gris, lang='spa')
    except:
        texto_extraido = pytesseract.image_to_string(gris)

    # 4. BÚSQUEDA DE COORDENADAS CON REGEX (PATRONES)
    # Buscamos números (\d+) seguidos de mE o mN (ignorando mayúsculas/minúsculas)
    # El \s* permite que haya espacios accidentales detectados por el OCR
    patron_este = re.search(r"(\d+)\s*\w*E", texto_extraido, re.IGNORECASE)
    patron_norte = re.search(r"(\d+)\s*\w*N", texto_extraido, re.IGNORECASE)

    # 5. ASIGNACIÓN A VARIABLES
    # Si encuentra el patrón, extrae solo el número (group 1)
    v_este = patron_este.group(1) if patron_este else "No detectado"
    v_norte = patron_norte.group(1) if patron_norte else "No detectado"

    return v_este, v_norte, texto_extraido

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == "__main__":
    # Define aquí la ruta de tu foto
    mi_foto = r"C:\Users\Joaquin\Documents\PROYECTOS PYTHON\20250829_080614.jpg"
    
    este, norte, texto_completo = extraer_coordenadas_gps(mi_foto)

    print("-" * 30)
    print(f"RESULTADOS DE LA IMAGEN:")
    print(f"Coordenada ESTE (mE): {este}")
    print(f"Coordenada NORTE (mN): {norte}")
    print("-" * 30)
    
    # Opcional: Descomenta la línea de abajo si quieres ver todo lo que leyó el OCR
    # print("Texto bruto detectado:", texto_completo)
