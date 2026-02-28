# Proyecto 6: Computer Vision

# Sistema de Seguridad con Reconocimiento Facial (Simulado)

## Descripción del proyecto
Este proyecto utiliza Visión por Computadora de última generación para transformar una cámara web común en un centinela de seguridad inteligente. A diferencia de los detectores de movimiento simples, este sistema "entiende" quién tiene permiso de estar en casa y quién es un extraño.

Funciones principales:

    - Detecta si la persona que ingresa al hogar es un **residente registrado**.  
    - Identifica **intrusos** que no están registrados.  
    - Guarda fotos de intrusos en la carpeta `intruders/`.  
    - Registra cada detección en un archivo `detections.log`.  
    - Simula **alertas por correo** cuando se detecta un intruso.  
    - Muestra un **dashboard en tiempo real** con conteo de residentes e intrusos detectados.  
    - Usa automáticamente la **cámara interna de la computadora** en macOS y Windows.  

> Nota: Las alertas de correo son simuladas para fines académicos.

Cómo funciona el cerebro del sistema?
El sistema opera en un ciclo de cuatro etapas críticas que ocurren en milisegundos:

Captura y Pre-procesamiento: El código toma el video de la cámara y utiliza un algoritmo de OpenCV para localizar rostros. No analiza todo el cuarto, solo los píxeles donde hay una cara humana.

Extracción de ADN Facial (Embeddings): Utiliza el modelo Facenet512. Convierte tu rostro en una lista de 512 números únicos. Es como una "huella digital" pero de tu cara.

Comparación Vectorial: El sistema compara esos números contra las fotos en la carpeta residents/ usando Similitud de Coseno. No busca una coincidencia exacta de píxeles (que fallaría con la luz), sino que mide el ángulo de tus rasgos.

Acción e Identificación: * Verde (Residente): Si la similitud es alta, te etiqueta con tu nombre.

Rojo (Intruso): Si la similitud es baja o nula, el sistema entra en Modo de Alerta Inmediata.

## Configuración de Carpetas (Estructura)
El proyecto ya incluye las carpetas necesarias. Aquí es donde tú actúas:

## Carpeta residents/ (Tu pase de entrada)
Para que el sistema sea 100% fiable y no te marque como intruso al mover la cabeza, debes guardar exactamente 5 fotos tuyas (puedes usar la cámara de tu celular o la misma laptop):

    - frente.jpg: Mirando directo a la lente, expresión neutra.

    - izquierda.jpg: Girando la cabeza unos 30 grados a la izquierda.

    - derecha.jpg: Girando la cabeza unos 30 grados a la derecha.

    - arriba.jpg: Inclinando la cabeza un poco hacia arriba.

    - lejos.jpg: Una foto de cuerpo medio, a 2 metros de la cámara.

Nota: Si hay más personas viviendo contigo, repite este proceso para cada una (ej. mama_frente.jpg, papa_frente.jpg).

## Carpeta intruders/ (Evidencia)
Aquí es donde el sistema guarda las "pruebas". Si el sistema detecta a alguien que no está en la carpeta de residentes:

    - Captura Instantánea: Toma una foto del intruso en el momento exacto.

    - Registro de Tiempo: Guarda el archivo con la fecha y hora exacta (ej. ALERTA_20241025_1530.jpg).

    - Registro Log: Escribe en detections.log para tener un historial de seguridad.

---

## Requisitos del sistema

- Python 3.9 o superior  
- Cámara conectada a la computadora  
- Conexión a internet la primera vez que se ejecuta (para descargar modelos de DeepFace)

---

## Librerías necesarias
Todas las librerías se instalan usando `pip` y están en `requirements.txt`.  

**Contenido de requirements.txt:**