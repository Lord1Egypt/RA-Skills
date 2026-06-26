'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui'
import { Loader2, Copy, Check, X, Bitcoin } from 'lucide-react'

interface CryptoTarget {
  type: 'credits' | 'plan' | 'addon'
  packId?: string
  plan?: string
  months?: number
  addonId?: string
  botId?: string
  label: string
  amountUsd: number
}

interface CryptoPaymentModalProps {
  target: CryptoTarget
  onClose: () => void
}

interface TokenDef {
  id: string        // coin ID (e.g. 'polygon/usdc', 'btc')
  label: string     // USDC, USDT, ETH, etc.
}

interface ChainDef {
  id: string
  name: string
  icon: string
  fee: string
  walletType: 'evm' | 'btc' | 'sol'
  tokens: TokenDef[]
}

// Quick-pick recommended options shown prominently at the top
const QUICK_PICKS = [
  { id: 'polygon/usdc', label: 'USDC · Polygon', fee: '~$0.001', recommended: true },
  { id: 'polygon/usdt', label: 'USDT · Polygon', fee: '~$0.001' },
]

// All chains — EVM chains use same wallet; others use dedicated env vars
const CHAINS: ChainDef[] = [
  {
    id: 'polygon', name: 'Polygon', icon: '🟣', fee: '~$0.001', walletType: 'evm',
    tokens: [{ id: 'polygon/usdc', label: 'USDC' }, { id: 'polygon/usdt', label: 'USDT' }, { id: 'matic', label: 'MATIC' }],
  },
  {
    id: 'base', name: 'Base', icon: '🔵', fee: '~$0.01', walletType: 'evm',
    tokens: [{ id: 'base/usdc', label: 'USDC' }, { id: 'base/eth', label: 'ETH' }],
  },
  {
    id: 'arbitrum', name: 'Arbitrum', icon: '🔵', fee: '~$0.05', walletType: 'evm',
    tokens: [{ id: 'arb/usdc', label: 'USDC' }, { id: 'arb/usdt', label: 'USDT' }, { id: 'arb/eth', label: 'ETH' }],
  },
  {
    id: 'optimism', name: 'Optimism', icon: '🔴', fee: '~$0.05', walletType: 'evm',
    tokens: [{ id: 'op/usdc', label: 'USDC' }, { id: 'op/eth', label: 'ETH' }],
  },
  {
    id: 'solana', name: 'Solana', icon: '◎', fee: '~$0.001', walletType: 'sol',
    tokens: [{ id: 'sol/usdc', label: 'USDC' }, { id: 'sol/usdt', label: 'USDT' }, { id: 'sol', label: 'SOL' }],
  },
  {
    id: 'bnb', name: 'BNB Chain', icon: '🟡', fee: '~$0.05', walletType: 'evm',
    tokens: [{ id: 'bep20/usdc', label: 'USDC' }, { id: 'bep20/usdt', label: 'USDT' }, { id: 'bnb', label: 'BNB' }],
  },
  {
    id: 'ethereum', name: 'Ethereum', icon: '⬡', fee: '~$2–5', walletType: 'evm',
    tokens: [{ id: 'eth/usdc', label: 'USDC' }, { id: 'eth/usdt', label: 'USDT' }, { id: 'eth/dai', label: 'DAI' }, { id: 'eth', label: 'ETH' }],
  },
  {
    id: 'avalanche', name: 'Avalanche', icon: '🔺', fee: '~$0.10', walletType: 'evm',
    tokens: [{ id: 'avax/usdc', label: 'USDC' }, { id: 'avax', label: 'AVAX' }],
  },
  {
    id: 'bitcoin', name: 'Bitcoin', icon: '₿', fee: '~$5–20', walletType: 'btc',
    tokens: [{ id: 'btc', label: 'BTC' }],
  },
]

type Step = 'select-coin' | 'payment' | 'confirmed'

function useCountdown(expiresAt: string | null) {
  const [secondsLeft, setSecondsLeft] = useState<number>(0)

  useEffect(() => {
    if (!expiresAt) return
    const calc = () => Math.max(0, Math.floor((new Date(expiresAt).getTime() - Date.now()) / 1000))
    setSecondsLeft(calc())
    const interval = setInterval(() => setSecondsLeft(calc()), 1000)
    return () => clearInterval(interval)
  }, [expiresAt])

  const mm = String(Math.floor(secondsLeft / 60)).padStart(2, '0')
  const ss = String(secondsLeft % 60).padStart(2, '0')
  return { display: `${mm}:${ss}`, expired: secondsLeft === 0 }
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false)
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch { /* ignore */ }
  }
  return (
    <button onClick={handleCopy} className="inline-flex items-center gap-1 text-xs text-primary hover:text-primary/80 transition-colors ml-2">
      {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
      {copied ? 'Copied' : 'Copy'}
    </button>
  )
}

export function CryptoPaymentModal({ target, onClose }: CryptoPaymentModalProps) {
  const router = useRouter()
  const [step, setStep] = useState<Step>('select-coin')
  const [selectedCoin, setSelectedCoin] = useState<string>('polygon/usdc')
  const [expandedChain, setExpandedChain] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Payment data from API
  const [paymentId, setPaymentId] = useState<string | null>(null)
  const [address, setAddress] = useState<string | null>(null)
  const [amountCoin, setAmountCoin] = useState<number | null>(null)
  const [coinLabel, setCoinLabel] = useState<string>('')
  const [expiresAt, setExpiresAt] = useState<string | null>(null)
  const [txHash, setTxHash] = useState<string | null>(null)

  const { display: countdown, expired: timerExpired } = useCountdown(expiresAt)

  const pollStatus = useCallback(async () => {
    if (!paymentId) return
    try {
      const res = await fetch(`/api/billing/crypto-checkout/${paymentId}/status`)
      if (!res.ok) return
      const data = await res.json()
      if (data.status === 'confirmed') {
        setTxHash(data.txHash ?? null)
        setStep('confirmed')
      } else if (data.status === 'failed') {
        setError('Payment failed or expired. Please start a new payment.')
        setStep('select-coin')
      }
    } catch { /* ignore */ }
  }, [paymentId])

  useEffect(() => {
    if (step !== 'payment' || !paymentId) return
    const interval = setInterval(pollStatus, 10_000)
    return () => clearInterval(interval)
  }, [step, paymentId, pollStatus])

  const handleInitiatePayment = async () => {
    setLoading(true)
    setError(null)
    try {
      const body: Record<string, unknown> = { type: target.type, coin: selectedCoin }
      if (target.type === 'credits') body.packId = target.packId
      if (target.type === 'plan') {
        body.plan = target.plan
        if (target.months) body.months = target.months
      }
      if (target.type === 'addon') {
        body.addonId = target.addonId
        if (target.botId) body.botId = target.botId
      }

      const res = await fetch('/api/billing/crypto-checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed to create payment')

      // Find coin label from chains
      let label = selectedCoin.split('/').pop()?.toUpperCase() ?? selectedCoin
      for (const chain of CHAINS) {
        const token = chain.tokens.find(t => t.id === selectedCoin)
        if (token) { label = `${token.label} (${chain.name})`; break }
      }

      setPaymentId(data.paymentId)
      setAddress(data.address)
      setAmountCoin(data.amount_coin)
      setCoinLabel(label)
      setExpiresAt(data.expires_at)
      setStep('payment')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleConfirmedClose = () => {
    router.refresh()
    onClose()
  }

  const [qrDataUrl, setQrDataUrl] = useState<string | null>(null)
  useEffect(() => {
    if (!address) { setQrDataUrl(null); return }
    import('qrcode').then(QRCode => {
      QRCode.toDataURL(address, { width: 200, margin: 1, color: { dark: '#000000', light: '#ffffff' } })
        .then(url => setQrDataUrl(url))
        .catch(() => setQrDataUrl(null))
    })
  }, [address])

  const isQuickPick = QUICK_PICKS.some(q => q.id === selectedCoin) && expandedChain === null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="bg-background rounded-xl shadow-xl w-full max-w-md relative">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b">
          <div className="flex items-center gap-2">
            <Bitcoin className="h-5 w-5 text-amber-500" />
            <h2 className="font-semibold">Pay with Crypto</h2>
          </div>
          <button onClick={step === 'confirmed' ? handleConfirmedClose : onClose} className="text-muted-foreground hover:text-foreground transition-colors">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="p-5">
          {/* Step 1 — Select coin */}
          {step === 'select-coin' && (
            <>
              <p className="text-sm text-muted-foreground mb-4">
                Paying <span className="font-semibold text-foreground">${target.amountUsd.toFixed(2)}</span> for {target.label}.
              </p>

              {/* Quick picks */}
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">Quick picks</p>
              <div className="grid grid-cols-2 gap-2 mb-5">
                {QUICK_PICKS.map(pick => (
                  <button
                    key={pick.id}
                    onClick={() => { setSelectedCoin(pick.id); setExpandedChain(null) }}
                    className={`relative flex flex-col items-start p-3 rounded-lg border text-left transition-colors ${
                      isQuickPick && selectedCoin === pick.id
                        ? 'border-primary bg-primary/5'
                        : 'border-border hover:border-primary/50'
                    }`}
                  >
                    {pick.recommended && (
                      <span className="absolute -top-2 left-2 text-xs bg-green-500 text-white px-1.5 py-0.5 rounded">Best</span>
                    )}
                    <span className="font-medium text-sm">🟣 {pick.label}</span>
                    <span className="text-xs text-muted-foreground mt-0.5">Fee: {pick.fee}</span>
                  </button>
                ))}
              </div>

              {/* Chain picker */}
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">Choose a chain</p>
              <div className="max-h-64 overflow-y-auto space-y-1.5 pr-0.5">
                {CHAINS.map(chain => {
                  const isExpanded = expandedChain === chain.id
                  const hasSelectedToken = chain.tokens.some(t => t.id === selectedCoin)
                  const isActive = isExpanded || (hasSelectedToken && expandedChain === chain.id)
                  return (
                    <div key={chain.id}>
                      {/* Chain row */}
                      <button
                        onClick={() => setExpandedChain(isExpanded ? null : chain.id)}
                        className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-lg border text-left transition-colors ${
                          isActive
                            ? 'border-primary bg-primary/5'
                            : 'border-border hover:border-primary/40'
                        }`}
                      >
                        <span className="text-base leading-none">{chain.icon}</span>
                        <span className="flex-1 font-medium text-sm">{chain.name}</span>
                        <span className="text-xs text-muted-foreground">{chain.fee}</span>
                        <span className={`text-xs transition-transform ${isExpanded ? 'rotate-180' : ''}`}>▾</span>
                      </button>

                      {/* Token strip */}
                      {isExpanded && (
                        <div className="flex gap-1.5 flex-wrap mt-1.5 ml-3 mb-1">
                          {chain.tokens.map(token => (
                            <button
                              key={token.id}
                              onClick={() => setSelectedCoin(token.id)}
                              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                                selectedCoin === token.id
                                  ? 'bg-primary text-primary-foreground border-primary'
                                  : 'bg-background border-border hover:border-primary'
                              }`}
                            >
                              {token.label}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>

              {error && <p className="text-sm text-destructive mt-3">{error}</p>}

              <Button className="w-full mt-4" onClick={handleInitiatePayment} disabled={loading}>
                {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                Continue
              </Button>
            </>
          )}

          {/* Step 2 — Send payment */}
          {step === 'payment' && address && amountCoin !== null && (
            <>
              <div className="flex items-center justify-between mb-4">
                <p className="text-sm text-muted-foreground">Send exactly to this address. Expires in:</p>
                <span className={`font-mono text-sm font-semibold ${timerExpired ? 'text-destructive' : 'text-foreground'}`}>
                  {timerExpired ? 'EXPIRED' : countdown}
                </span>
              </div>

              {timerExpired && (
                <div className="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-sm text-destructive">
                  This payment window has expired. Please start a new payment.
                </div>
              )}

              {qrDataUrl && (
                <div className="flex justify-center mb-4">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={qrDataUrl} alt="Payment QR code" width={200} height={200} className="rounded-lg border" />
                </div>
              )}

              <div className="bg-muted rounded-lg p-3 mb-3">
                <p className="text-xs text-muted-foreground mb-1">Amount (exact)</p>
                <div className="flex items-center justify-between">
                  <span className="font-mono text-sm font-semibold break-all">{amountCoin} {coinLabel}</span>
                  <CopyButton text={String(amountCoin)} />
                </div>
              </div>

              <div className="bg-muted rounded-lg p-3 mb-4">
                <p className="text-xs text-muted-foreground mb-1">Deposit address</p>
                <div className="flex items-start justify-between gap-2">
                  <span className="font-mono text-xs break-all">{address}</span>
                  <CopyButton text={address} />
                </div>
              </div>

              <p className="text-xs text-muted-foreground text-center">Monitoring the blockchain — this page updates automatically.</p>
              <div className="flex items-center justify-center gap-2 mt-3">
                <Loader2 className="h-3.5 w-3.5 animate-spin text-muted-foreground" />
                <span className="text-xs text-muted-foreground">Waiting for payment…</span>
              </div>
            </>
          )}

          {/* Step 3 — Confirmed */}
          {step === 'confirmed' && (
            <div className="text-center py-4">
              <div className="w-14 h-14 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
                <Check className="h-7 w-7 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Payment Confirmed!</h3>
              <p className="text-sm text-muted-foreground mb-4">Your {target.label} has been applied to your account.</p>
              {txHash && <p className="text-xs text-muted-foreground font-mono break-all mb-4">Tx: {txHash}</p>}
              <Button className="w-full" onClick={handleConfirmedClose}>Done</Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
