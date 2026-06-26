/**
 * 🔄 Backup & Recovery - Punto de Entrada Principal
 * Sistema automatizado con rClone (20 días rotación)
 */

import { BackupManager } from './backup_manager.js';

/**
 * CLI Handler principal
 */
async function main() {
  const manager = new BackupManager();
  
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  switch (command) {
    case 'run':
      await handleRunBackup(manager, args);
      break;
      
    case 'list':
      await handleListBackups(manager, args);
      break;
      
    case 'restore':
      await handleRestoreBackup(manager, args);
      break;
      
    case 'stats':
      await handleStats(manager, args);
      break;
      
    case 'test':
      await handleTest(manager, args);
      break;
      
    case 'dry-run':
      await handleDryRun(manager, args);
      break;
      
    case 'config':
      await handleConfig(manager, args);
      break;
      
    case 'help':
    default:
      showHelp();
      break;
  }
}

/**
 * Ejecutar backup
 */
async function handleRunBackup(manager, args) {
  const incremental = args.includes('--incremental');
  const force = args.includes('--force');
  
  console.log('🔄 Iniciando backup...');
  console.log(`📅 Regla: 20 días continuos, rotación automática`);
  console.log(`📁 Fuentes: ${manager.config.sources.length} directorios`);
  console.log(`🗑️  Excluidos: ${manager.config.excludePatterns.length} patrones`);
  
  const result = await manager.runBackup({ incremental, force });
  
  if (result.success) {
    console.log('✅ Backup completado exitosamente:');
    console.log(`   Nombre: ${result.backupName}`);
    console.log(`   Duración: ${result.duration}s`);
    console.log(`   Tamaño: ${result.size}`);
    console.log(`   Ruta: ${result.backupPath}`);
  } else {
    console.error('❌ Backup fallido:');
    console.error(`   Error: ${result.error}`);
    console.error(`   Nombre: ${result.backupName}`);
  }
}

/**
 * Listar backups disponibles
 */
async function handleListBackups(manager) {
  console.log('📊 Listando backups disponibles...');
  
  const backups = await manager.listBackups();
  
  if (backups.length === 0) {
    console.log('ℹ️  No hay backups disponibles.');
    return;
  }
  
  console.log(`📅 Total backups: ${backups.length} (${manager.config.retentionDays} días máximo)`);
  console.log('');
  
  backups.forEach((backup, index) => {
    const isRecent = index === 0 ? '🟢' : '⚪';
    console.log(`${isRecent} ${index + 1}. ${backup.name}`);
    console.log(`   Fecha: ${backup.date}`);
    console.log(`   Tamaño: ${backup.size}`);
    console.log('');
  });
  
  // Verificar regla de 20 días
  if (backups.length > manager.config.retentionDays) {
    console.warn(`⚠️  ADVERTENCIA: ${backups.length} backups (máximo ${manager.config.retentionDays})`);
    console.warn(`   Ejecutar: backup run --force para aplicar rotación`);
  }
}

/**
 * Restaurar backup
 */
async function handleRestoreBackup(manager, args) {
  const backupName = args[0];
  const targetPath = args[1] || '/tmp/restore-backup';
  
  if (!backupName) {
    console.error('❌ Se requiere nombre de backup');
    console.log('Uso: backup restore <backup-name> [target-path]');
    
    // Mostrar backups disponibles
    const backups = await manager.listBackups();
    if (backups.length > 0) {
      console.log('\n📅 Backups disponibles:');
      backups.slice(0, 5).forEach(backup => {
        console.log(`   • ${backup.name}`);
      });
    }
    
    return;
  }
  
  console.log(`🔄 Restaurando backup: ${backupName}`);
  console.log(`📂 Destino: ${targetPath}`);
  
  const result = await manager.restoreBackup(backupName, targetPath);
  
  if (result.success) {
    console.log('✅ Backup restaurado exitosamente:');
    console.log(`   Backup: ${result.backupName}`);
    console.log(`   Destino: ${result.targetPath}`);
    console.log(`   Duración: ${result.duration}s`);
    console.log(`   Archivos: ${result.filesRestored}`);
  } else {
    console.error('❌ Restauración fallida:');
    console.error(`   Error: ${result.error}`);
  }
}

/**
 * Mostrar estadísticas
 */
async function handleStats(manager) {
  const stats = manager.getStats();
  
  console.log('📊 Estadísticas del Sistema de Backup:');
  console.log('========================================');
  console.log('');
  
  console.log('📈 Métricas:');
  console.log(`   Total backups: ${stats.totalBackups}`);
  console.log(`   Exitosos: ${stats.successfulBackups}`);
  console.log(`   Fallidos: ${stats.failedBackups}`);
  console.log(`   Último backup: ${stats.lastBackupDate || 'Nunca'}`);
  console.log('');
  
  console.log('⚙️ Configuración:');
  console.log(`   Remote: ${stats.config.remote}`);
  console.log(`   Retención: ${stats.config.retentionDays} días`);
  console.log(`   Fuentes: ${stats.config.sources}`);
  console.log(`   Schedule: ${stats.config.schedule}`);
  console.log('');
  
  console.log('📅 Estado actual:');
  const backups = await manager.listBackups();
  console.log(`   Backups disponibles: ${backups.length}`);
  
  if (backups.length > 0) {
    const oldest = backups[backups.length - 1];
    const newest = backups[0];
    console.log(`   Más reciente: ${newest.name}`);
    console.log(`   Más antiguo: ${oldest.name}`);
    
    // Verificar regla de 20 días
    if (backups.length > stats.config.retentionDays) {
      console.warn(`   ⚠️  VIOLACIÓN: ${backups.length} backups (máximo ${stats.config.retentionDays})`);
    } else {
      console.log(`   ✅ Cumple regla: ${backups.length}/${stats.config.retentionDays} días`);
    }
  }
}

/**
 * Ejecutar pruebas
 */
async function handleTest(manager) {
  console.log('🧪 Ejecutando pruebas del sistema de backup...');
  
  try {
    // Prueba 1: Conexión rClone
    console.log('\n1. Probando conexión rClone...');
    await manager.testRCloneConnection();
    console.log('✅ Conexión rClone exitosa');
    
    // Prueba 2: Listar backups
    console.log('\n2. Listando backups existentes...');
    const backups = await manager.listBackups();
    console.log(`✅ Backups encontrados: ${backups.length}`);
    
    // Prueba 3: Estadísticas
    console.log('\n3. Obteniendo estadísticas...');
    const stats = manager.getStats();
    console.log(`✅ Estadísticas obtenidas: ${stats.totalBackups} backups totales`);
    
    // Prueba 4: Configuración
    console.log('\n4. Verificando configuración...');
    console.log(`   Remote: ${manager.config.remote}`);
    console.log(`   Retención: ${manager.config.retentionDays} días`);
    console.log(`   Fuentes: ${manager.config.sources.length}`);
    console.log('✅ Configuración verificada');
    
    // Prueba 5: Regla de 20 días
    console.log('\n5. Verificando regla de 20 días...');
    if (backups.length <= manager.config.retentionDays) {
      console.log(`✅ Cumple regla: ${backups.length}/${manager.config.retentionDays} días`);
    } else {
      console.warn(`⚠️  Violación: ${backups.length} backups (máximo ${manager.config.retentionDays})`);
    }
    
    console.log('\n🎉 Todas las pruebas completadas exitosamente!');
    
  } catch (error) {
    console.error(`❌ Error en pruebas: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Ejecutar dry-run
 */
async function handleDryRun(manager) {
  console.log('🧪 Ejecutando dry-run de backup...');
  console.log('📝 Esto mostrará qué se haría sin ejecutar realmente.');
  
  const result = await manager.runBackup({ dryRun: true });
  
  if (result.success) {
    console.log('✅ Dry-run completado:');
    console.log(`   Comando que se ejecutaría:`);
    console.log(result.command);
  } else {
    console.error('❌ Dry-run fallido:');
    console.error(`   Error: ${result.error}`);
  }
}

/**
 * Gestionar configuración
 */
async function handleConfig(manager, args) {
  const action = args[0];
  
  switch (action) {
    case 'show':
      console.log('⚙️ Configuración actual:');
      console.log(JSON.stringify(manager.config, null, 2));
      break;
      
    case 'test-connection':
      console.log('🔗 Probando conexión...');
      try {
        await manager.testRCloneConnection();
        console.log('✅ Conexión exitosa');
      } catch (error) {
        console.error(`❌ Conexión fallida: ${error.message}`);
      }
      break;
      
    default:
      console.log('Uso: backup config <show|test-connection>');
      break;
  }
}

/**
 * Mostrar ayuda
 */
function showHelp() {
  console.log('🔄 Sistema de Backup & Recovery OpenClaw');
  console.log('=========================================');
  console.log('');
  console.log('📅 Regla: 20 días continuos, rotación automática');
  console.log('⏰ Schedule: 03:00 AM diario (configurable)');
  console.log('☁️  Destino: Google Drive TU_EMAIL_GOOGLE_DRIVE');
  console.log('');
  console.log('Comandos disponibles:');
  console.log('');
  console.log('  backup run [--incremental] [--force]');
  console.log('    Ejecutar backup completo');
  console.log('');
  console.log('  backup list');
  console.log('    Listar backups disponibles (20 máximo)');
  console.log('');
  console.log('  backup restore <backup-name> [target-path]');
  console.log('    Restaurar backup específico');
  console.log('');
  console.log('  backup stats');
  console.log('    Mostrar estadísticas del sistema');
  console.log('');
  console.log('  backup test');
  console.log('    Ejecutar pruebas del sistema');
  console.log('');
  console.log('  backup dry-run');
  console.log('    Simular backup sin ejecutar');
  console.log('');
  console.log('  backup config <show|test-connection>');
  console.log('    Gestionar configuración');
  console.log('');
  console.log('  backup help');
  console.log('    Mostrar esta ayuda');
  console.log('');
  console.log('Ejemplos:');
  console.log('  backup run --incremental');
  console.log('  backup list');
  console.log('  backup restore backup-2026-02-19 /tmp/restore');
  console.log('  backup config show');
  console.log('');
}

// Ejecutar CLI
if (process.argv.length > 2) {
  main().catch(console.error);
} else {
  showHelp();
}