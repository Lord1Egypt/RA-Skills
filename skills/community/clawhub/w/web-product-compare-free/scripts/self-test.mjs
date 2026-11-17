#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'fixtures/success-input.json', 'fixtures/failure-input.json', 'fixtures/expected-report.md'];
const errors = [];
for (const file of required) if (!existsSync(resolve(root, file))) errors.push(`缺少文件：${file}`);
const load = (file) => readFileSync(resolve(root, file), 'utf8');
if (!errors.length) {
  const valid = JSON.parse(load('fixtures/success-input.json'));
  const invalid = JSON.parse(load('fixtures/failure-input.json'));
  const usable = (value) => value.products?.length >= 2 && value.products?.length <= 5 && value.products.every((item) => item.name && item.url && item.visiblePrice && item.specifications && item.afterSales && item.scenarios);
  if (!usable(valid)) errors.push('成功样例不具备 2–5 个完整可见字段商品');
  if (usable(invalid)) errors.push('失败样例没有被识别为资料缺失');
  const skill = load('SKILL.md');
  const agent = load('agents/openai.yaml');
  const manifest = load('manifest.yaml');
  const report = load('fixtures/expected-report.md');
  const version = manifest.match(/^version:\s*(.+)$/m)?.[1]?.trim();
  for (const needle of ['finally', 'close_session', 'browserId', '2–5', '只读']) if (!skill.includes(needle)) errors.push(`SKILL.md 缺少运行约束：${needle}`);
  for (const needle of ['github:', 'gitee:', '一任务一 session']) if (!agent.includes(needle)) errors.push(`agents/openai.yaml 缺少：${needle}`);
  for (const needle of ['self_test:', 'trigger_words:', 'tags:']) if (!manifest.includes(needle)) errors.push(`manifest.yaml 缺少：${needle}`);
  for (const needle of ['读取日期：2026-10-04', 'https://shop.example.test/products/light-a', '选择建议']) if (!report.includes(needle)) errors.push(`成功报告缺少：${needle}`);
  if (!version) errors.push('manifest.yaml 缺少可识别的 version');
  // dist 是发布流水线生成的私有产物；克隆或安装后的结构自检不依赖它。
}
console.log(JSON.stringify({ ok: errors.length === 0, checks: required.length, errors }, null, 2));
if (errors.length) process.exitCode = 1;
