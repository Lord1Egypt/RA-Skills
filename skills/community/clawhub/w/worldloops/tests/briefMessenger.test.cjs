'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');

const ADAPTER_SIGNAL = 'examples/adapters/gmail-claim-contact-request.example.json';

const apiEnv = {
  ...process.env,
  WORLDLOOPS_API_BASE_URL: process.env.WORLDLOOPS_API_BASE_URL || 'https://api.worldloops.ai',
};

console.log('\nbriefMessenger tests\n');

// --- --format messenger via brief:reconcile ---
const reconcileResult = spawnSync(
  'npm',
  [
    'run',
    '--silent',
    'brief:reconcile',
    '--',
    '--adapter-signal',
    ADAPTER_SIGNAL,
    '--format',
    'messenger',
  ],
  { encoding: 'utf8', env: apiEnv }
);

assert.strictEqual(
  reconcileResult.status,
  0,
  `--format messenger: expected exit 0\n${reconcileResult.stdout}\n${reconcileResult.stderr}`
);

const out = reconcileResult.stdout;

assert.ok(
  !out.trim().startsWith('{'),
  '--format messenger: output must not start with raw JSON braces'
);
assert.ok(
  !out.includes('"openLoops":'),
  '--format messenger: output must not contain raw "openLoops":'
);
assert.ok(
  !out.includes('"proposalCandidates":'),
  '--format messenger: output must not contain raw "proposalCandidates":'
);
assert.ok(
  out.includes('externalWrite: false'),
  '--format messenger: output must contain "externalWrite: false"'
);
assert.ok(
  out.includes('WorldLoops Guard'),
  '--format messenger: output must contain "WorldLoops Guard"'
);
assert.ok(
  !out.toLowerCase().includes('telegram'),
  '--format messenger: output must not contain Telegram-specific naming'
);

console.log('  PASS  --format messenger: exits 0');
console.log('  PASS  --format messenger: output does not start with raw JSON braces');
console.log('  PASS  --format messenger: no raw "openLoops":');
console.log('  PASS  --format messenger: no raw "proposalCandidates":');
console.log('  PASS  --format messenger: externalWrite: false present');
console.log('  PASS  --format messenger: WorldLoops Guard header present');
console.log('  PASS  --format messenger: no Telegram-specific naming');

if (out.includes('requires_approval')) {
  console.log('  PASS  --format messenger: requires_approval present');
} else {
  console.log('  NOTE  --format messenger: requires_approval not in output (API may have returned no candidates)');
}

// --- brief:messenger alias ---
const messengerResult = spawnSync(
  'npm',
  ['run', '--silent', 'brief:messenger', '--', '--adapter-signal', ADAPTER_SIGNAL],
  { encoding: 'utf8', env: apiEnv }
);

assert.strictEqual(
  messengerResult.status,
  0,
  `brief:messenger: expected exit 0\n${messengerResult.stdout}\n${messengerResult.stderr}`
);

const mout = messengerResult.stdout;

assert.ok(
  !mout.trim().startsWith('{'),
  'brief:messenger: output must not start with raw JSON braces'
);
assert.ok(
  !mout.includes('"openLoops":'),
  'brief:messenger: output must not contain raw "openLoops":'
);
assert.ok(
  !mout.includes('"proposalCandidates":'),
  'brief:messenger: output must not contain raw "proposalCandidates":'
);
assert.ok(
  mout.includes('externalWrite: false'),
  'brief:messenger: output must contain "externalWrite: false"'
);

console.log('  PASS  brief:messenger: exits 0');
console.log('  PASS  brief:messenger: output does not start with raw JSON braces');
console.log('  PASS  brief:messenger: no raw "openLoops":');
console.log('  PASS  brief:messenger: no raw "proposalCandidates":');
console.log('  PASS  brief:messenger: externalWrite: false present');

console.log('\nbriefMessenger: all assertions passed\n');
