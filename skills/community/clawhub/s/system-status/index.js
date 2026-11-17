const { execSync } = require('child_process');
const os = require('os');

function getDiskInfo() {
  try {
    const out = execSync('wmic logicaldisk where "DeviceID=\'C:\'" get Size,FreeSpace /format:list', { encoding: 'utf8' });
    const size = parseInt(out.match(/Size=(\d+)/)?.[1] || '0');
    const free = parseInt(out.match(/FreeSpace=(\d+)/)?.[1] || '0');
    return { totalGB: (size / 1e9).toFixed(1), freeGB: (free / 1e9).toFixed(1), usedPct: ((1 - free / size) * 100).toFixed(1) };
  } catch { return null; }
}

function getMemoryInfo() {
  const total = os.totalmem();
  const free = os.freemem();
  return { totalGB: (total / 1e9).toFixed(1), freeGB: (free / 1e9).toFixed(1), usedPct: ((1 - free / total) * 100).toFixed(1) };
}

function getCPUInfo() {
  try {
    const out = execSync('wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors /format:list', { encoding: 'utf8' });
    const name = out.match(/Name=(.+)/)?.[1]?.trim() || 'Unknown';
    const cores = out.match(/NumberOfCores=(\d+)/)?.[1] || '?';
    const threads = out.match(/NumberOfLogicalProcessors=(\d+)/)?.[1] || '?';
    return { name, cores, threads };
  } catch { return null; }
}

function getTopDirs() {
  try {
    const out = execSync('powershell -Command "Get-ChildItem C:\\ -Directory | ForEach-Object { $size = (Get-ChildItem $_.FullName -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum -ErrorAction SilentlyContinue).Sum / 1MB; Write-Output \\"$($_.Name) => $([math]::Round($size,0)) MB\\" }"', { encoding: 'utf8', timeout: 15000 });
    return out.trim().split('\n').filter(Boolean);
  } catch { return []; }
}

function report() {
  const disk = getDiskInfo();
  const mem = getMemoryInfo();
  const cpu = getCPUInfo();
  const topDirs = getTopDirs();

  let lines = ['=== System Status ===', ''];
  if (cpu) lines.push(`CPU: ${cpu.name} (${cpu.cores}C/${cpu.threads}T)`);
  if (mem) lines.push(`RAM: ${mem.freeGB} GB free / ${mem.totalGB} GB total (${mem.usedPct}% used)`);
  if (disk) lines.push(`Disk C: ${disk.freeGB} GB free / ${disk.totalGB} GB total (${disk.usedPct}% used)`);
  lines.push('');
  lines.push('Top C:\\ directories by file count:');
  topDirs.forEach(d => lines.push(`  ${d}`));
  lines.push('');
  lines.push(`Uptime: ${os.uptime()}s`);

  console.log(lines.join('\n'));
}

if (require.main === module) report();
module.exports = { report, getDiskInfo, getMemoryInfo, getCPUInfo };
