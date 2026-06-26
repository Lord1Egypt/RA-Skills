/**
 * 事件总线 - 技能进化事件系统
 * 
 * 设计模式：观察者模式 (Observer Pattern) + 事件驱动架构
 * 
 * @version v0.3.0
 * @author 王的奴隶 · 严谨专业版
 */

const EventEmitter = require('events');

// 事件类型常量
const SkillEvents = {
  // 基础事件
  CALLED: 'skill:called',
  COMPLETED: 'skill:completed',
  FAILED: 'skill:failed',
  TIMEOUT: 'skill:timeout',

  // 进化事件
  OPTIMIZATION_START: 'skill:optimization:start',
  OPTIMIZATION_COMPLETE: 'skill:optimization:complete',
  REPORT_GENERATED: 'skill:report:generated',

  // v0.3.0 新增：状态机事件
  STATE_CHANGE: 'skill:state:change',
  STATE_IDLE: 'skill:state:idle',
  STATE_ANALYZING: 'skill:state:analyzing',
  STATE_PLANNING: 'skill:state:planning',
  STATE_IMPLEMENTING: 'skill:state:implementing',
  STATE_TESTING: 'skill:state:testing',
  STATE_DEPLOYING: 'skill:state:deploying',
  STATE_COMPLETED: 'skill:state:completed',
  STATE_FAILED: 'skill:state:failed',

  // v0.3.0 新增：流水线事件
  PIPELINE_START: 'skill:pipeline:start',
  PIPELINE_STAGE_COMPLETE: 'skill:pipeline:stage:complete',
  PIPELINE_COMPLETE: 'skill:pipeline:complete',
  PIPELINE_ERROR: 'skill:pipeline:error',

  // v0.3.0 新增：持久化事件
  STATE_PERSISTED: 'skill:state:persisted',
  LOG_SAVED: 'skill:log:saved',
  STATE_RESTORED: 'skill:state:restored'
};

class EventBus extends EventEmitter {
  constructor(options = {}) {
    super();
    this.maxListeners = options.maxListeners || 100;
    this.eventHistory = [];
    this.maxHistorySize = options.maxHistorySize || 1000;
  }

  /**
   * 发布事件
   * @param {string} event - 事件类型
   * @param {Object} data - 事件数据
   */
  publish(event, data = {}) {
    const eventRecord = {
      event,
      data,
      timestamp: Date.now(),
      id: `${event}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    };

    // 记录事件历史
    this.eventHistory.push(eventRecord);
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory.shift();
    }

    // 发布事件
    this.emit(event, data);
    this.emit('*', { event, data, timestamp: eventRecord.timestamp });

    return eventRecord.id;
  }

  /**
   * 订阅事件
   * @param {string} event - 事件类型
   * @param {Function} callback - 回调函数
   */
  subscribe(event, callback) {
    this.on(event, callback);
  }

  /**
   * 取消订阅
   * @param {string} event - 事件类型
   * @param {Function} callback - 回调函数
   */
  unsubscribe(event, callback) {
    this.off(event, callback);
  }

  /**
   * 获取事件历史
   * @param {Object} filters - 过滤条件
   * @returns {Array}
   */
  getHistory(filters = {}) {
    let history = [...this.eventHistory];

    if (filters.event) {
      history = history.filter(e => e.event === filters.event);
    }
    if (filters.startTime) {
      history = history.filter(e => e.timestamp >= filters.startTime);
    }
    if (filters.endTime) {
      history = history.filter(e => e.timestamp <= filters.endTime);
    }

    return history;
  }

  /**
   * 清空事件历史
   */
  clearHistory() {
    this.eventHistory = [];
  }

  /**
   * 获取监听器统计
   * @returns {Object}
   */
  getStats() {
    const events = this.eventNames();
    const stats = {
      totalEvents: events.length,
      eventListeners: {}
    };

    for (const event of events) {
      stats.eventListeners[event] = this.listenerCount(event);
    }

    return stats;
  }
}

// 事件创建辅助函数
function createSkillEvent(skillName, eventType, additionalData = {}) {
  return {
    skillName,
    eventType,
    timestamp: Date.now(),
    ...additionalData
  };
}

module.exports = {
  EventBus,
  SkillEvents,
  createSkillEvent
};
