/**
 * 🔄 Backup Manager - Sistema de Backup y Recuperación
 * Regla: 20 días continuos, rotación automática
 */

import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Configuración
const CONFIG_FILE = '/workspace/skills/backup-recovery/config/backup_config.json';
const LOG_FILE = '/workspace/logs/backup.log';
const BACKUP_REMOTE = 'tiklick-drive'; // Configurar con rclone config
const BACKUP_BASE_PATH = 'OpenClaw-Backups';
const RETENTION_DAYS = 20; // Regla: 20 días máximo

/**
 * Clase principal del sistema de backup
 */
export class BackupManager {
  constructor() {
    this.config = this.loadConfig();
    this.stats = {
      totalBackups: 0,
      successfulBackups: 0,
      failedBackups: 0,
      totalSizeGB: 0,
      lastBackupDate: null,
      nextBackupDate: null
    };
    
    this.initialize();
  }
  
  /**
   * Cargar configuración
   */
  loadConfig() {
    const defaultConfig = {
      remote: BACKUP_REMOTE,
      basePath: BACKUP_BASE_PATH,
      retentionDays: RETENTION_DAYS,
      sources: [
        '/home/rhandus/.openclaw',
        '/workspace'
      ],
      excludePatterns: [
        '**/node_modules/',
        '**/.git/',
        '**/dist/',
        '**/build/',
        '**/vendor/',
        '*.log',
        '*.tmp',
        '*.cache'
      ],
      schedule: '0 3 * * *', // 03:00 AM diario
      alertOnFailure: true,
      enableEncryption: false,
      compressionLevel: 6
    };
    
    try {
      if (fs.existsSync(CONFIG_FILE)) {
        const data = fs.readFileSync(CONFIG_FILE, 'utf8');
        return { ...defaultConfig, ...JSON.parse(data) };
      }
    } catch (error) {
      this.log(`Error cargando configuración: ${error.message}`, 'error');
    }
    
    return defaultConfig;
  }
  
  /**
   * Inicializar sistema
   */
  initialize() {
    this.log('🚀 Inicializando sistema de backup...', 'info');
    
    // Crear directorio de logs si no existe
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    
    // Crear directorio de configuración
    const configDir = path.dirname(CONFIG_FILE);
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    
    // Guardar configuración por defecto
    this.saveConfig();
    
    this.log('✅ Sistema de backup inicializado', 'info');
  }
  
  /**
   * Guardar configuración
   */
  saveConfig() {
    try {
      const data = JSON.stringify(this.config, null, 2);
      fs.writeFileSync(CONFIG_FILE, data);
      this.log('Configuración guardada', 'info');
    } catch (error) {
      this.log(`Error guardando configuración: ${error.message}`, 'error');
    }
  }
  
  /**
   * Registrar en log
   */
  log(message, level = 'info') {
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;
    
    try {
      fs.appendFileSync(LOG_FILE, logEntry);
    } catch (error) {
      console.error(`Error escribiendo log: ${error.message}`);
    }
    
    // También log a consola
    const emoji = level === 'error' ? '❌' : level === 'warning' ? '⚠️' : '📝';
    console.log(`${emoji} ${message}`);
  }
  
  /**
   * Ejecutar backup completo
   */
  async runBackup(options = {}) {
    const {
      incremental = false,
      force = false,
      dryRun = false
    } = options;
    
    const backupDate = new Date().toISOString().split('T')[0];
    const backupName = `backup-${backupDate}`;
    const backupPath = `${this.config.basePath}/${backupName}`;
    
    this.log(`🔄 Iniciando backup: ${backupName}`, 'info');
    
    try {
      // 1. Verificar conexión rClone
      await this.testRCloneConnection();
      
      // 2. Crear lista de exclusión
      const excludeArgs = this.config.excludePatterns
        .map(pattern => `--exclude "${pattern}"`)
        .join(' ');
      
      // 3. Construir comando rClone - UN solo comando para todas las fuentes
      let command = `rclone sync \\\n`;
      
      if (incremental) {
        command += `  --backup-dir "${this.config.remote}:${this.config.basePath}/incremental-${backupDate}" \\\n`;
      }
      
      command += `  ${excludeArgs} \\\n`;
      command += `  --progress \\\n`;
      command += `  --log-file ${LOG_FILE} \\\n`;
      command += `  -L \\\n`;  // Follow symlinks
      
      // Combinar todas las fuentes en un solo comando
      const allSources = this.config.sources.join(' ');
      command += `  ${allSources} \\\n`;
      command += `  "${this.config.remote}:${backupPath}"`;
      
      if (dryRun) {
        command += ` --dry-run`;
        this.log(`🧪 Dry run command:\n${command}`, 'info');
        return { success: true, dryRun: true, command };
      }
      
      this.log(`📡 Ejecutando backup...`, 'info');
      
      // 4. Ejecutar backup
      const startTime = Date.now();
      const { stdout, stderr } = await execAsync(command, { shell: true });
      const duration = Math.round((Date.now() - startTime) / 1000);
      
      // 5. Verificar éxito
      if (stderr && !stderr.includes('INFO')) {
        throw new Error(`rClone error: ${stderr}`);
      }
      
      // 6. Aplicar rotación (mantener solo 20 días)
      await this.applyRetention();
      
      // 7. Actualizar estadísticas
      this.stats.totalBackups++;
      this.stats.successfulBackups++;
      this.stats.lastBackupDate = new Date().toISOString();
      
      this.log(`✅ Backup completado exitosamente: ${backupName} (${duration}s)`, 'info');
      
      return {
        success: true,
        backupName,
        backupPath,
        duration,
        size: await this.getBackupSize(backupPath)
      };
      
    } catch (error) {
      this.log(`❌ Error en backup: ${error.message}`, 'error');
      this.stats.totalBackups++;
      this.stats.failedBackups++;
      
      // Alertar si está configurado
      if (this.config.alertOnFailure) {
        await this.alertBackupFailure(error.message, backupName);
      }
      
      return {
        success: false,
        error: error.message,
        backupName
      };
    }
  }
  
  /**
   * Aplicar retención (20 días máximo)
   */
  async applyRetention() {
    this.log(`🔄 Aplicando retención: ${RETENTION_DAYS} días máximo`, 'info');
    
    try {
      // Listar todos los backups
      const command = `rclone lsd "${this.config.remote}:${this.config.basePath}" --format "tp"`;
      const { stdout } = await execAsync(command, { shell: true });
      
      const backups = stdout
        .split('\n')
        .filter(line => line.includes('backup-'))
        .map(line => {
          const parts = line.split(/\s+/);
          return {
            name: parts[parts.length - 1],
            date: parts[parts.length - 1].replace('backup-', '')
          };
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date)); // Más antiguo primero
      
      // Eliminar backups antiguos (>20 días)
      if (backups.length > RETENTION_DAYS) {
        const toDelete = backups.slice(0, backups.length - RETENTION_DAYS);
        
        this.log(`📊 Backups encontrados: ${backups.length}, a eliminar: ${toDelete.length}`, 'info');
        
        for (const backup of toDelete) {
          this.log(`🗑️  Eliminando backup antiguo: ${backup.name}`, 'info');
          
          const deleteCommand = `rclone purge "${this.config.remote}:${this.config.basePath}/${backup.name}"`;
          await execAsync(deleteCommand, { shell: true });
          
          this.log(`✅ Eliminado: ${backup.name}`, 'info');
        }
        
        // Verificar que quedan exactamente 20
        const verifyCommand = `rclone lsd "${this.config.remote}:${this.config.basePath}" | grep -c "backup-"`;
        const { stdout: countOutput } = await execAsync(verifyCommand, { shell: true });
        const currentCount = parseInt(countOutput.trim());
        
        if (currentCount === RETENTION_DAYS) {
          this.log(`✅ Rotación correcta: ${currentCount} backups (${RETENTION_DAYS} días)`, 'info');
        } else {
          this.log(`⚠️  Rotación incompleta: ${currentCount} backups (esperado ${RETENTION_DAYS})`, 'warning');
        }
      } else {
        this.log(`✅ Rotación no necesaria: ${backups.length} backups (<= ${RETENTION_DAYS})`, 'info');
      }
      
    } catch (error) {
      this.log(`❌ Error aplicando retención: ${error.message}`, 'error');
    }
  }
  
  /**
   * Obtener tamaño de backup
   */
  async getBackupSize(backupPath) {
    try {
      const command = `rclone size "${this.config.remote}:${backupPath}" --json`;
      const { stdout } = await execAsync(command, { shell: true });
      const sizeInfo = JSON.parse(stdout);
      
      const sizeGB = (sizeInfo.bytes / 1024 / 1024 / 1024).toFixed(2);
      return `${sizeGB} GB`;
      
    } catch (error) {
      return 'Desconocido';
    }
  }
  
  /**
   * Probar conexión rClone
   */
  async testRCloneConnection() {
    try {
      this.log('🔗 Probando conexión rClone...', 'info');
      
      const command = `rclone lsd "${this.config.remote}:"`;
      await execAsync(command, { shell: true });
      
      this.log('✅ Conexión rClone exitosa', 'info');
      return true;
      
    } catch (error) {
      throw new Error(`Conexión rClone fallida: ${error.message}`);
    }
  }
  
  /**
   * Alertar fallo de backup
   */
  async alertBackupFailure(errorMessage, backupName) {
    this.log(`🚨 Enviando alerta de fallo de backup: ${backupName}`, 'warning');
    
    // Integración con sistema de alertas existente
    try {
      const alertCommand = `cd /workspace/skills/alerting-system && \
                           node src/index.js create \
                           "Backup Fallido: ${backupName}" \
                           "Error: ${errorMessage}" \
                           "backup-system" \
                           "critical"`;
      
      await execAsync(alertCommand, { shell: true });
      this.log('✅ Alerta de fallo enviada', 'info');
      
    } catch (alertError) {
      this.log(`❌ Error enviando alerta: ${alertError.message}`, 'error');
    }
  }
  
  /**
   * Listar backups disponibles
   */
  async listBackups() {
    try {
      const command = `rclone lsd "${this.config.remote}:${this.config.basePath}" | grep "backup-"`;
      const { stdout } = await execAsync(command, { shell: true });
      
      const backups = stdout
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
          const parts = line.split(/\s+/);
          return {
            name: parts[parts.length - 1],
            date: parts[parts.length - 1].replace('backup-', ''),
            size: 'Desconocido' // Se podría obtener con comando adicional
          };
        })
        .sort((a, b) => new Date(b.date) - new Date(a.date)); // Más reciente primero
      
      return backups;
      
    } catch (error) {
      this.log(`❌ Error listando backups: ${error.message}`, 'error');
      return [];
    }
  }
  
  /**
   * Recuperar backup específico
   */
  async restoreBackup(backupName, targetPath = '/tmp/restore') {
    try {
      this.log(`🔄 Recuperando backup: ${backupName} → ${targetPath}`, 'info');
      
      // Crear directorio destino
      if (!fs.existsSync(targetPath)) {
        fs.mkdirSync(targetPath, { recursive: true });
      }
      
      const sourcePath = `${this.config.remote}:${this.config.basePath}/${backupName}`;
      const command = `rclone copy "${sourcePath}" "${targetPath}" --progress`;
      
      const startTime = Date.now();
      const { stdout, stderr } = await execAsync(command, { shell: true });
      const duration = Math.round((Date.now() - startTime) / 1000);
      
      if (stderr && !stderr.includes('INFO')) {
        throw new Error(`rClone error: ${stderr}`);
      }
      
      this.log(`✅ Backup recuperado: ${backupName} (${duration}s)`, 'info');
      
      return {
        success: true,
        backupName,
        targetPath,
        duration,
        filesRestored: await this.countFiles(targetPath)
      };
      
    } catch (error) {
      this.log(`❌ Error recuperando backup: ${error.message}`, 'error');
      return {
        success: false,
        error: error.message,
        backupName
      };
    }
  }
  
  /**
   * Contar archivos en directorio
   */
  async countFiles(dirPath) {
    try {
      const command = `find "${dirPath}" -type f | wc -l`;
      const { stdout } = await execAsync(command, { shell: true });
      return parseInt(stdout.trim());
    } catch (error) {
      return 0;
    }
  }
  
  /**
   * Obtener estadísticas
   */
  getStats() {
    return {
      ...this.stats,
      config: {
        remote: this.config.remote,
        retentionDays: this.config.retentionDays,
        sources: this.config.sources.length,
        schedule: this.config.schedule
      },
      timestamp: new Date().toISOString()
    };
  }
}

// CLI para pruebas
if (process.argv[2] === 'test') {
  const manager = new BackupManager();
  
  console.log('🧪 Probando sistema de backup...');
  
  // Probar conexión
  manager.testRCloneConnection()
    .then(() => {
      console.log('✅ Conexión rClone exitosa');
      
      // Listar backups existentes
      return manager.listBackups();
    })
    .then(backups => {
      console.log(`📊 Backups existentes: ${backups.length}`);
      backups.forEach((backup, i) => {
        console.log(`  ${i + 1}. ${backup.name} (${backup.date})`);
      });
      
      // Mostrar estadísticas
      console.log('\n📈 Estadísticas:');
      console.log(JSON.stringify(manager.getStats(), null, 2));
      
      console.log('\n🎉 Pruebas completadas exitosamente');
    })
    .catch(error => {
      console.error('❌ Error en pruebas:', error.message);
      process.exit(1);
    });
}

if (process.argv[2] === 'dry-run') {
  const manager = new BackupManager();
  
  console.log('🧪 Ejecutando dry-run de backup...');
  
  manager.runBackup({ dryRun: true, incremental: false })
    .then(result => {
      console.log('✅ Dry-run completado:');
      console.log(JSON.stringify(result, null, 2));
    })
    .catch(console.error);
}

if (process.argv[2] === 'stats') {
  const manager = new BackupManager();
  console.log('📊 Estadísticas del Sistema de Backup:');
  console.log(JSON.stringify(manager.getStats(), null, 2));
}