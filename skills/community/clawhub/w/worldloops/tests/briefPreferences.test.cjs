'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

// Use a fresh temp dir so tests never touch the real .worldloops/ prefs
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'worldloops-brief-prefs-test-'));

const testEnv = {
  ...process.env,
  WORLDLOOPS_DIR: tmpDir,
  WORLDLOOPS_API_BASE_URL: process.env.WORLDLOOPS_API_BASE_URL || 'https://api.worldloops.ai',
};

const FIXTURE_INBOX = 'scripts/fixtures/inbox';

console.log('\nbriefPreferences tests\n');

function run(args, env) {
  return spawnSync('npm', ['run', '--silent', ...args], {
    encoding: 'utf8',
    env: env || testEnv,
  });
}

function assertExternalWriteFalse(output, label) {
  assert.ok(
    output.includes('externalWrite:false') || output.includes('externalWrite: false') ||
    output.includes('sourceExternalWrite:false'),
    `${label}: must include externalWrite:false`
  );
}

// ── brief:preferences exits 0 ─────────────────────────────────────────────────

{
  const result = run(['brief:preferences']);
  assert.strictEqual(result.status, 0, `brief:preferences: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assert.ok(result.stdout.includes('Daily Brief'), 'brief:preferences: must mention Daily Brief');
  assertExternalWriteFalse(result.stdout, 'brief:preferences');
  console.log('  PASS  brief:preferences: exits 0');
  console.log('  PASS  brief:preferences: mentions Daily Brief');
  console.log('  PASS  brief:preferences: externalWrite:false present');
}

// ── default time is 09:00 ─────────────────────────────────────────────────────

{
  const result = run(['brief:preferences']);
  assert.ok(result.stdout.includes('09:00'), 'brief:preferences: default time must be 09:00');
  console.log('  PASS  brief:preferences: default time is 09:00');
}

// ── v1.9.1: default schedule says local time, not UTC ────────────────────────

{
  const result = run(['brief:preferences']);
  assert.ok(
    result.stdout.includes('local time'),
    'brief:preferences: default schedule must say "local time"'
  );
  assert.ok(
    !result.stdout.includes('(UTC)'),
    'brief:preferences: default schedule must not say "(UTC)"'
  );
  console.log('  PASS  brief:preferences: default schedule says "local time"');
  console.log('  PASS  brief:preferences: default schedule does not say "(UTC)"');
}

// ── v1.9.1: brief:deliver --dry-run says local time ──────────────────────────

{
  const result = run(['guard:daily', '--', '--inbox', FIXTURE_INBOX]);
  assert.ok(
    result.stdout.includes('local time'),
    'guard:daily: schedule line must say "local time"'
  );
  assert.ok(
    !result.stdout.includes('(UTC)'),
    'guard:daily: schedule line must not say "(UTC)"'
  );
  console.log('  PASS  guard:daily: schedule says "local time"');
  console.log('  PASS  guard:daily: schedule does not say "(UTC)"');
}

// ── default delivery channel is local ─────────────────────────────────────────

{
  const result = run(['brief:preferences']);
  assert.ok(result.stdout.toLowerCase().includes('local'), 'brief:preferences: default channel must be local');
  console.log('  PASS  brief:preferences: default delivery channel is local');
}

// ── brief:preferences:set -- --time 08:30 ────────────────────────────────────

{
  const setResult = run(['brief:preferences:set', '--', '--time', '08:30']);
  assert.strictEqual(setResult.status, 0, `brief:preferences:set --time: exit 0\n${setResult.stdout}\n${setResult.stderr}`);
  assertExternalWriteFalse(setResult.stdout, 'brief:preferences:set --time');

  const showResult = run(['brief:preferences']);
  assert.ok(showResult.stdout.includes('08:30'), 'brief:preferences: time updated to 08:30');
  console.log('  PASS  brief:preferences:set --time 08:30: exits 0');
  console.log('  PASS  brief:preferences:set --time 08:30: externalWrite:false present');
  console.log('  PASS  brief:preferences: time updated to 08:30');
}

// ── brief:preferences:set -- --channel telegram ──────────────────────────────

{
  const setResult = run(['brief:preferences:set', '--', '--channel', 'telegram']);
  assert.strictEqual(setResult.status, 0, `brief:preferences:set --channel telegram: exit 0\n${setResult.stdout}\n${setResult.stderr}`);
  assertExternalWriteFalse(setResult.stdout, 'brief:preferences:set --channel telegram');

  const showResult = run(['brief:preferences']);
  assert.ok(showResult.stdout.includes('telegram'), 'brief:preferences: channel updated to telegram');
  console.log('  PASS  brief:preferences:set --channel telegram: exits 0');
  console.log('  PASS  brief:preferences: channel updated to telegram');
}

// ── brief:preferences:set -- --channel slack ──────────────────────────────────

{
  const setResult = run(['brief:preferences:set', '--', '--channel', 'slack']);
  assert.strictEqual(setResult.status, 0, `brief:preferences:set --channel slack: exit 0\n${setResult.stdout}\n${setResult.stderr}`);

  const showResult = run(['brief:preferences']);
  assert.ok(showResult.stdout.includes('slack'), 'brief:preferences: channel updated to slack');
  console.log('  PASS  brief:preferences:set --channel slack: exits 0');
  console.log('  PASS  brief:preferences: channel updated to slack');
}

// ── brief:preferences:set -- --channel discord ────────────────────────────────

{
  const setResult = run(['brief:preferences:set', '--', '--channel', 'discord']);
  assert.strictEqual(setResult.status, 0, `brief:preferences:set --channel discord: exit 0\n${setResult.stdout}\n${setResult.stderr}`);
  console.log('  PASS  brief:preferences:set --channel discord: exits 0');
}

// ── brief:preferences:set -- --channel local (reset) ─────────────────────────

{
  const setResult = run(['brief:preferences:set', '--', '--channel', 'local']);
  assert.strictEqual(setResult.status, 0, `brief:preferences:set --channel local: exit 0\n${setResult.stdout}\n${setResult.stderr}`);
  console.log('  PASS  brief:preferences:set --channel local: exits 0');
}

// ── guard:daily includes schedule and delivery channel info ──────────────────

{
  const result = run(['guard:daily', '--', '--inbox', FIXTURE_INBOX]);
  assert.strictEqual(result.status, 0, `guard:daily with prefs: expected exit 0\n${result.stdout}\n${result.stderr}`);

  // After resetting to local, output should include schedule and channel info
  const hasSchedule = result.stdout.includes('schedule') || result.stdout.includes('Schedule') ||
    result.stdout.includes('08:30') || result.stdout.includes('09:00');
  assert.ok(hasSchedule, 'guard:daily: must include schedule info');

  const hasChannel = result.stdout.includes('channel') || result.stdout.includes('Channel') ||
    result.stdout.includes('local') || result.stdout.includes('telegram');
  assert.ok(hasChannel, 'guard:daily: must include delivery channel info');

  console.log('  PASS  guard:daily: includes schedule info');
  console.log('  PASS  guard:daily: includes delivery channel info');
}

// ── brief:deliver --dry-run exits 0 ──────────────────────────────────────────

{
  const result = run(['brief:deliver', '--', '--dry-run', '--inbox', FIXTURE_INBOX]);
  assert.strictEqual(result.status, 0, `brief:deliver --dry-run: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assert.ok(
    result.stdout.includes('Daily Brief'),
    'brief:deliver --dry-run: must mention Daily Brief'
  );
  assert.ok(
    result.stdout.includes('dry-run'),
    'brief:deliver --dry-run: output must include "dry-run"'
  );
  assertExternalWriteFalse(result.stdout, 'brief:deliver --dry-run');
  assert.ok(
    result.stdout.includes('sourceExternalWrite:false') ||
    result.stdout.includes('No Gmail, Calendar, or Slack'),
    'brief:deliver --dry-run: must confirm no external system modified'
  );
  console.log('  PASS  brief:deliver --dry-run: exits 0');
  console.log('  PASS  brief:deliver --dry-run: mentions Daily Brief');
  console.log('  PASS  brief:deliver --dry-run: dry-run mode labeled');
  console.log('  PASS  brief:deliver --dry-run: source safety confirmed');
}

// ── brief:deliver --channel telegram exits 0, delivery-ready message ─────────

{
  const result = run(['brief:deliver', '--', '--channel', 'telegram', '--inbox', FIXTURE_INBOX]);
  assert.strictEqual(result.status, 0, `brief:deliver --channel telegram: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assert.ok(
    result.stdout.includes('telegram') || result.stdout.includes('Telegram'),
    'brief:deliver --channel telegram: output must mention telegram'
  );
  assert.ok(
    result.stdout.includes('not active') || result.stdout.includes('Delivery-ready') ||
    result.stdout.includes('delivery'),
    'brief:deliver --channel telegram: must show delivery status'
  );
  assertExternalWriteFalse(result.stdout, 'brief:deliver --channel telegram');
  console.log('  PASS  brief:deliver --channel telegram: exits 0');
  console.log('  PASS  brief:deliver --channel telegram: delivery channel mentioned');
  console.log('  PASS  brief:deliver --channel telegram: delivery status shown');
  console.log('  PASS  brief:deliver --channel telegram: externalWrite:false present');
}

// ── brief:deliver --channel slack exits 0, delivery-ready message ─────────────

{
  const result = run(['brief:deliver', '--', '--channel', 'slack', '--inbox', FIXTURE_INBOX]);
  assert.strictEqual(result.status, 0, `brief:deliver --channel slack: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assert.ok(
    result.stdout.includes('slack') || result.stdout.includes('Slack'),
    'brief:deliver --channel slack: output must mention slack'
  );
  assertExternalWriteFalse(result.stdout, 'brief:deliver --channel slack');
  console.log('  PASS  brief:deliver --channel slack: exits 0');
  console.log('  PASS  brief:deliver --channel slack: slack mentioned');
}

// ── brief:deliver --channel local (default local output) ─────────────────────

{
  const result = run(['brief:deliver', '--', '--channel', 'local', '--inbox', FIXTURE_INBOX]);
  assert.strictEqual(result.status, 0, `brief:deliver --channel local: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assert.ok(
    result.stdout.includes('Daily Brief'),
    'brief:deliver --channel local: must mention Daily Brief'
  );
  assert.ok(
    result.stdout.includes('local'),
    'brief:deliver --channel local: must confirm local delivery mode'
  );
  console.log('  PASS  brief:deliver --channel local: exits 0');
  console.log('  PASS  brief:deliver --channel local: Daily Brief shown');
  console.log('  PASS  brief:deliver --channel local: local delivery confirmed');
}

// ── no cron/daemon scheduler installation in compiled scripts ─────────────────
// Check for actual scheduler usage (imports, API calls) not just the word in strings

{
  const files = [
    'dist/scripts/briefDeliver.js',
    'dist/scripts/briefPreferences.js',
    'dist/scripts/briefPreferencesSet.js',
    'dist/dailyBriefRunner.js',
  ];
  for (const f of files) {
    if (!fs.existsSync(f)) continue;
    const src = fs.readFileSync(f, 'utf8');
    assert.ok(!src.includes("require('cron')"), `${f}: must not import cron`);
    assert.ok(!src.includes('require("cron")'), `${f}: must not import cron`);
    assert.ok(!src.includes('CronJob'), `${f}: must not reference CronJob`);
    assert.ok(!src.includes('launchctl'), `${f}: must not reference launchctl`);
    assert.ok(!src.includes('new Daemon('), `${f}: must not instantiate Daemon`);
    assert.ok(!src.includes('setInterval('), `${f}: must not install background polling`);
  }
  console.log('  PASS  brief scripts: no cron/daemon/launchd scheduler installation');
}

// ── no connector/OAuth/direct-fetch in compiled scripts ──────────────────────

{
  const files = [
    'dist/scripts/briefDeliver.js',
    'dist/scripts/briefPreferences.js',
    'dist/scripts/briefPreferencesSet.js',
    'dist/dailyBriefRunner.js',
  ];
  for (const f of files) {
    if (!fs.existsSync(f)) continue;
    const src = fs.readFileSync(f, 'utf8');
    assert.ok(!src.includes('googleapis'), `${f}: must not reference googleapis`);
    assert.ok(!src.includes('OAuth'), `${f}: must not reference OAuth`);
    assert.ok(!src.includes("fetch('"), `${f}: must not contain fetch() with single-quote string`);
    assert.ok(!src.includes('fetch("'), `${f}: must not contain fetch() with double-quote string`);
  }
  console.log('  PASS  brief scripts: no connector/OAuth/direct-fetch behavior');
}

// ── SKILL.md: mentions default 09:00 local time and brief:preferences commands ─

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const publicSection = skill.slice(0, runtimeIdx);

  assert.ok(publicSection.includes('09:00'), 'SKILL.md: must mention default 09:00 time');
  assert.ok(
    publicSection.includes('local time'),
    'SKILL.md: must say "local time" for default schedule'
  );
  assert.ok(
    !publicSection.includes('09:00 (UTC)'),
    'SKILL.md: must not use "09:00 (UTC)"'
  );
  assert.ok(
    publicSection.includes('brief:preferences'),
    'SKILL.md: must document brief:preferences command'
  );
  assert.ok(
    publicSection.includes('brief:deliver'),
    'SKILL.md: must document brief:deliver command'
  );
  assert.ok(
    !publicSection.toLowerCase().includes('email is a messenger'),
    'SKILL.md: must not call email a messenger'
  );
  console.log('  PASS  SKILL.md: 09:00 default time mentioned');
  console.log('  PASS  SKILL.md: "local time" wording present');
  console.log('  PASS  SKILL.md: does not use "09:00 (UTC)"');
  console.log('  PASS  SKILL.md: brief:preferences documented');
  console.log('  PASS  SKILL.md: brief:deliver documented');
}

// ── package.json: new scripts exist ──────────────────────────────────────────

{
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  assert.ok(pkg.scripts['brief:preferences'], 'package.json: brief:preferences must exist');
  assert.ok(pkg.scripts['brief:preferences:set'], 'package.json: brief:preferences:set must exist');
  assert.ok(pkg.scripts['brief:deliver'], 'package.json: brief:deliver must exist');
  assert.ok(pkg.scripts['test:brief-preferences'], 'package.json: test:brief-preferences must exist');
  console.log('  PASS  package.json: brief:preferences, brief:preferences:set, brief:deliver present');
  console.log('  PASS  package.json: test:brief-preferences present');
}

// Cleanup temp dir
try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch { /* ignore */ }

console.log('\nbriefPreferences: all assertions passed\n');
