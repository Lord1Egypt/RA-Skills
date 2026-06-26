#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const OPENCLAW_ROOT = process.env.OPENCLAW_ROOT || path.join(process.env.HOME || '', '.openclaw');
const STATE_DIR =
  process.env.OPENCLAW_RUNTIME_INSTRUCTIONS_DIR ||
  path.join(OPENCLAW_ROOT, 'memory', 'runtime-instructions');
const execFileAsync = promisify(execFile);

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

function parseCsv(v) {
  if (!v) return [];
  return String(v)
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean);
}

async function getAccessToken({ clientEmail, privateKey }) {
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

  const body = new URLSearchParams({
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    assertion,
  });

  const resp = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body,
  });
  if (!resp.ok) {
    const txt = await resp.text();
    throw new Error(`token_request_failed ${resp.status}: ${txt.slice(0, 300)}`);
  }
  const json = await resp.json();
  if (!json.access_token) throw new Error('token_missing_access_token');
  return json.access_token;
}

async function getGcloudAccessToken() {
  const { stdout } = await execFileAsync('gcloud', ['auth', 'print-access-token'], {
    timeout: 15000,
    maxBuffer: 1024 * 1024,
  });
  const token = String(stdout || '').trim();
  if (!token) throw new Error('gcloud_token_empty');
  return token;
}

function normalizeRow(headers, row) {
  const out = {};
  headers.forEach((h, i) => {
    out[h] = (row[i] || '').trim();
  });
  return out;
}

function matchRow(rows, jobId, jobName) {
  const id = String(jobId || '').trim();
  const name = String(jobName || '').trim().toLowerCase();

  let match = null;
  if (id) {
    match = rows.find((r) => String(r.job_id || '').trim() === id);
    if (match) return match;
  }
  if (name) {
    match = rows.find((r) => String(r.job_name || '').trim().toLowerCase() === name);
    if (match) return match;
  }
  return null;
}

function buildInstructionDoc(config, context) {
  const nonOverridableBlock = [
    '## Core Runtime Contract (non-overridable)',
    'Do not alter these operating constraints in any runtime override.',
    '- Operational Guardrails (required)',
    '- Testing & Recovery Contract (required)',
    '- Supabase Proof Contract (non-optional)',
    '- Focus Lock Contract (mandatory, non-overridable)',
    '- KPI_REPORT fields defined by the runtime job payload must be preserved',
    '',
    'This file is allowed to narrow goals, priorities, and platform scope,',
    'but it cannot remove or weaken those core constraints.',
  ].join('\n');

  const lines = [];
  lines.push('# Live Instructions (Google Sheet)');
  lines.push('');
  lines.push(`job_id: ${context.jobId}`);
  lines.push(`job_name: ${context.jobName}`);
  lines.push(`config_version: ${config.config_version || 'unknown'}`);
  lines.push(`updated_at: ${config.updated_at || 'unknown'}`);
  lines.push(`enabled: ${String(parseBool(config.enabled))}`);
  lines.push(`department: ${config.department || ''}`);
  lines.push(`area: ${config.area || ''}`);
  lines.push('');
  lines.push('## Goal');
  lines.push(config.goal || '');
  lines.push('');
  lines.push('## Priority Actions');
  for (const a of parseCsv(config.priority_actions)) lines.push(`- ${a}`);
  if (!parseCsv(config.priority_actions).length) lines.push('-');
  lines.push('');
  lines.push('## Do Not Do');
  for (const x of parseCsv(config.do_not_do)) lines.push(`- ${x}`);
  if (!parseCsv(config.do_not_do).length) lines.push('-');
  lines.push('');
  lines.push('## Platform Scope');
  for (const p of parseCsv(config.platform_scope)) lines.push(`- ${p}`);
  if (!parseCsv(config.platform_scope).length) lines.push('-');
  lines.push('');
  lines.push('## KPI Focus');
  for (const k of parseCsv(config.kpi_focus)) lines.push(`- ${k}`);
  if (!parseCsv(config.kpi_focus).length) lines.push('-');
  lines.push('');
  lines.push('## Limits');
  lines.push(`max_actions_per_run: ${config.max_actions_per_run || ''}`);
  lines.push('');
  lines.push('## Notes');
  lines.push(config.notes || '');
  lines.push('');
  lines.push('Treat this file as highest-priority runtime instruction source for this run.');
  lines.push('');
  lines.push(nonOverridableBlock);
  return lines.join('\n');
}

async function main() {
  const args = parseArgs(process.argv);
  const jobId = args['job-id'] || '';
  const jobName = args['job-name'] || '';
  const localOnly = parseBool(args['local-only']) || parseBool(process.env.OPENCLAW_LOCAL_INSTRUCTIONS_ONLY);
  const spreadsheetId = process.env.GOOGLE_SHEETS_SPREADSHEET_ID;
  const range = process.env.GOOGLE_SHEETS_RANGE || 'job_instructions!A1:Z2000';
  const clientEmail = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
  const privateKeyRaw = process.env.GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY;
  const privateKey = privateKeyRaw ? privateKeyRaw.replace(/\\n/g, '\n') : '';

  if (!jobId && !jobName) {
    throw new Error('missing_job_identifier: pass --job-id or --job-name');
  }

  await fs.mkdir(STATE_DIR, { recursive: true });
  const key = jobId || jobName.toLowerCase().replace(/[^a-z0-9_-]+/g, '_');
  const jsonPath = path.join(STATE_DIR, `${key}.json`);
  const mdPath = path.join(STATE_DIR, `${key}.md`);

  const context = { jobId: jobId || 'unknown', jobName: jobName || 'unknown' };

  const missingEnv = [];
  if (!spreadsheetId) missingEnv.push('GOOGLE_SHEETS_SPREADSHEET_ID');
  const hasServiceAccountCreds = Boolean(clientEmail && privateKey);

  if (missingEnv.length) {
    if (localOnly) {
      const fallback = await fs.readFile(jsonPath, 'utf8').then(JSON.parse).catch(() => null);
      if (fallback) {
        console.log(`sheet_config_status=cache (local-only)`);
        console.log(`sheet_config_version=${fallback.config_version || 'unknown'}`);
        console.log(`sheet_config_updated_at=${fallback.updated_at || 'unknown'}`);
        console.log(`runtime_instructions_md=${mdPath}`);
        console.log(`runtime_instructions_json=${jsonPath}`);
        return;
      }
      if (await fs.access(mdPath).then(() => true).catch(() => false)) {
        console.log('sheet_config_status=builtin_default (local-only)');
        console.log('sheet_config_version=v1-local');
        console.log('sheet_config_updated_at=unknown');
        console.log(`runtime_instructions_md=${mdPath}`);
        return;
      }
      throw new Error('local_only_no_runtime_instructions');
    }

    const fallback = await fs.readFile(jsonPath, 'utf8').then(JSON.parse).catch(() => null);
    if (fallback) {
      console.log(`sheet_config_fallback=cache reason=missing_env vars=${missingEnv.join(',')}`);
      console.log(`runtime_instructions_md=${mdPath}`);
      return;
    }
    throw new Error(`missing_env ${missingEnv.join(',')}`);
  }

  try {
    let token;
    let authMode;
    if (hasServiceAccountCreds) {
      token = await getAccessToken({ clientEmail, privateKey });
      authMode = 'service_account';
    } else {
      token = await getGcloudAccessToken();
      authMode = 'gcloud';
    }
    const url = `https://sheets.googleapis.com/v4/spreadsheets/${encodeURIComponent(spreadsheetId)}/values/${encodeURIComponent(range)}`;
    const resp = await fetch(url, { headers: { authorization: `Bearer ${token}` } });
    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`sheet_read_failed ${resp.status}: ${txt.slice(0, 300)}`);
    }
    const body = await resp.json();
    const values = body.values || [];
    if (!values.length) throw new Error('sheet_empty');

    const headers = values[0].map((h) => String(h || '').trim());
    const rows = values.slice(1).map((r) => normalizeRow(headers, r));
    const row = matchRow(rows, jobId, jobName);
    if (!row) throw new Error(`job_not_found_in_sheet job_id=${jobId} job_name=${jobName}`);

    const config = {
      ...row,
      enabled: String(parseBool(row.enabled)),
      fetched_at: new Date().toISOString(),
      source_range: range,
      source_spreadsheet_id: spreadsheetId,
    };

    await fs.writeFile(jsonPath, JSON.stringify(config, null, 2) + '\n', 'utf8');
    await fs.writeFile(mdPath, buildInstructionDoc(config, context) + '\n', 'utf8');

    console.log('sheet_config_status=fresh');
    console.log(`sheet_config_version=${config.config_version || 'unknown'}`);
    console.log(`sheet_config_updated_at=${config.updated_at || 'unknown'}`);
    console.log(`sheet_auth_mode=${authMode}`);
    console.log(`runtime_instructions_md=${mdPath}`);
    console.log(`runtime_instructions_json=${jsonPath}`);
  } catch (err) {
    if (localOnly) {
      const fallback = await fs.readFile(jsonPath, 'utf8').then(JSON.parse).catch(() => null);
      if (fallback) {
        console.log(`sheet_config_status=cache (local-only)`);
        console.log(`sheet_config_version=${fallback.config_version || 'unknown'}`);
        console.log(`runtime_instructions_md=${mdPath}`);
        return;
      }
      throw err;
    }

    const fallback = await fs.readFile(jsonPath, 'utf8').then(JSON.parse).catch(() => null);
    if (fallback) {
      console.log(`sheet_config_fallback=cache reason=${String(err.message || err)}`);
      console.log(`sheet_config_version=${fallback.config_version || 'unknown'}`);
      console.log(`runtime_instructions_md=${mdPath}`);
      return;
    }
    throw err;
  }
}

main().catch((err) => {
  console.error(`ERROR: ${String(err.message || err)}`);
  process.exit(1);
});
