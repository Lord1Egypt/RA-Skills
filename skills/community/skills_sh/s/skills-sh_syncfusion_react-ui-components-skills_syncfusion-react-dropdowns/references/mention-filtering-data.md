# Filtering Data in Syncfusion React Mention

## Table of Contents
- [Overview](#overview)
- [Minimum Filter Character Length](#minimum-filter-character-length)
- [Filter Type](#filter-type)
- [Allow Spaces in Search](#allow-spaces-in-search)
- [Customize Suggestion Count](#customize-suggestion-count)
- [Debounce Delay](#debounce-delay)
- [Custom Filtering with the filtering Event](#custom-filtering-with-the-filtering-event)

## Overview

The Mention component filters suggestion list items as the user types after the trigger character. All filtering runs automatically—configure it through props.

## Minimum Filter Character Length

Use `minLength` to control how many characters the user must type before the popup appears. Useful for large remote datasets to reduce unnecessary network requests.

Default: `0` (popup opens as soon as the trigger character is typed).

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const searchData: DataManager = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });
  const dataFields: Object = { text: 'ContactName', value: 'CustomerID' };
  const query: Query = new Query().select(['ContactName', 'CustomerID']).take(7);

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
      {/* Popup opens only after 3 characters are typed */}
      <MentionComponent
        dataSource={searchData}
        target={mentionTarget}
        fields={dataFields}
        query={query}
        minLength={3}
      />
    </div>
  );
}

export default App;
```

## Filter Type

The `filterType` property determines how typed characters are matched against list items:

| Value | Description |
|-------|-------------|
| `'Contains'` | Items containing the typed text (default) |
| `'StartsWith'` | Items beginning with the typed text |
| `'EndsWith'` | Items ending with the typed text |

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const searchData: DataManager = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });
  const query: Query = new Query().select(['ContactName', 'CustomerID']).take(7);
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
        target={mentionTarget}
        dataSource={searchData}
        query={query}
        fields={fields}
        filterType="EndsWith"
      />
    </div>
  );
}

export default App;
```

## Allow Spaces in Search

By default, pressing space while searching closes the popup if the text does not match. Set `allowSpaces={true}` to keep the popup open and search with spaces included—useful for full-name matching.

Default: `false`.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Name: 'Andrew Fuller', ID: '1' },
    { Name: 'Anne Dodsworth', ID: '2' },
    { Name: 'Janet Leverling', ID: '3' },
    { Name: 'Laura Callahan', ID: '4' },
    { Name: 'Margaret Peacock', ID: '5' },
  ];
  const fields: Object = { text: 'Name' };

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
      {/* User can type "@Andrew Fuller" without closing popup */}
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
        allowSpaces={true}
      />
    </div>
  );
}

export default App;
```

## Customize Suggestion Count

Use `suggestionCount` to control the maximum number of items shown in the popup at once. Default: `25`.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const emailData: { [key: string]: Object }[] = [
    { Name: 'Selma Rose', EmailId: 'selma@gmail.com' },
    { Name: 'Maria', EmailId: 'maria@gmail.com' },
    { Name: 'Russo Kay', EmailId: 'russo@gmail.com' },
    { Name: 'Robert', EmailId: 'robert@gmail.com' },
    { Name: 'Camden Kate', EmailId: 'camden@gmail.com' },
    { Name: 'Garth', EmailId: 'garth@gmail.com' },
    { Name: 'Andrew James', EmailId: 'james@gmail.com' },
    { Name: 'Olivia', EmailId: 'olivia@gmail.com' },
    { Name: 'Sophia', EmailId: 'sophia@gmail.com' },
    { Name: 'Margaret', EmailId: 'margaret@gmail.com' },
  ];
  const fields: Object = { text: 'Name' };

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
      {/* Show at most 8 suggestions */}
      <MentionComponent
        target={mentionTarget}
        dataSource={emailData}
        fields={fields}
        suggestionCount={8}
      />
    </div>
  );
}

export default App;
```

## Debounce Delay

Use `debounceDelay` to set the delay (in milliseconds) before a filter operation runs after the user types. Useful for remote data to avoid firing too many requests.

Default: `300` ms.

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={remoteDataSource}
  fields={fields}
  debounceDelay={500}
/>
```

## Custom Filtering with the filtering Event

The `filtering` event fires on each keystroke during search. Use it to apply custom logic or queries:

```tsx
import { MentionComponent, FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Name: 'Andrew Fuller', ID: '1' },
    { Name: 'Anne Dodsworth', ID: '2' },
    { Name: 'Janet Leverling', ID: '3' },
  ];
  const fields: Object = { text: 'Name' };

  function onFiltering(args: FilteringEventArgs): void {
    // Custom query example: only show items where Name starts with typed text
    let query: Query = new Query();
    query = args.text !== '' ? query.where('Name', 'startswith', args.text, true) : query;
    args.updateData(userData, query);
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
        dataSource={userData}
        fields={fields}
        filtering={onFiltering}
      />
    </div>
  );
}

export default App;
```

## Gotchas

- When `minLength` is set, the popup only opens after the required number of characters are typed. Setting it to `0` opens the popup immediately on the trigger character.
- `allowSpaces` only keeps the popup open during search—it doesn't prevent space from closing the popup after a selection.
- `suggestionCount` limits the displayed list, not the underlying filtered set. The data source may have more matches than shown.
- For remote data, increasing `debounceDelay` reduces API calls when the user types quickly.
