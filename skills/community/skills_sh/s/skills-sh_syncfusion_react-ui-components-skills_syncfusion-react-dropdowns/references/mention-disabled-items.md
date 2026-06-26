# Disabled Items in Syncfusion React Mention

## Overview

The Mention component supports disabling individual items so they appear in the list but cannot be selected. Disabled items are visually indicated (greyed out) and ignored during keyboard navigation.

There are two ways to disable items:
1. **Via data**: Set a `disabled` field in your data and map it through `fields.disabled`
2. **Via method**: Call `disableItem()` programmatically at runtime

## Disabling Items via Data (fields.disabled)

Map a boolean field in your data to `fields.disabled`. Items with `true` for that field will be non-selectable:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const statusData = [
    { Status: 'Open', State: false },
    { Status: 'Waiting for Customer', State: false },
    { Status: 'On Hold', State: true },        // disabled
    { Status: 'Follow-up', State: false },
    { Status: 'Closed', State: true },           // disabled
    { Status: 'Solved', State: false },
    { Status: 'Feature Request', State: false },
  ];
  // Map 'State' boolean field to the disabled behavior
  const fields = { value: 'Status', disabled: 'State' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag status"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={statusData}
        fields={fields}
      />
    </div>
  );
}

export default App;
```

## Disabling Items Programmatically (disableItem)

Use the `disableItem()` method to disable items dynamically after the component is rendered. Access the component via a ref.

`disableItem` accepts one of:
- An `HTMLLIElement` (the list item element)
- A string, number, or boolean matching the item's value
- An object matching the data item
- An index number

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData = [
    { Name: 'Alice', ID: '1' },
    { Name: 'Bob', ID: '2' },
    { Name: 'Carol', ID: '3' },
  ];
  const fields = { text: 'Name', value: 'ID' };
  const mentionRef = React.useRef<MentionComponent>(null);

  function handleDisable() {
    if (mentionRef.current) {
      // Disable by value string
      mentionRef.current.disableItem('2');
    }
  }

  return (
    <div>
      <button onClick={handleDisable}>Disable Bob</button>
      <table>
        <tr>
          <td>
            <label>Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        ref={mentionRef}
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
      />
    </div>
  );
}

export default App;
```

### disableItem Method Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `item` | `string \| number \| boolean \| object \| HTMLLIElement` | The item to disable—by value, index, or element |

> `disableItem` disables one item at a time. To disable multiple items, call it in a loop.

## Gotchas

- Disabled items are still visible in the suggestion list but cannot be selected with mouse, touch, or keyboard.
- When items are disabled using `disableItem()`, the disabled state is also reflected back in the `dataSource`.
- The `fields.disabled` approach is preferred for initial state; `disableItem()` is better for dynamic/runtime changes.
