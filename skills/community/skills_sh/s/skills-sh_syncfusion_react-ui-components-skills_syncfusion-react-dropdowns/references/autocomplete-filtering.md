# Filtering – Syncfusion React AutoComplete

## Table of Contents
- [Filter Types](#filter-types)
- [Suggestion Count](#suggestion-count)
- [Minimum Filter Character Length](#minimum-filter-character-length)
- [Case Sensitive Filtering](#case-sensitive-filtering)
- [Diacritics Filtering](#diacritics-filtering)
- [Debounce Delay](#debounce-delay)
- [Custom Filtering with the filtering Event](#custom-filtering-with-the-filtering-event)

---

## Filter Types

Control how suggestion matching works via `filterType`. Default is `'Contains'`.

| FilterType | Description |
|---|---|
| `'StartsWith'` | Matches items that begin with the typed characters |
| `'EndsWith'` | Matches items that end with the typed characters |
| `'Contains'` | Matches items containing the typed characters anywhere |

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const searchData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });
  const query: Query = new Query().from('Suppliers').select(['SupplierID', 'ContactName']).take(10);
  const fields: object = { value: 'ContactName' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={searchData}
      query={query}
      fields={fields}
      filterType="StartsWith"
      sortOrder="Ascending"
      placeholder="Find a supplier"
    />
  );
}
```

---

## Suggestion Count

Limit the number of items shown in the suggestion popup using `suggestionCount`. Default is `20`.

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={customerData}
  query={query}
  fields={{ value: 'ContactName' }}
  suggestionCount={5}
  filterType="StartsWith"
  sortOrder="Ascending"
  placeholder="Find a customer"
/>
```

---

## Minimum Filter Character Length

Set the minimum number of characters the user must type before filtering begins via `minLength`. Default is `1`.

Useful for remote data to avoid triggering requests on every single character:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const searchData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });
  const query: Query = new Query().select(['ContactName', 'CustomerID']).take(10);
  const fields: object = { value: 'ContactName' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={searchData}
      query={query}
      fields={fields}
      filterType="StartsWith"
      sortOrder="Ascending"
      minLength={3}
      placeholder="Type at least 3 chars"
    />
  );
}
```

---

## Case Sensitive Filtering

By default `ignoreCase` is `true` (case-insensitive). Set `ignoreCase={false}` to make filtering case-sensitive:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const searchData: string[] = ['ram', 'Ravi', 'suresh', 'Suresh'];

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={searchData}
      filterType="StartsWith"
      ignoreCase={false}
      placeholder="e.g. Ravi"
    />
  );
}
```

> With `ignoreCase={false}`, typing "r" will match "ram" but not "Ravi".

---

## Diacritics Filtering

Enable `ignoreAccent={true}` to ignore diacritic characters (accents) during filtering. This helps users search international character lists without typing the exact accented character:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const diacriticsData: string[] = [
    'Aeróbics', 'Aeróbics en Agua', 'Aerografía', 'Aeromodelaje',
    'Águilas', 'Ajedrez', 'Ala Delta', 'Álbumes de Música'
  ];

  return (
    <AutoCompleteComponent
      id="diacritics"
      dataSource={diacriticsData}
      ignoreAccent={true}
      placeholder="e.g. aero"
    />
  );
}
```

> With `ignoreAccent={true}`, typing "aero" will match "Aeróbics", "Aerografía", etc.

---

## Debounce Delay

Use `debounceDelay` to set a millisecond delay before the filter action fires. Default is `300ms`. Set to `0` to disable debounce entirely:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const sportsData: string[] = ['Badminton', 'Basketball', 'Cricket', 'Football', 'Golf'];

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={sportsData}
      debounceDelay={500}     // Wait 500ms after user stops typing
      placeholder="Find a game"
    />
  );
}
```

---

## Custom Filtering with the filtering Event

Use the `filtering` event to implement custom filter logic, such as sending custom server-side queries:

```tsx
import { AutoCompleteComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, Query, ODataV4Adaptor } from '@syncfusion/ej2-data';
import * as React from 'react';

export default function App() {
  const remoteData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });

  function onFiltering(args: FilteringEventArgs) {
    // Build a custom query based on user input
    const query = new Query()
      .from('Customers')
      .select(['ContactName', 'CustomerID'])
      .where('ContactName', 'startswith', args.text, true)
      .take(10);
    args.updateData(remoteData, query);
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={remoteData}
      fields={{ value: 'ContactName' }}
      filtering={onFiltering}
      placeholder="Find a customer"
    />
  );
}
```

> The `filtering` event fires on every keystroke (subject to `debounceDelay`). Call `args.updateData(dataSource, query)` to provide filtered results.
