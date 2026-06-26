#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

const OPENCLAW_ROOT = process.env.OPENCLAW_ROOT || path.join(process.env.HOME || '', '.openclaw');
const JOBS_PATH =
  process.env.OPENCLAW_CRON_JOBS_PATH || path.join(OPENCLAW_ROOT, 'cron', 'jobs.json');

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) continue;
    const k = a.slice(2);
    const v = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : 'true';
    out[k] = v;
  }
  return out;
}

function b64url(input) {
  const buf = Buffer.isBuffer(input) ? input : Buffer.from(input);
  return buf.toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
}

function parseBool(v) {
  if (v == null) return false;
  return ['1', 'true', 'yes', 'y', 'on'].includes(String(v).trim().toLowerCase());
}

async function getServiceAccountToken(clientEmail, privateKey) {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const claim = {
    iss: clientEmail,
    scope: 'https://www.googleapis.com/auth/spreadsheets.readonly',
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600,
  };

  const signingInput = `${b64url(JSON.stringify(header))}.${b64url(JSON.stringify(claim))}`;
  const signer = crypto.createSign('RSA-SHA256');
  signer.update(signingInput);
  signer.end();
  const signature = signer.sign(privateKey);
  const assertion = `${signingInput}.${b64url(signature)}`;

  const resp = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion,
    }),
  });
  if (!resp.ok) throw new Error(`token_failed_${resp.status}`);
  const json = await resp.json();
  if (!json.access_token) throw new Error('token_missing');
  return json.access_token;
}

function toRows(values) {
  if (!values || !values.length) return [];
  const headers = values[0].map((x) => String(x || '').trim());
  return values.slice(1).map((row) => {
    const obj = {};
    headers.forEach((h, i) => {
      obj[h] = String(row[i] || '').trim();
    });
    return obj;
  });
}

async function loadSheetRows() {
  const spreadsheetId = process.env.GOOGLE_SHEETS_SPREADSHEET_ID;
  const range = process.env.GOOGLE_SHEETS_RANGE || 'Sheet1!A1:Z2000';
  const clientEmail = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKeyRaw = process.env.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY;
  if (!spreadsheetId || !clientEmail || !privateKeyRaw) {
    throw new Error('missing_env_google_sheet_auth');
  }
  const privateKey = privateKeyRaw.replace(/\\n/g, '\n');
  const token = await getServiceAccountToken(clientEmail, privateKey);
  const url = `https://sheets.googleapis.com/v4/spreadsheets/${encodeURIComponent(spreadsheetId)}/values/${encodeURIComponent(range)}`;
  const resp = await fetch(url, { headers: { authorization: `Bearer ${token}` } });
  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error(`sheet_fetch_failed_${resp.status}:${txt.slice(0,200)}`);
  }
  const body = await resp.json();
  return toRows(body.values || []);
}

async function main() {
  const args = parseArgs(process.argv);
  const apply = parseBool(args.apply);

  const rows = await loadSheetRows();
  const desired = new Map();
  for (const r of rows) {
    if (!r.job_id) continue;
    desired.set(r.job_id, parseBool(r.enabled));
  }

  const jobsDoc = JSON.parse(await fs.readFile(JOBS_PATH, 'utf8'));
  const changes = [];

  for (const job of jobsDoc.jobs || []) {
    const has = desired.has(job.id);
    const shouldEnable = has ? desired.get(job.id) : false;
    if (job.enabled !== shouldEnable) {
      changes.push({ id: job.id, name: job.name, from: job.enabled, to: shouldEnable, reason: has ? 'sheet_enabled' : 'missing_in_sheet' });
      job.enabled = shouldEnable;
      job.updatedAtMs = Date.now();
    }
  }

  if (!apply) {
    console.log(JSON.stringify({ mode: 'dry-run', totalJobs: jobsDoc.jobs?.length || 0, changes }, null, 2));
    return;
  }

  const backup = `${JOBS_PATH}.pre-sheet-reconcile.${Date.now()}.bak`;
  await fs.copyFile(JOBS_PATH, backup);
  await fs.writeFile(JOBS_PATH, JSON.stringify(jobsDoc, null, 2) + '\n', 'utf8');
  console.log(JSON.stringify({ mode: 'apply', totalJobs: jobsDoc.jobs?.length || 0, changes, backup }, null, 2));
}

main().catch((err) => {
  console.error(String(err.message || err));
  process.exit(1);
});
