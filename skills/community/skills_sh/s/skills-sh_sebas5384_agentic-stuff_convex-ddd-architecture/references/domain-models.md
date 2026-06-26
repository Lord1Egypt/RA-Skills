# Domain Models Reference

Domain models represent business concepts and encapsulate business logic through Aggregates.

## File Structure

```typescript
// convex/[subDomain]/domain/[modelName].model.ts

import { Infer, v } from "convex/values";
import { withoutSystemFields } from "convex-helpers";
import { IAggregate } from "../../_shared/libs/aggregate";

// 1. Define field-level validators for complex types
export const RecordStatusModel = v.union(
  v.literal("draft"),
  v.literal("published"),
  v.literal("archived"),
);
export type RecordStatus = Infer<typeof RecordStatusModel>;

// 2. Define the full model with system fields
export const RecordModel = v.object({
  _id: v.id("records"),
  _creationTime: v.number(),
  parentId: v.id("workspaces"),
  title: v.string(),
  description: v.optional(v.string()),
  timelineStart: v.number(),
  timelineEnd: v.union(v.number(), v.null()),
  status: RecordStatusModel,
  publishedAt: v.optional(v.number()),
});

// 3. Define the "new" model without system fields
export const NewRecordModel = v.object(withoutSystemFields(RecordModel.fields));

// 4. Export inferred types
export type NewRecord = Infer<typeof NewRecordModel>;
export type RecordEntity = Infer<typeof RecordModel>;

// 5. Define the Aggregate class
export class RecordAgg implements IAggregate<RecordEntity> {
  constructor(private record: RecordEntity) {}

  // State transitions with invariant checks
  publish() {
    if (this.record.status !== "draft") {
      throw new Error("Only draft records can be published");
    }
    this.record.status = "published";
    this.record.publishedAt = Date.now();
    return this;
  }

  archive() {
    const canArchive = this.record.status === "draft" || this.record.status === "published";
    if (!canArchive) {
      throw new Error("Record cannot be archived from current status");
    }
    this.record.status = "archived";
    return this;
  }

  updateTimeline(start: number, end: number | null) {
    if (end !== null && end < start) {
      throw new Error("Timeline end must be after start");
    }
    this.record.timelineStart = start;
    this.record.timelineEnd = end;
    return this;
  }

  // Getters for derived values
  get isActive() {
    return this.record.status === "published";
  }

  get durationDays() {
    if (!this.record.timelineEnd) return null;
    return Math.ceil((this.record.timelineEnd - this.record.timelineStart) / (1000 * 60 * 60 * 24));
  }

  // Required: return the underlying model
  getModel(): RecordEntity {
    return this.record;
  }
}
```

## Rules

### 1. Always Include System Fields

```typescript
// ✅ Correct
export const ContactModel = v.object({
  _id: v.id("contacts"),
  _creationTime: v.number(),
  name: v.string(),
});

// ❌ Missing system fields
export const ContactModel = v.object({
  name: v.string(),
});
```

### 2. Export New Model Without System Fields

Use `withoutSystemFields` from `convex-helpers`:

```typescript
export const NewContactModel = v.object(withoutSystemFields(ContactModel.fields));
export type NewContact = Infer<typeof NewContactModel>;
```

### 3. Complex Fields Get Dedicated Validators

```typescript
// ✅ Extracted validator for status
export const OrderStatusModel = v.union(
  v.literal("pending"),
  v.literal("processing"),
  v.literal("shipped"),
  v.literal("delivered"),
);
export type OrderStatus = Infer<typeof OrderStatusModel>;

// ❌ Inline complex type
export const OrderModel = v.object({
  status: v.union(v.literal("pending"), v.literal("processing"), ...), // Hard to reuse
});
```

### 4. Avoid Manual Type Definitions

```typescript
// ✅ Infer from validator
export type Contact = Infer<typeof ContactModel>;

// ❌ Manual type (can drift from validator)
export type Contact = {
  _id: Id<"contacts">;
  _creationTime: number;
  name: string;
};
```

### 5. API shapes (DTOs) vs domain models

**Domain `domain/` holds persisted shapes**: `*Model`, `New*Model`, aggregates. **Do not** put query or mutation **DTO** definitions there—DTOs describe a specific function’s `args` / `returns` wire contract and belong **in that query or mutation file** (or beside it if split for size). Name local DTO `v.object(...)` values with a `*Dto` suffix when helpful for readability.

Do **not** add channel- or feature-specific picks of a model (for example `WorkItemModel.pick(...)` for an assistant tool) to `domain/*.model.ts`—those belong next to the handler that returns them.

When a return or argument shape is a **subset or extension of a table document**, derive it in the handler file from the domain model using `SomeModel.pick(...).extend({ ... })` so it cannot drift from the model. Reusability across the domain is for **models**, not for API DTOs.

When **several queries in the same module** share one composite wire shape, factor it into **a single file next to those queries** (for example `queries/boardStructure.dtos.ts`), not under `domain/`.

## Aggregate Pattern

### Purpose

Aggregates:
- Enforce business invariants
- Manage state transitions
- Provide domain-specific methods
- Keep business logic testable

### Structure

```typescript
interface IAggregate<T> {
  getModel(): T;
}

class OrderAgg implements IAggregate<Order> {
  constructor(private order: Order) {}

  // Static factory method for creating new entities
  static create(customerId: Id<"customers">, items: OrderItem[]): NewOrder {
    return {
      customerId,
      items,
      status: "pending",
      totalAmount: items.reduce((sum, i) => sum + i.price, 0),
    };
  }

  // Business operations as methods
  confirm() { /* ... */ }
  ship(trackingNumber: string) { /* ... */ }
  deliver() { /* ... */ }
  cancel(reason: string) { /* ... */ }

  // Derived state
  get canCancel() { /* ... */ }
  get totalValue() { /* ... */ }

  getModel(): Order {
    return this.order;
  }
}
```

### Static Factory Method

Use a static `create` method to construct new entities:

```typescript
class BattleAgg implements IAggregate<Battle> {
  constructor(private battle: Battle) {}

  // Factory method returns NewModel (without system fields)
  static create(heroId: Id<"heroProfiles">, level: number): NewBattle {
    // Implementation logic belongs HERE, not in mutations
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
}
```

Usage in mutations:

```typescript
const createBattle = mutation({
  handler: async (ctx, args) => {
    const newBattle = BattleAgg.create(args.heroId, args.level);
    const battleAgg = await BattleRepository.create(ctx, newBattle);
    return battleAgg.getModel();
  },
});
```

### Encapsulating Domain Logic

Keep all business logic inside aggregates, not in mutations.

**Use getters instead of direct field access:**

```typescript
// ✅ Correct - encapsulated in aggregate
class BattleAgg {
  get isDefeated(): boolean {
    return this.battle.status === "defeated";
  }

  get isActive(): boolean {
    return this.battle.status === "active";
  }
}

// In mutation:
if (battleAgg.isDefeated) { ... }

// ❌ Wrong - leaking domain logic
if (battle.status === "defeated") { ... }
```

**Validation belongs in aggregate methods:**

```typescript
// ✅ Correct - validation inside aggregate
class BattleAgg {
  takeDamage(attackPower: number): void {
    if (attackPower <= 0) {
      throw new Error("Attack power must be positive");
    }
    if (this.isDefeated) {
      throw new Error("Cannot attack a defeated monster");
    }
    this.battle.monsterHealth = Math.max(0, this.battle.monsterHealth - attackPower);
    if (this.battle.monsterHealth <= 0) {
      this.markDefeated();
    }
  }
}

// ❌ Wrong - validation in mutation
if (args.attackPower <= 0) throw new Error("...");
battleAgg.takeDamage(args.attackPower);
```

**Void returns for mutation methods:**

Let consumers check state via getters instead of returning booleans:

```typescript
// ✅ Correct - void return, consumer uses getter
class BattleAgg {
  takeDamage(attackPower: number): void {
    // ... apply damage ...
  }
}

// In mutation:
battleAgg.takeDamage(args.attackPower);
if (battleAgg.isDefeated) {
  // handle defeat
}

// ❌ Wrong - returning boolean
takeDamage(attackPower: number): boolean {
  // ... apply damage ...
  return this.isDefeated; // Implicit coupling
}
```

**Private helper methods:**

```typescript
class HeroProfileAgg {
  purchaseItem(item: Equipment): void {
    this.hero.credits -= item.price;
    this.hero.inventory.push(item.id);
    if (item.type === "weapon") {
      this.recalculateAttackPower(); // Private helper
    }
  }

  private recalculateAttackPower(): void {
    const weaponBonus = calculateTotalAttackBonus(this.hero.inventory);
    this.hero.attackPower = BASE_ATTACK_POWER + weaponBonus;
  }
}
```

**Boolean query methods:**

```typescript
class HeroProfileAgg {
  canAfford(price: number): boolean {
    return this.hero.credits >= price;
  }

  ownsItem(itemId: string): boolean {
    return this.hero.inventory.includes(itemId);
  }
}
```

### State Transition Detection

For triggers or cross-domain events, add methods to detect state changes:

```typescript
class BattleAgg {
  // Detect if monster was just slain (comparing previous state)
  wasSlainFrom(previousState: BattleAgg): boolean {
    return previousState.isActive && this.isDefeated;
  }
}

// Usage in triggers:
const previousBattle = new BattleAgg(change.oldDoc);
const currentBattle = new BattleAgg(change.newDoc);

if (currentBattle.wasSlainFrom(previousBattle)) {
  // Monster was just slain - reward the hero
}
```

### Module-level Constants

Define business constants at the module level:

```typescript
// convex/economy/domain/heroProfile.model.ts
const BASE_ATTACK_POWER = 10;
const CREDITS_PER_LEVEL = 10;

export class HeroProfileAgg {
  static create(name: string): NewHeroProfile {
    return {
      name,
      credits: 0,
      attackPower: BASE_ATTACK_POWER,
      inventory: [],
    };
  }

  rewardCredits(monsterLevel: number): void {
    this.hero.credits += monsterLevel * CREDITS_PER_LEVEL;
  }
}
```

### Using Aggregates in Mutations

```typescript
const confirmOrder = internalMutation({
  args: { orderId: v.id("orders") },
  returns: OrderModel,
  handler: async (ctx, args): Promise<Order> => {
    // 1. Load via repository (returns Aggregate)
    const orderAgg = await OrderRepository.get(ctx, args.orderId);
    
    // 2. Apply business logic
    orderAgg.confirm();
    
    // 3. Persist via repository
    return OrderRepository.save(ctx, orderAgg);
  },
});
```

## Table Schema Integration

Export the model from `_tables.ts`:

```typescript
// convex/order/_tables.ts
import { defineTable } from "convex/server";
import { withoutSystemFields } from "convex-helpers";
import { OrderModel } from "./domain/order.model";

export const orderTables = {
  orders: defineTable(withoutSystemFields(OrderModel.fields))
    .index("by_customer", ["customerId"])
    .index("by_status", ["status"]),
};
```

Then compose in the main schema:

```typescript
// convex/schema.ts
import { defineSchema } from "convex/server";
import { orderTables } from "./order/_tables";
import { customerTables } from "./customer/_tables";

export default defineSchema({
  ...orderTables,
  ...customerTables,
});
```

## Testing Aggregates

Aggregates can be unit tested without Convex:

```typescript
describe("OrderAgg", () => {
  it("should transition from pending to confirmed", () => {
    const order = createMockOrder({ status: "pending" });
    const agg = new OrderAgg(order);
    
    agg.confirm();
    
    expect(agg.getModel().status).toBe("confirmed");
  });

  it("should throw when confirming shipped order", () => {
    const order = createMockOrder({ status: "shipped" });
    const agg = new OrderAgg(order);
    
    expect(() => agg.confirm()).toThrow("Cannot confirm shipped order");
  });
});
```

## Turn-Based State Management

For turn-based game mechanics (like ATB combat systems), use FIFO queue patterns in domain models.

### Queue-Based Turn System

Use a circular queue to manage turn order:

```typescript
export const TurnActorModel = v.union(v.literal("hero"), v.literal("monster"));
export type TurnActor = Infer<typeof TurnActorModel>;

export class BattleAgg implements IAggregate<Battle> {
  /**
   * Generates a turn queue based on game difficulty.
   * Higher level = more monster turns per hero turn.
   */
  static generateTurnQueue(monsterLevel: number): TurnActor[] {
    const isLowLevel = monsterLevel <= 2;
    const isMidLevel = monsterLevel >= 3 && monsterLevel <= 5;
    const isHighLevel = monsterLevel >= 6 && monsterLevel <= 9;

    if (isLowLevel) {
      return ["hero", "hero", "monster"]; // 2:1 ratio
    }
    if (isMidLevel) {
      return ["hero", "monster"]; // 1:1 balanced
    }
    if (isHighLevel) {
      return ["hero", "monster", "monster"]; // 1:2 ratio
    }
    // Level 10+: Very hard
    return ["hero", "monster", "monster", "monster"]; // 1:3 ratio
  }

  /**
   * Get the current turn actor from the queue.
   */
  get currentTurn(): TurnActor {
    const turnQueue = this.safeTurnQueue;
    const currentIndex = this.safeCurrentTurnIndex;
    return turnQueue[currentIndex];
  }

  /**
   * Advance to the next turn in the queue.
   * Wraps around when reaching the end (creates infinite loop).
   */
  advanceTurn(): void {
    if (!this.isActive) {
      return; // Don't advance if battle is over
    }

    const turnQueue = this.safeTurnQueue;
    const currentIndex = this.safeCurrentTurnIndex;
    const nextIndex = currentIndex + 1;
    this.battle.currentTurnIndex = nextIndex % turnQueue.length;
  }

  get isHeroTurn(): boolean {
    return this.isActive && this.currentTurn === "hero";
  }

  get isMonsterTurn(): boolean {
    return this.isActive && this.currentTurn === "monster";
  }
}
```

**Key patterns:**

1. **Static factory method** - `generateTurnQueue()` creates the queue based on game state
2. **Circular queue** - Use modulo operator to wrap around: `nextIndex % turnQueue.length`
3. **State checks** - Use getters (`isHeroTurn`, `isMonsterTurn`) instead of direct field access
4. **Turn validation** - Mutations validate whose turn it is before allowing actions

**Usage in mutations:**

```typescript
const strikeMonster = mutation({
  handler: async (ctx, args) => {
    const battleAgg = await BattleRepository.get(ctx, args.battleId);
    
    // Validate it's the hero's turn
    if (!battleAgg.isHeroTurn) {
      throw new Error("It's not the hero's turn");
    }

    battleAgg.takeDamage(args.attackPower);
    
    // Advance turn queue after action
    if (battleAgg.isActive) {
      battleAgg.advanceTurn();
    }

    await BattleRepository.save(ctx, battleAgg);
    return {
      battle: battleAgg.getModel(),
      nextTurn: battleAgg.currentTurn,
    };
  },
});
```

**Benefits:**

- Turn order is deterministic and predictable
- Easy to adjust difficulty by changing queue ratios
- State is encapsulated in the aggregate
- Mutations can validate turn order before allowing actions

## Value Objects

Not all domain objects need an Aggregate class. For immutable objects defined by their attributes (not identity), use Value Objects. See [value-objects.md](value-objects.md).

Examples: Equipment catalogs, money, addresses, configuration objects.
