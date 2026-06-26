const fs = require('fs');
const path = require('path');
const os = require('os');
const AdmZip = require('adm-zip');

const BASE_URL = 'https://api.signus.ai';
const API_URL_PREFIX = '/api/signus';

function out(obj) {
  console.log(JSON.stringify(obj));
  process.exit(0);
}

function fail(msg, details = null) {
  console.log(JSON.stringify({ ok: false, error: msg, details }));
  process.exit(1);
}

function log(msg) {
  console.error(`[DEBUG] ${msg}`);
}

function parsePayload() {
  const args = process.argv.slice(2);
  if (args.length === 0) return {};

  try {
    return JSON.parse(args[0]);
  } catch {
    fail('Invalid JSON payload argument');
  }
}

function ensureIdentity(payload) {
  if (payload.name && String(payload.name).trim()) return;

  if (payload.firstName || payload.lastName) {
    const full = `${payload.firstName || ''} ${payload.lastName || ''}`.trim();
    if (full) {
      payload.name = full;
      delete payload.firstName;
      delete payload.lastName;
      return;
    }
  }

  if (payload.initials && String(payload.initials).trim()) {
    payload.name = String(payload.initials).trim();
    delete payload.initials;
    return;
  }

  fail('Missing required input: name, firstName/lastName, or initials');
}

function listImagesRecursive(dir) {
  const exts = new Set(['.png', '.jpg', '.jpeg', '.webp']);
  const files = [];

  function walk(current) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (exts.has(path.extname(entry.name).toLowerCase())) files.push(full);
    }
  }

  walk(dir);
  return files.sort();
}

function extractZipBuffer(zipBuffer, outputDir) {
  try {
    const zip = new AdmZip(zipBuffer);
    zip.extractAllTo(outputDir, true);
  } catch (err) {
    fail('Failed to extract ZIP response', { message: err.message });
  }
}

async function postJson(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/zip, application/octet-stream, application/json, */*',
    },
    body: JSON.stringify(payload),
  });

  const arrayBuffer = await res.arrayBuffer();
  const body = Buffer.from(arrayBuffer);
  const contentType = String(res.headers.get('content-type') || '').toLowerCase();

  return {
    ok: res.ok,
    status: res.status,
    contentType,
    body,
    url,
  };
}

async function downloadSignature(generationId, sigId, fileName) {
  const url = `${BASE_URL}${API_URL_PREFIX}/v0/signature-generations/font/${generationId}/signatures/${sigId}/${fileName}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Download failed (${res.status}) for ${sigId}`);
  }
  return Buffer.from(await res.arrayBuffer());
}

async function main() {
  const payload = parsePayload();
  ensureIdentity(payload);

  const countLimit = payload.count ? Number(payload.count) : null;

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const safeName = String(payload.name).replace(/\s+/g, '_');
  const outputDir = path.join(os.homedir(), '.openclaw', 'media', 'signatures-font', `${safeName}-${timestamp}`);
  fs.mkdirSync(outputDir, { recursive: true });
  log(`Output dir: ${outputDir}`);

  const endpoints = [
    `${BASE_URL}${API_URL_PREFIX}/v0/signature-generations/font`,
    `${BASE_URL}${API_URL_PREFIX}/v0/users/me/signature-generations/font`,
  ];

  let response = null;
  let lastError = null;

  for (const endpoint of endpoints) {
    log(`POST ${endpoint}`);
    const resp = await postJson(endpoint, payload);

    if (resp.ok) {
      response = resp;
      break;
    }

    lastError = {
      endpoint,
      status: resp.status,
      contentType: resp.contentType,
      bodyPreview: resp.body.toString('utf8').slice(0, 400),
    };
  }

  if (!response) {
    fail('Font generation failed on all known endpoints', lastError);
  }

  const signatures = [];

  if (response.contentType.includes('application/zip') || response.contentType.includes('application/octet-stream')) {
    const zipPath = path.join(outputDir, 'font-signatures.zip');
    fs.writeFileSync(zipPath, response.body);
    extractZipBuffer(response.body, outputDir);

    const images = listImagesRecursive(outputDir).filter((f) => !f.endsWith('.zip'));
    const limited = countLimit ? images.slice(0, countLimit) : images;

    if (limited.length === 0) {
      fail('Archive extracted but no image files were found', { outputDir });
    }

    for (let i = 0; i < limited.length; i++) {
      signatures.push({ id: String(i + 1), filePath: limited[i] });
    }
  } else {
    let json;
    try {
      json = JSON.parse(response.body.toString('utf8'));
    } catch {
      fail('Expected JSON or ZIP response, but body was not parseable JSON', {
        contentType: response.contentType,
      });
    }

    const items = json?.payload?.thisPageItems;
    if (!Array.isArray(items) || items.length === 0) {
      fail('JSON response did not include signature items', { responseUrl: response.url });
    }

    for (const item of items) {
      if (countLimit && signatures.length >= countLimit) break;

      const generationId = item.generationId;
      const sigId = item.generatedSignatureId;
      if (!generationId || !sigId) continue;

      const fileType = String(item?.files?.[0]?.fileType || 'CLEAN').toUpperCase();
      const fileName = fileType === 'WATERMARK' ? 'watermark.png' : 'clean.png';

      try {
        const img = await downloadSignature(generationId, sigId, fileName);
        const filePath = path.join(outputDir, `${sigId}.png`);
        fs.writeFileSync(filePath, img);
        signatures.push({ id: sigId, filePath });
      } catch (err) {
        log(err.message);
      }
    }

    if (signatures.length === 0) {
      fail('No signatures were downloadable from JSON payload');
    }
  }

  out({
    ok: true,
    count: signatures.length,
    directory: outputDir,
    signatures,
  });
}

main();
