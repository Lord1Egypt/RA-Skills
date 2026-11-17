/**
 * Reconstruct a Claim Credential - Veritier Quickstart (JavaScript)
 * ==================================================================
 * Public GET needs no API key. JWKS lists current and previous Ed25519 kids.
 *
 * Usage:
 *   node reconstruct_credential.mjs crc_...
 *   node reconstruct_credential.mjs crc_... --revoke
 *
 * Docs: https://veritier.ai/docs#attestation
 */

import "dotenv/config";

const API_URL = "https://api.veritier.ai";
const API_KEY = process.env.VERITIER_API_KEY || "";
const args = process.argv.slice(2).filter((a) => a !== "--revoke");
const doRevoke = process.argv.includes("--revoke");
const credId = args[0] || process.env.VERITIER_CREDENTIAL_ID || "";

if (!credId) {
  console.error("Usage: node reconstruct_credential.mjs crc_... [--revoke]");
  process.exit(1);
}

const jwk = await fetch(`${API_URL}/v1/credentials/.well-known/jwk`);
if (!jwk.ok) {
  console.error(`JWKS error (${jwk.status}): ${await jwk.text()}`);
  process.exit(1);
}
const kids = ((await jwk.json()).keys || []).map((k) => k.kid);
console.log(`JWKS kids: ${kids.join(", ")}\n`);

const pub = await fetch(`${API_URL}/v1/credentials/${credId}`);
if (!pub.ok) {
  console.error(`GET error (${pub.status}): ${await pub.text()}`);
  process.exit(1);
}

const data = await pub.json();
console.log(`id:              ${data.id}`);
console.log(`decision:        ${data.decision}`);
console.log(`procedure:       ${data.procedure}`);
console.log(`action_id:       ${data.action_id}`);
console.log(`engine_version:  ${data.engine_version}`);
console.log(`signature_valid: ${data.signature_valid}`);
console.log(`revoked:         ${data.revoked}`);
console.log(`as_of:           ${data.as_of}`);
console.log(`public page:     https://veritier.ai/c/${credId}`);
console.log("\nThis is a workpaper, not a judicial finding.");

if (data.revoked) {
  console.log("Issuer revoked this credential. Do not treat the decision as current.");
}

if (doRevoke) {
  if (!API_KEY) {
    console.error("\n--revoke requires VERITIER_API_KEY (same account that issued it).");
    process.exit(1);
  }
  const revoked = await fetch(`${API_URL}/v1/credentials/${credId}/revoke`, {
    method: "POST",
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
  console.log(`\nrevoke HTTP ${revoked.status}: ${(await revoked.text()).slice(0, 300)}`);
}
