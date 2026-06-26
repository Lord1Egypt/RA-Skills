/**
 * Verify Claims from a URL - Veritier Use Case (JavaScript)
 * ===========================================================
 * Fetches a publicly accessible URL and fact-checks every claim found
 * in the document using Veritier's real-time verification engine.
 *
 * Usage:
 *   node verify_article_url.mjs https://example.com/article
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

// ── Get URL from command-line argument ──────────────────────────────────
const url = process.argv[2];
if (!url) {
  console.log("Usage: node verify_article_url.mjs <URL>");
  console.log(
    "Example: node verify_article_url.mjs https://en.wikipedia.org/wiki/Moon"
  );
  process.exit(1);
}

console.log(`🔗 URL: ${url}\n`);
console.log("⏳ Fetching document and verifying claims...\n");

const response = await fetch(`${API_URL}/v1/verify`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    document: { type: "url", content: url },
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
let trueCount = 0,
  falseCount = 0,
  nullCount = 0;

console.log(`✓ Verified ${results.length} claim(s) from document:\n`);

for (const res of results) {
  const verdict = res.verdict;
  const icon = icons[String(verdict)] || "❓";
  const sources = (res.source_urls || []).join(", ");

  if (verdict === true) trueCount++;
  else if (verdict === false) falseCount++;
  else nullCount++;

  console.log(`  ${icon} Claim: '${res.claim}'`);
  console.log(`     Verdict:     ${verdict}`);
  console.log(`     Confidence:  ${res.confidence_score}`);
  console.log(`     Explanation: ${res.explanation}`);
  console.log(`     Sources: ${sources || "N/A"}`);
  console.log();
}

// ── Summary ─────────────────────────────────────────────────────────────
console.log("─".repeat(50));
console.log(
  `  Summary: ${trueCount} true · ${falseCount} false · ${nullCount} inconclusive`
);
console.log(
  `  Rate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);
