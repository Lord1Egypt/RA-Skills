# ESLint Rules for DDD Architecture

ESLint rules that enforce DDD architectural patterns at lint-time. These rules ensure consistent patterns across the codebase and prevent architectural violations.

## Setup

Add these rules to your `eslint.config.mjs` file. The rules use ESLint's flat config format.

## Rule Categories

### 1. Custom Function Imports

**Purpose**: Ensure all Convex functions use the custom wrappers from `customFunctions.ts` instead of raw imports from `_generated/server`.

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
            importNames: [
              "mutation",
              "query",
              "action",
              "internalMutation",
              "internalQuery",
            ],
            message:
              "Use custom functions from '../customFunctions' instead. Example: import { mutation } from '../customFunctions'",
          },
        ],
      },
    ],
  },
},
```

**Why**: Custom functions wrap the raw Convex functions to integrate triggers and other cross-cutting concerns. Direct imports bypass these integrations.

### 2. Repository Pattern Enforcement

**Purpose**: Block direct `ctx.db` operations outside of repository adapters, enforcing the repository pattern.

```javascript
{
  files: ["convex/**/*.ts"],
  ignores: ["convex/**/adapters/**/*.ts", "convex/_generated/**", "convex/customFunctions.ts"],
  rules: {
    "no-restricted-syntax": [
      "error",
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='insert']",
        message:
          "Direct ctx.db.insert is not allowed. Use an aggregate and save it with a repository instead.",
      },
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='patch']",
        message:
          "Direct ctx.db.patch is not allowed. Use an aggregate and save it with a repository instead.",
      },
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='replace']",
        message:
          "Direct ctx.db.replace is not allowed. Use an aggregate and save it with a repository instead.",
      },
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='delete']",
        message:
          "Direct ctx.db.delete is not allowed. Use an aggregate and save it with a repository instead.",
      },
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='query']",
        message:
          "Prefer using a repository to query data so you can work with aggregates instead of raw documents.",
      },
      {
        selector:
          "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='get']",
        message:
          "Prefer using a repository to fetch data so you can work with aggregates instead of raw documents.",
      },
    ],
  },
},
```

**Why**: Direct database operations bypass domain logic encapsulated in aggregates. Repositories ensure all data access goes through the domain layer.

**Exception**: Files in `convex/**/adapters/**/*.ts` are excluded because repository implementations need direct database access.

### 3. Mutation Location Enforcement

**Purpose**: Ensure mutations and internal mutations are only defined in the `mutations/` folder.

```javascript
{
  files: ["convex/**/*.ts"],
  ignores: [
    "convex/**/mutations/**/*.ts",
    "convex/_generated/**",
    "convex/customFunctions.ts",
  ],
  rules: {
    "no-restricted-syntax": [
      "error",
      {
        selector: "CallExpression[callee.name='mutation']",
        message:
          "Define mutations in a `mutations` folder. Filename should match the mutation name. Move to `convex/**/mutations/`.",
      },
      {
        selector: "CallExpression[callee.name='internalMutation']",
        message:
          "Define internal mutations in a `mutations` folder. Filename should match the mutation name. Move to `convex/**/mutations/`.",
      },
    ],
  },
},
```

**Why**: Organizing mutations in dedicated folders makes the codebase navigable and ensures consistent structure across sub-domains.

### 4. Default Export Pattern

**Purpose**: Ensure mutation/query files use the correct export pattern with `export default`.

```javascript
{
  files: ["convex/**/mutations/**/*.ts", "convex/**/queries/**/*.ts"],
  ignores: ["convex/_generated/**"],
  rules: {
    "no-restricted-syntax": [
      "error",
      {
        selector: "ExportNamedDeclaration > VariableDeclaration > VariableDeclarator > CallExpression[callee.name=/^(mutation|query|internalMutation|internalQuery)$/]",
        message:
          "Use `const name = mutation({...}); export default name;` instead of `export const name = mutation({...})`",
      },
    ],
  },
},
```

**Why**: Convex generates API paths from file structure. Using `export default` creates clean paths like `api.combat.mutations.createBattle.default`. Named exports create redundant paths like `api.combat.mutations.createBattle.createBattle`.

**Correct Pattern**:

```typescript
// convex/combat/mutations/createBattle.ts
const createBattle = mutation({
  args: { heroId: v.id("heroProfiles") },
  handler: async (ctx, args) => {
    // ...
  },
});

export default createBattle;
```

**Incorrect Pattern**:

```typescript
// ❌ Creates api.combat.mutations.createBattle.createBattle
export const createBattle = mutation({
  args: { heroId: v.id("heroProfiles") },
  handler: async (ctx, args) => {
    // ...
  },
});
```

## Complete Configuration Example

```javascript
// eslint.config.mjs
import { defineConfig, globalIgnores } from "eslint/config";
import nextCoreWebVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

export default defineConfig([
  ...nextCoreWebVitals,
  ...nextTypescript,
  globalIgnores(["convex/_generated"]),
  
  // Rule 1: Custom function imports
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
  
  // Rule 2: Repository pattern enforcement
  {
    files: ["convex/**/*.ts"],
    ignores: ["convex/**/adapters/**/*.ts", "convex/_generated/**", "convex/customFunctions.ts"],
    rules: {
      "no-restricted-syntax": [
        "error",
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='insert']",
          message: "Direct ctx.db.insert is not allowed. Use a repository instead.",
        },
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='patch']",
          message: "Direct ctx.db.patch is not allowed. Use a repository instead.",
        },
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='replace']",
          message: "Direct ctx.db.replace is not allowed. Use a repository instead.",
        },
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='delete']",
          message: "Direct ctx.db.delete is not allowed. Use a repository instead.",
        },
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='query']",
          message: "Prefer using a repository to query data.",
        },
        {
          selector: "CallExpression[callee.object.object.name='ctx'][callee.object.property.name='db'][callee.property.name='get']",
          message: "Prefer using a repository to fetch data.",
        },
      ],
    },
  },
  
  // Rule 3: Mutation location enforcement
  {
    files: ["convex/**/*.ts"],
    ignores: ["convex/**/mutations/**/*.ts", "convex/_generated/**", "convex/customFunctions.ts"],
    rules: {
      "no-restricted-syntax": [
        "error",
        {
          selector: "CallExpression[callee.name='mutation']",
          message: "Define mutations in a `mutations` folder.",
        },
        {
          selector: "CallExpression[callee.name='internalMutation']",
          message: "Define internal mutations in a `mutations` folder.",
        },
      ],
    },
  },
  
  // Rule 4: Default export pattern
  {
    files: ["convex/**/mutations/**/*.ts", "convex/**/queries/**/*.ts"],
    ignores: ["convex/_generated/**"],
    rules: {
      "no-restricted-syntax": [
        "error",
        {
          selector: "ExportNamedDeclaration > VariableDeclaration > VariableDeclarator > CallExpression[callee.name=/^(mutation|query|internalMutation|internalQuery)$/]",
          message: "Use `const name = mutation({...}); export default name;` instead of named export.",
        },
      ],
    },
  },
]);
```

## Disabling Rules

For legitimate exceptions, disable rules inline:

```typescript
// eslint-disable-next-line no-restricted-syntax
await ctx.db.insert("auditLog", { ... }); // Allowed in specific cases
```

Document why the exception is needed in a comment.
