/**
 * LLM Integration 测试套件
 * 
 * 测试覆盖:
 * - Prompt 构建
 * - JSON Schema 验证
 * - 输出解析
 */

const { PromptBuilder, SchemaValidator, REASON_SCHEMA } = require('../src/llm-integration');

// 测试辅助函数
function test(name, fn) {
  return { name, fn };
}

async function runTests() {
  console.log('🧪 LLM Integration 测试套件');
  console.log('=' .repeat(50));

  const tests = [
    // ========== Prompt 构建测试 ==========
    test('PromptBuilder - 基础 Reason Prompt', async () => {
      const builder = new PromptBuilder();
      const tools = [
        { name: 'calculator', description: '计算器', keywords: ['计算', '数学'] },
        { name: 'search', description: '搜索工具', keywords: ['搜索', '查找'] }
      ];
      
      const prompt = builder.buildReasonPrompt('计算 123+456', [], tools);
      
      if (!prompt.includes('计算 123+456')) throw new Error('缺少用户查询');
      if (!prompt.includes('calculator')) throw new Error('缺少工具列表');
      if (!prompt.includes('JSON Schema')) throw new Error('缺少 Schema');
      if (!prompt.includes('guardrails')) throw new Error('缺少 Guardrails');
      
      console.log('✅ PromptBuilder - 基础 Reason Prompt');
    }),

    test('PromptBuilder - 带历史上下文', async () => {
      const builder = new PromptBuilder();
      const tools = [{ name: 'search', description: '搜索', keywords: ['搜索'] }];
      const history = [
        {
          thought: '使用 search 工具',
          action: 'search',
          observation: '搜索结果：AI 发展趋势...'
        }
      ];
      
      const prompt = builder.buildReasonPrompt('总结搜索结果', history, tools);
      
      if (!prompt.includes('execution_history')) throw new Error('缺少历史上下文');
      if (!prompt.includes('AI 发展趋势')) throw new Error('历史内容丢失');
      
      console.log('✅ PromptBuilder - 带历史上下文');
    }),

    test('PromptBuilder - 禁用 Guardrails', async () => {
      const builder = new PromptBuilder({ includeGuardrails: false });
      const tools = [{ name: 'test', description: '测试', keywords: [] }];
      
      const prompt = builder.buildReasonPrompt('测试', [], tools);
      
      if (prompt.includes('guardrails')) throw new Error('不应包含 Guardrails');
      
      console.log('✅ PromptBuilder - 禁用 Guardrails');
    }),

    test('PromptBuilder - Planner Prompt', async () => {
      const builder = new PromptBuilder();
      const tools = [
        { name: 'search', description: '搜索' },
        { name: 'analyze', description: '分析' }
      ];
      
      const prompt = builder.buildPlannerPrompt(
        '分析 AI 行业趋势并给出建议',
        tools
      );
      
      if (!prompt.includes('Planner')) throw new Error('缺少角色定义');
      if (!prompt.includes('complexity')) throw new Error('缺少复杂度评估');
      if (!prompt.includes('JSON Schema')) throw new Error('缺少 Schema');
      
      console.log('✅ PromptBuilder - Planner Prompt');
    }),

    test('PromptBuilder - Reflexion Prompt', async () => {
      const builder = new PromptBuilder();
      const history = [
        { action: 'search', observation: '结果 1' },
        { action: 'search', observation: '结果 2' }
      ];
      const plan = { summary: '3 步计划' };
      const reflections = [
        { insights: ['工具使用重复度高'] }
      ];
      
      const prompt = builder.buildReflexionPrompt('复杂任务', history, plan, reflections);
      
      if (!prompt.includes('Reflector')) throw new Error('缺少角色定义');
      if (!prompt.includes('反思 1')) throw new Error('缺少反思历史');
      if (!prompt.includes('JSON Schema')) throw new Error('缺少 Schema');
      
      console.log('✅ PromptBuilder - Reflexion Prompt');
    }),

    // ========== Schema 验证测试 ==========
    test('SchemaValidator - 有效 JSON', async () => {
      const jsonStr = JSON.stringify({
        thought: '使用 calculator 工具',
        action: 'FINAL_ANSWER',
        answer: '答案是 579'
      });
      
      const result = SchemaValidator.validate(jsonStr, REASON_SCHEMA);
      
      if (!result.valid) throw new Error(`验证失败：${result.error}`);
      if (!result.data) throw new Error('数据为空');
      if (result.data.thought !== '使用 calculator 工具') throw new Error('数据错误');
      
      console.log('✅ SchemaValidator - 有效 JSON');
    }),

    test('SchemaValidator - 无效 JSON', async () => {
      const jsonStr = '{ invalid json }';
      
      const result = SchemaValidator.validate(jsonStr, REASON_SCHEMA);
      
      if (result.valid) throw new Error('应该验证失败');
      if (!result.error) throw new Error('缺少错误信息');
      if (!result.error.includes('解析失败')) throw new Error('错误类型错误');
      
      console.log('✅ SchemaValidator - 无效 JSON');
    }),

    test('SchemaValidator - 缺少必填字段', async () => {
      const jsonStr = JSON.stringify({
        thought: '思考'
        // 缺少 action
      });
      
      const result = SchemaValidator.validate(jsonStr, REASON_SCHEMA);
      
      if (result.valid) throw new Error('应该验证失败');
      if (!result.error.includes('缺少必填字段')) throw new Error('错误类型错误');
      
      console.log('✅ SchemaValidator - 缺少必填字段');
    }),

    test('SchemaValidator - Markdown 格式清理', async () => {
      const jsonStr = '```json\n{"thought": "测试", "action": "FINAL_ANSWER", "answer": "答案"}\n```';
      
      const result = SchemaValidator.validate(jsonStr, REASON_SCHEMA);
      
      if (!result.valid) throw new Error(`验证失败：${result.error}`);
      if (result.data.answer !== '答案') throw new Error('数据解析错误');
      
      console.log('✅ SchemaValidator - Markdown 格式清理');
    }),

    test('SchemaValidator - 字符串长度验证', async () => {
      const jsonStr = JSON.stringify({
        thought: 'x'.repeat(600), // 超过 500 限制
        action: 'FINAL_ANSWER',
        answer: '答案'
      });
      
      const result = SchemaValidator.validate(jsonStr, REASON_SCHEMA);
      
      if (result.valid) throw new Error('应该验证失败');
      if (!result.error.includes('超过最大长度')) throw new Error('错误类型错误');
      
      console.log('✅ SchemaValidator - 字符串长度验证');
    }),

    test('SchemaValidator - 枚举验证', async () => {
      const jsonStr = JSON.stringify({
        thought: '思考',
        action: 'INVALID_ACTION' // 不在枚举中
      });
      
      const schema = {
        ...REASON_SCHEMA,
        properties: {
          ...REASON_SCHEMA.properties,
          action: {
            ...REASON_SCHEMA.properties.action,
            enum: ['FINAL_ANSWER', 'calculator', 'search']
          }
        }
      };
      
      const result = SchemaValidator.validate(jsonStr, schema);
      
      if (result.valid) throw new Error('应该验证失败');
      if (!result.error.includes('不在枚举中')) throw new Error('错误类型错误');
      
      console.log('✅ SchemaValidator - 枚举验证');
    }),

    // ========== 集成测试 ==========
    test('集成测试 - 完整 ReAct 循环 Prompt', async () => {
      const builder = new PromptBuilder({ includeExamples: true });
      const tools = [
        { name: 'tavily-search', description: '联网搜索', keywords: ['搜索', '查找', '最新'] },
        { name: 'calculator', description: '计算器', keywords: ['计算', '数学'] },
        { name: 'rag-retrieve', description: '本地检索', keywords: ['文档', '知识'] }
      ];
      
      // Phase 1: 初始 Reason
      const prompt1 = builder.buildReasonPrompt('搜索 2026 年 AI 发展趋势', [], tools);
      if (!prompt1.includes('tavily-search')) throw new Error('缺少工具');
      
      // Phase 2: 执行后 Reason
      const history = [{
        thought: '使用 tavily-search',
        action: 'tavily-search',
        observation: { results: [{ title: 'AI 趋势 2026', snippet: '多模态...' }] }
      }];
      const prompt2 = builder.buildReasonPrompt('搜索 2026 年 AI 发展趋势', history, tools);
      if (!prompt2.includes('execution_history')) throw new Error('缺少历史');
      
      // Phase 3: Reflexion
      const prompt3 = builder.buildReflexionPrompt(
        '搜索 2026 年 AI 发展趋势',
        [...history, { action: 'search', observation: '结果 2' }],
        { summary: '搜索计划' },
        []
      );
      if (!prompt3.includes('Reflector')) throw new Error('缺少反思');
      
      console.log('✅ 集成测试 - 完整 ReAct 循环 Prompt');
    }),
  ];

  // 运行测试
  let passed = 0;
  let failed = 0;

  for (const { name, fn } of tests) {
    try {
      await fn();
      passed++;
    } catch (error) {
      console.log(`❌ ${name}`);
      console.log(`   ${error.message}`);
      failed++;
    }
  }

  // 汇总结果
  console.log('=' .repeat(50));
  console.log(`📊 测试结果：${passed} passed, ${failed} failed`);
  console.log(`✅ 通过率：${((passed / tests.length) * 100).toFixed(1)}%`);

  if (failed > 0) {
    process.exit(1);
  }
}

// 运行测试
runTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});
