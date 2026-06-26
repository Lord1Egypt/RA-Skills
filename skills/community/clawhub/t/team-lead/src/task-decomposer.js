/**
 * Team Lead - Task Decomposer
 * 将复杂任务拆解为可分配的子任务
 */

export class TaskDecomposer {
  constructor() {
    this.templates = this.loadTemplates();
  }

  /**
   * 加载预定义任务模板
   */
  loadTemplates() {
    return {
      research: {
        pattern: /研究 | 分析 | 报告 | 调研 | 市场 | 调查/i,
        steps: [
          { type: 'search', agentType: 'search', parallel: true, label: '信息搜索' },
          { type: 'analyze', agentType: 'analysis', parallel: false, label: '数据分析', dependsOn: ['search'] },
          { type: 'summarize', agentType: 'writing', parallel: false, label: '报告撰写', dependsOn: ['analyze'] }
        ]
      },

      coding: {
        pattern: /代码 | 开发 | 功能 | 修复|bug| 实现 | 编程 | 软件/i,
        steps: [
          { type: 'plan', agentType: 'planning', parallel: false, label: '需求分析' },
          { type: 'implement', agentType: 'coding', parallel: false, label: '代码实现', dependsOn: ['plan'] },
          { type: 'review', agentType: 'review', parallel: true, label: '代码审查', dependsOn: ['implement'] },
          { type: 'test', agentType: 'testing', parallel: true, label: '测试用例', dependsOn: ['implement'] }
        ]
      },

      content: {
        pattern: /写作 | 文章 | 内容 | 翻译 | 文案 | 博客 | 邮件/i,
        steps: [
          { type: 'outline', agentType: 'planning', parallel: false, label: '大纲规划' },
          { type: 'draft', agentType: 'writing', parallel: false, label: '初稿撰写', dependsOn: ['outline'] },
          { type: 'edit', agentType: 'editing', parallel: true, label: '编辑润色', dependsOn: ['draft'] },
          { type: 'factcheck', agentType: 'review', parallel: true, label: '事实核查', dependsOn: ['draft'] }
        ]
      },

      translation: {
        pattern: /翻译 | 本地化 | 多语言/i,
        steps: [
          { type: 'translate', agentType: 'translation', parallel: true, label: '翻译' },
          { type: 'review', agentType: 'editing', parallel: false, label: '校对', dependsOn: ['translate'] }
        ]
      },

      design: {
        pattern: /设计 | 创意 | 视觉 | 图像 | 界面|ui|ux/i,
        steps: [
          { type: 'brief', agentType: 'planning', parallel: false, label: '需求梳理' },
          { type: 'concept', agentType: 'design', parallel: true, label: '概念设计', dependsOn: ['brief'] },
          { type: 'refine', agentType: 'design', parallel: false, label: '细化完善', dependsOn: ['concept'] },
          { type: 'feedback', agentType: 'review', parallel: true, label: '反馈收集', dependsOn: ['refine'] }
        ]
      },

      learning: {
        pattern: /学习 | 教程 | 解释 | 教学 | 培训 | 课程/i,
        steps: [
          { type: 'assess', agentType: 'planning', parallel: false, label: '水平评估' },
          { type: 'curate', agentType: 'research', parallel: true, label: '资料整理', dependsOn: ['assess'] },
          { type: 'explain', agentType: 'teaching', parallel: false, label: '讲解说明', dependsOn: ['curate'] },
          { type: 'exercise', agentType: 'teaching', parallel: true, label: '练习设计', dependsOn: ['explain'] }
        ]
      }
    };
  }

  /**
   * 分解任务
   */
  decompose(task, context = {}) {
    console.log(`[TaskDecomposer] Decomposing task: ${task.substring(0, 50)}...`);

    // 1. 尝试匹配模板
    const template = this.matchTemplate(task);
    
    if (template) {
      console.log(`[TaskDecomposer] Matched template: ${template.name}`);
      return this.createFromTemplate(template, task, context);
    }

    // 2. 无模板时使用启发式分解
    console.log('[TaskDecomposer] Using heuristic decomposition');
    return this.heuristicDecompose(task, context);
  }

  /**
   * 匹配任务模板
   */
  matchTemplate(task) {
    const taskLower = task.toLowerCase();
    
    for (const [name, template] of Object.entries(this.templates)) {
      if (template.pattern.test(task)) {
        return { name, ...template };
      }
    }
    
    return null;
  }

  /**
   * 从模板创建分解结果
   */
  createFromTemplate(template, task, context) {
    const subtasks = template.steps.map((step, index) => {
      const dependencies = step.dependsOn || [];
      const resolvedDeps = dependencies.map(dep => 
        template.steps.find((s, i) => i < index && s.type === dep)?.id || `step-${index - 1}`
      );

      return {
        id: `step-${index}`,
        type: step.type,
        label: step.label,
        suggestedAgentType: step.agentType,
        dependsOn: resolvedDeps,
        parallel: step.parallel,
        priority: this.calculatePriority(step, template.steps),
        input: this.generateInput(task, context, step),
        estimatedTime: this.estimateTime(step.type)
      };
    });

    return {
      originalTask: task,
      template: template.name,
      subtasks,
      executionPlan: this.buildExecutionPlan(subtasks),
      estimatedTotalTime: subtasks.reduce((sum, s) => sum + s.estimatedTime, 0),
      context
    };
  }

  /**
   * 启发式分解（无模板时）
   */
  heuristicDecompose(task, context) {
    // 简单启发式：按任务长度和复杂度分解
    const wordCount = task.split(/\s+/).length;
    
    if (wordCount < 10) {
      // 简单任务，不需要分解
      return {
        originalTask: task,
        template: 'simple',
        subtasks: [{
          id: 'step-0',
          type: 'execute',
          label: '执行任务',
          suggestedAgentType: 'general',
          dependsOn: [],
          parallel: false,
          priority: 1,
          input: { task, context },
          estimatedTime: 60
        }],
        executionPlan: [{ type: 'sequential', tasks: [0] }],
        estimatedTotalTime: 60,
        context
      };
    }

    // 中等复杂度任务
    return {
      originalTask: task,
      template: 'heuristic',
      subtasks: [
        {
          id: 'step-0',
          type: 'analyze',
          label: '任务分析',
          suggestedAgentType: 'planning',
          dependsOn: [],
          parallel: false,
          priority: 1,
          input: { task, context, instruction: '分析任务需求，明确目标' },
          estimatedTime: 30
        },
        {
          id: 'step-1',
          type: 'execute',
          label: '执行任务',
          suggestedAgentType: 'general',
          dependsOn: ['step-0'],
          parallel: false,
          priority: 2,
          input: { task, context, instruction: '根据分析结果执行任务' },
          estimatedTime: 120
        },
        {
          id: 'step-2',
          type: 'review',
          label: '质量检查',
          suggestedAgentType: 'review',
          dependsOn: ['step-1'],
          parallel: false,
          priority: 3,
          input: { task, context, instruction: '检查结果质量' },
          estimatedTime: 30
        }
      ],
      executionPlan: [
        { type: 'sequential', tasks: [0] },
        { type: 'sequential', tasks: [1] },
        { type: 'sequential', tasks: [2] }
      ],
      estimatedTotalTime: 180,
      context
    };
  }

  /**
   * 计算优先级
   */
  calculatePriority(step, allSteps) {
    const dependents = allSteps.filter(s => 
      s.dependsOn?.includes(step.type)
    ).length;
    
    // 被依赖越多的步骤优先级越高
    return 1 + dependents;
  }

  /**
   * 估算执行时间（秒）
   */
  estimateTime(stepType) {
    const estimates = {
      search: 60,
      analyze: 90,
      plan: 45,
      implement: 180,
      review: 60,
      test: 90,
      write: 120,
      edit: 60,
      translate: 90,
      design: 150,
      teach: 120,
      execute: 90
    };
    return estimates[stepType] || 90;
  }

  /**
   * 生成子任务输入
   */
  generateInput(task, context, step) {
    const instructions = {
      search: '搜索相关信息，提供来源链接和关键数据',
      analyze: '分析数据，提取关键洞察和趋势',
      plan: '制定详细计划，包括步骤和时间估算',
      implement: '实现功能，遵循最佳实践和编码规范',
      review: '审查内容，识别问题和改进建议',
      test: '生成全面的测试用例并执行',
      write: '撰写清晰、结构化的内容',
      edit: '优化语言表达，提升可读性',
      translate: '准确翻译，保持原意和语境',
      design: '创建美观、实用的设计方案',
      teach: '清晰讲解，适合目标受众水平'
    };

    return {
      task,
      context,
      stepType: step.type,
      instruction: instructions[step.type] || '完成指定任务',
      outputFormat: this.getOutputFormat(step.type)
    };
  }

  /**
   * 获取推荐输出格式
   */
  getOutputFormat(stepType) {
    const formats = {
      search: 'structured-list',
      analyze: 'insight-report',
      plan: 'step-by-step',
      implement: 'code-with-comments',
      review: 'feedback-list',
      test: 'test-cases',
      write: 'structured-article',
      edit: 'tracked-changes',
      translate: 'parallel-text',
      design: 'visual-description',
      teach: 'lesson-plan'
    };
    return formats[stepType] || 'markdown';
  }

  /**
   * 构建执行计划
   */
  buildExecutionPlan(subtasks) {
    const plan = [];
    const visited = new Set();

    // 拓扑排序 + 并行分组
    const remaining = [...subtasks];
    
    while (remaining.length > 0) {
      // 找出当前可执行的子任务（所有依赖已完成）
      const ready = remaining.filter(s => 
        s.dependsOn.every(dep => visited.has(dep))
      );

      if (ready.length === 0) {
        // 循环依赖检测
        console.warn('[TaskDecomposer] Circular dependency detected!');
        break;
      }

      // 将可并行执行的分组
      const parallelGroup = ready.filter(s => s.parallel);
      const sequentialTasks = ready.filter(s => !s.parallel);

      if (parallelGroup.length > 0) {
        plan.push({
          type: 'parallel',
          tasks: parallelGroup.map(s => subtasks.indexOf(s))
        });
        parallelGroup.forEach(s => visited.add(s.id));
        parallelGroup.forEach(s => {
          const idx = remaining.findIndex(r => r.id === s.id);
          if (idx > -1) remaining.splice(idx, 1);
        });
      }

      // 串行任务逐个执行
      for (const task of sequentialTasks) {
        plan.push({
          type: 'sequential',
          tasks: [subtasks.indexOf(task)]
        });
        visited.add(task.id);
        const idx = remaining.findIndex(r => r.id === task.id);
        if (idx > -1) remaining.splice(idx, 1);
      }
    }

    return plan;
  }

  /**
   * 获取分解统计
   */
  getStats(decomposition) {
    return {
      totalSubtasks: decomposition.subtasks.length,
      parallelGroups: decomposition.executionPlan.filter(p => p.type === 'parallel').length,
      sequentialSteps: decomposition.executionPlan.filter(p => p.type === 'sequential').length,
      estimatedTime: decomposition.estimatedTotalTime,
      template: decomposition.template
    };
  }
}
