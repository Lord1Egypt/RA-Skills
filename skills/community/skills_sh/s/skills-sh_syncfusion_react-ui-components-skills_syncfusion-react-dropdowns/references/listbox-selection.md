# Selection in React ListBox

## Table of Contents
- [Single Selection](#single-selection)
- [Multiple Selection](#multiple-selection)
- [Checkbox Selection](#checkbox-selection)
- [Selection Events](#selection-events)
- [Programmatic Selection](#programmatic-selection)
- [Getting Selected Items](#getting-selected-items)
- [Disabling Items](#disabling-items)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Single Selection

Single selection allows users to select one item at a time. This is the default mode.

### Enable Single Selection Mode

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      selectionSettings={{ mode: 'Single' }}
    />
  );
}

export default App;
```

### Single Selection with Default Item

Pre-select an item when component loads:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' }
  ];

  const handleSelect = () => {
    // Pre-select item with id '2'
    listBoxRef.current.value = '2';
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Single' }}
      />
      <button onClick={handleSelect}>Select TypeScript</button>
    </div>
  );
}

export default App;
```

---

## Multiple Selection

Multiple selection allows users to select multiple items using Ctrl+Click or Shift+Click.

### Enable Multiple Selection Mode

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'TypeScript', id: '4' },
    { text: 'React', id: '5' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      selectionSettings={{ mode: 'Multiple' }}
    />
  );
}

export default App;
```

### Multiple Selection with Pre-selected Items

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'TypeScript', id: '4' },
    { text: 'React', id: '5' }
  ];

  const handlePreSelect = () => {
    // Pre-select multiple items
    listBoxRef.current.value = ['2', '4', '5'];
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      <button onClick={handlePreSelect}>Select CSS, TS, React</button>
    </div>
  );
}

export default App;
```

---

## Checkbox Selection

Checkbox selection renders a checkbox alongside each list item. **You must inject the `CheckBoxSelection` service** when `showCheckbox` is enabled, otherwise checkboxes will not appear.

### Basic Checkbox Selection

```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' },
    { text: 'Vue', id: '4' }
  ];

  const selectionSettings: SelectionSettingsModel = { showCheckbox: true };

  return (
    <ListBoxComponent dataSource={data} fields={{ text: 'text', value: 'id' }} selectionSettings={selectionSettings}>
      <Inject services={[CheckBoxSelection]} />
    </ListBoxComponent>
  );
}

export default App;
```

### Checkbox Selection with "Select All"

Enable a "Select All" checkbox at the top of the list:

```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'HTML', id: '1' },
    { text: 'CSS', id: '2' },
    { text: 'JavaScript', id: '3' },
    { text: 'TypeScript', id: '4' },
    { text: 'React', id: '5' }
  ];

  const selectionSettings: SelectionSettingsModel = {
    showCheckbox: true,
    showSelectAll: true
  };

  return (
    <ListBoxComponent dataSource={data} fields={{ text: 'text', value: 'id' }} selectionSettings={selectionSettings}>
      <Inject services={[CheckBoxSelection]} />
    </ListBoxComponent>
  );
}

export default App;
```

### Checkbox Selection with Change Event

Capture selected values when checkboxes are toggled:

```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [selectedItems, setSelectedItems] = useState<string[]>([]);

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' }
  ];

  const selectionSettings: SelectionSettingsModel = { showCheckbox: true };

  const handleChange = (e) => {
    setSelectedItems(e.value);
  };

  return (
    <div>
      <ListBoxComponent
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={selectionSettings}
        change={handleChange}
      >
        <Inject services={[CheckBoxSelection]} />
      </ListBoxComponent>
      <p>Selected: {selectedItems.join(', ')}</p>
    </div>
  );
}

export default App;
```

### Checkbox Position

Control whether the checkbox appears on the left (default) or right side:

```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Option A', id: '1' },
    { text: 'Option B', id: '2' },
    { text: 'Option C', id: '3' }
  ];

  const selectionSettings: SelectionSettingsModel = {
    showCheckbox: true,
    checkboxPosition: 'Right'
  };

  return (
    <ListBoxComponent dataSource={data} fields={{ text: 'text', value: 'id' }} selectionSettings={selectionSettings}>
      <Inject services={[CheckBoxSelection]} />
    </ListBoxComponent>
  );
}

export default App;
```

> **Important:** Always import and inject `CheckBoxSelection` from `@syncfusion/ej2-react-dropdowns` when using `showCheckbox: true`. Without the injection, checkboxes will not render.

---

## Selection Events

### Change Event - Fires When Selection Changes

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' }
  ];

  const handleChange = (e) => {
    console.log('Value:', e.value);      // Selected item value(s)
    console.log('Items:', e.items);      // Selected item object(s)
    console.log('Elements:', e.elements); // Selected list elements
    console.log('Event:', e.event);      // Native event
  };

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      change={handleChange}
    />
  );
}

export default App;
```

### Multiple Selection Change Event

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const [selectedItems, setSelectedItems] = useState([]);

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' },
    { text: 'React', id: '3' }
  ];

  const handleChange = (e) => {
    // e.value is an array for multiple selections
    console.log('Selected Values:', e.value);
    console.log('Selected Items:', e.items);
    setSelectedItems(e.value);
  };

  return (
    <div>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
        change={handleChange}
      />
      <p>Selected: {selectedItems.join(', ')}</p>
    </div>
  );
}

export default App;
```

---

## Programmatic Selection

### Setting Selection from Code

Use refs to access the ListBox and set selections programmatically:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'Option A', id: '1' },
    { text: 'Option B', id: '2' },
    { text: 'Option C', id: '3' },
    { text: 'Option D', id: '4' }
  ];

  const selectById = (id) => {
    // Find the text for the given id and select by text
    const item = data.find(d => d.id === id);
    if (item) {
      listBoxRef.current.selectItems([item.text], true);
    }
  };

  const clearSelection = () => {
    listBoxRef.current.selectItems(
      data.map(item => item.text),
      false
    );
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      
      <div>
        <button onClick={() => selectById('2')}>Select Option B</button>
        <button onClick={clearSelection}>Clear</button>
      </div>
    </div>
  );
}

export default App;
```

### Multiple Items Programmatically

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' },
    { text: 'Item 4', id: '4' }
  ];

  const selectMultiple = (ids) => {
    // Set array of IDs for multiple selection
    listBoxRef.current.value = ids;
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      
      <button onClick={() => selectMultiple(['1', '3'])}>
        Select Items 1 & 3
      </button>
    </div>
  );
}

export default App;
```

---

## Getting Selected Items

### Access Selected Item Data

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'JavaScript', id: '1', category: 'Language' },
    { text: 'React', id: '2', category: 'Framework' },
    { text: 'TypeScript', id: '3', category: 'Language' }
  ];

  const getSelectedData = () => {
    const selected = listBoxRef.current.value;
    console.log('Selected ID:', selected);

    // Find full item data
    const selectedItem = data.find(item => item.id === selected);
    console.log('Selected Item:', selectedItem);
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
      <button onClick={getSelectedData}>Get Selected Data</button>
    </div>
  );
}

export default App;
```

### Multiple Selection Data

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function App() {
  const listBoxRef = useRef();

  const data = [
    { text: 'CSS', id: '1' },
    { text: 'HTML', id: '2' },
    { text: 'JavaScript', id: '3' }
  ];

  const getMultipleSelected = () => {
    const selectedIds = listBoxRef.current.value;
    const selectedItems = data.filter(item => 
      selectedIds.includes(item.id)
    );
    console.log('Selected Items:', selectedItems);
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      <button onClick={getMultipleSelected}>Get All Selected</button>
    </div>
  );
}

export default App;
```

---

## Disabling Items

### Disable Specific Items

Some items can be disabled from user selection:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript (Coming Soon)', id: '2', disabled: true },
    { text: 'React', id: '3' },
    { text: 'Vue (Deprecated)', id: '4', disabled: true }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id', disabled: 'disabled' }}
    />
  );
}

export default App;
```

---

## Common Patterns

### Single Select with Instant Action

Auto-close or trigger action on selection:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'Dashboard', id: '1' },
    { text: 'Settings', id: '2' },
    { text: 'Profile', id: '3' }
  ];

  const handleNavigate = (e) => {
    const page = data.find(item => item.id === e.value);
    console.log('Navigate to:', page.text);
    // Trigger navigation, API call, etc.
  };

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      selectionSettings={{ mode: 'Single' }}
      change={handleNavigate}
    />
  );
}

export default App;
```

### Multi-Select with Submit Button

Collect multiple selections and submit:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef, useState } from 'react';

function App() {
  const listBoxRef = useRef();
  const [submitted, setSubmitted] = useState(null);

  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'React', id: '2' },
    { text: 'Node.js', id: '3' }
  ];

  const handleSubmit = () => {
    const selected = listBoxRef.current.value;
    setSubmitted(selected);
    console.log('Submitted:', selected);
  };

  return (
    <div>
      <ListBoxComponent 
        ref={listBoxRef}
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        selectionSettings={{ mode: 'Multiple' }}
      />
      <button onClick={handleSubmit}>Submit Selection</button>
      {submitted && <p>Selected: {submitted.join(', ')}</p>}
    </div>
  );
}

export default App;
```

---

## Troubleshooting

### Checkboxes not appearing with `showCheckbox: true`
- You must inject the `CheckBoxSelection` service:
```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

<ListBoxComponent dataSource={data} selectionSettings={{ showCheckbox: true }}>
  <Inject services={[CheckBoxSelection]} />
</ListBoxComponent>
```
- Without `<Inject services={[CheckBoxSelection]} />`, the checkboxes will not render even if `showCheckbox: true` is set.

### Selection not working
- Ensure `fields` mapping includes a `value` property
- Check that item IDs are unique
- Verify data structure: `[{ text: '...', id: '...' }]`

### Pre-selection not applied
- Use refs and set in a useEffect hook (for Vite/CRA):
```tsx
useEffect(() => {
  if (listBoxRef.current) {
    listBoxRef.current.value = '2';
  }
}, []);
```

### Multiple selection shows single value
- Set `selectionSettings={{ mode: 'Multiple' }}` explicitly
- Verify `change` event returns array: `e.value` should be `['1', '2']`

### Items appear disabled unexpectedly
- Remove `disabled` field from data if not needed
- Check CSS for opacity or pointer-events styles
