# Check whether a UNIHIKER M10 is reachable. The computer needs OpenSSH, not Python.
# Usage: .\check_connection.ps1
#       .\check_connection.ps1 -M10Host 192.168.199.102

param(
    [string]$M10Host = "10.1.2.3",
    [string]$User = "root"
)

$ErrorActionPreference = "Continue"

if ($M10Host -notmatch '^[A-Za-z0-9.-]+$' -or $User -notmatch '^[A-Za-z0-9._-]+$') {
    Write-Host "FAIL: The SSH host or user name contains unsupported characters." -ForegroundColor Red
    exit 1
}

Write-Host "=== UNIHIKER M10 connection check ===" -ForegroundColor Cyan
Write-Host "Target: ${User}@${M10Host}"
Write-Host ""

# 1. Ping
Write-Host "[1/2] Ping $M10Host ..."
$ping = ping -n 1 -w 1500 $M10Host 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: Ping failed. Check the USB cable or confirm both devices are on the same Wi-Fi network." -ForegroundColor Red
    exit 1
}
Write-Host "OK: Ping succeeded" -ForegroundColor Green

# 2. SSH and M10 Python library check
Write-Host "[2/2] Checking SSH (the factory-default password is dfrobot)..."
$remoteCmd = 'hostname && python3 --version && python3 -c "import unihiker, pinpong; print(1)"'
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "${User}@${M10Host}" $remoteCmd
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: The SSH or M10 Python library check failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "UNIHIKER M10 connected @ $M10Host" -ForegroundColor Green
exit 0
