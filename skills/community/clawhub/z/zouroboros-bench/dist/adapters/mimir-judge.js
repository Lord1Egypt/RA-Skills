// src/adapters/mimir-judge.ts
import Database from "better-sqlite3";
import { execSync } from "child_process";
import { homedir } from "os";
import { join } from "path";
var GATE_URL = process.env.MIMIR_GATE_URL || "http://localhost:7820";
var OPENAI_API_KEY = process.env.OPENAI_API_KEY || "";
var MEMORY_DB_PATH = process.env.ZO_MEMORY_DB || join(homedir(), ".zouroboros", "memory.db");
var MEMORY_CLI = process.env.ZOUROBOROS_MEMORY_CLI ?? "zouroboros-memory";
var _cachedPatterns = null;
var _cacheTimestamp = 0;
var CACHE_TTL_MS = 5 * 60 * 1e3;
function loadDeprecatedPatterns() {
  const now = Date.now();
  if (_cachedPatterns && now - _cacheTimestamp < CACHE_TTL_MS) {
    return _cachedPatterns;
  }
  try {
    const db = new Database(MEMORY_DB_PATH, { readonly: true });
    const STATUS_SIGNALS = ["removed", "abandoned", "deprecated", "replaced", "obsolete"];
    const likeClause = STATUS_SIGNALS.map(() => "LOWER(value) LIKE ?").join(" OR ");
    const params = STATUS_SIGNALS.map((s) => `%${s}%`);
    const rows = db.prepare(
      `SELECT entity, key, value FROM facts WHERE (${likeClause}) AND decay_class IN ('permanent', 'stable')`
    ).all(...params);
    db.close();
    const seen = /* @__PURE__ */ new Set();
    const patterns = [];
    for (const row of rows) {
      const parts = row.entity.split(".");
      if (parts.length < 2) continue;
      const term = parts[parts.length - 1];
      if (term.length < 4) continue;
      if (seen.has(term.toLowerCase())) continue;
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
async function storeContradiction(entity, pattern, signal, question, hypothesis) {
  try {
    const key = `mimir-correction-${pattern}`;
    const db = new Database(MEMORY_DB_PATH, { readonly: true });
    const existing = db.prepare("SELECT id FROM facts WHERE entity = ? AND key = ? LIMIT 1").get(entity, key);
    db.close();
    if (existing) return;
    const value = `[[${entity}]] flagged as ${signal} by Mimir judge. Hypothesis "${hypothesis.slice(0, 120)}" incorrectly referenced "${pattern}" in response to: "${question.slice(0, 120)}"`;
    execSync(
      `${MEMORY_CLI} store --entity "${entity}" --key "${key}" --value "${encodeURIComponent(value)}" --decay stable`,
      {
        env: { ...process.env },
        stdio: "pipe",
        timeout: 1e4
      }
    );
  } catch {
  }
}
var MIN_JUDGE_CONFIDENCE = 0.35;
function checkRetrievalConfidence(mimirOutput) {
  const scoreMatches = [...mimirOutput.matchAll(/score:\s*([\d.]+)/g)];
  if (scoreMatches.length === 0) {
    if (mimirOutput.includes("[Mimir Synthesis]") && !mimirOutput.includes("[Memory Context")) {
      return { confident: false, reason: "Synthesis without retrieval scores (briefing-only)" };
    }
    return { confident: true, reason: "Non-scored context (briefing/continuation)" };
  }
  const scores = scoreMatches.map((m) => parseFloat(m[1]));
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
  const max = Math.max(...scores);
  if (avg < MIN_JUDGE_CONFIDENCE && max < MIN_JUDGE_CONFIDENCE + 0.1) {
    return {
      confident: false,
      reason: `avgScore=${avg.toFixed(3)}, maxScore=${max.toFixed(3)} (threshold=${MIN_JUDGE_CONFIDENCE})`
    };
  }
  return { confident: true, reason: `avgScore=${avg.toFixed(3)}` };
}
function findDeprecatedMention(hypothesis) {
  const hypLower = hypothesis.toLowerCase();
  for (const { pattern, entity } of loadDeprecatedPatterns()) {
    if (hypLower.includes(pattern)) {
      return { entity, term: pattern };
    }
  }
  return null;
}
async function mimirJudge(question, groundTruth, hypothesis, category, upstreamVerdict) {
  if (upstreamVerdict === "incorrect") {
    return { verdict: "abstain", reason: "Upstream already incorrect \u2014 Mimir only downgrades" };
  }
  const mimirQuery = `remind me about ${category.replace(/-/g, " ")}: ${question}`;
  let mimirOutput = "";
  try {
    const resp = await fetch(`${GATE_URL}/gate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: mimirQuery, persona: "mimir" }),
      signal: AbortSignal.timeout(3e4)
    });
    if (!resp.ok) {
      return { verdict: "abstain", reason: `Gate returned ${resp.status}` };
    }
    const data = await resp.json();
    if (data.exit_code !== 0 || !data.output || data.output.length < 20) {
      return { verdict: "abstain", reason: "No institutional knowledge for this topic" };
    }
    mimirOutput = data.output;
  } catch (err) {
    return { verdict: "abstain", reason: `Gate error: ${err}` };
  }
  const confidenceCheck = checkRetrievalConfidence(mimirOutput);
  if (!confidenceCheck.confident) {
    return {
      verdict: "abstain",
      reason: `Low retrieval confidence: ${confidenceCheck.reason}`,
      mimir_context: mimirOutput.slice(0, 300)
    };
  }
  if (!OPENAI_API_KEY) {
    const result = heuristicMimirCheck(hypothesis, mimirOutput, question);
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
        Authorization: `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: prompt }],
        max_tokens: 100,
        temperature: 0.1
      }),
      signal: AbortSignal.timeout(1e4)
    });
    if (!resp.ok) {
      return { verdict: "abstain", reason: `OpenAI returned ${resp.status}` };
    }
    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content?.trim() || "";
    const firstLine = content.split("\n")[0].toLowerCase();
    const reason = content.split("\n").slice(1).join(" ").trim() || "No reason provided";
    let verdict = "uncertain";
    if (firstLine.includes("incorrect")) verdict = "incorrect";
    else if (firstLine.includes("correct") && !firstLine.includes("incorrect")) verdict = "correct";
    if (verdict === "incorrect") {
      const match = findDeprecatedMention(hypothesis);
      const correctionEntity = match?.entity || `mimir.llm-catch.${category}`;
      const correctionTerm = match?.term || category;
      await storeContradiction(correctionEntity, correctionTerm, "contradicted", question, hypothesis);
    }
    return {
      verdict,
      reason,
      mimir_context: mimirOutput.slice(0, 300)
    };
  } catch (err) {
    return { verdict: "abstain", reason: `Comparison failed: ${err}` };
  }
}
function extractPattern(reason) {
  const match = reason.match(/references "([^"]+)"/);
  return match?.[1] || "unknown";
}
function heuristicMimirCheck(hypothesis, mimirContext, question) {
  const hypLower = hypothesis.toLowerCase();
  const ctxLower = mimirContext.toLowerCase();
  const removedPatterns = loadDeprecatedPatterns();
  for (const { pattern, signal, entity } of removedPatterns) {
    if (hypLower.includes(pattern) && (ctxLower.includes(signal) || ctxLower.includes(pattern))) {
      return {
        verdict: "incorrect",
        reason: `Hypothesis references "${pattern}" which institutional knowledge (${entity}) marks as ${signal}`,
        mimir_context: mimirContext.slice(0, 300)
      };
    }
  }
  return {
    verdict: "correct",
    reason: "No contradictions detected (heuristic fallback)",
    mimir_context: mimirContext.slice(0, 300)
  };
}
export {
  mimirJudge
};
