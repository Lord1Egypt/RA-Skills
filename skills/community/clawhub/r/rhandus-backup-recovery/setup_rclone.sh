#!/bin/bash
# 🔧 Script de configuración rClone para Google Drive
# Para backups diarios de OpenClaw

set -e

echo "🔄 Configurando rClone para Google Drive..."
echo "=========================================="

# Verificar rClone instalado
if ! command -v rclone &> /dev/null; then
    echo "❌ rClone no encontrado. Instalar primero:"
    echo "   sudo apt install rclone"
    exit 1
fi

echo "✅ rClone encontrado: $(rclone version | head -1)"

# Crear configuración interactiva
echo ""
echo "📋 Configuración de Google Drive para backups:"
echo "--------------------------------------------"

# Solicitar información
read -p "Nombre del remote [tiklick-drive]: " REMOTE_NAME
REMOTE_NAME=${REMOTE_NAME:-tiklick-drive}

echo ""
echo "🔐 Para configurar Google Drive, necesitas:"
echo "1. Ir a https://console.cloud.google.com/"
echo "2. Crear proyecto o usar existente"
echo "3. Habilitar Google Drive API"
echo "4. Crear credenciales OAuth 2.0"
echo "5. Obtener Client ID y Client Secret"
echo ""

read -p "Client ID: " CLIENT_ID
read -p "Client Secret: " CLIENT_SECRET

echo ""
echo "📁 Configurando remote '${REMOTE_NAME}'..."

# Crear configuración rClone
rclone config create "${REMOTE_NAME}" drive \
    client_id "${CLIENT_ID}" \
    client_secret "${CLIENT_SECRET}" \
    scope "drive.file" \
    root_folder_id "" \
    --all

if [ $? -eq 0 ]; then
    echo "✅ Remote '${REMOTE_NAME}' configurado exitosamente"
else
    echo "❌ Error configurando remote"
    exit 1
fi

# Probar conexión
echo ""
echo "🔗 Probando conexión a Google Drive..."
rclone lsd "${REMOTE_NAME}:"

if [ $? -eq 0 ]; then
    echo "✅ Conexión exitosa"
else
    echo "❌ Error de conexión"
    exit 1
fi

# Crear estructura de backups
echo ""
echo "📂 Creando estructura de backups..."
rclone mkdir "${REMOTE_NAME}:OpenClaw-Backups"

if [ $? -eq 0 ]; then
    echo "✅ Carpeta 'OpenClaw-Backups' creada"
else
    echo "⚠️  La carpeta ya existe o hubo error"
fi

# Crear archivo de configuración para el skill
CONFIG_DIR="/workspace/skills/backup-recovery/config"
mkdir -p "${CONFIG_DIR}"

cat > "${CONFIG_DIR}/backup_config.json" << EOF
{
  "remote": "${REMOTE_NAME}",
  "basePath": "OpenClaw-Backups",
  "retentionDays": 20,
  "sources": [
    "/home/rhandus/.openclaw",
    "/workspace"
  ],
  "excludePatterns": [
    "**/node_modules/",
    "**/.git/",
    "**/dist/",
    "**/build/",
    "**/vendor/",
    "*.log",
    "*.tmp",
    "*.cache"
  ],
  "schedule": "0 3 * * *",
  "alertOnFailure": true,
  "enableEncryption": false,
  "compressionLevel": 6
}
EOF

echo "✅ Configuración guardada en: ${CONFIG_DIR}/backup_config.json"

# Crear cron job para backup diario
echo ""
echo "⏰ Configurando cron job para backup diario (03:00 AM)..."

CRON_JOB="0 3 * * * cd /workspace/skills/backup-recovery && node src/index.js run 2>&1 | tee -a /var/log/openclaw_backup_cron.log"

# Agregar al crontab del usuario actual
(crontab -l 2>/dev/null | grep -v "backup-recovery"; echo "${CRON_JOB}") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job configurado:"
    echo "   ${CRON_JOB}"
else
    echo "❌ Error configurando cron job"
fi

# Crear script de monitoreo
echo ""
echo "📊 Creando script de monitoreo..."

cat > /usr/local/bin/check-backup-status << 'EOF'
#!/bin/bash
# Script para verificar estado de backups

BACKUP_DIR="/workspace/skills/backup-recovery"
LOG_FILE="/var/log/openclaw_backup.log"

echo "🔍 Verificando estado de backups..."
echo "=================================="

# Verificar último backup
if [ -f "$LOG_FILE" ]; then
    LAST_BACKUP=$(grep "Backup completado exitosamente" "$LOG_FILE" | tail -1)
    if [ -n "$LAST_BACKUP" ]; then
        echo "✅ Último backup exitoso:"
        echo "   $LAST_BACKUP"
    else
        echo "⚠️  No se encontraron backups exitosos recientes"
    fi
else
    echo "📝 Log file no encontrado: $LOG_FILE"
fi

# Verificar cron job
echo ""
echo "⏰ Verificando cron job..."
crontab -l | grep "backup-recovery"

# Verificar configuración
echo ""
echo "⚙️  Verificando configuración..."
cd "$BACKUP_DIR" && node src/index.js stats 2>/dev/null || echo "❌ Error ejecutando stats"

# Verificar espacio en Drive (si está configurado)
echo ""
echo "💾 Verificando espacio..."
REMOTE_NAME=$(grep '"remote"' "${BACKUP_DIR}/config/backup_config.json" | cut -d'"' -f4)
if [ -n "$REMOTE_NAME" ]; then
    rclone size "${REMOTE_NAME}:OpenClaw-Backups" --json 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
gb = data['bytes'] / 1024 / 1024 / 1024
print(f'📦 Espacio utilizado: {gb:.2f} GB')
print(f'📁 Archivos: {data[\"count\"]:,}')
" || echo "❌ Error verificando espacio"
fi
EOF

chmod +x /usr/local/bin/check-backup-status

echo "✅ Script de monitoreo creado: /usr/local/bin/check-backup-status"

# Probar sistema
echo ""
echo "🧪 Probando sistema de backup..."
cd /workspace/skills/backup-recovery

echo "1. Probando conexión..."
node src/index.js config test-connection

echo ""
echo "2. Listando backups existentes..."
node src/index.js list

echo ""
echo "3. Mostrando estadísticas..."
node src/index.js stats

echo ""
echo "🎉 Configuración completada exitosamente!"
echo ""
echo "📋 Resumen:"
echo "   ✅ rClone configurado: ${REMOTE_NAME}"
echo "   ✅ Destino: Google Drive (TU_EMAIL_GOOGLE_DRIVE)"
echo "   ✅ Carpeta: OpenClaw-Backups"
echo "   ✅ Retención: 20 días continuos"
echo "   ✅ Schedule: 03:00 AM diario"
echo "   ✅ Monitoreo: /usr/local/bin/check-backup-status"
echo ""
echo "🚀 Para ejecutar primer backup:"
echo "   cd /workspace/skills/backup-recovery"
echo "   node src/index.js run"
echo ""
echo "📅 El sistema mantendrá automáticamente 20 backups,"
echo "   eliminando el más antiguo cuando se cree uno nuevo."