/**
 * 虚拟论坛 - 子代理交锋引擎
 * Subagent Arena v3.5 (重构版)
 * 
 * 修复：
 * - [P1] 移除硬编码路径 /Users/caoyirong
 * - [P1] 增加输入验证和错误处理
 * - [P1] 集成 ContextManager 解决上下文膨胀
 * - [P2] 使用 shared-config 消除重复代码
 * 改进：
 * - 支持指数退避重试
 * - 支持流式进度回调
 * - 支持中途暂停/恢复
 */

const path = require('path');
const fs = require('fs');
const {
  getDefaultSkillsDir,
  DISCUSSION_MODES,
  MODERATOR_STYLES,
  DEFAULTS,
  loadSkill,
  validateConfig,
  exponentialBackoff
} = require('./shared-config.js');
const ContextManager = require('./context-manager.js');

const ArgumentTracker = require('./argument-tracker.js');

class SubagentArena {
  constructor(skillsDir = null) {
    this.skillsDir = skillsDir || getDefaultSkillsDir();
    this.arena = null;
    this.debaterSessions = {};
    this.contextManager = null;
    this.isPaused = false;
    this.isAborted = false;  // [FIX] 添加abort标志
    this.abortController = null;  // [FIX] 用于graceful shutdown
    this.onRoundComplete = null; // 进度回调钩子
    this.argumentTracker = new ArgumentTracker(); // [v3.5.2 FIX] 集成论点追踪器
    
    // [FIX] 设置信号处理，实现graceful shutdown
    this._setupSignalHandlers();
  }

  /**
   * [FIX] 设置信号处理器，实现graceful shutdown
   */
  _setupSignalHandlers() {
    // 仅在主进程（非测试环境）设置
    if (process.env.NODE_ENV !== 'test' && typeof process.on === 'function') {
      const handleAbort = () => {
        console.log('\n⚠️ 收到中断信号，正在优雅关闭...');
        this.abort();
      };
      process.on('SIGINT', handleAbort);
      process.on('SIGTERM', handleAbort);
    }
  }

  /**
   * [FIX] 中断辩论（优雅关闭）
   */
  abort() {
    this.isAborted = true;
    this.isPaused = false;  // 不再暂停，直接停止
    if (this.abortController) {
      this.abortController.abort();
    }
    console.log('⚠️ 辩论已中断');
  }

  /**
   * 加载Skill内容（使用共享函数）
   */
  async loadSkill(skillName) {
    return loadSkill(this.skillsDir, skillName);
  }

  /**
   * 初始化竞技场
   */
  async initArena(config) {
    // [P1 FIX] 输入验证
    validateConfig(config);

    const {
      topic,
      mode = DEFAULTS.mode,
      rounds = DEFAULTS.rounds,
      participants = [],
      moderatorName = DEFAULTS.moderatorName,
      moderatorSkill = DEFAULTS.moderatorSkill,
      moderatorStyle = DEFAULTS.moderatorStyle,
      contextWindowSize,
      summarizeEveryNRounds
    } = config;

    // 初始化上下文管理器
    this.contextManager = new ContextManager({
      windowSize: contextWindowSize || DEFAULTS.contextWindowSize,
      summarizeEvery: summarizeEveryNRounds || DEFAULTS.summarizeEveryNRounds
    });

    this.arena = {
      id: Date.now(),
      topic,
      mode,
      rounds,
      participants: [...participants],
      moderatorName,
      moderatorSkill,
      moderatorStyle,
      status: 'initializing',
      debateHistory: [],
      scores: {},
      results: {}
    };

    // 初始化分数
    for (const p of participants) {
      this.arena.scores[p.name] = 0;
    }

    // 加载所有Skill
    console.log('📚 加载Skills...');
    let loadFailures = 0;
    for (const p of participants) {
      p.skillContent = await this.loadSkill(p.skillName);
      if (p.skillContent) {
        console.log(` ✓ ${p.name}`);
      } else {
        console.warn(` ✗ ${p.name} (Skill 加载失败，将使用空背景)`);
        loadFailures++;
      }
    }

    // [FIX] 如果所有Skill都加载失败，抛出错误而非继续
    if (loadFailures === participants.length) {
      const errMsg = '所有参与者的Skill都加载失败，辩论无法进行。请检查skillName是否正确。';
      console.error(`❌ ${errMsg}`);
      throw new Error(errMsg);
    }
    
    // 如果部分失败，给出警告但继续
    if (loadFailures > 0) {
      console.warn(`⚠️ ${loadFailures}/${participants.length} 个Skill加载失败，辩论质量可能受影响`);
    }

    if (moderatorSkill) {
      this.arena.moderatorSkillContent = await this.loadSkill(moderatorSkill);
      if (this.arena.moderatorSkillContent) {
        console.log(` ✓ 主持人 ${moderatorName}`);
      } else {
        console.warn(` ⚠️ 主持人 ${moderatorName} (Skill加载失败，将使用通用主持风格)`);
      }
    }

    this.arena.status = 'ready';
    return this.arena;
  }

  /**
   * 构建辩论者系统提示（使用共享模式定义）
   */
  buildDebaterSystemPrompt(participant) {
    const modeConfig = DISCUSSION_MODES[this.arena.mode] || DISCUSSION_MODES.adversarial;

    return `你是${participant.name}。

背景资料：
${participant.skillContent || '（无可用背景）'}

讨论话题：${this.arena.topic}

讨论模式：${modeConfig.instruction}

你的任务：
1. 用第一人称表达你的观点
2. 体现你的性格、思维方式和表达风格
3. 可以向对方提问或质疑
4. 必要时引用具体数据或案例
5. 每次发言控制在 ${DEFAULTS.minResponseLength}-${DEFAULTS.maxResponseLength} 字

重要：
- 保持角色一致性
- 不要重复已经说过的观点
- 针对对方最新发言做出回应`;
  }

  /**
   * 运行辩论（带重试和进度回调）
   */
  async runDebate() {
    if (!this.arena || this.arena.status !== 'ready') {
      throw new Error('竞技场未初始化，请先调用 initArena()');
    }

    this.arena.status = 'running';
    console.log(`\n🎭 辩论开始: ${this.arena.topic}`);
    console.log(` 模式: ${DISCUSSION_MODES[this.arena.mode]?.name || this.arena.mode}`);
    console.log(` 轮次: ${this.arena.rounds}\n`);

    for (let round = 1; round <= this.arena.rounds && !this.isAborted; round++) {
      // 检查暂停（但abort优先级更高）
      while (this.isPaused && !this.isAborted) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
      
      // 如果被中断，退出循环
      if (this.isAborted) break;

      console.log(`--- 第 ${round}/${this.arena.rounds} 轮 ---`);

      for (const participant of this.arena.participants) {
        // 获取压缩后的上下文（而非完整历史）
        const context = this.contextManager.getContextForParticipant(participant.name);

        let response = null;
        // [P1 FIX] 指数退避重试
        for (let attempt = 0; attempt < DEFAULTS.apiRetryAttempts; attempt++) {
          try {
            response = await this.getDebaterResponse(participant, context);
            break;
          } catch (e) {
            console.warn(` ⚠️ ${participant.name} 第 ${attempt + 1} 次调用失败: ${e.message}`);
            if (attempt < DEFAULTS.apiRetryAttempts - 1) {
              await exponentialBackoff(attempt);
            } else {
              console.error(` ❌ ${participant.name} 调用彻底失败，跳过本轮`);
              response = `（${participant.name} 本轮未能发言）`;
            }
          }
        }

        // 记录到上下文管理器
        this.contextManager.addRound({
          round,
          speaker: participant.name,
          content: response,
          type: 'statement'
        });

        // [v3.5.2 FIX] 记录到论点追踪器
        this.argumentTracker.addArgument(participant.name, response, 'statement', round);

        this.arena.debateHistory.push({
          round,
          speaker: participant.name,
          content: response,
          timestamp: Date.now()
        });
      }

      // 检查是否需要生成摘要（节省 Token）
      if (this.contextManager.needsSummarization()) {
        console.log(` 📝 生成历史摘要（节省 Token）...`);
        const textToSummarize = this.contextManager.getTextForSummarization();
        try {
          const summary = await this.generateSummary(textToSummarize);
          this.contextManager.addSummary(summary, round);
        } catch (e) {
          console.warn(` ⚠️ 摘要生成失败: ${e.message}`);
        }
      }

      // 进度回调
      if (typeof this.onRoundComplete === 'function') {
        this.onRoundComplete(round, this.arena.debateHistory.slice(-this.arena.participants.length));
      }

      // Token 使用估算
      const tokenEst = this.contextManager.getTokenEstimate();
      console.log(` 💰 Token 节省: ${tokenEst.savings}`);
    }

    // [FIX] 处理中断退出
    if (this.isAborted) {
      console.log('⚠️ 辩论被中断');
      this.arena.status = 'aborted';
    } else {
      this.arena.status = 'completed';
      console.log(`\n✅ 辩论结束`);
    }
    
    return this.arena;
  }

  /**
   * 获取辩论者回复（子代理调用 - 需要对接实际 API）
   * @abstract 子类或调用者需要实现具体的 API 调用
   * 
   * [P0 FIX] 添加超时保护，防止无限阻塞
   */
  async getDebaterResponse(participant, context, options = {}) {
    const timeoutMs = options.timeoutMs || 30000; // 默认30秒超时
    
    // 这里是子代理调用的占位符
    // 实际使用时需要对接 OpenClaw 的 sessions_spawn / sessions_send
    // 或者调用其他 LLM API
    
    // [P0 FIX] 抛出一个需要实现的错误，并提供超时说明
    throw new Error(
      `getDebaterResponse 需要实现具体的API调用。` +
      `timeoutMs=${timeoutMs}ms 已配置。` +
      `请在子类中实现或通过依赖注入提供具体调用逻辑。`
    );
  }

  /**
   * 安全调用API（带超时保护）
   * [P0 FIX] 新增方法：防止API调用无限阻塞
   * 
   * @param {Function} apiCall - 要调用的异步函数
   * @param {number} timeoutMs - 超时毫秒数
   * @param {string} errorMessage - 超时时错误消息
   * @returns {Promise} API调用结果或超时错误
   */
  async safeApiCall(apiCall, timeoutMs = 30000, errorMessage = 'API调用超时') {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
      console.warn(`⚠️ API调用超时 (${timeoutMs}ms)`);
    }, timeoutMs);
    
    try {
      // 如果apiCall接受signal参数，传递给它
      if (typeof apiCall === 'function') {
        // 包装函数，添加timeout
        const wrappedApiCall = async () => {
          try {
            const result = await Promise.race([
              apiCall(),
              new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Timeout')), timeoutMs)
              )
            ]);
            return result;
          } catch (e) {
            if (e.name === 'AbortError' || e.message === 'Timeout') {
              throw new Error(errorMessage);
            }
            throw e;
          }
        };
        
        const result = await wrappedApiCall();
        clearTimeout(timeoutId);
        return result;
      }
      return await apiCall();
    } catch (e) {
      clearTimeout(timeoutId);
      if (e.name === 'AbortError' || e.message.includes('Timeout')) {
        throw new Error(`${errorMessage} (${timeoutMs}ms)`);
      }
      throw e;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * 生成摘要（需要对接实际 API）
   * @abstract
   * 
   * [FIX] 实现默认的简单摘要，避免抛出错误导致流程中断
   * 在无LLM API情况下，使用简单的提取式摘要作为降级方案
   */
  async generateSummary(text) {
    // 简单提取式摘要：提取关键句子
    const sentences = text.split(/[。！？\n]/).filter(s => s.trim().length > 10);
    
    if (sentences.length === 0) {
      return '(本轮无实质内容，无需摘要)';
    }
    
    // 简单策略：取前3句 + 最后1句（如果有更多的话）
    const keySentences = [];
    
    if (sentences.length > 0) {
      keySentences.push(sentences[0]); // 第一句通常最重要
    }
    if (sentences.length > 4) {
      // 中间随机选一句
      const midIdx = Math.floor(sentences.length / 2);
      keySentences.push(sentences[midIdx]);
    }
    if (sentences.length > 2) {
      keySentences.push(sentences[sentences.length - 1]); // 最后一句通常是结论
    }
    
    // 如果只有很少的句子，全部包含
    if (keySentences.length < 3 && sentences.length <= 3) {
      keySentences.push(...sentences.slice(1, -1).filter(s => !keySentences.includes(s)));
    }
    
    const summary = keySentences.join('。') + '。';
    const speakerCount = (text.match(/\】/g) || []).length;
    
    return `[提取式摘要] 本轮讨论涉及${speakerCount}位发言者，主要观点：${summary}`;
  }

  /**
   * 暂停辩论
   */
  pause() {
    this.isPaused = true;
    console.log('⏸️ 辩论已暂停');
  }

  /**
   * 恢复辩论
   */
  resume() {
    this.isPaused = false;
    console.log('▶️ 辩论已恢复');
  }

  /**
   * 格式化输出
   */
  formatOutput(formatType = 'dialogue') {
    if (!this.arena) return '';

    switch (formatType) {
      case 'dialogue':
        return this.arena.debateHistory
          .map(h => `【${h.speaker}】(第${h.round}轮)\n${h.content}`)
          .join('\n\n---\n\n');
      case 'json':
        return JSON.stringify(this.arena, null, 2);
      default:
        return this.arena.debateHistory
          .map(h => `${h.speaker}: ${h.content}`)
          .join('\n\n');
    }
  }
}

module.exports = SubagentArena;
