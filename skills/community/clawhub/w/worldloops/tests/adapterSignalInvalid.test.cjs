const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const { validateAdapterSignal } = require('../dist/adapter/validateAdapterSignal');

const root = path.resolve(__dirname, '..');

const cases = [
  {
    file: 'examples/adapters/invalid-external-write.json',
    desc: 'invalid-external-write: externalWrite: true is rejected',
    errorContains: 'externalWrite',
  },
  {
    file: 'examples/adapters/invalid-missing-required-field.json',
    desc: 'invalid-missing-required-field: missing observedAt is rejected',
    errorContains: 'observedAt',
  },
  {
    file: 'examples/adapters/invalid-date.json',
    desc: 'invalid-date: human-readable date string is rejected',
    errorContains: 'observedAt',
  },
];

for (const { file, desc, errorContains } of cases) {
  const raw = fs.readFileSync(path.join(root, file), 'utf8');
  const input = JSON.parse(raw);
  const result = validateAdapterSignal(input);

  assert.strictEqual(result.ok, false, `${desc}: expected ok: false`);
  assert.ok(Array.isArray(result.errors) && result.errors.length > 0, `${desc}: expected non-empty errors array`);

  if (errorContains) {
    assert.ok(
      result.errors.some((e) => e.includes(errorContains)),
      `${desc}: expected an error containing "${errorContains}", got: ${JSON.stringify(result.errors)}`
    );
  }
}

console.log('adapterSignalInvalid tests passed');
