# Checkout Flow Copy

Reduce abandonment with reassuring, clear microcopy at every step.

## Cart Page

### Cart Header
❌ "Shopping Cart"
✅ "Your Cart (3 items)"
✅ "Almost yours..."

### Empty Cart
**Pattern:**
```
Your cart is empty

[Friendly nudge + action]

[CTA: Continue Shopping] or [CTA: View Bestsellers]
```

**Examples:**
- "Your cart is feeling lonely. Let's fix that."
- "Nothing here yet — but we've got ideas."
- "Looks like you haven't found 'the one' yet."

### Cart Item Display
Each item should show:
- Product image (clickable)
- Product name (linked)
- Selected variants (size, color)
- Price (and original if discounted)
- Quantity selector
- Remove option

**Remove confirmation:**
"Remove [Product Name] from cart?"
[Cancel] [Remove]

### Cart Summary
```
Subtotal: €89.00
Shipping: Calculated at checkout (or "Free" if applicable)
─────────────────
Estimated total: €89.00

[Proceed to Checkout]
```

**Trust signals to include:**
- "Free shipping on orders over €50"
- "Free returns within 30 days"
- "Secure checkout"
- Payment icons row

### Upsell/Cross-sell in Cart
**Headers that convert:**
- "Complete your order" (bundles)
- "Don't forget" (accessories)
- "Customers also bought"
- "Add for just €X more" (threshold shipping)

**Threshold nudge:**
"You're €15 away from free shipping!"
[Add something] or show qualifying products

### Cart Urgency (Use Sparingly)
Only use if true:
- "Only 3 left in stock"
- "Reserved for 15 minutes"
- "Sale ends tonight"

❌ Fake urgency destroys trust

## Checkout Page — Information Step

### Progress Indicator
Show where they are:
```
[Information] → Shipping → Payment
    ●────────────○────────────○
```

### Form Labels & Placeholders
Be specific, reduce errors:

| Field | Label | Placeholder |
|-------|-------|-------------|
| Email | Email address | you@example.com |
| First name | First name | — |
| Last name | Last name | — |
| Address | Street address | 123 Main Street |
| Apt/Suite | Apartment, suite, etc. (optional) | — |
| City | City | — |
| Postal code | Postal code | 1234 AB |
| Phone | Phone (for delivery updates) | +31 6... |

**Optional field indicator:**
Mark optional fields, not required ones: "Apartment (optional)"

### Form Validation Messages
Be helpful, not angry:

❌ "Invalid email"
✅ "Please enter a valid email address (e.g., you@example.com)"

❌ "Error in postal code"
✅ "This postal code doesn't look right. Dutch format: 1234 AB"

❌ "Required field"
✅ "Please enter your [field name]"

### Newsletter Opt-in
**Pre-checked (GDPR-compliant in some regions):**
"Email me with news and offers"

**Better (explicit consent):**
□ "Yes, I'd like to receive exclusive offers and updates"

## Checkout — Shipping Step

### Shipping Options
```
○ Standard Shipping — €4.95
  Arrives in 3-5 business days

● Express Shipping — €9.95
  Arrives in 1-2 business days

○ Same-Day Delivery — €14.95
  Order by 2pm, get it today (Amsterdam area only)
```

**What to include:**
- Clear price
- Delivery timeframe
- Any restrictions

### Shipping Information Copy
"Shipping calculated based on your address"
"Free shipping on orders over €50"
"We ship to 45+ countries"

### Delivery Date Estimates
Be specific when possible:
- "Estimated delivery: Thursday, Feb 13"
- "Usually arrives within 3-5 business days"

### Gift Options (if available)
"🎁 Is this a gift?"
□ "Add gift wrapping (+€3.50)"
□ "Include a gift message"

## Checkout — Payment Step

### Payment Method Selection
```
How would you like to pay?

◉ iDEAL
○ Credit/debit card
○ PayPal
○ Klarna — Pay in 30 days
○ Apple Pay
```

### Credit Card Form
**Labels:**
- Card number
- Expiration date (MM/YY)
- Security code (CVV)
- Name on card

**Helpful microcopy:**
- "The 3-digit code on the back of your card"
- "As it appears on your card"

### Security Signals
Place near payment form:
- 🔒 "Secure checkout — your data is encrypted"
- "Payments processed by Stripe"
- SSL badge
- Payment provider logos

### Save Payment Info
"□ Save my payment info for faster checkout next time"
"Your card details are encrypted and stored securely."

### Order Summary (Payment Step)
```
Order Summary
─────────────────────────────────
Product Name × 1              €49.00
Product Name × 2              €40.00
─────────────────────────────────
Subtotal                      €89.00
Shipping (Express)             €9.95
─────────────────────────────────
Total                         €98.95
─────────────────────────────────

□ I agree to the Terms of Service and Privacy Policy

[Pay €98.95]
```

### Terms Checkbox
Keep it simple:
"□ I agree to the Terms and Privacy Policy"

Link terms, don't dump them.

### CTA Button
Be specific about what happens:
- "Pay €98.95"
- "Complete order"
- "Place order"

❌ "Submit"
❌ "Continue"

## Order Confirmation Page

### Primary Message
```
🎉 Thank you, [First Name]!

Your order #12345 is confirmed.
We've sent a confirmation to [email@example.com].
```

### Order Details
```
Order #12345
Placed on February 11, 2026

[Product image] Product Name × 1    €49.00
[Product image] Product Name × 2    €40.00

Shipping: Express (1-2 days)         €9.95
Total paid:                         €98.95
```

### What's Next
```
What happens next?

1. We're preparing your order
2. You'll receive a shipping confirmation with tracking
3. Your package arrives in 1-2 business days

Estimated delivery: Thursday, Feb 13
```

### Additional Actions
- "Track your order"
- "Continue shopping"
- "Create an account for faster checkout" (guest checkout)
- "Share your purchase" (optional, brand-dependent)

### Support Info
"Questions? Contact us at support@brand.com"
"Need to change something? Email us within 1 hour."

## Error States

### Payment Declined
```
Payment unsuccessful

Your card was declined. This can happen for several reasons:
• Insufficient funds
• Incorrect card details
• Bank security block

Please try:
1. Check your card details
2. Try a different payment method
3. Contact your bank

[Try Again] [Use Different Payment]
```

### Out of Stock at Checkout
```
Sorry, [Product Name] just sold out

This item is no longer available in your selected size/color.

[Remove from cart] [See alternatives]
```

### Session Expired
```
Your session expired

For your security, checkout sessions expire after 30 minutes.
Don't worry — your cart is saved.

[Return to cart]
```

## A/B Testing Opportunities

High-impact elements to test:
1. **CTA button copy** — "Buy now" vs "Add to cart" vs "Get yours"
2. **Trust signals placement** — Near CTA vs footer vs both
3. **Progress indicator style** — Steps vs percentage vs none
4. **Urgency messaging** — Stock warnings, time limits
5. **Shipping threshold** — Amount for free shipping
6. **Guest checkout prominence** — Required account vs optional
