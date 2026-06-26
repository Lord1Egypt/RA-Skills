import { spawnSync } from 'node:child_process';

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const apiEnv = {
  ...process.env,
  WORLDLOOPS_API_BASE_URL:
    process.env.WORLDLOOPS_API_BASE_URL || 'https://api.worldloops.ai',
};

console.log('\nsmoke:public (requires public worldloops API)\n');

// --- standard multi-source reconcile ---
const result = spawnSync(
  'npm',
  [
    'run',
    '--silent',
    'brief:reconcile',
    '--',
    '--gmail-event',
    'scripts/fixtures/openclaw-gmail-webhook.json',
    '--calendar-event',
    'scripts/fixtures/openclaw-calendar-events.json',
    '--gog-gmail',
    'scripts/fixtures/gog-gmail-messages.json',
    '--gog-calendar',
    'scripts/fixtures/gog-calendar-events.json',
  ],
  { encoding: 'utf8', env: apiEnv }
);

assert(result.status === 0, `expected exit 0\n${result.stdout}\n${result.stderr}`);

let parsed;
try {
  parsed = JSON.parse(result.stdout);
} catch (err) {
  throw new Error(`stdout is not JSON:\n${result.stdout}\n${err}`);
}

assert(typeof parsed.ok === 'boolean', 'ok should be boolean');
assert(parsed.safety?.externalWrite === false, 'externalWrite should be false');

if (parsed.ok) {
  assert(Array.isArray(parsed.openLoops), 'openLoops should be an array');
  assert(Array.isArray(parsed.proposalCandidates), 'proposalCandidates should be an array');
}

console.log('  PASS  public reconcile command returns stable JSON');
console.log('  PASS  safety.externalWrite is false');

// --- Re: thread fixture (blind-spot regression) ---
const reThreadResult = spawnSync(
  'npm',
  [
    'run',
    '--silent',
    'brief:reconcile',
    '--',
    '--gog-gmail',
    'scripts/fixtures/gog-gmail-re-thread.json',
  ],
  { encoding: 'utf8', env: apiEnv }
);

assert(
  reThreadResult.status === 0,
  `Re: thread fixture: expected exit 0\n${reThreadResult.stdout}\n${reThreadResult.stderr}`
);

let parsedReThread;
try {
  parsedReThread = JSON.parse(reThreadResult.stdout);
} catch (err) {
  throw new Error(`Re: thread fixture stdout is not JSON:\n${reThreadResult.stdout}\n${err}`);
}

assert(typeof parsedReThread.ok === 'boolean', 'Re: thread fixture: ok should be boolean');
assert(
  parsedReThread.safety?.externalWrite === false,
  'Re: thread fixture: externalWrite should be false'
);

console.log('  PASS  Re: thread fixture runs without error');
console.log('  PASS  Re: thread fixture: safety.externalWrite is false');

console.log('\n4 tests — 4 passed, 0 failed\n');
