---
name: backup-recovery
description: "Backup & Recovery Automation for OpenClaw using rClone. Daily backups to Google Drive with 20-day rotation."
metadata:
  openclaw:
    emoji: "🔄"
    ui:
      color: "#4CAF50"
      icon: "backup"
  author: "Rhandus Malpica"
  website: "https://tiklick.com"
  license: "MIT"
---

# Backup & Recovery Automation

Sistema automatizado de backup y recuperación para OpenClaw usando rClone. Backups diarios a Google Drive con rotación de 20 días.

## 🎯 Reglas de Backup (Definidas por Rhandus)

### **Frecuencia y Destino:**
- **Diario:** Un backup completo cada día
- **Destino:** Google Drive de `TU_EMAIL_GOOGLE_DRIVE`
- **Historial:** 20 días continuos máximo
- **Rotación:** Día 21 → Elimina día 1
- **No acumulación:** Solo 20 backups siempre

### **Estructura de Backups:**
```
Google Drive:/OpenClaw-Backups/
├── backup-2026-02-19/          # Más reciente
├── backup-2026-02-18/
├── ...
├── backup-2026-01-31/          # Día 20
└── backup-2026-01-30/          # Se elimina al crear nuevo
```

## 📋 Características

### **Nivel 1 (Base):**
- ✅ **Backup diario automático** (03:00 AM)
- ✅ **Rotación 20 días** automática
- ✅ **Verificación integridad** (checksums)
- ✅ **Logging completo** con alertas
- ✅ **Configuración rClone** para Google Drive

### **Nivel 2 (Avanzado):**
- 🔄 **Recuperación asistida** (CLI interactivo)
- 📊 **Dashboard visualización** estado backups
- 📧 **Reportes automáticos** (éxito/fallo)
- 🔐 **Cifrado opcional** (end-to-end)
- ⚡ **Backup incremental** para velocidad

### **Nivel 3 (Inteligente):**
- 🧠 **Detección cambios importantes**
- ⏰ **Schedule inteligente** (bajo uso sistema)
- 📈 **Análisis espacio** y optimización
- 🔗 **Integración multi-cloud** (Drive + alternativas)
- 🤖 **Auto-recovery** para fallos críticos

## 🚀 Uso

### **Comandos Principales:**

#### `backup run`
Ejecutar backup manualmente.

```bash
# Backup completo ahora
backup run --full

# Backup solo cambios (incremental)
backup run --incremental

# Backup específico de configuración
backup run --config-only

# Forzar rotación (eliminar >20 días)
backup run --force-rotate
```

#### `backup status`
Ver estado de backups.

```bash
# Estado actual
backup status

# Listar backups disponibles
backup status --list

# Verificar integridad
backup status --verify

# Espacio utilizado
backup status --space
```

#### `backup recover`
Recuperar desde backup.

```bash
# Listar disponibles para recuperación
backup recover --list

# Recuperar backup específico
backup recover --date 2026-02-19

# Recuperar archivo específico
backup recover --file /workspace/MEMORY.md --date 2026-02-18

# Recuperar configuración OpenClaw
backup recover --config
```

#### `backup config`
Gestionar configuración.

```bash
# Mostrar configuración actual
backup config --show

# Probar conexión Google Drive
backup config --test

# Actualizar credenciales
backup config --update-credentials

# Cambiar schedule
backup config --schedule "0 3 * * *"
```

## ⚙️ Configuración

### **Archivos a Incluir en Backup:**

#### **Críticos (Siempre):**
```
/home/rhandus/.openclaw/
├── openclaw.json              # Configuración principal
├── agents/                    # Configuraciones agentes
├── sessions/                  # Sesiones activas
└── workspace/                 # Workspace (symlink)
```

#### **Workspace (Excluyendo innecesarios):**
```
/workspace/
├── MEMORY.md                  # Memoria a largo plazo
├── AGENTS.md                  # Configuración agentes
├── SOUL.md                    # Personalidad
├── IDENTITY.md                # Identidad
├── USER.md                    # Información usuario
├── TOOLS.md                   # Herramientas locales
├── HEARTBEAT.md               # Tareas periódicas
├── skills/                    # Todos los skills
├── openclaw.backup.json       # Backup configuración
└── .openclaw_contacts.env     # Contactos alertas
```

#### **Excluidos (No backup):**
```
**/node_modules/
**/.git/
**/dist/
**/build/
**/vendor/
*.log
*.tmp
*.cache
```

### **Variables de Entorno:**
```bash
BACKUP_DRIVE_REMOTE="tiklick-drive"
BACKUP_SOURCE="/home/rhandus/.openclaw /workspace"
BACKUP_EXCLUDE="**/node_modules/ **/.git/"
BACKUP_RETENTION_DAYS=20
BACKUP_SCHEDULE="0 3 * * *"  # 03:00 AM diario
BACKUP_LOG_FILE="/var/log/openclaw_backup.log"
BACKUP_ALERT_ON_FAILURE=true
```

## 🔧 Integración con rClone

### **Configuración rClone:**
```bash
# Crear configuración
rclone config create tiklick-drive drive \
  client_id "YOUR_CLIENT_ID" \
  client_secret "YOUR_CLIENT_SECRET" \
  scope "drive.file" \
  root_folder_id "YOUR_ROOT_FOLDER_ID"

# Probar conexión
rclone lsd tiklick-drive:

# Crear carpeta backups
rclone mkdir tiklick-drive:OpenClaw-Backups
```

### **Comando Backup Básico:**
```bash
rclone sync \
  --progress \
  --exclude "**/node_modules/" \
  --exclude "**/.git/" \
  --exclude "*.log" \
  --backup-dir "tiklick-drive:OpenClaw-Backups/backup-$(date +%Y-%m-%d)" \
  /home/rhandus/.openclaw \
  tiklick-drive:OpenClaw-Backups/current
```

## 🎯 Ejemplos para Tiklick

### **Backup Diario Automático:**
```bash
# Script ejecutado por cron a las 03:00 AM
backup run --full --rotate --notify
```

### **Verificación Semanal:**
```bash
# Domingo a las 04:00 AM
backup status --verify --report
```

### **Recuperación Rápida:**
```bash
# Recuperar configuración crítica
backup recover --config --date $(date -d "yesterday" +%Y-%m-%d)

# Recuperar skill específico
backup recover --file /workspace/skills/alerting-system --date 2026-02-19
```

### **Monitoreo Espacio:**
```bash
# Alertar si espacio > 80%
backup status --space --alert-if-over 80
```

## 📊 Métricas y Monitoreo

### **Métricas a Seguir:**
- **Tiempo backup:** < 15 minutos
- **Tasa éxito:** > 99%
- **Espacio utilizado:** < 50GB
- **Rotación correcta:** 20 backups exactos
- **Integridad verificada:** 100% de backups

### **Dashboard de Estado:**
- **Backups últimos 20 días** (verde/rojo)
- **Espacio utilizado** en Drive
- **Tiempo último backup**
- **Estado verificación integridad**
- **Próxima rotación programada**

## 🛡️ Seguridad

### **Protección de Datos:**
- **Acceso restringido:** Solo `TU_EMAIL_GOOGLE_DRIVE`
- **Cifrado opcional:** rClone crypt backend
- **Logs seguros:** Sin datos sensibles
- **Auditoría:** Registro completo de operaciones

### **Recuperación de Desastres:**
1. **Backup corrupto:** Usar penúltimo backup
2. **Drive inaccesible:** Alertar inmediatamente
3. **Sistema caído:** Recovery desde último backup verificado
4. **Credenciales comprometidas:** Rotar inmediatamente

## 🔄 Mantenimiento

### **Diario:**
- Verificar éxito backup nocturno
- Revisar logs en busca de errores
- Confirmar rotación correcta (20 backups)

### **Semanal:**
- Verificar integridad todos los backups
- Limpiar logs antiguos (>30 días)
- Revisar espacio disponible en Drive

### **Mensual:**
- Auditoría completa del sistema
- Prueba de recuperación completa
- Actualización rClone y dependencias
- Revisión y ajuste de exclusiones

## 🚨 Plan de Implementación

### **Semana 1: Base (Actual)**
- Configuración rClone y Google Drive
- Script backup básico con rotación 20 días
- Sistema logging y alertas
- Testing inicial

### **Semana 2: Avanzado**
- CLI interactivo para recuperación
- Dashboard visualización estado
- Reportes automáticos por email
- Integración con sistema de alertas

### **Semana 3: Inteligente**
- Backup incremental inteligente
- Detección cambios importantes
- Auto-recovery para fallos
- Optimización espacio y velocidad

---

**Estado:** 🟢 PRODUCCIÓN (v1.0.0)  
**Autor:** Rhandus Malpica  
**Empresa:** Tiklick  
**Website:** https://tiklick.com  
**Licencia:** MIT  
**Publicado en ClawHub:** 2026-02-20