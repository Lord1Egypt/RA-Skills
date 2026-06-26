/**
 * Disinformation Shield - Veritier Use Case (JavaScript)
 * ========================================================
 * Screens user-generated content, social media posts, or news snippets for
 * false claims before they spread. Acts as a truth firewall for platforms
 * that need to catch misinformation at the point of entry.
 *
 * Unlike hallucination_audit (which targets AI-generated text), this example
 * targets human-authored content - viral posts, forwarded messages, and
 * news articles that may contain misleading or fabricated claims.
 *
 * Usage:
 *   1. npm install dotenv
 *   2. Set VERITIER_API_KEY in your .env
 *   3. node disinformation_shield.mjs
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

// ── Simulated user-generated content (social media post / forwarded message) ─
const incomingContent =
  "BREAKING: The WHO just confirmed that drinking hot water with lemon " +
  "cures the flu. A new study from Harvard Medical School published last " +
  "week found that 98% of patients recovered within 24 hours. The CDC has " +
  "already updated their official guidelines to recommend this treatment.";

console.log("🛡  Veritier Disinformation Shield");
console.log("━".repeat(50));
console.log(`\n📥 Incoming content:\n   "${incomingContent}"\n`);
console.log("⏳ Screening for false claims...\n");

const response = await fetch(`${API_URL}/v1/verify`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ text: incomingContent }),
});

if (!response.ok) {
  console.error(`✗ API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const results = data.results || [];

const falseClaims = results.filter((r) => r.verdict === false);
const unverifiedClaims = results.filter((r) => r.verdict === null);
const trueClaims = results.filter((r) => r.verdict === true);

// ── Display results ──────────────────────────────────────────────────────
if (falseClaims.length > 0) {
  console.log(
    `🚨 DISINFORMATION DETECTED (${falseClaims.length} false claim(s)):\n`
  );
  for (const r of falseClaims) {
    console.log(`  ❌ "${r.claim}"`);
    console.log(`     Why it's false: ${r.explanation ?? "N/A"}`);
    if (r.source_urls?.length) {
      console.log(`     Evidence: ${r.source_urls.slice(0, 3).join(", ")}`);
    }
    console.log();
  }
}

if (unverifiedClaims.length > 0) {
  console.log(
    `⚠  UNVERIFIABLE CLAIMS (${unverifiedClaims.length}):\n`
  );
  for (const r of unverifiedClaims) {
    console.log(`  ❓ "${r.claim}"`);
    console.log(
      `     Note: ${r.explanation ?? "Insufficient evidence to verify"}`
    );
    console.log();
  }
}

if (trueClaims.length > 0) {
  console.log(`✅ Verified claims (${trueClaims.length}):`);
  for (const r of trueClaims) {
    console.log(`   ✓ "${r.claim}"`);
  }
}

// ── Verdict summary ──────────────────────────────────────────────────────
console.log(`\n${"━".repeat(50)}`);
const total = results.length;
const risk = total > 0 ? ((falseClaims.length / total) * 100).toFixed(0) : 0;

if (falseClaims.length > 0) {
  console.log(
    `  🚫 BLOCKED - ${falseClaims.length}/${total} claims are false (${risk}% disinformation rate)`
  );
  console.log(`  → This content should NOT be published or shared.`);
} else if (unverifiedClaims.length > 0) {
  console.log(
    `  ⚠  FLAGGED - ${unverifiedClaims.length}/${total} claims could not be verified`
  );
  console.log(`  → This content requires human review before publishing.`);
} else {
  console.log(`  ✅ PASSED - All ${total} claims verified as accurate`);
  console.log(`  → This content is safe to publish.`);
}
