// Minimal JSON-RPC client over fetch for broadcasting signed transactions.
// No viem/ethers — just the handful of methods aacp-tx.mjs needs.
// RPC URL: A2A_RPC_URL env, else a public BSC mainnet node. Only uses
// send/receipt/nonce/gas/fee methods (no log filters), so public nodes are fine.

const DEFAULT_RPC = "https://bsc-rpc.publicnode.com";

export function rpcUrl() {
  return (process.env.A2A_RPC_URL || DEFAULT_RPC).replace(/\/$/, "");
}

let idCounter = 0;
export async function rpc(method, params = []) {
  const res = await fetch(rpcUrl(), {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: ++idCounter, method, params }),
  });
  const text = await res.text();
  let json;
  try { json = JSON.parse(text); } catch { throw new Error(`RPC ${method}: non-JSON response ${text.slice(0, 200)}`); }
  if (json.error) throw new Error(`RPC ${method} error ${json.error.code}: ${json.error.message}`);
  return json.result;
}

export const toHex = (v) => "0x" + BigInt(v).toString(16);
export const fromHex = (h) => BigInt(h);

export async function getChainId() {
  return Number(fromHex(await rpc("eth_chainId")));
}

export async function getNonce(address) {
  return fromHex(await rpc("eth_getTransactionCount", [address, "pending"]));
}

// EIP-1559 fees floored to the network's eth_gasPrice so BSC (often near-zero
// base fee but a non-zero min gas price) does not underprice and stall the tx.
// maxFee = max(baseFee*2 + gasPrice, gasPrice); tip = min(gasPrice, maxFee).
export async function getFees() {
  const gp = fromHex(await rpc("eth_gasPrice"));
  let baseFee = 0n;
  try {
    const block = await rpc("eth_getBlockByNumber", ["latest", false]);
    if (block && block.baseFeePerGas) baseFee = fromHex(block.baseFeePerGas);
  } catch { /* chains without 1559 block field */ }
  let maxFee = baseFee * 2n + gp;
  if (maxFee < gp) maxFee = gp;
  let tip = gp;
  if (tip > maxFee) tip = maxFee;
  return { maxPriorityFeePerGas: tip, maxFeePerGas: maxFee };
}

export async function estimateGas({ from, to, value, data }) {
  const tx = { from, to, value: toHex(value ?? 0) };
  if (data && data !== "0x") tx.data = data;
  const est = fromHex(await rpc("eth_estimateGas", [tx]));
  return (est * 12n) / 10n; // +20% buffer
}

export async function sendRawTransaction(rawHex) {
  return rpc("eth_sendRawTransaction", [rawHex]);
}

export async function waitReceipt(txHash, { timeoutMs = 120000, intervalMs = 3000 } = {}) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const r = await rpc("eth_getTransactionReceipt", [txHash]).catch(() => null);
    if (r) return r;
    await new Promise((res) => setTimeout(res, intervalMs));
  }
  throw new Error(`receipt timeout for ${txHash} after ${timeoutMs}ms`);
}
