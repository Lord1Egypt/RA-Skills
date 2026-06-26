# Templates in Syncfusion React Mention

## Table of Contents
- [Overview](#overview)
- [Item Template](#item-template)
- [Display Template](#display-template)
- [No Records Template](#no-records-template)
- [Spinner Template](#spinner-template)
- [Group Template](#group-template)
- [Action Failure Template](#action-failure-template)

## Overview

The Mention component exposes several template props that accept a JSX-returning function or an HTML string. Templates give you full control over how suggestion list items appear, how selected values are rendered in the editor, and what users see during loading or empty states.

## Item Template

Use `itemTemplate` to customize each suggestion list item in the popup. The template function receives the data object for the current item.

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
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(10);
  const fields: Object = { text: 'FirstName', value: 'EmployeeID' };

  function itemTemplate(data: any): JSX.Element {
    return (
      <span>
        <span>{data.FirstName}</span>
        <span className="city">{data.City}</span>
      </span>
    );
  }

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
        itemTemplate={itemTemplate}
        query={query}
        sortOrder="Ascending"
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## Display Template

Use `displayTemplate` to control what text is inserted into the editor after an item is selected. This is separate from `itemTemplate`—the popup can show rich content while the inserted text stays clean.

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
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(10);
  const fields: Object = { text: 'FirstName', value: 'EmployeeID' };

  function itemTemplate(data: any): JSX.Element {
    return (
      <span>
        <span>{data.FirstName}</span>
        <span className="city">{data.City}</span>
      </span>
    );
  }

  // Inserted text = "FirstName - City"
  function displayTemplate(data: any): JSX.Element {
    return (
      <React.Fragment>
        <span>{data.FirstName} - {data.City}</span>
      </React.Fragment>
    );
  }

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
        itemTemplate={itemTemplate}
        displayTemplate={displayTemplate}
        query={query}
        sortOrder="Ascending"
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## No Records Template

Use `noRecordsTemplate` to customize the message shown when the search returns no results. Accepts an HTML string or a JSX function.

**HTML string:**
```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const dataSource: never[] = [];
  const noRecordsTemplate: string = "<span class='norecord'>NO DATA AVAILABLE</span>";

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
        noRecordsTemplate={noRecordsTemplate}
      />
    </div>
  );
}

export default App;
```

## Spinner Template

Use `spinnerTemplate` to display a custom loading indicator while remote data is being fetched.

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
    .from('Employees')
    .select(['FirstName', 'City', 'EmployeeID'])
    .take(10);
  const fields: Object = { text: 'FirstName', value: 'EmployeeID' };

  function spinnerTemplate(): JSX.Element {
    return (
      <React.Fragment>
        <div className="spinner_loader"></div>
      </React.Fragment>
    );
  }

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
        sortOrder="Ascending"
        spinnerTemplate={spinnerTemplate}
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## Group Template

Use `groupTemplate` to customize how group headers appear in the popup when items are grouped via `fields.groupBy`.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const teamData: { [key: string]: Object }[] = [
    { Name: 'Alice', Department: 'Engineering' },
    { Name: 'Bob', Department: 'Engineering' },
    { Name: 'Carol', Department: 'Design' },
    { Name: 'Dave', Department: 'Design' },
  ];
  const fields: Object = { text: 'Name', groupBy: 'Department' };

  function groupTemplate(data: any): JSX.Element {
    return (
      <strong style={{ color: '#0078d4' }}>{data.Department}</strong>
    );
  }

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
        target={mentionTarget}
        dataSource={teamData}
        fields={fields}
        groupTemplate={groupTemplate}
      />
    </div>
  );
}

export default App;
```

## Action Failure Template

Use `actionFailureTemplate` to display a message when the remote data fetch fails. Accepts an HTML string or JSX function.

Default: `'Request failed'`.

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={remoteDataSource}
  fields={fields}
  actionFailureTemplate="<span>Failed to load data. Please try again.</span>"
/>
```

## Gotchas

- Template functions receive the raw data object—ensure your field names match.
- `displayTemplate` only affects the text inserted into the editor, not the popup item appearance (use `itemTemplate` for that).
- For `noRecordsTemplate`, an HTML string like `"<span>No results</span>"` is accepted. Passing a JSX function is also valid.
- The `spinnerTemplate` only shows for remote data fetches—it has no effect with local arrays.
