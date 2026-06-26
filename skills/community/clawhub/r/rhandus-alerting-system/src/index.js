/**
 * 🚨 Alerting System - Punto de Entrada Principal
 * Sistema centralizado de alertas y notificaciones
 */

import { AlertManager } from './alert_manager.js';

/**
 * CLI Handler principal
 */
async function main() {
  const manager = new AlertManager();
  
  const command = process.argv[2];
  const args = process.argv.slice(3);
  
  switch (command) {
    case 'create':
      await handleCreateAlert(manager, args);
      break;
      
    case 'resolve':
      await handleResolveAlert(manager, args);
      break;
      
    case 'list':
      await handleListAlerts(manager, args);
      break;
      
    case 'stats':
      await handleStats(manager, args);
      break;
      
    case 'monitor':
      await handleMonitor(manager, args);
      break;
      
    case 'test':
      await handleTest(manager, args);
      break;
      
    case 'help':
    default:
      showHelp();
      break;
  }
}

/**
 * Crear nueva alerta
 */
async function handleCreateAlert(manager, args) {
  const title = args[0] || 'Alerta sin título';
  const message = args[1] || 'Sin mensaje proporcionado';
  const service = args[2] || 'general';
  const priority = args[3] || 'warning';
  
  const alert = await manager.createAlert({
    title,
    message,
    service,
    priority,
    channels: ['telegram', 'log'],
    metadata: { source: 'cli', args }
  });
  
  console.log('✅ Alerta creada:');
  console.log(JSON.stringify(alert, null, 2));
}

/**
 * Resolver alerta
 */
async function handleResolveAlert(manager, args) {
  const alertId = args[0];
  const notes = args.slice(1).join(' ') || 'Resuelta manualmente';
  
  if (!alertId) {
    console.error('❌ Se requiere ID de alerta');
    console.log('Uso: alert resolve <alert_id> [notes]');
    return;
  }
  
  const alert = manager.resolveAlert(alertId, notes);
  
  if (alert) {
    console.log('✅ Alerta resuelta:');
    console.log(JSON.stringify(alert, null, 2));
  } else {
    console.error(`❌ No se pudo resolver alerta: ${alertId}`);
  }
}

/**
 * Listar alertas
 */
async function handleListAlerts(manager, args) {
  const filter = args[0] || 'active';
  
  let alerts;
  
  switch (filter) {
    case 'active':
      alerts = manager.listActiveAlerts();
      console.log('🚨 Alertas Activas:');
      break;
      
    case 'all':
      alerts = manager.alerts.alerts;
      console.log('📋 Todas las Alertas:');
      break;
      
    case 'resolved':
      alerts = manager.alerts.alerts.filter(a => a.status === 'resolved');
      console.log('✅ Alertas Resueltas:');
      break;
      
    default:
      console.error(`❌ Filtro no válido: ${filter}`);
      console.log('Filtros válidos: active, all, resolved');
      return;
  }
  
  if (alerts.length === 0) {
    console.log('No hay alertas.');
    return;
  }
  
  alerts.forEach(alert => {
    const emoji = manager.getPriorityEmoji(alert.priority);
    const time = new Date(alert.createdAt).toLocaleTimeString();
    console.log(`${emoji} ${alert.id} - ${alert.title} (${alert.service}) - ${time}`);
  });
  
  console.log(`\n📊 Total: ${alerts.length} alerta(s)`);
}

/**
 * Mostrar estadísticas
 */
async function handleStats(manager) {
  const stats = manager.getStats();
  
  console.log('📊 Estadísticas del Sistema de Alertas:');
  console.log('========================================');
  console.log(`Total alertas: ${stats.totalAlerts}`);
  console.log(`Activas: ${stats.activeAlerts}`);
  console.log(`Resueltas: ${stats.resolvedAlerts}`);
  console.log(`Tiempo actividad: ${stats.uptime}`);
  console.log('');
  
  console.log('📈 Por prioridad:');
  Object.entries(stats.byPriority).forEach(([priority, count]) => {
    if (count > 0) {
      const emoji = manager.getPriorityEmoji(priority);
      console.log(`  ${emoji} ${priority}: ${count}`);
    }
  });
  
  console.log('');
  console.log('🏷️  Por servicio (top 5):');
  Object.entries(stats.byService)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .forEach(([service, count]) => {
      console.log(`  ${service}: ${count}`);
    });
}

/**
 * Monitorear endpoint
 */
async function handleMonitor(manager, args) {
  const url = args[0];
  
  if (!url) {
    console.error('❌ Se requiere URL para monitorear');
    console.log('Uso: alert monitor <url> [expected_status]');
    return;
  }
  
  const expectedStatus = parseInt(args[1]) || 200;
  
  console.log(`📡 Monitoreando: ${url} (esperado: ${expectedStatus})`);
  
  const result = await manager.monitorHTTP(url, {
    expectedStatus,
    alertOnFailure: true,
    alertPriority: 'critical',
    serviceName: 'http-monitor'
  });
  
  console.log('✅ Resultado:');
  console.log(JSON.stringify(result, null, 2));
}

/**
 * Ejecutar pruebas
 */
async function handleTest(manager) {
  console.log('🧪 Ejecutando pruebas del sistema de alertas...');
  
  // Prueba 1: Crear alerta de prueba
  console.log('\n1. Creando alerta de prueba...');
  const testAlert = await manager.createAlert({
    title: 'Prueba del Sistema de Alertas',
    message: 'Esta es una alerta de prueba del sistema.',
    service: 'testing',
    priority: 'info',
    channels: ['log'],
    metadata: { test: true }
  });
  
  console.log(`✅ Alerta creada: ${testAlert.id}`);
  
  // Prueba 2: Listar alertas activas
  console.log('\n2. Listando alertas activas...');
  const activeAlerts = manager.listActiveAlerts();
  console.log(`✅ Alertas activas: ${activeAlerts.length}`);
  
  // Prueba 3: Estadísticas
  console.log('\n3. Obteniendo estadísticas...');
  const stats = manager.getStats();
  console.log(`✅ Estadísticas obtenidas: ${stats.totalAlerts} alertas totales`);
  
  // Prueba 4: Resolver alerta
  console.log('\n4. Resolviendo alerta de prueba...');
  const resolved = manager.resolveAlert(testAlert.id, 'Prueba completada');
  console.log(`✅ Alerta resuelta: ${resolved ? 'Sí' : 'No'}`);
  
  // Prueba 5: Estadísticas finales
  console.log('\n5. Estadísticas finales:');
  const finalStats = manager.getStats();
  console.log(`   Total: ${finalStats.totalAlerts}`);
  console.log(`   Activas: ${finalStats.activeAlerts}`);
  console.log(`   Resueltas: ${finalStats.resolvedAlerts}`);
  
  console.log('\n🎉 Todas las pruebas completadas exitosamente!');
}

/**
 * Mostrar ayuda
 */
function showHelp() {
  console.log('🚨 Sistema de Alertas OpenClaw');
  console.log('===============================');
  console.log('');
  console.log('Comandos disponibles:');
  console.log('');
  console.log('  alert create <title> <message> [service] [priority]');
  console.log('    Crear nueva alerta');
  console.log('');
  console.log('  alert resolve <alert_id> [notes]');
  console.log('    Marcar alerta como resuelta');
  console.log('');
  console.log('  alert list [active|all|resolved]');
  console.log('    Listar alertas');
  console.log('');
  console.log('  alert stats');
  console.log('    Mostrar estadísticas');
  console.log('');
  console.log('  alert monitor <url> [expected_status]');
  console.log('    Monitorear endpoint HTTP');
  console.log('');
  console.log('  alert test');
  console.log('    Ejecutar pruebas del sistema');
  console.log('');
  console.log('  alert help');
  console.log('    Mostrar esta ayuda');
  console.log('');
  console.log('Prioridades: info, warning, critical, emergency');
  console.log('');
}

// Ejecutar CLI
if (process.argv.length > 2) {
  main().catch(console.error);
} else {
  showHelp();
}