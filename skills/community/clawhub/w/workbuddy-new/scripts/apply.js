const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFile, spawn } = require('child_process');

function log(skillDir, msg) {
  const t = new Date().toISOString().replace('T', ' ').split('.')[0];
  const logFile = path.join(skillDir, 'applied-asar-log.txt');
  try { fs.appendFileSync(logFile, `${t} ${msg}\n`, 'utf8'); } catch (_) {}
}

function locateAppAsar() {
  const localApp = process.env.LOCALAPPDATA || 'C:\\Users\\qingc\\AppData\\Local';
  const cand = path.join(localApp, 'Programs', 'WorkBuddy', 'resources', 'app.asar');
  if (fs.existsSync(cand)) return cand;
  return 'C:\\Users\\qingc\\AppData\\Local\\Programs\\WorkBuddy\\resources\\app.asar';
}

function locateExe() {
  const localApp = process.env.LOCALAPPDATA || 'C:\\Users\\qingc\\AppData\\Local';
  const cand = path.join(localApp, 'Programs', 'WorkBuddy', 'WorkBuddy.exe');
  if (fs.existsSync(cand)) return cand;
  return 'C:\\Users\\qingc\\AppData\\Local\\Programs\\WorkBuddy\\WorkBuddy.exe';
}

// 真正的安装步骤：杀主进程解锁 -> 覆盖 app.asar -> 重启。
// 由计划任务触发（WorkBuddy 已关闭，文件解锁）。
function runInstall() {
  const skillDir = path.dirname(__dirname);
  const appAsar = locateAppAsar();
  const patchedAsar = path.join(process.env.TEMP || os.tmpdir(), 'wb-dream-skin', '_patched.asar');
  log(skillDir, '=== install start (post-kill) ===');
  log(skillDir, `PatchedAsar=${patchedAsar}`);
  if (!fs.existsSync(patchedAsar)) {
    log(skillDir, 'ERROR: patched asar missing');
    process.exit(1);
  }
  fs.copyFileSync(patchedAsar, appAsar);
  log(skillDir, 'app.asar overwritten with skinned copy');
  setTimeout(() => {
    const exe = locateExe();
    spawn(exe, [], { detached: true, windowsHide: false, stdio: 'ignore' }).unref();
    log(skillDir, `relaunched WorkBuddy from ${exe}`);
  }, 800);
}

// 调度一次性任务：跑临时 ps1（杀主进程 -> 等 2s -> node apply.js --install）
function runSchedule() {
  const skillDir = path.dirname(__dirname);
  const tmpDir = path.join(process.env.TEMP || os.tmpdir(), 'wb-dream-skin');
  fs.mkdirSync(tmpDir, { recursive: true });
  const ps1 = path.join(tmpDir, 'kill-restart.ps1');
  const js = path.join(__dirname, 'apply.js');
  const node = process.execPath;
  const ps = [
    '$ErrorActionPreference="SilentlyContinue"',
    `Get-CimInstance Win32_Process -Filter "Name='WorkBuddy.exe'" | Where-Object { $_.CommandLine -notmatch '--type=' -and $_.CommandLine -notmatch 'codebuddy' -and $_.CommandLine -notmatch 'app.asar.main' -and $_.CommandLine -notmatch '--require' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }`,
    'Start-Sleep -Seconds 2',
    `& '${node}' '${js}' --install`,
  ].join('\n');
  fs.writeFileSync(ps1, ps, 'utf8');
  log(skillDir, `wrote temp ps1: ${ps1}`);

  const taskName = 'ApplyWorkBuddySkin';
  const next = new Date(Date.now() + 60 * 1000);
  const t = next.toTimeString().slice(0, 8);
  const tr = `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ${ps1}`;
  log(skillDir, 'scheduling detached install+restart task');
  // 先删旧任务（忽略错误），再创建。直接调 schtasks.exe，不经过 cmd 以避免引号剥离。
  execFile('schtasks', ['/delete', '/tn', taskName, '/F'], { windowsHide: true }, () => {
    execFile('schtasks', ['/create', '/tn', taskName, '/tr', tr, '/sc', 'once', '/st', t, '/F'],
      { windowsHide: true }, (err, stdout, stderr) => {
        if (stdout) log(skillDir, `schedule stdout: ${stdout.trim()}`);
        if (stderr) log(skillDir, `schedule stderr: ${stderr.trim()}`);
        if (err) log(skillDir, `schedule error: ${err.message}`);
        else log(skillDir, `scheduled install task at ${t}`);
      });
  });
}

function runApply() {
  const skillDir = path.dirname(__dirname);
  const appAsar = locateAppAsar();
  const backupAsar = `${appAsar}.bak`;
  const patchedAsar = path.join(process.env.TEMP || os.tmpdir(), 'wb-dream-skin', '_patched.asar');

  log(skillDir, '=== apply start ===');
  log(skillDir, `AppAsar=${appAsar}`);
  log(skillDir, `PatchedAsar=${patchedAsar}`);

  if (!fs.existsSync(patchedAsar)) {
    log(skillDir, 'ERROR: patched asar missing — run asar-patch.js first');
    process.exit(1);
  }

  if (!fs.existsSync(backupAsar)) {
    fs.copyFileSync(appAsar, backupAsar);
    log(skillDir, `backup written: ${backupAsar}`);
  } else {
    log(skillDir, 'backup already exists, kept');
  }

  runSchedule();
}

function main() {
  const args = process.argv.slice(2);
  if (args.includes('--install')) runInstall();
  else runApply();
}

main();
