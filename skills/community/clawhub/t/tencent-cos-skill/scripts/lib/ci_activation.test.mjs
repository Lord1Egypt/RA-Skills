import assert from 'node:assert/strict';
import test from 'node:test';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import {
  CI_ACTIVATION_COMMANDS,
  assertCiActivationRequestAllowed,
  evaluateCiActivation,
  getCiActivationRequestService,
} from './ci_activation.mjs';
import { cosRequest } from './ci_client.mjs';
import { createCiService } from './ci_service_lifecycle.mjs';
import { queryCiServiceStatus } from './ci_service_status.mjs';

const bucket = 'example-1250000000';
const region = 'ap-guangzhou';
const creds = { secretId: 'test-id', secretKey: 'test-key', token: '', source: 'runtime' };
const options = { bucket, region, creds };
const servicePaths = {
  ci: '/', document: '/docbucket', media: '/mediabucket', voice: '/asrbucket',
  file: '/file_bucket', asyncImage: '/picbucket', asyncContentRecognition: '/ai_bucket',
};
const raw = (request, body, extra = {}) => ({
  ...request, ok: true, status: 200, requestId: 'fixture-request', elapsedMs: 1, body, ...extra,
});
const fail = (request, code) => raw(request, `<Error><Code>${code}</Code><Message>fixture error</Message></Error>`, { ok: false, status: 403 });

function assertExactClientAction(result) {
  assert.deepEqual(Object.keys(result.clientAction).sort(), ['command', 'skill']);
  assert.equal(result.clientAction.skill, 'tencentcloud-cos');
  assert.equal(typeof result.clientAction.command, 'string');
  assert.equal(result.clientAction.command, JSON.stringify({ action: 'requestCiActivation', ...result.interaction }));
  assert.deepEqual(JSON.parse(result.clientAction.command), { action: 'requestCiActivation', ...result.interaction });
}

function stubRequests(ciStatus = 'off', serviceResponse = '<Response></Response>') {
  const calls = [];
  return {
    calls,
    request: async request => {
      calls.push(request);
      assert.equal(request.method, 'GET', 'activation interception must never write');
      return request.pathname === '/'
        ? raw(request, JSON.stringify({ CIStatus: ciStatus }))
        : raw(request, serviceResponse);
    },
  };
}

test('固定 v1 契约只在任务前置查询要求服务时返回；纯状态查询不触发交互', async () => {
  const stub = stubRequests();
  const readOnly = await queryCiServiceStatus({ ...options, request: stub.request });
  assert.equal(readOnly.interaction, undefined);
  assert.equal(readOnly.clientAction, undefined);
  assert.equal(readOnly.activationStatus, undefined);
  const result = await queryCiServiceStatus({ ...options, request: stub.request, requiredService: 'ci' });
  assertExactClientAction(result);
  assert.deepEqual(result.interaction, {
    type: 'ci_activation', version: 1, status: 'requires_confirmation', bucket, region,
    service: 'ci', reason: 'ci_not_enabled', precheck: { ciBucketStatus: 'off', serviceStatus: 'disabled' },
  });
});

test('七个服务的严格模式开通全部转只读前置检查，模型 confirmed 参数无效', async () => {
  for (const service of Object.keys(CI_ACTIVATION_COMMANDS)) {
    const stub = stubRequests();
    const result = await createCiService({ ...options, service, request: stub.request, env: { KIKI: '1' }, confirmed: true });
    assert.equal(result.ok, true);
    assert.equal(result.tool, CI_ACTIVATION_COMMANDS[service]);
    assert.equal(result.operation, 'precheck');
    assert.equal(result.interaction.service, service);
    assert.equal(result.interaction.bucket, result.bucket);
    assert.equal(result.interaction.region, result.region);
    assert.equal(result.activationStatus, 'requires_confirmation');
    assertExactClientAction(result);
    assert.equal(stub.calls.length, 1);
  }
});

test('CI 已绑定但各目标子服务未开通时分别触发；CI 总服务已开通不伪造开通回执', async () => {
  for (const service of Object.keys(CI_ACTIVATION_COMMANDS)) {
    const stub = stubRequests('on');
    const result = await createCiService({ ...options, service, request: stub.request, env: { KIKI: '1' } });
    assert.equal(result.operation, 'precheck');
    if (service === 'ci') {
      assert.equal(result.activationStatus, 'already_enabled');
      assert.equal(result.interaction, undefined);
      assert.equal(result.clientAction, undefined);
    } else {
      assertExactClientAction(result);
      assert.equal(result.interaction.reason, 'service_not_enabled');
      assert.equal(result.interaction.service, service);
      assert.deepEqual(result.interaction.precheck, { ciBucketStatus: 'on', serviceStatus: 'disabled' });
    }
    assert.equal(stub.calls.length, 7);
  }
});

test('NoSuchBucket 可以触发；权限、归属和未知错误保留原错误且不触发', async () => {
  for (const code of ['NoSuchBucket', 'AccessDenied', 'UserNotBucketOwner', 'InternalError']) {
    const calls = [];
    const request = async requestOptions => {
      calls.push(requestOptions);
      assert.equal(requestOptions.method, 'GET');
      return fail(requestOptions, code);
    };
    const result = await createCiService({ ...options, service: 'ci', request, env: { KIKI: '1' } });
    assert.equal(result.ciBucketError.code, code);
    if (code === 'NoSuchBucket') {
      assertExactClientAction(result);
      assert.equal(result.interaction.reason, 'ci_not_enabled');
      assert.equal('error' in result.interaction.precheck, false);
    } else {
      assert.equal(result.ok, false);
      assert.equal(result.interaction, undefined);
      assert.equal(result.clientAction, undefined);
      assert.equal(result.error.code, code);
    }
  }
});

test('解绑中和子服务权限/未知错误不能伪装成未开通', async () => {
  const unbinding = stubRequests('unbinding');
  const result = await queryCiServiceStatus({ ...options, requiredService: 'media', request: unbinding.request });
  assert.equal(result.activationStatus, 'blocked');
  assert.equal(result.interaction, undefined);
  assert.equal(result.clientAction, undefined);
  for (const code of ['AccessDenied', 'InternalError']) {
    const status = await queryCiServiceStatus({
      ...options, requiredService: 'media',
      request: async request => request.pathname === '/' ? raw(request, '{"CIStatus":"on"}') : fail(request, code),
    });
    assert.equal(status.activationStatus, 'blocked');
    assert.equal(status.interaction, undefined);
    assert.equal(status.clientAction, undefined);
    assert.equal(status.activationError.code, code);
    assert.equal(status.dataProcessing.mediaProcessing.error.code, code);
  }
});

test('已开通子服务、缺失状态、伪成功状态和非法服务不会触发开通 UI', () => {
  const base = { bucket, region, ciBucketStatus: 'on' };
  assert.equal(evaluateCiActivation({ ...base, dataProcessing: { mediaProcessing: { status: 'enabled' } } }, 'media').activationStatus, 'already_enabled');
  assert.equal(evaluateCiActivation(base, 'media').activationStatus, 'blocked');
  assert.equal(evaluateCiActivation({ ...base, ciBucketError: { code: 'Unknown' } }, 'ci').activationStatus, 'blocked');
  for (const service of ['', true, 'asyncRecognition', '__proto__']) {
    assert.throws(() => evaluateCiActivation(base, service), error => error.code === 'InvalidArgs');
  }
});

test('阻塞或已开通的前置检查不会生成客户端动作', () => {
  for (const snapshot of [
    { bucket, region, ciBucketStatus: 'on' },
    { bucket, region, ciBucketStatus: 'unbinding' },
    { bucket, region, ciBucketStatus: 'noAuth', ciBucketError: { code: 'AccessDenied' } },
    { bucket, region, ciBucketStatus: 'off', ciBucketError: { code: 'UserNotBucketOwner' } },
    { bucket, region, ciBucketStatus: 'on', ciBucketError: { code: 'InternalError' } },
  ]) {
    const result = evaluateCiActivation(snapshot, 'ci');
    assert.equal(result.clientAction, undefined);
    assert.equal(result.interaction, undefined);
  }
});

test('非法 required-service 在发请求前拒绝', async () => {
  await assert.rejects(queryCiServiceStatus({ ...options, requiredService: true, request: () => assert.fail('must not request') }), error => error.code === 'InvalidArgs');
});

test('已知开通端点归一化并阻止请求层直接写入；正常查询和 COS 请求不受影响', () => {
  const host = `${bucket}.ci.${region}.myqcloud.com`;
  for (const [service, pathname] of Object.entries(servicePaths)) {
    const method = service === 'ci' ? 'PUT' : 'POST';
    for (const variant of [pathname, `${pathname}/`, `//${pathname}`, `${pathname}?fixture=1`, pathname.replace('/', '/%2f')]) {
      assert.equal(getCiActivationRequestService({ host, method, pathname: variant }), service, variant);
      assert.throws(() => assertCiActivationRequestAllowed({ host, method, pathname: variant }, { KIKI: '1' }), error => error.code === 'CiActivationRequiresInteraction');
    }
    assert.doesNotThrow(() => assertCiActivationRequestAllowed({ host, method, pathname }, {}));
    assert.doesNotThrow(() => assertCiActivationRequestAllowed({ host, method: 'GET', pathname }, { KIKI: '1' }));
  }
  assert.equal(getCiActivationRequestService({ host, method: 'POST', pathname: '/other/../docbucket' }), 'document');
  assert.equal(getCiActivationRequestService({ host: `${bucket}.cos.${region}.myqcloud.com`, method: 'PUT', pathname: '/' }), null);
  assert.equal(getCiActivationRequestService({ host, method: 'POST', pathname: '/jobs' }), null);
});

test('原语 cosRequest 在 fetch 之前兜底拒绝直接开通请求', async () => {
  const old = process.env.KIKI;
  process.env.KIKI = '1';
  try {
    for (const [service, pathname] of Object.entries(servicePaths)) {
      await assert.rejects(cosRequest({ method: service === 'ci' ? 'PUT' : 'POST', host: `${bucket}.ci.${region}.myqcloud.com`, pathname, creds }), error => error.code === 'CiActivationRequiresInteraction');
    }
  } finally {
    if (old === undefined) delete process.env.KIKI;
    else process.env.KIKI = old;
  }
});

// CLI integration runs with fabricated credentials and blocks every real network
// primitive. Only read-only fetch receives a synthetic CI response.
const preload = `
import http from 'node:http';
import https from 'node:https';
import net from 'node:net';
import tls from 'node:tls';
import Module, { syncBuiltinESMExports } from 'node:module';
const deny = () => { throw new Error('real network forbidden in activation fixture'); };
http.request = http.get = https.request = https.get = net.connect = net.createConnection = tls.connect = deny;
syncBuiltinESMExports();
// The SDK is an explicit stub; this tests CLI routing, not SDK cloud behavior.
const load = Module._load;
Module._load = function (name, ...args) {
  if (name === 'cos-nodejs-sdk-v5') return class { request() { deny(); } };
  return load.call(this, name, ...args);
};
globalThis.fetch = async (url, options) => {
  if (options.method !== 'GET') deny();
  const pathname = new URL(url).pathname;
  return new Response(pathname === '/' ? '{"CIStatus":"off"}' : '<Response></Response>', { status: 200 });
};
`;
function runCli(script, args) {
  const file = fileURLToPath(new URL(`../${script}`, import.meta.url));
  const result = spawnSync(process.execPath, ['--import', `data:text/javascript,${encodeURIComponent(preload)}`, file, ...args, '--bucket', bucket, '--region', region], {
    env: { KIKI: '1', TENCENTCLOUD_SECRET_ID: 'fixture-id', TENCENTCLOUD_SECRET_KEY: 'fixture-key' },
    encoding: 'utf8', timeout: 10000,
  });
  assert.equal(result.error, undefined);
  assert.ok((result.stdout || result.stderr).trim().startsWith('{'), result.stderr || result.stdout);
  return { ...result, payload: JSON.parse(result.stdout || result.stderr) };
}

test('真实 CLI 输出可直接作为前端契约输入：状态入口和七个开通入口', () => {
  const plain = runCli('ci_api.mjs', ['ci-service-status']);
  assert.equal(plain.status, 0);
  assert.equal(plain.payload.interaction, undefined);
  assert.equal(plain.payload.clientAction, undefined);
  const precheck = runCli('ci_api.mjs', ['ci-service-status', '--required-service', 'media']);
  assert.equal(precheck.status, 0);
  assert.equal(precheck.payload.tool, 'ci-service-status');
  assert.equal(precheck.payload.interaction.service, 'media');
  assertExactClientAction(precheck.payload);
  for (const [service, command] of Object.entries(CI_ACTIVATION_COMMANDS)) {
    const result = runCli('cos_node.mjs', [command, '--confirmed', 'true']);
    assert.equal(result.status, 0, result.stderr || result.stdout);
    assert.equal(result.payload.ok, true);
    assert.equal(result.payload.tool, command);
    assert.equal(result.payload.operation, 'precheck');
    assert.equal(result.payload.interaction.service, service);
    assertExactClientAction(result.payload);
    assert.equal(result.payload.bucket, bucket);
    assert.equal(result.payload.region, region);
  }
});

test('真实 ci-request CLI 的七种等价写法同样被拦截；解绑仍拒绝', () => {
  for (const [service, pathname] of Object.entries(servicePaths)) {
    const result = runCli('cos_node.mjs', ['ci-request', '--method', service === 'ci' ? 'PUT' : 'POST', '--path', `/${pathname}/?fixture=1`]);
    assert.equal(result.status, 0, result.stderr || result.stdout);
    assert.equal(result.payload.tool, CI_ACTIVATION_COMMANDS[service]);
    assert.equal(result.payload.operation, 'precheck');
    assert.equal(result.payload.interaction.service, service);
    assertExactClientAction(result.payload);
  }
  const unbind = runCli('cos_node.mjs', ['ci-request', '--method', 'PUT', '--path', '/?unbind']);
  assert.equal(unbind.status, 1);
  assert.equal(unbind.payload.code, 'ActionDenied');
  assert.equal(unbind.payload.interaction, undefined);
  assert.equal(unbind.payload.clientAction, undefined);
});

test('已开通目标服务不受其他子服务权限或未知错误影响', async () => {
  const serviceLists = {
    document: 'DocBucketList', media: 'MediaBucketList', voice: 'AsrBucketList',
    file: 'FileBucketList', asyncImage: 'PicBucketList', asyncContentRecognition: 'AiBucketList',
  };
  for (const requiredService of Object.keys(CI_ACTIVATION_COMMANDS)) {
    for (const unrelatedError of ['AccessDenied', 'InternalError']) {
      const calls = [];
      const request = async requestOptions => {
        calls.push(requestOptions);
        assert.equal(requestOptions.method, 'GET');
        if (requestOptions.pathname === '/') return raw(requestOptions, '{"CIStatus":"on"}');
        if (requestOptions.pathname === servicePaths[requiredService]) {
          const list = serviceLists[requiredService];
          return raw(requestOptions, `<Response><${list}><BucketId>${bucket}</BucketId></${list}></Response>`);
        }
        return fail(requestOptions, unrelatedError);
      };
      const result = await queryCiServiceStatus({ ...options, requiredService, request });
      assert.equal(result.activationStatus, 'already_enabled', `${requiredService}: unrelated ${unrelatedError}`);
      assert.equal(result.activationError, undefined);
      assert.equal(result.interaction, undefined);
      assert.equal(result.clientAction, undefined);
      assert.equal(calls.length, 7);
    }
  }
});

test('纯状态查询在关闭、解绑和错误状态下仍保留原输出且没有开通字段', async () => {
  const cases = [
    ['off', null, 'off'], ['unbinding', null, 'unbinding'], ['on', null, 'on'],
    [null, 'NoSuchBucket', 'off'], [null, 'UserNotBucketOwner', 'off'],
    [null, 'AccessDenied', 'noAuth'], [null, 'InternalError', 'on'],
  ];
  for (const [ciStatus, ciError, expectedStatus] of cases) {
    const request = async requestOptions => {
      assert.equal(requestOptions.method, 'GET');
      return requestOptions.pathname === '/'
        ? ciError ? fail(requestOptions, ciError) : raw(requestOptions, JSON.stringify({ CIStatus: ciStatus }))
        : fail(requestOptions, 'InternalError');
    };
    const result = await queryCiServiceStatus({ ...options, request });
    assert.deepEqual(Object.keys(result).sort(), [
      'bucket', 'region', 'ciBucketStatus', 'ciBucketAction', 'ciBucketRequest', 'dataProcessing',
      ...(ciError ? ['ciBucketError'] : []),
    ].sort());
    assert.equal(result.ciBucketStatus, expectedStatus);
    assert.equal(result.ciBucketError?.code, ciError || undefined);
    for (const field of ['activationStatus', 'activationError', 'interaction', 'clientAction']) {
      assert.equal(Object.hasOwn(result, field), false, `${expectedStatus}: unexpected ${field}`);
    }
  }
});

const confirmation = {
  type: 'ci_activation_decision', version: 1, status: 'confirmed', bucket, region, service: 'ci', toolCallId: 'fixture-call',
};
test('确认分支重新预检；权限、归属、解绑和未知错误均不会写入', async () => {
  for (const state of ['AccessDenied', 'UserNotBucketOwner', 'InternalError', 'unbinding']) {
    const calls = [];
    const result = await createCiService({ ...options, service: 'ci', env: { KIKI: '1' },
      activationConfirmation: confirmation,
      request: async req => {
        calls.push(req);
        assert.equal(req.method, 'GET');
        return state === 'unbinding' ? raw(req, '{"CIStatus":"unbinding"}') : fail(req, state);
      },
    });
    assert.equal(result.ok, false);
    assert.equal(result.activationStatus, 'blocked');
    assert.ok(calls.length);
  }
});
test('写后未就绪、复查失败或写入失败均不自动重复写入', async () => {
  for (const outcome of ['still-off', 'verify-error', 'write-error', 'write-timeout']) {
    let writes = 0;
    const result = await createCiService({ ...options, service: 'ci', env: { KIKI: '1' },
      activationConfirmation: confirmation,
      request: async req => {
        if (req.method !== 'GET') {
          writes++;
          assertCiActivationRequestAllowed(req, { KIKI: '1' });
          if (outcome === 'write-error') return fail(req, 'AccessDenied');
          if (outcome === 'write-timeout') return { ...fail(req, 'RequestTimeout'), timedOut: true };
          return raw(req, '<Response/>');
        }
        if (writes && outcome === 'verify-error') throw new Error('fixture read failed');
        return raw(req, '{"CIStatus":"off"}');
      },
    });
    assert.equal(result.ok, false);
    assert.equal(writes, 1);
    if (outcome === 'still-off' || outcome === 'verify-error') assert.equal(result.error.code, 'CiActivationNotVerified');
  }
});
test('请求层确认例外仅匹配对应桶地域服务，解绑和未确认仍拒绝', () => {
  const confirmed = { method: 'PUT', host: bucket + '.ci.' + region + '.myqcloud.com', pathname: '/',
    query: {}, activationConfirmation: confirmation };
  assert.doesNotThrow(() => assertCiActivationRequestAllowed(confirmed, { KIKI: '1' }));
  for (const change of [{ host: 'other-1250000000.ci.' + region + '.myqcloud.com' },
    { method: 'POST', pathname: '/docbucket' }, { query: { unbind: '' } }, { pathname: '/?unbind' },
    { activationConfirmation: { ...confirmation, status: 'cancelled' } }, { activationConfirmation: undefined }]) {
    assert.throws(() => assertCiActivationRequestAllowed({ ...confirmed, ...change }, { KIKI: '1' }));
  }
});
