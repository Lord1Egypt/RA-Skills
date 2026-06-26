# Working with Data in Syncfusion React Mention

## Table of Contents
- [Overview](#overview)
- [Field Mappings](#field-mappings)
- [Array of Simple Data](#array-of-simple-data)
- [Array of JSON Data](#array-of-json-data)
- [Array of Complex (Nested) Data](#array-of-complex-nested-data)
- [Remote Data – OData V4](#remote-data--odata-v4)
- [Remote Data – Web API](#remote-data--web-api)
- [Grouped Data](#grouped-data)

## Overview

The Mention loads data through the `dataSource` property. It accepts:
- Arrays of strings, numbers, or booleans (primitive)
- Arrays of JSON objects
- A `DataManager` instance for remote/service-based data

Use the `fields` property to map your data object's properties to the component's `text`, `value`, `groupBy`, and `iconCss` fields.

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | Display text for each list item |
| `value` | `number \| string` | Hidden unique value for each item |
| `groupBy` | `string` | Category to group list items |
| `iconCss` | `string` | CSS class for icon per item |

> When binding complex data, map `fields` correctly—otherwise the selected item will be `undefined`.

## Array of Simple Data

For primitive arrays (strings, numbers), both `text` and `value` represent the same data. No `fields` mapping is required.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: string[] = ['Selma Rose', 'Garth', 'Robert', 'William', 'Joseph'];

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent target={mentionTarget} dataSource={userData} />
    </div>
  );
}

export default App;
```

## Array of JSON Data

Map object properties to `text` and `value` using the `fields` prop:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const sportsData: { [key: string]: Object }[] = [
    { ID: 'game1', Game: 'Badminton' },
    { ID: 'game2', Game: 'Football' },
    { ID: 'game3', Game: 'Tennis' },
    { ID: 'game4', Game: 'Hockey' },
    { ID: 'game5', Game: 'Basketball' },
  ];
  const fields: Object = { text: 'Game', value: 'ID' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag sport"></div>
          </td>
        </tr>
      </table>
      <MentionComponent target={mentionTarget} dataSource={sportsData} fields={fields} />
    </div>
  );
}

export default App;
```

## Array of Complex (Nested) Data

For nested objects, use dot notation in field names:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const countriesData: { [key: string]: Object }[] = [
    { Country: { Name: 'Australia' }, Code: { ID: 'AU' } },
    { Country: { Name: 'Bermuda' }, Code: { ID: 'BM' } },
    { Country: { Name: 'Canada' }, Code: { ID: 'CA' } },
    { Country: { Name: 'Cameroon' }, Code: { ID: 'CM' } },
    { Country: { Name: 'Denmark' }, Code: { ID: 'DK' } },
    { Country: { Name: 'France' }, Code: { ID: 'FR' } },
  ];
  // Dot notation maps nested properties
  const fields: Object = { text: 'Country.Name', value: 'Code.ID' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag country"></div>
          </td>
        </tr>
      </table>
      <MentionComponent target={mentionTarget} dataSource={countriesData} fields={fields} />
    </div>
  );
}

export default App;
```

## Remote Data – OData V4

Use `DataManager` with `ODataV4Adaptor` to bind an OData v4 service. The `query` property lets you select specific columns and limit records:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const dataSource: DataManager = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });
  const query: Query = new Query()
    .from('Customers')
    .select(['ContactName', 'CustomerID'])
    .take(6);
  const fields: Object = { text: 'ContactName', value: 'CustomerID' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        dataSource={dataSource}
        target={mentionTarget}
        fields={fields}
        query={query}
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## Remote Data – Web API

Use `WebApiAdaptor` for REST APIs:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, WebApiAdaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const dataSource: DataManager = new DataManager({
    url: 'url',
    adaptor: new WebApiAdaptor(),
    crossDomain: true,
  });
  const query: Query = new Query()
    .select(['FirstName', 'EmployeeID'])
    .take(7)
    .requiresCount();
  const fields: Object = { text: 'FirstName', value: 'EmployeeID' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        dataSource={dataSource}
        target={mentionTarget}
        fields={fields}
        query={query}
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## Grouped Data

Use the `groupBy` field to group suggestion items under category headers:

```tsx
const teamData: { [key: string]: Object }[] = [
  { Name: 'Alice', Department: 'Engineering' },
  { Name: 'Bob', Department: 'Engineering' },
  { Name: 'Carol', Department: 'Design' },
  { Name: 'Dave', Department: 'Design' },
];
const fields: Object = { text: 'Name', groupBy: 'Department' };

<MentionComponent target={mentionTarget} dataSource={teamData} fields={fields} />
```

## Gotchas

- Always set `fields` when binding JSON data; without it, the component cannot determine which property to display.
- For remote data, use `popupWidth` to prevent the popup from being too narrow for longer text values.
- `query.requiresCount()` is needed for Web API adaptor to handle server-side paging correctly.
- Use `actionFailureTemplate` to show a user-friendly message when the remote request fails.
