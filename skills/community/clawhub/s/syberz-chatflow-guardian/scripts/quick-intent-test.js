/**
 * 快速意图识别测试
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

console.log('🎯 意图识别修复验证');
console.log('='.repeat(40));

// 演示中发现的原始问题
const demoIssues = [
  { 
    input: '你好，最近怎么样？', 
    before: 'question', 
    expected: 'social',
    fixed: analyzer.analyzeIntent('你好，最近怎么样？')
  },
  { 
    input: '谢谢你的帮助', 
    before: 'task_request', 
    expected: 'feedback',
    fixed: analyzer.analyzeIntent('谢谢你的帮助')
  }
];

console.log('\n🔍 演示中发现的问题修复验证：\n');

demoIssues.forEach((issue, index) => {
  console.log(`问题 ${index + 1}: "${issue.input}"`);
  console.log(`  修复前: ${issue.before} ❌`);
  console.log(`  预期结果: ${issue.expected} ✅`);
  console.log(`  修复后: ${issue.fixed} ${issue.fixed === issue.expected ? '✅' : '❌'}`);
  console.log('');
});

// 额外验证一些关键场景
console.log('📋 额外验证：\n');

const extraTests = [
  { input: '早上好', expected: 'social' },
  { input: '什么是人工智能？', expected: 'question' },
  { input: '帮我分析数据', expected: 'task_request' },
  { input: '这个功能很好用', expected: 'feedback' },
  { input: '需要改进一下', expected: 'feedback' }
];

extraTests.forEach((test, index) => {
  const result = analyzer.analyzeIntent(test.input);
  console.log(`  ${test.input.padEnd(20)} → ${result.padEnd(12)} ${result === test.expected ? '✅' : '❌'}`);
});

console.log('\n' + '='.repeat(40));

// 统计结果
const allTests = [...demoIssues, ...extraTests.map(t => ({ input: t.input, expected: t.expected, fixed: analyzer.analyzeIntent(t.input) }))];
const passed = allTests.filter(t => t.fixed === t.expected).length;
const total = allTests.length;

console.log(`📊 验证结果: ${passed}/${total} 通过 (${((passed/total)*100).toFixed(1)}%)`);

if (passed === total) {
  console.log('🎉 所有问题已成功修复！');
} else {
  console.log('⚠️  仍有问题需要修复');
}