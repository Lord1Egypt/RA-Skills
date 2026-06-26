# Dual ListBox (Transfer List) in React ListBox

## Table of Contents
- [Overview](#overview)
- [Basic Dual ListBox](#basic-dual-listbox)
- [Toolbar Operations](#toolbar-operations)
- [Custom Styling](#custom-styling)
- [Advanced Patterns](#advanced-patterns)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Dual ListBox enables users to transfer items between two list boxes using toolbar buttons. It's perfect for:
- Item selection interfaces (e.g., available vs selected items)
- Permission management (available permissions → granted permissions)
- Skill assignment (all skills → assigned skills)
- Data migration (source → destination)

### Available Operations

| Operation | Description |
|-----------|-------------|
| **moveUp** | Move selected item up within the same list |
| **moveDown** | Move selected item down within the same list |
| **moveTo** | Move selected item to the other list |
| **moveFrom** | Move selected item from the other list |
| **moveAllTo** | Move all items to the other list |
| **moveAllFrom** | Move all items from the other list |

---

## Basic Dual ListBox

### Simple Two-Way Transfer

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  const groupA = [
    { Name: 'Australia', Code: 'AU' },
    { Name: 'Bermuda', Code: 'BM' },
    { Name: 'Canada', Code: 'CA' },
    { Name: 'Cameroon', Code: 'CM' },
    { Name: 'Denmark', Code: 'DK' }
  ];

  const groupB = [
    { Name: 'India', Code: 'IN' },
    { Name: 'Italy', Code: 'IT' },
    { Name: 'Japan', Code: 'JP' },
    { Name: 'Mexico', Code: 'MX' },
    { Name: 'Norway', Code: 'NO' }
  ];

  const fields = { text: 'Name' };
  
  const toolbar = {
    items: ['moveUp', 'moveDown', 'moveTo', 'moveFrom', 'moveAllTo', 'moveAllFrom']
  };

  return (
    <div className="dual-listbox-wrapper">
      <div className="listbox-container">
        <h3>Available Countries</h3>
        <ListBoxComponent 
          dataSource={groupA}
          fields={fields}
          scope="#listbox-2"
          toolbarSettings={toolbar}
        />
      </div>

      <div className="listbox-container">
        <h3>Selected Countries</h3>
        <ListBoxComponent 
          id="listbox-2"
          dataSource={groupB}
          fields={fields}
        />
      </div>
    </div>
  );
}

export default App;
```

**CSS:**
```css
.dual-listbox-wrapper {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.listbox-container {
  flex: 1;
  min-width: 250px;
}

.listbox-container h3 {
  margin-top: 0;
  margin-bottom: 10px;
}
```

### With Custom Heights

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const availableItems = [
    { text: 'Item A', id: '1' },
    { text: 'Item B', id: '2' },
    { text: 'Item C', id: '3' },
    { text: 'Item D', id: '4' },
    { text: 'Item E', id: '5' }
  ];

  const selectedItems = [
    { text: 'Item X', id: '6' },
    { text: 'Item Y', id: '7' }
  ];

  const toolbar = {
    items: ['moveTo', 'moveFrom']
  };

  return (
    <div style={{ display: 'flex', gap: '30px' }}>
      <div>
        <label>Available:</label>
        <ListBoxComponent 
          dataSource={availableItems}
          fields={{ text: 'text', value: 'id' }}
          scope="#selected"
          toolbarSettings={toolbar}
          height="300px"
        />
      </div>

      <div>
        <label>Selected:</label>
        <ListBoxComponent 
          id="selected"
          dataSource={selectedItems}
          fields={{ text: 'text', value: 'id' }}
          height="300px"
        />
      </div>
    </div>
  );
}

export default App;
```

---

## Toolbar Operations

### Move Up/Down Within List

Users can reorder items within the same list:

```tsx
const toolbar = {
  items: ['moveUp', 'moveDown']
};

<ListBoxComponent 
  dataSource={priorityItems}
  fields={{ text: 'text' }}
  toolbarSettings={toolbar}
/>
```

### Single Direction Transfer (To Only)

Transfer only from left to right:

```tsx
const toolbar = {
  items: ['moveTo', 'moveAllTo']  // No moveFrom/moveAllFrom
};

<ListBoxComponent 
  dataSource={groupA}
  scope="#listbox-2"
  toolbarSettings={toolbar}
/>
```

### Bidirectional Transfer

Full two-way transfer with reordering:

```tsx
const toolbar = {
  items: [
    'moveUp',
    'moveDown',
    'moveTo',
    'moveFrom',
    'moveAllTo',
    'moveAllFrom'
  ]
};
```

### Custom Toolbar Layout

Control which operations appear and in what order:

```tsx
const toolbar = {
  items: ['moveAllTo', 'moveTo', 'moveFrom', 'moveAllFrom']
};

// Or for simple transfer:
const toolbar = {
  items: ['moveTo', 'moveFrom']
};

// Or reordering only:
const toolbar = {
  items: ['moveUp', 'moveDown']
};
```

---

## Custom Styling

### Style the Container

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import './App.css';

function App() {
  return (
    <div className="dual-listbox-custom">
      <div className="listbox-wrapper">
        <h3>Source</h3>
        <ListBoxComponent 
          dataSource={sourceItems}
          fields={{ text: 'text' }}
          scope="#target"
          toolbarSettings={{ items: ['moveAllTo'] }}
        />
      </div>

      <div className="listbox-wrapper">
        <h3>Target</h3>
        <ListBoxComponent 
          id="target"
          dataSource={targetItems}
          fields={{ text: 'text' }}
        />
      </div>
    </div>
  );
}

export default App;
```

**CSS:**
```css
.dual-listbox-custom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  padding: 20px;
}

.listbox-wrapper {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #f9f9f9;
}

.listbox-wrapper h3 {
  margin-top: 0;
  color: #333;
}

.e-listbox {
  border-radius: 4px;
}

.e-listbox .e-list-item {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.e-listbox .e-list-item.e-selected {
  background-color: #e3f2fd;
  color: #1976d2;
}
```

### Responsive Grid

```css
.dual-listbox-custom {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 20px;
}

@media (max-width: 768px) {
  .dual-listbox-custom {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
```

---

## Advanced Patterns

### Track Changes Between Lists

Monitor items moved and generate an audit trail using the `change` event:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useState } from 'react';

function App() {
  const sourceItems = [
    { text: 'A', id: '1' },
    { text: 'B', id: '2' },
    { text: 'C', id: '3' }
  ];

  const targetItems = [];
  const [auditLog, setAuditLog] = useState<string[]>([]);

  const handleChange = (e: any) => {
    const timestamp = new Date().toLocaleTimeString();
    const movedItems = (e.items as { text: string }[]).map(i => i.text).join(', ');
    const logEntry = `${timestamp} - Selection changed: ${movedItems}`;
    setAuditLog(prev => [...prev, logEntry]);
  };

  return (
    <div>
      <div style={{ display: 'flex', gap: '20px' }}>
        <div>
          <h3>Source</h3>
          <ListBoxComponent 
            dataSource={sourceItems}
            fields={{ text: 'text', value: 'id' }}
            scope="#target"
            toolbarSettings={{ items: ['moveTo', 'moveAllTo'] }}
            change={handleChange}
          />
        </div>

        <div>
          <h3>Target</h3>
          <ListBoxComponent 
            id="target"
            dataSource={targetItems}
            fields={{ text: 'text', value: 'id' }}
          />
        </div>
      </div>

      <div style={{ marginTop: '30px' }}>
        <h4>Audit Log:</h4>
        <ul>
          {auditLog.map((log, i) => <li key={i}>{log}</li>)}
        </ul>
      </div>
    </div>
  );
}

export default App;
```

### Validation Before Transfer

Use the `beforeDrop` event to validate and prevent transferring invalid items:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const sourceItems = [
    { text: 'Valid Item', id: '1', valid: true },
    { text: 'Invalid Item', id: '2', valid: false },
    { text: 'Another Valid', id: '3', valid: true }
  ];

  const targetItems = [];

  // beforeDrop fires before item is dropped — set e.cancel = true to prevent
  const handleBeforeDrop = (e) => {
    const droppedItems = e.items as { valid?: boolean }[];
    const hasInvalid = droppedItems.some((item: any) => item.valid === false);
    if (hasInvalid) {
      alert('Cannot transfer invalid items');
      e.cancel = true;
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>
        <ListBoxComponent 
          dataSource={sourceItems}
          fields={{ text: 'text' }}
          scope="#target"
          toolbarSettings={{ items: ['moveTo'] }}
          beforeDrop={handleBeforeDrop}
        />
      </div>

      <div>
        <ListBoxComponent 
          id="target"
          dataSource={targetItems}
        />
      </div>
    </div>
  );
}

export default App;
```

### Capacity Limits

Limit the number of items that can be in the target list using `maximumSelectionLength`:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const MAX_SELECTIONS = 3;

  const sourceItems = [
    { text: 'Item 1', id: '1' },
    { text: 'Item 2', id: '2' },
    { text: 'Item 3', id: '3' },
    { text: 'Item 4', id: '4' }
  ];

  const targetItems = [];

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div>
        <h3>Source</h3>
        <ListBoxComponent 
          dataSource={sourceItems}
          fields={{ text: 'text', value: 'id' }}
          scope="#target"
          toolbarSettings={{ items: ['moveTo'] }}
        />
      </div>

      <div>
        <h3>Target (max {MAX_SELECTIONS})</h3>
        <ListBoxComponent 
          id="target"
          dataSource={targetItems}
          fields={{ text: 'text', value: 'id' }}
          maximumSelectionLength={MAX_SELECTIONS}
        />
      </div>
    </div>
  );
}

export default App;
```

---

## Common Use Cases

### Permission Assignment

```tsx
function PermissionManager() {
  const allPermissions = [
    { text: 'Read', id: '1' },
    { text: 'Write', id: '2' },
    { text: 'Delete', id: '3' },
    { text: 'Admin', id: '4' }
  ];

  const assignedPermissions = [];

  const toolbar = {
    items: ['moveTo', 'moveFrom', 'moveAllTo', 'moveAllFrom']
  };

  return (
    <div style={{ display: 'flex', gap: '40px' }}>
      <div>
        <h3>Available Permissions</h3>
        <ListBoxComponent 
          dataSource={allPermissions}
          scope="#assigned"
          toolbarSettings={toolbar}
        />
      </div>

      <div>
        <h3>Assigned Permissions</h3>
        <ListBoxComponent 
          id="assigned"
          dataSource={assignedPermissions}
        />
      </div>
    </div>
  );
}
```

### Skill Assignment

```tsx
function SkillAssignment() {
  const skillPool = [
    { text: 'JavaScript', id: '1' },
    { text: 'React', id: '2' },
    { text: 'Node.js', id: '3' },
    { text: 'Python', id: '4' }
  ];

  const employeeSkills = [
    { text: 'TypeScript', id: '5' }
  ];

  const toolbar = {
    items: ['moveTo', 'moveFrom']
  };

  return (
    <div style={{ display: 'flex', gap: '30px' }}>
      <div>
        <h3>Available Skills</h3>
        <ListBoxComponent 
          dataSource={skillPool}
          scope="#employee"
          toolbarSettings={toolbar}
          height="300px"
        />
      </div>

      <div>
        <h3>Employee Skills</h3>
        <ListBoxComponent 
          id="employee"
          dataSource={employeeSkills}
          height="300px"
        />
      </div>
    </div>
  );
}
```

### Email Recipients

```tsx
function EmailRecipients() {
  const allContacts = [
    { text: 'john@example.com', id: '1' },
    { text: 'jane@example.com', id: '2' },
    { text: 'bob@example.com', id: '3' }
  ];

  const selectedRecipients = [];

  return (
    <div style={{ display: 'flex', gap: '30px' }}>
      <div>
        <h3>All Contacts</h3>
        <ListBoxComponent 
          dataSource={allContacts}
          scope="#recipients"
          toolbarSettings={{ items: ['moveAllTo'] }}
        />
      </div>

      <div>
        <h3>Recipients</h3>
        <ListBoxComponent 
          id="recipients"
          dataSource={selectedRecipients}
        />
      </div>
    </div>
  );
}
```

---

## Troubleshooting

### Toolbar buttons not working
- Verify `scope` attribute matches target ListBox id
- Ensure target ListBox has `id="..."` attribute
- Check that both ListBoxes are rendered

### Items not transferring
- Verify `scope` points to correct list: `scope="#target-id"`
- Ensure ListBoxes have different data sources
- Check browser console for errors

### Can't move back and forth
- Include both `moveTo` and `moveFrom` in toolbar items
- Verify both ListBoxes have toolbar settings if needed
- Check that `scope` is set on the first ListBox only

### Toolbar position incorrect
- Toolbar appears between lists - this is default behavior
- Adjust CSS margins if needed
- Ensure parent container has enough width

### Transfer preserves original data
- Transfer creates copy, doesn't remove from source
- To remove from source, manually update state
- Use state management to track items in each list
