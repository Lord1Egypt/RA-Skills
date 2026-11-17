import { readFile } from 'node:fs/promises';

const [successInput, successOutput, failureInput, failureOutput] = await Promise.all([
  readFile('fixtures/success-input.md', 'utf8'),
  readFile('fixtures/success-output.md', 'utf8'),
  readFile('fixtures/failure-input.md', 'utf8'),
  readFile('fixtures/failure-output.md', 'utf8'),
]);

function requireText(text, needle, label) {
  if (!text.includes(needle)) throw new Error(`${label} missing: ${needle}`);
}

// These executable reference checks exercise both declared branches against
// concrete inputs; they do not claim to validate an LLM's judgment.
requireText(successInput, '原话只在小样本里有效，不能推广到所有人。', 'success input');
requireText(successOutput, '“原话只在小样本里有效，不能推广到所有人。”', 'success output');
requireText(successOutput, '说话人：林岚（研究负责人）', 'success attribution');
requireText(successOutput, '位置：00:35', 'success anchor');
requireText(successOutput, '小样本', 'success qualifier');
requireText(failureInput, '一篇编辑摘要称', 'failure input');
requireText(failureOutput, '当前材料是二手采访摘要，不是可回查的受访者原话。', 'failure output');
requireText(failureOutput, '请提供获授权的采访逐字稿', 'failure recovery');
console.log('Fixture branches verified: traceable quote accepted; secondary summary withheld.');
