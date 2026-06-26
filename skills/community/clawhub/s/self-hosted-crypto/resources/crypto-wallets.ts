/**
 * crypto-wallets.ts
 *
 * Self-custody HD wallet derivation for on-chain crypto payments.
 * The master mnemonic (CRYPTO_MASTER_MNEMONIC) never leaves the server.
 *
 * Derivation paths:
 *   EVM:  m/44'/60'/0'/0/{index}  — checksummed Ethereum address, valid on all EVM chains
 *   BTC:  m/84'/0'/0'/0/{index}   — native SegWit P2WPKH (bc1q...)
 *   SOL:  m/44'/501'/{index}'/0'  — ed25519 public key (base58)
 *
 * SERVER-ONLY — never import this in client components.
 */

import { createHmac } from 'crypto'
import { HDNodeWallet, Mnemonic } from 'ethers'
import { HDKey } from '@scure/bip32'
import { mnemonicToSeedSync } from '@scure/bip39'
import { sha256 } from '@noble/hashes/sha256'
import { ripemd160 } from '@noble/hashes/ripemd160'
import { bech32 } from '@scure/base'
import { Keypair } from '@solana/web3.js'

// ─── Types ────────────────────────────────────────────────────────────────────

export type WalletType = 'evm' | 'btc' | 'sol'

export interface CoinRoute {
  walletType: WalletType
  network?: string   // key into EVM_CHAINS (EVM only)
  token?: string     // 'usdc' | 'usdt' | 'dai' — undefined means native
  decimals: number
}

// ─── Chain configuration ──────────────────────────────────────────────────────

export interface EvmChainConfig {
  rpc: string
  chainId: number
}

export const EVM_CHAINS: Record<string, EvmChainConfig> = {
  eth:       { rpc: 'https://cloudflare-eth.com',             chainId: 1     },
  base:      { rpc: 'https://mainnet.base.org',               chainId: 8453  },
  polygon:   { rpc: 'https://polygon-rpc.com',                chainId: 137   },
  arbitrum:  { rpc: 'https://arb1.arbitrum.io/rpc',           chainId: 42161 },
  optimism:  { rpc: 'https://mainnet.optimism.io',            chainId: 10    },
  bnb:       { rpc: 'https://bsc-dataseed.binance.org',       chainId: 56    },
  avalanche: { rpc: 'https://api.avax.network/ext/bc/C/rpc',  chainId: 43114 },
}

// ERC-20 token contract addresses per network
export const ERC20_CONTRACTS: Record<string, Partial<Record<string, string>>> = {
  usdc: {
    eth:       '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    base:      '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    polygon:   '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',
    arbitrum:  '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
    optimism:  '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',
    bnb:       '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
    avalanche: '0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E',
  },
  usdt: {
    eth:       '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    polygon:   '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
    arbitrum:  '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
    bnb:       '0x55d398326f99059fF775485246999027B3197955',
  },
  dai: {
    eth:       '0x6B175474E89094C44Da98b954EedeAC495271d0F',
  },
}

// Solana SPL token mint addresses
export const SOL_TOKEN_MINTS: Record<string, string> = {
  usdc: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  usdt: 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
}

export const SOL_RPC = 'https://api.mainnet-beta.solana.com'
export const BTC_API = 'https://mempool.space/api/address'

// CoinGecko IDs for native token price lookups
export const COINGECKO_IDS: Record<string, string> = {
  eth:       'ethereum',
  matic:     'matic-network',
  bnb:       'binancecoin',
  avax:      'avalanche-2',
  sol:       'solana',
  btc:       'bitcoin',
}

// ─── Coin routing ─────────────────────────────────────────────────────────────

/**
 * Maps a coin ID (stored in crypto_payments.coin) to routing info.
 * Returns null for unsupported coins.
 */
export function routeCoin(coin: string): CoinRoute | null {
  switch (coin) {
    // Ethereum
    case 'eth':          return { walletType: 'evm', network: 'eth',       decimals: 18 }
    case 'eth/usdc':     return { walletType: 'evm', network: 'eth',       token: 'usdc', decimals: 6 }
    case 'eth/usdt':     return { walletType: 'evm', network: 'eth',       token: 'usdt', decimals: 6 }
    case 'eth/dai':      return { walletType: 'evm', network: 'eth',       token: 'dai',  decimals: 18 }
    // Base
    case 'base/eth':     return { walletType: 'evm', network: 'base',      decimals: 18 }
    case 'base/usdc':    return { walletType: 'evm', network: 'base',      token: 'usdc', decimals: 6 }
    // Polygon
    case 'matic':        return { walletType: 'evm', network: 'polygon',   decimals: 18 }
    case 'polygon/usdc': return { walletType: 'evm', network: 'polygon',   token: 'usdc', decimals: 6 }
    case 'polygon/usdt': return { walletType: 'evm', network: 'polygon',   token: 'usdt', decimals: 6 }
    // Arbitrum
    case 'arb/eth':      return { walletType: 'evm', network: 'arbitrum',  decimals: 18 }
    case 'arb/usdc':     return { walletType: 'evm', network: 'arbitrum',  token: 'usdc', decimals: 6 }
    case 'arb/usdt':     return { walletType: 'evm', network: 'arbitrum',  token: 'usdt', decimals: 6 }
    // Optimism
    case 'op/eth':       return { walletType: 'evm', network: 'optimism',  decimals: 18 }
    case 'op/usdc':      return { walletType: 'evm', network: 'optimism',  token: 'usdc', decimals: 6 }
    // BNB Chain
    case 'bnb':          return { walletType: 'evm', network: 'bnb',       decimals: 18 }
    case 'bep20/usdc':   return { walletType: 'evm', network: 'bnb',       token: 'usdc', decimals: 6 }
    case 'bep20/usdt':   return { walletType: 'evm', network: 'bnb',       token: 'usdt', decimals: 6 }
    // Avalanche
    case 'avax':         return { walletType: 'evm', network: 'avalanche', decimals: 18 }
    case 'avax/usdc':    return { walletType: 'evm', network: 'avalanche', token: 'usdc', decimals: 6 }
    // Bitcoin
    case 'btc':          return { walletType: 'btc', decimals: 8 }
    // Solana
    case 'sol':          return { walletType: 'sol', decimals: 9 }
    case 'sol/usdc':     return { walletType: 'sol', token: 'usdc', decimals: 6 }
    case 'sol/usdt':     return { walletType: 'sol', token: 'usdt', decimals: 6 }
    default: return null
  }
}

// ─── HD Derivation ────────────────────────────────────────────────────────────

function getMnemonic(): string {
  const m = process.env.CRYPTO_MASTER_MNEMONIC?.trim()
  if (!m) throw new Error('CRYPTO_MASTER_MNEMONIC is not set')
  return m
}

/**
 * Derive an EVM address at the given index.
 * Path: m/44'/60'/0'/0/{index}
 * Returns a checksummed Ethereum address valid on all EVM chains.
 */
export function deriveEvmAddress(index: number): string {
  const mnemonic = getMnemonic()
  // Derive to m/44'/60'/0'/0 (account chain root), then child index = MetaMask Account N+1
  const parent = HDNodeWallet.fromPhrase(mnemonic, undefined, "m/44'/60'/0'/0")
  return parent.deriveChild(index).address
}

/**
 * Derive a Bitcoin native SegWit (bech32 P2WPKH) address at the given index.
 * Path: m/84'/0'/0'/0/{index}
 * Returns a bc1q... address.
 */
export function deriveBtcAddress(index: number): string {
  const seed = mnemonicToSeedSync(getMnemonic())
  const root = HDKey.fromMasterSeed(seed)
  const child = root.derive(`m/84'/0'/0'/0/${index}`)
  if (!child.publicKey) throw new Error('BTC derivation failed: no public key')

  // P2WPKH: OP_0 <hash160(pubkey)>
  const hash160 = ripemd160(sha256(child.publicKey))
  const words = bech32.toWords(hash160)
  return bech32.encode('bc', [0, ...words])
}

/**
 * Derive a Solana address at the given index using SLIP-0010 ed25519 derivation.
 * Path: m/44'/501'/{index}'/0'  (all-hardened, matches Phantom/Solflare)
 * Returns a base58 public key.
 *
 * Note: SLIP-0010 uses HMAC key "ed25519 seed" (not BIP32's "Bitcoin seed").
 * This is the standard used by all major Solana wallets.
 */
export function deriveSolAddress(index: number): string {
  const seed = mnemonicToSeedSync(getMnemonic())

  // SLIP-0010 master key derivation
  let I = createHmac('sha512', 'ed25519 seed').update(seed).digest()
  let key = I.slice(0, 32)
  let chainCode = I.slice(32)

  // Derive each hardened segment: 44' → 501' → {index}' → 0'
  for (const idx of [44, 501, index, 0]) {
    const indexBuf = Buffer.alloc(4)
    indexBuf.writeUInt32BE(0x80000000 + idx) // hardened
    const data = Buffer.concat([Buffer.from([0x00]), key, indexBuf])
    I = createHmac('sha512', chainCode).update(data).digest()
    key = I.slice(0, 32)
    chainCode = I.slice(32)
  }

  return Keypair.fromSeed(key).publicKey.toBase58()
}

/**
 * Derive the deposit address for the given wallet type and derivation index.
 */
export function deriveAddress(walletType: WalletType, index: number): string {
  switch (walletType) {
    case 'evm': return deriveEvmAddress(index)
    case 'btc': return deriveBtcAddress(index)
    case 'sol': return deriveSolAddress(index)
  }
}

// ─── Amount conversion ────────────────────────────────────────────────────────

/**
 * Convert a decimal coin amount (e.g. 0.00123 ETH) to its raw integer
 * representation (wei, lamports, satoshis, token units).
 * Uses string math to avoid floating-point precision drift.
 */
export function toRawAmount(amountCoin: number, decimals: number): bigint {
  const fixed = amountCoin.toFixed(decimals)
  const [integer, fraction = ''] = fixed.split('.')
  const paddedFraction = fraction.padEnd(decimals, '0').slice(0, decimals)
  const factor = 10n ** BigInt(decimals)
  return BigInt(integer) * factor + BigInt(paddedFraction)
}
