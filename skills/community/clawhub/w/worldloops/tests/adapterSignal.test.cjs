const assert = require('node:assert');

const { validateAdapterSignal } = require('../dist/adapter/validateAdapterSignal');
const { toWorldLoopsSignal } = require('../dist/adapter/toWorldLoopsSignal');

const validInput = {
  source: 'slack',
  sourceType: 'message',
  externalWrite: false,
  text: 'Hey, can you review the Q2 metrics dashboard before the meeting tomorrow?',
  observedAt: '2026-05-19T10:30:00.000Z',
  url: 'https://example.slack.com/archives/C01/p123',
  summary: 'Review request for Q2 metrics dashboard',
};

// valid signal passes
const result = validateAdapterSignal(validInput);
assert.strictEqual(result.ok, true);
assert.strictEqual(result.signal.source, 'slack');
assert.strictEqual(result.signal.sourceType, 'message');
assert.strictEqual(result.signal.externalWrite, false);
assert.strictEqual(result.signal.text, validInput.text);
assert.strictEqual(result.signal.observedAt, validInput.observedAt);
assert.strictEqual(result.signal.url, validInput.url);
assert.strictEqual(result.signal.summary, validInput.summary);

// bridge: known source maps directly
const signal = toWorldLoopsSignal(result.signal);
assert.strictEqual(signal.source, 'slack');
assert.strictEqual(signal.text, validInput.text);
assert.strictEqual(signal.createdAt, validInput.observedAt);
assert.strictEqual(signal.url, validInput.url);

// bridge: unknown source falls back to 'manual'
const linearResult = validateAdapterSignal({ ...validInput, source: 'linear' });
assert.strictEqual(linearResult.ok, true);
const linearSignal = toWorldLoopsSignal(linearResult.signal);
assert.strictEqual(linearSignal.source, 'manual');

// bridge: all known sources pass through
for (const src of ['slack', 'gmail', 'calendar', 'github', 'manual']) {
  const r = validateAdapterSignal({ ...validInput, source: src });
  assert.strictEqual(r.ok, true);
  const s = toWorldLoopsSignal(r.signal);
  assert.strictEqual(s.source, src);
}

// optional fields are optional
const minimalResult = validateAdapterSignal({
  source: 'github',
  sourceType: 'pr',
  externalWrite: false,
  text: 'PR #42 awaiting review',
  observedAt: '2026-05-19T12:00:00.000Z',
});
assert.strictEqual(minimalResult.ok, true);
assert.strictEqual(minimalResult.signal.url, undefined);
assert.strictEqual(minimalResult.signal.summary, undefined);
assert.strictEqual(minimalResult.signal.metadata, undefined);

// bridge: optional url absent in signal when not in adapter
const minimalSignal = toWorldLoopsSignal(minimalResult.signal);
assert.strictEqual(minimalSignal.url, undefined);

// metadata field is preserved on adapter signal
const withMeta = validateAdapterSignal({
  ...validInput,
  metadata: { prNumber: 487, repo: 'example-org/api' },
});
assert.strictEqual(withMeta.ok, true);
assert.deepStrictEqual(withMeta.signal.metadata, { prNumber: 487, repo: 'example-org/api' });

// not an object
assert.strictEqual(validateAdapterSignal('a string').ok, false);
assert.strictEqual(validateAdapterSignal(null).ok, false);
assert.strictEqual(validateAdapterSignal(42).ok, false);
assert.strictEqual(validateAdapterSignal([]).ok, false);

// missing required fields
const missing = validateAdapterSignal({});
assert.strictEqual(missing.ok, false);
assert.ok(missing.errors.length >= 5, 'all required fields should fail');

// externalWrite: true is rejected
const writeTrue = validateAdapterSignal({ ...validInput, externalWrite: true });
assert.strictEqual(writeTrue.ok, false);
assert.ok(writeTrue.errors.some((e) => e.includes('externalWrite')));

// externalWrite: missing is rejected
const writeMissing = validateAdapterSignal({ ...validInput, externalWrite: undefined });
assert.strictEqual(writeMissing.ok, false);
assert.ok(writeMissing.errors.some((e) => e.includes('externalWrite')));

// invalid observedAt
const badDate = validateAdapterSignal({ ...validInput, observedAt: 'not-a-date' });
assert.strictEqual(badDate.ok, false);
assert.ok(badDate.errors.some((e) => e.includes('observedAt')));

// observedAt missing
const noDate = validateAdapterSignal({ ...validInput, observedAt: undefined });
assert.strictEqual(noDate.ok, false);
assert.ok(noDate.errors.some((e) => e.includes('observedAt')));

// empty text
const emptyText = validateAdapterSignal({ ...validInput, text: '' });
assert.strictEqual(emptyText.ok, false);
assert.ok(emptyText.errors.some((e) => e.includes('text')));

// empty source
const emptySource = validateAdapterSignal({ ...validInput, source: '' });
assert.strictEqual(emptySource.ok, false);
assert.ok(emptySource.errors.some((e) => e.includes('source')));

// metadata: non-object is rejected
const badMeta = validateAdapterSignal({ ...validInput, metadata: 'not-an-object' });
assert.strictEqual(badMeta.ok, false);
assert.ok(badMeta.errors.some((e) => e.includes('metadata')));

console.log('adapterSignal tests passed');
