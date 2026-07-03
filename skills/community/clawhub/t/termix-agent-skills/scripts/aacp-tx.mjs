#!/usr/bin/env node
//
// Termix Platform (dev-v2) on-chain tx-intent executor.
//
// Backend "prepare" endpoints return unsigned tx-intents ({contract, callData,
// value, chainId, action}). This script signs them with WALLET_KEY and broadcasts
// to the chain — the only on-chain building block the skill needs. The backend
// already ABI-encodes callData, so no contract ABI is required here.
//
// Usage:
//   WALLET_KEY=0x.. node aacp-tx.mjs --intent  '<intent-json>'
//   WALLET_KEY=0x.. node aacp-tx.mjs --intents '<intent-json-array>'   # sequential (e.g. approve+deposit)
//   node aacp-tx.mjs --intent '<json>' --dry-run    # print what would be sent, do NOT broadcast
//
// Intent fields (either naming accepted):
//   to | contract     target address (0x..)
//   data | callData   encoded call (0x.., optional for plain transfers)
//   value             wei as decimal string (default "0")
//   chainId           optional; defaults to the RPC's chain id
//   action            optional label echoed in output
//
// Flags: --no-wait (skip receipt wait), --rpc <url> (override A2A_RPC_URL).
//
// Env: WALLET_KEY (required to broadcast), A2A_RPC_URL (optional RPC override).
//
import { addressFromPrivateKey, signTransaction } from "./vendor/eth-signer.mjs";
import { getChainId, getNonce, getFees, estimateGas, sendRawTransaction, waitReceipt, rpcUrl } from "./eth-rpc.mjs";

const args = process.argv.slice(2);
function arg(name) {
  const i = args.indexOf(`--${name}`);
  if (i < 0) return undefined;
  const v = args[i + 1];
  return v && !v.startsWith("--") ? v : true;
}

function requireWalletKey() {
  const key = process.env.WALLET_KEY?.trim();
  if (!key) throw new Error("WALLET_KEY env is required to sign and broadcast.");
  if (!/^0x[a-fA-F0-9]{64}$/.test(key)) throw new Error("WALLET_KEY must be a 0x-prefixed 32-byte hex private key.");
  return key;
}

function normalizeIntent(raw) {
  if (!raw || typeof raw !== "object") throw new Error("intent must be a JSON object");
  const to = raw.to ?? raw.contract;
  const data = raw.data ?? raw.callData ?? "0x";
  if (!to || !/^0x[a-fA-F0-9]{40}$/.test(to)) throw new Error(`intent.to/contract is not a valid address: ${to}`);
  return {
    action: raw.action ?? raw.id ?? "tx",
    to,
    data: data || "0x",
    value: String(raw.value ?? "0"),
    chainId: raw.chainId != null ? Number(raw.chainId) : undefined,
  };
}

function parseIntents() {
  const single = arg("intent");
  const multi = arg("intents");
  let list;
  if (typeof multi === "string") {
    const parsed = JSON.parse(multi);
    list = Array.isArray(parsed) ? parsed : [parsed];
  } else if (typeof single === "string") {
    const parsed = JSON.parse(single);
    list = Array.isArray(parsed) ? parsed : [parsed];
  } else {
    throw new Error("Provide --intent '<json>' or --intents '<json[]>'");
  }
  return list.map(normalizeIntent);
}

async function main() {
  if (args.includes("--help") || args.includes("-h")) {
    process.stderr.write("Usage: WALLET_KEY=0x.. node aacp-tx.mjs --intent '<json>' [--intents '<json[]>'] [--dry-run] [--no-wait]\n");
    return;
  }
  const intents = parseIntents();
  const dryRun = args.includes("--dry-run");
  const noWait = args.includes("--no-wait");

  // Summary (always printed first so the operator/LLM can confirm before broadcast).
  const summary = intents.map((it) => ({ action: it.action, to: it.to, value: it.value, dataLen: (it.data.length - 2) / 2 }));
  process.stderr.write(`[aacp-tx] rpc=${rpcUrl()} intents=${intents.length}\n`);
  process.stderr.write(`[aacp-tx] plan=${JSON.stringify(summary)}\n`);

  if (dryRun) {
    console.log(JSON.stringify({ dryRun: true, rpc: rpcUrl(), intents: summary }, null, 2));
    return;
  }

  const pk = requireWalletKey();
  const from = addressFromPrivateKey(pk);
  const rpcChainId = await getChainId();
  let nonce = await getNonce(from);
  const results = [];

  for (const it of intents) {
    const chainId = it.chainId ?? rpcChainId;
    if (it.chainId && it.chainId !== rpcChainId) {
      throw new Error(`intent.chainId ${it.chainId} != RPC chainId ${rpcChainId} — set A2A_RPC_URL to the right network`);
    }
    const fees = await getFees();
    const gas = await estimateGas({ from, to: it.to, value: it.value, data: it.data });
    const signed = signTransaction(pk, {
      chainId,
      nonce,
      maxPriorityFeePerGas: fees.maxPriorityFeePerGas,
      maxFeePerGas: fees.maxFeePerGas,
      gas,
      to: it.to,
      value: it.value,
      data: it.data,
    });
    const txHash = await sendRawTransaction(signed.raw);
    process.stderr.write(`[aacp-tx] sent ${it.action} nonce=${nonce} tx=${txHash}\n`);
    let status = "submitted";
    let blockNumber = null;
    if (!noWait) {
      const receipt = await waitReceipt(txHash);
      status = receipt.status === "0x1" ? "success" : "reverted";
      blockNumber = receipt.blockNumber ? Number(BigInt(receipt.blockNumber)) : null;
      if (status === "reverted") {
        results.push({ action: it.action, txHash, status, blockNumber });
        console.log(JSON.stringify({ from, results }, null, 2));
        throw new Error(`tx ${txHash} (${it.action}) reverted on-chain`);
      }
    }
    results.push({ action: it.action, txHash, status, blockNumber, nonce: Number(nonce) });
    nonce += 1n;
  }

  console.log(JSON.stringify({ from, chainId: rpcChainId, results }, null, 2));
}

main().catch((err) => {
  process.stderr.write(`error: ${err.message}\n`);
  process.exit(1);
});
