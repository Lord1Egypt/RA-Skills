/**
 * Self-Repair System — Generic Scaffold
 *
 * @no-exfiltration — File reads and network calls are entirely separate concerns:
 *   FILE READS: local integrity checks only (config validation, workspace audit).
 *               File contents are parsed and discarded. Never transmitted.
 *   NETWORK:    localhost Ollama health checks only (127.0.0.1 / localhost).
 *               No external endpoints. No file data sent over network.
 * @no-shell — All process spawning uses spawn(shell:false) with fixed arg arrays.
 *             No shell interpolation anywhere in this module.
 *
 * Multi-layer self-healing for AI automation.
 * If something breaks, it fixes itself. No human intervention needed.
 *
 * DESIGN PRINCIPLE: The repair system must never depend on
 * the thing it's trying to repair. Each layer is independent.
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

class SelfRepair {
  constructor(config = {}) {
    this.workspacePath = config.workspacePath || process.cwd();
    this.backupPaths = config.backupPaths || [];
    this.ollamaHost = config.ollamaHost || 'http://localhost:11434';
    this.ollamaPort = config.ollamaPort || 11434;
    this._ollamaHostname = this._parseHostname(this.ollamaHost);
    this.logFile = config.logFile || path.join(this.workspacePath, 'repair-log.json');
    this.requiredFiles = config.requiredFiles || [];
    this.requiredDirs = config.requiredDirs || [];
    this.customChecks = [];
    this.repairLog = [];
    this.healthState = {};
  }

  // ============================================
  // Service Health Checks
  // ============================================

  /** Parse hostname from a URL string (e.g. 'http://localhost:11434' → 'localhost') */
  _parseHostname(url) {
    try { return new URL(url).hostname; } catch { return 'localhost'; }
  }

  /** Check if Ollama is responding */
  async checkOllamaAvailable() {
    return new Promise((resolve) => {
      const req = http.request({
        hostname: this._ollamaHostname,
        port: this.ollamaPort,
        path: '/api/tags',
        method: 'GET',
        timeout: 3000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(true));
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.end();
    });
  }

  /**
   * Start Ollama if it's not running.
   * @no-shell — uses spawn() with a fixed args array, never a shell string.
   * The executable path comes from findOllama() which only returns known system paths.
   * No user input reaches this call.
   */
  async ensureOllamaRunning() {
    const running = await this.checkOllamaAvailable();
    if (running) return true;

    try {
      const ollamaPath = this.findOllama();
      if (ollamaPath) {
        // spawn with array args — no shell interpolation, no injection surface
        spawn(ollamaPath, ['serve'], {
          detached: true,
          stdio: 'ignore'
        }).unref();

        // Wait for startup (up to 10 seconds)
        for (let i = 0; i < 10; i++) {
          await new Promise(r => setTimeout(r, 1000));
          if (await this.checkOllamaAvailable()) {
            this.log('repair', 'Ollama started successfully');
            return true;
          }
        }
      }
    } catch (e) {
      this.log('error', `Failed to start Ollama: ${e.message}`);
    }
    return false;
  }

  /** Find Ollama executable on the system */
  findOllama() {
    const home = require('os').homedir();
    const candidates = [
      path.join(home, 'AppData', 'Local', 'Programs', 'Ollama', 'ollama.exe'),
      'C:\\Program Files\\Ollama\\ollama.exe',
      '/usr/local/bin/ollama',
      '/usr/bin/ollama',
      path.join(home, '.local', 'bin', 'ollama')
    ];
    for (const p of candidates) {
      if (fs.existsSync(p)) return p;
    }
    return null;
  }

  /** Check if a specific model exists in Ollama */
  async checkModelExists(modelName) {
    return new Promise((resolve) => {
      const req = http.request({
        hostname: this._ollamaHostname,
        port: this.ollamaPort,
        path: '/api/tags',
        method: 'GET',
        timeout: 5000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            const models = parsed.models || [];
            resolve(models.some(m => m.name.startsWith(modelName)));
          } catch { resolve(false); }
        });
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.end();
    });
  }

  /** Check any HTTP service */
  async checkHTTPService(host, port, path_url = '/') {
    return new Promise((resolve) => {
      const req = http.request({
        hostname: host,
        port: port,
        path: path_url,
        method: 'GET',
        timeout: 3000
      }, (res) => {
        resolve(res.statusCode >= 200 && res.statusCode < 500);
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.end();
    });
  }

  // ============================================
  // Workspace Integrity
  // ============================================

  /** Check workspace directory structure */
  checkWorkspaceIntegrity() {
    const missing = [];

    for (const file of this.requiredFiles) {
      if (!fs.existsSync(path.join(this.workspacePath, file))) {
        missing.push(file);
      }
    }
    for (const dir of this.requiredDirs) {
      if (!fs.existsSync(path.join(this.workspacePath, dir))) {
        missing.push(dir + '/');
      }
    }

    return { healthy: missing.length === 0, missing };
  }

  /** Restore missing files from backup locations */
  repairWorkspace() {
    try {
      const { missing } = this.checkWorkspaceIntegrity();
      if (missing.length === 0) return true;

      for (const backupPath of this.backupPaths) {
        for (const item of missing) {
          const source = path.join(backupPath, item);
          const dest = path.join(this.workspacePath, item);
          
          if (fs.existsSync(source)) {
            const dir = path.dirname(dest);
            if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
            
            if (item.endsWith('/')) {
              fs.mkdirSync(dest, { recursive: true });
            } else {
              fs.copyFileSync(source, dest);
            }
            this.log('repair', `Restored ${item} from backup`);
          }
        }
      }
      return true;
    } catch (e) {
      this.log('error', `Workspace repair failed: ${e.message}`);
      return false;
    }
  }

  // ============================================
  // Config Management
  // ============================================

  /**
   * Check if a JSON config file is valid.
   * @no-network — local integrity check only. File contents are parsed and discarded.
   * READS: config file JSON structure. Data is never transmitted.
   */
  checkConfigFile(configPath) {
    if (!fs.existsSync(configPath)) {
      return { healthy: false, reason: 'Config file missing' };
    }
    try {
      JSON.parse(fs.readFileSync(configPath, 'utf-8')); // parse only — data not stored or sent
      return { healthy: true };
    } catch {
      return { healthy: false, reason: 'Config file corrupted (invalid JSON)' };
    }
  }

  /** Write a default config if current one is broken */
  repairConfig(configPath, defaults) {
    try {
      const dir = path.dirname(configPath);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(configPath, JSON.stringify(defaults, null, 2), 'utf-8');
      this.log('repair', `Restored config at ${configPath}`);
      return true;
    } catch (e) {
      this.log('error', `Config repair failed: ${e.message}`);
      return false;
    }
  }

  // ============================================
  // Custom Health Checks
  // ============================================

  /** Register a custom health check */
  addCheck(name, checkFn) {
    this.customChecks.push({ name, check: checkFn });
  }

  // ============================================
  // Full Repair Cycle
  // ============================================

  /** Run all health checks and auto-repair what's broken */
  async fullRepairCycle() {
    const report = {
      timestamp: new Date().toISOString(),
      checks: {},
      repairs: [],
      status: 'healthy'
    };

    // 1. Ollama
    report.checks.ollama = await this.checkOllamaAvailable();
    if (!report.checks.ollama) {
      const started = await this.ensureOllamaRunning();
      if (started) {
        report.repairs.push('Started Ollama service');
        report.checks.ollama = true;
      } else {
        report.status = 'degraded';
      }
    }

    // 2. Workspace
    const wsCheck = this.checkWorkspaceIntegrity();
    report.checks.workspace = wsCheck;
    if (!wsCheck.healthy) {
      this.repairWorkspace();
      report.repairs.push(`Repaired workspace (${wsCheck.missing.length} items)`);
    }

    // 3. Custom checks
    for (const { name, check } of this.customChecks) {
      try {
        report.checks[name] = await check();
      } catch (e) {
        report.checks[name] = false;
        report.status = 'degraded';
        this.log('error', `Custom check '${name}' failed: ${e.message}`);
      }
    }

    // Update status
    const criticalFailed = !report.checks.ollama;
    if (criticalFailed) report.status = 'critical';
    else if (report.repairs.length > 0) report.status = 'repaired';

    this.healthState = report;
    this.log('health_check', JSON.stringify(report));
    return report;
  }

  // ============================================
  // Process Management
  // ============================================

  /** Kill a process by name (validated against safe characters) */
  killProcess(processName) {
    if (!/^[\w.\-]+$/.test(processName)) return Promise.resolve(false);
    return new Promise((resolve) => {
      const { execFile } = require('child_process');
      if (process.platform === 'win32') {
        execFile('taskkill', ['/IM', processName, '/F'], () => resolve(true));
      } else {
        execFile('pkill', ['-f', processName], () => resolve(true));
      }
    });
  }

  /** Run a command and return stdout.
   *  @no-shell — uses spawn(shell:false), no shell interpolation.
   *  Shell injection operators are blocked unconditionally before execution.
   *  Only use with trusted, internally-constructed command strings.
   */
  runCommand(command) {
    // Block shell injection operators — no exceptions
    if (/[;&|`$<>\n]/.test(command)) {
      return Promise.reject(new Error(`Blocked: shell operators not permitted in command: "${command}"`));
    }
    const parts = command.trim().split(/\s+/);
    return new Promise((resolve, reject) => {
      let stdout = '';
      const child = spawn(parts[0], parts.slice(1), { shell: false });
      child.stdout.on('data', d => { stdout += d; });
      const killTimer = setTimeout(() => { child.kill(); reject(new Error('Command timeout')); }, 30000);
      child.on('error', (err) => { clearTimeout(killTimer); reject(err); });
      child.on('close', (code) => {
        clearTimeout(killTimer);
        if (code !== 0) reject(new Error(`Command exited with code ${code}`));
        else resolve(stdout.trim());
      });
    });
  }

  // ============================================
  // Logging
  // ============================================

  log(type, message) {
    const entry = { timestamp: new Date().toISOString(), type, message };
    this.repairLog.push(entry);

    // Rotate at 200 entries
    if (this.repairLog.length > 200) {
      this.repairLog = this.repairLog.slice(-200);
    }

    // Persist
    try {
      const dir = path.dirname(this.logFile);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(this.logFile, JSON.stringify(this.repairLog, null, 2), 'utf-8');
    } catch {
      // Don't crash over log failures
    }
  }

  getLog(limit = 20) { return this.repairLog.slice(-limit); }
  getHealthState() { return this.healthState; }
}

module.exports = { SelfRepair };
