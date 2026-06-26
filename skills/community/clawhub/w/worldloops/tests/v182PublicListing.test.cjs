'use strict';

const assert = require('node:assert');
const fs = require('node:fs');

console.log('\nv182PublicListing tests\n');

// ── SKILL.md: no Korean phrase ────────────────────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  assert.ok(
    !skill.includes('데모 보여줘'),
    'SKILL.md: must not contain Korean phrase "데모 보여줘"'
  );
  console.log('  PASS  SKILL.md: no Korean phrase "데모 보여줘"');
}

// ── SKILL.md: safe default command is npm run --silent demo ───────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  assert.ok(runtimeIdx !== -1, 'SKILL.md: must contain ## Agent Runtime Instructions section');
  const runtimeSection = skill.slice(runtimeIdx);

  const defaultCmdIdx = runtimeSection.indexOf('Safe default command');
  assert.ok(defaultCmdIdx !== -1, 'SKILL.md runtime: must contain "Safe default command" section');

  const defaultCmdBlock = runtimeSection.slice(defaultCmdIdx, defaultCmdIdx + 300);

  assert.ok(
    defaultCmdBlock.includes('npm run --silent demo'),
    'SKILL.md: safe default command must be "npm run --silent demo"'
  );
  console.log('  PASS  SKILL.md: safe default command is npm run --silent demo');
}

// ── SKILL.md: brief:reconcile not the safe default runtime command ────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const runtimeSection = skill.slice(runtimeIdx);

  const defaultCmdIdx = runtimeSection.indexOf('Safe default command');
  assert.ok(defaultCmdIdx !== -1, 'SKILL.md runtime: must contain "Safe default command" section');

  const defaultCmdBlock = runtimeSection.slice(defaultCmdIdx, defaultCmdIdx + 300);

  assert.ok(
    !defaultCmdBlock.includes('brief:reconcile'),
    'SKILL.md: safe default command must not be brief:reconcile'
  );
  console.log('  PASS  SKILL.md: brief:reconcile not the safe default runtime command');
}

// ── SKILL.md: Output section is compact-first ─────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  assert.ok(runtimeIdx !== -1, 'SKILL.md: must contain ## Agent Runtime Instructions section');
  const runtimeSection = skill.slice(runtimeIdx);

  const outputIdx = runtimeSection.indexOf('### Output');
  assert.ok(outputIdx !== -1, 'SKILL.md: must contain ### Output section in runtime instructions');
  const outputBlock = runtimeSection.slice(outputIdx, outputIdx + 400);

  assert.ok(
    outputBlock.includes('compact') || outputBlock.includes('messenger-friendly'),
    'SKILL.md Output: must say compact or messenger-friendly output is default'
  );
  assert.ok(
    !outputBlock.includes('The skill returns safe JSON'),
    'SKILL.md Output: must not say "The skill returns safe JSON"'
  );
  console.log('  PASS  SKILL.md Output: compact/messenger-friendly is default');
  console.log('  PASS  SKILL.md Output: no "The skill returns safe JSON"');
}

// ── README.md: no JSON-first output wording ───────────────────────────────────

{
  const readme = fs.readFileSync('README.md', 'utf8');
  assert.ok(
    !readme.includes('The skill returns safe JSON'),
    'README.md: must not say "The skill returns safe JSON"'
  );
  assert.ok(
    !readme.includes('returns safe JSON containing'),
    'README.md: must not say "returns safe JSON containing"'
  );
  console.log('  PASS  README.md: no JSON-first default output wording');
}

// ── package.json: version is 1.9.0 ───────────────────────────────────────────

{
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  assert.ok(
    pkg.version === '1.9.5' || pkg.version === '1.9.4',
    `package.json: version must be 1.9.5 (or 1.9.4), got ${pkg.version}`
  );
  console.log(`  PASS  package.json: version is ${pkg.version}`);
}

// ── SKILL.md: version is 1.9.0 ───────────────────────────────────────────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  assert.ok(
    skill.includes('version: "1.9.5"') || skill.includes('version: "1.9.4"'),
    'SKILL.md: version must be 1.9.5 (or 1.9.4)'
  );
  const skillVer = skill.match(/version: "([^"]+)"/)?.[1] ?? 'unknown';
  console.log(`  PASS  SKILL.md: version is ${skillVer}`);
}

// ── SKILL.md: local payload handoff commands present in runtime section ────────

{
  const skill = fs.readFileSync('SKILL.md', 'utf8');
  const runtimeIdx = skill.indexOf('## Agent Runtime Instructions');
  const runtimeSection = skill.slice(runtimeIdx);

  assert.ok(
    runtimeSection.includes('guard:gmail -- --input'),
    'SKILL.md runtime: must include guard:gmail local payload handoff command'
  );
  assert.ok(
    runtimeSection.includes('guard:calendar -- --input'),
    'SKILL.md runtime: must include guard:calendar local payload handoff command'
  );
  assert.ok(
    runtimeSection.includes('guard:slack -- --input'),
    'SKILL.md runtime: must include guard:slack local payload handoff command'
  );
  assert.ok(
    runtimeSection.includes('guard:github -- --input'),
    'SKILL.md runtime: must include guard:github local payload handoff command'
  );
  console.log('  PASS  SKILL.md: guard:gmail/calendar/slack/github local payload commands present');
}

console.log('\nv182PublicListing: all assertions passed\n');
