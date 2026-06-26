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
const MCP_URL = "https://api.veritier.ai/mcp/";  // hardcoded — never sent to any other domain

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
console.log(`  Key:      ${"*".repeat(8)} (length: ${API_KEY.length})\n`);

try {
  // [1] Initialize MCP session
  const init = await mcpRequest({
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: { name: "veritier-mcp-test-js", version: "2.0" },
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
  console.log(`\n⏳ Extracting claims from: "${extractText}"`);

  const extractResult = await mcpRequest({
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "extract_text",
      arguments: { text: extractText },
    },
  });

  const extractContent = extractResult.result.content[0].text;
  console.log("✓ extract_text result:\n");
  for (const line of extractContent.split("\n")) {
    console.log(`  ${line}`);
  }

  // [4] Test verify_text (with a known false claim)
  const testClaim = "The Eiffel Tower is located in Berlin.";
  console.log(`\n⏳ Verifying: "${testClaim}"`);

  const verifyResult = await mcpRequest({
    jsonrpc: "2.0",
    id: 4,
    method: "tools/call",
    params: {
      name: "verify_text",
      arguments: { text: testClaim },
    },
  });

  const verifyContent = verifyResult.result.content[0].text;
  console.log("✓ verify_text result:\n");
  for (const line of verifyContent.split("\n")) {
    console.log(`  ${line}`);
  }

  console.log(
    "\n✓ All checks passed! Your MCP integration is working correctly."
  );
} catch (err) {
  console.error(`\n✗ Error: ${err.message}`);
  process.exit(1);
}
