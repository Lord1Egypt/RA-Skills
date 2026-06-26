/**
 * 对话分析模块
 * 
 * 负责：
 * 1. 分析用户意图
 * 2. 判断响应优先级
 * 3. 检查回答完整性
 * 4. 评估是否需要思考
 */

class Analyzer {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.intentPatterns = this.buildIntentPatterns();
    this.completenessPatterns = this.buildCompletenessPatterns();
  }

  /**
   * 构建意图识别模式
   */
  buildIntentPatterns() {
    return {
      question: [
        // 中文问题模式 - 更精确
        /^(什么|如何|为什么|哪[里个]|谁|多少|几[点个]|什么时候|何时|怎么办|怎么解决|如何实现|怎么用|怎么操作)/,
        /[？?]$/, // 以问号结尾
        /^请问/, /^问一下/, /^想请教/, /^求助/,
        
        // 英文问题模式
        /^(what|how|why|when|where|who|which|can|could|would|should|is|are|do|does|did)/i,
        /\?$/ // 以问号结尾
      ],
      
      task_request: [
        /^(帮我|请帮我|需要|想要|希望|请求|要求|请)(.+)(一下|个|些)/,
        /^(做|执行|实现|完成|处理|解决|创建|建立|开发|设计|分析|调研|调查|研究|检查|测试)/,
        /^(我要|我需要|我想要|我希望)(.+)/
      ],
      
      feedback: [
        /^(谢谢|感谢|辛苦了|很棒|很好|不错|可以|还行|需要改进|有问题|不对|错了|纠正|多谢)/,
        /^(建议|意见|反馈|评价|评分)/,
        /^(.+)的帮助$/  // "谢谢你的帮助"应该匹配这个
      ],
      
      social: [
        /^(你好|早上好|中午好|晚上好|晚安|再见|拜拜|哈哈|呵呵|嘿嘿|嘻嘻|😊|😂|😄)/,
        /^(最近|最近怎么样|在忙什么|还好吗|吃饭了吗|怎么样|过得怎么样)/,
        /^(.+)好$/,  // "你好"等
        /^(.+)早$/,  // "早"
        /^(.+)安$/   // "晚安"
      ]
    };
  }

  /**
   * 构建完整性检查模式
   */
  buildCompletenessPatterns() {
    return {
      incomplete_thought: [
        /(但是|然而|不过|另外|还有|此外|而且|同时)[，,]\s*$/,
        /(首先|第一|第一步|一、|1\.)\s*$/,
        /^(总的来说|综上所述|总之|最后)[，,]\s*$/
      ],
      
      missing_example: [
        /(例如|比如|举例|例如说|比如说|举个例子|例如：|比如：)[，,]\s*$/,
        /^(下面|以下|接下来)(是|给出|提供|展示)[：:]\s*$/
      ],
      
      unfinished_step: [
        /(步骤|流程|过程|方法|做法|操作)(如下|如下所示|如下：|为：)[\s\S]{0,50}$/,
        /(第一步|第二步|第三步|第四步|第五步)[：:]\s*$/
      ],
      
      partial_answer: [
        /(原因|理由|因素|方面)(有|包括|如下)[：:]\s*$/,
        /(优点|好处|优势|缺点|劣势|不足)(有|包括|如下)[：:]\s*$/
      ]
    };
  }

  /**
   * 分析对话状态
   * @param {Object} conversationState - 对话状态
   */
  async analyze(conversationState) {
    try {
      const analysis = {
        needsResponse: false,
        needsCompletion: false,
        priority: null,
        intent: 'unknown',
        requiresThinking: false,
        details: {}
      };

      // 分析最后发言
      if (conversationState.lastSpeaker === 'user') {
        // 用户最后发言，需要判断是否响应
        analysis.needsResponse = conversationState.timeSince >= 60; // 至少等待1分钟
        
        if (analysis.needsResponse) {
          // 分析用户意图
          analysis.intent = this.analyzeIntent(conversationState.lastMessage.content);
          analysis.priority = this.getPriority(analysis.intent);
          analysis.requiresThinking = this.requiresThinking(conversationState, analysis.intent);
          
          this.logger.info('用户发言分析完成', {
            intent: analysis.intent,
            priority: analysis.priority,
            requiresThinking: analysis.requiresThinking,
            timeSince: conversationState.timeSince + 's'
          });
        }
      } else if (conversationState.lastSpeaker === 'ai') {
        // AI最后发言，需要检查完整性
        analysis.needsCompletion = this.checkCompleteness(conversationState.lastMessage.content).needsCompletion;
        
        if (analysis.needsCompletion) {
          analysis.intent = 'completion_needed';
          analysis.priority = 'p1'; // 补全优先级较高
          
          this.logger.info('AI发言完整性检查', {
            needsCompletion: true,
            reason: 'incomplete_message'
          });
        }
      }

      analysis.details = {
        lastSpeaker: conversationState.lastSpeaker,
        timeSince: conversationState.timeSince,
        messageLength: conversationState.lastMessage?.content?.length || 0
      };

      return analysis;
    } catch (error) {
      this.logger.error('分析对话失败', { error: error.message });
      throw error;
    }
  }

  /**
   * 分析用户意图（改进版，按优先级检查）
   * @param {string} message - 用户消息
   */
  analyzeIntent(message) {
    if (!message || typeof message !== 'string') {
      return 'unknown';
    }

    const cleanMessage = message.trim();
    
    // 按优先级检查意图（从最具体到最一般）
    // 1. 首先检查社交意图（有明确模式）
    for (const pattern of this.intentPatterns.social) {
      if (pattern.test(cleanMessage)) {
        this.logger.debug('识别到社交意图', { pattern: pattern.toString() });
        return 'social';
      }
    }
    
    // 2. 检查反馈意图
    for (const pattern of this.intentPatterns.feedback) {
      if (pattern.test(cleanMessage)) {
        this.logger.debug('识别到反馈意图', { pattern: pattern.toString() });
        return 'feedback';
      }
    }
    
    // 3. 检查问题意图
    for (const pattern of this.intentPatterns.question) {
      if (pattern.test(cleanMessage)) {
        this.logger.debug('识别到问题意图', { pattern: pattern.toString() });
        return 'question';
      }
    }
    
    // 4. 检查任务请求意图
    for (const pattern of this.intentPatterns.task_request) {
      if (pattern.test(cleanMessage)) {
        this.logger.debug('识别到任务请求意图', { pattern: pattern.toString() });
        return 'task_request';
      }
    }

    // 如果没有匹配到特定模式，使用启发式规则
    // 首先检查是否为空消息
    if (cleanMessage.length === 0) {
      return 'unknown';
    }
    
    // 检查是否包含反馈关键词（即使消息较短）
    const feedbackKeywords = ['改进', '建议', '意见', '反馈', '评价', '评分', '问题', '错误', '不对', '纠正', '好用', '很棒', '很好', '不错', '可以'];
    for (const keyword of feedbackKeywords) {
      if (cleanMessage.includes(keyword)) {
        return 'feedback';
      }
    }
    
    // 检查是否包含请求关键词
    const requestWords = ['请', '帮忙', '帮我', '需要', '想要', '希望', '请求', '要求'];
    for (const word of requestWords) {
      if (cleanMessage.includes(word)) {
        return 'task_request';
      }
    }
    
    // 检查是否包含问号
    if (cleanMessage.includes('？') || cleanMessage.includes('?')) {
      return 'question'; // 包含问号很可能是问题
    }
    
    // 短消息很可能是社交
    if (cleanMessage.length < 10) {
      return 'social';
    }

    return 'unknown';
  }

  /**
   * 根据意图获取优先级
   * @param {string} intent - 用户意图
   */
  getPriority(intent) {
    const mapping = this.config.intent_mapping || {};
    return mapping[intent] || 'p1'; // 默认为p1优先级
  }

  /**
   * 判断是否需要思考
   * @param {Object} conversationState - 对话状态
   * @param {string} intent - 用户意图
   */
  requiresThinking(conversationState, intent) {
    // 复杂问题需要思考
    if (intent === 'question') {
      const message = conversationState.lastMessage.content || '';
      const messageLength = message.length;
      
      // 长问题很可能需要思考
      if (messageLength > 100) return true;
      
      // 包含技术术语可能需要思考
      const technicalTerms = ['代码', '程序', '算法', 'API', '数据库', '服务器', '部署', '配置'];
      for (const term of technicalTerms) {
        if (message.includes(term)) return true;
      }
    }
    
    // 任务请求需要思考
    if (intent === 'task_request') {
      return true;
    }
    
    // 历史对话较长可能需要思考上下文
    if (conversationState.historyLength > 20) {
      return true;
    }
    
    return false;
  }

  /**
   * 检查回答完整性
   * @param {string} message - AI消息
   */
  checkCompleteness(message) {
    if (!message || typeof message !== 'string') {
      return { needsCompletion: false, reason: null };
    }

    const cleanMessage = message.trim();
    
    // 检查各种不完整模式
    for (const [patternType, patterns] of Object.entries(this.completenessPatterns)) {
      for (const pattern of patterns) {
        if (pattern.test(cleanMessage)) {
          this.logger.debug('检测到不完整模式', { 
            patternType, 
            pattern: pattern.toString() 
          });
          return { 
            needsCompletion: true, 
            reason: patternType,
            pattern: pattern.toString()
          };
        }
      }
    }

    // 额外的启发式检查
    // 检查消息是否以逗号、顿号等结尾（可能不完整）
    const incompleteEndings = [/[，,]\s*$/, /[；;]\s*$/, /[：:]\s*$/, /[、]\s*$/];
    for (const ending of incompleteEndings) {
      if (ending.test(cleanMessage)) {
        return { needsCompletion: true, reason: 'incomplete_ending' };
      }
    }

    // 检查消息是否太短（可能被截断）
    if (cleanMessage.length < 50 && !cleanMessage.endsWith('。') && !cleanMessage.endsWith('!') && !cleanMessage.endsWith('?') && !cleanMessage.endsWith('.')) {
      return { needsCompletion: true, reason: 'too_short' };
    }

    return { needsCompletion: false, reason: null };
  }

  /**
   * 评估消息复杂度
   * @param {string} message - 消息内容
   */
  assessComplexity(message) {
    if (!message) return 0;
    
    let complexity = 0;
    
    // 长度因素
    complexity += Math.min(message.length / 500, 1.0);
    
    // 技术术语因素
    const technicalTerms = ['函数', '变量', '类', '对象', '接口', '协议', '算法', '数据结构'];
    technicalTerms.forEach(term => {
      if (message.includes(term)) complexity += 0.2;
    });
    
    // 代码块因素
    const codeBlocks = message.match(/```[\s\S]*?```/g) || [];
    complexity += codeBlocks.length * 0.3;
    
    // 列表因素
    const listItems = message.match(/^\s*[-*•]\s+/gm) || [];
    complexity += listItems.length * 0.1;
    
    return Math.min(complexity, 1.0);
  }
}

module.exports = Analyzer;