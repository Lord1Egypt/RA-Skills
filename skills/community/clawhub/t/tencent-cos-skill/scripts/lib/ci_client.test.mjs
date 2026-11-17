import assert from 'node:assert/strict';
import test from 'node:test';

import {
  assertActionAllowed,
  cosRequest,
  createCosAuthorization,
  decryptEnvBuffer,
  encryptEnvBuffer,
  getHiddenActions,
  getRuntimeCredentials,
  getRuntimeMode,
  validateCosHost,
} from './ci_client.mjs';

test('仅 KIKI=1 时识别为严格模式', () => {
  assert.equal(getRuntimeMode({ KIKI: '1' }), 'strict');
  assert.equal(getRuntimeMode({ KIKI: ' 1 ' }), 'strict');
  assert.equal(getRuntimeMode({ KIKI: '0' }), 'public');
  assert.equal(getRuntimeMode({ KIKI: 'true' }), 'public');
  assert.equal(getRuntimeMode({ TENCENTCLOUD_UIN: '10001' }), 'public');
  assert.equal(getRuntimeMode({}), 'public');
});

test('未提供运行时凭证时读取 TENCENT_COS 凭证', () => {
  const credentials = getRuntimeCredentials({
    TENCENT_COS_SECRET_ID: 'public-id',
    TENCENT_COS_SECRET_KEY: 'public-key',
    TENCENT_COS_TOKEN: 'public-token',
  });

  assert.deepEqual(credentials, {
    secretId: 'public-id',
    secretKey: 'public-key',
    token: 'public-token',
    uin: '',
    ownerUin: '',
    source: 'env',
  });
});

test('存在运行时凭证时优先读取 TENCENTCLOUD 凭证', () => {
  const credentials = getRuntimeCredentials({
    TENCENTCLOUD_UIN: '10001',
    TENCENTCLOUD_OWNER_UIN: '10000',
    TENCENTCLOUD_SECRET_ID: 'runtime-id',
    TENCENTCLOUD_SECRET_KEY: 'runtime-key',
    TENCENTCLOUD_TOKEN: 'runtime-token',
    TENCENT_COS_SECRET_ID: 'public-id',
    TENCENT_COS_SECRET_KEY: 'public-key',
  });

  assert.deepEqual(credentials, {
    secretId: 'runtime-id',
    secretKey: 'runtime-key',
    token: 'runtime-token',
    uin: '10001',
    ownerUin: '10000',
    source: 'runtime',
  });
});

test('KIKI=1 不改变凭证来源', () => {
  const credentials = getRuntimeCredentials({
    KIKI: '1',
    TENCENT_COS_SECRET_ID: 'public-id',
    TENCENT_COS_SECRET_KEY: 'public-key',
  });

  assert.equal(credentials.secretId, 'public-id');
  assert.equal(credentials.secretKey, 'public-key');
  assert.equal(credentials.source, 'env');
});

test('严格模式隐藏凭证管理和删除 action', () => {
  const publicEnv = {};
  const strictEnv = { KIKI: '1' };
  const expectedHiddenActions = [
    'delete',
    'delete-multiple',
    'delete-file-meta-index',
    'delete-ai-process-bucket',
    'delete-async-image-process-bucket',
    'delete-ci-bucket',
    'delete-doc-process-bucket',
    'delete-media-bucket',
    'delete-asr-bucket',
    'delete-file-process-bucket',
    'encrypt-env',
    'decrypt-env',
  ];

  assert.deepEqual(getHiddenActions(publicEnv), []);
  assert.deepEqual(getHiddenActions(strictEnv), expectedHiddenActions);
  assert.ok(getHiddenActions(strictEnv, ['upload', 'delete-future-resource']).includes('delete-future-resource'));
  assert.doesNotThrow(() => assertActionAllowed('delete', publicEnv));
  assert.doesNotThrow(() => assertActionAllowed('upload', strictEnv));
  expectedHiddenActions.forEach(action => {
    assert.throws(
      () => assertActionAllowed(action, strictEnv),
      error => error.code === 'ActionDenied',
    );
  });
  assert.throws(
    () => assertActionAllowed('delete-future-resource', strictEnv),
    error => error.code === 'ActionDenied',
  );
});

test('COS 签名参数列表将驼峰查询参数名转为小写', () => {
  const authorization = createCosAuthorization({
    secretId: 'id',
    secretKey: 'key',
    method: 'GET',
    pathname: '/ai_bucket',
    query: {
      bucketNames: 'example-1250000000',
      pageNumber: '1',
      pageSize: '1',
    },
    headers: { host: 'ci.ap-guangzhou.myqcloud.com' },
  });

  assert.match(authorization, /q-url-param-list=bucketnames;pagenumber;pagesize/);
});

test('仅允许腾讯云 COS 和 CI 服务域名', () => {
  assert.doesNotThrow(() => validateCosHost('service.cos.myqcloud.com'));
  assert.doesNotThrow(() => validateCosHost('example-1250000000.ci.ap-guangzhou.myqcloud.com'));
  assert.doesNotThrow(() => validateCosHost('ci.ap-guangzhou.myqcloud.com'));
  assert.throws(
    () => validateCosHost('127.0.0.1'),
    error => error.code === 'InvalidArgs',
  );
  assert.throws(
    () => validateCosHost('metadata.internal'),
    error => error.code === 'InvalidArgs',
  );
});

test('凭证加解密共享实现可完整往返', () => {
  const plaintext = 'TENCENT_COS_SECRET_ID=test-id\nTENCENT_COS_SECRET_KEY=test-key\n';
  const encrypted = encryptEnvBuffer(plaintext);

  assert.notEqual(encrypted.toString('utf-8'), plaintext);
  assert.equal(decryptEnvBuffer(encrypted), plaintext);
});

test('严格模式拒绝通用 DELETE 请求', () => {
  const publicEnv = {};
  const strictEnv = { KIKI: '1' };

  assert.doesNotThrow(() => assertActionAllowed('ci-request', publicEnv, { method: 'DELETE' }));
  assert.doesNotThrow(() => assertActionAllowed('ci-request', strictEnv, { method: 'POST' }));
  assert.throws(
    () => assertActionAllowed('ci-request', strictEnv, { method: 'delete' }),
    error => error.code === 'ActionDenied',
  );
});

test('严格模式下 cosRequest 请求原语在请求层拒绝 DELETE（兜底，含删除数据集路径）', async () => {
  const previous = process.env.KIKI;
  process.env.KIKI = '1';
  try {
    // 拦截发生在 fetch 之前，不会发出真实网络请求
    await assert.rejects(
      () => cosRequest({
        method: 'DELETE',
        host: '1250000000.ci.ap-guangzhou.myqcloud.com',
        pathname: '/datasets/example-dataset',
        creds: { secretId: 'id', secretKey: 'key', token: '', source: 'runtime' },
      }),
      error => error.code === 'ActionDenied',
    );
  } finally {
    if (previous === undefined) {
      delete process.env.KIKI;
    } else {
      process.env.KIKI = previous;
    }
  }
});
