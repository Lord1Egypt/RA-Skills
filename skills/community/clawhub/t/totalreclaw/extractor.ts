/**
 * TotalReclaw Plugin - Fact Extractor
 *
 * Uses LLM calls to extract atomic facts from conversation messages.
 * Matches the extraction prompts described in SKILL.md.
 */

import { chatCompletion, resolveLLMConfig } from './llm-client.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ExtractionAction = 'ADD' | 'UPDATE' | 'DELETE' | 'NOOP';

export type EntityType = 'person' | 'project' | 'tool' | 'company' | 'concept' | 'place';

export interface ExtractedEntity {
  name: string;
  type: EntityType;
  role?: string;
}

// ---------------------------------------------------------------------------
// Memory Taxonomy v1 — the 6 canonical memory types. Single source of truth.
//
// Plugin v3.0.0 adopts v1 as the ONLY taxonomy. Legacy v0 tokens
// (fact, decision, episodic, goal, context, rule) are accepted only on the
// read-side via `LEGACY_V0_MEMORY_TYPES` / `V0_TO_V1_TYPE` and
// `normalizeToV1Type` in `claims-helper.ts`, so pre-v3 vault entries can
// still be decoded. Extraction and write paths emit v1 exclusively.
//
// When adding a new type, update ALL of:
//   - This constant
//   - `mcp/src/v1-types.ts`
//   - `python/src/totalreclaw/agent/extraction.py`
//   - `rust/totalreclaw-core/src/claims.rs`
//   - `skill/plugin/claims-helper.ts`
//   - The `EXTRACTION_SYSTEM_PROMPT` Types: list
// ---------------------------------------------------------------------------

export const VALID_MEMORY_TYPES = [
  'claim',
  'preference',
  'directive',
  'commitment',
  'episode',
  'summary',
] as const;

/** v1 MemoryType — the 6 canonical types. */
export type MemoryType = (typeof VALID_MEMORY_TYPES)[number];

/**
 * Runtime type guard — returns whether an unknown value is a valid v1
 * `MemoryType`. Legacy v0 tokens return `false`; use `normalizeToV1Type()`
 * in `claims-helper.ts` to coerce them on the read path.
 */
export function isValidMemoryType(value: unknown): value is MemoryType {
  return typeof value === 'string' && (VALID_MEMORY_TYPES as readonly string[]).includes(value);
}

/**
 * Backward-compat alias so existing consumers that import `MemoryTypeV1`
 * keep compiling. Identical to `MemoryType` as of plugin v3.0.0.
 * @deprecated Use `MemoryType` instead.
 */
export type MemoryTypeV1 = MemoryType;

/**
 * Backward-compat alias. Same list as `VALID_MEMORY_TYPES`.
 * @deprecated Use `VALID_MEMORY_TYPES` instead.
 */
export const VALID_MEMORY_TYPES_V1: readonly MemoryType[] = VALID_MEMORY_TYPES;

/**
 * Backward-compat alias. Same guard as `isValidMemoryType`.
 * @deprecated Use `isValidMemoryType` instead.
 */
export function isValidMemoryTypeV1(value: unknown): value is MemoryType {
  return isValidMemoryType(value);
}

/**
 * Legacy v0 memory types — retained as a typed constant so the read-side
 * `V0_TO_V1_TYPE` mapping can reference them without redeclaration.
 *
 * Do NOT emit these on the write/extraction path. They exist solely so
 * `claims-helper.ts::readClaimFromBlob` can decode pre-v1 vault entries
 * whose encrypted blobs still carry v0 token strings.
 */
export const LEGACY_V0_MEMORY_TYPES = [
  'fact',
  'preference',
  'decision',
  'episodic',
  'goal',
  'context',
  'summary',
  'rule',
] as const;

export type MemoryTypeV0 = (typeof LEGACY_V0_MEMORY_TYPES)[number];

export type MemorySource =
  | 'user'
  | 'user-inferred'
  | 'assistant'
  | 'external'
  | 'derived';

export type MemoryScope =
  | 'work'
  | 'personal'
  | 'health'
  | 'family'
  | 'creative'
  | 'finance'
  | 'misc'
  | 'unspecified';

export type MemoryVolatility = 'stable' | 'updatable' | 'ephemeral';

export const VALID_MEMORY_SOURCES: readonly MemorySource[] = [
  'user',
  'user-inferred',
  'assistant',
  'external',
  'derived',
];

export const VALID_MEMORY_SCOPES: readonly MemoryScope[] = [
  'work',
  'personal',
  'health',
  'family',
  'creative',
  'finance',
  'misc',
  'unspecified',
];

export const VALID_MEMORY_VOLATILITIES: readonly MemoryVolatility[] = [
  'stable',
  'updatable',
  'ephemeral',
];

/**
 * Legacy v0 → v1 type mapping used by the read-side adapter when decoding
 * a pre-v1 vault entry that still carries a v0 token string.
 *
 * Decisions (v0) map to v1 `claim` — the reasoning lives in the separate
 * `reasoning` field rather than being encoded in the type.
 */
export const V0_TO_V1_TYPE: Record<MemoryTypeV0, MemoryType> = {
  fact: 'claim',
  preference: 'preference',
  decision: 'claim',
  episodic: 'episode',
  goal: 'commitment',
  context: 'claim',
  summary: 'summary',
  rule: 'directive',
};

// ---------------------------------------------------------------------------
// ExtractedFact — canonical shape carried through the extraction pipeline
// ---------------------------------------------------------------------------

/**
 * Extracted fact. Shape carries full v1 taxonomy fields (source / scope /
 * reasoning / volatility). `source` is required on the write path —
 * `storeExtractedFacts` supplies `'user-inferred'` as a defensive default
 * when a heuristic upstream fails to populate it.
 */
export interface ExtractedFact {
  text: string;
  /** v1 taxonomy type. Always present on newly-extracted facts. */
  type: MemoryType;
  importance: number; // 1-10
  action: ExtractionAction;
  existingFactId?: string;
  entities?: ExtractedEntity[];
  confidence?: number; // 0.0-1.0, LLM self-assessed
  /**
   * v1 provenance tag. Required on the write path — when missing,
   * `storeExtractedFacts` supplies `'user-inferred'` as a defensive default.
   */
  source?: MemorySource;
  /** v1 life-domain scope. Default 'unspecified'. */
  scope?: MemoryScope;
  /**
   * Decision-with-reasoning "because Y" clause, for type=claim. Max 256 chars.
   */
  reasoning?: string;
  /**
   * v1 stability signal. Assigned by `comparativeRescoreV1` or, when rescore
   * is skipped (facts.length < 5), by the `defaultVolatility` heuristic.
   */
  volatility?: MemoryVolatility;
  /**
   * am-1: Crystal-shaped debrief structured metadata. When present,
   * re-attached as `metadata` on the v1 blob after core validation.
   * Only set on Crystal debrief facts (type='summary', source='derived').
   */
  crystalMetadata?: CrystalMetadata;
}

/** Structured metadata for a Crystal-shaped session summary (am-1). */
export interface CrystalMetadata {
  subtype: 'session_crystal';
  key_outcomes: string[];
  open_threads: string[];
  lessons: string[];
  session_id?: string;
  source_message_ids?: string[];
  files_affected?: string[];    // coding hosts (OpenClaw, MCP)
  topics_discussed?: string[];  // chat hosts (Hermes, NanoClaw)
}

const ALLOWED_ENTITY_TYPES: ReadonlySet<EntityType> = new Set([
  'person',
  'project',
  'tool',
  'company',
  'concept',
  'place',
]);

/**
 * Default confidence when the LLM does not provide one.
 * Mirrors the fallback used by other extraction clients.
 */
export const DEFAULT_EXTRACTION_CONFIDENCE = 0.85;

interface ContentBlock {
  type?: string;
  text?: string;
  thinking?: string;
}

interface ConversationMessage {
  role?: string;
  content?: string | ContentBlock[];
  text?: string;
}


// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Extract text content from a conversation message (handles various formats).
 *
 * OpenClaw AgentMessage objects use content arrays:
 *   { role: "user", content: [{ type: "text", text: "..." }] }
 *   { role: "assistant", content: [{ type: "text", text: "..." }, { type: "toolCall", ... }] }
 *
 * We also handle the simpler { role, content: "string" } format.
 */
function messageToText(msg: unknown): { role: string; content: string } | null {
  if (!msg || typeof msg !== 'object') return null;

  const m = msg as ConversationMessage;
  const role = m.role ?? 'unknown';

  // Only keep user and assistant messages
  if (role !== 'user' && role !== 'assistant') return null;

  let textContent: string;

  if (typeof m.content === 'string') {
    // Simple string content
    textContent = m.content;
  } else if (Array.isArray(m.content)) {
    // OpenClaw AgentMessage format: array of content blocks
    // Extract text from { type: "text", text: "..." } blocks
    const textParts = (m.content as ContentBlock[])
      .filter((block) => block.type === 'text' && typeof block.text === 'string')
      .map((block) => block.text as string);
    textContent = textParts.join('\n');
  } else if (typeof m.text === 'string') {
    // Fallback: { text: "..." } field
    textContent = m.text;
  } else {
    return null;
  }

  if (textContent.length < 3) return null;

  return { role, content: textContent };
}

/**
 * Truncate messages to fit within a token budget (rough estimate: 4 chars per token).
 */
function truncateMessages(messages: Array<{ role: string; content: string }>, maxChars: number): string {
  const lines: string[] = [];
  let totalChars = 0;

  for (const msg of messages) {
    const line = `[${msg.role}]: ${msg.content}`;
    if (totalChars + line.length > maxChars) break;
    lines.push(line);
    totalChars += line.length;
  }

  return lines.join('\n\n');
}

/**
 * Parse a single entity object from LLM output. Returns null if invalid.
 * Invalid entities are silently dropped so a bad entity never fails the whole fact.
 */
export function parseEntity(raw: unknown): ExtractedEntity | null {
  if (!raw || typeof raw !== 'object') return null;
  const e = raw as Record<string, unknown>;
  const name = typeof e.name === 'string' ? e.name.trim() : '';
  if (name.length === 0) return null;
  const type = String(e.type ?? '').toLowerCase() as EntityType;
  if (!ALLOWED_ENTITY_TYPES.has(type)) return null;
  const entity: ExtractedEntity = { name: name.slice(0, 128), type };
  if (typeof e.role === 'string' && e.role.trim().length > 0) {
    entity.role = e.role.trim().slice(0, 128);
  }
  return entity;
}

/**
 * Clamp a raw confidence value to [0, 1]. Returns the default when missing or NaN.
 */
export function normalizeConfidence(raw: unknown): number {
  if (typeof raw !== 'number' || !Number.isFinite(raw)) return DEFAULT_EXTRACTION_CONFIDENCE;
  if (raw < 0) return 0;
  if (raw > 1) return 1;
  return raw;
}

/**
 * Minimal logger shape accepted by the extraction pipeline. Matches the
 * OpenClaw plugin logger so callers can pass `api.logger` directly.
 *
 * All methods are optional so tests can pass a partial object and callers
 * that don't care about observability can omit the argument entirely.
 */
export interface ExtractorLogger {
  info?: (msg: string) => void;
  warn?: (msg: string) => void;
}


// ---------------------------------------------------------------------------
// Phase 2.2.6: lexical importance bumps
// ---------------------------------------------------------------------------

/**
 * Escape regex metacharacters so a string can be used as a literal pattern.
 */
function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Compute a lexical importance bump (0-2) for a single fact based on signals
 * in the surrounding conversation text.
 *
 * This is a Phase 2.2.6 quality fix complementing the prompt rubric tightening
 * (item A). Where the rubric tells the LLM to use the full 1-10 range, the
 * bump tells us *as a post-process*: when the user's actual phrasing carries
 * strong "remember this" signals that the LLM may have under-weighted, push
 * the score up.
 *
 * Signals detected (each adds +1, capped at +2 total):
 *
 *   1. **Strong intent phrases** anywhere in the conversation:
 *      "remember this", "never forget", "rule of thumb", "critical",
 *      "don't ever forget", explicit "always X" / "never Y" patterns.
 *   2. **Emphasis markers**: `!!` (double exclamation), or 3+ all-caps words
 *      in a row (e.g. "DO NOT FORGET", "VERY IMPORTANT").
 *   3. **Repetition**: the fact's first ~20 chars appear at least twice in
 *      the conversation text (paraphrased restating).
 *
 * The bump is additive on top of whatever the LLM scored; final importance
 * is capped at 10.
 *
 * Final-importance ceiling: this never makes a fact pass the importance >= 6
 * filter on its own — a fact still needs to have an LLM score >= 5 (because
 * +2 from 5 = 7, above floor; +1 from 5 = 6, above floor). This is intentional:
 * the bump is for "the LLM correctly identified this as worth storing but
 * under-weighted it", not "the LLM said skip but we're overriding."
 */
export function computeLexicalImportanceBump(
  factText: string,
  conversationText: string,
): number {
  let bump = 0;
  const lowerConv = conversationText.toLowerCase();

  // Signal 1: strong intent phrases anywhere in the conversation
  const strongIntent =
    /\b(remember this|never forget|rule of thumb|don't (?:ever )?forget|critical|important|gotcha|note to self)\b/i;
  if (strongIntent.test(lowerConv)) bump += 1;

  // Signal 2: emphasis markers — double exclamation OR 3+ consecutive all-caps words
  // (3+ chars each, to avoid false positives on acronyms like "AWS S3 IAM")
  const doubleExclamation = /!!/;
  const allCapsPhrase = /\b[A-Z]{3,}(?:\s+[A-Z]{3,}){2,}\b/;
  if (doubleExclamation.test(conversationText) || allCapsPhrase.test(conversationText)) {
    bump += 1;
  }

  // Signal 3: repetition — extract content words (length >= 5, not common stop
  // words) from the fact, and check if any single one appears 2+ times in the
  // conversation. This is more robust to LLM paraphrasing than a fingerprint
  // match: "User prefers PostgreSQL" extracted from "I prefer PostgreSQL ...
  // yeah PostgreSQL is right for OLTP" still triggers because "postgresql"
  // appears multiple times even though the leading chars differ.
  const lowerFact = factText.toLowerCase();
  const stopWords = new Set([
    'about', 'after', 'again', 'against', 'because', 'before', 'being',
    'between', 'could', 'doing', 'during', 'every', 'further', 'having',
    'their', 'these', 'those', 'through', 'under', 'until', 'where', 'which',
    'while', 'would', 'should', 'about', 'thing', 'things', 'something',
    'someone', 'always', 'never', 'often', 'still', 'really', 'maybe',
    'using', 'works', 'work', 'user', 'users', 'with', 'from', 'into',
    'like', 'just', 'than', 'them', 'they', 'will', 'when', 'what', 'were',
    'this', 'that', 'have', 'this',
  ]);
  const factWords = lowerFact.split(/[^a-z0-9_]+/).filter((w) => w.length >= 5 && !stopWords.has(w));
  let triggered = false;
  for (const word of factWords) {
    const occurrences = (lowerConv.match(new RegExp(`\\b${escapeRegExp(word)}\\b`, 'g')) || [])
      .length;
    if (occurrences >= 2) {
      triggered = true;
      break;
    }
  }
  if (triggered) bump += 1;

  return Math.min(bump, 2);
}


// ---------------------------------------------------------------------------
// Compaction-Aware Extraction (Phase 2.3)
// ---------------------------------------------------------------------------

/**
 * Compaction-specific system prompt (v1 taxonomy). Fires when the conversation
 * context is about to be compacted. LAST CHANCE to capture knowledge before
 * it is lost, so the importance floor is 5 instead of 6 and the prompt is
 * more aggressive about extracting active-project context, claims, and
 * episodes.
 *
 * Differences from `EXTRACTION_SYSTEM_PROMPT`:
 *   - Opening framing emphasizes urgency ("last chance")
 *   - Format-agnostic: handles bullet lists, prose, mixed formats
 *   - Importance threshold lowered to 5
 *   - More aggressive on claim / episode / directive types
 *   - Anti-pattern: don't skip content just because it's in a summary
 *
 * Output format matches `EXTRACTION_SYSTEM_PROMPT` exactly (same merged
 * topics+facts JSON shape with v1 type / source / scope fields), so the
 * same `parseMergedResponseV1` parser can validate it.
 */
export const COMPACTION_SYSTEM_PROMPT = `You are extracting memories from a conversation that is about to be compacted. The context will be LOST after this point — this is your LAST CHANCE to capture everything worth remembering. Be more aggressive than usual: err on the side of storing.

Work in TWO explicit phases within one response:

PHASE 1 — Topic identification.
Identify the 2-3 main topics the user was engaging with before extracting any fact. Topics should be short phrases (2-5 words each). If there's no clear user-focused topic, use an empty topics array.

PHASE 2 — Fact extraction anchored to those topics (plus preserve active context).
Extract valuable memories. Prefer facts that directly relate to the identified topics (importance 7-9 range). Active project context, decisions in progress, and current working state score 6-8 during compaction — capture them even when they'd normally be marginal.

Rules:
1. Each memory = single self-contained piece of information
2. Focus on user-specific info useful in future conversations
3. Skip generic knowledge, greetings, small talk
4. Score importance 1-10 (5+ = worth storing during compaction)
5. Every memory MUST attribute a source (provenance critical)

Importance rubric (full 1-10 range, NOT just 7-8):
- 10: Core identity, never-forget ("remember this forever", name/birthday)
- 9: Affects many future decisions / high-impact rules
- 8: Preference / decision-with-reasoning / operational rule
- 7: Specific durable fact
- 6: Borderline — during compaction, capture anyway
- 5: Would normally drop; keep as compaction safety net
- 4 or below: DROP (greetings, filler)

═══════════════════════════════════════════════════════════════
TYPE (6 values)
═══════════════════════════════════════════════════════════════
- claim: factual assertion (absorbs v0 fact/context/decision; decisions populate reasoning)
- preference: likes/dislikes/tastes
- directive: imperative rule ("always X", "never Y")
- commitment: future intent ("will do X")
- episode: notable event
- summary: derived synthesis (source must be derived|assistant)

═══════════════════════════════════════════════════════════════
SOURCE (provenance, CRITICAL)
═══════════════════════════════════════════════════════════════
- user: user explicitly stated it (in [user]: turns)
- user-inferred: extractor inferred from user signals
- assistant: assistant authored — DOWNGRADE unless user affirmed/quoted
- external, derived: rare

IF fact substance appears ONLY in [assistant]: turns without user affirmation → source:assistant.

═══════════════════════════════════════════════════════════════
SCOPE
═══════════════════════════════════════════════════════════════
work | personal | health | family | creative | finance | misc | unspecified

═══════════════════════════════════════════════════════════════
ENTITIES
═══════════════════════════════════════════════════════════════
- type ∈ {person, project, tool, company, concept, place}
- prefer specific names ("PostgreSQL" not "database")
- omit umbrella categories when specific name is present

═══════════════════════════════════════════════════════════════
REASONING (only for claims that are decisions)
═══════════════════════════════════════════════════════════════
For type=claim where the user expressed a decision-with-reasoning, populate "reasoning" with the WHY clause.

═══════════════════════════════════════════════════════════════
FORMAT-AGNOSTIC PARSING (IMPORTANT)
═══════════════════════════════════════════════════════════════
The conversation may contain bullet lists, numbered lists, section headers, code snippets, or plain prose. Treat ALL formats as potential sources of extractable memory:
- Bullets/list items: each item is a candidate.
- Section headers (Context, Decisions, Key Learnings, Open Questions): use the header as a TYPE HINT (Context → claim, Decisions → claim+reasoning, Learnings → directive, Open Questions → commitment).
- Plain prose: parse each distinct assertion as a candidate.
- Code snippets: extract config choices, tool versions, architectural decisions embedded in comments or structure.
- Mixed format: apply all of the above.

Do NOT skip content just because it's in a summary. The agent has already filtered — your job is to convert into structured memories, not to re-evaluate worth.

═══════════════════════════════════════════════════════════════
OUTPUT FORMAT (no markdown, no code fences)
═══════════════════════════════════════════════════════════════
{
  "topics": ["topic 1", "topic 2"],
  "facts": [
    {
      "text": "...",
      "type": "claim|preference|directive|commitment|episode",
      "source": "user|user-inferred|assistant",
      "scope": "work|personal|health|...",
      "importance": N,
      "confidence": 0.9,
      "action": "ADD",
      "reasoning": "...",    // optional, only for claim+decision
      "entities": [{"name": "...", "type": "tool"}]
    }
  ]
}

If nothing worth extracting: {"topics": [], "facts": []}`;

/**
 * Parse facts for compaction context (v1 taxonomy; importance floor 5).
 *
 * Identical to `parseFactsResponse` except the importance floor is 5 instead
 * of 6 — compaction is the last chance to capture context, so we accept
 * borderline facts that would normally be dropped.
 *
 * Accepts the same merged-topic v1 JSON shape as the main prompt. The
 * inner `parseMergedResponseV1` enforces the >=6 floor, so we re-run a
 * lenient >=5 pass on the raw parsed payload to admit the borderline items.
 */
export function parseFactsResponseForCompaction(
  response: string,
  logger?: ExtractorLogger,
): ExtractedFact[] {
  const originalPreview = response.trim().slice(0, 200);
  let cleaned = response.trim();

  // Strip <think>...</think> and <thinking>...</thinking> tags
  cleaned = cleaned
    .replace(/<think(?:ing)?>[\s\S]*?<\/think(?:ing)?>/gi, '')
    .trim();

  // Strip markdown code fences if present
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }

  const tryParse = (input: string): unknown => {
    try {
      return JSON.parse(input);
    } catch {
      return undefined;
    }
  };

  let parsed = tryParse(cleaned);
  let recoveryUsed: 'none' | 'bracket-scan' = 'none';
  if (parsed === undefined) {
    // Try bare-array first (legacy compaction output), then object (v1 merged).
    const arrMatch = cleaned.match(/\[[\s\S]*\]/);
    if (arrMatch) {
      parsed = tryParse(arrMatch[0]);
      if (parsed !== undefined) recoveryUsed = 'bracket-scan';
    }
    if (parsed === undefined) {
      const objMatch = cleaned.match(/\{[\s\S]*\}/);
      if (objMatch) {
        parsed = tryParse(objMatch[0]);
        if (parsed !== undefined) recoveryUsed = 'bracket-scan';
      }
    }
  }
  if (recoveryUsed === 'bracket-scan') {
    logger?.info?.(
      `parseFactsResponseForCompaction: recovered JSON via bracket-scan fallback`,
    );
  }

  if (!parsed || typeof parsed !== 'object') {
    logger?.warn?.(
      `parseFactsResponseForCompaction: could not parse LLM output as JSON object. Preview: ${JSON.stringify(originalPreview)}`,
    );
    return [];
  }

  const obj = parsed as Record<string, unknown>;
  const rawFacts = Array.isArray(obj.facts) ? (obj.facts as unknown[]) : null;

  // Legacy v0 compaction output (bare JSON array) — best-effort parse.
  const rawArray = rawFacts ?? (Array.isArray(parsed) ? (parsed as unknown[]) : null);
  if (!rawArray) {
    logger?.warn?.(
      `parseFactsResponseForCompaction: expected { facts: [...] } object, got ${typeof parsed}`,
    );
    return [];
  }

  const validActions: ExtractionAction[] = ['ADD', 'UPDATE', 'DELETE', 'NOOP'];

  const facts = rawArray
    .filter(
      (f): f is Record<string, unknown> =>
        !!f &&
        typeof f === 'object' &&
        typeof (f as Record<string, unknown>).text === 'string' &&
        ((f as Record<string, unknown>).text as string).length >= 5,
    )
    .map((f) => {
      const rawType = String(f.type ?? 'claim').toLowerCase();
      // Accept v1 tokens directly; coerce legacy v0 tokens via V0_TO_V1_TYPE.
      let type: MemoryType;
      if (isValidMemoryType(rawType)) {
        type = rawType;
      } else if ((LEGACY_V0_MEMORY_TYPES as readonly string[]).includes(rawType)) {
        type = V0_TO_V1_TYPE[rawType as MemoryTypeV0];
      } else {
        type = 'claim';
      }

      const rawSource = String(f.source ?? 'user-inferred').toLowerCase();
      const source: MemorySource = (VALID_MEMORY_SOURCES as readonly string[]).includes(rawSource)
        ? (rawSource as MemorySource)
        : 'user-inferred';

      const rawScope = String(f.scope ?? 'unspecified').toLowerCase();
      const scope: MemoryScope = (VALID_MEMORY_SCOPES as readonly string[]).includes(rawScope)
        ? (rawScope as MemoryScope)
        : 'unspecified';

      const reasoning = typeof f.reasoning === 'string' ? f.reasoning.slice(0, 256) : undefined;

      const action = validActions.includes(String(f.action) as ExtractionAction)
        ? (String(f.action) as ExtractionAction)
        : 'ADD';

      let entities: ExtractedEntity[] | undefined;
      if (Array.isArray(f.entities)) {
        const valid = (f.entities as unknown[])
          .map(parseEntity)
          .filter((e): e is ExtractedEntity => e !== null);
        if (valid.length > 0) entities = valid;
      }

      const result: ExtractedFact = {
        text: String(f.text).slice(0, 512),
        type,
        source,
        scope,
        reasoning,
        importance: Math.max(1, Math.min(10, Number(f.importance) || 5)),
        action,
        existingFactId: typeof f.existingFactId === 'string' ? f.existingFactId : undefined,
        confidence: normalizeConfidence(f.confidence),
      };
      if (entities) result.entities = entities;
      return result;
    })
    // Reject illegal type:summary + source:user
    .filter((f) => !(f.type === 'summary' && f.source === 'user'))
    // Compaction: importance >= 5 (not 6)
    .filter((f) => f.importance >= 5 || f.action === 'DELETE');

  return facts;
}

/**
 * Extract facts using the compaction-aware prompt.
 *
 * This is called from the `before_compaction` hook — the LAST CHANCE to
 * capture knowledge before conversation context is lost. Key differences
 * from `extractFacts`:
 *   - Uses `COMPACTION_SYSTEM_PROMPT` (lower threshold, format-agnostic, more aggressive)
 *   - Always processes the full conversation (`mode: 'full'`)
 *   - Importance filter is >= 5 instead of >= 6
 *   - Lexical importance bumps still apply
 *
 * @param rawMessages - The messages array from the hook event (unknown[])
 * @param existingMemories - Optional list of existing memories for dedup context
 * @param logger - Optional logger for observability
 * @returns Array of extracted facts, or empty array on failure.
 */
export async function extractFactsForCompaction(
  rawMessages: unknown[],
  existingMemories?: Array<{ id: string; text: string }>,
  logger?: ExtractorLogger,
): Promise<ExtractedFact[]> {
  const config = resolveLLMConfig();
  if (!config) {
    logger?.info?.('extractFactsForCompaction: no LLM config resolved (skipping extraction)');
    return [];
  }

  // Parse messages
  const parsed = rawMessages
    .map(messageToText)
    .filter((m): m is { role: string; content: string } => m !== null);

  if (parsed.length === 0) {
    logger?.info?.(`extractFactsForCompaction: no parseable messages (raw count=${rawMessages.length})`);
    return [];
  }

  // Always full mode — process entire conversation for compaction
  const conversationText = truncateMessages(parsed, 12_000);

  if (conversationText.length < 20) {
    logger?.info?.(
      `extractFactsForCompaction: conversation too short (${conversationText.length} chars < 20)`,
    );
    return [];
  }

  // Build existing memories context if available
  let memoriesContext = '';
  if (existingMemories && existingMemories.length > 0) {
    const memoriesStr = existingMemories
      .map((m) => `[ID: ${m.id}] ${m.text}`)
      .join('\n');
    memoriesContext = `\n\nExisting memories (use these for dedup — classify as UPDATE/DELETE/NOOP if they conflict or overlap):\n${memoriesStr}`;
  }

  const userPrompt = `Extract ALL valuable long-term memories from this conversation before it is compacted and lost:\n\n${conversationText}${memoriesContext}`;

  let response: string | null | undefined;
  try {
    response = await chatCompletion(config, [
      { role: 'system', content: COMPACTION_SYSTEM_PROMPT },
      { role: 'user', content: userPrompt },
    ], {
      // 3.3.1-rc.2: retry transient 429 / timeout (same policy as extractFacts).
      retry: { attempts: 3, baseDelayMs: 1000 },
      timeoutMs: 30_000,
      logger,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger?.warn?.(`extractFactsForCompaction: chatCompletion threw: ${msg}`);
    return [];
  }

  if (!response) {
    logger?.info?.('extractFactsForCompaction: chatCompletion returned null/empty response');
    return [];
  }

  logger?.info?.(
    `extractFactsForCompaction: LLM returned ${response.length} chars; handing to parseFactsResponseForCompaction`,
  );
  let facts = parseFactsResponseForCompaction(response, logger);

  // v1 provenance filter (tag-don't-drop). Uses importance >= 5 floor because
  // the filter's own floor is 5 in lax mode, matching compaction semantics.
  facts = applyProvenanceFilterLax(facts, conversationText);

  // Comparative rescore if >= 5 facts (same as default pipeline), else
  // assign defaultVolatility so v1 write path has a value.
  facts = await comparativeRescoreV1(facts, conversationText, logger);
  facts = facts.map((f) => ({ ...f, volatility: f.volatility ?? defaultVolatility(f) }));

  // Lexical importance bumps (same as regular extraction)
  for (const f of facts) {
    const bump = computeLexicalImportanceBump(f.text, conversationText);
    if (bump > 0) {
      const oldImportance = f.importance;
      const effectiveBump = f.importance >= 8 ? Math.min(bump, 1) : bump;
      f.importance = Math.min(10, f.importance + effectiveBump);
      logger?.info?.(
        `extractFactsForCompaction: lexical bump +${bump} for "${f.text.slice(0, 60)}..." (${oldImportance} → ${f.importance})`,
      );
    }
  }

  return facts;
}

// ---------------------------------------------------------------------------
// Debrief Extraction
// ---------------------------------------------------------------------------

/**
 * Canonical debrief system prompt — must be identical across all clients.
 */
export const DEBRIEF_SYSTEM_PROMPT = `You are reviewing a conversation that just ended. The following facts were
already extracted and stored during this conversation:

{already_stored_facts}

Your job is to capture what turn-by-turn extraction MISSED. Focus on:

1. **Broader context** — What was the conversation about overall? What project,
   problem, or topic tied the discussion together?
2. **Outcomes & conclusions** — What was decided, agreed upon, or resolved?
3. **What was attempted** — What approaches were tried? What worked, what didn't, and why?
4. **Relationships** — How do topics discussed relate to each other or to things
   from previous conversations?
5. **Open threads** — What was left unfinished or needs follow-up?

Do NOT repeat facts already stored. Only add genuinely new information that provides
broader context a future conversation would benefit from.

Return a JSON array (no markdown, no code fences):
[{"text": "...", "type": "summary|context", "importance": N}]

- Use type "summary" for conclusions, outcomes, and decisions-of-the-session
- Use type "context" for broader project context, open threads, and what-was-tried
- Importance 7-8 for most debrief items (they are high-value by definition)
- Maximum 5 items (debriefs should be concise, not exhaustive)
- Each item should be 1-3 sentences, self-contained

If the conversation was too short or trivial to warrant a debrief, return: []`;

export interface DebriefItem {
  text: string;
  type: 'summary' | 'context';
  importance: number;
}

/**
 * Parse a debrief response into validated DebriefItems.
 */
export function parseDebriefResponse(response: string): DebriefItem[] {
  let cleaned = response.trim();
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }

  try {
    const parsed = JSON.parse(cleaned);
    if (!Array.isArray(parsed)) return [];

    return parsed
      .filter(
        (item: unknown) =>
          item &&
          typeof item === 'object' &&
          typeof (item as Record<string, unknown>).text === 'string' &&
          ((item as Record<string, unknown>).text as string).length >= 5,
      )
      .map((item: unknown) => {
        const d = item as Record<string, unknown>;
        const type: 'summary' | 'context' = d.type === 'summary' ? 'summary' : 'context';
        const rawImportance = typeof d.importance === 'number' ? d.importance : 7;
        const importance = Math.max(1, Math.min(10, rawImportance));
        return { text: String(d.text).slice(0, 512), type, importance };
      })
      .filter((d) => d.importance >= 6)
      .slice(0, 5);
  } catch {
    return [];
  }
}

/**
 * Extract a session debrief using LLM.
 *
 * @param rawMessages - All messages from the session
 * @param storedFactTexts - Texts of facts already stored in this session (for dedup)
 * @returns Array of debrief items, or empty array on failure
 */
export async function extractDebrief(
  rawMessages: unknown[],
  storedFactTexts: string[],
): Promise<DebriefItem[]> {
  const config = resolveLLMConfig();
  if (!config) return [];

  const parsed = rawMessages
    .map(messageToText)
    .filter((m): m is { role: string; content: string } => m !== null);

  // Minimum 4 turns (8 messages) to warrant a debrief
  if (parsed.length < 8) return [];

  const conversationText = truncateMessages(parsed, 12_000);
  if (conversationText.length < 20) return [];

  const alreadyStored = storedFactTexts.length > 0
    ? storedFactTexts.map((t) => `- ${t}`).join('\n')
    : '(none)';

  const systemPrompt = DEBRIEF_SYSTEM_PROMPT.replace('{already_stored_facts}', alreadyStored);

  try {
    const response = await chatCompletion(config, [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Review this conversation and provide a debrief:\n\n${conversationText}` },
    ], {
      // 3.3.1-rc.2: retry transient 429 / timeout.
      retry: { attempts: 3, baseDelayMs: 1000 },
      timeoutMs: 30_000,
    });

    if (!response) return [];
    return parseDebriefResponse(response);
  } catch {
    return [];
  }
}

// ---------------------------------------------------------------------------
// Crystal-shaped debrief (am-1) — one structured summary per session
// ---------------------------------------------------------------------------

const _CRYSTAL_COMMON_FIELDS = `Return a JSON object (no markdown, no code fences):
{
  "narrative": "1-2 sentence summary of what happened this session",
  "key_outcomes": ["outcome or decision 1", "outcome or decision 2"],
  "open_threads": ["unfinished item 1"],
  "lessons": ["lesson or gotcha 1"],
  "importance": 8
}`;

export const CRYSTAL_SYSTEM_PROMPT_CHAT = `You are crystallising a finished conversation into one structured session summary.

The following facts were already extracted and stored during this conversation:
{already_stored_facts}

Write ONE Crystal that captures what turn-by-turn extraction missed. Include:
- narrative: 1-2 sentences describing the conversation overall
- key_outcomes: decisions made, problems solved, conclusions reached
- open_threads: things left unfinished or needing follow-up
- lessons: patterns, gotchas, or insights worth remembering
- topics_discussed: the main subjects covered
- importance: 7-10 (8 default)

Do NOT repeat facts already stored. Return null for trivial or very short conversations.

${_CRYSTAL_COMMON_FIELDS}

Also include "topics_discussed": ["topic 1", "topic 2"] in the object.
Return null (not an object) for trivial or very short conversations.`;

export const CRYSTAL_SYSTEM_PROMPT_CODING = `You are crystallising a finished coding session into one structured session summary.

The following facts were already extracted and stored during this conversation:
{already_stored_facts}

Write ONE Crystal that captures what turn-by-turn extraction missed. Include:
- narrative: 1-2 sentences describing the session overall
- key_outcomes: decisions made, bugs fixed, features built
- open_threads: things left unfinished or needing follow-up
- lessons: patterns, gotchas, or insights worth remembering
- files_affected: file paths mentioned or worked on (extract from assistant messages)
- importance: 7-10 (8 default)

Do NOT repeat facts already stored. Return null for trivial or very short sessions.

${_CRYSTAL_COMMON_FIELDS}

Also include "files_affected": ["/path/to/file.ts", ...] in the object (may be []).
Return null (not an object) for trivial or very short sessions.`;

/** Parse an LLM Crystal response into a CrystalMetadata + narrative pair. */
export function parseCrystalResponse(
  response: string,
  hostType: 'chat' | 'coding' = 'chat',
): { narrative: string; importance: number; metadata: CrystalMetadata } | null {
  let cleaned = response.trim();
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }
  if (cleaned.toLowerCase() === 'null' || cleaned === '') return null;

  let parsed: unknown;
  try {
    parsed = JSON.parse(cleaned);
  } catch {
    return null;
  }

  if (parsed === null) return null;
  if (typeof parsed !== 'object' || Array.isArray(parsed)) return null;

  const d = parsed as Record<string, unknown>;
  const narrative = typeof d.narrative === 'string' ? d.narrative.trim().slice(0, 512) : '';
  if (narrative.length < 10) return null;

  const strList = (key: string): string[] => {
    const raw = d[key];
    if (!Array.isArray(raw)) return [];
    return raw.map((x) => String(x).trim()).filter((x) => x.length > 0).slice(0, 10);
  };

  let importance = typeof d.importance === 'number' ? d.importance : 8;
  importance = Math.max(1, Math.min(10, Math.round(importance)));

  const metadata: CrystalMetadata = {
    subtype: 'session_crystal',
    key_outcomes: strList('key_outcomes'),
    open_threads: strList('open_threads'),
    lessons: strList('lessons'),
  };
  if (hostType === 'coding') {
    metadata.files_affected = strList('files_affected');
  } else {
    metadata.topics_discussed = strList('topics_discussed');
  }

  return { narrative, importance, metadata };
}

/**
 * Extract a Crystal session summary using LLM.
 *
 * Returns null if LLM unavailable, session too short, or LLM returns null.
 */
export async function extractCrystal(
  rawMessages: unknown[],
  storedFactTexts: string[],
  hostType: 'chat' | 'coding' = 'coding',
): Promise<{ narrative: string; importance: number; metadata: CrystalMetadata } | null> {
  const config = resolveLLMConfig();
  if (!config) return null;

  const parsed = rawMessages
    .map(messageToText)
    .filter((m): m is { role: string; content: string } => m !== null);

  if (parsed.length < 8) return null;

  const conversationText = truncateMessages(parsed, 12_000);
  if (conversationText.length < 20) return null;

  const alreadyStored = storedFactTexts.length > 0
    ? storedFactTexts.map((t) => `- ${t}`).join('\n')
    : '(none)';

  const promptTemplate = hostType === 'coding'
    ? CRYSTAL_SYSTEM_PROMPT_CODING
    : CRYSTAL_SYSTEM_PROMPT_CHAT;
  const systemPrompt = promptTemplate.replace('{already_stored_facts}', alreadyStored);

  try {
    const response = await chatCompletion(config, [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: `Crystallise this session:\n\n${conversationText}` },
    ], {
      retry: { attempts: 3, baseDelayMs: 1000 },
      timeoutMs: 30_000,
    });

    if (!response) return null;
    return parseCrystalResponse(response, hostType);
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// v1 Taxonomy Extraction Pipeline (default as of plugin v3.0.0)
//
// Produces facts conforming to Memory Taxonomy v1 (6 types: claim,
// preference, directive, commitment, episode, summary; 5 sources; 8 scopes).
//
// The G-pipeline uses a single merged-topic prompt that returns both the
// 2-3 main topics the user engaged with AND the extracted facts, so topic
// anchoring is preserved within one call. After extraction we apply:
//
//   1. `applyProvenanceFilterLax`  — tag-don't-drop. Assistant-sourced facts
//      get their importance capped at 7 rather than being filtered out; the
//      reranker later uses the source field to deprioritize them.
//   2. `comparativeRescoreV1`      — spread importance across the 1-10 range
//      and assign volatility. Forced when the batch has >= 5 facts.
//   3. `defaultVolatility`         — heuristic fallback.
//
// This matches the winning G pipeline from the 200-conv benchmark.
// ---------------------------------------------------------------------------

/**
 * The main extraction system prompt (v1 merged-topic pipeline).
 *
 * Exported as both `EXTRACTION_SYSTEM_PROMPT` (canonical) and
 * `EXTRACTION_SYSTEM_PROMPT_V1_MERGED` (deprecated alias) for back-compat.
 */
export const EXTRACTION_SYSTEM_PROMPT = `You are a memory extraction engine using Memory Taxonomy v1. Work in TWO explicit phases within one response:

PHASE 1 — Topic identification.
Before extracting any fact, identify the 2-3 main topics the user was engaging with. Topics should be short phrases (2-5 words each). If the conversation has no clear user-focused topic, use an empty topics array.

PHASE 2 — Fact extraction anchored to those topics.
Extract valuable memories. Prefer facts that directly relate to the identified topics (importance 7-9 range). Tangential facts may still be extracted but score lower (6-7 range).

Rules:
1. Each memory = single self-contained piece of information
2. Focus on user-specific info useful in future conversations
3. Skip generic knowledge, greetings, small talk, ephemeral task coordination
4. Score importance 1-10 (6+ = worth storing)
5. Every memory MUST attribute a source (provenance critical)

Importance rubric (use FULL 1-10 range):
- 10: Critical, core identity, never-forget content
- 9: Affects many future decisions
- 8: High-value preference/decision/rule
- 7: Specific durable fact
- 6: Borderline
- 5 or below: NOT worth storing — drop

DO NOT cluster everything at 7-8-9.

═══════════════════════════════════════════════════════════════
TYPE (6 values)
═══════════════════════════════════════════════════════════════
- claim: factual assertion (absorbs fact/context/decision; decisions populate reasoning field)
- preference: likes/dislikes/tastes
- directive: imperative rule ("always X", "never Y")
- commitment: future intent ("will do X")
- episode: notable event
- summary: derived synthesis (source must be derived|assistant) — do NOT emit for turn-extraction

═══════════════════════════════════════════════════════════════
SOURCE (provenance, CRITICAL)
═══════════════════════════════════════════════════════════════
- user: user explicitly stated it (in [user]: turns)
- user-inferred: extractor inferred from user signals
- assistant: assistant authored content — DOWNGRADE unless user affirmed/quoted/used it
- external, derived: rare

IF fact substance appears ONLY in [assistant]: turns without user affirmation → source:assistant

═══════════════════════════════════════════════════════════════
SCOPE (life domain)
═══════════════════════════════════════════════════════════════
work | personal | health | family | creative | finance | misc | unspecified

═══════════════════════════════════════════════════════════════
ENTITIES
═══════════════════════════════════════════════════════════════
- type ∈ {person, project, tool, company, concept, place}
- prefer specific names ("PostgreSQL" not "database")
- omit umbrella categories when specific name is present

═══════════════════════════════════════════════════════════════
REASONING (only for claims that are decisions)
═══════════════════════════════════════════════════════════════
For type=claim where the user expressed a decision-with-reasoning, populate "reasoning" with the WHY clause.

═══════════════════════════════════════════════════════════════
OUTPUT FORMAT (no markdown, no code fences)
═══════════════════════════════════════════════════════════════
{
  "topics": ["topic 1", "topic 2"],
  "facts": [
    {
      "text": "...",
      "type": "claim|preference|directive|commitment|episode",
      "source": "user|user-inferred|assistant",
      "scope": "work|personal|health|...",
      "importance": N,
      "confidence": 0.9,
      "action": "ADD",
      "reasoning": "...",     // optional, only for claim+decision
      "entities": [{"name": "...", "type": "tool"}]
    }
  ]
}

If nothing worth extracting: {"topics": [], "facts": []}`;

/**
 * @deprecated Use `EXTRACTION_SYSTEM_PROMPT` instead. Kept only as a
 * back-compat alias for callers that imported the v1 rollout name.
 */
export const EXTRACTION_SYSTEM_PROMPT_V1_MERGED = EXTRACTION_SYSTEM_PROMPT;

/**
 * Parse a v1 merged-topic LLM response. Returns both the topic list and the
 * validated/filtered fact list. Illegal combinations (summary+user) are
 * dropped; importance < 6 with action != DELETE is dropped.
 *
 * Exported as both `parseFactsResponse` (canonical, returns facts array) and
 * `parseMergedResponseV1` (returns `{ topics, facts }`). Prefer the former
 * unless the topic list is needed.
 */
export function parseMergedResponseV1(
  response: string,
  logger?: ExtractorLogger,
): { topics: string[]; facts: ExtractedFact[] } {
  const originalPreview = response.trim().slice(0, 200);
  let cleaned = response.trim();
  cleaned = cleaned.replace(/<think(?:ing)?>[\s\S]*?<\/think(?:ing)?>/gi, '').trim();
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }

  const tryParse = (input: string): unknown => {
    try { return JSON.parse(input); } catch { return undefined; }
  };

  let parsed = tryParse(cleaned);
  let recoveryUsed: 'none' | 'bracket-scan' = 'none';
  if (parsed === undefined) {
    // First try an outermost-array greedy match (legacy bare-array format).
    const arrMatch = cleaned.match(/\[[\s\S]*\]/);
    if (arrMatch) {
      parsed = tryParse(arrMatch[0]);
      if (parsed !== undefined) recoveryUsed = 'bracket-scan';
    }
    if (parsed === undefined) {
      // Fall back to an outermost-object greedy match (merged-topic format).
      const objMatch = cleaned.match(/\{[\s\S]*\}/);
      if (objMatch) {
        parsed = tryParse(objMatch[0]);
        if (parsed !== undefined) recoveryUsed = 'bracket-scan';
      }
    }
  }
  if (recoveryUsed === 'bracket-scan') {
    logger?.info?.(
      `parseFactsResponse: recovered JSON via bracket-scan fallback`,
    );
  }

  if (!parsed || typeof parsed !== 'object') {
    logger?.warn?.(
      `parseFactsResponse: could not parse LLM output as JSON. Preview: ${JSON.stringify(originalPreview)}`,
    );
    return { topics: [], facts: [] };
  }

  // Dual-format acceptance: either the merged object `{ topics, facts }` or
  // a bare JSON array of fact objects (legacy / test fixture shape). The
  // bare array is wrapped as { topics: [], facts: [...] } so the downstream
  // logic stays uniform. A single fact object (no wrapper) is also wrapped.
  let obj: Record<string, unknown>;
  if (Array.isArray(parsed)) {
    obj = { topics: [], facts: parsed };
  } else if (
    typeof (parsed as Record<string, unknown>).facts === 'undefined' &&
    typeof (parsed as Record<string, unknown>).text === 'string'
  ) {
    // Single fact object, not a merged wrapper.
    obj = { topics: [], facts: [parsed] };
  } else {
    obj = parsed as Record<string, unknown>;
  }

  const rawTopics = obj.topics;
  const topics = Array.isArray(rawTopics)
    ? (rawTopics as unknown[])
        .filter((t): t is string => typeof t === 'string' && t.length > 0)
        .slice(0, 3)
    : [];

  const rawFacts = obj.facts;
  if (!Array.isArray(rawFacts)) return { topics, facts: [] };

  const validActions: ExtractionAction[] = ['ADD', 'UPDATE', 'DELETE', 'NOOP'];

  const facts = (rawFacts as unknown[])
    .filter(
      (f): f is Record<string, unknown> =>
        !!f &&
        typeof f === 'object' &&
        typeof (f as Record<string, unknown>).text === 'string' &&
        ((f as Record<string, unknown>).text as string).length >= 5,
    )
    .map((f) => {
      const rawType = String(f.type ?? 'claim').toLowerCase();
      // Accept both v1 tokens and legacy v0 tokens — coerce v0 via V0_TO_V1_TYPE.
      let type: MemoryType;
      if (isValidMemoryType(rawType)) {
        type = rawType;
      } else if ((LEGACY_V0_MEMORY_TYPES as readonly string[]).includes(rawType)) {
        type = V0_TO_V1_TYPE[rawType as MemoryTypeV0];
      } else {
        type = 'claim';
      }

      const rawSource = String(f.source ?? 'user-inferred').toLowerCase();
      const source: MemorySource =
        (VALID_MEMORY_SOURCES as readonly string[]).includes(rawSource)
          ? (rawSource as MemorySource)
          : 'user-inferred';

      const rawScope = String(f.scope ?? 'unspecified').toLowerCase();
      const scope: MemoryScope =
        (VALID_MEMORY_SCOPES as readonly string[]).includes(rawScope)
          ? (rawScope as MemoryScope)
          : 'unspecified';

      const reasoning = typeof f.reasoning === 'string' ? f.reasoning.slice(0, 256) : undefined;

      const action = validActions.includes(String(f.action) as ExtractionAction)
        ? (String(f.action) as ExtractionAction)
        : 'ADD';

      let entities: ExtractedEntity[] | undefined;
      if (Array.isArray(f.entities)) {
        const valid = (f.entities as unknown[])
          .map(parseEntity)
          .filter((e): e is ExtractedEntity => e !== null);
        if (valid.length > 0) entities = valid;
      }

      const fact: ExtractedFact = {
        text: String(f.text).slice(0, 512),
        type,
        source,
        scope,
        reasoning,
        importance: Math.max(1, Math.min(10, Number(f.importance) || 5)),
        confidence: normalizeConfidence(f.confidence),
        action,
        existingFactId: typeof f.existingFactId === 'string' ? f.existingFactId : undefined,
      };
      if (entities) fact.entities = entities;
      return fact;
    })
    // Reject illegal type:summary + source:user
    .filter((f) => !(f.type === 'summary' && f.source === 'user'))
    // Importance threshold (preserves DELETE)
    .filter((f) => f.importance >= 6 || f.action === 'DELETE');

  return { topics, facts };
}

/**
 * Parse an LLM extraction response into structured v1 facts. Canonical
 * parser used by the default `extractFacts()` pipeline.
 *
 * This is a thin wrapper around `parseMergedResponseV1` that discards the
 * topic list so existing callers that expect a flat `ExtractedFact[]`
 * signature keep working.
 */
export function parseFactsResponse(
  response: string,
  logger?: ExtractorLogger,
): ExtractedFact[] {
  return parseMergedResponseV1(response, logger).facts;
}

/**
 * Tag-don't-drop provenance filter (pipeline G / F).
 *
 * For each fact:
 *   - If source is already "assistant", cap importance at 7.
 *   - Otherwise, keyword-match the fact against user turns. If <30% of
 *     content words (length >= 4) appear in user turns AND source != "user",
 *     tag source as "assistant" and cap importance at 7 (keep the fact).
 *   - Drop facts below importance 5 (unless DELETE action).
 */
export function applyProvenanceFilterLax(
  facts: ExtractedFact[],
  conversationText: string,
): ExtractedFact[] {
  const userTurnsLower = conversationText
    .split(/\n\n/)
    .filter((line) => line.startsWith('[user]:'))
    .join(' ')
    .toLowerCase();

  return facts
    .map((f) => {
      if (f.source === 'assistant') {
        return { ...f, importance: Math.min(f.importance, 7) };
      }

      const factWords = f.text
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, ' ')
        .split(/\s+/)
        .filter((w) => w.length >= 4);

      const matchedWords = factWords.filter((w) => userTurnsLower.includes(w)).length;
      const matchRatio = factWords.length > 0 ? matchedWords / factWords.length : 0;

      if (matchRatio < 0.3 && f.source !== 'user') {
        return {
          ...f,
          source: 'assistant' as MemorySource,
          importance: Math.min(f.importance, 7),
        };
      }

      return f;
    })
    .filter((f) => f.importance >= 5 || f.action === 'DELETE');
}

/**
 * Heuristic fallback volatility when the LLM doesn't assign one.
 */
export function defaultVolatility(f: ExtractedFact): MemoryVolatility {
  if (f.type === 'commitment') return 'updatable';
  if (f.type === 'episode') return 'stable';
  if (f.type === 'directive') return 'stable';
  if (f.scope === 'health' || f.scope === 'family') return 'stable';
  return 'updatable';
}

const COMPARATIVE_PROMPT_V1 = `You are a memory re-ranker for the v1 taxonomy. You receive facts already extracted from one conversation, each with initial importance. Your job is twofold:

1. RE-RANK importance to spread across the 1-10 range (avoid clustering at 7-8-9)
2. ASSIGN volatility to each fact

Re-ranking rules:
- Top 1/3 of facts (most significant for this user): importance 9-10
- Middle 1/3: importance 7-8
- Bottom 1/3: importance 5-6 (borderline, may be dropped)
- A fact may stay at 10 if it's clearly identity-defining (name, birthday) or marked as "never forget"
- Never raise without justification; never lower below 5 unless clearly noise
- You MUST produce a spread

Volatility rules:
- stable: unlikely to change for years (name, allergies, birthplace, fundamental traits)
- updatable: changes occasionally (current job, active project, partner's name, address)
- ephemeral: short-lived state (today's task, this week's plan, current trip itinerary)

Use the FULL conversation context to judge volatility — a single claim may be ambiguous, but in context you can usually tell.

Return JSON array, same order as input, ONLY with importance + volatility fields:
[{"importance": N, "volatility": "stable|updatable|ephemeral"}, ...]
No markdown.`;

/**
 * Comparative re-scoring pass (v1). Forces re-scoring when facts.length >= 5
 * so the importance distribution spreads across the 1-10 range. When
 * facts.length < 5, assigns defaultVolatility and returns.
 */
export async function comparativeRescoreV1(
  facts: ExtractedFact[],
  conversationText: string,
  logger?: ExtractorLogger,
): Promise<ExtractedFact[]> {
  // G-tuned behavior: force rescore when >= 5 facts
  if (facts.length < 2 || facts.length < 5) {
    return facts.map((f) => ({ ...f, volatility: f.volatility ?? defaultVolatility(f) }));
  }

  const config = resolveLLMConfig();
  if (!config) {
    return facts.map((f) => ({ ...f, volatility: defaultVolatility(f) }));
  }

  const factsForPrompt = facts
    .map((f, i) => `${i + 1}. [imp: ${f.importance}] [type: ${f.type}] [scope: ${f.scope ?? 'unspecified'}] ${f.text}`)
    .join('\n');

  const userPrompt = `Conversation context:\n${conversationText}\n\nExtracted facts:\n${factsForPrompt}\n\nReturn ${facts.length} JSON objects, each with "importance" + "volatility". Match input order.`;

  let response: string | null | undefined;
  try {
    response = await chatCompletion(config, [
      { role: 'system', content: COMPARATIVE_PROMPT_V1 },
      { role: 'user', content: userPrompt },
    ], {
      // 3.3.1-rc.2: retry transient 429 / timeout (rescore is an inner
      // call after extractFacts — if extraction backs off successfully
      // the rescore usually also passes on first try, but keep symmetry).
      retry: { attempts: 3, baseDelayMs: 1000 },
      timeoutMs: 30_000,
      logger,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger?.warn?.(`comparativeRescoreV1: chatCompletion threw: ${msg}`);
    return facts.map((f) => ({ ...f, volatility: defaultVolatility(f) }));
  }

  if (!response) {
    return facts.map((f) => ({ ...f, volatility: defaultVolatility(f) }));
  }

  let cleaned = response.trim();
  cleaned = cleaned.replace(/<think(?:ing)?>[\s\S]*?<\/think(?:ing)?>/gi, '').trim();
  if (cleaned.startsWith('```')) {
    cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
  }
  const match = cleaned.match(/\[[\s\S]*\]/);
  if (match) cleaned = match[0];

  let parsed: unknown;
  try {
    parsed = JSON.parse(cleaned);
  } catch {
    return facts.map((f) => ({ ...f, volatility: defaultVolatility(f) }));
  }
  if (!Array.isArray(parsed)) {
    return facts.map((f) => ({ ...f, volatility: defaultVolatility(f) }));
  }

  return facts.map((f, i) => {
    const entry = parsed[i] as Record<string, unknown> | undefined;
    const rawImp = entry && typeof entry === 'object' ? Number(entry.importance) : NaN;
    const rawVol = entry && typeof entry === 'object' ? String(entry.volatility ?? '').toLowerCase() : '';

    const newImp = Number.isFinite(rawImp)
      ? Math.max(5, Math.min(10, Math.round(rawImp)))
      : f.importance;
    const newVol: MemoryVolatility =
      (VALID_MEMORY_VOLATILITIES as readonly string[]).includes(rawVol)
        ? (rawVol as MemoryVolatility)
        : defaultVolatility(f);

    return { ...f, importance: newImp, volatility: newVol };
  });
}

/**
 * Main extraction entry point (default pipeline as of plugin v3.0.0).
 *
 * Pipeline: single merged-topic LLM call → `applyProvenanceFilterLax`
 * (tag-don't-drop) → `comparativeRescoreV1` (forces re-rank when >= 5 facts)
 * → `defaultVolatility` fallback → lexical importance bumps.
 *
 * Produces v1-shaped facts with `type`, `source`, `scope`, `volatility`,
 * and optional `reasoning` fields populated. The caller should hand the
 * result to `storeExtractedFacts` which emits a v1 canonical claim blob.
 */
export async function extractFacts(
  rawMessages: unknown[],
  mode: 'turn' | 'full',
  existingMemories?: Array<{ id: string; text: string }>,
  profileContext?: string,
  logger?: ExtractorLogger,
): Promise<ExtractedFact[]> {
  const config = resolveLLMConfig();
  if (!config) {
    logger?.info?.('extractFacts: no LLM config resolved (skipping extraction)');
    return [];
  }

  const parsed = rawMessages
    .map(messageToText)
    .filter((m): m is { role: string; content: string } => m !== null);

  if (parsed.length === 0) {
    logger?.info?.(`extractFacts: no parseable messages (raw count=${rawMessages.length})`);
    return [];
  }

  const relevantMessages = mode === 'turn' ? parsed.slice(-6) : parsed;
  const conversationText = truncateMessages(relevantMessages, 12_000);

  if (conversationText.length < 20) {
    logger?.info?.(
      `extractFacts: conversation too short (${conversationText.length} chars < 20, parsed=${parsed.length}, mode=${mode})`,
    );
    return [];
  }

  let memoriesContext = '';
  if (existingMemories && existingMemories.length > 0) {
    const memoriesStr = existingMemories
      .map((m) => `[ID: ${m.id}] ${m.text}`)
      .join('\n');
    memoriesContext = `\n\nExisting memories (use these for dedup — classify as UPDATE/DELETE/NOOP if they conflict or overlap):\n${memoriesStr}`;
  }

  const userPrompt =
    mode === 'turn'
      ? `Extract important facts from these recent conversation turns:\n\n${conversationText}${memoriesContext}`
      : `Extract ALL valuable long-term memories from this conversation before it is lost:\n\n${conversationText}${memoriesContext}`;

  const systemPrompt = profileContext || EXTRACTION_SYSTEM_PROMPT;

  let response: string | null | undefined;
  try {
    response = await chatCompletion(config, [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ], {
      // 3.3.1-rc.2: the headline fix for the rc.1 QA NO-GO — 5/6 extraction
      // windows failed on zai 429 + timeouts with no retry. 3 attempts with
      // 1s → 2s → 4s backoff recovers virtually all transient rate-limit
      // hiccups. Graceful timeout: per-attempt 30s, total worst-case 30+1+30+2+30+4≈97s.
      retry: { attempts: 3, baseDelayMs: 1000 },
      timeoutMs: 30_000,
      logger,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger?.warn?.(`extractFacts: chatCompletion threw: ${msg}`);
    return [];
  }

  if (!response) {
    logger?.info?.('extractFacts: chatCompletion returned null/empty response');
    return [];
  }

  logger?.info?.(
    `extractFacts: LLM returned ${response.length} chars; parsing merged response`,
  );
  const { topics, facts: rawFacts } = parseMergedResponseV1(response, logger);
  if (topics.length > 0) {
    logger?.info?.(`extractFacts: topics = ${JSON.stringify(topics)}`);
  }

  // Provenance filter (tag-don't-drop)
  let facts = applyProvenanceFilterLax(rawFacts, conversationText);

  // Comparative rescore (forces re-rank when >= 5 facts)
  facts = await comparativeRescoreV1(facts, conversationText, logger);

  // Ensure every fact has a volatility (defensive: rescore may have skipped)
  facts = facts.map((f) => ({ ...f, volatility: f.volatility ?? defaultVolatility(f) }));

  // Lexical importance bumps (same as v0 pipeline)
  for (const f of facts) {
    const bump = computeLexicalImportanceBump(f.text, conversationText);
    if (bump > 0) {
      const oldImportance = f.importance;
      const effectiveBump = f.importance >= 8 ? Math.min(bump, 1) : bump;
      f.importance = Math.min(10, f.importance + effectiveBump);
      logger?.info?.(
        `extractFacts: lexical bump +${bump} for "${f.text.slice(0, 60)}..." (${oldImportance} → ${f.importance})`,
      );
    }
  }

  return facts;
}
