# GSAP Debug Checklist

Use this checklist when animations aren't working as expected.

---

## 1. Target & Selector Issues

- [ ] **Element exists?** Confirm the target element exists in DOM when animation runs
- [ ] **Selector correct?** Check for typos, wrong class/id names
- [ ] **Scope correct?** In React/Next.js, ensure `.class` selectors are scoped to component
- [ ] **SSR timing?** Only run GSAP code after component mounts (client-side)
- [ ] **Ref populated?** Ensure `ref.current` is not null before animating

**Quick test:**
```js
console.log(gsap.utils.toArray(".target")); // Should return array of elements
```

---

## 2. CSS Conflicts

- [ ] **Transform overrides?** CSS `transform` will fight with GSAP transforms
- [ ] **Transition on element?** CSS `transition` causes double-animation
- [ ] **Display/visibility?** `display: none` prevents animation; use `autoAlpha` instead
- [ ] **Opacity initial state?** Element might already be at target opacity

**Quick fix:**
```js
gsap.set(".target", { clearProps: "all" }); // Reset to CSS defaults
```

---

## 3. Timeline Issues

- [ ] **Using position params?** Replace delays with `<`, `>`, `+=0.2`, labels
- [ ] **Defaults conflicting?** Check if timeline `defaults` override tween-specific values
- [ ] **Inspect timing:** `gsap.globalTimeline.timeScale(0.2)` to slow down
- [ ] **Add labels:** `tl.addLabel("start")` for better debugging

**Debug pattern:**
```js
const tl = gsap.timeline({ onUpdate: () => console.log(tl.progress()) });
```

---

## 4. ScrollTrigger Issues

- [ ] **Enable markers:** `markers: true` (remove in production!)
- [ ] **Validate start/end:** Do positions make sense for element sizes?
- [ ] **Call refresh:** `ScrollTrigger.refresh()` after dynamic content loads
- [ ] **Custom scroller:** Set `scroller: ".container"` if not using window
- [ ] **Pin issues:** Try `anticipatePin: 1`, check for layout shifts
- [ ] **Duplicate triggers:** Use `gsap.context()` + `ctx.revert()` in React

**Debug pattern:**
```js
ScrollTrigger.create({
  trigger: ".section",
  start: "top 80%",
  markers: true,
  onEnter: () => console.log("Entered"),
  onLeave: () => console.log("Left"),
  onToggle: self => console.log("Active:", self.isActive)
});
```

---

## 5. Performance Issues

### Pointer/Mouse Jank
- [ ] **Using quickTo?** Never create new tweens on every pointer event
- [ ] **Using quickSetter?** For ultra-fast updates without tweens

**Fix:**
```js
const xTo = gsap.quickTo(".cursor", "x", { duration: 0.2 });
const yTo = gsap.quickTo(".cursor", "y", { duration: 0.2 });
```

### Layout Thrash
- [ ] **Batch reads/writes:** Read all `getBoundingClientRect()` first, then set values
- [ ] **Avoid layout props:** Prefer `x/y/scale/rotation` over `top/left/width/height`

### Too Many Triggers
- [ ] **Use batching:** `ScrollTrigger.batch()` for list items
- [ ] **Consolidate:** One timeline per section, not per element
- [ ] **Reduce count:** Do you really need 50 scroll triggers?

---

## 6. React/Next.js Issues

- [ ] **Client component?** Add `"use client"` directive
- [ ] **Using context?** Wrap in `gsap.context()` and call `ctx.revert()` on cleanup
- [ ] **Duplicate animations?** StrictMode causes double-mount; context handles this
- [ ] **Ref timing:** Use `useLayoutEffect` for DOM-dependent animations
- [ ] **Deps array:** Include dependencies that should re-trigger animations

**Correct pattern:**
```jsx
useLayoutEffect(() => {
  const ctx = gsap.context(() => {
    gsap.from(".box", { y: 50 });
  }, containerRef);
  return () => ctx.revert();
}, []);
```

---

## 7. Plugin Issues

- [ ] **Registered?** `gsap.registerPlugin(ScrollTrigger, Flip, ...)`
- [ ] **Imported?** Import from correct path
- [ ] **Available?** Some plugins require GSAP membership (now all free)
- [ ] **SSR-safe?** Don't import/register during SSR

---

## 8. Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "Cannot read property 'x' of null" | Target doesn't exist | Check selector, timing |
| "GSAP target not found" | Invalid selector | Verify element exists |
| "Invalid property" | Typo or wrong property name | Check GSAP docs |
| "ScrollTrigger.refresh()" | Layout changed after creation | Call refresh() after content loads |
| Duplicate animations | No cleanup in React | Use context + revert |

---

## 9. Debug Tools

```js
// Slow motion
gsap.globalTimeline.timeScale(0.2);

// Pause everything
gsap.globalTimeline.pause();

// List all tweens
gsap.globalTimeline.getChildren();

// List all ScrollTriggers
ScrollTrigger.getAll();

// Kill specific trigger
ScrollTrigger.getById("myTrigger").kill();

// Kill all
gsap.killTweensOf(".target");
ScrollTrigger.killAll();

// GSDevTools (visual debugger)
GSDevTools.create({ animation: myTimeline });
```

---

## 10. Quick Sanity Checks

1. **Simplest test:** Does `gsap.to(".box", { x: 100 })` work?
2. **Plugin test:** Does `console.log(ScrollTrigger)` show the plugin?
3. **Timing test:** Wrap in `setTimeout` - if it works, it's a timing issue
4. **CSS test:** Add `!important` to CSS properties to see if they're fighting