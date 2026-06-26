import { readFile, writeFile } from "fs/promises"
import { existsSync } from "fs"
import { WALLET_STORE_PATH } from "./environment.ts"
import type { WalletStore, EncryptedWalletRecord } from "./types.ts"

const DEFAULT_STORE: WalletStore = { version: 1, wallets: {} }

export const readStore = async (): Promise<WalletStore> => {
  if (!existsSync(WALLET_STORE_PATH)) return structuredClone(DEFAULT_STORE)
  const raw = await readFile(WALLET_STORE_PATH, "utf-8")
  return JSON.parse(raw) as WalletStore
}

export const writeStore = async (store: WalletStore): Promise<void> => {
  await writeFile(WALLET_STORE_PATH, JSON.stringify(store, null, 2), "utf-8")
}

export const getWallet = async (name: string): Promise<EncryptedWalletRecord | null> => {
  const store = await readStore()
  return store.wallets[name] ?? null
}

export const saveWallet = async (record: EncryptedWalletRecord): Promise<void> => {
  const store = await readStore()
  store.wallets[record.name] = record
  await writeStore(store)
}

export const listWallets = async (): Promise<EncryptedWalletRecord[]> => {
  const store = await readStore()
  return Object.values(store.wallets)
}

export const deleteWallet = async (name: string): Promise<void> => {
  const store = await readStore()
  delete store.wallets[name]
  await writeStore(store)
}
