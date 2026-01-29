import os
import subprocess
import pandas as pd
from datetime import datetime

def run_lab():
    print("🚀 Iniciando Laboratorio Purple Team...")
    
    # 1. Ejecutar Red Team (Generador de logs)
    print("🔴 [Red Team] Simulando ataques...")
    subprocess.run(["python3", "red_generator.py"])
    
    # 2. Ejecutar Blue Team (Analizador de logs)
    print("🔵 [Blue Team] Ejecutando detección y generando gráfica...")
    subprocess.run(["python3", "blue_analyzer.py"])
    
    # 3. Recopilar resultados para el Dashboard
    if not os.path.exists("auth_simulated.log"):
        print("❌ Error crítico: No se generó el archivo de logs.")
        return

    df = pd.read_csv("auth_simulated.log", sep=" ")
    total_logs = len(df)
    
    # Leer alertas del Blue Team (archivo alerts.csv)
    if os.path.exists("alerts.csv") and os.path.getsize("alerts.csv") > 0:
        alerts_df = pd.read_csv("alerts.csv")
        # Convertimos la tabla a formato Markdown
        tabla_ips = alerts_df.to_markdown(index=False)
        num_alertas = len(alerts_df)
    else:
        tabla_ips = "*No se detectaron IPs maliciosas bajo los criterios actuales.*"
        num_alertas = 0

    # 4. Construir el contenido del SUMMARY.md
    markdown_content = f"""
# 🛡️ Panel de Control - Purple SIEM Lab
*Generado automáticamente el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*

## 📊 Resumen de la Operación
| Métrica | Valor |
| :--- | :--- |
| **Total de Eventos Analizados** | {total_logs} |
| **IPs Sospechosas Detectadas** | {num_alertas} |
| **Estado de la Defensa** | {'⚠️ Incidente Detectado' if num_alertas > 0 else '✅ Sistema Seguro'} |

## 🚨 Detalle de Amenazas (Fuerza Bruta)
{tabla_ips}

## 🚩 Evidencia Forense
La siguiente gráfica muestra la distribución de intentos fallidos. Las barras rojas indican IPs que superaron el umbral de seguridad definido.

![Gráfica de Detección](deteccion_ataque.png)

---
**Entorno de ejecución:** {os.uname().nodename} (Linux Mint 22.3 Zena)
*Proyecto para Portafolio de Ciberseguridad.*
"""
    
    # Guardar el reporte
    with open("SUMMARY.md", "w") as f:
        f.write(markdown_content)
    
    print("\n" + "="*40)
    print("✅ PROCESO COMPLETADO CON ÉXITO")
    print(f"📄 Reporte: SUMMARY.md")
    print(f"🖼️  Gráfica: deteccion_ataque.png")
    print("="*40)
    
    # Abrir el resumen automáticamente en el visor de Mint
    try:
        subprocess.run(["xdg-open", "SUMMARY.md"])
    except:
        print("📖 Resumen generado. Puedes abrir 'SUMMARY.md' manualmente.")

if __name__ == "__main__":
    run_lab()
