const assert = require('node:assert');

const { getCapabilityBoundary } = require('../dist/policy/capabilityBoundary');

const boundary = getCapabilityBoundary();

assert.strictEqual(boundary.externalWrite, false);
assert.strictEqual(boundary.mode, 'safe_by_default');

assert.ok(boundary.allowed.length > 0, 'allowed capabilities are defined');
assert.ok(boundary.denied.length > 0, 'denied capabilities are defined');

const allowedNames = boundary.allowed.map((capability) => capability.name);
const deniedNames = boundary.denied.map((capability) => capability.name);

assert.ok(allowedNames.includes('readSignals'), 'readSignals is allowed');
assert.ok(allowedNames.includes('persistLocalOpenLoopState'), 'persistLocalOpenLoopState is allowed');
assert.ok(allowedNames.includes('transitionLocalOpenLoopState'), 'transitionLocalOpenLoopState is allowed');

assert.ok(deniedNames.includes('sendEmail'), 'sendEmail is denied');
assert.ok(deniedNames.includes('sendSlackMessage'), 'sendSlackMessage is denied');
assert.ok(deniedNames.includes('createCalendarEvent'), 'createCalendarEvent is denied');
assert.ok(deniedNames.includes('writeExternalSystem'), 'writeExternalSystem is denied');

assert.ok(
  boundary.denied.every((capability) => capability.allowed === false),
  'all denied capabilities have allowed=false'
);

assert.ok(
  boundary.denied.every((capability) => capability.boundary === 'external_write'),
  'all denied capabilities cross external_write boundary'
);

console.log('capabilityBoundary tests passed');
