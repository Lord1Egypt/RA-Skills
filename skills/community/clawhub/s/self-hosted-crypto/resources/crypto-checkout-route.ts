import { NextResponse } from 'next/server'
import { createClient, createServiceClient } from '@/lib/supabase/server'
import { checkRateLimit } from '@/lib/rate-limit'
import { PLANS } from '@/lib/stripe'
import { CREDIT_PACKS } from '@/lib/models'
import { routeCoin, deriveAddress, COINGECKO_IDS, type WalletType } from '@/lib/crypto-wallets'

const SUPPORTED_COINS = [
  // Polygon
  'polygon/usdc', 'polygon/usdt', 'matic',
  // Base
  'base/usdc', 'base/eth',
  // Arbitrum
  'arb/usdc', 'arb/usdt', 'arb/eth',
  // Optimism
  'op/usdc', 'op/eth',
  // Solana
  'sol/usdc', 'sol/usdt', 'sol',
  // BNB Chain
  'bep20/usdc', 'bep20/usdt', 'bnb',
  // Ethereum
  'eth/usdc', 'eth/usdt', 'eth/dai', 'eth',
  // Avalanche
  'avax/usdc', 'avax',
  // Bitcoin
  'btc',
] as const
type CoinId = typeof SUPPORTED_COINS[number]

// ─── Exchange rate ────────────────────────────────────────────────────────────

async function getAmountCoin(amountUsd: number, coin: string): Promise<number> {
  const route = routeCoin(coin)!

  // Stablecoins are 1:1 USD — no API call needed
  if (route.token === 'usdc' || route.token === 'usdt' || route.token === 'dai') {
    return parseFloat(amountUsd.toFixed(route.decimals))
  }

  // Native token: map to CoinGecko ID
  // e.g. 'base/eth' → 'eth', 'arb/eth' → 'eth', 'matic' → 'matic', 'btc' → 'btc'
  const nativeSymbol = coin.includes('/') ? coin.split('/')[1] : coin
  const geckoId = COINGECKO_IDS[nativeSymbol]
  if (!geckoId) throw new Error(`No CoinGecko ID for coin: ${coin}`)

  const res = await fetch(
    `https://api.coingecko.com/api/v3/simple/price?ids=${geckoId}&vs_currencies=usd`,
    { cache: 'no-store', signal: AbortSignal.timeout(6000) }
  )
  if (!res.ok) throw new Error(`CoinGecko API failed: ${res.status}`)
  const data = await res.json()
  const priceUsd: number = data[geckoId]?.usd
  if (!priceUsd) throw new Error(`No price returned for ${geckoId}`)

  const amount = amountUsd / priceUsd
  return parseFloat(amount.toFixed(Math.min(route.decimals, 8)))
}

// ─── POST /api/billing/crypto-checkout ───────────────────────────────────────

export async function POST(request: Request) {
  // Auth
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Rate limit: 3 requests per 5 minutes
  const rl = await checkRateLimit(`crypto-checkout:${user.id}`, { limit: 3, windowMs: 5 * 60 * 1000 })
  if (!rl.allowed) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 })
  }

  // Parse body
  let body: { type: string; packId?: string; plan?: string; months?: number; addonId?: string; botId?: string; coin: string }
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ error: 'Invalid JSON' }, { status: 400 })
  }

  const { type, packId, plan, months, addonId, botId, coin } = body

  // Validate coin
  if (!SUPPORTED_COINS.includes(coin as CoinId)) {
    return NextResponse.json({ error: 'Unsupported coin' }, { status: 400 })
  }
  const route = routeCoin(coin)
  if (!route) {
    return NextResponse.json({ error: 'Unsupported coin' }, { status: 400 })
  }

  // Resolve amount_usd + payment metadata
  let amount_usd: number
  let credits: number | null = null
  let planId: string | null = null
  let planMonths: number | null = null

  if (type === 'credits') {
    if (!packId) return NextResponse.json({ error: 'packId required for credits' }, { status: 400 })
    const pack = CREDIT_PACKS.find(p => p.id === packId)
    if (!pack) return NextResponse.json({ error: 'Invalid packId' }, { status: 400 })
    amount_usd = pack.price
    credits = pack.credits
  } else if (type === 'plan') {
    if (!plan) return NextResponse.json({ error: 'plan required for plan type' }, { status: 400 })
    const planConfig = PLANS.find(p => p.id === plan)
    if (!planConfig) return NextResponse.json({ error: 'Invalid plan' }, { status: 400 })
    if (planConfig.billing === 'once') {
      amount_usd = planConfig.price
      planId = plan
    } else {
      if (!months || ![1, 3, 6, 12].includes(months)) {
        return NextResponse.json({ error: 'months must be 1, 3, 6, or 12' }, { status: 400 })
      }
      amount_usd = parseFloat((planConfig.price * months).toFixed(2))
      planId = plan
      planMonths = months
    }
  } else if (type === 'addon') {
    const validAddons: Record<string, number> = {
      lifetime_memory_boost: 12.99,
      lifetime_power_pack: 29.99,
    }
    if (!addonId || !validAddons[addonId]) {
      return NextResponse.json({ error: 'Invalid addonId' }, { status: 400 })
    }
    // Validate bot ownership if botId provided
    if (botId) {
      const { data: bot } = await supabase
        .from('bots')
        .select('id')
        .eq('id', botId)
        .eq('user_id', user.id)
        .single()
      if (!bot) {
        return NextResponse.json({ error: 'Bot not found' }, { status: 404 })
      }
    }
    amount_usd = validAddons[addonId]
    // Store addonId:botId in the plan column for per-bot fulfillment
    planId = botId ? `${addonId}:${botId}` : addonId
  } else {
    return NextResponse.json({ error: 'type must be "credits", "plan", or "addon"' }, { status: 400 })
  }

  // Fetch exchange rate
  let amount_coin: number
  try {
    amount_coin = await getAmountCoin(amount_usd, coin)
  } catch (err) {
    console.error('[crypto-checkout] Exchange rate fetch failed:', err)
    return NextResponse.json({ error: 'Failed to fetch exchange rate' }, { status: 502 })
  }

  const serviceClient = await createServiceClient()
  const expiresAt = new Date(Date.now() + 60 * 60 * 1000).toISOString() // 1-hour payment window
  const walletType: WalletType = route.walletType

  // Derive a unique address — retry on unique constraint collision (concurrent requests)
  let depositAddress!: string
  let derivationIndex!: number
  let paymentId!: string

  for (let attempt = 0; attempt < 3; attempt++) {
    // Get the highest derivation index used so far for this wallet type
    const { data: maxRow } = await serviceClient
      .from('crypto_payments')
      .select('derivation_index')
      .eq('wallet_type', walletType)
      .order('derivation_index', { ascending: false })
      .limit(1)
      .maybeSingle()

    derivationIndex = ((maxRow as { derivation_index: number } | null)?.derivation_index ?? -1) + 1 + attempt

    try {
      depositAddress = deriveAddress(walletType, derivationIndex)
    } catch (err) {
      console.error('[crypto-checkout] Address derivation failed:', err)
      return NextResponse.json({ error: 'Address generation failed' }, { status: 500 })
    }

    const { data: payment, error: insertError } = await serviceClient
      .from('crypto_payments')
      .insert({
        user_id: user.id,
        type,
        credits,
        plan: planId,
        months: planMonths,
        amount_usd,
        amount_coin,
        coin,
        address: depositAddress,
        wallet_type: walletType,
        derivation_index: derivationIndex,
        status: 'pending',
        expires_at: expiresAt,
      })
      .select('id')
      .single()

    if (insertError) {
      // Unique constraint violation — another concurrent request took this index; try next
      if ((insertError as { code?: string }).code === '23505') {
        continue
      }
      console.error('[crypto-checkout] Insert failed:', insertError)
      return NextResponse.json({ error: 'Failed to create payment' }, { status: 500 })
    }

    paymentId = payment!.id
    break
  }

  if (!paymentId) {
    return NextResponse.json({ error: 'Failed to allocate payment address' }, { status: 500 })
  }

  return NextResponse.json({
    paymentId,
    address: depositAddress,
    amount_coin,
    amount_usd,
    coin,
    expires_at: expiresAt,
  })
}
