#!/usr/bin/env node
import fs from 'node:fs';
import {execFileSync, spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md', 'LICENSE', 'icon-512.png', 'fixtures/success-page.json', 'fixtures/failure-unconfirmed-filter.json', 'fixtures/failure-unconfirmed-ownership.json'];
for (const file of required) if (!fs.existsSync(path.join(root, file))) throw new Error(`缺少 ${file}`);
const manifest = fs.readFileSync(path.join(root, 'manifest.yaml'), 'utf8');
const skill = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
if (!manifest.includes('name: shop-order-status-digest-free') || !manifest.includes('slug: shop-order-status-digest-free')) throw new Error('manifest 名称错误');
if (!manifest.includes('license: MIT-0') || !fs.readFileSync(path.join(root, 'LICENSE'), 'utf8').startsWith('MIT No Attribution')) throw new Error('MIT-0 metadata/license mismatch');
if (!skill.includes('不重复确认') || !skill.includes('若确实无法判断') || !skill.includes('严格只读') || skill.includes('草稿字段填充')) throw new Error('authorization/read-only policy mismatch');
for (const file of ['SKILL.md', 'README.md', 'README.en.md']) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  if (text.includes('github.com/xxjrq/easybr/releases/tag/v1.7.8')) throw new Error('stale EasyBR download URL');
  if (!text.includes('www.ebrower.com/down.html')) throw new Error(`missing official EasyBR download center in ${file}`);
}
if (!skill.includes('name: shop-order-status-digest-free')) throw new Error('SKILL frontmatter 名称错误');
const png = fs.readFileSync(path.join(root, 'icon-512.png'));
if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') throw new Error('图标不是 PNG');
if (png.readUInt32BE(16) !== 512 || png.readUInt32BE(20) !== 512) throw new Error('图标不是 512×512');
const successFixture = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/success-page.json'), 'utf8'));
const filterFixture = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/failure-unconfirmed-filter.json'), 'utf8'));
if (!successFixture.fixture_notice.includes('合成') || !filterFixture.fixture_notice.includes('合成')) throw new Error('offline order fixtures must be labeled synthetic');
if (successFixture.authorization?.explicit_in_current_request !== true) throw new Error('successful fixture must use explicit current-request authority');
const success = execFileSync(process.execPath, ['scripts/summarize-fixture.mjs', 'fixtures/success-page.json'], {cwd: root, encoding: 'utf8'});
const report = JSON.parse(success);
if (!report.reportable || report.status_counts['待发货'] !== 1 || report.needs_action.length !== 2) throw new Error('成功样例摘要不正确');
if (success.includes('DEMO-ORDER-001') || report.needs_action[0]?.order_id !== 'DEMO-…001') throw new Error('成功样例未遮盖完整订单号');
try {
  execFileSync(process.execPath, ['scripts/summarize-fixture.mjs', 'fixtures/failure-unconfirmed-filter.json'], {cwd: root, encoding: 'utf8', stdio: 'pipe'});
  throw new Error('未确认筛选时应拒绝报告');
} catch (error) {
  if (error.message === '未确认筛选时应拒绝报告') throw error;
  if (error.status !== 2 || !String(error.stdout).includes('不报告全店总数')) throw new Error('未确认筛选样例没有正确拒绝');
}
const ownership = spawnSync(process.execPath, ['scripts/summarize-fixture.mjs', 'fixtures/failure-unconfirmed-ownership.json'], {cwd: root, encoding: 'utf8'});
if (ownership.status !== 2 || !ownership.stdout.includes('当前请求未明确店铺归属或用户授权')) throw new Error('未确认订单归属时必须拒绝');
if (ownership.stdout.includes('DEMO-ORDER-001') || ownership.stdout.includes('status_counts')) throw new Error('未确认归属时泄露了订单数据');
console.log('self-test passed: metadata, synthetic fixture, masked digest, unconfirmed filter and ownership refusal verified');
