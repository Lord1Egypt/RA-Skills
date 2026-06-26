/**
 * Hallucination Audit - Veritier Use Case (JavaScript)
 * =====================================================
 * Demonstrates how to use Veritier as a post-generation safety net
 * for LLM outputs. Feeds simulated AI-generated text through the
 * verification engine and highlights any false claims.
 *
 * This is the #1 use case for AI developers: catch hallucinations
 * before they reach users.
 *
 * Usage:
 *   node hallucination_audit.mjs
 *
 * Get your free API key: https://veritier.ai/register
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";  // hardcoded � never sent to any other domain

if (!API_KEY) {
  console.error("✗ Error: VERITIER_API_KEY is not set.");
  console.error("  Get your free key at https://veritier.ai/register");
  process.exit(1);
}

// ── Simulated LLM output (contains deliberate hallucinations) ──────────
const llmOutput =
  "Albert Einstein won the Nobel Prize in Physics in 1921 for his " +
  "discovery of the photoelectric effect. He was born in Munich, Germany " +
  "on March 14, 1879. Einstein published his theory of general relativity " +
  "in 1915, and he later became the second president of Israel in 1952.";

console.log("🤖 Simulated LLM output:");
console.log(`   "${llmOutput}"\n`);
console.log("⏳ Auditing for hallucinations...\n");

const response = await fetch(`${API_URL}/v1/verify`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: llmOutput,
    grounding_mode: "web",
  }),
});

if (!response.ok) {
  console.error(`✗ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const results = data.results || [];

// ── Separate true claims from hallucinations ────────────────────────────
const hallucinations = results.filter((r) => r.verdict === false);
const verified = results.filter((r) => r.verdict === true);
const inconclusive = results.filter((r) => r.verdict === null);

if (hallucinations.length > 0) {
  console.log(`🚨 HALLUCINATIONS DETECTED (${hallucinations.length}):\n`);
  for (const res of hallucinations) {
    const sources = (res.source_urls || []).join(", ");
    console.log(`  ❌ "${res.claim}"`);
    console.log(`     Why it's wrong: ${res.explanation}`);
    console.log(`     Evidence: ${sources || "N/A"}`);
    console.log();
  }
} else {
  console.log("✅ No hallucinations detected.\n");
}

if (verified.length > 0) {
  console.log(`✅ Verified claims (${verified.length}):`);
  for (const res of verified) {
    console.log(`   ✓ "${res.claim}"`);
  }
  console.log();
}

if (inconclusive.length > 0) {
  console.log(`❓ Inconclusive (${inconclusive.length}):`);
  for (const res of inconclusive) {
    console.log(`   ? "${res.claim}"`);
  }
  console.log();
}

// ── Verdict ─────────────────────────────────────────────────────────────
const total = results.length;
console.log("─".repeat(50));
if (hallucinations.length > 0) {
  const pct = total > 0 ? ((hallucinations.length / total) * 100).toFixed(0) : 0;
  console.log(
    `  ⚠ Audit result: ${hallucinations.length}/${total} claims are false (${pct}% hallucination rate)`
  );
  console.log(
    "  → This LLM output should NOT be published without correction."
  );
} else {
  console.log("  ✓ Audit result: All claims verified. Safe to publish.");
}
