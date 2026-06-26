# API Reference — Syncfusion React Rating Component

**Source:** https://ej2.syncfusion.com/react/documentation/api/rating/index-default

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Enums](#enums)
- [Event Argument Interfaces](#event-argument-interfaces)

---

## Import

```tsx
import {
  RatingComponent,
  PrecisionType,
  LabelPosition,
  RatingItemEventArgs,
  RatingHoverEventArgs,
  RatingChangedEventArgs,
} from '@syncfusion/ej2-react-inputs';
```

---

## Properties

### allowReset
**Type:** `boolean` | **Default:** `false`

Shows or hides the reset button. When `true`, the user can click the reset button to restore the rating to its minimum value.

```tsx
<RatingComponent id="rating" allowReset={true} value={3} />
```

---

### cssClass
**Type:** `string` | **Default:** `''`

One or more CSS classes to customize the component's appearance (colors, fonts, sizes, icon shapes, etc.).

```tsx
<RatingComponent id="rating" value={3} cssClass="my-custom-rating" />
```

---

### disabled
**Type:** `boolean` | **Default:** `false`

Disables the component. When `true`, the user cannot interact with the rating, and the component may appear dimmed.

```tsx
<RatingComponent id="rating" value={3} disabled={true} />
```

---

### emptyTemplate
**Type:** `string | function | JSX.Element` | **Default:** `''`

Template for the appearance of each **unrated** item. If `fullTemplate` is not defined, this template is used for both rated and unrated items.

```tsx
function emptyTemplate() {
  return <span className="custom-icon"></span>;
}
<RatingComponent id="rating" value={3} emptyTemplate={emptyTemplate} />
```

---

### enableAnimation
**Type:** `boolean` | **Default:** `true`

When `true`, a hover animation is shown when the user moves their cursor over rating items.

```tsx
<RatingComponent id="rating" value={3} enableAnimation={false} />
```

---

### enablePersistence
**Type:** `boolean` | **Default:** `false`

When `true`, the component's state (current value) is persisted across page reloads via browser local storage.

```tsx
<RatingComponent id="rating" value={3} enablePersistence={true} />
```

---

### enableRtl
**Type:** `boolean` | **Default:** `false`

Renders the component in right-to-left direction. Arrow Left increases the value, Arrow Right decreases it.

```tsx
<RatingComponent id="rating" value={3} enableRtl={true} />
```

---

### enableSingleSelection
**Type:** `boolean` | **Default:** `false`

When `true`, only the clicked item is highlighted. When `false` (default), all items from the first to the selected item are highlighted.

```tsx
<RatingComponent id="rating" value={3} enableSingleSelection={true} />
```

---

### fullTemplate
**Type:** `string | function | JSX.Element` | **Default:** `''`

Template for the appearance of each **rated** item.

```tsx
function fullTemplate() {
  return <span className="filled-icon"></span>;
}
<RatingComponent id="rating" value={3} fullTemplate={fullTemplate} />
```

---

### itemsCount
**Type:** `number` | **Default:** `5`

The number of rating items (symbols) to display.

```tsx
<RatingComponent id="rating" itemsCount={10} value={7} />
```

---

### labelPosition
**Type:** `string | LabelPosition` | **Default:** `LabelPosition.Right`

Position of the value label relative to the rating. Requires `showLabel={true}`.

**Possible values:** `'Top'`, `'Bottom'`, `'Left'`, `'Right'`

```tsx
<RatingComponent id="rating" value={3} showLabel={true} labelPosition="Top" />
// or
<RatingComponent id="rating" value={3} showLabel={true} labelPosition={LabelPosition.Top} />
```

---

### labelTemplate
**Type:** `string | function | JSX.Element` | **Default:** `''`

Custom template for the label. The current `value` is available in the template context.

```tsx
<RatingComponent
  id="rating"
  value={3}
  showLabel={true}
  labelTemplate="<span>${value} out of 5</span>"
/>
```

---

### locale
**Type:** `string` | **Default:** `''`

Overrides the global culture/localization. Default is `'en-US'`.

```tsx
<RatingComponent id="rating" value={3} locale="fr-FR" />
```

---

### min
**Type:** `number` | **Default:** `0.0`

The minimum selectable rating value. Users cannot select a value below this.

```tsx
<RatingComponent id="rating" min={1} />
```

---

### precision
**Type:** `string | PrecisionType` | **Default:** `PrecisionType.Full`

Controls the granularity of the rating value.

**Possible values:** `'Full'`, `'Half'`, `'Quarter'`, `'Exact'`

```tsx
<RatingComponent id="rating" value={2.5} precision={PrecisionType.Half} />
// or
<RatingComponent id="rating" value={2.5} precision="Half" />
```

---

### readOnly
**Type:** `boolean` | **Default:** `false`

When `true`, the component is non-interactive (user cannot change the value) but remains visible and focusable.

```tsx
<RatingComponent id="rating" value={4} readOnly={true} />
```

---

### showLabel
**Type:** `boolean` | **Default:** `false`

When `true`, displays a label showing the current rating value.

```tsx
<RatingComponent id="rating" value={3} showLabel={true} />
```

---

### showTooltip
**Type:** `boolean` | **Default:** `true`

When `true`, shows a tooltip when the user hovers over a rating item.

```tsx
<RatingComponent id="rating" value={3} showTooltip={false} />
```

---

### tooltipTemplate
**Type:** `string | function | JSX.Element` | **Default:** `''`

Custom template for tooltip content. The current `value` is available in the template context.

```tsx
<RatingComponent
  id="rating"
  value={3}
  showTooltip={true}
  tooltipTemplate="<span>${value} Star</span>"
/>
```

---

### value
**Type:** `number` | **Default:** `0.0`

The current rating value. Ranges from `min` to `itemsCount`. Supports decimals based on `precision`.

```tsx
<RatingComponent id="rating" value={3.5} />
```

---

### visible
**Type:** `boolean` | **Default:** `true`

Controls component visibility. When `false`, the component is hidden.

```tsx
<RatingComponent id="rating" value={3} visible={true} />
```

---

## Methods

### destroy()
**Returns:** `void`

Destroys the Rating component instance and cleans up DOM elements and event listeners.

```tsx
const ratingRef = React.useRef<RatingComponent>(null);
ratingRef.current?.destroy();
```

---

### reset()
**Returns:** `void`

Resets the rating value to the `min` value.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const ratingRef = React.useRef<RatingComponent>(null);

  return (
    <div>
      <RatingComponent id="rating" min={1} value={3} ref={ratingRef} />
      <button onClick={() => ratingRef.current?.reset()}>Reset</button>
    </div>
  );
}
```

---

## Events

### beforeItemRender
**Type:** `EmitType<RatingItemEventArgs>`

Raised before rendering each rating item. Use to customize items at render time.

```tsx
<RatingComponent id="rating" beforeItemRender={(args: RatingItemEventArgs) => { /* ... */ }} />
```

---

### created
**Type:** `EmitType<Event>`

Raised after the rating component has fully rendered.

```tsx
<RatingComponent id="rating" created={() => console.log('Ready')} />
```

---

### onItemHover
**Type:** `EmitType<RatingHoverEventArgs>`

Raised when the user hovers over a rating item.

```tsx
<RatingComponent id="rating" onItemHover={(args: RatingHoverEventArgs) => console.log(args.value)} />
```

---

### valueChanged
**Type:** `EmitType<RatingChangedEventArgs>`

Raised when the selected rating value changes.

```tsx
<RatingComponent
  id="rating"
  valueChanged={(args: RatingChangedEventArgs) => {
    console.log('Previous:', args.previousValue, 'New:', args.value);
  }}
/>
```

---

## Enums

### PrecisionType

```tsx
import { PrecisionType } from '@syncfusion/ej2-react-inputs';
```

| Value | Increment | Description |
|-------|-----------|-------------|
| `PrecisionType.Full` | 1.0 | Whole number increments (default) |
| `PrecisionType.Half` | 0.5 | Half increments |
| `PrecisionType.Quarter` | 0.25 | Quarter increments |
| `PrecisionType.Exact` | 0.1 | Tenth increments |

---

### LabelPosition

```tsx
import { LabelPosition } from '@syncfusion/ej2-react-inputs';
```

| Value | Description |
|-------|-------------|
| `LabelPosition.Top` | Label above the rating |
| `LabelPosition.Bottom` | Label below the rating |
| `LabelPosition.Left` | Label to the left of the rating |
| `LabelPosition.Right` | Label to the right of the rating (default) |

---

## Event Argument Interfaces

### RatingItemEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | The rating item's DOM element |
| `value` | `number` | The value of the item |
| `index` | `number` | Zero-based index of the item |

### RatingHoverEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | The hovered item's DOM element |
| `value` | `number` | The value of the hovered item |

### RatingChangedEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number` | The newly selected rating value |
| `previousValue` | `number` | The previously selected rating value |
