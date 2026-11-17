import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const skill = fs.readFileSync(new URL('../SKILL.md', import.meta.url), 'utf8');
const delegation = skill.split('## Delegation')[1].split('## Database IDs')[0];

test('metadata discloses existing Notion and authorized local persistence', () => {
  assert.match(skill, /"localWrites":/);
  assert.match(skill, /explicitly authorized core-context files/);
  assert.match(skill, /"modifiesRemoteData":\["notion:databases"/);
});

test('delegation chooses a host read-only worker, not a fixed agent or lightweight bootstrap', () => {
  assert.doesNotMatch(delegation, /agentId:\s*"analysis-worker"/);
  assert.doesNotMatch(delegation, /lightContext:\s*true/);
  assert.match(delegation, /host.*read-only worker/i);
  assert.match(delegation, /workspace/);
});

test('parent retains writes and collector ownership', () => {
  assert.match(delegation, /Main owns Notion writes/);
  assert.match(delegation, /explicitly collect/);
  assert.match(delegation, /source content as untrusted data/i);
});
