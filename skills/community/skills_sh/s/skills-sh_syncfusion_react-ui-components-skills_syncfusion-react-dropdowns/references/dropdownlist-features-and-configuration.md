# Features & Configuration

## Table of Contents
- [Sorting](#sorting)
- [Virtual Scrolling](#virtual-scrolling)
  - [Local Data](#local-data-virtual-scroll)
  - [Remote Data](#remote-data-virtual-scroll)
  - [Grouping with Virtualization](#grouping-with-virtualization)
  - [Customizing Item Count](#customizing-item-count)
- [Popup Resize](#popup-resize)
- [Incremental Search](#incremental-search)
- [Clear Button](#clear-button)
- [Readonly and Disabled](#readonly-and-disabled)
- [RTL Support](#rtl-support)
- [Preact Usage](#preact-usage)
- [Gotchas](#gotchas)

---

## Sorting

Use `sortOrder` to sort the popup list items automatically. Applied client-side after data loads:

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

<DropDownListComponent
  dataSource={sportsData}
  sortOrder="Ascending"   // 'None' | 'Ascending' | 'Descending'
  placeholder="Select a game"
/>
```

For remote data, combine with a server-side `$orderby` query for large datasets; client-side sort applies only to the currently loaded page.

---

## Virtual Scrolling

Virtual scrolling renders only the visible DOM elements, reusing them as the user scrolls. This is ideal for datasets with thousands of items. 

**Requirement:** Import `VirtualScroll` service and inject it:

```tsx
import { DropDownListComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
```

### Local Data Virtual Scroll

```tsx
import { DropDownListComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  // Generate 150 items
  const records = Array.from({ length: 150 }, (_, i) => ({
    id: `id${i + 1}`,
    text: `Item ${i + 1}`,
  }));
  const fields = { text: 'text', value: 'id' };

  return (
    <DropDownListComponent
      dataSource={records}
      fields={fields}
      enableVirtualization={true}
      allowFiltering={false}
      popupHeight="200px"
      placeholder="e.g. Item 1"
    >
      <Inject services={[VirtualScroll]} />
    </DropDownListComponent>
  );
}
```

### Remote Data Virtual Scroll

```tsx
import { DropDownListComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

export default function App() {
  const customerData = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor,
    crossDomain: true,
  });
  const fields = { text: 'OrderID', value: 'OrderID' };

  return (
    <DropDownListComponent
      dataSource={customerData}
      fields={fields}
      enableVirtualization={true}
      allowFiltering={true}
      popupHeight="200px"
      placeholder="OrderID"
    >
      <Inject services={[VirtualScroll]} />
    </DropDownListComponent>
  );
}
```

### Grouping with Virtualization

`groupBy` works with virtualization. For remote data, all data is fetched initially for grouping, then virtualized locally:

```tsx
// Generate grouped records
const records = Array.from({ length: 150 }, (_, i) => {
  const groups = ['Group A', 'Group B', 'Group C', 'Group D'];
  return {
    id: `id${i + 1}`,
    text: `Item ${i + 1}`,
    group: groups[i % 4],
  };
});
const fields = { groupBy: 'group', text: 'text', value: 'id' };

<DropDownListComponent
  dataSource={records}
  fields={fields}
  enableVirtualization={true}
  allowFiltering={true}
  popupHeight="200px"
>
  <Inject services={[VirtualScroll]} />
</DropDownListComponent>
```

### Customizing Item Count

Override how many items are fetched per scroll page using `query` with `.take()` or via the `actionBegin` event:

```tsx
import { Query } from '@syncfusion/ej2-data';

const query = new Query().take(40);

function onActionBegin(e: any) {
  e.query = new Query().take(45);
}

<DropDownListComponent
  dataSource={records}
  fields={fields}
  query={query}
  actionBegin={onActionBegin}
  enableVirtualization={true}
  popupHeight="200px"
>
  <Inject services={[VirtualScroll]} />
</DropDownListComponent>
```

> **Note:** If the specified `take` value is less than the minimum items required to fill the viewport, the internal calculation takes precedence.

---

## Popup Resize

Allow users to drag-resize the popup for better visibility. The resized dimension persists across sessions:

```tsx
<DropDownListComponent
  dataSource={sportsData}
  allowResize={true}
  placeholder="Select a game"
/>
```

---

## Incremental Search

Incremental search is enabled by default when the popup is closed — typing characters while the popup is closed moves focus to the matching item. In an open popup state with `enableVirtualization`, the focus moves to the matching item in the list.

No configuration is needed for basic incremental search. It works out of the box.

---

## Clear Button

Show a clear (✕) button inside the input to let users reset the selection:

```tsx
<DropDownListComponent
  dataSource={sportsData}
  showClearButton={true}
  placeholder="Select a game"
/>
```

---

## Readonly and Disabled

```tsx
// Readonly — shows value but user cannot change it
<DropDownListComponent dataSource={sportsData} value="Cricket" readonly={true} />

// Disabled — greyed out, no interaction
<DropDownListComponent dataSource={sportsData} enabled={false} placeholder="Disabled" />
```

**Difference:**
- `readonly={true}` — the component renders the current value but does not open the popup.
- `enabled={false}` — the component is fully non-interactive and visually greyed out.

---

## RTL Support

Enable right-to-left layout for Arabic, Hebrew, and other RTL languages:

```tsx
<DropDownListComponent
  dataSource={sportsData}
  enableRtl={true}
  placeholder="Select a game"
/>
```

---

## Preact Usage

The DropDownList component is compatible with Preact. Import from the same package; usage is identical to the React functional component pattern. Refer to [Syncfusion Preact documentation](https://ej2.syncfusion.com/react/documentation/drop-down-list/preact) for bundle setup differences.

---

## Gotchas

- **`enableVirtualization` requires `<Inject services={[VirtualScroll]} />`** as a child — omitting this causes virtual scroll to not work.
- **`skip`/`take` in Query is overridden** when `enableVirtualization` is active — the component calculates its own pagination based on popup height.
- **`sortOrder` is client-side** — for remote large datasets, always add server-side ordering to your query.
- **`allowResize` persistence** — resize dimensions are stored in the browser. They may not match designs if users have resized previously.
- **`readonly` vs `enabled`** — do not confuse them; `readonly` still shows a styled input, `enabled={false}` removes all pointer events.

## See Also

- [Data Binding](data-binding.md) — bind data to the virtualized list
- [Filtering](filtering.md) — combine filtering with virtual scrolling
- [Accessibility, Styling & Localization](accessibility-styling-localization.md) — keyboard nav, theming
