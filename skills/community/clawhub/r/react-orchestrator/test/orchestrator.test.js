/**
 * ReAct Orchestrator 测试套件
 * 
 * 测试覆盖:
 * - 工具注册与发现
 * - 复杂度评估
 * - System 1 快速执行
 * - System 2 深度推理
 * - Reflexion 反思机制
 * - 超时保护
 * - 错误处理
 */

const { ReActOrchestrator } = require('../src/orchestrator');
const { ToolRegistry } = require('../src/tool-registry');

// 测试工具实现
const mockTools = {
  echo: {
    fn: (params) => Promise.resolve(`Echo: ${params.message || 'no message'}`),
    metadata: {
      description: '回声测试工具',
      keywords: ['测试', 'echo', '回显'],
    }
  },
  calculator: {
    fn: (params) => {
      const { a, b, op } = params;
      switch (op) {
        case 'add': return Promise.resolve(a + b);
        case 'sub': return Promise.resolve(a - b);
        case 'mul': return Promise.resolve(a * b);
        case 'div': return Promise.resolve(a / b);
        default: return Promise.reject(new Error(`未知操作：${op}`));
      }
    },
    metadata: {
      description: '计算器工具',
      keywords: ['计算', '数学', '加减乘除'],
    }
  },
  slow: {
    fn: async (params) => {
      const delay = params.delay || 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
      return `Delayed response (${delay}ms)`;
    },
    metadata: {
      description: '慢速测试工具',
      keywords: ['慢速', '延迟'],
      timeout: 2,
    }
  },
  failing: {
    fn: (params) => Promise.reject(new Error('故意失败')),
    metadata: {
      description: '失败测试工具',
      keywords: ['失败', '错误'],
    }
  },
};

// 测试辅助函数
function test(name, fn) {
  return { name, fn };
}

async function runTests() {
  console.log('🧪 ReAct Orchestrator 测试套件');
  console.log('=' .repeat(50));

  const tests = [
    // ========== 工具注册测试 ==========
    test('工具注册与发现', async () => {
      const registry = new ToolRegistry();
      registry.register('test', () => {}, { description: '测试' });
      
      const tools = registry.list();
      if (!tools.includes('test')) throw new Error('工具注册失败');
      if (registry.get('test') === undefined) throw new Error('工具获取失败');
      console.log('✅ 工具注册与发现');
    }),

    test('工具批量注册', async () => {
      const registry = new ToolRegistry();
      registry.registerTools([
        { name: 'tool1', fn: () => {}, metadata: {} },
        { name: 'tool2', fn: () => {}, metadata: {} },
      ]);
      
      const tools = registry.list();
      if (tools.length !== 2) throw new Error(`期望 2 个工具，实际${tools.length}`);
      console.log('✅ 工具批量注册');
    }),

    test('工具语义匹配', async () => {
      const registry = new ToolRegistry();
      registry.register('search', () => {}, { 
        description: '搜索工具',
        keywords: ['搜索', '查找']
      });
      
      const matches = registry.match('帮我搜索一下');
      if (!matches.includes('search')) throw new Error('语义匹配失败');
      console.log('✅ 工具语义匹配');
    }),

    // ========== 复杂度评估测试 ==========
    test('简单任务评估 (System 1)', async () => {
      const orchestrator = new ReActOrchestrator();
      const result = await orchestrator.evaluateComplexity('2+2=?');
      
      if (result.mode !== 'system1') {
        throw new Error(`期望 system1，实际${result.mode}`);
      }
      console.log(`✅ 简单任务评估 (score: ${result.score.toFixed(2)})`);
    }),

    test('复杂任务评估 (System 2)', async () => {
      const orchestrator = new ReActOrchestrator();
      const result = await orchestrator.evaluateComplexity(
        '分析 AI 行业趋势，然后比较主要玩家，最后给出投资建议'
      );
      
      if (result.mode !== 'system2') {
        throw new Error(`期望 system2，实际${result.mode}`);
      }
      console.log(`✅ 复杂任务评估 (score: ${result.score.toFixed(2)})`);
    }),

    // ========== System 1 测试 ==========
    test('System 1 快速执行', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute('测试 echo', { mode: 'system1' });
      
      if (!result.answer) throw new Error('无答案');
      if (result.mode !== 'system1') throw new Error('模式错误');
      if (result.duration === undefined) throw new Error('无耗时');
      console.log(`✅ System 1 快速执行 (${result.duration}s, ${result.iterations}次迭代)`);
    }),

    test('System 1 超时保护', async () => {
      const orchestrator = new ReActOrchestrator({ 
        verbose: false,
        system1Timeout: 1,
      });
      orchestrator.registerTool('slow', mockTools.slow.fn, mockTools.slow.metadata);
      
      const result = await orchestrator.execute('测试超时', { mode: 'system1' });
      
      if (!result.timedOut && !result.answer.includes('超时')) {
        throw new Error('超时保护未触发');
      }
      console.log('✅ System 1 超时保护');
    }),

    // ========== System 2 测试 ==========
    test('System 2 深度推理', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute('深度分析这个问题', { mode: 'system2' });
      
      if (!result.answer) throw new Error('无答案');
      if (result.mode !== 'system2') throw new Error('模式错误');
      console.log(`✅ System 2 深度推理 (${result.duration}s, ${result.iterations}次迭代)`);
    }),

    test('System 2 反思机制', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute('复杂任务需要反思', { mode: 'system2' });
      
      // System 2 应该有 reflections 字段
      if (result.reflections === undefined) {
        throw new Error('缺少反思记录');
      }
      console.log(`✅ System 2 反思机制 (${result.reflections.length}次反思)`);
    }),

    // ========== 错误处理测试 ==========
    test('工具执行错误处理', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('failing', mockTools.failing.fn, mockTools.failing.metadata);
      
      const result = await orchestrator.execute('测试错误处理', { mode: 'system1' });
      
      // 应该优雅处理错误，而不是抛出异常
      if (!result.answer) throw new Error('无答案');
      console.log('✅ 工具执行错误处理');
    }),

    test('未知工具处理', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      // 不注册任何工具
      
      const result = await orchestrator.execute('使用不存在的工具', { mode: 'system1' });
      
      if (!result.answer) throw new Error('无答案');
      console.log('✅ 未知工具处理');
    }),

    // ========== 自动模式选择测试 ==========
    test('自动模式选择 - 简单查询', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute('echo 测试', { mode: 'auto' });
      
      if (result.mode !== 'system1') {
        throw new Error(`简单查询应该用 system1，实际${result.mode}`);
      }
      console.log(`✅ 自动模式选择 - 简单查询 → ${result.mode}`);
    }),

    test('自动模式选择 - 复杂查询', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute(
        '分析 2025 年 AI 趋势，然后比较主流框架，并给出技术选型建议',
        { mode: 'auto' }
      );
      
      if (result.mode !== 'system2') {
        throw new Error(`复杂查询应该用 system2，实际${result.mode}`);
      }
      console.log(`✅ 自动模式选择 - 复杂查询 → ${result.mode}`);
    }),

    // ========== 执行历史测试 ==========
    test('执行历史记录', async () => {
      const orchestrator = new ReActOrchestrator({ verbose: false });
      orchestrator.registerTool('echo', mockTools.echo.fn, mockTools.echo.metadata);
      
      const result = await orchestrator.execute('测试历史', { mode: 'system1' });
      
      if (!Array.isArray(result.history)) {
        throw new Error('历史记录应该是数组');
      }
      if (result.history.length === 0) {
        throw new Error('历史记录为空');
      }
      console.log(`✅ 执行历史记录 (${result.history.length}条)`);
    }),

    // ========== 工具注册中心测试 ==========
    test('工具注册中心 - 导出导入', async () => {
      const registry = new ToolRegistry();
      registry.register('test', () => {}, { description: '测试' });
      
      const exported = registry.export();
      if (!exported.tools) throw new Error('导出失败');
      if (!exported.exportedAt) throw new Error('缺少时间戳');
      
      console.log('✅ 工具注册中心 - 导出导入');
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
