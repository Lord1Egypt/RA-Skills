# Buttons and Actions

## Table of Contents
- [Built-in Button Support](#built-in-button-support)
- [Button Model Properties](#button-model-properties)
- [Click Event Handlers](#click-event-handlers)
- [Icon Buttons](#icon-buttons)
- [Styling Buttons](#styling-buttons)
- [Primary and Secondary Buttons](#primary-and-secondary-buttons)
- [Common Patterns](#common-patterns)
- [Edge Cases](#edge-cases)

## Built-in Button Support

The Dialog supports built-in footer buttons via the `buttons` property:

```jsx
import React, { useRef } from 'react';
import { DialogComponent } from '@syncfusion/ej2-react-popups';
import './App.css';

export default function App() {
  const dialogRef = useRef(null);

  const buttons = [
    {
      buttonModel: {
        content: 'OK',
        cssClass: 'e-flat',
        isPrimary: true,
      },
      click: () => {
        console.log('OK clicked');
        dialogRef.current?.hide();
      },
    },
    {
      buttonModel: {
        content: 'Cancel',
        cssClass: 'e-flat',
      },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Open</button>

      <DialogComponent
        ref={dialogRef}
        header="Confirmation"
        buttons={buttons}
        target="#dialog-target"
      >
        Are you sure?
      </DialogComponent>
    </div>
  );
}
```

## Button Model Properties

Each button in the array has a `buttonModel` object:

| Property | Type | Description |
|----------|------|-------------|
| `content` | string | Button text/label |
| `cssClass` | string | CSS classes (e.g., 'e-flat', 'e-outline') |
| `isPrimary` | boolean | Highlight as primary action |
| `isDisabled` | boolean | Disable button |
| `iconCss` | string | Icon class (Font Awesome, Material Icons) |
| `id` | string | Button HTML id |

### Example with Full Properties

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Save',
      cssClass: 'e-flat e-primary',
      isPrimary: true,
      iconCss: 'e-icons e-save',
      id: 'save-btn',
    },
    click: handleSave,
  },
  {
    buttonModel: {
      content: 'Delete',
      cssClass: 'e-flat e-danger',
      iconCss: 'e-icons e-delete',
      id: 'delete-btn',
    },
    click: handleDelete,
  },
];
```

## Click Event Handlers

Each button has a `click` callback:

```jsx
const buttons = [
  {
    buttonModel: { content: 'Submit', isPrimary: true, cssClass: 'e-flat' },
    click: () => {
      console.log('Submit clicked');
      // Perform action
      dialogRef.current?.hide();
    },
  },
];
```

### Access Button Data in Handler

```jsx
const buttons = [
  {
    buttonModel: { content: 'Action 1', cssClass: 'e-flat' },
    click: function() {
      // 'this' refers to the button element
      console.log(this.textContent); // "Action 1"
    },
  },
];
```

### Multiple Actions

```jsx
const handleApply = () => {
  console.log('Apply clicked');
  saveData();
  refreshUI();
  dialogRef.current?.hide();
};

const buttons = [
  {
    buttonModel: { content: 'Apply', isPrimary: true, cssClass: 'e-flat' },
    click: handleApply,
  },
];
```

## Icon Buttons

### With Syncfusion Icons

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Save',
      cssClass: 'e-flat',
      iconCss: 'e-icons e-save',
    },
    click: () => console.log('Save'),
  },
  {
    buttonModel: {
      content: 'Delete',
      cssClass: 'e-flat',
      iconCss: 'e-icons e-delete',
    },
    click: () => console.log('Delete'),
  },
];
```

### Available Syncfusion Icons

- `e-save` - Save icon
- `e-delete` - Delete icon
- `e-edit` - Edit icon
- `e-update` - Update/refresh icon
- `e-print` - Print icon
- `e-export` - Export icon
- `e-close` - Close icon
- `e-search` - Search icon
- `e-settings` - Settings icon

### Font Awesome Icons

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Download',
      cssClass: 'e-flat',
      iconCss: 'fa fa-download',
    },
    click: () => console.log('Download'),
  },
  {
    buttonModel: {
      content: 'Share',
      cssClass: 'e-flat',
      iconCss: 'fa fa-share',
    },
    click: () => console.log('Share'),
  },
];
```

### Material Icons

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Favorite',
      cssClass: 'e-flat',
      iconCss: 'material-icons',
      content: '<span class="material-icons">favorite</span> Favorite',
    },
    click: () => console.log('Favorite'),
  },
];
```

## Styling Buttons

### CSS Classes

Built-in classes:
- `e-flat` - Flat button style
- `e-outline` - Outline style
- `e-primary` - Primary theme color (combine with isPrimary)
- `e-danger` - Red danger style
- `e-success` - Green success style
- `e-warning` - Yellow warning style
- `e-info` - Blue info style
- `e-small` - Smaller button
- `e-large` - Larger button

### Styling Examples

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Primary',
      cssClass: 'e-flat e-primary',
      isPrimary: true,
    },
    click: () => {},
  },
  {
    buttonModel: {
      content: 'Danger',
      cssClass: 'e-flat e-danger',
    },
    click: () => {},
  },
  {
    buttonModel: {
      content: 'Success',
      cssClass: 'e-flat e-success',
    },
    click: () => {},
  },
];
```

### Custom CSS

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Custom',
      cssClass: 'my-custom-button',
    },
    click: () => {},
  },
];
```

```css
.my-custom-button {
  background: linear-gradient(to right, #667eea, #764ba2) !important;
  color: white !important;
  border: none !important;
  font-weight: bold !important;
}

.my-custom-button:hover {
  opacity: 0.8;
}
```

## Primary and Secondary Buttons

### Marking Primary Action

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Save',
      cssClass: 'e-flat',
      isPrimary: true,  // Highlighted as main action
    },
    click: handleSave,
  },
  {
    buttonModel: {
      content: 'Cancel',
      cssClass: 'e-flat',
      isPrimary: false,  // Secondary action
    },
    click: handleCancel,
  },
];
```

**Visual difference:** Primary button has different background color.

### Confirmation Pattern

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'Delete',
      cssClass: 'e-flat e-danger',
      isPrimary: true,  // Dangerous action as primary
    },
    click: handleDelete,
  },
  {
    buttonModel: {
      content: 'Cancel',
      cssClass: 'e-flat',
    },
    click: handleCancel,
  },
];
```

## Common Patterns

### Pattern 1: OK/Cancel Dialog

```jsx
export function ConfirmDialog() {
  const dialogRef = useRef(null);

  const buttons = [
    {
      buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
      click: () => {
        console.log('Confirmed');
        dialogRef.current?.hide();
      },
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Confirm</button>
      <DialogComponent
        ref={dialogRef}
        header="Confirm Action"
        buttons={buttons}
        target="#dialog-target"
      >
        Proceed with this action?
      </DialogComponent>
    </div>
  );
}
```

### Pattern 2: Yes/No Dialog

```jsx
const buttons = [
  {
    buttonModel: { content: 'Yes', isPrimary: true, cssClass: 'e-flat e-success' },
    click: handleYes,
  },
  {
    buttonModel: { content: 'No', cssClass: 'e-flat' },
    click: handleNo,
  },
];
```

### Pattern 3: Multiple Actions

```jsx
const buttons = [
  {
    buttonModel: { content: 'Save', isPrimary: true, cssClass: 'e-flat' },
    click: handleSave,
  },
  {
    buttonModel: { content: 'Save As', cssClass: 'e-flat' },
    click: handleSaveAs,
  },
  {
    buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
    click: handleCancel,
  },
];
```

### Pattern 4: Single Button (Alert)

```jsx
const buttons = [
  {
    buttonModel: { content: 'OK', isPrimary: true, cssClass: 'e-flat' },
    click: () => dialogRef.current?.hide(),
  },
];
```

### Pattern 5: Form Actions

```jsx
const buttons = [
  {
    buttonModel: { content: 'Submit', isPrimary: true, cssClass: 'e-flat' },
    click: handleSubmit,
  },
  {
    buttonModel: { content: 'Reset', cssClass: 'e-flat' },
    click: handleReset,
  },
  {
    buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
    click: handleCancel,
  },
];
```

### Pattern 6: Delete Dialog (Danger Pattern)

```jsx
export function DeleteDialog() {
  const dialogRef = useRef(null);

  const buttons = [
    {
      buttonModel: {
        content: 'Delete',
        cssClass: 'e-flat e-danger',
        isPrimary: true,
      },
      click: () => {
        performDelete();
        dialogRef.current?.hide();
      },
    },
    {
      buttonModel: { content: 'Cancel', cssClass: 'e-flat' },
      click: () => dialogRef.current?.hide(),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Delete</button>
      <DialogComponent
        ref={dialogRef}
        header="⚠️ Delete Item"
        buttons={buttons}
        isModal={true}
        target="#dialog-target"
      >
        This action cannot be undone. Continue?
      </DialogComponent>
    </div>
  );
}
```

## Edge Cases

### Disabled Buttons

```jsx
const [isLoading, setIsLoading] = React.useState(false);

const buttons = [
  {
    buttonModel: {
      content: 'Submit',
      cssClass: 'e-flat',
      isPrimary: true,
      isDisabled: isLoading,  // Disable while processing
    },
    click: () => {
      setIsLoading(true);
      performAction().finally(() => setIsLoading(false));
    },
  },
];
```

### Button with Loading State

```jsx
const [isSubmitting, setIsSubmitting] = React.useState(false);

const handleSubmit = async () => {
  setIsSubmitting(true);
  try {
    await submitForm();
    dialogRef.current?.hide();
  } finally {
    setIsSubmitting(false);
  }
};

const buttons = [
  {
    buttonModel: {
      content: isSubmitting ? 'Submitting...' : 'Submit',
      cssClass: 'e-flat',
      isPrimary: true,
      isDisabled: isSubmitting,
    },
    click: handleSubmit,
  },
];
```

### No Buttons (Footer Template Only)

Use `footerTemplate` if you need complete control and don't want built-in buttons:

```jsx
const footerTemplate = (
  <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end', padding: '15px' }}>
    <button className="e-control e-btn">Custom 1</button>
    <button className="e-control e-btn">Custom 2</button>
  </div>
);

<DialogComponent footerTemplate={footerTemplate}>
  Content
</DialogComponent>
```

### Very Long Button Text

```jsx
const buttons = [
  {
    buttonModel: {
      content: 'This is a very long button label that might wrap',
      cssClass: 'e-flat',
    },
    click: () => {},
  },
];
```

**Solution:** Set button width
```css
.e-dialog .e-footer .e-btn {
  min-width: 100px;
}
```

### Dynamic Button Properties

```jsx
export function DynamicButtons() {
  const dialogRef = useRef(null);
  const [count, setCount] = React.useState(0);

  const buttons = [
    {
      buttonModel: {
        content: `Clicked ${count} times`,
        cssClass: 'e-flat',
      },
      click: () => setCount(count + 1),
    },
  ];

  return (
    <div id="dialog-target" style={{ position: 'relative' }}>
      <button onClick={() => dialogRef.current?.show()}>Show</button>
      <DialogComponent
        ref={dialogRef}
        header="Counter"
        buttons={buttons}
        target="#dialog-target"
      >
        Click the button below to count
      </DialogComponent>
    </div>
  );
}
```

**Next:** Choose another reference topic based on your needs.
