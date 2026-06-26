/**
 * System 2 Engine - 深度反思推理引擎
 * 
 * 特点：
 * - 高延迟 (~10-15s)
 * - 多迭代 (最多 15 次)
 * - 带 Reflexion 自我反思机制
 * - 适合复杂规划、多步推理、战略决策
 * 
 * 基于 ReAct + Reflexion 循环：
 * Reason → Act → Observe → Reflect → Retry/Continue
 */

class System2Engine {
  constructor(options = {}) {
    this.config = {
      model: options.model ?? 'qwen3.5-plus',
      temperature: options.temperature ?? 0.7, // 高温度，更创造性
      // Reflexion 配置
      reflectionThreshold: options.reflectionThreshold ?? 3, // 每 N 次迭代反思一次
      maxReflections: options.maxReflections ?? 3, // 最多反思次数
    };
  }

  /**
   * 执行 System 2 ReAct + Reflexion 循环
   */
  async run(query, context) {
    const { toolRegistry, timeout, maxIterations, verbose } = context;
    const history = [];
    const reflections = [];
    const startTime = Date.now();

    // 设置超时
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`System 2 超时 (${timeout}s)`)), timeout * 1000);
    });

    const executionPromise = this._executeLoop(query, toolRegistry, history, reflections, maxIterations, verbose);

    try {
      return await Promise.race([executionPromise, timeoutPromise]);
    } catch (error) {
      if (error.message.includes('超时')) {
        return {
          answer: `⚠️ System 2 执行超时 (${timeout}s)，任务过于复杂，建议分解为多个子任务。`,
          history,
          reflections,
          iterations: history.length,
          timedOut: true,
        };
      }
      throw error;
    }
  }

  async _executeLoop(query, toolRegistry, history, reflections, maxIterations, verbose) {
    let currentQuery = query;
    let plan = null;

    // 初始规划阶段
    if (verbose) {
      console.log('[System 2] 📋 初始规划阶段...');
    }
    plan = await this._createPlan(query, toolRegistry);
    if (verbose) {
      console.log(`[System 2] 规划：${plan.summary}`);
    }

    for (let iteration = 0; iteration < maxIterations; iteration++) {
      if (verbose) {
        console.log(`[System 2] 迭代 ${iteration + 1}/${maxIterations}`);
      }

      // REFLECTION: 定期反思（每 N 次迭代或遇到错误时）
      const shouldReflect = 
        (iteration + 1) % this.config.reflectionThreshold === 0 ||
        (history.length > 0 && typeof history[history.length - 1].observation === 'string' && history[history.length - 1].observation?.includes('❌'));

      if (shouldReflect && reflections.length < this.config.maxReflections) {
        if (verbose) {
          console.log(`[System 2] 🤔 反思阶段 (${reflections.length + 1}/${this.config.maxReflections})...`);
        }

        const reflection = await this._reflect(query, history, plan);
        reflections.push(reflection);

        if (verbose) {
          console.log(`[System 2] 反思洞察：${reflection.insights.join('; ')}`);
        }

        // 根据反思调整计划
        if (reflection.shouldReplan) {
          plan = await this._createPlan(query, toolRegistry, reflection);
          if (verbose) {
            console.log(`[System 2] 📝 计划已调整：${plan.summary}`);
          }
        }

        // 如果反思认为已足够，提前结束
        if (reflection.isComplete) {
          if (verbose) {
            console.log('[System 2] ✅ 反思确认完成');
          }
          return {
            answer: await this._synthesizeFinalAnswer(query, history, reflections),
            history,
            reflections,
            iterations: iteration + 1,
          };
        }
      }

      // REASON: 思考下一步（考虑当前计划）
      const thought = await this._reason(currentQuery, history, toolRegistry, plan, reflections);

      if (verbose) {
        console.log(`[System 2] 思考：${thought.summary}`);
      }

      // 判断是否已有足够信息给出答案
      if (thought.action === 'FINAL_ANSWER') {
        return {
          answer: thought.answer,
          history,
          reflections,
          iterations: iteration + 1,
        };
      }

      // ACT: 执行工具
      const tool = toolRegistry.get(thought.toolName);
      if (!tool) {
        return {
          answer: `❌ 未知工具：${thought.toolName}。可用工具：${toolRegistry.list().join(', ')}`,
          history,
          reflections,
          iterations: iteration + 1,
        };
      }

      let observation;
      try {
        observation = await tool.fn(thought.params);
        if (verbose) {
          console.log(`[System 2] 工具 ${thought.toolName} 执行完成`);
        }
      } catch (error) {
        observation = `❌ 工具执行失败：${error.message}`;
        if (verbose) {
          console.log(`[System 2] 工具执行失败：${error.message}`);
        }
      }

      // OBSERVE: 记录观察
      history.push({
        iteration: iteration + 1,
        thought: thought.summary,
        action: thought.toolName,
        params: thought.params,
        observation,
        timestamp: Date.now(),
        planStep: plan?.steps?.[iteration],
      });

      // 更新查询上下文
      currentQuery = this._buildContext(query, history, reflections, plan);
    }

    // 达到最大迭代次数，强制给出答案
    return {
      answer: await this._synthesizeFinalAnswer(query, history, reflections),
      history,
      reflections,
      iterations: maxIterations,
      maxIterationsReached: true,
    };
  }

  /**
   * 创建初始计划
   */
  async _createPlan(query, toolRegistry, reflection = null) {
    // 简化实现：基于关键词生成计划
    // 实际应调用 LLM 进行规划

    const steps = [];
    
    // 检测任务类型
    if (/搜索 | 查找 | 调研/i.test(query)) {
      steps.push('搜索相关信息');
      steps.push('筛选重要结果');
      steps.push('整理总结');
    } else if (/代码 | 编程 | 脚本/i.test(query)) {
      steps.push('分析需求');
      steps.push('编写代码');
      steps.push('测试验证');
    } else if (/分析 | 比较 | 评估/i.test(query)) {
      steps.push('收集信息');
      steps.push('对比分析');
      steps.push('得出结论');
    } else {
      steps.push('理解问题');
      steps.push('执行操作');
      steps.push('返回结果');
    }

    return {
      summary: `${steps.length}步计划：${steps.join(' → ')}`,
      steps,
      createdAt: Date.now(),
      adjustedFrom: reflection ? reflection.adjustedFrom : null,
    };
  }

  /**
   * REFLECT 阶段：反思当前进展
   */
  async _reflect(query, history, plan) {
    const insights = [];
    let shouldReplan = false;
    let isComplete = false;
    let adjustedFrom = null;

    // 分析历史
    const failures = history.filter(h => typeof h.observation === 'string' && h.observation?.includes('❌'));
    const successes = history.filter(h => typeof h.observation !== 'string' || !h.observation?.includes('❌'));

    // 洞察 1: 错误模式检测
    if (failures.length >= 2) {
      insights.push(`检测到 ${failures.length} 次工具执行失败，可能需要调整策略`);
      shouldReplan = true;
      adjustedFrom = plan?.summary;
    }

    // 洞察 2: 进展评估
    if (successes.length >= 3) {
      insights.push(`已积累 ${successes.length} 次成功执行，信息充足`);
      isComplete = true;
    }

    // 洞察 3: 计划偏离检测
    if (plan && history.length > 0) {
      const executedTools = history.map(h => h.action);
      const planMismatch = plan.steps.some((step, i) => {
        const tool = executedTools[i];
        return tool && !step.includes(tool);
      });
      if (planMismatch) {
        insights.push('实际执行与计划有偏离，考虑调整');
        shouldReplan = true;
        adjustedFrom = plan?.summary;
      }
    }

    // 洞察 4: 冗余检测
    if (history.length >= 5) {
      const uniqueTools = new Set(history.map(h => h.action));
      if (uniqueTools.size < history.length / 2) {
        insights.push('工具使用重复度高，可能需要新方向');
        shouldReplan = true;
        adjustedFrom = plan?.summary;
      }
    }

    return {
      insights,
      shouldReplan,
      isComplete,
      adjustedFrom,
      timestamp: Date.now(),
    };
  }

  /**
   * REASON 阶段：思考下一步（考虑计划和反思）
   */
  async _reason(query, history, toolRegistry, plan, reflections) {
    const availableTools = toolRegistry.list();

    // 如果有足够历史，倾向于给出答案
    if (history.length >= 5) {
      const synthesized = await this._synthesizeFinalAnswer(query, history, reflections);
      return {
        summary: '已有充分执行历史，合成最终答案',
        action: 'FINAL_ANSWER',
        answer: synthesized,
      };
    }

    // 基于计划选择下一步工具
    if (plan && plan.steps && history.length < plan.steps.length) {
      const currentStep = plan.steps[history.length];
      
      // 简单匹配（实际应使用语义匹配）
      if (/搜索/i.test(currentStep)) {
        if (availableTools.includes('tavily-search')) {
          return {
            summary: `按计划执行：${currentStep}`,
            action: 'tavily-search',
            toolName: 'tavily-search',
            params: { query },
          };
        }
      }
      
      if (/检索 | 笔记 | 知识/i.test(currentStep)) {
        if (availableTools.includes('rag-retrieve')) {
          return {
            summary: `按计划执行：${currentStep}`,
            action: 'rag-retrieve',
            toolName: 'rag-retrieve',
            params: { query },
          };
        }
      }
      
      if (/代码 | 执行/i.test(currentStep)) {
        if (availableTools.includes('powershell-sandbox')) {
          return {
            summary: `按计划执行：${currentStep}`,
            action: 'powershell-sandbox',
            toolName: 'powershell-sandbox',
            params: {},
          };
        }
      }
    }

    // 默认：选择第一个可用工具
    if (availableTools.length > 0) {
      return {
        summary: `使用 ${availableTools[0]} 处理查询`,
        action: availableTools[0],
        toolName: availableTools[0],
        params: {},
      };
    }

    // 无工具可用
    return {
      summary: '无可用工具，基于已有知识回答',
      action: 'FINAL_ANSWER',
      answer: `基于您的查询"${query}"，我没有找到可用的工具。请检查工具注册。`,
    };
  }

  /**
   * 构建完整上下文
   */
  _buildContext(query, history, reflections, plan) {
    let context = `原始查询：${query}\n`;
    
    if (plan) {
      context += `\n计划：${plan.summary}\n`;
    }

    if (reflections.length > 0) {
      context += `\n反思洞察:\n${reflections.map(r => 
        `- ${r.insights.join('; ')}`
      ).join('\n')}\n`;
    }

    if (history.length > 0) {
      context += `\n执行历史:\n${history.map(h => 
        `[${h.iteration}] ${h.action}: ${typeof h.observation === 'string' ? h.observation.substring(0, 100) : JSON.stringify(h.observation)}`
      ).join('\n')}`;
    }

    return context;
  }

  /**
   * 合成最终答案（考虑反思）
   */
  async _synthesizeFinalAnswer(query, history, reflections = []) {
    const parts = [];

    // 反思总结
    if (reflections.length > 0) {
      parts.push(`## 反思过程\n${reflections.map((r, i) => 
        `**反思 ${i + 1}**: ${r.insights.join('; ')}`
      ).join('\n')}\n`);
    }

    // 执行结果
    if (history.length > 0) {
      parts.push(`## 执行结果\n${history.map(h => 
        `**步骤 ${h.iteration}** (${h.action}): ${typeof h.observation === 'string' ? h.observation.substring(0, 150) : JSON.stringify(h.observation)}`
      ).join('\n')}\n`);
    }

    // 最终答案
    parts.push(`## 结论\n针对"${query}"，经过 ${history.length} 步执行和 ${reflections.length} 次反思，完成处理。`);

    return parts.join('\n');
  }
}

module.exports = { System2Engine };
