# SplitButton API Reference

Complete documentation of SplitButton component properties, methods, events, and interfaces.

## Table of Contents
- [Component Properties](#component-properties)
- [Item Model Properties](#item-model-properties)
- [Methods](#methods)
- [Events](#events)
- [Event Arguments](#event-arguments)
- [CSS Classes](#css-classes)
- [Type Definitions](#type-definitions)
- [Quick Reference Tables](#quick-reference-tables)

---

## Component Properties

### Basic Properties

#### `cssClass`
**Type:** `string`  
**Default:** `''`  
**Description:** CSS classes to apply to the SplitButton element. Can combine multiple classes.

**Example:**
```tsx
<SplitButtonComponent cssClass="e-primary e-large" />
```

**Available Classes:**
- `e-primary` - Primary button style (blue)
- `e-success` - Success style (green)
- `e-info` - Info style (cyan)
- `e-warning` - Warning style (orange)
- `e-danger` - Danger style (red)
- `e-link` - Link style
- `e-flat` - Flat button type
- `e-outline` - Outline button type
- `e-round` - Rounded button type
- `e-small` - Small size
- `e-large` - Large size

---

#### `disabled`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Disables the SplitButton when set to true. Disabled buttons cannot be clicked.

**Example:**
```tsx
<SplitButtonComponent disabled={true} />
<SplitButtonComponent disabled={isLoading} />
```

---

#### `enableRtl`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Enables right-to-left (RTL) mode for RTL languages like Arabic and Hebrew.

**Example:**
```tsx
<SplitButtonComponent enableRtl={true} dir="rtl" />
```

---

#### `iconCss`
**Type:** `string`  
**Default:** `''`  
**Description:** CSS class for the icon to display on the primary button. Use Syncfusion icon classes.

**Example:**
```tsx
<SplitButtonComponent iconCss="e-icons e-save" />
```

**Common Icon Classes:**
- `e-icons e-save` - Save icon
- `e-icons e-delete` - Delete icon
- `e-icons e-edit` - Edit icon
- `e-icons e-close` - Close icon
- `e-icons e-download` - Download icon
- `e-icons e-upload` - Upload icon
- `e-icons e-settings` - Settings icon
- `e-icons e-mail` - Mail icon
- `e-icons e-print` - Print icon

---

#### `iconPosition`
**Type:** `string`  
**Default:** `'Left'`  
**Description:** Position of the icon relative to button text.

**Valid Values:**
- `'Left'` - Icon on the left (default)
- `'Right'` - Icon on the right
- `'Top'` - Icon on top
- `'Bottom'` - Icon on bottom

**Example:**
```tsx
<SplitButtonComponent 
  iconCss="e-icons e-chevron-right"
  iconPosition="Right"
>
  Next
</SplitButtonComponent>
```

---

#### `items`
**Type:** `ItemModel[]`  
**Default:** `[]`  
**Description:** Array of dropdown menu items. Each item is an ItemModel.

**Example:**
```tsx
const items = [
  { text: 'Save', iconCss: 'e-icons e-save' },
  { text: 'Save As', iconCss: 'e-icons e-save-as' },
  { separator: true },
  { text: 'Save All', iconCss: 'e-icons e-save-all' }
];

<SplitButtonComponent items={items} />
```

---

#### `content`
**Type:** `string | ReactNode`  
**Default:** `''`  
**Description:** Text or React component to display as the button label (children prop).

**Example:**
```tsx
<SplitButtonComponent items={items}>
  Save
</SplitButtonComponent>

<SplitButtonComponent items={items}>
  <span>Save <strong>Now</strong></span>
</SplitButtonComponent>
```

---

#### `title`
**Type:** `string`  
**Default:** `''`  
**Description:** Tooltip text to display on hover over the primary button.

**Example:**
```tsx
<SplitButtonComponent
  items={items}
  title="Save the current document (Ctrl+S)"
/>
```

---

### Advanced Properties

#### `ref`
**Type:** `React.Ref<SplitButtonComponent>`  
**Description:** Reference to the component instance for imperative access.

**Example:**
```tsx
const splitBtnRef = useRef<SplitButtonComponent>(null);

<SplitButtonComponent ref={splitBtnRef} items={items} />

// Access methods
splitBtnRef.current?.element
```

---

#### `itemTemplate`
**Type:** `function`  
**Description:** Custom template function for rendering dropdown items.

**Signature:**
```tsx
itemTemplate?: (props: ItemModel) => ReactNode
```

**Example:**
```tsx
const itemTemplate = (props: any) => {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <span>{props.text}</span>
      <span style={{ color: '#999' }}>{props.shortcut}</span>
    </div>
  );
};

<SplitButtonComponent
  items={items}
  itemTemplate={itemTemplate}
/>
```

---

#### `beforeItemRender`
**Type:** `function`  
**Description:** Event fired before each item is rendered in the dropdown.

**Signature:**
```tsx
beforeItemRender?: (args: IItemRendering) => void
```

**Example:**
```tsx
const handleBeforeItemRender = (args: any) => {
  console.log('Rendering item:', args.item.text);
};

<SplitButtonComponent
  items={items}
  beforeItemRender={handleBeforeItemRender}
/>
```

---

## Item Model Properties

Defines structure for each item in the `items` array.

```tsx
interface ItemModel {
  text?: string;              // Item display text
  iconCss?: string;           // Icon CSS class
  id?: string;                // Unique identifier
  disabled?: boolean;         // Disable this item
  separator?: boolean;        // Display as separator line
  title?: string;             // Tooltip text
  url?: string;               // Navigation URL
  target?: string;            // Link target (_blank, _self, etc.)
  [key: string]: any;         // Custom properties
}
```

### Item Properties Details

#### `text`
**Type:** `string`  
**Description:** Display text for the item.

```tsx
{ text: 'Save' }
```

---

#### `iconCss`
**Type:** `string`  
**Description:** CSS class for item icon.

```tsx
{ text: 'Save', iconCss: 'e-icons e-save' }
```

---

#### `id`
**Type:** `string`  
**Description:** Unique identifier for the item.

```tsx
{ id: 'save-item', text: 'Save' }
```

---

#### `disabled`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Disable individual item.

```tsx
{ text: 'Save All', disabled: true }
```

---

#### `separator`
**Type:** `boolean`  
**Default:** `false`  
**Description:** Display as separator line instead of clickable item.

```tsx
{ separator: true }
```

---

#### `title`
**Type:** `string`  
**Description:** Tooltip for the item.

```tsx
{ text: 'Save', title: 'Save current document (Ctrl+S)' }
```

---

#### `url`
**Type:** `string`  
**Description:** Navigation URL for the item.

```tsx
{ text: 'External Link', url: 'https://example.com' }
```

---

#### `target`
**Type:** `string`  
**Description:** Link target attribute.

**Valid Values:**
- `'_self'` - Same window (default)
- `'_blank'` - New window/tab
- `'_parent'` - Parent frame
- `'_top'` - Top frame

```tsx
{ text: 'External Link', url: 'https://example.com', target: '_blank' }
```

---

#### Custom Properties
You can add custom properties to items for template usage.

```tsx
const items = [
  { 
    text: 'Save', 
    iconCss: 'e-icons e-save',
    shortcut: 'Ctrl+S',
    category: 'File'
  }
];
```

---

## Methods

### `show()`
**Description:** Shows the dropdown menu.

**Signature:**
```tsx
show(): void
```

**Example:**
```tsx
const splitBtnRef = useRef<SplitButtonComponent>(null);

const handleShowDropdown = () => {
  splitBtnRef.current?.show();
};
```

---

### `hide()`
**Description:** Hides the dropdown menu.

**Signature:**
```tsx
hide(): void
```

**Example:**
```tsx
const handleHideDropdown = () => {
  splitBtnRef.current?.hide();
};
```

---

### `toggle()`
**Description:** Toggles the dropdown menu visibility.

**Signature:**
```tsx
toggle(): void
```

**Example:**
```tsx
const handleToggle = () => {
  splitBtnRef.current?.toggle();
};
```

---

### `click()`
**Description:** Programmatically trigger the primary button click event.

**Signature:**
```tsx
click(): void
```

**Example:**
```tsx
const handleProgrammaticClick = () => {
  splitBtnRef.current?.click();
};
```

---

### `refresh()`
**Description:** Refresh the component with updated properties.

**Signature:**
```tsx
refresh(): void
```

**Example:**
```tsx
const handleRefresh = () => {
  splitBtnRef.current?.refresh();
};
```

---

## Events

### `click`
**Type:** `(args: ClickEventArgs) => void`  
**Description:** Triggered when the primary button is clicked.

**Example:**
```tsx
const handleClick = (args: any) => {
  console.log('Primary button clicked');
};

<SplitButtonComponent items={items} click={handleClick} />
```

---

### `select`
**Type:** `(args: SelectEventArgs) => void`  
**Description:** Triggered when a dropdown menu item is selected/clicked.

**Example:**
```tsx
const handleSelect = (args: any) => {
  console.log('Selected item:', args.item.text);
};

<SplitButtonComponent items={items} select={handleSelect} />
```

---

### `beforeOpen`
**Type:** `(args: BeforeOpenCloseEventArgs) => void`  
**Description:** Triggered before the dropdown menu opens. Can be prevented by setting `args.cancel = true`.

**Example:**
```tsx
const handleBeforeOpen = (args: any) => {
  console.log('Dropdown is about to open');
  // args.cancel = true; // Prevent opening
};

<SplitButtonComponent items={items} beforeOpen={handleBeforeOpen} />
```

---

### `open`
**Type:** `(args: OpenCloseEventArgs) => void`  
**Description:** Triggered after the dropdown menu opens.

**Example:**
```tsx
const handleOpen = (args: any) => {
  console.log('Dropdown opened');
};

<SplitButtonComponent items={items} open={handleOpen} />
```

---

### `beforeClose`
**Type:** `(args: BeforeOpenCloseEventArgs) => void`  
**Description:** Triggered before the dropdown menu closes. Can be prevented by setting `args.cancel = true`.

**Example:**
```tsx
const handleBeforeClose = (args: any) => {
  console.log('Dropdown is about to close');
};

<SplitButtonComponent items={items} beforeClose={handleBeforeClose} />
```

---

### `close`
**Type:** `(args: OpenCloseEventArgs) => void`  
**Description:** Triggered after the dropdown menu closes.

**Example:**
```tsx
const handleClose = (args: any) => {
  console.log('Dropdown closed');
};

<SplitButtonComponent items={items} close={handleClose} />
```

---

### `created`
**Type:** `(args: void) => void`  
**Description:** Triggered after the component is created and initialized.

**Example:**
```tsx
const handleCreated = () => {
  console.log('SplitButton created');
};

<SplitButtonComponent items={items} created={handleCreated} />
```

---

### `destroy`
**Type:** `(args: void) => void`  
**Description:** Triggered before the component is destroyed.

**Example:**
```tsx
const handleDestroy = () => {
  console.log('SplitButton destroyed');
};

<SplitButtonComponent items={items} destroy={handleDestroy} />
```

---

## Event Arguments

### ClickEventArgs
Arguments passed to the `click` event handler.

```tsx
interface ClickEventArgs {
  element?: HTMLElement;        // DOM element of the button
  event?: MouseEvent;           // Native mouse event
}
```

---

### SelectEventArgs
Arguments passed to the `select` event handler.

```tsx
interface SelectEventArgs {
  item: ItemModel;              // Selected item object
  element?: HTMLElement;        // Item element
  event?: MouseEvent;           // Native mouse event
}
```

---

### BeforeOpenCloseEventArgs
Arguments passed to `beforeOpen` and `beforeClose` events.

```tsx
interface BeforeOpenCloseEventArgs {
  cancel?: boolean;             // Set to true to prevent action
  element?: HTMLElement;        // DOM element
  event?: MouseEvent;           // Native event
}
```

---

### OpenCloseEventArgs
Arguments passed to `open` and `close` events.

```tsx
interface OpenCloseEventArgs {
  element?: HTMLElement;        // DOM element
  event?: MouseEvent;           // Native event
}
```

---

## CSS Classes

### Button Style Classes

| Class | Purpose |
|-------|---------|
| `e-btn` | Base button styling |
| `e-primary` | Primary button (blue) |
| `e-success` | Success button (green) |
| `e-info` | Info button (cyan) |
| `e-warning` | Warning button (orange) |
| `e-danger` | Danger button (red) |
| `e-link` | Link button style |

### Button Type Classes

| Class | Purpose |
|-------|---------|
| `e-flat` | Flat button appearance |
| `e-outline` | Outlined button |
| `e-round` | Rounded button |

### Size Classes

| Class | Purpose |
|-------|---------|
| `e-small` | Small button |
| `e-large` | Large button |
| `e-block` | Full-width block button |

### State Classes

| Class | Purpose |
|-------|---------|
| `e-disabled` | Disabled state |
| `e-active` | Active/selected state |
| `e-hover` | Hover state |

### Layout Classes

| Class | Purpose |
|-------|---------|
| `e-btn-group` | Button group container |
| `e-dropdown-popup` | Dropdown menu popup |
| `e-menu-item` | Menu item styling |

---

## Type Definitions

```tsx
import { 
  SplitButtonComponent,
  ItemModel,
  IItemRendering,
  ClickEventArgs,
  SelectEventArgs,
  BeforeOpenCloseEventArgs,
  OpenCloseEventArgs
} from '@syncfusion/ej2-react-splitbuttons';
```

### SplitButtonComponent

Main component for the SplitButton.

```tsx
interface SplitButtonComponent {
  // Properties
  cssClass?: string;
  disabled?: boolean;
  enableRtl?: boolean;
  iconCss?: string;
  iconPosition?: string;
  items?: ItemModel[];
  itemTemplate?: (props: ItemModel) => ReactNode;
  title?: string;
  
  // Methods
  show(): void;
  hide(): void;
  toggle(): void;
  click(): void;
  refresh(): void;
  
  // Events
  click?: (args: ClickEventArgs) => void;
  select?: (args: SelectEventArgs) => void;
  beforeOpen?: (args: BeforeOpenCloseEventArgs) => void;
  open?: (args: OpenCloseEventArgs) => void;
  beforeClose?: (args: BeforeOpenCloseEventArgs) => void;
  close?: (args: OpenCloseEventArgs) => void;
  created?: () => void;
  destroy?: () => void;
}
```

---

## Quick Reference Tables

### Property Quick Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `cssClass` | string | `''` | CSS classes |
| `disabled` | boolean | `false` | Disable button |
| `enableRtl` | boolean | `false` | RTL support |
| `iconCss` | string | `''` | Icon class |
| `iconPosition` | string | `'Left'` | Icon position |
| `items` | ItemModel[] | `[]` | Menu items |
| `itemTemplate` | function | - | Custom item template |
| `title` | string | `''` | Tooltip text |

---

### Event Quick Reference

| Event | Triggered | Arguments |
|-------|-----------|-----------|
| `click` | Primary button clicked | ClickEventArgs |
| `select` | Menu item selected | SelectEventArgs |
| `beforeOpen` | Before menu opens | BeforeOpenCloseEventArgs |
| `open` | After menu opens | OpenCloseEventArgs |
| `beforeClose` | Before menu closes | BeforeOpenCloseEventArgs |
| `close` | After menu closes | OpenCloseEventArgs |
| `created` | Component created | void |
| `destroy` | Before component destroyed | void |

---

### Icon Position Quick Reference

| Value | Position |
|-------|----------|
| `'Left'` | Icon on left (default) |
| `'Right'` | Icon on right |
| `'Top'` | Icon on top |
| `'Bottom'` | Icon on bottom |

---

### Common Style Combinations

| Use Case | CSS Class |
|----------|-----------|
| Primary action | `e-primary` |
| Danger/Delete | `e-danger` |
| Success/Confirm | `e-success` |
| Warning/Caution | `e-warning` |
| Information | `e-info` |
| Subtle action | `e-flat e-primary` |
| Outlined button | `e-outline e-primary` |
| Rounded button | `e-round e-primary` |
| Small button | `e-small e-primary` |
| Large button | `e-large e-primary` |

---

## Usage Examples

### Complete Example with All Properties

```tsx
import React, { useRef, useState } from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function CompleteExample() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);
  const [lastAction, setLastAction] = useState('');

  const items = [
    { text: 'Save', iconCss: 'e-icons e-save', id: 'save-item' },
    { text: 'Save As', iconCss: 'e-icons e-save-as', id: 'save-as-item' },
    { separator: true },
    { text: 'Save All', iconCss: 'e-icons e-save-all', id: 'save-all-item' }
  ];

  const itemTemplate = (props: any) => {
    return <span>{props.text}</span>;
  };

  const handleClick = (args: any) => {
    setLastAction('Primary clicked');
  };

  const handleSelect = (args: any) => {
    setLastAction(`Selected: ${args.item.text}`);
  };

  const handleBeforeOpen = (args: any) => {
    console.log('Before open');
  };

  const handleOpen = (args: any) => {
    console.log('Menu opened');
  };

  return (
    <div>
      <SplitButtonComponent
        ref={splitBtnRef}
        items={items}
        cssClass="e-primary"
        disabled={false}
        enableRtl={false}
        iconCss="e-icons e-save"
        iconPosition="Left"
        itemTemplate={itemTemplate}
        title="Save options"
        click={handleClick}
        select={handleSelect}
        beforeOpen={handleBeforeOpen}
        open={handleOpen}
      >
        Save
      </SplitButtonComponent>
      <p>{lastAction}</p>
    </div>
  );
}

export default CompleteExample;
```

---

## Next Steps

- **Features** → Read [splitbutton-features.md](splitbutton-features.md) for practical examples
- **Customization** → Read [customization.md](customization.md) for advanced styling
- **Accessibility** → Read [accessibility.md](accessibility.md) for WCAG compliance
