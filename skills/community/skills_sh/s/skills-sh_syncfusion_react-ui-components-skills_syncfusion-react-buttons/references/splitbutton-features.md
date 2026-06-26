# SplitButton Features

## Table of Contents
- [Dropdown Items](#dropdown-items)
- [Icons and Text Combinations](#icons-and-text-combinations)
- [Disabled State](#disabled-state)
- [Event Handling](#event-handling)
- [Dynamic Item Manipulation](#dynamic-item-manipulation)
- [Keyboard Navigation](#keyboard-navigation)
- [Separators and Grouping](#separators-and-grouping)
- [Tooltips](#tooltips)
- [Best Practices](#best-practices)

## Dropdown Items

Define menu items for the dropdown using the `items` property.

### Basic Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function BasicItems() {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  return (
    <SplitButtonComponent items={items} cssClass="e-primary">
      Save
    </SplitButtonComponent>
  );
}

export default BasicItems;
```

### Items with Icons

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ItemsWithIcons() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-save"
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default ItemsWithIcons;
```

### Items with Descriptions

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ItemsWithDescriptions() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save', description: 'Ctrl+S' },
    { text: 'Save As', iconCss: 'e-icons e-save-as', description: 'Ctrl+Shift+S' },
    { text: 'Save All', iconCss: 'e-icons e-save-all', description: 'Ctrl+Alt+S' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>
          {props.iconCss && <i className={props.iconCss} style={{ marginRight: '8px' }} />}
          {props.text}
        </span>
        {props.description && (
          <span style={{ fontSize: '12px', color: '#999', marginLeft: '16px' }}>
            {props.description}
          </span>
        )}
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default ItemsWithDescriptions;
```

## Icons and Text Combinations

Combine icons with text in various ways.

### Icon-Left (Default)

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function IconLeftCombination() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-save"
      iconPosition="Left"
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default IconLeftCombination;
```

### Icon-Right

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function IconRightCombination() {
  const items = [
    { text: 'Next', iconCss: 'e-icons e-chevron-right' },
    { text: 'Skip', iconCss: 'e-icons e-skip-right' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-chevron-right"
      iconPosition="Right"
      cssClass="e-primary"
    >
      Next
    </SplitButtonComponent>
  );
}

export default IconRightCombination;
```

### Icon-Only Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function IconOnlyItems() {
  const items = [
    { iconCss: 'e-icons e-save', title: 'Save' },
    { iconCss: 'e-icons e-delete', title: 'Delete' },
    { iconCss: 'e-icons e-edit', title: 'Edit' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <i 
        className={props.iconCss} 
        title={props.title}
        style={{ fontSize: '16px', cursor: 'pointer' }}
      />
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary e-round"
      iconCss="e-icons e-ellipsis-h"
      title="More Actions"
    />
  );
}

export default IconOnlyItems;
```

### Mixed Content with Icons and Badges

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function MixedContentItems() {
  const items = [
    { text: 'Notifications', badge: '5', iconCss: 'e-icons e-bell' },
    { text: 'Messages', badge: '2', iconCss: 'e-icons e-mail' },
    { text: 'Comments', badge: '12', iconCss: 'e-icons e-chat' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>
          {props.iconCss && <i className={props.iconCss} style={{ marginRight: '8px' }} />}
          {props.text}
        </span>
        {props.badge && (
          <span 
            style={{
              backgroundColor: '#e74c3c',
              color: 'white',
              borderRadius: '12px',
              padding: '2px 6px',
              fontSize: '11px',
              marginLeft: '8px'
            }}
          >
            {props.badge}
          </span>
        )}
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
      iconCss="e-icons e-bell"
    >
      Alerts
    </SplitButtonComponent>
  );
}

export default MixedContentItems;
```

## Disabled State

Control when the SplitButton is disabled.

### Static Disabled State

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function StaticDisabled() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  return (
    <div>
      {/* Active SplitButton */}
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        Active
      </SplitButtonComponent>

      {/* Disabled SplitButton */}
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        disabled={true}
        style={{ marginLeft: '10px' }}
      >
        Disabled
      </SplitButtonComponent>
    </div>
  );
}

export default StaticDisabled;
```

### Dynamic Disabled State

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function DynamicDisabled() {
  const [isProcessing, setIsProcessing] = useState(false);
  const items = [{ text: 'Send' }, { text: 'Schedule Send' }];

  const handlePrimaryClick = async () => {
    setIsProcessing(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('Email sent');
      alert('Email sent successfully!');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        disabled={isProcessing}
        click={handlePrimaryClick}
      >
        {isProcessing ? 'Sending...' : 'Send'}
      </SplitButtonComponent>
      <p style={{ marginTop: '10px' }}>
        Status: <strong>{isProcessing ? 'Processing' : 'Ready'}</strong>
      </p>
    </div>
  );
}

export default DynamicDisabled;
```

### Disable Specific Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function DisableSpecificItems() {
  const [items, setItems] = useState([
    { text: 'Save', disabled: false },
    { text: 'Save As', disabled: false },
    { text: 'Save All', disabled: true }  // Disabled item
  ]);

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default DisableSpecificItems;
```

## Event Handling

Handle various SplitButton events.

### Primary Click Event

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function PrimaryClickEvent() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];

  const handlePrimaryClick = (args: any) => {
    console.log('Primary button clicked');
    console.log('Event:', args);
    alert('Primary action performed');
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      click={handlePrimaryClick}
    >
      Save
    </SplitButtonComponent>
  );
}

export default PrimaryClickEvent;
```

### Select Event (Menu Item Click)

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function SelectEvent() {
  const [selectedItem, setSelectedItem] = useState('');
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  const handleSelect = (args: any) => {
    console.log('Menu item selected:', args.item.text);
    setSelectedItem(args.item.text);
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        select={handleSelect}
      >
        Save
      </SplitButtonComponent>
      {selectedItem && (
        <p style={{ marginTop: '10px' }}>
          Last selected: <strong>{selectedItem}</strong>
        </p>
      )}
    </div>
  );
}

export default SelectEvent;
```

### Before Open Event

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function BeforeOpenEvent() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  const handleBeforeOpen = (args: any) => {
    console.log('Dropdown menu is about to open');
    console.log('Event:', args);
    // Can modify items or prevent opening
    // args.cancel = true; // To prevent opening
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      beforeOpen={handleBeforeOpen}
    >
      Action
    </SplitButtonComponent>
  );
}

export default BeforeOpenEvent;
```

### Open Event

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function OpenEvent() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  const handleOpen = (args: any) => {
    console.log('Dropdown menu opened');
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      open={handleOpen}
    >
      Action
    </SplitButtonComponent>
  );
}

export default OpenEvent;
```

### Close Event

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function CloseEvent() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  const handleClose = (args: any) => {
    console.log('Dropdown menu closed');
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      close={handleClose}
    >
      Action
    </SplitButtonComponent>
  );
}

export default CloseEvent;
```

### Multiple Event Handlers

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function MultipleEvents() {
  const [log, setLog] = useState<string[]>([]);
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  const addLog = (message: string) => {
    setLog(prev => [...prev.slice(-4), `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const handlePrimaryClick = () => {
    addLog('Primary clicked');
  };

  const handleSelect = (args: any) => {
    addLog(`Menu item selected: ${args.item.text}`);
  };

  const handleBeforeOpen = () => {
    addLog('Before open');
  };

  const handleOpen = () => {
    addLog('Menu opened');
  };

  const handleClose = () => {
    addLog('Menu closed');
  };

  return (
    <div style={{ padding: '20px' }}>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        click={handlePrimaryClick}
        select={handleSelect}
        beforeOpen={handleBeforeOpen}
        open={handleOpen}
        close={handleClose}
      >
        Action
      </SplitButtonComponent>

      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <h4>Event Log:</h4>
        {log.map((entry, index) => (
          <div key={index} style={{ fontSize: '12px', color: '#666' }}>
            {entry}
          </div>
        ))}
      </div>
    </div>
  );
}

export default MultipleEvents;
```

## Dynamic Item Manipulation

Add, remove, and modify items at runtime.

### Add Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function AddItems() {
  const [items, setItems] = useState([
    { text: 'Option 1' },
    { text: 'Option 2' }
  ]);

  const addItem = () => {
    const newItem = { text: `Option ${items.length + 1}` };
    setItems([...items, newItem]);
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        Select
      </SplitButtonComponent>
      <button onClick={addItem} style={{ marginLeft: '10px' }}>
        Add Item
      </button>
      <p>Total items: {items.length}</p>
    </div>
  );
}

export default AddItems;
```

### Remove Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function RemoveItems() {
  const [items, setItems] = useState([
    { text: 'Option 1' },
    { text: 'Option 2' },
    { text: 'Option 3' }
  ]);

  const removeLastItem = () => {
    if (items.length > 1) {
      setItems(items.slice(0, -1));
    }
  };

  const removeItemByIndex = (index: number) => {
    setItems(items.filter((_, i) => i !== index));
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
      >
        Select
      </SplitButtonComponent>
      <button onClick={removeLastItem} style={{ marginLeft: '10px' }}>
        Remove Last
      </button>
      <button 
        onClick={() => removeItemByIndex(0)} 
        style={{ marginLeft: '10px' }}
      >
        Remove First
      </button>
      <p>Total items: {items.length}</p>
    </div>
  );
}

export default RemoveItems;
```

### Update Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function UpdateItems() {
  const [items, setItems] = useState([
    { text: 'Option 1', status: 'available' },
    { text: 'Option 2', status: 'available' },
    { text: 'Option 3', status: 'locked' }
  ]);

  const updateItem = (index: number) => {
    const updated = [...items];
    updated[index].status = updated[index].status === 'available' ? 'locked' : 'available';
    setItems(updated);
  };

  const itemTemplate = (props: any) => {
    return (
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>{props.text}</span>
        <span 
          style={{
            fontSize: '11px',
            padding: '2px 6px',
            backgroundColor: props.status === 'available' ? '#28a745' : '#dc3545',
            color: 'white',
            borderRadius: '3px'
          }}
        >
          {props.status}
        </span>
      </div>
    );
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        itemTemplate={itemTemplate}
      >
        Select
      </SplitButtonComponent>
      <div style={{ marginTop: '10px' }}>
        {items.map((item, index) => (
          <button 
            key={index}
            onClick={() => updateItem(index)}
            style={{ marginRight: '10px', marginBottom: '5px' }}
          >
            Toggle {item.text}
          </button>
        ))}
      </div>
    </div>
  );
}

export default UpdateItems;
```

## Keyboard Navigation

Users can navigate the dropdown using keyboard.

### Navigation Keys

| Key | Action |
|-----|--------|
| Arrow Down | Move to next item |
| Arrow Up | Move to previous item |
| Space/Enter | Select focused item |
| Escape | Close dropdown |
| Tab | Close dropdown, move focus to next element |

### Example with Keyboard Support

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function KeyboardNavigation() {
  const items = [
    { text: 'Save (Ctrl+S)', iconCss: 'e-icons e-save' },
    { text: 'Save As (Ctrl+Shift+S)', iconCss: 'e-icons e-save-as' },
    { text: 'Save All (Ctrl+Alt+S)', iconCss: 'e-icons e-save-all' }
  ];

  const handleKeyDown = (e: React.KeyboardEvent) => {
    console.log('Key pressed:', e.key);
  };

  return (
    <div>
      <p style={{ color: '#666', marginBottom: '10px' }}>
        Use Arrow keys to navigate, Space/Enter to select, Escape to close
      </p>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        onKeyDown={handleKeyDown}
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default KeyboardNavigation;
```

## Separators and Grouping

Organize menu items with separators.

### Item Separator

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ItemSeparator() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { separator: true },  // Separator line
    { text: 'Save All', iconCss: 'e-icons e-save-all' },
    { text: 'Save Backup', iconCss: 'e-icons e-backup' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default ItemSeparator;
```

### Grouped Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function GroupedItems() {
  const items = [
    // Save group
    { text: 'Save', iconCss: 'e-icons e-save', group: 'Save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as', group: 'Save' },
    { separator: true },
    
    // Print group
    { text: 'Print', iconCss: 'e-icons e-print', group: 'Print' },
    { text: 'Print Preview', iconCss: 'e-icons e-preview', group: 'Print' },
    { separator: true },
    
    // Export group
    { text: 'Export PDF', iconCss: 'e-icons e-pdf', group: 'Export' },
    { text: 'Export Excel', iconCss: 'e-icons e-excel', group: 'Export' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      File
    </SplitButtonComponent>
  );
}

export default GroupedItems;
```

## Tooltips

Add tooltips to SplitButton and items.

### Primary Button Tooltip

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function PrimaryTooltip() {
  const items = [{ text: 'Save' }];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      title="Save the current document (Ctrl+S)"
    >
      Save
    </SplitButtonComponent>
  );
}

export default PrimaryTooltip;
```

### Item Tooltips

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ItemTooltips() {
  const items = [
    { text: 'Save', title: 'Save current document' },
    { text: 'Save As', title: 'Save with new name' },
    { text: 'Save All', title: 'Save all open documents' }
  ];

  const itemTemplate = (props: any) => {
    return (
      <span title={props.title}>
        {props.text}
      </span>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      itemTemplate={itemTemplate}
    >
      Save
    </SplitButtonComponent>
  );
}

export default ItemTooltips;
```

## Best Practices

### 1. Clear Item Text

Always use descriptive text that clearly indicates what will happen when clicked.

```tsx
// ✓ Good
const goodItems = [
  { text: 'Save' },
  { text: 'Save As' }
];

// ✗ Avoid
const badItems = [
  { text: 'S' },
  { text: 'Ctrl+S' }
];
```

### 2. Use Icons Consistently

When using icons in items, also use in primary button.

```tsx
// ✓ Good
<SplitButtonComponent
  items={[
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' }
  ]}
  iconCss="e-icons e-save"
>
  Save
</SplitButtonComponent>

// ✗ Avoid mixing icon styles
```

### 3. Handle Events Properly

Clean up resources in event handlers.

```tsx
const handleSelect = (args: any) => {
  // Do immediate work
  const itemText = args.item.text;
  
  // For async operations, provide feedback
  // setIsLoading(true);
};
```

### 4. Provide Keyboard Shortcuts

Show keyboard shortcuts in tooltips or item descriptions.

```tsx
const items = [
  { text: 'Save', description: 'Ctrl+S' },
  { text: 'Save As', description: 'Ctrl+Shift+S' }
];
```

### 5. Limit Item Count

Keep dropdown items between 3-10 for better UX.

```tsx
// ✓ Good (6 items)
const items = [
  { text: 'Option 1' },
  { text: 'Option 2' },
  { text: 'Option 3' },
  { text: 'Option 4' },
  { text: 'Option 5' },
  { text: 'Option 6' }
];

// ✗ Avoid (20+ items - use grouped lists instead)
```

## Next Steps

- **Customization** → Read [customization.md](customization.md) for advanced styling and templates
- **API Reference** → Read [api-reference.md](api-reference.md) for all available properties
- **Accessibility** → Read [accessibility.md](accessibility.md) for WCAG compliance
