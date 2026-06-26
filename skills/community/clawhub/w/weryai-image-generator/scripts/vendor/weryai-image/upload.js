import fs from 'node:fs/promises';
import path from 'node:path';
import {
  isRemoteUrl,
  normalizeLocalFilePath,
  resolvePublicUrlFromSource,
} from '../weryai-core/upload.js';

const IMAGE_EXTS = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif']);
const IMAGE_SIZE_MAX_BYTES = 10 * 1024 * 1024;

export { isRemoteUrl, normalizeLocalFilePath };

export function collectLocalUploadPreview(input) {
  const out = [];
  const images = Array.isArray(input.images) ? input.images : [];
  images.forEach((value, idx) => {
    if (typeof value === 'string' && value.trim() && !isRemoteUrl(value)) {
      out.push({ field: `images[${idx}]`, source: value, kind: 'image' });
    }
  });
  return out;
}

export async function validateLocalImageSource(value, fieldName, errors) {
  if (!value || typeof value !== 'string') return;
  if (isRemoteUrl(value)) {
    return;
  }
  const localPath = normalizeLocalFilePath(value);
  if (!localPath) {
    errors.push(`${fieldName} local path is invalid.`);
    return;
  }

  let stat;
  try {
    stat = await fs.stat(localPath);
  } catch {
    errors.push(`${fieldName} local file not found: ${value}`);
    return;
  }
  if (!stat.isFile()) {
    errors.push(`${fieldName} local path is not a file: ${value}`);
    return;
  }

  const ext = path.extname(localPath).toLowerCase();
  if (!IMAGE_EXTS.has(ext)) {
    errors.push(`${fieldName} must use one of image formats: jpg, jpeg, png, webp, gif.`);
  }
  if (stat.size > IMAGE_SIZE_MAX_BYTES) {
    errors.push(`${fieldName} exceeds 10MB image limit.`);
  }
}

export async function validateLocalImageSources(images) {
  const errors = [];
  const list = Array.isArray(images) ? images : [];
  await Promise.all(
    list.map((value, idx) => validateLocalImageSource(value, `images[${idx}]`, errors)),
  );
  return errors;
}

export async function resolveImageUploadSources(ctx, body) {
  const out = { ...body };
  if (Array.isArray(out.images)) {
    out.images = await Promise.all(out.images.map((item) => resolvePublicUrlFromSource(ctx, item)));
  }
  return out;
}
