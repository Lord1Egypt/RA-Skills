# Templates – Syncfusion React AutoComplete

## Table of Contents
- [Item Template](#item-template)
- [Group Template](#group-template)
- [Header Template](#header-template)
- [Footer Template](#footer-template)
- [No Records Template](#no-records-template)
- [Action Failure Template](#action-failure-template)

---

## Item Template

Customize the rendering of each suggestion list item using `itemTemplate`. Receives the data item as a parameter:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });
  const query: Query = new Query()
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(6);
  const fields: object = { value: 'FirstName' };

  // Two-column layout: name + city
  function itemTemplate(data: any): JSX.Element {
    return (
      <span>
        <span className="name">{data.FirstName}</span>
        <span className="city">{data.City}</span>
      </span>
    );
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      itemTemplate={itemTemplate}
      sortOrder="Ascending"
      placeholder="Find an employee"
    />
  );
}
```

---

## Group Template

Customize the group header title rendered above grouped items using `groupTemplate`. Applies to both inline and floating headers:

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

---

## Header Template

Place a static custom element at the top of the popup list using `headerTemplate`. Useful for column labels:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const employeeData: DataManager = new DataManager({
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
    url: 'url'
  });
  const query: Query = new Query()
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(6);
  const fields: object = { value: 'FirstName' };

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

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={employeeData}
      query={query}
      fields={fields}
      headerTemplate={headerTemplate}
      itemTemplate={itemTemplate}
      sortOrder="Ascending"
      placeholder="Find an employee"
    />
  );
}
```

---

## Footer Template

Place a static custom element at the bottom of the popup list using `footerTemplate`. Useful for showing item counts:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

export default function App() {
  const sportsData: string[] = [
    'Badminton', 'Basketball', 'Cricket', 'Football',
    'Golf', 'Gymnastics', 'Hockey', 'Rugby', 'Snooker', 'Tennis'
  ];
  let atcObject: any;

  function onOpen(): void {
    const count = atcObject.getItems().length;
    const ele = document.getElementsByClassName('foot')[0] as HTMLElement;
    if (ele) ele.innerHTML = `Total list items: ${count}`;
  }

  function footerTemplate(): JSX.Element {
    return <span className="foot" />;
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      ref={(ac) => { atcObject = ac; }}
      dataSource={sportsData}
      footerTemplate={footerTemplate}
      open={onOpen}
      placeholder="Find a game"
    />
  );
}
```

---

## No Records Template

Show a custom message when no matching items are found using `noRecordsTemplate`:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const data: { [key: string]: Object }[] = [];

  function noRecordsTemplate(): JSX.Element {
    return <span className="norecord">No data available</span>;
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={data}
      noRecordsTemplate={noRecordsTemplate}
      placeholder="Find an item"
    />
  );
}
```

---

## Action Failure Template

Show a custom message when a remote data fetch request fails using `actionFailureTemplate`:

```tsx
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  // Intentionally broken URL to demonstrate failure template
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

  function actionFailureTemplate(): JSX.Element {
    return <span className="action-failure">Data fetch failed</span>;
  }

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={customerData}
      query={query}
      fields={fields}
      actionFailureTemplate={actionFailureTemplate}
      placeholder="Find a customer"
    />
  );
}
```

---

## Template Property Summary

| Property | Type | Description |
|---|---|---|
| `itemTemplate` | `string \| Function` | Template for each suggestion list item |
| `groupTemplate` | `string \| Function` | Template for group header labels |
| `headerTemplate` | `string \| Function` | Template for the static popup header |
| `footerTemplate` | `string \| Function` | Template for the static popup footer |
| `noRecordsTemplate` | `string \| Function` | Template shown when no records are found |
| `actionFailureTemplate` | `string \| Function` | Template shown when remote data fetch fails |
