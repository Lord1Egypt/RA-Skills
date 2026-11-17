// Data flow: sends chat messages (and optional Basic auth) to the configured Theta-managed dedicated
// endpoint (*.thetaedgecloud.com / *.onthetaedgecloud.com HTTPS only). *.onthetaedgecloud.com is a
// shared Theta domain that also hosts other customers' deployments, so configure your own endpoint.
// max_tokens is clamped to 1..5000 per call.
import { ThetaConfig } from '../config.js';
import { BasicAuth } from '../types.js';
import { getJson, postJson } from './http.js';
import { thetaUrl } from '../security.js';
import { assertLive, boundChatParams, findCallbackFields, snapshotBody } from '../approval.js';

const ALLOWED_INFERENCE_DOMAIN_SUFFIXES = ['.thetaedgecloud.com', '.onthetaedgecloud.com'];

function isLoopbackOrPrivateHost(hostname: string): boolean {
  const host = hostname.toLowerCase();
  if (host === 'localhost' || host === '::1' || host === '0.0.0.0' || host === '::ffff:127.0.0.1') return true;

  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(host)) {
    const parts = host.split('.').map((p) => Number.parseInt(p, 10));
    if (parts.some((p) => !Number.isInteger(p) || p < 0 || p > 255)) return true;
    if (parts[0] === 10 || parts[0] === 127) return true;
    if (parts[0] === 169 && parts[1] === 254) return true;
    if (parts[0] === 192 && parts[1] === 168) return true;
    if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
  }

  return host.startsWith('fe80:') || host.startsWith('fc') || host.startsWith('fd');
}

function parseEndpoint(raw: string, label: string): URL {
  try {
    const parsed = new URL(raw.trim());
    if (parsed.protocol !== 'https:') throw new Error(`${label} must use https://`);
    if (parsed.username || parsed.password) throw new Error(`${label} must not include embedded credentials`);
    if (!parsed.hostname || isLoopbackOrPrivateHost(parsed.hostname)) {
      throw new Error(`${label} host is unsafe (private/loopback not allowed)`);
    }
    return parsed;
  } catch (error) {
    if (error instanceof Error && error.message.includes(label)) throw error;
    throw new Error(`${label} must be an absolute https URL`);
  }
}

function isAllowedHost(hostname: string): boolean {
  const host = hostname.toLowerCase();
  if (['controller.thetaedgecloud.com', 'ondemand.thetaedgecloud.com', 'api.thetaedgecloud.com', 'ai-chars-api.thetaedgecloud.com'].includes(host)) return false;
  return ALLOWED_INFERENCE_DOMAIN_SUFFIXES.some((suffix) => host.endsWith(suffix));
}

function endpoint(cfg: ThetaConfig, e?: string): string {
  const v = e ?? cfg.inferenceEndpoint;
  if (!v) throw new Error('THETA_INFERENCE_ENDPOINT missing');
  const parsed = parseEndpoint(thetaUrl(v, 'dedicated'), 'THETA_INFERENCE_ENDPOINT');
  if (!isAllowedHost(parsed.hostname)) {
    throw new Error('THETA_INFERENCE_ENDPOINT host is not allowed; use a Theta EdgeCloud endpoint');
  }
  return parsed.href.replace(/\/$/, '');
}

function auth(cfg: ThetaConfig, e?: string, a?: BasicAuth): BasicAuth | undefined {
  if (a) return a;
  if (e && (!cfg.inferenceEndpoint || new URL(e.trim()).origin !== new URL(cfg.inferenceEndpoint.trim()).origin)) return undefined;
  return cfg.inferenceAuth;
}

function net(cfg: ThetaConfig, service: string, authOverride?: BasicAuth) {
  return {
    service,
    auth: authOverride,
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

export const edgecloudInferenceClient = {
  listModels: (cfg: ThetaConfig, e?: string, a?: BasicAuth) =>
    getJson(`${endpoint(cfg, e)}/v1/models`, net(cfg, 'edgecloud-inference', auth(cfg, e, a))),

  gradioConfig: (cfg: ThetaConfig, e?: string, a?: BasicAuth) =>
    getJson(`${endpoint(cfg, e)}/config`, net(cfg, 'edgecloud-inference', auth(cfg, e, a))),

  chat: (cfg: ThetaConfig, body: { model: string; messages: Array<{ role: string; content: string }>; max_tokens?: number }, e?: string, a?: BasicAuth) => {
    assertLive(cfg, 'Dedicated inference chat');
    // Snapshot first (runs any getter/toJSON once), then validate and bound the plain copy; only
    // that copy is serialized and sent.
    const finalBody = boundChatParams(snapshotBody(body));
    if (!Array.isArray(finalBody.messages) || finalBody.messages.length === 0) {
      throw new Error('body must be an object with a non-empty messages array');
    }
    const hooks = findCallbackFields(finalBody);
    if (hooks.length) throw new Error(`Dedicated chat does not support webhook/callback fields (${hooks.map((h) => h.path).join(', ')})`);
    return postJson(`${endpoint(cfg, e)}/v1/chat/completions`, finalBody, net(cfg, 'edgecloud-inference', auth(cfg, e, a)));
  }
};
