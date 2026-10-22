# ==============================================================================
# Script de Despliegue Automatizado - Docker Compose PHP2Shell
# ==============================================================================
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " [KODIAK SHIELD CD CYBER RANGE] DESPLEGANDO CON DOCKER COMPOSE" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

$dockerDir = Join-Path $PSScriptRoot "..\docker-compose"

Write-Host "`n[*] Iniciando contenedores en red aislada..." -ForegroundColor Green
docker compose -f "$dockerDir\docker-compose.yml" up -d

Write-Host "`n[+] Contenedores activos:" -ForegroundColor Cyan
docker compose -f "$dockerDir\docker-compose.yml" ps

Write-Host "`nPara ingresar a la consola de Kali Linux ejecute:" -ForegroundColor Yellow
Write-Host "docker exec -it attacker-kali /bin/bash" -ForegroundColor White
