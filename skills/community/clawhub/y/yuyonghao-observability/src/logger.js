/**
 * Observability Logger - 结构化日志系统
 * 
 * 功能:
 * - 结构化日志（JSON 格式）
 * - 多级别日志（error/warn/info/debug）
 * - 多输出（console/file/elasticsearch）
 * - 上下文追踪（traceId/spanId）
 * - 性能指标集成
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const winston = require('winston');
const path = require('path');
const fs = require('fs');

// 确保日志目录存在
const logDir = path.join(__dirname, '..', 'logs');
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// 日志格式
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// 控制台格式（彩色）
const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, ...meta }) => {
    const context = meta.traceId ? `[${meta.traceId.substr(0, 8)}]` : '';
    return `${timestamp} ${level}: ${context} ${message} ${Object.keys(meta).length ? JSON.stringify(meta) : ''}`;
  })
);

class ObservabilityLogger {
  constructor(options = {}) {
    this.options = {
      // 日志级别
      level: options.level || 'info',
      // 日志目录
      logDir: options.logDir || logDir,
      // 是否输出到控制台
      console: options.console !== false,
      // 是否输出到文件
      file: options.file !== false,
      // 是否输出到 Elasticsearch（待实现）
      elasticsearch: options.elasticsearch || false,
      // 默认上下文
      defaultMeta: options.defaultMeta || {},
    };

    // 创建 Winston logger
    this.logger = winston.createLogger({
      level: this.options.level,
      defaultMeta: this.options.defaultMeta,
      transports: []
    });

    // 控制台输出
    if (this.options.console) {
      this.logger.add(new winston.transports.Console({
        format: consoleFormat
      }));
    }

    // 文件输出（按级别分文件）
    if (this.options.file) {
      this.logger.add(new winston.transports.File({
        filename: path.join(this.options.logDir, 'error.log'),
        level: 'error',
        format: logFormat,
        maxsize: 10 * 1024 * 1024, // 10MB
        maxFiles: 5
      }));

      this.logger.add(new winston.transports.File({
        filename: path.join(this.options.logDir, 'combined.log'),
        format: logFormat,
        maxsize: 10 * 1024 * 1024,
        maxFiles: 5
      }));
    }

    // 生成 traceId
    this.currentTraceId = this._generateTraceId();
    this.currentSpanId = null;

    this.info('Observability Logger 初始化完成', {
      level: this.options.level,
      console: this.options.console,
      file: this.options.file
    });
  }

  /**
   * 生成 traceId
   */
  _generateTraceId() {
    return `trace-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 生成 spanId
   */
  _generateSpanId() {
    return `span-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 设置当前 trace 上下文
   */
  setContext(traceId, spanId = null) {
    this.currentTraceId = traceId || this._generateTraceId();
    this.currentSpanId = spanId || this._generateSpanId();
    return { traceId: this.currentTraceId, spanId: this.currentSpanId };
  }

  /**
   * 获取当前上下文
   */
  getContext() {
    return {
      traceId: this.currentTraceId,
      spanId: this.currentSpanId
    };
  }

  /**
   * 创建子 span
   */
  createChildSpan(operation) {
    const parentSpanId = this.currentSpanId;
    const childSpanId = this._generateSpanId();
    
    this.currentSpanId = childSpanId;
    
    return {
      traceId: this.currentTraceId,
      parentSpanId,
      spanId: childSpanId,
      operation,
      end: () => {
        this.currentSpanId = parentSpanId;
        this.debug('Span ended', { operation, spanId: childSpanId });
      }
    };
  }

  /**
   * 日志方法
   */
  error(message, meta = {}) {
    this.logger.error(message, { ...this.getContext(), ...meta });
  }

  warn(message, meta = {}) {
    this.logger.warn(message, { ...this.getContext(), ...meta });
  }

  info(message, meta = {}) {
    this.logger.info(message, { ...this.getContext(), ...meta });
  }

  debug(message, meta = {}) {
    this.logger.debug(message, { ...this.getContext(), ...meta });
  }

  /**
   * 性能日志
   */
  perf(operation, duration, meta = {}) {
    this.info(`[PERF] ${operation}`, {
      duration,
      unit: 'ms',
      ...meta
    });
  }

  /**
   * 指标日志
   */
  metric(name, value, type = 'gauge', meta = {}) {
    this.info(`[METRIC] ${name}`, {
      value,
      type,
      ...meta
    });
  }

  /**
   * 结构化日志
   */
  log(level, message, structuredData = {}) {
    this.logger.log(level, message, {
      ...this.getContext(),
      ...structuredData
    });
  }

  /**
   * 开始追踪
   */
  startTrace(operation, meta = {}) {
    const context = this.setContext();
    this.info(`[TRACE START] ${operation}`, {
      ...context,
      ...meta
    });
    return context;
  }

  /**
   * 结束追踪
   */
  endTrace(operation, context, duration, meta = {}) {
    this.info(`[TRACE END] ${operation}`, {
      ...context,
      duration,
      ...meta
    });
  }

  /**
   * 包装异步函数（自动追踪）
   */
  wrap(fn, operation) {
    const self = this;
    return async function(...args) {
      const traceContext = self.setContext();
      const span = self.createChildSpan(operation);
      
      try {
        const result = await fn.apply(this, args);
        span.end();
        return result;
      } catch (error) {
        self.error('Operation failed', {
          ...traceContext,
          operation,
          error: error.message,
          stack: error.stack
        });
        throw error;
      }
    };
  }

  /**
   * 获取日志目录
   */
  getLogDir() {
    return this.options.logDir;
  }

  /**
   * 导出日志（用于分析）
   */
  exportLogs(options = {}) {
    const { level = 'info', startTime, endTime, limit = 1000 } = options;
    
    // 读取日志文件（简化版）
    const logFile = path.join(this.options.logDir, 'combined.log');
    
    if (!fs.existsSync(logFile)) {
      return [];
    }

    const content = fs.readFileSync(logFile, 'utf8');
    const lines = content.split('\n').filter(line => line.trim());
    
    return lines
      .slice(-limit)
      .map(line => {
        try {
          return JSON.parse(line);
        } catch {
          return { raw: line };
        }
      })
      .filter(log => {
        if (!log.timestamp) return true;
        return log.level >= level;
      });
  }
}

// 导出
module.exports = { ObservabilityLogger };
