# Sendivent Node.js SDK Guide

TypeScript/Node.js examples for the Sendivent notification API.

---

## Installation

```bash
npm install @appitude/sendivent
```

---

## Quick Start

### 1. Set your API key

```bash
export SENDIVENT_API_KEY="live_your_key_here"
```

### 2. Initialize the client

```typescript
import { Sendivent } from "@appitude/sendivent";

const sendivent = new Sendivent(process.env.SENDIVENT_API_KEY);
```

### 3. Send a notification

```typescript
await sendivent
  .event("user.welcome")
  .to("user@example.com")
  .payload({
    name: "Jane",
    activationUrl: "https://yourapp.com/activate?token=abc123",
  })
  .send();
```

This sends the `user.welcome` event to the given email address. The event's configured channels (email, SMS, Slack, etc.) fire automatically based on what templates and integrations are set up in the dashboard.

---

## Send Notification

The SDK uses a **builder pattern** — chain methods and call `.send()` at the end.

### Basic — send by email

```typescript
await sendivent
  .event("order.confirmed")
  .to("customer@example.com")
  .payload({
    orderNumber: "ORD-12345",
    total: "$99.00",
    estimatedDelivery: "April 5, 2026",
  })
  .send();
```

### Send by phone number

```typescript
await sendivent
  .event("verification.code")
  .to("+14155551234")
  .payload({ code: "482910" })
  .send();
```

### Send with contact object (custom fields go to meta)

```typescript
await sendivent
  .event("payment.failed")
  .to({
    email: "user@example.com",
    name: "Jane Smith",
    subscriptionTier: "premium",  // stored in contact.meta
    accountId: "acc_789",         // stored in contact.meta
  })
  .payload({
    amount: "$49.00",
    retryDate: "April 2, 2026",
  })
  .send();
```

Access in templates: `{{contact.name}}`, `{{contact.meta.subscriptionTier}}`, `{{payload.amount}}`

### Send to multiple recipients

```typescript
await sendivent
  .event("weekly.digest")
  .to([
    { email: "alice@example.com", name: "Alice", role: "admin" },
    { email: "bob@example.com", name: "Bob", role: "member" },
  ])
  .payload({
    weekOf: "March 24, 2026",
    totalEvents: 42,
  })
  .send();
```

Each recipient gets a personalized notification with their own contact data + shared payload.

### Force a specific channel

```typescript
await sendivent
  .event("alert.critical")
  .to("ops@example.com")
  .payload({ service: "api-gateway", error: "Connection timeout" })
  .channel("slack")
  .send();
```

### With language override

```typescript
await sendivent
  .event("user.welcome")
  .to("user@example.com")
  .payload({ name: "Erik" })
  .language("sv")  // Swedish template
  .send();
```

### With sender override

```typescript
await sendivent
  .event("invoice.sent")
  .to("customer@example.com")
  .payload({ invoiceNumber: "INV-001" })
  .from("billing@yourcompany.com")  // must be verified
  .send();
```

### With channel overrides

```typescript
await sendivent
  .event("order.shipped")
  .to("customer@example.com")
  .payload({ trackingUrl: "https://..." })
  .overrides({
    email: {
      subject: "Your package is on the way!",
      reply_to: "support@yourcompany.com",
    },
  })
  .send();
```

### With idempotency key

```typescript
await sendivent
  .event("order.confirmed")
  .to("customer@example.com")
  .payload({ orderNumber: "ORD-12345" })
  .idempotencyKey("order-12345-confirmation")
  .send();
```

Prevents duplicate sends if the same key is used again.

---

## Contacts

### Create or upsert contact

```typescript
const contact = await sendivent.contacts.upsert({
  email: "jane@example.com",
  name: "Jane Smith",
  id: "user_123",         // maps to external_id in the API
  phone: "+14155551234",
});
```

If a contact with the same identifier already exists, it will be updated with the new data.

> **Note:** The SDK uses `id` for your application's user ID, which maps to `external_id` in the REST API.

### Find contact

```typescript
const contact = await sendivent.contacts.get("jane@example.com");
// Also works with: UUID, phone number, external_id, slack user ID
```

### Update contact

```typescript
await sendivent.contacts.update("jane@example.com", {
  name: "Jane Doe",
  avatar: "https://example.com/jane.jpg",
});
```

### Delete contact

```typescript
await sendivent.contacts.delete("jane@example.com");
```

### Register push token

```typescript
await sendivent.contacts.registerPushToken(
  "jane@example.com",
  "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
);
```

### Remove push token

```typescript
await sendivent.contacts.removePushToken(
  "jane@example.com",
  "ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]"
);
```

> **Note:** Listing contacts is available via the REST API (`GET /v1/contacts`) but not yet in the SDK.

---

## Webhooks

### Create webhook endpoint

Webhooks are managed via the REST API. Use `fetch` or any HTTP client:

```typescript
const response = await fetch("https://api.sendivent.com/v1/webhooks", {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${process.env.SENDIVENT_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    url: "https://yourapp.com/webhooks/sendivent",
    enabled_events: ["delivery.sent", "delivery.failed", "delivery.bounced"],
  }),
});

const data = await response.json();
console.log(data.webhook.signing_secret); // Save this for verification
```

### Verify webhook signature

```typescript
import crypto from "crypto";

function verifyWebhook(body: string, signature: string, secret: string): boolean {
  const expected = crypto
    .createHmac("sha256", secret)
    .update(body)
    .digest("hex");
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

---

## Error Handling

```typescript
try {
  await sendivent
    .event("user.welcome")
    .to("user@example.com")
    .payload({ name: "Jane" })
    .send();
} catch (error) {
  if (error instanceof Error) {
    // Error message includes status code and API error
    // e.g. "Sendivent API request failed: 404 - Event 'user.welcome' not found"
    console.error(error.message);
  }
}
```

---

## Full Workflow Example

```typescript
import { Sendivent } from "@appitude/sendivent";

const sendivent = new Sendivent(process.env.SENDIVENT_API_KEY);

async function onUserSignup(user: { email: string; name: string; plan: string }) {
  // Create contact (unknown fields like 'plan' go to meta automatically)
  await sendivent.contacts.upsert({
    email: user.email,
    name: user.name,
    plan: user.plan,
  });

  // Send welcome notification (email + slack if configured)
  await sendivent
    .event("user.welcome")
    .to(user.email)
    .payload({
      activationUrl: `https://yourapp.com/activate?email=${user.email}`,
      supportEmail: "support@yourcompany.com",
    })
    .send();
}

async function onOrderConfirmed(order: { email: string; id: string; total: string }) {
  await sendivent
    .event("order.confirmed")
    .to(order.email)
    .payload({
      orderNumber: order.id,
      total: order.total,
    })
    .idempotencyKey(`order-${order.id}-confirmed`)
    .send();
}
```

---

## Reference

- [SKILL.md](../SKILL.md) — REST API endpoints and parameter reference
- [API Guide](api-guide.md) — API method reference
- [Official Docs](https://sendivent.com/docs) — Full documentation
