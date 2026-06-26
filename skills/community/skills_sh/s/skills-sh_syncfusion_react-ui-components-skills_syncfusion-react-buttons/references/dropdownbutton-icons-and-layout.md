# Icons and Layout — Syncfusion React DropDownButton

## Table of Contents
- [Button Icon with iconCss](#button-icon-with-iconcss)
- [Icon Position](#icon-position)
- [Icon-Only Button](#icon-only-button)
- [Sprite Image Icon](#sprite-image-icon)
- [Vertical Button Layout](#vertical-button-layout)
- [Customize Icon Size and Button Width](#customize-icon-size-and-button-width)

---

## Button Icon with iconCss

Use the `iconCss` property to render an icon inside the DropDownButton. Set it to one or more CSS class names that define the icon. The `e-icons` class provides Syncfusion's built-in icon set.

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Edit' },
    { text: 'Delete' },
    { text: 'Mark as Read' },
    { text: 'Like Message' },
  ];

  return (
    <DropDownButtonComponent items={items} iconCss="ddb-icons e-message">
      Message
    </DropDownButtonComponent>
  );
}

export default App;
```

> Third-party icon libraries (Font Awesome, Bootstrap Icons, etc.) work the same way — pass the relevant class names to `iconCss`.

---

## Icon Position

Control where the icon appears relative to the button text using `iconPosition`. Accepted values: `"Left"` (default) | `"Top"`.

```tsx
function App() {
  const items: ItemModel[] = [
    { text: 'Edit' }, { text: 'Delete' },
    { text: 'Mark as Read' }, { text: 'Like Message' },
  ];

  return (
    <div>
      {/* Icon on the left (default) */}
      <DropDownButtonComponent items={items} iconCss="ddb-icons e-message">
        Message
      </DropDownButtonComponent>

      {/* Icon on top */}
      <DropDownButtonComponent items={items} iconCss="ddb-icons e-message" iconPosition="Top">
        Message
      </DropDownButtonComponent>
    </div>
  );
}
```

---

## Icon-Only Button

Create an icon-only button (no text, no caret) by:
1. Setting `iconCss` (required for the icon).
2. Adding `e-caret-hide` via `cssClass` to hide the dropdown arrow.
3. Omitting button text (leave children empty).

```tsx
function App() {
  const items: ItemModel[] = [
    { text: 'New tab' },
    { text: 'New window' },
    { text: 'New incognito window' },
    { separator: true },
    { text: 'Print' },
    { text: 'Cast' },
    { text: 'Find' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="e-icons e-menu"
      cssClass="e-caret-hide"
    />
  );
}
```

---

## Sprite Image Icon

Use sprite images as button icons by specifying a custom CSS class in `iconCss`. Define the `width`, `height`, and `background-position` in your stylesheet to display the correct sprite frame.

```tsx
function App() {
  const items: ItemModel[] = [
    { text: 'Display Settings' },
    { text: 'System Settings' },
    { text: 'Additional Settings' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="e-icons e-image"
      cssClass="e-caret-hide"
    />
  );
}
```

**Typical CSS for a 32×32 sprite frame:**

```css
.e-image {
  width: 32px;
  height: 32px;
  background-image: url('sprite.png');
  background-position: -64px 0;
}
```

---

## Vertical Button Layout

Add the `e-vertical` class via `cssClass` together with `iconPosition="Top"` to stack the icon above the button text.

```tsx
function App() {
  const items: ItemModel[] = [
    { text: 'Edit' }, { text: 'Delete' },
    { text: 'Mark as Read' }, { text: 'Like Message' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="ddb-icons e-message"
      cssClass="e-vertical"
      iconPosition="Top"
    >
      Message
    </DropDownButtonComponent>
  );
}
```

---

## Customize Icon Size and Button Width

Apply a custom CSS class via `cssClass` to control button width and icon dimensions. Combine with `iconPosition="Top"` for a toolbar-style button.

```tsx
function App() {
  const items: ItemModel[] = [
    { text: 'Find' }, { text: 'Replace' },
    { text: 'Go To' }, { text: 'Go To Special' },
  ];

  return (
    <DropDownButtonComponent
      items={items}
      iconCss="e-icons e-search"
      cssClass="e-custom e-vertical"
      iconPosition="Top"
    >
      Find & Select
    </DropDownButtonComponent>
  );
}
```

**CSS to set button width to 85px and icon size to 40px:**

```css
.e-custom {
  width: 85px;
}

.e-custom .e-btn-icon {
  font-size: 40px;
}
```
