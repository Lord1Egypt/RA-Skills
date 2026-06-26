#!/usr/bin/env node
const DEFAULT_BASE_URL = "http://localhost:8787";

function normalizeBaseUrl(value) {
  return value.replace(/\/+$/, "");
}

async function main() {
  const [, , toolName, rawArgs] = process.argv;

  if (!toolName) {
    console.error("Missing tool name");
    process.exit(1);
  }

  let args = {};
  if (rawArgs) {
    try {
      args = JSON.parse(rawArgs);
    } catch (error) {
      console.error(`Invalid JSON arguments: ${error instanceof Error ? error.message : String(error)}`);
      process.exit(4);
    }
  }

  if (!args || typeof args !== "object" || Array.isArray(args)) {
    console.error("Arguments must be a JSON object");
    process.exit(4);
  }

  const token = process.env.MY_MCP_TOKEN;
  if (!token) {
    console.error("Missing MY_MCP_TOKEN");
    process.exit(2);
  }

  const baseUrl = normalizeBaseUrl(process.env.MY_MCP_BASE_URL || DEFAULT_BASE_URL || "http://127.0.0.1:8787");
  const response = await fetch(`${baseUrl}/mcp/tools/${encodeURIComponent(toolName)}`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ arguments: args }),
  });

  const text = await response.text();
  if (!response.ok) {
    console.error(text || `Request failed: ${response.status} ${response.statusText}`);
    process.exit(3);
  }

  process.stdout.write(text.endsWith("\n") ? text : `${text}\n`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : String(error));
  process.exit(10);
});
