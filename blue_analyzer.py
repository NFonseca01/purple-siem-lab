import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_logs():
    print("🔵 [Blue Team] Iniciando análisis de logs...")
    
    # 1. Cargar los datos
    log_file = "auth_simulated.log"
    if not os.path.exists(log_file):
        print(f"❌ Error: No se encuentra {log_file}. Ejecuta primero el Red Team.")
        return

    # Leer el log (usando espacio como separador según nuestro generador)
    df = pd.read_csv(log_file, sep=" ")

    # 2. Lógica de Detección
    # Filtramos por estado 'Failed' y contamos ocurrencias por IP
    failed_attempts = df[df['Status'] == 'Failed'].groupby('IP').size().reset_index(name='intentos')
    
    # 3. Definir Umbral de Alerta
    UMBRAL = 10
    sospechosos = failed_attempts[failed_attempts['intentos'] > UMBRAL]

    # 4. Exportar hallazgos para el Dashboard (Importante para el resumen)
    sospechosos.to_csv("alerts.csv", index=False)
    
    print(f"🚨 Análisis completado. Se detectaron {len(sospechosos)} IPs sobre el umbral.")

    # 5. Generación de Visualización (Impacto visual para GitHub)
    plt.figure(figsize=(10, 6))
    
    # Colorear de rojo las IPs que superan el umbral
    colors = ['red' if x > UMBRAL else 'skyblue' for x in failed_attempts['intentos']]
    
    plt.bar(failed_attempts['IP'], failed_attempts['intentos'], color=colors)
    plt.axhline(y=UMBRAL, color='darkred', linestyle='--', label=f'Umbral de Alerta ({UMBRAL})')
    
    plt.title('Detección de Fuerza Bruta: Intentos Fallidos por IP', fontsize=14)
    plt.xlabel('Dirección IP Source', fontsize=12)
    plt.ylabel('Cantidad de Intentos', fontsize=12)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar sin mostrar (para no detener el script purple_dashboard.py)
    plt.savefig("deteccion_ataque.png")
    print("📊 Gráfica 'deteccion_ataque.png' guardada con éxito.")

if __name__ == "__main__":
    analyze_logs()
