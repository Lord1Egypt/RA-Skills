// EVM wallet management for Polygon/Polymarket
// Uses the same AES-GCM + PBKDF2 encryption as src/wallet.ts.
// Stored separately from Solana wallets — different key curve (secp256k1 vs ed25519).

import { ethers } from "ethers"
import { readFile, writeFile } from "fs/promises"
import { existsSync } from "fs"
import path from "path"
import os from "os"
import { encryptWithPassword, decryptWithPassword, getMasterKey } from "./crypto.ts"

const EVM_WALLET_STORE_PATH =
  process.env["EVM_WALLET_STORE_PATH"] ??
  path.join(process.env["RAPHAEL_DATA_DIR"] ?? path.join(os.homedir(), ".raphael"), "evm-wallets.json")

type EvmWalletRecord = {
  name: string
  address: string               // checksummed Ethereum address
  encryptedPrivateKey: string   // AES-GCM, base64
  salt: string                  // PBKDF2 salt, base64
  createdAt: string
}

type EvmWalletStore = {
  version: number
  wallets: Record<string, EvmWalletRecord>
}

// ── Store helpers ─────────────────────────────────────────────────────────────

const readEvmStore = async (): Promise<EvmWalletStore> => {
  if (!existsSync(EVM_WALLET_STORE_PATH)) return { version: 1, wallets: {} }
  const raw = await readFile(EVM_WALLET_STORE_PATH, "utf-8")
  return JSON.parse(raw) as EvmWalletStore
}

const writeEvmStore = async (store: EvmWalletStore): Promise<void> => {
  await writeFile(EVM_WALLET_STORE_PATH, JSON.stringify(store, null, 2), "utf-8")
}

// ── Public API ────────────────────────────────────────────────────────────────

export type EvmWalletInfo = {
  name: string
  address: string
  createdAt: string
}

export const createEvmWallet = async (name: string): Promise<EvmWalletInfo> => {
  const store = await readEvmStore()
  if (store.wallets[name]) throw new Error(`EVM wallet "${name}" already exists`)

  const wallet = ethers.Wallet.createRandom()
  const masterKey = await getMasterKey()
  const { encrypted, salt } = await encryptWithPassword(wallet.privateKey, masterKey)

  store.wallets[name] = {
    name,
    address: wallet.address,
    encryptedPrivateKey: encrypted,
    salt,
    createdAt: new Date().toISOString(),
  }

  await writeEvmStore(store)
  return { name, address: wallet.address, createdAt: store.wallets[name].createdAt }
}

export const loadEvmWallet = async (name: string): Promise<ethers.Wallet> => {
  const store = await readEvmStore()
  const record = store.wallets[name]
  if (!record) throw new Error(`EVM wallet "${name}" not found. Run: solana-wallet evm-wallet create ${name}`)

  const masterKey = await getMasterKey()
  const privateKey = await decryptWithPassword(record.encryptedPrivateKey, masterKey, record.salt)
  return new ethers.Wallet(privateKey)
}

export const listEvmWallets = async (): Promise<EvmWalletInfo[]> => {
  const store = await readEvmStore()
  return Object.values(store.wallets).map(r => ({ name: r.name, address: r.address, createdAt: r.createdAt }))
}

export const getEvmAddress = async (name: string): Promise<string> => {
  const store = await readEvmStore()
  const record = store.wallets[name]
  if (!record) throw new Error(`EVM wallet "${name}" not found`)
  return record.address
}
