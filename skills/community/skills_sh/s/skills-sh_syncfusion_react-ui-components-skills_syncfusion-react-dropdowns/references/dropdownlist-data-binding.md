# Data Binding & Value Binding

## Table of Contents
- [Fields Mapping](#fields-mapping)
- [Binding Local Data](#binding-local-data)
  - [Primitive Array](#1-primitive-array-strings-numbers)
  - [JSON Object Array](#2-json-object-array)
  - [Complex/Nested Objects](#3-complex--nested-objects)
- [Binding Remote Data](#binding-remote-data)
- [Value Binding](#value-binding)
  - [Preselecting a Value](#preselecting-a-value)
  - [Object Binding](#object-binding)
- [Disabling Individual Items](#disabling-individual-items)
- [Gotchas](#gotchas)

---

## Fields Mapping

When binding JSON objects, use the `fields` prop to map your data columns:

| Field | Type | Purpose |
|---|---|---|
| `text` | `string` | Display label shown in the list and input |
| `value` | `string` | Hidden unique identifier |
| `groupBy` | `string` | Column used to group items |
| `iconCss` | `string` | CSS class for an icon displayed beside the item |
| `disabled` | `string` | Boolean column — items where this is `true` are non-selectable |

> **Important:** When binding complex data, always set `fields` correctly. Without it, selected items will be `undefined`.

---

## Binding Local Data

### 1. Primitive Array (strings, numbers)

Simplest case — no `fields` needed. Value and text are the same:

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: string[] = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  return (
    <DropDownListComponent
      id="ddlelement"
      dataSource={sportsData}
      placeholder="Select a game"
    />
  );
}
```

### 2. JSON Object Array

Map `text` (display) and `value` (key) from your object columns:

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData = [
    { Id: 'game1', Game: 'Badminton' },
    { Id: 'game2', Game: 'Football' },
    { Id: 'game3', Game: 'Tennis' },
  ];
  const fields = { text: 'Game', value: 'Id' };

  return (
    <DropDownListComponent
      dataSource={sportsData}
      fields={fields}
      placeholder="Select a game"
    />
  );
}
```

### 3. Complex / Nested Objects

Use dot-notation strings for nested properties:

```tsx
const countriesData = [
  { Country: { Name: 'Australia' }, Code: { Id: 'AU' } },
  { Country: { Name: 'Bermuda' },   Code: { Id: 'BM' } },
  { Country: { Name: 'Canada' },    Code: { Id: 'CA' } },
];
// Map nested properties with dot notation
const fields = { text: 'Country.Name', value: 'Code.Id' };

<DropDownListComponent dataSource={countriesData} fields={fields} placeholder="Select a country" />
```

---

## Binding Remote Data

Use `DataManager` to fetch data from OData, OData V4, or Web API services.

### OData V4 (Northwind)

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const customerData = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url',
  });
  const query = new Query().from('Customers').select(['ContactName', 'CustomerID']).take(6);
  const fields = { text: 'ContactName', value: 'CustomerID' };

  return (
    <DropDownListComponent
      dataSource={customerData}
      query={query}
      fields={fields}
      sortOrder="Ascending"
      placeholder="Select a customer"
    />
  );
}
```

### Web API

```tsx
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';

const orderData = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor,
  crossDomain: true,
});
const fields = { text: 'OrderID', value: 'OrderID' };

<DropDownListComponent dataSource={orderData} fields={fields} placeholder="Select an Order" />
```

---

## Value Binding

### Preselecting a Value

#### Primitive value preselection

```tsx
// String array — pass the string directly
<DropDownListComponent
  dataSource={['Badminton', 'Cricket', 'Football']}
  value="Cricket"
  placeholder="Select a game"
/>
```

#### JSON object — preselect by the `value` field

```tsx
const sportsData = [
  { Id: 'game1', Game: 'Badminton' },
  { Id: 'game2', Game: 'Football' },
];
const fields = { text: 'Game', value: 'Id' };

<DropDownListComponent
  dataSource={sportsData}
  fields={fields}
  value="game2"   // matches the Id
  placeholder="Select a game"
/>
```

### Object Binding

Enable `allowObjectBinding` to work with entire object values instead of primitive keys. When enabled, the `value` prop accepts and returns an object of the same shape as your data items:

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const records = Array.from({ length: 10 }, (_, i) => ({
    id: `id${i + 1}`,
    text: `Item ${i + 1}`,
  }));
  const fields = { text: 'text', value: 'id' };
  // Preselect using a full object
  const value = { text: 'Item 1', id: 'id1' };

  return (
    <DropDownListComponent
      dataSource={records}
      fields={fields}
      value={value}
      allowObjectBinding={true}
      placeholder="e.g. Item 1"
    />
  );
}
```

---

## Disabling Individual Items

Map a boolean column from your data using `fields.disabled`. Items where this value is `true` appear greyed out and cannot be selected:

```tsx
const statusData = [
  { Status: 'Open',                    State: false },
  { Status: 'Waiting for Customer',    State: false },
  { Status: 'On Hold',                 State: true  },  // disabled
  { Status: 'Follow-up',               State: false },
  { Status: 'Closed',                  State: true  },  // disabled
];
const fields = { text: 'Status', value: 'Status', disabled: 'State' };

<DropDownListComponent dataSource={statusData} fields={fields} placeholder="Select a status" />
```

---

## Gotchas

- **Missing `fields` mapping with JSON data** → selected value will be `undefined`. Always set `text` and `value` when using objects.
- **`value` prop must match the `value` field** (not the `text` field) for preselection to work.
- **Dot-notation for nested objects** — use `'Country.Name'` style strings, not function accessors.
- **Remote data + `sortOrder`** — sort is applied client-side after the query resolves; combine with server-side `$orderby` for large datasets.
- **`allowObjectBinding`** — when enabled, reading `dropdownRef.value` returns the full object, not a primitive.

## See Also

- [Filtering](filtering.md) — search the bound data
- [Grouping & Templates](grouping-and-templates.md) — group items with `groupBy`
- [How-To](how-to.md) — add/remove items, cascading, remote data how-to
