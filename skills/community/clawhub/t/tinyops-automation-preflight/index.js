'use strict';

const fs = require('node:fs');
const path = require('node:path');

const DEFAULT_API_BASE = 'https://automation-integration-preflight.p.rapidapi.com';
const RAPIDAPI_HOST = 'automation-integration-preflight.p.rapidapi.com';

function input(name, fallback = '') {
  const key = `INPUT_${name.toUpperCase()}`;
  const value = process.env[key];
  return typeof value === 'string' && value.trim() ? value.trim() : fallback;
}

function workflowEscape(value) {
  return String(value).replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');
}

function redact(value, secrets) {
  let result = String(value);
  for (const secret of secrets.filter(Boolean)) result = result.split(secret).join('[redacted]');
  return result;
}

function validateTarget(raw) {
  let target;
  try {
    target = new URL(raw);
  } catch {
    throw new Error('url must be a valid public HTTP or HTTPS URL');
  }
  if (!['http:', 'https:'].includes(target.protocol)) {
    throw new Error('url must use HTTP or HTTPS');
  }
  if (raw.length > 2048) throw new Error('url exceeds 2048 characters');
  return target.toString();
}

function resolveOutputPath(raw) {
  const workspace = path.resolve(process.env.GITHUB_WORKSPACE || process.cwd());
  const outputPath = path.resolve(workspace, raw || 'automation-preflight-report.json');
  if (outputPath !== workspace && !outputPath.startsWith(`${workspace}${path.sep}`)) {
    throw new Error('output-file must stay inside the GitHub workspace');
  }
  return outputPath;
}

function appendOutput(name, value) {
  const outputFile = process.env.GITHUB_OUTPUT;
  if (outputFile) fs.appendFileSync(outputFile, `${name}=${String(value)}\n`, 'utf8');
}

function readinessLabel(payload) {
  if (typeof payload?.readiness === 'string') return payload.readiness;
  for (const key of ['status', 'label', 'level', 'decision']) {
    if (typeof payload?.readiness?.[key] === 'string') return payload.readiness[key];
  }
  return '';
}

async function requestPreflight({
  rapidApiKey,
  url,
  mode = 'analyze',
  objective = '',
  apiBase = DEFAULT_API_BASE,
  userAgent = 'tinyops-automation-preflight/1.1',
}) {
  if (!rapidApiKey) throw new Error('rapidapi-key is required');
  const target = validateTarget(url);
  const normalizedMode = String(mode).toLowerCase();
  if (!['analyze', 'acceptance-pack'].includes(normalizedMode)) {
    throw new Error('mode must be analyze or acceptance-pack');
  }
  if (objective.length > 500) throw new Error('objective exceeds 500 characters');
  const endpoint = '/rapidapi/analyze';
  const body = {
    url: target,
    ...(normalizedMode === 'acceptance-pack' ? { mode: normalizedMode } : {}),
    ...(objective ? { objective } : {}),
  };

  const response = await fetch(`${apiBase}${endpoint}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-rapidapi-key': rapidApiKey,
      'x-rapidapi-host': RAPIDAPI_HOST,
      'user-agent': userAgent,
    },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(45_000),
  });
  const responseText = await response.text();
  let payload;
  try {
    payload = JSON.parse(responseText);
  } catch {
    payload = { error: 'service returned a non-JSON response' };
  }
  if (!response.ok) {
    const safeDetail = redact(responseText.slice(0, 500), [rapidApiKey]);
    throw new Error(`service returned HTTP ${response.status}: ${safeDetail}`);
  }

  return { payload, status: response.status, target, mode: normalizedMode };
}

async function runAction() {
  const rapidApiKey = input('rapidapi-key');
  console.log(`::add-mask::${workflowEscape(rapidApiKey)}`);
  const outputPath = resolveOutputPath(input('output-file', 'automation-preflight-report.json'));
  const result = await requestPreflight({
    rapidApiKey,
    url: input('url'),
    mode: input('mode', 'analyze'),
    objective: input('objective'),
    apiBase: process.env.AUTOMATION_PREFLIGHT_API_BASE_URL || DEFAULT_API_BASE,
    userAgent: 'tinyops-automation-preflight-action/1.1',
  });
  const { payload, status, target, mode } = result;

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
  const readiness = readinessLabel(payload);
  appendOutput('readiness', readiness);
  appendOutput('report-file', outputPath);
  appendOutput('http-status', status);

  if (process.env.GITHUB_STEP_SUMMARY) {
    const safeTarget = target.replace(/\|/g, '\\|');
    fs.appendFileSync(
      process.env.GITHUB_STEP_SUMMARY,
      `## Automation integration preflight\n\n| Field | Result |\n| --- | --- |\n| Target | ${safeTarget} |\n| Mode | ${mode} |\n| HTTP status | ${status} |\n| Readiness | ${readiness || 'See JSON report'} |\n| Report | \`${path.basename(outputPath)}\` |\n`,
      'utf8',
    );
  }
  console.log(`::notice title=Automation preflight complete::Report saved to ${workflowEscape(path.basename(outputPath))}`);
}

if (require.main === module) {
  runAction().catch((error) => {
    const rapidApiKey = input('rapidapi-key');
    const safeMessage = redact(error?.message || error, [rapidApiKey]).slice(0, 1000);
    console.error(`::error title=Automation preflight failed::${workflowEscape(safeMessage)}`);
    if (input('fail-on-error', 'true').toLowerCase() !== 'false') process.exitCode = 1;
  });
}

module.exports = { readinessLabel, redact, requestPreflight, validateTarget };
