# Schema Migrations

Guidelines for handling schema changes in Convex projects, especially in CI/CD environments where code is deployed before migrations run.

## The Problem

In CI/CD pipelines, the typical workflow is:
1. Deploy code (including schema changes)
2. Run migrations to transform existing data

If new fields are marked as **required** (`v.number()`), the deployment will fail because existing documents in the database don't have those fields. Convex validates all existing documents against the new schema during deployment.

## The Solution: Optional Fields for Migration Compatibility

Make new fields optional initially to allow deployments before migrations run.

### Step 1: Add Fields as Optional

```typescript
// convex/combat/domain/battle.model.ts
export const BattleModel = v.object({
  _id: v.id("battles"),
  _creationTime: v.number(),
  heroId: v.id("heroProfiles"),
  monsterHealth: v.number(),
  monsterMaxHealth: v.number(),
  monsterLevel: v.number(),
  // New ATB fields - optional for migration compatibility
  heroHealth: v.optional(v.number()),
  heroMaxHealth: v.optional(v.number()),
  turnQueue: v.optional(v.array(TurnActorModel)),
  currentTurnIndex: v.optional(v.number()),
  status: BattleStatusModel,
});
```

**Why optional?** The schema will accept both:
- Old documents (without the new fields)
- New documents (with the new fields)

### Step 2: Handle Optional Fields in Aggregates

Add safe accessors and graceful degradation:

```typescript
export class BattleAgg implements IAggregate<Battle> {
  constructor(private battle: Battle) {}

  /**
   * Check if this battle has the new fields.
   * Legacy battles created before the migration won't have these fields.
   */
  get hasATBFields(): boolean {
    return (
      this.battle.heroHealth !== undefined &&
      this.battle.heroMaxHealth !== undefined &&
      this.battle.turnQueue !== undefined &&
      this.battle.currentTurnIndex !== undefined
    );
  }

  /**
   * Assert new fields exist and throw if not.
   * Used internally to safely access optional fields.
   */
  private assertATBFields(): void {
    if (!this.hasATBFields) {
      throw new Error(
        "This battle does not support ATB combat. Please start a new battle.",
      );
    }
  }

  /**
   * Safe getter - throws if fields missing.
   */
  private get safeHeroHealth(): number {
    this.assertATBFields();
    return this.battle.heroHealth!;
  }

  private get safeHeroMaxHealth(): number {
    this.assertATBFields();
    return this.battle.heroMaxHealth!;
  }

  private get safeTurnQueue(): TurnActor[] {
    this.assertATBFields();
    return this.battle.turnQueue!;
  }

  private get safeCurrentTurnIndex(): number {
    this.assertATBFields();
    return this.battle.currentTurnIndex!;
  }

  // Graceful degradation for getters
  get isHeroTurn(): boolean {
    if (!this.hasATBFields) return false;
    return this.isActive && this.currentTurn === "hero";
  }

  get isMonsterTurn(): boolean {
    if (!this.hasATBFields) return false;
    return this.isActive && this.currentTurn === "monster";
  }
}
```

**Pattern:**
- Use `hasATBFields` to check if new fields exist
- Use `assertATBFields()` for methods that require the new fields
- Use safe getters (`safeHeroHealth`, etc.) that throw if fields are missing
- Provide graceful degradation for boolean getters

### Step 3: Create Migration to Clean Up Old Data

Use `@convex-dev/migrations` to transform or delete incompatible documents:

```typescript
// convex/migrations/deleteOldBattles.ts
import { migrations } from "./runner";

/**
 * Migration to delete old battles that don't have the ATB combat fields.
 * These battles were created before the turn-based combat system was implemented.
 */
export const deleteOldBattles = migrations.define({
  table: "battles",
  migrateOne: async (ctx, doc) => {
    // Check if this is an old battle (missing the new ATB fields)
    const hasNewFields =
      "heroHealth" in doc &&
      "heroMaxHealth" in doc &&
      "turnQueue" in doc &&
      "currentTurnIndex" in doc;

    if (!hasNewFields) {
      // Delete old battles that don't have ATB fields
      await ctx.db.delete(doc._id);
    }

    // Return undefined to indicate no update needed (we're deleting instead)
    return undefined;
  },
});
```

**Alternative: Transform instead of delete**

```typescript
export const addDefaultValues = migrations.define({
  table: "battles",
  migrateOne: async (ctx, doc) => {
    if (doc.heroHealth === undefined) {
      // Transform old document to have new fields with defaults
      return {
        heroHealth: 100,
        heroMaxHealth: 100,
        turnQueue: ["hero", "monster"],
        currentTurnIndex: 0,
      };
    }
    return undefined; // No update needed
  },
});
```

### Step 4: CI/CD Workflow

```bash
# 1. Deploy code (schema accepts old documents due to optional fields)
npx convex deploy

# 2. Run migrations (clean up or transform old data)
npx convex run migrations/runner:runAll

# 3. After migration completes, new documents will always have required fields
```

**Why this works:**

1. **Deployment succeeds** - Schema accepts both old and new documents
2. **Migrations run** - After deployment, migrations clean up or transform incompatible data
3. **New documents** - Always have the required fields (created by aggregate factory methods)
4. **Legacy documents** - Either gracefully handled or cleaned up

### Step 5: Optional - Make Fields Required After Migration

After migrations complete and all old data is cleaned up, you can optionally make fields required again:

```typescript
// After migration is complete and verified
export const BattleModel = v.object({
  // ... other fields ...
  heroHealth: v.number(), // Now required
  heroMaxHealth: v.number(), // Now required
  turnQueue: v.array(TurnActorModel), // Now required
  currentTurnIndex: v.number(), // Now required
});
```

**However**, keeping fields optional provides better backwards compatibility and allows for gradual rollouts.

## Migration Setup

### Install Dependencies

```bash
npm install @convex-dev/migrations
```

### Configure Component

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import migrations from "@convex-dev/migrations/convex.config";

const app = defineApp();
app.use(migrations);

export default app;
```

### Create Runner

```typescript
// convex/migrations/runner.ts
import { Migrations } from "@convex-dev/migrations";
import { components } from "../_generated/api";
import { internal } from "../_generated/api";

export const migrations = new Migrations(components.migrations);

// Runner for all migrations
export const runAll = migrations.runner([
  internal.migrations.deleteOldBattles.deleteOldBattles,
]);
```

## Best Practices

1. **Always make new fields optional** when adding to existing models
2. **Use safe getters** in aggregates to access optional fields
3. **Provide graceful degradation** for boolean checks
4. **Delete or transform** old data in migrations, don't leave incompatible documents
5. **Test migrations** on development data before running in production
6. **Keep fields optional** for better backwards compatibility, unless you have a strong reason to make them required

## When to Use This Pattern

- Adding new required fields to existing models
- Changing field types (e.g., `v.string()` to `v.union(...)`)
- Removing fields (make them optional first, then delete in migration)
- Restructuring nested objects

## When NOT to Use This Pattern

- Adding new optional fields (they're already optional)
- Creating new tables (no existing data to migrate)
- Adding indexes (doesn't affect document structure)
