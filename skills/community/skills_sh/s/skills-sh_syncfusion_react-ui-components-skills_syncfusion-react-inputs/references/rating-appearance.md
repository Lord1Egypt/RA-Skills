# Appearance and Customization in React Rating Component

## Table of Contents
- [Items Count](#items-count)
- [Disabled State](#disabled-state)
- [Visible / Hidden](#visible--hidden)
- [Read-Only Mode](#read-only-mode)
- [CSS Customization with cssClass](#css-customization-with-cssclass)
  - [Changing Border Color](#changing-border-color)
  - [Changing Fill Colors](#changing-fill-colors)
  - [Changing Item Spacing](#changing-item-spacing)
  - [Changing the Rating Icon](#changing-the-rating-icon)
- [Animation](#animation)

---

## Items Count

Control the number of rating symbols with `itemsCount`. Default is `5`.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" itemsCount={8} value={3} />
    </div>
  );
}
export default App;
```

---

## Disabled State

Set `disabled={true}` to prevent user interaction. The component shows a dimmed visual appearance.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} disabled={true} />
    </div>
  );
}
export default App;
```

- Disabled is different from read-only: disabled components are visually dimmed and not focusable.

---

## Visible / Hidden

Use `visible` to show or hide the rating component. Default is `true`.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  const ratingRef = React.useRef<RatingComponent>(null);

  const toggleVisible = () => {
    if (ratingRef.current) {
      ratingRef.current.visible = !ratingRef.current.visible;
    }
  };

  return (
    <div className="wrap">
      <button onClick={toggleVisible}>Toggle Visible</button>
      <RatingComponent id="rating" value={3} visible={true} ref={ratingRef} />
    </div>
  );
}
export default App;
```

---

## Read-Only Mode

Use `readOnly={true}` to display the rating without allowing changes. The component is still visible and focusable but non-interactive.

```tsx
import { RatingComponent } from '@syncfusion/ej2-react-inputs';
import * as React from 'react';

function App() {
  return (
    <div className="wrap">
      <RatingComponent id="rating" value={3} readOnly={true} />
    </div>
  );
}
export default App;
```

- Use `readOnly` for **display-only** rating (e.g., showing an average score).
- Use `disabled` when the rating field is conditionally unavailable.

---

## CSS Customization with cssClass

Pass a custom CSS class via `cssClass` and override the relevant CSS variables or properties.

### Changing Border Color

Change the icon outline/stroke color using `.e-rating-icon` with `text-stroke` (or `-webkit-text-stroke`):

```tsx
<RatingComponent id="rating" value={3} cssClass="custom-border" />
```

```css
.custom-border .e-rating-icon {
  -webkit-text-stroke: 2px #ff0000;
}
```

---

### Changing Fill Colors

Customize rated (filled) and unrated (empty) fill colors using `linear-gradient` on `.e-rating-icon`. The first color-stop is the rated color, the second is the unrated color. `--rating-value` provides the current item's value for partial fill support.

```tsx
<RatingComponent id="rating" value={3} cssClass="custom-fill" />
```

```css
.custom-fill .e-rating-icon {
  background: linear-gradient(
    to right,
    #ffe814 calc(var(--rating-value) * 100%),
    #d8d7d4 calc(var(--rating-value) * 100%)
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

### Changing Item Spacing

Adjust spacing between rating items by targeting `.e-rating-item-container`:

```tsx
<RatingComponent id="rating" value={3} cssClass="custom-spacing" />
```

```css
.custom-spacing .e-rating-item-container {
  margin: 0 8px;
}
```

---

### Changing the Rating Icon

Replace the default star with any font icon by overriding `.e-icons.e-star-filled:before`:

```tsx
<RatingComponent id="rating" value={3} cssClass="custom-icon" />
```

```css
.custom-icon .e-icons.e-star-filled:before {
  content: '\e700'; /* Replace with your font icon code */
  font-family: 'YourIconFont';
}
```

---

## Animation

The `enableAnimation` property controls whether items animate on hover. Default is `true`.

```tsx
{/* Disable hover animation */}
<RatingComponent id="rating" value={3} enableAnimation={false} />
```

- Disable animation when using custom emoji or SVG templates to avoid visual conflicts.
