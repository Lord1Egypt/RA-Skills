# Modern Effects Catalogue — Tailwind v4 + shadcn/ui

A reference library of production-usable visual effects, expressed with Tailwind v4 utilities and arbitrary-value/CSS-variable escapes where a utility doesn't exist. Same underlying mechanisms as the `ui-master-static` skill's `modern-effects.md` (native CSS), just wired through Tailwind's class syntax and `@theme` tokens. **Use one signature effect per screen** — see the restraint note in `SKILL.md`.

## Glassmorphism

```tsx
<div className="rounded-xl border border-white/15 bg-white/8 p-6 shadow-lg backdrop-blur-xl backdrop-saturate-150">
  Frosted panel content
</div>
```

`backdrop-blur-xl` + `bg-white/8` (low-opacity background) + a light border is the full recipe. `backdrop-filter` is broadly supported but compositing-expensive — don't stack it across every card in a scrollable list, reserve it for headers, modals, and a handful of hero elements.

Fallback for non-supporting browsers via the `supports-` variant (Tailwind v4 built-in):

```tsx
<div className="bg-white/8 backdrop-blur-xl supports-[not(backdrop-filter:blur(1px))]:bg-neutral-900/90">
```

## Layered / mesh gradients

A flat two-stop `bg-gradient-to-r` reads as a template default. Layer multiple radial gradients via an arbitrary background value for a mesh-gradient look:

```tsx
<div
  className="absolute inset-0 -z-10"
  style={{
    backgroundImage: `
      radial-gradient(at 20% 20%, oklch(70% 0.15 250 / 0.5) 0px, transparent 50%),
      radial-gradient(at 80% 0%, oklch(75% 0.18 320 / 0.4) 0px, transparent 50%),
      radial-gradient(at 50% 100%, oklch(65% 0.16 180 / 0.35) 0px, transparent 50%)
    `,
  }}
/>
```

Tailwind's utility classes don't cover multi-layer radial gradients directly — this is a legitimate case for an inline `style` escape rather than fighting the utility system.

Animated conic-gradient border using `@property` (declare once in the CSS entrypoint alongside `@theme`, works identically under Tailwind since it's plain CSS):

```css
/* app/globals.css, outside @theme */
@property --angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

@keyframes spin-border {
  to { --angle: 360deg; }
}

.gradient-border::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: conic-gradient(from var(--angle), var(--color-primary), var(--color-accent), var(--color-primary));
  animation: spin-border 4s linear infinite;
  z-index: -1;
}
```

```tsx
<div className="gradient-border relative rounded-xl p-[2px]">
  <div className="rounded-[calc(theme(borderRadius.xl)-2px)] bg-background p-6">Content</div>
</div>
```

## Elevation

Use the shadow tokens from `design-tokens.md` (`shadow-xs` → `shadow-lg` already ship as Tailwind defaults, or override via `@theme`) — reserve larger shadows for genuinely floating elements. Colored/tinted shadows read as more polished for brand-forward cards:

```tsx
<div className="shadow-[0_8px_24px_-4px_var(--color-primary)]/25 rounded-xl border p-6">
```

## Scroll-driven animations (native CSS, no JS library)

Tailwind doesn't wrap `animation-timeline` in a utility — declare it as plain CSS (in the entrypoint or a `<style>` block) and apply the class name normally:

```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  animation: reveal-in linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
@keyframes reveal-in {
  to { opacity: 1; transform: translateY(0); }
}
@supports not (animation-timeline: view()) {
  .reveal { opacity: 1; transform: none; animation: none; }
}
```

```tsx
<div className="reveal rounded-xl border p-6">Fades/slides in on scroll</div>
```

**Support**: Chromium-first, growing but not universal — the `@supports` fallback above is required, not optional.

## Micro-interactions

Tailwind's `transition-*` + state variants (`hover:`, `active:`, `focus-visible:`) cover almost all of this natively — this is where Tailwind is at its strongest relative to hand-written CSS:

```tsx
<button
  className="rounded-md bg-primary px-4 py-2 text-primary-foreground
             transition-[transform,box-shadow,background-color] duration-150 ease-out
             hover:-translate-y-0.5 hover:shadow-sm hover:bg-primary/90
             active:translate-y-0 active:duration-75
             focus-visible:outline-2 focus-visible:outline-primary focus-visible:outline-offset-2"
>
  Action
</button>
```

Keep `duration-150` for frequent small interactions; reserve `duration-300`+ for larger state changes (panel open/close).

## 3D transforms

```tsx
<div
  className="rounded-xl border p-6 transition-transform duration-300 ease-out will-change-transform
             [transform-style:preserve-3d] hover:[transform:perspective(800px)_rotateX(6deg)_rotateY(-6deg)_scale(1.02)]"
>
  Tilt on hover
</div>
```

For mouse-tracked tilt (rotation follows cursor), set CSS custom properties from a `pointermove` handler and reference them in an inline `style`, same pattern as `ui-master-static`'s `modern-effects.md` — Tailwind utilities can't read runtime pointer coordinates, this always needs a small amount of JS.

```tsx
function TiltCard({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);

  function handlePointerMove(e: React.PointerEvent<HTMLDivElement>) {
    const rect = ref.current!.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    ref.current!.style.setProperty("--rx", `${y * -12}deg`);
    ref.current!.style.setProperty("--ry", `${x * 12}deg`);
  }

  return (
    <div
      ref={ref}
      onPointerMove={handlePointerMove}
      onPointerLeave={() => {
        ref.current!.style.setProperty("--rx", "0deg");
        ref.current!.style.setProperty("--ry", "0deg");
      }}
      className="rounded-xl border p-6 transition-transform duration-300 ease-out [transform-style:preserve-3d]"
      style={{ transform: "perspective(800px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))" }}
    >
      {children}
    </div>
  );
}
```

## Complex keyframe animations

Register named keyframes via `@theme` in v4 (this is the CSS-first way to make a custom keyframe available as a utility-style animation class):

```css
@theme {
  --animate-pulse-settle: pulse-settle 600ms cubic-bezier(0.4, 0, 0.2, 1) both;
}

@keyframes pulse-settle {
  0%   { transform: scale(0.9); opacity: 0; }
  40%  { transform: scale(1.05); opacity: 1; }
  70%  { transform: scale(0.98); }
  100% { transform: scale(1); }
}
```

```tsx
<span className="animate-pulse-settle">New</span>
```

Declaring the animation in `@theme` generates the `animate-pulse-settle` utility automatically — no separate `<style>` block needed at the call site.

## Checklist before shipping an effects-heavy screen

- [ ] Exactly one signature effect anchors this screen; everything else stays quiet
- [ ] Every scroll-driven or large-motion effect has a `prefers-reduced-motion:reduce` variant (Tailwind: `motion-reduce:` modifier, e.g. `motion-reduce:animate-none motion-reduce:transition-none`)
- [ ] Chromium-first features (`animation-timeline`) have a `@supports` fallback
- [ ] `backdrop-blur` usage is bounded, not stacked across a scrollable list
- [ ] Micro-interaction durations stay in the 100–200ms range; longer durations are reserved for intentional showcase moments
