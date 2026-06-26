#!/usr/bin/env node
/**
 * Bottleneck Analyzer - Identify performance bottlenecks
 */

class BottleneckAnalyzer {
  constructor(options = {}) {
    this.responseTimeThreshold = options.responseTimeThreshold || 1000; // 1 second
    this.errorRateThreshold = options.errorRateThreshold || 0.05; // 5%
    this.memoryThreshold = options.memoryThreshold || 100 * 1024 * 1024; // 100MB
  }

  /**
   * Analyze skill performance
   */
  analyze(skillName, metrics) {
    const issues = [];

    // Check response time
    const avgResponseTime = this.calculateAverage(metrics, 'responseTime');
    if (avgResponseTime > this.responseTimeThreshold) {
      issues.push({
        type: 'slow_response',
        severity: avgResponseTime > this.responseTimeThreshold * 2 ? 'high' : 'medium',
        message: `Average response time ${avgResponseTime.toFixed(2)}ms exceeds threshold ${this.responseTimeThreshold}ms`,
        metric: avgResponseTime,
        threshold: this.responseTimeThreshold,
      });
    }

    // Check error rate
    const errorRate = this.calculateErrorRate(metrics);
    if (errorRate > this.errorRateThreshold) {
      issues.push({
        type: 'high_error_rate',
        severity: errorRate > this.errorRateThreshold * 2 ? 'high' : 'medium',
        message: `Error rate ${(errorRate * 100).toFixed(2)}% exceeds threshold ${(this.errorRateThreshold * 100).toFixed(2)}%`,
        metric: errorRate,
        threshold: this.errorRateThreshold,
      });
    }

    // Check memory usage
    const avgMemory = this.calculateAverage(metrics, 'memoryUsage');
    if (avgMemory > this.memoryThreshold) {
      issues.push({
        type: 'high_memory',
        severity: avgMemory > this.memoryThreshold * 2 ? 'high' : 'medium',
        message: `Average memory usage ${(avgMemory / 1024 / 1024).toFixed(2)}MB exceeds threshold ${(this.memoryThreshold / 1024 / 1024).toFixed(2)}MB`,
        metric: avgMemory,
        threshold: this.memoryThreshold,
      });
    }

    // Check for memory leaks
    const memoryTrend = this.calculateTrend(metrics, 'memoryUsage');
    if (memoryTrend > 0.1) { // 10% increase per day
      issues.push({
        type: 'memory_leak',
        severity: 'high',
        message: `Potential memory leak detected: ${(memoryTrend * 100).toFixed(2)}% daily increase`,
        metric: memoryTrend,
      });
    }

    return {
      skill: skillName,
      issues,
      summary: {
        totalIssues: issues.length,
        highSeverity: issues.filter(i => i.severity === 'high').length,
        mediumSeverity: issues.filter(i => i.severity === 'medium').length,
      },
    };
  }

  /**
   * Calculate average of a metric
   */
  calculateAverage(metrics, field) {
    const values = metrics
      .filter(m => m[field] !== undefined)
      .map(m => m[field]);

    if (values.length === 0) return 0;
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  /**
   * Calculate error rate
   */
  calculateErrorRate(metrics) {
    if (metrics.length === 0) return 0;
    const errors = metrics.filter(m => m.error || m.status === 'error').length;
    return errors / metrics.length;
  }

  /**
   * Calculate trend (slope) of a metric
   */
  calculateTrend(metrics, field) {
    const values = metrics
      .filter(m => m[field] !== undefined)
      .map((m, i) => ({ x: i, y: m[field] }));

    if (values.length < 2) return 0;

    const n = values.length;
    const sumX = values.reduce((a, b) => a + b.x, 0);
    const sumY = values.reduce((a, b) => a + b.y, 0);
    const sumXY = values.reduce((a, b) => a + b.x * b.y, 0);
    const sumXX = values.reduce((a, b) => a + b.x * b.x, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    return slope / (sumY / n); // Return as percentage of average
  }
}

module.exports = { BottleneckAnalyzer };
