# Filtering

## Table of Contents
- [Overview](#overview)
- [Basic Filtering](#basic-filtering)
- [Preventing Default Filtering](#preventing-default-filtering)
- [Filter Types](#filter-types)
- [Case-Sensitive Filtering](#case-sensitive-filtering)
- [Filtering by Multiple Fields](#filtering-by-multiple-fields)
- [Remote Filtering with Minimum Characters](#remote-filtering-with-minimum-characters)
- [Diacritics Filtering](#diacritics-filtering)
- [Debounce Delay](#debounce-delay)
- [Virtual Scroll + Filtering](#virtual-scroll--filtering)
- [Gotchas](#gotchas)

---

## Overview

Enable `allowFiltering` to show a search box in the popup. As the user types, the `filtering` event fires — handle it to filter your data and call `args.updateData()` to return results.

> **Critical rule:** Whenever you supply a custom `filtering` handler, you **must** set `args.preventDefaultAction = true` at the start of the handler. Without it, the component runs its own built-in filtering logic **on top of** your custom logic, causing duplicate or incorrect results.

---

## Basic Filtering

```tsx
import { DropDownListComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';

export default function App() {
  const searchData = [
    { Index: 's1', Country: 'Alaska' },
    { Index: 's2', Country: 'California' },
    { Index: 's3', Country: 'Florida' },
    { Index: 's4', Country: 'Georgia' },
  ];
  const fields = { text: 'Country', value: 'Index' };

  function onFiltering(args: FilteringEventArgs) {
    // Always prevent the built-in default filtering when using a custom handler
    args.preventDefaultAction = true;
    let query = new Query();
    // 'startswith' filter — pass true for case-insensitive (4th param)
    query = args.text !== ''
      ? query.where('Country', 'startswith', args.text, true)
      : query;
    args.updateData(searchData, query);
  }

  return (
    <DropDownListComponent
      dataSource={searchData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      popupHeight="250px"
      placeholder="Select a country"
    />
  );
}
```

---

## Preventing Default Filtering

When you implement a custom `filtering` handler, the component's built-in filtering still runs unless you explicitly stop it. This double-filtering causes items to be filtered twice — first by your logic, then by the internal engine — resulting in unexpected empty lists or wrong matches.

**Always set `args.preventDefaultAction = true` as the very first line of any custom `filtering` handler.**

```tsx
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;   // ← required for all custom handlers
  // ... your filtering logic ...
  args.updateData(myData, myQuery);
}
```

| Scenario | `preventDefaultAction` needed? |
|---|---|
| Built-in filtering only (no handler) | ❌ Not needed — no handler at all |
| Custom handler with `updateData` on local data | ✅ **Always** |
| Custom handler with `updateData` on remote `DataManager` | ✅ **Always** |
| Early-return guard (minimum characters) | ✅ **Always** (set it before the guard) |

```tsx
// ✅ Correct pattern — prevent default BEFORE any early return
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  if (args.text.length < 2) {
    args.updateData(allData); // show full list until 2 chars typed
    return;
  }
  const query = new Query().where('Name', 'startswith', args.text, true);
  args.updateData(allData, query);
}

// ❌ Incorrect — preventDefaultAction set after early return; default runs for short text
function onFilteringWrong(args: FilteringEventArgs) {
  if (args.text.length < 2) return;
  args.preventDefaultAction = true;
  const query = new Query().where('Name', 'startswith', args.text, true);
  args.updateData(allData, query);
}
```

---

## Filter Types

Choose the filter operator in the `query.where()` call:

| Operator | Behavior |
|---|---|
| `'startswith'` | Matches items that begin with the typed text |
| `'contains'` | Matches items that contain the typed text anywhere |
| `'endsWith'` | Matches items that end with the typed text |

```tsx
// Contains filter
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  let query = new Query();
  query = args.text !== ''
    ? query.where('Country', 'contains', args.text, true)  // case-insensitive
    : query;
  args.updateData(searchData, query);
}

// EndsWith filter
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  let query = new Query();
  query = args.text !== ''
    ? query.where('Country', 'endsWith', args.text, true)
    : query;
  args.updateData(searchData, query);
}
```

---

## Case-Sensitive Filtering

The 4th parameter of `query.where()` controls case sensitivity:
- `true` → case-insensitive (default recommendation)
- `false` → case-sensitive (user must type exact casing)

```tsx
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  let query = new Query();
  query = args.text !== ''
    ? query.where('Country', 'contains', args.text, false)  // case-SENSITIVE
    : query;
  args.updateData(searchData, query);
}
```

---

## Filtering by Multiple Fields

By default the DropDownList filters only the mapped `text` field. Use `Predicate` from `@syncfusion/ej2-data` to match the typed text against **both** the `text` and `value` fields (or any combination of fields) simultaneously.

### Filter by Text and Value Fields

```tsx
import { DropDownListComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query, Predicate } from '@syncfusion/ej2-data';

export default function App() {
  const countryData = [
    { Name: 'Australia', Code: 'AU' },
    { Name: 'Bermuda',   Code: 'BM' },
    { Name: 'Canada',    Code: 'CA' },
    { Name: 'Cameroon',  Code: 'CM' },
    { Name: 'Denmark',   Code: 'DK' },
    { Name: 'France',    Code: 'FR' },
  ];
  const fields = { text: 'Name', value: 'Code' };

  function onFiltering(args: FilteringEventArgs) {
    args.preventDefaultAction = true;
    if (args.text === '') {
      args.updateData(countryData);
      return;
    }
    // Build a Predicate that matches the typed text against BOTH Name and Code
    const predicate = new Predicate('Name', 'contains', args.text, true)
      .or('Code', 'contains', args.text, true);
    const query = new Query().where(predicate);
    args.updateData(countryData, query);
  }

  return (
    <DropDownListComponent
      dataSource={countryData}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      placeholder="Search by name or code (e.g. 'CA' or 'Canada')"
    />
  );
}
```

**How it works:**
- `new Predicate('Name', 'contains', args.text, true)` matches items whose `Name` contains the typed text (case-insensitive).
- `.or('Code', 'contains', args.text, true)` extends the predicate to also match items whose `Code` contains the typed text.
- Typing `"ca"` returns both `Canada` (name match) and `Cameroon` (name match) **and** `CA` (code match).

### Filter Across Three or More Fields

Chain additional `.or()` calls for each extra field:

```tsx
function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  if (args.text === '') {
    args.updateData(employeeData);
    return;
  }
  const predicate = new Predicate('FirstName', 'contains', args.text, true)
    .or('LastName',  'contains', args.text, true)
    .or('EmployeeID', 'contains', args.text, true);
  args.updateData(employeeData, new Query().where(predicate));
}
```

### Using `startswith` Instead of `contains`

Swap the operator in each `Predicate` call:

```tsx
const predicate = new Predicate('Name', 'startswith', args.text, true)
  .or('Code', 'startswith', args.text, true);
```

### Remote Data with Multiple-Field Predicate

The same `Predicate` approach works with a remote `DataManager` — the predicate is serialised into the outgoing query:

```tsx
import { DataManager, ODataV4Adaptor, Query, Predicate } from '@syncfusion/ej2-data';

const remoteData = new DataManager({
  url: 'url',
  adaptor: new ODataV4Adaptor,
  crossDomain: true,
});
const fields = { text: 'ContactName', value: 'CustomerID' };

function onFiltering(args: FilteringEventArgs) {
  args.preventDefaultAction = true;
  if (args.text === '') {
    args.updateData(remoteData);
    return;
  }
  const predicate = new Predicate('ContactName', 'startswith', args.text, true)
    .or('CustomerID', 'startswith', args.text, true);
  const query = new Query()
    .select(['ContactName', 'CustomerID'])
    .where(predicate)
    .take(10);
  args.updateData(remoteData, query);
}
```

> **Note:** When filtering remote data across multiple fields, ensure the server supports the generated OData `$filter` expression with `or` conditions. Some APIs may need custom adaptors.

---

## Remote Filtering with Minimum Characters

For remote data sources, avoid firing a server request on every keystroke. Return early until the user has typed at least N characters:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const searchData = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url',
  });
  const fields = { text: 'ContactName', value: 'CustomerID' };
  const query = new Query().select(['ContactName', 'CustomerID']).take(7);

  function onFiltering(e: FilteringEventArgs) {
    e.preventDefaultAction = true;
    if (e.text === '') {
      // Show full list when search is cleared
      e.updateData(searchData);
    } else {
      // Only filter after 3 characters to limit requests
      if (e.text.length < 3) return;
      let q = new Query().select(['ContactName', 'CustomerID']);
      q = q.where('ContactName', 'startswith', e.text, true);
      e.updateData(searchData, q);
    }
  }

  return (
    <DropDownListComponent
      dataSource={searchData}
      query={query}
      fields={fields}
      allowFiltering={true}
      filtering={onFiltering}
      sortOrder="Ascending"
      popupHeight="250px"
      placeholder="Select a customer"
    />
  );
}
```

---

## Diacritics Filtering

Enable `ignoreAccent` to ignore accent characters (é, ñ, ü, etc.) when filtering international data:

```tsx
const diacriticsData = [
  'Aeróbics',
  'Aeróbics en Agua',
  'Aerografía',
  'Aeromodelaje',
  'Águilas',
  'Ajedrez',
];

<DropDownListComponent
  dataSource={diacriticsData}
  allowFiltering={true}
  ignoreAccent={true}
  filterBarPlaceholder="e.g: aero"
  placeholder="Select a value"
/>
```

With `ignoreAccent={true}`, typing "aero" matches "Aeróbics", "Aerografía", etc.

---

## Debounce Delay

Control the delay (in ms) before filtering fires after each keystroke. Default is 300ms. Set to `0` to disable debouncing:

```tsx
<DropDownListComponent
  dataSource={sportsData}
  allowFiltering={true}
  debounceDelay={300}
  placeholder="Select a game"
/>
```

Increase `debounceDelay` for remote sources to reduce server load.

---

## Virtual Scroll + Filtering

When `enableVirtualization` is active, `allowFiltering` still works. The component filters the virtualized data on the client side (for local data) or sends filtered requests to the server (for remote data):

```tsx
import { DropDownListComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

<DropDownListComponent
  dataSource={records}
  fields={fields}
  enableVirtualization={true}
  allowFiltering={true}
  popupHeight="200px"
  placeholder="e.g. Item 1"
>
  <Inject services={[VirtualScroll]} />
</DropDownListComponent>
```

---

## Gotchas

- **`args.preventDefaultAction = true` is mandatory in every custom handler** — without it, the component's built-in filtering runs on top of your custom logic, causing double-filtering, empty lists, or wrong results. Set it as the very first statement.
- **Set `preventDefaultAction` before any early return** — if you guard with a minimum-character check, `preventDefaultAction` must come before the guard so the default filter is suppressed even when you return early.
- **Always call `args.updateData()`** — even when `args.text === ''` (pass original data to reset). Failing to call it leaves the list empty.
- **`filtering` event vs `allowFiltering` prop** — you need both: `allowFiltering={true}` shows the search box; the `filtering` event handles the actual filtering logic.
- **Multi-field filtering requires `Predicate`** — chaining `.where()` calls replaces the previous condition; use `Predicate` with `.or()` / `.and()` to combine conditions across fields.
- **Class components** — must `.bind(this)` in the filtering prop: `filtering={this.onFiltering.bind(this)}`.
- **Remote data minimum characters** — without a `minLength` guard, every keystroke fires a server request, which can be very slow.
- **`debounceDelay={0}`** disables the built-in delay entirely; only do this for local data.

## See Also

- [Data Binding](data-binding.md) — configure the data source
- [How-To: Highlight Filtering](how-to.md#highlight-filtered-text) — highlight matched characters
- [How-To: Limit Search Results](how-to.md#limit-search-results) — cap the number of results returned
