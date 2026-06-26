# How-To Patterns

## Table of Contents
- [Add Items Dynamically](#add-items-dynamically)
- [Remove an Item](#remove-an-item)
- [Cascading Dropdowns](#cascading-dropdowns)
- [Multiple Cascading Dropdowns](#multiple-cascading-dropdowns)
- [Close Popup on Page Scroll](#close-popup-on-page-scroll)
- [Tooltip on List Items](#tooltip-on-list-items)
- [Icons in List Items](#icons-in-list-items)
- [Detect Value Change Source](#detect-value-change-source)
- [Clear the Selected Value](#clear-the-selected-value)
- [Limit Search Results](#limit-search-results)
- [Highlight Filtered Text](#highlight-filtered-text)
- [Remote Data Binding How-To](#remote-data-binding-how-to)

---

## Add Items Dynamically

Use the `addItem()` method on the component instance. Pass the item object and an optional index. Without an index, the item is added at the end:

```tsx
import { useRef } from 'react';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const ddlRef = useRef<DropDownListComponent>(null);
  const sportsData = [
    { Id: 'game1', Game: 'Badminton' },
    { Id: 'game2', Game: 'Football' },
    { Id: 'game3', Game: 'Tennis' },
  ];
  const fields = { text: 'Game', value: 'Id' };

  return (
    <div>
      <DropDownListComponent ref={ddlRef} dataSource={sportsData} fields={fields} placeholder="Select a game" />
      {/* Add at position 0 (first) */}
      <button onClick={() => ddlRef.current?.addItem({ Id: 'game0', Game: 'Hockey' }, 0)}>
        Add Hockey (first)
      </button>
      {/* Add at position 2 (between items) */}
      <button onClick={() => ddlRef.current?.addItem({ Id: 'game4', Game: 'Golf' }, 2)}>
        Add Golf (middle)
      </button>
      {/* Add at end (no index) */}
      <button onClick={() => ddlRef.current?.addItem({ Id: 'game5', Game: 'Cricket' })}>
        Add Cricket (last)
      </button>
    </div>
  );
}
```

---

## Remove an Item

Splice the item from the data source array or remove the DOM list item directly. After removal, handle edge cases like the removed item being currently selected:

```tsx
import { useRef } from 'react';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const ddlRef = useRef<any>(null);
  const sportsData = [
    { Id: 'game1', Game: 'Badminton' },
    { Id: 'game2', Game: 'Football' },
    { Id: 'game3', Game: 'Tennis' },
  ];
  const fields = { text: 'Game', value: 'Id' };

  function removeFirst() {
    const ddl = ddlRef.current;
    if (ddl.list) {
      // Clear selection if removing the selected item
      if (ddl.index === 0) {
        ddl.value = null;
        ddl.dataBind();
      }
      const firstLi = ddl.list.querySelectorAll('li')[0];
      if (firstLi) firstLi.remove();
      // Show no-data state if list is now empty
      if (!ddl.list.querySelectorAll('li')[0]) {
        ddl.dataSource = [];
        ddl.list.classList.add('e-nodata');
      }
    } else {
      // Popup not yet opened — splice from raw data
      sportsData.splice(0, 1);
    }
  }

  return (
    <div>
      <DropDownListComponent ref={ddlRef} dataSource={sportsData} fields={fields} placeholder="Select a game" />
      <button onClick={removeFirst}>Remove first item</button>
    </div>
  );
}
```

---

## Cascading Dropdowns

In a cascading (dependent) dropdown setup, the child dropdown's data source is filtered based on the parent's selected value. Use the `change` event of the parent and the `dataBind()` method to apply changes immediately:

```tsx
import { useRef } from 'react';
import { Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const countryRef = useRef<any>(null);
  const stateRef   = useRef<any>(null);
  const cityRef    = useRef<any>(null);

  const countryData = [
    { CountryName: 'Australia',     CountryId: '2' },
    { CountryName: 'United States', CountryId: '1' },
  ];
  const stateData = [
    { StateName: 'New York',   CountryId: '1', StateId: '101' },
    { StateName: 'Virginia',   CountryId: '1', StateId: '102' },
    { StateName: 'Tasmania',   CountryId: '2', StateId: '105' },
  ];
  const cityData = [
    { CityName: 'Albany',     StateId: '101', CityId: 201 },
    { CityName: 'Beacon',     StateId: '101', CityId: 202 },
    { CityName: 'Emporia',    StateId: '102', CityId: 206 },
    { CityName: 'Hampton',    StateId: '102', CityId: 205 },
    { CityName: 'Hobart',     StateId: '105', CityId: 213 },
    { CityName: 'Launceston', StateId: '105', CityId: 214 },
  ];

  function onCountryChange() {
    // Filter states by selected country
    stateRef.current.query = new Query().where('CountryId', 'equal', countryRef.current.value);
    stateRef.current.enabled = true;
    stateRef.current.text = null;
    stateRef.current.dataBind();
    // Reset city
    cityRef.current.text = null;
    cityRef.current.enabled = false;
    cityRef.current.dataBind();
  }

  function onStateChange() {
    // Filter cities by selected state
    cityRef.current.query = new Query().where('StateId', 'equal', stateRef.current.value);
    cityRef.current.enabled = true;
    cityRef.current.text = null;
    cityRef.current.dataBind();
  }

  return (
    <div>
      <DropDownListComponent
        ref={countryRef}
        dataSource={countryData}
        fields={{ value: 'CountryId', text: 'CountryName' }}
        placeholder="Select a country"
        change={onCountryChange}
      />
      <DropDownListComponent
        ref={stateRef}
        dataSource={stateData}
        fields={{ value: 'StateId', text: 'StateName' }}
        enabled={false}
        placeholder="Select a state"
        change={onStateChange}
      />
      <DropDownListComponent
        ref={cityRef}
        dataSource={cityData}
        fields={{ text: 'CityName', value: 'CityId' }}
        enabled={false}
        placeholder="Select a city"
      />
    </div>
  );
}
```

> **Key pattern:** Always call `dataBind()` after mutating properties on a component ref — this flushes all pending property changes to the DOM simultaneously.

---

## Multiple Cascading Dropdowns

For more than two levels (e.g., Country → State → City → District), repeat the same pattern. Each level:
1. Listens to its parent's `change` event
2. Filters its data with `new Query().where(...)`
3. Resets and enables/disables child dropdowns via `dataBind()`

The three-level Country → State → City example above already demonstrates this pattern.

---

## Close Popup on Page Scroll

Use `hidePopup()` on the component instance, triggered from a window scroll event listener:

```tsx
import { useEffect, useRef } from 'react';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const ddlRef = useRef<any>(null);
  const sportsData = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  useEffect(() => {
    const handleScroll = () => ddlRef.current?.hidePopup();
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <DropDownListComponent ref={ddlRef} dataSource={sportsData} placeholder="Select a game" />
  );
}
```

---

## Tooltip on List Items

Combine with `@syncfusion/ej2-popups` `Tooltip` to show extra info on hover:

```tsx
import { useEffect, useRef } from 'react';
import { Tooltip } from '@syncfusion/ej2-popups';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const ddlRef = useRef<any>(null);
  let tooltip: Tooltip;

  const countryData = [
    { id: '1', text: 'Australia',     content: 'National sport: Cricket' },
    { id: '2', text: 'Bhutan',        content: 'National sport: Archery' },
    { id: '3', text: 'China',         content: 'National sport: Table Tennis' },
    { id: '4', text: 'India',         content: 'National sport: Hockey' },
    { id: '5', text: 'Spain',         content: 'National sport: Football' },
  ];
  const fields = { text: 'text', value: 'id' };

  useEffect(() => {
    tooltip = new Tooltip({
      beforeRender(args: any) {
        const item = countryData.find(d => d.text === args.target.textContent);
        if (item) { tooltip.content = item.content; tooltip.dataBind(); }
      },
      content: 'Loading...',
      position: 'TopCenter',
      target: '.e-list-item',
    });
    tooltip.appendTo('body');
    return () => tooltip.destroy();
  }, []);

  function onClose() { tooltip.close(); }

  return (
    <DropDownListComponent
      ref={ddlRef}
      dataSource={countryData}
      fields={fields}
      close={onClose}
      placeholder="Select a country"
    />
  );
}
```

---

## Icons in List Items

Map a CSS class column to `fields.iconCss`. Syncfusion renders a `<span>` with that class before each list item's text:

```tsx
const sortFormatData = [
  { Class: 'asc-sort',  Type: 'Sort A to Z', Id: '1' },
  { Class: 'dsc-sort',  Type: 'Sort Z to A', Id: '2' },
  { Class: 'filter',    Type: 'Filter',      Id: '3' },
  { Class: 'clear',     Type: 'Clear',       Id: '4' },
];
const fields = { text: 'Type', iconCss: 'Class', value: 'Id' };

<DropDownListComponent dataSource={sortFormatData} fields={fields} placeholder="Select a format" />
```

Then define the icon styles in your CSS:

```css
.asc-sort::before  { content: '↑'; }
.dsc-sort::before  { content: '↓'; }
.filter::before    { content: '⊟'; }
.clear::before     { content: '✕'; }
```

---

## Detect Value Change Source

The `change` event's `isInteracted` flag tells you whether the change came from user interaction or a programmatic assignment:

```tsx
import { useRef } from 'react';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const ddlRef = useRef<any>(null);
  const sportsData = ['Badminton', 'Cricket', 'Football', 'Golf', 'Tennis'];

  function onChange(args: any) {
    if (args.isInteracted) {
      console.log('User selected:', args.value);
    } else {
      console.log('Programmatic change to:', args.value);
    }
  }

  return (
    <div>
      <DropDownListComponent
        ref={ddlRef}
        dataSource={sportsData}
        placeholder="Select a game"
        change={onChange}
      />
      <button onClick={() => { ddlRef.current.value = 'Football'; }}>
        Set Football programmatically
      </button>
    </div>
  );
}
```

---

## Clear the Selected Value

Set `value` to `null` and call `dataBind()`:

```tsx
function clearSelection() {
  ddlRef.current.value = null;
  ddlRef.current.dataBind();
}
```

Or use the built-in `showClearButton` prop for a UI clear button:

```tsx
<DropDownListComponent dataSource={sportsData} showClearButton={true} placeholder="Select" />
```

---

## Limit Search Results

In the `filtering` event, cap the number of results returned by adding a `.take()` to the query:

```tsx
function onFiltering(args: FilteringEventArgs) {
  let query = new Query().take(5); // max 5 results
  query = args.text !== ''
    ? query.where('Country', 'startswith', args.text, true)
    : query;
  args.updateData(searchData, query);
}
```

---

## Highlight Filtered Text

Use the `filtering` event to wrap matching characters in a `<strong>` tag using a `highlightSearch` utility or manual string replacement. The Syncfusion `highlightSearch` function from `@syncfusion/ej2-dropdowns` can be applied inside `itemTemplate`:

```tsx
import { highlightSearch } from '@syncfusion/ej2-dropdowns';

function itemTemplate(data: any): JSX.Element {
  // highlightSearch highlights matched text characters in the item
  return (
    <span dangerouslySetInnerHTML={{
      __html: highlightSearch(data.Country, filterText, true, 'StartsWith')
    }} />
  );
}
```

> Store the current filter text in a ref or state variable and update it inside the `filtering` event handler.

---

## Remote Data Binding How-To

For a complete remote binding example with error handling and loading state:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const customerData = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url',
  });
  const query = new Query()
    .from('Customers')
    .select(['ContactName', 'CustomerID'])
    .take(10);
  const fields = { text: 'ContactName', value: 'CustomerID' };

  function onActionBegin() { /* Show loading indicator */ }
  function onActionComplete() { /* Hide loading indicator */ }

  function failureTemplate(): JSX.Element {
    return <span>Failed to load customers. Check your network.</span>;
  }

  return (
    <DropDownListComponent
      dataSource={customerData}
      query={query}
      fields={fields}
      actionBegin={onActionBegin}
      actionComplete={onActionComplete}
      actionFailureTemplate={failureTemplate}
      placeholder="Select a customer"
    />
  );
}
```

## See Also

- [Data Binding](data-binding.md) — foundational data binding patterns
- [Filtering](filtering.md) — search and filter configuration
- [Features & Configuration](features-and-configuration.md) — virtual scroll, resize, RTL
