---
name: syncfusion-react-appbar
description: Create responsive navigation headers with AppBar component. Build top, bottom, or sticky app bars with buttons, menus, icons, and sidebars. Use when building navigation elements, toolbars, action bars, or responsive headers with dynamic content layout. Includes color modes (Light, Dark, Primary, Inherit), size modes (Regular, Prominent, Dense), spacing, separators, and full accessibility support.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Syncfusion React AppBar

The AppBar component creates flexible navigation headers and toolbars at the top or bottom of your application. It's used to display branding, screen titles, navigation controls, and actions while supporting responsive layouts, multiple positioning modes, and rich styling options.

## When to Use This Skill

Use AppBar when you need to:
- Display application branding and navigation at the top/bottom of pages
- Create action bars with buttons, menus, or dropdowns
- Build responsive toolbars that adapt to screen size
- Implement sticky/fixed navigation that stays visible while scrolling
- Create responsive sidebars with menu navigation
- Add visual separation between grouped controls
- Support accessibility standards (WCAG 2.2, Section 508, keyboard navigation)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies
- React setup (Vite and Create React App)
- CSS imports and theme configuration
- Basic AppBar with buttons and icons
- First working example

### Positioning and Layout
📄 **Read:** [references/positioning-and-layout.md](references/positioning-and-layout.md)
- Position modes: Top (default), Bottom, Sticky
- Spacer for horizontal content spacing
- Separator for visual grouping
- Media queries for responsive design
- Layout patterns for different screen sizes

### Size and Color Modes
📄 **Read:** [references/size-and-color-modes.md](references/size-and-color-modes.md)
- Mode property: Regular, Prominent, Dense
- ColorMode property: Light, Dark, Primary, Inherit
- When to use each mode combination
- Height customization for prominent AppBars
- Visual hierarchy with color modes

### Design Patterns
📄 **Read:** [references/design-patterns.md](references/design-patterns.md)
- AppBar with Menu component integration
- AppBar with Button and DropDownButton
- AppBar with Sidebar for responsive navigation
- Navigation and branding patterns
- e-inherit CSS class usage
- Responsive sidebar with TreeView

### Styling and Accessibility
📄 **Read:** [references/styling-and-accessibility.md](references/styling-and-accessibility.md)
- CSS customization with cssClass property
- HTML attributes and aria-label
- CSS class reference (.e-appbar, .e-prominent, etc.)
- WCAG 2.2 and Section 508 compliance
- Keyboard navigation support
- RTL, color contrast, and mobile support

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete property documentation (colorMode, mode, position, isSticky, cssClass, htmlAttributes, enableRtl, enablePersistence, locale)
- Event documentation (created, destroyed)
- Working code examples for every property
- Event handler examples
- Common property combinations
- Summary table of all APIs

## Quick Start

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass='e-inherit menu' iconCss='e-icons e-menu'></ButtonComponent>
      <span className="regular">My App</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass='e-inherit login'>Login</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Basic Navigation Bar
```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit">Home</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">About</ButtonComponent>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">Contact</ButtonComponent>
</AppBarComponent>
```

### Pattern 2: Prominent AppBar with Title
```tsx
<AppBarComponent colorMode="Primary" mode="Prominent" cssClass="prominent-appbar">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span className="prominent">Large Title Section</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">Action</ButtonComponent>
</AppBarComponent>
```

### Pattern 3: Dense Toolbar
```tsx
<AppBarComponent colorMode="Dark" mode="Dense">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
  <div className="e-appbar-separator"></div>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-bold"></ButtonComponent>
</AppBarComponent>
```

### Pattern 4: Sticky AppBar with Bottom Position
```tsx
<AppBarComponent colorMode="Primary" isSticky position="Bottom">
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">Save</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">Cancel</ButtonComponent>
</AppBarComponent>
```

## Key Props

Quick reference for the most commonly used AppBar properties:

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `colorMode` | string | `"Light"` | Color scheme: Light, Dark, Primary, Inherit |
| `mode` | string | `"Regular"` | Size mode: Regular, Prominent, Dense |
| `position` | string | `"Top"` | Vertical position: Top, Bottom |
| `isSticky` | boolean | `false` | Stick to viewport while scrolling |
| `cssClass` | string | - | Custom CSS classes for styling |
| `htmlAttributes` | Record | `{}` | HTML attributes (aria-label, data-*, etc.) |
| `enableRtl` | boolean | `false` | Enable right-to-left direction |
| `enablePersistence` | boolean | `false` | Persist state between reloads |
| `locale` | string | `"en-US"` | Language and culture settings |

**For detailed explanations and code examples for all properties, events, and methods, see the [API Reference](references/api-reference.md).**

## Common Use Cases

**Use Case 1: E-commerce Product Page**
- Primary AppBar at top with brand logo and search
- Navigation buttons (Home, Products, About)
- Right-aligned user account and cart icons
- Sticky so it stays visible when scrolling products

**Use Case 2: Admin Dashboard**
- Dark AppBar with application name
- Left sidebar toggle button (e-menu icon)
- Center spacer for balance
- Right-aligned user profile and logout

**Use Case 3: Mobile-First App**
- Responsive menu button (hidden on desktop)
- Dense mode to save screen space
- Bottom AppBar with action buttons on mobile
- Top AppBar on desktop with full navigation

**Use Case 4: Document Editor**
- Dense AppBar with editing tools (cut, copy, paste)
- Separators to group related buttons
- Undo/Redo on left, Format options on right
- Sticky while editing document

---

**Next Steps:** Choose a reference file above based on your specific task. For example, if you're getting started, read "Getting Started". If you need to position the AppBar, read "Positioning and Layout".
