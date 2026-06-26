const assert = require('node:assert');
const { execFileSync } = require('node:child_process');

const EXPECTED_IDS = [
  'file-write',
  'api-call',
  'state-transition',
  'human-review',
  'notification-draft',
  'escalation',
];

// ── human-readable output ─────────────────────────────────────────────────────

const humanOutput = execFileSync(
  process.execPath,
  ['dist/scripts/proposalTemplates.js'],
  { encoding: 'utf8' }
);

assert.throws(
  () => JSON.parse(humanOutput),
  'default output should not be valid JSON'
);

assert.ok(humanOutput.includes('Proposal Templates'), 'human output should include header');
assert.ok(humanOutput.includes('externalWrite'), 'human output should mention externalWrite');
assert.ok(humanOutput.includes('false'), 'human output should show externalWrite:false');

for (const id of EXPECTED_IDS) {
  assert.ok(humanOutput.includes(id), `human output should include template id: ${id}`);
}

// ── --json output ─────────────────────────────────────────────────────────────

const jsonOutput = execFileSync(
  process.execPath,
  ['dist/scripts/proposalTemplates.js', '--json'],
  { encoding: 'utf8' }
);

const json = JSON.parse(jsonOutput);

assert.strictEqual(json.ok, true);
assert.strictEqual(json.source, 'worldloops.local');
assert.strictEqual(json.count, 6, 'should have 6 templates');
assert.ok(Array.isArray(json.templates), 'templates should be an array');
assert.strictEqual(json.templates.length, 6);
assert.strictEqual(json.safety.externalWrite, false);

// ── all 6 templates present ───────────────────────────────────────────────────

const templateIds = json.templates.map((t) => t.id);
for (const id of EXPECTED_IDS) {
  assert.ok(templateIds.includes(id), `JSON output should include template id: ${id}`);
}

// ── each template has required fields and externalWrite:false ─────────────────

for (const t of json.templates) {
  assert.ok(t.id, `template ${t.id} should have id`);
  assert.ok(t.title, `template ${t.id} should have title`);
  assert.ok(t.description, `template ${t.id} should have description`);
  assert.ok(t.category, `template ${t.id} should have category`);
  assert.ok(t.riskLevel, `template ${t.id} should have riskLevel`);
  assert.strictEqual(t.externalWrite, false, `template ${t.id} externalWrite must be false`);
  assert.strictEqual(t.requiredReview, true, `template ${t.id} requiredReview must be true`);
  assert.ok(Array.isArray(t.suggestedChecks), `template ${t.id} should have suggestedChecks array`);
  assert.ok(Array.isArray(t.exampleUseCases), `template ${t.id} should have exampleUseCases array`);
}

console.log('proposalTemplates tests passed');
