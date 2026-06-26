/**
 * Integration example — how to wire CryptoPaymentModal into a billing page.
 *
 * This shows three common use cases:
 *   1. Paying for a credit pack
 *   2. Upgrading to a paid plan
 *   3. Purchasing a one-time addon
 */
'use client'

import { useState } from 'react'
import { CryptoPaymentModal } from '@/components/dashboard/crypto-payment-modal'

// ── Example 1: Credit pack purchase ──────────────────────────────────────────

export function BuyCreditsButton() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>
        Buy 1,000 Credits — Pay with Crypto
      </button>

      {open && (
        <CryptoPaymentModal
          target={{
            type: 'credits',
            packId: '1000',        // must match a CREDIT_PACKS entry on the server
            label: '1,000 Credits',
            amountUsd: 10,
          }}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  )
}

// ── Example 2: Plan upgrade ───────────────────────────────────────────────────

export function UpgradeToPro() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>
        Upgrade to Pro — Pay with Crypto
      </button>

      {open && (
        <CryptoPaymentModal
          target={{
            type: 'plan',
            plan: 'pro',           // must match a PLANS entry on the server
            months: 1,             // omit for lifetime/one-time plans
            label: 'Pro Plan (1 month)',
            amountUsd: 29,
          }}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  )
}

// ── Example 3: One-time addon ─────────────────────────────────────────────────

export function BuyAddon({ botId }: { botId: string }) {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button onClick={() => setOpen(true)}>
        Add Memory Boost — $12.99
      </button>

      {open && (
        <CryptoPaymentModal
          target={{
            type: 'addon',
            addonId: 'memory_boost',  // must match validAddons on the server
            botId,                     // optional — scopes addon to specific resource
            label: 'Memory Boost',
            amountUsd: 12.99,
          }}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  )
}
