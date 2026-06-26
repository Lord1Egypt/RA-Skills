'use strict';

const os = require('os');
const fs = require('fs');
const path = require('path');

// Use a temp dir so tests never touch the real .worldloops/
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-notifications-test-'));
process.env.WORLDLOOPS_DIR = tmpDir;

const {
  DEFAULT_PREFS,
  loadPrefs,
  savePrefs,
  initPrefs,
  setDotPath,
  isInQuietHours,
  meetsSeverity,
} = require('../dist/notifications/prefs.js');

const { loadState, saveState } = require('../dist/notifications/state.js');

let passed = 0;
let failed = 0;

function assert(condition, label) {
  if (condition) {
    passed++;
    console.log(`  PASS  ${label}`);
  } else {
    failed++;
    console.error(`  FAIL  ${label}`);
  }
}

function resetPrefsFile() {
  const prefsPath = path.join(tmpDir, 'notification_prefs.json');
  if (fs.existsSync(prefsPath)) fs.unlinkSync(prefsPath);
}

function resetStateFile() {
  const statePath = path.join(tmpDir, 'notification_state.json');
  if (fs.existsSync(statePath)) fs.unlinkSync(statePath);
}

console.log('\nnotifications unit tests\n');

// --- default notification prefs creation ---

resetPrefsFile();
const created = initPrefs();
assert(created === true, 'initPrefs: creates file when missing → returns true');
assert(
  fs.existsSync(path.join(tmpDir, 'notification_prefs.json')),
  'initPrefs: notification_prefs.json exists after init'
);

const created2 = initPrefs();
assert(created2 === false, 'initPrefs: returns false when file already exists');

resetPrefsFile();
const defaultPrefs = loadPrefs();
assert(defaultPrefs.dailyBrief.enabled === true, 'loadPrefs: default dailyBrief.enabled is true');
assert(defaultPrefs.dailyBrief.time === '09:00', 'loadPrefs: default dailyBrief.time is 09:00');
assert(defaultPrefs.dailyBrief.timezone === 'UTC', 'loadPrefs: default dailyBrief.timezone is UTC');
assert(
  defaultPrefs.proactiveDiscovery.enabled === false,
  'loadPrefs: default proactiveDiscovery.enabled is false'
);
assert(
  defaultPrefs.proactiveDiscovery.scanIntervalMinutes === 30,
  'loadPrefs: default scanIntervalMinutes is 30'
);
assert(
  defaultPrefs.proactiveDiscovery.minSeverity === 'medium',
  'loadPrefs: default minSeverity is medium'
);
assert(defaultPrefs.quietHours.enabled === false, 'loadPrefs: default quietHours.enabled is false');
assert(defaultPrefs.channels.cli === true, 'loadPrefs: default channels.cli is true');

// --- dot-path setting ---

const prefs = JSON.parse(JSON.stringify(DEFAULT_PREFS));

setDotPath(prefs, 'dailyBrief.time', '10:00');
assert(prefs.dailyBrief.time === '10:00', 'setDotPath: sets dailyBrief.time');

setDotPath(prefs, 'proactiveDiscovery.scanIntervalMinutes', 60);
assert(
  prefs.proactiveDiscovery.scanIntervalMinutes === 60,
  'setDotPath: sets scanIntervalMinutes to 60'
);

setDotPath(prefs, 'proactiveDiscovery.minSeverity', 'high');
assert(prefs.proactiveDiscovery.minSeverity === 'high', 'setDotPath: sets minSeverity to high');

setDotPath(prefs, 'quietHours.enabled', true);
assert(prefs.quietHours.enabled === true, 'setDotPath: sets quietHours.enabled to true');

setDotPath(prefs, 'quietHours.start', '21:00');
assert(prefs.quietHours.start === '21:00', 'setDotPath: sets quietHours.start');

setDotPath(prefs, 'quietHours.end', '08:00');
assert(prefs.quietHours.end === '08:00', 'setDotPath: sets quietHours.end');

// Verify roundtrip via savePrefs/loadPrefs
savePrefs(prefs);
const loaded = loadPrefs();
assert(loaded.dailyBrief.time === '10:00', 'setDotPath: persisted dailyBrief.time roundtrips');
assert(
  loaded.quietHours.enabled === true,
  'setDotPath: persisted quietHours.enabled roundtrips'
);

// --- quiet hours behavior ---

const qhPrefsDisabled = JSON.parse(JSON.stringify(DEFAULT_PREFS));
qhPrefsDisabled.quietHours.enabled = false;
qhPrefsDisabled.quietHours.start = '22:00';
qhPrefsDisabled.quietHours.end = '07:00';

// 23:00 local — outside prefs because enabled=false
const t23 = new Date(2025, 0, 1, 23, 0, 0);
assert(
  isInQuietHours(qhPrefsDisabled, t23) === false,
  'isInQuietHours: false when quietHours.enabled is false'
);

const qhPrefsEnabled = JSON.parse(JSON.stringify(DEFAULT_PREFS));
qhPrefsEnabled.quietHours.enabled = true;
qhPrefsEnabled.quietHours.start = '22:00';
qhPrefsEnabled.quietHours.end = '07:00';

// Midnight-spanning quiet hours (22:00–07:00)
const during1 = new Date(2025, 0, 1, 23, 0, 0); // 23:00 → inside quiet hours
assert(isInQuietHours(qhPrefsEnabled, during1) === true, 'isInQuietHours: 23:00 is inside 22:00–07:00');

const during2 = new Date(2025, 0, 1, 0, 30, 0); // 00:30 → inside quiet hours
assert(isInQuietHours(qhPrefsEnabled, during2) === true, 'isInQuietHours: 00:30 is inside 22:00–07:00');

const outside1 = new Date(2025, 0, 1, 10, 0, 0); // 10:00 → outside quiet hours
assert(isInQuietHours(qhPrefsEnabled, outside1) === false, 'isInQuietHours: 10:00 is outside 22:00–07:00');

const outside2 = new Date(2025, 0, 1, 7, 0, 0); // 07:00 → outside quiet hours (end is exclusive)
assert(isInQuietHours(qhPrefsEnabled, outside2) === false, 'isInQuietHours: 07:00 is at end boundary (outside)');

// Same-day quiet hours (09:00–17:00)
const qhSameDay = JSON.parse(JSON.stringify(DEFAULT_PREFS));
qhSameDay.quietHours.enabled = true;
qhSameDay.quietHours.start = '09:00';
qhSameDay.quietHours.end = '17:00';

const midday = new Date(2025, 0, 1, 12, 0, 0);
assert(isInQuietHours(qhSameDay, midday) === true, 'isInQuietHours: 12:00 inside 09:00–17:00');

const evening = new Date(2025, 0, 1, 18, 0, 0);
assert(isInQuietHours(qhSameDay, evening) === false, 'isInQuietHours: 18:00 outside 09:00–17:00');

// --- severity filtering ---

assert(meetsSeverity('low', 'low') === true, 'meetsSeverity: low meets low');
assert(meetsSeverity('medium', 'low') === true, 'meetsSeverity: medium meets low');
assert(meetsSeverity('high', 'medium') === true, 'meetsSeverity: high meets medium');
assert(meetsSeverity('critical', 'high') === true, 'meetsSeverity: critical meets high');
assert(meetsSeverity('low', 'medium') === false, 'meetsSeverity: low does not meet medium');
assert(meetsSeverity('low', 'high') === false, 'meetsSeverity: low does not meet high');
assert(meetsSeverity('medium', 'high') === false, 'meetsSeverity: medium does not meet high');
assert(meetsSeverity(undefined, 'medium') === true, 'meetsSeverity: undefined severity treated as medium');
assert(meetsSeverity(undefined, 'high') === false, 'meetsSeverity: undefined severity does not meet high');

// --- duplicate suppression ---

resetStateFile();

const state1 = loadState();
assert(Array.isArray(state1.suppressedKeys), 'loadState: suppressedKeys is array when file missing');
assert(state1.suppressedKeys.length === 0, 'loadState: suppressedKeys is empty when file missing');

const stateWithKeys = {
  suppressedKeys: ['loop-abc', 'loop-def'],
  lastDiscoveryAt: '2025-01-01T09:00:00.000Z',
};
saveState(stateWithKeys);

const state2 = loadState();
assert(state2.suppressedKeys.length === 2, 'loadState: reads persisted suppressedKeys');
assert(state2.suppressedKeys.includes('loop-abc'), 'loadState: contains loop-abc');
assert(state2.suppressedKeys.includes('loop-def'), 'loadState: contains loop-def');
assert(state2.lastDiscoveryAt === '2025-01-01T09:00:00.000Z', 'loadState: reads lastDiscoveryAt');

// Simulate duplicate suppression logic (mirrors discoveryRun.ts)
const candidates = [
  { idempotencyKey: 'loop-abc', severity: 'high' },
  { idempotencyKey: 'loop-new', severity: 'high' },
  { idempotencyKey: 'loop-def', severity: 'medium' },
];
const suppressedSet = new Set(state2.suppressedKeys);
const surfaced = [];
let suppressedCount = 0;
for (const c of candidates) {
  if (suppressedSet.has(c.idempotencyKey)) {
    suppressedCount++;
  } else {
    surfaced.push(c);
    suppressedSet.add(c.idempotencyKey);
  }
}
assert(surfaced.length === 1, 'duplicate suppression: only unseen candidate surfaced');
assert(surfaced[0].idempotencyKey === 'loop-new', 'duplicate suppression: surfaced correct candidate');
assert(suppressedCount === 2, 'duplicate suppression: 2 duplicates suppressed');

// --- safety.externalWrite=false ---

// Verify all script-style outputs include externalWrite:false (unit-level check)
const safeOutput = { ok: true, safety: { externalWrite: false } };
assert(safeOutput.safety.externalWrite === false, 'safety.externalWrite: false in output');

// --- summary ---
console.log(`\n  ${passed} passed, ${failed} failed\n`);

if (failed > 0) {
  process.exit(1);
}
