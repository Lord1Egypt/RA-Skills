/**
 * 响应生成模块
 * 
 * 负责：
 * 1. 生成各种类型的响应
 * 2. 管理响应模板
 * 3. 生成进度汇报
 * 4. 补全不完整的回答
 */

class Responder {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.templates = this.buildTemplates();
  }

  /**
   * 构建响应模板
   */
  buildTemplates() {
    return {
      // 立即响应模板
      immediate_response: [
        "收到，正在为您处理...",
        "好的，我马上帮您查看。",
        "明白了，正在分析您的问题。",
        "正在处理您的请求，请稍等。"
      ],
      
      // 快速响应模板
      quick_response: [
        "正在处理，稍后给您回复。",
        "这个问题我需要查一下，稍等。",
        "正在为您准备答案。",
        "请稍等，我正在处理。"
      ],
      
      // 标准响应模板
      standard_response: [
        "感谢您的反馈，已收到。",
        "好的，我会注意这一点。",
        "明白了，继续处理中。",
        "收到，继续工作。"
      ],
      
      // 延迟响应模板
      delayed_response: [
        "看到了，稍后处理。",
        "好的，记下了。",
        "收到，稍后回复。",
        "明白了，晚些处理。"
      ],
      
      // 补全模板
      completion: [
        "补充说明一下：",
        "接上文继续说明：",
        "补充细节如下：",
        "完整回答应该是："
      ],
      
      // 进度汇报模板
      progress_started: "正在处理【{task}】，已开始执行...",
      progress_working: "正在处理【{task}】，已完成{percent}%，预计还需要{time_left}...",
      progress_completed: "【{task}】已完成！这是结果摘要：{summary}",
      progress_blocked: "执行【{task}】时遇到问题：{issue}，正在尝试解决方案...",
      
      // 检查提醒模板
      check_reminder: [
        "还在处理中，马上就好。",
        "正在全力处理，稍等片刻。",
        "处理中，很快会给您回复。",
        "正在努力解决，请稍候。"
      ],
      
      // 确认模板
      confirmation: [
        "我的理解是否正确？",
        "是这样吗？",
        "请确认一下。",
        "对吗？"
      ]
    };
  }

  /**
   * 生成响应
   * @param {Object} analysis - 分析结果
   */
  async generateResponse(analysis) {
    try {
      let response = null;
      
      if (analysis.intent === 'completion_needed') {
        // 需要补全
        response = await this.generateCompletionResponse(analysis);
      } else if (analysis.needsResponse) {
        // 需要响应
        response = await this.generateNormalResponse(analysis);
      }
      
      if (response) {
        response.timestamp = new Date().toISOString();
        response.priority = analysis.priority;
        response.type = analysis.intent === 'completion_needed' ? 'completion' : 'response';
        
        this.logger.debug('生成响应成功', {
          type: response.type,
          priority: response.priority,
          contentLength: response.content.length
        });
      }
      
      return response;
    } catch (error) {
      this.logger.error('生成响应失败', { error: error.message });
      return null;
    }
  }

  /**
   * 生成普通响应
   * @param {Object} analysis - 分析结果
   */
  async generateNormalResponse(analysis) {
    const templates = this.templates[`${analysis.priority}_response`] || this.templates.standard_response;
    const template = this.selectRandomTemplate(templates);
    
    return {
      content: template,
      requiresThinking: analysis.requiresThinking,
      intent: analysis.intent
    };
  }

  /**
   * 生成补全响应
   * @param {Object} analysis - 分析结果
   */
  async generateCompletionResponse(analysis) {
    const template = this.selectRandomTemplate(this.templates.completion);
    
    // 这里应该调用模型来生成补全内容
    // 暂时返回简单补全
    const completionContent = `${template} 我需要补充完整这个回答，请稍等。`;
    
    return {
      content: completionContent,
      requiresThinking: true,
      intent: 'completion'
    };
  }

  /**
   * 随机选择模板
   * @param {Array} templates - 模板数组
   */
  selectRandomTemplate(templates) {
    if (!Array.isArray(templates) || templates.length === 0) {
      return "收到，正在处理。";
    }
    
    const randomIndex = Math.floor(Math.random() * templates.length);
    return templates[randomIndex];
  }

  /**
   * 生成进度汇报
   * @param {Object} task - 任务信息
   */
  generateProgressReport(task) {
    try {
      const { name, progress, estimatedTime, status, summary, issue } = task;
      
      let template = '';
      let content = '';
      
      switch (status) {
        case 'started':
          template = this.templates.progress_started;
          content = template.replace('{task}', name);
          break;
          
        case 'working':
          template = this.templates.progress_working;
          content = template
            .replace('{task}', name)
            .replace('{percent}', Math.round(progress * 100))
            .replace('{time_left}', estimatedTime || '一段时间');
          break;
          
        case 'completed':
          template = this.templates.progress_completed;
          content = template
            .replace('{task}', name)
            .replace('{summary}', summary || '任务已完成');
          break;
          
        case 'blocked':
          template = this.templates.progress_blocked;
          content = template
            .replace('{task}', name)
            .replace('{issue}', issue || '未知问题');
          break;
          
        default:
          content = `任务【${name}】当前进度：${Math.round(progress * 100)}%`;
      }
      
      const response = {
        content,
        type: 'progress_report',
        task: name,
        progress,
        status,
        timestamp: new Date().toISOString()
      };
      
      this.logger.info('生成进度汇报', {
        task: name,
        progress: Math.round(progress * 100) + '%',
        status
      });
      
      return response;
    } catch (error) {
      this.logger.error('生成进度汇报失败', { error: error.message });
      return {
        content: `任务【${task.name}】正在处理中...`,
        type: 'progress_report',
        task: task.name,
        progress: 0,
        status: 'unknown',
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 生成检查提醒
   * @param {Object} conversationState - 对话状态
   */
  generateCheckReminder(conversationState) {
    const template = this.selectRandomTemplate(this.templates.check_reminder);
    
    return {
      content: template,
      type: 'check_reminder',
      timeSince: conversationState.timeSince,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 生成确认请求
   * @param {Object} context - 上下文信息
   */
  generateConfirmation(context) {
    const template = this.selectRandomTemplate(this.templates.confirmation);
    let content = '';
    
    if (context.summary) {
      content = `您说的是：${context.summary}。${template}`;
    } else {
      content = `关于您刚才说的，${template}`;
    }
    
    return {
      content,
      type: 'confirmation',
      context,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 格式化时间估计
   * @param {number} seconds - 秒数
   */
  formatTimeEstimate(seconds) {
    if (seconds < 60) {
      return `${seconds}秒`;
    } else if (seconds < 3600) {
      return `${Math.floor(seconds / 60)}分钟`;
    } else if (seconds < 86400) {
      return `${Math.floor(seconds / 3600)}小时`;
    } else {
      return `${Math.floor(seconds / 86400)}天`;
    }
  }

  /**
   * 根据优先级获取响应延迟
   * @param {string} priority - 优先级
   */
  getResponseDelay(priority) {
    const delays = {
      p0: 0,      // 立即
      p1: 5000,   // 5秒
      p2: 15000,  // 15秒
      p3: 30000   // 30秒
    };
    
    return delays[priority] || delays.p2;
  }

  /**
   * 生成思考中提示
   */
  generateThinkingIndicator() {
    const indicators = [
      "🤔 思考中...",
      "💭 正在分析...",
      "🧠 处理中...",
      "🔍 查找信息中..."
    ];
    
    const randomIndex = Math.floor(Math.random() * indicators.length);
    return indicators[randomIndex];
  }
}

module.exports = Responder;