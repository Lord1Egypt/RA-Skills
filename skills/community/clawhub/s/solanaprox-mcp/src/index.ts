#!/usr/bin/env node
/**
 * SolanaProx MCP Server
 * Lets AI agents pay for inference using Solana/USDC
 * No API keys. Your wallet is your identity.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

const SOLANAPROX_URL = process.env.SOLANAPROX_URL || "https://solanaprox.com";
const WALLET_ADDRESS = process.env.SOLANA_WALLET || "";

if (!WALLET_ADDRESS) {
  console.error("❌ SOLANA_WALLET environment variable is required");
  console.error("   Set it to your Phantom wallet address");
  console.error("   Example: SOLANA_WALLET=FjGCr4... npx solanaprox-mcp");
  process.exit(1);
}

// ============================================================================
// TOOL DEFINITIONS
// ============================================================================

const tools: Tool[] = [
  {
    name: "ask_ai",
    description:
      "Send a prompt to an AI model via SolanaProx. Costs are automatically deducted from your Solana wallet balance in USDC. Supports Claude and GPT-4 models. Use this for any AI inference task.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: {
          type: "string",
          description: "The prompt or question to send to the AI model",
        },
        model: {
          type: "string",
          description:
            "AI model to use. Options: claude-sonnet-4-20250514 (default), gpt-4-turbo",
          default: "claude-sonnet-4-20250514",
        },
        max_tokens: {
          type: "number",
          description: "Maximum tokens in response (default: 1024, max: 4096)",
          default: 1024,
        },
        system: {
          type: "string",
          description: "Optional system prompt to set context for the AI",
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "check_balance",
    description:
      "Check your current SolanaProx balance. Returns available USDC and SOL balance that can be used for AI requests.",
    inputSchema: {
      type: "object",
      properties: {
        wallet: {
          type: "string",
          description:
            "Solana wallet address to check. Defaults to configured wallet.",
        },
      },
      required: [],
    },
  },
  {
    name: "estimate_cost",
    description:
      "Estimate the cost of an AI request before making it. Returns estimated USD cost based on prompt length and model.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: {
          type: "string",
          description: "The prompt to estimate cost for",
        },
        model: {
          type: "string",
          description: "Model to use for estimation",
          default: "claude-sonnet-4-20250514",
        },
        max_tokens: {
          type: "number",
          description: "Expected max tokens in response",
          default: 1024,
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "list_models",
    description:
      "List all available AI models on SolanaProx with their pricing.",
    inputSchema: {
      type: "object",
      properties: {},
      required: [],
    },
  },
];

// ============================================================================
// API HELPERS
// ============================================================================

async function callAI(
  prompt: string,
  model: string = "claude-sonnet-4-20250514",
  maxTokens: number = 1024,
  system?: string
): Promise<{ response: string; cost_usd: number; model: string }> {
  const messages: any[] = [{ role: "user", content: prompt }];

  const body: any = {
    model,
    max_tokens: maxTokens,
    messages,
  };

  if (system) {
    body.system = system;
  }

  const res = await fetch(`${SOLANAPROX_URL}/v1/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Wallet-Address": WALLET_ADDRESS,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const error = await res.text();
    if (res.status === 402) {
      throw new Error(
        `Insufficient balance. Deposit USDC at ${SOLANAPROX_URL} to continue. Wallet: ${WALLET_ADDRESS}`
      );
    }
    throw new Error(`SolanaProx API error (${res.status}): ${error}`);
  }

  const data = await res.json() as any;

  const responseText =
    data.content?.[0]?.text ||
    data.choices?.[0]?.message?.content ||
    JSON.stringify(data);

  // Estimate cost from usage if available
  const inputTokens = data.usage?.input_tokens || 0;
  const outputTokens = data.usage?.output_tokens || 0;
  const costUSD = estimateCostFromTokens(model, inputTokens, outputTokens);

  return {
    response: responseText,
    cost_usd: costUSD,
    model: data.model || model,
  };
}

async function getBalance(wallet?: string): Promise<{
  total_usd: number;
  usdc: number;
  sol_usd: number;
  wallet: string;
}> {
  const targetWallet = wallet || WALLET_ADDRESS;
  const res = await fetch(
    `${SOLANAPROX_URL}/api/balance/${targetWallet}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch balance: ${res.statusText}`);
  }

  return res.json() as any;
}

async function getCapabilities(): Promise<any> {
  const res = await fetch(`${SOLANAPROX_URL}/api/capabilities`);
  if (!res.ok) throw new Error("Failed to fetch capabilities");
  return res.json();
}

function estimateCostFromTokens(
  model: string,
  inputTokens: number,
  outputTokens: number
): number {
  // Pricing per 1M tokens (with 20% markup)
  const pricing: Record<string, { input: number; output: number }> = {
    "claude-sonnet-4-20250514": { input: 3.6, output: 18.0 },
    "claude-3-5-sonnet-20241022": { input: 3.6, output: 18.0 },
    "gpt-4-turbo": { input: 12.0, output: 36.0 },
  };

  const p = pricing[model] || { input: 3.6, output: 18.0 };
  return (inputTokens * p.input + outputTokens * p.output) / 1_000_000;
}

function estimateCostFromPrompt(
  prompt: string,
  model: string,
  maxTokens: number
): number {
  // Rough estimate: 4 chars per token
  const estimatedInputTokens = Math.ceil(prompt.length / 4);
  const estimatedOutputTokens = maxTokens / 2; // assume half of max
  return estimateCostFromTokens(
    model,
    estimatedInputTokens,
    estimatedOutputTokens
  );
}

// ============================================================================
// MCP SERVER
// ============================================================================

const server = new Server(
  {
    name: "solanaprox",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "ask_ai": {
        const { prompt, model, max_tokens, system } = args as any;

        const result = await callAI(
          prompt,
          model || "claude-sonnet-4-20250514",
          max_tokens || 1024,
          system
        );

        return {
          content: [
            {
              type: "text",
              text: `${result.response}\n\n---\n⚡ Powered by SolanaProx | Model: ${result.model} | Cost: ~$${result.cost_usd.toFixed(6)} USDC`,
            },
          ],
        };
      }

      case "check_balance": {
        const { wallet } = args as any;
        const balance = await getBalance(wallet);

        return {
          content: [
            {
              type: "text",
              text: [
                `💰 SolanaProx Balance`,
                `Wallet: ${balance.wallet || WALLET_ADDRESS}`,
                `Total: $${balance.total_usd?.toFixed(4)} USD`,
                `USDC: $${balance.usdc?.toFixed(4)}`,
                `SOL value: $${balance.sol_usd?.toFixed(4)}`,
                ``,
                balance.total_usd > 0
                  ? `✅ Ready to make AI requests`
                  : `⚠️  No balance. Deposit USDC at ${SOLANAPROX_URL}`,
              ].join("\n"),
            },
          ],
        };
      }

      case "estimate_cost": {
        const { prompt, model, max_tokens } = args as any;
        const cost = estimateCostFromPrompt(
          prompt,
          model || "claude-sonnet-4-20250514",
          max_tokens || 1024
        );

        return {
          content: [
            {
              type: "text",
              text: [
                `💵 Cost Estimate`,
                `Model: ${model || "claude-sonnet-4-20250514"}`,
                `Prompt length: ~${Math.ceil(prompt.length / 4)} tokens`,
                `Max output: ${max_tokens || 1024} tokens`,
                `Estimated cost: ~$${cost.toFixed(6)} USDC`,
                ``,
                `Note: Cached responses get 50% discount`,
              ].join("\n"),
            },
          ],
        };
      }

      case "list_models": {
        const capabilities = await getCapabilities();

        const modelList = capabilities.models
          ?.map(
            (m: any) =>
              `• ${m.id}\n  Provider: ${m.provider}\n  Cost: $${m.pricing?.input_per_1m || "?"}/1M input tokens`
          )
          .join("\n\n");

        return {
          content: [
            {
              type: "text",
              text: `🤖 Available Models on SolanaProx\n\n${modelList || "Claude Sonnet 4, GPT-4 Turbo"}\n\nPay with SOL or USDC. Deposit at ${SOLANAPROX_URL}`,
            },
          ],
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `❌ Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// ============================================================================
// START
// ============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(
    `✅ SolanaProx MCP Server running | Wallet: ${WALLET_ADDRESS.slice(0, 8)}...`
  );
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
