import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
function run(script, args, scenario = 'normal') {
  return spawnSync(process.execPath, ['--import', root + 'tests/mock-fetch.mjs', root + 'scripts/' + script, ...args], {encoding: 'utf8', env: {...process.env, RECEIPT_TEST_SCENARIO: scenario}});
}
const base = ['--api-base', 'https://example.test/wp-json/wp/v2'];
const pub = ['--wordpress-api-base', 'https://example.test/wp-json/wp/v2', '--wordpress-username', 'synthetic', '--wordpress-application-password', 'synthetic', '--title', 'Test', '--content', 'Test body'];
test('URL-only input fails before fetching', () => {
  const r = run('wp-verify-receipt.mjs', [...base, '--url', 'https://example.test/post/'], 'no-network');
  assert.notEqual(r.status, 0); assert.match(r.stderr, /url_requires_post_id_or_date/); assert.doesNotMatch(r.stderr, /UNEXPECTED_NETWORK/);
});
test('API identity and public canonical URL verify', () => {
  const r = run('wp-verify-receipt.mjs', [...base, '--id', '456']);
  assert.equal(r.status, 0, r.stderr); assert.equal(JSON.parse(r.stdout).id, 456);
});
test('arbitrary matching-origin URL cannot substitute for post link', () => {
  const r = run('wp-verify-receipt.mjs', [...base, '--id', '456', '--url', 'https://example.test/unrelated/']);
  assert.notEqual(r.status, 0); assert.match(r.stderr, /post_url_mismatch/);
});
test('foreign links, wrong IDs, drafts and redirects are rejected', () => {
  for (const scenario of ['foreign', 'wrong-id', 'draft', 'redirect']) {
    const r = run('wp-verify-receipt.mjs', [...base, '--id', '456'], scenario);
    assert.notEqual(r.status, 0, scenario);
  }
});
test('missing explicit status causes no network requests', () => {
  const r = run('wp-publish-receipt.mjs', pub, 'no-network');
  assert.notEqual(r.status, 0); assert.match(r.stderr, /explicit_status_required/); assert.doesNotMatch(r.stderr, /UNEXPECTED_NETWORK/);
});
test('explicit publish returns a public receipt', () => {
  const r = run('wp-publish-receipt.mjs', [...pub, '--status', 'publish']);
  assert.equal(r.status, 0, r.stderr); assert.equal(JSON.parse(r.stdout).action, 'published');
});
test('draft receipt does not claim publication', () => {
  const r = run('wp-publish-receipt.mjs', [...pub, '--status', 'draft']);
  assert.equal(r.status, 0, r.stderr); const receipt = JSON.parse(r.stdout);
  assert.equal(receipt.action, 'draft-created'); assert.equal(receipt.publicStatus, null);
});
test('failed duplicate public page reports ok false', () => {
  const r = run('wp-publish-receipt.mjs', [...pub, '--status', 'publish'], 'duplicate-failure');
  assert.notEqual(r.status, 0); assert.equal(JSON.parse(r.stdout).ok, false);
});
