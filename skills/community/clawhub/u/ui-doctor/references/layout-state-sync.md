# Layout & State Synchronization

Root-cause patterns for the most common class of "UI feels broken/inconsistent" bug: two or more components each maintaining their own copy of state that should be shared, so they drift out of sync when one changes.

## 1. The core anti-pattern: duplicated source of truth

**Symptom**: Sidebar collapses, main content area doesn't resize. Modal closes, backdrop stays. Tab changes, URL doesn't update (or vice versa).

**Root cause pattern**: each component holds its own local `useState` (or equivalent) for what is conceptually one shared value, instead of one owning source that all consumers read from.

```
❌ Broken pattern:
<Sidebar />         // has its own useState(collapsed)
<MainContent />     // has its own useState(sidebarWidth), never told sidebar changed

✅ Fixed pattern (lifted state / shared context):
<LayoutProvider>          // owns `collapsed` state, exposes via context
  <Sidebar />              // reads collapsed from context, calls toggle()
  <MainContent />          // reads collapsed from context, computes margin/width from it
</LayoutProvider>
```

## 2. Where to look for this pattern (in order of likelihood)

1. **Independent `useState`/`ref` in sibling components** for anything describing shared layout (collapsed/expanded, open/closed, active tab, selected item, current breakpoint).
2. **CSS driven by a hardcoded class/value in one component**, while a sibling's CSS is driven by a *different* hardcoded value that's supposed to match it (e.g. sidebar sets `width: 0` via its own class, main content has a hardcoded `margin-left: 240px` that never changes) — this is the same bug expressed in CSS instead of JS.
3. **Prop drilling that stops partway** — a value is lifted partially (passed to some descendants but a sibling further down the tree reads stale local state instead of the lifted prop).
4. **Animation/transition timing mismatch** — even when state *is* shared correctly, if the sidebar's collapse transition and the main content's margin transition use different `motion.duration`/easing tokens, they'll visually desync mid-animation even though the end state is correct. Check that both sides of a synchronized layout change share the same transition token (see `design-system-architect`'s motion tokens if that skill's output is present).

## 3. Fix strategies, in order of preference

1. **Lift state to a common ancestor** (or a dedicated layout context/provider) — the default fix for React/Vue-style component trees. All consumers read from one place.
2. **CSS custom property set at a shared ancestor**, read by all descendants (`--sidebar-width: 240px` set on a layout root, both sidebar width and content margin reference `var(--sidebar-width)`) — good when the relationship is purely visual/CSS and doesn't need JS logic beyond toggling a class.
3. **Global/shared state store** (Zustand, Redux, Context+useReducer, signals) — appropriate when more than 2 components need the same layout state, or state needs to persist across route changes.
4. **`ResizeObserver`/`matchMedia` listeners feeding one shared value** — for cases driven by actual measured size rather than a toggle (e.g. a sidebar that's user-resizable via drag, not just collapse/expand).

Never fix this class of bug by adding a `setTimeout`/manual re-sync call between components as a patch — that's treating the symptom (visual desync) without removing the duplicated state, and it will re-break under different timing (e.g. slower devices, different animation duration).

## 4. Verifying the fix

After lifting state or switching to a shared source, confirm:
- [ ] Toggling the state from any single trigger point updates *all* dependent components in the same render/paint — no manual re-sync calls needed anywhere.
- [ ] The same bug pattern doesn't exist elsewhere in the codebase for other toggle-style components (accordions, modals, tabs, drawers) — audit broadly, not just the reported instance (see Step 4 of `SKILL.md`).
- [ ] Transition timing tokens match between all components that animate together as a result of the same state change.
