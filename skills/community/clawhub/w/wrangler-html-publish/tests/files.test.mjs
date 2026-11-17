import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { defaults, archive, stage } from '../scripts/files.mjs';

const sha = x => crypto.createHash('sha256').update(x).digest('hex');
function sandbox(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'html-publish-test-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  return root;
}
function plan(root, files) {
  return { project: 'synthetic-example', branch: 'main', files: files.map(([source, target]) => ({ root, source, target, sha256: sha(fs.readFileSync(path.join(root, source))) })) };
}

test('默认目录跟随当前用户，配置支持环境变量覆盖', () => {
  const d = defaults({}, path.join(os.tmpdir(), 'another-user'));
  assert.equal(d.archive, path.join(os.tmpdir(), 'another-user', 'Documents', 'published-html'));
  assert.equal(defaults({ HTML_PUBLISH_CONFIG: 'custom.json' }).config, 'custom.json');
  assert.equal(defaults({ XDG_CONFIG_HOME: '/custom-config' }).config, path.join('/custom-config', 'wrangler-html-publish', 'config.json'));
});
test('中文与空格路径归档，保持原文件，同名失败不覆盖', t => {
  const root = sandbox(t);
  const source = path.join(root, '合成 页面.html');
  fs.writeFileSync(source, '<title>synthetic</title>');
  const out = archive(source, path.join(root, '用户 目录'), 'report-one');
  assert.equal(fs.readFileSync(path.join(out, 'index.html'), 'utf8'), fs.readFileSync(source, 'utf8'));
  assert.throws(() => archive(source, path.join(root, '用户 目录'), 'report-one'));
  assert.throws(() => archive(source, root, '../escape'));
});
test('staging 保留 slug/资源/旧页，仅复制白名单，不包含草稿', t => {
  const root = sandbox(t);
  fs.writeFileSync(path.join(root, 'old.html'), 'old synthetic');
  fs.writeFileSync(path.join(root, 'new.html'), 'new synthetic');
  fs.writeFileSync(path.join(root, 'chart.svg'), '<svg/>');
  fs.writeFileSync(path.join(root, 'private.html'), 'synthetic private draft');
  const dest = path.join(root, 'stage');
  const result = stage(plan(root, [['old.html', 'old/index.html'], ['new.html', 'new/index.html'], ['chart.svg', 'new/assets/chart.svg']]), dest);
  assert.equal(result.files.length, 3);
  assert.equal(fs.readFileSync(path.join(dest, 'old/index.html'), 'utf8'), 'old synthetic');
  assert.ok(fs.existsSync(path.join(dest, 'new/assets/chart.svg')));
  assert.ok(!fs.existsSync(path.join(dest, 'private.html')));
});
test('审核后改动导致哈希不符，目标尚未创建', t => {
  const root = sandbox(t);
  fs.writeFileSync(path.join(root, 'page.html'), 'before');
  const p = plan(root, [['page.html', 'page/index.html']]);
  fs.writeFileSync(path.join(root, 'page.html'), 'after');
  const dest = path.join(root, 'stage');
  assert.throws(() => stage(p, dest), /变化/);
  assert.ok(!fs.existsSync(dest));
});
test('拒绝路径穿越、隐藏文件、后端配置和重复目标', t => {
  const root = sandbox(t);
  fs.writeFileSync(path.join(root, 'page.html'), 'synthetic');
  for (const target of ['../escape.html', '/absolute.html', 'a\\b.html', 'C:/page.html', '.env', 'functions/test.html', '_worker.js', 'wrangler.json', '_headers']) {
    assert.throws(() => stage(plan(root, [['page.html', target]]), path.join(root, 'stage')));
  }
  assert.throws(() => stage(plan(root, [['page.html', 'a.html'], ['page.html', 'A.html']]), path.join(root, 'stage')), /重复/);
});
test('已有 staging 不覆盖', t => {
  const root = sandbox(t);
  fs.writeFileSync(path.join(root, 'page.html'), 'synthetic');
  const dest = path.join(root, 'stage');
  fs.mkdirSync(dest);
  fs.writeFileSync(path.join(dest, 'keep.txt'), 'keep');
  assert.throws(() => stage(plan(root, [['page.html', 'page/index.html']]), dest));
  assert.equal(fs.readFileSync(path.join(dest, 'keep.txt'), 'utf8'), 'keep');
});
test('拒绝符号链接源', { skip: process.platform === 'win32' ? 'Windows 创建符号链接可能需要额外权限' : false }, t => {
  const root = sandbox(t);
  fs.writeFileSync(path.join(root, 'real.html'), 'synthetic');
  fs.symlinkSync(path.join(root, 'real.html'), path.join(root, 'linked.html'));
  assert.throws(() => stage(plan(root, [['linked.html', 'page/index.html']]), path.join(root, 'stage')), /符号链接/);
});
