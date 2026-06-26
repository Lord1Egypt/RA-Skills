# Legacy Migration Learnings

Migration-focused guidance for moving legacy Convex code toward this skill's DDD and Hexagonal architecture guidelines.

Use this document as a practical reference while planning and executing incremental refactors.

## Repository Adoption

- When repositories replace shared helper functions (for example, `getActiveRecords` -> `RecordRepository.byParentId`), clean up the dead helpers immediately.
- Adopt repositories in mutations first; queries can follow later since they are read-only and the risk of inconsistency is lower.

## File Organization

- ID generation logic that uses `ctx.db` belongs in `adapters/`, not `_libs/`, because it performs database operations.
- During incremental repository adoption, cross-domain `ctx.db.get()` is a temporary bridge only. Track each use and replace it once the target domain exposes a repository.

## DTOs, models, and types

- Use `withoutSystemFields` from `convex-helpers` only in model files to derive `NewXModel`; everywhere else reference `NewXModel` directly.
- Prefer native Convex `VObject` methods (`.pick()`, `.omit()`, `.extend()`, `.partial()`) on domain `*Model` validators over spreading `pick()` from `convex-helpers` on `.fields`.
- Name Convex `v.object(...)` used for a specific function’s `args` / `returns` with a `*Dto` suffix when it helps; **define DTOs in that query or mutation file**, not under `domain/`. Derive from domain `*Model` using `VObject.pick` / `.extend` when the wire shape matches a document subset.

## Schema

- The `_tables.ts` file should be thin: only `defineTable(NewXModel.fields)` with indexes. All field definitions live in domain model files.
- Every table needs a model file, even if the aggregate is a lightweight `getModel()` wrapper with no business logic.

## Incremental Migration

- Break large refactors into rollback-friendly commits grouped by concern (infrastructure, file moves, logic changes, frontend updates).
- When renaming files or moving functions (e.g., `mutations.ts` → `mutations/`), Convex requires the full move in a single step since a file and directory with the same name cannot coexist.
- Frontend API paths change when adopting one-file-per-function with `export default` (append `.default` to all call sites).

## Legacy Migration Checklist

- Map current legacy modules to target boundaries (`domain/`, `adapters/`, `queries/`, `mutations/`).
- Move write-path logic to repositories first, then converge read paths.
- Eliminate direct `_generated/server` imports in favor of `customFunctions.ts`.
- Convert one API surface at a time to one-file-per-function with `export default`.
- Stage required schema changes as optional first, then complete migration and harden constraints.
