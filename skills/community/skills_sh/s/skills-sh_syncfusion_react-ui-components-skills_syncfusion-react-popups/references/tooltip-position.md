# Position — Syncfusion React Tooltip

## Table of Contents
- [12 Static Positions](#12-static-positions)
- [Tip Pointer Positioning](#tip-pointer-positioning)
- [Dynamic Positioning (Draggable Targets)](#dynamic-positioning-draggable-targets)
- [Mouse Trailing](#mouse-trailing)
- [Offset Values](#offset-values)
- [Collision Handling](#collision-handling)

---

## 12 Static Positions

Use the `position` prop to place the tooltip relative to its target. Default is `TopCenter`.

| Group | Values |
|-------|--------|
| Top | `TopLeft`, `TopCenter`, `TopRight` |
| Bottom | `BottomLeft`, `BottomCenter`, `BottomRight` |
| Left | `LeftTop`, `LeftCenter`, `LeftBottom` |
| Right | `RightTop`, `RightCenter`, `RightBottom` |

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  let tooltipRef: TooltipComponent;

  function handleChange(e: React.ChangeEvent<HTMLSelectElement>) {
    tooltipRef.position = e.target.value as any;
    tooltipRef.refresh();
  }

  return (
    <div>
      <TooltipComponent
        ref={t => (tooltipRef = t)}
        content="Tooltip Content"
        target="#tooltip"
        position="TopCenter"
      >
        <div id="tooltip">Show Tooltip</div>
      </TooltipComponent>

      <select onChange={handleChange} defaultValue="TopCenter">
        <option value="TopLeft">Top Left</option>
        <option value="TopCenter">Top Center</option>
        <option value="TopRight">Top Right</option>
        <option value="BottomLeft">Bottom Left</option>
        <option value="BottomCenter">Bottom Center</option>
        <option value="BottomRight">Bottom Right</option>
        <option value="LeftTop">Left Top</option>
        <option value="LeftCenter">Left Center</option>
        <option value="LeftBottom">Left Bottom</option>
        <option value="RightTop">Right Top</option>
        <option value="RightCenter">Right Center</option>
        <option value="RightBottom">Right Bottom</option>
      </select>
    </div>
  );
}
export default App;
```

> Call `refresh()` after programmatically changing `position` to reposition the tooltip immediately.

---

## Tip Pointer Positioning

Control the arrow indicator with two props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `showTipPointer` | `boolean` | `true` | Show or hide the arrow |
| `tipPointerPosition` | `TipPointerPosition` | `'Auto'` | `Auto` \| `Start` \| `Middle` \| `End` |

**Hide the tip pointer:**
```tsx
<TooltipComponent content="No arrow" showTipPointer={false}>
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

**Pin arrow to Start:**
```tsx
<TooltipComponent
  content="Arrow at start"
  tipPointerPosition="Start"
  target="#target"
>
  <button className="e-btn" id="target">Hover</button>
</TooltipComponent>
```

> `Auto` — arrow auto-adjusts within the target's length and never points outside the target element.  
> `Start`, `Middle`, `End` — pin the arrow to a fixed position along the tooltip edge.

---

## Dynamic Positioning (Draggable Targets)

Use the `refresh(element)` method to reposition the tooltip as a target moves (e.g., draggable elements):

```tsx
import * as React from 'react';
import { TooltipComponent } from '@syncfusion/ej2-react-popups';
import { Draggable } from '@syncfusion/ej2-base';

function App() {
  let tooltipRef: TooltipComponent;

  React.useEffect(() => {
    const el = document.getElementById('demoSmart') as HTMLElement;
    const drag = new Draggable(el, {
      clone: false,
      dragArea: '#targetContainer',
      drag: (args: any) => {
        if (args.element.getAttribute('data-tooltip-id') === null) {
          tooltipRef.open(args.element);
        } else {
          tooltipRef.refresh(args.element);
        }
      },
      dragStart: (args: any) => {
        if (args.element.getAttribute('data-tooltip-id') === null) {
          tooltipRef.open(args.element);
        }
      },
      dragStop: () => {
        tooltipRef.close();
      }
    });
  }, []);

  const noAnimation = { open: { effect: 'None' }, close: { effect: 'None' } };

  return (
    <div id="targetContainer">
      <TooltipComponent
        ref={t => (tooltipRef = t)}
        target="#demoSmart"
        content="Drag me !!!"
        animation={noAnimation}
      >
        <div id="demoSmart" style={{ width: 60, height: 60, background: '#4285f4' }} />
      </TooltipComponent>
    </div>
  );
}
export default App;
```

- `refresh(target?)` — recalculates the tooltip's position relative to the given element.

---

## Mouse Trailing

Set `mouseTrail={true}` to make the tooltip follow the mouse cursor instead of anchoring to the target:

```tsx
<TooltipComponent
  content="I follow your mouse!"
  mouseTrail={true}
  showTipPointer={false}
>
  <div id="target" style={{ width: '300px', height: '150px', background: '#f0f0f0' }}>
    Move your mouse here
  </div>
</TooltipComponent>
```

> When `mouseTrail` is enabled, `tipPointerPosition` values (`Start`, `End`, `Middle`) are ignored — the pointer auto-adjusts to prevent pointing outside the target.

---

## Offset Values

Add pixel-level distance between the target and the tooltip with `offsetX` and `offsetY`:

```tsx
<TooltipComponent
  content="Offset tooltip"
  offsetX={30}
  offsetY={30}
  showTipPointer={false}
  mouseTrail={true}
>
  <div id="target">Hover Me</div>
</TooltipComponent>
```

- `offsetX` — horizontal distance from target in pixels.
- `offsetY` — vertical distance from target in pixels.

---

## Collision Handling

The tooltip automatically adjusts when it would overflow the viewport:
- **Horizontal overflow** → tooltip shifts horizontally.
- **Vertical overflow** → tooltip flips to the opposite side.

**windowCollision** — when `true` and using the `target` prop, collision is calculated against the viewport (window) rather than the tooltip element itself:

```tsx
<TooltipComponent
  content="Collision-aware tooltip"
  target=".item"
  windowCollision={true}
  position="TopCenter"
>
  <div className="item">Near Edge</div>
</TooltipComponent>
```

> Use `windowCollision={true}` when targets are near the viewport edge and you need collision detection to reference the window boundary.

---

## See Also
- [Customization](customization.md) — `cssClass`, tip pointer shape, dimensions
- [Animation](animation.md) — open/close effects
- [API Reference](api.md) — `position`, `tipPointerPosition`, `mouseTrail`, `offsetX`, `offsetY`, `windowCollision`, `refresh()`
