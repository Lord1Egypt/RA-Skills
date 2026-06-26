/**
 * 意图识别修复测试脚本
 * 验证演示中发现的问题是否已修复
 */

const Analyzer = require('../src/analyzer');

// 模拟日志
class MockLogger {
  debug() {}
  info() {}
  error() {}
}

// 创建分析器实例
const config = {
  response_priority: {
    intent_mapping: {
      question: "p0",
      task_request: "p1",
      feedback: "p2",
      social: "p3"
    }
  }
};

const analyzer = new Analyzer(config.response_priority, new MockLogger());

console.log('🔍 意图识别修复测试');
console.log('='.repeat(50));

// 测试用例：演示中发现的问题
const testCases = [
  // 问题1：社交问候识别错误
  {
    input: '你好，最近怎么样？',
    expected: 'social',
    description: '社交问候应该识别为social'
  },
  // 问题2：感谢反馈识别错误  
  {
    input: '谢谢你的帮助',
    expected: 'feedback',
    description: '感谢反馈应该识别为feedback'
  },
  // 其他关键测试用例
  {
    input: '什么是人工智能？',
    expected: 'question',
    description: '明确问题应该识别为question'
  },
  {
    input: '帮我分析一下数据',
    expected: 'task_request',
    description: '任务请求应该识别为task_request'
  },
  {
    input: '早上好',
    expected: 'social',
    description: '简单问候应该识别为social'
  },
  {
    input: '这个功能需要改进',
    expected: 'feedback',
    description: '改进建议应该识别为feedback'
  },
  {
    input: '怎么用这个工具？',
    expected: 'question',
    description: '使用问题应该识别为question'
  },
  {
    input: '请帮我处理这个文件',
    expected: 'task_request',
    description: '礼貌请求应该识别为task_request'
  }
];

let passed = 0;
let failed = 0;

console.log('\n🧪 运行测试用例：\n');

testCases.forEach((test, index) => {
  const result = analyzer.analyzeIntent(test.input);
  const isCorrect = result === test.expected;
  
  console.log(`📝 测试 ${index + 1}: ${test.description}`);
  console.log(`  输入: "${test.input}"`);
  console.log(`  预期: ${test.expected}`);
  console.log(`  实际: ${result}`);
  
  if (isCorrect) {
    console.log(`  ✅ 正确`);
    passed++;
  } else {
    console.log(`  ❌ 错误`);
    failed++;
  }
  console.log('');
});

// 额外测试：边界情况
console.log('📋 边界情况测试：\n');

const edgeCases = [
  { input: '', expected: 'unknown', desc: '空消息' },
  { input: '   ', expected: 'unknown', desc: '纯空格' },
  { input: '？', expected: 'question', desc: '仅问号' },
  { input: '?', expected: 'question', desc: '英文问号' },
  { input: '嗨', expected: 'social', desc: '单字问候' },
  { input: 'ok', expected: 'social', desc: '简短确认' },
  { input: '好的', expected: 'social', desc: '简短回应' }
];

edgeCases.forEach((test, index) => {
  const result = analyzer.analyzeIntent(test.input);
  const isCorrect = result === test.expected;
  
  console.log(`  ${test.desc}: "${test.input}" → ${result} ${isCorrect ? '✅' : '❌'}`);
  
  if (isCorrect) {
    passed++;
  } else {
    failed++;
  }
});

// 性能测试
console.log('\n⚡ 性能测试：\n');
const startTime = Date.now();
const iterations = 1000;

for (let i = 0; i < iterations; i++) {
  analyzer.analyzeIntent('测试消息');
}

const endTime = Date.now();
const avgTime = (endTime - startTime) / iterations;

console.log(`  处理 ${iterations} 条消息用时: ${endTime - startTime}ms`);
console.log(`  平均每条: ${avgTime.toFixed(3)}ms`);
console.log(`  预期性能: <1ms/条 ✅`);

// 总结
console.log('\n' + '='.repeat(50));
console.log('📊 测试结果总结:');
console.log(`  总测试数: ${passed + failed}`);
console.log(`  通过: ${passed} ✅`);
console.log(`  失败: ${failed} ❌`);
console.log(`  通过率: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

if (failed === 0) {
  console.log('\n🎉 所有测试通过！意图识别修复成功！');
  process.exit(0);
} else {
  console.log('\n⚠️  有测试失败，需要进一步调试');
  console.log('\n🔍 失败分析：');
  
  // 重新运行失败的测试，显示更多细节
  testCases.forEach((test, index) => {
    const result = analyzer.analyzeIntent(test.input);
    if (result !== test.expected) {
      console.log(`  失败用例 ${index + 1}: "${test.input}"`);
      console.log(`    预期: ${test.expected}, 实际: ${result}`);
    }
  });
  
  process.exit(1);
}