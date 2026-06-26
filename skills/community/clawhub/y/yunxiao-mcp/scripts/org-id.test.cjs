const test = require('node:test');
const assert = require('node:assert/strict');

const { resolveOrgId } = require('./org-id.cjs');

test('prefers explicit organization ID', () => {
  const result = resolveOrgId({
    explicitOrgId: 'explicit-org',
    envOrgId: 'env-org',
    organizations: [{ id: 'detected-org' }]
  });

  assert.equal(result, 'explicit-org');
});

test('falls back to environment organization ID', () => {
  const result = resolveOrgId({
    explicitOrgId: undefined,
    envOrgId: 'env-org',
    organizations: [{ id: 'detected-org' }]
  });

  assert.equal(result, 'env-org');
});

test('falls back to first detected organization ID', () => {
  const result = resolveOrgId({
    explicitOrgId: undefined,
    envOrgId: undefined,
    organizations: [{ id: 'detected-org' }]
  });

  assert.equal(result, 'detected-org');
});

test('returns null when no organization ID is available', () => {
  const result = resolveOrgId({
    explicitOrgId: undefined,
    envOrgId: undefined,
    organizations: []
  });

  assert.equal(result, null);
});
