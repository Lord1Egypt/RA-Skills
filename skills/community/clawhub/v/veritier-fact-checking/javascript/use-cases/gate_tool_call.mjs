/**
 * Gate a Tool Call - Veritier Use Case (JavaScript)
 * ==================================================
 * Attest before the agent runs a command. Only proceed on decision=allow.
 * HTTP 200 with decision=block means refuse the action (success, not an error).
 *
 * Usage:
 *   node gate_tool_call.mjs
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

const command = "npm install lodash";
const payload = {
  action_id: "agent_npm_install",
  text: command,
  procedure: "package_exists",
  on_null: "block",
};
if (API_KEY.startsWith("vt_test_")) {
  payload.mock_decision = "allow";
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
  console.error(`Attest failed (${response.status}): ${await response.text()}`);
  process.exit(1);
}

const data = await response.json();
const cred = data.credential || {};

console.log(`command:  ${command}`);
console.log(`decision: ${data.decision}`);
console.log(`workpaper: ${cred.verify_url}`);

if (data.decision !== "allow") {
  console.log("Refusing to run the command. The gate fired.");
  process.exit(2);
}

console.log("Allowed. In a real agent you would now execute the command.");
console.log("Informational verify credentials are not a gate - use attest_action.");
