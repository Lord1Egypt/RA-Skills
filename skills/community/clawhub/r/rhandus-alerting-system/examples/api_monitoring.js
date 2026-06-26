/**
 * 📡 Ejemplo: Monitoreo de APIs Tiklick con Sistema de Alertas
 * Integración con skill api-testing existente
 */

import { AlertManager } from '../src/alert_manager.js';

// APIs críticas de Tiklick para monitorear
const TIKLICK_APIS = [
  {
    name: 'API Principal Tiklick',
    url: 'https://api.tiklick.com/health',
    expectedStatus: 200,
    checkInterval: 60, // segundos
    priority: 'critical'
  },
  {
    name: 'API Pagos',
    url: 'https://pagos.tiklick.com/status',
    expectedStatus: 200,
    checkInterval: 120,
    priority: 'critical'
  },
  {
    name: 'API Autenticación',
    url: 'https://auth.tiklick.com/health',
    expectedStatus: 200,
    checkInterval: 90,
    priority: 'critical'
  },
  {
    name: 'Dashboard Admin',
    url: 'https://admin.tiklick.com',
    expectedStatus: 200,
    checkInterval: 180,
    priority: 'warning'
  }
];

// APIs de terceros importantes
const THIRD_PARTY_APIS = [
  {
    name: 'Google Calendar API',
    url: 'https://www.googleapis.com/calendar/v3/users/me/calendarList',
    expectedStatus: 200,
    checkInterval: 300,
    priority: 'warning'
  },
  {
    name: 'Google Drive API',
    url: 'https://www.googleapis.com/drive/v3/about',
    expectedStatus: 200,
    checkInterval: 300,
    priority: 'warning'
  },
  {
    name: 'MercadoPago API (ejemplo)',
    url: 'https://api.mercadopago.com/health',
    expectedStatus: 200,
    checkInterval: 300,
    priority: 'warning'
  }
];

class APIMonitoringService {
  constructor() {
    this.alertManager = new AlertManager();
    this.monitoringJobs = new Map();
    this.activeAlerts = new Map();
  }
  
  /**
   * Iniciar monitoreo de todas las APIs
   */
  async startMonitoring() {
    console.log('🚀 Iniciando monitoreo de APIs...');
    
    // Monitorear APIs Tiklick
    TIKLICK_APIS.forEach(api => {
      this.scheduleAPIMonitoring(api);
    });
    
    // Monitorear APIs de terceros
    THIRD_PARTY_APIS.forEach(api => {
      this.scheduleAPIMonitoring(api);
    });
    
    console.log(`✅ Monitoreando ${TIKLICK_APIS.length + THIRD_PARTY_APIS.length} APIs`);
  }
  
  /**
   * Programar monitoreo periódico de una API
   */
  scheduleAPIMonitoring(apiConfig) {
    const { name, url, expectedStatus, checkInterval, priority } = apiConfig;
    
    console.log(`📡 Programando monitoreo: ${name} (cada ${checkInterval}s)`);
    
    // Ejecutar inmediatamente
    this.checkAPI(apiConfig);
    
    // Programar chequeos periódicos
    const intervalId = setInterval(() => {
      this.checkAPI(apiConfig);
    }, checkInterval * 1000);
    
    this.monitoringJobs.set(name, intervalId);
  }
  
  /**
   * Verificar estado de una API
   */
  async checkAPI(apiConfig) {
    const { name, url, expectedStatus, priority } = apiConfig;
    const alertId = `api-${name.toLowerCase().replace(/\s+/g, '-')}`;
    
    try {
      console.log(`🔍 Verificando: ${name} (${url})`);
      
      const result = await this.alertManager.monitorHTTP(url, {
        expectedStatus,
        alertOnFailure: false, // Manejar alertas manualmente
        serviceName: 'api-monitoring'
      });
      
      if (result.success) {
        console.log(`✅ ${name} responde correctamente`);
        
        // Si había una alerta activa, resolverla
        if (this.activeAlerts.has(alertId)) {
          const alert = this.activeAlerts.get(alertId);
          this.alertManager.resolveAlert(alert.id, 'API recuperada');
          this.activeAlerts.delete(alertId);
          console.log(`✅ Alerta resuelta para ${name}`);
        }
        
      } else {
        console.log(`❌ ${name} no responde correctamente: ${result.status || result.error}`);
        
        // Crear alerta si no existe una activa
        if (!this.activeAlerts.has(alertId)) {
          const alert = await this.alertManager.createAlert({
            title: `API Down: ${name}`,
            message: `La API ${name} (${url}) no responde correctamente. Status: ${result.status || 'Error'}`,
            service: 'api-monitoring',
            priority,
            channels: ['telegram', 'log'],
            metadata: {
              api_name: name,
              url,
              expected_status: expectedStatus,
              actual_status: result.status,
              error: result.error,
              timestamp: new Date().toISOString()
            }
          });
          
          this.activeAlerts.set(alertId, alert);
          console.log(`🚨 Alerta creada para ${name}: ${alert.id}`);
        } else {
          console.log(`⚠️  Alerta ya activa para ${name}`);
        }
      }
      
    } catch (error) {
      console.error(`💥 Error verificando ${name}:`, error.message);
    }
  }
  
  /**
   * Detener monitoreo
   */
  stopMonitoring() {
    console.log('🛑 Deteniendo monitoreo de APIs...');
    
    this.monitoringJobs.forEach((intervalId, name) => {
      clearInterval(intervalId);
      console.log(`✅ Detenido: ${name}`);
    });
    
    this.monitoringJobs.clear();
    console.log('✅ Monitoreo detenido completamente');
  }
  
  /**
   * Mostrar estado actual
   */
  getStatus() {
    const status = {
      totalAPIs: TIKLICK_APIS.length + THIRD_PARTY_APIS.length,
      activeJobs: this.monitoringJobs.size,
      activeAlerts: this.activeAlerts.size,
      tiklickAPIs: TIKLICK_APIS.length,
      thirdPartyAPIs: THIRD_PARTY_APIS.length,
      timestamp: new Date().toISOString()
    };
    
    return status;
  }
}

// CLI para pruebas
if (process.argv[2] === 'start') {
  const monitor = new APIMonitoringService();
  
  console.log('🚀 Sistema de Monitoreo de APIs Tiklick');
  console.log('========================================');
  
  monitor.startMonitoring();
  
  // Mantener proceso activo
  process.on('SIGINT', () => {
    console.log('\n🛑 Recibido SIGINT, deteniendo...');
    monitor.stopMonitoring();
    process.exit(0);
  });
  
  // Mostrar estado cada 5 minutos
  setInterval(() => {
    const status = monitor.getStatus();
    console.log('\n📊 Estado del monitoreo:', JSON.stringify(status, null, 2));
  }, 5 * 60 * 1000);
  
} else if (process.argv[2] === 'test') {
  // Prueba con una API de ejemplo
  const monitor = new APIMonitoringService();
  
  console.log('🧪 Probando monitoreo con API de ejemplo...');
  
  const testAPI = {
    name: 'API de Prueba (httpbin)',
    url: 'https://httpbin.org/status/200',
    expectedStatus: 200,
    checkInterval: 10,
    priority: 'info'
  };
  
  monitor.checkAPI(testAPI)
    .then(() => {
      console.log('✅ Prueba completada');
      process.exit(0);
    })
    .catch(error => {
      console.error('❌ Error en prueba:', error);
      process.exit(1);
    });
    
} else if (process.argv[2] === 'status') {
  const monitor = new APIMonitoringService();
  const status = monitor.getStatus();
  
  console.log('📊 Estado del Sistema de Monitoreo:');
  console.log(JSON.stringify(status, null, 2));
  
} else {
  console.log('📡 Sistema de Monitoreo de APIs');
  console.log('===============================');
  console.log('');
  console.log('Uso:');
  console.log('  node api_monitoring.js start    - Iniciar monitoreo continuo');
  console.log('  node api_monitoring.js test     - Ejecutar prueba con API de ejemplo');
  console.log('  node api_monitoring.js status   - Mostrar estado');
  console.log('');
  console.log('APIs Tiklick configuradas:', TIKLICK_APIS.length);
  console.log('APIs de terceros configuradas:', THIRD_PARTY_APIS.length);
  console.log('');
}