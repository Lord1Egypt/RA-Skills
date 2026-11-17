# AGENT CASH: Risk Control & Chargeback Mitigation Strategy

**Date:** 2026-02-24
**Source:** Strategic review session

## 1. Core Model

AGENT CASH is a user-approved payment gate for digital unlocks.
The platform acts as Merchant of Record for card-based transactions under a $25 cap.

The goal is not to eliminate refunds.
The goal is to minimize chargebacks and protect the processing account.

## 2. Refund Philosophy

- Offer no-questions-asked refunds.
- Refund quickly (ideally within 24 hours of request).
- Make refund easier than filing a bank dispute.
- Do not fight small disputes.
- Optimize for low dispute rate, not maximum revenue retention.

**Key metric:** Disputes / Total Transactions must stay below ~0.9%.

## 3. Double-Loss Protection (Refund + Chargeback)

Before issuing refund:
- Check if dispute already exists.
- If dispute exists ... handle through dispute flow.
- If no dispute ... refund immediately.

**Goal:** Refund before dispute is filed to avoid double exposure.

## 4. Seller Risk Segmentation

AGENT CASH is not an open marketplace. It should operate as a curated, tiered network.

### Tier 0: Default / Unverified
- Very low transaction cap (e.g., $0.10-$0.25).
- Limited volume.
- Strict monitoring.

### Tier 1: Whitelisted / Verified
- Higher transaction cap (up to $25).
- Standard refund window (15-30 days).
- Expanded volume.
- Seller agreement required.

### Tier 2: High-Trust
- Higher limits.
- Preferred placement.
- Performance-based upgrade.

**Upgrade criteria:**
- Sustained low dispute rate.
- Good refund cooperation.
- Legitimate digital content.

## 5. Seller Vetting (Beta Model)

AGENT CASH launches as a limited beta.

**Seller requirements:**
- Application and manual review.
- Clear website and pricing.
- Digital product clarity.
- Agreement to refund cooperation.
- Acceptance of tiered risk structure.

Only approved domains are enabled. This prevents unknown sellers from spiking dispute rates.

## 6. Buyer Abuse Controls

To prevent serial refund/chargeback abuse:
- Require login or verified email.
- Track refunds per account/IP/device.
- Limit refund frequency.
- Monitor unusual patterns.
- Enforce velocity limits.

The goal is not to block legitimate refunds, but to stop systematic abuse.

## 7. Financial Risk Buffer

Maintain liquidity buffer equal to approximately 10-20% of projected monthly processing volume.

This covers:
- Refunds
- Dispute fees
- Temporary holds

Risk is modeled against gross transaction volume, not platform fee revenue.

## 8. Strategic Positioning

AGENT CASH is:
- Not a wallet.
- Not stored value.
- Not peer-to-peer.
- Not open financial infrastructure.

It is: **A curated micro-transaction unlock network for trusted digital sellers.**

The system mitigates chargeback risk through:
- Low transaction caps
- Proactive refunds
- Seller vetting
- Tiered limits
- Continuous dispute monitoring

## 9. Primary Risk Objective

The operational objective is:

**Protect the Stripe account by keeping dispute rate low and predictable.**

Everything else (refund generosity, tiering, vetting, caps) exists to support that objective.
