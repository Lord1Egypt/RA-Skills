#!/bin/bash
# encrypt.sh — cifra stdin a un archivo .age
# Uso: cat secreto | encrypt.sh <archivo_salida.age>
# Usa la clave pública del comentario de key.txt

set -euo pipefail
OUT="${1:-}"
[ -z "$OUT" ] && { echo "Uso: echo secreto | $0 <archivo.age>" >&2; exit 1; }

PUBKEY=$(head -2 /root/.age/key.txt | grep "^# public key:" | sed 's/.*: //')
[ -z "$PUBKEY" ] && { echo "No se pudo leer la clave pública de /root/.age/key.txt" >&2; exit 1; }

age -r "$PUBKEY" > "$OUT"
