import fs from 'node:fs';

export function validateAudio(filePath, config) {
  if (!filePath) return { ok: false, error: 'no_file_path' };
  if (!fs.existsSync(filePath)) return { ok: false, error: 'file_not_found' };

  const stats = fs.statSync(filePath);
  if (stats.size === 0) return { ok: false, error: 'file_empty' };
  if (stats.size < config.limits.minFileSizeBytes) return { ok: false, error: 'file_too_small' };

  const ageSeconds = (Date.now() - stats.mtimeMs) / 1000;
  if (ageSeconds > config.limits.maxFileAgeSeconds) return { ok: false, error: 'file_stale' };

  return { ok: true, path: filePath, size: stats.size, ageSeconds: Math.floor(ageSeconds) };
}
