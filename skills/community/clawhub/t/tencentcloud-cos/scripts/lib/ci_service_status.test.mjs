import assert from 'node:assert/strict';
import test from 'node:test';

import {
  parseCiBucketStatus,
  queryCiServiceStatus,
} from './ci_service_status.mjs';

function rawResponse(overrides = {}) {
  return {
    ok: true,
    status: 200,
    method: 'GET',
    host: 'example-1250000000.ci.ap-guangzhou.myqcloud.com',
    pathname: '/',
    query: {},
    requestId: 'request-id',
    elapsedMs: 1,
    body: '',
    ...overrides,
  };
}

const credentials = {
  secretId: 'id',
  secretKey: 'key',
  token: '',
  source: 'runtime',
};

test('解析 CI 总开关状态和错误映射', () => {
  assert.equal(parseCiBucketStatus(rawResponse({ body: '{"CIStatus":"on"}' })).status, 'on');
  assert.equal(parseCiBucketStatus(rawResponse({ body: '{"CIStatus":"off"}' })).status, 'off');
  assert.equal(parseCiBucketStatus(rawResponse({ body: '{"CIStatus":"unbinding"}' })).status, 'unbinding');
  assert.equal(parseCiBucketStatus(rawResponse({
    ok: false,
    status: 403,
    body: '<Error><Code>AccessDenied</Code></Error>',
  })).status, 'noAuth');
  assert.equal(parseCiBucketStatus(rawResponse({
    ok: false,
    status: 404,
    body: '<Error><Code>NoSuchBucket</Code></Error>',
  })).status, 'off');
});

test('CI 未绑定时不继续查询子服务', async () => {
  let requestCount = 0;
  const request = async () => {
    requestCount += 1;
    return rawResponse({ body: '{"CIStatus":"off"}' });
  };

  const result = await queryCiServiceStatus({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });

  assert.equal(requestCount, 1);
  assert.equal(result.ciBucketStatus, 'off');
  assert.equal(result.dataProcessing.imageProcessing, false);
  assert.equal(result.dataProcessing.asyncImageProcessing.status, 'disabled');
  assert.equal(result.dataProcessing.contentRecognition, false);
  assert.equal(result.dataProcessing.asyncContentRecognition.status, 'disabled');
  assert.equal('contentAudit' in result, false);
  assert.equal('complete' in result, false);
});

test('CI 总开关无权限时跳过四项数据处理但独立查询两项异步服务', async () => {
  let requestCount = 0;
  const request = async () => {
    requestCount += 1;
    return rawResponse({
      ok: false,
      status: 403,
      body: '<Error><Code>AccessDenied</Code></Error>',
    });
  };

  const result = await queryCiServiceStatus({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });

  assert.equal(requestCount, 3);
  assert.equal(result.ciBucketStatus, 'noAuth');
  assert.equal(result.dataProcessing.documentProcessing.status, 'noAuth');
  assert.equal(result.dataProcessing.mediaProcessing.status, 'noAuth');
  assert.equal(result.dataProcessing.voiceProcessing.status, 'noAuth');
  assert.equal(result.dataProcessing.fileProcessing.status, 'noAuth');
  assert.equal(result.dataProcessing.asyncImageProcessing.status, 'noAuth');
  assert.equal(result.dataProcessing.imageProcessing, null);
  assert.equal(result.dataProcessing.contentRecognition, null);
  assert.equal(result.dataProcessing.asyncContentRecognition.status, 'noAuth');
});

test('CI 已绑定时并行查询四项数据处理和两项异步服务', async () => {
  const paths = [];
  const request = async options => {
    paths.push(options.pathname);
    if (options.pathname === '/') {
      return rawResponse({ ...options, body: '{"CIStatus":"on"}' });
    }
    if (options.pathname === '/ai_bucket') {
      return rawResponse({
        ...options,
        body: '<Response><AiBucketList><BucketId>example-1250000000</BucketId></AiBucketList></Response>',
      });
    }
    if (options.pathname === '/picbucket') {
      return rawResponse({
        ...options,
        body: '<Response><PicBucketList><BucketId>example-1250000000</BucketId></PicBucketList></Response>',
      });
    }
    const listNames = {
      '/docbucket': 'DocBucketList',
      '/mediabucket': 'MediaBucketList',
      '/asrbucket': 'AsrBucketList',
      '/file_bucket': 'FileBucketList',
    };
    return rawResponse({
      ...options,
      body: `<Response><${listNames[options.pathname]}><BucketId>example-1250000000</BucketId></${listNames[options.pathname]}></Response>`,
    });
  };

  const result = await queryCiServiceStatus({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });

  assert.deepEqual(paths.sort(), [
    '/',
    '/ai_bucket',
    '/asrbucket',
    '/docbucket',
    '/file_bucket',
    '/mediabucket',
    '/picbucket',
  ]);
  assert.equal(result.dataProcessing.imageProcessing, true);
  assert.equal(result.dataProcessing.asyncImageProcessing.status, 'enabled');
  assert.equal(result.dataProcessing.documentProcessing.status, 'enabled');
  assert.equal(result.dataProcessing.mediaProcessing.status, 'enabled');
  assert.equal(result.dataProcessing.voiceProcessing.status, 'enabled');
  assert.equal(result.dataProcessing.fileProcessing.status, 'enabled');
  assert.equal(result.dataProcessing.contentRecognition, true);
  assert.equal(result.dataProcessing.asyncContentRecognition.status, 'enabled');
});

test('非法 bucket 和 region 在发请求前被拒绝', async () => {
  await assert.rejects(
    queryCiServiceStatus({
      bucket: 'example.com/evil-1250000000',
      region: 'ap-guangzhou',
      creds: credentials,
      request: async () => rawResponse(),
    }),
    error => error.code === 'InvalidArgs',
  );
});
