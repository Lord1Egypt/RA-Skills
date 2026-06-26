import { NextResponse } from 'next/server'
import { timingSafeEqual } from 'crypto'
import { createServiceClient } from '@/lib/supabase/server'
import { JsonRpcProvider, Contract } from 'ethers'
import { Connection, PublicKey } from '@solana/web3.js'
import {
  EVM_CHAINS, ERC20_CONTRACTS, SOL_RPC, BTC_API, SOL_TOKEN_MINTS,
  routeCoin, toRawAmount,
} from '@/lib/crypto-wallets'
import { ADDON_RESOURCES } from '@/lib/stripe'

export const maxDuration = 60

// Minimal ERC-20 ABI — only balanceOf needed
const ERC20_ABI = ['function balanceOf(address owner) view returns (uint256)']

// ─── Auth ──────────────────────────────────────────────────────────────────────

function isAuthorized(request: Request): boolean {
  const cronSecret = process.env.CRON_SECRET
  if (!cronSecret) return false
  const token = request.headers.get('Authorization')?.replace('Bearer ', '') ?? ''
  try {
    return (
      token.length === cronSecret.length &&
      timingSafeEqual(Buffer.from(token), Buffer.from(cronSecret))
    )
  } catch {
    return false
  }
}

// ─── Balance checkers ─────────────────────────────────────────────────────────

async function getEvmNativeBalance(rpc: string, address: string): Promise<bigint> {
  const provider = new JsonRpcProvider(rpc)
  return await provider.getBalance(address)
}

async function getEvmTokenBalance(
  rpc: string, address: string, tokenAddress: string
): Promise<bigint> {
  const provider = new JsonRpcProvider(rpc)
  const contract = new Contract(tokenAddress, ERC20_ABI, provider)
  return (await contract.balanceOf(address)) as bigint
}

async function getBtcBalanceSatoshis(address: string): Promise<bigint> {
  const res = await fetch(`${BTC_API}/${address}`, {
    cache: 'no-store',
    signal: AbortSignal.timeout(8000),
  })
  if (!res.ok) throw new Error(`mempool.space API failed: ${res.status}`)
  const data = await res.json()
  // funded_txo_sum = total satoshis ever received (cumulative, never decreases)
  return BigInt(data.chain_stats?.funded_txo_sum ?? 0)
}

async function getSolNativeBalance(address: string): Promise<bigint> {
  const connection = new Connection(SOL_RPC, 'confirmed')
  const lamports = await connection.getBalance(new PublicKey(address))
  return BigInt(lamports)
}

async function getSolTokenBalance(address: string, mintAddress: string): Promise<bigint> {
  const connection = new Connection(SOL_RPC, 'confirmed')
  const accounts = await connection.getTokenAccountsByOwner(new PublicKey(address), {
    mint: new PublicKey(mintAddress),
  })
  if (accounts.value.length === 0) return 0n

  let total = 0n
  for (const account of accounts.value) {
    const info = await connection.getTokenAccountBalance(account.pubkey)
    total += BigInt(info.value.amount)
  }
  return total
}

// ─── Payment application ──────────────────────────────────────────────────────

async function applyPayment(serviceClient: Awaited<ReturnType<typeof createServiceClient>>, payment: {
  id: string
  user_id: string
  type: string
  credits: number | null
  plan: string | null
  months: number | null
}) {
  if (payment.type === 'credits' && payment.credits) {
    const { error } = await serviceClient.rpc('add_credits', {
      p_user_id: payment.user_id,
      p_amount: payment.credits,
    })
    if (error) console.error(`[check-crypto] add_credits failed for ${payment.id}:`, error)
  } else if (payment.type === 'plan' && payment.plan) {
    if (payment.months) {
      const expiresAt = new Date()
      expiresAt.setDate(expiresAt.getDate() + payment.months * 30)
      const { error } = await serviceClient
        .from('profiles')
        .update({ plan: payment.plan, crypto_plan_expires_at: expiresAt.toISOString() })
        .eq('id', payment.user_id)
      if (error) console.error(`[check-crypto] Plan update failed for ${payment.id}:`, error)
    } else {
      const { error } = await serviceClient
        .from('profiles')
        .update({ plan: payment.plan })
        .eq('id', payment.user_id)
      if (error) console.error(`[check-crypto] Lifetime plan update failed for ${payment.id}:`, error)
    }
  } else if (payment.type === 'addon' && payment.plan) {
    // payment.plan stores "addonId:botId" or just "addonId" (legacy)
    const parts = payment.plan.split(':')
    const addonId = parts[0]
    const botId = parts[1] // may be undefined for legacy payments
    const addonRes = ADDON_RESOURCES[addonId]
    if (!addonRes) {
      console.error(`[check-crypto] Unknown addon ${addonId} for payment ${payment.id}`)
      return
    }

    // Update bot resource overrides — target specific bot or all
    const updateData: Record<string, number> = { resource_memory_mb: addonRes.memory_mb }
    if (addonRes.volume_gb) updateData.resource_volume_gb = addonRes.volume_gb

    if (botId) {
      await serviceClient.from('bots').update(updateData).eq('id', botId).eq('user_id', payment.user_id)
    } else {
      await serviceClient.from('bots').update(updateData).eq('user_id', payment.user_id)
    }

    // Track active addon on profile
    const { error } = await serviceClient.from('profiles')
      .update({ lifetime_addons: [addonId] })
      .eq('id', payment.user_id)
    if (error) console.error(`[check-crypto] Addon update failed for ${payment.id}:`, error)
    else console.info(`[check-crypto] Applied addon ${addonId} for user ${payment.user_id}${botId ? ` bot ${botId}` : ''}`)
  }
}

// ─── Single payment check ─────────────────────────────────────────────────────

async function checkPayment(
  serviceClient: Awaited<ReturnType<typeof createServiceClient>>,
  payment: {
    id: string
    user_id: string
    coin: string
    address: string
    amount_coin: number
    type: string
    credits: number | null
    plan: string | null
    months: number | null
  }
): Promise<'confirmed' | 'pending' | 'error'> {
  const route = routeCoin(payment.coin)
  if (!route) {
    console.warn(`[check-crypto] Unknown coin: ${payment.coin}`)
    return 'error'
  }

  let onChainBalance: bigint
  const expectedRaw = toRawAmount(payment.amount_coin, route.decimals)
  const minRequired = expectedRaw * 995n / 1000n // 0.5% tolerance

  try {
    if (route.walletType === 'evm') {
      const chain = EVM_CHAINS[route.network!]
      if (!chain) { console.warn(`[check-crypto] Unknown EVM network: ${route.network}`); return 'error' }

      if (route.token) {
        const contractAddress = ERC20_CONTRACTS[route.token]?.[route.network!]
        if (!contractAddress) {
          console.warn(`[check-crypto] No contract for ${route.token} on ${route.network}`)
          return 'error'
        }
        onChainBalance = await getEvmTokenBalance(chain.rpc, payment.address, contractAddress)
      } else {
        onChainBalance = await getEvmNativeBalance(chain.rpc, payment.address)
      }
    } else if (route.walletType === 'btc') {
      onChainBalance = await getBtcBalanceSatoshis(payment.address)
    } else if (route.walletType === 'sol') {
      if (route.token) {
        const mint = SOL_TOKEN_MINTS[route.token]
        if (!mint) { console.warn(`[check-crypto] No mint for SOL token: ${route.token}`); return 'error' }
        onChainBalance = await getSolTokenBalance(payment.address, mint)
      } else {
        onChainBalance = await getSolNativeBalance(payment.address)
      }
    } else {
      return 'error'
    }
  } catch (err) {
    console.error(`[check-crypto] Balance check failed for payment ${payment.id}:`, err)
    return 'error'
  }

  if (onChainBalance < minRequired) {
    return 'pending'
  }

  // Payment confirmed — update atomically (WHERE status='pending' prevents double-processing)
  const { error: updateError } = await serviceClient
    .from('crypto_payments')
    .update({ status: 'confirmed', confirmed_at: new Date().toISOString() })
    .eq('id', payment.id)
    .eq('status', 'pending')

  if (updateError) {
    console.warn(`[check-crypto] Could not mark ${payment.id} as confirmed:`, updateError.message)
    return 'error'
  }

  await applyPayment(serviceClient, payment)
  return 'confirmed'
}

// ─── POST /api/cron/check-crypto-payments ────────────────────────────────────

export async function POST(request: Request) {
  if (!isAuthorized(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const serviceClient = await createServiceClient()
  const now = new Date()

  // Expire timed-out payments
  await serviceClient
    .from('crypto_payments')
    .update({ status: 'failed' })
    .eq('status', 'pending')
    .lte('expires_at', now.toISOString())

  // Fetch all active pending payments
  const { data: payments, error: fetchError } = await serviceClient
    .from('crypto_payments')
    .select('id, user_id, coin, address, amount_coin, type, credits, plan, months')
    .eq('status', 'pending')
    .gt('expires_at', now.toISOString())

  if (fetchError) {
    console.error('[check-crypto] Failed to fetch pending payments:', fetchError)
    return NextResponse.json({ error: 'DB error' }, { status: 500 })
  }

  if (!payments || payments.length === 0) {
    return NextResponse.json({ checked: 0, confirmed: 0 })
  }

  // Check all payments in parallel
  const results = await Promise.allSettled(
    payments.map(p => checkPayment(serviceClient, p))
  )

  const confirmed = results.filter(r => r.status === 'fulfilled' && r.value === 'confirmed').length
  const errors = results.filter(r => r.status === 'rejected' || (r.status === 'fulfilled' && r.value === 'error')).length

  console.info(`[check-crypto] ${payments.length} checked, ${confirmed} confirmed, ${errors} errors`)
  return NextResponse.json({ checked: payments.length, confirmed, errors })
}
