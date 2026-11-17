#!/usr/bin/env bash
# Script determinista para inspección y simulación de actualizaciones en WSL.
# Modo simulación: ejecuta consultas de solo lectura y dry-run (-s). No instala paquetes.

set -euo pipefail

output_json="{}"

# 1. Información de la distribución
os_id="unknown"
os_version="unknown"
os_codename="unknown"
if [ -f /etc/os-release ]; then
    # shellcheck source=/dev/null
    . /etc/os-release
    os_id="${ID:-unknown}"
    os_version="${VERSION_ID:-unknown}"
    os_codename="${VERSION_CODENAME:-unknown}"
fi

# 2. Detección de gestor de paquetes y actualizaciones
pkg_manager="unknown"
upgrades="[]"
installed_pkgs="[]"

if command -v apt-get >/dev/null 2>&1; then
    pkg_manager="apt"
    # Consultar actualizaciones simuladas (dry-run)
    # Distinguir actualizaciones de seguridad (origen security.ubuntu.com o debian-security)
    upgrades=$(apt-get -s dist-upgrade 2>/dev/null | awk '
        /^Inst / {
            pkg=$2;
            # Formato: Inst pkg [current] (target source)
            match($0, /\(([^ ]+) ([^\)]+)\)/, m);
            target=m[1];
            source=m[2];
            is_sec = (source ~ /security/ ? "true" : "false");
            printf "{\"name\":\"%s\",\"id\":\"%s\",\"target_version\":\"%s\",\"source\":\"%s\",\"is_security\":%s}\n", pkg, pkg, target, source, is_sec;
        }
    ' | jq -s . 2>/dev/null || echo "[]")
elif command -v dnf >/dev/null 2>&1; then
    pkg_manager="dnf"
    upgrades=$(dnf check-update -q 2>/dev/null | awk '{if (NF>=3) printf "{\"name\":\"%s\",\"id\":\"%s\",\"target_version\":\"%s\",\"source\":\"dnf\",\"is_security\":false}\n", $1, $1, $2}' | jq -s . 2>/dev/null || echo "[]")
elif command -v apk >/dev/null 2>&1; then
    pkg_manager="apk"
fi

# 3. Comprobación de reinicio pendiente
reboot_pending=false
if [ -f /var/run/reboot-required ]; then
    reboot_pending=true
fi

# 4. Servicios configurados pasados como argumentos
services_status="{}"
if [ "$#" -gt 0 ]; then
    for srv in "$@"; do
        status="inactive"
        if command -v systemctl >/dev/null 2>&1; then
            if systemctl is-active "$srv" >/dev/null 2>&1; then
                status="active"
            fi
        elif command -v service >/dev/null 2>&1; then
            if service "$srv" status >/dev/null 2>&1; then
                status="active"
            fi
        fi
        services_status=$(echo "$services_status" | jq --arg s "$srv" --arg st "$status" '.[$s] = $st' 2>/dev/null || echo "{}")
    done
fi

cat <<EOF
{
  "os_id": "$os_id",
  "os_version": "$os_version",
  "os_codename": "$os_codename",
  "pkg_manager": "$pkg_manager",
  "reboot_pending": $reboot_pending,
  "upgrades": $upgrades,
  "services": $services_status
}
EOF
