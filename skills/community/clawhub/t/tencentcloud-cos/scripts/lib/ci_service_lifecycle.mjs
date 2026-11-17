import {
  assertActionAllowed,
  ciHost,
  cosRequest,
  extractXmlTag,
  getRuntimeCredentials,
  isStrictMode,
  parseCiRawError,
  summarizeCiRequest,
  validateCosBucket,
  validateCosRegion,
} from './ci_client.mjs';
import {
  describeCiServiceBuckets,
  getService,
  parseBucketNode,
  queryCiServiceBucketStatus,
} from './ci_service_query.mjs';
import { CI_ACTIVATION_COMMANDS, validateCiActivationConfirmation } from './ci_activation.mjs';
import { queryCiServiceStatus } from './ci_service_status.mjs';

export {
  CI_SERVICE_LIFECYCLE,
  describeCiServiceBuckets,
  parseCiServiceBucketList,
  queryCiServiceBucketStatus,
} from './ci_service_query.mjs';

async function mutateCiService({
  operation,
  service,
  bucket,
  region,
  creds,
  request,
  activationConfirmation,
}) {
  validateCosBucket(bucket);
  validateCosRegion(region);
  const config = getService(service);
  const deleting = operation === 'delete';
  const action = deleting ? config.deleteAction : config.createAction;
  const method = deleting ? config.deleteMethod || 'DELETE' : config.createMethod || 'POST';
  const query = deleting ? config.deleteQuery || {} : {};
  const raw = await request({
    method,
    host: ciHost(bucket, region),
    pathname: config.pathname,
    query,
    creds,
    body: '',
    ...(activationConfirmation ? { activationConfirmation } : {}),
    extraHeaders: {
      Accept: 'application/xml',
      'Content-Type': 'application/xml',
    },
  });
  const base = {
    action,
    service,
    bucket,
    region,
    operation,
    request: summarizeCiRequest(raw),
  };
  if (!raw.ok) {
    return { ok: false, ...base, error: parseCiRawError(raw) };
  }
  const bucketXml = config.resultName ? extractXmlTag(raw.body, config.resultName) : null;
  return {
    ok: true,
    ...base,
    ...(bucketXml ? { bucketInfo: parseBucketNode(bucketXml) } : {}),
  };
}

export function createCiService({
  service,
  bucket,
  region,
  creds = getRuntimeCredentials(),
  request = cosRequest,
  env = process.env,
  activationConfirmation,
}) {
  // Keep the default KiKi precheck and all public-mode behavior unchanged.
  if (isStrictMode(env) && activationConfirmation !== undefined) {
    const decision = validateCiActivationConfirmation(activationConfirmation, { bucket, region, service });
    return createConfirmedCiService({ service, bucket, region, creds, request, activationConfirmation: decision });
  }
  if (isStrictMode(env)) {
    const config = getService(service);
    return queryCiServiceStatus({ bucket, region, creds, request, requiredService: service }).then(status => ({
      ok: status.activationStatus !== 'blocked',
      tool: CI_ACTIVATION_COMMANDS[service],
      action: config.createAction,
      service,
      operation: 'precheck',
      ...status,
      ...(status.activationError ? { error: status.activationError } : {}),
    }));
  }
  return mutateCiService({
    operation: 'create',
    service,
    bucket,
    region,
    creds,
    request,
  });
}

async function createConfirmedCiService(options) {
  const { service, bucket, region, creds, request } = options;
  const check = () => queryCiServiceStatus({ bucket, region, creds, request, requiredService: service });
  const before = await check();
  if (before.activationStatus === 'blocked') {
    return { ok: false, operation: 'precheck', ...before, error: before.activationError };
  }
  if (before.activationStatus === 'already_enabled') {
    return { ok: true, operation: 'precheck', ...before };
  }
  const created = await mutateCiService({ ...options, operation: 'create' });
  if (!created.ok) return created;
  // A successful write response alone is not proof that the service is ready.
  // Never repeat a write here, including when the verification request fails.
  try {
    const after = await check();
    if (after.activationStatus === 'already_enabled') return { ...created, activationStatus: 'enabled' };
  } catch {}
  return {
    ...created, ok: false, activationStatus: 'unverified',
    error: { code: 'CiActivationNotVerified', message: '开通请求已提交，服务状态尚未确认；请先查询状态，不要重复开通。' },
  };
}

export function deleteCiService({
  service,
  bucket,
  region,
  creds = getRuntimeCredentials(),
  request = cosRequest,
  env = process.env,
}) {
  const config = getService(service);
  const method = config.deleteMethod || 'DELETE';
  assertActionAllowed(config.deleteCommand || `delete-${service}-service`, env, { method });
  return mutateCiService({
    operation: 'delete',
    service,
    bucket,
    region,
    creds,
    request,
  });
}

export const describeAsyncImageProcessBuckets = options => describeCiServiceBuckets({
  ...options,
  service: 'asyncImage',
});

export const queryAsyncImageProcessServiceStatus = options => queryCiServiceBucketStatus({
  ...options,
  service: 'asyncImage',
});

export const createAsyncImageProcessBucket = options => createCiService({
  ...options,
  service: 'asyncImage',
});

export const deleteAsyncImageProcessBucket = options => deleteCiService({
  ...options,
  service: 'asyncImage',
});

export const describeAsyncContentRecognitionBuckets = options => describeCiServiceBuckets({
  ...options,
  service: 'asyncContentRecognition',
});

export const queryAsyncContentRecognitionServiceStatus = options => queryCiServiceBucketStatus({
  ...options,
  service: 'asyncContentRecognition',
});

export const createAsyncContentRecognitionBucket = options => createCiService({
  ...options,
  service: 'asyncContentRecognition',
});

export const deleteAsyncContentRecognitionBucket = options => deleteCiService({
  ...options,
  service: 'asyncContentRecognition',
});
