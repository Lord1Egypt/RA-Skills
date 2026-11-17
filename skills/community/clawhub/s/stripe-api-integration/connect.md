# Connect — Marketplaces and Platforms

**Read `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`** (or its box) before writing any Connect call: the charge type already in production determines fees, liability and reporting, and changing it later is a migration, not a parameter.

**Contents:** [Charge Type Decides Everything](#charge-type-decides-everything) · [Connect Account Types](#connect-account-types) · [Create Connected Account](#create-connected-account) · [Account Onboarding](#account-onboarding) · [Payment Flows](#payment-flows) · [Application Fees](#application-fees) · [Payouts to Connected Accounts](#payouts-to-connected-accounts) · [Refunds with Connect](#refunds-with-connect) · [Express Dashboard](#express-dashboard) · [Account Updates](#account-updates) · [Connect Webhooks](#connect-webhooks) · [Common Patterns](#common-patterns) · [Negative Balances and Seller Risk](#negative-balances-and-seller-risk)

## Charge Type Decides Everything

| | Direct charge | Destination charge | Separate charges and transfers |
|---|---|---|---|
| Charge is created on | The connected account | The platform | The platform |
| Funds land | Seller's balance | Platform balance, then transferred | Platform balance, transferred later or to several sellers |
| Statement descriptor | Seller's | Platform's | Platform's |
| Dispute liability | The seller | **The platform** | **The platform** |
| Processing fee paid by | The seller | The platform | The platform |
| Fits | Sellers with their own brand and their own customers | A platform that owns the customer relationship | One payment split between several sellers, or money held before release |

Pick from liability and brand, not from which is easiest to write. The platform absorbing dispute liability is a real cost line that has to be priced into the application fee (`disputes.md`), and the descriptor the buyer sees is the single biggest driver of `unrecognized` disputes.

Operational corollaries: acting on a connected account means the `Stripe-Account` header, not a different key; idempotency keys are scoped per account; and platform and connected balances reconcile separately (`reconciliation.md`).

## Connect Account Types

| Type | Control | Onboarding | Payouts | Use Case |
|------|---------|------------|---------|----------|
| Standard | Low | Stripe-hosted | Direct to account | Independent businesses |
| Express | Medium | Stripe-hosted | Platform controls | Gig workers, sellers |
| Custom | Full | Build your own | Platform controls | White-label platforms |

## Create Connected Account

### Express Account
```bash
curl https://api.stripe.com/v1/accounts \
  -u "$STRIPE_SECRET_KEY:" \
  -d "type=express" \
  -d "country=US" \
  -d "email=seller@example.com" \
  -d "capabilities[card_payments][requested]=true" \
  -d "capabilities[transfers][requested]=true"
```

### Standard Account
```bash
curl https://api.stripe.com/v1/accounts \
  -u "$STRIPE_SECRET_KEY:" \
  -d "type=standard" \
  -d "country=US" \
  -d "email=merchant@example.com"
```

### Custom Account
```bash
curl https://api.stripe.com/v1/accounts \
  -u "$STRIPE_SECRET_KEY:" \
  -d "type=custom" \
  -d "country=US" \
  -d "email=user@example.com" \
  -d "capabilities[card_payments][requested]=true" \
  -d "capabilities[transfers][requested]=true" \
  -d "business_type=individual"
```

## Account Onboarding

### Create Account Link (Express/Custom)
```bash
curl https://api.stripe.com/v1/account_links \
  -u "$STRIPE_SECRET_KEY:" \
  -d "account=acct_XXX" \
  -d "refresh_url=https://example.com/reauth" \
  -d "return_url=https://example.com/return" \
  -d "type=account_onboarding"
```

### Check Onboarding Status
```bash
curl https://api.stripe.com/v1/accounts/acct_XXX \
  -u "$STRIPE_SECRET_KEY:"

# Check: charges_enabled, payouts_enabled, requirements
```

## Payment Flows

### Direct Charge (Funds go to connected account)
```bash
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -H "Stripe-Account: acct_XXX" \
  -d "amount=10000" \
  -d "currency=usd" \
  -d "application_fee_amount=1000"
```

### Destination Charge (Funds go to platform, then transferred)
```bash
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=10000" \
  -d "currency=usd" \
  -d "transfer_data[destination]=acct_XXX" \
  -d "transfer_data[amount]=9000"
```

### Separate Charges and Transfers
```bash
# 1. Charge customer
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=10000" \
  -d "currency=usd"

# 2. Transfer to connected account
curl https://api.stripe.com/v1/transfers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=9000" \
  -d "currency=usd" \
  -d "destination=acct_XXX" \
  -d "source_transaction=ch_XXX"
```

## Application Fees

### On Direct Charge
```bash
-d "application_fee_amount=1000"
```

### On Destination Charge
```bash
-d "transfer_data[amount]=9000"  # Platform keeps 10000-9000 = 1000
```

## Payouts to Connected Accounts

### Create Payout (for Express/Custom)
```bash
curl https://api.stripe.com/v1/payouts \
  -u "$STRIPE_SECRET_KEY:" \
  -H "Stripe-Account: acct_XXX" \
  -d "amount=10000" \
  -d "currency=usd"
```

### Check Account Balance
```bash
curl https://api.stripe.com/v1/balance \
  -u "$STRIPE_SECRET_KEY:" \
  -H "Stripe-Account: acct_XXX"
```

## Refunds with Connect

### Refund Direct Charge (Refund from connected account)
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -H "Stripe-Account: acct_XXX" \
  -d "charge=ch_XXX"
```

### Refund Destination Charge (Reverse transfer too)
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "charge=ch_XXX" \
  -d "reverse_transfer=true"
```

### Refund Application Fee
```bash
curl https://api.stripe.com/v1/refunds \
  -u "$STRIPE_SECRET_KEY:" \
  -d "charge=ch_XXX" \
  -d "refund_application_fee=true"
```

## Express Dashboard

### Create Login Link
```bash
curl https://api.stripe.com/v1/accounts/acct_XXX/login_links \
  -u "$STRIPE_SECRET_KEY:"
```

Redirects to Express dashboard where sellers can:
- View balance and payouts
- Update banking info
- See transaction history

## Account Updates

### Update Connected Account
```bash
curl https://api.stripe.com/v1/accounts/acct_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "business_profile[url]=https://seller.example.com" \
  -d "business_profile[mcc]=5734"
```

### Delete Connected Account
```bash
curl -X DELETE https://api.stripe.com/v1/accounts/acct_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

## Connect Webhooks

| Event | When | Action |
|-------|------|--------|
| `account.updated` | Account status changes | Check charges_enabled |
| `account.application.authorized` | OAuth authorized | Store account ID |
| `account.application.deauthorized` | OAuth revoked | Disable features |
| `payout.paid` | Payout sent | Notify seller |
| `payout.failed` | Payout failed | Alert and retry |

## Common Patterns

### Split Payment (Multiple Sellers)
```bash
# Pay to platform, then transfer to multiple accounts
curl https://api.stripe.com/v1/payment_intents \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=10000" \
  -d "currency=usd"

# Transfer to Seller A
curl https://api.stripe.com/v1/transfers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=4000" \
  -d "destination=acct_SELLER_A" \
  -d "source_transaction=ch_XXX"

# Transfer to Seller B
curl https://api.stripe.com/v1/transfers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=5000" \
  -d "destination=acct_SELLER_B" \
  -d "source_transaction=ch_XXX"

# Platform keeps 1000
```

### Hold and Release
```bash
# Create transfer with manual payout timing
curl https://api.stripe.com/v1/accounts/acct_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "settings[payouts][schedule][delay_days]=manual"

# Later, trigger payout
curl https://api.stripe.com/v1/payouts \
  -u "$STRIPE_SECRET_KEY:" \
  -H "Stripe-Account: acct_XXX" \
  -d "amount=5000" \
  -d "currency=usd"
```

---

## Onboarding Is a Treadmill, Not a Form

- Requirements differ by country, business type and volume, and they change. `requirements[currently_due]`, `eventually_due` and `past_due` on the account object are the contract: read them and surface exactly what is missing, rather than asking sellers for everything up front.
- `charges_enabled` and `payouts_enabled` are the only reliable readiness flags. An account that finished the onboarding flow is not necessarily either.
- Hosted onboarding hands the treadmill to Stripe; owning the UI means owning every new requirement in every new country. Teams that are not in the compliance business hand it over (`SKILL.md`, Where Experts Disagree).
- The newer controller-based account configuration expresses who owns fees, losses and the dashboard directly; the older Standard, Express and Custom labels map onto the same choices and still appear everywhere. Whichever vocabulary the account uses, the underlying questions are: who pays the fee, who eats the loss, and whose dashboard the seller logs into.
- An account link expires quickly and is single-use — generate it when the seller clicks, never in advance.

## Negative Balances and Seller Risk

A refund or a dispute after the seller has been paid out leaves their balance negative, and that is a receivable, not a Stripe problem. Decide before launch: hold a rolling reserve, delay payouts for new sellers, or absorb it on the platform. Platforms that decide this after the first fraudulent seller decide it expensively.

Payout timing to sellers is a product decision too: instant costs a percentage, standard is free and slower, and manual gives you the release moment as a lever against fraud.

---

**Write in the same turn**: the charge type, the application fee model and who holds dispute liability go to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`, and the reasoning to `artifacts/decision-<charge-type>.md` with its `## Boxes` line. Each connected seller who is a named person or company goes to `~/Clawic/data/contacts/contacts.md` and is referenced here by name only — never duplicate the seller record inside this skill's box. A seller loss that the platform absorbed is a row in `incidents/<year>.md`.
