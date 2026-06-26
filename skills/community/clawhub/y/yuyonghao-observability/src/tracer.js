/**
 * Observability System - Distributed Tracing
 * Tracks task execution across multiple agents
 */

const { ObservabilityLogger } = require('./logger');

class TraceSpan {
  constructor(traceId, spanId, name, parentSpanId = null) {
    this.traceId = traceId;
    this.spanId = spanId;
    this.name = name;
    this.parentSpanId = parentSpanId;
    this.startTime = Date.now();
    this.endTime = null;
    this.duration = null;
    this.status = 'running'; // running, completed, error
    this.tags = {};
    this.logs = [];
    this.error = null;
  }

  setTag(key, value) {
    this.tags[key] = value;
  }

  log(message, data = {}) {
    this.logs.push({
      timestamp: Date.now(),
      message,
      data
    });
  }

  setError(error) {
    this.error = {
      message: error.message,
      stack: error.stack
    };
    this.status = 'error';
  }

  end() {
    this.endTime = Date.now();
    this.duration = this.endTime - this.startTime;
    if (this.status !== 'error') {
      this.status = 'completed';
    }
  }

  toJSON() {
    return {
      traceId: this.traceId,
      spanId: this.spanId,
      parentSpanId: this.parentSpanId,
      name: this.name,
      startTime: this.startTime,
      endTime: this.endTime,
      duration: this.duration,
      status: this.status,
      tags: this.tags,
      logs: this.logs,
      error: this.error
    };
  }
}

class Tracer {
  constructor(options = {}) {
    this.logger = options.logger || new ObservabilityLogger();
    this.traces = new Map();
    this.spans = new Map();
    this.maxTraces = options.maxTraces || 1000;
    this.sampleRate = options.sampleRate !== undefined ? options.sampleRate : 1.0; // 100% sampling
  }

  generateId() {
    return Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  }

  shouldSample() {
    if (this.sampleRate <= 0) return false;
    if (this.sampleRate >= 1) return true;
    return Math.random() < this.sampleRate;
  }

  /**
   * Start a new trace
   */
  startTrace(name, context = {}) {
    if (!this.shouldSample()) {
      return null;
    }

    const traceId = this.generateId();
    const span = new TraceSpan(traceId, this.generateId(), name);
    
    // Add context tags
    Object.entries(context).forEach(([key, value]) => {
      span.setTag(key, value);
    });

    this.traces.set(traceId, {
      traceId,
      name,
      startTime: Date.now(),
      spans: [span]
    });
    this.spans.set(span.spanId, span);

    this.logger.debug('Trace started', {
      traceId,
      name,
      context
    });

    return span;
  }

  /**
   * Start a child span
   */
  startSpan(name, parentSpan, context = {}) {
    if (!parentSpan) {
      return this.startTrace(name, context);
    }

    const span = new TraceSpan(
      parentSpan.traceId,
      this.generateId(),
      name,
      parentSpan.spanId
    );

    // Add context tags
    Object.entries(context).forEach(([key, value]) => {
      span.setTag(key, value);
    });

    // Add to trace
    const trace = this.traces.get(parentSpan.traceId);
    if (trace) {
      trace.spans.push(span);
    }

    this.spans.set(span.spanId, span);

    this.logger.debug('Span started', {
      traceId: span.traceId,
      spanId: span.spanId,
      name,
      parentSpanId: span.parentSpanId
    });

    return span;
  }

  /**
   * End a span
   */
  endSpan(span, error = null) {
    if (!span) return;

    if (error) {
      span.setError(error);
    }

    span.end();

    this.logger.debug('Span ended', {
      traceId: span.traceId,
      spanId: span.spanId,
      name: span.name,
      duration: span.duration
    });

    // Log trace completion when root span ends
    if (!span.parentSpanId) {
      this.logTraceCompletion(span.traceId);
    }

    // Cleanup old traces
    this.cleanup();
  }

  /**
   * Log trace completion
   */
  logTraceCompletion(traceId) {
    const trace = this.traces.get(traceId);
    if (!trace) return;

    trace.endTime = Date.now();
    trace.duration = trace.endTime - trace.startTime;

    // Calculate span statistics
    const spanStats = {
      total: trace.spans.length,
      completed: trace.spans.filter(s => s.status === 'completed').length,
      errors: trace.spans.filter(s => s.status === 'error').length,
      avgDuration: trace.spans.reduce((sum, s) => sum + (s.duration || 0), 0) / trace.spans.length
    };

    this.logger.info('Trace completed', {
      traceId,
      name: trace.name,
      duration: trace.duration,
      spanStats
    });
  }

  /**
   * Get trace by ID
   */
  getTrace(traceId) {
    return this.traces.get(traceId);
  }

  /**
   * Get recent traces
   */
  getRecentTraces(limit = 10) {
    return Array.from(this.traces.values())
      .sort((a, b) => b.startTime - a.startTime)
      .slice(0, limit);
  }

  /**
   * Export trace to JSON
   */
  exportTrace(traceId) {
    const trace = this.traces.get(traceId);
    if (!trace) return null;

    return {
      ...trace,
      spans: trace.spans.map(s => s.toJSON())
    };
  }

  /**
   * Cleanup old traces
   */
  cleanup() {
    if (this.traces.size <= this.maxTraces) return;

    const traceIds = Array.from(this.traces.keys())
      .sort((a, b) => {
        const traceA = this.traces.get(a);
        const traceB = this.traces.get(b);
        return traceA.startTime - traceB.startTime;
      });

    // Remove oldest traces
    const toRemove = traceIds.slice(0, traceIds.length - this.maxTraces);
    toRemove.forEach(traceId => {
      const trace = this.traces.get(traceId);
      trace.spans.forEach(span => this.spans.delete(span.spanId));
      this.traces.delete(traceId);
    });

    this.logger.debug(`Cleaned up ${toRemove.length} old traces`);
  }

  /**
   * Get tracer statistics
   */
  getStats() {
    const traces = Array.from(this.traces.values());
    const spans = Array.from(this.spans.values());

    return {
      totalTraces: this.traces.size,
      totalSpans: this.spans.size,
      activeTraces: traces.filter(t => !t.endTime).length,
      completedTraces: traces.filter(t => t.endTime).length,
      errorTraces: traces.filter(t => t.spans.some(s => s.status === 'error')).length,
      avgTraceDuration: traces.filter(t => t.duration).reduce((sum, t) => sum + t.duration, 0) / traces.length || 0,
      avgSpanDuration: spans.filter(s => s.duration).reduce((sum, s) => sum + s.duration, 0) / spans.length || 0
    };
  }
}

module.exports = { Tracer, TraceSpan };
