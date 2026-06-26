const assert = require('assert');
const { detectRules, generateCard, parseArgs } = require('../src/generator');

const mixed = detectRules({ symptom: 'Top1相似度很高但引用了错误政策' });
assert(mixed.length >= 2);
assert.strictEqual(mixed[0].key, 'top1_pollution');

const card = generateCard({
  symptom: '引用了错误政策但看起来有出处',
  scenario: '企业制度问答',
  quick: true,
});
assert(card.includes('Trigger signal'));
assert(card.includes('Control Changes'));
assert(card.includes('Refuse, Clarify, Or Handoff'));
assert(card.includes('Required Logs'));

const args = parseArgs(['node', 'generator.js', '--symptom', 'Top1错文档', '--scenario', '客服知识库', '--quick']);
assert.strictEqual(args.symptom, 'Top1错文档');
assert.strictEqual(args.scenario, '客服知识库');
assert.strictEqual(args.quick, true);

console.log('rag-hallucination-governor tests passed');
