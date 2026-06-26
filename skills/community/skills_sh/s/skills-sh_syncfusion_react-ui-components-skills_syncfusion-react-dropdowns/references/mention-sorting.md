# Sorting in Syncfusion React Mention

## Overview

Use the `sortOrder` property to sort the suggestion list items before they are displayed. This applies to both local and remote data.

| Value | Description |
|-------|-------------|
| `'None'` | No sorting applied (default) |
| `'Ascending'` | Items sorted A → Z |
| `'Descending'` | Items sorted Z → A |

## Sorting the Suggestion List

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const sportData: { [key: string]: Object }[] = [
    { ID: 'game1', Game: 'Badminton' },
    { ID: 'game2', Game: 'Football' },
    { ID: 'game3', Game: 'Tennis' },
    { ID: 'game4', Game: 'Hockey' },
    { ID: 'game5', Game: 'Basketball' },
    { ID: 'game6', Game: 'Cricket' },
  ];
  const fields: Object = { text: 'Game' };

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
      <MentionComponent
        target={mentionTarget}
        dataSource={sportData}
        fields={fields}
        sortOrder="Descending"
      />
    </div>
  );
}

export default App;
```

## Combining Sort with Templates

`sortOrder` works alongside `itemTemplate` and `displayTemplate`. The data is sorted first, then templates are applied:

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={{ text: 'Name', value: 'ID' }}
  sortOrder="Ascending"
  itemTemplate={(data: any) => <span>{data.Name}</span>}
/>
```

## Gotchas

- `sortOrder` applies after filtering—items are filtered first, then sorted.
- For remote data, sorting may be handled server-side depending on the adaptor. `sortOrder` in the component applies client-side sorting on top of what the server returns.
- When using grouped data (`fields.groupBy`), items are sorted within each group.
