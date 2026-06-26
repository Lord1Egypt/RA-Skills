# Examples

Complete examples demonstrating the DDD architecture patterns.

## Example 1: Invoice Sub-domain

### Directory Structure

```
convex/
  billing/
    _libs/
      stripeClient.ts
    _tables.ts
    _triggers.ts
    queries/
      getById.ts
      listByAccount.ts
    mutations/
      create.ts
      openFromStripe.ts
      markPaid.ts
    domain/
      invoice.model.ts
      invoice.repository.ts
    adapters/
      invoice.repository.ts
      sendToStripe.action.ts
```

### Domain Model

```typescript
// convex/billing/domain/invoice.model.ts
import { Infer, v } from "convex/values";
import { withoutSystemFields } from "convex-helpers";
import { IAggregate } from "../../_shared/libs/aggregate";

export const InvoiceStatusModel = v.union(
  v.literal("draft"),
  v.literal("open"),
  v.literal("paid"),
  v.literal("voided"),
);
export type InvoiceStatus = Infer<typeof InvoiceStatusModel>;

export const InvoiceModel = v.object({
  _id: v.id("invoices"),
  _creationTime: v.number(),
  accountId: v.id("accounts"),
  customerId: v.id("customers"),
  amount: v.number(),
  currency: v.string(),
  description: v.string(),
  status: InvoiceStatusModel,
  stripeId: v.optional(v.string()),
  paidAt: v.optional(v.number()),
  dueDate: v.number(),
});

export const NewInvoiceModel = v.object(withoutSystemFields(InvoiceModel.fields));
export type NewInvoice = Infer<typeof NewInvoiceModel>;
export type Invoice = Infer<typeof InvoiceModel>;

export class InvoiceAgg implements IAggregate<Invoice> {
  constructor(private invoice: Invoice) {}

  markAsOpen(params: { stripeId: string }) {
    if (this.invoice.status !== "draft") {
      throw new Error("Only draft invoices can be opened");
    }
    this.invoice.status = "open";
    this.invoice.stripeId = params.stripeId;
    return this;
  }

  markAsPaid() {
    if (this.invoice.status !== "open") {
      throw new Error("Only open invoices can be marked as paid");
    }
    this.invoice.status = "paid";
    this.invoice.paidAt = Date.now();
    return this;
  }

  void() {
    const canVoid = this.invoice.status === "draft" || this.invoice.status === "open";
    if (!canVoid) {
      throw new Error("Invoice cannot be voided");
    }
    this.invoice.status = "voided";
    return this;
  }

  get isOverdue() {
    return this.invoice.status === "open" && Date.now() > this.invoice.dueDate;
  }

  getModel(): Invoice {
    return this.invoice;
  }
}
```

### Repository Interface

```typescript
// convex/billing/domain/invoice.repository.ts
import { QueryCtx, MutationCtx } from "../../_generated/server";
import { IRepository } from "../../_shared/libs/repository";
import { Invoice, InvoiceAgg, InvoiceStatus } from "./invoice.model";

export interface IInvoiceRepository extends IRepository<"invoices", InvoiceAgg> {
  byAccount(
    ctx: QueryCtx,
    accountId: Invoice["accountId"],
    limit?: number,
  ): Promise<InvoiceAgg[]>;

  byCustomer(
    ctx: QueryCtx,
    customerId: Invoice["customerId"],
  ): Promise<InvoiceAgg[]>;

  listByStatus(
    ctx: QueryCtx,
    status: InvoiceStatus,
    limit?: number,
  ): Promise<InvoiceAgg[]>;

  listOverdue(ctx: QueryCtx): Promise<InvoiceAgg[]>;
}
```

### Repository Implementation

```typescript
// convex/billing/adapters/invoice.repository.ts
import { createRepository } from "../../_shared/libs/repository";
import { IInvoiceRepository } from "../domain/invoice.repository";
import { InvoiceAgg } from "../domain/invoice.model";

export const InvoiceRepository: IInvoiceRepository = {
  ...createRepository("invoices", (doc) => new InvoiceAgg(doc)),

  byAccount: async (ctx, accountId, limit = 50) => {
    const invoices = await ctx.db
      .query("invoices")
      .withIndex("by_account", (q) => q.eq("accountId", accountId))
      .order("desc")
      .take(limit);

    return invoices.map((inv) => new InvoiceAgg(inv));
  },

  byCustomer: async (ctx, customerId) => {
    const invoices = await ctx.db
      .query("invoices")
      .withIndex("by_customer", (q) => q.eq("customerId", customerId))
      .collect();

    return invoices.map((inv) => new InvoiceAgg(inv));
  },

  listByStatus: async (ctx, status, limit = 100) => {
    const invoices = await ctx.db
      .query("invoices")
      .withIndex("by_status", (q) => q.eq("status", status))
      .take(limit);

    return invoices.map((inv) => new InvoiceAgg(inv));
  },

  listOverdue: async (ctx) => {
    const now = Date.now();
    const openInvoices = await ctx.db
      .query("invoices")
      .withIndex("by_status", (q) => q.eq("status", "open"))
      .collect();

    return openInvoices
      .filter((inv) => inv.dueDate < now)
      .map((inv) => new InvoiceAgg(inv));
  },
};
```

### Tables Definition

```typescript
// convex/billing/_tables.ts
import { defineTable } from "convex/server";
import { withoutSystemFields } from "convex-helpers";
import { InvoiceModel } from "./domain/invoice.model";

export const billingTables = {
  invoices: defineTable(withoutSystemFields(InvoiceModel.fields))
    .index("by_account", ["accountId"])
    .index("by_customer", ["customerId"])
    .index("by_status", ["status"]),
};
```

### Mutation

```typescript
// convex/billing/mutations/create.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { pick } from "convex-helpers";
import { internal } from "../../_generated/api";
import { InvoiceModel, Invoice, NewInvoiceModel } from "../domain/invoice.model";
import { InvoiceRepository } from "../adapters/invoice.repository";

const create = mutation({
  args: {
    invoice: v.object(pick(NewInvoiceModel.fields, [
      "accountId",
      "customerId",
      "amount",
      "currency",
      "description",
      "dueDate",
    ])),
  },
  returns: InvoiceModel,
  handler: async (ctx, args): Promise<Invoice> => {
    // Create in draft status
    const invoiceAgg = await InvoiceRepository.create(ctx, {
      ...args.invoice,
      status: "draft",
    });

    // Schedule async send to Stripe
    await ctx.scheduler.runAfter(
      0,
      internal.billing.adapters.sendToStripe.default,
      { invoiceId: invoiceAgg.getModel()._id },
    );

    return invoiceAgg.getModel();
  },
});

export default create;
```

### Action Adapter

```typescript
// convex/billing/adapters/sendToStripe.action.ts
"use node";

import { internalAction } from "../../_generated/server";
import { internal } from "../../_generated/api";
import { v } from "convex/values";
import stripeClient from "../_libs/stripeClient";

const sendToStripe = internalAction({
  args: {
    invoiceId: v.id("invoices"),
  },
  returns: v.null(),
  handler: async (ctx, args): Promise<null> => {
    // Load current invoice data
    const invoice = await ctx.runQuery(
      internal.billing.queries.getById.default,
      { invoiceId: args.invoiceId },
    );

    if (!invoice) {
      throw new Error("Invoice not found");
    }

    // Load customer for Stripe ID
    const customer = await ctx.runQuery(
      internal.customer.queries.getById.default,
      { customerId: invoice.customerId },
    );

    if (!customer?.stripeId) {
      throw new Error("Customer has no Stripe ID");
    }

    // Map to Stripe DTO and create
    const stripeInvoice = await stripeClient.invoices.create({
      customer: customer.stripeId,
      auto_advance: true,
      collection_method: "send_invoice",
      days_until_due: Math.ceil((invoice.dueDate - Date.now()) / (1000 * 60 * 60 * 24)),
      description: invoice.description,
      metadata: { convexInvoiceId: invoice._id },
    });

    // Add line item
    await stripeClient.invoiceItems.create({
      invoice: stripeInvoice.id,
      customer: customer.stripeId,
      amount: invoice.amount,
      currency: invoice.currency,
      description: invoice.description,
    });

    // Finalize and send
    const finalizedInvoice = await stripeClient.invoices.finalizeInvoice(stripeInvoice.id);
    await stripeClient.invoices.sendInvoice(finalizedInvoice.id);

    // Update local invoice with Stripe ID
    await ctx.runMutation(
      internal.billing.mutations.openFromStripe.default,
      {
        invoiceId: args.invoiceId,
        stripeId: finalizedInvoice.id,
      },
    );

    return null;
  },
});

export default sendToStripe;
```

---

## Example 2: Contact Sub-domain with Triggers

### Trigger Setup

```typescript
// convex/contact/_triggers.ts
import { Change, Triggers } from "convex-helpers/server/triggers";
import { DataModel } from "../_generated/dataModel";
import { MutationCtx } from "../_generated/server";
import { internal } from "../_generated/api";

async function syncToCRM(ctx: MutationCtx, change: Change<DataModel, "contacts">) {
  if (change.operation === "delete") return;

  // Schedule async CRM sync
  await ctx.scheduler.runAfter(
    0,
    internal.contact.adapters.syncToCRM.default,
    { contactId: change.newDoc!._id },
  );
}

async function updateCompanyContactCount(
  ctx: MutationCtx,
  change: Change<DataModel, "contacts">,
) {
  const companyId = change.newDoc?.company ?? change.oldDoc?.company;
  if (!companyId) return;

  // Recalculate contact count
  const contacts = await ctx.db
    .query("contacts")
    .withIndex("by_company", (q) => q.eq("company", companyId))
    .collect();

  await ctx.db.patch(companyId, { contactCount: contacts.length });
}

export default function registerTriggers(triggers: Triggers<DataModel>) {
  triggers.register("contacts", async (ctx, change) => {
    await syncToCRM(ctx, change);
    await updateCompanyContactCount(ctx, change);
  });
}
```

---

## Example 3: Using pick() for Arguments

```typescript
// convex/contact/mutations/updateProfile.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { pick } from "convex-helpers";
import { ContactModel, Contact } from "../domain/contact.model";
import { ContactRepository } from "../adapters/contact.repository";

const updateProfile = mutation({
  args: {
    contactId: v.id("contacts"),
    // Pick only the fields that can be updated
    profile: v.object(
      pick(ContactModel.fields, [
        "firstName",
        "lastName",
        "email",
        "phoneNumber",
        "jobFunction",
        "title",
      ]),
    ),
  },
  returns: ContactModel,
  handler: async (ctx, args): Promise<Contact> => {
    const contactAgg = await ContactRepository.get(ctx, args.contactId);
    if (!contactAgg) {
      throw new Error("Contact not found");
    }

    contactAgg.updateProfile(args.profile);

    const saved = await ContactRepository.save(ctx, contactAgg);
    return saved.getModel();
  },
});

export default updateProfile;
```

---

## Example 4: Workflow for Multi-step Process

```typescript
// convex/order/_workflows.ts
import { workflow } from "../workflow";
import { internal } from "../_generated/api";
import { v } from "convex/values";

export const fulfillOrder = workflow.define({
  args: {
    orderId: v.id("orders"),
  },
  handler: async (step, args) => {
    // Step 1: Validate inventory
    const inventoryOk = await step.runAction(
      internal.inventory.actions.validateStock.default,
      { orderId: args.orderId },
    );

    if (!inventoryOk) {
      await step.runMutation(
        internal.order.mutations.markFailed.default,
        { orderId: args.orderId, reason: "Insufficient inventory" },
      );
      return;
    }

    // Step 2: Reserve inventory
    await step.runMutation(
      internal.inventory.mutations.reserve.default,
      { orderId: args.orderId },
    );

    // Step 3: Process payment
    const paymentResult = await step.runAction(
      internal.payment.actions.charge.default,
      { orderId: args.orderId },
    );

    if (!paymentResult.success) {
      // Rollback inventory reservation
      await step.runMutation(
        internal.inventory.mutations.release.default,
        { orderId: args.orderId },
      );
      
      await step.runMutation(
        internal.order.mutations.markFailed.default,
        { orderId: args.orderId, reason: paymentResult.error },
      );
      return;
    }

    // Step 4: Create shipment
    await step.runAction(
      internal.shipping.actions.createLabel.default,
      { orderId: args.orderId },
    );

    // Step 5: Mark as fulfilled
    await step.runMutation(
      internal.order.mutations.markFulfilled.default,
      { orderId: args.orderId },
    );
  },
});
```

### Starting the Workflow

```typescript
// convex/order/mutations/startFulfillment.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { fulfillOrder } from "../_workflows";
import { OrderModel, Order } from "../domain/order.model";
import { OrderRepository } from "../adapters/order.repository";

const startFulfillment = mutation({
  args: { orderId: v.id("orders") },
  returns: OrderModel,
  handler: async (ctx, args): Promise<Order> => {
    const orderAgg = await OrderRepository.get(ctx, args.orderId);
    if (!orderAgg) {
      throw new Error("Order not found");
    }

    orderAgg.startFulfillment();

    // Start the workflow
    await fulfillOrder.start(ctx, { orderId: args.orderId });

    const saved = await OrderRepository.save(ctx, orderAgg);
    return saved.getModel();
  },
});

export default startFulfillment;
```

---

## Example 5: RPG Game - Combat and Economy Domains

A real example demonstrating cross-domain communication via triggers, value objects, and aggregate state detection.

### Directory Structure

```
convex/
  _shared/
    _libs/
      aggregate.ts
      repository.ts
  _triggers.ts
  customFunctions.ts
  schema.ts
  combat/
    _tables.ts
    _triggers.ts
    domain/
      battle.model.ts
      battle.repository.ts
    adapters/
      battle.repository.ts
    mutations/
      createBattle.ts
      strikeMonster.ts
    queries/
      getActiveBattle.ts
  economy/
    _tables.ts
    domain/
      heroProfile.model.ts
      heroProfile.repository.ts
      equipment.model.ts          # Value Object
    adapters/
      heroProfile.repository.ts
    mutations/
      createHeroProfile.ts
      purchaseItem.ts
      rewardCredits.ts
    queries/
      getHeroProfile.ts
      getShopItems.ts
```

### Battle Aggregate with State Detection

```typescript
// convex/combat/domain/battle.model.ts
import { Infer, v } from "convex/values";
import { withoutSystemFields } from "convex-helpers";
import { IAggregate } from "../../_shared/_libs/aggregate";
import { Id } from "../../_generated/dataModel";

export const BattleStatusModel = v.union(
  v.literal("active"),
  v.literal("defeated"),
);

export const BattleModel = v.object({
  _id: v.id("battles"),
  _creationTime: v.number(),
  heroId: v.id("heroProfiles"),
  monsterHealth: v.number(),
  monsterMaxHealth: v.number(),
  monsterLevel: v.number(),
  status: BattleStatusModel,
});

export const NewBattleModel = v.object(withoutSystemFields(BattleModel.fields));
export type Battle = Infer<typeof BattleModel>;
export type NewBattle = Infer<typeof NewBattleModel>;

export class BattleAgg implements IAggregate<Battle> {
  constructor(private battle: Battle) {}

  // Factory method with implementation logic
  static create(heroId: Id<"heroProfiles">, level: number): NewBattle {
    const randomBetween = (min: number, max: number): number =>
      Math.floor(Math.random() * (max - min + 1)) + min;

    const healthMultiplier = randomBetween(10, 20);
    const monsterHealth = level * healthMultiplier;

    return {
      heroId,
      monsterHealth,
      monsterMaxHealth: monsterHealth,
      monsterLevel: level,
      status: "active",
    };
  }

  // Business method with validation
  takeDamage(attackPower: number): void {
    if (attackPower <= 0) {
      throw new Error("Attack power must be positive");
    }
    if (this.isDefeated) {
      throw new Error("Cannot attack a defeated monster");
    }

    this.battle.monsterHealth = Math.max(0, this.battle.monsterHealth - attackPower);

    if (this.battle.monsterHealth <= 0) {
      this.battle.status = "defeated";
    }
  }

  // Getters for state queries
  get isActive(): boolean {
    return this.battle.status === "active";
  }

  get isDefeated(): boolean {
    return this.battle.status === "defeated";
  }

  get heroId(): Id<"heroProfiles"> {
    return this.battle.heroId;
  }

  get monsterLevel(): number {
    return this.battle.monsterLevel;
  }

  // State transition detection for triggers
  wasSlainFrom(previousState: BattleAgg): boolean {
    return previousState.isActive && this.isDefeated;
  }

  getModel(): Battle {
    return this.battle;
  }
}
```

### Trigger with Aggregate-based Event Detection

```typescript
// convex/combat/_triggers.ts
import { Triggers, Change } from "convex-helpers/server/triggers";
import { DataModel } from "../_generated/dataModel";
import { MutationCtx } from "../_generated/server";
import { internal } from "../_generated/api";
import { BattleAgg } from "./domain/battle.model";

async function onMonsterSlain(
  ctx: MutationCtx,
  change: Change<DataModel, "battles">,
) {
  if (change.operation !== "update") return;
  if (!change.oldDoc || !change.newDoc) return;

  // Use aggregates to detect state transition
  const previousBattle = new BattleAgg(change.oldDoc);
  const currentBattle = new BattleAgg(change.newDoc);

  if (!currentBattle.wasSlainFrom(previousBattle)) return;

  // Cross-domain communication
  await ctx.runMutation(internal.economy.mutations.rewardCredits.default, {
    heroId: change.newDoc.heroId,
    monsterLevel: change.newDoc.monsterLevel,
  });
}

export default function registerCombatTriggers(triggers: Triggers<DataModel>) {
  triggers.register("battles", async (ctx, change) => {
    await onMonsterSlain(ctx, change);
  });
}
```

### Value Object for Equipment

```typescript
// convex/economy/domain/equipment.model.ts
import { Infer, v } from "convex/values";

export const EquipmentTypeModel = v.union(
  v.literal("weapon"),
  v.literal("consumable"),
);

// Value Object - no _id, not a database entity
export const EquipmentModel = v.object({
  id: v.string(),
  name: v.string(),
  type: EquipmentTypeModel,
  price: v.number(),
  attackBonus: v.optional(v.number()),
});

export type Equipment = Infer<typeof EquipmentModel>;

// Static catalog
export const SHOP_ITEMS: ReadonlyArray<Equipment> = [
  { id: "wooden_sword", name: "Wooden Sword", type: "weapon", price: 50, attackBonus: 5 },
  { id: "iron_sword", name: "Iron Sword", type: "weapon", price: 100, attackBonus: 10 },
] as const;

// Helper functions
export const findEquipmentById = (id: string): Equipment | undefined =>
  SHOP_ITEMS.find((item) => item.id === id);

export const calculateTotalAttackBonus = (equipmentIds: string[]): number =>
  equipmentIds.reduce((total, id) => {
    const item = findEquipmentById(id);
    return total + (item?.attackBonus ?? 0);
  }, 0);
```

### Mutation Using Value Object

```typescript
// convex/economy/mutations/purchaseItem.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { HeroProfileModel, HeroProfile } from "../domain/heroProfile.model";
import { HeroProfileRepository } from "../adapters/heroProfile.repository";
import { findEquipmentById } from "../domain/equipment.model";

const purchaseItem = mutation({
  args: {
    heroId: v.id("heroProfiles"),
    itemId: v.string(),
  },
  returns: HeroProfileModel,
  handler: async (ctx, args): Promise<HeroProfile> => {
    const heroAgg = await HeroProfileRepository.get(ctx, args.heroId);
    if (!heroAgg) {
      throw new Error("Hero not found");
    }

    // Look up value object from catalog
    const item = findEquipmentById(args.itemId);
    if (!item) {
      throw new Error(`Item "${args.itemId}" not found in shop`);
    }

    // Use aggregate method (validates credits, updates inventory)
    heroAgg.purchaseItem(item);
    await HeroProfileRepository.save(ctx, heroAgg);

    return heroAgg.getModel();
  },
});

export default purchaseItem;
```

### Query Returning Value Objects

```typescript
// convex/economy/queries/getShopItems.ts
import { query } from "../../customFunctions";
import { v } from "convex/values";
import { EquipmentModel, SHOP_ITEMS, Equipment } from "../domain/equipment.model";

const getShopItems = query({
  args: {},
  returns: v.array(EquipmentModel),
  handler: async (): Promise<Equipment[]> => {
    return [...SHOP_ITEMS];
  },
});

export default getShopItems;
```

### Cross-Domain Repository Access in Mutation

```typescript
// convex/combat/mutations/strikeMonster.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { BattleModel, Battle } from "../domain/battle.model";
import { BattleRepository } from "../adapters/battle.repository";
import { HeroProfileRepository } from "../../economy/adapters/heroProfile.repository";

const strikeMonster = mutation({
  args: {
    battleId: v.id("battles"),
    attackPower: v.number(),
  },
  returns: v.object({
    battle: BattleModel,
    isDefeated: v.boolean(),
  }),
  handler: async (ctx, args): Promise<{ battle: Battle; isDefeated: boolean }> => {
    const battleAgg = await BattleRepository.get(ctx, args.battleId);
    if (!battleAgg) {
      throw new Error("Battle not found");
    }

    // Business logic in aggregate
    battleAgg.takeDamage(args.attackPower);
    await BattleRepository.save(ctx, battleAgg);

    // Cross-domain access when defeated
    if (battleAgg.isDefeated) {
      const heroAgg = await HeroProfileRepository.get(ctx, battleAgg.heroId);
      if (heroAgg) {
        heroAgg.rewardCredits(battleAgg.monsterLevel);
        await HeroProfileRepository.save(ctx, heroAgg);
      }
    }

    return {
      battle: battleAgg.getModel(),
      isDefeated: battleAgg.isDefeated,
    };
  },
});

export default strikeMonster;
```
