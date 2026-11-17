import assert from 'node:assert/strict';
import test from 'node:test';

import {
  CI_SERVICE_LIFECYCLE,
  createAsyncContentRecognitionBucket,
  createAsyncImageProcessBucket,
  createCiService,
  deleteAsyncContentRecognitionBucket,
  deleteAsyncImageProcessBucket,
  deleteCiService,
  describeAsyncContentRecognitionBuckets,
  describeAsyncImageProcessBuckets,
  parseCiServiceBucketList,
  queryAsyncContentRecognitionServiceStatus,
  queryAsyncImageProcessServiceStatus,
} from './ci_service_lifecycle.mjs';

const credentials = {
  secretId: 'id',
  secretKey: 'key',
  token: '',
  source: 'runtime',
};

function rawResponse(options, overrides = {}) {
  return {
    ok: true,
    status: 200,
    requestId: 'request-id',
    elapsedMs: 1,
    body: '<Response><RequestId>request-id</RequestId></Response>',
    ...options,
    ...overrides,
  };
}

test('生命周期配置包含 CI 绑定、四个处理服务及两个异步服务', () => {
  assert.deepEqual(Object.keys(CI_SERVICE_LIFECYCLE), [
    'ci',
    'document',
    'media',
    'voice',
    'file',
    'asyncImage',
    'asyncContentRecognition',
  ]);
});

test('四个处理服务使用桶级 POST 开通和 DELETE 关闭', async () => {
  const expected = {
    document: ['/docbucket', 'CreateDocProcessBucket', 'DeleteDocProcessBucket'],
    media: ['/mediabucket', 'CreateMediaBucket', 'DeleteMediaBucket'],
    voice: ['/asrbucket', 'CreateAsrBucket', 'DeleteAsrBucket'],
    file: ['/file_bucket', 'CreateFileProcessBucket', 'DeleteFileProcessBucket'],
  };

  for (const [service, [pathname, createAction, deleteAction]] of Object.entries(expected)) {
    const calls = [];
    const request = async options => {
      calls.push(options);
      return rawResponse(options);
    };
    const created = await createCiService({
      service,
      bucket: 'example-1250000000',
      region: 'ap-guangzhou',
      creds: credentials,
      request,
    });
    const deleted = await deleteCiService({
      service,
      bucket: 'example-1250000000',
      region: 'ap-guangzhou',
      creds: credentials,
      request,
      env: {},
    });

    assert.equal(created.action, createAction);
    assert.equal(deleted.action, deleteAction);
    assert.equal(calls[0].method, 'POST');
    assert.equal(calls[1].method, 'DELETE');
    assert.equal(calls[0].pathname, pathname);
    assert.equal(calls[1].pathname, pathname);
    assert.equal(calls[0].host, 'example-1250000000.ci.ap-guangzhou.myqcloud.com');
  }
});

test('CI 使用 PUT 根路径绑定并通过 unbind 子资源解绑', async () => {
  const calls = [];
  const request = async options => {
    calls.push(options);
    return rawResponse(options);
  };

  const created = await createCiService({
    service: 'ci',
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });
  const deleted = await deleteCiService({
    service: 'ci',
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
    env: {},
  });

  assert.equal(created.action, 'CreateCIBucket');
  assert.equal(deleted.action, 'DeleteCIBucket');
  assert.equal(calls[0].method, 'PUT');
  assert.equal(calls[0].pathname, '/');
  assert.deepEqual(calls[0].query, {});
  assert.equal(calls[1].method, 'PUT');
  assert.equal(calls[1].pathname, '/');
  assert.deepEqual(calls[1].query, { unbind: '' });
});

test('严格模式拒绝所有关闭和解绑操作', () => {
  ['ci', 'document', 'media', 'voice', 'file'].forEach(service => {
    assert.throws(
      () => deleteCiService({
        service,
        bucket: 'example-1250000000',
        region: 'ap-guangzhou',
        creds: credentials,
        request: async options => rawResponse(options),
        env: { KIKI: '1' },
      }),
      error => error.code === 'ActionDenied',
    );
  });
});

test('请求失败时保留接口错误和请求摘要', async () => {
  const result = await createCiService({
    service: 'document',
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request: async options => rawResponse(options, {
      ok: false,
      status: 403,
      body: '<Error><Code>AccessDenied</Code><Message>denied</Message></Error>',
    }),
  });

  assert.equal(result.ok, false);
  assert.equal(result.error.code, 'AccessDenied');
  assert.equal(result.request.status, 403);
});

test('统一解析异步图片和异步内容识别存储桶列表', () => {
  const imageBuckets = parseCiServiceBucketList(
    '<Response><PicBucketList><BucketId>image-1250000000</BucketId></PicBucketList></Response>',
    'asyncImage',
  );
  const contentBuckets = parseCiServiceBucketList(
    '<Response><AiBucketList><BucketId>content-1250000000</BucketId></AiBucketList></Response>',
    'asyncContentRecognition',
  );

  assert.equal(imageBuckets[0].bucketId, 'image-1250000000');
  assert.equal(contentBuckets[0].bucketId, 'content-1250000000');
});

test('两个异步服务使用各自地域级查询接口', async () => {
  const calls = [];
  const request = async options => {
    calls.push(options);
    const listName = options.pathname === '/picbucket' ? 'PicBucketList' : 'AiBucketList';
    return rawResponse(options, {
      body: `<Response><${listName}><BucketId>example-1250000000</BucketId></${listName}></Response>`,
    });
  };

  const imageResult = await describeAsyncImageProcessBuckets({
    region: 'ap-guangzhou',
    bucketNames: 'example-1250000000',
    pageSize: 1,
    creds: credentials,
    request,
  });
  const contentResult = await describeAsyncContentRecognitionBuckets({
    region: 'ap-guangzhou',
    bucketNames: 'example-1250000000',
    pageSize: 1,
    creds: credentials,
    request,
  });

  assert.equal(imageResult.action, 'DescribePicProcessBucket');
  assert.equal(contentResult.action, 'DescribeAiProcessBucket');
  assert.deepEqual(calls.map(item => item.pathname), ['/picbucket', '/ai_bucket']);
  assert.equal(calls[0].host, 'ci.ap-guangzhou.myqcloud.com');
});

test('两个异步服务独立判断开通状态', async () => {
  const request = async options => {
    const listName = options.pathname === '/picbucket' ? 'PicBucketList' : 'AiBucketList';
    return rawResponse(options, {
      body: `<Response><${listName}><BucketId>example-1250000000</BucketId></${listName}></Response>`,
    });
  };

  const imageStatus = await queryAsyncImageProcessServiceStatus({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });
  const contentStatus = await queryAsyncContentRecognitionServiceStatus({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });

  assert.equal(imageStatus.status, 'enabled');
  assert.equal(contentStatus.status, 'enabled');
});

test('两个异步服务使用桶级 POST 开通和 DELETE 关闭', async () => {
  const calls = [];
  const request = async options => {
    calls.push(options);
    const resultName = options.pathname === '/picbucket' ? 'PicBucket' : 'AiBucket';
    return rawResponse(options, {
      body: `<Response><${resultName}><BucketId>example-1250000000</BucketId></${resultName}></Response>`,
    });
  };

  const imageCreated = await createAsyncImageProcessBucket({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });
  const contentCreated = await createAsyncContentRecognitionBucket({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
  });
  await deleteAsyncImageProcessBucket({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
    env: {},
  });
  await deleteAsyncContentRecognitionBucket({
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request,
    env: {},
  });

  assert.equal(imageCreated.bucketInfo.bucketId, 'example-1250000000');
  assert.equal(contentCreated.bucketInfo.bucketId, 'example-1250000000');
  assert.deepEqual(calls.map(item => [item.method, item.pathname]), [
    ['POST', '/picbucket'],
    ['POST', '/ai_bucket'],
    ['DELETE', '/picbucket'],
    ['DELETE', '/ai_bucket'],
  ]);
});

test('严格模式拒绝两个异步服务关闭操作', () => {
  const options = {
    bucket: 'example-1250000000',
    region: 'ap-guangzhou',
    creds: credentials,
    request: async requestOptions => rawResponse(requestOptions),
    env: { KIKI: '1' },
  };

  assert.throws(
    () => deleteAsyncImageProcessBucket(options),
    error => error.code === 'ActionDenied',
  );
  assert.throws(
    () => deleteAsyncContentRecognitionBucket(options),
    error => error.code === 'ActionDenied',
  );
});
