#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const required = [
  'SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md',
  'LICENSE', 'icon-512.png', 'fixtures/success-input.yaml', 'fixtures/success-output.md',
  'fixtures/failure-input.yaml', 'fixtures/failure-expected.md'
];
const fail = (message) => { console.error(`FAIL: ${message}`); process.exitCode = 1; };
for (const path of required) if (!existsSync(resolve(root, path))) fail(`missing ${path}`);

const read = (path) => readFileSync(resolve(root, path), 'utf8');
if (!process.exitCode) {
  const skill = read('SKILL.md');
  const manifest = read('manifest.yaml');
  const agent = read('agents/openai.yaml');
  const success = read('fixtures/success-input.yaml');
  const output = read('fixtures/success-output.md');
  const failure = read('fixtures/failure-input.yaml');
  if (!skill.startsWith('---\nname: selfmedia-title-lab-cn\n')) fail('invalid SKILL frontmatter');
  if (!manifest.includes('self_test: node scripts/self-test.mjs')) fail('manifest self_test is not runnable');
  if (!agent.includes('display_name: 自媒体标题改写')) fail('agent display name mismatch');
  for (const platform of ['抖音', '小红书', 'B站']) {
    if (!success.includes(platform) || !output.includes(`### ${platform}`)) fail(`success fixture lacks ${platform}`);
  }
  if (failure.includes('核心收益:')) fail('failure fixture must omit core benefit');
  if (!output.includes('## 推荐使用') || !output.includes('**契合原因：**')) fail('success output lacks recommendation');
}
if (!process.exitCode) console.log('PASS: repository structure and success/failure fixtures are valid.');
