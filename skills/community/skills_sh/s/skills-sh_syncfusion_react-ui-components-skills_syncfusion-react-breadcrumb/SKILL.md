---
name: syncfusion-react-breadcrumb
description: Implement and configure Syncfusion React Breadcrumb component for navigation paths, routing, and site hierarchy. Use this skill whenever users need breadcrumb navigation, want to create hierarchical navigation paths, display location breadcrumbs, handle navigation between pages, customize overflow behaviors, or integrate breadcrumbs with routing libraries.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation Components"
---

# Syncfusion React Breadcrumb Component Skill

## Table of Contents
1. [When to Use This Skill](#when-to-use-this-skill)
2. [Component Overview](#component-overview)
3. [Documentation and Navigation Guide](#documentation-and-navigation-guide)
4. [Quick Start Example](#quick-start-example)
5. [Common Patterns](#common-patterns)
6. [Key Props Reference](#key-props-reference)
7. [Common Use Cases](#common-use-cases)

## When to Use This Skill

Use this skill when you need to:
- Create breadcrumb navigation showing the current location in a hierarchical structure
- Enable navigation between different pages or sections in your application
- Handle breadcrumb item overflow with different strategies (Menu, Scroll, Collapsed, etc.)
- Customize breadcrumb appearance with icons, templates, or separators
- Implement accessible breadcrumb navigation with keyboard support
- Bind breadcrumb items dynamically from URLs or data
- Integrate breadcrumbs with routing libraries for single-page applications
- Disable entire breadcrumb or individual items conditionally
- Handle breadcrumb events and perform custom logic
- Apply RTL support for internationalization

## Component Overview

The Syncfusion React Breadcrumb component provides a flexible way to display navigation paths and breadcrumb trails in your application. Key capabilities include:

- **Navigation Support**: Enable or disable navigation with fine-grained control (component-level and item-level)
- **Component Control**: Enable/disable entire component, set active item, apply custom CSS classes
- **Item-Level Control**: Disable individual items, apply icons, set IDs for identification
- **Flexible Data Binding**: Bind items declaratively or generate from URLs dynamically
- **Overflow Modes**: Handle content overflow with 6 modes (Menu, Collapsed, Scroll, Wrap, Hidden, None)
- **Customization**: Use item templates and separator templates for rich, custom layouts
- **Event Handling**: 4 events (beforeItemRender, itemClick, created) with comprehensive arguments
- **Internationalization**: Full RTL support for right-to-left languages
- **Accessibility**: Full WCAG 2.2 compliance with keyboard navigation and screen reader support
- **Icon Integration**: Support for font icons, images, and SVG graphics
- **State Management**: Set active items programmatically, manage item enabled/disabled states

## Documentation and Navigation Guide

### API Properties and Events Reference
📄 **Read:** [references/api-properties-and-events.md](references/api-properties-and-events.md)

Complete API reference with code examples:
- All BreadcrumbComponent properties (activeItem, cssClass, disabled, enableNavigation, etc.)
- All BreadcrumbItem properties (disabled, iconCss, id, text, url)
- All component events (beforeItemRender, itemClick, created)
- Event arguments and usage examples
- All 6 overflow modes with examples
- Property and event summary tables

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Start here if you're new to Syncfusion Breadcrumb:
- Installation and dependencies setup
- Vite vs Create React App environment setup
- Adding CSS stylesheets and themes
- Creating your first basic breadcrumb component
- Adding items to breadcrumb
- TypeScript configuration and types

### Navigation and Routing
📄 **Read:** [references/navigation-and-routing.md](references/navigation-and-routing.md)

Use when you need to enable navigation:
- Enable or disable item navigation (enableNavigation property)
- Implement relative and absolute URLs
- Enable active item (last breadcrumb) navigation (enableActiveItemNavigation)
- Open URLs in new tabs using beforeItemRender
- Handle itemClick events
- Advanced routing integration with React Router

### Customization and Templates
📄 **Read:** [references/customization.md](references/customization.md)

Use when customizing the breadcrumb appearance:
- Overflow modes (Menu, Collapsed, Scroll, Wrap, Hidden, None)
- Item templates for rich content (itemTemplate property)
- Separator templates with custom icons (separatorTemplate)
- Managing maximum items display (maxItems property)
- Item-level disabling (disabled property)
- Styling and CSS classes (cssClass property)

### Icon Integration and Data Binding
📄 **Read:** [references/icon-integration-data-binding.md](references/icon-integration-data-binding.md)

Use when working with icons or dynamic data:
- Font icon implementation (Syncfusion icons with iconCss)
- Adding images and SVG graphics as icons
- Icon positioning (left, right, icon-only)
- Data binding from tag directives
- URL-based item generation (url property on component)
- Static URL configuration
- Customizing generated item text with beforeItemRender

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)

Use when implementing accessible breadcrumbs:
- WCAG 2.2 compliance guidelines
- ARIA attributes and roles
- Keyboard navigation support (Tab, Shift+Tab, Enter)
- Screen reader optimization
- Right-to-left (RTL) support (enableRtl property)
- Testing with accessibility tools

## Quick Start Example

Here's a minimal working example to get started:

```tsx
import { BreadcrumbComponent, BreadcrumbItemDirective, BreadcrumbItemsDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-navigations/styles/tailwind3.css';

export default function App() {
  return (
    <BreadcrumbComponent enableNavigation={false}>
      <BreadcrumbItemsDirective>
        <BreadcrumbItemDirective iconCss="e-icons e-home" url="/" />
        <BreadcrumbItemDirective text="Components" url="/components" />
        <BreadcrumbItemDirective text="Breadcrumb" url="/breadcrumb" />
      </BreadcrumbItemsDirective>
    </BreadcrumbComponent>
  );
}
```

## Common Patterns

### Pattern 1: Navigation Enabled Breadcrumb

Enable user navigation by setting `enableNavigation={true}` and providing URLs:

```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="../" />
    <BreadcrumbItemDirective text="Products" url="../products" />
    <BreadcrumbItemDirective text="Category" url="../products/category" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Pattern 2: Breadcrumb with Icons

Add visual context with icon-based breadcrumbs:

```tsx
<BreadcrumbComponent enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective iconCss="e-icons e-home" />
    <BreadcrumbItemDirective iconCss="e-bicons e-folder" text="Folder" />
    <BreadcrumbItemDirective iconCss="e-bicons e-file" text="Document" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Pattern 3: Handling Overflow

Use overflow modes for responsive breadcrumb trails:

```tsx
<BreadcrumbComponent maxItems={3} overflowMode="Menu" enableNavigation={false}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" />
    <BreadcrumbItemDirective text="Folder 1" />
    <BreadcrumbItemDirective text="Folder 2" />
    <BreadcrumbItemDirective text="Folder 3" />
    <BreadcrumbItemDirective text="File" />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

### Pattern 4: Component-Level Control

Disable entire component or set active item programmatically:

```tsx
import { useState } from 'react';

export default function App() {
  const [isDisabled, setIsDisabled] = useState(false);
  const [activeUrl, setActiveUrl] = useState('/products');

  return (
    <div>
      <BreadcrumbComponent 
        disabled={isDisabled}
        activeItem={activeUrl}
        enableNavigation={true}
      >
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

### Pattern 5: Item-Level Disabling

Disable specific items based on conditions:

```tsx
<BreadcrumbComponent enableNavigation={true}>
  <BreadcrumbItemsDirective>
    <BreadcrumbItemDirective text="Home" url="/" disabled={false} />
    <BreadcrumbItemDirective text="Products" url="/products" disabled={false} />
    <BreadcrumbItemDirective text="Admin Only" url="/admin" disabled={!isAdmin} />
  </BreadcrumbItemsDirective>
</BreadcrumbComponent>
```

## Key Props Reference

### Component-Level Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `enableNavigation` | boolean | true | Enable/disable item navigation |
| `enableActiveItemNavigation` | boolean | false | Make last item clickable |
| `disabled` | boolean | false | Disable entire component |
| `activeItem` | string | N/A | URL of active breadcrumb item |
| `cssClass` | string | N/A | CSS classes for container |
| `enableRtl` | boolean | false | Right-to-left rendering |
| `maxItems` | number | N/A | Maximum visible items before overflow |
| `overflowMode` | string | 'Menu' | Overflow behavior: Menu, Collapsed, Scroll, Wrap, Hidden, None |
| `items` | BreadcrumbItemModel[] | N/A | Breadcrumb items array |
| `itemTemplate` | Function\|string | N/A | Custom template for items |
| `separatorTemplate` | Function\|string | N/A | Custom template for separators |
| `url` | string | N/A | Generate items from URL path |

### Item-Level Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `text` | string | '' | Display text |
| `url` | string | '' | Navigation URL |
| `iconCss` | string | null | Icon CSS classes |
| `disabled` | boolean | false | Disable individual item |
| `id` | string | '' | Unique item identifier |

### Events

| Event | Fires When | Arguments |
|-------|-----------|-----------|
| `beforeItemRender` | Before rendering each item | cancel, element, item, name |
| `itemClick` | When item clicked | cancel, element, event, item, name |
| `created` | Component rendering completes | Event |

## Common Use Cases

1. **File System Navigation**: Display current folder path with folder/file icons
2. **E-commerce Product Path**: Show category → subcategory → product hierarchy
3. **Documentation Navigation**: Navigate through documentation sections and pages
4. **Multi-step Forms**: Display form steps and progress
5. **Website Navigation**: Show current page location within site hierarchy

---

**Next Steps:**
- Read the appropriate reference file based on your needs
- Copy code examples and adapt to your use case
- Refer to API documentation for advanced properties
- Test with different themes (Tailwind, Bootstrap, Fluent, Material)
