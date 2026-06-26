# Data Binding in Syncfusion React MultiSelect

## Table of Contents
- [Overview](#overview)
- [Field Mapping](#field-mapping)
- [Local Data Binding](#local-data-binding)
- [Remote Data Binding](#remote-data-binding)
- [Value Binding](#value-binding)
- [Troubleshooting](#troubleshooting)

---

## Overview

The MultiSelect loads data from the `dataSource` property. It supports:
- **Local data:** arrays of strings, numbers, or objects
- **Remote data:** `DataManager` connected to OData, OData V4, Web API, or custom services

Choose your data source type:
- Simple list? → Use a string/number array (no field mapping needed)
- Structured data? → Use object array + `fields` mapping
- Server-side data? → Use `DataManager` with the appropriate adaptor

---

## Field Mapping

When using object data, map columns to the required fields via the `fields` property:

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Display text for each item |
| `value` | `string` | Hidden value stored on selection (must be unique) |
| `groupBy` | `string` | Category for grouping items |
| `iconCss` | `string` | CSS class for item icon |
| `disabled` | `string` | Boolean column to disable specific items |

```tsx
const fields = { text: 'sports', value: 'id', groupBy: 'category', disabled: 'isDisabled' };
```

> **Important:** When binding complex data, always set `fields` correctly. If omitted, selected values will be `undefined`.

---

## Local Data Binding

### Array of Strings

The simplest form — `text` and `value` both represent the same item:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = ['Badminton', 'Basketball', 'Cricket', 'Football', 'Golf', 'Tennis'];
  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      placeholder="Select a sport"
    />
  );
}
```

### Array of Objects

Map `text` and `value` columns explicitly:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData = [
    { id: 'game1', sports: 'Badminton' },
    { id: 'game2', sports: 'Football' },
    { id: 'game3', sports: 'Tennis' },
    { id: 'game4', sports: 'Cricket' },
  ];
  const fields = { text: 'sports', value: 'id' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
    />
  );
}
```

### Array of Objects with Grouping

Add a `groupBy` field to categorize items:

```tsx
const vegetableData = [
  { vegetable: 'Cabbage', category: 'Leafy and Salad', id: 'item1' },
  { vegetable: 'Spinach', category: 'Leafy and Salad', id: 'item2' },
  { vegetable: 'Chickpea', category: 'Beans', id: 'item3' },
  { vegetable: 'Green bean', category: 'Beans', id: 'item4' },
  { vegetable: 'Garlic', category: 'Bulb and Stem', id: 'item5' },
];
const fields = { groupBy: 'category', text: 'vegetable', value: 'id' };

<MultiSelectComponent
  id="mtselement"
  dataSource={vegetableData}
  fields={fields}
  popupHeight="200px"
  placeholder="Select a vegetable"
/>
```

---

## Remote Data Binding

Use `DataManager` to connect to server-side data. Choose the adaptor that matches your API:

| Adaptor | Use for |
|---------|---------|
| `ODataAdaptor` | OData services |
| `ODataV4Adaptor` | OData V4 services |
| `WebApiAdaptor` | ASP.NET Web API |
| `UrlAdaptor` | Custom URL-based services |
| `JsonAdaptor` | Local JSON (in-memory) |

### OData V4 Example

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const employeeData = new DataManager({
    adaptor: new ODataV4Adaptor(),
    crossDomain: true,
    url: 'url',
  });
  const query = new Query().from('Employees').select(['FirstName', 'EmployeeID']).take(10);
  const fields = { text: 'FirstName', value: 'EmployeeID' };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      placeholder="Select an employee"
    />
  );
}
```

> **Note:** For remote data with filtering, always handle the `filtering` event with `updateData`. See [filtering.md](filtering.md).

---

## Value Binding

### Pre-select Values (Primitive)

Pass an array of value-field values to `value`:

```tsx
// Primitive pre-selection (string or number IDs)
<MultiSelectComponent
  id="mtselement"
  dataSource={sportsData}
  fields={fields}
  value={['game1', 'game3']}
  placeholder="Select a game"
/>
```

Supported primitive types: `string`, `number`, `boolean`, `null`.

### Object Binding

When `allowObjectBinding={true}`, the `value` prop accepts full objects and the selection returns complete object references:

```tsx
const records = Array.from({ length: 150 }, (_, i) => ({
  id: `id${i + 1}`,
  text: `Item ${i + 1}`,
}));
const fields = { text: 'text', value: 'id' };

// Pre-select using full objects
const preSelected = [{ id: 'id1', text: 'Item 1' }, { id: 'id2', text: 'Item 2' }];

<MultiSelectComponent
  id="mtselement"
  dataSource={records}
  fields={fields}
  value={preSelected}
  allowObjectBinding={true}
  placeholder="Select items"
/>
```

> **When to use `allowObjectBinding`:** Use when the parent component needs the full object reference on selection, not just the ID. Useful in forms that need the full entity.

---

## Troubleshooting

**Selected item shows `undefined`:**
→ You're using object data without `fields` mapping. Always set `fields={{ text: '...', value: '...' }}`.

**Remote data doesn't load:**
→ Check CORS headers on the server. Set `crossDomain: true` in `DataManager` options.

**Filtering doesn't work with remote data:**
→ Handle the `filtering` event manually with `updateData()`. See [filtering.md](filtering.md).

**Pre-selected values not shown:**
→ Ensure the values in the `value` array exactly match the `value` field values in `dataSource`.

## See Also

- [Grouping](grouping.md)
- [Filtering](filtering.md)
- [Selection Modes and Features](selection-and-features.md)
