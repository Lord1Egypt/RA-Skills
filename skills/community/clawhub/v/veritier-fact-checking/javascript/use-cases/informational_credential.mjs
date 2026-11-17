/**
 * Informational Claim Credential on Verify - Veritier Use Case (JavaScript)
 * ==========================================================================
 * Optional action_id on POST /v1/verify mints a signed workpaper. Verdicts stay
 * the same; verify is not fail-closed. Use attest_action to gate a tool call.
 *
 * Usage:
 *   node informational_credential.mjs
 *
 * Docs: https://veritier.ai/docs#attestation
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const API_URL = "https://api.veritier.ai";

if (!API_KEY) {
  console.error("Error: VERITIER_API_KEY is not set.");
  process.exit(1);
}

const body = {
  text: "Water boils at 100 degrees Celsius at standard pressure.",
  grounding_mode: "web",
  action_id: "verify_workpaper_demo",
};
if (API_KEY.startsWith("vt_test_")) {
  body.mock_verdict = true;
  console.log("TEST MODE: mock_verdict=true plus action_id\n");
}

const response = await fetch(`${API_URL}/v1/verify`, {
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
const cred = data.credential || {};
console.log(`claims: ${ (data.results || []).length }`);
console.log(`informational credential: ${cred.id}`);
console.log(`verify_url: ${cred.verify_url}`);
console.log("Verify is not fail-closed. Use attest_action to gate an action.");

if (cred.id) {
  const pub = await fetch(`${API_URL}/v1/credentials/${cred.id}`);
  const reconstructed = pub.ok ? await pub.json() : { status: pub.status };
  console.log(`\npublic GET decision: ${reconstructed.decision ?? reconstructed.status}`);
}

if (data.warnings?.length) {
  console.log(`\nWarnings: ${data.warnings.join("; ")}`);
}
