const assert = require('node:assert');

const { adjudicateSeverity } = require('../dist/policy/severityPolicy');

const low = adjudicateSeverity('low');
assert.strictEqual(low.severity, 'low');
assert.strictEqual(low.action, 'track');
assert.strictEqual(low.approvalRequired, false);
assert.strictEqual(low.shouldEscalate, false);
assert.strictEqual(low.safety.externalWrite, false);

const medium = adjudicateSeverity('medium');
assert.strictEqual(medium.severity, 'medium');
assert.strictEqual(medium.action, 'propose');
assert.strictEqual(medium.approvalRequired, false);
assert.strictEqual(medium.shouldEscalate, false);
assert.strictEqual(medium.safety.externalWrite, false);

const high = adjudicateSeverity('high');
assert.strictEqual(high.severity, 'high');
assert.strictEqual(high.action, 'require_approval');
assert.strictEqual(high.approvalRequired, true);
assert.strictEqual(high.shouldEscalate, false);
assert.strictEqual(high.safety.externalWrite, false);

const critical = adjudicateSeverity('critical');
assert.strictEqual(critical.severity, 'critical');
assert.strictEqual(critical.action, 'escalate');
assert.strictEqual(critical.approvalRequired, true);
assert.strictEqual(critical.shouldEscalate, true);
assert.strictEqual(critical.safety.externalWrite, false);

const fallback = adjudicateSeverity(undefined);
assert.strictEqual(fallback.severity, 'medium');
assert.strictEqual(fallback.action, 'propose');

console.log('severityPolicy tests passed');
