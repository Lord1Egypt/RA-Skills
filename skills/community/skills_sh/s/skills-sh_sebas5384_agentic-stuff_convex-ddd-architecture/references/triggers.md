# Triggers Reference

Triggers react to database changes using `convex-helpers/server/triggers`.

## Setup

### 1. Create Central Trigger Registry

```typescript
// convex/_triggers.ts
import { Triggers } from "convex-helpers/server/triggers";
import { DataModel } from "./_generated/dataModel";
import registerCombatTriggers from "./combat/_triggers";
import registerEconomyTriggers from "./economy/_triggers";

// Central trigger registry
export const triggers = new Triggers<DataModel>();

// Register triggers from each sub-domain
registerCombatTriggers(triggers);
registerEconomyTriggers(triggers);

export default triggers;
```

### 2. Integrate with Custom Functions

```typescript
// convex/customFunctions.ts
import {
  customMutation,
  customCtx,
} from "convex-helpers/server/customFunctions";
import {
  mutation as rawMutation,
  internalMutation as rawInternalMutation,
  query as rawQuery,
} from "./_generated/server";
import triggers from "./_triggers";

// Mutations wrapped with trigger support
export const mutation = customMutation(rawMutation, customCtx(triggers.wrapDB));
export const internalMutation = customMutation(
  rawInternalMutation,
  customCtx(triggers.wrapDB),
);

// Queries don't need wrapping
export const query = rawQuery;
```

See [custom-functions.md](custom-functions.md) for complete setup.

### 2. Define Triggers in Sub-domain

```typescript
// convex/project/_triggers.ts
import { Change, Triggers } from "convex-helpers/server/triggers";
import { DataModel } from "../_generated/dataModel";
import { MutationCtx } from "../_generated/server";
import { internal } from "../_generated/api";

async function onProjectCreate(
  ctx: MutationCtx,
  change: Change<DataModel, "projects">,
) {
  if (change.operation !== "insert") return;

  const project = change.newDoc;
  
  // Create related entities
  await ctx.db.insert("projectSettings", {
    projectId: project._id,
    notifications: true,
    visibility: "private",
  });
}

async function onProjectStatusChange(
  ctx: MutationCtx,
  change: Change<DataModel, "projects">,
) {
  if (change.operation !== "update") return;
  
  const statusChanged = change.oldDoc.status !== change.newDoc.status;
  if (!statusChanged) return;

  // Non-blocking: schedule workflow
  await ctx.scheduler.runAfter(
    0,
    internal.project.workflows.notifyStatusChange.start,
    {
      projectId: change.newDoc._id,
      oldStatus: change.oldDoc.status,
      newStatus: change.newDoc.status,
    },
  );
}

export default function registerTriggers(triggers: Triggers<DataModel>) {
  triggers.register("projects", async (ctx, change) => {
    await onProjectCreate(ctx, change);
    await onProjectStatusChange(ctx, change);
  });
}
```

## Change Object

The `Change` type provides access to:

```typescript
type Change<DataModel, TableName> = {
  operation: "insert" | "update" | "delete";
  oldDoc: Doc<TableName> | undefined; // undefined on insert
  newDoc: Doc<TableName> | undefined; // undefined on delete
  id: Id<TableName>;
};
```

### Checking Operation Type

```typescript
async function handleChange(ctx: MutationCtx, change: Change<DataModel, "orders">) {
  switch (change.operation) {
    case "insert":
      // change.newDoc is defined, change.oldDoc is undefined
      console.log("New order:", change.newDoc);
      break;
      
    case "update":
      // Both oldDoc and newDoc are defined
      console.log("Order updated from", change.oldDoc, "to", change.newDoc);
      break;
      
    case "delete":
      // change.oldDoc is defined, change.newDoc is undefined
      console.log("Order deleted:", change.oldDoc);
      break;
  }
}
```

## Best Practices

### 1. Triggers Run in Transaction

**Caution**: Trigger code runs within the same transaction as the mutation that caused the change. If a trigger fails, the entire transaction rolls back.

```typescript
// ⚠️ This will block the mutation and rollback on failure
triggers.register("orders", async (ctx, change) => {
  // Don't do heavy synchronous work here
  await someHeavyComputation();
});
```

### 2. Use Scheduler for Non-blocking Work

```typescript
// ✅ Schedule async work to not block the mutation
triggers.register("orders", async (ctx, change) => {
  if (change.operation !== "insert") return;

  await ctx.scheduler.runAfter(
    0,
    internal.orders.actions.syncToWarehouse.default,
    { orderId: change.newDoc._id },
  );
});
```

### 3. Keep Triggers Focused

Each trigger should handle one concern:

```typescript
// ✅ Separate triggers for separate concerns
async function createDefaultSettings(ctx, change) { /* ... */ }
async function notifyTeam(ctx, change) { /* ... */ }
async function updateMetrics(ctx, change) { /* ... */ }

export default function registerTriggers(triggers: Triggers<DataModel>) {
  triggers.register("projects", async (ctx, change) => {
    await createDefaultSettings(ctx, change);
    await notifyTeam(ctx, change);
    await updateMetrics(ctx, change);
  });
}
```

### 4. Check for Specific Field Changes

```typescript
async function onStatusChange(ctx: MutationCtx, change: Change<DataModel, "orders">) {
  if (change.operation !== "update") return;
  
  // Only react if status actually changed
  const statusChanged = change.oldDoc?.status !== change.newDoc?.status;
  if (!statusChanged) return;

  // Handle status change
  // ...
}
```

### 5. Avoid Infinite Loops

Be careful not to create circular triggers:

```typescript
// ❌ Dangerous: trigger A updates table B, trigger B updates table A
triggers.register("tableA", async (ctx, change) => {
  await ctx.db.patch(relatedBId, { /* ... */ }); // Triggers tableB trigger
});

triggers.register("tableB", async (ctx, change) => {
  await ctx.db.patch(relatedAId, { /* ... */ }); // Triggers tableA trigger → loop!
});

// ✅ Use flags or checks to prevent loops
triggers.register("tableA", async (ctx, change) => {
  if (change.newDoc?.syncedFromB) return; // Skip if update came from B
  
  await ctx.db.patch(relatedBId, {
    data: change.newDoc?.data,
    syncedFromA: true,
  });
});
```

## Testing Considerations

Triggers execute during tests too. Plan accordingly:

```typescript
// In tests, triggers will fire on mutations
test("creating order creates settings", async () => {
  const orderId = await ctx.runMutation(api.orders.create, { /* ... */ });
  
  // Trigger should have created settings
  const settings = await ctx.runQuery(api.orderSettings.byOrder, { orderId });
  expect(settings).toBeDefined();
});
```

## Common Patterns

### Audit Trail

```typescript
triggers.register("documents", async (ctx, change) => {
  await ctx.db.insert("auditLog", {
    tableName: "documents",
    documentId: change.id,
    operation: change.operation,
    oldValue: change.oldDoc,
    newValue: change.newDoc,
    timestamp: Date.now(),
  });
});
```

### Cascading Deletes

```typescript
triggers.register("projects", async (ctx, change) => {
  if (change.operation !== "delete") return;

  // Delete related entities
  const tasks = await ctx.db
    .query("tasks")
    .withIndex("by_project", (q) => q.eq("projectId", change.id))
    .collect();

  for (const task of tasks) {
    await ctx.db.delete(task._id);
  }
});
```

### Denormalization / Derived Data

```typescript
triggers.register("orderItems", async (ctx, change) => {
  // Recalculate order total when items change
  const orderId = change.newDoc?.orderId ?? change.oldDoc?.orderId;
  if (!orderId) return;

  const items = await ctx.db
    .query("orderItems")
    .withIndex("by_order", (q) => q.eq("orderId", orderId))
    .collect();

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  await ctx.db.patch(orderId, { totalAmount: total });
});
```

### Event Detection Using Aggregates

Use Aggregates to detect state transitions in triggers. This keeps domain logic in the aggregate, not scattered in trigger code.

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

  // Create aggregates from old and new state
  const previousBattle = new BattleAgg(change.oldDoc);
  const currentBattle = new BattleAgg(change.newDoc);

  // Use aggregate method to detect state transition
  if (!currentBattle.wasSlainFrom(previousBattle)) return;

  // Cross-domain communication via internal mutation
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

The aggregate provides the `wasSlainFrom` method:

```typescript
// In battle.model.ts
class BattleAgg {
  get isActive(): boolean {
    return this.battle.status === "active";
  }

  get isDefeated(): boolean {
    return this.battle.status === "defeated";
  }

  wasSlainFrom(previousState: BattleAgg): boolean {
    return previousState.isActive && this.isDefeated;
  }
}
```

**Benefits:**
- Domain logic stays in the aggregate
- Trigger code is simple and declarative
- State transition logic is testable without triggers

### Cross-Domain Communication

Use `ctx.runMutation` with internal mutations for cross-domain events:

```typescript
// In combat trigger, call economy mutation
await ctx.runMutation(internal.economy.mutations.rewardCredits.default, {
  heroId: change.newDoc.heroId,
  monsterLevel: change.newDoc.monsterLevel,
});
```

The internal mutation in the other domain handles the business logic:

```typescript
// convex/economy/mutations/rewardCredits.ts
import { internalMutation } from "../../customFunctions";

const rewardCredits = internalMutation({
  args: {
    heroId: v.id("heroProfiles"),
    monsterLevel: v.number(),
  },
  handler: async (ctx, args) => {
    const heroAgg = await HeroProfileRepository.get(ctx, args.heroId);
    if (!heroAgg) throw new Error("Hero not found");

    heroAgg.rewardCredits(args.monsterLevel);
    await HeroProfileRepository.save(ctx, heroAgg);

    return heroAgg.getModel();
  },
});

export default rewardCredits;
```

**Note:** The cross-domain mutation runs in the same transaction as the trigger, ensuring consistency.
