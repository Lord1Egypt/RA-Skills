/**
 * TotalReclaw Plugin — Knowledge Graph helpers for the write path.
 *
 * Builds canonical Claim JSON from an ExtractedFact, generates entity
 * trapdoors for blind search, and resolves the claim-format feature flag.
 *
 * The canonical Claim schema uses compact short keys (t, c, cf, i, sa, ea, e, ...)
 * and is produced byte-identically across Rust, WASM, and Python via
 * `canonicalizeClaim()` in @totalreclaw/core.
 */

import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import type {
  ExtractedEntity,
  ExtractedFact,
  MemoryType,
  MemoryTypeV0,
  MemoryTypeV1,
  MemoryScope,
  MemorySource,
  MemoryVolatility,
} from './extractor.js';
import {
  isValidMemoryType,
  isValidMemoryTypeV1,
  V0_TO_V1_TYPE,
  VALID_MEMORY_SCOPES,
  VALID_MEMORY_SOURCES,
  VALID_MEMORY_VOLATILITIES,
  VALID_MEMORY_TYPES_V1,
} from './extractor.js';
import { envStringLower } from './entry.js';

// Lazy-load WASM. We use createRequire so this module loads cleanly under
// both the OpenClaw runtime (CJS-ish tsx) and bare Node ESM (used by tests).
const requireWasm = createRequire(import.meta.url);
let _wasm: typeof import('@totalreclaw/core') | null = null;
function getWasm() {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core');
  return _wasm!;
}

// ---------------------------------------------------------------------------
// Category mapping (ExtractedFact.type → compact Claim category short key)
// ---------------------------------------------------------------------------

// Legacy v0 type → compact category mapping. Kept for reading pre-v1 vault
// entries that stored the short-form category as the decrypted `c` key.
const TYPE_TO_CATEGORY_V0: Record<MemoryTypeV0, string> = {
  fact: 'fact',
  preference: 'pref',
  decision: 'dec',
  episodic: 'epi',
  goal: 'goal',
  context: 'ctx',
  summary: 'sum',
  rule: 'rule',
};

// v1 type → compact category mapping for recall display. These short keys
// remain the display-layer category tags (e.g. `[rule]`, `[fact]`) that the
// recall tool surfaces, so the v1 types map onto the v0 category keys.
const TYPE_TO_CATEGORY_V1: Record<MemoryType, string> = {
  claim: 'claim',
  preference: 'pref',
  directive: 'rule',  // v1 directive → v0 category "rule" for display
  commitment: 'goal', // v1 commitment → v0 category "goal" for display
  episode: 'epi',
  summary: 'sum',
};

/**
 * Map any memory type (v1 or legacy v0) to the compact category short key.
 *
 * v1 types take priority; unknown tokens fall through to the v0 table for
 * pre-v1 vault entries; anything else returns `'fact'`.
 */
export function mapTypeToCategory(type: MemoryType | MemoryTypeV0): string {
  if (type in TYPE_TO_CATEGORY_V1) return TYPE_TO_CATEGORY_V1[type as MemoryType];
  return TYPE_TO_CATEGORY_V0[type as MemoryTypeV0] ?? 'fact';
}

// ---------------------------------------------------------------------------
// Canonical Claim builder
// ---------------------------------------------------------------------------

export interface BuildClaimInput {
  fact: ExtractedFact;
  importance: number; // 1-10, may differ from fact.importance after store-time dedup supersede
  /**
   * Source-agent metadata string. Carried through as legacy context only —
   * plugin v3.0.0 emits v1 JSON blobs where provenance lives in `fact.source`
   * and this field is ignored. Kept on the input interface so existing
   * call-site signatures continue to type-check.
   */
  sourceAgent: string;
  /** Creation timestamp. Defaults to now. */
  extractedAt?: string;
  /**
   * 3.3.1-rc.22 — optional embedding-model id stamped on the claim for
   * forward-compat. Defaults to omitted (callers that already know the
   * active embedder pass it in; legacy paths leave it unset). The field
   * is plugin-scoped — it survives the core validator's strip pass via
   * the same re-attach path used for `schema_version` / `volatility`.
   */
  embeddingModelId?: string;
}

/**
 * Construct a canonical Claim JSON string from an ExtractedFact.
 *
 * As of plugin v3.0.0, this unconditionally emits a Memory Taxonomy v1 JSON
 * blob (schema_version "1.0") — forwarded to `buildCanonicalClaimV1`. The
 * legacy v0 short-key {t, c, i, sa, ea} format is no longer produced on the
 * write path.
 *
 * When `fact.source` is missing we default it to `'user-inferred'` so a
 * misconfigured extraction hook doesn't drop the write. The outer protobuf
 * wrapper's `version` field MUST be set to 4 when storing the returned
 * payload (see `subgraph-store.ts::encodeFactProtobuf`).
 */
export function buildCanonicalClaim(input: BuildClaimInput): string {
  const { fact, importance, extractedAt, embeddingModelId } = input;

  // Defensive: ensure fact.source is always populated before v1 validation.
  // `applyProvenanceFilterLax` should have set this upstream; this is the
  // belt-and-suspenders fallback for explicit tool paths / legacy callers.
  const factWithSource: ExtractedFact = fact.source
    ? fact
    : { ...fact, source: 'user-inferred' };

  return buildCanonicalClaimV1({
    fact: factWithSource,
    importance,
    createdAt: extractedAt,
    embeddingModelId,
  });
}

// ---------------------------------------------------------------------------
// v1 Claim payload builder (Phase 3 — plugin v3.0.0)
//
// Produces a MemoryClaimV1-shaped JSON payload matching
// `docs/specs/totalreclaw/memory-taxonomy-v1.md`.
//
// The v1 payload uses long field names + a schema_version marker so that
// decrypt logic can discriminate between v0 short-key claims and v1 claims
// without any external hint. The protobuf outer wrapper sets `version = 4`
// when writing v1 payloads — see `subgraph-store.ts`.
// ---------------------------------------------------------------------------

export const V1_SCHEMA_VERSION = '1.0' as const;

/**
 * v1.1 pin state — `"pinned"` = user explicitly pinned (immune to
 * auto-supersede); `"unpinned"` (or absence) = standard behavior.
 *
 * Surface of the `pin_status` field added in spec v1.1 (2026-04-19). Writers
 * that understand v1.1 emit this field on the pin path; readers at 1.0 / 1.1
 * that see it MUST honor `"pinned"` as immunity from auto-supersede.
 */
export type PinStatus = 'pinned' | 'unpinned';

export interface BuildClaimV1Input {
  /** The extracted fact in v1 shape. Must have `type` as a MemoryTypeV1 token. */
  fact: ExtractedFact;
  /** Final importance after any store-time dedup adjustment. 1-10. */
  importance: number;
  /** Creation timestamp. Defaults to now. */
  createdAt?: string;
  /** Optional superseded-by chain pointer (for pin / retype / forget). */
  supersededBy?: string;
  /** Optional explicit expiration timestamp. */
  expiresAt?: string;
  /** Stable claim ID. Defaults to crypto.randomUUID() at the call site; keep the
   *  same ID for both the blob and the on-chain fact id. */
  id?: string;
  /**
   * v1.1 pin state. When `"pinned"`, the claim is immune to auto-supersede.
   * Omitted or `"unpinned"` both mean unpinned (field is additive — absence
   * equivalent to `"unpinned"` on the wire). Surfaced in the final JSON only
   * when provided.
   */
  pinStatus?: PinStatus;
  /**
   * 3.3.1-rc.22 — optional embedding-model id stamped on the claim for
   * distillation forward-compat. Survives the core validator strip pass
   * via the same re-attach path used for `schema_version` / `volatility`.
   * When omitted the field is not emitted (legacy claims remain untagged
   * and are read back as "unspecified").
   */
  embeddingModelId?: string;
}

/**
 * Build a v1 MemoryClaimV1 JSON blob.
 *
 * Throws if the fact does not have a valid v1 `source` set — v1 requires
 * every claim to carry provenance (the whole taxonomy depends on it).
 *
 * The build pipeline:
 *   1. Build the full v1 payload object (including plugin-only extras like
 *      `volatility` and `schema_version`).
 *   2. Send the core-required subset through `validateMemoryClaimV1` for
 *      schema enforcement (throws on invalid type/source/missing id).
 *   3. Emit the FULL payload (core canonical fields + plugin extras) as the
 *      final stored JSON so round-trip preserves client-side state.
 *
 * Plugin-only extras (not round-tripped by core's validator as of v2.0.0):
 *   - `schema_version` — version marker the decrypt path reads
 *   - `volatility` — stable | updatable | ephemeral (re-scored after extraction)
 *
 * The outer protobuf wrapper's `version` field must be set to 4 when storing
 * the returned payload (see subgraph-store.ts).
 */
export function buildCanonicalClaimV1(input: BuildClaimV1Input): string {
  const { fact, importance, createdAt, supersededBy, expiresAt } = input;
  const id = input.id ?? crypto.randomUUID();

  if (!fact.source) {
    throw new Error(
      'buildCanonicalClaimV1: fact.source is required (v1 taxonomy mandates provenance)',
    );
  }
  if (!(VALID_MEMORY_SOURCES as readonly string[]).includes(fact.source)) {
    throw new Error(`buildCanonicalClaimV1: invalid source "${fact.source}"`);
  }

  const type = normalizeToV1Type(fact.type);
  const resolvedCreatedAt = createdAt ?? new Date().toISOString();
  const resolvedImportance = Math.max(1, Math.min(10, Math.round(importance)));

  // Core-canonical subset sent through validateMemoryClaimV1. Core strips
  // fields it doesn't understand, so we send it the subset it accepts and
  // re-attach client-side extras to the final payload.
  const corePayload: Record<string, unknown> = {
    id,
    text: fact.text,
    type,
    source: fact.source,
    created_at: resolvedCreatedAt,
    importance: resolvedImportance,
  };

  if (fact.scope && (VALID_MEMORY_SCOPES as readonly string[]).includes(fact.scope)) {
    corePayload.scope = fact.scope;
  }
  if (fact.reasoning && fact.reasoning.length > 0) {
    corePayload.reasoning = fact.reasoning.slice(0, 256);
  }
  if (fact.entities && fact.entities.length > 0) {
    corePayload.entities = fact.entities.slice(0, 8).map((e) => {
      const entity: Record<string, unknown> = { name: e.name, type: e.type };
      if (e.role) entity.role = e.role;
      return entity;
    });
  }
  if (typeof fact.confidence === 'number') {
    corePayload.confidence = Math.max(0, Math.min(1, fact.confidence));
  }
  if (expiresAt) corePayload.expires_at = expiresAt;
  if (supersededBy) corePayload.superseded_by = supersededBy;
  // v1.1 pin_status — additive field; only emitted when the caller opts in.
  if (input.pinStatus === 'pinned' || input.pinStatus === 'unpinned') {
    corePayload.pin_status = input.pinStatus;
  }

  // Validate through core — throws on invalid type / source / missing id.
  const validated = getWasm().validateMemoryClaimV1(JSON.stringify(corePayload)) as string;
  const canonical = JSON.parse(validated) as Record<string, unknown>;

  // Re-attach plugin-only extras not round-tripped by core's validator.
  canonical.schema_version = V1_SCHEMA_VERSION;
  if (fact.volatility && (VALID_MEMORY_VOLATILITIES as readonly string[]).includes(fact.volatility)) {
    canonical.volatility = fact.volatility;
  }
  // 3.3.1-rc.22 — forward-compat embedder marker. Plugin-only field;
  // survives the core validator via re-attach. Future distillation
  // detects this on read to re-embed selectively without forcing a
  // vault-wide rebuild.
  if (typeof input.embeddingModelId === 'string' && input.embeddingModelId.length > 0) {
    canonical.embedding_model_id = input.embeddingModelId;
  }
  // am-1: Crystal-shaped debrief structured metadata. Re-attached after
  // validation using the same plugin-extra pattern as volatility.
  if (fact.crystalMetadata) {
    canonical.metadata = fact.crystalMetadata;
  }

  return JSON.stringify(canonical);
}

// ---------------------------------------------------------------------------
// buildV1ClaimBlob — lightweight v1 blob builder for pin / retype / set_scope
//
// Unlike buildCanonicalClaimV1 (which consumes a full ExtractedFact), this
// helper takes raw primitives and is the right entry point when synthesizing
// a new blob from a previously-decrypted one — e.g. the pin path rewrites the
// blob with an updated pin_status field and everything else preserved.
//
// The output is a v1.1 JSON payload with schema_version "1.0" (v1.1 is
// additive; on-wire schema_version is unchanged per spec). The outer protobuf
// wrapper MUST be written at version 4 — see `subgraph-store.ts`.
// ---------------------------------------------------------------------------

export interface BuildV1ClaimBlobInput {
  /** Human-readable fact text (5-512 UTF-8 chars). */
  text: string;
  /** v1 memory type. Must be one of the 6 canonical values. */
  type: MemoryType;
  /** Provenance per spec §provenance-filter. */
  source: MemorySource;
  /** Optional stable UUID; defaults to randomUUID(). */
  id?: string;
  /** Optional creation timestamp (ISO 8601 UTC); defaults to now. */
  createdAt?: string;
  /** Optional scope (defaults to omitted → "unspecified"). */
  scope?: MemoryScope;
  /** Optional volatility (defaults to omitted → "updatable"). */
  volatility?: MemoryVolatility;
  /** Optional reasoning clause for decision-style claims. */
  reasoning?: string;
  /** Optional structured entities. */
  entities?: ExtractedEntity[];
  /** Optional expiration timestamp. */
  expiresAt?: string;
  /** Optional importance (1-10, advisory). */
  importance?: number;
  /** Optional confidence (0-1). */
  confidence?: number;
  /** Optional superseded-by chain pointer. */
  supersededBy?: string;
  /**
   * Optional v1.1 pin state.
   *
   * - `"pinned"` → user explicitly pinned; the claim MUST NOT be auto-superseded.
   * - `"unpinned"` → explicit unpin (resets a previous pin).
   * - Undefined/omitted → field not emitted; receivers treat as unpinned.
   *
   * Callers are free to pass `"unpinned"` to create an explicit un-pin
   * supersede event, or to pass `undefined` to leave the field absent on a
   * non-pin write.
   */
  pinStatus?: PinStatus;
  /**
   * 3.3.1-rc.22 — optional embedding-model id stamped on the claim for
   * distillation forward-compat. See `BuildClaimV1Input.embeddingModelId`.
   */
  embeddingModelId?: string;
}

/**
 * Build a v1.1 canonical claim JSON string, validated through the core
 * `validateMemoryClaimV1` WASM export.
 *
 * Output is UTF-8 JSON ready for encryption as the inner blob of a
 * protobuf-v4 fact (outer `version = 4`). Field ordering follows the core
 * validator, so the result is byte-identical to what MCP's equivalent helper
 * produces for the same inputs (cross-client parity).
 *
 * Throws on malformed input (missing required field, invalid enum value).
 */
export function buildV1ClaimBlob(input: BuildV1ClaimBlobInput): string {
  if (!(VALID_MEMORY_SOURCES as readonly string[]).includes(input.source)) {
    throw new Error(`buildV1ClaimBlob: invalid source "${input.source}"`);
  }
  if (!isValidMemoryType(input.type)) {
    throw new Error(`buildV1ClaimBlob: invalid type "${input.type}"`);
  }

  const corePayload: Record<string, unknown> = {
    id: input.id ?? crypto.randomUUID(),
    text: input.text,
    type: input.type,
    source: input.source,
    created_at: input.createdAt ?? new Date().toISOString(),
  };

  if (input.scope && (VALID_MEMORY_SCOPES as readonly string[]).includes(input.scope)) {
    corePayload.scope = input.scope;
  }
  if (input.reasoning && input.reasoning.length > 0) {
    corePayload.reasoning = input.reasoning.slice(0, 256);
  }
  if (input.entities && input.entities.length > 0) {
    corePayload.entities = input.entities.slice(0, 8).map((e) => {
      const entity: Record<string, unknown> = { name: e.name, type: e.type };
      if (e.role) entity.role = e.role;
      return entity;
    });
  }
  if (typeof input.importance === 'number') {
    corePayload.importance = Math.max(1, Math.min(10, Math.round(input.importance)));
  }
  if (typeof input.confidence === 'number') {
    corePayload.confidence = Math.max(0, Math.min(1, input.confidence));
  }
  if (input.expiresAt) corePayload.expires_at = input.expiresAt;
  if (input.supersededBy) corePayload.superseded_by = input.supersededBy;
  if (input.pinStatus === 'pinned' || input.pinStatus === 'unpinned') {
    corePayload.pin_status = input.pinStatus;
  }

  // Validate via core — throws on invalid shape.
  const validated = getWasm().validateMemoryClaimV1(JSON.stringify(corePayload)) as string;
  const canonical = JSON.parse(validated) as Record<string, unknown>;
  canonical.schema_version = V1_SCHEMA_VERSION;
  if (input.volatility && (VALID_MEMORY_VOLATILITIES as readonly string[]).includes(input.volatility)) {
    canonical.volatility = input.volatility;
  }
  // 3.3.1-rc.22 — see `buildCanonicalClaimV1` comment.
  if (typeof input.embeddingModelId === 'string' && input.embeddingModelId.length > 0) {
    canonical.embedding_model_id = input.embeddingModelId;
  }
  return JSON.stringify(canonical);
}

/**
 * Normalize any type token (v0 or v1) to a v1 type. Uses the v0→v1 mapping
 * for legacy tokens; passes through when already v1.
 */
export function normalizeToV1Type(type: string): MemoryType {
  if (isValidMemoryType(type)) return type;
  return V0_TO_V1_TYPE[type as MemoryTypeV0] ?? 'claim';
}

/**
 * Heuristic: does a decrypted blob look like a v1 JSON payload?
 *
 * We check for the schema_version marker + the long-form `text` field.
 * Falls back false on any parse error.
 */
export function isV1Blob(decrypted: string): boolean {
  try {
    const obj = JSON.parse(decrypted) as Record<string, unknown>;
    return (
      typeof obj === 'object' &&
      obj !== null &&
      typeof obj.text === 'string' &&
      typeof obj.type === 'string' &&
      typeof obj.schema_version === 'string' &&
      obj.schema_version.startsWith('1.')
    );
  } catch {
    return false;
  }
}

/**
 * Parse a decrypted v1 blob into a structured object. Returns null if the
 * blob is not a v1 payload or fails validation.
 */
export interface V1BlobReadResult {
  text: string;
  type: MemoryTypeV1;
  source: MemorySource;
  scope: MemoryScope;
  volatility: MemoryVolatility;
  reasoning?: string;
  entities?: Array<{ name: string; type: string; role?: string }>;
  importance: number; // integer 1-10
  confidence: number; // 0-1
  createdAt: string;
  expiresAt?: string;
  supersededBy?: string;
  id?: string;
  /**
   * v1.1 pin state. Absent when the blob was written by a v1.0 client or
   * when the writer explicitly omitted the field (treated as `"unpinned"`).
   */
  pinStatus?: PinStatus;
  /**
   * 3.3.1-rc.22 — embedder identity tag. Absent on claims written by
   * older plugin versions. Forward-compat marker; consumers MAY use it
   * to decide whether a claim's stored embedding matches the active
   * embedder before letting cosine similarity make a relevance call.
   */
  embeddingModelId?: string;
}

export function readV1Blob(decrypted: string): V1BlobReadResult | null {
  try {
    const obj = JSON.parse(decrypted) as Record<string, unknown>;
    if (typeof obj.schema_version !== 'string' || !obj.schema_version.startsWith('1.')) {
      return null;
    }

    const text = typeof obj.text === 'string' ? obj.text : '';
    const rawType = typeof obj.type === 'string' ? obj.type : 'claim';
    const type: MemoryTypeV1 = isValidMemoryTypeV1(rawType) ? rawType : 'claim';

    const rawSource = typeof obj.source === 'string' ? obj.source : 'user-inferred';
    const source: MemorySource = (VALID_MEMORY_SOURCES as readonly string[]).includes(rawSource)
      ? (rawSource as MemorySource)
      : 'user-inferred';

    const rawScope = typeof obj.scope === 'string' ? obj.scope : 'unspecified';
    const scope: MemoryScope = (VALID_MEMORY_SCOPES as readonly string[]).includes(rawScope)
      ? (rawScope as MemoryScope)
      : 'unspecified';

    const rawVolatility = typeof obj.volatility === 'string' ? obj.volatility : 'updatable';
    const volatility: MemoryVolatility = (VALID_MEMORY_VOLATILITIES as readonly string[]).includes(rawVolatility)
      ? (rawVolatility as MemoryVolatility)
      : 'updatable';

    const impRaw = typeof obj.importance === 'number' ? obj.importance : 5;
    const importance = Math.max(1, Math.min(10, Math.round(impRaw)));

    const confRaw = typeof obj.confidence === 'number' ? obj.confidence : 0.85;
    const confidence = Math.max(0, Math.min(1, confRaw));

    const result: V1BlobReadResult = {
      text,
      type,
      source,
      scope,
      volatility,
      importance,
      confidence,
      createdAt: typeof obj.created_at === 'string' ? obj.created_at : '',
    };

    if (typeof obj.reasoning === 'string' && obj.reasoning.length > 0) {
      result.reasoning = obj.reasoning;
    }
    if (Array.isArray(obj.entities)) {
      result.entities = (obj.entities as unknown[]).filter(
        (e): e is { name: string; type: string; role?: string } =>
          !!e &&
          typeof e === 'object' &&
          typeof (e as { name?: unknown }).name === 'string' &&
          typeof (e as { type?: unknown }).type === 'string',
      ) as Array<{ name: string; type: string; role?: string }>;
    }
    if (typeof obj.expires_at === 'string') result.expiresAt = obj.expires_at;
    if (typeof obj.superseded_by === 'string') result.supersededBy = obj.superseded_by;
    if (typeof obj.id === 'string') result.id = obj.id;
    if (typeof obj.pin_status === 'string') {
      const ps = obj.pin_status;
      if (ps === 'pinned' || ps === 'unpinned') {
        result.pinStatus = ps;
      }
    }
    // 3.3.1-rc.22 — pull the embedder identity tag through. Plugin-only
    // field added by `buildCanonicalClaimV1` / `buildV1ClaimBlob` after
    // core validation.
    if (typeof obj.embedding_model_id === 'string' && obj.embedding_model_id.length > 0) {
      result.embeddingModelId = obj.embedding_model_id;
    }

    return result;
  } catch {
    return null;
  }
}

// Suppress unused-import lint warnings for VALID_MEMORY_TYPES_V1 — it is
// exported from extractor.ts for downstream clients and kept in scope here
// so future v1 helpers can reuse it without re-importing.
void VALID_MEMORY_TYPES_V1;

// ---------------------------------------------------------------------------
// Back-compat alias: buildCanonicalClaimRouted
//
// Plugin v3.0.0 removed the v0/v1 taxonomy toggle (`TOTALRECLAW_TAXONOMY_VERSION`
// env var) — all extraction + write paths emit v1 unconditionally. This
// alias is kept so any external caller that imports the Phase-3 rollout
// name keeps compiling; it simply forwards to `buildCanonicalClaim`.
//
// @deprecated Use `buildCanonicalClaim` directly.
// ---------------------------------------------------------------------------

export function buildCanonicalClaimRouted(input: BuildClaimInput): string {
  return buildCanonicalClaim(input);
}

// ---------------------------------------------------------------------------
// Digest helpers (Stage 3b read path)
// ---------------------------------------------------------------------------

/**
 * Well-known blind index marker used to locate digest claims on the subgraph.
 * Computed as plain SHA-256("type:digest") — same primitive as word trapdoors
 * so it lives in the existing `blindIndices` array. The `type:` namespace
 * prefix keeps it distinct from any user word trapdoor.
 */
export const DIGEST_TRAPDOOR: string = crypto
  .createHash('sha256')
  .update('type:digest')
  .digest('hex');

/** Compact category short key for digest claims (ClaimCategory::Digest). */
export const DIGEST_CATEGORY = 'dig';

/** Distinctive source marker so operators can grep for digest writes. */
export const DIGEST_SOURCE_AGENT = 'openclaw-plugin-digest';

/**
 * Hard ceiling on claim count for LLM-assisted digest compilation.
 * Above this, we skip the LLM entirely and use the template path to keep
 * token cost bounded. See plan §9 and Stage 3b design question #3.
 */
export const DIGEST_CLAIM_CAP = 200;

export type DigestMode = 'on' | 'off' | 'template';

/**
 * Digest injection is always ON in v1. The TOTALRECLAW_DIGEST_MODE env var
 * was removed — the G-pipeline ships a digest on every recall with an LLM
 * template fallback baked into the digest compiler. Kept as a function
 * returning `'on'` so legacy call-sites continue to compile.
 *
 * @deprecated v1 always returns `'on'`.
 */
export function resolveDigestMode(): DigestMode {
  return 'on';
}

// ---------------------------------------------------------------------------
// Auto-resolution mode — INTERNAL DEBUG KILL-SWITCH
//
// Not a user-facing env var. This is kept as an emergency off-switch for
// auto-contradiction-resolution if we have to disable it in production
// without a redeploy. It is NOT documented in the env var reference and
// MUST NOT be surfaced in any client README / SKILL.md.
//
// See `contradiction-sync.ts` for the read site.
// ---------------------------------------------------------------------------

export type AutoResolveMode = 'active' | 'off' | 'shadow';

/**
 * Internal kill-switch for the auto-resolution loop.
 *
 * - `active` (default, unset, unknown): full detection + auto-resolution.
 * - `off`: skip contradiction detection entirely; Phase 1 behaviour.
 * - `shadow`: detect + log decisions, but do not apply them (debug only).
 *
 * @internal Not public config — emergency kill-switch only.
 */
export function resolveAutoResolveMode(): AutoResolveMode {
  const raw = envStringLower('TOTALRECLAW_AUTO_RESOLVE_MODE');
  if (raw === 'off') return 'off';
  if (raw === 'shadow') return 'shadow';
  return 'active';
}

// ---------------------------------------------------------------------------
// Decrypted blob reader — handles both new Claim ({t,c,i,...}) and
// legacy {text, metadata: {importance: 0-1}} formats transparently.
// Any decrypt site should use this instead of parsing doc.text directly.
// ---------------------------------------------------------------------------

export interface BlobReadResult {
  text: string;
  importance: number; // integer 1-10
  category: string;
  metadata: Record<string, unknown>;
}

export function readClaimFromBlob(decryptedJson: string): BlobReadResult {
  try {
    const obj = JSON.parse(decryptedJson) as Record<string, unknown>;

    // v1 payload: long-form fields + schema_version "1.x"
    if (
      typeof obj.text === 'string' &&
      typeof obj.type === 'string' &&
      typeof obj.schema_version === 'string' &&
      obj.schema_version.startsWith('1.')
    ) {
      const importance = typeof obj.importance === 'number'
        ? Math.max(1, Math.min(10, Math.round(obj.importance)))
        : 5;
      return {
        text: obj.text,
        importance,
        category: mapTypeToCategory(obj.type as MemoryTypeV1),
        metadata: {
          type: obj.type,
          source: typeof obj.source === 'string' ? obj.source : 'user-inferred',
          scope: typeof obj.scope === 'string' ? obj.scope : 'unspecified',
          volatility: typeof obj.volatility === 'string' ? obj.volatility : 'updatable',
          reasoning: typeof obj.reasoning === 'string' ? obj.reasoning : undefined,
          // v1.1: surface pin_status verbatim for downstream (recall display +
          // export). Absent ⇒ undefined (receivers treat as "unpinned").
          pin_status: typeof obj.pin_status === 'string' ? obj.pin_status : undefined,
          importance: importance / 10,
          created_at: typeof obj.created_at === 'string' ? obj.created_at : '',
          schema_version: obj.schema_version,
        },
      };
    }

    // New canonical Claim format: short keys
    if (typeof obj.t === 'string' && typeof obj.c === 'string') {
      const importance = typeof obj.i === 'number' ? Math.max(1, Math.min(10, Math.round(obj.i))) : 5;
      return {
        text: obj.t,
        importance,
        category: obj.c,
        metadata: {
          type: obj.c,
          importance: importance / 10,
          source: typeof obj.sa === 'string' ? obj.sa : 'auto-extraction',
          created_at: typeof obj.ea === 'string' ? obj.ea : '',
        },
      };
    }
    // Legacy plugin {text, metadata: {importance: 0-1}} format
    if (typeof obj.text === 'string') {
      const meta = (obj.metadata as Record<string, unknown>) ?? {};
      const impFloat = typeof meta.importance === 'number' ? meta.importance : 0.5;
      const importance = Math.max(1, Math.min(10, Math.round(impFloat * 10)));
      return {
        text: obj.text,
        importance,
        category: typeof meta.type === 'string' ? meta.type : 'fact',
        metadata: meta,
      };
    }
  } catch {
    // fall through
  }
  return { text: decryptedJson, importance: 5, category: 'fact', metadata: {} };
}

export interface BuildDigestClaimInput {
  /** The full Digest JSON produced by buildTemplateDigest / assembleDigestFromLlm. */
  digestJson: string;
  /** ISO 8601 timestamp the digest was compiled at. Becomes the `ea` field. */
  compiledAt: string;
}

/**
 * Wrap a serialized Digest JSON as a canonical Claim so it can be encrypted
 * and stored on-chain via the same pipeline as regular facts.
 *
 * Stores the raw Digest JSON as the claim's `t` (text) field. Reader path
 * is `parseClaimOrLegacy(decrypted) → extractDigestFromClaim`.
 *
 * Digest claims deliberately carry no entity refs — otherwise entity
 * trapdoors would surface the digest blob in normal recall queries.
 */
export function buildDigestClaim(input: BuildDigestClaimInput): string {
  const { digestJson, compiledAt } = input;
  const claim = {
    t: digestJson,
    c: DIGEST_CATEGORY,
    cf: 1.0,
    i: 10,
    sa: DIGEST_SOURCE_AGENT,
    ea: compiledAt,
  };
  return getWasm().canonicalizeClaim(JSON.stringify(claim));
}

/**
 * Parse a canonical Claim JSON (produced by parseClaimOrLegacy) and, if it is
 * a digest claim, return the wrapped Digest object. Returns null if the claim
 * is not of category `dig` or if the inner JSON fails to parse.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function extractDigestFromClaim(canonicalClaimJson: string): any | null {
  let claim: { c?: string; t?: string };
  try {
    claim = JSON.parse(canonicalClaimJson);
  } catch {
    return null;
  }
  if (claim.c !== DIGEST_CATEGORY || typeof claim.t !== 'string') return null;
  try {
    const digest = JSON.parse(claim.t);
    // Minimal shape check: a Digest must at least have prompt_text.
    if (typeof digest !== 'object' || digest === null) return null;
    if (typeof digest.prompt_text !== 'string') return null;
    return digest;
  } catch {
    return null;
  }
}

/**
 * Lightweight check: does this decrypted blob look like a digest claim?
 * Used to filter digest blobs out of user-facing recall results.
 *
 * Accepts both canonical Claim JSON (`{c:"dig",...}`) and the already-parsed
 * form; returns false for legacy `{text, metadata}` docs and any parse error.
 */
export function isDigestBlob(decrypted: string): boolean {
  try {
    const obj = JSON.parse(decrypted);
    return obj && typeof obj === 'object' && obj.c === DIGEST_CATEGORY;
  } catch {
    return false;
  }
}

/**
 * Hours between two timestamps.
 *
 * Returns `Infinity` when `compiledAtIso` is unparseable (forces a recompile,
 * which is the safe default when we can't trust the stored timestamp). Returns
 * 0 for future dates (clock-skew defensive).
 */
export function hoursSince(compiledAtIso: string, nowMs: number): number {
  const then = Date.parse(compiledAtIso);
  if (Number.isNaN(then)) return Infinity;
  const deltaMs = nowMs - then;
  if (deltaMs <= 0) return 0;
  return deltaMs / (1000 * 60 * 60);
}

/**
 * The digest is stale if new claims have been written since it was compiled.
 * Both inputs are Unix seconds.
 *
 * Falsely-equal or regressing values (clock skew, empty vault) return false —
 * we only recompile on strictly-newer evidence.
 */
export function isDigestStale(
  digestVersion: number,
  currentMaxCreatedAtUnix: number,
): boolean {
  return currentMaxCreatedAtUnix > digestVersion;
}

export interface RecompileGuardInput {
  countNewClaims: number;
  hoursSinceCompilation: number;
}

/**
 * Recompile guard (plan §15.10):
 *   trigger if countNewClaims >= 10 OR hoursSinceCompilation >= 24.
 *
 * The caller is still responsible for the in-memory "in progress" flag
 * (see digest-sync.ts) — this is a pure predicate.
 */
export function shouldRecompile(input: RecompileGuardInput): boolean {
  const { countNewClaims, hoursSinceCompilation } = input;
  return countNewClaims >= 10 || hoursSinceCompilation >= 24;
}

// ---------------------------------------------------------------------------
// Entity trapdoors
// ---------------------------------------------------------------------------

/**
 * Compute a single entity trapdoor: sha256("entity:" + normalized_name) as hex.
 *
 * Uses the same primitive (plain SHA-256, not HMAC) as word / stem trapdoors in
 * `generateBlindIndices()`. The `entity:` prefix namespaces the result so a
 * user called "postgresql" never collides with the word trapdoor for the token
 * "postgresql". The search path must construct queries with the same prefix.
 *
 * Rationale for plain SHA-256 vs HMAC: the existing word trapdoor implementation
 * in `rust/totalreclaw-core/src/blind.rs` uses plain SHA-256 of the normalized
 * token (no dedup_key). For entity trapdoors to appear in the same blindIndices
 * array and be findable by the current search pipeline, they must use the same
 * primitive. Adopting HMAC for entities alone would break search consistency.
 */
export function computeEntityTrapdoor(name: string): string {
  const normalized = getWasm().normalizeEntityName(name);
  return crypto
    .createHash('sha256')
    .update('entity:' + normalized)
    .digest('hex');
}

/**
 * Compute entity trapdoors for every entity on a fact, deduplicated.
 * Returns an empty array when the fact has no entities.
 */
export function computeEntityTrapdoors(entities: readonly ExtractedEntity[] | undefined): string[] {
  if (!entities || entities.length === 0) return [];
  const seen = new Set<string>();
  const out: string[] = [];
  for (const e of entities) {
    const td = computeEntityTrapdoor(e.name);
    if (!seen.has(td)) {
      seen.add(td);
      out.push(td);
    }
  }
  return out;
}
