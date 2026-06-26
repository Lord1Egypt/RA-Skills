# API Reference — Syncfusion React DropDownButton

Source: https://ej2.syncfusion.com/react/documentation/api/drop-down-button/index-default

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Events](#events)
- [Methods](#methods)
- [Type Definitions](#type-definitions)

---

## Import

```tsx
import {
  DropDownButtonComponent,
  ItemModel,
  MenuEventArgs,
  OpenCloseMenuEventArgs,
  BeforeOpenCloseMenuEventArgs,
} from '@syncfusion/ej2-react-splitbuttons';
```

---

## Properties

### animationSettings `DropDownMenuAnimationSettingsModel`

Specifies the animation settings for opening the popup. Controls `effect`, `duration`, and `easing`.

- **Default:** `{ effect: 'None' }`
- **Supported effects:** `'None'` | `'SlideDown'` | `'ZoomIn'` | `'FadeIn'`

```tsx
<DropDownButtonComponent
  items={items}
  animationSettings={{ effect: 'SlideDown', duration: 800, easing: 'ease' }}
>
  Slide Down
</DropDownButtonComponent>
```

---

### closeActionEvents `string`

Specifies the DOM event name(s) that close the DropDownButton popup.

- **Default:** `""`

---

### content `string`

Defines the HTML or text content rendered inside the button element. Equivalent to placing text as children.

- **Default:** `""`

```tsx
<DropDownButtonComponent items={items} content="Clipboard" />
```

---

### createPopupOnClick `boolean`

When `true`, the popup element is created only on the first open. Use this for performance optimization with large item lists.

- **Default:** `false`

---

### cssClass `string`

One or more space-separated CSS class names applied to the button element. Use to apply color styles, size variants, layout, or custom classes.

- **Default:** `""`
- **Common values:** `"e-primary"` `"e-success"` `"e-info"` `"e-warning"` `"e-danger"` `"e-outline"` `"e-flat"` `"e-small"` `"e-large"` `"e-vertical"` `"e-caret-hide"` `"e-caret-up"` `"e-round-corner"`

```tsx
<DropDownButtonComponent items={items} cssClass="e-primary e-small">
  Action
</DropDownButtonComponent>
```

---

### disabled `boolean`

Disables the button. A disabled button is non-interactive, cannot receive focus, and sets `aria-disabled="true"`.

- **Default:** `false`

```tsx
<DropDownButtonComponent items={items} disabled={true}>
  Disabled
</DropDownButtonComponent>
```

---

### enableHtmlSanitizer `boolean`

When `true`, sanitizes untrusted HTML before rendering it inside the component.

- **Default:** `true`

---

### enablePersistence `boolean`

When `true`, persists the component state (e.g., open/close) across page reloads using browser local storage.

- **Default:** `false`

---

### enableRtl `boolean`

Renders the component in right-to-left (RTL) direction. Use for Arabic, Hebrew, and other RTL locales.

- **Default:** `false`

```tsx
<DropDownButtonComponent items={items} enableRtl={true}>
  Message
</DropDownButtonComponent>
```

---

### iconCss `string`

CSS class(es) for the button icon. Supports Syncfusion built-in icons (`e-icons`), Font Awesome, or any font-icon class.

- **Default:** `""`

```tsx
<DropDownButtonComponent items={items} iconCss="ddb-icons e-message">
  Message
</DropDownButtonComponent>
```

---

### iconPosition `SplitButtonIconPosition`

Positions the icon relative to the button text.

- **Default:** `"Left"`
- **Values:** `"Left"` | `"Top"`

```tsx
<DropDownButtonComponent items={items} iconCss="e-icons e-home" iconPosition="Top">
  Home
</DropDownButtonComponent>
```

---

### itemTemplate `string | Function`

A template function (or HTML string) used to render each popup item. The function receives an object with a `properties` field exposing the `ItemModel` data.

- **Default:** `null`

```tsx
function itemTemplate(data: any) {
  return (
    <div>
      <span className={`e-menu-icon ${data.properties.iconCss}`} />
      <span>{data.properties.text}</span>
    </div>
  );
}

<DropDownButtonComponent items={items} itemTemplate={itemTemplate}>
  Actions
</DropDownButtonComponent>
```

---

### items `ItemModel[]`

Array of action items rendered inside the popup. Each item is an `ItemModel` object.

- **Default:** `[]`

```tsx
const items: ItemModel[] = [
  { text: 'Cut' },
  { text: 'Copy', iconCss: 'e-icons e-copy' },
  { separator: true },
  { text: 'Paste', disabled: true },
];
```

**ItemModel fields:**

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Item label |
| `iconCss` | `string` | Icon CSS class(es) |
| `url` | `string` | Navigation URL |
| `separator` | `boolean` | Renders a horizontal divider |
| `disabled` | `boolean` | Disables the item |
| `id` | `string` | Unique identifier |

---

### locale `string`

Overrides the global culture and localization for this instance.

- **Default:** `''` (uses global `'en-US'`)

---

### popupWidth `string | number`

Sets the width of the popup. Accepts CSS units (`"200px"`, `"50%"`) or a number (treated as pixels).

- **Default:** `"auto"`

```tsx
<DropDownButtonComponent items={items} popupWidth="300px">
  Wide Popup
</DropDownButtonComponent>
```

---

### target `string | Element`

Specifies a custom element (by CSS selector or DOM reference) to use as the popup content. When set, the `items` property is ignored.

- **Default:** `""`

```tsx
<div id="customPopup">
  {/* Custom popup content */}
</div>

<DropDownButtonComponent target="#customPopup" cssClass="e-caret-hide" />
```

---

## Events

### beforeClose `EmitType<BeforeOpenCloseMenuEventArgs>`

Fires before the popup closes. Cancel closing by setting `args.cancel = true`.

```tsx
function beforeClose(args: BeforeOpenCloseMenuEventArgs) {
  // args.cancel = true; // Prevent close
}
<DropDownButtonComponent items={items} beforeClose={beforeClose}>Actions</DropDownButtonComponent>
```

---

### beforeItemRender `EmitType<MenuEventArgs>`

Fires during rendering of each popup item. Mutate `args.element` to customize item HTML.

```tsx
function beforeItemRender(args: MenuEventArgs) {
  if (args.item.text === 'Copy') {
    args.element.innerHTML = '<u>C</u>opy';
  }
}
<DropDownButtonComponent items={items} beforeItemRender={beforeItemRender}>Clipboard</DropDownButtonComponent>
```

---

### beforeOpen `EmitType<BeforeOpenCloseMenuEventArgs>`

Fires before the popup opens. Cancel opening by setting `args.cancel = true`.

```tsx
function beforeOpen(args: BeforeOpenCloseMenuEventArgs) {
  console.log('About to open');
}
<DropDownButtonComponent items={items} beforeOpen={beforeOpen}>Actions</DropDownButtonComponent>
```

---

### close `EmitType<OpenCloseMenuEventArgs>`

Fires after the popup closes.

```tsx
function onClose(args: OpenCloseMenuEventArgs) {
  console.log('Popup closed');
}
<DropDownButtonComponent items={items} close={onClose}>Actions</DropDownButtonComponent>
```

---

### created `EmitType<Event>`

Fires once after the component finishes rendering.

```tsx
function onCreated() {
  console.log('DropDownButton ready');
}
<DropDownButtonComponent items={items} created={onCreated}>Actions</DropDownButtonComponent>
```

---

### open `EmitType<OpenCloseMenuEventArgs>`

Fires after the popup opens. Use `args.element.parentElement` to access the popup wrapper for positioning.

```tsx
function onOpen(args: OpenCloseMenuEventArgs) {
  const popup = args.element.parentElement as HTMLElement;
  popup.style.top = '50px';
}
<DropDownButtonComponent items={items} open={onOpen}>Actions</DropDownButtonComponent>
```

---

### select `EmitType<MenuEventArgs>`

Fires when the user selects a popup item. `args.item` contains the selected `ItemModel`.

```tsx
function onSelect(args: MenuEventArgs) {
  console.log('Selected:', args.item.text);
}
<DropDownButtonComponent items={items} select={onSelect}>Actions</DropDownButtonComponent>
```

---

## Methods

Access methods via a component `ref`:

```tsx
let ddb: DropDownButtonComponent;
<DropDownButtonComponent ref={(scope) => { ddb = scope as DropDownButtonComponent; }} items={items}>
  Actions
</DropDownButtonComponent>
```

### addItems(items: ItemModel[], text?: string): void

Appends new items to the popup. If `text` is provided, inserts before the item matching that text.

```tsx
ddb.addItems([{ text: 'Select All' }]);          // Append
ddb.addItems([{ text: 'Undo' }], 'Copy');        // Insert before 'Copy'
```

---

### destroy(): void

Destroys the component instance and cleans up DOM and event listeners.

```tsx
ddb.destroy();
```

---

### focusIn(): void

Sets focus to the DropDownButton element programmatically.

```tsx
ddb.focusIn();
```

---

### getPersistData(): string

Returns a JSON string of the properties that are persisted across page reloads (when `enablePersistence` is `true`).

```tsx
const state = ddb.getPersistData();
```

---

### removeItems(items: string[], isUniqueId?: boolean): void

Removes items from the popup by text. Set `isUniqueId = true` to remove by `id` instead of `text`.

```tsx
ddb.removeItems(['Paste']);                      // Remove by text
ddb.removeItems(['item-3'], true);               // Remove by id
```

---

### toggle(): void

Opens the popup if closed; closes it if open.

```tsx
ddb.toggle();
```

---

## Type Definitions

### ItemModel

```ts
interface ItemModel {
  text?: string;
  iconCss?: string;
  url?: string;
  separator?: boolean;
  disabled?: boolean;
  id?: string;
}
```

### MenuEventArgs

```ts
interface MenuEventArgs {
  item: ItemModel;       // The item that triggered the event
  element: HTMLElement;  // The DOM element of the item
  event: Event;          // The original DOM event
}
```

### OpenCloseMenuEventArgs

```ts
interface OpenCloseMenuEventArgs {
  element: HTMLElement;  // The popup list element
  event: Event;          // The original DOM event
}
```

### BeforeOpenCloseMenuEventArgs

```ts
interface BeforeOpenCloseMenuEventArgs {
  element: HTMLElement;  // The popup list element
  event: Event;          // The original DOM event
  cancel: boolean;       // Set to true to cancel the open/close action
}
```
