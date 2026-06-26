import {
  Connection,
  PublicKey,
  SystemProgram,
  Transaction,
  sendAndConfirmTransaction,
  LAMPORTS_PER_SOL,
} from "@solana/web3.js"
import {
  getOrCreateAssociatedTokenAccount,
  createTransferInstruction,
  getMint,
} from "@solana/spl-token"
import { SOLANA_RPC_URL, explorerTx } from "./environment.ts"
import { loadKeypair } from "./wallet.ts"
import type { TransferResult } from "./types.ts"

const getConnection = (rpcUrl = SOLANA_RPC_URL) => new Connection(rpcUrl, "confirmed")

export const transferSOL = async (
  fromWalletName: string,
  toAddress: string,
  amountSol: number,
  rpcUrl?: string
): Promise<TransferResult> => {
  const rpc = rpcUrl ?? SOLANA_RPC_URL
  const connection = getConnection(rpc)
  const keypair = await loadKeypair(fromWalletName)
  const toPubkey = new PublicKey(toAddress)

  const tx = new Transaction().add(
    SystemProgram.transfer({
      fromPubkey: keypair.publicKey,
      toPubkey,
      lamports: Math.floor(amountSol * LAMPORTS_PER_SOL),
    })
  )

  const signature = await sendAndConfirmTransaction(connection, tx, [keypair])

  return {
    signature,
    explorerUrl: explorerTx(signature, rpc),
    from: keypair.publicKey.toBase58(),
    to: toAddress,
    amount: amountSol,
  }
}

export const transferSPL = async (
  fromWalletName: string,
  toAddress: string,
  mintAddress: string,
  amount: number,
  rpcUrl?: string
): Promise<TransferResult> => {
  const rpc = rpcUrl ?? SOLANA_RPC_URL
  const connection = getConnection(rpc)
  const keypair = await loadKeypair(fromWalletName)
  const mintPubkey = new PublicKey(mintAddress)
  const toPubkey = new PublicKey(toAddress)

  const mintInfo = await getMint(connection, mintPubkey)
  const adjustedAmount = BigInt(Math.floor(amount * 10 ** mintInfo.decimals))

  const fromATA = await getOrCreateAssociatedTokenAccount(
    connection, keypair, mintPubkey, keypair.publicKey
  )
  const toATA = await getOrCreateAssociatedTokenAccount(
    connection, keypair, mintPubkey, toPubkey
  )

  const tx = new Transaction().add(
    createTransferInstruction(fromATA.address, toATA.address, keypair.publicKey, adjustedAmount)
  )

  const signature = await sendAndConfirmTransaction(connection, tx, [keypair])

  return {
    signature,
    explorerUrl: explorerTx(signature, rpc),
    from: keypair.publicKey.toBase58(),
    to: toAddress,
    amount,
    mint: mintAddress,
  }
}
