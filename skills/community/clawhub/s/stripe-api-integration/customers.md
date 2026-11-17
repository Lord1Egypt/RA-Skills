# Customers, Products, Prices, Coupons

**Read `## Catalog` in `~/Clawic/data/stripe-api-integration/memory.md`** (or `catalog.md` when `## Boxes` points there) before creating anything here: the price id that already exists, and the one it replaced, are the two facts nobody can reconstruct from memory.

**Contents:** [Object Rules That Bite Later](#object-rules-that-bite-later) · [Customers](#customers) · [Products](#products) · [Prices](#prices) · [Coupons](#coupons) · [ID Prefixes Reference](#id-prefixes-reference)

## Object Rules That Bite Later

- **Stripe allows duplicate customers with the same email, and will happily create one per checkout.** Look the customer up by your own key before creating — a customer created twice is a subscription the Billing Portal cannot show, an invoice history split in half, and a support ticket you cannot answer. Search is eventually consistent, so the lookup belongs in your database, not in Stripe (`api-mechanics.md`).
- **A price is effectively immutable**: amount, currency, interval and tier structure are frozen once it exists. Changing what you charge means creating a new price and migrating deliberately (`pricing-models.md`).
- **Deleting is archiving.** Products and prices that have been used are deactivated, not removed, and live subscriptions keep billing on a deactivated price. That is correct behavior and it is why retired rows stay in the catalog with their date.
- **Metadata does not propagate.** A customer's metadata is not on their invoices; set it where you will read it (`api-mechanics.md`).
- The customer's `invoice_settings[default_payment_method]` is what subscriptions charge. Attaching a payment method without setting it is the most common cause of a renewal that fails against nothing (`dunning.md`).
- Tax id, billing address and name on the customer object are what appear on the invoice. Collect them at checkout or credit-note your way back later (`tax.md`).

## Customers

### List Customers
```bash
curl "https://api.stripe.com/v1/customers?limit=10&email=customer@example.com" \
  -u "$STRIPE_SECRET_KEY:"
```

Query parameters: `limit`, `starting_after`, `ending_before`, `email`, `created`

### Get Customer
```bash
curl https://api.stripe.com/v1/customers/cus_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

### Create Customer
```bash
curl https://api.stripe.com/v1/customers \
  -u "$STRIPE_SECRET_KEY:" \
  -d "email=customer@example.com" \
  -d "name=John Doe" \
  -d "metadata[user_id]=123"
```

### Update Customer
```bash
curl https://api.stripe.com/v1/customers/cus_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Jane Doe"
```

### Delete Customer
```bash
curl -X DELETE https://api.stripe.com/v1/customers/cus_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Products

### List Products
```bash
curl "https://api.stripe.com/v1/products?limit=10&active=true" \
  -u "$STRIPE_SECRET_KEY:"
```

### Create Product
```bash
curl https://api.stripe.com/v1/products \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Pro Plan" \
  -d "description=Full access to all features"
```

### Update Product
```bash
curl https://api.stripe.com/v1/products/prod_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "name=Updated Plan" \
  -d "active=true"
```

### Delete Product
```bash
curl -X DELETE https://api.stripe.com/v1/products/prod_XXX \
  -u "$STRIPE_SECRET_KEY:"
```

---

## Prices

### List Prices
```bash
curl "https://api.stripe.com/v1/prices?product=prod_XXX&active=true" \
  -u "$STRIPE_SECRET_KEY:"
```

### Create Recurring Price
```bash
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_XXX" \
  -d "unit_amount=1999" \
  -d "currency=usd" \
  -d "recurring[interval]=month"
```

### Create One-time Price
```bash
curl https://api.stripe.com/v1/prices \
  -u "$STRIPE_SECRET_KEY:" \
  -d "product=prod_XXX" \
  -d "unit_amount=4999" \
  -d "currency=usd"
```

### Update Price
```bash
curl https://api.stripe.com/v1/prices/price_XXX \
  -u "$STRIPE_SECRET_KEY:" \
  -d "active=false"
```

---

## Coupons

### Create Percentage Coupon
```bash
curl https://api.stripe.com/v1/coupons \
  -u "$STRIPE_SECRET_KEY:" \
  -d "percent_off=25" \
  -d "duration=repeating" \
  -d "duration_in_months=3"
```

### Create Fixed Amount Coupon
```bash
curl https://api.stripe.com/v1/coupons \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount_off=1000" \
  -d "currency=usd" \
  -d "duration=once"
```

### Create Promotion Code
```bash
curl https://api.stripe.com/v1/promotion_codes \
  -u "$STRIPE_SECRET_KEY:" \
  -d "coupon=COUPON_ID" \
  -d "code=SUMMER25" \
  -d "max_redemptions=100"
```

---

## ID Prefixes Reference

| Prefix | Resource |
|--------|----------|
| `cus_` | Customer |
| `prod_` | Product |
| `price_` | Price |
| `pm_` | Payment Method |

---

**Write in the same turn** any product, price, coupon or promotion code created, retired or replaced: its row goes to `## Catalog` in `~/Clawic/data/stripe-api-integration/memory.md` with the id, the model, the amount with its currency, the interval and what it replaced. Count the entries first — past ~15, split the section to `catalog.md` before appending and add its `## Boxes` line (`memory-template.md`). A named client behind a customer record goes to `~/Clawic/data/contacts/contacts.md`, referenced here by name only.
