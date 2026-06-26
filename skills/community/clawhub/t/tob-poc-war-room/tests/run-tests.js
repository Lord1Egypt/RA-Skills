const assert = require('assert');
const { generateReport, parseArgs } = require('../src/generator');

function includesAll(text, fragments) {
  for (const fragment of fragments) {
    assert(
      text.includes(fragment),
      `expected output to include: ${fragment}\n\nActual output:\n${text.slice(0, 1200)}`
    );
  }
}

const highPassButSilent = generateReport({
  industry: '零售',
  objective: '客服知识库 POC 通过率 >=90%',
  day: 8,
  problems: '一个 SSO 问题 60h 未关闭，客户 champion 认可结果',
  passRate: 93,
  silenceDays: 7,
});
includesAll(highPassButSilent, [
  '当前通过率：93%',
  '客户沉默：7 天',
  '采购路径：未知',
  '通过率达到收口线',
  '客户沉默达到 7 天',
  '采购路径未知',
  '不要直接丢报价',
  'poc-to-contract-closer',
]);

const yellowPass = generateReport({
  industry: '教育',
  objective: '教材答疑准确率 >=90%',
  day: 4,
  problems: '教材版本不一致，教师反馈答案来源不清',
  passRate: 78,
  silenceDays: 0,
});
includesAll(yellowPass, [
  '通过率处于黄区',
  '未来 48 小时集中处理',
  '问题清零',
]);

const args = parseArgs([
  'node',
  'generator.js',
  '--industry',
  '零售',
  '--pass-rate',
  '93',
  '--silence-days',
  '7',
  '--procurement-path',
  '比价采购',
]);
assert.strictEqual(args.industry, '零售');
assert.strictEqual(args.passRate, 93);
assert.strictEqual(args.silenceDays, 7);
assert.strictEqual(args.procurementPath, '比价采购');

console.log('tob-poc-war-room tests passed');
