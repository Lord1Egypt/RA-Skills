# Repository Pattern Reference

Repositories abstract database access and return Aggregates to enforce domain boundaries.

> **Important**: Repository adapters (in `adapters/`) are the **only** place allowed to use direct `ctx.db` operations (`insert`, `patch`, `replace`, `delete`, `get`, `query`). All other code must go through repositories. This is enforced by ESLint rules. See [eslint-rules.md](eslint-rules.md).

## Structure

### Interface (in domain/)

```typescript
// convex/contact/domain/contact.repository.ts
import { QueryCtx, MutationCtx } from "../../_generated/server";
import { IRepository } from "../../_shared/libs/repository";
import { Contact, ContactAgg } from "./contact.model";

export interface IContactRepository extends IRepository<"contacts", ContactAgg> {
  // Custom query methods
  byCompany(
    ctx: QueryCtx,
    clause: { company: Contact["company"] },
    limit?: number,
  ): Promise<ContactAgg[]>;

  byAccount(
    ctx: QueryCtx,
    clause: {
      account: Contact["account"];
      company?: Contact["company"];
    },
    limit?: number,
  ): Promise<ContactAgg[]>;

  listActive(ctx: QueryCtx, limit?: number): Promise<ContactAgg[]>;
}
```

### Implementation (in adapters/)

```typescript
// convex/contact/adapters/contact.repository.ts
import { createRepository } from "../../_shared/libs/repository";
import { IContactRepository } from "../domain/contact.repository";
import { ContactAgg } from "../domain/contact.model";

export const ContactRepository: IContactRepository = {
  // Compose with base methods
  ...createRepository("contacts", (doc) => new ContactAgg(doc)),

  byCompany: async (ctx, clause, limit = 100) => {
    const contacts = await ctx.db
      .query("contacts")
      .withIndex("by_company", (q) => q.eq("company", clause.company))
      .take(limit);

    return contacts.map((contact) => new ContactAgg(contact));
  },

  byAccount: async (ctx, clause, limit = 1) => {
    const base = ctx.db
      .query("contacts")
      .withIndex("by_account", (q) => q.eq("account", clause.account));

    if (clause.company) {
      const result = await base
        .filter((q) => q.eq(q.field("company"), clause.company))
        .unique();
      if (result) return [new ContactAgg(result)];
      return [];
    }

    const contacts = await base.take(limit);
    return contacts.map((contact) => new ContactAgg(contact));
  },

  listActive: async (ctx, limit = 50) => {
    const contacts = await ctx.db
      .query("contacts")
      .withIndex("by_status", (q) => q.eq("status", "active"))
      .take(limit);

    return contacts.map((contact) => new ContactAgg(contact));
  },
};
```

## Base Repository Interface

```typescript
// convex/_shared/libs/repository.ts
import { QueryCtx, MutationCtx } from "../_generated/server";
import { Doc, Id, TableNames } from "../_generated/dataModel";

export interface IRepository<
  TTable extends TableNames,
  TAggregate = Doc<TTable>,
> {
  get(ctx: QueryCtx, id: Id<TTable>): Promise<TAggregate | null>;
  save(ctx: MutationCtx, aggregate: TAggregate): Promise<TAggregate>;
  create(ctx: MutationCtx, data: Omit<Doc<TTable>, "_id" | "_creationTime">): Promise<TAggregate>;
  delete(ctx: MutationCtx, id: Id<TTable>): Promise<void>;
}

export function createRepository<
  TTable extends TableNames,
  TAggregate,
>(
  tableName: TTable,
  toAggregate: (doc: Doc<TTable>) => TAggregate,
): IRepository<TTable, TAggregate> {
  return {
    get: async (ctx, id) => {
      const doc = await ctx.db.get(id);
      if (!doc) return null;
      return toAggregate(doc);
    },

    save: async (ctx, aggregate) => {
      const model = (aggregate as any).getModel();
      await ctx.db.replace(model._id, model);
      return aggregate;
    },

    create: async (ctx, data) => {
      const id = await ctx.db.insert(tableName, data as any);
      const doc = await ctx.db.get(id);
      if (!doc) throw new Error("Failed to create document");
      return toAggregate(doc);
    },

    delete: async (ctx, id) => {
      await ctx.db.delete(id);
    },
  };
}
```

## Method Naming Conventions

### Basic CRUD

| Method | Description | Return |
|--------|-------------|--------|
| `get(ctx, id)` | Fetch by ID | `Promise<Agg \| null>` |
| `save(ctx, agg)` | Update entire document (replace) | `Promise<Agg>` |
| `create(ctx, data)` | Insert new document | `Promise<Agg>` |
| `delete(ctx, id)` | Remove document | `Promise<void>` |

### Query Methods

Use these prefixes:
- **`list`**: Return multiple items (optionally paginated)
- **`by`**: Filter by a specific field/index
- **`with`**: Include related data or apply conditions

```typescript
// Examples
listPending(): Promise<OrderAgg[]>;
listByStatus(status: OrderStatus): Promise<OrderAgg[]>;
paginatedList(opts: PaginationOpts): Promise<PaginatedResult<OrderAgg>>;

byCustomer(customerId: Id<"customers">): Promise<OrderAgg[]>;
byProduct(productId: Id<"products">): Promise<OrderAgg[]>;

withItems(orderId: Id<"orders">): Promise<OrderWithItemsAgg>;
withCustomer(orderId: Id<"orders">): Promise<OrderWithCustomerAgg>;
```

## Rules

### 1. Always Return Aggregates

```typescript
// ✅ Returns Aggregate
async get(ctx, id) {
  const doc = await ctx.db.get(id);
  return doc ? new ContactAgg(doc) : null;
}

// ❌ Returns raw document
async get(ctx, id) {
  return await ctx.db.get(id);
}
```

### 2. Avoid Field-Specific Update Methods

```typescript
// ❌ Avoid: bypasses business logic
async updateEmail(ctx, id, email) {
  await ctx.db.patch(id, { email });
}

// ✅ Prefer: use aggregate methods
const contactAgg = await ContactRepository.get(ctx, contactId);
contactAgg.changeEmail(newEmail); // Validates, triggers side effects
await ContactRepository.save(ctx, contactAgg);
```

### 3. Don't Deconstruct Models in Arguments

```typescript
// ❌ Cherry-picking fields
async createContact(ctx, { firstName, lastName, email }) {
  // Fields disconnected from model
}

// ✅ Pass the model or relevant portion
async createContact(ctx, contact: NewContact) {
  // Type-safe, validates against model schema
}
```

### 4. Use Indexes for Queries

```typescript
// ✅ Uses index
byCompany: async (ctx, clause) => {
  return ctx.db
    .query("contacts")
    .withIndex("by_company", (q) => q.eq("company", clause.company))
    .collect();
}

// ❌ Full table scan
byCompany: async (ctx, clause) => {
  return ctx.db
    .query("contacts")
    .filter((q) => q.eq(q.field("company"), clause.company))
    .collect();
}
```

## Usage in Mutations

```typescript
const updateContact = internalMutation({
  args: {
    contactId: v.id("contacts"),
    data: v.object(pick(ContactModel.fields, ["firstName", "lastName"])),
  },
  returns: ContactModel,
  handler: async (ctx, args): Promise<Contact> => {
    const contactAgg = await ContactRepository.get(ctx, args.contactId);
    if (!contactAgg) {
      throw new Error("Contact not found");
    }

    // Apply changes through aggregate
    contactAgg.updateProfile(args.data);

    // Persist and return
    const saved = await ContactRepository.save(ctx, contactAgg);
    return saved.getModel();
  },
});
```

## Paginated Queries

```typescript
interface IPaginatedRepository<TTable extends TableNames, TAggregate> {
  paginatedList(
    ctx: QueryCtx,
    opts: { paginationOpts: PaginationOpts; filters?: Partial<Doc<TTable>> },
  ): Promise<{
    page: TAggregate[];
    isDone: boolean;
    continueCursor: string;
  }>;
}

// Implementation
paginatedList: async (ctx, opts) => {
  const result = await ctx.db
    .query("contacts")
    .order("desc")
    .paginate(opts.paginationOpts);

  return {
    page: result.page.map((doc) => new ContactAgg(doc)),
    isDone: result.isDone,
    continueCursor: result.continueCursor,
  };
}
```

## Queries Use Repositories

Not just mutations - **queries** should also use repositories to access data:

```typescript
// convex/combat/queries/getActiveBattle.ts
import { query } from "../../customFunctions";
import { v } from "convex/values";
import { BattleModel } from "../domain/battle.model";
import { BattleRepository } from "../adapters/battle.repository";

const getActiveBattle = query({
  args: { heroId: v.id("heroProfiles") },
  returns: v.union(BattleModel, v.null()),
  handler: async (ctx, args) => {
    const battleAgg = await BattleRepository.getActiveByHero(ctx, args.heroId);
    if (!battleAgg) return null;
    return battleAgg.getModel();
  },
});

export default getActiveBattle;
```

**Why**: Consistent data access patterns, even for read-only operations. If query logic changes (e.g., filtering, permissions), it's centralized in the repository.

## Cross-Domain Repository Access

Mutations can use repositories from other domains when needed:

```typescript
// convex/combat/mutations/strikeMonster.ts
import { mutation } from "../../customFunctions";
import { BattleRepository } from "../adapters/battle.repository";
import { HeroProfileRepository } from "../../economy/adapters/heroProfile.repository";

const strikeMonster = mutation({
  handler: async (ctx, args) => {
    const battleAgg = await BattleRepository.get(ctx, args.battleId);
    if (!battleAgg) throw new Error("Battle not found");

    battleAgg.takeDamage(args.attackPower);
    await BattleRepository.save(ctx, battleAgg);

    // Cross-domain: update hero profile when monster defeated
    if (battleAgg.isDefeated) {
      const heroAgg = await HeroProfileRepository.get(ctx, battleAgg.heroId);
      if (heroAgg) {
        heroAgg.rewardCredits(battleAgg.monsterLevel);
        await HeroProfileRepository.save(ctx, heroAgg);
      }
    }

    return battleAgg.getModel();
  },
});

export default strikeMonster;
```

**Note**: Cross-domain access should be intentional. For complex cross-domain workflows, consider using triggers or internal mutations instead.

## Aligned Indexes

Define table indexes that match your repository query methods:

```typescript
// convex/combat/_tables.ts
import { defineTable } from "convex/server";
import { withoutSystemFields } from "convex-helpers";
import { BattleModel } from "./domain/battle.model";

export const combatTables = {
  battles: defineTable(withoutSystemFields(BattleModel.fields))
    .index("by_hero_and_status", ["heroId", "status"])  // Matches getActiveByHero
    .index("by_hero", ["heroId"]),                       // Matches getByHero
};
```

The repository uses these indexes:

```typescript
// convex/combat/adapters/battle.repository.ts
export const BattleRepository: IBattleRepository = {
  getActiveByHero: async (ctx, heroId) => {
    const doc = await ctx.db
      .query("battles")
      .withIndex("by_hero_and_status", (q) =>
        q.eq("heroId", heroId).eq("status", "active"),
      )
      .unique();

    if (!doc) return null;
    return new BattleAgg(doc);
  },
};
```

**Best practice**: Name indexes to reflect the query pattern they support (e.g., `by_customer`, `by_status`, `by_hero_and_status`).
