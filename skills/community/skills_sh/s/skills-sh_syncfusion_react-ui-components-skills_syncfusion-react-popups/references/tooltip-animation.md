# Animation — Syncfusion React Tooltip

## Table of Contents
- [animation Property](#animation-property)
- [Available Effects](#available-effects)
- [Custom Duration and Delay](#custom-duration-and-delay)
- [Disabling Animation](#disabling-animation)
- [Animating via open() and close() Methods](#animating-via-open-and-close-methods)
- [Transition Effect (CSS Transitions)](#transition-effect-css-transitions)

---

## animation Property

The `animation` prop accepts an `AnimationModel` object with `open` and `close` keys, each describing the animation for that state:

```tsx
const tooltipAnimation = {
  open:  { effect: 'ZoomIn',  duration: 1000, delay: 0 },
  close: { effect: 'ZoomOut', duration: 500,  delay: 0 }
};

<TooltipComponent animation={tooltipAnimation} content="Zoom animation">
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

**Defaults:**
- `open`:  `{ effect: 'FadeIn',  duration: 150, delay: 0 }`
- `close`: `{ effect: 'FadeOut', duration: 150, delay: 0 }`

---

## Available Effects

| Effect | Direction |
|--------|-----------|
| `FadeIn` / `FadeOut` | Opacity fade |
| `FadeZoomIn` / `FadeZoomOut` | Fade + scale |
| `FlipXDownIn` / `FlipXDownOut` | Flip on X axis downward |
| `FlipXUpIn` / `FlipXUpOut` | Flip on X axis upward |
| `FlipYLeftIn` / `FlipYLeftOut` | Flip on Y axis leftward |
| `FlipYRightIn` / `FlipYRightOut` | Flip on Y axis rightward |
| `ZoomIn` / `ZoomOut` | Scale zoom |
| `None` | No animation |

> Flip effects look best when `showTipPointer={false}` since the rotating tooltip would conflict visually with the tip arrow.

---

## Custom Duration and Delay

Each animation model supports:
- `effect` — animation name (see table above)
- `duration` — milliseconds for the animation (default `150`)
- `delay` — milliseconds to wait before starting the animation (default `0`)

```tsx
const slowOpen = {
  open:  { effect: 'FadeZoomIn',  duration: 600, delay: 200 },
  close: { effect: 'FadeZoomOut', duration: 300, delay: 0 }
};

<TooltipComponent animation={slowOpen} content="Slow open, fast close">
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

---

## Disabling Animation

Set `effect` to `'None'` for instant show/hide with no transition:

```tsx
const noAnimation = {
  open:  { effect: 'None' },
  close: { effect: 'None' }
};

<TooltipComponent animation={noAnimation} content="Instant tooltip">
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

> Useful for draggable scenarios where animation would lag behind position updates.

---

## Animating via open() and close() Methods

Pass `TooltipAnimationSettings` directly to `open()` or `close()` to override the default animation for a specific interaction:

```tsx
import * as React from 'react';
import { TooltipComponent, TooltipAnimationSettings } from '@syncfusion/ej2-react-popups';

function App() {
  let tooltipRef: TooltipComponent;

  function handleClick(): void {
    if (tooltipRef.element.getAttribute('data-tooltip-id')) {
      const closeAnim: TooltipAnimationSettings = { effect: 'FadeOut', duration: 1000 };
      tooltipRef.close(closeAnim);
    } else {
      const openAnim: TooltipAnimationSettings = { effect: 'FadeIn', duration: 1000 };
      tooltipRef.open(tooltipRef.element, openAnim);
    }
  }

  return (
    <TooltipComponent
      ref={t => (tooltipRef = t)}
      content="Custom animation via method"
      opensOn="Custom"
    >
      <div id="target" onClick={handleClick}>Click Here</div>
    </TooltipComponent>
  );
}
export default App;
```

- Animation passed to `open()` / `close()` takes precedence over the `animation` prop for that call.
- If no animation is passed to the method, the `animation` prop values are used.

---

## Transition Effect (CSS Transitions)

Apply CSS position transitions via the `beforeRender` event to create a smooth tooltip-sliding effect across targets:

```tsx
import * as React from 'react';
import { TooltipComponent, TooltipEventArgs } from '@syncfusion/ej2-react-popups';

function App() {
  let tooltipRef: TooltipComponent;

  const defaultAnimation = {
    open:  { effect: 'ZoomIn',  duration: 500 },
    close: { effect: 'ZoomOut', duration: 500 }
  };

  function onBeforeRender(args: TooltipEventArgs): void {
    if (args.element) {
      // Disable animation on first render to allow CSS transition to take over
      tooltipRef.animation = { open: { effect: 'None' } };
      args.element.style.display = 'block';
      args.element.style.transitionProperty = 'left,top';
      args.element.style.transitionDuration = '1000ms';
    }
  }

  function onAfterClose(args: TooltipEventArgs): void {
    // Restore animation after close
    tooltipRef.animation = defaultAnimation;
  }

  return (
    <TooltipComponent
      ref={t => (tooltipRef = t)}
      target=".circle-tool"
      animation={defaultAnimation}
      closeDelay={1000}
      beforeRender={onBeforeRender}
      afterClose={onAfterClose}
    >
      <div className="circle-tool" title="Turtle" />
      <div className="circle-tool" title="Snake" />
      <div className="circle-tool" title="Croc" />
    </TooltipComponent>
  );
}
export default App;
```

**How it works:**
1. On `beforeRender`, temporarily replace animation with `None` so the tooltip renders immediately.
2. Set CSS `transition` on `left` and `top` so the browser animates position changes.
3. On `afterClose`, restore the original animation for future interactions.

---

## See Also
- [Open Mode](open-mode.md) — `open()`, `close()` methods
- [Customization](customization.md) — `showTipPointer` for flip effects
- [API Reference](api.md) — `animation`, `AnimationModel`, `TooltipAnimationSettings`, `beforeRender`, `afterClose`
