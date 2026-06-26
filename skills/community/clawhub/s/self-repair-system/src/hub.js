/**
 * Automation Hub — Central Orchestrator
 * 
 * Ties together self-repair and scheduled routines.
 * One import, one start(), everything runs.
 */

const { SelfRepair } = require('./self-repair');
const { RoutineManager } = require('./routine-manager');
const http = require('http');

class AutomationHub {
  constructor(config = {}) {
    this.config = {
      workspacePath: config.workspacePath || process.cwd(),
      ollamaHost: config.ollamaHost || 'http://localhost:11434',
      ollamaPort: config.ollamaPort || 11434,
      defaultModel: config.defaultModel || 'llama3.1:8b',
      backupPaths: config.backupPaths || [],
      requiredFiles: config.requiredFiles || [],
      requiredDirs: config.requiredDirs || [],
      healthCheckInterval: config.healthCheckInterval || 5 * 60 * 1000, // 5 min
      ...config
    };

    // Initialize subsystems
    this.repair = new SelfRepair({
      workspacePath: this.config.workspacePath,
      backupPaths: this.config.backupPaths,
      ollamaPort: this.config.ollamaPort,
      requiredFiles: this.config.requiredFiles,
      requiredDirs: this.config.requiredDirs
    });

    this.routines = new RoutineManager();
    this.running = false;
    this.healthTimer = null;
  }

  /** Boot everything up */
  async start() {
    console.log('[Hub] Starting automation hub...');

    // 1. Run initial health check + repair
    const health = await this.repair.fullRepairCycle();
    console.log(`[Hub] Initial health: ${health.status}`);
    if (health.repairs.length > 0) {
      console.log(`[Hub] Auto-repairs: ${health.repairs.join(', ')}`);
    }

    // 2. Start periodic health checks
    this.healthTimer = setInterval(async () => {
      const h = await this.repair.fullRepairCycle();
      if (h.status !== 'healthy') {
        console.log(`[Hub] Health: ${h.status} — repairs: ${h.repairs.join(', ')}`);
      }
    }, this.config.healthCheckInterval);

    // 3. Start routine manager
    this.routines.start();

    this.running = true;
    console.log('[Hub] All systems online.');
    return health;
  }

  /** Shut down cleanly */
  async stop() {
    if (this.healthTimer) clearInterval(this.healthTimer);
    this.routines.stop();
    this.running = false;
    console.log('[Hub] Shut down.');
  }

  /** Send a prompt to Ollama and get a response */
  async ask(prompt, model = null) {
    const targetModel = model || this.config.defaultModel;
    
    return new Promise((resolve, reject) => {
      const body = JSON.stringify({
        model: targetModel,
        prompt: prompt,
        stream: false
      });

      const hostname = (() => { try { return new URL(this.config.ollamaHost).hostname; } catch { return 'localhost'; } })();
      const req = http.request({
        hostname,
        port: this.config.ollamaPort,
        path: '/api/generate',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        },
        timeout: 120000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            resolve(parsed.response || '');
          } catch (e) {
            reject(new Error('Failed to parse Ollama response'));
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Ollama timeout')); });
      req.write(body);
      req.end();
    });
  }

  /** Ask Ollama with the default model */
  async smartAsk(taskText) {
    const response = await this.ask(taskText);
    return { response, model: this.config.defaultModel };
  }

  /** Schedule a recurring task */
  schedule(name, cronExpr, taskFn) {
    this.routines.add(name, cronExpr, taskFn);
  }

  /** Get current system status */
  status() {
    return {
      running: this.running,
      health: this.repair.getHealthState(),
      recentLog: this.repair.getLog(10),
      routines: this.routines.list()
    };
  }
}

module.exports = { AutomationHub };
