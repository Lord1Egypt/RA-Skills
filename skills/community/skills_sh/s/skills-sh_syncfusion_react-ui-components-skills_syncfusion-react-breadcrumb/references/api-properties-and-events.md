# API Properties and Events Reference

## Table of Contents
- [BreadcrumbComponent Properties](#breadcrumbcomponent-properties)
- [BreadcrumbItem Properties](#breadcrumbitem-properties)
- [Component Events](#component-events)
- [Event Arguments](#event-arguments)
- [Overflow Modes](#overflow-modes)

---

## BreadcrumbComponent Properties

### activeItem
**Type:** `string`  
**Default:** N/A

Specifies the URL of the active Breadcrumb item. Use this property to programmatically set which breadcrumb item is currently active.

**Example:**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { useState } from 'react';

export default function App() {
  const [active, setActive] = useState('/products');

  return (
    <BreadcrumbComponent activeItem={active} enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

### cssClass
**Type:** `string`  
**Default:** N/A

Defines one or more CSS classes separated by spaces in the Breadcrumb element. Use this to apply custom styling to the entire breadcrumb container.

**Example:**
```tsx
<BreadcrumbComponent cssClass="custom-breadcrumb highlight-nav">
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="Products" url="/products" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**CSS:**
```css
.custom-breadcrumb {
  background-color: #f5f5f5;
  padding: 12px 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.highlight-nav .e-breadcrumb-item a {
  color: #0078d4;
  font-weight: 500;
}
```

---

### disabled
**Type:** `boolean`  
**Default:** `false`

Enable or disable the entire breadcrumb component. When set to `true`, the breadcrumb becomes inactive and non-interactive.

**Example:**
```tsx
import { useState } from 'react';
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  const [isDisabled, setIsDisabled] = useState(false);

  return (
    <div>
      <button onClick={() => setIsDisabled(!isDisabled)}>
        Toggle Breadcrumb Disabled
      </button>
      
      <BreadcrumbComponent disabled={isDisabled} enableNavigation={true}>
        <BreadcrumbItemsDirective>
          <BreadcrumbItemDirective text="Home" url="/" />
          <BreadcrumbItemDirective text="Products" url="/products" />
          <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
        </BreadcrumbItemsDirective>
      </BreadcrumbComponent>
    </div>
  );
}
```

---

### enableNavigation
**Type:** `boolean`  
**Default:** `true`

Enable or disable item navigation. When set to `false`, breadcrumb items are not clickable and navigation is prevented.

**Example:**
```tsx
// Display-only breadcrumb (navigation disabled)
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="Products" url="/products" />
    <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### enableActiveItemNavigation
**Type:** `boolean`  
**Default:** `false`

Enable or disable navigation on the active item (last breadcrumb). When set to `true`, the last breadcrumb item becomes clickable.

**Example:**
```tsx
<BreadcrumbComponent enableNavigation={true} enableActiveItemNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="Products" url="/products" />
    <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`

Enable or disable rendering the component in right-to-left direction. Set to `true` for RTL languages like Arabic, Hebrew, or Persian.

**Example:**
```tsx
<BreadcrumbComponent enableRtl={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="الصفحة الرئيسية" url="/" />
    <BreadcrumbItemDirective text="المنتجات" url="/products" />
    <BreadcrumbItemDirective text="الإلكترونيات" url="/products/electronics" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### items
**Type:** `BreadcrumbItemModel[]`  
**Default:** N/A

Defines the list of Breadcrumb items. Can be set programmatically to dynamically generate breadcrumbs.

**Example:**
```tsx
import { useState } from 'react';
import { BreadcrumbComponent } from '@syncfusion/ej2-react-navigations';

interface BreadcrumbItemModel {
  text?: string;
  url?: string;
  iconCss?: string;
  disabled?: boolean;
  id?: string;
}

export default function App() {
  const breadcrumbItems: BreadcrumbItemModel[] = [
    { text: 'Home', url: '/' },
    { text: 'Products', url: '/products' },
    { text: 'Electronics', url: '/products/electronics' },
  ];

  return (
    <BreadcrumbComponent items={breadcrumbItems} enableNavigation={true}>
    </BreadcrumbComponent>
  );
}
```

---

### maxItems
**Type:** `number`  
**Default:** N/A

Specifies the maximum number of breadcrumb items to display before triggering overflow behavior. Additional items are handled according to the `overflowMode` setting.

**Example:**
```tsx
<BreadcrumbComponent maxItems={3} overflowMode="Menu" enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Level 1" url="/" />
    <BreadcrumbItemDirective text="Level 2" url="/l2" />
    <BreadcrumbItemDirective text="Level 3" url="/l2/l3" />
    <BreadcrumbItemDirective text="Level 4" url="/l2/l3/l4" />
    <BreadcrumbItemDirective text="Level 5" url="/l2/l3/l4/l5" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### overflowMode
**Type:** `string | BreadcrumbOverflowMode`  
**Default:** `'Menu'`

Specifies the overflow mode when breadcrumb items exceed `maxItems`. Accepted values:
- **Menu**: Shows breadcrumbs that fit + remaining items in dropdown
- **Collapsed**: Shows first and last items with ellipsis for middle items
- **Scroll**: Shows HTML scrollbar when width exceeds container
- **Wrap**: Wraps items to multiple lines
- **Hidden**: Shows fitting items, hides rest (visible on navigation)
- **None**: Shows all items on single line

**Example (Menu Mode - Default):**
```tsx
<BreadcrumbComponent maxItems={3} overflowMode="Menu" enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="Folder1" url="/f1" />
    <BreadcrumbItemDirective text="Folder2" url="/f1/f2" />
    <BreadcrumbItemDirective text="Folder3" url="/f1/f2/f3" />
    <BreadcrumbItemDirective text="Folder4" url="/f1/f2/f3/f4" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Example (Collapsed Mode):**
```tsx
<BreadcrumbComponent maxItems={3} overflowMode="Collapsed" enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="Folder1" url="/f1" />
    <BreadcrumbItemDirective text="Folder2" url="/f1/f2" />
    <BreadcrumbItemDirective text="Folder3" url="/f1/f2/f3" />
    <BreadcrumbItemDirective text="Folder4" url="/f1/f2/f3/f4" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Example (Scroll Mode):**
```tsx
<BreadcrumbComponent overflowMode="Scroll" enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="VeryLongFolderName1" url="/vlfn1" />
    <BreadcrumbItemDirective text="VeryLongFolderName2" url="/vlfn1/vlfn2" />
    <BreadcrumbItemDirective text="VeryLongFolderName3" url="/vlfn1/vlfn2/vlfn3" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### itemTemplate
**Type:** `string | Function`  
**Default:** N/A

Specifies a custom template for breadcrumb items. Can be a template string or a function returning JSX.

**Example (Function Template):**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  const itemTemplate = (data: any): JSX.Element => {
    return (
      <div style={{ padding: '4px 8px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <strong>{data.text}</strong>
      </div>
    );
  };

  return (
    <BreadcrumbComponent itemTemplate={itemTemplate}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

### separatorTemplate
**Type:** `string | Function`  
**Default:** N/A

Specifies a custom template for separators between breadcrumb items.

**Example (Function Template with Custom Icon):**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  const separatorTemplate = (): JSX.Element => {
    return (
      <span className="e-icons e-arrow" style={{ margin: '0 8px' }}></span>
    );
  };

  return (
    <BreadcrumbComponent separatorTemplate={separatorTemplate}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

### url
**Type:** `string`  
**Default:** N/A

Defines a URL from which breadcrumb items are automatically generated. If not provided and no items are specified, the current page URL is used.

**Example (Static URL):**
```tsx
<BreadcrumbComponent 
  url="url" 
  enableNavigation={false}
>
</BreadcrumbComponent>
```

This generates breadcrumbs:
- products
- electronics
- phones

**Example (Current Page URL):**
```tsx
// If current URL is /admin/users/profile, breadcrumbs are auto-generated
<BreadcrumbComponent enableNavigation={false}></BreadcrumbComponent>
```

---

## BreadcrumbItem Properties

### disabled
**Type:** `boolean`  
**Default:** `false`

Enable or disable an individual breadcrumb item. When set to `true`, that specific item becomes inactive.

**Example:**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" disabled={false} />
        <BreadcrumbItemDirective text="Discontinued" url="/products/discontinued" disabled={true} />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" disabled={false} />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

### iconCss
**Type:** `string`  
**Default:** `null`

Defines CSS class(es) for the breadcrumb item icon. Supports Syncfusion icons, custom images, or SVG.

**Example (Font Icons):**
```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" text="Home" url="/" />
    <BreadcrumbItemDirective iconCss="e-bicons e-folder" text="Folder" url="/folder" />
    <BreadcrumbItemDirective iconCss="e-bicons e-file" text="File" url="/file" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Example (Image Icon):**
```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="custom-icon-home" text="Home" url="/" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**CSS:**
```css
.custom-icon-home {
  background-image: url('./assets/home.png');
  background-size: 16px 16px;
  width: 16px;
  height: 16px;
  display: inline-block;
  margin-right: 8px;
}
```

---

### id
**Type:** `string`  
**Default:** `''`

Specifies a unique identifier for the breadcrumb item. Useful for identifying items in event handlers or dynamic updates.

**Example:**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbClickEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  const handleItemClick = (args: BreadcrumbClickEventArgs) => {
    console.log('Clicked item ID:', args.item.id);
  };

  return (
    <BreadcrumbComponent itemClick={handleItemClick} enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective id="home-item" text="Home" url="/" />
        <BreadcrumbItemDirective id="products-item" text="Products" url="/products" />
        <BreadcrumbItemDirective id="electronics-item" text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

### text
**Type:** `string`  
**Default:** `''`

Specifies the display text content of the breadcrumb item.

**Example:**
```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" />
    <BreadcrumbItemDirective text="User Profile" url="/profile" />
    <BreadcrumbItemDirective text="Settings" url="/profile/settings" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

### url
**Type:** `string`  
**Default:** `''`

Specifies the URL for the breadcrumb item. Used for navigation when `enableNavigation` is `true`.

**Example (Relative URLs):**
```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Products" url="./products" />
    <BreadcrumbItemDirective text="Electronics" url="./products/electronics" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Example (Absolute URLs):**
```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="url" />
    <BreadcrumbItemDirective text="Products" url="url" />
    <BreadcrumbItemDirective text="Electronics" url="url" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

---

## Component Events

### beforeItemRender
**Type:** `EmitType<BreadcrumbBeforeItemRenderEventArgs>`

Triggers before rendering each breadcrumb item. Use this event to customize item rendering or cancel rendering.

**Event Arguments:**
- `cancel` (boolean): Set to `true` to cancel the item rendering
- `element` (HTMLElement): The DOM element of the breadcrumb item
- `item` (BreadcrumbItemModel): The breadcrumb item data
- `name` (string): Event name

**Example (Modify Item Classes):**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  const beforeItemRenderHandler = (args: BreadcrumbBeforeItemRenderEventArgs) => {
    // Add custom class to all items
    args.element.classList.add('custom-item-class');
    
    // Add special styling to home item
    if (args.item.text === 'Home') {
      args.element.style.fontWeight = 'bold';
      args.element.classList.add('highlight-home');
    }
  };

  return (
    <BreadcrumbComponent beforeItemRender={beforeItemRenderHandler} enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Example (Cancel Rendering):**
```tsx
const beforeItemRenderHandler = (args: BreadcrumbBeforeItemRenderEventArgs) => {
  // Cancel rendering of disabled items
  if (args.item.disabled) {
    args.cancel = true;
  }
};
```

**Example (Open URL in New Tab):**
```tsx
const beforeItemRenderHandler = (args: BreadcrumbBeforeItemRenderEventArgs) => {
  if (args.element.children[0]) {
    args.element.children[0].target = "_blank";
    args.element.children[0].rel = "noopener noreferrer";
  }
};
```

---

### itemClick
**Type:** `EmitType<BreadcrumbClickEventArgs>`

Triggers when a breadcrumb item is clicked.

**Event Arguments:**
- `cancel` (boolean): Set to `true` to cancel the click action
- `element` (HTMLElement): The DOM element of the clicked item
- `event` (Event): The click event object
- `item` (BreadcrumbItemModel): The clicked breadcrumb item data
- `name` (string): Event name

**Example (Handle Item Click):**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbClickEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
    console.log('Clicked item:', args.item.text);
    console.log('Item URL:', args.item.url);
    console.log('Item element:', args.element);
  };

  return (
    <BreadcrumbComponent itemClick={itemClickHandler} enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Example (Cancel Navigation):**
```tsx
const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
  // Prevent navigation for certain items
  if (args.item.text === 'Restricted') {
    args.cancel = true;
    console.log('Navigation cancelled for restricted item');
  }
};
```

**Example (Log Native Click Event):**
```tsx
const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
  console.log('Native event:', args.event);
  console.log('Was ctrl+click:', (args.event as MouseEvent).ctrlKey);
  console.log('Mouse button:', (args.event as MouseEvent).button);
};
```

---

### created
**Type:** `EmitType<Event>`

Triggers once the component rendering is completed. Use this to perform initialization tasks or access the component.

**Example:**
```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { useRef } from 'react';

export default function App() {
  const breadcrumbRef = useRef<any>(null);

  const handleCreated = () => {
    console.log('Breadcrumb component created successfully');
    
    // Access component instance
    if (breadcrumbRef.current) {
      console.log('Component items:', breadcrumbRef.current.items);
      console.log('Component disabled:', breadcrumbRef.current.disabled);
    }
  };

  return (
    <BreadcrumbComponent 
      ref={breadcrumbRef}
      created={handleCreated}
      enableNavigation={false}
    >
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

---

## Event Arguments

### BreadcrumbBeforeItemRenderEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | boolean | Set to `true` to prevent the item from rendering |
| `element` | HTMLElement | The DOM element of the breadcrumb item |
| `item` | BreadcrumbItemModel | The breadcrumb item object being rendered |
| `name` | string | Name of the event (e.g., 'beforeItemRender') |

### BreadcrumbClickEventArgs

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | boolean | Set to `true` to cancel the click action |
| `element` | HTMLElement | The DOM element of the clicked item |
| `event` | Event | The native click event object |
| `item` | BreadcrumbItemModel | The clicked breadcrumb item object |
| `name` | string | Name of the event (e.g., 'itemClick') |

---

## Overflow Modes

Complete reference for all overflow modes:

| Mode | Behavior | Use Case |
|------|----------|----------|
| **Menu** (Default) | Shows items that fit, remaining items in dropdown submenu | Efficient space usage, keep all items accessible |
| **Collapsed** | Shows first and last items, middle items in collapsed icon | Very narrow containers |
| **Scroll** | Shows HTML scrollbar when content exceeds container width | All items visible horizontally scrollable |
| **Wrap** | Wraps items to multiple lines | Responsive design, mobile-friendly |
| **Hidden** | Shows fitting items, hides rest (visible on navigation) | Deep hierarchies, navigate to reveal |
| **None** | Shows all items on single line | Sufficient container space |

---

## Summary Table: All Component Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `activeItem` | string | N/A | URL of active breadcrumb item |
| `cssClass` | string | N/A | CSS classes for breadcrumb container |
| `disabled` | boolean | false | Disable entire component |
| `enableNavigation` | boolean | true | Allow item navigation |
| `enableActiveItemNavigation` | boolean | false | Make last item clickable |
| `enableRtl` | boolean | false | Render in RTL direction |
| `items` | BreadcrumbItemModel[] | N/A | Breadcrumb items array |
| `maxItems` | number | N/A | Maximum items before overflow |
| `overflowMode` | string | 'Menu' | Overflow behavior mode |
| `itemTemplate` | Function/string | N/A | Custom item template |
| `separatorTemplate` | Function/string | N/A | Custom separator template |
| `url` | string | N/A | URL to auto-generate items from |

---

## Summary Table: All Item Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `disabled` | boolean | false | Disable individual item |
| `iconCss` | string | null | Icon CSS classes |
| `id` | string | '' | Unique item identifier |
| `text` | string | '' | Display text |
| `url` | string | '' | Navigation URL |

---

## All Events Summary

| Event | Fires When | Arguments |
|-------|-----------|-----------|
| `beforeItemRender` | Before each item renders | cancel, element, item, name |
| `itemClick` | When an item is clicked | cancel, element, event, item, name |
| `created` | Component rendering completes | Event |
