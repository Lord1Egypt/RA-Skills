/**
 * WebSocket Reconnect Skill - Test Suite
 */

const { WebSocketReconnect } = require('../scripts/websocket-reconnect.js');

// Test results tracking
let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(`   Error: ${error.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed');
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}

console.log('🧪 WebSocket Reconnect Test Suite\n');

// Test 1: Constructor with default options
test('Constructor with default options', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  assertEqual(ws.maxRetries, 10, 'maxRetries should be 10');
  assertEqual(ws.baseDelay, 1000, 'baseDelay should be 1000');
  assertEqual(ws.maxDelay, 30000, 'maxDelay should be 30000');
  assertEqual(ws.multiplier, 2, 'multiplier should be 2');
  assertEqual(ws.jitter, 0.1, 'jitter should be 0.1');
  assertEqual(ws.state, 'CLOSED', 'initial state should be CLOSED');
  assertEqual(ws.circuitState, 'CLOSED', 'initial circuit state should be CLOSED');
});

// Test 2: Constructor with custom options
test('Constructor with custom options', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    maxRetries: 5,
    baseDelay: 500,
    maxDelay: 10000,
    multiplier: 1.5,
    jitter: 0.2
  });
  assertEqual(ws.maxRetries, 5, 'maxRetries should be 5');
  assertEqual(ws.baseDelay, 500, 'baseDelay should be 500');
  assertEqual(ws.maxDelay, 10000, 'maxDelay should be 10000');
  assertEqual(ws.multiplier, 1.5, 'multiplier should be 1.5');
  assertEqual(ws.jitter, 0.2, 'jitter should be 0.2');
});

// Test 3: Exponential backoff calculation without jitter
test('Exponential backoff calculation without jitter', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    baseDelay: 1000,
    multiplier: 2,
    jitter: 0,
    maxDelay: 30000
  });
  
  assertEqual(ws.calculateDelay(0), 1000, 'attempt 0 should be 1000ms');
  assertEqual(ws.calculateDelay(1), 2000, 'attempt 1 should be 2000ms');
  assertEqual(ws.calculateDelay(2), 4000, 'attempt 2 should be 4000ms');
  assertEqual(ws.calculateDelay(3), 8000, 'attempt 3 should be 8000ms');
  assertEqual(ws.calculateDelay(4), 16000, 'attempt 4 should be 16000ms');
  assertEqual(ws.calculateDelay(5), 30000, 'attempt 5 should be capped at 30000ms');
});

// Test 4: Exponential backoff with max delay cap
test('Exponential backoff with max delay cap', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    baseDelay: 1000,
    multiplier: 2,
    jitter: 0,
    maxDelay: 5000
  });
  
  assertEqual(ws.calculateDelay(0), 1000, 'attempt 0 should be 1000ms');
  assertEqual(ws.calculateDelay(1), 2000, 'attempt 1 should be 2000ms');
  assertEqual(ws.calculateDelay(2), 4000, 'attempt 2 should be 4000ms');
  assertEqual(ws.calculateDelay(3), 5000, 'attempt 3 should be capped at 5000ms');
  assertEqual(ws.calculateDelay(10), 5000, 'attempt 10 should be capped at 5000ms');
});

// Test 5: Jitter adds randomness
test('Jitter adds randomness', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    baseDelay: 1000,
    multiplier: 1,
    jitter: 0.1
  });
  
  const delays = [];
  for (let i = 0; i < 10; i++) {
    delays.push(ws.calculateDelay(0));
  }
  
  // With 10% jitter on 1000ms, delays should be between 900-1100ms
  const allInRange = delays.every(d => d >= 900 && d <= 1100);
  assert(allInRange, 'All delays should be within jitter range');
  
  // Should have some variation
  const uniqueDelays = new Set(delays);
  assert(uniqueDelays.size > 1, 'Jitter should create variation in delays');
});

// Test 6: Event registration and emission
test('Event registration and emission', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  let eventFired = false;
  let eventData = null;
  
  ws.on('custom', (data) => {
    eventFired = true;
    eventData = data;
  });
  
  ws.emit('custom', { test: 'value' });
  
  assert(eventFired, 'Event handler should be called');
  assertEqual(eventData.test, 'value', 'Event data should match');
});

// Test 7: Multiple event handlers
test('Multiple event handlers', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  let count = 0;
  
  ws.on('test', () => count++);
  ws.on('test', () => count++);
  ws.on('test', () => count++);
  
  ws.emit('test');
  
  assertEqual(count, 3, 'All handlers should be called');
});

// Test 8: Event handler removal
test('Event handler removal', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  let count = 0;
  
  const handler = () => count++;
  ws.on('test', handler);
  ws.on('test', () => count++);
  
  ws.off('test', handler);
  ws.emit('test');
  
  assertEqual(count, 1, 'Removed handler should not be called');
});

// Test 9: Get stats
test('Get stats', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    maxRetries: 10
  });
  
  const stats = ws.getStats();
  
  assertEqual(stats.state, 'CLOSED', 'state should be CLOSED');
  assertEqual(stats.circuitState, 'CLOSED', 'circuitState should be CLOSED');
  assertEqual(stats.retryCount, 0, 'retryCount should be 0');
  assertEqual(stats.maxRetries, 10, 'maxRetries should be 10');
  assert(typeof stats.lastActivity === 'number', 'lastActivity should be a number');
});

// Test 10: Circuit breaker state transitions
test('Circuit breaker state transitions', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    circuitBreaker: {
      failureThreshold: 3,
      resetTimeout: 100
    }
  });
  
  assertEqual(ws.getCircuitState(), 'CLOSED', 'Initial state should be CLOSED');
  
  // Simulate failures
  ws.circuitFailures = 3;
  ws.openCircuit();
  
  assertEqual(ws.getCircuitState(), 'OPEN', 'State should be OPEN after failures');
  
  // Wait for reset timeout
  setTimeout(() => {
    // State should transition to HALF-OPEN automatically
    // Note: This is async, so we can't test it synchronously
  }, 150);
});

// Test 11: Manual circuit breaker control
test('Manual circuit breaker control', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  
  ws.openCircuit();
  assertEqual(ws.getCircuitState(), 'OPEN', 'Should be OPEN after openCircuit()');
  
  ws.closeCircuit();
  assertEqual(ws.getCircuitState(), 'CLOSED', 'Should be CLOSED after closeCircuit()');
  assertEqual(ws.circuitFailures, 0, 'circuitFailures should be reset');
});

// Test 12: Reset connection state
test('Reset connection state', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  
  ws.retryCount = 5;
  ws.circuitFailures = 3;
  ws.manualClose = true;
  ws.openCircuit();
  
  ws.reset();
  
  assertEqual(ws.retryCount, 0, 'retryCount should be reset');
  assertEqual(ws.circuitFailures, 0, 'circuitFailures should be reset');
  assertEqual(ws.manualClose, false, 'manualClose should be reset');
  assertEqual(ws.getCircuitState(), 'CLOSED', 'circuit should be CLOSED');
});

// Test 13: Close connection
test('Close connection', () => {
  const ws = new WebSocketReconnect({ url: 'ws://localhost:8080' });
  let closeEventFired = false;
  
  ws.on('stateChange', (state) => {
    if (state === 'CLOSED') {
      closeEventFired = true;
    }
  });
  
  ws.manualClose = true; // Prevent reconnect attempts
  ws.close();
  
  assertEqual(ws.state, 'CLOSED', 'State should be CLOSED');
  assert(closeEventFired, 'CLOSED state change event should fire');
});

// Test 14: Heartbeat configuration
test('Heartbeat configuration', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    heartbeatInterval: 15000,
    heartbeatTimeout: 3000,
    heartbeatMessage: JSON.stringify({ type: 'custom_ping' })
  });
  
  assertEqual(ws.heartbeatInterval, 15000, 'heartbeatInterval should be 15000');
  assertEqual(ws.heartbeatTimeout, 3000, 'heartbeatTimeout should be 3000');
  assertEqual(ws.heartbeatMessage, '{"type":"custom_ping"}', 'heartbeatMessage should match');
});

// Test 15: Error handling
test('Error handling', () => {
  const ws = new WebSocketReconnect({
    url: 'ws://localhost:8080',
    circuitBreaker: { failureThreshold: 2 }
  });
  
  let errorCount = 0;
  ws.on('error', () => errorCount++);
  
  // Simulate errors
  ws.handleError(new Error('Test error 1'));
  ws.handleError(new Error('Test error 2'));
  
  assertEqual(errorCount, 2, 'Error handler should be called twice');
  assertEqual(ws.circuitFailures, 2, 'circuitFailures should be 2');
  assertEqual(ws.getCircuitState(), 'OPEN', 'Circuit should be OPEN after threshold');
});

// Summary
console.log('\n' + '='.repeat(50));
console.log(`Tests passed: ${passed}`);
console.log(`Tests failed: ${failed}`);
console.log(`Total: ${passed + failed}`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
} else {
  console.log('\n✅ All tests passed!');
  process.exit(0);
}
