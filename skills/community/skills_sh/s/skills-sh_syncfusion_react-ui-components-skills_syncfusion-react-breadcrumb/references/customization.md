# Customization and Templates

## Table of Contents
- [Overflow Modes](#overflow-modes)
- [Item-Level Disabling](#item-level-disabling)
- [Item Templates](#item-templates)
- [Separator Templates](#separator-templates)
- [Managing Maximum Items](#managing-maximum-items)
- [Styling and CSS Classes](#styling-and-css-classes)

## Overflow Modes

The `overflowMode` property controls how breadcrumb items are displayed when they exceed available container space. Use `maxItems` to specify the maximum number of items to display.

### Menu Mode (Default)

Menu mode displays the maximum number of items that fit in the container and places remaining items in a dropdown menu:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  function breadcrumbTemplate(): JSX.Element {
    return (
      <span className="e-bicons e-arrow"></span>
    );
  }

  return (
    <BreadcrumbComponent maxItems={3} enableNavigation={false} overflowMode='Menu' separatorTemplate={breadcrumbTemplate}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="../" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
        <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
        <BreadcrumbItemDirective text="Icons" url="./breadcrumb/icons" />
        <BreadcrumbItemDirective text="Navigation" url="./breadcrumb/navigation" />
        <BreadcrumbItemDirective text="Overflow" url="./breadcrumb/overflow" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Space-constrained layouts where you need efficient space utilization while maintaining accessibility to all items.

### Collapsed Mode

Collapsed mode displays the first and last items while hiding intermediate items behind a collapsed icon (ellipsis). Click the ellipsis to reveal hidden items:

```tsx
<BreadcrumbComponent maxItems={3} enableNavigation={false} overflowMode='Collapsed' separatorTemplate={breadcrumbTemplate}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
    <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
    <BreadcrumbItemDirective text="Icons" url="./breadcrumb/icons" />
    <BreadcrumbItemDirective text="Navigation" url="./breadcrumb/navigation" />
    <BreadcrumbItemDirective text="Overflow" url="./breadcrumb/overflow" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Very narrow containers where showing first and last items is most important.

### Scroll Mode

Scroll mode displays a horizontal scrollbar when breadcrumb width exceeds container space:

```tsx
<BreadcrumbComponent maxItems={3} enableNavigation={false} overflowMode='Scroll' separatorTemplate={breadcrumbTemplate}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
    <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
    <BreadcrumbItemDirective text="Icons" url="./breadcrumb/icons" />
    <BreadcrumbItemDirective text="Navigation" url="./breadcrumb/navigation" />
    <BreadcrumbItemDirective text="Overflow" url="./breadcrumb/overflow" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** When you want all items visible but need horizontal scrolling.

### Wrap Mode

Wrap mode automatically wraps breadcrumb items to multiple lines when total width exceeds container space:

```tsx
<BreadcrumbComponent maxItems={3} enableNavigation={false} overflowMode='Wrap' separatorTemplate={breadcrumbTemplate}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
    <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
    <BreadcrumbItemDirective text="Icons" url="./breadcrumb/icons" />
    <BreadcrumbItemDirective text="Navigation" url="./breadcrumb/navigation" />
    <BreadcrumbItemDirective text="Overflow" url="./breadcrumb/overflow" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Mobile-responsive breadcrumbs that can flow to multiple lines.

---

## Item-Level Disabling

Individual breadcrumb items can be disabled independently using the `disabled` property. Disabled items are non-clickable and visually distinguished from active items.

### Disabling Specific Items

Use the `disabled` property on `BreadcrumbItemDirective` to disable individual items:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" disabled={false} />
        <BreadcrumbItemDirective text="Products" url="/products" disabled={false} />
        <BreadcrumbItemDirective text="Discontinued" url="/products/discontinued" disabled={true} />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" disabled={false} />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Result:** The "Discontinued" item is non-clickable and visually grayed out.

### Dynamic Item Disabling

Disable items programmatically based on conditions:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { useState } from 'react';

export default function App() {
  const [userRole, setUserRole] = useState('viewer'); // 'viewer' or 'admin'

  const isAdminOnly = userRole !== 'admin';

  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" disabled={false} />
        <BreadcrumbItemDirective text="Dashboard" url="/dashboard" disabled={false} />
        <BreadcrumbItemDirective text="Admin Panel" url="/admin" disabled={isAdminOnly} />
        <BreadcrumbItemDirective text="Settings" url="/admin/settings" disabled={isAdminOnly} />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Role-based navigation where certain breadcrumb paths are only accessible to specific users.

### Styling Disabled Items

Disabled items automatically receive the `aria-disabled` attribute and can be styled with CSS:

```css
/* Style disabled breadcrumb items */
.e-breadcrumb-item[aria-disabled="true"] {
  opacity: 0.6;
  cursor: not-allowed;
  color: #999;
}

.e-breadcrumb-item[aria-disabled="true"] a {
  pointer-events: none;
  text-decoration: line-through;
}
```

### Combining with beforeItemRender

Use `beforeItemRender` event to add custom styling to disabled items:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  const beforeItemRenderHandler = (args: BreadcrumbBeforeItemRenderEventArgs) => {
    if (args.item.disabled) {
      args.element.classList.add('disabled-breadcrumb');
      args.element.style.opacity = '0.5';
      args.element.style.backgroundColor = '#f0f0f0';
    }
  };

  return (
    <BreadcrumbComponent 
      enableNavigation={true}
      beforeItemRender={beforeItemRenderHandler}
    >
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" disabled={false} />
        <BreadcrumbItemDirective text="Premium Feature" url="/premium" disabled={true} />
        <BreadcrumbItemDirective text="Settings" url="/settings" disabled={false} />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

### Hidden Mode

Hidden mode displays maximum items that fit and completely hides remaining items. Hidden items become visible when navigating to previous levels:

```tsx
<BreadcrumbComponent maxItems={3} enableNavigation={false} overflowMode='Hidden' separatorTemplate={breadcrumbTemplate}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
    <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
    <BreadcrumbItemDirective text="Icons" url="./breadcrumb/icons" />
    <BreadcrumbItemDirective text="Navigation" url="./breadcrumb/navigation" />
    <BreadcrumbItemDirective text="Overflow" url="./breadcrumb/overflow" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Deeply nested navigation where older items are hidden until you navigate back.

### None Mode

None mode displays all items on a single line without any overflow handling:

```tsx
<BreadcrumbComponent enableNavigation={false} overflowMode='None'>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb" />
    <BreadcrumbItemDirective text="Default" url="./breadcrumb/default-functionalities" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Containers with sufficient space or when maxItems is not set.

## Item Templates

Customize individual breadcrumb items using the `itemTemplate` property:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { ChipListComponent, ChipsDirective, ChipDirective } from '@syncfusion/ej2-react-buttons';

export default function App() {
  function chipTemplate(data: any): JSX.Element {
    return (
      <ChipListComponent>
        <ChipsDirective>
          <ChipDirective text={data.text}></ChipDirective>
        </ChipsDirective>
      </ChipListComponent>
    );
  }

  return (
    <BreadcrumbComponent cssClass="e-breadcrumb-chips" itemTemplate={chipTemplate}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Cart" />
        <BreadcrumbItemDirective text="Billing" />
        <BreadcrumbItemDirective text="Shipping" />
        <BreadcrumbItemDirective text="Payment" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Shopping cart navigation steps with chip-style UI.

### Conditional Item Templates

Apply custom styling to specific items based on conditions:

```tsx
export default function App() {
  function specificItemTemplate(data: any): JSX.Element {
    return (
      <div>
        {data.text === "Breadcrumb" ? (
          <span>
            <span className="e-searchfor-text">
              <span style={{ marginRight: "5px" }}>Search for:</span>
              <a className="e-breadcrumb-text" href={data.url} onClick={() => { return false }}>
                {data.text}
              </a>
            </span>
          </span>
        ) : (
          <a className="e-breadcrumb-text" href={data.url} onClick={() => { return false }}>
            {data.text}
          </a>
        )}
      </div>
    );
  }

  return (
    <BreadcrumbComponent 
      itemTemplate={specificItemTemplate} 
      cssClass="e-specific-item-template"
      enableNavigation={false}
    >
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="url" />
        <BreadcrumbItemDirective text="Components" url="url" />
        <BreadcrumbItemDirective text="Navigations" url="url" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Highlight specific breadcrumb items with custom styling or labels.

## Separator Templates

Customize the separators between breadcrumb items using the `separatorTemplate` property:

```tsx
export default function App() {
  function arrowSeparatorTemplate(): JSX.Element {
    return (
      <span className="e-icons e-arrow"></span>
    );
  }

  return (
    <BreadcrumbComponent separatorTemplate={arrowSeparatorTemplate}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Cart" />
        <BreadcrumbItemDirective text="Billing" />
        <BreadcrumbItemDirective text="Shipping" />
        <BreadcrumbItemDirective text="Payment" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Available Separator Icons:**
- `e-icons e-arrow` - Arrow separator
- `e-icons e-chevron-right` - Chevron separator
- `e-icons e-slash` - Slash separator
- Custom HTML or JSX elements

**Use Case:** Create visually distinctive navigation paths with custom separators.

## Managing Maximum Items

The `maxItems` property controls the maximum number of breadcrumb items displayed before overflow behavior is triggered:

```tsx
// Display maximum 5 items before showing overflow
<BreadcrumbComponent maxItems={5} overflowMode='Menu' enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Level 1" />
    <BreadcrumbItemDirective text="Level 2" />
    <BreadcrumbItemDirective text="Level 3" />
    <BreadcrumbItemDirective text="Level 4" />
    <BreadcrumbItemDirective text="Level 5" />
    <BreadcrumbItemDirective text="Level 6" />
    <BreadcrumbItemDirective text="Level 7" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Common Settings:**
- `maxItems={2}` - Very compact, ideal for mobile
- `maxItems={3}` - Compact, common for tablets
- `maxItems={5}` - Default, common for desktop
- `maxItems={10}` - Spacious, shows most items

## Styling and CSS Classes

Add custom CSS classes using the `cssClass` property:

```tsx
export default function App() {
  return (
    <BreadcrumbComponent 
      cssClass="custom-breadcrumb"
      enableNavigation={false}
    >
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" />
        <BreadcrumbItemDirective text="Products" />
        <BreadcrumbItemDirective text="Electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**In your CSS file:**

```css
.custom-breadcrumb {
  background-color: #f5f5f5;
  padding: 12px 16px;
  border-radius: 4px;
}

.custom-breadcrumb .e-breadcrumb-item {
  font-size: 14px;
  color: #333;
}

.custom-breadcrumb .e-breadcrumb-item a {
  color: #0078d4;
  text-decoration: none;
}

.custom-breadcrumb .e-breadcrumb-item a:hover {
  text-decoration: underline;
}
```

**Common Styling:**
- Background color and padding
- Font size and weight
- Link colors and hover states
- Separator styling
- Active item highlighting
