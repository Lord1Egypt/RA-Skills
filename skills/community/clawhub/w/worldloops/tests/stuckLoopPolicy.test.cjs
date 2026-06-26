const assert = require('node:assert');

const { evaluateStuckLoop } = require('../dist/policy/stuckLoopPolicy');

function loop(overrides = {}) {
  return {
    id: 'loop-1',
    canonicalKey: 'test:loop',
    title: 'Test loop',
    sourceSignals: [],
    status: 'todo',
    severity: 'medium',
    adjudication: {
      severity: 'medium',
      action: 'propose',
      approvalRequired: false,
      shouldEscalate: false,
      reason: 'test',
      safety: { externalWrite: false },
    },
    owner: null,
    dueAt: null,
    lastObservedAt: '2026-05-18T00:00:00.000Z',
    updatedAt: '2026-05-18T00:00:00.000Z',
    history: [],
    safety: { externalWrite: false },
    ...overrides,
  };
}

const now = '2026-05-20T01:00:00.000Z';

const todoTimeout = evaluateStuckLoop(loop(), now, {
  todoTimeoutHours: 48,
  doingTimeoutHours: 24,
});
assert.strictEqual(todoTimeout.shouldTransition, true);
assert.strictEqual(todoTimeout.from, 'todo');
assert.strictEqual(todoTimeout.to, 'escalated');
assert.strictEqual(todoTimeout.reason, 'todo_timeout');
assert.strictEqual(todoTimeout.safety.externalWrite, false);

const doingTimeout = evaluateStuckLoop(
  loop({ status: 'doing', updatedAt: '2026-05-18T23:00:00.000Z' }),
  now,
  { todoTimeoutHours: 48, doingTimeoutHours: 24 }
);
assert.strictEqual(doingTimeout.shouldTransition, true);
assert.strictEqual(doingTimeout.from, 'doing');
assert.strictEqual(doingTimeout.to, 'escalated');
assert.strictEqual(doingTimeout.reason, 'doing_timeout');

const snoozeExpired = evaluateStuckLoop(
  loop({ status: 'snoozed', dueAt: '2026-05-19T00:00:00.000Z' }),
  now
);
assert.strictEqual(snoozeExpired.shouldTransition, true);
assert.strictEqual(snoozeExpired.from, 'snoozed');
assert.strictEqual(snoozeExpired.to, 'todo');
assert.strictEqual(snoozeExpired.reason, 'snooze_expired');

const highOverdue = evaluateStuckLoop(
  loop({ severity: 'high', dueAt: '2026-05-19T00:00:00.000Z' }),
  now
);
assert.strictEqual(highOverdue.shouldTransition, true);
assert.strictEqual(highOverdue.to, 'escalated');
assert.strictEqual(highOverdue.reason, 'high_or_critical_overdue');

const freshTodo = evaluateStuckLoop(
  loop({ updatedAt: '2026-05-19T23:00:00.000Z' }),
  now,
  { todoTimeoutHours: 48, doingTimeoutHours: 24 }
);
assert.strictEqual(freshTodo.shouldTransition, false);
assert.strictEqual(freshTodo.reason, 'none');

const doneLoop = evaluateStuckLoop(
  loop({ status: 'done', severity: 'critical', dueAt: '2026-05-19T00:00:00.000Z' }),
  now
);
assert.strictEqual(doneLoop.shouldTransition, false);

console.log('stuckLoopPolicy tests passed');
