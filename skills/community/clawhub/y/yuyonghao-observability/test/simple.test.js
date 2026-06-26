/**
 * Observability 简单测试
 */

const { ObservabilitySystem } = require('./src/index');

console.log('🧪 Observability 简单测试');
console.log('='.repeat(50));

let passed = 0;
let failed = 0;

async function test(name, fn) {
  process.stdout.write(`${name}... `);
  try {
    await fn();
    console.log('✅');
    passed++;
  } catch (error) {
    console.log(`❌ ${error.message}`);
    failed++;
  }
}

async function runTests() {
  // Test 1: System init
  await test('System init', () => {
    const obs = new ObservabilitySystem({
      logging: { level: 'info', console: false, file: false }
    });
    if (!obs.logger) throw new Error('Logger not created');
    if (!obs.metrics) throw new Error('Metrics not created');
  });

  // Test 2: Logger methods
  await test('Logger methods', () => {
    const obs = new ObservabilitySystem({
      logging: { level: 'debug', console: false }
    });
    obs.logger.info('Test info');
    obs.logger.warn('Test warn');
    obs.logger.error('Test error');
    obs.logger.debug('Test debug');
  });

  // Test 3: Counter
  await test('Counter', () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const counter = obs.metrics.counter('test.counter', 'Test');
    counter.inc();
    counter.inc(5);
    const summary = obs.metrics.getSummary();
    if (summary.totalCalls !== 6) throw new Error('Counter mismatch');
  });

  // Test 4: Gauge
  await test('Gauge', () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const gauge = obs.metrics.gauge('test.gauge', 'Test');
    gauge.set(10);
    const summary = obs.metrics.getSummary();
    if (summary.activeAgents !== 10) throw new Error('Gauge mismatch');
  });

  // Test 5: Histogram
  await test('Histogram', () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const histogram = obs.metrics.histogram('calls.latency', 'Latency');
    histogram.observe(50);
    histogram.observe(150);
    const summary = obs.metrics.getSummary();
    if (summary.avgLatency <= 0) throw new Error('Histogram avg mismatch');
  });

  // Test 6: Trace
  await test('Trace', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const trace = obs.startTrace('test.operation');
    if (!trace.traceId) throw new Error('Trace ID missing');
    const result = trace.end({ result: 'success' });
    if (!result.duration) throw new Error('Duration missing');
  });

  // Test 7: Wrap function
  await test('Wrap function', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const fn = obs.wrap(async (x) => x * 2, 'test.multiply');
    const result = await fn(21);
    if (result !== 42) throw new Error('Function result mismatch');
  });

  // Test 8: Error recording
  await test('Error recording', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    try {
      throw new Error('Test error');
    } catch (error) {
      obs.recordError(error, { test: true });
    }
    const summary = obs.metrics.getSummary();
    if (summary.totalErrors < 1) throw new Error('Error not recorded');
  });

  // Test 9: Export metrics
  await test('Export metrics', () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    obs.metrics.counter('test.counter').inc(5);
    const prometheus = obs.exportMetrics('prometheus');
    if (!prometheus.includes('test.counter')) {
      throw new Error('Prometheus export failed');
    }
  });

  // Test 10: Get status
  await test('Get status', () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const status = obs.getStatus();
    if (status.activeTraces === undefined) throw new Error('activeTraces missing');
    if (!status.metrics) throw new Error('metrics missing');
    if (!status.logDir) throw new Error('logDir missing');
  });

  // Summary
  console.log('='.repeat(50));
  console.log(`Results: ${passed}/${passed + failed} passed`);
  console.log(`Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  if (failed > 0) {
    process.exit(1);
  } else {
    console.log('\n🎉 All tests passed!');
  }
}

runTests();
