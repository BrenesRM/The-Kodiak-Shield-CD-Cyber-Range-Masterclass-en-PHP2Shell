#!/usr/bin/env python3
"""
================================================================================
LABORATORIO DE HACKING ÉTICO: ANÁLISIS DE FALLAS EN EL CORE DE PHP (PHP2SHELL)
Script de Diagnóstico, Fuzzing de Límites de Memoria y Auditoría Blue Team
Basado en: CVE-2026-109618 y CVE-2026-109619
================================================================================
"""

import sys
import time
import json
import argparse
import urllib.request
import urllib.error

BANNER = r"""
  ___  _   _ ____ ____  ____  _          _ _ 
 |  _ \| | | |  _ \___ \/ ___|| |__   ___| | |
 | |_) | |_| | |_) |__) \___ \| '_ \ / _ \ | |
 |  __/|  _  |  __// __/ ___) | | | |  __/ | |
 |_|   |_| |_|_|  |_____|____/|_| |_|\___|_|_|
 [ Kodiak Shield CD Cyber Range - Diagnostic & Audit Suite ]
"""

def print_banner():
    print(BANNER)

def check_target_recon(target_url):
    print("\n" + "="*60)
    print(" [FASE 1: RECONOCIMIENTO Y ANÁLISIS DE RUNTIME]")
    print("="*60)
    print(f"[*] Conectando a {target_url}...")
    
    try:
        req = urllib.request.Request(target_url, headers={"User-Agent": "CyberRange-Recon/1.0"})
        with urllib.request.urlopen(req, timeout=5) as res:
            raw_data = res.read().decode('utf-8')
            try:
                data = json.loads(raw_data)
                print(f"[+] Estado del Servicio      : {data.get('system', data.get('service', 'Online'))}")
                print(f"[+] Versión de PHP           : {data.get('php_version', 'Desconocida')}")
                print(f"[+] SAPI                     : {data.get('sapi', 'Desconocido')}")
                print(f"[+] memory_limit             : {data.get('memory_limit')}")
                print(f"[+] post_max_size            : {data.get('post_max_size')}")
                print(f"[+] session.upload_progress  : {data.get('session_upload_progress_enabled', data.get('session_upload_progress'))}")
                
                # Evaluación preliminar de vulnerabilidad
                php_ver = data.get('php_version', '')
                if "8.4.26" in php_ver:
                    print("\n[!] ALERTA DE SEGURIDAD:")
                    print("    Versión detectada: PHP 8.4.26 (VULNERABLE a CVE-2026-109618 / 109619).")
                    print("    El runtime contiene el defecto de recuperación por longjmp() en OOM.")
                elif "8.4.27" in php_ver:
                    print("\n[OK] ESTADO SEGURO:")
                    print("    Versión detectada: PHP 8.4.27 (PARCHEADA contra PHP2Shell).")
                
                return data
            except json.JSONDecodeError:
                print(f"[+] Respuesta recibida (no JSON):\n{raw_data[:200]}...")
                return {}
    except Exception as e:
        print(f"[-] Error de conexión con el objetivo: {e}")
        return None

def test_multipart_boundary(target_url, size_mb=1):
    print("\n" + "="*60)
    print(f" [FASE 2: PRUEBA DE PARSEO MULTIPART / FORM-DATA ({size_mb} MB)]")
    print("="*60)
    
    boundary = "---------------------------CyberRangeAuditBoundary98765"
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "CyberRange-SecurityAuditor/2.0"
    }

    dummy_body = b"B" * (size_mb * 1024 * 1024)
    payload = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="diagnostic_field"\r\n\r\n'
        f"payload_audit_test\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="sample_file"; filename="audit_blob.bin"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode('utf-8') + dummy_body + f"\r\n--{boundary}--\r\n".encode('utf-8')

    print(f"[*] Enviando paquete multipart simulado ({round(len(payload) / (1024*1024), 2)} MB)...")
    start_time = time.time()
    
    try:
        req = urllib.request.Request(target_url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as res:
            elapsed = round(time.time() - start_time, 2)
            print(f"[+] Petición completada en {elapsed}s.")
            print(f"[+] Código de Respuesta HTTP: {res.status} OK")
            print("    -> El servidor procesó la petición sin abortar el worker.")
    except urllib.error.HTTPError as e:
        elapsed = round(time.time() - start_time, 2)
        print(f"[!] Respuesta del Servidor: HTTP {e.code} ({e.reason}) en {elapsed}s")
        
        if e.code == 403:
            print("\n[ESCUDO BLUE TEAM ACTIVO]")
            print(" -> El servidor Web frontal (NGINX/WAF) interceptó la cabecera multipart.")
            print(" -> La petición fue descartada ANTES de alcanzar el motor PHP-FPM.")
            print(" -> Mitigación perimetral exitosa (Slide 13 del PDF).")
        elif e.code == 502:
            print("\n[ALERTA DE CAÍDA EN WORKER / OOM]")
            print(" -> Error 502 Bad Gateway: PHP-FPM cerró el socket abruptamente.")
            print(" -> Esto ocurre cuando el worker de PHP colapsa por OOM durante el parseo.")
            print(" -> En versiones vulnerables, esto activa la condición de longjmp() sin limpieza.")
        elif e.code == 504:
            print("\n[TIMEOUT DETECTADO]")
            print(" -> Gateway Timeout: El proceso no respondió en el tiempo asignado.")
    except Exception as e:
        print(f"[-] Fallo en la comunicación de red: {e}")

def verify_blue_team_mitigations(target_url):
    print("\n" + "="*60)
    print(" [FASE 3: VERIFICACIÓN DE MITIGACIONES BLUE TEAM]")
    print("="*60)
    
    print("[*] Verificando bloqueo perimetral de multipart/form-data...")
    boundary = "----TestBoundaryMitigationCheck"
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    dummy_payload = f"--{boundary}--\r\n".encode('utf-8')
    
    try:
        req = urllib.request.Request(target_url, data=dummy_payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5) as res:
            print(f"[-] ADVERTENCIA: La petición multipart fue ACEPTADA (HTTP {res.status}).")
            print("    La mitigación en NGINX/Apache NO está activa o no está filtrando.")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("[+] CONFIRMADO: Regla NGINX 403 Forbidden activa para multipart/form-data.")
        else:
            print(f"[?] Código retornado: {e.code}")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Auditoría Educativa PHP2Shell")
    parser.add_argument("--target", default="http://localhost:80", help="URL del objetivo (ej. http://target-web:80 o http://vulnerable-php:80)")
    parser.add_argument("--size", type=int, default=2, help="Tamaño en MB para la prueba de carga multipart (default: 2)")
    parser.add_argument("--check-mitigation", action="store_true", help="Comprueba si las mitigaciones de Blue Team están activas")
    
    args = parser.parse_args()
    
    recon = check_target_recon(args.target)
    if not recon:
        sys.exit(1)
        
    if args.check_mitigation:
        verify_blue_team_mitigations(args.target)
    else:
        test_multipart_boundary(args.target, size_mb=args.size)

if __name__ == "__main__":
    main()
