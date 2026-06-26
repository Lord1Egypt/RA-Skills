/**
 * Shared REST API helpers for all skill scripts.
 * Hardcoded to staging — do not allow env override (security: prevents API URL redirection).
 */

const BASE = 'https://api.staging.rhaios.com';
export const HEALTH_URL = `${BASE}/health`;
export const DETECTED_ENV = 'staging' as const;

/** Map tool names to their REST API endpoints and HTTP methods */
const TOOL_ROUTES: Record<string, { method: 'GET' | 'POST'; path: string }> = {
  yield_discover:    { method: 'POST', path: '/v1/yield/discover' },
  yield_prepare:     { method: 'POST', path: '/v1/yield/prepare' },
  yield_execute:     { method: 'POST', path: '/v1/yield/execute' },
  yield_status:      { method: 'GET',  path: '/v1/yield/status' },
  yield_history:     { method: 'GET',  path: '/v1/yield/history' },
  yield_setup_relay: { method: 'POST', path: '/v1/yield/setup-relay' },
};

export async function callApi(
  name: string,
  args: Record<string, unknown>,
  /** Timeout in ms — long-running tools (setup relay) need more than default */
  timeoutMs = 120_000,
): Promise<{ payload: Record<string, unknown>; isError: boolean }> {
  const route = TOOL_ROUTES[name];
  if (!route) {
    throw new Error(`Unknown API tool '${name}'. Available: ${Object.keys(TOOL_ROUTES).join(', ')}`);
  }

  let url: string;
  const headers: Record<string, string> = {
    'Accept': 'application/json',
  };

  if (route.method === 'GET') {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(args)) {
      if (value !== undefined && value !== null) {
        params.set(key, String(value));
      }
    }
    const qs = params.toString();
    url = `${BASE}${route.path}${qs ? `?${qs}` : ''}`;
  } else {
    url = `${BASE}${route.path}`;
    headers['Content-Type'] = 'application/json';
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  let res: Response;
  try {
    res = await fetch(url, {
      method: route.method,
      headers,
      ...(route.method === 'POST' ? { body: JSON.stringify(args) } : {}),
      signal: controller.signal,
    });
  } catch (err: unknown) {
    clearTimeout(timer);
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new Error(`API call '${name}' timed out after ${timeoutMs}ms`);
    }
    throw err;
  }
  clearTimeout(timer);

  const raw = await res.text();
  let payload: Record<string, unknown>;
  try {
    payload = JSON.parse(raw);
  } catch {
    throw new Error(`API returned non-JSON for '${name}' (HTTP ${res.status}): ${raw.slice(0, 500)}`);
  }

  if (!res.ok) {
    if (res.status === 402) {
      throw new Error('x402: payment required — this endpoint is paid on this server');
    }
    return { payload, isError: true };
  }

  return { payload, isError: false };
}
