from deepface import DeepFace
import cv2
import os
from datetime import datetime
import numpy as np
import time

# --- CONFIGURACIÓN DE ALTA PRIORIDAD ---
RESIDENTS_DIR = "residents/"
INTRUDERS_DIR = "intruders/"
LOG_FILE = "detections.log"
COOLDOWN_ALERTA = 3 
UMBRAL_COSENO = 0.42 

# Asegurar carpetas
os.makedirs(RESIDENTS_DIR, exist_ok=True)
os.makedirs(INTRUDERS_DIR, exist_ok=True)

# Detector facial
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def cargar_base_datos():
    embs, filenames = [], []
    archivos = [f for f in os.listdir(RESIDENTS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not archivos:
        print("🚨 ATENCIÓN: No hay residentes registrados. Todo será marcado como INTRUSO.")
        return [], []
    
    print(f"🔄 Cargando {len(archivos)} imágenes de residentes...")
    for f in archivos:
        try:
            path = os.path.join(RESIDENTS_DIR, f)
            img_rep = DeepFace.represent(img_path=path, model_name="Facenet512", enforce_detection=True)
            embs.append(np.array(img_rep[0]["embedding"]))
            # Extraer nombre del archivo (ej: "juan_frente.jpg" -> "Juan")
            filenames.append(f.split('_')[0].capitalize())
        except Exception as e:
            print(f"Error cargando {f}: {e}")
    return embs, filenames

# Inicialización
resident_embs, resident_names = cargar_base_datos()
cap = cv2.VideoCapture(0)
ultima_captura = 0

# Variables para el Dashboard
contador_residentes = 0
contador_intrusos = 0
residentes_detectados_hoy = set() # Para no contar dos veces a la misma persona seguido

print("⚡ SISTEMA DE VIGILANCIA ACTIVO - RESPUESTA INMEDIATA")

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostros = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100))

    # Variable para saber si en este frame hay alguien
    hay_intruso_en_frame = False

    for (x, y, w, h) in rostros:
        rostro_img = frame[y:y+h, x:x+w].copy()
        nombre_display = "INTRUSO"
        color_display = (0, 0, 255) 
        es_residente = False

        if resident_embs:
            try:
                res = DeepFace.represent(rostro_img, model_name="Facenet512", 
                                       enforce_detection=False, detector_backend='opencv')
                target_emb = np.array(res[0]["embedding"])

                for i, res_emb in enumerate(resident_embs):
                    similitud = np.dot(target_emb, res_emb) / (np.linalg.norm(target_emb) * np.linalg.norm(res_emb))
                    
                    if similitud > UMBRAL_COSENO:
                        es_residente = True
                        nombre_display = f"RESIDENTE: {resident_names[i]}"
                        color_display = (0, 255, 0)
                        
                        # Dashboard: Contar residente único
                        if resident_names[i] not in residentes_detectados_hoy:
                            contador_residentes += 1
                            residentes_detectados_hoy.add(resident_names[i])
                        break 
            except:
                pass 

        # ACCIÓN SI ES INTRUSO
        if not es_residente:
            hay_intruso_en_frame = True
            ahora = time.time()
            if (ahora - ultima_captura) > COOLDOWN_ALERTA:
                timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                timestamp_file = datetime.now().strftime("%H%M%S_%f")
                
                # 1. Guardar Foto
                ruta_foto = os.path.join(INTRUDERS_DIR, f"ALERTA_{timestamp_file}.jpg")
                cv2.imwrite(ruta_foto, frame) 
                
                # 2. Registro en Log
                with open(LOG_FILE, "a") as f:
                    f.write(f"[{timestamp_str}] ALERTA: Intruso detectado - Foto: {ruta_foto}\n")
                
                # 3. Simulación de Correo y Alerta
                print(f"⚠️ ¡INTRUSO! Captura guardada. 📧 SIMULACIÓN: Correo de alerta enviado a seguridad.")
                
                contador_intrusos += 1
                ultima_captura = ahora

        # UI: Cuadro y Nombre
        cv2.rectangle(frame, (x, y), (x+w, y+h), color_display, 2)
        cv2.putText(frame, nombre_display, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_display, 2)

    # --- DASHBOARD EN TIEMPO REAL ---
    # Fondo para el contador
    cv2.rectangle(frame, (0, 0), (300, 80), (0, 0, 0), -1)
    cv2.putText(frame, f"Residentes: {contador_residentes}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Intrusos: {contador_intrusos}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("SISTEMA DE SEGURIDAD CRITICO", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()