# Common Bugs Checklist

Quick-reference bug patterns organized by category. For detailed code examples, see the dedicated language guides.

## Universal Issues

### Logic Errors
- [ ] Off-by-one errors in loops and array access
- [ ] Incorrect boolean logic (De Morgan's law violations)
- [ ] Missing null/undefined checks
- [ ] Race conditions in concurrent code
- [ ] Incorrect comparison operators (`==` vs `===`, `=` vs `==`)
- [ ] Integer overflow/underflow
- [ ] Floating point comparison issues

### Resource Management
- [ ] Memory leaks (unclosed connections, listeners)
- [ ] File handles not closed
- [ ] Database connections not released
- [ ] Event listeners not removed
- [ ] Timers/intervals not cleared

### Error Handling
- [ ] Swallowed exceptions (empty catch blocks)
- [ ] Generic exception handling hiding specific errors
- [ ] Missing error propagation
- [ ] Incorrect error types thrown
- [ ] Missing finally/cleanup blocks

## TypeScript/JavaScript

- [ ] `==` instead of `===`
- [ ] Using `any` — prefer proper types or `unknown` with type guards
- [ ] Missing `await` on async calls
- [ ] Unhandled promise rejections (no try-catch around await)
- [ ] `this` context lost in callbacks
- [ ] Missing `key` prop in lists
- [ ] Closure capturing stale loop variable
- [ ] `parseInt` without radix parameter
- [ ] Modifying array/object during iteration

**Full guide:** [TypeScript Review Guide](typescript.md)

## React / React 19

- [ ] Hooks called conditionally or in loops (violates Rules of Hooks)
- [ ] `useEffect` dependency array incomplete or incorrect
- [ ] `useEffect` missing cleanup function (subscriptions, timers, fetches)
- [ ] `useEffect` used for derived state (use `useMemo` instead)
- [ ] `useMemo`/`useCallback` over-used or used without `React.memo`
- [ ] Component defined inside another component (re-mounts every render)
- [ ] Unstable props (inline objects/functions passed to memo components)
- [ ] Direct mutation of props
- [ ] List missing `key` or using array index as key (reorderable lists)
- [ ] Server Component using client APIs (`useState`, `useEffect`, `onClick`)
- [ ] `'use client'` on parent making entire subtree client-side
- [ ] `useActionState` calling `setState` instead of returning new state
- [ ] `useFormStatus` called in same component as `<form>` (must be in child)
- [ ] `useOptimistic` used for critical operations (payments, deletions)
- [ ] Single Suspense boundary for entire page (slow blocks fast)
- [ ] Missing Error Boundary wrapping Suspense

**TanStack Query v5:**
- [ ] `queryKey` missing parameters that affect data
- [ ] Default `staleTime: 0` causing excessive refetches
- [ ] `useSuspenseQuery` with `enabled` option (not supported)
- [ ] Mutation not invalidating related queries on success
- [ ] Optimistic update missing rollback in `onError`

**Full guide:** [React Review Guide](react.md)

## Vue 3

- [ ] Destructuring `reactive()` object loses reactivity (use `toRefs`)
- [ ] Passing `props.x` to composable instead of `() => props.x` or `toRef(props, 'x')`
- [ ] `watch` with async callback missing `onCleanup` (race condition)
- [ ] `computed` with side effects (mutations, API calls)
- [ ] `v-for` using index as `:key` when list can reorder
- [ ] `v-if` and `v-for` on the same element
- [ ] `defineProps` without TypeScript type declaration
- [ ] Directly mutating props instead of emitting events

**Full guide:** [Vue 3 Review Guide](vue.md)

## Python

- [ ] Mutable default arguments (`def f(x=[])`)
- [ ] Bare `except:` catching `KeyboardInterrupt` and `SystemExit`
- [ ] Shared mutable class attributes (`class C: items = []`)
- [ ] Using `is` instead of `==` for value comparison
- [ ] Forgetting `self` parameter in methods
- [ ] Modifying list while iterating
- [ ] String concatenation in loops (use `"".join()`)
- [ ] Not closing files (use `with` statement)
- [ ] Missing type annotations on public functions

**Full guide:** [Python Review Guide](python.md)

## Rust

**Ownership & Borrowing:**
- [ ] Unnecessary `clone()` to work around borrow checker
- [ ] `Arc<Mutex<T>>` when single-owner would suffice
- [ ] Storing borrows in structs when owned data is simpler

**Unsafe Code:**
- [ ] `unsafe` block without `SAFETY:` comment explaining invariants
- [ ] `unsafe fn` without `# Safety` doc section

**Async & Concurrency:**
- [ ] Blocking in async context (`std::fs`, `std::thread::sleep`)
- [ ] Holding `std::sync::Mutex` across `.await`
- [ ] Spawned task missing `'static` lifetime bound

**Error Handling:**
- [ ] `unwrap()`/`expect()` in production code
- [ ] Library using `anyhow` instead of `thiserror`
- [ ] Swallowing error context (`map_err(|_| ...)`)
- [ ] Ignoring `must_use` return values

**Performance:**
- [ ] Unnecessary `.collect()` — prefer lazy iterators
- [ ] String concatenation in loops without `with_capacity`
- [ ] `Box<dyn Trait>` when `impl Trait` would work

**Full guide:** [Rust Review Guide](rust.md)

## Go

- [ ] Ignoring errors (`result, _ := SomeFunction()`)
- [ ] Goroutine with no exit mechanism (leak)
- [ ] Missing or incorrect `context.Context` propagation
- [ ] Loop variable capture issue (Go < 1.22)
- [ ] `defer` in loops (deferred until function, not loop iteration)
- [ ] Variable shadowing
- [ ] Map used before initialization
- [ ] Error wrapping with `%v` instead of `%w` (breaks `errors.Is`/`errors.As`)

**Full guide:** [Go Review Guide](go.md)

## Java / Spring Boot

- [ ] POJO/DTO with manual boilerplate instead of `record`
- [ ] Traditional switch missing `break` (use switch expressions)
- [ ] Field injection instead of constructor injection
- [ ] JPA N+1 query (missing `fetch join` or `@EntityGraph`)
- [ ] Incorrect `equals`/`hashCode` on JPA entities
- [ ] `Optional.get()` without `isPresent()` check
- [ ] Stream operations with side effects

**Full guide:** [Java Review Guide](java.md)

## SQL

- [ ] String concatenation for queries (SQL injection risk) — use parameterized queries
- [ ] Missing indexes on filtered/joined columns
- [ ] `SELECT *` instead of specific columns
- [ ] N+1 query patterns
- [ ] Missing `LIMIT` on large tables
- [ ] Not handling `NULL` comparisons correctly (`IS NULL` vs `= NULL`)
- [ ] Missing transactions for related operations

## API Design

- [ ] Inconsistent resource naming
- [ ] Wrong HTTP methods (POST for idempotent operations)
- [ ] Missing pagination for list endpoints
- [ ] Incorrect status codes
- [ ] Missing input validation and sanitization
- [ ] Trusting client-side validation only

## Testing

- [ ] Testing implementation details instead of behavior
- [ ] Missing edge case tests
- [ ] Flaky tests (non-deterministic)
- [ ] Tests with external dependencies (no mocks)
- [ ] Missing negative tests (error cases)
- [ ] Overly complex test setup