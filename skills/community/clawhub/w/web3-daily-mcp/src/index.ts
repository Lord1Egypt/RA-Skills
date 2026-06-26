#!/usr/bin/env node
/**
 * Web3 Daily MCP Server
 * 
 * Provides real-time Web3 research digest through MCP protocol.
 * This server wraps the J4Y backend API and exposes it as MCP tools.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_BASE = "https://j4y-production.up.railway.app";

// Create MCP server
const server = new McpServer({
  name: "web3-daily",
  version: "1.0.0",
});

/**
 * Tool: get_public_digest
 * Get public Web3 digest (no wallet required)
 */
server.tool(
  "get_public_digest",
  "Get today's Web3 public digest with macro news, KOL sentiment, and market data. No personal data required.",
  {
    language: z.enum(["zh", "en"]).default("zh").describe("Output language: zh (Chinese) or en (English)"),
  },
  async ({ language }) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/digest/public`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language }),
      });

      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.message || "Failed to generate digest");
      }

      return {
        content: [
          {
            type: "text",
            text: data.digest,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching public digest: ${error instanceof Error ? error.message : "Unknown error"}`,
          },
        ],
        isError: true,
      };
    }
  }
);

/**
 * Tool: get_personalized_digest
 * Get personalized Web3 digest based on wallet address
 */
server.tool(
  "get_personalized_digest",
  "Get personalized Web3 digest based on your wallet's on-chain behavior. Includes holdings analysis, relevant news, and tailored recommendations.",
  {
    wallet_address: z.string().regex(/^0x[a-fA-F0-9]{40}$/).describe("EVM wallet address (0x + 40 hex characters)"),
    language: z.enum(["zh", "en"]).default("zh").describe("Output language: zh (Chinese) or en (English)"),
  },
  async ({ wallet_address, language }) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/digest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ wallet_address, language }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API returned ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.message || "Failed to generate personalized digest");
      }

      return {
        content: [
          {
            type: "text",
            text: data.digest,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching personalized digest: ${error instanceof Error ? error.message : "Unknown error"}`,
          },
        ],
        isError: true,
      };
    }
  }
);

/**
 * Tool: get_wallet_profile
 * Get on-chain profile analysis for a wallet
 */
server.tool(
  "get_wallet_profile",
  "Analyze a wallet's on-chain behavior and generate an investor profile. Includes holdings, transaction patterns, and investment style.",
  {
    wallet_address: z.string().regex(/^0x[a-fA-F0-9]{40}$/).describe("EVM wallet address (0x + 40 hex characters)"),
    language: z.enum(["zh", "en"]).default("zh").describe("Output language: zh (Chinese) or en (English)"),
    force_update: z.boolean().default(false).describe("Force regenerate profile (bypass 24h cache)"),
  },
  async ({ wallet_address, language, force_update }) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/profile`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ wallet_address, language, force_update }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `API returned ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status !== "success") {
        throw new Error(data.message || "Failed to generate profile");
      }

      // Format profile for display
      const profile = data.display_profile;
      const formattedProfile = `
# Wallet Profile: ${wallet_address.slice(0, 6)}...${wallet_address.slice(-4)}

## Summary
${profile.summary || profile.deep_insight}

## Asset Overview
- Total Value: $${profile.asset_overview?.total_value?.toLocaleString() || "N/A"}
- Top Holdings: ${profile.asset_overview?.top_holdings?.map((h: any) => `${h.symbol} (${h.percentage}%)`).join(", ") || "N/A"}

## Investment Style
${profile.personality_brief || "N/A"}

## Recent Activity
${profile.recent_TX || "N/A"}

## Interest Areas
${profile.interest_radar || "N/A"}
`;

      return {
        content: [
          {
            type: "text",
            text: formattedProfile,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching wallet profile: ${error instanceof Error ? error.message : "Unknown error"}`,
          },
        ],
        isError: true,
      };
    }
  }
);

/**
 * Tool: get_market_overview
 * Get current market data (BTC/ETH prices, Fear & Greed Index)
 */
server.tool(
  "get_market_overview",
  "Get current crypto market overview including BTC/ETH prices and Fear & Greed Index.",
  {},
  async () => {
    try {
      const response = await fetch(`${API_BASE}/health`);
      
      if (!response.ok) {
        throw new Error("Service unavailable");
      }

      // Fetch public digest to get market data (it's cached)
      const digestResponse = await fetch(`${API_BASE}/api/v1/digest/public`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: "en" }),
      });

      if (!digestResponse.ok) {
        throw new Error(`API returned ${digestResponse.status}`);
      }

      const data = await digestResponse.json();
      
      // Extract market overview section from digest
      const digest = data.digest || "";
      const marketMatch = digest.match(/## 📊 Market Overview[\s\S]*?(?=## 📰|---)/);
      
      if (marketMatch) {
        return {
          content: [
            {
              type: "text",
              text: marketMatch[0].trim(),
            },
          ],
        };
      }

      return {
        content: [
          {
            type: "text",
            text: "Market data available in full digest. Use get_public_digest for complete information.",
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching market overview: ${error instanceof Error ? error.message : "Unknown error"}`,
          },
        ],
        isError: true,
      };
    }
  }
);

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Web3 Daily MCP Server started");
}

main().catch(console.error);
