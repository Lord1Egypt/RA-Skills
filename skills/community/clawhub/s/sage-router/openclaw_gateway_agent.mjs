import { randomUUID } from 'node:crypto';
import { loadOpenClawGatewaySdk } from './openclaw_sdk_resolver.mjs';

let callGateway, clientName, clientMode;
try {
  const sdk = await loadOpenClawGatewaySdk();
  callGateway = sdk.callGateway;
  clientName = sdk.clientName;
  clientMode = sdk.clientMode;
} catch (error) {
  console.error('Cannot load OpenClaw SDK. Ensure openclaw is installed globally.', error instanceof Error ? error.message : String(error));
  process.exit(1);
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

function extractText(result) {
  const payloads = result?.result?.payloads;
  if (!Array.isArray(payloads)) return '';
  return payloads
    .map((payload) => typeof payload?.text === 'string' ? payload.text : '')
    .filter(Boolean)
    .join('\n\n');
}

const raw = await readStdin();
const input = raw.trim() ? JSON.parse(raw) : {};

function buildRequest({ includeOverrides }) {
  const params = {
    agentId: input.agentId || 'main',
    message: input.message || '',
    idempotencyKey: randomUUID(),
  };
  if (includeOverrides && input.provider) params.provider = input.provider;
  if (includeOverrides && input.model) params.model = input.model;
  return {
    method: 'agent',
    params,
    expectFinal: true,
    timeoutMs: Number(input.timeoutMs) || 120000,
    clientName,
    mode: clientMode,
    ...(process.env.OPENCLAW_GATEWAY_TOKEN ? { token: process.env.OPENCLAW_GATEWAY_TOKEN } : {}),
  };
}

async function runRequest(includeOverrides) {
  const result = await callGateway(buildRequest({ includeOverrides }));
  console.log(JSON.stringify({
    ok: true,
    text: extractText(result),
    provider: result?.result?.meta?.agentMeta?.provider,
    model: result?.result?.meta?.agentMeta?.model,
    usedOverrides: includeOverrides,
  }));
}

const allowOverrides = process.env.SAGE_ROUTER_OPENCLAW_ALLOW_MODEL_OVERRIDE === '1';

try {
  await runRequest(allowOverrides);
  process.exit(0);
} catch (error) {
  const message = error instanceof Error ? error.stack || error.message : String(error);
  const shouldRetryWithoutOverrides = allowOverrides && /sessions\.patch|gateway request timeout|model set failed/i.test(message);
  if (shouldRetryWithoutOverrides) {
    try {
      await runRequest(false);
      process.exit(0);
    } catch (retryError) {
      console.error(retryError instanceof Error ? retryError.stack || retryError.message : String(retryError));
      process.exit(1);
    }
  }
  console.error(message);
  process.exit(1);
}
