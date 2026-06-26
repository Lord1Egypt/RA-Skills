# API Reference — Syncfusion React Tooltip

**Source:** https://ej2.syncfusion.com/react/documentation/api/tooltip/index-default  
**Component:** `TooltipComponent` from `@syncfusion/ej2-react-popups`

> ⚠️ Only use APIs listed in this file. Do not reference undocumented or non-existent properties, methods, or events.

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Type Definitions](#type-definitions)
- [Position Values](#position-values)
- [TipPointerPosition Values](#tippointerposition-values)
- [Animation Effects](#animation-effects)

---

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `animation` | `AnimationModel` | `{ open: { effect: 'FadeIn', duration: 150, delay: 0 }, close: { effect: 'FadeOut', duration: 150, delay: 0 } }` | Open and close animation settings |
| `closeDelay` | `number` | `0` | Delay (ms) before closing the tooltip |
| `container` | `string \| HTMLElement` | `body` | Container element where the tooltip popup is appended |
| `content` | `string \| HTMLElement \| Function` | — | Tooltip display content (string, HTML, or JSX template function) |
| `cssClass` | `string` | `null` | Custom CSS class(es) applied to the tooltip element |
| `enableHtmlParse` | `boolean` | `true` | Parse HTML string content into DOM elements; set `false` to display raw HTML string |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitize untrusted HTML/scripts before rendering |
| `enablePersistence` | `boolean` | `false` | Persist component state across page reloads |
| `enableRtl` | `boolean` | `false` | Render component in right-to-left direction |
| `height` | `string \| number` | `'auto'` | Tooltip height; overflow enables scroll mode |
| `htmlAttributes` | `{ [key: string]: string }` | `{}` | Additional HTML attributes (tabindex, title, etc.) on the tooltip popup root element |
| `isSticky` | `boolean` | `false` | Keep tooltip visible until user clicks the close button |
| `locale` | `string` | `''` | Override global culture/localization (default `'en-US'`) |
| `mouseTrail` | `boolean` | `false` | Tooltip follows mouse pointer movement |
| `offsetX` | `number` | `0` | Horizontal distance (px) between target and tooltip |
| `offsetY` | `number` | `0` | Vertical distance (px) between target and tooltip |
| `openDelay` | `number` | `0` | Delay (ms) before opening the tooltip |
| `opensOn` | `string` | `'Auto'` | Trigger mode: `Auto` \| `Hover` \| `Click` \| `Focus` \| `Custom` (combinable with space, e.g., `"Hover Click"`) |
| `position` | `Position` | `'TopCenter'` | Placement relative to target element (12 values) |
| `showTipPointer` | `boolean` | `true` | Show or hide the tip arrow pointer |
| `target` | `string` | — | CSS selector for multi-target tooltips within the container |
| `tipPointerPosition` | `TipPointerPosition` | `'Auto'` | Tip arrow position: `Auto` \| `Start` \| `Middle` \| `End` |
| `width` | `string \| number` | `'auto'` | Tooltip width; `'auto'` fits content within viewport |
| `windowCollision` | `boolean` | `false` | Use viewport (window) as collision boundary when `target` is set |

---

## Methods

### `open(element?, animation?)`

Shows the tooltip on a specified target element with optional animation settings.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `element` | `HTMLElement` | Optional | Target element to display tooltip on |
| `animation` | `TooltipAnimationSettings` | Optional | Animation override for this open call |

Returns: `void`

```tsx
tooltipRef.open(targetElement);
tooltipRef.open(targetElement, { effect: 'ZoomIn', duration: 500 });
```

---

### `close(animation?)`

Hides the tooltip with optional animation settings.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `animation` | `TooltipAnimationSettings` | Optional | Animation override for this close call |

Returns: `void`

```tsx
tooltipRef.close();
tooltipRef.close({ effect: 'FadeOut', duration: 300 });
```

---

### `refresh(target?)`

Recalculates and updates the tooltip's content and/or position.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `target` | `HTMLElement` | Optional | Element to refresh position/content for |

Returns: `void`

```tsx
tooltipRef.refresh();
tooltipRef.refresh(targetElement);
```

> Use after programmatically changing `position` or when the target element moves.

---

### `destroy()`

Destroys the tooltip component instance and cleans up event listeners.

Returns: `void`

```tsx
tooltipRef.destroy();
```

> Use with `render()` to toggle tooltip behavior at runtime.

---

### `dataBind()`

Applies all pending property changes to the component immediately.

Returns: `void`

```tsx
tooltipRef.content = 'New content';
tooltipRef.dataBind(); // apply changes immediately
```

> Required after programmatically setting `content` or `animation` between renders.

---

### `render()`

Re-initializes the component after `destroy()` has been called.

Returns: `void`

```tsx
tooltipRef.render();
```

---

## Events

| Event | Type | Description |
|-------|------|-------------|
| `beforeRender` | `EmitType<TooltipEventArgs>` | Fires before tooltip and content are added to DOM. Set `cancel: true` to prevent rendering. Use for dynamic content loading. |
| `beforeOpen` | `EmitType<TooltipEventArgs>` | Fires before tooltip is displayed. Set `cancel: true` to prevent opening. Use for dynamic positioning or style changes. |
| `afterOpen` | `EmitType<TooltipEventArgs>` | Fires after tooltip is fully shown. |
| `beforeClose` | `EmitType<TooltipEventArgs>` | Fires before tooltip hides. Set `cancel: true` to keep it open. |
| `afterClose` | `EmitType<TooltipEventArgs>` | Fires after tooltip is fully closed. |
| `beforeCollision` | `EmitType<TooltipEventArgs>` | Fires on each collision fit calculation. |
| `created` | `EmitType<Object>` | Fires after the component is created. |
| `destroyed` | `EmitType<Object>` | Fires when the component is destroyed. |

**Usage example:**
```tsx
function onBeforeRender(args: TooltipEventArgs): void {
  // args.cancel = true; // prevent rendering
  // args.element — the tooltip DOM element (available from beforeOpen onward)
  // args.target — the target element that triggered the tooltip
}

<TooltipComponent
  beforeRender={onBeforeRender}
  beforeOpen={(args) => { /* dynamic styles */ }}
  afterOpen={(args) => { /* post-open logic */ }}
  beforeClose={(args) => { /* args.cancel = true to prevent close */ }}
  afterClose={(args) => { /* cleanup */ }}
  content="..."
>
  <button className="e-btn">Hover</button>
</TooltipComponent>
```

---

## Type Definitions

### AnimationModel

```typescript
interface AnimationModel {
  open?: TooltipAnimationSettings;
  close?: TooltipAnimationSettings;
}
```

### TooltipAnimationSettings

```typescript
interface TooltipAnimationSettings {
  effect?: Effect;    // animation effect name (see Animation Effects below)
  duration?: number;  // animation duration in milliseconds
  delay?: number;     // delay before animation starts (ms)
}
```

### TooltipEventArgs

```typescript
interface TooltipEventArgs {
  cancel: boolean;       // set to true to cancel the action
  element: HTMLElement;  // the tooltip popup DOM element
  target: HTMLElement;   // the element that triggered the tooltip
  event: Event;          // the original DOM event
  name: string;          // event name
}
```

---

## Position Values

Valid values for the `position` property:

```
TopLeft | TopCenter | TopRight
BottomLeft | BottomCenter | BottomRight
LeftTop | LeftCenter | LeftBottom
RightTop | RightCenter | RightBottom
```

Default: `TopCenter`

---

## TipPointerPosition Values

Valid values for the `tipPointerPosition` property:

| Value | Description |
|-------|-------------|
| `Auto` | Auto-adjusts within target length, never points outside (default) |
| `Start` | Pin arrow to start of tooltip edge |
| `Middle` | Pin arrow to middle of tooltip edge |
| `End` | Pin arrow to end of tooltip edge |

---

## Animation Effects

Valid values for `TooltipAnimationSettings.effect`:

| Effect | Type |
|--------|------|
| `FadeIn` / `FadeOut` | Opacity fade |
| `FadeZoomIn` / `FadeZoomOut` | Fade + scale |
| `FlipXDownIn` / `FlipXDownOut` | X-axis flip downward |
| `FlipXUpIn` / `FlipXUpOut` | X-axis flip upward |
| `FlipYLeftIn` / `FlipYLeftOut` | Y-axis flip leftward |
| `FlipYRightIn` / `FlipYRightOut` | Y-axis flip rightward |
| `ZoomIn` / `ZoomOut` | Scale zoom |
| `None` | No animation |

---

## Import Reference

```tsx
import {
  TooltipComponent,
  TooltipEventArgs,
  TooltipAnimationSettings
} from '@syncfusion/ej2-react-popups';

// For Fetch-based dynamic content:
import { Fetch } from '@syncfusion/ej2-base';

// For legacy Ajax:
import { Ajax } from '@syncfusion/ej2-base';

// For draggable positioning:
import { Draggable } from '@syncfusion/ej2-base';
```
