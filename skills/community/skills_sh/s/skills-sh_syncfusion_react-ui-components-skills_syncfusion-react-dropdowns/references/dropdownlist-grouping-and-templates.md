# Grouping & Templates

## Table of Contents
- [Grouping](#grouping)
  - [Basic Grouping](#basic-grouping)
  - [Custom Group Header Template](#custom-group-header-template)
- [Item Template](#item-template)
- [Value Template](#value-template)
- [Group Template](#group-template)
- [Header Template](#header-template)
- [Footer Template](#footer-template)
- [No-Records Template](#no-records-template)
- [Action Failure Template](#action-failure-template)
- [Gotchas](#gotchas)

---

## Grouping

### Basic Grouping

Map a `groupBy` field in the `fields` prop to categorize list items. The DropDownList renders both inline and fixed group headers — the fixed header updates as you scroll:

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const vegetableData = [
    { Vegetable: 'Cabbage',    Category: 'Leafy and Salad', Id: 'item1' },
    { Vegetable: 'Spinach',    Category: 'Leafy and Salad', Id: 'item2' },
    { Vegetable: 'Yarrow',     Category: 'Leafy and Salad', Id: 'item4' },
    { Vegetable: 'Chickpea',   Category: 'Beans',           Id: 'item6' },
    { Vegetable: 'Green bean', Category: 'Beans',           Id: 'item7' },
    { Vegetable: 'Garlic',     Category: 'Bulb and Stem',   Id: 'item9' },
    { Vegetable: 'Onion',      Category: 'Bulb and Stem',   Id: 'item11' },
  ];
  // groupBy maps the category column
  const fields = { groupBy: 'Category', text: 'Vegetable', value: 'Id' };

  return (
    <DropDownListComponent
      dataSource={vegetableData}
      fields={fields}
      placeholder="Select a vegetable"
    />
  );
}
```

### Custom Group Header Template

Use `groupTemplate` to fully customize the group header element. Works with both inline and fixed headers:

```tsx
import { DataManager, ODataV4Adaptor, Predicate, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url',
  });
  const groupPredicate = new Predicate('City', 'equal', 'london').or('City', 'equal', 'seattle');
  const query = new Query()
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(6)
    .where(groupPredicate);
  const fields = { text: 'FirstName', value: 'EmployeeID', groupBy: 'City' };

  function groupTemplate(data: any): JSX.Element {
    return <strong>{data.City}</strong>;
  }

  return (
    <DropDownListComponent
      dataSource={employeeData}
      query={query}
      fields={fields}
      groupTemplate={groupTemplate}
      sortOrder="Ascending"
      placeholder="Select an employee"
    />
  );
}
```

---

## Item Template

Customize the rendering of each list item using `itemTemplate`. The template function receives the data item and returns JSX:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url',
  });
  const query = new Query()
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(6);
  const fields = { text: 'FirstName', value: 'EmployeeID' };

  // Each item shows Name on the left, City on the right
  function itemTemplate(data: any): JSX.Element {
    return (
      <span>
        <span className="name">{data.FirstName}</span>
        <span className="city">{data.City}</span>
      </span>
    );
  }

  return (
    <DropDownListComponent
      dataSource={employeeData}
      query={query}
      fields={fields}
      itemTemplate={itemTemplate}
      sortOrder="Ascending"
      placeholder="Select an employee"
    />
  );
}
```

---

## Value Template

Customize what is shown in the input element after a selection using `valueTemplate`. Different from `itemTemplate` which controls the popup list:

```tsx
// Shows "FirstName - City" in the input after selection
function valueTemplate(data: any): JSX.Element {
  return <span>{data.FirstName} - {data.City}</span>;
}

<DropDownListComponent
  dataSource={employeeData}
  query={query}
  fields={fields}
  itemTemplate={itemTemplate}
  valueTemplate={valueTemplate}
  placeholder="Select an employee"
/>
```

> **Note:** `valueTemplate` only renders when an item is selected. `itemTemplate` controls the popup list rows.

---

## Header Template

Place a static element at the top of the popup using `headerTemplate` — useful for column labels that match your `itemTemplate` layout:

```tsx
function headerTemplate(): JSX.Element {
  return (
    <span className="head">
      <span className="name">Name</span>
      <span className="city">City</span>
    </span>
  );
}

function itemTemplate(data: any): JSX.Element {
  return (
    <span className="item">
      <span className="name">{data.FirstName}</span>
      <span className="city">{data.City}</span>
    </span>
  );
}

<DropDownListComponent
  dataSource={employeeData}
  fields={fields}
  headerTemplate={headerTemplate}
  itemTemplate={itemTemplate}
  placeholder="Select an employee"
/>
```

---

## Footer Template

Place content at the bottom of the popup — useful for item counts, CTAs, or links:

```tsx
const sportsData = ['Basketball', 'Cricket', 'Football', 'Golf'];

function footerTemplate(): JSX.Element {
  return (
    <span className="foot">
      Total items: {sportsData.length}
    </span>
  );
}

<DropDownListComponent
  dataSource={sportsData}
  footerTemplate={footerTemplate}
  placeholder="Select a game"
/>
```

---

## No-Records Template

Shown when the data source is empty or filtering returns no results:

```tsx
function noRecordsTemplate(): JSX.Element {
  return <span className="norecord">No data available</span>;
}

<DropDownListComponent
  dataSource={[]}
  noRecordsTemplate={noRecordsTemplate}
  placeholder="Select an item"
/>
```

---

## Action Failure Template

Shown when a remote data request fails:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

// Note: intentionally broken URL to demo failure template
const customerData = new DataManager({
  adaptor: new ODataV4Adaptor,
  crossDomain: true,
  url: 'url', // broken URL
});

function failureTemplate(): JSX.Element {
  return <span className="action-failure">Data fetch failed. Check your connection.</span>;
}

<DropDownListComponent
  dataSource={customerData}
  actionFailureTemplate={failureTemplate}
  placeholder="Select a customer"
/>
```

---

## Gotchas

- **Template functions in class components** must be bound: `itemTemplate={this.itemTemplate.bind(this)}`.
- **`valueTemplate` requires a selection** — it does not render on initial empty state; use `placeholder` for that.
- **`groupTemplate` vs `headerTemplate`** — `groupTemplate` styles the group dividers inside the list; `headerTemplate` adds a fixed element above the entire list.
- **CSS for templates** — templates inject raw JSX into the list item, so you must provide your own CSS classes (`.name`, `.city`, etc.) in your stylesheet.
- **Mixing `itemTemplate` + `groupTemplate`** — both can be used simultaneously; they apply to different elements.

## See Also

- [Data Binding](data-binding.md) — configure `groupBy` in the `fields` mapping
- [Accessibility, Styling & Localization](accessibility-styling-localization.md) — template CSS, localization of no-records text
