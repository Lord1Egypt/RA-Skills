import assert from 'node:assert/strict';
import test from 'node:test';
import { listThetaRuntimeCommands } from '../../dist/index.js';

// Offline: asserts the command inventory only; no network.
test('no wallet, rewards or chain commands are exposed by the cloud runtime', () => {
  assert.equal(listThetaRuntimeCommands().some(c=>/wallet|reward|rpc/i.test(c)),false);
});
