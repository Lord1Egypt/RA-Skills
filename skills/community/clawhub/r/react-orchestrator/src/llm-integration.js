/**
 * LLM Integration Layer - 结构化 Prompt + JSON Schema 输出约束
 * 
 * 基于 2026 最佳实践：
 * - 结构化 Prompting（任务规划 + 逻辑执行 + 工具选择 + Guardrails + 错误处理）
 * - JSON Schema 约束输出格式
 * - Token 优化（上下文压缩）
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

// JSON Schema for ReAct Reason 阶段输出
const REASON_SCHEMA = {
  type: "object",
  required: ["thought", "action"],
  properties: {
    thought: {
      type: "string",
      description: "当前思考过程，分析下一步应该做什么",
      maxLength: 500
    },
    action: {
      type: "string",
      enum: ["FINAL_ANSWER"], // 动态添加工具名称
      description: "选择要执行的动作：FINAL_ANSWER 或工具名称"
    },
    toolName: {
      type: "string",
      description: "如果 action 是工具名称，这里填写工具名"
    },
    params: {
      type: "object",
      description: "工具调用参数",
      additionalProperties: true
    },
    answer: {
      type: "string",
      description: "如果 action 是 FINAL_ANSWER，这里填写最终答案",
      maxLength: 2000
    }
  }
};

// JSON Schema for Planner 输出
const PLANNER_SCHEMA = {
  type: "object",
  required: ["complexity", "plan"],
  properties: {
    complexity: {
      type: "object",
      required: ["level", "score", "reasons"],
      properties: {
        level: { type: "string", enum: ["simple", "medium", "complex"] },
        score: { type: "number", minimum: 0, maximum: 1 },
        reasons: { type: "array", items: { type: "string" } }
      }
    },
    plan: {
      type: "object",
      required: ["steps", "estimatedIterations", "recommendedMode"],
      properties: {
        steps: {
          type: "array",
          items: {
            type: "object",
            required: ["id", "description", "role"],
            properties: {
              id: { type: "integer" },
              description: { type: "string" },
              role: { type: "string", enum: ["planner", "executor", "reviewer"] },
              dependencies: { type: "array", items: { type: "integer" } }
            }
          }
        },
        estimatedIterations: { type: "integer", minimum: 1, maximum: 20 },
        recommendedMode: { type: "string", enum: ["system1", "system2"] }
      }
    }
  }
};

// JSON Schema for Reflexion 输出
const REFLEXION_SCHEMA = {
  type: "object",
  required: ["insights", "shouldReplan", "isComplete"],
  properties: {
    insights: {
      type: "array",
      items: { type: "string" },
      description: "反思得出的洞察"
    },
    shouldReplan: {
      type: "boolean",
      description: "是否需要调整计划"
    },
    isComplete: {
      type: "boolean",
      description: "任务是否已完成"
    },
    adjustedFrom: {
      type: "string",
      description: "如果调整计划，记录原计划摘要"
    },
    confidence: {
      type: "number",
      minimum: 0,
      maximum: 1,
      description: "对当前判断的置信度"
    }
  }
};

/**
 * 结构化 Prompt 模板生成器
 */
class PromptBuilder {
  constructor(options = {}) {
    this.options = {
      // 模型特定优化
      model: options.model || 'qwen3.5-plus',
      // 是否包含示例
      includeExamples: options.includeExamples !== false,
      // 是否包含 Guardrails
      includeGuardrails: options.includeGuardrails !== false,
    };
  }

  /**
   * 构建 ReAct Reason 阶段 Prompt
   */
  buildReasonPrompt(query, history, availableTools, context = {}) {
    const toolList = availableTools.map(t => 
      `- **${t.name}**: ${t.description || '无描述'} (关键词：${t.keywords?.join(', ') || '无'})`
    ).join('\n');

    const historyContext = history.length > 0 ? `
<execution_history>
${history.map((h, i) => 
`[Step ${i + 1}]
Thought: ${h.thought}
Action: ${h.action}
Observation: ${typeof h.observation === 'string' ? h.observation.substring(0, 200) : JSON.stringify(h.observation)}`
).join('\n\n')}
</execution_history>` : '';

    const guardrails = this.options.includeGuardrails ? `
<guardrails>
⚠️ 重要规则：
1. 必须从可用工具列表中选择工具，不要编造不存在的工具
2. 如果已有足够信息，立即返回 FINAL_ANSWER
3. 参数提取必须准确，不要臆测缺失的参数
4. 如果工具执行失败超过 2 次，考虑换用其他工具或返回答案
5. 思考过程要简洁明了，直接指出下一步行动
</guardrails>` : '';

    const examples = this.options.includeExamples ? `
<examples>
示例 1 - 简单查询：
用户：计算 123 + 456
思考：用户需要数学计算，calculator 工具可以处理加法运算
行动：调用 calculator 工具，参数 a=123, b=456, op='add'

示例 2 - 需要搜索：
用户：搜索最新的 AI 发展趋势
思考：用户需要最新信息，tavily-search 工具可以联网搜索
行动：调用 tavily-search 工具，参数 query='AI 发展趋势 2026'

示例 3 - 已有足够信息：
用户：总结刚才的搜索结果
思考：已经执行过搜索，历史中有足够信息，可以直接合成答案
行动：返回 FINAL_ANSWER，总结搜索结果
</examples>` : '';

    return `你是一个智能 AI 助手，使用 ReAct (Reason+Act) 框架处理用户请求。

<task>
用户查询：${query}
${context.additionalContext ? `\n额外上下文：${context.additionalContext}` : ''}
</task>

<available_tools>
${toolList}
</available_tools>
${historyContext}
${examples}
${guardrails}

<output_format>
请严格按照以下 JSON Schema 格式输出（Reason 阶段）：
{
  "type": "object",
  "required": ["thought", "action"],
  ...
}

输出必须是纯 JSON，不要包含任何其他文本。
</output_format>

你的思考：`;
  }

  /**
   * 构建 Planner Prompt
   */
  buildPlannerPrompt(query, availableTools) {
    const toolList = availableTools.map(t => 
      `- ${t.name}: ${t.description || '无描述'}`
    ).join('\n');

    return `你是一个专业的任务规划师 (Planner)。你的任务是分析用户查询，评估复杂度，并制定执行计划。

<task>
用户查询：${query}
</task>

<available_tools>
${toolList}
</available_tools>

<instructions>
1. 分析任务复杂度（0-1 分）：
   - 0.0-0.3: simple - 简单查询，单步即可完成
   - 0.3-0.6: medium - 中等复杂，需要 2-3 步
   - 0.6-1.0: complex - 高度复杂，需要多步推理和反思

2. 制定执行计划：
   - 分解为具体步骤
   - 为每步分配角色（planner/executor/reviewer）
   - 标注步骤间的依赖关系
   - 估算需要的迭代次数

3. 推荐执行模式：
   - system1: 简单任务，快速执行（~3-5s）
   - system2: 复杂任务，深度推理（~10-15s，带反思）
</instructions>

<output_format>
请严格按照以下 JSON Schema 格式输出：
${JSON.stringify(PLANNER_SCHEMA, null, 2)}

输出必须是纯 JSON，不要包含任何其他文本。
</output_format>

你的规划：`;
  }

  /**
   * 构建 Reflexion Prompt
   */
  buildReflexionPrompt(query, history, plan, reflections) {
    const historySummary = history.map(h => 
      `[${h.action}] ${typeof h.observation === 'string' ? h.observation.substring(0, 100) : 'object'}`
    ).join('\n');

    const reflectionHistory = reflections.length > 0 ? `
<previous_reflections>
${reflections.map((r, i) => 
`反思 ${i + 1}: ${r.insights?.join('; ') || '无'}`
).join('\n')}
</previous_reflections>` : '';

    return `你是一个反思者 (Reflector)。你的任务是审视当前执行进展，提供洞察和建议。

<original_task>
${query}
</original_task>

<original_plan>
${plan?.summary || '无明确计划'}
</original_plan>

<execution_history>
${historySummary}
</execution_history>
${reflectionHistory}

<instructions>
请分析以下方面：

1. **错误模式检测**: 是否有工具反复失败？
2. **进展评估**: 是否已积累足够信息？
3. **计划偏离**: 实际执行是否偏离原计划？
4. **冗余检测**: 是否有重复或无效的操作？
5. **完成判断**: 任务是否可以结束？

基于分析，给出：
- insights: 关键洞察（数组）
- shouldReplan: 是否需要调整计划（布尔值）
- isComplete: 任务是否完成（布尔值）
- confidence: 对判断的置信度（0-1）
</instructions>

<output_format>
请严格按照以下 JSON Schema 格式输出：
${JSON.stringify(REFLEXION_SCHEMA, null, 2)}

输出必须是纯 JSON，不要包含任何其他文本。
</output_format>

你的反思：`;
  }

  /**
   * 构建最终答案合成 Prompt
   */
  buildSynthesizePrompt(query, history, reflections = []) {
    const historyText = history.map((h, i) => 
      `**步骤 ${i + 1}** (${h.action}): ${typeof h.observation === 'string' ? h.observation : JSON.stringify(h.observation)}`
    ).join('\n');

    const reflectionsText = reflections.length > 0 ? `
**反思过程**:
${reflections.map((r, i) => 
`- 反思 ${i + 1}: ${r.insights?.join('; ') || '无'}`
).join('\n')}` : '';

    return `基于以下执行历史，为用户查询合成一个清晰、完整的最终答案。

<query>
${query}
</query>

<execution_history>
${historyText}
</execution_history>
${reflectionsText}

<instructions>
1. 直接回答用户问题，不要提及执行过程
2. 如果有多个结果，用清晰的格式组织
3. 如果执行中有错误，简要说明但不强调
4. 保持答案简洁但有信息量
5. 如有必要，提供后续建议
</instructions>

你的最终答案：`;
  }
}

/**
 * JSON Schema 验证器
 */
class SchemaValidator {
  /**
   * 验证并解析 JSON 输出
   * @param {string} jsonStr - LLM 返回的 JSON 字符串
   * @param {Object} schema - JSON Schema
   * @returns {{valid: boolean, data?: any, error?: string}}
   */
  static validate(jsonStr, schema) {
    try {
      // 清理可能的 markdown 格式
      let cleaned = jsonStr.trim();
      if (cleaned.startsWith('```json')) {
        cleaned = cleaned.replace(/^```json\s*/, '').replace(/\s*```$/, '');
      } else if (cleaned.startsWith('```')) {
        cleaned = cleaned.replace(/^```\s*/, '').replace(/\s*```$/, '');
      }

      const data = JSON.parse(cleaned);

      // 基础验证（简化版，完整验证需使用 ajv 等库）
      const errors = this._basicValidate(data, schema, '');
      
      if (errors.length > 0) {
        return {
          valid: false,
          error: `验证失败：${errors.join('; ')}`,
          data: null
        };
      }

      return { valid: true, data, error: null };
    } catch (parseError) {
      return {
        valid: false,
        error: `JSON 解析失败：${parseError.message}`,
        data: null
      };
    }
  }

  static _basicValidate(data, schema, path) {
    const errors = [];

    // 类型检查
    if (schema.type && typeof data !== schema.type) {
      errors.push(`${path || 'root'} 类型错误：期望 ${schema.type}, 实际 ${typeof data}`);
      return errors;
    }

    // 必填字段检查
    if (schema.required && Array.isArray(schema.required)) {
      for (const field of schema.required) {
        if (data[field] === undefined) {
          errors.push(`缺少必填字段：${path ? `${path}.${field}` : field}`);
        }
      }
    }

    // 对象属性验证
    if (schema.type === 'object' && schema.properties) {
      for (const [key, propSchema] of Object.entries(schema.properties)) {
        if (data[key] !== undefined) {
          const propErrors = this._basicValidate(data[key], propSchema, path ? `${path}.${key}` : key);
          errors.push(...propErrors);
        }
      }
    }

    // 数组验证
    if (schema.type === 'array' && Array.isArray(data) && schema.items) {
      data.forEach((item, index) => {
        const itemErrors = this._basicValidate(item, schema.items, `${path}[${index}]`);
        errors.push(...itemErrors);
      });
    }

    // 枚举验证
    if (schema.enum && !schema.enum.includes(data)) {
      errors.push(`${path || 'root'} 值不在枚举中：${data}`);
    }

    // 字符串长度验证
    if (schema.type === 'string' && typeof data === 'string') {
      if (schema.maxLength && data.length > schema.maxLength) {
        errors.push(`${path || 'root'} 超过最大长度：${data.length} > ${schema.maxLength}`);
      }
      if (schema.minLength && data.length < schema.minLength) {
        errors.push(`${path || 'root'} 小于最小长度：${data.length} < ${schema.minLength}`);
      }
    }

    // 数字范围验证
    if (schema.type === 'number' && typeof data === 'number') {
      if (schema.minimum !== undefined && data < schema.minimum) {
        errors.push(`${path || 'root'} 小于最小值：${data} < ${schema.minimum}`);
      }
      if (schema.maximum !== undefined && data > schema.maximum) {
        errors.push(`${path || 'root'} 超过最大值：${data} > ${schema.maximum}`);
      }
    }

    return errors;
  }
}

// 导出
module.exports = {
  PromptBuilder,
  SchemaValidator,
  REASON_SCHEMA,
  PLANNER_SCHEMA,
  REFLEXION_SCHEMA
};
