---
name: use-effect
description: Refactor React code away from direct useEffect usage. Use when Codex needs to review, rewrite, or prevent useEffect in React components, custom hooks, or frontend architecture; diagnose infinite loops or race conditions caused by effects; replace effect-driven state syncing with derived values, event handlers, query libraries, keyed remounts, or a mount-only wrapper such as useMountEffect; or enforce a no-direct-useEffect rule in linting and agent guidance.
---

# Use Effect

Inspect the local React patterns before changing code. Prefer the project's existing data-fetching library, lifecycle wrapper, and lint setup over introducing new abstractions.

Treat direct `useEffect` as a code smell by default. Replace it with clearer control flow unless the code is genuinely synchronizing with an external system on mount or unmount.

## Workflow

1. Locate every direct `useEffect` in the relevant scope and classify why it exists.
2. Decide whether the effect is:
   - deriving state from props or state
   - fetching data
   - relaying an action that should happen in response to a user event
   - synchronizing with an external system on mount
   - resetting local state when an identity changes
3. Replace the effect with the narrowest alternative pattern.
4. Preserve existing project conventions. If the codebase already has `useMountEffect`, use it instead of raw `useEffect(..., [])`.
5. Verify behavior by running the relevant tests or targeted checks. Pay special attention to loops, duplicate requests, stale state, and remount semantics.

## Replacement Rules

### Derive State, Do Not Sync It

If an effect sets state from other props or state, compute the value during render instead.

Common smell:

```tsx
useEffect(() => {
  setFilteredProducts(products.filter((p) => p.inStock));
}, [products]);
```

Preferred direction:

```tsx
const filteredProducts = products.filter((p) => p.inStock);
```

Also collapse multi-step derived values instead of chaining effects through intermediary state.

### Use Data-Fetching Abstractions

If an effect fetches data and then writes it into local state, prefer the project's query or loader abstraction. Reuse the codebase's existing library when present.

Common smell:

```tsx
useEffect(() => {
  fetchProduct(productId).then(setProduct);
}, [productId]);
```

Preferred direction:

```tsx
const { data: product } = useQuery({
  queryKey: ["product", productId],
  queryFn: () => fetchProduct(productId),
});
```

If the project does not already use a client-side query library, check whether the fetch belongs in framework loaders, server components, or route-level data APIs before adding one.

### Use Event Handlers, Not Effect Relays

If state is only used as a flag to make an effect do work later, move that work into the event handler that caused it.

Common smell:

```tsx
useEffect(() => {
  if (liked) {
    postLike();
    setLiked(false);
  }
}, [liked]);
```

Preferred direction:

```tsx
const handleLike = () => {
  postLike();
};
```

### Use Mount-Only Effects Only for External Sync

For true setup and cleanup with external systems, use the project's mount-only wrapper if it exists. Keep this category narrow: DOM integration, subscriptions, widget lifecycle, imperative browser APIs.

If a precondition gates the mount-only effect, prefer conditional rendering so the component mounts only when ready.

```tsx
if (isLoading) return <LoadingScreen />;
return <VideoPlayer />;
```

Then let `VideoPlayer` run mount-only setup once.

### Reset with `key`, Not Dependency Choreography

If the goal is "treat this as a new instance when identity changes", remount with `key` instead of writing effect logic that tries to reset local state.

```tsx
return <VideoPlayer key={videoId} videoId={videoId} />;
```

Use this when the desired behavior is a fresh lifecycle boundary.

## Code Review Heuristics

Flag direct `useEffect` when you see:

- `setState` driven by props or other state
- `fetch(...).then(setState)` or async loading logic inside an effect
- state used as an action flag
- dependency arrays that are being "fixed" incrementally
- effect chains where one effect updates state that triggers another effect
- logic that really wants remount semantics

Do not remove mount-only effects that are genuinely integrating with external systems unless you replace them with an equivalent lifecycle boundary.

## Adoption Guidance

When the user asks for a broader rollout:

- Add or update lint rules that ban direct `useEffect`.
- Add a local wrapper such as `useMountEffect` only if the codebase wants an explicit exception path.
- Update agent guidance or contributor docs so future edits do not reintroduce direct effects.
- Prefer incremental refactors around touched files unless the user asks for a full migration.

## References

Read [patterns.md](./references/patterns.md) when you need detailed smell tests, larger before/after examples, or help choosing between replacement patterns.
