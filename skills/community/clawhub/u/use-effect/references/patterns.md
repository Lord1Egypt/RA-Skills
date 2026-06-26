# useEffect Replacement Patterns

Use this reference when the replacement is not obvious from the local code.

## Decision Tree

Ask these questions in order:

1. Is the effect only computing a value from props or state?
Use derived values in render.

2. Is the effect loading data?
Use the project's data-loading abstraction.

3. Is the effect reacting to a user action that already has a handler?
Move the logic into the handler.

4. Is the effect performing setup and cleanup for an external system?
Use a mount-only wrapper such as `useMountEffect`, or the project's equivalent.

5. Is the effect trying to reset state when an ID or entity changes?
Remount with `key`.

If none of these fit, inspect whether the component owns too many responsibilities and should be split.

## Pattern 1: Derived State

Bad:

```tsx
const [tax, setTax] = useState(0);
const [total, setTotal] = useState(0);

useEffect(() => {
  setTax(subtotal * 0.1);
}, [subtotal]);

useEffect(() => {
  setTotal(subtotal + tax);
}, [subtotal, tax, total]);
```

Better:

```tsx
const tax = subtotal * 0.1;
const total = subtotal + tax;
```

Smell test:

- `useEffect(() => setX(derive(y)), [y])`
- local state mirrors props
- multiple effects form a dependency chain

## Pattern 2: Data Fetching

Bad:

```tsx
const [product, setProduct] = useState<Product | null>(null);

useEffect(() => {
  let cancelled = false;

  fetchProduct(productId).then((next) => {
    if (!cancelled) setProduct(next);
  });

  return () => {
    cancelled = true;
  };
}, [productId]);
```

Better:

```tsx
const { data: product } = useQuery({
  queryKey: ["product", productId],
  queryFn: () => fetchProduct(productId),
});
```

Why:

- centralizes caching and staleness
- avoids hand-rolled cancellation patterns
- prevents repeated bespoke loading logic

## Pattern 3: Event-Driven Actions

Bad:

```tsx
const [shouldSubmit, setShouldSubmit] = useState(false);

useEffect(() => {
  if (!shouldSubmit) return;
  submitForm();
  setShouldSubmit(false);
}, [shouldSubmit]);
```

Better:

```tsx
const handleSubmit = () => {
  submitForm();
};
```

Smell test:

- "set flag, then effect does the real work"
- handler exists but effect owns the action

## Pattern 4: Mount-Only External Sync

Valid cases:

- focusing or scrolling an element on mount
- subscribing to browser APIs
- bootstrapping or disposing of a third-party widget
- starting imperative media playback after the component is allowed to exist

Example:

```tsx
function useMountEffect(effect: () => void | (() => void)) {
  useEffect(effect, []);
}
```

Prefer conditional mounting over guards inside the effect.

Bad:

```tsx
useEffect(() => {
  if (!isReady) return;
  startPlayer();
}, [isReady]);
```

Better:

```tsx
function PlayerGate({ isReady }: { isReady: boolean }) {
  if (!isReady) return null;
  return <Player />;
}

function Player() {
  useMountEffect(() => startPlayer());
  return null;
}
```

## Pattern 5: Keyed Reset

Bad:

```tsx
useEffect(() => {
  resetDraft(userId);
}, [userId]);
```

Better:

```tsx
return <DraftEditor key={userId} userId={userId} />;
```

Use this when the UX truly wants a fresh component instance for each identity.

## Architecture Guidance

No-direct-`useEffect` often forces cleaner component boundaries:

- parents own orchestration
- children assume preconditions are met
- lifecycle boundaries become explicit in the tree

If a component becomes difficult to rewrite without an effect, consider lifting orchestration up or splitting the component into a persistent shell plus a conditionally mounted instance.
