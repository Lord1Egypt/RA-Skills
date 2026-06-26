/**
 * Metrics Collector v1.0
 * 内存指标，无外部依赖
 * 支持：Counter, Gauge, Histogram, Timer
 */

class Counter {
  constructor(name, labels = {}) {
    this.name = name;
    this.labels = labels;
    this.value = 0;
  }
  inc(n = 1) { this.value += n; }
  get() { return { name: this.name, labels: this.labels, value: this.value }; }
}

class Gauge {
  constructor(name, labels = {}) {
    this.name = name;
    this.labels = labels;
    this.value = 0;
  }
  set(n) { this.value = n; }
  inc(n = 1) { this.value += n; }
  dec(n = 1) { this.value -= n; }
  get() { return { name: this.name, labels: this.labels, value: this.value }; }
}

class Histogram {
  constructor(name, labels = {}, buckets = [0.01, 0.05, 0.1, 0.5, 1, 5]) {
    this.name = name;
    this.labels = labels;
    this.buckets = buckets;
    this.values = [];
  }
  observe(n) { this.values.push(n); }
  get() {
    const sorted = [...this.values].sort((a, b) => a - b);
    const p50 = sorted[Math.floor(sorted.length * 0.5)] || 0;
    const p95 = sorted[Math.floor(sorted.length * 0.95)] || 0;
    const p99 = sorted[Math.floor(sorted.length * 0.99)] || 0;
    return { name: this.name, labels: this.labels, count: this.values.length, p50, p95, p99 };
  }
}

class Timer {
  constructor(name, labels = {}) {
    this.name = name;
    this.labels = labels;
    this.start = Date.now();
  }
  end() { return (Date.now() - this.start) / 1000; }
}

class MetricsCollector {
  constructor() {
    this.counters = new Map();
    this.gauges = new Map();
    this.histograms = new Map();
  }

  _key(name, labels) {
    return `${name}::${JSON.stringify(labels)}`;
  }

  counter(name, labels = {}) {
    const k = this._key(name, labels);
    if (!this.counters.has(k)) this.counters.set(k, new Counter(name, labels));
    return this.counters.get(k);
  }

  gauge(name, labels = {}) {
    const k = this._key(name, labels);
    if (!this.gauges.has(k)) this.gauges.set(k, new Gauge(name, labels));
    return this.gauges.get(k);
  }

  histogram(name, labels = {}) {
    const k = this._key(name, labels);
    if (!this.histograms.has(k)) this.histograms.set(k, new Histogram(name, labels));
    return this.histograms.get(k);
  }

  timer(name, labels = {}) {
    return new Timer(name, labels);
  }

  // 全部指标
  collect() {
    return {
      counters: [...this.counters.values()].map(c => c.get()),
      gauges: [...this.gauges.values()].map(g => g.get()),
      histograms: [...this.histograms.values()].map(h => h.get()),
    };
  }
}

export const metrics = new MetricsCollector();

// 预定义指标（自动收集）
export function recordSearchLatency(durationMs, mode) {
  const h = metrics.histogram('memory_search_duration_ms', { mode });
  h.observe(durationMs);
  metrics.counter('memory_search_total', { mode }).inc();
}

export function recordStore(size) {
  metrics.counter('memory_store_total').inc();
  metrics.counter('memory_store_bytes_total').inc(size);
}

export function recordError(type) {
  metrics.counter('memory_errors_total', { type }).inc();
}
