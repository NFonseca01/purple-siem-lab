import pandas as pd
import random
from datetime import datetime, timedelta

# 1. Configuración del escenario
n_entries = 1000
log_data = []
start_time = datetime.now()

# IPs simuladas para el laboratorio
attacker_ip = "192.168.1.50"
user_ips = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]

print("🔴 [Red Team] Iniciando generación de logs sintéticos...")

# 2. Bucle de generación de eventos
for i in range(n_entries):
    # Generar marca de tiempo realista (intervalos de 1 a 60 segundos)
    current_time = start_time + timedelta(seconds=i * random.randint(1, 60))
    
    # SIMULACIÓN DE ATAQUE: Entre el evento 500 y 550 forzamos un ataque de fuerza bruta
    if 500 <= i <= 550:
        ip = attacker_ip
        status = "Failed"
        user = "admin"
    else:
        # Actividad normal: mezclar logins exitosos y algunos fallos humanos
        ip = random.choice(user_ips)
        status = "Accepted" if random.random() > 0.1 else "Failed"
        user = "usuario_normal"

    # CONSTRUCCIÓN DE LA FILA: Exactamente 8 elementos para coincidir con el DataFrame
    log_data.append([
        current_time.strftime('%b'),       # Month
        current_time.strftime('%d'),       # Day
        current_time.strftime('%H:%M:%S'), # Time
        "localhost",                       # Hostname
        f"sshd[{random.randint(1000, 9000)}]:", # Process
        status,                            # Status
        user,                              # User
        ip                                 # IP
    ])

# 3. Creación del DataFrame y exportación
# Definimos exactamente 8 nombres de columna
columnas = ['Month', 'Day', 'Time', 'Hostname', 'Process', 'Status', 'User', 'IP']

try:
    df = pd.DataFrame(log_data, columns=columnas)
    # Guardamos con separador de espacio para emular el formato auth.log
    df.to_csv("auth_simulated.log", index=False, sep=" ")
    print("✅ Red Team: 'auth_simulated.log' generado con éxito (8 columnas).")
except Exception as e:
    print(f"❌ Error al generar el DataFrame: {e}")
