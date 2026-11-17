import fs from 'node:fs/promises';
import path from 'node:path';

import { createStableError, redactString } from './redact.mjs';

const DEFAULT_API_BASE_URL = 'https://api.figma.com';
const DEFAULT_MAX_ATTEMPTS = 3;
const DEFAULT_RETRY_DELAY_MS = 250;
const MAX_IMAGE_BYTES = 20 * 1024 * 1024;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function buildUrl(baseUrl, pathname, searchParams = {}) {
  const url = new URL(pathname, baseUrl);
  for (const [key, value] of Object.entries(searchParams)) {
    if (value !== undefined && value !== null) {
      url.searchParams.set(key, String(value));
    }
  }
  return url;
}

function retryAfterMs(response, fallbackMs) {
  const raw = response.headers.get('Retry-After');
  if (!raw) {
    return fallbackMs;
  }
  const seconds = Number(raw);
  if (Number.isFinite(seconds) && seconds >= 0) {
    return seconds * 1000;
  }
  const dateMs = new Date(raw).getTime();
  if (Number.isFinite(dateMs)) {
    return Math.max(0, dateMs - Date.now());
  }
  return fallbackMs;
}

function errorCodeForStatus(status) {
  if (status === 401) {
    return 'figma_api_unauthorized';
  }
  if (status === 403) {
    return 'figma_api_forbidden';
  }
  if (status === 404) {
    return 'figma_api_not_found';
  }
  if (status === 429) {
    return 'figma_api_rate_limited';
  }
  if (status >= 500) {
    return 'figma_api_server_error';
  }
  return 'figma_api_failed';
}

async function parseJson(response) {
  try {
    return await response.json();
  } catch {
    throw createStableError('figma_api_invalid_json', 'Figma API returned invalid JSON');
  }
}

async function toStructuredResult(promise) {
  try {
    const value = await promise;
    return { ok: true, status: 200, value };
  } catch (error) {
    if (error?.status === 401) {
      return { ok: false, status: 401, error };
    }
    throw error;
  }
}

function ensureAllowedHttpsImageUrl(imageUrl, allowedImageUrls) {
  if (!allowedImageUrls?.has(imageUrl)) {
    throw createStableError('image_url_not_allowed', 'Image URL was not returned by the current Figma Images API response');
  }

  let parsed;
  try {
    parsed = new URL(imageUrl);
  } catch {
    throw createStableError('image_url_invalid', 'Figma image URL is invalid');
  }

  if (parsed.protocol !== 'https:') {
    throw createStableError('image_url_invalid_protocol', 'Figma image URL must use https');
  }
}

async function responseToBuffer(response) {
  const contentLength = Number(response.headers.get('Content-Length'));
  if (Number.isFinite(contentLength) && contentLength > MAX_IMAGE_BYTES) {
    throw createStableError('screenshot_failed', 'Figma screenshot exceeds the 20 MiB limit');
  }

  const bytes = Buffer.from(await response.arrayBuffer());
  if (bytes.byteLength > MAX_IMAGE_BYTES) {
    throw createStableError('screenshot_failed', 'Figma screenshot exceeds the 20 MiB limit');
  }
  return bytes;
}

export function createFigmaRestClient(options) {
  const apiBaseUrl = options.apiBaseUrl ?? DEFAULT_API_BASE_URL;
  const fetchImpl = options.fetchImpl ?? fetch;
  const imageFetchImpl = options.imageFetchImpl ?? fetchImpl;
  const tokenProvider = options.tokenProvider;
  const maxAttempts = options.maxAttempts ?? DEFAULT_MAX_ATTEMPTS;
  const retryDelayMs = options.retryDelayMs ?? DEFAULT_RETRY_DELAY_MS;
  const sleepImpl = options.sleep ?? sleep;

  if (!tokenProvider?.withTokenRetry) {
    throw createStableError('figma_token_provider_missing', 'Figma token provider is required');
  }

  async function authorizedJson(pathname, searchParams) {
    const result = await tokenProvider.withTokenRetry((token) =>
      toStructuredResult(authorizedJsonOnce({ pathname, searchParams, token })),
    );
    if (result?.ok) {
      return result.value;
    }
    throw result.error;
  }

  async function authorizedJsonOnce({ pathname, searchParams, token }) {
    const url = buildUrl(apiBaseUrl, pathname, searchParams);
    let lastNetworkError = null;

    for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
      let response;
      try {
        response = await fetchImpl(url, {
          method: 'GET',
          headers: {
            Authorization: `${token.tokenType ?? 'Bearer'} ${token.accessToken}`,
          },
        });
      } catch (error) {
        lastNetworkError = error;
        if (attempt < maxAttempts) {
          await sleepImpl(retryDelayMs * attempt);
          continue;
        }
        throw createStableError(
          'figma_api_network_error',
          redactString(`Figma API network error: ${error?.message ?? error}`),
          { retryable: true },
        );
      }

      if (response.ok) {
        return parseJson(response);
      }

      if (response.status === 429 && attempt < maxAttempts) {
        await sleepImpl(retryAfterMs(response, retryDelayMs * attempt));
        continue;
      }

      if (response.status >= 500 && attempt < maxAttempts) {
        await sleepImpl(retryDelayMs * attempt);
        continue;
      }

      throw createStableError(errorCodeForStatus(response.status), `Figma API request failed with ${response.status}`, {
        status: response.status,
        retryable: response.status === 429 || response.status >= 500,
      });
    }

    throw createStableError(
      'figma_api_network_error',
      redactString(`Figma API network error: ${lastNetworkError?.message ?? 'unknown'}`),
      { retryable: true },
    );
  }

  async function getMe() {
    return authorizedJson('/v1/me');
  }

  async function getNode({ fileKey, nodeId, depth }) {
    const body = await authorizedJson(`/v1/files/${encodeURIComponent(fileKey)}/nodes`, {
      ids: nodeId,
      depth,
    });
    const node = body?.nodes?.[nodeId];
    if (!node) {
      throw createStableError('figma_node_not_found', 'Figma node is null or missing', {
        retryable: false,
      });
    }
    return {
      fileVersion: body.version ?? null,
      document: node.document,
      node,
      raw: body,
    };
  }

  async function getFile({ fileKey, depth }) {
    const body = await authorizedJson(`/v1/files/${encodeURIComponent(fileKey)}`, {
      depth,
    });
    return {
      fileVersion: body.version ?? null,
      document: body.document,
      raw: body,
    };
  }

  async function getImages({ fileKey, nodeIds, scale = 2, format = 'png' }) {
    const ids = Array.isArray(nodeIds) ? nodeIds.join(',') : nodeIds;
    const body = await authorizedJson(`/v1/images/${encodeURIComponent(fileKey)}`, {
      ids,
      format,
      scale,
    });
    const images = body?.images ?? {};
    return {
      images,
      allowedImageUrls: new Set(Object.values(images).filter((value) => typeof value === 'string' && value.length > 0)),
    };
  }

  async function downloadImage({ imageUrl, allowedImageUrls, outPath }) {
    ensureAllowedHttpsImageUrl(imageUrl, allowedImageUrls);
    let response;
    try {
      response = await imageFetchImpl(imageUrl);
    } catch {
      throw createStableError('screenshot_failed', 'Could not download Figma screenshot', {
        retryable: true,
      });
    }

    if (!response.ok) {
      throw createStableError('screenshot_failed', `Figma screenshot download failed with ${response.status}`, {
        status: response.status,
        retryable: response.status >= 500 || response.status === 429,
      });
    }

    const bytes = await responseToBuffer(response);
    await fs.mkdir(path.dirname(outPath), { recursive: true });
    await fs.writeFile(outPath, bytes);
    return {
      path: outPath,
      byteLength: bytes.byteLength,
    };
  }

  async function exportNodeImage({ fileKey, nodeId, outPath, scale = 2 }) {
    const { images, allowedImageUrls } = await getImages({ fileKey, nodeIds: [nodeId], scale });
    const imageUrl = images[nodeId];
    if (!imageUrl) {
      throw createStableError('screenshot_failed', 'Figma Images API did not return a URL for the node');
    }
    return downloadImage({ imageUrl, allowedImageUrls, outPath });
  }

  return {
    getMe,
    getNode,
    getFile,
    getImages,
    downloadImage,
    exportNodeImage,
  };
}
