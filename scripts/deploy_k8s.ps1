# ==============================================================================
# Script de Despliegue Automatizado - Laboratorio K8s PHP2Shell
# ==============================================================================
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " [KODIAK SHIELD CD CYBER RANGE] DESPLEGANDO LABORATORIO K8S" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

$k8sDir = Join-Path $PSScriptRoot "..\k8s"

# 1. Crear namespace y cuotas
Write-Host "`n[*] 1. Aplicando Namespace y ResourceQuota..." -ForegroundColor Green
kubectl apply -f "$k8sDir\00-namespace.yaml"

# 2. Configurar contexto
Write-Host "[*] 2. Configurando contexto actual al namespace php2shell-sandbox..." -ForegroundColor Green
kubectl config set-context --current --namespace=php2shell-sandbox

# 3. Desplegar Objetivo (Target PHP 8.4.26-FPM + Nginx)
Write-Host "[*] 3. Desplegando Target Pod (PHP 8.4.26 vulnerable)..." -ForegroundColor Green
kubectl apply -f "$k8sDir\01-target-pod.yaml"

# 4. Desplegar Atacante (Kali Linux)
Write-Host "[*] 4. Desplegando Attacker Pod (Kali Linux)..." -ForegroundColor Green
kubectl apply -f "$k8sDir\02-attacker-pod.yaml"

# 5. Aplicar políticas de red de aislamiento
Write-Host "[*] 5. Aplicando políticas de aislamiento de red (NetworkPolicy)..." -ForegroundColor Green
kubectl apply -f "$k8sDir\03-network-policy.yaml"

Write-Host "`n[+] Despliegue completado. Estado de los pods:" -ForegroundColor Cyan
kubectl get pods -n php2shell-sandbox

Write-Host "`nPara acceder a la terminal del pod atacante ejecute:" -ForegroundColor Yellow
Write-Host "kubectl exec -it attacker-pod -n php2shell-sandbox -- /bin/bash" -ForegroundColor White
