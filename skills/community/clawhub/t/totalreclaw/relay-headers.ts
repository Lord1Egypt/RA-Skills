/**
 * Shared outbound-header helper for relay calls.
 *
 * Centralizes the common `X-TotalReclaw-*` headers so every fetch site
 * consistently tags requests with:
 *   - `X-TotalReclaw-Client`  — caller identity (defaults to `openclaw-plugin`).
 *   - `X-TotalReclaw-Session` — optional QA / observability tag from
 *     `TOTALRECLAW_SESSION_ID`. Used by Axiom log filters and the
 *     `qa-totalreclaw` skill to scope log searches per QA run.
 *
 * Pure function — no I/O, no network. Reads `getSessionId()` (which reads the
 * env var via getter so harnesses that flip the env between calls pick up
 * the new value).
 *
 * The session-id env var was accidentally placed in the v1 REMOVED_ENV_VARS
 * list and silently warned-and-dropped, breaking Axiom traceability for QA
 * runs (see internal#127). This helper is the canonical re-entry point for
 * the variable.
 */

import { getSessionId } from './config.js';

/** Default `X-TotalReclaw-Client` value. */
export const DEFAULT_CLIENT_ID = 'openclaw-plugin';

/**
 * Build the standard outbound header set.
 *
 * @param overrides - merge-in additional headers (`Authorization`,
 *   `Content-Type`, etc.); these win over the defaults.
 * @param clientId - override the `X-TotalReclaw-Client` value.
 *
 * Always includes `X-TotalReclaw-Client`. Includes `X-TotalReclaw-Session`
 * only when `TOTALRECLAW_SESSION_ID` is set + non-empty.
 */
export function buildRelayHeaders(
  overrides: Record<string, string> = {},
  clientId: string = DEFAULT_CLIENT_ID,
): Record<string, string> {
  const headers: Record<string, string> = {
    'X-TotalReclaw-Client': clientId,
  };
  const sessionId = getSessionId();
  if (sessionId) {
    headers['X-TotalReclaw-Session'] = sessionId;
  }
  // Caller-supplied headers (Authorization, Content-Type, Accept, etc.) take
  // precedence over the defaults but should generally not stomp the X-* tags.
  return { ...headers, ...overrides };
}
