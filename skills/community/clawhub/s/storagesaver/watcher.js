#!/usr/bin/env node
/**
 * watcher.js — StorageSaver's scheduled storage watcher.
 *
 * Inspects the Mac's storage, classifies findings into categories, and
 * emits a prioritized recommendation message when usage is high enough to
 * bother with. Designed to run weekly via cron / launchd / an agent
 * scheduler (see SKILL.md).
 *
 * Categories:
 *   🧹 Easy wins   — Trash, caches, build cruft (low-risk reclaim)
 *   📱 Stale apps  — Apps not opened in >1 year, sized >=500 MB
 *   📦 Dev cruft   — node_modules, Xcode artifacts, Docker, iOS backups
 *   🎬 Big media   — Large video files worth moving to external/NAS storage
 *   🗂️ Big files   — Anything else >500 MB worth surfacing
 *
 * Thresholds (% used on the data volume):
 *   <70%       → silent (no alert)
 *   70–84%     → "heads up" tone
 *   85–94%     → "getting tight" tone
 *   >=95%      → "urgent" tone
 *
 * Notifications: set NOTIFY_CMD to any shell command; the message is piped
 * to its stdin and the generated report HTML path (if any) is passed as $1.
 * Without NOTIFY_CMD the message prints to stdout.
 *
 * State/logs/reports live under ~/.config/storagesaver/.
 *
 * Safety: pure observation. Never deletes or moves anything.
 *
 * Usage:
 *   node watcher.js              normal weekly run, notifies if warranted
 *   node watcher.js --quick      skips slow scans (no full-home traversal)
 *   node watcher.js --force      always notify (ignore <70% silent rule)
 *   node watcher.js --dry-run    gather + log + format, but do NOT notify
 *   node watcher.js --stdout     print the full breakdown to stdout
 */

'use strict';

const { spawnSync } = require('child_process');
const fs   = require('fs');
const path = require('path');
const os   = require('os');

// ── Config ────────────────────────────────────────────────────────────────────

const HOME = os.homedir();
const CONFIG_DIR = process.env.STORAGESAVER_CONFIG_DIR ||
  path.join(process.env.XDG_CONFIG_HOME || path.join(HOME, '.config'), 'storagesaver');
const STATE_FILE = path.join(CONFIG_DIR, 'watcher-state.json');
const LOG_FILE   = path.join(CONFIG_DIR, 'watcher.log');
const OUTPUT_DIR = path.join(CONFIG_DIR, 'reports');

const DATA_VOLUME = process.platform === 'darwin' ? '/System/Volumes/Data' : '/';

const CODE_ROOTS = [
  path.join(HOME, 'Code'),
  path.join(HOME, 'Projects'),
  path.join(HOME, 'projects'),
  path.join(HOME, 'Developer'),
  path.join(HOME, 'Sites'),
  path.join(HOME, 'git'),
  path.join(HOME, 'repos'),
];

const MIN_MEDIA_FILE_BYTES = 200 * 1024 * 1024;     // 200 MB
const MIN_STALE_APP_BYTES  = 500 * 1024 * 1024;     // 500 MB
const STALE_APP_DAYS       = 365;
const OLD_DOWNLOAD_DAYS    = 90;
const OLD_DOWNLOAD_MIN_MB  = 50;
const MAX_REPORT_FILES     = 20;

// Alert debounce: if usage is in the same bucket and we alerted recently,
// stay silent — a weekly watcher shouldn't nag daily about the same state.
const ALERT_QUIET_MS = 6 * 24 * 3600 * 1000;  // 6 days

// Flags
const QUICK   = process.argv.includes('--quick');
const FORCE   = process.argv.includes('--force');
const DRY_RUN = process.argv.includes('--dry-run');
const STDOUT  = process.argv.includes('--stdout');

// ── Utilities ─────────────────────────────────────────────────────────────────

function log(line) {
  const stamp = new Date().toISOString();
  const msg = `[${stamp}] ${line}\n`;
  try { fs.appendFileSync(LOG_FILE, msg); } catch (_) {}
  process.stderr.write(msg);
}

function loadState() {
  try { return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8')); }
  catch (_) { return {}; }
}

function saveState(state) {
  try { fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2)); }
  catch (e) { log(`state save error: ${e.message}`); }
}

function bytesHuman(bytes) {
  if (!Number.isFinite(bytes) || bytes <= 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  let v = bytes;
  while (v >= 1024 && i < units.length - 1) { v /= 1024; i++; }
  return `${v.toFixed(v >= 10 || i === 0 ? 0 : 1)} ${units[i]}`;
}

// Run `du -sk` and return bytes (or null on error / nonexistent).
// Bounded to 20s per path so a single huge tree can't blow up total runtime.
function duBytes(p) {
  if (!p || !fs.existsSync(p)) return null;
  try {
    const r = spawnSync('du', ['-skx', p], { encoding: 'utf8', timeout: 20_000 });
    if (r.status !== 0) return null;
    const kb = parseInt(r.stdout.trim().split(/\s+/)[0], 10);
    return Number.isFinite(kb) ? kb * 1024 : null;
  } catch (_) { return null; }
}

function safeExec(cmd, args, opts = {}) {
  try {
    const r = spawnSync(cmd, args, { encoding: 'utf8', timeout: 60_000, ...opts });
    return { ok: r.status === 0, stdout: r.stdout || '', stderr: r.stderr || '' };
  } catch (e) {
    return { ok: false, stdout: '', stderr: e.message };
  }
}

function ensureDir(p) {
  try { fs.mkdirSync(p, { recursive: true }); } catch (_) {}
}

// Shell-quote a single argument for safe inclusion in copy/paste commands.
function shq(s) {
  if (s === null || s === undefined) return "''";
  return "'" + String(s).replace(/'/g, "'\\''") + "'";
}

// ── Data gathering ────────────────────────────────────────────────────────────

function gatherDisk() {
  const r = safeExec('df', ['-k', DATA_VOLUME]);
  const last = r.stdout.trim().split('\n').pop() || '';
  const cols = last.split(/\s+/);
  // df -k cols: Filesystem 1024-blocks Used Available Capacity ...
  const totalKb = parseInt(cols[1], 10);
  const usedKb  = parseInt(cols[2], 10);
  const availKb = parseInt(cols[3], 10);
  const pct     = parseInt((cols[4] || '').replace('%', ''), 10);
  return {
    totalBytes:  totalKb * 1024,
    usedBytes:   usedKb  * 1024,
    availBytes:  availKb * 1024,
    percentUsed: pct,
  };
}

function gatherUserDirs() {
  const entries = {
    Downloads:  path.join(HOME, 'Downloads'),
    Desktop:    path.join(HOME, 'Desktop'),
    Documents:  path.join(HOME, 'Documents'),
    Movies:     path.join(HOME, 'Movies'),
    Videos:     path.join(HOME, 'Videos'),
    Pictures:   path.join(HOME, 'Pictures'),
    Music:      path.join(HOME, 'Music'),
    Trash:      path.join(HOME, '.Trash'),
  };
  const out = {};
  for (const [name, p] of Object.entries(entries)) out[name] = duBytes(p);
  return out;
}

function gatherDevCruft() {
  const targets = {
    'Xcode DerivedData':      path.join(HOME, 'Library/Developer/Xcode/DerivedData'),
    'Xcode Archives':         path.join(HOME, 'Library/Developer/Xcode/Archives'),
    'Xcode iOS DeviceSupport':path.join(HOME, 'Library/Developer/Xcode/iOS DeviceSupport'),
    'Docker VM disk store':   path.join(HOME, 'Library/Containers/com.docker.docker'), // holds Docker.raw (sparse, grow-only VM disk image)
    'Docker Scout cache':     path.join(HOME, '.docker/scout'),                         // vuln-scan SBOM cache — NOT the VM disk; `docker scout cache prune` does NOT clear it
    'Docker Group Containers':path.join(HOME, 'Library/Group Containers/group.com.docker'),
    'iOS device backups':     path.join(HOME, 'Library/Application Support/MobileSync/Backup'),
    'npm cache':              path.join(HOME, '.npm'),
    'yarn cache':             path.join(HOME, 'Library/Caches/Yarn'),
    'pnpm store':             path.join(HOME, 'Library/pnpm'),
    'go build cache':         path.join(HOME, 'Library/Caches/go-build'),
    'pip cache':              path.join(HOME, 'Library/Caches/pip'),
    'gradle cache':           path.join(HOME, '.gradle'),
    'HuggingFace model cache':path.join(HOME, '.cache/huggingface'),                     // ML models, re-downloadable
    'PyTorch cache':          path.join(HOME, '.cache/torch'),
    'Unity cache':            path.join(HOME, 'Library/Unity/cache'),
    'core dumps':             '/cores',
  };
  const out = {};
  for (const [name, p] of Object.entries(targets)) out[name] = duBytes(p);

  // Homebrew cache — needs `brew --cache`
  try {
    const r = safeExec('brew', ['--cache']);
    if (r.ok) {
      const brewPath = r.stdout.trim();
      out['homebrew cache'] = duBytes(brewPath);
    }
  } catch (_) {}

  return out;
}

function gatherOldDownloads() {
  const dir = path.join(HOME, 'Downloads');
  if (!fs.existsSync(dir)) return [];
  // find files older than 90 days, larger than 50 MB
  const r = safeExec('find', [
    dir, '-maxdepth', '2', '-type', 'f',
    '-mtime', `+${OLD_DOWNLOAD_DAYS}`,
    '-size', `+${OLD_DOWNLOAD_MIN_MB}M`,
  ]);
  if (!r.ok) return [];
  const items = [];
  for (const f of r.stdout.split('\n').filter(Boolean)) {
    try {
      const st = fs.statSync(f);
      items.push({ path: f, bytes: st.size, mtime: st.mtimeMs });
    } catch (_) {}
  }
  items.sort((a, b) => b.bytes - a.bytes);
  return items.slice(0, 15);
}

// Read CFBundleIdentifier from an .app's Info.plist (or return null).
function readBundleId(appPath) {
  const plist = path.join(appPath, 'Contents', 'Info.plist');
  if (!fs.existsSync(plist)) return null;
  const r = safeExec('defaults', ['read', plist, 'CFBundleIdentifier']);
  if (!r.ok) return null;
  const id = (r.stdout || '').trim();
  return id || null;
}

// Best-effort "when did this app last actually run?" detection.
// Combines multiple signals; prefs plist mtime is the most reliable on modern macOS.
// Returns { ms: <epochMs>|null, source: <string> }.
function detectAppLastUsed(appPath, bundleId) {
  const candidates = [];

  // Signal 1: Spotlight kMDItemLastUsedDate (often null on modern macOS, but use if present).
  const r = safeExec('mdls', ['-name', 'kMDItemLastUsedDate', '-raw', appPath]);
  if (r.ok) {
    const raw = (r.stdout || '').trim();
    if (raw && raw !== '(null)') {
      const t = Date.parse(raw);
      if (Number.isFinite(t)) candidates.push({ ms: t, source: 'spotlight' });
    }
  }

  // Signal 2: ~/Library/Preferences/<bundleId>.plist mtime (apps write prefs when used).
  if (bundleId) {
    const prefsPaths = [
      path.join(HOME, 'Library/Preferences', `${bundleId}.plist`),
      path.join(HOME, 'Library/Preferences/ByHost', `${bundleId}.plist`),
    ];
    for (const pp of prefsPaths) {
      try {
        const st = fs.statSync(pp);
        candidates.push({ ms: st.mtimeMs, source: 'prefs' });
      } catch (_) {}
    }
  }

  // Signal 3: ~/Library/Containers/<bundleId> mtime (sandboxed apps).
  if (bundleId) {
    const container = path.join(HOME, 'Library/Containers', bundleId);
    try {
      const st = fs.statSync(container);
      candidates.push({ ms: st.mtimeMs, source: 'container' });
    } catch (_) {}
  }

  // Signal 4: Saved Application State (apps with persistent windows write here).
  if (bundleId) {
    const sas = path.join(HOME, 'Library/Saved Application State', `${bundleId}.savedState`);
    try {
      const st = fs.statSync(sas);
      candidates.push({ ms: st.mtimeMs, source: 'saved-state' });
    } catch (_) {}
  }

  if (!candidates.length) return { ms: null, source: null };
  // Take the MOST RECENT signal (= most generous estimate of "last used").
  candidates.sort((a, b) => b.ms - a.ms);
  return candidates[0];
}

// Is the app running RIGHT NOW? Background utilities (window managers,
// launchers, clipboard managers) can look ancient by file signals — they
// rarely rewrite prefs — while running 24/7. Lesson (2026-07): file-signal-only
// detection nearly flagged live apps.
function isAppRunning(appPath) {
  // Match by executable path, not name — avoids false hits on grep/sed etc.
  const r = safeExec('pgrep', ['-f', path.join(appPath, 'Contents/MacOS')]);
  return r.ok && r.stdout.trim().length > 0;
}

// Login items = user explicitly wants these auto-started; never call them stale.
let _loginItems = null;
function loginItems() {
  if (_loginItems) return _loginItems;
  const r = safeExec('osascript', ['-e',
    'tell application "System Events" to get the name of every login item']);
  _loginItems = new Set(
    r.ok ? r.stdout.trim().split(',').map(s => s.trim().toLowerCase()).filter(Boolean) : []
  );
  return _loginItems;
}

function gatherStaleApps() {
  if (QUICK) return [];
  const apps = [];
  let dirents;
  try { dirents = fs.readdirSync('/Applications'); }
  catch (_) { return []; }

  const nowMs = Date.now();
  for (const name of dirents) {
    if (!name.endsWith('.app')) continue;
    const p = path.join('/Applications', name);
    const bytes = duBytes(p);
    if (!bytes || bytes < MIN_STALE_APP_BYTES) continue;

    // In-use protections: currently running, or a login item → not stale,
    // regardless of how old the file signals look.
    if (isAppRunning(p)) continue;
    if (loginItems().has(name.replace(/\.app$/, '').toLowerCase())) continue;

    const bundleId = readBundleId(p);
    const { ms: lastUsedMs, source } = detectAppLastUsed(p, bundleId);
    const ageDays = lastUsedMs ? (nowMs - lastUsedMs) / 86_400_000 : null;

    // Stale = no signal at all, or most-recent signal >365 days old.
    // NOTE: helper-style apps invoked by other tools (e.g. a diff viewer
    // launched via git difftool) leave few signals — the message should
    // always say "confirm before deleting", never present these as certain.
    if (lastUsedMs === null || ageDays >= STALE_APP_DAYS) {
      apps.push({ path: p, name, bytes, lastUsedMs, ageDays, source, bundleId });
    }
  }
  apps.sort((a, b) => b.bytes - a.bytes);
  return apps.slice(0, 15);
}

function gatherNodeModules() {
  if (QUICK) return [];
  const roots = CODE_ROOTS.filter(d => fs.existsSync(d));
  if (!roots.length) return [];
  const r = safeExec('find', [
    ...roots, '-maxdepth', '6', '-name', 'node_modules', '-type', 'd', '-prune',
  ], { timeout: 60_000 });
  if (!r.ok) return [];
  const items = [];
  for (const dir of r.stdout.split('\n').filter(Boolean)) {
    const bytes = duBytes(dir);
    if (bytes) items.push({ path: dir, bytes });
  }
  items.sort((a, b) => b.bytes - a.bytes);
  return items.slice(0, 10);
}

function gatherLargeFiles() {
  if (QUICK) return [];
  // Top 20 files >500 MB in home. Prune heavy dirs (caches, container bundles,
  // group containers, the Photos library, node_modules, Trash) so find never
  // descends into them, and cap depth so the traversal stays bounded. The big
  // app-managed trees are surfaced separately via gatherBigAppData()/du.
  const r = safeExec('find', [
    HOME,
    '-maxdepth', '3',
    '(',
      '-path', path.join(HOME, 'Library/Caches'), '-o',
      '-path', path.join(HOME, 'Library/Containers'), '-o',
      '-path', path.join(HOME, 'Library/Group Containers'), '-o',
      '-path', path.join(HOME, 'Pictures/Photos Library.photoslibrary'), '-o',
      '-name', 'node_modules', '-o',
      '-path', path.join(HOME, '.Trash'),
    ')', '-prune', '-o',
    '(', '-type', 'f', '-size', '+500M', '-print', ')',
  ], { timeout: 60_000 });
  if (!r.ok) return [];
  const items = [];
  for (const f of r.stdout.split('\n').filter(Boolean)) {
    try {
      const st = fs.statSync(f);
      items.push({ path: f, bytes: st.size });
    } catch (_) {}
  }
  items.sort((a, b) => b.bytes - a.bytes);
  return items.slice(0, 20);
}

function gatherMediaFiles() {
  if (QUICK) return [];
  const exts = ['mp4', 'mkv', 'mov', 'avi', 'm4v', 'wmv', 'flv', 'iso'];
  const dirs = [
    path.join(HOME, 'Movies'),
    path.join(HOME, 'Videos'),
    path.join(HOME, 'Downloads'),
    path.join(HOME, 'Desktop'),
    path.join(HOME, 'Documents'),
  ].filter(d => fs.existsSync(d));
  if (!dirs.length) return [];

  // Depth-cap + prune node_modules so a stray project tree under Documents/etc
  // can't turn this into a full recursive crawl.
  const args = [...dirs, '-maxdepth', '2',
    '(', '-name', 'node_modules', ')', '-prune', '-o',
    '-type', 'f', '('];
  exts.forEach((ext, i) => {
    if (i) args.push('-o');
    args.push('-iname', `*.${ext}`);
  });
  args.push(')', '-size', `+${Math.round(MIN_MEDIA_FILE_BYTES / 1024 / 1024)}M`, '-print');

  const r = safeExec('find', args, { timeout: 60_000 });
  if (!r.ok) return [];
  const items = [];
  for (const f of r.stdout.split('\n').filter(Boolean)) {
    try {
      const st = fs.statSync(f);
      items.push({ path: f, bytes: st.size });
    } catch (_) {}
  }
  items.sort((a, b) => b.bytes - a.bytes);
  return items.slice(0, 20);
}

// Known app/system caches proven safe to reclaim by hand (once found ~15 GB
// of these sitting on a 99%-full disk). All regenerate on demand.
function gatherAppCaches() {
  const targets = {
    'Chrome disk cache':       path.join(HOME, 'Library/Caches/Google/Chrome'),                                // per-profile Cache dirs; Chrome rebuilds them
    'GoogleUpdater crx_cache': path.join(HOME, 'Library/Application Support/Google/GoogleUpdater/crx_cache'),  // update payloads, re-download
    'Claude Desktop VM image': path.join(HOME, 'Library/Application Support/Claude/vm_bundles'),               // local sandbox VM, re-downloads on next use
    'Docker installer cache':  path.join(HOME, 'Library/Application Support/com.docker.install'),              // installer payloads — safe even if you keep Docker
    'Messages render cache':   path.join(HOME, 'Library/Messages/Caches'),                                     // preview/render cache — NOT the messages themselves
    'Spotify cache':           path.join(HOME, 'Library/Caches/com.spotify.client'),
  };
  const out = {};
  for (const [name, p] of Object.entries(targets)) out[name] = duBytes(p);

  // Chrome update clones (one machine had 14 GB of these!). The updater leaves
  // a full ~1.4 GB clone of Chrome.app under the user temp container on EVERY
  // update and never cleans them. Recurs forever — find it dynamically.
  try {
    const r = safeExec('find', ['/private/var/folders', '-maxdepth', '4',
      '-name', 'com.google.Chrome.code_sign_clone'], { timeout: 15_000 });
    const dir = r.stdout.split('\n').filter(Boolean)[0];
    if (dir) { out['Chrome update clones'] = duBytes(dir); out._chromeClonesPath = dir; }
  } catch (_) {}
  return out;
}

// Generic sweep of ~/Library/Caches: any folder >=1 GB (trivy, ms-playwright, …).
// Caches are regenerable by definition; the guidance is always "quit the app, rm".
// Skips com.apple.* (riskier, system-managed) and folders covered elsewhere.
function gatherLibraryCaches() {
  if (QUICK) return [];
  const dir = path.join(HOME, 'Library/Caches');
  const SKIP = new Set(['Google', 'com.spotify.client', 'pip', 'Yarn', 'go-build', 'Homebrew']);
  const out = [];
  let names = [];
  try { names = fs.readdirSync(dir); } catch (_) { return out; }
  for (const name of names) {
    if (name.startsWith('.') || name.startsWith('com.apple.') || SKIP.has(name)) continue;
    const bytes = duBytes(path.join(dir, name));
    if (bytes && bytes >= 1024 ** 3) out.push({ path: path.join(dir, name), bytes });
  }
  out.sort((a, b) => b.bytes - a.bytes);
  return out.slice(0, 8);
}

// Does a matching app still exist in /Applications? Real-world lesson: found
// 1.2 GB of Application Support data for an app uninstalled long ago.
// Normalized substring match both ways so 'Code' matches 'Visual Studio
// Code.app'. Fails open (returns true) so we never wrongly call live data
// orphaned.
function appExistsFor(name) {
  const norm = s => s.toLowerCase().replace(/\.app$/, '').replace(/[^a-z0-9]/g, '');
  const target = norm(name);
  if (target.length < 4) return true; // too short to match reliably — fail open
  for (const appDir of ['/Applications', path.join(HOME, 'Applications')]) {
    let apps = [];
    try { apps = fs.readdirSync(appDir).filter(a => a.endsWith('.app')); } catch (_) { continue; }
    for (const a of apps) {
      const an = norm(a);
      if (an.includes(target) || target.includes(an)) return true;
    }
  }
  return false;
}

// Big app-data folders + cloud caches the targeted scans miss (e.g. a local
// sandbox VM bundle, Steam, Google Drive's local cache, Messages attachments).
// These are app-managed — surface them for review with safe guidance, never a
// blind rm.
function gatherBigAppData() {
  if (QUICK) return [];
  const out = [];
  const THRESH = 2 * 1024 * 1024 * 1024; // 2 GB
  const roots = [
    { dir: path.join(HOME, 'Library/Application Support'), kind: 'app' },
    { dir: path.join(HOME, 'Library/CloudStorage'),        kind: 'cloud' },
  ];
  for (const { dir, kind } of roots) {
    if (!fs.existsSync(dir)) continue;
    let names;
    try { names = fs.readdirSync(dir); } catch (_) { continue; }
    for (const name of names) {
      if (name.startsWith('.')) continue;
      const p = path.join(dir, name);
      const bytes = duBytes(p);
      if (bytes && bytes >= THRESH) {
        const entry = { path: p, bytes, kind };
        // Flag app-data folders whose app is gone from /Applications (orphaned data).
        if (kind === 'app') entry.orphan = !appExistsFor(name);
        out.push(entry);
      }
    }
  }
  // Messages store (iMessage history + attachments) — one big folder. Break out
  // the safe-to-clear render cache vs the never-touch attachments/chat.db.
  const msgs = duBytes(path.join(HOME, 'Library/Messages'));
  if (msgs && msgs >= THRESH) {
    out.push({
      path: path.join(HOME, 'Library/Messages'), bytes: msgs, kind: 'messages',
      cachesBytes:      duBytes(path.join(HOME, 'Library/Messages/Caches')),
      attachmentsBytes: duBytes(path.join(HOME, 'Library/Messages/Attachments')),
    });
  }
  out.sort((a, b) => b.bytes - a.bytes);
  return out.slice(0, 8);
}

// ── Message formatting ───────────────────────────────────────────────────────

function severity(pct) {
  if (pct >= 95) return 'urgent';
  if (pct >= 85) return 'tight';
  if (pct >= 70) return 'headsup';
  return 'silent';
}

function bucketEmoji(sev) {
  return { urgent: '🚨', tight: '⚠️', headsup: '👋', silent: '✅' }[sev] || '💾';
}

function vibe(sev) {
  switch (sev) {
    case 'urgent':  return "Disk is basically full — let's clear space now.";
    case 'tight':   return "Getting tight. Some easy wins below.";
    case 'headsup': return "Heads up — a few things worth pruning.";
    default:        return "All good.";
  }
}

function formatMessage(report) {
  const { disk, easyWins, bigMedia, staleApps, devCruft, bigFiles, appData = [] } = report;
  const sev = severity(disk.percentUsed);
  const emoji = bucketEmoji(sev);

  const lines = [];
  lines.push(`${emoji} Mac storage: ${disk.percentUsed}% used, ${bytesHuman(disk.availBytes)} free`);
  lines.push(vibe(sev));
  lines.push('');

  let recoveryEstimate = 0;

  if (easyWins.length) {
    lines.push('🧹 Easy wins (with commands):');
    for (const w of easyWins) {
      lines.push(`  • ${w.label} — ${bytesHuman(w.bytes)}`);
      if (w.cmd) lines.push(`      $ ${w.cmd}`);
      recoveryEstimate += w.bytes;
    }
    lines.push('');
  }

  if (bigMedia.length) {
    lines.push('🎬 Big media files (move to external/NAS storage, or delete after backing up):');
    for (const m of bigMedia) {
      lines.push(`  • ${path.basename(m.path)} — ${bytesHuman(m.bytes)}`);
      lines.push(`      $ rsync -avh --progress --remove-source-files ${shq(m.path)} /path/to/external/`);
      recoveryEstimate += m.bytes;
    }
    lines.push('');
    lines.push('  (rsync with --remove-source-files copies then deletes the source after verifying.)');
    lines.push('');
  }

  if (staleApps.length) {
    lines.push("📱 Apps you don't seem to use (CONFIRM before deleting — helper apps leave few signals):");
    for (const a of staleApps) {
      let when;
      if (a.lastUsedMs) {
        const d = new Date(a.lastUsedMs).toISOString().slice(0, 10);
        const days = Math.round(a.ageDays);
        when = `last touched ${d} (~${days}d ago, via ${a.source})`;
      } else {
        when = 'no usage signal found';
      }
      lines.push(`  • ${a.name.replace(/\.app$/, '')} — ${bytesHuman(a.bytes)} (${when})`);
      lines.push(`      $ trash ${shq(a.path)}    # or: rm -rf ${shq(a.path)}`);
      recoveryEstimate += a.bytes;
    }
    lines.push('');
  }

  if (devCruft.length) {
    lines.push('📦 Dev cruft (with commands):');
    for (const c of devCruft) {
      lines.push(`  • ${c.label} — ${bytesHuman(c.bytes)}`);
      if (c.cmd) lines.push(`      $ ${c.cmd}`);
      recoveryEstimate += c.bytes;
    }
    lines.push('');
  }

  if (appData.length) {
    lines.push('🧰 Big app data & cloud caches (review — app-managed, not blind-delete):');
    for (const a of appData) {
      lines.push(`  • ${a.label} — ${bytesHuman(a.bytes)}`);
      if (a.cmd) lines.push(`      ${a.cmd}`);
    }
    lines.push('');
  }

  if (bigFiles.length) {
    lines.push('🗂️  Other big files (review manually):');
    for (const f of bigFiles) {
      lines.push(`  • ${f.path.replace(HOME, '~')} — ${bytesHuman(f.bytes)}`);
    }
    lines.push('');
  }

  if (recoveryEstimate > 0) {
    lines.push(`💡 Potential recovery: ~${bytesHuman(recoveryEstimate)}`);
  }

  return lines.join('\n').trim();
}

// ── Decision logic: pick items per category ──────────────────────────────────

function decide(raw) {
  const easyWins = [];
  const bigMedia = [];
  const staleApps = [];
  const devCruft = [];
  const bigFiles = [];

  // Easy wins: Trash, caches, build artifacts >1 GB — each with a copy/paste command.
  const easyCandidates = [
    { label: 'Empty Trash',          bytes: raw.userDirs.Trash,                         cmd: "rm -rf ~/.Trash/*  # or use Finder: right-click Trash → Empty Trash" },
    { label: 'Xcode DerivedData',    bytes: raw.devCruft['Xcode DerivedData'],          cmd: "rm -rf ~/Library/Developer/Xcode/DerivedData/*" },
    { label: 'Xcode Archives',       bytes: raw.devCruft['Xcode Archives'],             cmd: "rm -rf ~/Library/Developer/Xcode/Archives/*  # only if you don't need old app archives" },
    { label: 'iOS DeviceSupport',    bytes: raw.devCruft['Xcode iOS DeviceSupport'],    cmd: "rm -rf ~/Library/Developer/Xcode/iOS\\ DeviceSupport/*" },
    { label: 'npm cache',            bytes: raw.devCruft['npm cache'],                  cmd: "npm cache clean --force" },
    { label: 'yarn cache',           bytes: raw.devCruft['yarn cache'],                 cmd: "yarn cache clean" },
    { label: 'pnpm store',           bytes: raw.devCruft['pnpm store'],                 cmd: "pnpm store prune" },
    { label: 'go build cache',       bytes: raw.devCruft['go build cache'],             cmd: "go clean -cache" },
    { label: 'pip cache',            bytes: raw.devCruft['pip cache'],                  cmd: "pip cache purge" },
    { label: 'gradle cache',         bytes: raw.devCruft['gradle cache'],               cmd: "rm -rf ~/.gradle/caches" },
    { label: 'Docker Scout cache',   bytes: raw.devCruft['Docker Scout cache'],         cmd: "rm -rf ~/.docker/scout  # vuln-scan SBOM cache; Docker rebuilds it. NOTE: `docker scout cache prune` does NOT clear it" },
    { label: 'HuggingFace models',   bytes: raw.devCruft['HuggingFace model cache'],    cmd: "rm -rf ~/.cache/huggingface  # ML models re-download on next use" },
    { label: 'PyTorch cache',        bytes: raw.devCruft['PyTorch cache'],              cmd: "rm -rf ~/.cache/torch" },
    { label: 'Unity cache',          bytes: raw.devCruft['Unity cache'],                cmd: "rm -rf ~/Library/Unity/cache  # only if not actively using Unity" },
    { label: 'homebrew cache',       bytes: raw.devCruft['homebrew cache'],             cmd: "brew cleanup -s && rm -rf $(brew --cache)" },
    { label: 'core dumps (/cores)',  bytes: raw.devCruft['core dumps'],                 cmd: "sudo rm -rf /cores/*" },
    // App/system caches proven safe by hand. Lower per-item minimums — several
    // of these were 700–900 MB and still worth taking on a full disk.
    { label: 'Chrome disk cache',    bytes: (raw.appCaches || {})['Chrome disk cache'],       min: 512 * 1024 * 1024, cmd: "rm -rf ~/Library/Caches/Google/Chrome/*  # rebuilds; ideally quit Chrome first (or reload any weird tab)" },
    { label: 'GoogleUpdater crx_cache', bytes: (raw.appCaches || {})['GoogleUpdater crx_cache'], min: 512 * 1024 * 1024, cmd: "rm -rf ~/Library/Application\\ Support/Google/GoogleUpdater/crx_cache  # update payloads, re-download" },
    { label: 'Claude Desktop VM image (vm_bundles)', bytes: (raw.appCaches || {})['Claude Desktop VM image'], cmd: "osascript -e 'quit app \"Claude\"'; rm -rf ~/Library/Application\\ Support/Claude/vm_bundles  # local sandbox VM — re-downloads on next use" },
    { label: 'Docker installer cache', bytes: (raw.appCaches || {})['Docker installer cache'], min: 512 * 1024 * 1024, cmd: "rm -rf ~/Library/Application\\ Support/com.docker.install  # installer payloads — safe even if you keep using Docker" },
    { label: 'Messages render cache', bytes: (raw.appCaches || {})['Messages render cache'], min: 512 * 1024 * 1024, cmd: "osascript -e 'quit app \"Messages\"'; rm -rf ~/Library/Messages/Caches  # regenerates; history/search/attachments untouched" },
    { label: 'Spotify cache',        bytes: (raw.appCaches || {})['Spotify cache'],           min: 512 * 1024 * 1024, cmd: "rm -rf ~/Library/Caches/com.spotify.client  # re-caches streams" },
    { label: 'Chrome update clones (code_sign_clone)', bytes: (raw.appCaches || {})['Chrome update clones'], min: 512 * 1024 * 1024,
      cmd: `find ${shq((raw.appCaches || {})._chromeClonesPath || '')} -mindepth 1 -maxdepth 1 -type d -mtime +1 -exec rm -rf {} +  # stale updater leftovers, one per Chrome update (found 14 GB of these once)` },
  ];
  // Generic ~/Library/Caches sweep (trivy, ms-playwright, …) — all regenerable.
  for (const c of (raw.libraryCaches || [])) {
    easyCandidates.push({
      label: `${path.basename(c.path)} cache`,
      bytes: c.bytes,
      cmd: `rm -rf ${shq(c.path)}  # app cache — regenerates; quit the app first`,
    });
  }
  for (const c of easyCandidates) {
    const min = c.min || 1 * 1024 * 1024 * 1024;
    if (c.bytes && c.bytes >= min) easyWins.push(c);
  }
  // Old downloads (combined)
  const oldDownloadsTotal = raw.oldDownloads.reduce((s, f) => s + f.bytes, 0);
  if (oldDownloadsTotal >= 1 * 1024 * 1024 * 1024) {
    easyWins.push({
      label: `Old Downloads (${raw.oldDownloads.length} files >90 days old)`,
      bytes: oldDownloadsTotal,
      cmd: `find ~/Downloads -maxdepth 2 -type f -mtime +90 -size +50M -print -exec trash {} \\;  # review first, then run`,
    });
  }
  easyWins.sort((a, b) => b.bytes - a.bytes);

  // Big media: large video files (show up to 12 to cover full seasons)
  if (raw.mediaFiles.length) {
    bigMedia.push(...raw.mediaFiles.slice(0, 12));
  }

  // Stale apps
  if (raw.staleApps.length) {
    staleApps.push(...raw.staleApps.slice(0, 6));
  }

  // Dev cruft NOT already in easy wins (Docker VM disk, iOS backups, node_modules).
  // IMPORTANT lesson: the big Docker space is the VM disk image (Docker.raw)
  // under Library/Containers — a sparse, grow-only file. `docker system prune`
  // frees space INSIDE the VM but does NOT shrink that host file, so it often
  // reclaims ~0 bytes. It must be purged via Docker Desktop. (The Scout cache
  // is handled as a separate easy win.)
  const dockerVm =
    (raw.devCruft['Docker VM disk store'] || 0) +
    (raw.devCruft['Docker Group Containers'] || 0);
  if (dockerVm >= 3 * 1024 * 1024 * 1024) {
    devCruft.push({
      label: `Docker VM disk image (${bytesHuman(raw.devCruft['Docker VM disk store'] || 0)})`,
      bytes: dockerVm,
      cmd: "# `docker system prune` will NOT shrink this — it's a grow-only VM disk image (Docker.raw).\n      # Keep Docker: Docker Desktop → 🐞 Troubleshoot → 'Clean / Purge data' (or lower the disk size in Settings → Resources → disk image).\n      # Remove entirely: quit Docker, then rm -rf ~/Library/Containers/com.docker.docker ~/Library/Group\\ Containers/group.com.docker  (and trash /Applications/Docker.app)",
    });
  }
  if (raw.devCruft['iOS device backups'] && raw.devCruft['iOS device backups'] >= 5 * 1024 * 1024 * 1024) {
    devCruft.push({
      label: 'iOS device backups',
      bytes: raw.devCruft['iOS device backups'],
      cmd: "# List backups first: ls -lah ~/Library/Application\\ Support/MobileSync/Backup/\n      # Then delete the ones for devices you don't own anymore.",
    });
  }
  for (const nm of raw.nodeModules.slice(0, 3)) {
    if (nm.bytes >= 1 * 1024 * 1024 * 1024) {
      devCruft.push({
        label: `node_modules in ${nm.path.replace(HOME, '~').replace(/\/node_modules$/, '')}`,
        bytes: nm.bytes,
        cmd: `rm -rf ${shq(nm.path)}  # safe — rerun npm/yarn/pnpm install when you need the project again`,
      });
    }
  }

  // Big files not already covered
  const covered = new Set([
    ...bigMedia.map(m => m.path),
    ...raw.oldDownloads.map(f => f.path),
  ]);
  for (const f of raw.largeFiles) {
    if (covered.has(f.path)) continue;
    if (f.path.startsWith('/Applications/')) continue;
    bigFiles.push(f);
    if (bigFiles.length >= 5) break;
  }

  // Big app-data / cloud caches — review-only (app-managed), with safe guidance.
  const appData = [];
  for (const a of (raw.bigAppData || [])) {
    const base = path.basename(a.path);
    let cmd;
    if (a.kind === 'cloud') {
      cmd = "# Cloud drive cache. NOTE (Google Drive): setting folders 'Online-only' does NOT free already-downloaded files (the ☁ icon lies — they sit as real cached blocks; du sees them). It only stops FUTURE downloads + lets them evict under disk pressure. To reclaim NOW: Drive Prefs → ⚙️ → Disconnect account, then reconnect in Stream mode (cloud copies + any separate local folders are safe). NEVER rm inside ~/Library/CloudStorage — the client treats a local delete as a cloud delete.";
    } else if (a.kind === 'messages') {
      // Lesson: with Messages in iCloud ON, lowering 'Keep messages' DELETES
      // old messages from iCloud on ALL devices — never recommend it.
      // The safe reclaim is the render cache, which regenerates on demand.
      const cacheB = a.cachesBytes || 0;
      const attachB = a.attachmentsBytes || 0;
      cmd = `# ⚠️ if Messages in iCloud is ON, do NOT lower 'Keep messages' — it deletes old messages from iCloud on ALL devices.`;
      if (cacheB >= 512 * 1024 * 1024) {
        cmd += `\n      # Safe reclaim (${bytesHuman(cacheB)} render cache — regenerates; history/search/attachments untouched):\n      #   osascript -e 'quit app "Messages"'; rm -rf ~/Library/Messages/Caches\n      # Leave Attachments/ (${bytesHuman(attachB)}) and chat.db alone.`;
      } else {
        cmd += `\n      # Render cache is currently small (${bytesHuman(cacheB)}); the bulk is Attachments/ (${bytesHuman(attachB)}) + chat.db — nothing safe to bulk-delete here.`;
      }
    } else if (/com\.docker\.docker/.test(a.path)) {
      continue; // already covered under Dev cruft (Docker VM disk)
    } else if (/Claude\/vm_bundles/.test(a.path) || base === 'Claude') {
      cmd = "# Claude Desktop — the bulk is vm_bundles/ (local sandbox VM image, surfaced under Easy wins when big). Quit Claude, rm -rf ~/Library/Application\\ Support/Claude/vm_bundles; it re-downloads on next use. Sessions/config are tiny — leave the rest.";
    } else if (base === 'Google') {
      // Lesson: a "Google 6.6 GB" folder turned out to be 5.2 GB of CHROME
      // browser data, only ~270 MB of DriveFS. Drill down so the message says so.
      const chromeB  = duBytes(path.join(a.path, 'Chrome'));
      const updaterB = duBytes(path.join(a.path, 'GoogleUpdater'));
      const driveB   = duBytes(path.join(a.path, 'DriveFS'));
      cmd = `# mostly Chrome BROWSER data (${bytesHuman(chromeB || 0)}), NOT Google Drive (DriveFS is ${bytesHuman(driveB || 0)}). Chrome's disposable disk cache lives in ~/Library/Caches/Google/Chrome (see Easy wins). The App Support side is profile data (Service Workers, Extensions) — shrink it by removing unused Chrome profiles, not by rm. GoogleUpdater is ${bytesHuman(updaterB || 0)}; its crx_cache is safe to rm.`;
    } else if (base === 'Steam') {
      // List actual installed games so the recommendation is concrete.
      let games = [];
      try {
        const common = path.join(a.path, 'steamapps/common');
        games = fs.readdirSync(common)
          .filter(n => !n.startsWith('.') && n !== 'Steam Controller Configs')
          .map(n => ({ n, b: duBytes(path.join(common, n)) || 0 }))
          .sort((x, y) => y.b - x.b).slice(0, 5);
      } catch (_) {}
      cmd = games.length
        ? `# installed games: ${games.map(g => `${g.n} (${bytesHuman(g.b)})`).join(', ')}. Uninstall via Steam, or (Steam quit) rm the game folder under steamapps/common/ + its appmanifest_*.acf`
        : '# no games installed — the rest is Steam client data; uninstall Steam entirely if unused';
    } else {
      cmd = `# review before deleting — this is ${base} app data; quit the app first, and prefer the app's own cache/clear option`;
    }
    if (a.orphan) {
      cmd += `\n      # ⚠️ no matching app found in /Applications — likely orphaned data from an uninstalled app; verify, then the whole folder is safe to rm`;
    }
    appData.push({ label: a.path.replace(HOME, '~'), bytes: a.bytes, cmd });
  }

  return { easyWins, bigMedia, staleApps, devCruft, bigFiles, appData };
}

// ── Notification ──────────────────────────────────────────────────────────────
// NOTIFY_CMD contract: message on stdin, report HTML path (if generated) as $1.
// Examples:
//   NOTIFY_CMD='mail -s "Mac storage" you@example.com'
//   NOTIFY_CMD='./my-notify.sh'   (script reads stdin, attaches "$1")
// Default (no NOTIFY_CMD): print the message to stdout.

function notify(message, filePath) {
  const cmd = process.env.NOTIFY_CMD;
  if (!cmd) {
    process.stdout.write(message + '\n');
    if (filePath) process.stdout.write(`report: ${filePath}\n`);
    return;
  }
  const args = ['-c', cmd + ' "$@"', 'storagesaver-notify'];
  if (filePath) args.push(filePath);
  const r = spawnSync('/bin/sh', args, { input: message, encoding: 'utf8', timeout: 120_000 });
  if (r.status !== 0) throw new Error(`NOTIFY_CMD exited ${r.status}: ${(r.stderr || '').slice(0, 200)}`);
}

// Find the storagesaver CLI: sibling checkout first, then PATH.
function findCli() {
  const sibling = path.join(__dirname, '..', 'bin', 'storagesaver.js');
  if (fs.existsSync(sibling)) return [process.execPath, sibling];
  return ['storagesaver'];
}

// ── Main ──────────────────────────────────────────────────────────────────────

(async function main() {
  ensureDir(CONFIG_DIR);
  ensureDir(OUTPUT_DIR);

  log(`run start (quick=${QUICK}, force=${FORCE}, dry=${DRY_RUN}, stdout=${STDOUT})`);

  const disk       = gatherDisk();
  const userDirs   = gatherUserDirs();
  const devCruft   = gatherDevCruft();
  const oldDownloads = gatherOldDownloads();
  const staleApps  = gatherStaleApps();
  const nodeModules = gatherNodeModules();
  const largeFiles = gatherLargeFiles();
  const mediaFiles = gatherMediaFiles();
  const bigAppData = gatherBigAppData();
  const appCaches  = gatherAppCaches();
  const libraryCaches = gatherLibraryCaches();

  const raw = {
    disk, userDirs, devCruft, oldDownloads,
    staleApps, nodeModules, largeFiles, mediaFiles, bigAppData,
    appCaches, libraryCaches,
  };

  // Save raw report to reports/ for inspection
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const reportPath = path.join(OUTPUT_DIR, `report-${stamp}.json`);
  try {
    fs.writeFileSync(reportPath, JSON.stringify(raw, null, 2));
    // Keep last N reports
    const reports = fs.readdirSync(OUTPUT_DIR)
      .filter(f => f.startsWith('report-') && f.endsWith('.json'))
      .sort();
    while (reports.length > MAX_REPORT_FILES) {
      try { fs.unlinkSync(path.join(OUTPUT_DIR, reports.shift())); } catch (_) {}
    }
  } catch (e) { log(`report save error: ${e.message}`); }

  const decision = decide(raw);
  const sev = severity(disk.percentUsed);

  log(`disk=${disk.percentUsed}% sev=${sev} easyWins=${decision.easyWins.length} bigMedia=${decision.bigMedia.length} staleApps=${decision.staleApps.length} devCruft=${decision.devCruft.length} appData=${decision.appData.length} bigFiles=${decision.bigFiles.length}`);

  const fullBreakdown = formatMessage({ disk, ...decision });
  if (STDOUT) {
    process.stdout.write(fullBreakdown + '\n');
  }

  // Decide whether to send
  const state = loadState();
  const now = Date.now();

  if (sev === 'silent' && !FORCE) {
    log('silent (usage <70%) — no message');
    state.lastRunAtMs = now;
    state.lastPercent = disk.percentUsed;
    saveState(state);
    return;
  }

  // Debounce: same bucket + recently alerted → stay quiet unless --force
  if (!FORCE && state.lastAlertAtMs && state.lastAlertSev === sev &&
      (now - state.lastAlertAtMs) < ALERT_QUIET_MS) {
    log(`debounced (last alert ${Math.round((now - state.lastAlertAtMs) / 3600000)}h ago, same bucket ${sev})`);
    state.lastRunAtMs = now;
    state.lastPercent = disk.percentUsed;
    saveState(state);
    return;
  }

  // Short-format message: a sentence or two of "do this", with the interactive
  // StorageSaver report attached for the digging. The full breakdown still
  // lands in reports/report-*.json; --stdout prints it.
  const topWins = decision.easyWins.slice(0, 2);
  const winTxt = topWins.length
    ? `Top move${topWins.length > 1 ? 's' : ''}: ${topWins.map(w => `${w.label} (${bytesHuman(w.bytes)})`).join(', then ')} — commands are in the map (green ⧉).`
    : 'No standout easy wins — poke the map for review items.';
  const message =
    `${bucketEmoji(sev)} Mac storage: ${disk.percentUsed}% used, ${bytesHuman(disk.availBytes)} free. ${winTxt}`;

  if (DRY_RUN) {
    log('dry-run — message NOT sent, report HTML NOT generated');
    log(`message preview:\n${message}`);
    return;
  }

  // Regenerate the interactive map so the attachment matches this run
  // (~60s full walk).
  let mapPath = null;
  try {
    const cli = findCli();
    const r = spawnSync(cli[0], [...cli.slice(1), 'scan', '--no-open',
      '--out', path.join(OUTPUT_DIR, 'storagesaver.html')],
      { encoding: 'utf8', timeout: 300_000 });
    if (r.status === 0) mapPath = path.join(OUTPUT_DIR, 'storagesaver.html');
    else log(`map scan failed: ${(r.stderr || '').slice(-200)}`);
  } catch (e) { log(`map scan error: ${e.message}`); }

  try {
    notify(message, mapPath);
    log(`sent (${message.length} chars${mapPath ? ' + storagesaver.html' : ''})`);
    state.lastAlertAtMs = now;
    state.lastAlertSev = sev;
    state.lastAlertPercent = disk.percentUsed;
  } catch (e) {
    log(`notify error: ${e.message}`);
  }

  state.lastRunAtMs = now;
  state.lastPercent = disk.percentUsed;
  saveState(state);
})().catch(e => {
  log(`fatal: ${e.stack || e.message}`);
  process.exit(1);
});
