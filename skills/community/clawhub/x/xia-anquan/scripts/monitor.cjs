#!/usr/bin/env node
/**
 * CIK Security Monitor - Real-time daemon
 * Runs periodic audits and alerts on anomalies
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const HOME = process.env.HOME || process.env.USERPROFILE;
const WORKSPACE = path.join(HOME, '.openclaw', 'workspace');
const AUDIT_DIR = path.join(HOME, '.cik-audit');
const STATE_FILE = path.join(AUDIT_DIR, 'monitor-state.json');
const LOG_FILE = path.join(AUDIT_DIR, 'monitor.log');

const args = process.argv.slice(2);
const daemon = args.includes('--daemon');
const interval = parseInt(extractArg(args, '--interval') || '300') * 1000; // default 5min
const verbose = args.includes('--verbose');

function extractArg(arr, flag) {
  const idx = arr.indexOf(flag);
  return idx !== -1 && arr[idx + 1] && !arr[idx + 1].startsWith('-') ? arr[idx + 1] : null;
}

function log(msg) {
  const entry = `[${new Date().toISOString()}] ${msg}`;
  fs.appendFileSync(LOG_FILE, entry + '\n');
  if (verbose) console.log(entry);
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { lastRun: null, lastAlert: null, consecutiveAlerts: 0 };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function runAudit() {
  return new Promise((resolve, reject) => {
    const child = spawn('node', [
      path.join(__dirname, 'audit.cjs'), '--json'
    ], { cwd: WORKSPACE });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', d => stdout += d);
    child.stderr.on('data', d => stderr += d);
    child.on('close', code => {
      try {
        const result = stdout.trim() ? JSON.parse(stdout) : null;
        resolve({ code, result, stderr });
      } catch (e) {
        reject(new Error(`Audit parse failed: ${e.message}\n${stderr}`));
      }
    });
    child.on('error', reject);
  });
}

function checkAnomalies(auditResult) {
  const anomalies = [];
  
  // Identity: file missing
  (auditResult.checks.identity || []).forEach(r => {
    if (r.status === 'MISSING') anomalies.push(`🚨 Identity文件丢失: ${r.file}`);
    if (r.status === 'SUSPICIOUS') anomalies.push(`🚨 Identity文件可疑: ${r.file} (${r.detail})`);
  });
  
  // Knowledge: suspicious patterns
  (auditResult.checks.knowledge || []).forEach(r => {
    if (r.status === 'FOUND') anomalies.push(`⚠️ Knowledge污染: ${r.file} (${r.detail})`);
    if (r.status === 'SUSPICIOUS') anomalies.push(`⚠️ Knowledge文件可疑: ${r.file}`);
  });
  
  // Capability: critical issues
  const cap = auditResult.checks.capability;
  const capResults = Array.isArray(cap) ? cap : (cap?.results || []);
  capResults.forEach(r => {
    if (r.level === 'CRITICAL') anomalies.push(`🚨 可疑脚本: ${r.file} (${r.detail})`);
    if (r.level === 'HIGH') anomalies.push(`⚠️ 高风险脚本: ${r.file} (${r.detail})`);
  });
  
  return anomalies;
}

async function tick() {
  const state = loadState();
  const now = new Date().toISOString();
  
  log('开始安全检查...');
  
  try {
    const { code, result } = await runAudit();
    
    if (code === 2 && result) {
      // Critical issues found
      const anomalies = checkAnomalies(result);
      if (anomalies.length > 0) {
        state.consecutiveAlerts++;
        state.lastAlert = now;
        
        log(`🚨 第${state.consecutiveAlerts}次告警`);
        for (const a of anomalies) {
          log(a);
          // Write to alerts.log for external monitoring
          fs.appendFileSync(
            path.join(AUDIT_DIR, 'alerts.log'),
            `[${now}] ${a}\n`
          );
        }
        
        // Alert suppression: only report every 3 consecutive alerts
        if (state.consecutiveAlerts === 1 || state.consecutiveAlerts % 3 === 0) {
          console.log('\n🛡️ CIK Security Alert\n');
          for (const a of anomalies) console.log(a);
          console.log(`\n时间: ${now}\n`);
        }
      }
    } else {
      if (state.consecutiveAlerts > 0) {
        log(`✅ 安全问题已修复 (连续${state.consecutiveAlerts}次告警后)");
      }
      state.consecutiveAlerts = 0;
    }
    
    state.lastRun = now;
    saveState(state);
    
  } catch (e) {
    log(`错误: ${e.message}`);
    console.error('Audit failed:', e.message);
  }
}

async function main() {
  if (!daemon) {
    await tick();
    return;
  }
  
  // Daemon mode
  log('CIK Security Monitor started (daemon)');
  console.log('🛡️ CIK Security Monitor running...');
  console.log(`   检查间隔: ${interval / 1000}s`);
  console.log(`   日志: ${LOG_FILE}\n`);
  
  // Run immediately, then on interval
  await tick();
  setInterval(tick, interval);
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
