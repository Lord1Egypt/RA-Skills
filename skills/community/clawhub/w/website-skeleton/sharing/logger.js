/**
 * 结构化日志工具
 *
 * 提供统一的日志格式，支持 requestId 追踪和耗时统计。
 *
 * 使用方式：
 *   import { createLogger } from '../sharing/logger.js';
 *   const log = createLogger(request);
 *
 *   log.info('order_created', { orderId: 'xxx' });
 *   log.warn('payment_retry', { attempt: 3 });
 *   log.error('db_connection_failed', err);
 */

let seq = 0;

/**
 * 从 Request 中生成唯一 requestId
 */
function getRequestId(request) {
  // 优先使用 EdgeOne 注入的 requestId
  const eoRequestId = request?.headers?.get?.('functions-request-id')
    || request?.headers?.get?.('x-request-id');
  if (eoRequestId) return eoRequestId;

  // 回退：基于时间戳+序列号
  const ts = Date.now().toString(36);
  const s = (seq++).toString(36).padStart(4, '0');
  return `${ts}-${s}`;
}

/**
 * 创建带有 context 的 logger 实例
 *
 * @param {Request} [request] - HTTP Request 对象
 * @param {object} [context]  - 额外上下文（如 tenant, userId）
 * @returns {{ info, warn, error, time, timeEnd }}
 */
export function createLogger(request, context = {}) {
  const requestId = request ? getRequestId(request) : '-';
  const base = { requestId, ...context };

  function format(level, message, data) {
    const entry = {
      ts: new Date().toISOString(),
      level,
      ...base,
      message,
    };
    if (data instanceof Error) {
      entry.error = data.message;
      entry.stack = data.stack?.split('\n').slice(0, 3).join(' | ');
    } else if (data !== undefined) {
      entry.data = data;
    }
    return JSON.stringify(entry);
  }

  return {
    info(message, data) {
      console.log(format('INFO', message, data));
    },
    warn(message, data) {
      console.warn(format('WARN', message, data));
    },
    error(message, data) {
      console.error(format('ERROR', message, data));
    },

    // 耗时统计
    timers: {},
    time(label) {
      this.timers[label] = Date.now();
    },
    timeEnd(label) {
      const start = this.timers[label];
      if (!start) return;
      const elapsed = Date.now() - start;
      delete this.timers[label];
      console.log(format('INFO', `timer:${label}`, { elapsedMs: elapsed }));
      return elapsed;
    },
  };
}

/** 无请求上下文的全局 logger */
export const log = createLogger();
