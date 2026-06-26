# Selection Modes and Features in Syncfusion React MultiSelect

## Table of Contents
- [Selection Modes](#selection-modes)
- [Checkbox Mode](#checkbox-mode)
- [Chip Customization](#chip-customization)
- [Custom Values](#custom-values)
- [Disabled Items](#disabled-items)
- [Popup Resizing](#popup-resizing)
- [Virtual Scrolling](#virtual-scrolling)

---

## Selection Modes

The `mode` prop controls how selected items are displayed in the input field:

| Mode | Display | When to Use |
|------|---------|-------------|
| `Default` | Chips (Box-style, removable) | Standard multi-select with chip UI |
| `Box` | Chips (same as Default) | Explicitly specified chip mode |
| `Delimiter` | Comma-separated text | Compact single-line display |
| `CheckBox` | Popup list with checkboxes | Selecting from a visible checklist |

```tsx
// Chip display (default)
<MultiSelectComponent mode="Box" ... />

// Comma-separated: "Badminton, Cricket, Tennis"
<MultiSelectComponent mode="Delimiter" ... />

// Checkbox list
<MultiSelectComponent mode="CheckBox" ... />
```

---

## Checkbox Mode

Enable checkbox-style selection by setting `mode="CheckBox"` and injecting the `CheckBoxSelection` module:

```tsx
import { CheckBoxSelection, Inject, MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = [
    { Id: 'game1', Game: 'Badminton' },
    { Id: 'game2', Game: 'Football' },
    { Id: 'game3', Game: 'Tennis' },
    { Id: 'game4', Game: 'Golf' },
    { Id: 'game5', Game: 'Cricket' },
    { Id: 'game6', Game: 'Hockey' },
  ];
  const fields = { text: 'Game', value: 'Id' };

  return (
    <MultiSelectComponent
      id="checkbox"
      dataSource={sportsData}
      fields={fields}
      mode="CheckBox"
      placeholder="Select games"
    >
      <Inject services={[CheckBoxSelection]} />
    </MultiSelectComponent>
  );
}
```

> **Why inject?** The `CheckBoxSelection` module is tree-shaken by default. You must explicitly inject it to enable checkbox rendering. Without it, `mode="CheckBox"` falls back to default chip display.

### Checkbox with "Select All"

Add a Select All option by setting `showSelectAll={true}`:

```tsx
<MultiSelectComponent
  id="checkbox"
  dataSource={sportsData}
  fields={fields}
  mode="CheckBox"
  showSelectAll={true}
  selectAllText="Select All"
  unSelectAllText="Unselect All"
  placeholder="Select games"
>
  <Inject services={[CheckBoxSelection]} />
</MultiSelectComponent>
```

---

## Chip Customization

Customize chip appearance per-item using the `tagging` event. Use the `setClass()` method to apply a custom CSS class:

```tsx
import { MultiSelectComponent, TaggingEventArgs } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const colorsData = [
    { Color: 'Chocolate', Code: '#75523C' },
    { Color: 'CadetBlue', Code: '#3B8289' },
    { Color: 'LimeGreen',  Code: '#4CD242' },
    { Color: 'Tomato',    Code: '#FF745C' },
  ];
  const fields = { text: 'Color', value: 'Code' };
  const preSelected = ['#75523C', '#4CD242'];

  const onTagging = (e: TaggingEventArgs) => {
    // Apply the color name as a CSS class to the chip element
    e.setClass((e.itemData as any)[fields.text].toLowerCase());
  };

  return (
    <MultiSelectComponent
      id="chip-customization"
      dataSource={colorsData}
      fields={fields}
      value={preSelected}
      mode="Box"
      tagging={onTagging}
      placeholder="Favorite Colors"
    />
  );
}
```

Then define per-color CSS:

```css
.chocolate { background-color: #75523C; color: white; }
.cadetblue  { background-color: #3B8289; color: white; }
.limegreen  { background-color: #4CD242; }
.tomato     { background-color: #FF745C; }
```

> **Pattern:** `setClass()` receives a string class name (not a style object). Define the CSS separately. The class is applied to the chip's root element.

---

## Custom Values

Allow users to type and select values not in the original data source using `allowCustomValue`:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = [
    { id: 'game1', sports: 'Badminton' },
    { id: 'game2', sports: 'Football' },
    { id: 'game3', sports: 'Tennis' },
  ];
  const fields = { text: 'sports', value: 'id' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      fields={fields}
      allowCustomValue={true}
      placeholder="Select or type a sport"
    />
  );
}
```

### Handling the Custom Value Selection Event

To act on custom entries (e.g., save to a database, validate), listen to `customValueSelection`:

```tsx
import { CustomValueEventArgs, MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';

const onCustomValue = (args: CustomValueEventArgs) => {
  console.log('New custom value entered:', args.text);
  // args.newData contains the new item object to be added
};

<MultiSelectComponent
  allowCustomValue={true}
  customValueSelection={onCustomValue}
  ...
/>
```

---

## Disabled Items

Disable specific items so they appear in the list but cannot be selected. Map a boolean field from the data to `fields.disabled`:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const tagData = [
    { Text: 'Add to KB',      State: false },  // selectable
    { Text: 'Enhancement',    State: true },   // disabled
    { Text: 'Presale',        State: false },  // selectable
    { Text: 'Approved',       State: true },   // disabled
    { Text: 'Breaking Issue', State: false },  // selectable
    { Text: 'New Feature',    State: true },   // disabled
  ];
  // 'State: true' means the item is disabled
  const fields = { value: 'Text', disabled: 'State' };

  return (
    <MultiSelectComponent
      id="atcelement"
      dataSource={tagData}
      fields={fields}
      placeholder="Select Tags"
    />
  );
}
```

> **Convention:** `disabled: true` in the data means the item is NOT selectable. Disabled items render visually greyed out and are skipped by keyboard navigation.

---

## Popup Resizing

Let users drag to resize the popup panel by enabling `allowResize`:

```tsx
<MultiSelectComponent
  id="mtselement"
  dataSource={tagData}
  allowResize={true}
  placeholder="Select Tags"
/>
```

The resized dimensions persist across user interactions. No additional configuration is needed.

---

## Virtual Scrolling

Improve performance for large datasets (500+ items) using virtualization. Only a fixed number of DOM elements are rendered and recycled as the user scrolls.

### Local Data

```tsx
import { Inject, MultiSelectComponent, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  // Generate 1000 items
  const records = Array.from({ length: 1000 }, (_, i) => ({
    id: `id${i + 1}`,
    text: `Item ${i + 1}`,
  }));
  const fields = { text: 'text', value: 'id' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={records}
      fields={fields}
      enableVirtualization={true}
      allowFiltering={false}
      popupHeight="200px"
      placeholder="Select items"
    >
      <Inject services={[VirtualScroll]} />
    </MultiSelectComponent>
  );
}
```

### Remote Data with Virtual Scrolling

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';
import { Inject, MultiSelectComponent, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const customerData = new DataManager({
    adaptor: new UrlAdaptor(),
    url: 'url',
  });
  const fields = { text: 'OrderID', value: 'OrderID' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={customerData}
      fields={fields}
      enableVirtualization={true}
      popupHeight="200px"
      placeholder="Select an order"
    >
      <Inject services={[VirtualScroll]} />
    </MultiSelectComponent>
  );
}
```

> **Required:** The `VirtualScroll` module MUST be injected via `<Inject services={[VirtualScroll]} />`. Without it, `enableVirtualization` has no effect.

**Virtual scroll behavior:**
- DOM elements are recycled as you scroll (reduces memory/rendering cost)
- `actionBegin` fires before data fetch; `actionComplete` fires after
- Incremental search (keyboard) is supported — typing moves focus to the matching item in the popup

## See Also

- [Data Binding](data-binding.md) — pre-selecting values, object binding
- [Templates](templates.md) — custom chip templates via `valueTemplate`
- [Filtering](filtering.md) — combining virtual scroll with search
- [Accessibility & Styling](accessibility-styling-localization.md) — CSS customization for chips
