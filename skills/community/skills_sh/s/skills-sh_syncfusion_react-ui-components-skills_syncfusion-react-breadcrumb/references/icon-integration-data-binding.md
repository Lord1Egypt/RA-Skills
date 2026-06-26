# Icon Integration and Data Binding

## Table of Contents
- [Loading Icons](#loading-icons)
- [Icon Types](#icon-types)
- [Icon Positioning](#icon-positioning)
- [Data Binding Methods](#data-binding-methods)
- [URL-Based Item Generation](#url-based-item-generation)

## Loading Icons

The `iconCss` property enables adding icons to breadcrumb items. Icons provide visual context and enhance navigation understanding.

### Font Icons

Use Syncfusion font icons by setting the `iconCss` property with the `e-icons` class and icon name:

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

**Common Syncfusion Icons:**
- `e-icons e-home` - Home icon
- `e-bicons e-folder` - Folder icon
- `e-bicons e-file` - File icon
- `e-bicons e-download` - Download icon
- `e-bicons e-settings` - Settings icon

**Default Position:** Icons appear to the left of the item text.

### Image Icons

Add images to breadcrumb items using the `iconCss` property with an image class:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective iconCss="e-image-home" url="url" />
        <BreadcrumbItemDirective text="Components" url="url" />
        <BreadcrumbItemDirective text="Navigations" url="url" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Define Image Classes in CSS:**

```css
.e-image-home {
  background-image: url('./assets/home.png');
  background-size: 16px 16px;
  width: 16px;
  height: 16px;
  display: inline-block;
  margin-right: 8px;
}
```

### SVG Images

Add SVG graphics to breadcrumb items:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective iconCss="e-svg-home" url="url" />
        <BreadcrumbItemDirective text="Components" url="url" />
        <BreadcrumbItemDirective text="Navigations" url="url" />
        <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

**Define SVG Classes in CSS:**

```css
.e-svg-home::before {
  content: url('data:image/svg+xml;utf8,<svg xmlns="url" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>');
  margin-right: 8px;
}
```

## Icon Types

The Breadcrumb component supports multiple icon classification systems:

### File System Icons (`e-bicons`)

File-related icons for file system navigation:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Program Files" iconCss="e-bicons e-folder" />
    <BreadcrumbItemDirective text="Services" iconCss="e-bicons e-folder" />
    <BreadcrumbItemDirective text="Config.json" iconCss="e-bicons e-file" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Utility Icons (`e-icons`)

General-purpose icons for various navigation scenarios:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" />
    <BreadcrumbItemDirective iconCss="e-icons e-settings" text="Settings" />
    <BreadcrumbItemDirective iconCss="e-icons e-bell" text="Notifications" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

## Icon Positioning

Icons can be positioned to the left (default) or right of item text.

### Icon on Left (Default)

Icons are positioned to the left of the item text by default:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Program Files" iconCss="e-bicons e-folder" />
    <BreadcrumbItemDirective text="Services" iconCss="e-bicons e-folder" />
    <BreadcrumbItemDirective text="Config.json" iconCss="e-bicons e-file" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Icon on Right

Add the `e-icon-right` class to position icons to the right using the `beforeItemRender` event:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
    if (args.element) {
      args.element.classList.add('e-icon-right');
    }
  }

  return (
    <div>
      <div><b>Icon Position - Left (Default)</b></div>
      <BreadcrumbComponent enableNavigation={false}>
        <BreadcrumbItemsDirective>
          <BreadcrumbItemDirective text="Program Files" iconCss="e-bicons e-folder" />
          <BreadcrumbItemDirective text="Services" iconCss="e-bicons e-folder" />
          <BreadcrumbItemDirective text="Config.json" iconCss="e-bicons e-file" />
        </BreadcrumbItemsDirective>
      </BreadcrumbComponent>

      <br />
      <br />

      <div><b>Icon Position - Right</b></div>
      <BreadcrumbComponent beforeItemRender={beforeItemRenderHandler} enableNavigation={false}>
        <BreadcrumbItemsDirective>
          <BreadcrumbItemDirective text="Program Files" iconCss="e-bicons e-folder" />
          <BreadcrumbItemDirective text="Services" iconCss="e-bicons e-folder" />
          <BreadcrumbItemDirective text="Config.json" iconCss="e-bicons e-file" />
        </BreadcrumbItemsDirective>
      </BreadcrumbComponent>
    </div>
  );
}
```

### Icon Only

Display only icons without text by omitting the `text` property:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" />
    <BreadcrumbItemDirective iconCss="e-bicons e-folder" />
    <BreadcrumbItemDirective iconCss="e-bicons e-file" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Use Case:** Compact breadcrumbs where icons are self-explanatory.

### Icon for First Item Only

Show icon only on the first item:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
    <BreadcrumbItemDirective text="Components" url="url" />
    <BreadcrumbItemDirective text="Navigations" url="url" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

## Data Binding Methods

### Items as Tag Directives (Recommended)

Use `BreadcrumbItemsDirective` and `BreadcrumbItemDirective` tags to declaratively bind items:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" url="url" />
    <BreadcrumbItemDirective text="Components" url="url" />
    <BreadcrumbItemDirective text="Navigations" url="url" />
    <BreadcrumbItemDirective text="Breadcrumb" url="./breadcrumb/default" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

**Advantages:**
- Declarative and readable
- TypeScript support
- Full IDE autocomplete

## URL-Based Item Generation

The Breadcrumb component can automatically generate items from URL paths.

### Current URL

When no items are provided, the breadcrumb generates items from the current page URL:

```tsx
<BreadcrumbComponent enableNavigation={false}></BreadcrumbComponent>
```

**Example:** If the URL is `/products/electronics/smartphones`, the breadcrumb automatically generates:
- "products"
- "electronics"
- "smartphones"

**Note:** This approach is useful when breadcrumb items match the URL structure.

### Static URL

Generate breadcrumb items from a provided URL using the `url` property:

```tsx
<BreadcrumbComponent 
  enableNavigation={false} 
  url="url"
>
</BreadcrumbComponent>
```

This generates breadcrumb items from the URL path segments.

### Customize Generated Items

Use the `beforeItemRender` event to customize text of auto-generated breadcrumb items:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import { BreadcrumbBeforeItemRenderEventArgs } from '@syncfusion/ej2-navigations';

export default function App() {
  function beforeItemRenderHandler(args: BreadcrumbBeforeItemRenderEventArgs): void {
    if (args.item.text === 'bind-to-location') {
      args.item.text = 'location';
    }
  }

  return (
    <BreadcrumbComponent 
      enableActiveItemNavigation={true} 
      url="url"
      beforeItemRender={beforeItemRenderHandler}
    >
    </BreadcrumbComponent>
  );
}
```

**Use Case:** Format auto-generated items for better readability (e.g., convert `bind-to-location` to `location`).

## Combining Icons and Data Binding

Combine static items with dynamic icons:

```tsx
export default function App() {
  interface BreadcrumbItem {
    text: string;
    url: string;
    iconCss?: string;
  }

  const items: BreadcrumbItem[] = [
    { text: 'Home', url: '/', iconCss: 'e-icons e-home' },
    { text: 'Products', url: '/products' },
    { text: 'Electronics', url: '/products/electronics' },
  ];

  return (
    <BreadcrumbComponent enableNavigation={true}>
      <BreadcrumbItemsDirective>
        {items.map((item, index) => (
          <BreadcrumbItemDirective
            key={index}
            text={item.text}
            url={item.url}
            iconCss={item.iconCss}
          />
        ))}
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

This pattern allows dynamic breadcrumb generation with per-item icon configuration.
