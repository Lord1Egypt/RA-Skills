---
name: rxjs
description: "ALWAYS use when working with RxJS Observables, operators, and reactive patterns in Angular applications."
metadata:
  version: 8.0.0
  generated_by: oguzhancart
  generated_at: 2026-02-19
---

# RxJS (Reactive Extensions for JavaScript)

**Version:** 8.x (2025)
**Tags:** Reactive Programming, Observables, Async

**References:** [Docs](https://rxjs.dev) — operators, API • [Angular RxJS](https://angular.io/guide/rxjs) • [GitHub](https://github.com/reactivex/rxjs)

## API Changes

This section documents recent version-specific API changes.

- NEW: RxJS 8 — Modern TypeScript types, smaller bundles, better tree-shaking [source](https://dev.to/cristiansifuentes/angular-rxjs-in-2025-the-experts-playbook-signals-rxjs-8-and-interop-28ed)

- NEW: Improved interop helpers — Simpler conversion to/from Signals with `toSignal` and `toObservable`

- NEW: RxJS 8 ergonomics — Compact operator signatures and safer defaults

- DEPRECATED: Legacy import style — Use RxJS 7+ pipeable operators instead of patch imports

## Best Practices

- Use AsyncPipe in templates — Handles subscription/unsubscription automatically, prevents memory leaks

```ts
@Component({
  template: `
    <div *ngIf="data$ | async as data">
      {{ data.name }}
    </div>
  `
})
export class MyComponent {
  data$ = this.service.getData();
}
```

- Use proper flattening operators — Choose based on use case:

```ts
// switchMap - cancel previous, keep latest (search)
search(term: string): Observable<SearchResult[]> {
  return this.searchService.search(term).pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => term ? this.http.get(...) : of([]))
  );
}

// mergeMap - run concurrently (multiple API calls)
this.items$.pipe(
  mergeMap(item => this.save(item))
);

// concatMap - run sequentially (order matters)
this.orders$.pipe(
  concatMap(order => this.processOrder(order))
);

// exhaustMap - ignore while running (form submit)
this.submit$.pipe(
  exhaustMap(() => this.submitForm())
);
```

- Always unsubscribe — Prevent memory leaks

```ts
// Use takeUntil pattern
private destroy$ = new Subject<void>();

ngOnInit() {
  this.data$.pipe(takeUntil(this.destroy$)).subscribe();
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}

// Or use takeUntilDestroyed (Angular 16+)
private destroy$ = takeUntilDestroyed();
```

- Use `catchError` for error handling

```ts
this.http.get('/api/data').pipe(
  catchError(error => {
    console.error(error);
    return of([]); // Return fallback value
  })
);
```

- Use `shareReplay(1)` for caching shared observables

```ts
this.data$ = this.http.get('/api/data').pipe(
  shareReplay(1)
);
```

- Name observables with `$` suffix — Improves readability

- Use Signals for UI state, RxJS for events — Modern Angular pattern

```ts
// Convert Observable to Signal
users = toSignal(this.users$, { initialValue: [] });

// Convert Signal to Observable (if needed)
name$ = toObservable(this.name);
```
