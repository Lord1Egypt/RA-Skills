# Value Objects

Value Objects are immutable domain objects defined by their attributes, not by a unique identity. Unlike Entities (which have an `_id` and are stored in the database), Value Objects represent concepts that are interchangeable when their values are equal.

## When to Use Value Objects

Use Value Objects for:

- **Static catalog data** (equipment, item types, categories)
- **Configuration objects** (settings, rules)
- **Composite values** (money, address, coordinates)
- **Enumerations with data** (status types with metadata)

## Structure

### Basic Value Object

```typescript
// convex/economy/domain/equipment.model.ts
import { Infer, v } from "convex/values";

// Type discriminator as a separate validator
export const EquipmentTypeModel = v.union(
  v.literal("weapon"),
  v.literal("consumable"),
);
export type EquipmentType = Infer<typeof EquipmentTypeModel>;

// Value Object model - note: NO v.id() field
export const EquipmentModel = v.object({
  id: v.string(),        // String identifier, NOT v.id("tableName")
  name: v.string(),
  type: EquipmentTypeModel,
  price: v.number(),
  attackBonus: v.optional(v.number()),
  healAmount: v.optional(v.number()),
});

export type Equipment = Infer<typeof EquipmentModel>;
```

### Key Characteristics

1. **No `_id` field**: Value Objects use a simple `id: v.string()` instead of `v.id("tableName")`
2. **No `_creationTime`**: Not a database entity
3. **No Aggregate class**: Logic lives in helper functions, not class methods
4. **Immutable**: Create new instances instead of mutating

## Static Catalog Data

Value Objects often represent static data that doesn't change at runtime:

```typescript
// Static catalog using ReadonlyArray and as const
export const SHOP_ITEMS: ReadonlyArray<Equipment> = [
  {
    id: "wooden_sword",
    name: "Wooden Sword",
    type: "weapon",
    price: 50,
    attackBonus: 5,
  },
  {
    id: "iron_sword",
    name: "Iron Sword",
    type: "weapon",
    price: 100,
    attackBonus: 10,
  },
  {
    id: "health_potion",
    name: "Health Potion",
    type: "consumable",
    price: 25,
    healAmount: 20,
  },
] as const;
```

Benefits:
- Type-safe at compile time
- No database queries needed
- Easy to test
- Clear separation from dynamic data

## Helper Functions

Instead of Aggregate methods, Value Objects use standalone helper functions:

```typescript
/**
 * Find an equipment item by its ID.
 */
export const findEquipmentById = (id: string): Equipment | undefined =>
  SHOP_ITEMS.find((item) => item.id === id);

/**
 * Calculate total attack bonus from a list of equipment IDs.
 */
export const calculateTotalAttackBonus = (equipmentIds: string[]): number =>
  equipmentIds.reduce((total, id) => {
    const item = findEquipmentById(id);
    return total + (item?.attackBonus ?? 0);
  }, 0);

/**
 * Get all weapons from the catalog.
 */
export const getWeapons = (): Equipment[] =>
  SHOP_ITEMS.filter((item) => item.type === "weapon");

/**
 * Check if an item exists in the catalog.
 */
export const isValidItemId = (id: string): boolean =>
  SHOP_ITEMS.some((item) => item.id === id);
```

## Using in Aggregates

Aggregates can use Value Objects for internal calculations:

```typescript
// convex/economy/domain/heroProfile.model.ts
import { Equipment, calculateTotalAttackBonus } from "./equipment.model";

const BASE_ATTACK_POWER = 10;

export class HeroProfileAgg implements IAggregate<HeroProfile> {
  constructor(private hero: HeroProfile) {}

  purchaseItem(item: Equipment): void {
    if (!this.canAfford(item.price)) {
      throw new Error(`Insufficient credits`);
    }

    this.hero.credits -= item.price;
    this.hero.inventory.push(item.id);

    if (item.type === "weapon") {
      this.recalculateAttackPower();
    }
  }

  private recalculateAttackPower(): void {
    // Uses Value Object helper function
    const weaponBonus = calculateTotalAttackBonus(this.hero.inventory);
    this.hero.attackPower = BASE_ATTACK_POWER + weaponBonus;
  }
}
```

## Using in Queries

Return Value Objects directly without database access:

```typescript
// convex/economy/queries/getShopItems.ts
import { query } from "../../customFunctions";
import { v } from "convex/values";
import { EquipmentModel, SHOP_ITEMS, Equipment } from "../domain/equipment.model";

const getShopItems = query({
  args: {},
  returns: v.array(EquipmentModel),
  handler: async (): Promise<Equipment[]> => {
    // Return a copy to prevent mutation
    return [...SHOP_ITEMS];
  },
});

export default getShopItems;
```

## Using in Mutations

Validate and look up Value Objects:

```typescript
// convex/economy/mutations/purchaseItem.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";
import { findEquipmentById } from "../domain/equipment.model";
import { HeroProfileRepository } from "../adapters/heroProfile.repository";

const purchaseItem = mutation({
  args: {
    heroId: v.id("heroProfiles"),
    itemId: v.string(),  // String ID, not v.id()
  },
  handler: async (ctx, args) => {
    const heroAgg = await HeroProfileRepository.get(ctx, args.heroId);
    if (!heroAgg) {
      throw new Error("Hero not found");
    }

    // Look up Value Object from catalog
    const item = findEquipmentById(args.itemId);
    if (!item) {
      throw new Error(`Item "${args.itemId}" not found in shop`);
    }

    // Use Value Object in aggregate method
    heroAgg.purchaseItem(item);
    await HeroProfileRepository.save(ctx, heroAgg);

    return heroAgg.getModel();
  },
});

export default purchaseItem;
```

## Value Objects vs Entities

| Aspect | Value Object | Entity (Aggregate) |
|--------|--------------|-------------------|
| Identity | Defined by values | Has unique `_id` |
| Storage | Static/in-memory | Database table |
| Mutability | Immutable | Mutable via methods |
| Logic | Helper functions | Class methods |
| Example | Equipment, Money | HeroProfile, Battle |

## Complex Value Objects

For Value Objects with behavior, you can still use classes:

```typescript
// Money value object with behavior
export class Money {
  constructor(
    public readonly amount: number,
    public readonly currency: string,
  ) {
    if (amount < 0) throw new Error("Amount cannot be negative");
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error("Cannot add different currencies");
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

The key difference from Aggregates: Value Objects are compared by value, not identity, and create new instances instead of mutating.
