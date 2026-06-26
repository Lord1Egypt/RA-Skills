/**
 * Observability 基础测试
 */

const { ObservabilitySystem } = require('./src/index');
const { MetricsCollector } = require('./src/metrics');

console.log('🧪 Observability 测试');
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
  // Test 1: Logger init
  await test('Logger init', async () => {
    const obs = new ObservabilitySystem({
      logging: { level: 'info', console: true, file: false }
    });
    if (!obs.logger) throw new Error('Logger not created');
  });

  // Test 2: Metrics init
  await test('Metrics init', async () => {
    const obs = new ObservabilitySystem({ metrics: { enabled: true } });
    if (!obs.metrics) throw new Error('Metrics not created');
  });

  // Test 3: Counter
  await test('Counter', async () => {
    const metrics = new MetricsCollector();
    const counter = metrics.counter('test.counter', 'Test counter');
    counter.inc();
    counter.inc(5);
    const data = metrics.getMetrics();
    if (data.counters['MetricsCollector.test.counter'].value !== 6) {
      throw new Error('Counter value mismatch');
    }
  });

  // Test 4: Gauge
  await test('Gauge', async () => {
    const metrics = new MetricsCollector();
    const gauge = metrics.gauge('test.gauge', 'Test gauge');
    gauge.set(10);
    const data = metrics.getMetrics();
    if (data.gauges['MetricsCollector.test.gauge'].value !== 10) {
      throw new Error('Gauge value mismatch');
    }
  });

  // Test 5: Histogram
  await test('Histogram', async () => {
    const metrics = new MetricsCollector();
    const histogram = metrics.histogram('test.histogram', 'Test histogram', {
      buckets: [10, 50, 100]
    });
    histogram.observe(25);
    histogram.observe(75);
    const data = metrics.getMetrics();
    const hist = data.histograms['MetricsCollector.test.histogram'];
    if (hist.count !== 2) throw new Error('Histogram count mismatch');
    if (hist.sum !== 100) throw new Error('Histogram sum mismatch');
  });

  // Test 6: Trace
  await test('Trace', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const trace = obs.startTrace('test.operation');
    if (!trace.traceId) throw new Error('Trace ID missing');
    if (!trace.spanId) throw new Error('Span ID missing');
    const result = trace.end({ result: 'success' });
    if (!result.duration) throw new Error('Duration missing');
  });

  // Test 7: Wrap function
  await test('Wrap function', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    const fn = obs.wrap(
      async (x) => x * 2,
      'test.multiply'
    );
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
    const status = obs.getStatus();
    if (status.metrics.totalErrors < 1) throw new Error('Error not recorded');
  });

  // Test 9: Export metrics
  await test('Export metrics (Prometheus)', async () => {
    const obs = new ObservabilitySystem({ logging: { console: false } });
    obs.metrics.counter('test.counter').inc(5);
    const prometheus = obs.exportMetrics('prometheus');
    if (!prometheus.includes('test.counter')) {
      throw new Error('Prometheus export failed');
    }
  });

  // Test 10: Get status
  await test('Get status', async () => {
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
