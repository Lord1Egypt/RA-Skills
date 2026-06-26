// Polymarket CLOB API — authenticated order management
// Auth model:
//   L1: EIP-712 ClobAuth signature → derive API credentials (key, secret, passphrase)
//   L2: HMAC-SHA256 of (timestamp + method + path + body) using secret → request headers
// Order signing: EIP-712 Order struct signed with the EVM wallet private key.

import { ethers } from "ethers"
import { createHmac } from "crypto"
import type { ethers as EthersType } from "ethers"

const CLOB_API = "https://clob.polymarket.com"
const POLYGON_RPC = process.env["POLYGON_RPC_URL"] ?? "https://polygon-rpc.com"
const USDC_POLYGON = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"

// Neg Risk CTF Exchange — used for all Polymarket weather markets (negRisk: true)
const NEG_RISK_CTF_EXCHANGE = "0xC5d563A36AE78145C45a50134d48A1215220f80a"

// ── Types ─────────────────────────────────────────────────────────────────────

export type ClobCreds = {
  apiKey: string
  apiSecret: string
  passphrase: string
}

export type PlacedOrder = {
  orderId: string
  status: string
  tokenId: string
  price: number
  sizeUsdc: number
}

// ── EIP-712 domains + types ───────────────────────────────────────────────────

const AUTH_DOMAIN = {
  name: "ClobAuthDomain",
  version: "1",
  chainId: 137n,
} as const

const AUTH_TYPES = {
  ClobAuth: [
    { name: "address",   type: "address" },
    { name: "timestamp", type: "string"  },
    { name: "nonce",     type: "int256"  },
    { name: "message",   type: "string"  },
  ],
}

const ORDER_DOMAIN = {
  name: "Polymarket CTF Exchange",
  version: "1",
  chainId: 137n,
  verifyingContract: NEG_RISK_CTF_EXCHANGE,
} as const

const ORDER_TYPES = {
  Order: [
    { name: "salt",          type: "uint256" },
    { name: "maker",         type: "address" },
    { name: "signer",        type: "address" },
    { name: "taker",         type: "address" },
    { name: "tokenId",       type: "uint256" },
    { name: "makerAmount",   type: "uint256" },
    { name: "takerAmount",   type: "uint256" },
    { name: "expiration",    type: "uint256" },
    { name: "nonce",         type: "uint256" },
    { name: "feeRateBps",    type: "uint256" },
    { name: "side",          type: "uint8"   },
    { name: "signatureType", type: "uint8"   },
  ],
}

// ── L1 Auth — derive API credentials ─────────────────────────────────────────

// Credentials are valid until invalidated; cache per wallet address for the process lifetime.
const credsCache = new Map<string, ClobCreds>()

export const getApiCreds = async (wallet: EthersType.Wallet): Promise<ClobCreds> => {
  const cached = credsCache.get(wallet.address)
  if (cached) return cached

  const timestamp = String(Math.floor(Date.now() / 1000))

  const signature = await wallet.signTypedData(AUTH_DOMAIN, AUTH_TYPES, {
    address:   wallet.address,
    timestamp,
    nonce:     0,
    message:   "This message attests that I control the given wallet",
  })

  const res = await fetch(`${CLOB_API}/auth/api-key`, {
    method: "GET",
    headers: {
      "POLY_ADDRESS":   wallet.address,
      "POLY_SIGNATURE": signature,
      "POLY_TIMESTAMP": timestamp,
      "POLY_NONCE":     "0",
    },
  })

  if (!res.ok) throw new Error(`CLOB auth failed (${res.status}): ${await res.text()}`)
  const data = await res.json() as { apiKey?: string; secret?: string; passphrase?: string }
  if (!data.apiKey || !data.secret || !data.passphrase) {
    throw new Error(`CLOB auth: unexpected response shape: ${JSON.stringify(data)}`)
  }

  const creds: ClobCreds = { apiKey: data.apiKey, apiSecret: data.secret, passphrase: data.passphrase }
  credsCache.set(wallet.address, creds)
  return creds
}

// ── L2 HMAC auth headers ──────────────────────────────────────────────────────

const l2Headers = (
  creds: ClobCreds,
  walletAddress: string,
  method: string,
  path: string,
  body = "",
): Record<string, string> => {
  const timestamp = String(Date.now() / 1000)
  const msg = timestamp + method.toUpperCase() + path + body
  const sig = createHmac("sha256", creds.apiSecret).update(msg).digest("base64")
  return {
    "Content-Type":    "application/json",
    "POLY_ADDRESS":    walletAddress,
    "POLY_SIGNATURE":  sig,
    "POLY_TIMESTAMP":  timestamp,
    "POLY_NONCE":      "0",
    "POLY_API-KEY":    creds.apiKey,
    "POLY_PASSPHRASE": creds.passphrase,
  }
}

// ── USDC balance check (Polygon RPC) ──────────────────────────────────────────

export const getUsdcBalance = async (address: string): Promise<number> => {
  const provider = new ethers.JsonRpcProvider(POLYGON_RPC)
  const usdc = new ethers.Contract(
    USDC_POLYGON,
    ["function balanceOf(address) view returns (uint256)"],
    provider,
  )
  const raw: bigint = await usdc.balanceOf(address) as bigint
  return Number(raw) / 1e6
}

// ── Place order ────────────────────────────────────────────────────────────────
// BUY `sizeUsdc` worth of YES shares at `limitPrice` (0–1).
// maker pays USDC, taker delivers YES tokens.

export const placeOrder = async (
  wallet: EthersType.Wallet,
  tokenId: string,
  limitPrice: number,    // e.g. 0.30
  sizeUsdc: number,      // USDC to spend, e.g. 5.0
): Promise<PlacedOrder> => {
  // Amount math (6 decimals for both USDC and CTF tokens)
  const tokensToReceive = sizeUsdc / limitPrice
  const makerAmount = BigInt(Math.floor(sizeUsdc      * 1e6))
  const takerAmount = BigInt(Math.floor(tokensToReceive * 1e6))

  const salt = BigInt(Math.floor(Math.random() * 1e15))
  const zero = "0x0000000000000000000000000000000000000000"

  const orderStruct = {
    salt,
    maker:         wallet.address,
    signer:        wallet.address,
    taker:         zero,
    tokenId:       BigInt(tokenId),
    makerAmount,
    takerAmount,
    expiration:    BigInt(0),   // GTC
    nonce:         BigInt(0),
    feeRateBps:    BigInt(0),
    side:          0,           // BUY
    signatureType: 0,           // EOA
  }

  const signature = await wallet.signTypedData(ORDER_DOMAIN, ORDER_TYPES, orderStruct)

  const body = JSON.stringify({
    order: {
      salt:          salt.toString(),
      maker:         wallet.address,
      signer:        wallet.address,
      taker:         zero,
      tokenId:       tokenId,
      makerAmount:   makerAmount.toString(),
      takerAmount:   takerAmount.toString(),
      expiration:    "0",
      nonce:         "0",
      feeRateBps:    "0",
      side:          0,
      signatureType: 0,
      signature,
    },
    owner:     wallet.address,
    orderType: "GTC",
  })

  const creds = await getApiCreds(wallet)
  const headers = l2Headers(creds, wallet.address, "POST", "/order", body)

  const res = await fetch(`${CLOB_API}/order`, { method: "POST", headers, body })
  if (!res.ok) throw new Error(`CLOB order failed (${res.status}): ${await res.text()}`)

  const data = await res.json() as { orderID?: string; status?: string; errorMsg?: string }
  if (data.errorMsg) throw new Error(`CLOB order rejected: ${data.errorMsg}`)

  return {
    orderId:  data.orderID ?? "unknown",
    status:   data.status  ?? "unknown",
    tokenId,
    price:    limitPrice,
    sizeUsdc,
  }
}

// ── List open orders ───────────────────────────────────────────────────────────

export const getOpenOrders = async (wallet: EthersType.Wallet): Promise<Array<{ id: string; asset_id: string }>> => {
  const creds = await getApiCreds(wallet)
  const path = "/orders?market_status=open"
  const headers = l2Headers(creds, wallet.address, "GET", path)

  const res = await fetch(`${CLOB_API}${path}`, { headers })
  if (!res.ok) throw new Error(`CLOB getOpenOrders failed (${res.status}): ${await res.text()}`)

  const data = await res.json() as Array<{ id: string; asset_id: string }>
  return Array.isArray(data) ? data : []
}

// ── Cancel order ───────────────────────────────────────────────────────────────

export const cancelOrder = async (wallet: EthersType.Wallet, orderId: string): Promise<void> => {
  const body = JSON.stringify({ orderID: orderId })
  const creds = await getApiCreds(wallet)
  const headers = l2Headers(creds, wallet.address, "DELETE", "/order", body)

  const res = await fetch(`${CLOB_API}/order`, { method: "DELETE", headers, body })
  if (!res.ok) throw new Error(`CLOB cancelOrder failed (${res.status}): ${await res.text()}`)
}
