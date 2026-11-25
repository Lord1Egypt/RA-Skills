#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = [
  'SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md',
  'LICENSE', 'icon-512.png', 'fixtures/success-input.md', 'fixtures/success-expected.md',
  'fixtures/failure-missing-brief.md'
];
const fail = (message) => { console.error(`FAIL: ${message}`); process.exitCode = 1; };
for (const file of required) if (!existsSync(resolve(root, file))) fail(`missing ${file}`);

const skill = readFileSync(resolve(root, 'SKILL.md'), 'utf8');
const manifest = readFileSync(resolve(root, 'manifest.yaml'), 'utf8');
const good = readFileSync(resolve(root, 'fixtures/success-input.md'), 'utf8');
const expected = readFileSync(resolve(root, 'fixtures/success-expected.md'), 'utf8');
const bad = readFileSync(resolve(root, 'fixtures/failure-missing-brief.md'), 'utf8');
for (const heading of ['## 最终提示词', '## 镜头动作顺序', '## 连续性约束', '## 对比与待确认']) {
  if (!expected.includes(heading)) fail(`success reference lacks ${heading}`);
}
if (!good.includes('画面意图') || !good.includes('原始提示词')) fail('success input is not actionable');
if (!bad.includes('缺失') || !bad.includes('主体')) fail('failure fixture does not demonstrate missing brief');
if (bad.includes('时长或镜头数均未提供') || bad.includes('先索取主体、想让观众感受到什么、时长/镜头数')) fail('failure fixture wrongly treats duration or shot count as required');
if (!bad.includes('默认一个 5–8 秒镜头')) fail('failure fixture does not state the optional-duration default');
if (expected.includes('浅棕色咖啡')) fail('success reference invents an unsupported product attribute');
if (!skill.includes('不调用视频生成 API') || !skill.includes('不编造任何模型参数')) fail('skill safety boundaries missing');
if (!skill.includes('时长或镜头数（可选；未知时默认一个 5–8 秒镜头')) fail('skill optional-duration rule missing');
if (!manifest.includes('self_test: node scripts/self-test.mjs')) fail('manifest self_test mismatch');
console.log('PASS: structure, working example, failure example, and boundaries verified.');
