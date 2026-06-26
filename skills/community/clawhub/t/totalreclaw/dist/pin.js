/** Pin/unpin pure operation for OpenClaw plugin — v1.1 taxonomy.
 *
 * As of core 2.1.1 / plugin pin path v1.1 (2026-04-19) the pin/unpin operation
 * emits a canonical v1.1 MemoryClaimV1 JSON blob (schema_version "1.0",
 * `pin_status` additive field) wrapped in the outer protobuf at `version = 4`.
 * The prior behavior — emitting v0 short-key blobs at `version = 3` on the
 * pin path — broke the v1 on-chain contract (RC QA bug #2). v0 blobs continue
 * to be READ correctly (via parseBlobForPin's fall-through), so mixed-version
 * vaults remain uniform from the user's point of view.
 */
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { buildV1ClaimBlob, mapTypeToCategory, readV1Blob, } from './claims-helper.js';
import { findLoserClaimInDecisionLog, maybeWriteFeedbackForPin, } from './contradiction-sync.js';
import { isValidMemoryType, V0_TO_V1_TYPE } from './extractor.js';
import { PROTOBUF_VERSION_V4 } from './subgraph-store.js';
import { confirmIndexed } from './confirm-indexed.js';
// Lazy-load WASM core (mirrors claims-helper.ts pattern — plays nicely under
// both the OpenClaw runtime (CJS-ish tsx) and bare Node ESM used by tests).
const requireWasm = createRequire(import.meta.url);
let _wasm = null;
function getWasm() {
    if (!_wasm)
        _wasm = requireWasm('@totalreclaw/core');
    return _wasm;
}
/**
 * Encode a FactPayload as the minimal Protobuf wire format via WASM core.
 *
 * The `version` field is threaded through so callers can opt into
 * `PROTOBUF_VERSION_V4` (Memory Taxonomy v1) for the new-fact write and leave
 * tombstone rows at the default (legacy v3). When omitted, defaults to v1
 * (`PROTOBUF_VERSION_V4`) — pin/unpin is a v1 write path.
 */
function encodeFactProtobufLocal(fact, version = PROTOBUF_VERSION_V4) {
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
const SHORT_TO_HUMAN = {
    a: 'active',
    p: 'pinned',
    s: 'superseded',
    r: 'retracted',
    c: 'contradicted',
};
const HUMAN_TO_SHORT = {
    active: 'a',
    pinned: 'p',
    superseded: 's',
    retracted: 'r',
    contradicted: 'c',
};
/** Parse a decrypted blob into a canonical mutable Claim + current human status. */
export function parseBlobForPin(decrypted) {
    let obj;
    try {
        obj = JSON.parse(decrypted);
    }
    catch {
        const shortClaim = buildCanonicalObjectFromLegacy(decrypted, {});
        return {
            source: { kind: 'v0', claim: shortClaim },
            claim: shortClaim,
            currentStatus: 'active',
            isLegacy: true,
        };
    }
    // v1 payload (plugin v3.0.0+): long-form fields + schema_version "1.x".
    // Preserve the v1 structure so the pin path can emit v1 on output.
    if (typeof obj.text === 'string' &&
        typeof obj.type === 'string' &&
        typeof obj.schema_version === 'string' &&
        obj.schema_version.startsWith('1.')) {
        const v1 = readV1Blob(decrypted);
        if (v1) {
            // Current status = pinStatus if present, else active.
            const human = v1.pinStatus === 'pinned' ? 'pinned' : 'active';
            const shortProjection = v1ToShortKeyClaim(obj);
            return {
                source: {
                    kind: 'v1',
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
                    id: v1.id,
                    pinStatus: v1.pinStatus,
                    embeddingModelId: v1.embeddingModelId,
                },
                claim: shortProjection,
                currentStatus: human,
                isLegacy: false,
            };
        }
        // readV1Blob returned null — fall through to v0 path.
    }
    // v0 canonical Claim — short keys present.
    if (typeof obj.t === 'string' && typeof obj.c === 'string') {
        const st = typeof obj.st === 'string' ? obj.st : 'a';
        const human = SHORT_TO_HUMAN[st] ?? 'active';
        const cloned = JSON.parse(JSON.stringify(obj));
        return {
            source: { kind: 'v0', claim: cloned },
            claim: cloned,
            currentStatus: human,
            isLegacy: false,
        };
    }
    // Legacy {text, metadata: {importance: 0-1}} shape.
    if (typeof obj.text === 'string') {
        const meta = obj.metadata ?? {};
        const shortClaim = buildCanonicalObjectFromLegacy(obj.text, meta);
        return {
            source: { kind: 'v0', claim: shortClaim },
            claim: shortClaim,
            currentStatus: 'active',
            isLegacy: true,
        };
    }
    const shortClaim = buildCanonicalObjectFromLegacy(decrypted, {});
    return {
        source: { kind: 'v0', claim: shortClaim },
        claim: shortClaim,
        currentStatus: 'active',
        isLegacy: true,
    };
}
/**
 * Convert a Memory Taxonomy v1 blob object into the short-key shape that
 * the rest of pin.ts manipulates. Pin operations tombstone the existing
 * fact and write a fresh one with the short-key format; the v1 inner blob
 * is not round-tripped through pin (that would require upgrading every
 * downstream read site). Since pin already rewrites the fact with new
 * indices, round-trip fidelity isn't required.
 */
function v1ToShortKeyClaim(v1) {
    const text = typeof v1.text === 'string' ? v1.text : '';
    const type = typeof v1.type === 'string' ? v1.type : 'claim';
    // Map v1 type to the short category key used by the v0 format.
    const category = isValidMemoryType(type) ? mapTypeToCategory(type) : 'fact';
    const impNum = typeof v1.importance === 'number' ? v1.importance : 5;
    const importance = Math.max(1, Math.min(10, Math.round(impNum)));
    const confidence = typeof v1.confidence === 'number' ? v1.confidence : 0.85;
    const source = typeof v1.source === 'string' ? v1.source : 'openclaw-plugin';
    const createdAt = typeof v1.created_at === 'string' ? v1.created_at : new Date().toISOString();
    const out = {
        t: text,
        c: category,
        cf: confidence,
        i: importance,
        sa: source,
        ea: createdAt,
    };
    if (Array.isArray(v1.entities) && v1.entities.length > 0) {
        out.e = v1.entities
            .map((e) => {
            if (!e || typeof e !== 'object')
                return null;
            const entity = e;
            const name = typeof entity.name === 'string' ? entity.name : '';
            const entType = typeof entity.type === 'string' ? entity.type : 'concept';
            if (!name)
                return null;
            const short = { n: name, tp: entType };
            if (typeof entity.role === 'string' && entity.role.length > 0) {
                short.r = entity.role;
            }
            return short;
        })
            .filter((e) => e !== null);
    }
    return out;
}
function buildCanonicalObjectFromLegacy(text, meta) {
    // Phase 2.2.6: use the single-source-of-truth mapping from claims-helper
    // instead of a local duplicate. Legacy blobs can carry arbitrary strings in
    // `metadata.type`, so we validate via `isValidMemoryType` before mapping —
    // unknown types fall back to 'fact'.
    const typeStr = typeof meta.type === 'string' ? meta.type : 'fact';
    const category = isValidMemoryType(typeStr) ? mapTypeToCategory(typeStr) : 'fact';
    const impFloat = typeof meta.importance === 'number' ? meta.importance : 0.5;
    const importance = Math.max(1, Math.min(10, Math.round(impFloat * 10)));
    const source = typeof meta.source === 'string' ? meta.source : 'openclaw-plugin';
    const createdAt = typeof meta.created_at === 'string' ? meta.created_at : new Date().toISOString();
    return {
        t: text,
        c: category,
        cf: 0.85,
        i: importance,
        sa: source,
        ea: createdAt,
    };
}
/**
 * Project a source blob (v1 or v0 short-key) into the v1 shape needed by
 * `buildV1ClaimBlob`. For v1 sources this is identity; for v0 sources we
 * upgrade the category / source fields per the spec's legacy-mapping table
 * (`fact|context|decision → claim`, `rule → directive`, `goal → commitment`,
 * etc.). Anything we can't determine falls back to a sensible default so the
 * build call doesn't throw.
 */
function projectToV1(src, defaultSourceAgent) {
    if (src.kind === 'v1') {
        return {
            text: src.text,
            type: src.type,
            source: src.source,
            scope: src.scope,
            volatility: src.volatility,
            reasoning: src.reasoning,
            entities: src.entities,
            importance: src.importance,
            confidence: src.confidence,
            embeddingModelId: src.embeddingModelId,
        };
    }
    // v0 path — upgrade short-key claim to v1.
    const claim = src.claim;
    const text = typeof claim.t === 'string' ? claim.t : '';
    const v0Category = typeof claim.c === 'string' ? claim.c : 'fact';
    // Legacy short category keys back to type names (reverse of TYPE_TO_CATEGORY_V0).
    const V0_CATEGORY_TO_V0_TYPE = {
        fact: 'fact',
        pref: 'preference',
        dec: 'decision',
        epi: 'episodic',
        goal: 'goal',
        ctx: 'context',
        sum: 'summary',
        rule: 'rule',
        ent: 'fact', // entity records don't round-trip as v1 claims; fall back
        dig: 'summary',
        claim: 'claim',
    };
    const v0TypeToken = V0_CATEGORY_TO_V0_TYPE[v0Category] ?? 'fact';
    // Use the shared v0→v1 map for the upgrade.
    const v1Type = V0_TO_V1_TYPE[v0TypeToken] ?? 'claim';
    const importance = typeof claim.i === 'number'
        ? Math.max(1, Math.min(10, Math.round(claim.i)))
        : 5;
    const confidence = typeof claim.cf === 'number' ? claim.cf : 0.85;
    // v0 `sa` isn't a provenance source — it's a "source agent" string like
    // "openclaw-plugin". Map heuristically: if it looks like an agent-style
    // string (contains "plugin"/"agent"/"derived"), mark it as appropriate;
    // otherwise default to "user-inferred" so Tier 1 reranker doesn't give it
    // "user" trust (which would be wrong for legacy blobs with no provenance
    // signal).
    const sa = typeof claim.sa === 'string' ? claim.sa : defaultSourceAgent;
    let v1Source = 'user-inferred';
    const saLower = sa.toLowerCase();
    if (saLower.includes('derived') || saLower.includes('digest') || saLower.includes('consolidat')) {
        v1Source = 'derived';
    }
    else if (saLower.includes('assistant')) {
        v1Source = 'assistant';
    }
    else if (saLower.includes('extern') || saLower.includes('mem0') || saLower.includes('import')) {
        v1Source = 'external';
    }
    const entities = Array.isArray(claim.e)
        ? claim.e
            .map((e) => {
            if (!e || typeof e !== 'object')
                return null;
            const entity = e;
            const name = typeof entity.n === 'string' ? entity.n : '';
            const entType = typeof entity.tp === 'string' ? entity.tp : 'concept';
            if (!name)
                return null;
            const out = { name, type: entType };
            if (typeof entity.r === 'string' && entity.r.length > 0)
                out.role = entity.r;
            return out;
        })
            .filter((x) => x !== null)
        : undefined;
    return {
        text,
        type: v1Type,
        source: v1Source,
        importance,
        confidence,
        entities,
    };
}
/**
 * Execute a pin or unpin operation on a single fact.
 *
 * The subgraph is append-only, so a status change requires writing a new fact
 * with the updated status and tombstoning the old one. The new fact's `sup`
 * field points to the old fact id, forming a cross-device-visible supersession
 * chain. Matches MCP's `executePinOperation` byte-for-byte on the supersession
 * semantics (short keys, idempotent no-op, decayScore=1.0, trapdoor regen).
 */
export async function executePinOperation(factId, targetStatus, deps, reason, confirmOpts) {
    // 1. Fetch the existing fact
    const existing = await deps.fetchFactById(factId);
    if (!existing) {
        return {
            success: false,
            fact_id: factId,
            error: `Fact not found: ${factId}`,
        };
    }
    // 2. Decrypt + parse current status
    const blobHex = existing.encryptedBlob.startsWith('0x')
        ? existing.encryptedBlob.slice(2)
        : existing.encryptedBlob;
    let plaintext;
    let recoveredFromDecisionLog = false;
    try {
        plaintext = deps.decryptBlob(blobHex);
    }
    catch (err) {
        // Phase 2.1 recovery path: if the on-chain blob is a tombstone (1-byte
        // `0x00` written by an auto-resolved supersede), the cipher will fail
        // because the ciphertext is shorter than the auth tag. Fall back to the
        // canonical Claim JSON we stashed in `decisions.jsonl` at supersede time.
        // Without this fallback, the user can never override an auto-resolution
        // and the weight-tuning loop never receives gradient signal.
        const errMsg = err instanceof Error ? err.message : String(err);
        const looksLikeTombstone = blobHex === '00' ||
            blobHex === '' ||
            errMsg.includes('Encrypted data too short') ||
            errMsg.includes('too short') ||
            errMsg.includes('Cipher');
        if (!looksLikeTombstone) {
            return {
                success: false,
                fact_id: factId,
                error: `Failed to decrypt fact: ${errMsg}`,
            };
        }
        const recovered = findLoserClaimInDecisionLog(factId);
        if (!recovered) {
            return {
                success: false,
                fact_id: factId,
                error: `Failed to decrypt fact and no recovery row in decisions.jsonl: ${errMsg}. ` +
                    'The fact may have been tombstoned by an auto-resolution that predates Phase 2.1 ' +
                    '(when loser_claim_json was added to the decision log).',
            };
        }
        plaintext = recovered;
        recoveredFromDecisionLog = true;
        deps.logger?.info?.(`pin: recovered loser claim from decisions.jsonl for ${factId.slice(0, 10)}…`);
    }
    const parsed = parseBlobForPin(plaintext);
    // Recovered claims always represent a fact the user is trying to override —
    // never short-circuit the operation as idempotent because the `st` field on
    // the recovered loser was whatever the original auto-resolution stored
    // (typically active). Drop the previous status so the targetStatus check
    // below produces a real on-chain write.
    if (recoveredFromDecisionLog) {
        parsed.currentStatus = 'active';
    }
    // 3. Idempotent early-exit
    if (parsed.currentStatus === targetStatus) {
        return {
            success: true,
            fact_id: factId,
            previous_status: parsed.currentStatus,
            new_status: targetStatus,
            idempotent: true,
            reason,
        };
    }
    // 4. Build the new canonical v1.1 claim with pin_status + superseded_by link.
    //
    // The new blob is ALWAYS v1.1 shaped (schema_version "1.0", pin_status
    // present) regardless of the source blob's format. v0 sources are upgraded
    // to v1 on the pin path; v1 sources round-trip their metadata (source,
    // scope, reasoning, entities, volatility) into the new blob.
    const pinStatus = targetStatus === 'pinned' ? 'pinned' : 'unpinned';
    const newFactId = crypto.randomUUID();
    // Project the source blob into v1 shape. For v0 sources we upgrade on the
    // fly: short-key `c` → v1 type, `sa` → source (heuristic), etc.
    const v1View = projectToV1(parsed.source, deps.sourceAgent);
    let canonicalJson;
    try {
        canonicalJson = buildV1ClaimBlob({
            id: newFactId,
            text: v1View.text,
            type: v1View.type,
            source: v1View.source,
            scope: v1View.scope,
            volatility: v1View.volatility,
            reasoning: v1View.reasoning,
            entities: v1View.entities,
            importance: v1View.importance,
            confidence: v1View.confidence,
            createdAt: new Date().toISOString(),
            supersededBy: factId,
            pinStatus,
            // 3.3.1-rc.22 — preserve the source claim's embedder tag through
            // pin mutation. The new fact reuses the same encrypted embedding
            // as the original (re-indexed via deps.regenerateBlindIndices),
            // so the embedder identity must round-trip too.
            embeddingModelId: v1View.embeddingModelId,
        });
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            error: `Failed to build v1 claim blob: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
    // 5. Encrypt the new blob
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
    // 5b. Regenerate trapdoors so the new fact is findable by the same text.
    const entityNames = v1View.entities
        ? v1View.entities.map((e) => e.name).filter((n) => typeof n === 'string' && n.length > 0)
        : [];
    let regenerated;
    try {
        regenerated = await deps.generateIndices(v1View.text, entityNames);
    }
    catch {
        regenerated = { blindIndices: [] };
    }
    // 6. Build tombstone + new protobuf payloads.
    //
    // Tombstone: empty blob ('00'), empty indices, decayScore=0, source='tombstone'.
    // Written at the DEFAULT protobuf version (legacy v3) because tombstone rows
    // carry no inner blob — the version field is irrelevant for readers and
    // writing v3 keeps round-trip compat with any pre-v1 tombstone parser.
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
        source: targetStatus === 'pinned' ? 'openclaw-plugin-pin' : 'openclaw-plugin-unpin',
        contentFp: '',
        agentId: deps.sourceAgent,
        encryptedEmbedding: regenerated.encryptedEmbedding,
    };
    // Outer protobuf version: v=4 for the new v1 claim, default (legacy v3)
    // for the tombstone. This is the core of the bug-2 fix — previously both
    // payloads went out at version=3 and the inner blob was v0 short-key.
    const payloads = [
        encodeFactProtobufLocal(tombstonePayload, /* version = legacy v3 */ 3),
        encodeFactProtobufLocal(newPayload, PROTOBUF_VERSION_V4),
    ];
    // 6b. Slice 2f: consult decisions.jsonl to see if this pin/unpin contradicts
    // a prior auto-resolution. If so, append a counterexample to feedback.jsonl
    // so the next digest-compile's tuning loop can nudge the weights. Voluntary
    // pins (no matching decision) produce no feedback row. Never fatal.
    const feedbackLogger = deps.logger ?? {
        info: () => { },
        warn: () => { },
    };
    try {
        await maybeWriteFeedbackForPin(factId, targetStatus, Math.floor(Date.now() / 1000), feedbackLogger);
    }
    catch {
        // Feedback wiring is best-effort — never block the pin op.
    }
    // 7. Submit both in a single batch UserOp.
    try {
        const { txHash, success } = await deps.submitBatch(payloads);
        if (!success) {
            return {
                success: false,
                fact_id: factId,
                previous_status: parsed.currentStatus,
                error: 'On-chain batch submission failed',
                tx_hash: txHash,
            };
        }
        // Read-after-write: poll the subgraph until the new (pinned/unpinned)
        // fact id is indexed and active. On timeout, surface `partial: true`
        // so a follow-up recall/export that races against indexer lag can
        // surface a clear "still propagating" hint rather than apparent staleness.
        const confirm = await confirmIndexed(newFactId, confirmOpts);
        return {
            success: true,
            fact_id: factId,
            new_fact_id: newFactId,
            previous_status: parsed.currentStatus,
            new_status: targetStatus,
            tx_hash: txHash,
            reason,
            ...(confirm.indexed ? {} : { partial: true }),
        };
    }
    catch (err) {
        return {
            success: false,
            fact_id: factId,
            previous_status: parsed.currentStatus,
            error: `Failed to submit pin batch: ${err instanceof Error ? err.message : String(err)}`,
        };
    }
}
/** Validate the `{fact_id, reason?}` input shape for pin/unpin tool calls. */
export function validatePinArgs(args) {
    if (!args || typeof args !== 'object') {
        return { ok: false, factId: '', error: 'Invalid input: fact_id is required' };
    }
    const record = args;
    const factId = record.fact_id;
    if (factId === undefined || factId === null) {
        return { ok: false, factId: '', error: 'Invalid input: fact_id is required' };
    }
    if (typeof factId !== 'string') {
        return { ok: false, factId: '', error: 'Invalid input: fact_id must be a non-empty string' };
    }
    if (factId.trim().length === 0) {
        return { ok: false, factId: '', error: 'Invalid input: fact_id must be a non-empty string' };
    }
    const reason = typeof record.reason === 'string' ? record.reason : undefined;
    return { ok: true, factId: factId.trim(), reason, error: '' };
}
