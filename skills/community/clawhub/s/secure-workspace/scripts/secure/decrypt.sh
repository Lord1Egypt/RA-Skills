#!/bin/bash
# decrypt.sh — descifra un archivo .age y lo muestra por stdout
# Uso: decrypt.sh <archivo.age>
# La clave privada debe estar en /root/.age/key.txt

set -euo pipefail
AGE_FILE="${1:-}"
[ -z "$AGE_FILE" ] && { echo "Uso: $0 <archivo.age>" >&2; exit 1; }
[ ! -f "$AGE_FILE" ] && { echo "No existe: $AGE_FILE" >&2; exit 1; }

age -d -i /root/.age/key.txt "$AGE_FILE"
