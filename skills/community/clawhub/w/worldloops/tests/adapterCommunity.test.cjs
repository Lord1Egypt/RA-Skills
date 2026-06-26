const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');

const { validateAdapterSignal } = require('../dist/adapter/validateAdapterSignal');

const root = path.resolve(__dirname, '..');
const communityDir = path.join(root, 'examples/adapters/community');

const files = fs.readdirSync(communityDir).filter((f) => f.endsWith('.example.json'));

assert.ok(files.length > 0, 'expected at least one community adapter example fixture in examples/adapters/community/');

for (const file of files) {
  const raw = fs.readFileSync(path.join(communityDir, file), 'utf8');
  const input = JSON.parse(raw);
  const result = validateAdapterSignal(input);

  assert.strictEqual(
    result.ok,
    true,
    `community adapter ${file}: expected ok: true, got errors: ${result.ok ? '[]' : JSON.stringify(result.errors)}`
  );
  assert.strictEqual(result.signal.externalWrite, false, `${file}: externalWrite must be false`);
  assert.ok(
    typeof result.signal.source === 'string' && result.signal.source.length > 0,
    `${file}: source must be a non-empty string`
  );
  assert.ok(
    typeof result.signal.sourceType === 'string' && result.signal.sourceType.length > 0,
    `${file}: sourceType must be a non-empty string`
  );
  assert.ok(
    typeof result.signal.text === 'string' && result.signal.text.length > 0,
    `${file}: text must be a non-empty string`
  );
  assert.ok(typeof result.signal.observedAt === 'string', `${file}: observedAt must be a string`);
}

console.log(
  `adapterCommunity tests passed (${files.length} community fixture${files.length === 1 ? '' : 's'} validated)`
);
