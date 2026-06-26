import { Keypair } from "@solana/web3.js"
import bs58 from "bs58"
const { encode: bs58Encode, decode: bs58Decode } = bs58
import { encryptWithPassword, decryptWithPassword, getMasterKey } from "./crypto.ts"
import { saveWallet, getWallet, listWallets as listFromStore } from "./db.ts"
import type { WalletInfo, EncryptedWalletRecord, Network } from "./types.ts"

export const createWallet = async (
  name: string,
  network: Network = "devnet",
  tags: string[] = []
): Promise<WalletInfo> => {
  const existing = await getWallet(name)
  if (existing) throw new Error(`Wallet "${name}" already exists`)

  const keypair = Keypair.generate()
  const privateKeyBs58 = bs58Encode(keypair.secretKey)

  const masterKey = await getMasterKey()
  const { encrypted, salt } = await encryptWithPassword(privateKeyBs58, masterKey)

  const record: EncryptedWalletRecord = {
    name,
    publicKey: keypair.publicKey.toBase58(),
    encryptedPrivateKey: encrypted,
    salt,
    createdAt: new Date().toISOString(),
    network,
    tags,
  }

  await saveWallet(record)

  return {
    name: record.name,
    publicKey: record.publicKey,
    network: record.network,
    createdAt: record.createdAt,
    tags: record.tags,
  }
}

// Load and decrypt a keypair into memory for signing
// Private key is never written back or logged
export const loadKeypair = async (name: string): Promise<Keypair> => {
  const record = await getWallet(name)
  if (!record) throw new Error(`Wallet "${name}" not found. Run: solana-wallet wallet list`)

  const masterKey = await getMasterKey()
  const privateKeyBs58 = await decryptWithPassword(record.encryptedPrivateKey, masterKey, record.salt)
  const secretKey = bs58Decode(privateKeyBs58)

  return Keypair.fromSecretKey(secretKey)
}

export const listWallets = async (): Promise<WalletInfo[]> => {
  const records = await listFromStore()
  return records.map(r => ({
    name: r.name,
    publicKey: r.publicKey,
    network: r.network,
    createdAt: r.createdAt,
    tags: r.tags,
  }))
}

export const getPublicKey = async (name: string): Promise<string> => {
  const record = await getWallet(name)
  if (!record) throw new Error(`Wallet "${name}" not found`)
  return record.publicKey
}
