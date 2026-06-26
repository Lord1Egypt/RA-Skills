# Data Binding – Syncfusion React AutoComplete

## Table of Contents
- [Field Mapping Overview](#field-mapping-overview)
- [Array of Strings](#array-of-strings)
- [Array of Objects](#array-of-objects)
- [Complex/Nested Object Arrays](#complexnested-object-arrays)
- [Remote Data with DataManager](#remote-data-with-datamanager)
- [Sorting Bound Data](#sorting-bound-data)

---

## Field Mapping Overview

When binding objects to AutoComplete, map data columns using the `fields` property:

| Field | Type | Description |
|---|---|---|
| `value` | `string` | The column whose value is shown in the input on selection |
| `groupBy` | `string` | Groups list items under categories |
| `iconCss` | `string` | CSS class applied as an icon before each list item |
| `disabled` | `string` | Boolean column to disable specific items |

> When binding complex data, always map fields correctly; otherwise the selected item will be `undefined`.

---

## Array of Strings

The simplest form — pass a `string[]` directly to `dataSource`:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: string[] = [
    'Badminton', 'Basketball', 'Cricket', 'Football',
    'Golf', 'Hockey', 'Snooker', 'Tennis'
  ];

  return (
    <AutoCompleteComponent id="atcelement" dataSource={sportsData} placeholder="Find a game" />
  );
}
```

---

## Array of Objects

Pass an object array and map the display column to `fields.value`:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: { [key: string]: Object }[] = [
    { id: 'Game1', game: 'Badminton' },
    { id: 'Game2', game: 'Basketball' },
    { id: 'Game3', game: 'Cricket' },
    { id: 'Game4', game: 'Football' },
    { id: 'Game5', game: 'Golf' },
    { id: 'Game6', game: 'Hockey' },
    { id: 'Game7', game: 'Rugby' },
    { id: 'Game8', game: 'Snooker' }
  ];

  const fields: object = { value: 'game' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={sportsData}
      fields={fields}
      placeholder="Find a game"
    />
  );
}
```

---

## Complex/Nested Object Arrays

Use dot-notation in the `value` field to access nested properties:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const countriesData: { [key: string]: Object }[] = [
    { Country: { Name: 'Australia' }, Code: { Id: 'AU' } },
    { Country: { Name: 'Bermuda' }, Code: { Id: 'BM' } },
    { Country: { Name: 'Canada' }, Code: { Id: 'CA' } },
    { Country: { Name: 'Denmark' }, Code: { Id: 'DK' } },
    { Country: { Name: 'France' }, Code: { Id: 'FR' } },
    { Country: { Name: 'Germany' }, Code: { Id: 'DE' } },
    { Country: { Name: 'India' }, Code: { Id: 'IN' } },
    { Country: { Name: 'Japan' }, Code: { Id: 'JP' } },
  ];

  // Dot notation maps the nested "Country.Name" path
  const fields: object = { value: 'Country.Name' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={countriesData}
      fields={fields}
      placeholder="Find a country"
    />
  );
}
```

---

## Remote Data with DataManager

Use `DataManager` with an adaptor to load data from a remote service. The `query` property controls what data is fetched:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const customerData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });

  const query: Query = new Query()
    .from('Customers')
    .select(['ContactName', 'CustomerID'])
    .take(6);

  const fields: object = { value: 'ContactName' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={customerData}
      query={query}
      fields={fields}
      sortOrder="Ascending"
      placeholder="Find a customer"
    />
  );
}
```

**Supported adaptors:** `ODataAdaptor`, `ODataV4Adaptor`, `WebApiAdaptor`, `UrlAdaptor`, `JsonAdaptor`

> Use the `query` property to select specific columns, apply filters, or limit the result set. Without a `query`, all records are fetched.

---

## Sorting Bound Data

Use `sortOrder` to sort the suggestion list alphabetically:

```tsx
<AutoCompleteComponent
  dataSource={customerData}
  fields={{ value: 'ContactName' }}
  sortOrder="Ascending"   // 'None' | 'Ascending' | 'Descending'
  placeholder="Find a customer"
/>
```

| Value | Behavior |
|---|---|
| `'None'` | No sorting applied (default) |
| `'Ascending'` | A → Z |
| `'Descending'` | Z → A |
