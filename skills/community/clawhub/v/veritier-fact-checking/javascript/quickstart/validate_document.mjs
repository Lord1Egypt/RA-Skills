/**
 * Document Authenticity Scan - Veritier Quickstart (JavaScript)
 * ==============================================================
 * REST fields: document_url, document_base64, or extracted_text (not "url").
 * MCP validate still uses the parameter name "url".
 *
 * Usage:
 *   node validate_document.mjs
 *
 * Docs: https://veritier.ai/docs
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";

if (!API_KEY) {
  console.error("Error: VERITIER_API_KEY is not set.");
  process.exit(1);
}

const body = {
  extracted_text: "Certificate of completion issued to Jane Doe on 12 January 2024.",
};
if (API_KEY.startsWith("vt_test_")) {
  body.mock_validation = true;
  console.log("TEST MODE: mock_validation=true (no pipeline, no quota)\n");
}

console.log("Running authenticity scan...\n");

const response = await fetch(`${API_URL}/v1/validate`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(body),
});

if (!response.ok) {
  console.error(`API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const result = data.result || data;
console.log(`verdict:          ${result.verdict}`);
console.log(`fraud_risk_score: ${result.fraud_risk_score}`);
console.log(`document_type:    ${result.document_type}`);
if (data.is_test) console.log("is_test: true");

if (data.warnings?.length) {
  console.log(`\nWarnings: ${data.warnings.join("; ")}`);
}

console.log(
  `\nRate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);
