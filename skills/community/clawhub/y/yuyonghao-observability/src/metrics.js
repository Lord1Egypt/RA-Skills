/**
 * Metrics Collector - 性能指标收集器
 * 
 * 功能:
 * - Counter（计数器）
 * - Gauge（仪表）
 * - Histogram（直方图）
 * - 指标导出（Prometheus 格式）
 * - 自动聚合
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

class MetricsCollector {
  constructor(options = {}) {
    this.options = {
      // 指标前缀
      prefix: options.prefix || 'agent',
      // 自动报告间隔（毫秒）
      reportInterval: options.reportInterval || 60000,
      // 是否自动报告
      autoReport: options.autoReport || false,
    };

    // 指标存储
    this.counters = new Map();      // name -> {value, labels}
    this.gauges = new Map();        // name -> {value, labels, timestamp}
    this.histograms = new Map();    // name -> {buckets, sum, count}
    
    // 报告回调
    this.reportCallbacks = [];

    // 自动报告
    if (this.options.autoReport) {
      this.startAutoReport();
    }

    // 初始化默认指标
    this._initDefaultMetrics();
  }

  /**
   * 初始化默认指标
   */
  _initDefaultMetrics() {
    // Agent 调用次数
    this.counter('calls.total', 'Total agent calls');
    
    // Agent 延迟
    this.histogram('calls.latency', 'Agent call latency', {
      buckets: [10, 50, 100, 500, 1000, 5000]
    });
    
    // Token 使用
    this.counter('tokens.total', 'Total tokens used');
    
    // 错误次数
    this.counter('errors.total', 'Total errors');
    
    // 活跃 Agent 数
    this.gauge('agents.active', 'Number of active agents');
  }

  /**
   * Counter（计数器）
   */
  counter(name, help = '') {
    const fullName = `${this.options.prefix}.${name}`;
    
    if (!this.counters.has(fullName)) {
      this.counters.set(fullName, {
        name: fullName,
        help,
        value: 0,
        labels: {}
      });
    }

    return {
      inc: (value = 1, labels = {}) => {
        const counter = this.counters.get(fullName);
        counter.value += value;
        counter.labels = { ...counter.labels, ...labels };
        this._triggerReport();
      },
      reset: () => {
        const counter = this.counters.get(fullName);
        counter.value = 0;
        counter.labels = {};
      }
    };
  }

  /**
   * Gauge（仪表）
   */
  gauge(name, help = '') {
    const fullName = `${this.options.prefix}.${name}`;
    
    if (!this.gauges.has(fullName)) {
      this.gauges.set(fullName, {
        name: fullName,
        help,
        value: 0,
        labels: {},
        timestamp: Date.now()
      });
    }

    return {
      set: (value, labels = {}) => {
        const gauge = this.gauges.get(fullName);
        gauge.value = value;
        gauge.labels = { ...gauge.labels, ...labels };
        gauge.timestamp = Date.now();
        this._triggerReport();
      },
      inc: (value = 1) => {
        const gauge = this.gauges.get(fullName);
        gauge.value += value;
        gauge.timestamp = Date.now();
        this._triggerReport();
      },
      dec: (value = 1) => {
        const gauge = this.gauges.get(fullName);
        gauge.value -= value;
        gauge.timestamp = Date.now();
        this._triggerReport();
      }
    };
  }

  /**
   * Histogram（直方图）
   */
  histogram(name, help = '', options = {}) {
    const fullName = `${this.options.prefix}.${name}`;
    const buckets = options.buckets || [10, 50, 100, 500, 1000];
    
    if (!this.histograms.has(fullName)) {
      this.histograms.set(fullName, {
        name: fullName,
        help,
        buckets: buckets.sort((a, b) => a - b),
        bucketCounts: new Array(buckets.length).fill(0),
        sum: 0,
        count: 0
      });
    }

    return {
      observe: (value, labels = {}) => {
        const histogram = this.histograms.get(fullName);
        
        // 找到对应的 bucket
        for (let i = 0; i < histogram.buckets.length; i++) {
          if (value <= histogram.buckets[i]) {
            histogram.bucketCounts[i]++;
            break;
          }
        }
        
        // 如果超过所有 bucket，计入最后一个
        if (value > histogram.buckets[histogram.buckets.length - 1]) {
          histogram.bucketCounts[histogram.bucketCounts.length - 1]++;
        }
        
        histogram.sum += value;
        histogram.count++;
        
        this._triggerReport();
      },
      reset: () => {
        const histogram = this.histograms.get(fullName);
        histogram.bucketCounts.fill(0);
        histogram.sum = 0;
        histogram.count = 0;
      }
    };
  }

  /**
   * 获取所有指标
   */
  getMetrics() {
    const metrics = {
      timestamp: Date.now(),
      counters: {},
      gauges: {},
      histograms: {}
    };

    // Counters
    for (const [name, counter] of this.counters) {
      metrics.counters[name] = {
        value: counter.value,
        labels: counter.labels
      };
    }

    // Gauges
    for (const [name, gauge] of this.gauges) {
      metrics.gauges[name] = {
        value: gauge.value,
        labels: gauge.labels,
        timestamp: gauge.timestamp
      };
    }

    // Histograms
    for (const [name, histogram] of this.histograms) {
      const percentiles = this._calculatePercentiles(histogram);
      
      metrics.histograms[name] = {
        count: histogram.count,
        sum: histogram.sum,
        avg: histogram.count > 0 ? histogram.sum / histogram.count : 0,
        buckets: histogram.buckets.map((bucket, i) => ({
          le: bucket,
          count: histogram.bucketCounts[i]
        })),
        percentiles
      };
    }

    return metrics;
  }

  /**
   * 计算百分位数
   */
  _calculatePercentiles(histogram) {
    if (histogram.count === 0) {
      return { p50: 0, p90: 0, p99: 0 };
    }

    const total = histogram.count;
    const percentiles = {};
    
    [50, 90, 99].forEach(p => {
      const targetCount = Math.ceil(total * (p / 100));
      let cumulative = 0;
      
      for (let i = 0; i < histogram.buckets.length; i++) {
        cumulative += histogram.bucketCounts[i];
        if (cumulative >= targetCount) {
          percentiles[`p${p}`] = histogram.buckets[i];
          return;
        }
      }
      
      percentiles[`p${p}`] = histogram.buckets[histogram.buckets.length - 1];
    });

    return percentiles;
  }

  /**
   * 导出为 Prometheus 格式
   */
  toPrometheus() {
    const lines = [];
    const metrics = this.getMetrics();

    // Counters
    for (const [name, data] of Object.entries(metrics.counters)) {
      lines.push(`# HELP ${name} ${data.help || ''}`);
      lines.push(`# TYPE ${name} counter`);
      lines.push(`${name} ${data.value}`);
    }

    // Gauges
    for (const [name, data] of Object.entries(metrics.gauges)) {
      lines.push(`# HELP ${name} ${data.help || ''}`);
      lines.push(`# TYPE ${name} gauge`);
      lines.push(`${name} ${data.value}`);
    }

    // Histograms
    for (const [name, data] of Object.entries(metrics.histograms)) {
      lines.push(`# HELP ${name} ${data.help || ''}`);
      lines.push(`# TYPE ${name} histogram`);
      
      data.buckets.forEach(bucket => {
        lines.push(`${name}_bucket{le="${bucket.le}"} ${bucket.count}`);
      });
      
      lines.push(`${name}_sum ${data.sum}`);
      lines.push(`${name}_count ${data.count}`);
    }

    return lines.join('\n');
  }

  /**
   * 注册报告回调
   */
  onReport(callback) {
    this.reportCallbacks.push(callback);
  }

  /**
   * 触发报告
   */
  _triggerReport() {
    if (this.reportCallbacks.length > 0) {
      const metrics = this.getMetrics();
      this.reportCallbacks.forEach(cb => cb(metrics));
    }
  }

  /**
   * 开始自动报告
   */
  startAutoReport() {
    this.autoReportTimer = setInterval(() => {
      this._triggerReport();
    }, this.options.reportInterval);
  }

  /**
   * 停止自动报告
   */
  stopAutoReport() {
    if (this.autoReportTimer) {
      clearInterval(this.autoReportTimer);
    }
  }

  /**
   * 重置所有指标
   */
  reset() {
    this.counters.clear();
    this.gauges.clear();
    this.histograms.clear();
    this._initDefaultMetrics();
  }

  /**
   * 获取统计摘要
   */
  getSummary() {
    const metrics = this.getMetrics();
    
    return {
      timestamp: metrics.timestamp,
      totalCalls: metrics.counters[`${this.options.prefix}.calls.total`]?.value || 0,
      totalErrors: metrics.counters[`${this.options.prefix}.errors.total`]?.value || 0,
      activeAgents: metrics.gauges[`${this.options.prefix}.agents.active`]?.value || 0,
      avgLatency: metrics.histograms[`${this.options.prefix}.calls.latency`]?.avg || 0,
      latencyP99: metrics.histograms[`${this.options.prefix}.calls.latency`]?.percentiles?.p99 || 0
    };
  }
}

// 导出
module.exports = { MetricsCollector };
