# Technical template

The primary implementation reference is [The Pudding website starter](https://github.com/the-pudding/website). Inspect its current README and branch state before starting because the repository is migrating from Svelte 4 to Svelte 5.

## Use the official starter directly when

- this is a new standalone visual story;
- Svelte and static/SSR output fit the deployment target;
- the editorial team benefits from its content/data workflow;
- the story needs reusable scrolly, viewport, and chart helpers.

Initialize from the current supported starter, then remove unused demo code. Do not copy Pudding branding, logos, or house fonts.

## Port the architecture when

- work occurs inside an existing React, Next.js, Vue, Sites, or CMS application;
- deployment constraints make the starter unsuitable;
- replacing the current stack would create more risk than value.

Preserve these boundaries:

```text
source data
  -> normalize and validate
  -> derive story states
  -> render marks from state
  -> update state from scroll or controls
  -> annotate with reader-facing copy
```

The renderer should not parse raw data, and the scroll observer should not directly mutate dozens of SVG attributes.

## Scrolly geometry

A robust structure:

```html
<section class="scrolly">
  <div class="graphic" aria-label="..."></div>
  <div class="steps">
    <article data-step="0">...</article>
    <article data-step="1">...</article>
  </div>
</section>
```

```css
.graphic {
  position: sticky;
  top: 0;
  min-height: 70svh;
}
```

Use IntersectionObserver or Scrollama to set a discrete active step. Use CSS sticky rather than calculating and writing fixed positions on every scroll event.

Do not use a fixed `100vh` step height as the only mobile strategy. Browser chrome changes the visual viewport and can cause jumps or covered text.

## State model

Represent each authored beat as data:

```js
const storyStates = [
  { id: "example", filter: "case-17", layout: "detail", annotation: "..." },
  { id: "context", filter: "all", layout: "distribution", annotation: "..." },
  { id: "mechanism", filter: "all", layout: "grouped", annotation: "..." }
];
```

Transitions compare previous and next states. Backscroll applies the same state deterministically. Keep URL-controlled exploratory state separate from authored scroll state.

For a React-style implementation, keep the observer and renderer joined only by an active-state id:

```tsx
const [activeId, setActiveId] = useState(storyStates[0].id);
const activeState = storyStatesById[activeId];

return (
  <Scrolly onStepEnter={(id) => setActiveId(id)}>
    <Graphic state={activeState} reducedMotion={reducedMotion} />
    <Steps states={storyStates} />
  </Scrolly>
);
```

`Graphic` must be a deterministic function of the full state. Do not encode transitions as an irreversible list of mutations; that breaks backscroll and refresh-at-mid-story behavior.

## Rendering and performance

- Use SVG for annotated marks and moderate item counts.
- Use canvas/WebGL for dense particles or maps, with an accessible text/SVG summary.
- Precompute expensive layouts and derived fields.
- Avoid React/Svelte state updates on every raw scroll event.
- Use `requestAnimationFrame` only when continuous progress is essential.
- Virtualize long lists and small-multiple fields.
- Reserve media dimensions to prevent layout shift.

## Reduced motion

At minimum:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Also shorten or bypass JavaScript tweens. Apply the final state immediately and preserve annotations and data labels.

## Sticky and interaction

If the sticky layer contains controls, ensure it can receive pointer events and does not sit under an overlay. If it is purely visual, set non-interactive layers to `pointer-events: none`. Test Safari iOS, Chrome Android emulation, and keyboard focus while the section is sticky.

## Responsive testing

Test:

- 320 × 568 and 390 × 844 phone viewports;
- 768 × 1024 tablet;
- 1440 × 900 desktop;
- landscape phone;
- 200% browser zoom;
- reduced motion;
- slow CPU and network profile.

Validate that the same thesis is available even if the rich interaction becomes a static or step-based fallback.

## Minimum automated QA

When the project has a browser-test setup, add a small Playwright suite that:

1. loads the opening without console errors;
2. scrolls to every step and asserts its state id;
3. scrolls backward and checks restoration;
4. tabs through every control and activates it by keyboard;
5. runs at 390 × 844 and 1440 × 900;
6. emulates reduced motion and confirms the final state and labels remain;
7. captures screenshots of the opening, central reveal, and ending.

Automation does not replace data and copy review. Record the tested browser, viewport, and commit in `qa-notes.md`.

## Official process references

- [Responsive scrollytelling best practices](https://pudding.cool/process/responsive-scrollytelling/)
- [Sticky scrollytelling implementation](https://pudding.cool/process/scrollytelling-sticky/)
- [Pudding's no-code and chart workflow overview](https://pudding.cool/process/no-code-charts/)
- [Roll-your-own scrollytelling demo](https://pudding.cool/process/how-to-implement-scrollytelling/demo/rollyourown/)
