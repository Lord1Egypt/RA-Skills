#!/usr/bin/env node
/**
 * Performance Monitor - Monitor skill performance metrics
 */

const fs = require('fs');
const path = require('path');

class PerformanceMonitor {
  constructor(options = {}) {
    this.metricsPath = options.metricsPath || path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'metrics');
    this.retentionDays = options.retentionDays || 30;
    this.ensureDirectory();
  }

  ensureDirectory() {
    if (!fs.existsSync(this.metricsPath)) {
      fs.mkdirSync(this.metricsPath, { recursive: true });
    }
  }

  /**
   * Record performance metric
   */
  record(skillName, metric) {
    const timestamp = new Date().toISOString();
    const entry = {
      skill: skillName,
      timestamp,
      ...metric,
    };

    const filePath = path.join(this.metricsPath, `${skillName}.jsonl`);
    fs.appendFileSync(filePath, JSON.stringify(entry) + '\n');

    return entry;
  }

  /**
   * Get metrics for a skill
   */
  getMetrics(skillName, days = 7) {
    const filePath = path.join(this.metricsPath, `${skillName}.jsonl`);
    if (!fs.existsSync(filePath)) return [];

    const since = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();

    return fs.readFileSync(filePath, 'utf-8')
      .split('\n')
      .filter(line => line.trim())
      .map(line => JSON.parse(line))
      .filter(m => m.timestamp >= since);
  }

  /**
   * Calculate average response time
   */
  getAverageResponseTime(skillName, days = 7) {
    const metrics = this.getMetrics(skillName, days);
    const responseTimes = metrics
      .filter(m => m.responseTime)
      .map(m => m.responseTime);

    if (responseTimes.length === 0) return 0;

    return responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length;
  }

  /**
   * Calculate error rate
   */
  getErrorRate(skillName, days = 7) {
    const metrics = this.getMetrics(skillName, days);
    if (metrics.length === 0) return 0;

    const errors = metrics.filter(m => m.error || m.status === 'error').length;
    return errors / metrics.length;
  }

  /**
   * Get all monitored skills
   */
  getMonitoredSkills() {
    if (!fs.existsSync(this.metricsPath)) return [];

    return fs.readdirSync(this.metricsPath)
      .filter(f => f.endsWith('.jsonl'))
      .map(f => f.replace('.jsonl', ''));
  }

  /**
   * Clean old metrics
   */
  cleanOldMetrics() {
    const cutoff = new Date(Date.now() - this.retentionDays * 24 * 60 * 60 * 1000);

    this.getMonitoredSkills().forEach(skill => {
      const filePath = path.join(this.metricsPath, `${skill}.jsonl`);
      const lines = fs.readFileSync(filePath, 'utf-8')
        .split('\n')
        .filter(line => {
          if (!line.trim()) return false;
          try {
            const metric = JSON.parse(line);
            return new Date(metric.timestamp) > cutoff;
          } catch {
            return false;
          }
        });

      fs.writeFileSync(filePath, lines.join('\n'));
    });
  }
}

module.exports = { PerformanceMonitor };
