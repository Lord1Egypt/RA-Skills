/**
 * Code Mode 转换层测试套件
 * 
 * 测试覆盖:
 * - 工具模板注册
 * - 代码生成
 * - 沙箱执行
 * - Token 节省估算
 */

const { CodeModeConverter } = require('../src/code-mode');

// 测试辅助函数
function test(name, fn) {
  return { name, fn };
}

async function runTests() {
  console.log('🧪 Code Mode 转换层测试套件');
  console.log('=' .repeat(50));

  const converter = new CodeModeConverter();

  const tests = [
    // ========== 模板注册测试 ==========
    test('内置工具模板注册', async () => {
      const tools = converter.getRegisteredTools();
      
      const expected = ['tavily-search', 'calculator', 'file-read', 'file-write', 'directory-list'];
      for (const tool of expected) {
        if (!tools.includes(tool)) {
          throw new Error(`缺少内置工具：${tool}`);
        }
      }
      
      console.log(`✅ 内置工具模板注册 (${tools.length}个工具)`);
    }),

    test('自定义工具模板注册', async () => {
      const customConverter = new CodeModeConverter();
      
      customConverter.registerTemplate('custom-tool', {
        javascript: (params) => `console.log(${JSON.stringify(params)});`,
        powershell: (params) => `Write-Host "${JSON.stringify(params)}"`
      });
      
      const tools = customConverter.getRegisteredTools();
      if (!tools.includes('custom-tool')) {
        throw new Error('自定义工具注册失败');
      }
      
      console.log('✅ 自定义工具模板注册');
    }),

    // ========== 代码生成测试 ==========
    test('Calculator 代码生成 (JavaScript)', async () => {
      const code = converter.convert('calculator', { a: 123, b: 456, op: 'add' }, 'javascript');
      
      if (!code.includes('123')) throw new Error('缺少参数 a');
      if (!code.includes('456')) throw new Error('缺少参数 b');
      if (!code.includes('add')) throw new Error('缺少操作符');
      if (!code.includes('switch')) throw new Error('缺少逻辑');
      
      console.log('✅ Calculator 代码生成 (JavaScript)');
    }),

    test('Calculator 代码生成 (PowerShell)', async () => {
      const code = converter.convert('calculator', { a: 123, b: 456, op: 'add' }, 'powershell');
      
      if (!code.includes('123')) throw new Error('缺少参数 a');
      if (!code.includes('456')) throw new Error('缺少参数 b');
      if (!code.includes('switch')) throw new Error('缺少逻辑');
      
      console.log('✅ Calculator 代码生成 (PowerShell)');
    }),

    test('Tavily Search 代码生成', async () => {
      const code = converter.convert('tavily-search', { query: 'AI trends', limit: 5 }, 'javascript');
      
      if (!code.includes('AI trends')) throw new Error('缺少查询');
      if (!code.includes('limit: 5')) throw new Error('缺少限制');
      if (!code.includes('tavily-search')) throw new Error('缺少模块引用');
      
      console.log('✅ Tavily Search 代码生成');
    }),

    test('File Read 代码生成', async () => {
      const code = converter.convert('file-read', { path: 'test.txt' }, 'javascript');
      
      if (!code.includes('test.txt')) throw new Error('缺少路径');
      if (!code.includes('readFileSync')) throw new Error('缺少读取函数');
      
      console.log('✅ File Read 代码生成');
    }),

    test('未知工具错误处理', async () => {
      try {
        converter.convert('unknown-tool', {}, 'javascript');
        throw new Error('应该抛出错误');
      } catch (error) {
        if (!error.message.includes('未知工具')) {
          throw new Error(`错误消息不正确：${error.message}`);
        }
      }
      
      console.log('✅ 未知工具错误处理');
    }),

    test('不支持的语言错误处理', async () => {
      try {
        converter.convert('calculator', {}, 'python');
        throw new Error('应该抛出错误');
      } catch (error) {
        if (!error.message.includes('不支持的语言')) {
          throw new Error(`错误消息不正确：${error.message}`);
        }
      }
      
      console.log('✅ 不支持的语言错误处理');
    }),

    // ========== 沙箱执行测试 ==========
    test('JavaScript 沙箱执行 - 简单计算', async () => {
      const code = converter.convert('calculator', { a: 123, b: 456, op: 'add' }, 'javascript');
      const result = await converter.execute(code, 'javascript', { timeout: 5000 });
      
      if (!result.success) throw new Error(`执行失败：${result.error}`);
      if (!result.output.includes('579')) throw new Error(`结果错误：${result.output}`);
      if (!result.duration) throw new Error('缺少耗时');
      
      console.log(`✅ JavaScript 沙箱执行 - 简单计算 (${result.duration}ms)`);
    }),

    test('JavaScript 沙箱执行 - 字符串输出', async () => {
      const code = `
const greeting = 'Hello, Code Mode!';
return greeting;
`.trim();
      
      const result = await converter.execute(code, 'javascript', { timeout: 5000 });
      
      if (!result.success) throw new Error(`执行失败：${result.error}`);
      if (!result.output.includes('Hello, Code Mode!')) throw new Error(`结果错误：${result.output}`);
      
      console.log(`✅ JavaScript 沙箱执行 - 字符串输出 (${result.duration}ms)`);
    }),

    test('JavaScript 沙箱执行 - JSON 返回', async () => {
      const code = `
return { name: 'Test', value: 42 };
`.trim();
      
      const result = await converter.execute(code, 'javascript', { timeout: 5000 });
      
      if (!result.success) throw new Error(`执行失败：${result.error}`);
      if (!result.output.includes('Test')) throw new Error(`结果错误：${result.output}`);
      
      console.log(`✅ JavaScript 沙箱执行 - JSON 返回 (${result.duration}ms)`);
    }),

    test('JavaScript 沙箱执行 - 错误处理', async () => {
      const code = `
throw new Error('故意抛出的错误');
`.trim();
      
      const result = await converter.execute(code, 'javascript', { timeout: 5000 });
      
      if (result.success) throw new Error('应该执行失败');
      if (!result.error.includes('故意抛出的错误')) throw new Error(`错误消息不正确：${result.error}`);
      
      console.log(`✅ JavaScript 沙箱执行 - 错误处理`);
    }),

    test('PowerShell 沙箱执行 - 简单输出', async () => {
      const code = `
"Hello from PowerShell"
`.trim();
      
      const result = await converter.execute(code, 'powershell', { timeout: 5000 });
      
      if (!result.success) throw new Error(`执行失败：${result.error}`);
      if (!result.output.includes('Hello from PowerShell')) throw new Error(`结果错误：${result.output}`);
      
      console.log(`✅ PowerShell 沙箱执行 - 简单输出 (${result.duration}ms)`);
    }),

    // ========== Token 节省估算测试 ==========
    test('Token 节省估算 - Calculator', async () => {
      const savings = converter.estimateTokenSavings('calculator', { a: 123, b: 456, op: 'add' });
      
      if (!savings.traditional) throw new Error('缺少传统 token 数');
      if (!savings.codeMode) throw new Error('缺少 Code Mode token 数');
      if (savings.percentage === undefined) throw new Error('缺少节省百分比');
      
      console.log(`✅ Token 节省估算 - Calculator (传统：${savings.traditional}, Code Mode: ${savings.codeMode}, 节省：${savings.percentage}%)`);
    }),

    test('Token 节省估算 - Tavily Search', async () => {
      const savings = converter.estimateTokenSavings('tavily-search', { query: 'AI trends 2026', limit: 5 });
      
      if (!savings.traditional) throw new Error('缺少传统 token 数');
      if (!savings.codeMode) throw new Error('缺少 Code Mode token 数');
      
      // Code Mode 应该更节省（或至少不会更差）
      // 注意：对于简单调用，Code Mode 可能不会节省，因为代码本身有开销
      // 但对于复杂调用（多步骤），Code Mode 优势明显
      
      console.log(`✅ Token 节省估算 - Tavily Search (传统：${savings.traditional}, Code Mode: ${savings.codeMode}, 节省：${savings.percentage}%)`);
    }),

    // ========== 集成测试 ==========
    test('集成测试 - 完整工作流', async () => {
      // 1. 注册自定义工具
      const customConverter = new CodeModeConverter();
      customConverter.registerTemplate('echo', {
        javascript: (params) => `return "Echo: ${params.message}";`
      });
      
      // 2. 生成代码
      const code = customConverter.convert('echo', { message: 'Hello Code Mode!' }, 'javascript');
      
      // 3. 执行
      const result = await customConverter.execute(code, 'javascript', { timeout: 5000 });
      
      if (!result.success) throw new Error(`执行失败：${result.error}`);
      if (!result.output.includes('Hello Code Mode!')) throw new Error(`结果错误：${result.output}`);
      
      // 4. 估算 Token
      const savings = customConverter.estimateTokenSavings('echo', { message: 'Hello Code Mode!' });
      
      console.log(`✅ 集成测试 - 完整工作流 (Token 节省：${savings.percentage}%)`);
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
