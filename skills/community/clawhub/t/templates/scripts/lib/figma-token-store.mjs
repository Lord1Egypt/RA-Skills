import fs from 'node:fs/promises';
import path from 'node:path';

import { acquireDirectoryLock } from './lock-dir.mjs';
import { createStableError, redactString } from './redact.mjs';

const TOKEN_SCHEMA_VERSION = 'figma-oauth-token/v1';
const REFRESH_BEFORE_EXPIRY_MS = 5 * 60 * 1000;
const FIGMA_OAUTH_TOKEN_URL = 'https://api.figma.com/v1/oauth/token';

const ENV_KEYS = [
  'FIGMA_CLIENT_ID',
  'FIGMA_CLIENT_SECRET',
  'FIGMA_ACCESS_TOKEN',
  'FIGMA_REFRESH_TOKEN',
  'FIGMA_TOKEN_TYPE',
  'FIGMA_TOKEN_EXPIRES_AT',
];

function modeOf(stat) {
  return stat.mode & 0o777;
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch (error) {
    if (error?.code === 'ENOENT') {
      return false;
    }
    throw error;
  }
}

async function assertSecurePermissions(tokenStorePath) {
  const dirPath = path.dirname(tokenStorePath);
  let dirStat;
  let fileStat;
  try {
    dirStat = await fs.stat(dirPath);
    fileStat = await fs.stat(tokenStorePath);
  } catch (error) {
    if (error?.code === 'ENOENT') {
      throw error;
    }
    throw createStableError('figma_token_store_unreadable', 'Could not read Figma token store permissions');
  }

  if (modeOf(dirStat) !== 0o700) {
    throw createStableError('figma_token_dir_insecure', 'Figma token directory must use 0700 permissions');
  }
  if (modeOf(fileStat) !== 0o600) {
    throw createStableError('figma_token_file_insecure', 'Figma token store must use 0600 permissions');
  }
}

function normalizeTokenRecord(record) {
  const expiresAt = normalizeExpiresAt(record.expiresAt);
  return {
    schemaVersion: TOKEN_SCHEMA_VERSION,
    clientId: record.clientId,
    clientSecret: record.clientSecret,
    accessToken: record.accessToken,
    refreshToken: record.refreshToken,
    tokenType: normalizeTokenType(record.tokenType),
    expiresAt,
  };
}

function normalizeTokenType(value) {
  if (typeof value !== 'string' || value.trim().length === 0) {
    return 'Bearer';
  }
  return value.trim().toLowerCase() === 'bearer' ? 'Bearer' : value.trim();
}

function normalizeExpiresAt(value) {
  if (typeof value === 'number' && Number.isFinite(value)) {
    return new Date(value < 1_000_000_000_000 ? value * 1000 : value).toISOString();
  }

  if (typeof value !== 'string' || value.length === 0) {
    return value;
  }

  if (/^\d+$/.test(value)) {
    const numericValue = Number(value);
    if (Number.isFinite(numericValue)) {
      return new Date(numericValue < 1_000_000_000_000 ? numericValue * 1000 : numericValue).toISOString();
    }
  }

  return value;
}

function validateTokenRecord(record, code = 'figma_token_store_invalid') {
  const normalized = normalizeTokenRecord(record ?? {});
  const missing = ['clientId', 'clientSecret', 'accessToken', 'refreshToken', 'tokenType', 'expiresAt'].filter(
    (key) => typeof normalized[key] !== 'string' || normalized[key].length === 0,
  );
  const expiresAtMs = new Date(normalized.expiresAt).getTime();
  if (missing.length > 0 || !Number.isFinite(expiresAtMs)) {
    throw createStableError(code, `${code}: missing or invalid Figma token fields`);
  }
  return normalized;
}

export async function readTokenStore(tokenStorePath) {
  await assertSecurePermissions(tokenStorePath);
  let raw;
  try {
    raw = await fs.readFile(tokenStorePath, 'utf8');
  } catch {
    throw createStableError('figma_token_store_unreadable', 'Could not read Figma token store');
  }

  try {
    return validateTokenRecord(JSON.parse(raw));
  } catch (error) {
    if (error?.code) {
      throw error;
    }
    throw createStableError('figma_token_store_invalid', 'Figma token store is not valid JSON');
  }
}

export async function writeTokenStore(tokenStorePath, record) {
  const normalized = validateTokenRecord(record);
  const dirPath = path.dirname(tokenStorePath);
  await fs.mkdir(dirPath, { recursive: true, mode: 0o700 });
  await fs.chmod(dirPath, 0o700);

  const tempPath = `${tokenStorePath}.${process.pid}.${Date.now()}.tmp`;
  await fs.writeFile(tempPath, `${JSON.stringify(normalized, null, 2)}\n`, { mode: 0o600 });
  await fs.chmod(tempPath, 0o600);
  await fs.rename(tempPath, tokenStorePath);
  await fs.chmod(tokenStorePath, 0o600);
  return normalized;
}

function parseEnvLine(line) {
  const trimmed = line.trim();
  if (trimmed.length === 0 || trimmed.startsWith('#')) {
    return null;
  }
  const equalIndex = trimmed.indexOf('=');
  if (equalIndex < 0) {
    return null;
  }
  const key = trimmed.slice(0, equalIndex).trim();
  let value = trimmed.slice(equalIndex + 1).trim();
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    value = value.slice(1, -1);
  }
  return { key, value };
}

async function readEnvFile(envFile) {
  let raw;
  try {
    raw = await fs.readFile(envFile, 'utf8');
  } catch (error) {
    if (error?.code === 'ENOENT') {
      return null;
    }
    throw createStableError('figma_env_unreadable', `Could not read Figma env file: ${envFile}`);
  }

  const values = {};
  for (const line of raw.split(/\r?\n/)) {
    const parsed = parseEnvLine(line);
    if (parsed && parsed.key.startsWith('FIGMA_')) {
      values[parsed.key] = parsed.value;
    }
  }
  return values;
}

async function importFromEnvFiles(envFiles) {
  for (const envFile of envFiles ?? []) {
    const values = await readEnvFile(envFile);
    if (!values) {
      continue;
    }
    const hasAll = ENV_KEYS.every((key) => typeof values[key] === 'string' && values[key].length > 0);
    if (!hasAll) {
      continue;
    }
    return validateTokenRecord(
      {
        clientId: values.FIGMA_CLIENT_ID,
        clientSecret: values.FIGMA_CLIENT_SECRET,
        accessToken: values.FIGMA_ACCESS_TOKEN,
        refreshToken: values.FIGMA_REFRESH_TOKEN,
        tokenType: values.FIGMA_TOKEN_TYPE,
        expiresAt: values.FIGMA_TOKEN_EXPIRES_AT,
      },
      'figma_env_missing',
    );
  }

  throw createStableError(
    'figma_env_missing',
    'No complete Figma credentials found in configured env files; initialize token store first',
  );
}

function shouldRefresh(record, now) {
  const expiresAtMs = new Date(record.expiresAt).getTime();
  return expiresAtMs - now.getTime() < REFRESH_BEFORE_EXPIRY_MS;
}

async function parseRefreshResponse(response, previousRecord, now) {
  let body = {};
  try {
    body = await response.json();
  } catch {
    body = {};
  }

  if (!response.ok) {
    if (body?.error === 'invalid_grant') {
      throw createStableError('figma_token_invalid_grant', 'Figma refresh token is invalid; reauthorize');
    }
    throw createStableError(
      'figma_token_refresh_failed',
      redactString('Figma token refresh failed', {
        secrets: [previousRecord.accessToken, previousRecord.refreshToken, previousRecord.clientSecret],
      }),
      { status: response.status, retryable: response.status >= 500 || response.status === 429 },
    );
  }

  const expiresInSeconds = Number(body.expires_in);
  const expiresAt = Number.isFinite(expiresInSeconds)
    ? new Date(now.getTime() + expiresInSeconds * 1000).toISOString()
    : previousRecord.expiresAt;

  return validateTokenRecord({
    ...previousRecord,
    accessToken: body.access_token,
    refreshToken: body.refresh_token || previousRecord.refreshToken,
    tokenType: body.token_type || previousRecord.tokenType || 'Bearer',
    expiresAt,
  });
}

async function refreshToken(record, options) {
  const fetchImpl = options.fetchImpl ?? fetch;
  const params = new URLSearchParams();
  params.set('client_id', record.clientId);
  params.set('client_secret', record.clientSecret);
  params.set('grant_type', 'refresh_token');
  params.set('refresh_token', record.refreshToken);

  const response = await fetchImpl(FIGMA_OAUTH_TOKEN_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: params,
  });
  return parseRefreshResponse(response, record, options.now());
}

async function loadExistingOrImport(options) {
  if (await exists(options.tokenStorePath)) {
    return readTokenStore(options.tokenStorePath);
  }

  const imported = await importFromEnvFiles(options.envFiles);
  return writeTokenStore(options.tokenStorePath, imported);
}

async function refreshUnderLock(currentRecord, options) {
  const lockDir = `${options.tokenStorePath.replace(/\.json$/i, '')}.lock`;
  const lock = await acquireDirectoryLock(lockDir, {
    now: options.now,
    retryDelayMs: options.lockRetryDelayMs,
    timeoutMs: options.lockTimeoutMs,
  });

  try {
    const latest = await loadExistingOrImport(options);
    if (options.forceRefresh && options.forceRefreshAccessToken && latest.accessToken !== options.forceRefreshAccessToken) {
      return latest;
    }
    if (!options.forceRefresh && !shouldRefresh(latest, options.now())) {
      return latest;
    }
    const refreshed = await refreshToken(latest, options);
    return writeTokenStore(options.tokenStorePath, refreshed);
  } finally {
    await lock.release();
  }
}

export async function ensureFigmaAccessToken(options) {
  const resolvedOptions = {
    ...options,
    now: options.now ?? (() => new Date()),
  };
  if (!resolvedOptions.tokenStorePath) {
    throw createStableError('figma_token_store_missing', 'Figma token store path is required');
  }

  const record = await loadExistingOrImport(resolvedOptions);
  if (!resolvedOptions.forceRefresh && !shouldRefresh(record, resolvedOptions.now())) {
    return {
      accessToken: record.accessToken,
      tokenType: record.tokenType,
      expiresAt: record.expiresAt,
      record,
    };
  }

  const refreshed = await refreshUnderLock(record, resolvedOptions);
  return {
    accessToken: refreshed.accessToken,
    tokenType: refreshed.tokenType,
    expiresAt: refreshed.expiresAt,
    record: refreshed,
  };
}

export async function withFigmaTokenRetry(options, operation) {
  const firstToken = await ensureFigmaAccessToken(options);
  const firstResult = await operation(firstToken);
  if (firstResult?.status !== 401) {
    return firstResult;
  }

  const refreshedToken = await ensureFigmaAccessToken({
    ...options,
    forceRefresh: true,
    forceRefreshAccessToken: firstToken.accessToken,
  });
  return operation(refreshedToken);
}
