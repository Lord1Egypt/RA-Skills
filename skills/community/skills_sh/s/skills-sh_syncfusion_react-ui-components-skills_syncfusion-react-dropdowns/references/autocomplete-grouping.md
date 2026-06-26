# Grouping – Syncfusion React AutoComplete

The AutoComplete supports grouping list items into categories using the `groupBy` field. The group header appears both as an inline header within the list and as a fixed floating header that updates dynamically when scrolling.

---

## Basic Grouping

Map the `groupBy` field in the `fields` property to the column that defines the category:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const vegetableData: { [key: string]: Object }[] = [
    { Vegetable: 'Cabbage',    Category: 'Leafy and Salad', Id: 'item1' },
    { Vegetable: 'Spinach',    Category: 'Leafy and Salad', Id: 'item2' },
    { Vegetable: 'Wheat grass',Category: 'Leafy and Salad', Id: 'item3' },
    { Vegetable: 'Yarrow',     Category: 'Leafy and Salad', Id: 'item4' },
    { Vegetable: 'Pumpkins',   Category: 'Leafy and Salad', Id: 'item5' },
    { Vegetable: 'Chickpea',   Category: 'Beans', Id: 'item6' },
    { Vegetable: 'Green bean', Category: 'Beans', Id: 'item7' },
    { Vegetable: 'Horse gram', Category: 'Beans', Id: 'item8' },
  ];

  // groupBy maps the category column; value maps the display text
  const fields: object = { groupBy: 'Category', value: 'Vegetable' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={vegetableData}
      fields={fields}
      placeholder="Select a vegetable"
    />
  );
}
```

---

## Custom Group Header with groupTemplate

Customize the group header rendered between groups using the `groupTemplate` property:

```tsx
import { DataManager, ODataV4Adaptor, Predicate, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });

  const groupPredicate = new Predicate('City', 'equal', 'london')
    .or('City', 'equal', 'seattle');

  const query: Query = new Query()
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(6)
    .where(groupPredicate);

  const fields: object = { value: 'FirstName', groupBy: 'City' };

  // Renders a bold city name as the group header
  function groupTemplate(data: any): JSX.Element {
    return <strong>{data.City}</strong>;
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      groupTemplate={groupTemplate}
      sortOrder="Ascending"
      placeholder="Find an employee"
    />
  );
}
```

> `groupTemplate` applies to both inline and floating (fixed) group headers. The same template is used for both.

---

## Key Properties for Grouping

| Property | Description |
|---|---|
| `fields.groupBy` | Maps the data column used to categorize items |
| `groupTemplate` | JSX template for rendering the group header label |
