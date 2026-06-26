import { Connection, VersionedTransaction, LAMPORTS_PER_SOL, PublicKey } from "@solana/web3.js"
import { getMint, getAssociatedTokenAddressSync } from "@solana/spl-token"
import { explorerTx } from "./environment.ts"
import { loadKeypair } from "./wallet.ts"
import type { SwapResult } from "./types.ts"

const RAYDIUM_SWAP_HOST = "https://transaction-v1.raydium.io"

export const SOL_MINT         = "So11111111111111111111111111111111111111112"
export const USDC_MINT        = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  // mainnet USDC
export const USDC_DEVNET_MINT = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"

export const solToLamports = (sol: number): number => Math.floor(sol * LAMPORTS_PER_SOL)

interface RaydiumSwapCompute {
  success: boolean
  data?: {
    inputMint: string
    inputAmount: string
    outputMint: string
    outputAmount: string
    slippageBps: number
    priceImpactPct: number
    routePlan: Array<{ poolId: string; inputMint: string; outputMint: string }>
  }
}

export const raydiumQuote = async (
  inputMint: string,
  outputMint: string,
  amountLamports: number,
  slippageBps = 300
): Promise<RaydiumSwapCompute> => {
  const url =
    `${RAYDIUM_SWAP_HOST}/compute/swap-base-in` +
    `?inputMint=${inputMint}` +
    `&outputMint=${outputMint}` +
    `&amount=${amountLamports}` +
    `&slippageBps=${slippageBps}` +
    `&txVersion=V0`

  const res = await fetch(url)
  if (!res.ok) throw new Error(`Raydium quote failed (${res.status}): ${await res.text()}`)
  return res.json() as Promise<RaydiumSwapCompute>
}

async function rpcPost<T>(rpcUrl: string, method: string, params: unknown[]): Promise<T> {
  const res = await fetch(rpcUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: Date.now(), method, params }),
  })
  const data = await res.json() as { result?: T; error?: { message: string; code?: number } }
  if (data.error) throw new Error(`RPC ${method} error: ${data.error.message}`)
  return data.result as T
}

async function simulateTx(rpcUrl: string, txBase64: string): Promise<void> {
  const result = await rpcPost<{ value: { err: unknown; logs?: string[] } }>(
    rpcUrl,
    "simulateTransaction",
    [txBase64, { encoding: "base64", commitment: "confirmed" }],
  )
  if (result.value.err) {
    const logs = result.value.logs?.slice(-5).join("\n") ?? ""
    throw new Error(`Simulation failed: ${JSON.stringify(result.value.err)}\n${logs}`)
  }
  console.log(`[RPC] Simulation OK`)
}

async function sendRawTx(rpcUrl: string, txBase64: string): Promise<string> {
  const sig = await rpcPost<string>(
    rpcUrl,
    "sendTransaction",
    [txBase64, { encoding: "base64", skipPreflight: true }],
  )
  if (!sig) throw new Error(`sendTransaction returned no signature`)
  return sig
}

// Solana transactions are regularly dropped — resend every 2s until confirmed or blockhash expires (~60s).
async function confirmTx(rpcUrl: string, signature: string, signedTxBase64: string, timeout = 60000): Promise<void> {
  const startTime = Date.now()
  let lastResend = 0
  let polls = 0

  while (Date.now() - startTime < timeout) {
    // Resend every 2s so the tx stays in validators' queues
    if (Date.now() - lastResend >= 2000) {
      sendRawTx(rpcUrl, signedTxBase64).catch(() => {}) // fire-and-forget
      lastResend = Date.now()
    }

    try {
      type StatusResult = Array<{ confirmationStatus?: string; err?: unknown } | null>
      const value = await rpcPost<{ value: StatusResult }>(
        rpcUrl,
        "getSignatureStatuses",
        [[signature]],
      )
      const entry = value.value[0]

      if (entry?.err) throw new Error(`Transaction failed on-chain: ${JSON.stringify(entry.err)}`)

      const status = entry?.confirmationStatus
      if (status === "confirmed" || status === "finalized") {
        console.log(`[RPC] ✅ Confirmed (${Math.round((Date.now() - startTime) / 1000)}s)`)
        return
      }

      polls++
      if (polls % 5 === 0) console.log(`[RPC] Waiting... ${Math.round((Date.now() - startTime) / 1000)}s (status: ${status ?? "unknown"})`)
    } catch (e) {
      if (e instanceof Error && e.message.startsWith("Transaction failed")) throw e
    }

    await new Promise(r => setTimeout(r, 1000))
  }

  throw new Error(`Transaction not confirmed within ${timeout / 1000}s — blockhash likely expired`)
}

export const raydiumSwap = async (
  walletName: string,
  inputMint: string,
  outputMint: string,
  amountLamports: number,
  slippageBps = 300,
  rpcUrl?: string,
  maxHops = Infinity,
): Promise<SwapResult> => {
  // Raydium routes sub-$1 swaps through illiquid intermediate tokens, producing ~40% worse rates.
  // 1_000_000 lamports ≈ 0.001 SOL; for token inputs 1_000_000 units = $1 USDC.
  // Enforce a floor of 1_000_000 base units (~$1) before even fetching a quote.
  if (amountLamports < 1_000_000) {
    throw new Error(
      `Trade amount ${amountLamports} is below the 1,000,000 base-unit minimum. ` +
      `Raydium routes micro-trades through illiquid intermediate pools — refusing to execute.`
    )
  }

  const rpc = rpcUrl || process.env.SOLANA_RPC_URL || "https://api.devnet.solana.com"
  const connection = new Connection(rpc, "confirmed")
  const keypair = await loadKeypair(walletName)

  console.log(`[RAYDIUM] Getting quote...`)
  const quoteResponse = await raydiumQuote(inputMint, outputMint, amountLamports, slippageBps)
  if (!quoteResponse.success) {
    throw new Error(`Raydium quote failed: ${JSON.stringify(quoteResponse)}`)
  }

  const route = quoteResponse.data!.routePlan
  const routeStr = route.map(h => `${h.inputMint.slice(0,4)}..→${h.outputMint.slice(0,4)}.. [${h.poolId.slice(0,8)}]`).join(" | ")
  console.log(`[RAYDIUM] Route (${route.length} hop${route.length !== 1 ? "s" : ""}): ${routeStr}`)
  console.log(`[RAYDIUM] Output: ${quoteResponse.data?.outputAmount}`)

  if (route.length > maxHops) {
    throw new Error(
      `Raydium routed through ${route.length} hops (max ${maxHops}). ` +
      `Refusing to execute — likely routing through illiquid intermediate tokens. ` +
      `Route: ${routeStr}`
    )
  }

  let computeUnitPrice = "1000000"
  try {
    const feeRes = await fetch(`${RAYDIUM_SWAP_HOST}/priority-fee`)
    if (feeRes.ok) {
      const feeData = await feeRes.json() as { data: { default: { h: number } } }
      computeUnitPrice = String(feeData.data.default.h)
    }
  } catch (e) {}

  // For token inputs (non-SOL), Raydium requires the ATA address explicitly.
  // Without it, their server-side account derivation fails with REQ_INPUT_ACCOUT_ERROR.
  const inputAccount = inputMint !== SOL_MINT
    ? getAssociatedTokenAddressSync(new PublicKey(inputMint), keypair.publicKey).toBase58()
    : undefined

  console.log(`[RAYDIUM] Building transaction...`)
  const swapRes = await fetch(`${RAYDIUM_SWAP_HOST}/transaction/swap-base-in`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      computeUnitPriceMicroLamports: computeUnitPrice,
      swapResponse: quoteResponse,
      txVersion: "V0",
      wallet: keypair.publicKey.toBase58(),
      wrapSol: inputMint === SOL_MINT,
      unwrapSol: outputMint === SOL_MINT,
      ...(inputAccount ? { inputAccount } : {}),
    }),
  })

  if (!swapRes.ok) throw new Error(`Raydium tx build failed (${swapRes.status}): ${await swapRes.text()}`)
  const swapData = await swapRes.json() as { success?: boolean; msg?: string; data?: Array<{ transaction: string }> }

  if (!swapData.success) throw new Error(`Raydium tx build failed: ${swapData.msg ?? "unknown error"}`)
  if (!swapData.data?.length) throw new Error(`Raydium tx build returned no transactions`)

  const txBuf = Buffer.from(swapData.data[0].transaction, "base64")
  const transaction = VersionedTransaction.deserialize(txBuf)
  transaction.sign([keypair])
  const signedBase64 = Buffer.from(transaction.serialize()).toString("base64")

  await simulateTx(rpc, signedBase64)

  const signature = await sendRawTx(rpc, signedBase64)
  console.log(`[RPC] TX: ${signature}`)

  await confirmTx(rpc, signature, signedBase64)

  const mintInfo = await getMint(connection, new PublicKey(outputMint))
  const outputAmount = parseInt(quoteResponse.data?.outputAmount || "0") / 10 ** mintInfo.decimals
  const inputAmountSol = amountLamports / LAMPORTS_PER_SOL

  return {
    signature,
    explorerUrl: explorerTx(signature, rpc),
    inputMint,
    outputMint,
    inputAmountSol,
    outputAmount,
  }
}
