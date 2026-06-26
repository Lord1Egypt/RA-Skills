# Open Mode — Syncfusion React Tooltip

## Table of Contents
- [opensOn Values](#openson-values)
- [Hover Mode](#hover-mode)
- [Click Mode](#click-mode)
- [Focus Mode](#focus-mode)
- [Custom Mode](#custom-mode)
- [Combining Multiple Modes](#combining-multiple-modes)
- [Sticky Mode](#sticky-mode)
- [Open and Close Delay](#open-and-close-delay)
- [Mobile Behavior](#mobile-behavior)

---

## opensOn Values

The `opensOn` prop controls when the tooltip becomes visible. Default: `'Auto'`.

| Value | Desktop Trigger | Mobile Trigger |
|-------|----------------|----------------|
| `Auto` | Hover or focus | Tap and hold |
| `Hover` | Mouse hover | Tap and hold |
| `Click` | Click | Single tap |
| `Focus` | Tab/focus | Single tap |
| `Custom` | None (programmatic only) | None (programmatic only) |

> `Auto` cannot be combined with other values. All other values can be combined with a space: `"Hover Click"`.

---

## Hover Mode

The default experience. Tooltip appears when the cursor enters the target:

```tsx
<TooltipComponent content="Tooltip from hover" opensOn="Hover" target="#hoverBtn">
  <button className="e-btn" id="hoverBtn">Hover Me</button>
</TooltipComponent>
```

---

## Click Mode

Tooltip appears when the user clicks the target element:

```tsx
<TooltipComponent content="Tooltip from click" opensOn="Click" target="#clickBtn">
  <button className="e-btn" id="clickBtn">Click Me</button>
</TooltipComponent>
```

---

## Focus Mode

Tooltip appears when the element receives keyboard focus (e.g., via Tab) and closes on blur:

```tsx
<TooltipComponent content="Focused!" opensOn="Focus" target="#focusInput">
  <span className="e-float-input">
    <input id="focusInput" type="text" placeholder="Tab to focus" />
  </span>
</TooltipComponent>
```

---

## Custom Mode

Tooltip is never shown by default interactions. You must call `open()` and `close()` manually. Useful for double-click, right-click, or any custom gesture:

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  let tooltipRef: TooltipComponent;
  let btnRef: HTMLButtonElement;

  function handleDoubleClick(): void {
    if (btnRef.getAttribute('data-tooltip-id')) {
      tooltipRef.close();
    } else {
      tooltipRef.open(btnRef);
    }
  }

  return (
    <TooltipComponent
      ref={t => (tooltipRef = t)}
      opensOn="Custom"
      content="Opened on double-click"
    >
      <button
        className="e-btn"
        ref={d => (btnRef = d)}
        onDoubleClick={handleDoubleClick}
      >
        Double Click to Open
      </button>
    </TooltipComponent>
  );
}
export default App;
```

**Toggle on single click:**
```tsx
function handleClick(): void {
  if (btnRef.getAttribute('data-tooltip-id')) {
    tooltipRef.close();
  } else {
    tooltipRef.open(btnRef);
  }
}
```

> `data-tooltip-id` is set on the target element when the tooltip is open — check this attribute to determine current state.

---

## Combining Multiple Modes

Separate values with a space to trigger on more than one interaction:

```tsx
{/* Opens on hover OR click */}
<TooltipComponent content="Hover or click me" opensOn="Hover Click">
  <button className="e-btn">Multi-trigger</button>
</TooltipComponent>
```

```tsx
{/* Opens on focus OR click */}
<TooltipComponent content="Focus or click" opensOn="Focus Click">
  <input type="text" />
</TooltipComponent>
```

> `Auto` cannot be part of a combined value.

---

## Sticky Mode

When `isSticky={true}`, the tooltip remains visible until the user clicks the × close icon:

```tsx
<TooltipComponent
  content="Click the × to close me"
  isSticky={true}
  position="BottomCenter"
>
  <button className="e-btn">Show Sticky Tooltip</button>
</TooltipComponent>
```

Combine with template content for rich, interactive tooltips:

```tsx
function richContent() {
  return <div><h4>Details</h4><p>Some long description...</p></div>;
}

<TooltipComponent content={richContent} isSticky={true} width="250px">
  <button className="e-btn">Rich Sticky Tooltip</button>
</TooltipComponent>
```

> Sticky mode is best experienced with scroll mode enabled (set a fixed `height` so content scrolls inside the tooltip).

---

## Open and Close Delay

Add a delay (in milliseconds) before the tooltip appears or disappears:

```tsx
<TooltipComponent
  content="Delayed tooltip"
  openDelay={1000}
  closeDelay={1000}
>
  <button className="e-btn">Hover Me</button>
</TooltipComponent>
```

- `openDelay` — wait this many ms after triggering before showing.
- `closeDelay` — wait this many ms after losing trigger before hiding.

Useful when tooltips appear on fast mouse movements and you want to avoid flickering.

---

## Mobile Behavior

On mobile, `Hover` behaves as tap-and-hold. The tooltip dismisses 1.5 seconds after the user lifts their finger (unless another action occurs first). `Click` and `Focus` respond to single taps.

---

## See Also
- [Content](content.md) — `beforeRender` for dynamic loading
- [Animation](animation.md) — `open()` and `close()` with animation settings
- [API Reference](api.md) — `opensOn`, `isSticky`, `openDelay`, `closeDelay`, `open()`, `close()`
