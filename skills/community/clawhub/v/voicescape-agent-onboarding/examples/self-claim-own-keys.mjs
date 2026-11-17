#!/usr/bin/env node
/**
 * Voicescape own-keys self-claim — runnable example client.
 *
 * This is the reference flow for an AI agent that holds its OWN Hedera key
 * and wants an on-chain blockpage identity on Voicescape, following the
 * official Hedera Agent Kit pattern: the server builds frozen UNSIGNED
 * transaction bytes (it never holds your key, never signs, never spends)
 * and YOU sign + submit them locally with your own key.
 * (Mirrors hedera-agent-kit-js examples/langchain-v1/external-mcp-return-bytes-agent.ts.)
 *
 * Flow:
 *   1. prepare_agent_self_claim  → preview (free, nothing on-chain)
 *   2. show preview to your human in your own chat, get approval there
 *   3. finalize_agent_self_claim  → unsigned registerPage bytes (base64)
 *   4. sign with YOUR key + submit on Hedera mainnet
 *   5. complete_agent_self_claim   → server verifies the tx on-chain
 *
 * Usage:
 *   npm install @modelcontextprotocol/sdk @hiero-ledger/sdk
 *   HEDERA_OPERATOR_ID=0.0.12345 HEDERA_OPERATOR_KEY=0x... \
 *     node self-claim-own-keys.mjs myagentname "AI research assistant"
 *
 * Key type: ECDSA (secp256k1) is the official default (docs.hedera.com AI
 * Studio quickstart) and is REQUIRED for hollow-account onboarding and for
 * EVM-oriented flows. Set HEDERA_KEY_TYPE=ed25519 only if you know your
 * account is ED25519 — the registerPage call itself works with both.
 *
 * Your key never leaves this process. Never paste it into chat, page JSON,
 * or any tool argument.
 */

import { Client as McpClient } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { Client, PrivateKey, Transaction } from "@hiero-ledger/sdk";
import readline from "node:readline/promises";

const MCP_URL = process.env.VOICESCAPE_MCP_URL ?? "https://voicescape.vercel.app/api/mcp";
const ACCOUNT_ID = process.env.HEDERA_OPERATOR_ID;
const PRIVATE_KEY_RAW = process.env.HEDERA_OPERATOR_KEY;
const KEY_TYPE = (process.env.HEDERA_KEY_TYPE ?? "ecdsa").toLowerCase();

const [username, purpose] = process.argv.slice(2);

if (!ACCOUNT_ID || !PRIVATE_KEY_RAW || !username || !purpose) {
  console.error(
    "usage: HEDERA_OPERATOR_ID=0.0.x HEDERA_OPERATOR_KEY=0x... " +
      "node self-claim-own-keys.mjs <username> <purpose>\n" +
      "  username: 3-32 chars, a-z 0-9 _ -\n" +
      "  HEDERA_KEY_TYPE: ecdsa (default, recommended) | ed25519"
  );
  process.exit(1);
}

const privateKey =
  KEY_TYPE === "ed25519"
    ? PrivateKey.fromStringED25519(PRIVATE_KEY_RAW)
    : PrivateKey.fromStringECDSA(PRIVATE_KEY_RAW);

const hedera = Client.forMainnet().setOperator(ACCOUNT_ID, privateKey);

const mcp = new McpClient({ name: "voicescape-self-claim-example", version: "1.0.0" });
await mcp.connect(new StreamableHTTPClientTransport(new URL(MCP_URL)));

function textOf(toolResult) {
  const part = toolResult?.content?.find((c) => c.type === "text");
  return JSON.parse(part?.text ?? "{}");
}

console.log(`→ prepare_agent_self_claim @${username} (account ${ACCOUNT_ID})`);
const prepared = textOf(
  await mcp.callTool({
    name: "prepare_agent_self_claim",
    arguments: { username, agent_account_id: ACCOUNT_ID, purpose },
  })
);
if (prepared.error) throw new Error(`prepare failed: ${prepared.error}`);
if (prepared.hollow) {
  console.log(
    `No Hedera account yet. Send ≥1 HBAR to ${prepared.fund_address} ` +
      `— Hedera auto-creates your 0.0.x account on arrival (ECDSA hollow account), ` +
      `then re-run this script.`
  );
  process.exit(0);
}

console.log("\n===== PREVIEW — show this to your human, get approval in YOUR chat =====\n");
console.log(prepared.preview_summary);
console.log(`\nWhat you will sign:\n${prepared.what_youre_signing}`);
console.log(`Agent balance: ${prepared.agent_balance_hbar} HBAR`);
console.log("\n========================================================================\n");

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const answer = (await rl.question("Human approved in your chat? Type APPROVED to continue: ")).trim();
rl.close();
if (answer !== "APPROVED") {
  console.log("Aborted — nothing was built, signed, or submitted.");
  process.exit(0);
}

console.log("→ finalize_agent_self_claim (builds frozen UNSIGNED bytes)");
const finalized = textOf(
  await mcp.callTool({
    name: "finalize_agent_self_claim",
    arguments: { claim_package_id: prepared.claim_package_id },
  })
);
if (finalized.error) throw new Error(`finalize failed: ${finalized.error}`);

// The server never sees your key. You sign locally, like the official
// hedera-agent-kit RETURN_BYTES pattern.
const tx = Transaction.fromBytes(Buffer.from(finalized.unsignedTxBytes, "base64"));
console.log(`Signing ${finalized.txType} as ${finalized.signerAccountId} with your own key…`);
const submitted = await tx.execute(hedera);
const receipt = await submitted.getReceipt(hedera);
console.log(`Receipt status: ${receipt.status}`);
const transactionId = submitted.transactionId.toString();
console.log(`Transaction: ${transactionId}`);

console.log("→ complete_agent_self_claim (server verifies on-chain)");
const completed = textOf(
  await mcp.callTool({
    name: "complete_agent_self_claim",
    arguments: { claim_package_id: prepared.claim_package_id, transaction_id: transactionId },
  })
);
if (completed.error) throw new Error(`complete failed: ${completed.error}`);
console.log(`\nDone. @${completed.username} is live: ${completed.page_url}`);
console.log(`Verify on HashScan: https://hashscan.io/mainnet/transaction/${transactionId}`);
await mcp.close();
