# 🌐 VTP Injection Attack (PoC)

## 📌 Descripción del Proyecto
Este repositorio contiene una Prueba de Concepto (PoC) desarrollada en Python con Scapy, diseñada para demostrar las vulnerabilidades del protocolo VTP (VLAN Trunking Protocol). 

El script permite a un atacante inyectar paquetes VTP falsificados con un número de revisión más alto. Al procesar estos paquetes, los switches de la red actualizan su base de datos de VLANs, lo que permite al atacante **crear VLANs arbitrarias y borrar las VLANs legítimas existentes**, comprometiendo la disponibilidad de la red (DoS).

⚠️ *Aviso Legal: Esta herramienta fue desarrollada con fines estrictamente académicos y educativos. No debe ser utilizada en redes de producción sin autorización explícita.*

## ⚙️ Requisitos y Dependencias
* **Sistema Operativo:** Kali Linux (o cualquier distribución basada en Linux).
* **Dependencias:** Python 3 y la librería Scapy.
* **Red:** La interfaz de red del atacante debe estar conectada a un puerto en modo Troncal (Trunk) o ser capaz de negociar uno mediante DTP.

```bash
# Instalación de Scapy
pip install scapy
```
🚀 Uso de la Herramienta
Otorga permisos de ejecución al script:

Bash
`chmod +x vtp_attack.py`
Ejecuta el script con privilegios de administrador (requerido por Scapy para inyectar paquetes a nivel de enlace de datos):

Bash
`sudo python3 vtp_attack.py`
Sigue el menú interactivo para ingresar:

El dominio VTP objetivo (ej. itla).

La opción deseada (Crear VLAN o Borrar/Resetear).

El ID y Nombre de la VLAN.

El número de revisión inflado (debe ser mayor al actual del switch).

🛡️ Contramedidas
Para prevenir este tipo de ataques en entornos corporativos:

Implementar contraseñas de dominio VTP (vtp password <clave>).

Utilizar VTP versión 3.

Configurar los switches en modo transparente si no se requiere la propagación dinámica de VLANs (vtp mode transparent).

Deshabilitar la negociación dinámica de troncales (DTP) en puertos de usuario final.
