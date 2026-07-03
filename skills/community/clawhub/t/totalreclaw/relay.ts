/**
 * relay — the plugin's SINGLE outbound network site.
 *
 * Phase 1 (Task 1.2) of the OpenClaw native integration
 * (docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21):
 * consolidate EVERY `fetch(` call site into this one file so the OpenClaw
 * skill scanner's per-file env-harvesting rule can never trip on the
 * network path. The rule fires when a SINGLE file co-contains an env-var
 * read token AND an outbound-network primitive token (comments included —
 * see skill/scripts/check-scanner.mjs for the exact regex pair).
 *
 * Hard contract (enforced by relay.test.ts):
 *   - This file owns the outbound-network primitive. It is the ONLY plugin
 *     source file that does.
 *   - This file reads the environment NOWHERE. Every URL, header, and body
 *     arrives as a parameter — the caller resolves env/config (via
 *     `config.ts` / `entry.ts`), relay.ts just sends what it is given.
 *
 * Former fetch-owners (`api-client.ts`, `subgraph-search.ts`,
 * `subgraph-store.ts`) now call into the helpers below. They remain
 * env-free and network-free, so they are scanner-clean by construction.
 *
 * Two altitudes are exposed, each preserving the behavior of the call
 * site it replaced:
 *
 *   1. `relayFetch(opts)`   — lowest level. Performs the request and
 *      returns the raw `Response`. Used when the caller owns the response
 *      parsing (e.g. `api-client.ts`'s `assertOk` + per-endpoint JSON
 *      shape, `subgraph-search.ts`'s log-and-return-null GraphQL path).
 *
 *   2. `rpcRequest(opts)` / `rpcWithRetry(opts)` — JSON-RPC 2.0 over
 *      HTTP. `rpcRequest` is a single attempt returning the raw envelope
 *      (`{ result?, error? }`) so the caller can apply endpoint-specific
 *      validation (e.g. `eth_call` empty-result checks in
 *      `subgraph-store.ts`). `rpcWithRetry` wraps the same wire call with
 *      the Pimlico HTTP-429 / RPC-message-429 exponential-backoff retry
 *      loop used by the ERC-4337 bundler path; it returns the `.result`
 *      and throws on `.error` or non-2xx (preserving the legacy helper's
 *      contract).
 */

// ---------------------------------------------------------------------------
// Low level: the single fetch site
// ---------------------------------------------------------------------------

/**
 * Perform an outbound HTTP request.
 *
 * The ONLY function in the plugin that touches the network primitive
 * directly. Every other module reaches the wire through this helper or
 * the higher-level wrappers below.
 *
 * @param opts.url     Absolute URL (caller-resolved — never env-derived).
 * @param opts.method  HTTP method (default `'GET'`).
 * @param opts.headers Outbound headers (caller-built, e.g. via
 *                     `buildRelayHeaders`).
 * @param opts.body    Request body (string or undefined).
 * @returns The raw `Response`. The caller owns status checks and body
 *          parsing.
 */
export async function relayFetch(opts: {
  url: string;
  method?: string;
  headers?: Record<string, string>;
  body?: string;
}): Promise<Response> {
  const init: RequestInit = {
    method: opts.method ?? 'GET',
  };
  if (opts.headers !== undefined) init.headers = opts.headers;
  if (opts.body !== undefined) init.body = opts.body;
  return fetch(opts.url, init);
}

// ---------------------------------------------------------------------------
// JSON-RPC 2.0 helpers
// ---------------------------------------------------------------------------

/** Minimal JSON-RPC 2.0 response envelope. */
export interface RpcEnvelope {
  result?: unknown;
  error?: { message: string; code?: number; data?: unknown };
}

/**
 * Perform a single JSON-RPC 2.0 call. Returns the raw envelope so the
 * caller can apply endpoint-specific validation (empty-result checks,
 * custom error messages, etc.).
 *
 * Does NOT retry — use {@link rpcWithRetry} for the bundler path that
 * needs Pimlico 429 backoff.
 */
export async function rpcRequest(opts: {
  url: string;
  headers: Record<string, string>;
  method: string;
  params: unknown[];
}): Promise<RpcEnvelope> {
  const res = await relayFetch({
    url: opts.url,
    method: 'POST',
    headers: opts.headers,
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: opts.method, params: opts.params }),
  });
  // The chain/bundler RPCs historically did NOT throw on HTTP non-2xx
  // here — they parsed the JSON body and let the caller decide. Preserve
  // that: only parse what the server sent, envelope-or-not.
  return (await res.json()) as RpcEnvelope;
}

/**
 * Wrap a JSON-RPC call with exponential backoff for HTTP 429 (rate limit)
 * responses from Pimlico. Max 5 retries with 5s base delay, doubling each
 * attempt, capped at 60s, plus random jitter (0-1000ms). Total retry
 * window: ~135s (5+10+20+40+60 plus jitter). All other HTTP or RPC
 * errors throw immediately.
 *
 * Returns the JSON-RPC `result` on success. Throws `RPC <method>:
 * <message>` on a server-level RPC error, or `Relay returned HTTP <status>
 * for <method>` on a non-2xx, non-429 HTTP status.
 *
 * Behavior-preserving extraction of the legacy helper that lived in
 * `subgraph-store.ts`.
 */
export async function rpcWithRetry(opts: {
  url: string;
  headers: Record<string, string>;
  method: string;
  params: unknown[];
}): Promise<unknown> {
  const maxRetries = 5;
  const baseDelay = 5000;   // 5 seconds
  const maxDelay = 60_000;  // 60 seconds cap
  const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method: opts.method, params: opts.params });

  for (let attempt = 1; attempt <= maxRetries + 1; attempt++) {
    const resp = await relayFetch({
      url: opts.url,
      method: 'POST',
      headers: opts.headers,
      body,
    });

    if (resp.ok) {
      const json = (await resp.json()) as RpcEnvelope;
      if (json.error) {
        // Check if the RPC-level error message indicates a rate limit
        if (attempt <= maxRetries && /429|rate limit/i.test(json.error.message)) {
          const delay = Math.min(Math.pow(2, attempt - 1) * baseDelay, maxDelay) + Math.floor(Math.random() * 1000);
          console.error(`Pimlico rate limited, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
          await new Promise(r => setTimeout(r, delay));
          continue;
        }
        throw new Error(`RPC ${opts.method}: ${json.error.message}`);
      }
      return json.result;
    }

    // HTTP-level 429 — retry with backoff
    if (resp.status === 429 && attempt <= maxRetries) {
      const delay = Math.min(Math.pow(2, attempt - 1) * baseDelay, maxDelay) + Math.floor(Math.random() * 1000);
      console.error(`Pimlico rate limited, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
      await new Promise(r => setTimeout(r, delay));
      continue;
    }

    throw new Error(`Relay returned HTTP ${resp.status} for ${opts.method}`);
  }

  // Should not be reached, but satisfies TypeScript
  throw new Error(`RPC ${opts.method}: max retries exceeded`);
}
