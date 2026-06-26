/**
 * Extract Claims from Text - Veritier Quickstart (JavaScript)
 * =============================================================
 * Extracts every falsifiable claim from a block of text WITHOUT verifying them.
 * Uses native fetch (Node 18+) - no external HTTP library needed.
 *
 * Usage:
 *   1. npm install dotenv
 *   2. cp .env.example .env  (then add your API key)
 *   3. node extract_text.mjs
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

// ── Sample text with multiple claims ────────────────────────────────────
const sampleText =
  "The Great Wall of China is over 13,000 miles long. " +
  "It was built during the Ming Dynasty. " +
  "The wall is visible from the International Space Station with the naked eye.";

console.log(`📝 Input text:\n   "${sampleText}"\n`);
console.log("⏳ Extracting claims...\n");

const response = await fetch(`${API_URL}/v1/extract`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ text: sampleText }),
});

if (!response.ok) {
  console.error(`✗ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const claims = data.claims || [];

console.log(`✓ Extracted ${claims.length} claim(s):\n`);
claims.forEach((claim, i) => {
  console.log(`  ${i + 1}. ${claim}`);
});

if (data.warnings?.length) {
  console.log(`\n⚠ Warnings: ${data.warnings.join("; ")}`);
}

console.log(
  `\n── Rate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);
