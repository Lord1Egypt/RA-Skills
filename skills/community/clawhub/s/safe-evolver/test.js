// 测试 Safe Evolver
const SafeEvolver = require('./index.js');

const evolver = new SafeEvolver();

// 模拟历史数据
const mockHistory = [
  {
    timestamp: '2026-04-05T10:00:00.000Z',
    toolCalls: 5,
    responses: 3,
    errors: 1,
    efficiency: 0.8
  },
  {
    timestamp: '2026-04-05T10:05:00.000Z',
    toolCalls: 7,
    responses: 5,
    errors: 0,
    efficiency: 0.9
  },
  {
    timestamp: '2026-04-05T10:10:00.000Z',
    toolCalls: 4,
    responses: 4,
    errors: 2,
    efficiency: 0.7
  }
];

console.log('🧪 测试 Safe Evolver...\n');

// 记录交互
console.log('1. 记录交互:');
const interaction1 = evolver.recordInteraction({
  toolCalls: 6,
  responses: 4,
  errors: 0,
  efficiency: 0.85
});
console.log('   已记录交互:', interaction1.timestamp);

const interaction2 = evolver.recordInteraction({
  toolCalls: 8,
  responses: 6,
  errors: 1,
  efficiency: 0.82
});
console.log('   已记录交互:', interaction2.timestamp);

// 分析历史
console.log('\n2. 分析历史:');
const improvements = evolver.analyzeHistory(mockHistory);
console.log('   发现改进机会:', improvements.length);

// 获取报告
console.log('\n3. 进化报告:');
const report = evolver.getReport();
console.log('   总交互次数:', report.totalInteractions);
console.log('   改进次数:', report.totalImprovements);
console.log('   最后更新:', report.lastUpdate);

console.log('\n✅ Safe Evolver 测试完成!');
