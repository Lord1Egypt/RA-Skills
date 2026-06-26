#!/bin/bash
# setup.sh — Configura cifrado age para OpenClaw workspace
# Ejecutar UNA SOLA VEZ después de clonar el repo

set -euo pipefail

echo "[*] Configurando cifrado age para OpenClaw workspace..."

# 1. Generar par de llaves
AGE_DIR="$HOME/.age"
mkdir -p "$AGE_DIR"
chmod 700 "$AGE_DIR"

if [ ! -f "$AGE_DIR/key.txt" ]; then
    age-keygen -o "$AGE_DIR/key.txt"
    echo "[✓] Par de llaves generado en $AGE_DIR/key.txt"
else
    echo "[!] Ya existe $AGE_DIR/key.txt, se reutiliza"
fi

PUBKEY=$(head -2 "$AGE_DIR/key.txt" | grep "^# public key:" | sed 's/.*: //')
echo "[i] Clave pública: $PUBKEY"
echo "[i] GUARDA ESTA CLAVE para compartir con otros hosts:"
echo "    $PUBKEY"

# 2. Crear scripts helper
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
cat > "$SCRIPTS_DIR/decrypt.sh" << 'HELPER'
#!/bin/bash
set -euo pipefail
AGE_FILE="${1:-}"
[ -z "$AGE_FILE" ] && { echo "Uso: $0 <archivo.age>" >&2; exit 1; }
[ ! -f "$AGE_FILE" ] && { echo "No existe: $AGE_FILE" >&2; exit 1; }
age -d -i "$HOME/.age/key.txt" "$AGE_FILE"
HELPER
chmod +x "$SCRIPTS_DIR/decrypt.sh"

cat > "$SCRIPTS_DIR/encrypt.sh" << 'HELPER'
#!/bin/bash
set -euo pipefail
OUT="${1:-}"
[ -z "$OUT" ] && { echo "Uso: echo secreto | $0 <archivo.age>" >&2; exit 1; }
PUBKEY=$(head -2 "$HOME/.age/key.txt" | grep "^# public key:" | sed 's/.*: //')
[ -z "$PUBKEY" ] && { echo "No se pudo leer clave pública" >&2; exit 1; }
age -r "$PUBKEY" > "$OUT"
HELPER
chmod +x "$SCRIPTS_DIR/encrypt.sh"

echo "[✓] Scripts helper creados en $SCRIPTS_DIR/"
echo ""
echo "[*] AHORA: cifra tus secrets manualmente:"
echo "    echo 'export API_KEY=xxx' | $SCRIPTS_DIR/encrypt.sh $SCRIPTS_DIR/secrets.env.age"
echo "    rm -f /ruta/al/archivo.original"
echo ""
echo "[*] Para descifrar:"
echo "    source <($SCRIPTS_DIR/decrypt.sh $SCRIPTS_DIR/secrets.env.age)"
