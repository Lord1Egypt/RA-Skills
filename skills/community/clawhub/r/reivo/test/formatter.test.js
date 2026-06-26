/**
 * OpenClaw skill audit tests — formatter.js
 */
const { formatStatus, formatMonthly } = require('../lib/formatter.js');

function assert(condition, message) {
  if (!condition) throw new Error(`FAIL: ${message}`);
}

function assertIncludes(str, substr, message) {
  if (!str.includes(substr)) throw new Error(`FAIL: ${message} — "${substr}" not found in output`);
}

function test(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
  } catch (e) {
    console.error(`  ✗ ${name}: ${e.message}`);
    process.exitCode = 1;
  }
}

console.log('formatter.js tests');

test('formatStatus includes all fields', () => {
  const result = formatStatus({ requests: 42, totalCost: 1.5, savedToday: 0.75 });
  assertIncludes(result, 'Reivo Daily Report', 'header');
  assertIncludes(result, '42', 'requests');
  assertIncludes(result, '$1.50', 'totalCost');
  assertIncludes(result, '$0.75', 'savedToday');
});

test('formatStatus with zero values', () => {
  const result = formatStatus({ requests: 0, totalCost: 0, savedToday: 0 });
  assertIncludes(result, '$0.00', 'zero cost');
  assertIncludes(result, '0', 'zero requests');
});

test('formatStatus with large numbers', () => {
  const result = formatStatus({ requests: 100000, totalCost: 9999.99, savedToday: 5000.50 });
  assertIncludes(result, '100000', 'large requests');
  assertIncludes(result, '$9999.99', 'large cost');
});

test('formatStatus with floating point precision', () => {
  const result = formatStatus({ requests: 1, totalCost: 0.1 + 0.2, savedToday: 0 });
  // 0.1 + 0.2 = 0.30000000000000004, but toFixed(2) should round
  assertIncludes(result, '$0.30', 'float rounding');
});

test('formatMonthly includes all fields', () => {
  const result = formatMonthly({ month: 'March 2026', totalRequests: 1000, totalCost: 50.0, saved: 25.0 });
  assertIncludes(result, 'March 2026', 'month');
  assertIncludes(result, '1000', 'totalRequests');
  assertIncludes(result, '$50.00', 'totalCost');
  assertIncludes(result, '$25.00', 'saved');
});

test('formatMonthly with zero saved', () => {
  const result = formatMonthly({ month: 'Jan', totalRequests: 5, totalCost: 1.23, saved: 0 });
  assertIncludes(result, '$0.00', 'zero saved');
});

test('formatStatus returns string with newlines', () => {
  const result = formatStatus({ requests: 1, totalCost: 1, savedToday: 0 });
  assert(typeof result === 'string', 'should be string');
  assert(result.includes('\n'), 'should contain newlines');
});

test('formatMonthly returns string with newlines', () => {
  const result = formatMonthly({ month: 'Jan', totalRequests: 1, totalCost: 1, saved: 0 });
  assert(typeof result === 'string', 'should be string');
  assert(result.includes('\n'), 'should contain newlines');
});

console.log('');
