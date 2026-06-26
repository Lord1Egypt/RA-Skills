/**
 * 【畅聊守护者】ChatFlow Guardian - 智能对话管理技能
 * 
 * 核心功能：确保你的对话永远不会中断！
 * 智能监控对话状态，确保用户的消息永远不会是最后一条
 * 
 * 三大增强功能：
 * 1. Multi-platform Support - Compatible with QQBot, WeCom, Slack, DingTalk, etc.
 * 2. Predictive Response - Predict user needs based on history, prepare answers in advance
 * 3. Deep Learning Optimization - Neural networks improve intent recognition accuracy
 * 
 * English: ChatFlow Guardian - Keep your conversations flowing smoothly!
 */

const Monitor = require('./monitor');
const Analyzer = require('./analyzer');
const Responder = require('./responder');
const Optimizer = require('./optimizer');
const Logger = require('./logger');
const PlatformManager = require('./platforms');
const PredictiveEngine = require('./predictive');
const DeepLearningOptimizer = require('./deeplearning');
const Config = require('../config/default.json');

class DialogManager {
  constructor(config = Config) {
    this.config = config;
    this.logger = new Logger(config.logging);
    
    // 核心功能模块
    this.monitor = new Monitor(config.monitoring, this.logger);
    this.analyzer = new Analyzer(config.response_priority, this.logger);
    this.responder = new Responder(config.progress_reporting, this.logger);
    this.optimizer = new Optimizer(config.token_optimization, this.logger);
    
    // 增强功能模块
    this.platformManager = new PlatformManager(config.platforms || {}, this.logger);
    this.predictiveEngine = new PredictiveEngine(config.predictive || {}, this.logger);
    this.deepLearningOptimizer = new DeepLearningOptimizer(config.deeplearning || {}, this.logger);
    
    this.isRunning = false;
    this.currentSession = null;
    this.platformsInitialized = false;
    this.deepLearningEnabled = config.deeplearning ? config.deeplearning.enabled : false;
  }

  /**
   * 启动对话管理
   * @param {Object} session - 当前会话信息
   */
  async start(session) {
    try {
      this.currentSession = session;
      this.isRunning = true;
      
      this.logger.info('智能对话管理技能启动（增强版）', {
        session: session.id,
        config: this.config.monitoring,
        platforms: this.config.platforms.enabled,
        predictive: this.config.predictive.enabled
      });

      // 初始化平台支持
      if (this.config.platforms.enabled) {
        await this.initializePlatforms();
        this.platformsInitialized = true;
      }

      // 启动监控循环
      await this.startMonitoringLoop();
      
      this.logger.info('技能启动完成', {
        platformsInitialized: this.platformsInitialized,
        predictiveEnabled: this.config.predictive.enabled
      });
      
      return true;
    } catch (error) {
      this.logger.error('启动失败', { error: error.message });
      throw error;
    }
  }

  /**
   * 初始化平台支持
   */
  async initializePlatforms() {
    try {
      this.logger.info('初始化平台支持', { 
        supportedPlatforms: this.config.platforms.supported 
      });
      
      // 初始化默认平台
      const defaultPlatform = this.config.platforms.default_platform;
      if (this.config.platforms.supported.includes(defaultPlatform)) {
        await this.platformManager.initializePlatform(defaultPlatform);
        this.logger.info('默认平台已初始化', { platform: defaultPlatform });
      }
      
      // 记录已初始化的平台
      const platformStatus = this.platformManager.getPlatformStatus();
      this.logger.info('平台初始化完成', { 
        initialized: Object.keys(platformStatus).length,
        platforms: Object.keys(platformStatus) 
      });
      
    } catch (error) {
      this.logger.error('平台初始化失败', { error: error.message });
      throw error;
    }
  }

  /**
   * 停止对话管理
   */
  async stop() {
    this.isRunning = false;
    await this.monitor.stop();
    this.logger.info('智能对话管理技能已停止');
  }

  /**
   * 启动监控循环
   */
  async startMonitoringLoop() {
    // 立即执行一次检查
    await this.checkConversation();
    
    // 设置定时检查
    const interval = Config.monitoring.check_interval * 1000;
    this.monitoringInterval = setInterval(async () => {
      if (this.isRunning) {
        await this.checkConversation();
      }
    }, interval);
  }

  /**
   * 检查对话状态
   */
  async checkConversation() {
    try {
      // 1. 获取当前对话状态
      const conversationState = await this.monitor.getConversationState();
      
      // 2. 如果是安静时段，跳过检查
      if (this.monitor.isQuietTime()) {
        this.logger.debug('安静时段，跳过检查');
        return;
      }
      
      // 3. 分析对话状态
      const analysis = await this.analyzer.analyze(conversationState);
      
      // 4. 如果不需要响应，直接返回
      if (!analysis.needsResponse && !analysis.needsCompletion) {
        return;
      }
      
      // 5. 优化token使用
      const optimized = await this.optimizer.optimize(analysis);
      
      // 6. 生成响应
      const response = await this.responder.generateResponse(optimized);
      
      // 7. 发送响应
      if (response) {
        await this.sendResponse(response);
        
        this.logger.info('已发送响应', {
          type: response.type,
          priority: response.priority,
          token_used: response.tokenCount
        });
      }
    } catch (error) {
      this.logger.error('检查对话状态失败', { error: error.message });
    }
  }

  /**
   * 发送响应消息
   * @param {Object} response - 响应对象
   */
  async sendResponse(response) {
    // 这里应该调用OpenClaw的消息发送API
    // 暂时使用控制台输出模拟
    console.log(`[Dialog Manager] ${new Date().toISOString()} - ${response.content}`);
    
    // 实际实现时：
    // await openclaw.sendMessage(response.content, response.options);
  }

  /**
   * 手动触发进度汇报
   * @param {Object} task - 任务信息
   */
  async reportProgress(task) {
    const report = this.responder.generateProgressReport(task);
    await this.sendResponse(report);
  }

  /**
   * 手动触发对话补全
   * @param {Object} message - 需要补全的消息
   */
  async completeMessage(message) {
    const completion = await this.analyzer.checkCompleteness(message);
    if (completion.needsCompletion) {
      const response = await this.responder.generateCompletion(completion);
      await this.sendResponse(response);
    }
  }

  /**
   * 增强意图识别（结合深度学习）
   * @param {string} message - 用户消息
   * @param {object} context - 上下文信息
   */
  async analyzeIntentEnhanced(message, context = {}) {
    try {
      // 基础意图识别
      const baselineIntent = this.analyzer.analyzeIntent(message);
      
      if (!this.deepLearningEnabled) {
        return {
          intent: baselineIntent,
          confidence: 0.5,
          enhanced: false,
          method: 'baseline'
        };
      }
      
      // 深度学习增强
      const enhancedResult = this.deepLearningOptimizer.enhanceIntentRecognition(
        message,
        context,
        baselineIntent
      );
      
      // 收集训练数据
      if (enhancedResult.enhanced && this.deepLearningOptimizer.dlConfig.trainingEnabled) {
        this.deepLearningOptimizer.collectTrainingData({
          userId: this.currentSession?.userId || 'unknown',
          message,
          intent: baselineIntent,
          predictedIntent: enhancedResult.intent,
          confidence: enhancedResult.confidence,
          responseTime: Date.now() - (context.timestamp || Date.now()),
          context,
          timestamp: Date.now()
        });
      }
      
      return {
        intent: enhancedResult.intent,
        confidence: enhancedResult.confidence,
        enhanced: enhancedResult.enhanced,
        method: enhancedResult.enhanced ? 'deep_learning' : 'baseline',
        baselineIntent,
        modelAccuracy: enhancedResult.modelAccuracy,
        features: enhancedResult.features
      };
      
    } catch (error) {
      this.logger.error('增强意图识别失败', { error: error.message });
      return {
        intent: 'unknown',
        confidence: 0.1,
        enhanced: false,
        method: 'error',
        error: error.message
      };
    }
  }

  /**
   * 预测用户下一个动作（深度学习增强）
   * @param {string} userId - 用户ID
   * @param {array} recentInteractions - 最近的交互历史
   */
  async predictUserNextAction(userId, recentInteractions = []) {
    if (!this.deepLearningEnabled) {
      return null;
    }
    
    try {
      const prediction = this.deepLearningOptimizer.predictNextAction(userId, recentInteractions);
      
      if (prediction) {
        this.logger.debug('用户行为预测', {
          userId,
          predictedIntent: prediction.nextIntent,
          confidence: prediction.confidence
        });
      }
      
      return prediction;
      
    } catch (error) {
      this.logger.error('用户行为预测失败', { error: error.message });
      return null;
    }
  }

  /**
   * 分析对话质量（深度学习增强）
   * @param {array} conversation - 对话记录
   */
  async analyzeConversationQuality(conversation) {
    if (!this.deepLearningEnabled) {
      return { score: 0.5, metrics: {} };
    }
    
    try {
      const qualityAnalysis = this.deepLearningOptimizer.analyzeConversationQuality(conversation);
      
      this.logger.debug('对话质量分析', {
        score: qualityAnalysis.score,
        metricsCount: Object.keys(qualityAnalysis.metrics || {}).length
      });
      
      return qualityAnalysis;
      
    } catch (error) {
      this.logger.error('对话质量分析失败', { error: error.message });
      return { score: 0.5, metrics: {} };
    }
  }

  /**
   * 获取技能状态（增强版）
   */
  getStatus() {
    const baseStatus = {
      isRunning: this.isRunning,
      session: this.currentSession,
      config: {
        check_interval: this.config.monitoring.check_interval,
        response_threshold: this.config.monitoring.response_threshold,
        token_optimization: this.config.token_optimization.enabled
      },
      stats: this.monitor.getStats()
    };
    
    // 添加增强功能状态
    const enhancedStatus = {
      enhanced: {
        platforms: this.config.platforms.enabled,
        predictive: this.config.predictive.enabled,
        deeplearning: this.config.deeplearning.enabled,
        advanced: this.config.advanced.auto_scaling
      },
      platforms: this.platformsInitialized ? 
        this.platformManager.getPlatformStatus() : null,
      predictions: this.config.predictive.enabled ? 
        this.predictiveEngine.getAllStats() : null,
      deeplearning: this.deepLearningEnabled ? 
        this.deepLearningOptimizer.getModelStatus() : null
    };
    
    return { ...baseStatus, ...enhancedStatus };
  }
}

module.exports = DialogManager;