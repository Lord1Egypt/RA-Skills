# Limitations — safe-change v0.1

This document is an honest disclosure of what safe-change can and cannot detect. Read it before trusting a "Low" risk score on a complex codebase.

---

## Design Decision: Regex over AST

`scan-impact.mjs` uses regex-based static analysis, not an AST compiler (ts-morph, TypeScript Compiler API, etc.).

**Why:** Zero install friction. ClawHub users can drop the skill folder and run immediately — no `npm install`, no peer dependencies, no version conflicts with the host project's TypeScript version.

**Trade-off:** Regex cannot understand code semantics. It pattern-matches text. This means the categories below are blind spots.

---

## Known Limitations

### 1. Dynamic Imports

**Not detected.**

```typescript
// This will NOT appear in the importer list
const mod = await import(`./services/${name}.service`);
const { NotificationsService } = await import('./notifications/notifications.service');
```

Dynamic imports with string literals are not matched by the current regex patterns. This is the most common false-negative in modern NestJS codebases that use lazy-loaded modules.

**Mitigation:** If you know the codebase uses dynamic imports, run `grep -r "import(" src/` manually and check the results.

---

### 2. Barrel Re-exports (index.ts)

**Undercounts importers.**

```typescript
// src/notifications/index.ts
export { NotificationsService } from './notifications.service';

// src/users/users.service.ts
import { NotificationsService } from '../notifications'; // <-- imports via barrel
```

The scanner checks if `notifications.service.ts` appears in the import string. When the import goes through `../notifications` (a barrel), the scanner does not trace through the barrel — it will miss `users.service.ts` as an importer.

**Mitigation:** Check for `index.ts` files in the target's directory. If one exists, grep for imports of the barrel path manually.

---

### 3. Decorator Aliases

**Not detected.**

```typescript
// A custom decorator wrapping @Controller
@JsonController('/notifications') // from routing-controllers or a custom factory
export class NotificationsController { ... }
```

The scanner looks specifically for `@Controller(`. Custom decorators that wrap `@Controller` internally are not detected. This will produce `routes.controllers: []` even though the file is a controller.

**Mitigation:** Search for `@JsonController`, `@RestController`, or similar aliases manually in your codebase. Add the known aliases to your project's safe-change workflow notes.

---

### 4. Type-only Imports

**May appear as importers but carry no runtime risk.**

```typescript
import type { NotificationsService } from './notifications.service';
```

Type-only imports are included in the importer count. A file that only imports a type will be listed as an importer, but changing the runtime behavior of `notifications.service.ts` will not affect it at runtime — only if the type signature changes.

**Impact:** Risk score may be slightly inflated for heavily type-shared files (e.g., `types.ts`, `interfaces.ts`). This is intentional — conservative is safer.

---

### 5. Re-export Chains

**Not traced.**

```typescript
// a.ts exports b.ts exports c.ts
// If your target is c.ts, the scanner finds direct importers of c.ts only
// Files that import via a.ts → b.ts are not detected
```

Multi-hop re-export chains are not traced. The scanner does one level of import detection.

---

### 6. Path Aliases (tsconfig paths)

**Partially detected.**

```typescript
// tsconfig.json
{ "paths": { "@notifications/*": ["src/notifications/*"] } }

// another-file.ts
import { NotificationsService } from '@notifications/notifications.service'; // <-- may be missed
```

The scanner resolves relative imports well but may miss imports that use `tsconfig` path aliases (`@app/`, `~`, `@/`, etc.). If your project uses path aliases heavily, the importer count may be undercounted.

**Mitigation:** For path-alias-heavy projects, supplement with `grep -r "@notifications" src/`.

---

### 7. JavaScript Files

**Not scanned.**

The scanner only reads `.ts` and `.tsx` files. If your project has `.js` or `.mjs` files that import TypeScript compiled outputs, those are not detected.

---

### 8. Language Coverage

**TypeScript only in v0.1.**

- Python, Go, Rust, Java — not supported
- PHP — not supported
- Vue SFC, Svelte — not supported (`.vue`, `.svelte` files are skipped)

---

### 9. Test Gap False Negatives

**Test factories and shared mocks.**

```typescript
// notifications.spec.ts
import { createMockNotificationsService } from '../testing/factories';
// Does NOT import notifications.service.ts directly
```

If a spec file imports a mock factory instead of the real service, `tests.gap` will be `true` even though test logic exists. This is a conservative false-positive for the gap flag — the skill would rather warn you than miss a real gap.

---

### 10. ENV Vars in Conditionals

**All ENV references are collected, including unreachable ones.**

```typescript
if (process.env.NODE_ENV === 'test') {
  // This ENV var is listed even in production analysis
  this.host = process.env.SMTP_HOST_OVERRIDE;
}
```

The scanner does not evaluate control flow. All `process.env.X` references are included in the list regardless of whether they are reachable at runtime.

---

## Summary Table

| Limitation | Risk | Workaround |
|------------|------|------------|
| Dynamic imports | False negative (undercount) | Manual `grep -r "import("` |
| Barrel re-exports | False negative (undercount) | Check `index.ts` + grep barrel path |
| Decorator aliases | False negative (no routes) | Know your custom decorators |
| Type-only imports | False positive (overcount) | Acceptable — conservative |
| Path aliases | False negative (undercount) | `grep -r "@alias"` |
| Multi-hop re-exports | False negative (undercount) | One-hop only by design |
| Test factories | False positive (gap flag) | Inspect spec file manually |

---

## Planned Improvements (v0.2+)

- `--follow-barrels` flag: trace `index.ts` re-exports one level deep
- Path alias resolution via `tsconfig.json` `paths` field
- `import type` exclusion flag for risk score calculation
- Vue SFC and Svelte support

These are not commitments — they are the known gaps that would most improve accuracy.
