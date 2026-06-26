/**
 * Performance Analyzer Module
 * Provides comprehensive performance profiling and bottleneck detection
 */

import { performance } from 'perf_hooks';
import { memoryUsage } from 'process';

class Statistics {
  static mean(values) {
    if (values.length === 0) return 0;
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  static median(values) {
    if (values.length === 0) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
  }

  static stdDev(values) {
    if (values.length < 2) return 0;
    const m = this.mean(values);
    const variance = values.reduce((sum, v) => sum + Math.pow(v - m, 2), 0) / (values.length - 1);
    return Math.sqrt(variance);
  }

  static percentile(values, p) {
    if (values.length === 0) return 0;
    const sorted = [...values].sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  static detectOutliers(values) {
    if (values.length < 4) return [];
    const sorted = [...values].sort((a, b) => a - b);
    const q1 = sorted[Math.floor(sorted.length * 0.25)];
    const q3 = sorted[Math.floor(sorted.length * 0.75)];
    const iqr = q3 - q1;
    const lowerBound = q1 - 1.5 * iqr;
    const upperBound = q3 + 1.5 * iqr;
    return values.map((v, i) => ({ value: v, index: i })).filter(({ value }) => value < lowerBound || value > upperBound);
  }
}

export class PerformanceAnalyzer {
  constructor(options = {}) {
    this.options = {
      warmupIterations: options.warmupIterations || 3,
      maxIterations: options.maxIterations || 1000,
      timeoutMs: options.timeoutMs || 30000,
      enableMemoryTracking: options.enableMemoryTracking !== false,
      enableCpuTracking: options.enableCpuTracking !== false,
      ...options
    };
    this.history = [];
  }

  async profile(fn, options = {}) {
    const config = { ...this.options, ...options };
    const iterations = config.iterations || 100;
    const results = { executionTimes: [], memoryUsage: [], cpuUsage: [], errors: [], returnValues: [] };

    for (let i = 0; i < config.warmupIterations; i++) { try { await fn(); } catch (e) {} }

    const startTime = performance.now();
    let completedIterations = 0;

    for (let i = 0; i < iterations && (performance.now() - startTime) < config.timeoutMs; i++) {
      const memBefore = config.enableMemoryTracking ? memoryUsage() : null;
      const cpuBefore = config.enableCpuTracking ? process.cpuUsage() : null;
      const iterStart = performance.now();

      try {
        const result = await fn();
        const iterEnd = performance.now();
        results.executionTimes.push(iterEnd - iterStart);
        results.returnValues.push(result);
        if (config.enableMemoryTracking) {
          const memAfter = memoryUsage();
          results.memoryUsage.push({ heapUsed: memAfter.heapUsed - memBefore.heapUsed, external: memAfter.external - memBefore.external, rss: memAfter.rss - memBefore.rss });
        }
        if (config.enableCpuTracking) {
          const cpuAfter = process.cpuUsage(cpuBefore);
          results.cpuUsage.push({ user: cpuAfter.user, system: cpuAfter.system });
        }
        completedIterations++;
      } catch (error) {
        results.errors.push({ iteration: i, error: error.message });
      }
    }

    const profile = this._generateProfile(results, completedIterations);
    this.history.push({ timestamp: new Date().toISOString(), profile });
    return profile;
  }

  _generateProfile(results, completedIterations) {
    const times = results.executionTimes;
    const mem = results.memoryUsage;
    const cpu = results.cpuUsage;

    const profile = {
      summary: { iterations: completedIterations, errors: results.errors.length, successRate: completedIterations > 0 ? ((completedIterations - results.errors.length) / completedIterations * 100).toFixed(2) + '%' : '0%' },
      timing: { mean: Statistics.mean(times), median: Statistics.median(times), min: times.length > 0 ? Math.min(...times) : 0, max: times.length > 0 ? Math.max(...times) : 0, stdDev: Statistics.stdDev(times), p50: Statistics.percentile(times, 50), p95: Statistics.percentile(times, 95), p99: Statistics.percentile(times, 99) },
      bottlenecks: this._identifyBottlenecks(times, results),
      hotspots: this._identifyHotspots(times),
      outliers: Statistics.detectOutliers(times).map(o => ({ iteration: o.index, value: o.value })),
      recommendations: []
    };

    if (mem.length > 0) {
      profile.memory = { meanHeapUsed: Statistics.mean(mem.map(m => m.heapUsed)), meanExternal: Statistics.mean(mem.map(m => m.external)), meanRss: Statistics.mean(mem.map(m => m.rss)), peakHeapUsed: Math.max(...mem.map(m => m.heapUsed)), peakRss: Math.max(...mem.map(m => m.rss)) };
    }

    if (cpu.length > 0) {
      profile.cpu = { meanUser: Statistics.mean(cpu.map(c => c.user)), meanSystem: Statistics.mean(cpu.map(c => c.system)), totalUser: cpu.reduce((sum, c) => sum + c.user, 0), totalSystem: cpu.reduce((sum, c) => sum + c.system, 0) };
    }

    profile.recommendations = this._generateRecommendations(profile);
    return profile;
  }

  _identifyBottlenecks(times, results) {
    const bottlenecks = [];
    if (times.length === 0) return bottlenecks;
    const mean = Statistics.mean(times);
    const stdDev = Statistics.stdDev(times);
    const threshold = mean + 2 * stdDev;
    const slowIterations = times.map((t, i) => ({ time: t, iteration: i })).filter(({ time }) => time > threshold);

    if (slowIterations.length > times.length * 0.1) {
      bottlenecks.push({ type: 'variability', severity: 'high', description: `High variability: ${slowIterations.length} iterations (${(slowIterations.length/times.length*100).toFixed(1)}%) exceeded threshold`, affectedIterations: slowIterations.slice(0, 5).map(s => s.iteration) });
    }
    if (results.errors.length > times.length * 0.05) {
      bottlenecks.push({ type: 'reliability', severity: results.errors.length > times.length * 0.2 ? 'critical' : 'medium', description: `High error rate: ${results.errors.length}/${times.length} iterations`, errors: results.errors.slice(0, 5) });
    }
    if (mean > 1000) {
      bottlenecks.push({ type: 'latency', severity: mean > 5000 ? 'critical' : 'medium', description: `High average latency: ${mean.toFixed(2)}ms`, suggestion: 'Consider async optimization or caching' });
    }
    return bottlenecks;
  }

  _identifyHotspots(times) {
    if (times.length === 0) return [];
    const mean = Statistics.mean(times);
    const threshold = mean * 1.5;
    return times.map((t, i) => ({ iteration: i, duration: t, severity: t > threshold * 2 ? 'critical' : t > threshold ? 'high' : 'medium' })).filter(h => h.duration > threshold).sort((a, b) => b.duration - a.duration).slice(0, 10);
  }

  _generateRecommendations(profile) {
    const recommendations = [];
    if (profile.timing.stdDev / profile.timing.mean > 0.5) {
      recommendations.push({ type: 'consistency', priority: 'high', description: 'High timing variance detected. Consider identifying and eliminating sources of non-determinism.' });
    }
    if (profile.timing.p95 / profile.timing.mean > 2) {
      recommendations.push({ type: 'latency', priority: 'high', description: 'Large gap between mean and p95 latency. Investigate tail latency causes.' });
    }
    if (profile.memory && profile.memory.peakHeapUsed > 50 * 1024 * 1024) {
      recommendations.push({ type: 'memory', priority: 'medium', description: 'High memory usage detected. Consider memory optimization or leak detection.' });
    }
    return recommendations;
  }

  getHistory() { return this.history; }
  clearHistory() { this.history = []; }
}

export default PerformanceAnalyzer;
