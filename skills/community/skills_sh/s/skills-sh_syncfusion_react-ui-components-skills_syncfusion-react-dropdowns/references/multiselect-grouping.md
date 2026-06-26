# Grouping in Syncfusion React MultiSelect

Organize dropdown items into labeled categories for easier navigation.

---

## Overview

Grouping lets you wrap items under category headers in the popup list. The group header appears both as an **inline** label (within the list flow) and as a **fixed** header (pinned at the top of the popup as you scroll).

Use grouping when your data has categories and you want users to understand the hierarchy — e.g., vegetable types, country regions, or product categories.

---

## Basic Grouping

Add a `groupBy` field to your data objects and map it in the `fields` property:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const vegetableData = [
    { vegetable: 'Cabbage',    category: 'Leafy and Salad', id: 'item1' },
    { vegetable: 'Spinach',    category: 'Leafy and Salad', id: 'item2' },
    { vegetable: 'Wheat grass',category: 'Leafy and Salad', id: 'item3' },
    { vegetable: 'Yarrow',     category: 'Leafy and Salad', id: 'item4' },
    { vegetable: 'Chickpea',   category: 'Beans',           id: 'item5' },
    { vegetable: 'Green bean', category: 'Beans',           id: 'item6' },
    { vegetable: 'Horse gram', category: 'Beans',           id: 'item7' },
    { vegetable: 'Garlic',     category: 'Bulb and Stem',   id: 'item8' },
    { vegetable: 'Nopal',      category: 'Bulb and Stem',   id: 'item9' },
    { vegetable: 'Onion',      category: 'Bulb and Stem',   id: 'item10' },
  ];
  const fields = { groupBy: 'category', text: 'vegetable', value: 'id' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={vegetableData}
      fields={fields}
      popupHeight="200px"
      placeholder="Select a vegetable"
    />
  );
}
```

---

## Fixed Group Headers

When the popup is open and the user scrolls, the **fixed header** at the top of the popup automatically updates to display the current group category. This is built-in behavior — no extra configuration needed.

The component handles both inline headers (between items) and fixed headers (pinned at popup top) automatically.

---

## Custom Group Header Template

Customize how group headers are rendered using the `groupTemplate` prop:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const countryData = [
    { name: 'Chicago',    id: 'US', country: 'United States' },
    { name: 'Houston',    id: 'US', country: 'United States' },
    { name: 'Mumbai',     id: 'IN', country: 'India' },
    { name: 'Bangalore',  id: 'IN', country: 'India' },
    { name: 'London',     id: 'UK', country: 'United Kingdom' },
    { name: 'Manchester', id: 'UK', country: 'United Kingdom' },
  ];
  const fields = { text: 'name', value: 'id', groupBy: 'country' };

  // Custom group header renders country name with an icon
  const groupTemplate = (data: any): JSX.Element => {
    return (<strong>🌍 {data.country}</strong>);
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={countryData}
      fields={fields}
      groupTemplate={groupTemplate}
      placeholder="Select a city"
    />
  );
}
```

---

## Combining Grouping with Filtering

Grouping works with `allowFiltering`. The group headers remain visible as the user filters items:

```tsx
<MultiSelectComponent
  id="mtselement"
  dataSource={vegetableData}
  fields={{ groupBy: 'category', text: 'vegetable', value: 'id' }}
  allowFiltering={true}
  placeholder="Search vegetables"
/>
```

For remote-filtered data with groups, handle the `filtering` event — see [filtering.md](filtering.md).

---

## Gotchas

- **Items must share the same `groupBy` value string exactly** (case-sensitive) to appear in the same group.
- Group order follows the order items appear in the data source, not alphabetical. Sort your data source beforehand if you need ordered groups.
- To allow selecting all items in a group at once, use `mode="CheckBox"` with `enableGroupCheckBox={true}` and inject the `CheckBoxSelection` module. This renders a checkbox on group headers that selects/deselects all items in that group.

## See Also

- [Data Binding](data-binding.md) — setting up `fields` with `groupBy`
- [Templates](templates.md) — custom group header templates
- [Filtering](filtering.md) — combining filtering with grouped data
