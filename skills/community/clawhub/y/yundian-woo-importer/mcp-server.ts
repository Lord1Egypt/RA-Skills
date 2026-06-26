#!/usr/bin/env node
/**
 * Yundian+ WooCommerce Importer MCP Server
 * 
 * Usage in Cursor/Trae:
 * Command: node mcp-server.js
 * Env: YUNDIAN_WOO_IMPORTER_API_KEY=your_api_key, YUNDIAN_WOO_IMPORTER_API_URL=https://your-domain.com
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const API_KEY = process.env.YUNDIAN_WOO_IMPORTER_API_KEY;
const API_URL = process.env.YUNDIAN_WOO_IMPORTER_API_URL || "http://localhost:3000"; // Note: Use the actual port where the app is running

if (!API_KEY) {
  console.error("Error: YUNDIAN_WOO_IMPORTER_API_KEY environment variable is required.");
  process.exit(1);
}

const server = new Server(
  {
    name: "yundian-woo-importer-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "import_products",
        description: "Queue products for import from Shopify, Wix, WordPress, or Amazon to WooCommerce.",
        inputSchema: {
          type: "object",
          properties: {
            platform: {
              type: "string",
              enum: ["shopify", "wix", "wordpress", "amazon"],
              description: "The source platform"
            },
            shopifyBaseUrl: {
              type: "string",
              description: "Required for Shopify. E.g., https://example.myshopify.com"
            },
            wixUrl: {
              type: "string",
              description: "Required for Wix"
            },
            productLinks: {
              type: "array",
              items: { type: "string" },
              description: "List of product URLs or handles to import"
            },
            mode: {
              type: "string",
              enum: ["all"],
              description: "Set to 'all' to discover and import all products (Shopify only)"
            }
          },
          required: ["platform"]
        }
      },
      {
        name: "check_import_status",
        description: "Check the status of an import job using the requestId",
        inputSchema: {
          type: "object",
          properties: {
            requestId: {
              type: "string",
              description: "The request ID returned by import_products"
            }
          },
          required: ["requestId"]
        }
      }
    ]
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    if (request.params.name === "import_products") {
      const response = await fetch(`${API_URL}/api/v1/import`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${API_KEY}`
        },
        body: JSON.stringify(request.params.arguments)
      });
      const data = await response.json();
      return {
        content: [{ type: "text", text: JSON.stringify(data, null, 2) }]
      };
    } 
    
    if (request.params.name === "check_import_status") {
      const { requestId } = request.params.arguments as any;
      const response = await fetch(`${API_URL}/api/v1/status?requestId=${requestId}`, {
        headers: {
          "Authorization": `Bearer ${API_KEY}`
        }
      });
      const data = await response.json();
      return {
        content: [{ type: "text", text: JSON.stringify(data, null, 2) }]
      };
    }

    throw new Error(`Unknown tool: ${request.params.name}`);
  } catch (error: any) {
    return {
      content: [{ type: "text", text: `Error: ${error.message}` }],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Yundian+ WooCommerce Importer MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
