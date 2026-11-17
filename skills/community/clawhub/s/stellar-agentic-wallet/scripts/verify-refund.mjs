#!/usr/bin/env node
// Poll a refund receipt until it is signed, then verify the signature.
//
//   node scripts/verify-refund.mjs <refund_id> [--wait] [--timeout <sec>] [--router <url>]
//
// Without --wait: one fetch; exits 2 if the refund is still pending.
// With --wait: polls every 5s until the receipt is signed. Refunds are
// paced by a once-per-minute signer cron, so they normally land within
// 1-2 minutes of the failed call; default timeout is 180s.
//
// Exit codes: 0 VALID · 1 INVALID or error · 2 still pending (no --wait)
// Read-only: no keys, no payments, no wallet needed.

import { Keypair, StrKey } from '@stellar/stellar-sdk'

const FIELDS = [
  'version', 'payment_id', 'payment_tx', 'merchant', 'amount', 'mode',
  'outcome', 'refund_tx', 'refund_amount', 'reason', 'confirmed_ledger',
  'iat', 'exp',
]

const args = process.argv.slice(2)
const refundId = args.find((a) => !a.startsWith('--'))
const wait = args.includes('--wait')
const timeoutSec = Number(args[args.indexOf('--timeout') + 1] || 0) || 180
const router = args.includes('--router')
  ? args[args.indexOf('--router') + 1]
  : 'https://apiserver.mpprouter.dev'

if (!refundId) {
  console.error('usage: verify-refund.mjs <refund_id> [--wait] [--timeout <sec>] [--router <url>]')
  process.exit(1)
}

const statusUrl = `${router}/v1/refunds/${refundId}`
const fetchJson = async (url) => {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${url} -> HTTP ${res.status}`)
  return res.json()
}

let body = await fetchJson(statusUrl)
const pending = (b) => (b.receipt?.outcome ?? b.outcome) === 'refund_pending'

if (pending(body)) {
  if (!wait) {
    console.error(`refund_pending — refunds land within 1-2 minutes; re-run with --wait to poll`)
    process.exit(2)
  }
  const deadline = Date.now() + timeoutSec * 1000
  while (pending(body)) {
    if (Date.now() > deadline) {
      console.error(`still refund_pending after ${timeoutSec}s — signer cron may be stuck; report the refund id`)
      process.exit(1)
    }
    await new Promise((r) => setTimeout(r, 5000))
    body = await fetchJson(statusUrl)
    console.error(`… ${body.receipt?.outcome ?? body.outcome}`)
  }
}

if (body.algorithm !== 'Ed25519') {
  console.error(`unexpected algorithm ${body.algorithm}`)
  process.exit(1)
}

// Trust the operator's published addresses, not the one inside the receipt.
const health = await fetchJson(`${router}/health`)
const trusted = [
  health.stellar.receipt_signer,
  ...(health.stellar.receipt_signer_retired ?? []),
].filter(Boolean)
const signer = body.signer.stellar_address
if (!trusted.includes(signer)) {
  console.error(`untrusted signer ${signer} (trusted: ${trusted.join(', ')})`)
  process.exit(1)
}

// Rebuild the exact signed bytes (rozo-receipt-json-v1: fixed key order).
const canonical = {}
for (const field of FIELDS) {
  if (body.receipt[field] !== undefined) canonical[field] = body.receipt[field]
}
const message = Buffer.from(JSON.stringify(canonical), 'utf8')
const signature = Buffer.from(
  body.signature.replace(/-/g, '+').replace(/_/g, '/'), 'base64',
)

const ok = Keypair.fromPublicKey(signer).verify(message, signature)
console.log(ok ? 'VALID' : 'INVALID', '·', signer)
console.log('outcome', body.receipt.outcome,
  '· payment_tx', body.receipt.payment_tx,
  '· refund_tx', body.receipt.refund_tx)
console.log('ed25519 public key',
  Buffer.from(StrKey.decodeEd25519PublicKey(signer)).toString('hex'))
process.exit(ok ? 0 : 1)
