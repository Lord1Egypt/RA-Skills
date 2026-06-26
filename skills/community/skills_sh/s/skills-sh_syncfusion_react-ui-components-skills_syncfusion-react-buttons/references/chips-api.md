# ChipListComponent API Reference

## Table of Contents
- [Import](#import)
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [ChipModel Interface](#chipmodel-interface)
- [Event Argument Types](#event-argument-types)

---

## Import

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
```

---

## Properties

### `text` — `string`
Specifies the text content for a single chip.

- **Default:** `''`
- **Use when:** Rendering a single `ChipListComponent` without `ChipsDirective`.

```tsx
<ChipListComponent text="Janet Leverling" />
```

---

### `chips` — `string[] | number[] | ChipModel[]`
Provides chip data programmatically as an array. Alternative to using `ChipsDirective`.

- **Default:** `[]`

```tsx
const chipsData = [
  { text: 'React', cssClass: 'e-primary' },
  { text: 'Angular', cssClass: 'e-success' }
];
<ChipListComponent chips={chipsData} />
```

---

### `selection` — `'None' | 'Single' | 'Multiple'`
Defines the selection behavior of the chip list.

- **Default:** `'None'`
- `'None'` — No selection (use for action chips)
- `'Single'` — One chip selected at a time (choice chips)
- `'Multiple'` — Multiple chips can be selected (filter chips)

```tsx
<ChipListComponent selection="Multiple">...</ChipListComponent>
```

---

### `selectedChips` — `string[] | number[] | number`
Pre-selects chips by index or text value.

- **Default:** `[]`
- Requires `selection` to be `'Single'` or `'Multiple'` to be visible.

```tsx
<ChipListComponent selection="Multiple" selectedChips={[0, 2]}>...</ChipListComponent>
```

---

### `enableDelete` — `boolean`
Shows a delete (×) icon on each chip, allowing removal.

- **Default:** `false`

```tsx
<ChipListComponent enableDelete={true}>...</ChipListComponent>
```

---

### `cssClass` — `string`
Applies custom CSS class(es) to the chip list or individual chip elements.

- **Default:** `''`
- Common values: `'e-outline'`, `'e-primary'`, `'e-success'`, `'e-info'`, `'e-warning'`, `'e-danger'`

```tsx
<ChipListComponent cssClass="e-outline">...</ChipListComponent>
```

---

### `enabled` — `boolean`
Enables or disables the entire chip list.

- **Default:** `true`
- When `false`, chips are visible but not interactive; `aria-disabled="true"` is applied.

```tsx
<ChipListComponent enabled={false}>...</ChipListComponent>
```

---

### `allowDragAndDrop` — `boolean`
Enables drag-and-drop reordering of chips within or across containers.

- **Default:** `false`

```tsx
<ChipListComponent allowDragAndDrop={true}>...</ChipListComponent>
```

---

### `dragArea` — `HTMLElement | string`
Restricts the draggable chip's movement to a specific container. Accepts a CSS selector string or an `HTMLElement`.

- **Default:** `null` (no restriction — full page)

```tsx
<ChipListComponent allowDragAndDrop={true} dragArea="#my-container">...</ChipListComponent>
```

---

### `leadingIconCss` — `string`
Specifies the CSS class for the leading (left) icon on a single chip.

- **Default:** `''`

```tsx
<ChipListComponent text="Janet" leadingIconCss="janet-icon" />
```

---

### `leadingIconUrl` — `string`
Specifies a direct image URL for the leading icon.

- **Default:** `''`

```tsx
<ChipDirective text="Profile" leadingIconUrl="https://example.com/avatar.png" />
```

---

### `avatarIconCss` — `string`
Specifies the CSS class for the avatar image in the chip.

- **Default:** `''`

```tsx
<ChipListComponent text="Andrew" avatarIconCss="andrew-avatar" />
```

---

### `avatarText` — `string`
Specifies text displayed inside the chip's circular avatar area (e.g., initials).

- **Default:** `''`

```tsx
<ChipDirective text="Andrew" avatarText="A" />
```

---

### `trailingIconCss` — `string`
Specifies the CSS class for the trailing (right) icon on a chip.

- **Default:** `''`

```tsx
<ChipDirective text="Remove" trailingIconCss="e-dlt-btn" />
```

---

### `trailingIconUrl` — `string`
Specifies a direct image URL for the trailing icon.

- **Default:** `''`

```tsx
<ChipDirective text="Download" trailingIconUrl="https://example.com/icons/download.svg" />
```

---

### `htmlAttributes` — `{ [key: string]: string }`
Passes additional HTML attributes (aria, data-*, title, etc.) to the chip element.

- **Default:** `{}`

```tsx
<ChipListComponent htmlAttributes={{ 'aria-label': 'Tag list', 'data-testid': 'chip-list' }}>
  ...
</ChipListComponent>
```

---

### `enableRtl` — `boolean`
Renders the component in right-to-left direction.

- **Default:** `false`

```tsx
<ChipListComponent enableRtl={true}>...</ChipListComponent>
```

---

### `enablePersistence` — `boolean`
Persists the component's state (e.g., selection) across page reloads using browser local storage.

- **Default:** `false`

```tsx
<ChipListComponent enablePersistence={true} selection="Multiple">...</ChipListComponent>
```

---

### `locale` — `string`
Overrides the global culture/localization for this component.

- **Default:** `''` (uses global `'en-US'`)

---

## Methods

Access methods via a React `ref`:

```tsx
const chipRef = React.useRef<ChipListComponent>(null);
<ChipListComponent ref={chipRef}>...</ChipListComponent>
```

---

### `add(chipsData)` → `void`
Adds chip(s) to the list programmatically.

- **Parameter:** `string | number | ChipModel | string[] | number[] | ChipModel[]`

```tsx
// Add a single chip by text
chipRef.current?.add('New Tag');

// Add multiple chips
chipRef.current?.add(['Tag A', 'Tag B']);

// Add with model
chipRef.current?.add({ text: 'React', cssClass: 'e-primary' });
```

---

### `remove(fields)` → `void`
Removes chip(s) by index or DOM element reference.

- **Parameter:** `number | number[] | HTMLElement | HTMLElement[]`

```tsx
// Remove chip at index 0
chipRef.current?.remove([0]);

// Remove by DOM element
const el = document.querySelector('.my-chip') as HTMLElement;
chipRef.current?.remove(el);
```

---

### `find(fields)` → `ChipDataArgs`
Finds a chip by index or DOM element and returns its data.

- **Parameter:** `number | HTMLElement`
- **Returns:** `ChipDataArgs` — contains chip data (`text`, `element`, etc.)

```tsx
const chipData = chipRef.current?.find(2);
console.log(chipData?.text); // logs text of chip at index 2
```

---

### `getSelectedChips()` → `SelectedItem | SelectedItems | undefined`
Returns the currently selected chip(s) data.

- Returns `SelectedItem` for single selection, `SelectedItems` for multiple.

```tsx
const selected = chipRef.current?.getSelectedChips();
console.log(selected);
```

---

### `select(fields)` → `void`
Programmatically selects chip(s) by index, text, or DOM element.

```tsx
// Select chip at index 1
chipRef.current?.select(1);
```

---

### `destroy()` → `void`
Removes the component from the DOM and detaches all event handlers.

```tsx
chipRef.current?.destroy();
```

---

## Events

### `onClick` — `EmitType<ClickEventArgs>`
Fires when a chip is clicked.

```tsx
<ChipListComponent onClick={(e) => console.log('Clicked:', e.target.textContent)}>
```

---

### `beforeClick` — `EmitType<ClickEventArgs>`
Fires before the click event is processed. Set `e.cancel = true` to prevent the click.

```tsx
<ChipListComponent beforeClick={(e) => { if (e.text === 'Locked') e.cancel = true; }}>
```

---

### `created` — `EmitType<Event>`
Fires when the component is created and rendered successfully.

```tsx
<ChipListComponent created={() => console.log('Chips ready')}>
```

---

### `delete` — `EmitType<DeleteEventArgs>`
Fires before a chip is removed. Set `e.cancel = true` to prevent deletion.

```tsx
<ChipListComponent
  enableDelete={true}
  delete={(e) => { if (e.text === 'Protected') e.cancel = true; }}
>
```

---

### `deleted` — `EmitType<ChipDeletedEventArgs>`
Fires after a chip has been removed.

```tsx
<ChipListComponent enableDelete={true} deleted={(e) => console.log('Removed:', e.text)}>
```

---

### `dragStart` — `EmitType<DragAndDropEventArgs>`
Fires when a chip starts being dragged. Set `args.cancel = true` to prevent dragging.

```tsx
<ChipListComponent
  allowDragAndDrop={true}
  dragStart={(args) => console.log('Drag started')}
>
```

---

### `dragging` — `EmitType<DragAndDropEventArgs>`
Fires continuously while a chip is being dragged. Use to customize the drag clone.

```tsx
<ChipListComponent
  allowDragAndDrop={true}
  dragging={(args) => { /* customize args.clonedElement */ }}
>
```

---

### `dragStop` — `EmitType<DragAndDropEventArgs>`
Fires when a drag operation ends. Set `args.cancel = true` to prevent the drop.

```tsx
<ChipListComponent
  allowDragAndDrop={true}
  dragStop={(args) => console.log('Drag stopped')}
>
```

---

## ChipModel Interface

When using the `chips` prop or `add()` method with object data, each item follows the `ChipModel` shape:

| Property | Type | Description |
|----------|------|-------------|
| `text` | `string` | Chip label text |
| `cssClass` | `string` | CSS class(es) for the chip |
| `avatarText` | `string` | Avatar initials text |
| `avatarIconCss` | `string` | CSS class for avatar image |
| `leadingIconCss` | `string` | CSS class for leading icon |
| `leadingIconUrl` | `string` | URL for leading icon image |
| `trailingIconCss` | `string` | CSS class for trailing icon |
| `trailingIconUrl` | `string` | URL for trailing icon image |
| `enabled` | `boolean` | Whether the chip is enabled |
| `htmlAttributes` | `object` | Additional HTML attributes |

```tsx
const chips: ChipModel[] = [
  { text: 'React', cssClass: 'e-primary', avatarText: 'R', enabled: true },
  { text: 'Angular', cssClass: 'e-success', avatarText: 'A', enabled: true },
  { text: 'Vue', cssClass: 'e-info', avatarText: 'V', enabled: false }
];

<ChipListComponent chips={chips} />
```

---

## Event Argument Types

| Event | Argument Type | Key Fields |
|-------|--------------|------------|
| `click` / `beforeClick` | `ClickEventArgs` | `text`, `element`, `cancel` |
| `delete` | `DeleteEventArgs` | `text`, `element`, `cancel` |
| `deleted` | `ChipDeletedEventArgs` | `text`, `element` |
| `dragStart` / `dragStop` / `dragging` | `DragAndDropEventArgs` | `element`, `clonedElement`, `cancel` |
| `created` | `Event` | Standard DOM Event |
