/**
 * XO Protocol — MCP Server
 *
 * Model Context Protocol server that exposes XO Protocol as tools
 * for Claude Desktop, ChatGPT, or any MCP-compatible AI client.
 *
 * Tools: verify_identity, search_connections, get_reputation,
 *        get_social_signals, get_profile, get_newsfeed
 *
 * Prerequisites:
 *   npm install @modelcontextprotocol/sdk
 *
 * Usage:
 *   Set environment variables:
 *     XO_API_KEY=your-api-key
 *     XO_ACCESS_TOKEN=your-jwt-token
 *
 *   Then add to Claude Desktop config (~/.claude/mcp_servers.json):
 *   {
 *     "xo-protocol": {
 *       "command": "node",
 *       "args": ["/path/to/mcp-server.js"],
 *       "env": {
 *         "XO_API_KEY": "your-api-key",
 *         "XO_ACCESS_TOKEN": "your-jwt-token"
 *       }
 *     }
 *   }
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const API_BASE = "https://protocol.xoxo.space";
const API_KEY = process.env.XO_API_KEY;
const ACCESS_TOKEN = process.env.XO_ACCESS_TOKEN;

if (!API_KEY || !ACCESS_TOKEN) {
  console.error("Missing XO_API_KEY or XO_ACCESS_TOKEN environment variables");
  process.exit(1);
}

const headers = {
  "X-API-Key": API_KEY,
  Authorization: `Bearer ${ACCESS_TOKEN}`,
};

async function callApi(path, params = {}) {
  const url = new URL(`${API_BASE}${path}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined) url.searchParams.set(k, String(v));
  });

  const res = await fetch(url, { headers });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || error.title || `HTTP ${res.status}`);
  }
  return res.json();
}

const server = new Server(
  { name: "xo-protocol", version: "2.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "verify_identity",
      description:
        "Check if a user is a verified real person. Returns trust score, SBT status, and verification attestations.",
      inputSchema: { type: "object", properties: {} },
    },
    {
      name: "search_connections",
      description:
        "Find compatible people. Returns AI-computed compatibility scores and ephemeral IDs for further lookups.",
      inputSchema: {
        type: "object",
        properties: {
          limit: {
            type: "number",
            description: "Number of connections to return (1-50, default 10)",
          },
        },
      },
    },
    {
      name: "get_reputation",
      description:
        "Get a user's reputation tier (novice to S) and score. Use 'me' for yourself, or a tmp_id from search_connections.",
      inputSchema: {
        type: "object",
        properties: {
          token: {
            type: "string",
            description: "User token: 'me' or a tmp_id",
            default: "me",
          },
        },
      },
    },
    {
      name: "get_social_signals",
      description:
        "Get a user's conversation quality score and data confidence level. Useful for gauging engagement quality.",
      inputSchema: {
        type: "object",
        properties: {
          token: {
            type: "string",
            description: "User token: 'me' or a tmp_id",
            default: "me",
          },
        },
      },
    },
    {
      name: "get_profile",
      description:
        "Get a user's self-disclosed interests and preferences. Only returns what the user chose to share. Requires profile scope.",
      inputSchema: {
        type: "object",
        properties: {
          token: {
            type: "string",
            description: "User token: 'me' or a tmp_id",
            default: "me",
          },
        },
      },
    },
    {
      name: "get_newsfeed",
      description:
        "Browse a connection's publicly shared posts and topics. Great for discovering shared interests before starting a conversation.",
      inputSchema: {
        type: "object",
        required: ["tmp_id"],
        properties: {
          tmp_id: {
            type: "string",
            description: "Ephemeral ID from search_connections",
          },
          limit: {
            type: "number",
            description: "Number of posts to return (1-50, default 20)",
          },
        },
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case "verify_identity":
        result = await callApi("/protocol/v1/identity/verify");
        break;

      case "search_connections":
        result = await callApi("/protocol/v1/connections/search", {
          limit: args?.limit,
        });
        break;

      case "get_reputation":
        result = await callApi(
          `/protocol/v1/reputation/${args?.token || "me"}`
        );
        break;

      case "get_social_signals":
        result = await callApi(
          `/protocol/v1/social-signals/${args?.token || "me"}`
        );
        break;

      case "get_profile":
        result = await callApi(
          `/protocol/v1/profile/${args?.token || "me"}`
        );
        break;

      case "get_newsfeed":
        result = await callApi(
          `/protocol/v1/newsfeed/${args?.tmp_id}`,
          { limit: args?.limit }
        );
        break;

      default:
        return {
          content: [{ type: "text", text: `Unknown tool: ${name}` }],
          isError: true,
        };
    }

    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
