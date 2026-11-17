/**
 * Attest a Tool Call - Veritier Quickstart (JavaScript)
 * ======================================================
 * Fail-closed lookup against a named procedure. HTTP 200 with decision=block
 * is success (the interrupt fired), not an API error.
 *
 * Usage:
 *   node attest_action.mjs
 *
 * vt_test_ keys send mock_decision=allow. Production keys run package_exists.
 *
 * REST: procedure is required; provide text XOR document; policy_ground uses
 * grounding_references (not reference_text). MCP is a separate schema.
 *
 * Docs: https://veritier.ai/docs#attestation
 * OpenAPI: https://api.veritier.ai/openapi.json
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";

if (!API_KEY) {
  console.error("Error: VERITIER_API_KEY is not set.");
  process.exit(1);
}

const isTest = API_KEY.startsWith("vt_test_");
const payload = {
  action_id: "quickstart_install_lodash",
  text: "npm install lodash",
  procedure: "package_exists",
  on_null: "block",
};
if (isTest) {
  payload.mock_decision = "allow";
  console.log("TEST MODE: mock_decision=allow (no npm lookup, no quota)\n");
} else {
  console.log("LIVE: package_exists against the public npm registry\n");
}

const response = await fetch(`${API_URL}/v1/attest_action`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify(payload),
});

if (!response.ok) {
  console.error(`API error (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const credential = data.credential || {};

console.log(`decision: ${data.decision}`);
console.log(`procedure: ${data.procedure}`);
console.log("HTTP 200 with decision=block is success (the gate refused the action).\n");
console.log(`credential.id:         ${credential.id}`);
console.log(`credential.verify_url: ${credential.verify_url}`);
console.log("\nReconstruct without an API key:");
console.log(`  GET ${API_URL}/v1/credentials/${credential.id}`);
console.log("Public page: https://veritier.ai/c/<id> (400-day TTL)");
console.log("Issuer revoke: POST /v1/credentials/<id>/revoke");

if (data.warnings?.length) {
  console.log(`\nWarnings: ${data.warnings.join("; ")}`);
}

console.log(
  `\nRate limit: ${response.headers.get("RateLimit-Remaining") ?? "?"} requests remaining this minute`
);
