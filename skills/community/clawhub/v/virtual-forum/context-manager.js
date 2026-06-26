/**
 * 上下文管理器
 * Context Manager for Virtual Forum v3.5
 *
 * 解决问题：上下文窗口无限膨胀导致 Token 爆炸（100-500元/次）
 * 策略：
 * 1. 滑动窗口：只保留最近 N 轮的完整对话
 * 2. 摘要压缩：每 M 轮生成一次历史摘要
 * 3. 参与者视角：每位辩论者维护独立的上下文视角
 */

const { DEFAULTS } = require('./shared-config.js');

class ContextManager {
  constructor(options = {}) {
    this.windowSize = options.windowSize || DEFAULTS.contextWindowSize;
    this.summarizeEvery = options.summarizeEvery || DEFAULTS.summarizeEveryNRounds;
    this.fullHistory = [];
    this.summaries = [];
    this.currentWindow = [];
    this.participantContexts = {};
  }

  /**
   * 添加一轮对话记录
   * @param {object} roundData - { round, speaker, content, type }
   */
  addRound(roundData) {
    this.fullHistory.push(roundData);
    this.currentWindow.push(roundData);

    // 滑动窗口：超出窗口大小时移除最早的记录
    if (this.currentWindow.length > this.windowSize) {
      this.currentWindow.shift();
    }

    // 更新参与者上下文
    const speaker = roundData.speaker;
    if (!this.participantContexts[speaker]) {
      this.participantContexts[speaker] = [];
    }
    this.participantContexts[speaker].push(roundData);
  }

  /**
   * 添加摘要（由主持人或系统生成）
   * @param {string} summary - 摘要文本
   * @param {number} upToRound - 摘要覆盖到第几轮
   */
  addSummary(summary, upToRound) {
    this.summaries.push({
      summary,
      upToRound,
      timestamp: Date.now()
    });
  }

  /**
   * 获取给特定辩论者的上下文
   * 包含：最新摘要 + 滑动窗口内的完整对话
   * 
   * [FIX] 强制Token上限检查，避免超出模型context window
   *
   * @param {string} participantName - 参与者名称
   * @returns {string} 格式化的上下文字符串
   */
  getContextForParticipant(participantName) {
    // [FIX] 强制Token上限检查（8K tokens = 约16000字符）
    const MAX_CONTEXT_CHARS = 16000; // 安全阈值（8K tokens）
    
    let context = '';

    // 1. 添加最新的历史摘要
    if (this.summaries.length > 0) {
      const latestSummary = this.summaries[this.summaries.length - 1];
      context += `【前 ${latestSummary.upToRound} 轮讨论摘要】\n${latestSummary.summary}\n\n`;
    }

    // 2. 添加滑动窗口内的完整对话
    context += '【近期对话】\n';
    for (const round of this.currentWindow) {
      const marker = round.speaker === participantName ? '（你的发言）' : '';
      context += `[第${round.round}轮] ${round.speaker}${marker}: ${round.content}\n\n`;
    }

    // [FIX] 如果上下文超长，强制触发压缩
    if (context.length > MAX_CONTEXT_CHARS) {
      console.warn(`⚠️ 上下文超长 (${context.length} chars)，强制压缩`);
      
      // 截断到安全长度，保留摘要 + 最近2轮
      const summaryPart = this.summaries.length > 0 
        ? this.summaries[this.summaries.length - 1].summary 
        : '';
      const recentPart = this.currentWindow.slice(-2).map(r => 
        `[第${r.round}轮] ${r.speaker}: ${r.content}`
      ).join('\n\n');
      
      context = `【讨论摘要】\n${summaryPart}\n\n【最近对话】\n${recentPart}\n\n[上下文已截断]`;
    }

    return context;
  }

  /**
   * 获取用于生成摘要的原始文本
   * @returns {string} 需要被摘要的对话文本
   */
  getTextForSummarization() {
    const lastSummaryRound = this.summaries.length > 0
      ? this.summaries[this.summaries.length - 1].upToRound
      : 0;

    const unsummarized = this.fullHistory.filter(r => r.round > lastSummaryRound);
    return unsummarized.map(r => `[第${r.round}轮] ${r.speaker}: ${r.content}`).join('\n');
  }

  /**
   * 检查是否需要生成新的摘要
   * @returns {boolean}
   */
  needsSummarization() {
    const lastSummaryRound = this.summaries.length > 0
      ? this.summaries[this.summaries.length - 1].upToRound
      : 0;
    const currentRound = this.fullHistory.length > 0
      ? this.fullHistory[this.fullHistory.length - 1].round
      : 0;

    return (currentRound - lastSummaryRound) >= this.summarizeEvery;
  }

  /**
   * 获取完整历史（用于最终报告）
   * @returns {Array}
   */
  getFullHistory() {
    return [...this.fullHistory];
  }

  /**
   * 获取 Token 使用估算
   * @returns {object} { windowTokens, fullTokens, savings }
   */
  getTokenEstimate() {
    const estimateTokens = (text) => Math.ceil(text.length / 2); // 中文约 2 字符/token

    const fullText = this.fullHistory.map(r => r.content).join('');
    const windowText = this.currentWindow.map(r => r.content).join('');
    const summaryText = this.summaries.map(s => s.summary).join('');

    const fullTokens = estimateTokens(fullText);
    const windowTokens = estimateTokens(windowText + summaryText);
    const savings = fullTokens > 0 ? ((1 - windowTokens / fullTokens) * 100).toFixed(1) : 0;

    return {
      fullTokens,
      windowTokens,
      savings: `${savings}%`
    };
  }

  /**
   * 重置
   */
  reset() {
    this.fullHistory = [];
    this.summaries = [];
    this.currentWindow = [];
    this.participantContexts = {};
  }
}

module.exports = ContextManager;
