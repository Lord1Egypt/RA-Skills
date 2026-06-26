/**
 * TotalReclaw Plugin - HTTP API Client
 *
 * Communicates with the TotalReclaw server over JSON/HTTP. Uses Node.js
 * built-in `fetch` (available since Node 18).
 *
 * All authenticated endpoints expect:
 *   Authorization: Bearer <hex-encoded-auth-key>
 *
 * The server hashes the auth key with SHA-256 to look up the user.
 *
 * Every outbound request goes through `buildRelayHeaders()` so the
 * `X-TotalReclaw-Client` tag is set + the optional QA-tracing
 * `X-TotalReclaw-Session` tag is forwarded when `TOTALRECLAW_SESSION_ID`
 * is set. See `relay-headers.ts` and internal#127.
 */
import { buildRelayHeaders } from './relay-headers.js';
// ---------------------------------------------------------------------------
// API Client Factory
// ---------------------------------------------------------------------------
/**
 * Create an API client bound to a specific TotalReclaw server URL.
 *
 * All methods are async and throw descriptive errors on non-2xx responses.
 */
export function createApiClient(serverUrl) {
    // Normalise URL -- strip trailing slash.
    const baseUrl = serverUrl.replace(/\/+$/, '');
    // ------------------------------------------------------------------
    // Shared helpers
    // ------------------------------------------------------------------
    /**
     * Throw a descriptive error when the server returns a non-2xx status.
     */
    async function assertOk(res, context) {
        if (res.ok)
            return;
        let body;
        try {
            body = await res.text();
        }
        catch {
            body = '(could not read response body)';
        }
        const hint = res.status === 401
            ? ' Authentication failed. If using a recovery phrase, check that all 12 words are in the correct order and spelled correctly.'
            : '';
        throw new Error(`${context}: HTTP ${res.status} - ${body}${hint}`);
    }
    // ------------------------------------------------------------------
    // Public methods
    // ------------------------------------------------------------------
    return {
        // ---- Registration (unauthenticated) ----
        /**
         * Register a new user.
         *
         * @param authKeyHash  Hex-encoded SHA-256 of the auth key (64 chars).
         * @param saltHex      Hex-encoded 32-byte salt (64 chars).
         * @returns `{ user_id }` on success.
         */
        async register(authKeyHash, saltHex) {
            const res = await fetch(`${baseUrl}/v1/register`, {
                method: 'POST',
                headers: buildRelayHeaders({ 'Content-Type': 'application/json' }),
                body: JSON.stringify({ auth_key_hash: authKeyHash, salt: saltHex }),
            });
            await assertOk(res, 'register');
            const json = (await res.json());
            if (!json.success && json.error_code !== 'USER_EXISTS') {
                throw new Error(`register: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
            if (!json.user_id) {
                throw new Error(`register: server did not return user_id (error_code=${json.error_code})`);
            }
            return { user_id: json.user_id };
        },
        // ---- Store (authenticated) ----
        /**
         * Store one or more encrypted facts.
         *
         * @param userId       The authenticated user's ID.
         * @param facts        Array of `StoreFactPayload` objects.
         * @param authKeyHex   Hex-encoded raw auth key (64 chars) for Bearer header.
         */
        async store(userId, facts, authKeyHex) {
            const res = await fetch(`${baseUrl}/v1/store`, {
                method: 'POST',
                headers: buildRelayHeaders({
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${authKeyHex}`,
                }),
                body: JSON.stringify({ user_id: userId, facts }),
            });
            await assertOk(res, 'store');
            const json = (await res.json());
            if (!json.success) {
                throw new Error(`store: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
            return {
                ids: json.ids ?? [],
                duplicate_ids: json.duplicate_ids,
            };
        },
        // ---- Search (authenticated) ----
        /**
         * Search for facts using blind trapdoors.
         *
         * @param userId         The authenticated user's ID.
         * @param trapdoors      SHA-256 hex hashes of query tokens.
         * @param maxCandidates  Maximum candidates to retrieve.
         * @param authKeyHex     Hex-encoded raw auth key for Bearer header.
         * @returns Array of encrypted search candidates.
         */
        async search(userId, trapdoors, maxCandidates, authKeyHex) {
            const res = await fetch(`${baseUrl}/v1/search`, {
                method: 'POST',
                headers: buildRelayHeaders({
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${authKeyHex}`,
                }),
                body: JSON.stringify({
                    user_id: userId,
                    trapdoors,
                    max_candidates: maxCandidates,
                }),
            });
            await assertOk(res, 'search');
            const json = (await res.json());
            if (!json.success) {
                throw new Error(`search: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
            return json.results ?? [];
        },
        // ---- Delete (authenticated) ----
        /**
         * Soft-delete a fact by ID.
         *
         * @param factId      The fact UUID to delete.
         * @param authKeyHex  Hex-encoded raw auth key for Bearer header.
         */
        async deleteFact(factId, authKeyHex) {
            const res = await fetch(`${baseUrl}/v1/facts/${encodeURIComponent(factId)}`, {
                method: 'DELETE',
                headers: buildRelayHeaders({
                    Authorization: `Bearer ${authKeyHex}`,
                }),
            });
            await assertOk(res, 'deleteFact');
            const json = (await res.json());
            if (!json.success) {
                throw new Error(`deleteFact: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
        },
        // ---- Batch Delete (authenticated) ----
        /**
         * Batch soft-delete facts by ID list.
         *
         * @param factIds     Array of fact UUIDs to delete (max 500).
         * @param authKeyHex  Hex-encoded raw auth key for Bearer header.
         * @returns The number of facts that were actually deleted.
         */
        async batchDelete(factIds, authKeyHex) {
            const res = await fetch(`${baseUrl}/v1/facts/batch-delete`, {
                method: 'POST',
                headers: buildRelayHeaders({
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${authKeyHex}`,
                }),
                body: JSON.stringify({ fact_ids: factIds }),
            });
            await assertOk(res, 'batchDelete');
            const json = (await res.json());
            if (!json.success) {
                throw new Error(`batchDelete: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
            return json.deleted_count ?? 0;
        },
        // ---- Export (authenticated) ----
        /**
         * Export all active facts (paginated).
         *
         * @param authKeyHex  Hex-encoded raw auth key for Bearer header.
         * @param limit       Page size (default 1000, max 5000).
         * @param cursor      Cursor from previous page (omit for first page).
         * @returns Page of facts with pagination metadata.
         */
        async exportFacts(authKeyHex, limit = 1000, cursor) {
            const params = new URLSearchParams({ limit: String(limit) });
            if (cursor)
                params.set('cursor', cursor);
            const res = await fetch(`${baseUrl}/v1/export?${params.toString()}`, {
                method: 'GET',
                headers: buildRelayHeaders({
                    Authorization: `Bearer ${authKeyHex}`,
                }),
            });
            await assertOk(res, 'exportFacts');
            const json = (await res.json());
            if (!json.success) {
                throw new Error(`exportFacts: server returned success=false - ${json.error_code}: ${json.error_message}`);
            }
            return {
                facts: json.facts ?? [],
                cursor: json.cursor,
                has_more: json.has_more ?? false,
                total_count: json.total_count,
            };
        },
        // ---- Health (unauthenticated) ----
        /**
         * Check server health.
         *
         * @returns `true` if the server responds with HTTP 200.
         */
        async health() {
            try {
                const res = await fetch(`${baseUrl}/health`, { method: 'GET' });
                return res.status === 200;
            }
            catch {
                return false;
            }
        },
    };
}
