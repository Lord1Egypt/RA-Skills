#!/usr/bin/env node
// System Monitor Pro - OpenClaw System Monitoring Skill
// Usage: node monitor.js [--remote user@host] [--json] [--alert-only]

const { execSync } = require('child_process');
const os = require('os');

const args = process.argv.slice(2);
const remoteHost = args.includes('--remote') ? args[args.indexOf('--remote') + 1] : null;
const jsonMode = args.includes('--json');
const alertOnly = args.includes('--alert-only');

// Thresholds
const THRESH = { cpu: 80, mem: 85, disk: 90, gpu: 90 };

function run(cmd, timeout = 8000) {
  try { return execSync(cmd, { timeout, encoding: 'utf8', stdio: ['pipe','pipe','pipe'] }).trim(); }
  catch { return null; }
}

function remoteRun(cmd) {
  // 用双引号包裹SSH命令，避免单引号嵌套问题
  const escaped = cmd.replace(/"/g, '\\"');
  return run(`ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no ${remoteHost} "${escaped}"`);
}

function exec(cmd) { return remoteHost ? remoteRun(cmd) : run(cmd); }

// ── Detect OS ──
function detectOS() {
  const p = exec('uname -s') || '';
  return p.includes('Darwin') ? 'macos' : 'linux';
}

// ── CPU ──
function getCPU(osType) {
  if (osType === 'macos') {
    const r = exec("top -l 1 -n 0 2>/dev/null | grep 'CPU usage' | awk '{print $3}' | tr -d '%'");
    return parseFloat(r) || 0;
  }
  // Linux: read /proc/stat
  const r = exec("cat /proc/loadavg | cut -d' ' -f1");
  const load = parseFloat(r) || 0;
  const cores = parseInt(exec("nproc") || '1');
  return Math.min(Math.round(load / cores * 100), 100);
}

// ── Memory ──
function getMemory(osType) {
  if (osType === 'macos') {
    const total = parseInt(exec('/usr/sbin/sysctl -n hw.memsize') || '0') / 1048576;
    const vm = exec('vm_stat') || '';
    const ps = 16384;
    const active = parseInt((vm.match(/Pages active:\s+(\d+)/) || [0,0])[1]) * ps / 1048576;
    const wired = parseInt((vm.match(/Pages wired down:\s+(\d+)/) || [0,0])[1]) * ps / 1048576;
    const used = Math.round(active + wired);
    return { used, total: Math.round(total), pct: total > 0 ? Math.round(used/total*100) : 0 };
  }
  // Linux: parse /proc/meminfo directly
  const info = exec("cat /proc/meminfo") || '';
  const totalKB = parseInt((info.match(/MemTotal:\s+(\d+)/) || [0,0])[1]);
  const availKB = parseInt((info.match(/MemAvailable:\s+(\d+)/) || [0,0])[1]);
  const total = Math.round(totalKB / 1024);
  const used = Math.round((totalKB - availKB) / 1024);
  return { used, total, pct: total > 0 ? Math.round(used/total*100) : 0 };
}

// ── Disk ──
function getDisk() {
  const r = exec("df -h / | tail -1") || '';
  const parts = r.split(/\s+/);
  const pct = parseInt((parts[4] || '0').replace('%',''));
  return { used: parts[2] || '?', total: parts[1] || '?', pct };
}

// ── GPU ──
function getGPU() {
  const r = exec('nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits 2>/dev/null');
  if (!r) return null;
  const [name, util, memUsed, memTotal, temp] = r.split(',').map(s => s.trim());
  return { name, util: parseInt(util), memUsed: parseInt(memUsed), memTotal: parseInt(memTotal), temp: parseInt(temp) };
}

// ── Gateway ──
function getGateway() {
  const r = exec('openclaw gateway status 2>&1') || '';
  const running = r.includes('running');
  const pid = (r.match(/pid (\d+)/) || [0,'?'])[1];
  return { running, pid };
}

// ── Cron ──
function getCrons() {
  const r = exec('openclaw cron list 2>&1') || '';
  const lines = r.split('\n').slice(1).filter(l => l.trim());
  let ok = 0, err = 0;
  const items = [];
  lines.forEach(l => {
    // 格式: ID  Name  Schedule  Next  Last  Status  Target  Agent
    const cols = l.split(/\s{2,}/).map(s => s.trim());
    // 找status列（ok/error）
    const statusIdx = cols.findIndex(c => c === 'ok' || c === 'error');
    const status = statusIdx >= 0 ? cols[statusIdx] : '?';
    const name = cols[1] || '?';
    if (status === 'ok') ok++; else err++;
    items.push({ name, status });
  });
  return { total: lines.length, ok, err, items };
}

// ── Uptime ──
function getUptime(osType) {
  if (osType === 'macos') return exec("uptime | sed 's/.*up //' | sed 's/,.*//'") || '?';
  return exec('uptime -p') || '?';
}

// ── Visual Bar ──
function bar(pct, width = 10) {
  const filled = Math.round(pct / 100 * width);
  const empty = width - filled;
  const ch = pct > THRESH.cpu ? '🟥' : pct > 60 ? '🟨' : '🟩';
  return ch.repeat(filled) + '⬜'.repeat(empty);
}

function alertTag(pct, thresh) {
  if (pct >= thresh) return ' ⚠️';
  return '';
}

// ── Main ──
function main() {
  const osType = detectOS();
  const hostname = exec('hostname') || '?';
  const cpu = getCPU(osType);
  const mem = getMemory(osType);
  const disk = getDisk();
  const gpu = getGPU();
  const gw = getGateway();
  const crons = getCrons();
  const uptime = getUptime(osType);

  const data = { hostname, os: osType, cpu, mem, disk, gpu, gateway: gw, crons, uptime };

  if (jsonMode) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  const alerts = [];
  if (cpu >= THRESH.cpu) alerts.push(`CPU ${cpu}%`);
  if (mem.pct >= THRESH.mem) alerts.push(`内存 ${mem.pct}%`);
  if (disk.pct >= THRESH.disk) alerts.push(`磁盘 ${disk.pct}%`);
  if (gpu && gpu.util >= THRESH.gpu) alerts.push(`GPU ${gpu.util}%`);
  if (!gw.running) alerts.push('Gateway 停止');
  if (crons.err > 0) alerts.push(`${crons.err}个Cron异常`);

  if (alertOnly && alerts.length === 0) {
    console.log('✅ 系统正常，无告警');
    return;
  }

  const lines = [];
  const tag = remoteHost ? ` (${remoteHost})` : ' (本机)';
  lines.push(`🦞 OpenClaw 系统状态 — ${hostname}${tag}`);
  lines.push('━'.repeat(36));
  lines.push(`🖥️ CPU    ${bar(cpu)} ${cpu}%${alertTag(cpu, THRESH.cpu)}`);
  lines.push(`💾 内存   ${bar(mem.pct)} ${mem.pct}%  ${(mem.used/1024).toFixed(1)}/${(mem.total/1024).toFixed(1)}GB${alertTag(mem.pct, THRESH.mem)}`);
  lines.push(`💿 磁盘   ${bar(disk.pct)} ${disk.pct}%  ${disk.used}/${disk.total}${alertTag(disk.pct, THRESH.disk)}`);

  if (gpu) {
    const vramPct = gpu.memTotal > 0 ? Math.round(gpu.memUsed/gpu.memTotal*100) : 0;
    lines.push(`🎮 GPU    ${bar(gpu.util)} ${gpu.util}%  ${gpu.name}`);
    lines.push(`📦 VRAM   ${bar(vramPct)} ${vramPct}%  ${gpu.memUsed}/${gpu.memTotal}MB  ${gpu.temp}°C`);
  }

  lines.push(`⏱️ 运行   ${uptime}`);
  lines.push('━'.repeat(36));
  lines.push(`🌐 Gateway ${gw.running ? '● 运行中' : '⊘ 停止'} ${gw.running ? '(pid '+gw.pid+')' : '⚠️'}`);
  lines.push(`⏰ Cron    ${crons.ok}/${crons.total} 正常${crons.err > 0 ? ' ⚠️ '+crons.err+'个异常' : ''}`);

  if (!alertOnly) {
    crons.items.forEach(c => {
      const icon = c.status === 'ok' ? '✅' : '❌';
      lines.push(`   ${icon} ${c.name}`);
    });
  }

  lines.push('━'.repeat(36));

  if (alerts.length > 0) {
    lines.push(`🔔 告警: ${alerts.join(' | ')}`);
  } else {
    lines.push('✅ 一切正常');
  }

  console.log(lines.join('\n'));
}

main();
