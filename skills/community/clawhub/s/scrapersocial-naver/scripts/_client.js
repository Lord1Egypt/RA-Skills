'use strict';

/**
 * Shared HTTP client for every ScraperSocial skill script.
 *
 * Copied verbatim into each skill by tools/generate.mjs.
 * Edit tools/templates/_client.js — never the copies under skills/.
 *
 * Zero dependencies. Node 20+ (uses built-in fetch).
 */

/**
 * The API key is only ever sent to this host. It is a constant on purpose:
 * nothing in the environment, the arguments or the configuration can redirect
 * a request elsewhere. The test suite talks to a local mock by patching
 * global fetch in a preload module; the shipped code has no override.
 */
const API_BASE = 'https://api.scrapersocial.com';
const ENV_VAR = 'SCRAPERSOCIAL_KEY';
const VERSION = '1.0.4';
const USER_AGENT =
  `social-media-api-skills/${VERSION} (+https://github.com/nikhonit/social-media-api-skills)`;

/**
 * Requests with limit > 50 do not return data. The API answers 202 with a job
 * id that has to be polled. These scripts are synchronous by design, so the
 * limit is clamped instead. Use the cursor to page beyond 50 items.
 */
const MAX_SYNC_LIMIT = 50;

const RETRY_STATUSES = new Set([429, 500, 502, 503, 504]);
const MAX_ATTEMPTS = 4;

/**
 * Without this a stalled connection hangs forever, which is much worse when an
 * agent is running these as subprocesses. Transcript and summary endpoints do
 * real work, so the value is generous. It is a constant: the scripts read no
 * environment variable other than the API key.
 */
const REQUEST_TIMEOUT_MS = 60_000;

/** Print a machine-readable error and exit non-zero. */
function fail(error, detail, requestId) {
  const payload = { error };
  if (detail) payload.detail = detail;
  // request_id is how support traces a call — always surface it when present.
  payload.request_id = requestId || null;
  process.stderr.write(JSON.stringify(payload, null, 2) + '\n');
  process.exit(1);
}

function readKey() {
  const key = process.env[ENV_VAR];
  if (!key) {
    fail(
      `Missing ${ENV_VAR}`,
      'Create a key at https://scrapersocial.com/app/keys, then run: ' +
        `export ${ENV_VAR}=sk_live_...  ` +
        'Signup at https://scrapersocial.com/signup includes 100 free credits, no card required.'
    );
  }
  return key;
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/**
 * Call a ScraperSocial endpoint and return the parsed JSON envelope.
 * Retries 429 and 5xx with exponential backoff; never retries other 4xx.
 */
async function callEndpoint(path, params = {}) {
  const key = readKey();
  const url = new URL(path, API_BASE);

  for (const [name, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === '') continue;
    if (name === 'limit') {
      const limit = Number(value);
      if (!Number.isFinite(limit) || limit < 1) {
        fail('invalid_limit', `--limit must be a positive integer, got: ${value}`);
      }
      if (limit > MAX_SYNC_LIMIT) {
        process.stderr.write(
          `note: limit ${limit} would create an async job; clamped to ${MAX_SYNC_LIMIT}. ` +
            'Page further with --cursor.\n'
        );
        url.searchParams.set('limit', String(MAX_SYNC_LIMIT));
        continue;
      }
    }
    url.searchParams.set(name, String(value));
  }

  let lastStatus = null;
  let lastBody = null;

  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt += 1) {
    let response;
    try {
      response = await fetch(url, {
        headers: {
          authorization: `Bearer ${key}`,
          accept: 'application/json',
          'user-agent': USER_AGENT,
        },
        signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
      });
    } catch (cause) {
      // Network failure or timeout: retry, then give up with the real reason.
      const timedOut = cause && (cause.name === 'TimeoutError' || cause.name === 'AbortError');
      if (attempt === MAX_ATTEMPTS) {
        fail(
          timedOut ? 'timeout' : 'network_error',
          timedOut
            ? `No response after ${REQUEST_TIMEOUT_MS}ms. Retry; transcript and summary endpoints can be slow on long media.`
            : String(cause && cause.message ? cause.message : cause)
        );
      }
      await sleep(2 ** attempt * 250);
      continue;
    }

    const text = await response.text();
    let body = null;
    try {
      body = text ? JSON.parse(text) : null;
    } catch {
      body = { raw: text };
    }

    if (response.ok) return body;

    lastStatus = response.status;
    lastBody = body;

    if (RETRY_STATUSES.has(response.status) && attempt < MAX_ATTEMPTS) {
      const retryAfter = Number(response.headers.get('retry-after'));
      const backoff = Number.isFinite(retryAfter) && retryAfter > 0
        ? retryAfter * 1000
        : 2 ** attempt * 250;
      await sleep(backoff);
      continue;
    }
    break;
  }

  const err = (lastBody && lastBody.error) || {};
  fail(
    err.code || `http_${lastStatus}`,
    err.hint ? `${err.message || ''} ${err.hint}`.trim() : err.message || `HTTP ${lastStatus}`,
    err.request_id
  );
}

/** Minimal `--flag value` / `--flag=value` parser. Returns { _, flags }. */
function parseFlags(argv) {
  const positional = [];
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      positional.push(arg);
      continue;
    }
    const eq = arg.indexOf('=');
    if (eq !== -1) {
      flags[arg.slice(2, eq)] = arg.slice(eq + 1);
    } else if (argv[i + 1] !== undefined && !argv[i + 1].startsWith('--')) {
      flags[arg.slice(2)] = argv[i + 1];
      i += 1;
    } else {
      flags[arg.slice(2)] = true;
    }
  }
  return { _: positional, flags };
}

/**
 * Boolean flags must honour an explicit value: `--fresh false` means false.
 * Treating any present flag as true silently inverts the user's intent.
 */
function boolFlag(value) {
  if (value === undefined || value === null) return false;
  if (value === true) return true;
  const normalised = String(value).trim().toLowerCase();
  return !(normalised === 'false' || normalised === '0' || normalised === 'no' || normalised === '');
}

/** Optional parameters every endpoint accepts. */
function commonParams(flags) {
  // A bare `--limit` with no value parses as boolean true, which is not a value.
  const valued = (v) => (v === true ? undefined : v);
  return {
    limit: valued(flags.limit),
    cursor: valued(flags.cursor),
    fields: valued(flags.fields),
    format: valued(flags.format),
    fresh: boolFlag(flags.fresh) ? 'true' : undefined,
  };
}

function usage(message) {
  process.stderr.write(message.trim() + '\n');
  process.exit(2);
}

/** Run an async main() and print its JSON result. */
function main(fn) {
  fn()
    .then((result) => {
      process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    })
    .catch((cause) => {
      fail('unexpected_error', String(cause && cause.stack ? cause.stack : cause));
    });
}

module.exports = {
  API_BASE,
  ENV_VAR,
  MAX_SYNC_LIMIT,
  REQUEST_TIMEOUT_MS,
  boolFlag,
  callEndpoint,
  commonParams,
  fail,
  main,
  parseFlags,
  usage,
};
