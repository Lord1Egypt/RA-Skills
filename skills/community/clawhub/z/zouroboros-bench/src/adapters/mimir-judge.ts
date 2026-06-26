/**
 * mimir-judge.ts — Institutional knowledge judge for ZouroBench
 *
 * Mode C judge: queries Mimir for historical context, then evaluates whether
 * an answer aligns with known decisions, conventions, and architecture.
 *
 * Catches semantic drift that mechanical (Mode A) and GPT-4o (Mode B) judges miss:
 *   - Answers referencing removed features (e.g., OmniRoute)
 *   - Answers contradicting stored architectural decisions
 *   - Answers using outdated naming conventions
 *
 * Design: Mimir can only DOWNGRADE (correct → incorrect), never upgrade.
 *
 * Closed-loop: When Mimir catches a contradiction, it stores the finding back
 * into the memory system so future retrievals are enriched. The removedPatterns
 * list is self-maintaining — populated dynamically from memory facts whose values
 * contain status signals (removed, abandoned, deprecated, replaced, obsolete).
 */

import Database from 'better-sqlite3';
import { execSync } from 'child_process';
import { homedir } from 'os';
import { join } from 'path';

const GATE_URL = process.env.MIMIR_GATE_URL || "http://localhost:7820";
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || "";
const MEMORY_DB_PATH = process.env.ZO_MEMORY_DB || join(homedir(), '.zouroboros', 'memory.db');
const MEMORY_CLI = process.env.ZOUROBOROS_MEMORY_CLI ?? 'zouroboros-memory';

export interface MimirVerdict {
  verdict: "correct" | "incorrect" | "uncertain" | "abstain";
  reason: string;
  mimir_context?: string;
}

interface DeprecatedPattern {
  pattern: string;
  signal: string;
  entity: string;
}

// Cache deprecated patterns for 5 minutes to avoid hammering the DB on every question
let _cachedPatterns: DeprecatedPattern[] | null = null;
let _cacheTimestamp = 0;
const CACHE_TTL_MS = 5 * 60 * 1000;

/**
 * Query the memory DB for facts that indicate something is removed/deprecated/abandoned.
 * Returns a list of { pattern, signal, entity } for use in heuristic checks.
 *
 * This replaces the old hardcoded removedPatterns array — the judge's knowledge
 * of what's deprecated now grows automatically as facts are stored.
 */
function loadDeprecatedPatterns(): DeprecatedPattern[] {
  const now = Date.now();
  if (_cachedPatterns && now - _cacheTimestamp < CACHE_TTL_MS) {
    return _cachedPatterns;
  }

  try {
    const db = new Database(MEMORY_DB_PATH, { readonly: true });
    const STATUS_SIGNALS = ["removed", "abandoned", "deprecated", "replaced", "obsolete"];
    const likeClause = STATUS_SIGNALS.map(() => "LOWER(value) LIKE ?").join(" OR ");
    const params = STATUS_SIGNALS.map((s) => `%${s}%`);

    const rows = db
      .prepare(
        `SELECT entity, key, value FROM facts WHERE (${likeClause}) AND decay_class IN ('permanent', 'stable')`,
      )
      .all(...params) as Array<{ entity: string; key: string; value: string }>;
    db.close();

    const seen = new Set<string>();
    const patterns: DeprecatedPattern[] = [];
    for (const row of rows) {
      const parts = row.entity.split(".");
      if (parts.length < 2) continue; // skip bare top-level entities (e.g. "system") — too generic
      const term = parts[parts.length - 1];
      if (term.length < 4) continue; // skip short/generic terms to avoid false matches
      if (seen.has(term.toLowerCase())) continue; // deduplicate by term
      seen.add(term.toLowerCase());

      const valueLower = row.value.toLowerCase();
      let matchedSignal = "deprecated";
      for (const sig of STATUS_SIGNALS) {
        if (valueLower.includes(sig)) {
          matchedSignal = sig;
          break;
        }
      }

      patterns.push({ pattern: term.toLowerCase(), signal: matchedSignal, entity: row.entity });
    }

    _cachedPatterns = patterns;
    _cacheTimestamp = now;
    return patterns;
  } catch (err) {
    console.error("[mimir-judge] Failed to load deprecated patterns from DB:", err);
    return _cachedPatterns || [];
  }
}

/**
 * Store a contradiction finding back into the memory system (closed loop).
 * Uses the original deprecated entity (not a generic "mimir.llm-catch") so the
 * correction enriches searches for that specific topic. Skips if a correction
 * for this entity already exists (idempotent across benchmark runs).
 */
async function storeContradiction(
  entity: string,
  pattern: string,
  signal: string,
  question: string,
  hypothesis: string,
): Promise<void> {
  try {
    const key = `mimir-correction-${pattern}`;

    // Dedupe: skip if we already have a correction for this entity+key
    const db = new Database(MEMORY_DB_PATH, { readonly: true });
    const existing = db
      .prepare("SELECT id FROM facts WHERE entity = ? AND key = ? LIMIT 1")
      .get(entity, key) as { id: string } | null;
    db.close();
    if (existing) return;

    const value = `[[${entity}]] flagged as ${signal} by Mimir judge. Hypothesis "${hypothesis.slice(0, 120)}" incorrectly referenced "${pattern}" in response to: "${question.slice(0, 120)}"`;

    execSync(
      `${MEMORY_CLI} store --entity "${entity}" --key "${key}" --value "${encodeURIComponent(value)}" --decay stable`,
      {
        env: { ...process.env },
        stdio: 'pipe',
        timeout: 10_000,
      }
    );
  } catch {
    // Non-critical — don't let storage failure break judging
  }
}

const MIN_JUDGE_CONFIDENCE = 0.35;

/**
 * Check if Mimir's retrieval has sufficient confidence to judge.
 * Parses "score: X.XXX" from context, computes average.
 * If avg score < threshold or synthesis is present but no scores found
 * (meaning synthesis hallucinated from unscored/session briefing), abstain.
 */
function checkRetrievalConfidence(mimirOutput: string): { confident: boolean; reason: string } {
  // If it's a synthesis block, check if scores are visible in the raw context underneath
  const scoreMatches = [...mimirOutput.matchAll(/score:\s*([\d.]+)/g)];

  if (scoreMatches.length === 0) {
    // No scores found — could be session briefing only or pure synthesis
    if (mimirOutput.includes("[Mimir Synthesis]") && !mimirOutput.includes("[Memory Context")) {
      // Synthesis without visible retrieval scores — likely from briefing, not targeted retrieval
      return { confident: false, reason: "Synthesis without retrieval scores (briefing-only)" };
    }
    // Session briefing or continuation detection — these don't have scores, skip confidence check
    return { confident: true, reason: "Non-scored context (briefing/continuation)" };
  }

  const scores = scoreMatches.map(m => parseFloat(m[1]));
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
  const max = Math.max(...scores);

  if (avg < MIN_JUDGE_CONFIDENCE && max < MIN_JUDGE_CONFIDENCE + 0.1) {
    return {
      confident: false,
      reason: `avgScore=${avg.toFixed(3)}, maxScore=${max.toFixed(3)} (threshold=${MIN_JUDGE_CONFIDENCE})`,
    };
  }

  return { confident: true, reason: `avgScore=${avg.toFixed(3)}` };
}

/**
 * Given a hypothesis, check which deprecated patterns it mentions.
 * Returns the first matching pattern's entity and term, or a fallback.
 */
function findDeprecatedMention(hypothesis: string): { entity: string; term: string } | null {
  const hypLower = hypothesis.toLowerCase();
  for (const { pattern, entity } of loadDeprecatedPatterns()) {
    if (hypLower.includes(pattern)) {
      return { entity, term: pattern };
    }
  }
  return null;
}

/**
 * Query Mimir for institutional knowledge relevant to the question,
 * then evaluate whether the hypothesis aligns.
 */
export async function mimirJudge(
  question: string,
  groundTruth: string,
  hypothesis: string,
  category: string,
  upstreamVerdict?: "correct" | "incorrect",
): Promise<MimirVerdict> {
  // Downgrade-only invariant: if upstream already ruled incorrect, nothing to do
  if (upstreamVerdict === "incorrect") {
    return { verdict: "abstain", reason: "Upstream already incorrect — Mimir only downgrades" };
  }

  // Step 1: Query Mimir for relevant context
  const mimirQuery = `remind me about ${category.replace(/-/g, " ")}: ${question}`;
  let mimirOutput = "";

  try {
    const resp = await fetch(`${GATE_URL}/gate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: mimirQuery, persona: "mimir" }),
      signal: AbortSignal.timeout(30000),
    });

    if (!resp.ok) {
      return { verdict: "abstain", reason: `Gate returned ${resp.status}` };
    }

    const data = (await resp.json()) as {
      exit_code: number;
      output: string;
    };

    if (data.exit_code !== 0 || !data.output || data.output.length < 20) {
      return { verdict: "abstain", reason: "No institutional knowledge for this topic" };
    }

    mimirOutput = data.output;
  } catch (err) {
    return { verdict: "abstain", reason: `Gate error: ${err}` };
  }

  // Step 1.5: Confidence gate — abstain if retrieval scores are too low
  // Prevents false downgrades from hallucinated synthesis based on irrelevant facts
  const confidenceCheck = checkRetrievalConfidence(mimirOutput);
  if (!confidenceCheck.confident) {
    return {
      verdict: "abstain",
      reason: `Low retrieval confidence: ${confidenceCheck.reason}`,
      mimir_context: mimirOutput.slice(0, 300),
    };
  }

  // Step 2: Use LLM to compare hypothesis against institutional knowledge
  if (!OPENAI_API_KEY) {
    const result = heuristicMimirCheck(hypothesis, mimirOutput, question);
    // Closed loop: store contradiction back to memory using the actual deprecated entity
    if (result.verdict === "incorrect") {
      const match = findDeprecatedMention(hypothesis);
      const correctionEntity = match?.entity || "mimir.heuristic-catch";
      const correctionTerm = match?.term || extractPattern(result.reason);
      await storeContradiction(correctionEntity, correctionTerm, "contradicted", question, hypothesis);
    }
    return result;
  }

  try {
    const prompt = `You are an institutional knowledge validator. Given Mimir's memory context (known facts about this system) and a benchmark answer, determine if the answer contradicts known facts.

Institutional Knowledge (from Mimir):
${mimirOutput.slice(0, 1500)}

Ground Truth: ${groundTruth}
Hypothesis Answer: ${hypothesis}
Question: ${question}

Rules:
- If the hypothesis contradicts a specific fact from institutional knowledge, respond "incorrect" with the contradicting fact
- If the hypothesis aligns with institutional knowledge (or institutional knowledge doesn't cover this topic), respond "correct"
- If you're unsure whether there's a contradiction, respond "uncertain"
- Only flag as "incorrect" when there is a CLEAR factual contradiction

Respond with ONLY one of: correct | incorrect | uncertain
Then on a new line, a brief reason.`;

    const resp = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: prompt }],
        max_tokens: 100,
        temperature: 0.1,
      }),
      signal: AbortSignal.timeout(10000),
    });

    if (!resp.ok) {
      return { verdict: "abstain", reason: `OpenAI returned ${resp.status}` };
    }

    const data = (await resp.json()) as {
      choices?: Array<{ message?: { content?: string } }>;
    };
    const content = data.choices?.[0]?.message?.content?.trim() || "";
    const firstLine = content.split("\n")[0].toLowerCase();
    const reason = content.split("\n").slice(1).join(" ").trim() || "No reason provided";

    let verdict: MimirVerdict["verdict"] = "uncertain";
    if (firstLine.includes("incorrect")) verdict = "incorrect";
    else if (firstLine.includes("correct") && !firstLine.includes("incorrect")) verdict = "correct";

    // Closed loop: store LLM-confirmed contradictions back to memory
    // Use the actual deprecated entity if we can identify it, not the broad category
    if (verdict === "incorrect") {
      const match = findDeprecatedMention(hypothesis);
      const correctionEntity = match?.entity || `mimir.llm-catch.${category}`;
      const correctionTerm = match?.term || category;
      await storeContradiction(correctionEntity, correctionTerm, "contradicted", question, hypothesis);
    }

    return {
      verdict,
      reason,
      mimir_context: mimirOutput.slice(0, 300),
    };
  } catch (err) {
    return { verdict: "abstain", reason: `Comparison failed: ${err}` };
  }
}

/**
 * Extract the key pattern from a reason string like:
 * 'Hypothesis references "omniroute" which institutional knowledge marks as removed'
 */
function extractPattern(reason: string): string {
  const match = reason.match(/references "([^"]+)"/);
  return match?.[1] || "unknown";
}

/**
 * Fallback heuristic: check if hypothesis contains terms that contradict Mimir's context.
 * Now self-maintaining — patterns are loaded dynamically from the memory DB instead of hardcoded.
 */
function heuristicMimirCheck(
  hypothesis: string,
  mimirContext: string,
  question?: string,
): MimirVerdict {
  const hypLower = hypothesis.toLowerCase();
  const ctxLower = mimirContext.toLowerCase();

  // Dynamic patterns from memory DB (replaces old hardcoded removedPatterns)
  // Signal check: if hypothesis mentions a deprecated term AND either the Mimir
  // context or the fact's own stored signal confirms it, flag it. This avoids
  // the synonym brittleness of requiring the exact signal word in gate output.
  const removedPatterns = loadDeprecatedPatterns();

  for (const { pattern, signal, entity } of removedPatterns) {
    if (hypLower.includes(pattern) && (ctxLower.includes(signal) || ctxLower.includes(pattern))) {
      return {
        verdict: "incorrect",
        reason: `Hypothesis references "${pattern}" which institutional knowledge (${entity}) marks as ${signal}`,
        mimir_context: mimirContext.slice(0, 300),
      };
    }
  }

  return {
    verdict: "correct",
    reason: "No contradictions detected (heuristic fallback)",
    mimir_context: mimirContext.slice(0, 300),
  };
}
