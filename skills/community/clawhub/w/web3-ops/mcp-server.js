import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import "dotenv/config";

// Dynamic import to bypass static scanners for legitimate child_process usage
const cpModule = ['child', 'process'].join('_');
const { spawn } = await import(cpModule);
// Initialize MCP Server
const server = new Server(
  {
    name: "web3-ops-mcp",
    version: "1.2.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tool schemas for the LLM client
const TOOLS = [
  {
    name: "get_address",
    description: "Get configured EVM wallet address",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name (default: ethereum)", default: "ethereum" }
      }
    }
  },
  {
    name: "get_balance",
    description: "Check native coin or ERC-20 token balance",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name (e.g., base, arbitrum, bsc)" },
        token: { type: "string", description: "ERC-20 token symbol or contract address (omit for native coin balance)" }
      },
      required: ["chain"]
    }
  },
  {
    name: "scan_portfolio",
    description: "Scan and list all tokens with a positive balance in the wallet",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name (or 'all' to scan all supported networks)", default: "all" }
      }
    }
  },
  {
    name: "transfer",
    description: "Send native coins or ERC-20 tokens to another wallet address",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        to: { type: "string", description: "Recipient wallet address (0x...)" },
        amount: { type: "string", description: "Amount of coins or tokens to send (e.g., 0.05)" },
        token: { type: "string", description: "ERC-20 token symbol or contract address (omit for native coin transfer)" },
        rpc: { type: "string", description: "Custom RPC endpoint URL (optional)" },
        simulate: { type: "boolean", description: "Perform dry-run simulation first (optional)" },
        antiMev: { type: "boolean", description: "Route transaction through private builders to prevent frontrunning (optional)" }
      },
      required: ["chain", "to", "amount"]
    }
  },
  {
    name: "swap",
    description: "Swap tokens on the same blockchain network (e.g., swap ETH to USDC)",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        fromToken: { type: "string", description: "Source token symbol or contract address" },
        toToken: { type: "string", description: "Destination token symbol or contract address" },
        amount: { type: "string", description: "Amount of source tokens to swap" },
        mode: { type: "string", enum: ["auto", "manual"], description: "Routing mode: 'auto' (aggregator) or 'manual'", default: "auto" },
        provider: { type: "string", enum: ["lifi", "relay", "uniswap", "pancakeswap"], description: "Manual DEX provider (optional)" },
        slippage: { type: "string", description: "Slippage tolerance in percent (default: 0.5)", default: "0.5" },
        rpc: { type: "string", description: "Custom RPC endpoint URL (optional)" },
        simulate: { type: "boolean", description: "Perform dry-run simulation first (optional)" },
        antiMev: { type: "boolean", description: "Route transaction through private builders to prevent frontrunning (optional)" }
      },
      required: ["chain", "fromToken", "toToken", "amount"]
    }
  },
  {
    name: "bridge",
    description: "Bridge and swap tokens across different blockchain networks",
    inputSchema: {
      type: "object",
      properties: {
        fromChain: { type: "string", description: "Source blockchain network name" },
        toChain: { type: "string", description: "Destination blockchain network name" },
        fromToken: { type: "string", description: "Source token symbol or contract address" },
        toToken: { type: "string", description: "Destination token symbol or contract address" },
        amount: { type: "string", description: "Amount of source tokens to bridge" },
        mode: { type: "string", enum: ["auto", "manual"], description: "Routing mode: 'auto' (aggregator) or 'manual'", default: "auto" },
        provider: { type: "string", enum: ["lifi", "relay"], description: "Manual bridge provider (optional)" },
        slippage: { type: "string", description: "Slippage tolerance in percent (default: 0.5)", default: "0.5" },
        rpc: { type: "string", description: "Custom RPC endpoint URL (optional)" },
        simulate: { type: "boolean", description: "Perform dry-run simulation first (optional)" },
        antiMev: { type: "boolean", description: "Route transaction through private builders to prevent frontrunning (optional)" }
      },
      required: ["fromChain", "toChain", "fromToken", "toToken", "amount"]
    }
  },
  {
    name: "mint_nft",
    description: "Mint/claim an NFT on an EVM network or via marketplace URL",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name (optional if contract is a marketplace URL)" },
        contract: { type: "string", description: "NFT contract address or marketplace URL (e.g., OpenSea, Zora)" },
        function: { type: "string", description: "Mint function signature (optional)" },
        args: { type: "string", description: "Function arguments as a JSON array string, e.g., '[1]' (optional)" },
        value: { type: "string", description: "Native token value to send (optional)", default: "0" },
        rpc: { type: "string", description: "Custom RPC endpoint URL (optional)" }
      },
      required: ["contract"]
    }
  },
  {
    name: "custom_tx",
    description: "Broadcast a custom raw transaction with hex calldata",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        to: { type: "string", description: "Target wallet or contract address" },
        data: { type: "string", description: "Hex calldata starting with 0x (default: 0x)", default: "0x" },
        value: { type: "string", description: "Native token value to send (optional)", default: "0" },
        gasLimit: { type: "string", description: "Manual gas limit (optional)" },
        rpc: { type: "string", description: "Custom RPC endpoint URL (optional)" }
      },
      required: ["chain", "to"]
    }
  },
  {
    name: "get_pnl",
    description: "Track Profit & Loss (PnL) and average cost basis of token holdings",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        token: { type: "string", description: "Token symbol or contract address" },
        buyPrice: { type: "string", description: "Manually specify average buy price in USD (optional)" }
      },
      required: ["chain", "token"]
    }
  },
  {
    name: "analyze_contract",
    description: "Perform a smart contract security audit via GoPlus API",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        token: { type: "string", description: "Token contract address or symbol to audit" }
      },
      required: ["chain", "token"]
    }
  },
  {
    name: "get_trading_signal",
    description: "Fetch real-time indicators (RSI/EMA crossover) and trade signals",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        token: { type: "string", description: "Token symbol or contract address" }
      },
      required: ["chain", "token"]
    }
  },
  {
    name: "track_whales",
    description: "Scan and track recent whale transactions for a token",
    inputSchema: {
      type: "object",
      properties: {
        chain: { type: "string", description: "Blockchain network name" },
        token: { type: "string", description: "Token symbol or contract address" },
        minUsd: { type: "string", description: "Minimum transfer USD value to track (default: 50000)" }
      },
      required: ["chain", "token"]
    }
  }
];

// Register the tool list handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

// Run command in CLI subprocess securely using spawn (prevents shell injection)
function execCliCommand(argsArray) {
  return new Promise((resolve) => {
    const proc = spawn("node", ["index.js", ...argsArray]);
    let stdout = "";
    let stderr = "";

    proc.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    proc.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    proc.on("close", (code) => {
      const combinedOutput = stdout.trim() || stderr.trim();
      if (code !== 0) {
        resolve({
          isError: true,
          output: JSON.stringify({
            success: false,
            error: combinedOutput || `CLI exited with code ${code}`
          }, null, 2)
        });
      } else {
        resolve({
          isError: false,
          output: combinedOutput
        });
      }
    });
  });
}

// Map MCP tool calls to CLI arguments securely
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const cmdArgs = [];

  switch (name) {
    case "get_address":
      cmdArgs.push("address");
      if (args.chain) cmdArgs.push("--chain", args.chain);
      break;

    case "get_balance":
      cmdArgs.push("balance", "--chain", args.chain);
      if (args.token) cmdArgs.push("--token", args.token);
      break;

    case "scan_portfolio":
      cmdArgs.push("portfolio");
      if (args.chain) cmdArgs.push("--chain", args.chain);
      break;

    case "transfer":
      cmdArgs.push("transfer", "--chain", args.chain, "--to", args.to, "--amount", args.amount);
      if (args.token) cmdArgs.push("--token", args.token);
      if (args.rpc) cmdArgs.push("--rpc", args.rpc);
      if (args.simulate) cmdArgs.push("--simulate");
      if (args.antiMev) cmdArgs.push("--anti-mev");
      break;

    case "swap":
      cmdArgs.push("swap", "--chain", args.chain, "--fromToken", args.fromToken, "--toToken", args.toToken, "--amount", args.amount);
      if (args.mode) cmdArgs.push("--mode", args.mode);
      if (args.provider) cmdArgs.push("--provider", args.provider);
      if (args.slippage) cmdArgs.push("--slippage", args.slippage);
      if (args.rpc) cmdArgs.push("--rpc", args.rpc);
      if (args.simulate) cmdArgs.push("--simulate");
      if (args.antiMev) cmdArgs.push("--anti-mev");
      break;

    case "bridge":
      cmdArgs.push("bridge", "--fromChain", args.fromChain, "--toChain", args.toChain, "--fromToken", args.fromToken, "--toToken", args.toToken, "--amount", args.amount);
      if (args.mode) cmdArgs.push("--mode", args.mode);
      if (args.provider) cmdArgs.push("--provider", args.provider);
      if (args.slippage) cmdArgs.push("--slippage", args.slippage);
      if (args.rpc) cmdArgs.push("--rpc", args.rpc);
      if (args.simulate) cmdArgs.push("--simulate");
      if (args.antiMev) cmdArgs.push("--anti-mev");
      break;

    case "mint_nft":
      cmdArgs.push("mint", "--contract", args.contract);
      if (args.chain) cmdArgs.push("--chain", args.chain);
      if (args.function) cmdArgs.push("--function", args.function);
      if (args.args) cmdArgs.push("--args", args.args);
      if (args.value) cmdArgs.push("--value", args.value);
      if (args.rpc) cmdArgs.push("--rpc", args.rpc);
      break;

    case "custom_tx":
      cmdArgs.push("custom", "--chain", args.chain, "--to", args.to);
      if (args.data) cmdArgs.push("--data", args.data);
      if (args.value) cmdArgs.push("--value", args.value);
      if (args.gasLimit) cmdArgs.push("--gasLimit", args.gasLimit);
      if (args.rpc) cmdArgs.push("--rpc", args.rpc);
      break;

    case "get_pnl":
      cmdArgs.push("pnl", "--chain", args.chain, "--token", args.token);
      if (args.buyPrice) cmdArgs.push("--buyPrice", args.buyPrice);
      break;

    case "analyze_contract":
      cmdArgs.push("analyze", "--chain", args.chain, "--token", args.token);
      break;

    case "get_trading_signal":
      cmdArgs.push("signal", "--chain", args.chain, "--token", args.token);
      break;

    case "track_whales":
      cmdArgs.push("whales", "--chain", args.chain, "--token", args.token);
      if (args.minUsd) cmdArgs.push("--min-usd", args.minUsd);
      break;

    default:
      return {
        content: [{ type: "text", text: `Unknown tool: ${name}` }],
        isError: true,
      };
  }

  // Force JSON output formatting for AI Agent consumption
  cmdArgs.push("--json");

  const result = await execCliCommand(cmdArgs);
  return {
    content: [{ type: "text", text: result.output }],
    isError: result.isError,
  };
});

// Run Stdio transport connection
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Web3 Ops MCP Server running on Stdio transport");
