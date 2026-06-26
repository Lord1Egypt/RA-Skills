# Adapters Reference

Adapters protect domain models from external concepts by translating between domain models and external DTOs.

## Types of Adapters

1. **Repository Adapters**: Abstract database access (see [repositories.md](repositories.md))
2. **Action Adapters**: Integrate with external APIs (this document)

## Action Adapters

Actions that communicate with external systems (payment gateways, CRMs, email providers) should:

1. Map domain models to external DTOs
2. Call the external API
3. Schedule a mutation to persist results
4. Keep business logic in mutations, not actions

### Basic Structure

```typescript
// convex/billing/adapters/sendInvoice.action.ts
"use node";

import { internalAction } from "../../_generated/server";
import { internal } from "../../_generated/api";
import { v } from "convex/values";
import { InvoiceModel, Invoice } from "../domain/invoice.model";
import { CustomerModel } from "../domain/customer.model";
import stripeClient from "../_libs/stripeClient";

const sendInvoice = internalAction({
  args: {
    invoice: InvoiceModel,
    customer: CustomerModel,
  },
  returns: v.null(),
  handler: async (ctx, args): Promise<null> => {
    const { customer, invoice } = args;

    // 1. Map domain model → external DTO
    const createInvoiceDTO = {
      amount: invoice.amount,
      currency: invoice.currency,
      customer: customer.stripeId,
      description: invoice.description,
    };

    // 2. Call external API
    const response = await stripeClient.invoices.create(createInvoiceDTO);

    // 3. Schedule mutation to persist (pass IDs for transaction safety)
    await ctx.runMutation(internal.billing.mutations.openFromStripe.default, {
      stripeId: response.id,
      invoiceId: invoice._id,
    });

    return null;
  },
});

export default sendInvoice;
```

### Corresponding Mutation

```typescript
// convex/billing/mutations/openFromStripe.ts
import { internalMutation } from "../../_generated/server";
import { v } from "convex/values";
import { InvoiceModel, Invoice } from "../domain/invoice.model";
import { InvoiceRepository } from "../adapters/invoice.repository";

const openFromStripe = internalMutation({
  args: {
    invoiceId: v.id("invoices"),
    stripeId: v.string(),
  },
  returns: InvoiceModel,
  handler: async (ctx, args): Promise<Invoice> => {
    // 1. Load aggregate (uses latest version)
    const invoiceAgg = await InvoiceRepository.get(ctx, args.invoiceId);
    if (!invoiceAgg) {
      throw new Error("Invoice not found");
    }

    // 2. Apply business logic
    invoiceAgg.markAsOpen({ stripeId: args.stripeId });

    // 3. Persist
    const saved = await InvoiceRepository.save(ctx, invoiceAgg);
    return saved.getModel();
  },
});

export default openFromStripe;
```

## Why Business Logic Stays in Mutations

**Problem**: Actions don't run in a transaction. If you apply business logic in an action, you're working with stale data that may have changed.

**Solution**: Pass only IDs to mutations. The mutation loads the current state and applies changes transactionally.

```typescript
// ❌ Business logic in action (uses potentially stale invoice)
const sendInvoice = internalAction({
  handler: async (ctx, args) => {
    const response = await stripeClient.invoices.create(...);
    
    // BAD: invoice may have changed since action started
    const updatedInvoice = {
      ...args.invoice,
      status: "open",
      stripeId: response.id,
    };
    
    await ctx.runMutation(internal.billing.mutations.save.default, {
      invoice: updatedInvoice,
    });
  },
});

// ✅ Business logic in mutation (uses current state)
const sendInvoice = internalAction({
  handler: async (ctx, args) => {
    const response = await stripeClient.invoices.create(...);
    
    // GOOD: mutation loads current invoice and applies changes
    await ctx.runMutation(internal.billing.mutations.openFromStripe.default, {
      invoiceId: args.invoice._id,
      stripeId: response.id,
    });
  },
});
```

## Flow Pattern

The recommended flow for external API interactions:

```
UI executes mutation → [scheduled action → mutation] → UI query updates
```

### Example: Creating a Payment

```typescript
// 1. UI calls mutation to create intent
// convex/payment/mutations/createIntent.ts
const createIntent = mutation({
  args: { orderId: v.id("orders"), amount: v.number() },
  returns: PaymentModel,
  handler: async (ctx, args): Promise<Payment> => {
    // Create payment entity in "pending" state
    const paymentAgg = await PaymentRepository.create(ctx, {
      orderId: args.orderId,
      amount: args.amount,
      status: "pending",
    });

    // Schedule action to create Stripe PaymentIntent
    await ctx.scheduler.runAfter(
      0,
      internal.payment.adapters.createStripeIntent.default,
      { paymentId: paymentAgg.getModel()._id },
    );

    return paymentAgg.getModel();
  },
});

// 2. Action calls Stripe
// convex/payment/adapters/createStripeIntent.action.ts
const createStripeIntent = internalAction({
  args: { paymentId: v.id("payments") },
  returns: v.null(),
  handler: async (ctx, args): Promise<null> => {
    const payment = await ctx.runQuery(
      internal.payment.queries.getById.default,
      { paymentId: args.paymentId },
    );

    const intent = await stripeClient.paymentIntents.create({
      amount: payment.amount,
      currency: "usd",
    });

    await ctx.runMutation(
      internal.payment.mutations.updateFromStripe.default,
      {
        paymentId: args.paymentId,
        stripeIntentId: intent.id,
        clientSecret: intent.client_secret,
      },
    );

    return null;
  },
});

// 3. Mutation updates payment with Stripe data
// convex/payment/mutations/updateFromStripe.ts
const updateFromStripe = internalMutation({
  args: {
    paymentId: v.id("payments"),
    stripeIntentId: v.string(),
    clientSecret: v.string(),
  },
  returns: PaymentModel,
  handler: async (ctx, args): Promise<Payment> => {
    const paymentAgg = await PaymentRepository.get(ctx, args.paymentId);
    if (!paymentAgg) throw new Error("Payment not found");

    paymentAgg.linkStripeIntent(args.stripeIntentId, args.clientSecret);

    const saved = await PaymentRepository.save(ctx, paymentAgg);
    return saved.getModel();
  },
});

// 4. UI subscribes to payment updates
// UI queries payment status, sees updates reactively
```

## DTO Mapping Functions

For complex mappings, create dedicated functions:

```typescript
// convex/billing/_libs/stripeMapper.ts

import { Invoice } from "../domain/invoice.model";
import { Customer } from "../domain/customer.model";
import Stripe from "stripe";

export function toStripeInvoiceCreate(
  invoice: Invoice,
  customer: Customer,
): Stripe.InvoiceCreateParams {
  return {
    customer: customer.stripeId,
    auto_advance: false,
    collection_method: "send_invoice",
    days_until_due: invoice.paymentTermsDays,
    description: invoice.description,
    metadata: {
      invoiceId: invoice._id,
      accountId: invoice.accountId,
    },
  };
}

export function fromStripeInvoice(
  stripeInvoice: Stripe.Invoice,
): Partial<Invoice> {
  return {
    stripeId: stripeInvoice.id,
    status: mapStripeStatus(stripeInvoice.status),
    amountDue: stripeInvoice.amount_due,
    amountPaid: stripeInvoice.amount_paid,
  };
}

function mapStripeStatus(status: Stripe.Invoice.Status | null): InvoiceStatus {
  switch (status) {
    case "draft": return "draft";
    case "open": return "open";
    case "paid": return "paid";
    case "void": return "voided";
    default: return "unknown";
  }
}
```

## External Client Setup

Create client wrappers in `_libs/`:

```typescript
// convex/billing/_libs/stripeClient.ts
"use node";

import Stripe from "stripe";

const stripeClient = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-12-18.acacia",
});

export default stripeClient;
```

## Error Handling

Actions should handle external API failures gracefully:

```typescript
const syncWithCRM = internalAction({
  args: { contactId: v.id("contacts") },
  returns: v.null(),
  handler: async (ctx, args): Promise<null> => {
    try {
      const contact = await ctx.runQuery(...);
      await crmClient.contacts.upsert(mapToDTO(contact));
      
      await ctx.runMutation(internal.contact.mutations.markSynced.default, {
        contactId: args.contactId,
      });
    } catch (error) {
      // Log error, mark sync failed, possibly retry
      await ctx.runMutation(internal.contact.mutations.markSyncFailed.default, {
        contactId: args.contactId,
        error: String(error),
      });
      
      // Optionally re-throw to trigger Convex retry
      throw error;
    }

    return null;
  },
});
```
