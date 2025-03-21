import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Lectura y carga de la imagen seleccionada 
ruta_carpeta = "C:/Users/cacer/Desktop/TERCER CORTE/Dataset"
nombre_imagen = 'img2.jpg'
ruta_completa = os.path.join(ruta_carpeta, nombre_imagen)
img = cv2.imread(ruta_completa)

if img is None:
    print("Error: No se pudo cargar la imagen. Verifica la ruta.")
    exit()

# Dimensiones que tiene dicha imagen como ancho y altura
height, width, channels = img.shape
print("Dimensiones de la imagen:")
print("Ancho:", width)
print("Altura:", height)

# Redimensionar la imagen con un nuevo ancho y un nuevo alto, del mismo modo se evidencia los tres canales de la imagen (RGB)
imagen = cv2.resize(img, (404, 303), interpolation=cv2.INTER_AREA)
print(imagen.shape)

# Cambiar la imagen a un solo canal, esto con la función de convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar las derivadas de Sobel en ejes x y y. Esta línea calcula el gradiente en dirección x de la imagen que previamente 
# se convirtió a escala de grises. cv2.CV_64F, nos dice el tipo de datos de salida para el gradiente (en este caso, números de 
# punto flotante de 64 bits). Los números 1 y 0, especifican que calcularemos el gradiente en dirección x (horizontal) y no en 
# dirección y (vertical). ksize = 3 es el tamaño del kernel usado para hacer el cálculo del gradiente

def detectar_bordes_sobel(imagen_gris):
    gradiente_x = cv2.Sobel(imagen_gris, cv2.CV_64F, 1, 0, ksize=3)
    gradiente_y = cv2.Sobel(imagen_gris, cv2.CV_64F, 0, 1, ksize=3)
    
    # Calculamos la magnitud del gradiente con el np.sqrt que nos permite calcular la raíz cuadrada de cada variable 
    # en la que se almacena el gradiente vertical y horizontal elevados respectivamente al cuadrado, con el operador **
    magnitud_gradiente = np.sqrt(gradiente_x**2 + gradiente_y**2)
    
    # Aplicar umbral para obtener los bordes de la imagen. Los bordes se marcan como píxeles blancos (255) en la imagen 
    # resultante, mientras que el resto de la imagen se representa como píxeles negros (0).
    umbral = np.max(magnitud_gradiente) * 0.1
    bordes = np.uint8(magnitud_gradiente > umbral) * 255
    
    cantidad_bordes_total = np.sum(bordes) // 255
    
    # Obtener la región de interés (ROI) desde el 55% de la imagen hacia arriba. Para nuestro caso, es evidente que 
    # deseamos hacer una detección de accesorio que presenta la persona en la imagen, es decir que este accesorio lo 
    # encontraremos desde la mitad de la imagen hacia arriba.
    altura_roi = int(bordes.shape[0] * 0.55)
    roi = bordes[:altura_roi, :]
    
    cantidad_bordes_roi = np.sum(roi) // 255
    
    return bordes, cantidad_bordes_total, cantidad_bordes_roi

bordes, cantidad_bordes_total, cantidad_bordes_roi = detectar_bordes_sobel(imagen_gris)

# Determinar clasificación teniendo en cuenta los valores de píxeles de borde y región de interés que arroja el programa
# en python de cada imagen dependiendo del tipo de accesorio que posee la persona: Normal, gafas y gorra, se creó una 
# hoja de cálculo en Excel que permitió recoger estos valores de cada imagen, para así tener una estadística que permitiera 
# generar unos rangos específicos, categorizando los parámetros máximos y mínimos con el fin de que el programa detectara 
# correctamente el tipo de accesorio que se muestra en la imagen.
if 7000 <= cantidad_bordes_total <= 7899 and 3050 <= cantidad_bordes_roi <= 3590:
    clasificacion = "NORMAL (Sin accesorios)"
elif 8295 <= cantidad_bordes_total <= 9050 and 4105 <= cantidad_bordes_roi <= 4760:
    clasificacion = "GAFAS"
elif 7900 <= cantidad_bordes_total <= 8550 and 3210 <= cantidad_bordes_roi <= 3680:
    clasificacion = "GORRA"
else:
    clasificacion = "No se pudo determinar"

# Imprimir clasificación en la terminal
print(f"La persona tiene {clasificacion}")

# Crear una figura con 3 subgráficos en una fila
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Imagen en escala de grises
axes[0].imshow(imagen_gris, cmap='gray')
axes[0].set_title("Imagen en Escala de Grises")
axes[0].axis('off')

# Imagen original
axes[1].imshow(cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
axes[1].set_title("Imagen Original")
axes[1].axis('off')

# Imagen con bordes detectados + Clasificación
axes[2].imshow(bordes, cmap='gray')
axes[2].set_title(f'Cantidad total de bordes: {cantidad_bordes_total}, ROI: {cantidad_bordes_roi}\n\nLa persona tiene {clasificacion}')
axes[2].axis('off')

# Ajustar el diseño para evitar solapamientos
plt.tight_layout()
plt.show()