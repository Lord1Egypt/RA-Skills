/**
 * 对话状态监控模块
 * 
 * 负责：
 * 1. 获取当前对话状态
 * 2. 判断是否在安静时段
 * 3. 计算响应超时时间
 * 4. 收集监控统计数据
 */

const EventEmitter = require('events');

class Monitor extends EventEmitter {
  constructor(config, logger) {
    super();
    this.config = config;
    this.logger = logger;
    this.stats = {
      checks: 0,
      responses: 0,
      completions: 0,
      skips: 0,
      errors: 0,
      startTime: Date.now()
    };
  }

  /**
   * 获取当前对话状态
   */
  async getConversationState() {
    try {
      this.stats.checks++;
      
      // 模拟获取对话状态
      // 实际实现需要调用OpenClaw的API获取真实数据
      const state = await this.simulateGetConversationState();
      
      this.logger.debug('获取对话状态成功', {
        lastSpeaker: state.lastSpeaker,
        timeSince: state.timeSince,
        isActive: state.isActive
      });
      
      return state;
    } catch (error) {
      this.stats.errors++;
      this.logger.error('获取对话状态失败', { error: error.message });
      throw error;
    }
  }

  /**
   * 模拟获取对话状态
   * 实际实现需要替换为真实的API调用
   */
  async simulateGetConversationState() {
    // 这里应该调用OpenClaw的API获取真实的对话状态
    // 暂时返回模拟数据
    
    const now = Date.now();
    
    // 模拟数据 - 实际应该从OpenClaw获取
    return {
      lastSpeaker: 'user', // 'user' 或 'ai'
      lastMessage: {
        id: 'msg_' + Date.now(),
        speaker: 'user',
        content: '这是一个测试消息',
        timestamp: now - 120000, // 2分钟前
        type: 'text'
      },
      conversationId: 'conv_' + this.stats.checks,
      participants: ['user', 'ai'],
      isActive: true,
      timeSince: 120, // 秒
      historyLength: 15
    };
  }

  /**
   * 判断是否在安静时段
   */
  isQuietTime() {
    if (!this.config.quiet_hours || this.config.quiet_hours.length === 0) {
      return false;
    }

    const now = new Date();
    const currentTime = now.getHours() * 100 + now.getMinutes(); // HHMM格式
    
    for (const timeRange of this.config.quiet_hours) {
      const [start, end] = timeRange.split('-');
      const startTime = this.timeToNumber(start);
      const endTime = this.timeToNumber(end);
      
      if (this.isTimeInRange(currentTime, startTime, endTime)) {
        this.logger.debug('当前是安静时段', { 
          currentTime: this.formatTime(currentTime),
          quietRange: timeRange 
        });
        return true;
      }
    }
    
    return false;
  }

  /**
   * 将时间字符串转换为数字
   * @param {string} timeStr - 时间字符串，如 "23:00"
   */
  timeToNumber(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 100 + minutes;
  }

  /**
   * 格式化数字时间为字符串
   * @param {number} timeNum - 数字时间
   */
  formatTime(timeNum) {
    const hours = Math.floor(timeNum / 100);
    const minutes = timeNum % 100;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  }

  /**
   * 判断时间是否在范围内
   * @param {number} current - 当前时间
   * @param {number} start - 开始时间
   * @param {number} end - 结束时间
   */
  isTimeInRange(current, start, end) {
    if (start <= end) {
      // 正常时间范围，如 09:00-18:00
      return current >= start && current < end;
    } else {
      // 跨午夜时间范围，如 23:00-07:00
      return current >= start || current < end;
    }
  }

  /**
   * 判断是否需要检查
   * @param {Object} state - 对话状态
   */
  shouldCheck(state) {
    // 如果对话不活跃，减少检查频率
    if (!state.isActive) {
      this.logger.debug('对话不活跃，跳过检查');
      return false;
    }
    
    // 如果距离上次检查时间太短，跳过
    const minInterval = (this.config.min_interval || 60) * 1000;
    const timeSinceLastCheck = Date.now() - (this.lastCheckTime || 0);
    
    if (timeSinceLastCheck < minInterval) {
      this.logger.debug('检查间隔太短，跳过', { 
        timeSinceLastCheck: Math.floor(timeSinceLastCheck / 1000) + 's',
        minInterval: this.config.min_interval + 's'
      });
      return false;
    }
    
    this.lastCheckTime = Date.now();
    return true;
  }

  /**
   * 判断是否超时需要响应
   * @param {Object} state - 对话状态
   */
  isResponseTimeout(state) {
    if (state.lastSpeaker !== 'user') {
      return false;
    }
    
    const threshold = this.config.response_threshold || 180; // 默认3分钟
    return state.timeSince >= threshold;
  }

  /**
   * 获取监控统计数据
   */
  getStats() {
    const now = Date.now();
    const uptime = Math.floor((now - this.stats.startTime) / 1000);
    
    return {
      ...this.stats,
      uptime: this.formatUptime(uptime),
      checksPerMinute: this.stats.checks / (uptime / 60),
      responseRate: this.stats.checks > 0 ? (this.stats.responses / this.stats.checks) * 100 : 0,
      skipRate: this.stats.checks > 0 ? (this.stats.skips / this.stats.checks) * 100 : 0,
      errorRate: this.stats.checks > 0 ? (this.stats.errors / this.stats.checks) * 100 : 0
    };
  }

  /**
   * 格式化运行时间
   * @param {number} seconds - 秒数
   */
  formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    const parts = [];
    if (days > 0) parts.push(`${days}d`);
    if (hours > 0) parts.push(`${hours}h`);
    if (minutes > 0) parts.push(`${minutes}m`);
    parts.push(`${secs}s`);
    
    return parts.join(' ');
  }

  /**
   * 停止监控
   */
  async stop() {
    this.logger.info('监控模块已停止');
    this.stats.endTime = Date.now();
  }

  /**
   * 记录响应
   */
  recordResponse() {
    this.stats.responses++;
  }

  /**
   * 记录补全
   */
  recordCompletion() {
    this.stats.completions++;
  }

  /**
   * 记录跳过
   */
  recordSkip() {
    this.stats.skips++;
  }
}

module.exports = Monitor;