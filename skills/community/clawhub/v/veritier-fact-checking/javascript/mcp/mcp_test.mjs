/**
 * Veritier MCP Integration Test (JavaScript)
 * =============================================
 * Verifies that the Veritier MCP Streamable HTTP endpoint is reachable
 * and responds correctly to MCP JSON-RPC requests using native fetch.
 *
 * This test uses the REMOTE HTTP transport (recommended) - no local
 * proxy or Python required.
 *
 * Usage:
 *   1. npm install dotenv
 *   2. Set VERITIER_API_KEY in your .env
 *   3. node mcp_test.mjs
 *
 * Get your free API key: https://veritier.ai/register
 */

import "dotenv/config";

const API_KEY = process.env.VERITIER_API_KEY || "";
const MCP_URL = "https://api.veritier.ai/mcp/";  // hardcoded - never sent to any other domain
const IS_TEST = API_KEY.startsWith("vt_test_");
const modeLabel = IS_TEST ? "TEST MODE (zero-quota, mock responses)" : "🔴 PRODUCTION MODE (quota will be consumed)";

if (!API_KEY) {
  console.error("✗ Error: VERITIER_API_KEY is not set.");
  console.error("  Get your free key at https://veritier.ai/register");
  process.exit(1);
}

const EXPECTED_TOOLS = [
  "extract_text",
  "extract_document",
  "verify_text",
  "verify_document",
  "validate",
  "attest_action",
];

/**
 * Send a JSON-RPC request to the MCP endpoint.
 */
async function mcpRequest(body) {
  const response = await fetch(MCP_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }

  return response.json();
}

console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
console.log("  Veritier MCP Integration Test (JS)");
console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
console.log(`  Endpoint: ${MCP_URL}`);
console.log(`  Key:      ${"*".repeat(8)} (length: ${API_KEY.length})`);
console.log(`  Mode:     ${modeLabel}\n`);

try {
  // [1] Initialize MCP session
  const init = await mcpRequest({
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "veritier-mcp-test-js", version: "2.2" },
    },
  });

  const serverInfo = init.result.serverInfo;
  console.log(
    `✓ Initialize: server=${serverInfo.name} v${serverInfo.version}`
  );

  // [2] Discover available tools
  const tools = await mcpRequest({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/list",
  });

  const toolNames = tools.result.tools.map((t) => t.name);
  console.log(`✓ Tools discovered: [${toolNames.join(", ")}]`);

  const missing = EXPECTED_TOOLS.filter((t) => !toolNames.includes(t));
  if (missing.length > 0) {
    console.error(`✗ Error: Missing expected tools: ${missing.join(", ")}`);
    process.exit(1);
  }

  // [3] Test extract_text
  const extractText =
    "The Eiffel Tower is located in Paris, France. It stands 330 metres tall.";
  const extractArgs = { text: extractText };
  if (IS_TEST) {
    extractArgs.mock_claims = 2;
    console.log(`\n⏳ [TEST] Extracting 2 mock claims from: "${extractText}"`);
  } else {
    console.log(`\n⏳ Extracting claims from: "${extractText}"`);
  }

  const extractResult = await mcpRequest({
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "extract_text",
      arguments: extractArgs,
    },
  });

  const extractContent = extractResult.result.content[0].text;
  console.log("✓ extract_text result:\n");
  for (const line of extractContent.split("\n")) {
    console.log(`  ${line}`);
  }
  if (IS_TEST && extractContent.includes("[TEST MODE]")) {
    console.log("✓ is_test flag confirmed in extract response");
  }

  // [4] Test verify_text (with a known false claim)
  const testClaim = "The Eiffel Tower is located in Berlin.";
  const verifyArgs = { text: testClaim };
  if (IS_TEST) {
    verifyArgs.mock_verdict = false;
    verifyArgs.action_id = "mcp_test_verify";
    console.log(`\n⏳ [TEST] Verifying with mock_verdict=false and action_id: "${testClaim}"`);
  } else {
    console.log(`\n⏳ Verifying: "${testClaim}"`);
  }

  const verifyResult = await mcpRequest({
    jsonrpc: "2.0",
    id: 4,
    method: "tools/call",
    params: {
      name: "verify_text",
      arguments: verifyArgs,
    },
  });

  const verifyContent = verifyResult.result.content[0].text;
  console.log("✓ verify_text result:\n");
  for (const line of verifyContent.split("\n")) {
    console.log(`  ${line}`);
  }
  if (IS_TEST && verifyContent.includes("[TEST MODE]")) {
    console.log("✓ is_test flag confirmed in verify response");
  }
  if (IS_TEST && verifyContent.includes("Informational credential")) {
    console.log("✓ verify_text action_id minted an informational credential");
  }

  // [5] Test validate
  const testUrl = "https://example.com/doc.pdf";
  const validateArgs = { url: testUrl };
  if (IS_TEST) {
    validateArgs.mock_validation = true;
    console.log(`\n⏳ [TEST] Validating with mock_validation=true: "${testUrl}"`);
  } else {
    console.log(`\n⏳ Validating: "${testUrl}"`);
  }

  const validateResult = await mcpRequest({
    jsonrpc: "2.0",
    id: 5,
    method: "tools/call",
    params: {
      name: "validate",
      arguments: validateArgs,
    },
  });

  const validateContent = validateResult.result.content[0].text;
  console.log("✓ validate result:\n");
  for (const line of validateContent.split("\n")) {
    console.log(`  ${line}`);
  }
  if (IS_TEST && validateContent.includes("[TEST MODE]")) {
    console.log("✓ is_test flag confirmed in validate response");
  }

  // [6] Test attest_action (test mode only - live attest hits npm)
  if (IS_TEST) {
    console.log('\n⏳ [TEST] Attesting with mock_decision=allow: "npm install lodash"');
    const attestResult = await mcpRequest({
      jsonrpc: "2.0",
      id: 6,
      method: "tools/call",
      params: {
        name: "attest_action",
        arguments: {
          action_id: "mcp_test_attest",
          text: "npm install lodash",
          procedure: "package_exists",
          mock_decision: "allow",
        },
      },
    });
    const attestContent = attestResult.result.content[0].text;
    console.log("✓ attest_action result:\n");
    for (const line of attestContent.split("\n").slice(0, 20)) {
      console.log(`  ${line}`);
    }
    if (attestContent.includes("crc_")) {
      console.log("✓ attest_action returned a credential id");
    }
  }

  console.log(
    "\n✓ All checks passed! Your MCP integration is working correctly."
  );
  if (IS_TEST) {
    console.log("  Zero quota was consumed - switch to a production key for live fact-checking.");
  }
} catch (err) {
  console.error(`\n✗ Error: ${err.message}`);
  process.exit(1);
}
