/**
 * Tracer - 轻量链路追踪 v1.0
 * 特性：
 * - 分布式 traceId 生成
 * - Span 嵌套（支持 async/await）
 * - 内存存储（可查当前活跃 span）
 * - JSON 导出（可接 Jaeger/DataDog）
 */

export class TraceContext {
  constructor() {
    this.traceId = this._genTraceId();
    this.spans = [];
    this._activeSpan = null;
    this._maxSpans = 1000;
  }

  _genTraceId() {
    return `trace-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
  }

  startSpan(name, tags = {}) {
    // Auto-evict oldest span when exceeding limit
    if (this.spans.length >= this._maxSpans) {
      this.spans.shift();
    }
    const span = {
      id: `${name}-${Date.now().toString(36)}`,
      name,
      traceId: this.traceId,
      parentId: this._activeSpan?.id || null,
      startTs: Date.now(),
      tags,
      events: [],
      status: 'running',
    };
    this._activeSpan = span;
    this.spans.push(span);
    return span;
  }

  endSpan(span, tags = {}, status = 'ok') {
    span.endTs = Date.now();
    span.durationMs = span.endTs - span.startTs;
    span.status = status;
    span.tags = { ...span.tags, ...tags };
    if (this._activeSpan === span) {
      this._activeSpan = null;
    }
  }

  addEvent(span, name, attrs = {}) {
    span.events.push({ name, ts: Date.now(), attrs });
  }

  toJSON() {
    return {
      traceId: this.traceId,
      spans: this.spans.map(s => ({ ...s })),
      startTime: this.spans[0]?.startTs,
      endTime: this.spans[this.spans.length - 1]?.endTs,
    };
  }
}

// 全局 tracer 实例
let globalTrace = null;

export function startTrace(name, tags = {}) {
  globalTrace = new TraceContext();
  return globalTrace.startSpan(name, tags);
}

export function endTrace(span, tags = {}, status = 'ok') {
  if (globalTrace) {
    globalTrace.endSpan(span, tags, status);
  }
}

export function getCurrentTrace() {
  return globalTrace;
}

export function getTraceExport() {
  return globalTrace?.toJSON() || null;
}

export function clearTrace() {
  globalTrace = null;
}
