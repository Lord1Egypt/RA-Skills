/**
 * ReAct Orchestrator 实际效果演示
 * 
 * 测试场景：
 * 1. 简单查询（System 1）- 快速回答
 * 2. 复杂调研（System 2）- 多步推理 + 反思
 */

const { ReActOrchestrator } = require('./src/orchestrator');

// 模拟工具实现
const mockTools = {
  // Tavily 搜索模拟
  'tavily-search': {
    fn: async (params) => {
      console.log(`  🔍 [搜索] "${params.query}"`);
      await new Promise(r => setTimeout(r, 800)); // 模拟网络延迟
      return {
        results: [
          { title: 'AI Agent 2026 发展趋势', snippet: '多模态、自主性、工具使用成为主流...' },
          { title: 'ReAct 框架最佳实践', snippet: 'Reason+Act 循环在复杂任务中表现优异...' },
        ],
        count: 2,
      };
    },
    metadata: {
      description: 'Tavily 联网搜索工具',
      keywords: ['搜索', '查找', '调研', '最新', '趋势', '搜索'],
      timeout: 10,
    }
  },

  // RAG 检索模拟
  'rag-retrieve': {
    fn: async (params) => {
      console.log(`  📚 [检索] "${params.query}"`);
      await new Promise(r => setTimeout(r, 300));
      return {
        documents: [
          { content: '本地笔记：MCP 协议是 2025 年 AI 工具连接标准', score: 0.89 },
          { content: '本地笔记：RAG 检索需要中文分词支持', score: 0.76 },
        ],
        count: 2,
      };
    },
    metadata: {
      description: '本地知识库检索',
      keywords: ['文档', '知识', '记忆', '检索', '笔记'],
      timeout: 5,
    }
  },

  // 计算器
  'calculator': {
    fn: async (params) => {
      console.log(`  🧮 [计算] ${params.a} ${params.op} ${params.b}`);
      const { a, b, op } = params;
      switch (op) {
        case 'add': return a + b;
        case 'mul': return a * b;
        default: return a + b;
      }
    },
    metadata: {
      description: '计算器工具',
      keywords: ['计算', '数学', '加减乘除'],
      timeout: 2,
    }
  },

  // 文件读取模拟
  'file-read': {
    fn: async (params) => {
      console.log(`  📄 [读取] ${params.path}`);
      await new Promise(r => setTimeout(r, 200));
      return `文件内容：这是 ${params.path} 的模拟内容...`;
    },
    metadata: {
      description: '文件读取工具',
      keywords: ['文件', '读取', '打开', '查看'],
      timeout: 5,
    }
  },
};

async function runDemo() {
  console.log('\n🦞 ReAct Orchestrator 实际效果演示\n');
  console.log('=' .repeat(60));

  const orchestrator = new ReActOrchestrator({
    verbose: true,
    complexityThreshold: 0.5,
  });

  // 注册所有工具
  for (const [name, { fn, metadata }] of Object.entries(mockTools)) {
    orchestrator.registerTool(name, fn, metadata);
  }

  console.log('\n' + '=' .repeat(60));
  console.log('📋 测试 1: 简单查询（预期 System 1）');
  console.log('=' .repeat(60));
  
  const simpleQuery = '计算 123 + 456';
  console.log(`\n用户查询：${simpleQuery}\n`);
  
  const simpleResult = await orchestrator.execute(simpleQuery, { mode: 'auto' });
  console.log(`\n📊 结果:`);
  console.log(`   模式：${simpleResult.mode}`);
  console.log(`   耗时：${simpleResult.duration}s`);
  console.log(`   迭代：${simpleResult.iterations}次`);
  console.log(`   答案：${simpleResult.answer.substring(0, 100)}...`);

  console.log('\n' + '=' .repeat(60));
  console.log('📋 测试 2: 中等复杂度（预期 System 1 或 System 2）');
  console.log('=' .repeat(60));
  
  const mediumQuery = '搜索 AI agent 最新发展趋势';
  console.log(`\n用户查询：${mediumQuery}\n`);
  
  const mediumResult = await orchestrator.execute(mediumQuery, { mode: 'auto' });
  console.log(`\n📊 结果:`);
  console.log(`   模式：${mediumResult.mode}`);
  console.log(`   耗时：${mediumResult.duration}s`);
  console.log(`   迭代：${mediumResult.iterations}次`);
  console.log(`   答案：${mediumResult.answer.substring(0, 150)}...`);

  console.log('\n' + '=' .repeat(60));
  console.log('📋 测试 3: 复杂调研（预期 System 2 + 反思）');
  console.log('=' .repeat(60));
  
  const complexQuery = '调研 2026 年 AI agent 发展趋势，然后检索本地笔记中的相关记录，最后给出技术选型建议';
  console.log(`\n用户查询：${complexQuery}\n`);
  
  const complexResult = await orchestrator.execute(complexQuery, { mode: 'auto' });
  console.log(`\n📊 结果:`);
  console.log(`   模式：${complexResult.mode}`);
  console.log(`   耗时：${complexResult.duration}s`);
  console.log(`   迭代：${complexResult.iterations}次`);
  console.log(`   反思：${complexResult.reflections?.length || 0}次`);
  console.log(`\n📝 完整答案:\n${complexResult.answer}`);

  console.log('\n' + '=' .repeat(60));
  console.log('📋 测试 4: 复杂度评估演示');
  console.log('=' .repeat(60));
  
  const queries = [
    '2+2=?',
    '搜索 Python 教程',
    '分析 AI 行业趋势并给出建议',
    '调研 2026 年技术发展，然后比较主流方案，最后给出选型建议',
  ];

  for (const q of queries) {
    const assessment = await orchestrator.evaluateComplexity(q);
    console.log(`\n查询："${q.substring(0, 30)}${q.length > 30 ? '...' : ''}"`);
    console.log(`   分数：${assessment.score.toFixed(2)} → ${assessment.mode.toUpperCase()}`);
    console.log(`   原因：${assessment.reasons.join(', ') || '简单任务'}`);
  }

  console.log('\n' + '=' .repeat(60));
  console.log('✅ 演示完成！\n');
}

// 运行演示
runDemo().catch(error => {
  console.error('❌ 演示失败:', error);
  process.exit(1);
});
