"use strict";
// Shared: sign the EIP-712 AgentInbox struct with the CDP wallet.
// action "pull"  → bodyHash = 0x00…00
// action "reply" → bodyHash = keccak256(text)   (so the text can't be altered in flight)
const crypto = require("crypto");
const { loadConfig, cdpClient } = require("./wallet-config");

const CHAIN_ID = 8453; // Base mainnet
const VERIFYING_CONTRACT = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";
const MCP = process.env.RSOFT_MCP_URL || "https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws";

async function keccak256(text) {
  // viem ships with cdp-sdk; keccak of the UTF-8 bytes, same as the bank (Web3.keccak(text=...)).
  const { keccak256: k, toBytes } = await import("viem");
  return k(toBytes(text));
}

async function signInbox(action, text) {
  const cfg = loadConfig();
  const cdp = await cdpClient(cfg);
  const account = await cdp.evm.getAccount({ address: cfg.AGENT_WALLET });
  const bodyHash = action === "reply" ? await keccak256(text) : "0x" + "00".repeat(32);
  const nonce = `inbox:${action}:${crypto.randomBytes(8).toString("hex")}`;
  const deadline = Math.floor(Date.now() / 1000) + 900; // 15 min
  const signature = await account.signTypedData({
    domain: { name: "RSoft Agentic Bank", version: "1", chainId: CHAIN_ID, verifyingContract: VERIFYING_CONTRACT },
    types: {
      AgentInbox: [
        { name: "agentWallet", type: "address" },
        { name: "action", type: "string" },
        { name: "bodyHash", type: "bytes32" },
        { name: "nonce", type: "string" },
        { name: "deadline", type: "uint256" },
      ],
    },
    primaryType: "AgentInbox",
    message: { agentWallet: account.address, action, bodyHash, nonce, deadline: BigInt(deadline) },
  });
  return { agent_wallet: account.address, signature, nonce, deadline };
}

module.exports = { signInbox, MCP };
