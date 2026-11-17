import {
  cosRequest,
  extractXmlTag,
  getRuntimeCredentials,
  parseCiRawError,
  summarizeCiRequest,
  validateCosBucket,
  validateCosRegion,
} from './ci_client.mjs';

export const CI_SERVICE_LIFECYCLE = Object.freeze({
  ci: {
    createAction: 'CreateCIBucket',
    deleteAction: 'DeleteCIBucket',
    pathname: '/',
    createMethod: 'PUT',
    deleteMethod: 'PUT',
    deleteQuery: { unbind: '' },
  },
  document: {
    describeAction: 'DescribeDocProcessBucket',
    createAction: 'CreateDocProcessBucket',
    deleteAction: 'DeleteDocProcessBucket',
    pathname: '/docbucket',
    listName: 'DocBucketList',
    responseLabel: 'document processing',
  },
  media: {
    describeAction: 'DescribeMediaBuckets',
    createAction: 'CreateMediaBucket',
    deleteAction: 'DeleteMediaBucket',
    pathname: '/mediabucket',
    listName: 'MediaBucketList',
    responseLabel: 'media processing',
  },
  voice: {
    describeAction: 'DescribeAsrBuckets',
    createAction: 'CreateAsrBucket',
    deleteAction: 'DeleteAsrBucket',
    pathname: '/asrbucket',
    listName: 'AsrBucketList',
    responseLabel: 'voice processing',
  },
  file: {
    describeAction: 'DescribeFileProcessBucket',
    createAction: 'CreateFileProcessBucket',
    deleteAction: 'DeleteFileProcessBucket',
    pathname: '/file_bucket',
    listName: 'FileBucketList',
    responseLabel: 'file processing',
  },
  asyncImage: {
    describeAction: 'DescribePicProcessBucket',
    createAction: 'CreatePicProcessBucket',
    deleteAction: 'DeletePicProcessBucket',
    pathname: '/picbucket',
    listName: 'PicBucketList',
    resultName: 'PicBucket',
    responseLabel: 'async image processing',
    deleteCommand: 'delete-async-image-process-bucket',
  },
  asyncContentRecognition: {
    describeAction: 'DescribeAiProcessBucket',
    createAction: 'CreateAiProcessBucket',
    deleteAction: 'DeleteAiProcessBucket',
    pathname: '/ai_bucket',
    listName: 'AiBucketList',
    resultName: 'AiBucket',
    responseLabel: 'async AI content recognition',
    deleteCommand: 'delete-ai-process-bucket',
  },
});

function parseInteger(value, fallback, max) {
  if (typeof value === 'boolean') {
    const error = new Error(`invalid pagination value: ${String(value)}`);
    error.code = 'InvalidArgs';
    throw error;
  }
  const parsed = Number(value ?? fallback);
  if (!Number.isInteger(parsed) || parsed < 1 || parsed > max) {
    const error = new Error(`invalid pagination value: ${String(value)}`);
    error.code = 'InvalidArgs';
    throw error;
  }
  return parsed;
}

function validateBucketFilters(bucketNames, bucketName) {
  if (bucketNames) {
    if (typeof bucketNames === 'boolean') {
      const error = new Error('invalid bucket names');
      error.code = 'InvalidArgs';
      throw error;
    }
    String(bucketNames).split(',').forEach(validateCosBucket);
  }
  if (
    bucketName
    && (
      typeof bucketName === 'boolean'
      || !/^[a-z0-9][a-z0-9.-]*$/i.test(String(bucketName))
    )
  ) {
    const error = new Error('invalid bucket name prefix');
    error.code = 'InvalidArgs';
    throw error;
  }
}

export function getService(service) {
  const config = CI_SERVICE_LIFECYCLE[service];
  if (!config) {
    const error = new Error(`unsupported CI service: ${String(service)}`);
    error.code = 'InvalidArgs';
    throw error;
  }
  return config;
}

export function parseBucketNode(xml) {
  return {
    bucketId: extractXmlTag(xml, 'BucketId'),
    name: extractXmlTag(xml, 'Name'),
    region: extractXmlTag(xml, 'Region'),
    createTime: extractXmlTag(xml, 'CreateTime'),
  };
}

export function parseCiServiceBucketList(xml, service) {
  const config = getService(service);
  if (!config.listName) {
    const error = new Error(`CI service does not support bucket listing: ${service}`);
    error.code = 'InvalidArgs';
    throw error;
  }
  const pattern = new RegExp(`<${config.listName}>([\\s\\S]*?)</${config.listName}>`, 'gi');
  return [...String(xml || '').matchAll(pattern)]
    .map(match => parseBucketNode(match[1]))
    .filter(item => item.bucketId);
}

export async function describeCiServiceBuckets({
  service,
  region,
  bucketNames,
  bucketName,
  pageNumber = 1,
  pageSize = 10,
  creds = getRuntimeCredentials(),
  request = cosRequest,
}) {
  const config = getService(service);
  if (!config.describeAction || !config.listName) {
    const error = new Error(`CI service does not support bucket listing: ${service}`);
    error.code = 'InvalidArgs';
    throw error;
  }
  validateCosRegion(region);
  validateBucketFilters(bucketNames, bucketName);
  const normalizedPageNumber = parseInteger(pageNumber, 1, Number.MAX_SAFE_INTEGER);
  const normalizedPageSize = parseInteger(pageSize, 10, 100);
  const query = {
    pageNumber: String(normalizedPageNumber),
    pageSize: String(normalizedPageSize),
    ...(bucketNames ? { bucketNames: String(bucketNames) } : {}),
    ...(bucketName ? { bucketName: String(bucketName) } : {}),
  };
  const raw = await request({
    method: 'GET',
    host: `ci.${region}.myqcloud.com`,
    pathname: config.pathname,
    query,
    creds,
    extraHeaders: { Accept: 'application/xml' },
  });
  const base = {
    action: config.describeAction,
    service,
    region,
    request: summarizeCiRequest(raw),
  };
  if (!raw.ok) {
    return { ok: false, ...base, error: parseCiRawError(raw) };
  }
  if (!/<Response(?:\s|>)/i.test(String(raw.body || ''))) {
    return {
      ok: false,
      ...base,
      error: {
        code: 'ResponseValidationError',
        message: `${config.responseLabel} response is not valid XML`,
        requestId: raw.requestId || null,
      },
    };
  }
  return {
    ok: true,
    ...base,
    totalCount: Number(extractXmlTag(raw.body, 'TotalCount') || 0),
    pageNumber: Number(extractXmlTag(raw.body, 'PageNumber') || normalizedPageNumber),
    pageSize: Number(extractXmlTag(raw.body, 'PageSize') || normalizedPageSize),
    buckets: parseCiServiceBucketList(raw.body, service),
  };
}

export async function queryCiServiceBucketStatus(options) {
  const { bucket } = options;
  validateCosBucket(bucket);
  const result = await describeCiServiceBuckets({
    ...options,
    bucketNames: bucket,
    pageNumber: 1,
    pageSize: 1,
  });
  if (!result.ok) {
    return {
      status: result.error.code === 'AccessDenied' ? 'noAuth' : 'error',
      action: result.action,
      error: result.error,
      request: result.request,
    };
  }
  return {
    status: result.buckets.some(item => item.bucketId === bucket) ? 'enabled' : 'disabled',
    action: result.action,
    request: result.request,
  };
}
