# Navigation and Routing

## Table of Contents
- [Enable/Disable Navigation](#enabledisable-navigation)
- [URL Types](#url-types)
- [Enable Active Item Navigation](#enable-active-item-navigation)
- [Handling Item Clicks](#handling-item-clicks)
- [Open URL in New Tab](#open-url-in-new-tab)
- [Handle beforeItemRender Event](#handle-beforeitemrender-event)
- [Advanced Routing Integration](#advanced-routing-integration)

## Enable/Disable Navigation

The `enableNavigation` property controls whether breadcrumb items are clickable and navigate to their URLs.

### Navigation Disabled (Default Behavior)

When `enableNavigation={false}`, breadcrumb items are not clickable:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
        <BreadcrumbItemDirective text="Components" url="url" />
        <BreadcrumbItemDirective text="Navigations" url="url" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Display-only breadcrumbs for status pages or reporting.

### Navigation Enabled

When `enableNavigation={true}`, breadcrumb items become clickable and navigate to their URLs:

```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
    <BreadcrumbItemDirective text="Components" url="url" />
    <BreadcrumbItemDirective text="Navigations" url="url" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Important:** The last breadcrumb item (active/current page) remains non-clickable by default. Use `enableActiveItemNavigation={true}` to make it clickable.

## URL Types

The Breadcrumb component supports both relative and absolute URLs.

### Relative URLs

Relative URLs contain only the path segment:

```tsx
<BreadcrumbComponent enableNavigation={false}>
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

**When to use:** Internal navigation within your application.

### Absolute URLs

Absolute URLs contain the complete path with protocol and domain:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="url" />
    <BreadcrumbItemDirective text="Getting Started" url="url" />
    <BreadcrumbItemDirective text="Icons" url="url" />
    <BreadcrumbItemDirective text="Navigation" url="url" />
    <BreadcrumbItemDirective text="Overflow" url="url" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**When to use:** External links or cross-domain navigation.

---

## Handling Item Clicks

Use the `itemClick` event to handle breadcrumb item clicks and execute custom logic before or instead of navigation.

### Basic Item Click Handler

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbClickEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
    console.log('Clicked item:', args.item.text);
    console.log('Item URL:', args.item.url);
    console.log('Item ID:', args.item.id);
    console.log('Element:', args.element);
  };

  return (
    <BreadcrumbComponent itemClick={itemClickHandler} enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective id="home" text="Home" url="/" />
        <BreadcrumbItemDirective id="products" text="Products" url="/products" />
        <BreadcrumbItemDirective id="electronics" text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

### Cancel Navigation on Item Click

Prevent navigation for certain items or conditions:

```tsx
const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
  // Prevent navigation for restricted items
  if (args.item.text === 'Admin Only' && !userIsAdmin) {
    args.cancel = true;
    alert('You do not have access to this section');
  }
  
  // Prevent default navigation and use custom logic
  if (args.item.id === 'special-action') {
    args.cancel = true;
    // Perform custom navigation or action
    customNavigationLogic(args.item.url);
  }
};
```

### Detect Modifier Keys

Check for Ctrl+Click, Shift+Click, etc.:

```tsx
const itemClickHandler = (args: BreadcrumbClickEventArgs) => {
  const mouseEvent = args.event as MouseEvent;
  
  if (mouseEvent.ctrlKey) {
    console.log('Ctrl+Click detected');
    // Open in new window
    window.open(args.item.url);
    args.cancel = true; // Prevent default navigation
  }
  
  if (mouseEvent.shiftKey) {
    console.log('Shift+Click detected');
  }
  
  if (mouseEvent.metaKey) {
    console.log('Meta/Cmd+Click detected (Mac)');
  }
};
```

---

## Enable Active Item Navigation

By default, the last breadcrumb item (active item representing the current page) is not clickable. Set `enableActiveItemNavigation={true}` to make it clickable:

```tsx
<BreadcrumbComponent enableNavigation={true} enableActiveItemNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="url" />
    <BreadcrumbItemDirective text="Getting Started" url="url" />
    <BreadcrumbItemDirective text="Icons" url="url" />
    <BreadcrumbItemDirective text="Navigation" url="url" />
    <BreadcrumbItemDirective text="Overflow" url="url" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Allow users to refresh or re-navigate to the current page.

## Open URL in New Tab

Use the `beforeItemRender` event to set the target property to "_blank" for opening URLs in new tabs:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
    if (args.element.children[0]) {
      args.element.children[0].target = "_blank";
    }
  }

  return (
    <BreadcrumbComponent enableActiveItemNavigation={true} beforeItemRender={beforeItemRenderHandler}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="url" />
        <BreadcrumbItemDirective text="Getting Started" url="url" />
        <BreadcrumbItemDirective text="Icons" url="url" />
        <BreadcrumbItemDirective text="Navigation" url="url" />
        <BreadcrumbItemDirective text="Overflow" url="url" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**How it works:**
- The `beforeItemRender` event fires before each breadcrumb item is rendered
- Access the DOM element via `args.element`
- Set `target="_blank"` on the anchor element to open URLs in a new tab

**Tip:** You can add other modifications like `rel="noopener noreferrer"` for security:

```tsx
function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
  if (args.element.children[0]) {
    args.element.children[0].target = "_blank";
    args.element.children[0].rel = "noopener noreferrer";
  }
}
```

## Handle beforeItemRender Event

The `beforeItemRender` event fires before each breadcrumb item is rendered, allowing you to modify items dynamically:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
    // Access the breadcrumb item
    console.log('Item text:', args.item.text);
    
    // Access the DOM element
    console.log('Element:', args.element);
    
    // Add custom classes or attributes
    args.element.classList.add('custom-breadcrumb-item');
    
    // Modify styling
    if (args.item.text === 'Home') {
      args.element.style.fontWeight = 'bold';
    }
  }

  return (
    <BreadcrumbComponent beforeItemRender={beforeItemRenderHandler}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Common Use Cases:**
- Add CSS classes conditionally
- Modify styling based on item properties
- Change URLs dynamically
- Add accessibility attributes
- Set target="_blank" for external links

## Advanced Routing Integration

For single-page applications using routing libraries like React Router:

```tsx
import { useNavigate } from 'react-router-dom';
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function Breadcrumb() {
  const navigate = useNavigate();

  const handleClick = (url: string) => {
    navigate(url);
  };

  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective text="Home" url="/" />
        <BreadcrumbItemDirective text="Products" url="/products" />
        <BreadcrumbItemDirective text="Electronics" url="/products/electronics" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Best Practice:** Set `enableNavigation={true}` and let the browser handle navigation with standard URLs. React Router will automatically intercept navigation for single-page app routing.
