/**
 * Verify Claims from Text - Veritier Quickstart (JavaScript)
 * ============================================================
 * Extracts and fact-checks every claim in a block of text using live web evidence.
 * Uses native fetch (Node 18+) - no external HTTP library needed.
 *
 * Usage:
 *   1. npm install dotenv
 *   2. cp .env.example .env  (then add your API key)
 *   3. node verify_text.mjs
 *
 * Get your free API key: https://veritier.ai/register
 * Full docs: https://veritier.ai/docs
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";  // hardcoded � never sent to any other domain

if (!API_KEY) {
  console.error("✗ Error: VERITIER_API_KEY is not set.");
  console.error("  Get your free key at https://veritier.ai/register");
  process.exit(1);
}

// ── Sample text with a mix of true and false claims ─────────────────────
const sampleText =
  "Python was created by Guido van Rossum and first released in 1991. " +
  "The language is named after the British comedy group Monty Python. " +
  "Python 3 was released in December 2010.";

console.log(`📝 Input text:\n   "${sampleText}"\n`);
console.log("⏳ Verifying claims against live web evidence...\n");

const response = await fetch(`${API_URL}/v1/verify`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    text: sampleText,
    grounding_mode: "web",
  }),
});

if (!response.ok) {
  console.error(`✗ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const results = data.results || [];

const icons = { true: "✅", false: "❌", null: "❓" };

console.log(`✓ Verified ${results.length} claim(s):\n`);
for (const res of results) {
  const verdict = res.verdict;
  const icon = icons[String(verdict)] || "❓";
  const sources = (res.source_urls || []).join(", ");

  console.log(`  ${icon} Claim: '${res.claim}'`);
  console.log(`     Verdict:    ${verdict}`);
  console.log(`     Confidence: ${res.confidence_score}`);
  console.log(`     Explanation: ${res.explanation}`);
  console.log(`     Sources: ${sources || "N/A"}`);
  console.log();
}

if (data.warnings?.length) {
  console.log(`⚠ Warnings: ${data.warnings.join("; ")}`);
}

console.log(
  `── Rate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);

// ─── Zero-quota integration testing ──────────────────────────────────────────
// Use a test API key (vt_test_...) and the mock_verdict field to test your
// integration without consuming your monthly verification quota.
// Returns 3 deterministic ClaimResult objects; no LLM is called.
//
// mock_verdict: true  → all verdicts True  (happy-path / success handling)
// mock_verdict: false → all verdicts False (error-path / failure handling)
//
// Example (replace your prod key with a vt_test_... key from your dashboard):
//
//   const response = await fetch(${API_URL}/v1/verify, {
//     method: "POST",
//     headers: {
//       Authorization: Bearer , // vt_test_... key
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ text: sampleText, mock_verdict: true }),
//   });
//   const data = await response.json();
//   console.log(data.is_test === true);     // confirms test mode
//
// See https://veritier.ai/docs#testing for full details.
//
// Optional action_id mints an informational Claim Credential. Verdicts stay
// the same; verify is not fail-closed. Use attest_action to gate a tool call.
// See use-cases/informational_credential.mjs and quickstart/attest_action.mjs.
