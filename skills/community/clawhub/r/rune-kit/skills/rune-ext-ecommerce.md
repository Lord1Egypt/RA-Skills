# rune-ext-ecommerce

> Rune L4 Skill | extension


# @rune/ecommerce

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

E-commerce codebases fail at the seams between systems: payment intents that succeed but order records that don't get created, inventory counts that go negative during flash sales, subscription proration that charges the wrong amount mid-cycle, tax calculations that use cart-time rates instead of checkout-time rates, carts that lose items when users sign in, and webhook handlers that process the same event twice. This pack addresses the full order lifecycle — storefront to payment to fulfillment — with patterns that handle the race conditions, state machines, and distributed system problems that every commerce platform eventually hits.

## Triggers

- Auto-trigger: when `shopify.app.toml`, `*.liquid`, `cart`, `checkout`, `stripe` in payment context, `inventory` schema detected
- `/rune shopify-dev` — audit Shopify theme or app architecture
- `/rune payment-integration` — set up or audit payment flows
- `/rune subscription-billing` — set up or audit recurring billing
- `/rune cart-system` — build or audit cart architecture
- `/rune inventory-mgmt` — audit inventory tracking and stock management
- `/rune order-management` — audit order lifecycle and fulfillment
- `/rune tax-compliance` — set up or audit tax calculation
- Called by `cook` (L1) when e-commerce project detected
- Called by `launch` (L1) when preparing storefront for production

## Skills Included

| Skill | Model | Description |
|-------|-------|-------------|
| [shopify-dev](skills/shopify-dev.md) | sonnet | Shopify theme, Hydrogen, app architecture — Liquid templates, Storefront API, metafields, webhook HMAC verification. |
| [payment-integration](skills/payment-integration.md) | sonnet | Stripe, 3DS, webhooks, fraud detection, multi-currency, Vietnamese gateways (SePay, VNPay, MoMo). |
| [subscription-billing](skills/subscription-billing.md) | sonnet | Trials, proration, dunning, plan changes mid-cycle, usage-based billing, cancellation flows. |
| [cart-system](skills/cart-system.md) | sonnet | Persistent carts, guest-to-auth merge, server-authoritative totals, coupon engine. |
| [inventory-mgmt](skills/inventory-mgmt.md) | sonnet | Atomic stock with optimistic locking, reservations, low-stock alerts, backorder handling. |
| [order-management](skills/order-management.md) | sonnet | State machine, fulfillment, refund/return flows, reconciliation, webhook fan-out. |
| [tax-compliance](skills/tax-compliance.md) | sonnet | Tax APIs, EU VAT reverse charge, digital goods tax, audit trail per order line item. |

## Common Workflows

| Workflow | Skills Involved | Description |
|----------|----------------|-------------|
| Full checkout | cart-system → tax-compliance → payment-integration → order-management | Complete purchase from cart to confirmation |
| Flash sale | inventory-mgmt → cart-system → payment-integration | High-concurrency stock control |
| Subscription signup | cart-system → payment-integration → subscription-billing | Free trial with payment method upfront |
| Plan upgrade | subscription-billing → payment-integration → tax-compliance | Mid-cycle upgrade with proration invoice |
| Order cancellation | order-management → inventory-mgmt → payment-integration | Cancel + release stock + issue refund |
| New market launch | tax-compliance → payment-integration (multi-currency) → shopify-dev | Localization, VAT, FX pricing |
| Fraud review | payment-integration (fraud patterns) → order-management | Risk scoring before order fulfilment |
| Product catalog | shopify-dev → inventory-mgmt | Variant structure + stock sync |

## Tech Stack Support

| Platform | Framework | Payment | Notes |
|----------|-----------|---------|-------|
| Shopify | Hydrogen 2.x (Remix) | Shopify Payments | Storefront + Admin API |
| Custom | Next.js 16 / SvelteKit | Stripe | Most flexible |
| Headless | Any frontend | Stripe / PayPal | API-first commerce |
| Medusa.js | Next.js | Stripe / PayPal | Open-source alternative |
| Saleor | React / Next.js | Stripe / Braintree | GraphQL-first |

## Connections

```
Calls → sentinel (L2): PCI compliance audit on payment code, webhook security
Calls → db (L2): schema design for orders, inventory, carts, subscriptions
Calls → perf (L2): audit checkout page load, cart update latency
Calls → verification (L3): run payment flow integration tests
Called By ← cook (L1): when e-commerce project detected
Called By ← launch (L1): pre-launch checkout verification
Called By ← review (L2): when payment or cart code under review
Called By ← ba (L2): requirements elicitation for e-commerce features
```

## Sharp Edges

| Failure Mode | Severity | Mitigation |
|---|---|---|
| Double charge from retried Payment Intent without idempotency key | CRITICAL | Derive idempotencyKey from `cartId-v${version}`, not timestamp; check for existing succeeded intent |
| Webhook signature fails because `req.body` is parsed JSON instead of raw bytes | CRITICAL | Use `express.raw({ type: 'application/json' })` for webhook route; verify with `req.body` as Buffer |
| Overselling during flash sale (stock goes negative) | CRITICAL | Use optimistic locking with version field; serializable isolation for high-contention items |
| Payment succeeded but order creation fails (money taken, no order record) | HIGH | Wrap in transaction; run reconciliation job matching payment intents to orders every hour |
| Same webhook processed twice creates duplicate orders | HIGH | Store `event.id` in database; check before processing; wrap in transaction |
| Guest cart items lost on login (separate cart created for auth user) | HIGH | Implement cart merge in auth callback; prefer server cart state over local |
| Subscription proration charges wrong amount on mid-cycle plan change | HIGH | Explicitly set `proration_behavior`; preview proration with `stripe.invoices.retrieveUpcoming` |
| Trial-to-paid conversion fails silently (no payment method on file) | HIGH | Require payment method at trial signup; set `missing_payment_method: 'cancel'` in trial settings |
| Tax calculated at cart time but rate changed by checkout (wrong amount charged) | MEDIUM | Recalculate tax at payment creation time using shipping address, not cart-add time |
| Liquid template outputs unescaped metafield content (XSS in Shopify theme) | HIGH | Always use `| escape` filter on user-generated metafield values |
| Cancelled order stock not returned to inventory | MEDIUM | Use order state machine with side effects — cancellation always triggers `releaseOrderReservations` |
| Reservation never expires for abandoned checkout (stock locked forever) | MEDIUM | Run reservation expiry job every 5 minutes; default reservation TTL = 15 minutes |
| Stolen card fraud passes payment but triggers chargeback later | HIGH | Apply fraud scoring before confirmation; hold high-risk orders for manual review |
| FX rate stale on multi-currency display — user sees wrong price | MEDIUM | Cache FX rates max 15 minutes; show rate timestamp to user; always charge in store base currency |

## Done When

- Checkout flow completes end-to-end: cart → tax → payment → order confirmation
- Subscription lifecycle handles trial → active → past_due → cancelled with proper dunning
- Inventory accurately tracks stock with no overselling under concurrent load
- Order state machine enforces valid transitions with side effects (stock release, refunds, notifications)
- Webhooks are idempotent, signature-verified, and handle all payment/subscription lifecycle events
- Tax calculated at checkout with audit trail stored per order line item
- Guest-to-authenticated cart merge works without data loss
- All prices, discounts, and coupons validated server-side
- Reconciliation job catches payment/order mismatches
- Fraud scoring applied to all orders; high-risk orders flagged for review
- Multi-currency display works with cached FX rates; charges always in base currency
- Structured report emitted for each skill invoked

## Cost Profile

~14,000–26,000 tokens per full pack run (all 7 skills). Individual skill: ~2,000–4,000 tokens. Sonnet default. Use haiku for detection scans; escalate to sonnet for payment flow, subscription lifecycle, and order state machine generation.

# cart-system

Shopping cart architecture — state management, persistent carts, guest checkout, coupon/discount engine, guest-to-auth cart merge.

#### Workflow

**Step 1 — Detect cart architecture**
Use Grep to find cart state: `cartStore`, `useCart`, `addToCart`, `localStorage.*cart`, `session.*cart`. Read cart-related components and API routes to understand: client vs server cart, persistence strategy, and discount handling.

**Step 2 — Audit cart integrity**
Check for:
- Cart total calculated client-side only (price manipulation — attacker changes localStorage price)
- No cart TTL (stale carts hold inventory reservations indefinitely)
- Missing guest-to-authenticated cart merge (items lost on login)
- Race conditions on concurrent cart updates (two tabs adding items, last write wins)
- Coupons validated client-side (attacker applies any discount code)
- No stock check at add-to-cart time (user adds 100 items, stock is 3)
- Cart stored in localStorage only (lost on device switch, no cross-device)

**Step 3 — Emit cart patterns**
Emit: server-authoritative cart with client cache, guest-to-auth merge flow, coupon validation middleware, and optimistic UI with server reconciliation.

#### Example

```typescript
// Server-authoritative cart with Zustand client cache
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartStore {
  items: CartItem[];
  cartId: string | null;
  addItem: (productId: string, variantId: string, qty: number) => Promise<void>;
  mergeGuestCart: (userId: string) => Promise<void>;
}

const useCart = create<CartStore>()(persist((set, get) => ({
  items: [], cartId: null,

  addItem: async (productId, variantId, qty) => {
    // Optimistic update (show item immediately)
    set(state => ({ items: [...state.items, { productId, variantId, qty, pending: true }] }));
    // Server reconciliation (validates stock, calculates price, applies discounts)
    const cart = await fetch('/api/cart/add', {
      method: 'POST',
      body: JSON.stringify({ cartId: get().cartId, productId, variantId, qty }),
    }).then(r => r.json());
    set({ items: cart.items, cartId: cart.id }); // server is source of truth
  },

  mergeGuestCart: async (userId) => {
    const { cartId } = get();
    if (!cartId) return;
    const merged = await fetch('/api/cart/merge', {
      method: 'POST', body: JSON.stringify({ guestCartId: cartId, userId }),
    }).then(r => r.json());
    set({ items: merged.items, cartId: merged.id });
  },
}), { name: 'cart-storage' }));

// Server — coupon validation (NEVER trust client)
app.post('/api/cart/apply-coupon', async (req, res) => {
  const { cartId, code } = req.body;
  const coupon = await couponService.validate(code); // checks: exists, not expired, usage limit
  if (!coupon) return res.status(400).json({ error: 'INVALID_COUPON' });

  const cart = await cartService.applyCoupon(cartId, coupon);
  // Recalculate totals server-side after discount
  res.json({ cart: cartService.calculateTotals(cart) });
});
```

---

# inventory-mgmt

Inventory management — stock tracking with optimistic locking, variant management, low stock alerts, backorder handling, reservation expiry.

#### Workflow

**Step 1 — Detect inventory model**
Use Grep to find stock-related code: `stock`, `inventory`, `quantity`, `variant`, `warehouse`, `sku`. Read schema files to understand: single vs multi-warehouse, variant structure, and reservation model.

**Step 2 — Audit stock integrity**
Check for:
- Stock decremented without transaction (oversell risk under concurrent load)
- No optimistic locking on concurrent updates (version field or `FOR UPDATE` lock)
- Inventory checked at cart-add but not at checkout (stale check — stock sold out between add and pay)
- Missing low-stock alerts (ops team discovers stockout from customer complaints)
- No reservation expiry for abandoned checkouts (stock locked forever)
- No backorder handling for out-of-stock items (zero stock = hard error vs queue)
- Flash sale race condition: 10 users checkout simultaneously with 3 items left = 7 oversold orders

**Step 3 — Emit inventory patterns**
Emit: atomic stock reservation with optimistic locking (version field), reservation expiry job for abandoned checkouts, low-stock alert trigger, and backorder queue.

#### Example

```typescript
// Atomic stock reservation with optimistic locking (Prisma)
async function reserveStock(variantId: string, qty: number, orderId: string) {
  const MAX_RETRIES = 3;
  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    const variant = await prisma.variant.findUniqueOrThrow({ where: { id: variantId } });

    if (variant.stock < qty && !variant.allowBackorder) {
      throw new Error(`Insufficient stock: ${variant.stock} available, ${qty} requested`);
    }

    try {
      const updated = await prisma.variant.update({
        where: { id: variantId, version: variant.version }, // optimistic lock
        data: {
          stock: { decrement: qty },
          version: { increment: 1 },
          reservations: { create: { orderId, qty, expiresAt: addMinutes(new Date(), 15) } },
        },
      });

      if (updated.stock <= updated.lowStockThreshold) {
        await alertService.trigger('LOW_STOCK', { variantId, currentStock: updated.stock });
      }
      return updated;
    } catch (e) {
      if (attempt === MAX_RETRIES - 1) throw new Error('Stock reservation failed: concurrent modification');
    }
  }
}

// Reservation expiry job — release stock from abandoned checkouts
async function releaseExpiredReservations() {
  const expired = await prisma.reservation.findMany({
    where: { expiresAt: { lt: new Date() }, status: 'PENDING' },
  });

  for (const reservation of expired) {
    await prisma.$transaction([
      prisma.variant.update({
        where: { id: reservation.variantId },
        data: { stock: { increment: reservation.qty } },
      }),
      prisma.reservation.update({
        where: { id: reservation.id },
        data: { status: 'EXPIRED' },
      }),
    ]);
  }
}

// Inventory webhook — push stock changes to external systems (3PL, ERP)
async function emitInventoryWebhook(variantId: string, newStock: number, event: string) {
  const variant = await prisma.variant.findUniqueOrThrow({
    where: { id: variantId },
    include: { product: true },
  });
  const payload = {
    event,                          // 'STOCK_UPDATED' | 'LOW_STOCK' | 'OUT_OF_STOCK'
    sku: variant.sku,
    variantId,
    productId: variant.productId,
    stock: newStock,
    threshold: variant.lowStockThreshold,
    timestamp: new Date().toISOString(),
  };
  // Fan-out to all registered webhook endpoints
  await webhookFanOut(payload, 'inventory.*');
}
```

---

# order-management

Order lifecycle — state machine, fulfillment workflows, refund/return flows, email notifications, reconciliation, webhook fan-out.

#### Workflow

**Step 1 — Detect order model**
Use Grep to find: `order`, `fulfillment`, `shipment`, `refund`, `return`, `order_status`, `OrderStatus`. Read schema to understand: order states, fulfillment model (self-ship, 3PL, dropship), and refund handling.

**Step 2 — Audit order lifecycle**
Check for:
- No explicit state machine: order status updated with raw string assignment (typos, invalid transitions)
- Missing reconciliation: payment succeeded but order creation failed (payment taken, no order)
- Partial fulfillment not handled: multi-item order with one item backordered
- Refund without inventory return: money refunded but stock not incremented back
- No email notifications on state transitions (customer has no visibility)
- Cancellation after partial fulfillment: must refund only unfulfilled items

**Step 3 — Emit order patterns**
Emit: typed state machine with valid transitions, reconciliation job, partial fulfillment handler, and refund flow with inventory return.

#### Example

```typescript
// Order state machine with valid transitions
type OrderStatus = 'pending' | 'confirmed' | 'processing' | 'partially_shipped' |
                   'shipped' | 'delivered' | 'cancelled' | 'refunded';

const VALID_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
  pending: ['confirmed', 'cancelled'],
  confirmed: ['processing', 'cancelled'],
  processing: ['partially_shipped', 'shipped', 'cancelled'],
  partially_shipped: ['shipped', 'cancelled'],
  shipped: ['delivered', 'refunded'],
  delivered: ['refunded'],
  cancelled: [],
  refunded: [],
};

async function transitionOrder(orderId: string, newStatus: OrderStatus) {
  const order = await prisma.order.findUniqueOrThrow({ where: { id: orderId } });
  const currentStatus = order.status as OrderStatus;

  if (!VALID_TRANSITIONS[currentStatus]?.includes(newStatus)) {
    throw new Error(`Invalid transition: ${currentStatus} → ${newStatus}`);
  }

  const updated = await prisma.$transaction(async (tx) => {
    const result = await tx.order.update({
      where: { id: orderId },
      data: {
        status: newStatus,
        statusHistory: { push: { from: currentStatus, to: newStatus, at: new Date() } },
      },
    });

    // Side effects per transition
    if (newStatus === 'cancelled') {
      await releaseOrderReservations(tx, orderId);
    }
    if (newStatus === 'refunded') {
      await processRefund(tx, orderId);
      await returnInventory(tx, orderId);
    }

    return result;
  });

  // Notifications (outside transaction — don't block on email)
  await notificationService.orderStatusChanged(updated);
  return updated;
}

// Reconciliation job — find payments without orders
async function reconcilePayments() {
  const recentIntents = await stripe.paymentIntents.list({
    created: { gte: Math.floor(Date.now() / 1000) - 3600 }, // last hour
    limit: 100,
  });

  for (const intent of recentIntents.data) {
    if (intent.status !== 'succeeded') continue;
    const cartId = intent.metadata.cartId;
    const order = await prisma.order.findFirst({ where: { paymentIntentId: intent.id } });

    if (!order) {
      // Payment succeeded but order not created — create it now
      await orderService.createFromIntent(intent);
      await alertService.trigger('RECONCILED_ORDER', { intentId: intent.id, cartId });
    }
  }
}

// Webhook fan-out for order status changes — notify 3PLs, ERPs, analytics
async function webhookFanOut(payload: Record<string, unknown>, topic: string) {
  const endpoints = await db.webhookEndpoint.findMany({
    where: { topics: { has: topic }, active: true },
  });
  await Promise.allSettled(
    endpoints.map(ep =>
      fetch(ep.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Rune-Signature': signPayload(payload, ep.secret),
          'X-Rune-Topic': topic,
          'X-Rune-Timestamp': String(Date.now()),
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(5000),
      }).catch(err => {
        // Log failure but don't throw — one bad endpoint shouldn't block others
        console.error(`Webhook delivery failed for ${ep.url}:`, err.message);
      })
    )
  );
}
```

---

# payment-integration

Payment integration — Stripe Payment Intents, 3D Secure, webhook handling, refunds, idempotency, PCI compliance, multi-currency, fraud detection, Vietnamese payment gateways (SePay, VNPay, MoMo).

#### Workflow

**Step 1 — Detect payment setup**
Use Grep to find `stripe`, `paypal`, `@stripe/stripe-js`, `@stripe/react-stripe-js`, payment-related endpoints. Read checkout handlers and webhook processors to understand: payment flow type (Payment Intents vs Checkout Sessions), webhook events handled, and error recovery.

**Step 2 — Audit payment security**
Check for:
- Missing idempotency keys on payment creation (double charges on retry)
- Webhook signature not verified (`stripe.webhooks.constructEvent` with `req.rawBody` — NOT parsed JSON body)
- Payment amount calculated client-side (price manipulation risk)
- No 3D Secure handling (`requires_action` status not handled in frontend)
- Secret keys in client bundle (check for `sk_live_` or `sk_test_` in frontend code)
- Missing failed payment recovery flow (no retry or dunning)
- Webhook processing not idempotent (same event processed twice creates duplicate orders)
- `req.body` used instead of `req.rawBody` for webhook signature verification (always fails)

**Step 3 — Emit robust payment flow**
Emit: server-side Payment Intent creation with idempotency, 3D Secure handling loop, comprehensive webhook handler with event deduplication, and refund flow with audit trail.

#### Example

```typescript
// Stripe Payment Intent — server-side, idempotent, 3DS-ready
import Stripe from 'stripe';
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

app.post('/api/checkout', async (req, res) => {
  const { cartId, paymentMethodId } = req.body;
  const cart = await cartService.getVerified(cartId); // server-side price calculation

  // Idempotency key derived from CART, not timestamp — prevents double charge on retry
  const idempotencyKey = `checkout-${cartId}-v${cart.version}`;

  const intent = await stripe.paymentIntents.create({
    amount: cart.totalInCents, // ALWAYS server-calculated
    currency: cart.currency,
    payment_method: paymentMethodId,
    confirm: true,
    return_url: `${process.env.APP_URL}/checkout/complete`,
    metadata: { cartId, userId: req.user.id },
    idempotencyKey,
  });

  if (intent.status === 'requires_action') {
    return res.json({ requiresAction: true, clientSecret: intent.client_secret });
  }
  if (intent.status === 'succeeded') {
    await orderService.create(cart, intent.id);
    return res.json({ success: true, orderId: intent.metadata.orderId });
  }
  res.status(400).json({ error: 'PAYMENT_FAILED' });
});

// Webhook — MUST use raw body for signature, deduplicate events
app.post('/api/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature']!;
  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return res.status(400).send('Signature verification failed');
  }

  // Deduplicate: check if event already processed
  const existing = await db.webhookEvent.findUnique({ where: { stripeEventId: event.id } });
  if (existing) return res.json({ received: true, duplicate: true });

  // Process within transaction
  await db.$transaction(async (tx) => {
    await tx.webhookEvent.create({ data: { stripeEventId: event.id, type: event.type } });

    if (event.type === 'payment_intent.succeeded') {
      const intent = event.data.object as Stripe.PaymentIntent;
      await orderService.confirmPayment(tx, intent.metadata.cartId, intent.id);
    }
  });

  res.json({ received: true });
});
```

#### Multi-Currency & Localization

```typescript
// Locale-aware price formatting — ALWAYS use Intl, never manual toFixed()
function formatPrice(amountInCents: number, currency: string, locale: string): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amountInCents / 100);
}

// Examples
formatPrice(1999, 'USD', 'en-US');  // $19.99
formatPrice(1999, 'EUR', 'de-DE');  // 19,99 €
formatPrice(1999, 'JPY', 'ja-JP');  // ¥1,999  (JPY has no minor units)

// Currency conversion with FX rate cache
interface FxRate { from: string; to: string; rate: number; fetchedAt: Date }

class FxService {
  private cache = new Map<string, FxRate>();

  async convert(amountInCents: number, from: string, to: string): Promise<number> {
    if (from === to) return amountInCents;
    const key = `${from}:${to}`;
    let rate = this.cache.get(key);

    // Refresh if stale (>15 min)
    if (!rate || Date.now() - rate.fetchedAt.getTime() > 15 * 60 * 1000) {
      const fresh = await this.fetchRate(from, to);
      rate = { from, to, rate: fresh, fetchedAt: new Date() };
      this.cache.set(key, rate);
    }
    return Math.round(amountInCents * rate.rate);
  }

  private async fetchRate(from: string, to: string): Promise<number> {
    // Use a reliable FX API (e.g., Frankfurter, Open Exchange Rates)
    const res = await fetch(`https://api.frankfurter.app/latest?from=${from}&to=${to}`);
    const data = await res.json();
    return data.rates[to];
  }
}

// Locale-aware pricing: show price in user's currency, charge in store's base currency
interface LocalizedPrice {
  displayAmount: string;   // "€18.45" — shown to user
  chargeAmount: number;    // 1999 cents USD — what actually gets charged
  currency: string;        // 'USD'
  displayCurrency: string; // 'EUR'
  exchangeRate: number;
}

async function getLocalizedPrice(
  amountInCents: number,
  storeCurrency: string,
  userLocale: string,
  userCurrency: string
): Promise<LocalizedPrice> {
  const fx = new FxService();
  const displayAmountInCents = await fx.convert(amountInCents, storeCurrency, userCurrency);
  return {
    displayAmount: formatPrice(displayAmountInCents, userCurrency, userLocale),
    chargeAmount: amountInCents,      // charge in store base currency
    currency: storeCurrency,
    displayCurrency: userCurrency,
    exchangeRate: displayAmountInCents / amountInCents,
  };
}
```

#### Vietnamese Payment Gateways (SePay, VNPay, MoMo, ZaloPay)

Vietnam market uses QR-based bank transfers and e-wallets instead of card payments. SePay is the simplest (webhook on bank transfer), VNPay is the most widely adopted gateway, MoMo/ZaloPay are e-wallet leaders.

**SePay — QR Bank Transfer (simplest integration)**

```typescript
// SePay: generate QR code for bank transfer, webhook on payment received
// Docs: https://my.sepay.vn/docs

interface SePayConfig {
  apiKey: string;
  bankAccount: string;  // your receiving bank account
  bankCode: string;     // e.g., 'MB', 'VCB', 'TCB', 'ACB'
  webhookSecret: string;
}

// Generate payment QR — user scans with banking app
async function createSePayQR(orderId: string, amountVND: number, config: SePayConfig) {
  // SePay uses structured transfer content for auto-matching
  const transferContent = `DH${orderId}`;  // prefix for order matching

  return {
    bankCode: config.bankCode,
    bankAccount: config.bankAccount,
    amount: amountVND,
    content: transferContent,
    // QR follows VietQR standard (NAPAS)
    qrUrl: `https://qr.sepay.vn/img?acc=${config.bankAccount}&bank=${config.bankCode}&amount=${amountVND}&des=${transferContent}`,
  };
}

// Webhook — SePay calls this when bank transfer is detected
app.post('/api/webhooks/sepay', async (req, res) => {
  // Verify webhook signature
  const signature = req.headers['x-sepay-signature'] as string;
  const payload = JSON.stringify(req.body);
  const expected = crypto.createHmac('sha256', process.env.SEPAY_WEBHOOK_SECRET!)
    .update(payload).digest('hex');

  if (signature !== expected) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  const { transferAmount, transferContent, transactionDate, id } = req.body;

  // Deduplicate
  const existing = await db.payment.findFirst({ where: { externalId: String(id) } });
  if (existing) return res.json({ success: true, duplicate: true });

  // Match order by transfer content (DH{orderId})
  const orderIdMatch = transferContent.match(/DH(\w+)/);
  if (!orderIdMatch) {
    console.error('SePay: unmatched transfer', { transferContent, id });
    return res.json({ success: true, matched: false });
  }

  await db.$transaction(async (tx) => {
    await tx.payment.create({
      data: {
        orderId: orderIdMatch[1],
        amount: transferAmount,
        method: 'BANK_TRANSFER',
        provider: 'sepay',
        externalId: String(id),
        paidAt: new Date(transactionDate),
      },
    });
    await tx.order.update({
      where: { id: orderIdMatch[1] },
      data: { status: 'PAID', paidAt: new Date(transactionDate) },
    });
  });

  res.json({ success: true });
});
```

**VNPay — Vietnam's largest payment gateway**

```typescript
// VNPay: redirect-based payment with HMAC-SHA512 signature
// Docs: https://sandbox.vnpayment.vn/apis/docs/huong-dan-tich-hop/

import crypto from 'crypto';
import qs from 'qs';

interface VNPayConfig {
  tmnCode: string;      // merchant code
  hashSecret: string;   // secret key
  vnpUrl: string;       // 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html' (sandbox)
  returnUrl: string;    // your callback URL
}

function createVNPayUrl(orderId: string, amountVND: number, ipAddr: string, config: VNPayConfig): string {
  const now = new Date();
  const createDate = now.toISOString().replace(/[-:T.Z]/g, '').slice(0, 14);

  const params: Record<string, string> = {
    vnp_Version: '2.1.0',
    vnp_Command: 'pay',
    vnp_TmnCode: config.tmnCode,
    vnp_Locale: 'vn',
    vnp_CurrCode: 'VND',
    vnp_TxnRef: orderId,
    vnp_OrderInfo: `Thanh toan don hang ${orderId}`,
    vnp_OrderType: 'other',
    vnp_Amount: String(amountVND * 100),  // VNPay uses smallest unit (x100)
    vnp_ReturnUrl: config.returnUrl,
    vnp_IpAddr: ipAddr,
    vnp_CreateDate: createDate,
  };

  // Sort params alphabetically — REQUIRED by VNPay
  const sortedParams = Object.keys(params).sort().reduce((acc, key) => {
    acc[key] = params[key];
    return acc;
  }, {} as Record<string, string>);

  const signData = qs.stringify(sortedParams, { encode: false });
  const hmac = crypto.createHmac('sha512', config.hashSecret);
  const signed = hmac.update(Buffer.from(signData, 'utf-8')).digest('hex');

  return `${config.vnpUrl}?${signData}&vnp_SecureHash=${signed}`;
}

// IPN (Instant Payment Notification) — VNPay server-to-server callback
app.get('/api/webhooks/vnpay-ipn', async (req, res) => {
  const vnpParams = { ...req.query } as Record<string, string>;
  const secureHash = vnpParams.vnp_SecureHash;
  delete vnpParams.vnp_SecureHash;
  delete vnpParams.vnp_SecureHashType;

  // Verify hash
  const sortedParams = Object.keys(vnpParams).sort().reduce((acc, key) => {
    acc[key] = vnpParams[key];
    return acc;
  }, {} as Record<string, string>);

  const signData = qs.stringify(sortedParams, { encode: false });
  const expectedHash = crypto.createHmac('sha512', process.env.VNPAY_HASH_SECRET!)
    .update(Buffer.from(signData, 'utf-8')).digest('hex');

  if (secureHash !== expectedHash) {
    return res.json({ RspCode: '97', Message: 'Invalid signature' });
  }

  const orderId = vnpParams.vnp_TxnRef;
  const responseCode = vnpParams.vnp_ResponseCode;

  if (responseCode === '00') {
    await orderService.confirmPayment(orderId, vnpParams.vnp_TransactionNo);
    return res.json({ RspCode: '00', Message: 'Confirm Success' });
  }

  await orderService.failPayment(orderId, responseCode);
  res.json({ RspCode: '00', Message: 'Confirm Success' });  // always return 00 to VNPay
});
```

**MoMo — E-wallet payment**

```typescript
// MoMo: QR or app-switch payment
// Docs: https://developers.momo.vn/v3/docs/payment/api/

interface MoMoConfig {
  partnerCode: string;
  accessKey: string;
  secretKey: string;
  endpoint: string;  // 'https://test-payment.momo.vn/v2/gateway/api/create'
  redirectUrl: string;
  ipnUrl: string;
}

async function createMoMoPayment(orderId: string, amountVND: number, config: MoMoConfig) {
  const requestId = `${config.partnerCode}-${Date.now()}`;
  const orderInfo = `Thanh toan don hang ${orderId}`;
  const extraData = '';  // base64 encoded extra data

  // HMAC SHA256 signature — order of fields matters!
  const rawSignature = [
    `accessKey=${config.accessKey}`,
    `amount=${amountVND}`,
    `extraData=${extraData}`,
    `ipnUrl=${config.ipnUrl}`,
    `orderId=${orderId}`,
    `orderInfo=${orderInfo}`,
    `partnerCode=${config.partnerCode}`,
    `redirectUrl=${config.redirectUrl}`,
    `requestId=${requestId}`,
    `requestType=payWithMethod`,
  ].join('&');

  const signature = crypto.createHmac('sha256', config.secretKey)
    .update(rawSignature).digest('hex');

  const response = await fetch(config.endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      partnerCode: config.partnerCode,
      accessKey: config.accessKey,
      requestId,
      amount: amountVND,
      orderId,
      orderInfo,
      redirectUrl: config.redirectUrl,
      ipnUrl: config.ipnUrl,
      extraData,
      requestType: 'payWithMethod',
      signature,
      lang: 'vi',
    }),
  });

  const data = await response.json();
  return { payUrl: data.payUrl, qrCodeUrl: data.qrCodeUrl, deeplink: data.deeplink };
}
```

**Sharp Edges — VN Payment Gotchas:**
- SePay: transfer content MUST be exact match — users sometimes add extra text → payment not auto-matched. Always show exact content to copy.
- VNPay: `vnp_Amount` is multiplied by 100 (not cents — VND has no decimals). Common bug: double-multiplying.
- VNPay: ALWAYS return `RspCode: '00'` to IPN even on failure — otherwise VNPay retries indefinitely.
- MoMo: signature field order is strict — wrong order = invalid signature. Copy exact order from docs.
- ZaloPay: similar to MoMo but uses HMAC-SHA256 with different field ordering. Check docs at `https://docs.zalopay.vn/`.
- All VN gateways: amounts are in VND (integer, no decimals). Never use floating point for VND.
- Sandbox environments often have rate limits and expire — test with real small amounts (10,000 VND) before go-live.

#### Fraud Detection

```typescript
// Risk scoring before order fulfilment
interface FraudSignals {
  ipAddress: string;
  userAgent: string;
  deviceFingerprint: string;
  email: string;
  billingCountry: string;
  shippingCountry: string;
  orderAmountCents: number;
  isFirstOrder: boolean;
}

interface RiskScore {
  score: number;       // 0–100, higher = riskier
  action: 'allow' | 'review' | 'block';
  reasons: string[];
}

async function scoreFraudRisk(signals: FraudSignals): Promise<RiskScore> {
  const reasons: string[] = [];
  let score = 0;

  // Velocity check — same IP, multiple orders in short window
  const recentOrdersFromIp = await db.order.count({
    where: { ipAddress: signals.ipAddress, createdAt: { gte: new Date(Date.now() - 3600_000) } },
  });
  if (recentOrdersFromIp >= 3) { score += 30; reasons.push('HIGH_VELOCITY_IP'); }

  // Card BIN country mismatch
  if (signals.billingCountry !== signals.shippingCountry) {
    score += 15; reasons.push('BILLING_SHIPPING_MISMATCH');
  }

  // High-value first order — common pattern for stolen cards
  if (signals.isFirstOrder && signals.orderAmountCents > 50000) {
    score += 25; reasons.push('HIGH_VALUE_FIRST_ORDER');
  }

  // Email domain is disposable (temp-mail.org, mailinator.com, etc.)
  const domain = signals.email.split('@')[1];
  const isDisposable = await disposableEmailService.check(domain);
  if (isDisposable) { score += 20; reasons.push('DISPOSABLE_EMAIL'); }

  // Device fingerprint seen with multiple different emails (account farm)
  const fingerprintEmails = await db.order.findMany({
    where: { deviceFingerprint: signals.deviceFingerprint },
    select: { email: true },
    distinct: ['email'],
  });
  if (fingerprintEmails.length > 5) { score += 25; reasons.push('FINGERPRINT_MULTI_ACCOUNT'); }

  const action = score >= 70 ? 'block' : score >= 40 ? 'review' : 'allow';
  return { score, action, reasons };
}

// Apply fraud check in checkout flow
app.post('/api/checkout/confirm', async (req, res) => {
  const { cartId } = req.body;
  const signals = extractFraudSignals(req);
  const risk = await scoreFraudRisk(signals);

  if (risk.action === 'block') {
    await db.fraudAttempt.create({ data: { ...signals, score: risk.score, reasons: risk.reasons } });
    return res.status(403).json({ error: 'ORDER_BLOCKED', code: 'FRAUD_RISK' });
  }
  if (risk.action === 'review') {
    // Proceed but flag for manual review after payment
    await db.order.create({ data: { cartId, fraudScore: risk.score, requiresReview: true } });
  }
  // ... normal checkout flow
});
```

---

# shopify-dev

Shopify development patterns — Liquid templates, Shopify API, Hydrogen/Remix storefronts, metafields, theme architecture, webhook HMAC verification.

#### Workflow

**Step 1 — Detect Shopify architecture**
Use Glob to find `shopify.app.toml`, `*.liquid`, `remix.config.*`, `hydrogen.config.*`. Use Grep to find Storefront API queries (`#graphql`), Admin API calls, metafield references, and API version strings. Classify: theme app extension, custom app, or Hydrogen storefront.

**Step 2 — Audit theme and API usage**
Check for:
- Liquid templates without `| escape` filter on user-generated metafield content (XSS vulnerability)
- Storefront API queries without pagination (`first: 250` max — cursor-based pagination required for larger sets)
- Hardcoded product IDs or variant IDs (break when products are recreated)
- Missing metafield type validation (metafield can be deleted/recreated with different type)
- Theme sections without `schema` blocks (limits merchant customization)
- Deprecated API version usage (Shopify deprecates versions on a rolling 12-month cycle)
- Webhook handlers without HMAC signature verification (anyone can POST fake events)

**Step 3 — Emit optimized patterns**
For Hydrogen: emit typed Storefront API loader with proper caching and pagination. For theme: emit section schema with metafield integration. For apps: emit webhook handler with HMAC verification and idempotency.

#### Example

```typescript
// Hydrogen — typed Storefront API loader with caching + pagination
import { json, type LoaderFunctionArgs } from '@shopify/remix-oxygen';

const PRODUCTS_QUERY = `#graphql
  query Products($first: Int!, $after: String) {
    products(first: $first, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id handle title
        variants(first: 10) {
          nodes { id title price { amount currencyCode } availableForSale }
        }
        metafield(namespace: "custom", key: "care_instructions") { value type }
      }
    }
  }
` as const;

export async function loader({ context }: LoaderFunctionArgs) {
  const { products } = await context.storefront.query(PRODUCTS_QUERY, {
    variables: { first: 24 },
    cache: context.storefront.CacheLong(),
  });
  return json({ products });
}

// Webhook handler with HMAC verification (Express)
import crypto from 'crypto';

function verifyShopifyWebhook(req: Request, secret: string): boolean {
  const hmac = req.headers['x-shopify-hmac-sha256'] as string;
  const body = (req as any).rawBody; // Must capture raw body before JSON parse
  const hash = crypto.createHmac('sha256', secret).update(body, 'utf8').digest('base64');
  return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(hmac));
}
```

---

# subscription-billing

Subscription billing — trial management, proration, dunning (failed payment retry), plan changes mid-cycle, usage-based billing, cancellation flows.

#### Workflow

**Step 1 — Detect subscription setup**
Use Grep to find: `stripe.subscriptions`, `subscription`, `recurring`, `billing_cycle`, `trial`, `prorate`, `dunning`. Check for Stripe Billing Portal, customer portal redirect, and subscription lifecycle webhook handlers.

**Step 2 — Audit subscription lifecycle**
Check for:
- Trial-to-paid transition: is payment method collected during trial signup? (If not, 60%+ of trials churn at conversion — Stripe data)
- Proration on plan change: `proration_behavior` defaults to `create_prorations` — mid-cycle upgrade charges immediately. Must explicitly choose behavior and communicate to user
- Failed payment handling: Stripe retries automatically per Smart Retries settings, but app must handle `invoice.payment_failed` webhook to notify user, restrict access, or trigger custom retry
- Cancellation: `cancel_at_period_end` vs immediate cancel — immediate loses remaining period revenue. Most SaaS should use `cancel_at_period_end` and show countdown
- Missing webhook handlers for: `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`, `invoice.paid`
- Usage-based billing: meter events must be sent before invoice finalization (not after) — late events are lost

**Step 3 — Emit subscription patterns**
Emit: subscription creation with trial + payment method upfront, plan change with explicit proration, dunning webhook handler, and cancellation flow.

#### Example

```typescript
// Create subscription with trial — collect payment method upfront
async function createSubscription(customerId: string, priceId: string, trialDays: number) {
  // Verify customer has payment method BEFORE creating subscription
  const paymentMethods = await stripe.paymentMethods.list({
    customer: customerId, type: 'card',
  });
  if (paymentMethods.data.length === 0) {
    throw new Error('Payment method required before starting trial');
  }

  return stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    trial_period_days: trialDays,
    payment_settings: {
      payment_method_types: ['card'],
      save_default_payment_method: 'on_subscription',
    },
    trial_settings: {
      end_behavior: { missing_payment_method: 'cancel' }, // Auto-cancel if no card at trial end
    },
    expand: ['latest_invoice.payment_intent'],
  });
}

// Plan change with explicit proration
async function changePlan(subscriptionId: string, newPriceId: string) {
  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  return stripe.subscriptions.update(subscriptionId, {
    items: [{ id: subscription.items.data[0].id, price: newPriceId }],
    proration_behavior: 'always_invoice', // Charge/credit immediately
    payment_behavior: 'error_if_incomplete', // Fail if upgrade payment fails
  });
}

// Dunning webhook — restrict access after payment failure
app.post('/webhooks/subscription', async (req, res) => {
  const event = verifyStripeEvent(req);

  switch (event.type) {
    case 'invoice.payment_failed': {
      const invoice = event.data.object as Stripe.Invoice;
      const attempt = invoice.attempt_count;
      if (attempt >= 3) {
        // After 3 failed retries, restrict access (don't cancel yet)
        await userService.setStatus(invoice.customer as string, 'past_due');
        await emailService.send(invoice.customer_email!, 'payment-failed-final');
      } else {
        await emailService.send(invoice.customer_email!, 'payment-failed-retry', { attempt });
      }
      break;
    }
    case 'customer.subscription.deleted': {
      const sub = event.data.object as Stripe.Subscription;
      await userService.deactivate(sub.customer as string);
      break;
    }
  }
  res.json({ received: true });
});
```

---

# tax-compliance

Tax calculation — sales tax API integration, VAT for EU, digital goods tax, tax-inclusive pricing, audit trail.

#### Workflow

**Step 1 — Detect tax setup**
Use Grep to find: `tax`, `vat`, `taxjar`, `avalara`, `tax_rate`, `taxAmount`, `tax_exempt`. Check if tax calculation exists and where it happens (cart time vs checkout time).

**Step 2 — Audit tax accuracy**
Check for:
- Tax calculated at cart time but not recalculated at checkout (rate may have changed, or user changed shipping address)
- Hardcoded tax rates instead of API-based calculation (rates change; nexus rules are complex)
- Missing tax on digital goods (many US states and all EU countries tax digital products)
- EU VAT: must charge buyer's country VAT rate for B2C digital sales (not seller's country)
- Tax-inclusive vs tax-exclusive display: must be consistent and clearly labeled
- No tax audit trail: amounts, rates, and jurisdiction must be stored per order for compliance
- Missing tax exemption handling (B2B customers with valid VAT number or tax-exempt certificate)

**Step 3 — Emit tax patterns**
Emit: tax calculation at checkout time (not cart time), API-based rate lookup, EU VAT reverse charge for B2B, and tax audit trail per order line item.

#### Example

```typescript
// Tax calculation at CHECKOUT time (not cart time) — rates may change
interface TaxLineItem {
  productId: string;
  amount: number;
  quantity: number;
  taxCode: string; // Product tax code (e.g., 'txcd_10000000' for general goods)
}

async function calculateTax(
  items: TaxLineItem[],
  shippingAddress: Address,
  customerTaxExempt: boolean
): Promise<TaxResult> {
  if (customerTaxExempt) {
    return { totalTax: 0, lineItems: items.map(i => ({ ...i, tax: 0, rate: 0 })) };
  }

  // Use tax API — never hardcode rates
  const calculation = await stripe.tax.calculations.create({
    currency: 'usd',
    line_items: items.map(item => ({
      amount: item.amount * item.quantity,
      reference: item.productId,
      tax_code: item.taxCode,
    })),
    customer_details: {
      address: {
        line1: shippingAddress.line1,
        city: shippingAddress.city,
        state: shippingAddress.state,
        postal_code: shippingAddress.postalCode,
        country: shippingAddress.country,
      },
      address_source: 'shipping',
    },
  });

  return {
    totalTax: calculation.tax_amount_exclusive,
    lineItems: calculation.line_items.data.map(li => ({
      productId: li.reference,
      tax: li.amount_tax,
      rate: li.tax_breakdown?.[0]?.rate ?? 0,
      jurisdiction: li.tax_breakdown?.[0]?.jurisdiction?.display_name ?? 'Unknown',
    })),
  };
}

// EU VAT validation — B2B reverse charge
async function validateEuVat(vatNumber: string, buyerCountry: string): Promise<boolean> {
  // Use VIES (VAT Information Exchange System) API
  const res = await fetch(
    `https://ec.europa.eu/taxation_customs/vies/rest-api/ms/${buyerCountry}/vat/${vatNumber.replace(/^[A-Z]{2}/, '')}`
  );
  const data = await res.json();
  return data.isValid === true;
}

// Store tax audit trail per order (required for compliance)
interface OrderTaxRecord {
  orderId: string;
  lineItemId: string;
  taxAmount: number;
  taxRate: number;
  jurisdiction: string;
  calculatedAt: Date;
  taxApiTransactionId: string;
}

// Commit tax record immediately at payment creation — never calculate retroactively
async function commitTaxRecord(orderId: string, calculation: TaxResult, txnId: string) {
  await prisma.orderTaxRecord.createMany({
    data: calculation.lineItems.map(li => ({
      orderId,
      lineItemId: li.productId,
      taxAmount: li.tax,
      taxRate: li.rate,
      jurisdiction: li.jurisdiction,
      calculatedAt: new Date(),
      taxApiTransactionId: txnId,
    })),
  });
}
```

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)