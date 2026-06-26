# Disabled Items – Syncfusion React AutoComplete

The AutoComplete supports disabling individual items so they appear in the list but cannot be selected, as well as disabling the entire component.

---

## Disabling Items via fields.disabled

Map a boolean column in the data source to `fields.disabled`. Items where this column is `true` will appear greyed out and be unselectable:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';

export default function App() {
  const statusData: { [key: string]: Object }[] = [
    { Status: 'Open',                 State: false },
    { Status: 'Waiting for Customer', State: false },
    { Status: 'On Hold',              State: true  },  // disabled
    { Status: 'Follow-up',            State: false },
    { Status: 'Closed',               State: true  },  // disabled
    { Status: 'Solved',               State: false },
    { Status: 'Feature Request',      State: false },
  ];

  const fields: object = { value: 'Status', disabled: 'State' };

  return (
    <AutoCompleteComponent
      id="atcelement"
      dataSource={statusData}
      fields={fields}
      placeholder="Select a status"
    />
  );
}
```

---

## Disabling Items Dynamically via disableItem Method

Use the `disableItem` method to disable a specific item at runtime. The method accepts the item value, an HTML `<li>` element reference, or an index:

```tsx
import { AutoCompleteComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

export default function App() {
  const acRef = useRef<AutoCompleteComponent>(null);

  const statusData: { [key: string]: Object }[] = [
    { Status: 'Open',         State: false },
    { Status: 'On Hold',      State: false },
    { Status: 'Closed',       State: false },
    { Status: 'Solved',       State: false },
  ];
  const fields: object = { value: 'Status' };

  function disableOnHold() {
    // Disable by value string
    acRef.current?.disableItem('On Hold');
  }

  return (
    <>
      <AutoCompleteComponent
        ref={acRef}
        id="atcelement"
        dataSource={statusData}
        fields={fields}
        placeholder="Select a status"
      />
      <button onClick={disableOnHold}>Disable "On Hold"</button>
    </>
  );
}
```

**disableItem parameter options:**

| Parameter | Type | Description |
|---|---|---|
| `item` | `string \| number \| object \| HTMLLIElement` | The value, object, index, or element of the item to disable |

> If the currently selected item is disabled dynamically, the selection is cleared automatically.

> To disable multiple items, iterate `disableItem` over an array of values.

---

## Disabling the Entire Component

Set `enabled={false}` to prevent all user interaction with the component:

```tsx
<AutoCompleteComponent
  id="atcelement"
  dataSource={statusData}
  fields={fields}
  enabled={false}
  placeholder="Select a status"
/>
```
