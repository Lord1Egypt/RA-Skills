/**
 * System 1 Engine - 快速直觉执行引擎
 * 
 * 特点：
 * - 低延迟 (~3-5s)
 * - 少迭代 (最多 5 次)
 * - 适合简单查询、事实检索、单步工具调用
 * 
 * 基于 ReAct 循环：Reason → Action → Observe → Repeat
 */

class System1Engine {
  constructor(options = {}) {
    this.config = {
      model: options.model ?? 'qwen3.5-plus',
      temperature: options.temperature ?? 0.3, // 低温度，更确定
    };
  }

  /**
   * 执行 System 1 ReAct 循环
   */
  async run(query, context) {
    const { toolRegistry, timeout, maxIterations, verbose } = context;
    const history = [];
    const startTime = Date.now();

    // 设置超时
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`System 1 超时 (${timeout}s)`)), timeout * 1000);
    });

    const executionPromise = this._executeLoop(query, toolRegistry, history, maxIterations, verbose, startTime);

    try {
      return await Promise.race([executionPromise, timeoutPromise]);
    } catch (error) {
      if (error.message.includes('超时')) {
        return {
          answer: `⚠️ System 1 执行超时 (${timeout}s)，建议切换到 System 2 深度推理模式。`,
          history,
          iterations: history.length,
          timedOut: true,
        };
      }
      throw error;
    }
  }

  async _executeLoop(query, toolRegistry, history, maxIterations, verbose, startTime) {
    let currentQuery = query;

    for (let iteration = 0; iteration < maxIterations; iteration++) {
      if (verbose) {
        console.log(`[System 1] 迭代 ${iteration + 1}/${maxIterations}`);
      }

      // STEP 1: REASON - 思考下一步
      const thought = await this._reason(currentQuery, history, toolRegistry);

      if (verbose) {
        console.log(`[System 1] 思考：${thought.summary}`);
      }

      // 判断是否已有足够信息给出答案
      if (thought.action === 'FINAL_ANSWER') {
        const duration = ((Date.now() - startTime) / 1000).toFixed(2);
        return {
          answer: thought.answer,
          history,
          iterations: iteration + 1,
          duration: parseFloat(duration),
        };
      }

      // STEP 2: ACT - 执行工具
      const tool = toolRegistry.get(thought.toolName);
      if (!tool) {
        const duration = ((Date.now() - startTime) / 1000).toFixed(2);
        return {
          answer: `❌ 未知工具：${thought.toolName}。可用工具：${toolRegistry.list().join(', ')}`,
          history,
          iterations: iteration + 1,
          duration: parseFloat(duration),
        };
      }

      let observation;
      try {
        observation = await tool.fn(thought.params);
        if (verbose) {
          console.log(`[System 1] 工具 ${thought.toolName} 执行完成`);
        }
      } catch (error) {
        observation = `❌ 工具执行失败：${error.message}`;
        if (verbose) {
          console.log(`[System 1] 工具执行失败：${error.message}`);
        }
      }

      // STEP 3: OBSERVE - 记录观察
      history.push({
        iteration: iteration + 1,
        thought: thought.summary,
        action: thought.toolName,
        params: thought.params,
        observation,
        timestamp: Date.now(),
      });

      // 更新查询上下文
      currentQuery = `${query}\n\n历史上下文:\n${history.map(h => 
        `- [${h.action}] ${h.observation}`
      ).join('\n')}`;
    }

    // 达到最大迭代次数，强制给出答案
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    return {
      answer: await this._synthesizeFinalAnswer(query, history),
      history,
      iterations: maxIterations,
      duration: parseFloat(duration),
      maxIterationsReached: true,
    };
  }

  /**
   * REASON 阶段：分析当前状态，决定下一步行动
   * 
   * 返回格式：
   * {
   *   summary: string,      // 思考摘要
   *   action: 'FINAL_ANSWER' | toolName,
   *   toolName?: string,    // 如果 action 不是 FINAL_ANSWER
   *   params?: object,      // 工具参数
   *   answer?: string       // 如果 action 是 FINAL_ANSWER
   * }
   */
  async _reason(query, history, toolRegistry) {
    // 简化的 Reason 实现（实际应调用 LLM）
    // 这里用启发式规则模拟，后续替换为真实 LLM 调用

    const availableTools = toolRegistry.list();

    // 如果有历史（执行过至少 1 次），倾向于给出最终答案
    if (history.length >= 1) {
      const synthesized = await this._synthesizeFinalAnswer(query, history);
      return {
        summary: '已有足够信息，合成最终答案',
        action: 'FINAL_ANSWER',
        answer: synthesized,
      };
    }

    // 简单关键词匹配选择工具（后续替换为语义匹配）
    const queryLower = query.toLowerCase();
    
    for (const toolName of availableTools) {
      const metadata = toolRegistry.getMetadata(toolName);
      if (metadata.keywords?.some(kw => queryLower.includes(kw.toLowerCase()))) {
        // 提取参数（简化版：从查询中提取关键信息）
        const params = this._extractParams(query, metadata.paramSchema, toolName);
        return {
          summary: `使用 ${toolName} 处理查询`,
          action: toolName,
          toolName,
          params,
        };
      }
    }

    // 没有匹配工具，直接回答
    return {
      summary: '无匹配工具，基于已有知识回答',
      action: 'FINAL_ANSWER',
      answer: `基于您的查询"${query}"，我没有找到匹配的工具。可用工具：${availableTools.join(', ')}。请提供更多细节或换一种问法。`,
    };
  }

  /**
   * 合成最终答案
   */
  async _synthesizeFinalAnswer(query, history) {
    if (history.length === 0) {
      return '暂无执行历史，无法合成答案。';
    }

    const observations = history.map(h => {
      const obs = typeof h.observation === 'string' ? h.observation : JSON.stringify(h.observation);
      return `- [${h.action}] ${obs}`;
    }).join('\n');
    
    return `根据执行结果：\n${observations}\n\n以上是针对"${query}"的处理结果。`;
  }

  /**
   * 提取工具参数（简化版）
   */
  _extractParams(query, paramSchema, toolName) {
    // 简化的参数提取逻辑
    const params = {};
    
    // 计算器参数提取
    if (toolName === 'calculator') {
      const numbers = query.match(/\d+/g);
      if (numbers && numbers.length >= 2) {
        params.a = parseInt(numbers[0]);
        params.b = parseInt(numbers[1]);
        params.op = query.includes('+') ? 'add' : query.includes('*') ? 'mul' : 'add';
      }
    }
    
    // 搜索工具参数提取
    if (toolName === 'tavily-search' || toolName === 'rag-retrieve') {
      params.query = query;
    }
    
    // 文件读取参数提取
    if (toolName === 'file-read') {
      const pathMatch = query.match(/["']([^"']+)["']/);
      params.path = pathMatch ? pathMatch[1] : 'unknown.txt';
    }
    
    return params;
  }
}

module.exports = { System1Engine };
