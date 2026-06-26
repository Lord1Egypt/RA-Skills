# Custom Functions

Custom function wrappers integrate cross-cutting concerns (like triggers) into Convex mutations and queries.

## Why Custom Functions

Convex's raw `mutation` and `query` functions from `_generated/server` don't automatically integrate with triggers or other middleware. Custom functions wrap these to:

1. Integrate database triggers via `convex-helpers`
2. Provide a single import point for all function definitions
3. Enable consistent behavior across all mutations

## Setup

### 1. Create the Custom Functions File

```typescript
// convex/customFunctions.ts
import {
  customMutation,
  customCtx,
} from "convex-helpers/server/customFunctions";
import {
  mutation as rawMutation,
  query as rawQuery,
  internalMutation as rawInternalMutation,
  internalQuery as rawInternalQuery,
} from "./_generated/server";
import triggers from "./_triggers";

// Mutations wrapped with trigger support
export const mutation = customMutation(rawMutation, customCtx(triggers.wrapDB));

export const internalMutation = customMutation(
  rawInternalMutation,
  customCtx(triggers.wrapDB),
);

// Queries don't need trigger wrapping (read-only)
export const query = rawQuery;

export const internalQuery = rawInternalQuery;

// Export raw functions for edge cases
export { rawMutation, rawInternalMutation };
```

### 2. Create the Triggers Registry

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

## Usage

### In Mutations

```typescript
// convex/combat/mutations/createBattle.ts
import { mutation } from "../../customFunctions";
import { v } from "convex/values";

const createBattle = mutation({
  args: { heroId: v.id("heroProfiles") },
  handler: async (ctx, args) => {
    // ctx.db is now wrapped with trigger support
    // Any inserts/updates will fire registered triggers
  },
});

export default createBattle;
```

### In Queries

```typescript
// convex/combat/queries/getActiveBattle.ts
import { query } from "../../customFunctions";
import { v } from "convex/values";

const getActiveBattle = query({
  args: { heroId: v.id("heroProfiles") },
  handler: async (ctx, args) => {
    // Queries use raw functions (no trigger wrapping needed)
  },
});

export default getActiveBattle;
```

### Internal Mutations

Use `internalMutation` for cross-domain communication or trigger handlers:

```typescript
// convex/economy/mutations/rewardCredits.ts
import { internalMutation } from "../../customFunctions";
import { v } from "convex/values";

const rewardCredits = internalMutation({
  args: {
    heroId: v.id("heroProfiles"),
    monsterLevel: v.number(),
  },
  handler: async (ctx, args) => {
    // Called from combat trigger when monster is slain
  },
});

export default rewardCredits;
```

## How Trigger Integration Works

The `customCtx(triggers.wrapDB)` wraps the `ctx.db` object so that:

1. `ctx.db.insert()` fires registered "insert" triggers
2. `ctx.db.patch()` and `ctx.db.replace()` fire "update" triggers
3. `ctx.db.delete()` fires "delete" triggers

The trigger handlers receive a `Change` object with the old and new document states.

## ESLint Enforcement

To ensure all code uses custom functions, add this ESLint rule:

```javascript
{
  files: ["convex/**/*.ts"],
  ignores: ["convex/customFunctions.ts"],
  rules: {
    "no-restricted-imports": [
      "error",
      {
        patterns: [
          {
            allowTypeImports: true,
            group: ["**/_generated/server"],
            importNames: ["mutation", "query", "action", "internalMutation", "internalQuery"],
            message: "Use custom functions from '../customFunctions' instead.",
          },
        ],
      },
    ],
  },
},
```

See [ESLint Rules](eslint-rules.md) for the complete configuration.

## Raw Function Exports

For edge cases where you need the unwrapped functions (e.g., specific performance needs), the raw versions are exported:

```typescript
import { rawMutation, rawInternalMutation } from "../customFunctions";
```

Use these sparingly and document why trigger integration isn't needed.
