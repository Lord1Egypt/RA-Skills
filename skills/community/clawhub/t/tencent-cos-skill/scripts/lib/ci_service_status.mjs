import {
  ciHost,
  cosRequest,
  getRuntimeCredentials,
  parseCiRawError,
  summarizeCiRequest,
  validateCosBucket,
  validateCosRegion,
} from './ci_client.mjs';
import { queryCiServiceBucketStatus } from './ci_service_query.mjs';
import { evaluateCiActivation, validateRequiredCiService } from './ci_activation.mjs';

const CI_BUCKET_ACTION = 'DescribeCIBuckets';

const PROCESSING_SERVICE_KEYS = Object.freeze({
  documentProcessing: 'document',
  mediaProcessing: 'media',
  voiceProcessing: 'voice',
  fileProcessing: 'file',
});

const CI_BUCKET_STATES = new Set(['on', 'off', 'unbinding']);

function parseJsonBody(body) {
  try {
    return JSON.parse(String(body || ''));
  } catch {
    return null;
  }
}

export function parseCiBucketStatus(raw) {
  if (!raw.ok) {
    const error = parseCiRawError(raw);
    if (error.code === 'AccessDenied') {
      return { status: 'noAuth', error };
    }
    if (['NoSuchBucket', 'UserNotBucketOwner'].includes(error.code)) {
      return { status: 'off', error };
    }
    return { status: 'on', error };
  }

  const data = parseJsonBody(raw.body);
  const status = data?.CIStatus;
  if (!CI_BUCKET_STATES.has(status)) {
    const error = new Error(`unexpected CIStatus: ${String(status)}`);
    error.code = 'ResponseValidationError';
    throw error;
  }
  return { status, error: null };
}

function createUniformStatus(status) {
  return Object.fromEntries(
    Object.keys(PROCESSING_SERVICE_KEYS).map(name => [name, { status }]),
  );
}

async function queryProcessingServices({ bucket, region, creds, request }) {
  const entries = await Promise.all(
    Object.entries(PROCESSING_SERVICE_KEYS).map(async ([name, service]) => [
      name,
      await queryCiServiceBucketStatus({
        service,
        bucket,
        region,
        creds,
        request,
      }),
    ]),
  );
  return Object.fromEntries(entries);
}

async function queryCiServiceStatusSnapshot({
  bucket,
  region,
  creds = getRuntimeCredentials(),
  request = cosRequest,
}) {
  validateCosBucket(bucket);
  validateCosRegion(region);

  const ciRaw = await request({
    method: 'GET',
    host: ciHost(bucket, region),
    pathname: '/',
    query: {},
    creds,
    extraHeaders: { Accept: 'application/json' },
  });
  const ciResult = parseCiBucketStatus(ciRaw);
  const base = {
    bucket,
    region,
    ciBucketStatus: ciResult.status,
    ciBucketAction: CI_BUCKET_ACTION,
    ciBucketRequest: summarizeCiRequest(ciRaw),
    ...(ciResult.error ? { ciBucketError: ciResult.error } : {}),
  };

  if (['off', 'unbinding'].includes(ciResult.status)) {
    return {
      ...base,
      dataProcessing: {
        imageProcessing: false,
        asyncImageProcessing: { status: 'disabled' },
        ...createUniformStatus('disabled'),
        contentRecognition: false,
        asyncContentRecognition: { status: 'disabled' },
      },
    };
  }

  const processingPromise = ciResult.status === 'noAuth'
    ? Promise.resolve(createUniformStatus('noAuth'))
    : queryProcessingServices({ bucket, region, creds, request });
  const [processingServices, asyncImageProcessing, asyncContentRecognition] = await Promise.all([
    processingPromise,
    queryCiServiceBucketStatus({ service: 'asyncImage', bucket, region, creds, request }),
    queryCiServiceBucketStatus({ service: 'asyncContentRecognition', bucket, region, creds, request }),
  ]);
  const defaultSynchronousCapability = ciResult.status === 'on' ? true : null;

  return {
    ...base,
    dataProcessing: {
      imageProcessing: defaultSynchronousCapability,
      asyncImageProcessing,
      ...processingServices,
      contentRecognition: defaultSynchronousCapability,
      asyncContentRecognition,
    },
  };
}

/** Plain status lookups stay read-only and never request user interaction. */
export async function queryCiServiceStatus({ requiredService, ...options }) {
  if (requiredService !== undefined) validateRequiredCiService(requiredService);
  const status = await queryCiServiceStatusSnapshot(options);
  return requiredService === undefined
    ? status
    : { ...status, ...evaluateCiActivation(status, requiredService) };
}
