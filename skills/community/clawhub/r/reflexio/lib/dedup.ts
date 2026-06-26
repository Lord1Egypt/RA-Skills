import type { InferFn } from "./openclaw-cli.ts";

const PREPROCESS_PROMPT = `Rewrite the following text into a single descriptive but concise sentence that captures the core facts or topics. Expand with 2-3 important synonyms or related terms to improve search matching. Remove conversational filler. Return ONLY the rewritten text.

Text: "{rawText}"`;

const DEDUP_PROMPT = `EXISTING: "{existingContent}"
NEW: "{newContent}"

Compare these two entries:
- If they are about different topics with no overlap, answer "keep_both".
- Otherwise, merge them: resolve contradictions (NEW wins over EXISTING), deduplicate redundant statements, preserve all non-contradicted facts from both. Return the merged result as 1-3 concise sentences.

Answer with ONLY a JSON object:
{"decision": "keep_both"} or {"decision": "merge_and_resolve", "resolved": "<merged, deduped, resolved body>"}`;

export type DedupResult =
  | { decision: "keep_both" }
  | { decision: "merge_and_resolve"; resolved: string };

/**
 * Rewrite raw text into a clean search query optimized for vector + FTS search.
 * Falls back to raw text if openclaw infer is unavailable.
 */
export async function preprocessQuery(rawText: string, inferFn: InferFn): Promise<string> {
  console.info(`[reflexio] preprocessQuery: inputLen=${rawText.length} input="${rawText.slice(0, 100)}"`);
  const prompt = PREPROCESS_PROMPT.replace("{rawText}", rawText);
  const result = await inferFn(prompt);
  if (!result || result.trim().length === 0) {
    console.info(`[reflexio] preprocessQuery: infer returned empty, falling back to raw text`);
    return rawText;
  }
  console.info(`[reflexio] preprocessQuery: rewritten="${result.trim().slice(0, 120)}"`);
  return result.trim();
}

/**
 * Ask LLM to compare new content against existing content.
 * Returns keep_both (different topics) or merge_and_resolve (with resolved body).
 * Defaults to keep_both on any failure.
 */
export async function judgeDedup(
  newContent: string,
  existingContent: string,
  inferFn: InferFn
): Promise<DedupResult> {
  console.info(`[reflexio] judgeDedup: existingLen=${existingContent.length} newLen=${newContent.length}`);
  console.info(`[reflexio] judgeDedup: existing="${existingContent.slice(0, 100)}" new="${newContent.slice(0, 100)}"`);
  const prompt = DEDUP_PROMPT
    .replace("{existingContent}", existingContent)
    .replace("{newContent}", newContent);

  const result = await inferFn(prompt);
  if (!result) {
    console.info(`[reflexio] judgeDedup: infer returned empty, defaulting to keep_both`);
    return { decision: "keep_both" };
  }

  console.info(`[reflexio] judgeDedup: raw result="${result.slice(0, 200)}"`);
  try {
    const parsed = JSON.parse(result);
    if (parsed.decision === "merge_and_resolve" && typeof parsed.resolved === "string" && parsed.resolved.trim()) {
      console.info(`[reflexio] judgeDedup: decision="merge_and_resolve" resolvedLen=${parsed.resolved.length}`);
      return { decision: "merge_and_resolve", resolved: parsed.resolved.trim() };
    }
    console.info(`[reflexio] judgeDedup: decision="keep_both"`);
    return { decision: "keep_both" };
  } catch (err) {
    console.error(`[reflexio] judgeDedup: JSON parse failed: ${err}, defaulting to keep_both`);
    return { decision: "keep_both" };
  }
}

/**
 * Extract the `id:` value from a memory search snippet containing YAML frontmatter.
 */
export function extractId(snippet: string): string | null {
  const match = /^id:\s*(\S+)/m.exec(snippet);
  return match ? match[1] : null;
}
