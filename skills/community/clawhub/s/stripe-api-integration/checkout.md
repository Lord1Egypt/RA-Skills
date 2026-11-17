# Checkout — Hosted Sessions, Payment Links, Embedded

**Read `## Catalog` and `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`** (or their boxes) before building a session: the price ids in use and whether this integration creates the customer before Checkout or lets Checkout create one.

**Contents:** [Which Hosted Surface](#which-hosted-surface) · [The Event Contract](#the-event-contract) · [Checkout Modes](#checkout-modes) · [Complete Checkout Flow](#complete-checkout-flow) · [Custom Fields](#custom-fields) · [Trial Periods](#trial-periods) · [Quantity Adjustable](#quantity-adjustable) · [Metadata](#metadata) · [Embedded Checkout](#embedded-checkout) · [Session Expiration](#session-expiration) · [Recovery](#recovery) · [Common Patterns](#common-patterns)

## Which Hosted Surface

| Surface | Fits | Cost of choosing it |
|---|---|---|
| Payment Link | A price you sell the same way to everyone; no backend at all | No per-customer logic, no dynamic amounts |
| Hosted Checkout Session | Anything server-driven: dynamic carts, per-customer trials, tax, promotion codes | A redirect away from your domain |
| Embedded Checkout | Keeping the customer on your page while Stripe still owns the payment fields | Slightly more integration, same PCI scope |
| Elements | The payment step is inside a flow you fully control | You rebuild wallets, local methods, SCA handling and address collection |

Default to hosted Checkout and move down the list only when a concrete requirement forces it: it carries wallets, local payment methods, SCA, address and tax collection, promotion codes and adaptive layout, all maintained by someone else (`SKILL.md`, Where Experts Disagree).

## The Event Contract

- `checkout.session.completed` means the session finished, **not** that money arrived. Check `payment_status`: `paid` for synchronous methods, `unpaid` when a bank-based method is still settling.
- For asynchronous methods, fulfillment belongs on `checkout.session.async_payment_succeeded`, and the failure path on `checkout.session.async_payment_failed` (`payment-methods.md`).
- `checkout.session.expired` is the recovery hook: the customer left, and you have their email if you collected it.
- Session metadata does not reach the PaymentIntent or the Subscription. Set `payment_intent_data[metadata]` and `subscription_data[metadata]` explicitly, or the surviving object has no link to your order (`api-mechanics.md`).
- Create the customer before the session when you need the record to be stable — letting Checkout create one per purchase is the fastest way to duplicate customers (`customers.md`).

## Checkout Modes

| Mode | Use Case | Creates |
|------|----------|---------|
| `payment` | One-time purchase | PaymentIntent |
| `subscription` | Recurring billing | Subscription |
| `setup` | Save card for later | SetupIntent |

## Complete Checkout Flow

### 1. Create Checkout Session
```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=subscription" \
  -d "customer=cus_XXX" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "success_url=https://example.com/success?session_id={CHECKOUT_SESSION_ID}" \
  -d "cancel_url=https://example.com/cancel" \
  -d "allow_promotion_codes=true" \
  -d "billing_address_collection=required" \
  -d "customer_update[address]=auto" \
  -d "customer_update[name]=auto"
```

### 2. Redirect Customer
```javascript
// Frontend - redirect to Stripe Checkout
window.location.href = session.url;
```

### 3. Handle Success
```bash
# Get session details after success
curl https://api.stripe.com/v1/checkout/sessions/cs_XXX?expand[]=subscription&expand[]=customer \
  -u "$STRIPE_SECRET_KEY:"
```

## Custom Fields

### Add Custom Fields
```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "custom_fields[0][key]=company" \
  -d "custom_fields[0][label][type]=custom" \
  -d "custom_fields[0][label][custom]=Company Name" \
  -d "custom_fields[0][type]=text" \
  -d "custom_fields[1][key]=size" \
  -d "custom_fields[1][label][type]=custom" \
  -d "custom_fields[1][label][custom]=T-Shirt Size" \
  -d "custom_fields[1][type]=dropdown" \
  -d "custom_fields[1][dropdown][options][0][label]=Small" \
  -d "custom_fields[1][dropdown][options][0][value]=S" \
  -d "custom_fields[1][dropdown][options][1][label]=Medium" \
  -d "custom_fields[1][dropdown][options][1][value]=M" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

## Trial Periods

### Add Trial to Subscription
```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=subscription" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "subscription_data[trial_period_days]=14" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

### Trial Without Payment Method
```bash
# Requires subscription_data[trial_settings][end_behavior][missing_payment_method]
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=subscription" \
  -d "payment_method_collection=if_required" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "subscription_data[trial_period_days]=14" \
  -d "subscription_data[trial_settings][end_behavior][missing_payment_method]=cancel" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

## Quantity Adjustable

```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=subscription" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=5" \
  -d "line_items[0][adjustable_quantity][enabled]=true" \
  -d "line_items[0][adjustable_quantity][minimum]=1" \
  -d "line_items[0][adjustable_quantity][maximum]=100" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

## Metadata

```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "metadata[order_id]=12345" \
  -d "metadata[campaign]=summer_sale" \
  -d "payment_intent_data[metadata][order_id]=12345" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

## Embedded Checkout

```javascript
// Initialize Stripe.js
const stripe = Stripe('pk_xxx');

// Create checkout session on server, return client_secret
const { clientSecret } = await fetch('/create-checkout-session').then(r => r.json());

// Mount embedded checkout
const checkout = await stripe.initEmbeddedCheckout({
  clientSecret,
});
checkout.mount('#checkout');
```

## Session Expiration

- Default: 24 hours
- Custom: Set `expires_at` (minimum 30 minutes, maximum 24 hours)

```bash
curl https://api.stripe.com/v1/checkout/sessions \
  -u "$STRIPE_SECRET_KEY:" \
  -d "mode=payment" \
  -d "expires_at=$(($(date +%s) + 3600))" \
  -d "line_items[0][price]=price_XXX" \
  -d "line_items[0][quantity]=1" \
  -d "success_url=https://example.com/success" \
  -d "cancel_url=https://example.com/cancel"
```

## Recovery

### Recover Abandoned Checkout
```bash
# List expired sessions
curl "https://api.stripe.com/v1/checkout/sessions?status=expired&limit=100" \
  -u "$STRIPE_SECRET_KEY:"

# Sessions include customer email if provided
# Use for recovery emails
```

## Common Patterns

### Upsell at Checkout
```bash
# Add upsell items with adjustable quantity starting at 0
-d "line_items[1][price]=price_ADDON"
-d "line_items[1][quantity]=0"
-d "line_items[1][adjustable_quantity][enabled]=true"
-d "line_items[1][adjustable_quantity][minimum]=0"
-d "line_items[1][adjustable_quantity][maximum]=10"
```

### Collect Tax ID
```bash
-d "tax_id_collection[enabled]=true"
```

### Collect Shipping Address
```bash
-d "shipping_address_collection[allowed_countries][0]=US"
-d "shipping_address_collection[allowed_countries][1]=CA"
```

## Conversion Details That Are Not Cosmetic

- **Collect the email early.** Without it, an expired session is unrecoverable; with it, abandoned-checkout recovery is a list you can email.
- **`allow_promotion_codes` shows a code field.** On a page with no active campaign it invites customers to leave and search for a code that does not exist — enable it when you are actually running one.
- **Ask for the address only where you need it**: tax calculation, physical shipping, or fraud signals. Each extra required field costs completions.
- **Set the locale or let it follow the browser**; a checkout in the wrong language converts like a broken page.
- **Expiry is a lever**: shorter sessions create urgency and strand slow buyers; the default day is right for most, and anything under an hour needs a reason.
- **Return to a page that confirms what happened**, driven by the event and not by the redirect — the redirect can be lost, and the payment still succeeded.

---

**Write in the same turn**: the surface chosen (Payment Link, hosted, embedded, Elements) and the customer-creation order go to `## Integration Shape` in `~/Clawic/data/stripe-api-integration/memory.md`; any price or promotion code created for the flow goes to `## Catalog`; a checkout configuration that measurably converted better is `artifacts/decision-checkout.md` with its `## Boxes` line.
