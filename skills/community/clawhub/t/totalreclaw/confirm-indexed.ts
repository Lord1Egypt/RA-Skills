/**
 * Read-after-write primitive — confirm a fact id has been indexed by the
 * subgraph after an on-chain mutation (retype / set_scope / pin / unpin /
 * forget).
 *
 * Wraps the pure-compute halves exported by `@totalreclaw/core`
 * (`wasmConfirmIndexedQuery`, `wasmConfirmIndexedParse`) in a host-side
 * polling loop. Subgraph indexer lag on Gnosis production runs 5-30s; this
 * helper polls every `pollIntervalMs` (default 1000ms) up to `timeoutMs`
 * (default 30000ms).
 *
 * Why this exists
 * ---------------
 * Pre-fix, mutation tools returned `{success: true}` based on the bundler
 * ack alone. A user who immediately ran `totalreclaw_export` would see the
 * pre-mutation state, because the subgraph indexer hadn't yet observed the
 * L1 inclusion. Confusing UX, root cause of rc.18 finding #117.
 *
 * Post-fix, mutation tools call `confirmIndexed(newFactId)` after submitting
 * the batched UserOp; on success they return normally, on timeout they
 * return `{success: true, partial: true, ...}` with the chain write
 * acknowledged but the indexer-level confirmation withheld.
 *
 * Mnemonic isolation: this helper never touches the mnemonic, encryption
 * key, or any decrypted blob. Only reads the public {id, isActive,
 * blockNumber} of a fact.
 */

import { createRequire } from 'node:module';
import { getSubgraphConfig } from './subgraph-store.js';
import { buildRelayHeaders } from './relay-headers.js';

/**
 * The four `wasmConfirmIndexed*` exports below ship in `@totalreclaw/core@2.3.x`
 * (the `confirm` module added in 2.2.x). Older type declarations don't list
 * them — we use a structural cast so the plugin's `--noCheck` build is
 * unblocked and runtime resolution is via dynamic require.
 */
type ConfirmIndexedCore = typeof import('@totalreclaw/core') & {
  wasmConfirmIndexedQuery(): string;
  wasmConfirmIndexedParse(responseJson: string): boolean;
  wasmConfirmIndexedDefaultPollMs(): number;
  wasmConfirmIndexedDefaultTimeoutMs(): number;
};

const requireWasm = createRequire(import.meta.url);
let _wasm: ConfirmIndexedCore | null = null;
function getWasm(): ConfirmIndexedCore {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core') as unknown as ConfirmIndexedCore;
  return _wasm!;
}

/** Result of a confirm-indexed poll loop. */
export interface ConfirmIndexedResult {
  /** True if the fact was found and `isActive == true` before the timeout. */
  indexed: boolean;
  /** Number of poll attempts before resolution (or timeout). */
  attempts: number;
  /** Total wall-clock ms spent polling. */
  elapsedMs: number;
  /** Last error message from the GraphQL adapter, if any. */
  lastError?: string;
}

export interface ConfirmIndexedOptions {
  /** Override the default 1s poll interval. */
  pollIntervalMs?: number;
  /** Override the default 30s total timeout. */
  timeoutMs?: number;
  /** Override `${relayUrl}/v1/subgraph` (test injection point). */
  subgraphUrl?: string;
  /** Override the auth-key-hex header (defaults to none). */
  authKeyHex?: string;
  /**
   * Direction of the read-after-write check.
   *   - `"active"` (default) — wait until fact is found AND `isActive == true`.
   *     Use after pin/unpin/retype/set_scope (we're confirming the *new* fact
   *     id has appeared).
   *   - `"inactive"` — wait until fact either disappears OR `isActive ==
   *     false`. Use after `forget`, where the *original* fact id is being
   *     tombstoned and a confirm-indexed wait should resolve once the
   *     subgraph has flipped it.
   */
  expect?: 'active' | 'inactive';
  /**
   * Test injection — caller-provided `fetch`-compatible POST. Defaults to
   * the global `fetch`. Letting tests stub this out avoids a network mock
   * dependency.
   */
  poster?: (url: string, body: string, headers: Record<string, string>) => Promise<{
    ok: boolean;
    status: number;
    text: () => Promise<string>;
  }>;
}

/**
 * Poll the subgraph until the new fact id is indexed-and-active, or the
 * timeout elapses. Returns a result object describing the outcome — never
 * throws on indexer-level transient errors; the caller decides whether to
 * surface a `partial: true` flag based on `result.indexed`.
 *
 * The host's submitBatch already returned a tx hash before this is called,
 * so on `indexed: false` the on-chain write is still acknowledged — just not
 * yet visible in the read API.
 */
export async function confirmIndexed(
  factId: string,
  options: ConfirmIndexedOptions = {},
): Promise<ConfirmIndexedResult> {
  // WASM bindings may be unavailable (e.g. core@<2.3.0 not yet published).
  // In that case the chain write has still succeeded — confirm step is
  // observational only. Return `indexed: false` so callers surface
  // `partial: true` rather than fail the whole tool invocation.
  let wasm: ConfirmIndexedCore;
  let query: string;
  let pollIntervalMs: number;
  let timeoutMs: number;
  try {
    wasm = getWasm();
    pollIntervalMs = options.pollIntervalMs ?? Number(wasm.wasmConfirmIndexedDefaultPollMs?.() ?? 1000);
    timeoutMs = options.timeoutMs ?? Number(wasm.wasmConfirmIndexedDefaultTimeoutMs?.() ?? 30000);
    query = wasm.wasmConfirmIndexedQuery();
  } catch (err) {
    return {
      indexed: false,
      attempts: 0,
      elapsedMs: 0,
      lastError: `confirm-indexed wasm bindings unavailable: ${err instanceof Error ? err.message : String(err)}`,
    };
  }
  const subgraphUrl =
    options.subgraphUrl ?? `${getSubgraphConfig().relayUrl}/v1/subgraph`;

  const overrides: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (options.authKeyHex) overrides['Authorization'] = `Bearer ${options.authKeyHex}`;
  const headers = buildRelayHeaders(overrides);

  const body = JSON.stringify({ query, variables: { id: factId } });

  const poster =
    options.poster ??
    (async (url, b, h) => {
      const r = await fetch(url, { method: 'POST', headers: h, body: b });
      return { ok: r.ok, status: r.status, text: () => r.text() };
    });

  const expect = options.expect ?? 'active';
  const start = Date.now();
  let attempts = 0;
  let lastError: string | undefined;

  while (Date.now() - start < timeoutMs) {
    attempts++;
    try {
      const r = await poster(subgraphUrl, body, headers);
      if (r.ok) {
        const txt = await r.text();
        try {
          // wasmConfirmIndexedParse returns `true` when fact is present AND
          // isActive==true. For `expect: 'inactive'` we invert: a `false`
          // (fact missing OR present-but-inactive) is the resolution signal.
          const isActive = wasm.wasmConfirmIndexedParse(txt);
          const resolved = expect === 'active' ? isActive : !isActive;
          if (resolved) {
            return { indexed: true, attempts, elapsedMs: Date.now() - start };
          }
        } catch (parseErr) {
          lastError = parseErr instanceof Error ? parseErr.message : String(parseErr);
        }
      } else {
        lastError = `HTTP ${r.status}`;
      }
    } catch (err) {
      lastError = err instanceof Error ? err.message : String(err);
    }
    // Sleep before the next attempt — but only if there's still budget.
    const remaining = timeoutMs - (Date.now() - start);
    if (remaining <= 0) break;
    await new Promise((res) => setTimeout(res, Math.min(pollIntervalMs, remaining)));
  }

  return {
    indexed: false,
    attempts,
    elapsedMs: Date.now() - start,
    lastError,
  };
}
