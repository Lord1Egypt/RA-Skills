#!/usr/bin/env node
/**
 * claim-bets.js — check redeemable bets and claim winnings on-chain via Pinwin
 *
 * Usage:
 *   node claim-bets.js                    # fetch redeemable bets and claim all
 *   node claim-bets.js --check-only       # show redeemable bets without claiming
 *   node claim-bets.js --betIds 42 43     # claim specific betIds directly
 *   node claim-bets.js --betIds 42,43     # comma-separated also works
 *
 * Required env: BETTOR_PRIVATE_KEY
 * Optional env: POLYGON_RPC_URL
 */

const { createPublicClient, createWalletClient, http } = require('viem')
const { privateKeyToAccount } = require('viem/accounts')
const { polygon } = require('viem/chains')
const { createInterface } = require('readline')

// ─── Constants ───────────────────────────────────────────────────────────────
const PINWIN_CLAIM_URL  = 'https://api.pinwin.xyz/agent/claim'
const BETS_SUBGRAPH_URL = 'https://thegraph.onchainfeed.org/subgraphs/name/azuro-protocol/azuro-api-polygon-v3'
/** Azuro ClientCore on Polygon — must match payload.to */
const CLAIM_CONTRACT    = '0x0FA7FB5407eA971694652E6E16C12A52625DE1b8'
const DEFAULT_RPC       = 'https://polygon-bor-rpc.publicnode.com'

// ─── Args ────────────────────────────────────────────────────────────────────
const args       = process.argv.slice(2)
const checkOnly  = args.includes('--check-only')
const betIdsIdx  = args.indexOf('--betIds')
const betIdsArg  = betIdsIdx !== -1
  ? args.slice(betIdsIdx + 1).join(',').split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n))
  : []

// ─── Setup ───────────────────────────────────────────────────────────────────
const privateKeyRaw = process.env.BETTOR_PRIVATE_KEY || ''
if (!privateKeyRaw) {
  console.error('Error: BETTOR_PRIVATE_KEY env var is not set')
  process.exit(1)
}
const privateKey = privateKeyRaw.startsWith('0x') ? privateKeyRaw : '0x' + privateKeyRaw
const account    = privateKeyToAccount(privateKey)
const bettor     = account.address.toLowerCase()
const rpc        = process.env.POLYGON_RPC_URL || DEFAULT_RPC

const publicClient = createPublicClient({ chain: polygon, transport: http(rpc) })
const walletClient = createWalletClient({ account, chain: polygon, transport: http(rpc) })

// ─── Query redeemable bets from subgraph ─────────────────────────────────────
async function fetchRedeemableBets() {
  const res = await fetch(BETS_SUBGRAPH_URL, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `query RedeemableBets($where: V3_Bet_filter!, $first: Int, $orderBy: V3_Bet_orderBy, $orderDirection: OrderDirection) {
        v3Bets(where: $where, first: $first, orderBy: $orderBy, orderDirection: $orderDirection) {
          betId status result isRedeemable isRedeemed amount payout createdBlockTimestamp
        }
      }`,
      variables: {
        where:          { bettor, isRedeemable: true },
        first:          50,
        orderBy:        'createdBlockTimestamp',
        orderDirection: 'desc',
      },
    }),
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok)    throw new Error(`Subgraph HTTP ${res.status}: ${JSON.stringify(data)}`)
  if (data.errors) throw new Error(`Subgraph error: ${JSON.stringify(data.errors)}`)
  return data.data?.v3Bets || []
}

// ─── Claim ────────────────────────────────────────────────────────────────────
async function claimBets(betIds) {
  console.log(`\n⏳ Calling Pinwin POST /agent/claim...`, { betIds, chain: 'polygon' })

  const res = await fetch(PINWIN_CLAIM_URL, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ betIds, chain: 'polygon' }),
  })
  const body = await res.json().catch(() => ({}))

  if (!res.ok) {
    throw new Error(`Pinwin claim error ${res.status}: ${JSON.stringify(body)}`)
  }
  if (!body.encoded) {
    throw new Error(`Pinwin response missing encoded field: ${JSON.stringify(body)}`)
  }

  const payload = JSON.parse(Buffer.from(body.encoded, 'base64').toString('utf8'))
  console.log('\n📋 Decoded claim payload:', JSON.stringify(payload, null, 2))

  // CRITICAL: verify claim contract
  if ((payload.to || '').toLowerCase() !== CLAIM_CONTRACT.toLowerCase()) {
    throw new Error(`❌ Claim contract mismatch! payload.to=${payload.to} expected=${CLAIM_CONTRACT}`)
  }
  console.log(`\n   ✅ Contract verified: ${payload.to}`)

  // Confirmation gate
  const rl = createInterface({ input: process.stdin, output: process.stdout })
  const answer = await new Promise(resolve => {
    rl.question(
      `\n🛑 CONFIRM CLAIM\n   Bet IDs: ${betIds.join(', ')}\n   Proceed? (type "yes" to confirm): `,
      ans => { rl.close(); resolve(ans.trim().toLowerCase()) }
    )
  })
  if (answer !== 'yes' && answer !== 'y') {
    console.log('\n❌ Claim cancelled by user.')
    process.exit(0)
  }

  // Send transaction
  console.log('\n⏳ Sending claim tx...')
  const value = payload.value != null ? BigInt(payload.value) : 0n
  const hash  = await walletClient.sendTransaction({
    to:      payload.to,
    data:    payload.data,
    value,
    chainId: Number(payload.chainId),
  })
  console.log(`   Tx hash: https://polygonscan.com/tx/${hash}`)

  console.log('   Waiting for receipt...')
  const receipt = await publicClient.waitForTransactionReceipt({ hash })

  console.log('\n' + '─'.repeat(50))
  console.log('✅ Winnings claimed!')
  console.log(`   Bet IDs: ${betIds.join(', ')}`)
  console.log(`   Block:   ${receipt.blockNumber}`)
  console.log(`   Status:  ${receipt.status}`)
  console.log(`   Tx:      https://polygonscan.com/tx/${hash}`)
  console.log('─'.repeat(50))

  console.log('\n---JSON---')
  console.log(JSON.stringify({ success: true, txHash: hash, betIds, polygonscan: `https://polygonscan.com/tx/${hash}` }))
}

// ─── Main ─────────────────────────────────────────────────────────────────────
;(async () => {
  console.log(`\n💰 claim-bets.js — Pinwin / Azuro`)
  console.log(`   Wallet: ${account.address}\n`)

  // If specific betIds provided, claim directly
  if (betIdsArg.length > 0) {
    console.log(`   Mode: direct claim for betIds ${betIdsArg.join(', ')}`)
    await claimBets(betIdsArg)
    return
  }

  // Otherwise fetch redeemable bets first
  console.log('⏳ Querying redeemable bets (isRedeemable: true)...')
  let redeemable = []
  try {
    redeemable = await fetchRedeemableBets()
  } catch (e) {
    console.error('❌ Failed to fetch bets:', e.message)
    process.exit(1)
  }

  if (redeemable.length === 0) {
    console.log('   No redeemable bets found for this wallet.')
    process.exit(0)
  }

  // Show summary
  console.log(`\n🎉 ${redeemable.length} bet(s) ready to claim:\n`)
  let totalPayout = 0
  redeemable.forEach(b => {
    const date   = new Date(parseInt(b.createdBlockTimestamp) * 1000)
      .toLocaleDateString('es-ES', { timeZone: 'Europe/Madrid' })
    const payout = parseFloat(b.payout || b.amount)
    totalPayout += payout
    const type   = b.status === 'Canceled' ? '🔄 Canceled (refund)' : '✅ Won'
    console.log(`   betId ${b.betId} | ${date} | ${type} | ${payout.toFixed(2)} USDT`)
  })
  console.log(`\n   Total claimable: ${totalPayout.toFixed(2)} USDT`)

  if (checkOnly) {
    console.log('\n   [--check-only] No claim executed.')
    process.exit(0)
  }

  const betIds = redeemable.map(b => parseInt(b.betId, 10))
  await claimBets(betIds)

})().catch(e => {
  console.error('\n❌ Fatal error:', e.message)
  process.exit(1)
})
