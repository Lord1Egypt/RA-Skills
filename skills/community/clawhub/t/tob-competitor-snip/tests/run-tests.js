const assert = require('assert');
const { detectScenario, generateCard, parseArgs } = require('../src/generator');

const priceRule = detectScenario('对方价格便宜30%');
assert.strictEqual(priceRule.key, 'price');

const card = generateCard({
  competitor: 'X公司',
  industry: '零售',
  customerConcern: '价格便宜30%',
});
assert(card.includes('竞品狙击卡片'));
assert(card.includes('3年TCO'));
assert(card.includes('差异化对比'));

const quick = generateCard({
  competitor: 'X公司',
  customerConcern: '品牌大',
  quick: true,
});
assert(quick.includes('狙击话术'));
assert(!quick.includes('差异化对比'));

const args = parseArgs(['node', 'generator.js', '--competitor', 'X公司', '--industry', '金融', '--concern', '功能更多', '--quick']);
assert.strictEqual(args.competitor, 'X公司');
assert.strictEqual(args.industry, '金融');
assert.strictEqual(args.customerConcern, '功能更多');
assert.strictEqual(args.quick, true);

console.log('tob-competitor-snip tests passed');
