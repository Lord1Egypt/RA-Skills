# Filtering in Syncfusion React MultiSelect

## Table of Contents
- [Overview](#overview)
- [Enable Filtering](#enable-filtering)
- [Handling the Filtering Event](#handling-the-filtering-event)
- [Filter Types](#filter-types)
- [Remote Data Filtering](#remote-data-filtering)
- [Case Sensitivity and Multiple Conditions](#case-sensitivity-and-multiple-conditions)
- [Performance Tips](#performance-tips)
- [Troubleshooting](#troubleshooting)

---

## Overview

Filtering lets users type characters in the input and see a filtered subset of options in real-time. Use filtering when:
- The list has 20+ items and users need to search quickly
- Items are loaded from a remote API (type-to-search pattern)
- You want to narrow choices for better UX

**Local data:** Set `allowFiltering={true}` — no extra event handling needed.  
**Remote data:** Set `allowFiltering={true}` AND handle the `filtering` event to query the server.

---

## Enable Filtering

For local data sources, enabling filtering is one line:

```tsx
import { MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const countries = ['Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Australia', 'Austria',
    'Bangladesh', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', 'Egypt', 'Finland'];

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={countries}
      allowFiltering={true}
      placeholder="Search a country"
    />
  );
}
```

---

## Handling the Filtering Event

For object data or custom filter logic, use the `filtering` event to supply filtered results via `updateData()`:

```tsx
import { Query } from '@syncfusion/ej2-data';
import { FilteringEventArgs, MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const searchData = [
    { index: 's1', country: 'Alaska' },
    { index: 's2', country: 'California' },
    { index: 's3', country: 'Florida' },
    { index: 's4', country: 'Georgia' },
    { index: 's5', country: 'Hawaii' },
    { index: 's6', country: 'Illinois' },
  ];
  const fields = { text: 'country', value: 'index' };

  const onFiltering = (args: FilteringEventArgs) => {
    let query = new Query();
    // Build filter query: show all items when input is empty
    query = args.text !== ''
      ? query.where('country', 'startswith', args.text, true)
      : query;
    // Pass filtered data back to the component
    args.updateData(searchData, query);
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={searchData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      placeholder="Select a country"
    />
  );
}
```

> **Key pattern:** Always call `args.updateData(dataSource, query)` inside the `filtering` handler. Without this call, the popup won't update with filtered results.

---

## Filter Types

Use different filter operators in the `Query.where()` method:

| Operator | Description | Example |
|----------|-------------|---------|
| `startswith` | Starts with typed text | `'Al'` → Alaska, Albania |
| `contains` | Contains typed text anywhere | `'an'` → Canada, Bangladesh |
| `endswith` | Ends with typed text | `'ia'` → India, Australia |
| `equal` | Exact match | `'Alaska'` |
| `notequal` | Excludes exact match | |

```tsx
// contains — often better UX than startswith
query = args.text !== ''
  ? query.where('country', 'contains', args.text, true)
  : query;
```

---

## Remote Data Filtering

For server-side filtering, use `DataManager` and build the query in the `filtering` event:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { FilteringEventArgs, MultiSelectComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const employeeData = new DataManager({
    adaptor: new ODataV4Adaptor(),
    crossDomain: true,
    url: 'url',
  });
  const query = new Query().from('Employees').select(['FirstName', 'EmployeeID']).take(6);
  const fields = { text: 'FirstName', value: 'EmployeeID' };

  const onFiltering = (args: FilteringEventArgs) => {
    let filteredQuery = new Query().from('Employees').select(['FirstName', 'EmployeeID']).take(6);
    filteredQuery = args.text !== ''
      ? filteredQuery.where('FirstName', 'startswith', args.text, true)
      : filteredQuery;
    args.updateData(employeeData, filteredQuery);
  };

  return (
    <MultiSelectComponent
      id="mtselement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      placeholder="Search employees"
    />
  );
}
```

---

## Case Sensitivity and Multiple Conditions

The 4th argument to `where()` controls case sensitivity (`true` = case-insensitive):

```tsx
// Case-insensitive (recommended for user-facing filters)
query.where('country', 'startswith', args.text, true)

// Case-sensitive
query.where('country', 'startswith', args.text, false)
```

Multiple conditions (AND logic):

```tsx
query
  .where('country', 'startswith', args.text, true)
  .where('active', 'equal', true);
```

---

## Performance Tips

- **Debounce large datasets:** For remote APIs, add a debounce delay to avoid firing requests on every keystroke. Consider adding a minimum character count before triggering remote calls.
- **Use virtual scrolling with filtering:** Combine `allowFiltering={true}` with `enableVirtualization={true}` and the `VirtualScroll` module for best performance on large remote datasets.
- **Limit query results:** Use `.take(n)` in the query to cap results returned from remote APIs.

---

## Troubleshooting

**Filtering is enabled but popup doesn't update with typed text:**
→ For object data, you must handle the `filtering` event and call `args.updateData()`. Local string arrays filter automatically.

**Remote filtering fires too many requests:**
→ The component fires one request per keystroke by default. Add a debounce wrapper around your remote call.

**Filter clears all items when input is empty:**
→ In the `filtering` handler, when `args.text === ''`, pass an empty `Query()` (no `where` clause) to show all items.

## See Also

- [Data Binding](data-binding.md) — setting up DataManager for remote data
- [Virtual Scroll](selection-and-features.md#virtual-scrolling) — combine with filtering for large datasets
- [Templates](templates.md) — customize the no-records display when filter has no results
