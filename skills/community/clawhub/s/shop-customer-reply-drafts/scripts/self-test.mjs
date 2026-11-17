#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = [
  'SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md',
  'LICENSE', 'icon-512.png', 'fixtures/success.json', 'fixtures/failure.json',
  'fixtures/success.expected.md', 'fixtures/failure.expected.md'
];
for (const file of required) {
  if (!existsSync(resolve(root, file))) throw new Error(`缺少必要产物：${file}`);
}
const success = JSON.parse(readFileSync(resolve(root, 'fixtures/success.json'), 'utf8'));
const failure = JSON.parse(readFileSync(resolve(root, 'fixtures/failure.json'), 'utf8'));
const successExpected = readFileSync(resolve(root, 'fixtures/success.expected.md'), 'utf8');
const failureExpected = readFileSync(resolve(root, 'fixtures/failure.expected.md'), 'utf8');
if (!success.product?.name || !success.store_policy?.shipping || !success.buyer_question) throw new Error('成功样例不具备可答复资料');
if (failure.product || failure.store_policy || !failure.buyer_question) throw new Error('失败样例必须只保留问题，以检验资料缺失');
if (!/售前/.test(successExpected) || !/48 小时/.test(successExpected) || !/库存需要为您核实/.test(successExpected) || /有米白色款/.test(successExpected) || /库存为用户提供的商品资料/.test(successExpected)) throw new Error('成功预期未保留事实和库存确认边界');
if (!/需人工确认/.test(failureExpected) || !/订单号/.test(failureExpected) || /可以马上退款/.test(failureExpected)) throw new Error('失败预期未识别缺失或存在越权承诺');
const icon = readFileSync(resolve(root, 'icon-512.png'));
if (icon.subarray(0, 8).compare(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10])) !== 0) throw new Error('图标不是 PNG');
if (icon.readUInt32BE(16) !== 512 || icon.readUInt32BE(20) !== 512) throw new Error('图标必须为 512×512 PNG');
const manifest = readFileSync(resolve(root, 'manifest.yaml'), 'utf8');
for (const key of ['description:', 'tags:', 'trigger_words:', 'self_test:']) {
  if (!manifest.includes(key)) throw new Error(`manifest 缺少展示字段：${key}`);
}
if (!/version: 1\.0\.3\b/.test(manifest)) throw new Error('manifest 版本必须为 1.0.3');
if (!/license: MIT-0\b/.test(manifest) || !readFileSync(resolve(root, 'LICENSE'), 'utf8').startsWith('MIT No Attribution')) throw new Error('package license must be MIT-0');
console.log('self-test passed: files, fixtures, safety boundaries, PNG signature, and manifest metadata verified. (Structural checks only; not a model behavior evaluation.)');
