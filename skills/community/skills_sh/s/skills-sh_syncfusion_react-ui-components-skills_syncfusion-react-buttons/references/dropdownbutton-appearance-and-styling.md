# Appearance and Styling — Syncfusion React DropDownButton

## Table of Contents
- [CSS Class Reference](#css-class-reference)
- [Color Styles](#color-styles)
- [Size Variants](#size-variants)
- [Rounded Corners](#rounded-corners)
- [Hide Dropdown Arrow](#hide-dropdown-arrow)
- [Popup Width](#popup-width)
- [Animation Settings](#animation-settings)
- [Theme Studio](#theme-studio)

---

## CSS Class Reference

Override default styles by targeting these CSS classes:

| CSS Class | Purpose |
|-----------|---------|
| `.e-dropdown-btn` | Container for the DropDownButton component |
| `.e-dropdown-btn.e-primary` | Primary color styling |
| `.e-dropdown-btn.e-success` | Success (green) color styling |
| `.e-dropdown-btn.e-info` | Info (blue) color styling |
| `.e-dropdown-btn.e-warning` | Warning (orange) color styling |
| `.e-dropdown-btn.e-danger` | Danger (red) color styling |
| `.e-dropdown-btn.e-outline` | Outline (bordered, transparent fill) styling |
| `.e-dropdown-btn.e-flat` | Flat (no border/shadow) styling |
| `.e-dropdown-btn:hover` | Hover state |
| `.e-dropdown-btn.e-active` | Active / pressed state |
| `.e-dropdown-btn:disabled` | Disabled state |
| `.e-dropdown-btn.e-small` | Small size |
| `.e-dropdown-btn.e-large` | Large size |
| `.e-dropdown-popup` | Popup container |
| `.e-dropdown-popup .e-item` | Individual popup item |
| `.e-dropdown-popup .e-item:hover` | Popup item hover state |
| `.e-dropdown-popup .e-item.e-selected` | Selected popup item |
| `.e-dropdown-popup .e-item.e-disabled` | Disabled popup item |
| `.e-dropdown-popup .e-separator` | Separator between items |
| `.e-dropdown-popup .e-icons` | Icons inside popup items |

---

## Color Styles

Apply predefined color styles using `cssClass`:

```tsx
{/* Primary */}
<DropDownButtonComponent items={items} cssClass="e-primary">Primary</DropDownButtonComponent>

{/* Success */}
<DropDownButtonComponent items={items} cssClass="e-success">Success</DropDownButtonComponent>

{/* Danger */}
<DropDownButtonComponent items={items} cssClass="e-danger">Danger</DropDownButtonComponent>

{/* Outline */}
<DropDownButtonComponent items={items} cssClass="e-outline">Outline</DropDownButtonComponent>

{/* Flat */}
<DropDownButtonComponent items={items} cssClass="e-flat">Flat</DropDownButtonComponent>
```

Multiple classes can be combined (space-separated):

```tsx
<DropDownButtonComponent items={items} cssClass="e-primary e-small">
  Small Primary
</DropDownButtonComponent>
```

---

## Size Variants

| Class | Effect |
|-------|--------|
| `e-small` | Compact height and font |
| `e-large` | Larger height and font |
| *(default)* | Normal size |

```tsx
<DropDownButtonComponent items={items} cssClass="e-small">Small</DropDownButtonComponent>
<DropDownButtonComponent items={items}>Normal</DropDownButtonComponent>
<DropDownButtonComponent items={items} cssClass="e-large">Large</DropDownButtonComponent>
```

---

## Rounded Corners

Add `e-round-corner` via `cssClass` to apply a 5px border-radius:

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' },
  ];

  return (
    <DropDownButtonComponent items={items} cssClass="e-round-corner">
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Hide Dropdown Arrow

Remove the caret icon by adding `e-caret-hide` via `cssClass`. Useful for icon-only buttons or custom-styled triggers.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' }, { text: 'Copy' }, { text: 'Paste' },
  ];

  return (
    <DropDownButtonComponent items={items} cssClass="e-caret-hide">
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Popup Width

Control the popup's width using the `popupWidth` property. Accepts CSS units (`"200px"`, `"50%"`) or a raw number (interpreted as pixels). Defaults to `"auto"`.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Selection', iconCss: 'e-icons e-list-unordered' },
    { text: 'Yes / No',  iconCss: 'e-icons e-check-box' },
    { text: 'Text',      iconCss: 'e-icons e-caption' },
    { text: 'None',      iconCss: 'e-icons e-mouse-pointer' },
  ];

  return (
    <DropDownButtonComponent items={items} popupWidth="200px">
      DropDownButton
    </DropDownButtonComponent>
  );
}

export default App;
```

---

## Animation Settings

Customize the popup open animation using the `animationSettings` property. It accepts `effect`, `duration`, and `easing`.

**Supported effects:**

| Effect | Description |
|--------|-------------|
| `None` | No animation — popup appears instantly (default) |
| `SlideDown` | Popup slides downward when opening |
| `ZoomIn` | Popup scales in from the center |
| `FadeIn` | Popup fades in gradually |

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Unread' },
    { text: 'Has Attachments' },
    { text: 'Categorized' },
    { separator: true },
    { text: 'Important' },
    { text: 'More Filters' },
  ];

  return (
    <div>
      <DropDownButtonComponent
        items={items}
        animationSettings={{ effect: 'SlideDown', duration: 800, easing: 'ease' }}
      >
        Slide Down
      </DropDownButtonComponent>

      <DropDownButtonComponent
        items={items}
        animationSettings={{ effect: 'FadeIn', duration: 800, easing: 'ease' }}
      >
        Fade In
      </DropDownButtonComponent>

      <DropDownButtonComponent
        items={items}
        animationSettings={{ effect: 'ZoomIn', duration: 800, easing: 'ease' }}
      >
        Zoom In
      </DropDownButtonComponent>
    </div>
  );
}

export default App;
```

---

## Theme Studio

For brand-specific themes, use the [Syncfusion Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material) to generate a custom CSS file, then replace the default theme imports with the generated file.
