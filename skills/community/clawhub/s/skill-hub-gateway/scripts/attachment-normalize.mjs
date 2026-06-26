import { promises as fs } from 'node:fs';
import { basename, extname, isAbsolute, resolve as resolvePath } from 'node:path';

export const DEFAULT_SITE_BASE_URL = 'https://gateway.binaryworks.app';
const DEFAULT_PATH_PREFIX = 'skill-inputs';
const DIRECT_UPLOAD_PATH = '/api/blob/upload-file';

const IMAGE_CAPABILITIES = new Set([
  'human_detect',
  'image_tagging',
  'face-detect',
  'person-detect',
  'hand-detect',
  'body-keypoints-2d',
  'body-contour-63pt',
  'face-keypoints-106pt',
  'head-pose',
  'face-feature-classification',
  'face-action-classification',
  'face-image-quality',
  'face-emotion-recognition',
  'face-physical-attributes',
  'face-social-attributes',
  'political-figure-recognition',
  'designated-person-recognition',
  'exhibit-image-recognition',
  'person-instance-segmentation',
  'person-semantic-segmentation',
  'concert-cutout',
  'full-body-matting',
  'head-matting',
  'product-cutout'
]);

const MIME_BY_EXTENSION = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
  '.webm': 'audio/webm',
  '.ogg': 'audio/ogg',
  '.m4a': 'audio/mp4',
  '.mp4': 'audio/mp4',
  '.pdf': 'application/pdf',
  '.txt': 'text/plain',
  '.md': 'text/markdown',
  '.markdown': 'text/markdown'
};

export async function normalizeExecutePayload(payloadRaw, options = {}) {
  const payload = toObject(payloadRaw);
  const capability = typeof payload.capability === 'string' ? payload.capability.trim() : '';
  const input = toObject(payload.input);

  const normalizedInput = { ...input };
  const explicitNormalized = normalizeExplicitUrlFields(normalizedInput, payload);

  if (!explicitNormalized) {
    const attachmentUrl = resolveAttachmentUrl(normalizedInput, payload);
    const targetFromCapability = resolveTargetField(capability);
    if (attachmentUrl) {
      const target = targetFromCapability ?? resolveTargetFieldFromUrl(attachmentUrl) ?? 'file_url';
      normalizedInput[target] = attachmentUrl;
    }
  }

  if (!hasAnyMediaUrl(normalizedInput)) {
    const filePath = resolveFilePath(normalizedInput, payload);
    if (filePath) {
      const siteBaseUrl = resolveTrustedSiteBaseUrl(options.siteBaseUrl);
      assertRequestedSiteBaseUrlAllowed(options.requestedSiteBaseUrl, siteBaseUrl);
      const userToken = normalizeToken(options.userToken);
      if (!userToken) {
        throw createNormalizeError(401, 'AUTH_UNAUTHORIZED', 'user token is required for file_path upload');
      }

      const uploaded = await uploadFilePath(filePath, {
        siteBaseUrl,
        userToken,
        now: options.now,
        pathPrefix: options.pathPrefix,
        uploadFileImpl: options.uploadFileImpl
      });

      const targetFromCapability = resolveTargetField(capability);
      const target = targetFromCapability ?? resolveTargetFieldFromMime(uploaded.contentType) ?? 'file_url';
      normalizedInput[target] = uploaded.url;
    }
  }

  return {
    ...payload,
    input: normalizedInput
  };
}

function toObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    return {};
  }
  return { ...value };
}

function normalizeExplicitUrlFields(input, payload) {
  let found = false;
  for (const field of ['image_url', 'audio_url', 'file_url']) {
    const inInput = typeof input[field] === 'string' ? input[field].trim() : '';
    if (inInput) {
      input[field] = inInput;
      found = true;
      continue;
    }

    const inPayload = typeof payload[field] === 'string' ? payload[field].trim() : '';
    if (inPayload) {
      input[field] = inPayload;
      found = true;
    }
  }
  return found;
}

function resolveAttachmentUrl(input, payload) {
  const fromInput =
    input.attachment && typeof input.attachment === 'object'
      ? typeof input.attachment.url === 'string'
        ? input.attachment.url.trim()
        : ''
      : '';
  if (fromInput) {
    return fromInput;
  }

  const fromPayload =
    payload.attachment && typeof payload.attachment === 'object'
      ? typeof payload.attachment.url === 'string'
        ? payload.attachment.url.trim()
        : ''
      : '';
  return fromPayload || null;
}

function resolveFilePath(input, payload) {
  const fromInput = typeof input.file_path === 'string' ? input.file_path.trim() : '';
  if (fromInput) {
    return fromInput;
  }

  const fromPayload = typeof payload.file_path === 'string' ? payload.file_path.trim() : '';
  return fromPayload || null;
}

function resolveTargetField(capability) {
  if (!capability) {
    return null;
  }
  if (IMAGE_CAPABILITIES.has(capability)) {
    return 'image_url';
  }
  if (capability === 'asr') {
    return 'audio_url';
  }
  if (capability === 'markdown_convert') {
    return 'file_url';
  }
  return null;
}

function hasAnyMediaUrl(input) {
  return ['image_url', 'audio_url', 'file_url'].some(
    (field) => typeof input[field] === 'string' && input[field].trim().length > 0
  );
}

export function resolveTrustedSiteBaseUrl(raw) {
  const candidate = typeof raw === 'string' && raw.trim() ? raw.trim() : DEFAULT_SITE_BASE_URL;
  try {
    const parsed = new URL(candidate);
    if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
      throw new Error('invalid protocol');
    }
    return parsed.toString().replace(/\/+$/, '');
  } catch {
    throw createNormalizeError(400, 'VALIDATION_BAD_REQUEST', `invalid site_base_url: ${raw}`);
  }
}

function assertRequestedSiteBaseUrlAllowed(requestedRaw, trustedSiteBaseUrl) {
  if (typeof requestedRaw !== 'string' || !requestedRaw.trim()) {
    return;
  }

  let requested;
  try {
    requested = new URL(requestedRaw.trim()).toString().replace(/\/+$/, '');
  } catch {
    throw createNormalizeError(400, 'VALIDATION_BAD_REQUEST', `invalid site_base_url: ${requestedRaw}`);
  }

  if (requested !== trustedSiteBaseUrl) {
    throw createNormalizeError(
      400,
      'VALIDATION_SITE_BASE_URL_NOT_ALLOWED',
      'site_base_url is not allowed',
      {
        allowed_site_base_url: trustedSiteBaseUrl
      }
    );
  }
}

function normalizeToken(raw) {
  return typeof raw === 'string' ? raw.trim() : '';
}

function resolveTargetFieldFromUrl(rawUrl) {
  try {
    const parsed = new URL(rawUrl);
    const ext = extname(parsed.pathname).toLowerCase();
    const mimeType = MIME_BY_EXTENSION[ext] ?? '';
    return resolveTargetFieldFromMime(mimeType);
  } catch {
    return null;
  }
}

function resolveTargetFieldFromMime(mimeType) {
  if (mimeType.startsWith('image/')) {
    return 'image_url';
  }
  if (mimeType.startsWith('audio/')) {
    return 'audio_url';
  }
  return 'file_url';
}

function resolveAbsolutePath(rawPath) {
  return isAbsolute(rawPath) ? rawPath : resolvePath(process.cwd(), rawPath);
}

async function uploadFilePath(filePath, options) {
  const absolutePath = resolveAbsolutePath(filePath);
  let content;
  try {
    content = await fs.readFile(absolutePath);
  } catch (error) {
    const code = error && typeof error === 'object' ? error.code : '';
    if (code === 'ENOENT') {
      throw createNormalizeError(400, 'VALIDATION_FILE_PATH_NOT_FOUND', `file_path not found: ${filePath}`, {
        file_path: filePath,
        absolute_path: absolutePath
      });
    }
    throw createNormalizeError(500, 'SYSTEM_UPLOAD_READ_FAILED', `failed to read file_path: ${filePath}`, {
      file_path: filePath,
      absolute_path: absolutePath
    });
  }

  const fileName = basename(absolutePath) || 'upload.bin';
  const ext = extname(fileName).toLowerCase();
  const contentType = MIME_BY_EXTENSION[ext] ?? '';
  if (!contentType) {
    throw createNormalizeError(
      400,
      'VALIDATION_FILE_TYPE_NOT_SUPPORTED',
      `unsupported file type for file_path: ${fileName}`,
      {
        file_path: filePath,
        file_name: fileName
      }
    );
  }

  if (typeof File !== 'function') {
    return await uploadFileViaBackend(fileName, content, {
      filePath,
      contentType,
      siteBaseUrl: options.siteBaseUrl,
      userToken: options.userToken,
      pathPrefix: options.pathPrefix
    });
  }

  const file = new File([content], fileName, { type: contentType });
  const pathname = buildBlobPathname(fileName, options.now, options.pathPrefix);

  const uploadFileImpl = options.uploadFileImpl ?? defaultUploadFile;

  try {
    const result = await uploadFileImpl(pathname, file, {
      siteBaseUrl: options.siteBaseUrl,
      userToken: options.userToken
    });

    if (!result || typeof result.url !== 'string' || !result.url.trim()) {
      throw new Error('missing upload url');
    }

    return {
      url: result.url.trim(),
      contentType
    };
  } catch (error) {
    if (shouldFallbackToBackend(error)) {
      return await uploadFileViaBackend(fileName, content, {
        filePath,
        contentType,
        siteBaseUrl: options.siteBaseUrl,
        userToken: options.userToken,
        pathPrefix: options.pathPrefix
      });
    }
    if (
      error &&
      typeof error === 'object' &&
      typeof error.status === 'number' &&
      typeof error.code === 'string'
    ) {
      throw error;
    }
    const message = error instanceof Error ? error.message : String(error);
    throw createNormalizeError(500, 'SYSTEM_UPLOAD_FAILED', message, {
      file_path: filePath,
      pathname
    });
  }
}

async function defaultUploadFile(pathname, file, context) {
  let upload;
  try {
    const module = await import('@vercel/blob/client');
    upload = module.upload;
  } catch {
    throw createNormalizeError(
      500,
      'SYSTEM_UPLOAD_DEPENDENCY_MISSING',
      'missing dependency @vercel/blob/client; pre-upload file via backend (for example Vercel Blob) and provide attachment.url/image_url'
    );
  }
  return await upload(pathname, file, {
    access: 'public',
    handleUploadUrl: `${context.siteBaseUrl}/api/blob/upload`,
    headers: {
      Authorization: `Bearer ${context.userToken}`
    }
  });
}

function shouldFallbackToBackend(error) {
  if (!error || typeof error !== 'object') {
    return false;
  }
  return (
    error.code === 'SYSTEM_UPLOAD_DEPENDENCY_MISSING' ||
    error.code === 'SYSTEM_UPLOAD_RUNTIME_UNSUPPORTED'
  );
}

async function uploadFileViaBackend(fileName, content, options) {
  const userToken = normalizeToken(options.userToken);
  if (!userToken) {
    throw createNormalizeError(401, 'AUTH_UNAUTHORIZED', 'user token is required for backend upload');
  }

  const headers = {
    Authorization: `Bearer ${userToken}`,
    'Content-Type': options.contentType,
    'X-Filename': fileName
  };

  if (typeof options.pathPrefix === 'string' && options.pathPrefix.trim()) {
    headers['X-Path-Prefix'] = options.pathPrefix.trim();
  }

  const url = `${options.siteBaseUrl}${DIRECT_UPLOAD_PATH}`;
  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers,
      body: content
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw createNormalizeError(500, 'SYSTEM_UPLOAD_FAILED', message, {
      file_path: options.filePath,
      upload_url: url
    });
  }

  const bodyText = await response.text();
  const parsed = safeJsonParse(bodyText);

  if (!response.ok) {
    const apiError =
      parsed && typeof parsed === 'object' && parsed.error && typeof parsed.error === 'object'
        ? parsed.error
        : null;
    throw createNormalizeError(
      response.status,
      typeof apiError?.code === 'string' ? apiError.code : 'SYSTEM_UPLOAD_FAILED',
      typeof apiError?.message === 'string' ? apiError.message : bodyText || 'upload failed',
      {
        file_path: options.filePath,
        upload_url: url,
        status: response.status
      }
    );
  }

  const urlValue =
    parsed && typeof parsed === 'object'
      ? typeof parsed.url === 'string'
        ? parsed.url
        : parsed.data && typeof parsed.data === 'object' && typeof parsed.data.url === 'string'
          ? parsed.data.url
          : ''
      : '';

  if (!urlValue.trim()) {
    throw createNormalizeError(500, 'SYSTEM_UPLOAD_FAILED', 'missing upload url', {
      file_path: options.filePath,
      upload_url: url
    });
  }

  return {
    url: urlValue.trim(),
    contentType: options.contentType
  };
}

function safeJsonParse(value) {
  if (!value) {
    return null;
  }
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

function buildBlobPathname(fileNameRaw, nowInput, pathPrefixRaw) {
  const now = nowInput instanceof Date ? nowInput : new Date();
  const pathPrefix =
    typeof pathPrefixRaw === 'string' && pathPrefixRaw.trim()
      ? pathPrefixRaw.trim().replace(/^\/+|\/+$/g, '')
      : DEFAULT_PATH_PREFIX;
  const safeFileName = sanitizeFileName(fileNameRaw);
  const yyyy = String(now.getUTCFullYear());
  const mm = String(now.getUTCMonth() + 1).padStart(2, '0');
  const dd = String(now.getUTCDate()).padStart(2, '0');
  const unique = `${now.getTime().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  return `${pathPrefix}/${yyyy}/${mm}/${dd}/${unique}-${safeFileName}`;
}

function sanitizeFileName(fileNameRaw) {
  const fallback = 'upload.bin';
  const trimmed = String(fileNameRaw ?? '').trim();
  if (!trimmed) {
    return fallback;
  }
  const clean = trimmed
    .replace(/[^A-Za-z0-9._-]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^\.+/, '')
    .slice(0, 120);
  return clean || fallback;
}

function createNormalizeError(status, code, message, details) {
  const error = new Error(message);
  error.status = status;
  error.code = code;
  error.details = details;
  return error;
}
