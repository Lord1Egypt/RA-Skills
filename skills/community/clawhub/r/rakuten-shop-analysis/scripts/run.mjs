import { buildCompactSkillOutput } from './format-output.mjs';

const SKILL_USAGE =
  'Usage: node clawhub/rakuten-shop-analysis/scripts/run.mjs <shopInput>';
const DEFAULT_RETRY_AFTER_SECONDS = 1;
const DEFAULT_API_BASE_URL = 'https://rakuten.845817074.xyz';

function buildHeaders() {
  return {
    'content-type': 'application/json',
  };
}

function readHeader(response, headerName) {
  if (!response?.headers) {
    return '';
  }

  if (typeof response.headers.get === 'function') {
    return response.headers.get(headerName) || '';
  }

  const normalizedHeaderName = String(headerName).toLowerCase();
  return String(
    response.headers[headerName] ||
      response.headers[normalizedHeaderName] ||
      ''
  ).trim();
}

function parseRetryAfterSeconds(value) {
  const parsed = Number.parseInt(String(value || '').trim(), 10);
  if (Number.isFinite(parsed) && parsed > 0) {
    return parsed;
  }
  return DEFAULT_RETRY_AFTER_SECONDS;
}

async function readJsonResponse(response) {
  const payload = await response.json();
  if (response.status >= 200 && response.status < 300) {
    return payload;
  }

  const errorMessage = payload?.error || `HTTP ${response.status}`;
  const error = new Error(errorMessage);
  error.statusCode = response.status;
  error.retryAfterSeconds = parseRetryAfterSeconds(
    readHeader(response, 'retry-after') ||
      payload?.retryAfterSeconds ||
      payload?.retry_after
  );
  throw error;
}

async function fetchJsonWithRateLimitRetry({
  url,
  options,
  fetchImpl,
  sleepImpl,
  maxAttempts = 3,
}) {
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    try {
      const response = await fetchImpl(url, options);
      return await readJsonResponse(response);
    } catch (error) {
      if (error?.statusCode !== 429 || attempt >= maxAttempts - 1) {
        throw error;
      }

      await sleepImpl((error.retryAfterSeconds || DEFAULT_RETRY_AFTER_SECONDS) * 1000);
    }
  }

  throw new Error(`Failed to fetch ${url}`);
}

async function createJob({
  apiBaseUrl,
  shopInput,
  headers,
  fetchImpl,
  sleepImpl,
}) {
  return fetchJsonWithRateLimitRetry({
    url: `${apiBaseUrl}/skills/rakuten-shop-analysis/jobs`,
    options: {
      method: 'POST',
      headers,
      body: JSON.stringify({
        shop_input: shopInput,
      }),
    },
    fetchImpl,
    sleepImpl,
  });
}

async function pollJob({
  apiBaseUrl,
  jobId,
  headers,
  fetchImpl,
  sleepImpl,
  maxPolls = 40,
  pollIntervalMs = 2000,
}) {
  for (let attempt = 0; attempt < maxPolls; attempt += 1) {
    const payload = await fetchJsonWithRateLimitRetry({
      url: `${apiBaseUrl}/skills/rakuten-shop-analysis/jobs/${jobId}`,
      options: {
        headers,
      },
      fetchImpl,
      sleepImpl,
    });

    if (payload.status === 'completed') {
      return payload;
    }

    if (payload.status === 'failed') {
      throw new Error(payload.error || `Job ${jobId} failed`);
    }

    if (attempt < maxPolls - 1) {
      await sleepImpl(pollIntervalMs);
    }
  }

  throw new Error(`Job ${jobId} did not complete in time`);
}

async function fetchSummary({
  apiBaseUrl,
  shopCode,
  headers,
  fetchImpl,
  sleepImpl,
}) {
  return fetchJsonWithRateLimitRetry({
    url: `${apiBaseUrl}/skills/rakuten-shop-analysis/shops/${shopCode}/summary`,
    options: {
      headers,
    },
    fetchImpl,
    sleepImpl,
  });
}

async function fetchAvailableBuckets({
  apiBaseUrl,
  shopCode,
  summary,
  headers,
  fetchImpl,
  sleepImpl,
}) {
  const availableBuckets = (summary?.buckets || []).filter(bucket => bucket?.available);
  const bucketEntries = await Promise.all(
    availableBuckets.map(async bucket => {
      const bucketPayload = await fetchJsonWithRateLimitRetry({
        url: `${apiBaseUrl}/skills/rakuten-shop-analysis/shops/${shopCode}/buckets/${bucket.bucketId}`,
        options: {
          headers,
        },
        fetchImpl,
        sleepImpl,
      });
      return [bucket.bucketId, bucketPayload];
    })
  );

  return Object.fromEntries(bucketEntries);
}

function defaultSleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function runRakutenShopAnalysisSkillCli({
  argv = process.argv.slice(2),
  stdout = process.stdout,
  stderr = process.stderr,
  fetchImpl = fetch,
  sleepImpl = defaultSleep,
} = {}) {
  const [shopInput] = argv;

  if (!shopInput) {
    stderr.write(`${SKILL_USAGE}\n`);
    return {
      exitCode: 1,
    };
  }

  const apiBaseUrl = DEFAULT_API_BASE_URL;
  const headers = buildHeaders();

  const createdJob = await createJob({
    apiBaseUrl,
    shopInput,
    headers,
    fetchImpl,
    sleepImpl,
  });
  const completedJob = await pollJob({
    apiBaseUrl,
    jobId: createdJob.jobId,
    headers,
    fetchImpl,
    sleepImpl,
  });
  const summary = await fetchSummary({
    apiBaseUrl,
    shopCode: completedJob.shopCode,
    headers,
    fetchImpl,
    sleepImpl,
  });
  const buckets = await fetchAvailableBuckets({
    apiBaseUrl,
    shopCode: completedJob.shopCode,
    summary,
    headers,
    fetchImpl,
    sleepImpl,
  });
  const output = buildCompactSkillOutput({
    shopInput,
    summary,
    buckets,
  });

  stdout.write(`${JSON.stringify(output, null, 2)}\n`);

  return {
    exitCode: 0,
    output,
  };
}

const isDirectRun =
  process.argv[1] &&
  new URL(`file://${process.argv[1].replace(/\\/g, '/')}`).href === import.meta.url;

if (isDirectRun) {
  runRakutenShopAnalysisSkillCli()
    .then(({ exitCode }) => {
      process.exitCode = exitCode;
    })
    .catch(error => {
      console.error(error);
      process.exitCode = 1;
    });
}
