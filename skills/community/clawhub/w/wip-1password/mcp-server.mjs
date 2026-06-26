#!/usr/bin/env node
// mcp-server.mjs ... MCP server for 1Password secrets
// Uses `op` CLI with service account token for headless access.
// Register with: claude mcp add --scope user wip-1password -- node /path/to/mcp-server.mjs

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { execSync } from "node:child_process";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const HOME = process.env.HOME || "";
const TOKEN_PATH = process.env.OP_SA_TOKEN_PATH || join(HOME, ".openclaw/secrets/op-sa-token");
const DEFAULT_VAULT = process.env.OP_DEFAULT_VAULT || "Agent Secrets";

function getSAToken() {
  if (!existsSync(TOKEN_PATH)) {
    throw new Error(`Service account token not found at ${TOKEN_PATH}`);
  }
  return readFileSync(TOKEN_PATH, "utf8").trim();
}

function opExec(args) {
  const token = getSAToken();
  return execSync(`op ${args}`, {
    env: { ...process.env, OP_SERVICE_ACCOUNT_TOKEN: token },
    encoding: "utf8",
    timeout: 15000,
  }).trim();
}

const server = new Server(
  { name: "wip-1password", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "op_read_secret",
      description: "Read a secret value from 1Password. Returns the decrypted value.",
      inputSchema: {
        type: "object",
        properties: {
          item: { type: "string", description: "Item title (e.g. 'OpenAI API')" },
          vault: { type: "string", description: `Vault name (default: ${DEFAULT_VAULT})` },
          field: { type: "string", description: "Field name (default: 'api key')" },
        },
        required: ["item"],
      },
    },
    {
      name: "op_list_items",
      description: "List all items in a 1Password vault.",
      inputSchema: {
        type: "object",
        properties: {
          vault: { type: "string", description: `Vault name (default: ${DEFAULT_VAULT})` },
        },
      },
    },
    {
      name: "op_test",
      description: "Test 1Password connectivity. Returns account info if successful.",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "op_read_secret": {
        const vault = args.vault || DEFAULT_VAULT;
        const field = args.field || "api key";
        const ref = `op://${vault}/${args.item}/${field}`;
        const value = opExec(`read "${ref}"`);
        return {
          content: [{ type: "text", text: value }],
        };
      }

      case "op_list_items": {
        const vault = args.vault || DEFAULT_VAULT;
        const result = opExec(`item list --vault "${vault}" --format json`);
        const items = JSON.parse(result);
        const summary = items.map(i => `- ${i.title} (${i.category})`).join("\n");
        return {
          content: [{ type: "text", text: summary || "No items found." }],
        };
      }

      case "op_test": {
        const result = opExec("whoami --format json");
        const info = JSON.parse(result);
        return {
          content: [{
            type: "text",
            text: `Connected. Account: ${info.account_uuid || info.url || "ok"}`,
          }],
        };
      }

      default:
        return {
          content: [{ type: "text", text: `Unknown tool: ${name}` }],
          isError: true,
        };
    }
  } catch (e) {
    return {
      content: [{ type: "text", text: `Error: ${e.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
