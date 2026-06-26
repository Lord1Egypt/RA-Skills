'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');

const apiEnv = {
  ...process.env,
  WORLDLOOPS_API_BASE_URL: process.env.WORLDLOOPS_API_BASE_URL || 'https://api.worldloops.ai',
};

console.log('\nguardAdapter tests\n');

// ── helpers ───────────────────────────────────────────────────────────────────

function run(args, env) {
  return spawnSync('npm', ['run', '--silent', ...args], {
    encoding: 'utf8',
    env: env || apiEnv,
  });
}

function assertNoRawJson(output, label) {
  assert.ok(!output.trim().startsWith('{'), `${label}: must not start with raw JSON`);
  assert.ok(!output.includes('"openLoops":'), `${label}: must not contain "openLoops":`);
  assert.ok(!output.includes('"proposalCandidates":'), `${label}: must not contain "proposalCandidates":`);
}

function assertExternalWriteFalse(output, label) {
  assert.ok(
    output.includes('externalWrite: false') || output.includes('externalWrite:false'),
    `${label}: must include externalWrite: false`
  );
}

function assertSafe(output, label) {
  assert.ok(output.includes('✅ Safe') || output.includes('Safe'), `${label}: must include Safe`);
}

// ── npm run demo ──────────────────────────────────────────────────────────────

{
  const result = run(['demo']);
  assert.strictEqual(result.status, 0, `demo: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'demo');
  assert.ok(
    result.stdout.includes('externalWrite:false'),
    'demo: must include externalWrite:false (no space)'
  );
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    'demo: header must be "Agent Execution Guard"'
  );
  assert.ok(
    result.stdout.includes('requires_approval'),
    'demo: must include requires_approval'
  );
  assert.ok(
    !result.stdout.includes('WorldLoops found 6 open loops'),
    'demo: must NOT output "WorldLoops found 6 open loops"'
  );
  assert.ok(
    result.stdout.includes('No email, draft, call, or external change made.'),
    'demo: must include compact safety line'
  );
  console.log('  PASS  demo: exits 0');
  console.log('  PASS  demo: no raw JSON');
  console.log('  PASS  demo: externalWrite:false present (no space)');
  console.log('  PASS  demo: "Agent Execution Guard" header present');
  console.log('  PASS  demo: requires_approval present');
  console.log('  PASS  demo: no "WorldLoops found 6 open loops"');
  console.log('  PASS  demo: compact safety line present');
}

// ── npm run guard:demo ────────────────────────────────────────────────────────

{
  const result = run(['guard:demo']);
  assert.strictEqual(result.status, 0, `guard:demo: expected exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:demo');
  assert.ok(
    result.stdout.includes('externalWrite:false'),
    'guard:demo: must include externalWrite:false (no space)'
  );
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    'guard:demo: header must be "Agent Execution Guard"'
  );
  assert.ok(
    result.stdout.includes('requires_approval'),
    'guard:demo: must include requires_approval'
  );
  assert.ok(
    !result.stdout.includes('WorldLoops found 6 open loops'),
    'guard:demo: must NOT output "WorldLoops found 6 open loops"'
  );
  assert.ok(
    result.stdout.includes('No email, draft, call, or external change made.'),
    'guard:demo: must include compact safety line'
  );
  console.log('  PASS  guard:demo: exits 0');
  console.log('  PASS  guard:demo: no raw JSON');
  console.log('  PASS  guard:demo: externalWrite:false present (no space)');
  console.log('  PASS  guard:demo: "Agent Execution Guard" header present');
  console.log('  PASS  guard:demo: requires_approval present');
  console.log('  PASS  guard:demo: no "WorldLoops found 6 open loops"');
  console.log('  PASS  guard:demo: compact safety line present');
}

// ── guard:adapter --source gmail ──────────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'gmail',
    '--input', 'examples/adapters/openclaw-gmail-claim.json',
    '--format', 'messenger',
  ]);
  assert.strictEqual(result.status, 0, `guard:adapter gmail: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:adapter gmail');
  assertExternalWriteFalse(result.stdout, 'guard:adapter gmail');
  assertSafe(result.stdout, 'guard:adapter gmail');
  console.log('  PASS  guard:adapter --source gmail: exits 0');
  console.log('  PASS  guard:adapter --source gmail: no raw JSON');
  console.log('  PASS  guard:adapter --source gmail: externalWrite: false present');
}

// ── guard:adapter --source calendar ──────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'calendar',
    '--input', 'examples/adapters/openclaw-calendar-prep.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:adapter calendar: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:adapter calendar');
  assertExternalWriteFalse(result.stdout, 'guard:adapter calendar');
  console.log('  PASS  guard:adapter --source calendar: exits 0');
  console.log('  PASS  guard:adapter --source calendar: no raw JSON');
}

// ── guard:adapter --source slack ──────────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'slack',
    '--input', 'examples/adapters/openclaw-slack-review-request.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:adapter slack: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:adapter slack');
  assertExternalWriteFalse(result.stdout, 'guard:adapter slack');
  console.log('  PASS  guard:adapter --source slack: exits 0');
  console.log('  PASS  guard:adapter --source slack: no raw JSON');
}

// ── guard:adapter --source github ─────────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'github',
    '--input', 'examples/adapters/openclaw-github-pr-review.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:adapter github: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:adapter github');
  assertExternalWriteFalse(result.stdout, 'guard:adapter github');
  console.log('  PASS  guard:adapter --source github: exits 0');
  console.log('  PASS  guard:adapter --source github: no raw JSON');
}

// ── guard:adapter --source generic ────────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'generic',
    '--input', 'examples/adapters/openclaw-generic-task.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:adapter generic: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:adapter generic');
  assertExternalWriteFalse(result.stdout, 'guard:adapter generic');
  console.log('  PASS  guard:adapter --source generic: exits 0');
  console.log('  PASS  guard:adapter --source generic: no raw JSON');
}

// ── guard:gmail alias ─────────────────────────────────────────────────────────

{
  const result = run([
    'guard:gmail', '--',
    '--input', 'examples/adapters/openclaw-gmail-claim.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:gmail: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:gmail');
  assertExternalWriteFalse(result.stdout, 'guard:gmail');
  console.log('  PASS  guard:gmail: exits 0');
  console.log('  PASS  guard:gmail: no raw JSON');
  console.log('  PASS  guard:gmail: externalWrite: false present');
}

// ── guard:calendar alias ──────────────────────────────────────────────────────

{
  const result = run([
    'guard:calendar', '--',
    '--input', 'examples/adapters/openclaw-calendar-prep.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:calendar: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:calendar');
  assertExternalWriteFalse(result.stdout, 'guard:calendar');
  console.log('  PASS  guard:calendar: exits 0');
  console.log('  PASS  guard:calendar: no raw JSON');
}

// ── guard:slack alias ─────────────────────────────────────────────────────────

{
  const result = run([
    'guard:slack', '--',
    '--input', 'examples/adapters/openclaw-slack-review-request.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:slack: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:slack');
  assertExternalWriteFalse(result.stdout, 'guard:slack');
  console.log('  PASS  guard:slack: exits 0');
  console.log('  PASS  guard:slack: no raw JSON');
}

// ── guard:github alias ────────────────────────────────────────────────────────

{
  const result = run([
    'guard:github', '--',
    '--input', 'examples/adapters/openclaw-github-pr-review.json',
  ]);
  assert.strictEqual(result.status, 0, `guard:github: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:github');
  assertExternalWriteFalse(result.stdout, 'guard:github');
  console.log('  PASS  guard:github: exits 0');
  console.log('  PASS  guard:github: no raw JSON');
}

// ── --compact flag ────────────────────────────────────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'gmail',
    '--input', 'examples/adapters/openclaw-gmail-claim.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `--compact: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, '--compact');
  assert.ok(
    result.stdout.includes('externalWrite:false'),
    '--compact: must include externalWrite:false (no space)'
  );
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    '--compact: header must be "Agent Execution Guard"'
  );
  assert.ok(
    result.stdout.includes('No email, draft, call, or external change made.'),
    '--compact: must include compact safety line'
  );
  console.log('  PASS  --compact: exits 0');
  console.log('  PASS  --compact: no raw JSON');
  console.log('  PASS  --compact: externalWrite:false present (no space)');
  console.log('  PASS  --compact: "Agent Execution Guard" header present');
  console.log('  PASS  --compact: compact safety line present');
}

// ── externalWrite:false enforced — no external connector ─────────────────────

{
  // Verify guardAdapter.js does not import or reference fetch of Gmail/Calendar/Slack/GitHub
  const src = fs.readFileSync('dist/scripts/guardAdapter.js', 'utf8');
  assert.ok(!src.includes('googleapis'), 'guardAdapter: must not reference googleapis');
  assert.ok(!src.includes('OAuth'), 'guardAdapter: must not reference OAuth');
  assert.ok(!src.includes('graph.microsoft.com'), 'guardAdapter: must not reference MS Graph');
  console.log('  PASS  guardAdapter: no connector/OAuth code');
}

// ── SKILL.md: first public section clean ──────────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');

  // Find the ## Agent Runtime Instructions boundary
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  assert.ok(runtimeIdx !== -1, 'SKILL.md: must contain ## Agent Runtime Instructions section');

  const publicSection = skill.slice(0, runtimeIdx);

  assert.ok(
    !publicSection.includes('Do not inspect `package.json` first'),
    'SKILL.md: public section must not include "Do not inspect package.json first"'
  );
  assert.ok(
    !publicSection.includes('Do not search the workspace first'),
    'SKILL.md: public section must not include "Do not search the workspace first"'
  );
  assert.ok(
    !publicSection.includes('Do not print raw JSON'),
    'SKILL.md: public section must not include "Do not print raw JSON"'
  );

  // Verify agent-facing rules exist after the Agent Runtime Instructions boundary
  const runtimeSection = skill.slice(runtimeIdx);
  assert.ok(
    runtimeSection.includes('Do not invent missing source data'),
    'SKILL.md: agent runtime instructions must appear after ## Agent Runtime Instructions'
  );

  console.log('  PASS  SKILL.md: public section does not contain agent-facing runtime phrases');
  console.log('  PASS  SKILL.md: agent runtime instructions are in ## Agent Runtime Instructions section');
}

// ── SKILL.md: version updated ─────────────────────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  assert.ok(
    skill.includes('version: "1.10.0"') || skill.includes('version: "1.9.5"') || skill.includes('version: "1.9.4"'),
    'SKILL.md: version must be 1.10.0, 1.9.5, or 1.9.4'
  );
  const skillVersion = skill.match(/version: "([^"]+)"/)?.[1] ?? 'unknown';
  console.log(`  PASS  SKILL.md: version is ${skillVersion}`);
}

// ── package.json: version and scripts ────────────────────────────────────────

{
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  assert.ok(
    pkg.version === '1.10.0' || pkg.version === '1.9.5' || pkg.version === '1.9.4',
    `package.json: version must be 1.10.0, 1.9.5, or 1.9.4, got ${pkg.version}`
  );
  assert.ok(pkg.scripts.demo, 'package.json: demo script must exist');
  assert.ok(pkg.scripts['guard:demo'], 'package.json: guard:demo script must exist');
  assert.ok(pkg.scripts['guard:adapter'], 'package.json: guard:adapter script must exist');
  assert.ok(pkg.scripts['guard:gmail'], 'package.json: guard:gmail script must exist');
  assert.ok(pkg.scripts['guard:calendar'], 'package.json: guard:calendar script must exist');
  assert.ok(pkg.scripts['guard:slack'], 'package.json: guard:slack script must exist');
  assert.ok(pkg.scripts['guard:github'], 'package.json: guard:github script must exist');
  assert.ok(
    pkg.scripts.demo.includes('guardAdapter.js') && pkg.scripts.demo.includes('--compact'),
    'package.json: demo script must use guardAdapter.js --compact'
  );
  assert.ok(
    pkg.scripts['guard:demo'].includes('guardAdapter.js') && pkg.scripts['guard:demo'].includes('--compact'),
    'package.json: guard:demo script must use guardAdapter.js --compact'
  );
  assert.ok(!pkg.scripts['wow:mobile'], 'package.json: wow:mobile must be removed (v1.8.0 routing cleanup)');
  console.log(`  PASS  package.json: version is ${pkg.version}`);
  console.log('  PASS  package.json: all guard scripts present');
  console.log('  PASS  package.json: demo uses guardAdapter.js --compact');
  console.log('  PASS  package.json: guard:demo uses guardAdapter.js --compact');
  console.log('  PASS  package.json: wow:mobile removed');
}

// ── guard:gmail with gog fixture ─────────────────────────────────────────────

{
  const result = run([
    'guard:gmail', '--',
    '--input', 'scripts/fixtures/gog-gmail-messages.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:gmail gog: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:gmail gog');
  assertExternalWriteFalse(result.stdout, 'guard:gmail gog');
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    'guard:gmail gog: must include "Agent Execution Guard"'
  );
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:gmail gog: must not include "Invalid adapter signal"'
  );
  console.log('  PASS  guard:gmail gog fixture: exits 0');
  console.log('  PASS  guard:gmail gog fixture: no raw JSON');
  console.log('  PASS  guard:gmail gog fixture: externalWrite:false present');
  console.log('  PASS  guard:gmail gog fixture: "Agent Execution Guard" header present');
  console.log('  PASS  guard:gmail gog fixture: no "Invalid adapter signal"');
}

// ── guard:calendar with gog fixture ──────────────────────────────────────────

{
  const result = run([
    'guard:calendar', '--',
    '--input', 'scripts/fixtures/gog-calendar-events.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:calendar gog: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:calendar gog');
  assertExternalWriteFalse(result.stdout, 'guard:calendar gog');
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    'guard:calendar gog: must include "Agent Execution Guard"'
  );
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:calendar gog: must not include "Invalid adapter signal"'
  );
  console.log('  PASS  guard:calendar gog fixture: exits 0');
  console.log('  PASS  guard:calendar gog fixture: no raw JSON');
  console.log('  PASS  guard:calendar gog fixture: externalWrite:false present');
  console.log('  PASS  guard:calendar gog fixture: "Agent Execution Guard" header present');
  console.log('  PASS  guard:calendar gog fixture: no "Invalid adapter signal"');
}

// ── guard:slack with host payload fixture ─────────────────────────────────────

{
  const result = run([
    'guard:slack', '--',
    '--input', 'scripts/fixtures/slack-messages.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:slack host payload: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:slack host payload');
  assertExternalWriteFalse(result.stdout, 'guard:slack host payload');
  assert.ok(
    result.stdout.includes('Agent Execution Guard'),
    'guard:slack host payload: must include "Agent Execution Guard"'
  );
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:slack host payload: must not include "Invalid adapter signal"'
  );
  console.log('  PASS  guard:slack host payload: exits 0');
  console.log('  PASS  guard:slack host payload: no raw JSON');
  console.log('  PASS  guard:slack host payload: externalWrite:false present');
  console.log('  PASS  guard:slack host payload: "Agent Execution Guard" header present');
  console.log('  PASS  guard:slack host payload: no "Invalid adapter signal"');
}

// ── no connector / OAuth / fetch in dist ──────────────────────────────────────

{
  const src = fs.readFileSync('dist/scripts/guardAdapter.js', 'utf8');
  assert.ok(!src.includes('googleapis'), 'guardAdapter: must not reference googleapis');
  assert.ok(!src.includes('OAuth'), 'guardAdapter: must not reference OAuth');
  assert.ok(!src.includes('graph.microsoft.com'), 'guardAdapter: must not reference MS Graph');
  assert.ok(!src.includes("fetch('"), 'guardAdapter: must not contain fetch() calls');
  assert.ok(!src.includes('fetch("'), 'guardAdapter: must not contain fetch() calls');
  console.log('  PASS  guardAdapter: no connector/OAuth/fetch behavior in dist');
}

// ── no --input → exits 1 with safe output ────────────────────────────────────

{
  const result = run(['guard:adapter', '--', '--source', 'gmail']);
  assert.strictEqual(result.status, 1, 'guard:adapter missing --input: must exit 1');
  assertExternalWriteFalse(result.stdout, 'guard:adapter missing --input');
  assertNoRawJson(result.stdout, 'guard:adapter missing --input');
  console.log('  PASS  guard:adapter missing --input: exits 1 safely');
}

// ── unknown --source → exits 1 with safe output ──────────────────────────────

{
  const result = run([
    'guard:adapter', '--',
    '--source', 'fakeconnector',
    '--input', 'examples/adapters/openclaw-gmail-claim.json',
  ]);
  assert.strictEqual(result.status, 1, 'guard:adapter unknown source: must exit 1');
  assertExternalWriteFalse(result.stdout, 'guard:adapter unknown source');
  assertNoRawJson(result.stdout, 'guard:adapter unknown source');
  console.log('  PASS  guard:adapter unknown --source: exits 1 safely');
}

console.log('\nguardAdapter: all assertions passed\n');
