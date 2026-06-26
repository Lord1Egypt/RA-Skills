# Events in React Rating Component

## Table of Contents
- [beforeItemRender](#beforeitemrender)
- [created](#created)
- [onItemHover](#onitemhover)
- [valueChanged](#valuechanged)
- [Event Arguments Reference](#event-arguments-reference)

---

## beforeItemRender

Fires before each rating item is rendered. Use it to customize or inspect items before they appear.

```tsx
import { RatingComponent, RatingItemEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function beforeItemRender(args: RatingItemEventArgs) {
    // args.element — the item DOM element
    // args.value   — the value of this item
    // args.index   — the zero-based index of this item
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" beforeItemRender={beforeItemRender} />
    </div>
  );
}
export default App;
```

- Called once per item during initial render and on re-render.
- Useful for conditionally applying classes or attributes to specific items.

---

## created

Fires after the rating component has fully rendered.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function created() {
    console.log('Rating component is ready');
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" created={created} />
    </div>
  );
}
export default App;
```

- Use for post-render initialization logic.
- The event receives a standard DOM `Event` object.

---

## onItemHover

Fires when the user hovers over a rating item. Provides the hovered item's details.

```tsx
import { RatingComponent, RatingHoverEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const [hovered, setHovered] = React.useState<number | null>(null);

  function onItemHover(args: RatingHoverEventArgs) {
    setHovered(args.value);
    // args.value   — the value of the hovered item
    // args.element — the hovered item DOM element
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" onItemHover={onItemHover} />
      {hovered !== null && <p>Hovering over: {hovered}</p>}
    </div>
  );
}
export default App;
```

- Useful for live previews: show a label or description as the user moves their cursor.

---

## valueChanged

Fires when the user selects a new rating value. Provides both the previous and new values.

```tsx
import { RatingComponent, RatingChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  function valueChanged(args: RatingChangedEventArgs) {
    console.log('Previous:', args.previousValue);
    console.log('New value:', args.value);
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" valueChanged={valueChanged} />
    </div>
  );
}
export default App;
```

**Practical example — display previous and new values:**

```tsx
import { RatingComponent, RatingChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const [info, setInfo] = React.useState('');

  function valueChanged(args: RatingChangedEventArgs) {
    setInfo(`Changed from ${args.previousValue} to ${args.value}`);
  }

  return (
    <div className="wrap">
      <RatingComponent id="rating" valueChanged={valueChanged} />
      <p>{info}</p>
    </div>
  );
}
export default App;
```

---

## Event Arguments Reference

### RatingItemEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | The rating item DOM element |
| `value` | `number` | The value of the item |
| `index` | `number` | Zero-based item index |

### RatingHoverEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `element` | `HTMLElement` | The hovered item DOM element |
| `value` | `number` | The value of the hovered item |

### RatingChangedEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `value` | `number` | The newly selected rating value |
| `previousValue` | `number` | The previously selected rating value |

---

## Event Import Reference

```tsx
import {
  RatingComponent,
  RatingItemEventArgs,
  RatingHoverEventArgs,
  RatingChangedEventArgs,
} from '@syncfusion/ej2-react-inputs';
```
