'use strict';
// WorkBuddy data-directory migration (universal edition).
// Copy %USERPROFILE%\.workbuddy -> <best non-system drive>:\workbuddy-data,
// then replace the C: dir with a junction pointing to the new location.
// Node-native throughout (fs.cpSync + fs.symlinkSync) — no powershell,
// no robocopy, no mklink. Runs from a staged neutral node (see migrate.bat)
// to avoid self-locking the node.exe that lives inside the migrated dir.
const fs = require('fs');
const cp = require('child_process');
const os = require('os');

const HOME = os.homedir();
const SRC = HOME + '/.workbuddy';
const SRC_OLD = HOME + '/.workbuddy_old';
const SYS = (process.env.SystemRoot || 'C:/Windows') + '/System32';

// Auto-pick a non-system fixed drive with the most free space.
function pickDrive() {
  const letters = 'DEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  let best = null, bestFree = 0;
  for (const d of letters) {
    try {
      const st = fs.statfsSync(d + ':');
      const free = st.bavail * st.bsize;
      if (free > bestFree) { bestFree = free; best = d; }
    } catch (e) {}
  }
  return best;
}
const DST_DRIVE = pickDrive();
if (!DST_DRIVE) {
  console.log('No suitable non-system drive found. Aborting.');
  process.exit(1);
}
const DST = DST_DRIVE + ':/workbuddy-data';
const LOG = DST_DRIVE + ':/migrate.log';

function log(s) {
  const t = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const line = '[' + t + '] ' + s;
  try { fs.appendFileSync(LOG, line + '\n'); } catch (e) {}
  console.log(line);
}
function sh(cmd, args) {
  return cp.spawnSync(cmd, args, { encoding: 'utf8', shell: false, timeout: 20000 });
}
function sleep(ms) { try { cp.execSync(SYS + '/timeout.exe /t ' + Math.ceil(ms / 1000) + ' /nobreak', { stdio: 'ignore' }); } catch (e) {} }
function freeGB(d) {
  try {
    const o = sh(SYS + '/fsutil.exe', ['volume', 'diskfree', d]);
    for (const l of (o.stdout || '').split('\n')) { const m = l.match(/:\s*([\d,]+)/); if (m) return (parseInt(m[1].replace(/,/g, ''), 10) / 1073741824).toFixed(1); }
  } catch (e) {}
  return '?';
}
function dbHead(p) { try { const b = Buffer.alloc(16); const fd = fs.openSync(p, 'r'); fs.readSync(fd, b, 0, 16, 0); fs.closeSync(fd); return b.toString('latin1').startsWith('SQLite format 3'); } catch (e) { return false; } }
function exists(p) { try { fs.accessSync(p); return true; } catch (e) { return false; } }

log('============================================');
log('WorkBuddy Migration (universal, node-native copy + junction)');
log('SRC = ' + SRC);
log('DST = ' + DST);
log('C: free BEFORE = ' + freeGB('C:') + ' GB');

// [guard] close WorkBuddy
log('[guard] checking WorkBuddy process');
for (let i = 0; i < 4; i++) {
  const p = sh(SYS + '/tasklist.exe', ['/fi', 'IMAGENAME eq WorkBuddy.exe', '/fo', 'CSV', '/nh']).stdout || '';
  if (!/WorkBuddy\.exe/i.test(p)) { log('[guard] WorkBuddy not running'); break; }
  log('[guard] WorkBuddy running -> taskkill');
  sh(SYS + '/taskkill.exe', ['/f', '/im', 'WorkBuddy.exe']);
  sleep(2000);
  if (i === 3) { log('ERROR: cannot close WorkBuddy. Close it manually and re-run.'); process.exit(1); }
}

// [0] DB safety: never let an empty/broken C db overwrite the good DST db
log('[0] database safety check');
const cDb = dbHead(SRC + '/workbuddy.db');
const eDb = dbHead(DST + '/workbuddy.db');
log('  C db valid=' + cDb + '  DST db valid=' + eDb);
if (!cDb && eDb) {
  log('  RESTORE: C db broken but DST db valid -> copy DST db to C first');
  for (const f of ['workbuddy.db', 'workbuddy.db-wal', 'workbuddy.db-shm']) {
    const sp = DST + '/' + f;
    if (exists(sp)) { try { fs.copyFileSync(sp, SRC + '/' + f); log('    restored ' + f); } catch (e) { log('    restore warn ' + f + ': ' + e.code); } }
  }
} else if (!cDb && !eDb) {
  log('  FATAL: both dbs broken. Aborting to avoid data loss.');
  process.exit(1);
} else {
  log('  C db is the source of truth -> proceed');
}

// [1/4] cleanup caches (best-effort, non-fatal)
log('[1/4] cleanup leftover caches');
for (const d of [SRC + '/logs/mcp-runtime', SRC + '/app/session/Cache', SRC + '/app/session/Code Cache', SRC + '/app/session/GPUCache']) {
  try { fs.rmSync(d, { recursive: true, force: true }); } catch (e) { log('  warn rm ' + d + ': ' + e.code); }
}
log('[1/4] cleanup done');

// [1.5] ensure DST drive has space
try {
  const st = fs.statfsSync(DST_DRIVE + ':');
  const free = st.bavail * st.bsize;
  log('  ' + DST_DRIVE + ': free = ' + (free / 1073741824).toFixed(1) + ' GB');
  if (free < 9 * 1073741824) { log('  FATAL: target drive has < 9 GB free, cannot host the data. Aborting.'); process.exit(1); }
} catch (e) { log('  warn target drive space check failed: ' + e.code); }

// [2/4] copy SRC -> DST with node-native fs.cpSync (reliable, no ACL issues)
log('[2/4] copying SRC -> DST (node fs.cpSync; 2-5 min; window may look frozen - do NOT close)');
try {
  if (exists(DST)) { fs.rmSync(DST, { recursive: true, force: true }); log('  removed stale DST'); }
  fs.cpSync(SRC, DST, { recursive: true, force: true, verbatimSymlinks: true });
  log('[2/4] copy done');
} catch (e) {
  log('  COPY ERROR: ' + e.message);
  log('  FATAL: copy failed. Source left intact. Re-run after reboot.');
  process.exit(1);
}

// [2.5] VERIFY copy before touching source
log('[2.5] verifying copy completeness');
const checks = {
  'node.exe': DST + '/binaries/node/versions/22.22.2/node.exe',
  'workbuddy.db': DST + '/workbuddy.db',
  'projects': DST + '/projects',
  'sessions': DST + '/sessions',
  'skills': DST + '/skills',
  'memory': DST + '/memory',
  'SOUL.md': DST + '/SOUL.md',
};
let allOk = true;
for (const k in checks) {
  const ok = exists(checks[k]);
  if (!ok) allOk = false;
  log('  ' + (ok ? 'OK  ' : 'MISS') + ' ' + k);
}
if (!dbHead(DST + '/workbuddy.db')) { allOk = false; log('  MISS workbuddy.db not a valid sqlite'); }
if (!allOk) { log('  FATAL: copy incomplete. Source left intact. Re-run after reboot.'); process.exit(1); }
log('[2.5] copy verified complete');

// [3/4] rename source -> _old (frees the C: name so we can create the junction)
log('[3/4] rename SRC -> SRC_old');
let renamed = false;
for (let i = 0; i < 6 && !renamed; i++) {
  try {
    if (exists(SRC_OLD)) { try { fs.rmSync(SRC_OLD, { recursive: true, force: true }); } catch (e) {} }
    fs.renameSync(SRC, SRC_OLD);
    renamed = true;
  } catch (e) {
    log('  rename attempt ' + (i + 1) + ' failed: ' + e.code + ' - retry');
    sh(SYS + '/taskkill.exe', ['/f', '/im', 'WorkBuddy.exe']);
    sleep(1500);
  }
}
if (!renamed) { log('ERROR: cannot rename source. Source left intact at ' + SRC + '.'); process.exit(1); }
log('[3/4] renamed OK');

// [4/4] create junction via node-native symlink (type junction, no admin needed)
log('[4/4] creating junction ' + SRC + ' -> ' + DST + ' (node fs.symlinkSync)');
let jok = false;
try {
  fs.symlinkSync(DST, SRC, 'junction');
  jok = fs.lstatSync(SRC).isSymbolicLink();
} catch (e) {
  log('  symlink failed: ' + e.code + ' ' + e.message);
  log('  Fallback: restore SRC from _old');
  try { fs.renameSync(SRC_OLD, SRC); } catch (e2) { log('  restore failed: ' + e2.code); }
  process.exit(1);
}
if (!jok) {
  log('  junction not detected -> fallback');
  try { fs.rmSync(SRC, { recursive: true, force: true }); } catch (e) {}
  try { fs.renameSync(SRC_OLD, SRC); } catch (e2) {}
  process.exit(1);
}
log('[4/4] junction created');

// verify
const nodeOk = exists(SRC + '/binaries/node/versions/22.22.2/node.exe');
const dbOk = dbHead(DST + '/workbuddy.db');
log('SELF-CHECK: junction OK = ' + jok);
log('SELF-CHECK: node reachable via C: = ' + nodeOk);
log('SELF-CHECK: DST db intact = ' + dbOk);
log('C: free AFTER = ' + freeGB('C:') + ' GB');

// reclaim C: space (non-fatal; some files may be locked until reboot)
log('reclaiming C: space: removing .workbuddy_old');
try { fs.rmSync(SRC_OLD, { recursive: true, force: true }); log('  .workbuddy_old removed'); }
catch (e) { log('  note: .workbuddy_old partially locked (' + e.code + '). Delete manually after reboot. It is NOT used by WorkBuddy.'); }

log('DONE. Migration succeeded. Reopen WorkBuddy - your history should be visible.');
process.exit(0);
