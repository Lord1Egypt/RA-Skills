import assert from 'node:assert/strict';
import test from 'node:test';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const bucket = 'example-1250000000';
const region = 'ap-guangzhou';
const host = `${bucket}.ci.${region}.myqcloud.com`;
const services = [
  ['ci', 'ci-bucket', '/', 'CIBucket'],
  ['document', 'doc-process-bucket', '/docbucket', 'DocProcessBucket'],
  ['media', 'media-bucket', '/mediabucket', 'MediaBucket'],
  ['voice', 'asr-bucket', '/asrbucket', 'AsrBucket'],
  ['file', 'file-process-bucket', '/file_bucket', 'FileProcessBucket'],
  ['asyncImage', 'async-image-process-bucket', '/picbucket', 'PicProcessBucket'],
  ['asyncContentRecognition', 'ai-process-bucket', '/ai_bucket', 'AiProcessBucket'],
];

// Exercise the real CLI with fabricated credentials. No network transport or
// local credential file is available; stubs report only request routing fields.
const preload = `
import http from 'node:http';
import https from 'node:https';
import net from 'node:net';
import tls from 'node:tls';
import fs from 'node:fs';
import Module, { syncBuiltinESMExports } from 'node:module';
const deny = () => { throw new Error('real network forbidden in CI compatibility fixture'); };
http.request = http.get = https.request = https.get = net.connect = net.createConnection = tls.connect = deny;
const exists = fs.existsSync;
fs.existsSync = path => /(?:^|\\/)\\.env(?:\\.enc)?$/.test(String(path)) ? false : exists(path);
syncBuiltinESMExports();
Date.now = () => 1700000000000;
const record = request => process.stderr.write('COMPAT_REQUEST ' + JSON.stringify(request) + '\\n');
const load = Module._load;
Module._load = function (name, ...args) {
  if (name === 'cos-nodejs-sdk-v5') return class {
    request(params, callback) {
      const url = params.Url ? new URL(params.Url) : null;
      record({ transport: 'sdk', method: params.Method, pathname: url?.pathname || params.Key });
      callback(null, { fixture: 'sdk-result' });
    }
  };
  return load.call(this, name, ...args);
};
let activated = false;
globalThis.fetch = async (input, options) => {
  const url = new URL(input);
  record({ transport: 'fetch', method: options.method, host: url.hostname,
    pathname: url.pathname, query: Object.fromEntries(url.searchParams) });
  let body = '<Response></Response>';
  if (process.env.FIXTURE_ERROR === '1') {
    return new Response('<Error><Code>AccessDenied</Code><Message>fixture denied</Message></Error>',
      { status: 403, headers: { 'x-cos-request-id': 'fixture-request' } });
  }
  if (process.env.FIXTURE_CONFIRMED_EXECUTION === '1') {
    if (options.method === 'PUT' || options.method === 'POST') activated = true;
    const list = { '/docbucket': 'DocBucketList', '/mediabucket': 'MediaBucketList', '/asrbucket': 'AsrBucketList',
      '/file_bucket': 'FileBucketList', '/picbucket': 'PicBucketList', '/ai_bucket': 'AiBucketList' }[url.pathname];
    if (activated && list) body = '<Response><' + list + '><BucketId>example-1250000000</BucketId></' + list + '></Response>';
  }
  if (url.pathname === '/' && options.method === 'GET') body = JSON.stringify({ CIStatus: activated ? 'on' : process.env.FIXTURE_CI_STATUS || 'off' });
  return new Response(body, { status: 200, headers: { 'x-cos-request-id': 'fixture-request' } });
};
`;

function runCli(script, args, { strict = false, fail = false, ciStatus = 'off', confirmedExecution = false } = {}) {
  const file = fileURLToPath(new URL(`../${script}`, import.meta.url));
  const result = spawnSync(process.execPath, ['--import', `data:text/javascript,${encodeURIComponent(preload)}`, file,
    ...args, '--bucket', bucket, '--region', region], {
    env: { KIKI: strict ? '1' : '0', FIXTURE_ERROR: fail ? '1' : '0', FIXTURE_CI_STATUS: ciStatus, FIXTURE_CONFIRMED_EXECUTION: confirmedExecution ? '1' : '0',
      TENCENTCLOUD_SECRET_ID: 'fixture-id', TENCENTCLOUD_SECRET_KEY: 'fixture-key', TENCENTCLOUD_TOKEN: 'fixture-token' },
    encoding: 'utf8', timeout: 10000,
  });
  assert.equal(result.error, undefined);
  const lines = result.stderr.split('\n');
  const calls = lines.filter(line => line.startsWith('COMPAT_REQUEST ')).map(line => JSON.parse(line.slice(15)));
  const diagnostics = lines.filter(line => !line.startsWith('COMPAT_REQUEST ')).join('\n');
  const payload = JSON.parse(result.stdout || diagnostics);
  return { status: result.status, payload, calls };
}

function requestSummary(method, pathname, query = {}, status = 200) {
  return { method, host, pathname, query, status, requestId: 'fixture-request', elapsedMs: 0 };
}

function assertNoActivation(payload) {
  for (const field of ['activationStatus', 'activationError', 'interaction', 'clientAction']) {
    assert.equal(Object.hasOwn(payload, field), false, `unexpected ${field}`);
  }
}

test('公开模式七种创建和关闭保持原请求、完整成功输出形状', () => {
  for (const [service, command, pathname, api] of services) {
    for (const operation of ['create', 'delete']) {
      const action = `${operation}-${command}`;
      const method = service === 'ci' ? 'PUT' : operation === 'create' ? 'POST' : 'DELETE';
      const query = service === 'ci' && operation === 'delete' ? { unbind: '' } : {};
      const result = runCli('cos_node.mjs', [action]);
      assert.equal(result.status, 0, action);
      assert.deepEqual(result.calls, [{ transport: 'fetch', method, host, pathname, query }], action);
      assert.deepEqual(result.payload, {
        success: true, action, apiAction: `${operation === 'create' ? 'Create' : 'Delete'}${api}`,
        service, bucket, region, operation, request: requestSummary(method, pathname, query),
      }, action);
    }
  }
});

test('三个共用输出器的失败仍保留原错误形状；不增加开通契约字段', () => {
  for (const [service, command, pathname] of [services[1], services[5], services[6]]) {
    for (const operation of ['create', 'delete']) {
      const action = `${operation}-${command}`;
      const method = operation === 'create' ? 'POST' : 'DELETE';
      const result = runCli('cos_node.mjs', [action], { fail: true });
      assert.equal(result.status, 1, `${service} ${operation}`);
      assert.deepEqual(result.payload, {
        success: false, action, mode: 'public', error: 'fixture denied', code: 'AccessDenied',
        request: requestSummary(method, pathname, {}, 403),
      });
    }
  }
});

test('两种异步桶列表查询在 public/KiKi 中保留原输出与请求', () => {
  for (const strict of [false, true]) {
    for (const [service, action, pathname, apiAction] of [
      ['asyncImage', 'describe-async-image-process-buckets', '/picbucket', 'DescribePicProcessBucket'],
      ['asyncContentRecognition', 'describe-ai-process-buckets', '/ai_bucket', 'DescribeAiProcessBucket'],
    ]) {
      const result = runCli('cos_node.mjs', [action], { strict });
      const query = { bucketNames: bucket, pageNumber: '1', pageSize: '10' };
      assert.equal(result.status, 0);
      assert.deepEqual(result.payload, {
        success: true, action, apiAction, service, region,
        request: { ...requestSummary('GET', pathname, query), host: `ci.${region}.myqcloud.com` },
        totalCount: 0, pageNumber: 1, pageSize: 10, buckets: [],
      });
      assert.deepEqual(result.calls, [{ transport: 'fetch', method: 'GET',
        host: `ci.${region}.myqcloud.com`, pathname, query }]);
    }
  }
});

test('未指定 required-service 的状态查询不添加任何交互，public/KiKi 结果一致', () => {
  for (const ciStatus of ['off', 'on']) {
    const publicResult = runCli('ci_api.mjs', ['ci-service-status'], { ciStatus });
    const strictResult = runCli('ci_api.mjs', ['ci-service-status'], { ciStatus, strict: true });
    assert.equal(publicResult.status, 0);
    assert.equal(strictResult.status, 0);
    assertNoActivation(publicResult.payload);
    assertNoActivation(strictResult.payload);
    const { runtime: publicRuntime, ...publicStatus } = publicResult.payload;
    const { runtime: strictRuntime, ...strictStatus } = strictResult.payload;
    assert.equal(publicRuntime.mode, 'public');
    assert.equal(strictRuntime.mode, 'strict');
    assert.deepEqual(strictStatus, publicStatus);
    assert.deepEqual(strictResult.calls, publicResult.calls);
    assert.equal(publicResult.calls.length, ciStatus === 'off' ? 1 : 7);
    assert.ok(publicResult.calls.every(call => call.method === 'GET'));
  }
});

test('KiKi 七种创建仅预检，新增字段限定在 precheck；关闭继续由原策略拒绝', () => {
  for (const [service, command] of services) {
    const action = `create-${command}`;
    const result = runCli('cos_node.mjs', [action], { strict: true });
    assert.equal(result.status, 0, action);
    assert.equal(result.payload.operation, 'precheck');
    assert.equal(result.payload.ok, true);
    assert.equal(result.payload.success, true);
    assert.equal(result.payload.tool, action);
    assert.equal(result.payload.interaction.service, service);
    assert.equal(result.payload.activationStatus, 'requires_confirmation');
    assert.deepEqual(JSON.parse(result.payload.clientAction.command), { action: 'requestCiActivation', ...result.payload.interaction });
    assert.deepEqual(result.calls, [{ transport: 'fetch', method: 'GET', host, pathname: '/', query: {} }]);
    const deleted = runCli('cos_node.mjs', [`delete-${command}`], { strict: true });
    assert.equal(deleted.status, 1);
    assert.equal(deleted.payload.code, 'ActionDenied');
    assertNoActivation(deleted.payload);
    assert.deepEqual(deleted.calls, []);
  }
});

test('KiKi 非开通 CI 请求维持 SDK 路由与原输出；正常任务端点不误拦截', () => {
  for (const [method, path] of [
    ['GET', '/'], ['GET', 'docbucket'], ['POST', 'jobs'], ['POST', 'doc_jobs'],
    ['POST', 'file_jobs'], ['POST', 'asr_jobs'], ['POST', 'image/auditing'],
    ['POST', 'dataset'], ['POST', 'ai_bucket/jobs'], ['PUT', 'jobs/example-job'],
  ]) {
    const result = runCli('cos_node.mjs', ['ci-request', '--method', method, '--path', path], { strict: true });
    assert.equal(result.status, 0, `${method} ${path}`);
    assert.deepEqual(result.payload, { success: true, action: 'ci-request', path, method, data: { fixture: 'sdk-result' } });
    assert.deepEqual(result.calls, [{ transport: 'sdk', method, pathname: `/${path}` }]);
  }
  const image = runCli('cos_node.mjs', ['image-info', '--key', 'fixture.webp'], { strict: true });
  assert.equal(image.status, 0);
  assert.deepEqual(image.payload, { success: true, action: 'image-info', key: 'fixture.webp', data: { fixture: 'sdk-result' } });
  assert.deepEqual(image.calls, [{ transport: 'sdk', method: 'GET', pathname: 'fixture.webp' }]);
});

test('公开模式通用开通请求继续走 SDK，KiKi 等价请求只返回预检', () => {
  for (const [service, , pathname] of services) {
    const method = service === 'ci' ? 'PUT' : 'POST';
    const args = ['ci-request', '--method', method, '--path', pathname];
    const publicResult = runCli('cos_node.mjs', args);
    assert.equal(publicResult.status, 0);
    assert.deepEqual(publicResult.payload, { success: true, action: 'ci-request', path: pathname, method, data: { fixture: 'sdk-result' } });
    assert.deepEqual(publicResult.calls, [{ transport: 'sdk', method, pathname: `/${pathname}` }]);
    const strictResult = runCli('cos_node.mjs', args, { strict: true });
    assert.equal(strictResult.status, 0);
    assert.equal(strictResult.payload.operation, 'precheck');
    assert.equal(strictResult.payload.interaction.service, service);
    assert.ok(strictResult.calls.every(call => call.transport === 'fetch' && call.method === 'GET'));
  }
});

const confirmationFor = service => ({
  type: 'ci_activation_decision', version: 1, status: 'confirmed', bucket, region, service, toolCallId: 'fixture-ci-call',
});
test('KiKi 七个专用开通 CLI 原样接收确认，预检后只写一次并复查；回执不进入输出', () => {
  for (const [service, command, pathname] of services) {
    const result = runCli('cos_node.mjs', ['create-' + command, '--activation-confirmation', JSON.stringify(confirmationFor(service))],
      { strict: true, confirmedExecution: true });
    assert.equal(result.status, 0, JSON.stringify(result.payload));
    assert.equal(result.payload.activationStatus, 'enabled');
    assert.equal(result.payload.operation, 'create');
    const writes = result.calls.filter(call => call.method !== 'GET');
    assert.deepEqual(writes, [{ transport: 'fetch', method: service === 'ci' ? 'PUT' : 'POST', host, pathname, query: {} }]);
    assert.equal(result.calls[0].method, 'GET');
    assert.equal(result.calls.at(-1).method, 'GET');
    assert.equal(JSON.stringify(result.payload).includes('ci_activation_decision'), false);
  }
});
test('新确认参数不放行通用 ci-request，不放行关闭，不更改公开模式输出', () => {
  const args = ['--activation-confirmation', JSON.stringify(confirmationFor('ci'))];
  const raw = runCli('cos_node.mjs', ['ci-request', '--method', 'PUT', '--path', '/', ...args], { strict: true });
  assert.equal(raw.payload.operation, 'precheck');
  assert.ok(raw.calls.every(call => call.method === 'GET'));
  const deleted = runCli('cos_node.mjs', ['delete-ci-bucket', ...args], { strict: true });
  assert.equal(deleted.payload.code, 'ActionDenied');
  assert.equal(deleted.calls.length, 0);
  const oldPublic = runCli('cos_node.mjs', ['create-ci-bucket']);
  const newPublic = runCli('cos_node.mjs', ['create-ci-bucket', ...args]);
  assert.deepEqual(newPublic, oldPublic);
});
test('KiKi 无效或跨范围确认在请求前拒绝，已开启时不重复写入', () => {
  for (const override of [{ status: 'cancelled' }, { bucket: 'other-1250000000' }, { region: 'ap-beijing' },
    { service: 'media' }, { toolCallId: '' }, { version: 2 }, { confirmed: true }]) {
    const result = runCli('cos_node.mjs', ['create-ci-bucket', '--activation-confirmation',
      JSON.stringify({ ...confirmationFor('ci'), ...override })], { strict: true });
    assert.equal(result.status, 1);
    assert.equal(result.payload.code, 'InvalidCiActivationConfirmation');
    assert.equal(result.calls.length, 0);
  }
  const result = runCli('cos_node.mjs', ['create-ci-bucket', '--activation-confirmation', JSON.stringify(confirmationFor('ci'))],
    { strict: true, ciStatus: 'on' });
  assert.equal(result.payload.activationStatus, 'already_enabled');
  assert.ok(result.calls.every(call => call.method === 'GET'));
});
