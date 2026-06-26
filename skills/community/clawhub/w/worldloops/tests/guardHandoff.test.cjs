'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');

const apiEnv = {
  ...process.env,
  WORLDLOOPS_API_BASE_URL: process.env.WORLDLOOPS_API_BASE_URL || 'https://api.worldloops.ai',
};

console.log('\nguardHandoff tests\n');

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

function assertAgentExecutionGuardHeader(output, label) {
  assert.ok(
    output.includes('Agent Execution Guard'),
    `${label}: compact output must contain "Agent Execution Guard"`
  );
}

// ── guard:gmail with handoff example ─────────────────────────────────────────

{
  const result = run([
    'guard:gmail', '--',
    '--input', 'examples/handoff/openclaw-gmail-live.redacted.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:gmail handoff: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:gmail handoff');
  assertExternalWriteFalse(result.stdout, 'guard:gmail handoff');
  assertAgentExecutionGuardHeader(result.stdout, 'guard:gmail handoff');
  assert.ok(
    result.stdout.includes('externalWrite:false'),
    'guard:gmail handoff: compact output must include externalWrite:false (no space)'
  );
  console.log('  PASS  guard:gmail handoff: exits 0');
  console.log('  PASS  guard:gmail handoff: no raw JSON');
  console.log('  PASS  guard:gmail handoff: externalWrite:false present');
  console.log('  PASS  guard:gmail handoff: "Agent Execution Guard" header present');
}

// ── guard:calendar with handoff example ──────────────────────────────────────

{
  const result = run([
    'guard:calendar', '--',
    '--input', 'examples/handoff/openclaw-calendar-live.redacted.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:calendar handoff: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:calendar handoff');
  assertExternalWriteFalse(result.stdout, 'guard:calendar handoff');
  assertAgentExecutionGuardHeader(result.stdout, 'guard:calendar handoff');
  console.log('  PASS  guard:calendar handoff: exits 0');
  console.log('  PASS  guard:calendar handoff: no raw JSON');
  console.log('  PASS  guard:calendar handoff: externalWrite:false present');
  console.log('  PASS  guard:calendar handoff: "Agent Execution Guard" header present');
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
  assertAgentExecutionGuardHeader(result.stdout, 'guard:gmail gog');
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:gmail gog: must not contain "Invalid adapter signal"'
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
  assertAgentExecutionGuardHeader(result.stdout, 'guard:calendar gog');
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:calendar gog: must not contain "Invalid adapter signal"'
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
  assertAgentExecutionGuardHeader(result.stdout, 'guard:slack host payload');
  assert.ok(
    !result.stdout.includes('Invalid adapter signal'),
    'guard:slack host payload: must not contain "Invalid adapter signal"'
  );
  console.log('  PASS  guard:slack host payload: exits 0');
  console.log('  PASS  guard:slack host payload: no raw JSON');
  console.log('  PASS  guard:slack host payload: externalWrite:false present');
  console.log('  PASS  guard:slack host payload: "Agent Execution Guard" header present');
  console.log('  PASS  guard:slack host payload: no "Invalid adapter signal"');
}

// ── guard:slack with handoff example ─────────────────────────────────────────

{
  const result = run([
    'guard:slack', '--',
    '--input', 'examples/handoff/openclaw-slack-live.redacted.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:slack handoff: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:slack handoff');
  assertExternalWriteFalse(result.stdout, 'guard:slack handoff');
  assertAgentExecutionGuardHeader(result.stdout, 'guard:slack handoff');
  console.log('  PASS  guard:slack handoff: exits 0');
  console.log('  PASS  guard:slack handoff: no raw JSON');
  console.log('  PASS  guard:slack handoff: externalWrite:false present');
  console.log('  PASS  guard:slack handoff: "Agent Execution Guard" header present');
}

// ── guard:github with handoff example ────────────────────────────────────────

{
  const result = run([
    'guard:github', '--',
    '--input', 'examples/handoff/openclaw-github-live.redacted.json',
    '--compact',
  ]);
  assert.strictEqual(result.status, 0, `guard:github handoff: exit 0\n${result.stdout}\n${result.stderr}`);
  assertNoRawJson(result.stdout, 'guard:github handoff');
  assertExternalWriteFalse(result.stdout, 'guard:github handoff');
  assertAgentExecutionGuardHeader(result.stdout, 'guard:github handoff');
  console.log('  PASS  guard:github handoff: exits 0');
  console.log('  PASS  guard:github handoff: no raw JSON');
  console.log('  PASS  guard:github handoff: externalWrite:false present');
  console.log('  PASS  guard:github handoff: "Agent Execution Guard" header present');
}

// ── no connector / OAuth / fetch behavior ─────────────────────────────────────

{
  const src = fs.readFileSync('dist/scripts/guardAdapter.js', 'utf8');
  assert.ok(!src.includes('googleapis'), 'guardAdapter: must not reference googleapis');
  assert.ok(!src.includes('OAuth'), 'guardAdapter: must not reference OAuth');
  assert.ok(!src.includes('graph.microsoft.com'), 'guardAdapter: must not reference MS Graph');
  assert.ok(!src.includes('fetch('), 'guardAdapter: must not contain fetch() calls to external APIs');
  console.log('  PASS  guardAdapter: no connector/OAuth/fetch behavior introduced');
}

// ── Quick Start: no "openclaw skills install worldloops" ──────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const readme = fs.readFileSync('README.md', 'utf8');

  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  assert.ok(runtimeIdx !== -1, 'SKILL.md: must contain ## Agent Runtime Instructions section');
  const skillPublic = skill.slice(0, runtimeIdx);

  assert.ok(
    !skillPublic.includes('openclaw skills install worldloops'),
    'SKILL.md Quick Start: must not contain "openclaw skills install worldloops"'
  );
  assert.ok(
    !readme.includes('openclaw skills install worldloops'),
    'README.md: must not contain "openclaw skills install worldloops"'
  );
  console.log('  PASS  SKILL.md Quick Start: no "openclaw skills install worldloops"');
  console.log('  PASS  README.md: no "openclaw skills install worldloops"');
}

// ── Quick Start: npm run doctor not in primary path ───────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const readme = fs.readFileSync('README.md', 'utf8');

  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const skillPublic = skill.slice(0, runtimeIdx);

  // Find Quick Start code block
  const skillQsStart = skillPublic.indexOf('## Quick Start');
  assert.ok(skillQsStart !== -1, 'SKILL.md: must contain ## Quick Start section');
  const skillQsBlock = skillPublic.slice(skillQsStart);
  // The primary bash block ends at the first closing ```
  const firstCodeBlock = skillQsBlock.match(/```bash([\s\S]*?)```/);
  assert.ok(firstCodeBlock, 'SKILL.md: Quick Start must contain a bash code block');
  assert.ok(
    !firstCodeBlock[1].includes('npm run doctor'),
    'SKILL.md: primary Quick Start bash block must not include npm run doctor'
  );

  // README Quick Start
  const readmeQsStart = readme.indexOf('## 🚀 Quick Start');
  assert.ok(readmeQsStart !== -1, 'README.md: must contain ## 🚀 Quick Start section');
  const readmeQsBlock = readme.slice(readmeQsStart);
  const readmeFirstCodeBlock = readmeQsBlock.match(/```bash([\s\S]*?)```/);
  assert.ok(readmeFirstCodeBlock, 'README.md: Quick Start must contain a bash code block');
  assert.ok(
    !readmeFirstCodeBlock[1].includes('npm run doctor'),
    'README.md: primary Quick Start bash block must not include npm run doctor'
  );

  console.log('  PASS  SKILL.md: npm run doctor not in primary Quick Start bash block');
  console.log('  PASS  README.md: npm run doctor not in primary Quick Start bash block');
}

// ── Quick Start: clawhub install worldloops present ──────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const readme = fs.readFileSync('README.md', 'utf8');

  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const skillPublic = skill.slice(0, runtimeIdx);

  assert.ok(
    skillPublic.includes('clawhub install worldloops'),
    'SKILL.md: Quick Start must include "clawhub install worldloops"'
  );
  assert.ok(
    readme.includes('clawhub install worldloops'),
    'README.md: Quick Start must include "clawhub install worldloops"'
  );
  console.log('  PASS  SKILL.md: "clawhub install worldloops" present in Quick Start');
  console.log('  PASS  README.md: "clawhub install worldloops" present in Quick Start');
}

// ── Quick Start: Optional Safety Check section present ───────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const readme = fs.readFileSync('README.md', 'utf8');

  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const skillPublic = skill.slice(0, runtimeIdx);

  assert.ok(
    skillPublic.includes('Optional Safety Check'),
    'SKILL.md: must contain Optional Safety Check section'
  );
  assert.ok(
    readme.includes('Optional Safety Check'),
    'README.md: must contain Optional Safety Check section'
  );
  console.log('  PASS  SKILL.md: Optional Safety Check section present');
  console.log('  PASS  README.md: Optional Safety Check section present');
}

// ── OpenClaw Signal Handoff section present ───────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const readme = fs.readFileSync('README.md', 'utf8');

  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const skillPublic = skill.slice(0, runtimeIdx);

  assert.ok(
    skillPublic.includes('OpenClaw Signal Handoff'),
    'SKILL.md: must contain OpenClaw Signal Handoff section'
  );
  assert.ok(
    readme.includes('OpenClaw Signal Handoff'),
    'README.md: must contain OpenClaw Signal Handoff section'
  );
  assert.ok(
    skillPublic.includes('externalWrite:false') || skillPublic.includes('externalWrite: false'),
    'SKILL.md: OpenClaw Signal Handoff section must reference externalWrite:false'
  );
  assert.ok(
    skillPublic.includes('.worldloops/inbox/'),
    'SKILL.md: must document .worldloops/inbox/ convention'
  );
  assert.ok(
    readme.includes('.worldloops/inbox/'),
    'README.md: must document .worldloops/inbox/ convention'
  );
  console.log('  PASS  SKILL.md: OpenClaw Signal Handoff section present');
  console.log('  PASS  README.md: OpenClaw Signal Handoff section present');
  console.log('  PASS  SKILL.md: externalWrite:false referenced in handoff section');
  console.log('  PASS  SKILL.md: .worldloops/inbox/ convention documented');
  console.log('  PASS  README.md: .worldloops/inbox/ convention documented');
}

// ── Handoff examples exist ────────────────────────────────────────────────────

{
  const files = [
    'examples/handoff/openclaw-gmail-live.redacted.json',
    'examples/handoff/openclaw-calendar-live.redacted.json',
    'examples/handoff/openclaw-slack-live.redacted.json',
    'examples/handoff/openclaw-github-live.redacted.json',
  ];
  for (const f of files) {
    assert.ok(fs.existsSync(f), `Handoff example must exist: ${f}`);
    const parsed = JSON.parse(fs.readFileSync(f, 'utf8'));
    assert.ok(parsed.externalWrite === false, `${f}: externalWrite must be false`);
    assert.ok(typeof parsed.source === 'string', `${f}: source must be a string`);
  }
  console.log('  PASS  examples/handoff/: all four redacted handoff examples exist');
  console.log('  PASS  examples/handoff/: all examples have externalWrite:false');
  console.log('  PASS  examples/handoff/: all examples have source field');
}

// ── .worldloops/inbox/ directory exists ──────────────────────────────────────

{
  assert.ok(fs.existsSync('.worldloops/inbox'), '.worldloops/inbox/ directory must exist');
  console.log('  PASS  .worldloops/inbox/ directory exists');
}

// ── package.json version is 1.8.0 ────────────────────────────────────────────

{
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  assert.ok(
    pkg.version === '1.10.0' || pkg.version === '1.9.5' || pkg.version === '1.9.4',
    `package.json: version must be 1.10.0, 1.9.5, or 1.9.4, got ${pkg.version}`
  );
  assert.ok(pkg.scripts['test:guard-handoff'], 'package.json: test:guard-handoff script must exist');
  console.log(`  PASS  package.json: version is ${pkg.version}`);
  console.log('  PASS  package.json: test:guard-handoff script exists');
}

// ── SKILL.md version is 1.8.1 ────────────────────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  assert.ok(
    skill.includes('version: "1.10.0"') || skill.includes('version: "1.9.5"') || skill.includes('version: "1.9.4"'),
    'SKILL.md: version must be 1.10.0, 1.9.5, or 1.9.4'
  );
  const skillVer = skill.match(/version: "([^"]+)"/)?.[1] ?? 'unknown';
  console.log(`  PASS  SKILL.md: version is ${skillVer}`);
}

console.log('\nguardHandoff: all assertions passed\n');
