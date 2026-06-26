import { Connection, PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js"
import { SOLANA_RPC_URL } from "./environment.ts"
import { loadKeypair, getPublicKey } from "./wallet.ts"
import type { BalanceResult, TokenBalance } from "./types.ts"

const getConnection = (rpcUrl = SOLANA_RPC_URL) => new Connection(rpcUrl, "confirmed")

export const getSolBalance = async (
  publicKey: string,
  rpcUrl?: string
): Promise<{ lamports: number; sol: number }> => {
  const connection = getConnection(rpcUrl)
  const lamports = await connection.getBalance(new PublicKey(publicKey))
  return { lamports, sol: lamports / LAMPORTS_PER_SOL }
}

export const getTokenBalances = async (
  publicKey: string,
  rpcUrl?: string
): Promise<TokenBalance[]> => {
  const connection = getConnection(rpcUrl)

  const accounts = await connection.getParsedTokenAccountsByOwner(
    new PublicKey(publicKey),
    { programId: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA") }
  )

  return accounts.value
    .map(acc => {
      const info = acc.account.data.parsed.info
      const ta = info.tokenAmount
      return {
        mint: info.mint as string,
        symbol: "UNKNOWN", // Jupiter token list lookup can enrich this later
        decimals: ta.decimals as number,
        amount: BigInt(ta.amount as string),
        uiAmount: (ta.uiAmount as number) ?? 0,
      } satisfies TokenBalance
    })
    .filter(t => t.uiAmount > 0)
}

export const getPortfolioSummary = async (
  walletName: string,
  rpcUrl?: string
): Promise<BalanceResult> => {
  const publicKey = await getPublicKey(walletName)
  const { lamports, sol } = await getSolBalance(publicKey, rpcUrl)
  const tokens = await getTokenBalances(publicKey, rpcUrl)

  return { walletName, publicKey, solBalance: sol, lamports, tokens }
}
