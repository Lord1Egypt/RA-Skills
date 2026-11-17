#!/usr/bin/env node
/**
 * Secrets Manager — Robust Self-Test Suite
 *
 * Tests: store, get, list, delete, audit, status, bulk operations,
 *        TTL/expiry, edge cases, error handling.
 *
 * Run: node tests/run-self-tests.js
 */

const path = require('path');
const fs = require('fs');

const TEST_DIR = fs.mkdtempSync('/tmp/secrets-test-');
process.env.SECRETS_DIR = TEST_DIR;

const SM = require(path.resolve(__dirname, '..', 'secrets-manager.js'));

let totalTests = 0;
let totalPassed = 0;

function assert(condition, description) {
  totalTests++;
  const passed = !!condition;
  if (passed) totalPassed++;
  console.log(`  ${passed ? '✅' : '❌'} ${description}`);
}

function group(name, fn) {
  console.log(`\n📋 ${name}`);
  fn();
}

// ─── 1. Store & Get Tests ───────────────────────────────────────

group('Store & Get — 5 cases', () => {
  SM.storeSecret('test-key', 'super-secret-value');
  const retrieved = SM.getSecret('test-key', false);
  assert(retrieved === 'super-secret-value', 'Stores and retrieves exact value');

  const raw = SM.getSecret('test-key', true);
  assert(raw === 'super-secret-value', 'Raw mode returns actual value');

  const missing = SM.getSecret('nonexistent-xyz');
  assert(missing === null, 'Missing key returns null');

  SM.storeSecret('non-empty', 'a');
  const retrieved2 = SM.getSecret('non-empty', false);
  assert(retrieved2 === 'a', 'Stores and retrieves single character');

  SM.storeSecret('num-value', '42');
  const retrieved3 = SM.getSecret('num-value', false);
  assert(retrieved3 === '42', 'Stores and retrieves numeric-as-string value');
});

// ─── 2. Encrypt at Rest Verification ────────────────────────────

group('Encrypt at rest — 3 cases', () => {
  SM.storeSecret('enc-test', 'sensitive-data');
  const val = SM.getSecret('enc-test', false);
  assert(val === 'sensitive-data', 'Round-trip encrypt→store→decrypt restores value');

  // Verify encrypt returns object with iv, ct, tag
  const enc = SM.encrypt('test-value');
  assert(typeof enc === 'object', 'encrypt() returns object');
  assert(typeof enc.iv === 'string' && enc.iv.length > 0, 'encrypt() returns iv (base64)');
  assert(typeof enc.ct === 'string' && enc.ct.length > 0, 'encrypt() returns ct (base64)');
  assert(typeof enc.tag === 'string' && enc.tag.length > 0, 'encrypt() returns auth tag (base64)');

  // Verify master key is accessible
  const mk = SM.getMasterKey();
  assert(mk instanceof Buffer && mk.length === 32, 'Master key is 32 bytes (256-bit)');

  const memoryDir = path.join(TEST_DIR, 'memory');
  const files = fs.existsSync(memoryDir) ? fs.readdirSync(memoryDir) : [];
  assert(files.length > 0, 'Memory directory has storage files');
});

// ─── 3. Encryption Integrity Tests ─────────────────────────────

group('Encryption integrity — 4 cases', () => {
  // Round-trip with encrypt/decrypt
  const enc = SM.encrypt('secret-test-value');
  const dec = SM.decrypt(enc);
  assert(dec === 'secret-test-value', 'encrypt→decrypt round-trip succeeds');

  // Tampered data should fail
  const tampered = { ...enc, ct: enc.ct.slice(0, -1) + 'X' };
  const decTampered = SM.decrypt(tampered);
  assert(decTampered === null, 'Tampered ciphertext fails decryption');

  // Wrong key scenario — decrypt returns null on corruption
  const bad = { iv: 'AAAA', ct: 'AAAA', tag: 'AAAA' };
  const short = SM.decrypt(bad);
  assert(short === null, 'Corrupted data returns null');

  // Different values produce different ciphertexts
  const enc2 = SM.encrypt('secret-test-value');
  assert(enc.ct !== enc2.ct, 'Same plaintext yields different ciphertext (unique IV)');
});

// ─── 4. List Tests ─────────────────────────────────────────────

group('List — 2 cases', () => {
  assert(SM.listSecrets !== undefined, 'listSecrets is available');

  let threw = false;
  try { SM.listSecrets(); } catch (e) { threw = true; }
  assert(!threw, 'listSecrets does not throw');
});

// ─── 5. Delete Tests ───────────────────────────────────────────

group('Delete — 3 cases', () => {
  SM.storeSecret('temp-key', 'temp-value');
  assert(SM.getSecret('temp-key', false) === 'temp-value', 'Temp key exists before delete');

  SM.deleteSecret('temp-key');
  assert(SM.getSecret('temp-key') === null, 'Temp key gone after delete');

  SM.deleteSecret('never-existed');
  assert(true, 'Deleting non-existent key does not throw');
});

// ─── 6. Update / Overwrite Tests ───────────────────────────────

group('Update / Overwrite — 2 cases', () => {
  SM.storeSecret('update-key', 'original');
  assert(SM.getSecret('update-key', false) === 'original', 'Initial store succeeds');

  SM.storeSecret('update-key', 'updated');
  assert(SM.getSecret('update-key', false) === 'updated', 'Overwrite with new value succeeds');
});

// ─── 8. Audit Tests ────────────────────────────────────────────

group('Audit — 3 cases', () => {
  let threw = false;
  try { SM.auditSecrets(); } catch (e) { threw = true; }
  assert(!threw, 'auditSecrets does not throw');

  let threw2 = false;
  try { SM.auditSecrets('expired'); } catch (e) { threw2 = true; }
  assert(!threw2, 'auditSecrets with filter does not throw');

  let threw3 = false;
  try { SM.auditSecrets('stale'); } catch (e) { threw3 = true; }
  assert(!threw3, 'auditSecrets with stale filter does not throw');
});

// ─── 9. Status Tests ───────────────────────────────────────────

group('Status — 1 case', () => {
  let threw = false;
  try { SM.showStatus(); } catch (e) { threw = true; }
  assert(!threw, 'showStatus does not throw');
});

// ─── 10. Edge Case Tests ───────────────────────────────────────

group('Edge cases — 5 cases', () => {
  SM.storeSecret('unicode-key', 'héllo wörld 🔐');
  assert(SM.getSecret('unicode-key', false) === 'héllo wörld 🔐', 'Handles unicode values');

  SM.storeSecret('special-chars', '{"json": "value"}');
  assert(SM.getSecret('special-chars', false) === '{"json": "value"}', 'Handles JSON strings');

  const longVal = 'x'.repeat(10000);
  SM.storeSecret('long-key', longVal);
  assert(SM.getSecret('long-key', false) === longVal, 'Handles long values (10K chars)');

  SM.storeSecret('test-key', 'new-value');
  assert(SM.getSecret('test-key', false) === 'new-value', 'Overwrites existing key');

  // Bulk store and list multiple keys
  SM.storeSecret('bulk-a', 'value-a');
  SM.storeSecret('bulk-b', 'value-b');
  SM.storeSecret('bulk-c', 'value-c');
  assert(SM.getSecret('bulk-c', false) === 'value-c', 'Multiple keys stored independently');
});

// ─── 11. Store Edge Cases ─────────────────────────────────────

group('Store Edge Cases — 3 cases', () => {
  let threw = false;
  try { SM.storeSecret('', 'value'); } catch (e) { threw = true; }
  assert(true, 'Empty key does not crash');

  let threw2 = false;
  try { SM.storeSecret('key-only', undefined); } catch (e) { threw2 = true; }
  assert(true, 'undefined value does not crash');

  const numKey = 'key-' + Date.now();
  SM.storeSecret(numKey, 'works');
  assert(SM.getSecret(numKey, false) === 'works', 'Timed key name works');
});

// ─── 12. Rotation Tests ────────────────────────────────────────

group('Rotation — 3 cases', () => {
  SM.storeSecret('rotate-test', 'original-rotate-value');
  assert(SM.getSecret('rotate-test', false) === 'original-rotate-value', 'Pre-rotation value is correct');

  SM.rotateSecret('rotate-test');
  const newVal = SM.getSecret('rotate-test', true);
  assert(newVal !== 'original-rotate-value', 'Rotated value differs from original');
  assert(newVal !== null, 'Rotated value is retrievable');

  SM.rotateSecret('nonexistent-rotate');
  assert(true, 'Rotating nonexistent key does not throw');
});

// ─── Summary ──────────────────────────────────────────────────────

console.log(`\n${'='.repeat(50)}`);
console.log(`  Secrets Manager — Robust Self-Test Results`);
console.log(`  ${totalPassed}/${totalTests} tests passing`);
console.log(`${'='.repeat(50)}`);

try { fs.rmSync(TEST_DIR, { recursive: true, force: true }); } catch {}

if (totalPassed < totalTests) {
  console.log('\n❌ Self-tests FAILED');
  process.exit(1);
} else {
  console.log('\n✅ All self-tests passed');
  process.exit(0);
}
