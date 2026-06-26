---
name: ngrx
description: "ALWAYS use when implementing Angular state management with NgRx, including Store, Effects, Entity, and Signal Store."
metadata:
  version: 19.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# @ngrx/store, @ngrx/effects, @ngrx/entity, @ngrx/signals

**Version:** 19.0.0 (2025)
**Tags:** State Management, Redux, Reactive, Store, Effects

**References:** [Docs](https://ngrx.io) — guides, API • [GitHub](https://github.com/ngrx/platform) • [GitHub Issues](https://github.com/ngrx/platform/issues)

## API Changes

This section documents recent version-specific API changes.

- NEW: NgRx Signal Store — Modern, lightweight state management with Signals API, reducing boilerplate significantly [source](https://ngrx.io/guide/signals/overview)

- NEW: Functional Effects — Modern approach to creating effects using functional programming patterns

- NEW: `withEntities` — Entity management for Signal Store, simplifies CRUD operations on collections

- NEW: `@ngrx/data` — Simplifies entity CRUD operations with automatic HTTP integration

- DEPRECATED: Classic NgRx patterns — Consider migrating to Signal Store for new projects

## Best Practices

- Use NgRx Signal Store for new projects — Combines NgRx structure with Signals performance

```ts
import { signalStore, withState, withMethods, withHooks } from '@ngrx/signals';

export const AuthStore = signalStore(
  withState({ user: null, isAuthenticated: false }),
  withMethods((store, authService = inject(AuthService)) => ({
    login(credentials: Credentials) {
      authService.login(credentials).pipe(
        tap(user => store.user.set(user))
      ).subscribe();
    }
  })),
  withHooks({
    onInit() {
      // Initialize store
    }
  })
);
```

- Use Entity Adapter for collections — Simplifies CRUD operations on entity collections

```ts
import { createEntityAdapter, EntityState } from '@ngrx/entity';

export interface Product extends EntityState<Product> {
  // Additional state properties
}

export const adapter = createEntityAdapter<Product>({
  selectId: (product) => product.id
});
```

- Keep reducers pure and synchronous — Never perform async operations in reducers

- Use Effects for side effects — Handle HTTP calls, navigation, and other async operations in effects

- Use strongly typed actions — Create action groups for better type safety

- Normalize state for complex data — Store entities in dictionaries indexed by ID

- Use memoized selectors — Prevent unnecessary re-computations

- Use `ChangeDetectionStrategy.OnPush` — Work well with reactive state
