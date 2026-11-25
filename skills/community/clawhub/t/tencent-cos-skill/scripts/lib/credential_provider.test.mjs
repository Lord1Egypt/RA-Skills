import assert from 'node:assert/strict';
import test from 'node:test';
import { spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  callerContext,
  credentialProviderHint,
  loadProviderCredentials,
  resetCredentialProvider,
  resolveCredentialProcess,
} from './credential_provider.mjs';

const dir = mkdtempSync(join(tmpdir(), 'cos-provider-test-'));
test.after(() => rmSync(dir, { recursive: true, force: true }));

/** 假提供方：按 FAKE_MODE 输出；把收到的调用上下文写进 secretKey 便于断言 */
const fake = join(dir, 'provider.mjs');
// Windows 上子进程缺 SystemRoot 等变量时 node 可能起不来，测试用的精简 env 带上这些
const winEssentials = Object.fromEntries(['SystemRoot', 'ComSpec', 'PATHEXT', 'TEMP', 'TMP']
  .filter(k => process.env[k] !== undefined).map(k => [k, process.env[k]]));
writeFileSync(fake, `
const mode = process.env.FAKE_MODE || 'ok';
const ctx = process.env.TENCENT_COS_CREDENTIAL_CONTEXT || '';
if (mode === 'ok') {
  console.log(JSON.stringify({ success: true, secretId: 'AKIDfake', secretKey: 'key|' + ctx, sessionToken: 'fake-token',
    expiredTime: 1700007200, bucket: 'example-1250000000', region: 'ap-guangzhou' }));
} else if (mode === 'not-logged-in') {
  console.log(JSON.stringify({ success: false, code: 'NotLoggedIn', error: '尚未登录腾讯云', next: 'tencentcloud-cos-oauth login --daemon' }));
  process.exit(1);
} else if (mode === 'crash') {
  console.error('Error: boom');
  process.exit(3);
} else if (mode === 'killed') {
  process.kill(process.pid, 'SIGKILL');
} else if (mode === 'noisy') {
  process.stderr.write('w'.repeat(300 * 1024));
  console.log(JSON.stringify({ success: true, secretId: 'AKIDnoisy', secretKey: 'k', sessionToken: 't' }));
} else if (mode === 'hang') {
  setTimeout(() => {}, 60000);
} else {
  console.log('hello');
}
`);
const explicit = (mode, extra = {}) => ({
  ...winEssentials,
  TENCENT_COS_CREDENTIAL_PROCESS: JSON.stringify([process.execPath, fake]),
  FAKE_MODE: mode,
  PATH: process.env.PATH,
  ...extra,
});
const argv = ['node', '/skill/scripts/cos_node.mjs', 'list'];

test('解析提供方命令：默认 tencentcloud-cos-oauth credential --json，可显式配置或关闭', () => {
  assert.deepEqual(resolveCredentialProcess({}), { command: 'tencentcloud-cos-oauth', args: ['credential', '--json'], explicit: false });
  assert.deepEqual(resolveCredentialProcess({ TENCENT_COS_CREDENTIAL_PROCESS: '["node","/a b/p.mjs"]' }).args, ['/a b/p.mjs']);
  assert.deepEqual(resolveCredentialProcess({ TENCENT_COS_CREDENTIAL_PROCESS: 'my-cred  --json' }).args, ['--json']);
  for (const off of ['off', 'OFF', '0', 'false', 'none']) {
    assert.equal(resolveCredentialProcess({ TENCENT_COS_CREDENTIAL_PROCESS: off }), null);
  }
  assert.deepEqual(resolveCredentialProcess({ TENCENT_COS_CREDENTIAL_PROCESS: '[1]' }), { invalid: true });
});

test('调用上下文只含入口与动作名', () => {
  assert.deepEqual(callerContext(['node', '/s/scripts/cos_node.mjs', 'sign-url', '--key', 'a']), { entry: 'cos', action: 'sign-url' });
  assert.deepEqual(callerContext(['node', '/s/scripts/ci_api.mjs', 'list-datasets']), { entry: 'ci', action: 'list-datasets' });
  assert.deepEqual(callerContext(['node', '/s/scripts/preview_gen.mjs', '/tmp/spec.json']), { entry: 'preview', action: 'preview' });
  assert.deepEqual(callerContext(['node', '/s/scripts/cos_node.mjs', '/etc/passwd']), { entry: 'cos' });
  assert.equal(callerContext(['node', '/tmp/other.mjs', 'list']), null);
});

test('成功：按临时密钥写入 TENCENT_COS_*，桶与地域都未设置时写入默认值', () => {
  resetCredentialProvider();
  const env = explicit('ok');
  assert.equal(loadProviderCredentials(env, { argv }), true);
  assert.equal(env.TENCENT_COS_SECRET_ID, 'AKIDfake');
  assert.equal(env.TENCENT_COS_SECRET_KEY, 'key|{"entry":"cos","action":"list"}');
  assert.equal(env.TENCENT_COS_TOKEN, 'fake-token');
  assert.equal(env.TENCENT_COS_BUCKET, 'example-1250000000');
  assert.equal(env.TENCENT_COS_REGION, 'ap-guangzhou');
  // 每个进程只执行一次
  assert.equal(loadProviderCredentials(explicit('ok'), { argv }), false);

  resetCredentialProvider();
  const own = explicit('ok', { TENCENT_COS_BUCKET: 'mine-1250000000' });
  loadProviderCredentials(own, { argv });
  assert.equal(own.TENCENT_COS_BUCKET, 'mine-1250000000');
  assert.equal(own.TENCENT_COS_REGION, undefined);
});

test('已有凭证时不调用提供方：运行时 TENCENTCLOUD_*、本地 TENCENT_COS_*', () => {
  for (const extra of [{ TENCENTCLOUD_SECRET_ID: 'rt' }, { TENCENTCLOUD_TOKEN: 'rt' }, { TENCENT_COS_SECRET_ID: 'l', TENCENT_COS_SECRET_KEY: 'k' }]) {
    resetCredentialProvider();
    const env = explicit('ok', extra);
    assert.equal(loadProviderCredentials(env, { argv }), false);
    assert.notEqual(env.TENCENT_COS_SECRET_ID, 'AKIDfake');
  }
});

test('失败：未登录时缺少凭证报错附带下一步；默认命令不存在时静默回落', () => {
  resetCredentialProvider();
  assert.equal(loadProviderCredentials(explicit('not-logged-in'), { argv }), false);
  assert.match(credentialProviderHint(), /尚未登录腾讯云（NotLoggedIn），下一步：tencentcloud-cos-oauth login --daemon/);

  resetCredentialProvider();
  assert.equal(loadProviderCredentials(explicit('garbage'), { argv }), false);
  assert.match(credentialProviderHint(), /InvalidCredentialProcessOutput/);

  resetCredentialProvider();
  assert.equal(loadProviderCredentials({ PATH: dir }, { argv, platform: 'darwin' }), false);
  assert.equal(credentialProviderHint(), '');

  // Windows 默认命令不存在（PATH + PATHEXT 都找不到），同样静默
  resetCredentialProvider();
  assert.equal(loadProviderCredentials({ PATH: dir }, { argv, platform: 'win32' }), false);
  assert.equal(credentialProviderHint(), '');
});

test('失败：提供方超时、异常退出、显式命令不存在时，缺少凭证报错附带原因', () => {
  resetCredentialProvider();
  assert.equal(loadProviderCredentials(explicit('hang'), { argv, timeoutMs: 500 }), false);
  assert.match(credentialProviderHint(), /CredentialProcessTimeout/);

  resetCredentialProvider();
  assert.equal(loadProviderCredentials(explicit('crash'), { argv }), false);
  assert.match(credentialProviderHint(), /异常退出（退出码 3）（CredentialProcessFailed）/);

  resetCredentialProvider();
  assert.equal(loadProviderCredentials(explicit('killed'), { argv }), false);
  assert.match(credentialProviderHint(), process.platform === 'win32' ? /异常退出（退出码 1）/ : /异常退出（信号 SIGKILL）/);

  resetCredentialProvider();
  const missing = { TENCENT_COS_CREDENTIAL_PROCESS: JSON.stringify([join(dir, 'no-such-provider')]), PATH: process.env.PATH };
  assert.equal(loadProviderCredentials(missing, { argv }), false);
  assert.match(credentialProviderHint(), /CredentialProcessNotFound/);
});

test('提供方往 stderr 输出很多内容时仍能取到凭证', () => {
  resetCredentialProvider();
  const env = explicit('noisy');
  assert.equal(loadProviderCredentials(env, { argv }), true, credentialProviderHint());
  assert.equal(env.TENCENT_COS_SECRET_ID, 'AKIDnoisy');
});

test('Windows：按 PATH + PATHEXT 找到 .cmd（路径含空格），不执行当前目录下的同名命令', () => {
  // 打桩的 npm 全局命令：Windows 上是 .cmd 批处理，其他系统上用同名 sh 脚本模拟（经 /bin/sh 启动）
  const writeShim = (file, provider) => {
    writeFileSync(file, process.platform === 'win32'
      ? `@"${process.execPath}" "${provider}" %*\r\n`
      : `#!/bin/sh\nexec "${process.execPath}" "${provider}" "$@"\n`, { mode: 0o755 });
  };
  const provider = join(dir, 'argv-provider.mjs');
  writeFileSync(provider, `console.log(JSON.stringify({ success: true, secretId: process.env.SHIM_ID || 'AKIDpath', secretKey: process.argv.slice(2).join(' '), sessionToken: 't' }));\n`);
  const bin = join(dir, 'npm global');
  const decoy = join(dir, 'workspace');
  mkdirSync(bin);
  mkdirSync(decoy);
  writeShim(join(bin, 'tencentcloud-cos-oauth.cmd'), provider);
  writeFileSync(join(decoy, 'decoy.mjs'), `console.log(JSON.stringify({ success: true, secretId: 'DECOY', secretKey: 'x' }));\n`);
  writeShim(join(decoy, 'tencentcloud-cos-oauth.cmd'), join(decoy, 'decoy.mjs'));

  const cwd = process.cwd();
  process.chdir(decoy);
  try {
    resetCredentialProvider();
    const env = { ...winEssentials, PATH: bin, PATHEXT: '.COM;.EXE;.BAT;.CMD' };
    assert.equal(loadProviderCredentials(env, { argv, platform: 'win32' }), true, credentialProviderHint());
    assert.equal(env.TENCENT_COS_SECRET_ID, 'AKIDpath');
    assert.equal(env.TENCENT_COS_SECRET_KEY, 'credential --json');

    // 参数含 cmd.exe 无法安全传递的字符：拒绝执行
    resetCredentialProvider();
    const bad = { ...winEssentials, TENCENT_COS_CREDENTIAL_PROCESS: JSON.stringify([join(bin, 'tencentcloud-cos-oauth.cmd'), '50%']) };
    assert.equal(loadProviderCredentials(bad, { argv, platform: 'win32' }), false);
    assert.match(credentialProviderHint(), /InvalidCredentialProcess/);
  } finally {
    process.chdir(cwd);
  }
});

// 端到端：真实 cos_node.mjs + SDK 打桩（无网络），验证提供方凭证与默认桶进入 SDK
const preload = `
import fs from 'node:fs';
import Module, { syncBuiltinESMExports } from 'node:module';
const exists = fs.existsSync;
fs.existsSync = path => /(?:^|[\\\\/])\\.env(?:\\.enc)?$/.test(String(path)) ? false : exists(path);
syncBuiltinESMExports();
const load = Module._load;
Module._load = function (name, ...args) {
  if (name === 'cos-nodejs-sdk-v5') return class {
    constructor(o) { process.stderr.write('SDK_INIT ' + JSON.stringify({ id: o.SecretId, token: o.SecurityToken }) + '\\n'); }
    getObjectUrl(p, cb) { process.stderr.write('SDK_URL ' + JSON.stringify({ bucket: p.Bucket, region: p.Region }) + '\\n'); cb(null, { Url: 'https://example/a.jpg' }); }
  };
  return load.call(this, name, ...args);
};
`;
function runCosNode(mode, extraEnv = {}) {
  const file = fileURLToPath(new URL('../cos_node.mjs', import.meta.url));
  return spawnSync(process.execPath, ['--import', `data:text/javascript,${encodeURIComponent(preload)}`, file, 'sign-url', '--key', 'a.jpg'], {
    env: { ...explicit(mode), ...extraEnv }, encoding: 'utf8', timeout: 10000,
  });
}

test('端到端：cos_node.mjs 使用提供方的临时密钥与默认桶', () => {
  const r = runCosNode('ok');
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stderr, /SDK_INIT \{"id":"AKIDfake","token":"fake-token"\}/);
  assert.match(r.stderr, /SDK_URL \{"bucket":"example-1250000000","region":"ap-guangzhou"\}/);
});

test('端到端：未登录时报缺少凭证并给出下一步；严格模式不使用提供方', () => {
  const r = runCosNode('not-logged-in');
  assert.equal(r.status, 1);
  assert.match(r.stderr, /下一步：tencentcloud-cos-oauth login --daemon/);
  const strict = runCosNode('ok', { KIKI: '1' });
  assert.equal(strict.status, 1);
  assert.doesNotMatch(strict.stderr, /AKIDfake/);
});
