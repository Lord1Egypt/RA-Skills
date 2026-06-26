/**
 * retype / set_scope pure operations for OpenClaw plugin — v1.1 taxonomy.
 *
 * Agents need to be able to reclassify an existing memory's `type`
 * (claim ↔ preference, etc.) or its `scope` (work ↔ personal ↔ health, ...)
 * without destroying the underlying text. The subgraph is append-only,
 * so like pin/unpin both operations tombstone the existing fact and
 * write a fresh v1.1 blob with the changed field. The new fact's
 * `superseded_by` points to the old fact id so cross-device readers see
 * the correct resolution.
 *
 * Why this module is separate from pin.ts
 * ---------------------------------------
 * `executePinOperation` is tightly coupled to `pin_status` handling
 * (idempotent short-circuit on matching status, decision-log recovery
 * for auto-supersede victims, feedback wiring into the tuning loop).
 * retype and set_scope are simpler — they don't short-circuit when the
 * new value equals the old (the user might be confirming a prior
 * auto-extraction's label) and they don't write feedback rows. Sharing
 * the transport / crypto deps with pin is still useful; callers pass
 * the same `RetypeSetScopeDeps` object.
 *
 * Scope and scanner surface
 * -------------------------
 * - No env-var reads — config is centralized in config.ts.
 * - No outbound HTTP — all network work happens inside the injected
 *   `submitBatch` dep (callers wire it to subgraph-store).
 * - No disk reads — callers supply an in-memory pre-loaded fact.
 */
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { buildV1ClaimBlob, mapTypeToCategory, readV1Blob, } from './claims-helper.js';
import { isValidMemoryType, VALID_MEMORY_SCOPES, V0_TO_V1_TYPE, } from './extractor.js';
import { PROTOBUF_VERSION_V4 } from './subgraph-store.js';
import { confirmIndexed } from './confirm-indexed.js';
// Lazy-load WASM core — mirrors pin.ts pattern.
const requireWasm = createRequire(import.meta.url);
let _wasm = null;
function getWasm() {
    if (!_wasm)
        _wasm = requireWasm('@totalreclaw/core');
    return _wasm;
}
function encodeFactProtobufLocal(fact, version) {
    const json = JSON.stringify({
        id: fact.id,
        timestamp: fact.timestamp,
        owner: fact.owner,
        encrypted_blob_hex: fact.encryptedBlob,
        blind_indices: fact.blindIndices,
        decay_score: fact.decayScore,
        source: fact.source,
        content_fp: fact.contentFp,
        agent_id: fact.agentId,
        encrypted_embedding: fact.encryptedEmbedding || null,
        version,
    });
    return Buffer.from(getWasm().encodeFactProtobuf(json));
}
function projectFromDecrypted(decrypted) {
    let obj;
    try {
        obj = JSON.parse(decrypted);
    }
    catch {
        return null;
    }
    // v1 blob (schema_version "1.x")
    if (typeof obj.text === 'string' &&
        typeof obj.type === 'string' &&
        typeof obj.schema_version === 'string' &&
        obj.schema_version.startsWith('1.')) {
        const v1 = readV1Blob(decrypted);
        if (v1) {
            return {
                text: v1.text,
                type: v1.type,
                source: v1.source,
                scope: v1.scope,
                volatility: v1.volatility,
                reasoning: v1.reasoning,
                entities: v1.entities,
                importance: v1.importance,
                confidence: v1.confidence,
                createdAt: v1.createdAt,
                expiresAt: v1.expiresAt,
                pinStatus: v1.pinStatus,
                embeddingModelId: v1.embeddingModelId,
            };
        }
    }
    // v0 short-key blob — upgrade to v1 shape.
    if (typeof obj.t === 'string' && typeof obj.c === 'string') {
        const v0Type = typeof obj.c === 'string' ? obj.c : 'fact';
        const v1Type = V0_TO_V1_TYPE[v0Type] ?? 'claim';
        const imp = typeof obj.i === 'number' ? obj.i : 5;
        const conf = typeof obj.cf === 'number' ? obj.cf : 0.85;
        const sa = typeof obj.sa === 'string' ? obj.sa : 'user';
        const validSource = ['user', 'user-inferred', 'assistant', 'external', 'derived'].includes(sa)
            ? sa
            : 'user';
        const ea = typeof obj.ea === 'string' ? obj.ea : new Date().toISOString();
        const entities = Array.isArray(obj.e)
            ? obj.e
                .map((e) => {
                if (!e || typeof e !== 'object')
                    return null;
                const entity = e;
                const name = typeof entity.n === 'string' ? entity.n : '';
                const entType = typeof entity.tp === 'string' ? entity.tp : 'concept';
                if (!name)
                    return null;
                const role = typeof entity.r === 'string' ? entity.r : undefined;
                return { name, type: entType, role };
            })
                .filter((e) => e !== null)
            : undefined;
        return {
            text: typeof obj.t === 'string' ? obj.t : '',
            type: v1Type,
            source: validSource,
            scope: undefined,
            volatility: undefined,
            reasoning: undefined,
            entities,
            importance: Math.max(1, Math.min(10, Math.round(imp))),
            confidence: Math.max(0, Math.min(1, conf)),
            createdAt: ea,
        };
    }
    return null;
}
// ---------------------------------------------------------------------------
// Core: retrieve existing fact, decrypt, rewrite with mutated field
// ---------------------------------------------------------------------------
async function rewriteWithMutation(factId, deps, mutate, confirmOpts) {
    const existing = await deps.fetchFactById(factId);
    if (!existing) {
        return { success: false, fact_id: factId, error: `Fact not found: ${factId}` };
    }
    const blobHex = existing.encryptedBlob.startsWith('0x')
        ? existing.encryptedBlob.slice(2)
        : existing.encryptedBlob;
    let plaintext;
    try {
        plaintext = deps.decryptBlob(blobHex);
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            error: `Failed to decrypt fact: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
    const current = projectFromDecrypted(plaintext);
    if (!current) {
        return {
            success: false,
            fact_id: factId,
            error: `Unrecognized blob shape for fact ${factId} — cannot retype/rescope`,
        };
    }
    const next = mutate(current);
    const newFactId = crypto.randomUUID();
    let canonicalJson;
    try {
        canonicalJson = buildV1ClaimBlob({
            id: newFactId,
            text: next.text,
            type: next.type,
            source: next.source,
            scope: next.scope,
            volatility: next.volatility,
            reasoning: next.reasoning,
            entities: next.entities,
            importance: next.importance,
            confidence: next.confidence,
            createdAt: new Date().toISOString(),
            supersededBy: factId,
            // Issue #117 follow-up: preserve pin_status so that retype / set_scope
            // on a pinned fact does NOT silently un-pin it. Without this, a pinned
            // fact loses its immunity to auto-supersede after any metadata edit.
            pinStatus: next.pinStatus,
            // 3.3.1-rc.22 — preserve the source claim's embedder tag through
            // retype/set_scope rewrites. Distillation forward-compat.
            embeddingModelId: next.embeddingModelId,
        });
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            error: `Failed to build v1 claim blob: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
    let newBlobHex;
    try {
        newBlobHex = deps.encryptBlob(canonicalJson);
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            error: `Failed to encrypt updated claim: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
    const entityNames = next.entities
        ? next.entities
            .map((e) => e.name)
            .filter((n) => typeof n === 'string' && n.length > 0)
        : [];
    let regenerated;
    try {
        regenerated = await deps.generateIndices(next.text, entityNames);
    }
    catch {
        regenerated = { blindIndices: [] };
    }
    const tombstonePayload = {
        id: factId,
        timestamp: new Date().toISOString(),
        owner: deps.owner,
        encryptedBlob: '00',
        blindIndices: [],
        decayScore: 0,
        source: 'tombstone',
        contentFp: '',
        agentId: deps.sourceAgent,
    };
    const newPayload = {
        id: newFactId,
        timestamp: new Date().toISOString(),
        owner: deps.owner,
        encryptedBlob: newBlobHex,
        blindIndices: regenerated.blindIndices,
        decayScore: 1.0,
        source: 'openclaw-plugin-retype',
        contentFp: '',
        agentId: deps.sourceAgent,
        encryptedEmbedding: regenerated.encryptedEmbedding,
    };
    const payloads = [
        encodeFactProtobufLocal(tombstonePayload, /* legacy v3 */ 3),
        encodeFactProtobufLocal(newPayload, PROTOBUF_VERSION_V4),
    ];
    try {
        const { txHash, success } = await deps.submitBatch(payloads);
        if (!success) {
            return {
                success: false,
                fact_id: factId,
                error: 'On-chain batch submission failed',
                tx_hash: txHash,
            };
        }
        // Read-after-write: poll the subgraph until the new fact id is indexed
        // and active, OR the timeout (default 30s) elapses. On timeout (or if
        // the WASM bindings are unavailable / subgraph unreachable), surface
        // `partial: true` so the caller knows the chain write succeeded but the
        // indexer has not yet caught up. The confirm step is observational —
        // never fail the whole operation just because confirm step couldn't run.
        let indexed = false;
        try {
            const confirm = await confirmIndexed(newFactId, confirmOpts);
            indexed = confirm.indexed;
        }
        catch {
            indexed = false;
        }
        return {
            success: true,
            fact_id: factId,
            new_fact_id: newFactId,
            previous_type: current.type,
            new_type: next.type,
            previous_scope: current.scope,
            new_scope: next.scope,
            tx_hash: txHash,
            ...(indexed ? {} : { partial: true }),
        };
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            error: `Failed to submit retype/rescope batch: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
}
// ---------------------------------------------------------------------------
// Public entry points
// ---------------------------------------------------------------------------
/**
 * Re-type an existing memory. Writes a new v1.1 claim with `type` changed;
 * tombstones the old fact. `superseded_by` on the new fact points to the
 * old id so cross-device readers see the correct resolution.
 */
export async function executeRetype(factId, newType, deps, confirmOpts) {
    if (!isValidMemoryType(newType)) {
        return {
            success: false,
            fact_id: factId,
            error: `Invalid new type "${newType}". Must be one of: claim, preference, directive, commitment, episode, summary.`,
        };
    }
    return rewriteWithMutation(factId, deps, (current) => ({
        ...current,
        type: newType,
    }), confirmOpts);
}
/**
 * Re-scope an existing memory. Writes a new v1.1 claim with `scope` changed;
 * tombstones the old fact.
 */
export async function executeSetScope(factId, newScope, deps, confirmOpts) {
    if (!VALID_MEMORY_SCOPES.includes(newScope)) {
        return {
            success: false,
            fact_id: factId,
            error: `Invalid new scope "${newScope}". Must be one of: ${VALID_MEMORY_SCOPES.join(', ')}.`,
        };
    }
    return rewriteWithMutation(factId, deps, (current) => ({
        ...current,
        scope: newScope,
    }), confirmOpts);
}
export function validateRetypeArgs(args) {
    if (typeof args !== 'object' || args === null) {
        return { ok: false, error: 'totalreclaw_retype requires an object argument.' };
    }
    const rec = args;
    const factId = rec.fact_id ?? rec.factId;
    if (typeof factId !== 'string' || factId.trim().length === 0) {
        return { ok: false, error: 'fact_id is required and must be a non-empty string.' };
    }
    const newType = rec.new_type ?? rec.newType ?? rec.type;
    if (typeof newType !== 'string' || !isValidMemoryType(newType)) {
        return {
            ok: false,
            error: `new_type must be one of: ${[...['claim', 'preference', 'directive', 'commitment', 'episode', 'summary']].join(', ')}`,
        };
    }
    return { ok: true, factId: factId.trim(), newType: newType };
}
export function validateSetScopeArgs(args) {
    if (typeof args !== 'object' || args === null) {
        return { ok: false, error: 'totalreclaw_set_scope requires an object argument.' };
    }
    const rec = args;
    const factId = rec.fact_id ?? rec.factId;
    if (typeof factId !== 'string' || factId.trim().length === 0) {
        return { ok: false, error: 'fact_id is required and must be a non-empty string.' };
    }
    const newScope = rec.new_scope ?? rec.newScope ?? rec.scope;
    if (typeof newScope !== 'string' || !VALID_MEMORY_SCOPES.includes(newScope)) {
        return {
            ok: false,
            error: `new_scope must be one of: ${VALID_MEMORY_SCOPES.join(', ')}`,
        };
    }
    return { ok: true, factId: factId.trim(), newScope: newScope };
}
// ---------------------------------------------------------------------------
// Export mapTypeToCategory re-export so callers (index.ts) don't need
// a separate import path.
// ---------------------------------------------------------------------------
export { mapTypeToCategory };
