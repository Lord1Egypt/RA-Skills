# SwiftUI — State, Identity, Layout, Performance

Two ideas explain nearly every SwiftUI bug. **Identity**: SwiftUI matches views across renders by position in the hierarchy plus explicit `.id()`; state lives with identity, so when identity changes, state resets. **Body purity**: `body` is a pure description that may run many times per frame, so anything side-effecting or expensive inside it is a bug waiting for a busy screen.

## Choosing a State Property Wrapper

| Wrapper | Ownership | Recreated when the view struct is recreated? | Use |
|---|---|---|---|
| `@State` | The view owns the value | No — survives while identity holds | Local value-type state; with `@Observable`, also the owned object |
| `@Binding` | Borrowed read/write | n/a | Child mutating the parent's state |
| `@StateObject` | The view owns the object | No — created exactly once per identity | `ObservableObject` the view creates (legacy path) |
| `@ObservedObject` | Someone else owns it | Yes — a new instance every recreation | `ObservableObject` passed in (legacy path) |
| `@EnvironmentObject` / `@Environment` | Injected by an ancestor | n/a | Cross-cutting dependencies |
| `@Bindable` | Borrowed, for `@Observable` types | n/a | Getting bindings out of an `@Observable` model |

- The `@StateObject`/`@ObservedObject` mistake: creating the object inline on an `@ObservedObject` property. The view struct is recreated on every parent render, so the object is recreated, so state resets and network calls restart.
- `@Observable` (`swift >=5.9`, Observation) replaces `ObservableObject` + `@Published`: hold it in `@State` where it is owned, pass it as a plain `let` where it is not, and use `@Bindable` for bindings. It also fixes the biggest performance flaw of the old path — an `ObservableObject` invalidates every observing view on any `@Published` change, while Observation tracks per-property reads.
- `@EnvironmentObject` traps at runtime when nothing injected it. Inject at the root and in every preview; there is no compile-time check.
- `@State` should be `private`. A non-private `@State` invites callers to pass an initial value that will be ignored on every render after the first.
- Initializing `@State` from an init parameter needs `_value = State(initialValue: x)` — and the initial value is used exactly once per identity, which is why "the view shows the old data" happens.

## Identity — Why State Resets or Refuses To

- Structural identity: position in the view tree. `if condition { A() } else { B() }` creates two different identities, so switching branches destroys state. When A and B are the same view with different data, prefer one view and change the data.
- Explicit identity: `.id(value)`. Changing it destroys and recreates the subtree with fresh state — a deliberate reset tool, and a bug when the value changes unintentionally (`.id(UUID())` recreates on every render).
- `ForEach` needs stable ids. Using array offsets as ids breaks on insert and delete: rows keep the wrong state and animations go sideways. Use `Identifiable` with a real, persistent id.
- Duplicate ids in a `ForEach` produce undefined rendering, not an error.
- A `NavigationStack` push does not remove the source view: `onAppear` fires again on the way back. Use `.task` for work that should follow the view's lifetime, and gate one-time work on a stored flag.

## Redraws and Performance

- `let _ = Self._printChanges()` at the top of `body` prints which property caused this invalidation — the fastest way to end a "why does this redraw" argument.
- `body` runs often. No sorting, no date formatting, no `JSONDecoder`, no `DispatchQueue`, no allocations you can hoist. Compute in the model, expose the ready value.
- `AnyView` erases structural identity, disabling SwiftUI's diffing for that subtree. Prefer `@ViewBuilder`, `Group`, or generics; keep `AnyView` for genuinely heterogeneous cases.
- `List` recycles rows; `LazyVStack` inside `ScrollView` creates rows lazily but does not recycle them, so a very long `LazyVStack` grows memory where a `List` does not.
- `EquatableView` / `.equatable()` skips a subtree when its inputs compare equal — worth it for expensive leaf views, not as a blanket habit.
- Passing a closure that captures a whole view model into many rows defeats value-based diffing; pass the small values the row needs.

## Layout

- The layout contract is: parent proposes a size, child chooses its own, parent places it. Nothing forces a child to accept.
- `GeometryReader` accepts the full proposed size and stacks its content at topLeading. Placing one in a `VStack` to measure a child usually breaks the surrounding layout — measure with a preference key or `onGeometryChange`-style read, or put the reader in a `.background`/`.overlay` where it takes the host's size.
- `frame(maxWidth: .infinity)` means "accept as much as offered", not "be as wide as the screen". `fixedSize()` means "ignore the proposal, use my ideal size".
- Spacer inside a `ScrollView` has nothing to push against — the scroll view proposes unbounded space in its axis.
- Layout priority resolves competing greedy children; `layoutPriority` beats adding nested stacks to force a size.
- Custom layout: the `Layout` protocol is the supported path; `alignmentGuide` handles the narrower "line these two things up" case.

## Animation

- `withAnimation { state = x }` animates everything driven by that change, including views you forgot about. `.animation(_:value:)` scopes to one value — prefer it.
- `.animation(_:)` without a value was deprecated for exactly this reason: it animated unrelated changes.
- `matchedGeometryEffect` needs both views to exist in the same `Namespace` and only one to be `isSource`.
- `transition` only applies when the view is inserted or removed **inside** an animated change; adding a transition without animating the condition does nothing.
- Animating a view whose identity changes plays an insert/remove, not a move — a mismatch between the animation you wrote and the one you see is usually an identity change (see above).

## Data Flow Beyond One Screen

- `@Environment` for dependencies (services, formatters, theme); explicit parameters for data the view genuinely needs. Environment-injecting everything makes previews unbuildable.
- Bindings from a model: `@Bindable model` then `$model.field`. Deriving a `Binding` by hand (`Binding(get:set:)`) is fine, but a get/set pair that also mutates local `@State` produces two sources of truth and visible flicker.
- Do not mutate observed state from inside `body` — the runtime warns "Publishing changes from within view updates is not allowed" and the result is undefined. Move it into `.task`, `.onChange`, or a button action.
- Sheets: `.sheet(item:)` re-evaluates its content when the item changes; `.sheet(isPresented:)` captures the content closure's values at presentation time, which is why the wrong row's detail appears.

## Combine, Where It Still Appears

- A `sink` whose `AnyCancellable` is not stored is cancelled immediately — the subscription vanishes and nothing arrives.
- `receive(on:)` must come before the terminal subscriber to affect delivery; placed after, it does nothing.
- `assign(to: &$published)` keeps no strong reference to the target, unlike `assign(to:on:)`, which does — the standard Combine retain cycle in view models (`arc.md`).
- Use the `print("label")` operator to see every event (subscription, values, completion) when a pipeline is silent.
- For new code, `AsyncSequence` covers most of what Combine was used for (`concurrency.md`); Combine remains where a framework hands you a publisher.

## Previews and Testability

- Previews run the real code with a fake environment: an unfulfilled `@EnvironmentObject` crashes there first, which is a feature.
- Keep view models free of view types so they can be tested without a host.
- A preview that needs a network call needs a stub — injecting the service through `@Environment` is what makes that possible.
