#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i++;
    }
  }
  return args;
}

function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function mapZone(zoneName) {
  const raw = String(zoneName || 'z2').trim();
  const simplified = raw
    .replace(/^qiniu\.zone\./i, '')
    .replace(/^zone_/i, '')
    .toLowerCase();
  const zoneMap = {
    z0: 'z0',
    zone_z0: 'z0',
    z1: 'z1',
    zone_z1: 'z1',
    z2: 'z2',
    zone_z2: 'z2',
    na0: 'na0',
    zone_na0: 'na0',
    as0: 'as0',
    zone_as0: 'as0'
  };
  if (!zoneMap[simplified]) {
    throw new Error(`Unsupported QINIU_ZONE: ${zoneName}`);
  }
  return zoneMap[simplified];
}

function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/mp4',
    '.aac': 'audio/aac',
    '.mp4': 'video/mp4',
    '.mov': 'video/quicktime',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.pdf': 'application/pdf',
    '.txt': 'text/plain'
  };
  return map[ext] || 'application/octet-stream';
}

function buildObjectKey(filePath, prefix, explicitKey) {
  if (explicitKey) return explicitKey.replace(/^\/+/, '');
  const ext = path.extname(filePath);
  const random = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${crypto.randomBytes(6).toString('hex')}`;
  const cleanedPrefix = (prefix || 'uploads').replace(/\\/g, '/').replace(/^\/+|\/+$/g, '');
  return cleanedPrefix ? `${cleanedPrefix}/${random}${ext}` : `${random}${ext}`;
}

function base64Url(input) {
  return Buffer.from(input)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function signHmacSha1(data, secretKey) {
  return crypto
    .createHmac('sha1', secretKey)
    .update(data)
    .digest('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function createUploadToken({ accessKey, secretKey, bucket, key }) {
  const putPolicy = {
    scope: `${bucket}:${key}`,
    deadline: Math.floor(Date.now() / 1000) + 3600,
    returnBody: '{"key":"$(key)","hash":"$(etag)","fsize":$(fsize),"bucket":"$(bucket)"}'
  };
  const encodedPolicy = base64Url(JSON.stringify(putPolicy));
  const sign = signHmacSha1(encodedPolicy, secretKey);
  return `${accessKey}:${sign}:${encodedPolicy}`;
}

async function uploadByForm({ uploadToken, key, filePath, mimeType, zone }) {
  const zones = {
    z0: 'https://upload.qiniup.com',
    z1: 'https://upload-z1.qiniup.com',
    z2: 'https://upload-z2.qiniup.com',
    na0: 'https://upload-na0.qiniup.com',
    as0: 'https://upload-as0.qiniup.com'
  };
  const endpoint = zones[zone];
  const fileBuffer = fs.readFileSync(filePath);
  const fileName = path.basename(filePath);

  const form = new FormData();
  form.append('token', uploadToken);
  form.append('key', key);
  form.append('file', new Blob([fileBuffer], { type: mimeType }), fileName);

  const response = await fetch(endpoint, {
    method: 'POST',
    body: form
  });

  const text = await response.text();
  if (!response.ok) {
    throw new Error(`Qiniu upload failed (${response.status}): ${text}`);
  }

  return text ? JSON.parse(text) : {};
}

function ensureTrailingSlashless(url) {
  return url.replace(/\/+$/, '');
}

function buildPublicUrl(domain, key) {
  return `${ensureTrailingSlashless(domain)}/${key}`;
}

function buildPrivateUrl(domain, key, accessKey, secretKey, expireSeconds) {
  const deadline = Math.floor(Date.now() / 1000) + expireSeconds;
  const publicUrl = buildPublicUrl(domain, key);
  const separator = publicUrl.includes('?') ? '&' : '?';
  const urlWithDeadline = `${publicUrl}${separator}e=${deadline}`;
  const encoded = signHmacSha1(urlWithDeadline, secretKey);
  return `${urlWithDeadline}&token=${accessKey}:${encoded}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const filePath = args['file-path'];
  if (!filePath) {
    throw new Error('Missing required argument: --file-path');
  }

  const resolvedPath = path.resolve(filePath);
  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`File not found: ${resolvedPath}`);
  }

  const stat = fs.statSync(resolvedPath);
  if (!stat.isFile()) {
    throw new Error(`Path is not a file: ${resolvedPath}`);
  }

  const accessKey = requireEnv('QINIU_ACCESS_KEY');
  const secretKey = requireEnv('QINIU_SECRET_KEY');
  const bucket = requireEnv('QINIU_BUCKET');
  const domain = requireEnv('QINIU_DOMAIN');
  const zone = mapZone(process.env.QINIU_ZONE || 'z2');
  const key = buildObjectKey(resolvedPath, args.prefix, args.key);
  const mimeType = getMimeType(resolvedPath);
  const uploadToken = createUploadToken({ accessKey, secretKey, bucket, key });

  const uploadResult = await uploadByForm({
    uploadToken,
    key,
    filePath: resolvedPath,
    mimeType,
    zone
  });

  const privateMode = args.private === true || String(process.env.QINIU_PRIVATE_BUCKET || '').toLowerCase() === 'true';
  const expireSeconds = Number(args['expire-seconds'] || process.env.QINIU_PRIVATE_EXPIRE_SECONDS || 3600);
  const url = privateMode
    ? buildPrivateUrl(domain, key, accessKey, secretKey, expireSeconds)
    : buildPublicUrl(domain, key);

  const result = {
    success: true,
    bucket,
    key,
    url,
    isPrivate: privateMode,
    expireSeconds: privateMode ? expireSeconds : null,
    size: stat.size,
    mimeType,
    sourcePath: resolvedPath,
    upload: uploadResult
  };

  console.log(JSON.stringify(result, null, args.json ? 0 : 2));
}

main().catch((error) => {
  const payload = {
    success: false,
    error: error.message
  };
  console.error(JSON.stringify(payload, null, 2));
  process.exit(1);
});
