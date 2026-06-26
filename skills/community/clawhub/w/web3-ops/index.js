#!/usr/bin/env node

import "dotenv/config";
import { Command } from "commander";
import { getAddress, getBalance, getPortfolio, createNewWallet } from "./actions/wallet.js";
import { transfer } from "./actions/transfer.js";
import { swapOrBridge } from "./actions/swapBridge.js";
import { mintNft } from "./actions/mintNft.js";
import { executeCustomTx } from "./actions/customTx.js";

// Import new advanced trading & security modules
import { calculatePnL } from "./actions/pnl.js";
import { analyzeTokenSecurity } from "./actions/auditor.js";
import { getTradingSignal } from "./actions/signals.js";
import { trackWhales } from "./actions/whales.js";
import { runPriceMonitor } from "./actions/monitor.js";

const program = new Command();

program
  .name("web3-ops")
  .description("CLI Utility for EVM Web3 operations as an OpenClaw Agent Skill")
  .version("1.0.0")
  // Global Options
  .option("--json", "Output strictly in JSON format (silences informational logs)", false)
  .option("--rpc <rpcUrl>", "Override default RPC URL with a custom node URL")
  .option("--simulate", "Simulate the transaction (dry run) without broadcasting it", false)
  .option("--anti-mev", "Route transaction through private RPCs to prevent MEV searcher sandwich attacks", false);

// Helper to merge command options with global options
const getMergedOpts = (cmdOpts) => {
  return { ...cmdOpts, ...program.opts() };
};

// 1. Get Wallet Address
program
  .command("address")
  .description("Get your configured EVM wallet address")
  .option("-c, --chain <chain>", "Blockchain network (e.g. ethereum, arbitrum, base, etc.)", "ethereum")
  .action((options) => {
    getAddress(getMergedOpts(options));
  });

// 2. Get Balance
program
  .command("balance")
  .description("Check native coin or ERC-20 token balance")
  .requiredOption("-c, --chain <chain>", "Blockchain network (e.g. arbitrum, base, polygon, etc.)")
  .option("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address (omit for native balance)")
  .action((options) => {
    getBalance(getMergedOpts(options));
  });

// 3. Scan Portfolio (New)
program
  .command("portfolio")
  .description("Scan and list all active token balances (>0) in your wallet")
  .option("-c, --chain <chain>", "Blockchain network (e.g. base, arbitrum, polygon, etc. or 'all')", "all")
  .action((options) => {
    getPortfolio(getMergedOpts(options));
  });

// 4. Transfer Coin/Token
program
  .command("transfer")
  .description("Send native coin or ERC-20 token to another wallet address")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-to, --to <address>", "Recipient wallet address")
  .requiredOption("-a, --amount <amount>", "Amount of tokens to send (e.g. 0.05)")
  .option("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address (omit for native coin)")
  .action((options) => {
    transfer(getMergedOpts(options));
  });

// 5. Swap Token (Same-chain)
program
  .command("swap")
  .description("Swap tokens on the same blockchain network (e.g. ETH to USDC)")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-f, --fromToken <symbolOrAddress>", "Source token symbol or contract address")
  .requiredOption("-t, --toToken <symbolOrAddress>", "Destination token symbol or contract address")
  .requiredOption("-a, --amount <amount>", "Amount of source tokens to swap")
  .option("-m, --mode <mode>", "Routing mode: 'auto' (aggregator) or 'manual'", "auto")
  .option("-p, --provider <provider>", "Manual swap provider: 'lifi', 'relay', 'uniswap', 'pancakeswap'", "lifi")
  .option("-s, --slippage <percent>", "Slippage tolerance in percent (e.g. 0.5)", "0.5")
  .action((options) => {
    swapOrBridge(getMergedOpts(options));
  });

// 6. Bridge Token (Cross-chain)
program
  .command("bridge")
  .description("Bridge and swap tokens across different blockchains (e.g. ETH on Arbitrum to USDC on Base)")
  .requiredOption("-fc, --fromChain <chain>", "Source blockchain network")
  .requiredOption("-tc, --toChain <chain>", "Destination blockchain network")
  .requiredOption("-f, --fromToken <symbolOrAddress>", "Source token symbol or contract address")
  .requiredOption("-t, --toToken <symbolOrAddress>", "Destination token symbol or contract address")
  .requiredOption("-a, --amount <amount>", "Amount of source tokens to bridge")
  .option("-m, --mode <mode>", "Routing mode: 'auto' or 'manual'", "auto")
  .option("-p, --provider <provider>", "Manual bridge provider: 'lifi', 'relay'", "lifi")
  .option("-s, --slippage <percent>", "Slippage tolerance in percent (e.g. 0.5)", "0.5")
  .action((options) => {
    swapOrBridge(getMergedOpts(options));
  });

// 7. Mint NFT
program
  .command("mint")
  .description("Mint/claim an NFT on an EVM network or via marketplace URL")
  .option("-c, --chain <chain>", "Blockchain network (optional if contract is a marketplace URL)")
  .requiredOption("-ct, --contract <contractAddress>", "NFT contract address or marketplace URL (OpenSea, Zora, Rarible)")
  .option("-f, --function <functionSig>", "Mint function signature")
  .option("-args, --args <jsonArray>", "Function arguments as a JSON array (e.g. '[1]')")
  .option("-v, --value <value>", "Native token value to send (for paid mints, in ETH/MATIC)", "0")
  .action((options) => {
    mintNft(getMergedOpts(options));
  });

// 8. Custom Transaction (Raw Tx)
program
  .command("custom")
  .description("Broadcast a custom transaction with raw hex calldata")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-to, --to <address>", "Target contract or wallet address")
  .option("-d, --data <hex>", "Hex calldata starting with 0x", "0x")
  .option("-v, --value <value>", "Native token value to send (in normal units, e.g. 0.001)", "0")
  .option("-g, --gasLimit <gas>", "Manual gas limit (optional)")
  .action((options) => {
    executeCustomTx(getMergedOpts(options));
  });

// 9. Profit & Loss Tracker (PnL)
program
  .command("pnl")
  .description("Track PnL (profit and loss) for a specific token")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address")
  .option("-b, --buyPrice <price>", "Manually specify average buy price in USD (optional)")
  .action((options) => {
    calculatePnL(getMergedOpts(options));
  });

// 10. Cutloss & Takeprofit Monitor
program
  .command("monitor")
  .description("Monitor token price and execute auto-swap on cutloss or takeprofit")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address")
  .requiredOption("-a, --amount <amount>", "Amount of tokens to sell on trigger")
  .option("--cutloss <value>", "Cutloss trigger (e.g. -10% or USD nominal price e.g. 0.85)")
  .option("--takeprofit <value>", "Takeprofit trigger (e.g. +20% or USD nominal price e.g. 1.50)")
  .option("--max-checks <count>", "Maximum number of price checks (polling loop limits)", "60")
  .option("--interval <seconds>", "Polling interval in seconds", "20")
  .option("--alert", "Send structured alert output if target is reached", false)
  .action((options) => {
    runPriceMonitor(getMergedOpts(options));
  });

// 11. Trading Signals
program
  .command("signal")
  .description("Get technical indicators (RSI/EMA) and trading recommendations for a token")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address")
  .option("--alert", "Flag alert to AI agent if signal is extreme (Strong Buy/Strong Sell)", false)
  .action((options) => {
    getTradingSignal(getMergedOpts(options));
  });

// 12. Smart Contract Auditor
program
  .command("analyze")
  .description("Run a security audit on a smart contract using GoPlus Security API")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address")
  .action((options) => {
    analyzeTokenSecurity(getMergedOpts(options));
  });

// 13. Whale Tracker
program
  .command("whales")
  .description("Scan blockchain explorer for large transactions of a token")
  .requiredOption("-c, --chain <chain>", "Blockchain network")
  .requiredOption("-t, --token <symbolOrAddress>", "ERC-20 token symbol or contract address")
  .option("--min-usd <value>", "Minimum USD value of transaction to count as whale", "50000")
  .option("--alert", "Alert AI agent if recent whale movement occurs", false)
  .action((options) => {
    trackWhales(getMergedOpts(options));
  });

// 14. Create EVM Wallet
program
  .command("create-wallet")
  .description("Generate a random EVM wallet and configure its credentials in the .env file")
  .option("--force", "Force overwrite of existing PRIVATE_KEY or MNEMONIC in .env", false)
  .action((options) => {
    createNewWallet(getMergedOpts(options));
  });

program.parse(process.argv);

