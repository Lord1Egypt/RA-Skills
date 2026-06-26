---
name: syncfusion-react-sidebar
description: Implement responsive Syncfusion React Sidebar component for navigation layouts. Use this when building responsive navigation menus, drawer layouts, or collapsible sidebars with various display modes (Over, Push, Slide). This skill covers sidebar configuration, animations, backdrop overlays, keyboard accessibility, and integration with multi-level navigation systems.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion React Sidebar

The Syncfusion React Sidebar is a responsive navigation component that enables flexible layout patterns for modern web applications. It supports multiple display modes (Over, Push, Slide, Auto), responsive breakpoints, touch gestures, keyboard navigation, and seamless integration with ListView and TreeView components.

## When to Use This Skill

Choose Sidebar when you need:
- **Responsive navigation** - Drawer menus that adapt to desktop/mobile viewports
- **Multi-mode layouts** - Over (float), Push (shift content), Slide (translate), or Auto (responsive) behaviors
- **Content organization** - Nested menus, ListView/TreeView integration, or multi-panel layouts
- **User interaction patterns** - Toggle buttons, backdrop overlays, auto-close on item click, or keyboard shortcuts
- **Accessibility** - ARIA labels, keyboard navigation (Tab, Enter, Escape), and screen reader support
- **Customization** - Themed styling, animation variations, RTL support, or custom context containers

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic sidebar rendering
- CSS imports and theme configuration
- Initial state management
- First working example

### API Reference: Properties
📄 **Read:** [references/properties-reference.md](references/properties-reference.md)
- All 18 properties with types, defaults, and examples
- Display properties (type, position, width, animate, showBackdrop, zIndex)
- Behavior properties (closeOnDocumentClick, enableGestures, enableRtl, mediaQuery)
- State properties (isOpen, enableDock, dockSize, enablePersistence)
- Container property (target)

### API Reference: Methods
📄 **Read:** [references/methods-reference.md](references/methods-reference.md)
- `show(e?: Event)` - Display sidebar with optional event parameter
- `hide(e?: Event)` - Hide sidebar with optional event parameter
- `toggle()` - Toggle open/closed state
- `destroy()` - Remove sidebar from DOM
- Complete examples for each method

### API Reference: Events
📄 **Read:** [references/events-reference.md](references/events-reference.md)
- `change` - State change notification (user or programmatic)
- `open` - Before sidebar opens (preventable)
- `close` - Before sidebar closes (preventable)
- `created` - After sidebar is initialized
- `destroyed` - When sidebar is removed
- Event handling examples and patterns

### API Reference: Event Arguments
📄 **Read:** [references/event-arguments-reference.md](references/event-arguments-reference.md)
- `ChangeEventArgs` interface - element, name, cancel, isInteracted
- `EventArgs` interface - cancel, element, event, isInteracted, model
- `SidebarModel` object - Complete configuration snapshot
- Type definitions and usage examples

### Sidebar Positioning & Behavior
📄 **Read:** [references/sidebar-positioning.md](references/sidebar-positioning.md)
- Sidebar types: Over, Push, Slide, Auto
- Position: Left or Right
- Width and dock size configuration
- Multiple sidebars side-by-side
- Media query responsive behavior

### Opening & Closing Sidebar
📄 **Read:** [references/opening-closing.md](references/opening-closing.md)
- Toggle functionality
- Programmatic show/hide methods
- Auto-close on document click
- Auto-close on escape key
- Animation transitions
- Event handling for state changes

### Content Integration
📄 **Read:** [references/content-integration.md](references/content-integration.md)
- ListView integration with sidebar
- TreeView integration for hierarchical navigation
- Custom HTML content and structures
- Dynamic data binding patterns
- Menu-like navigation structures

### Styling & Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- CSS class customization
- Theme styles (default, material, bootstrap)
- Animation variations and timing
- Responsive breakpoint patterns
- RTL (Right-to-Left) support
- Custom animations

### Accessibility & Best Practices
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG compliance guidelines
- Keyboard navigation (Tab, Enter, Escape)
- ARIA attributes for screen readers
- Focus management
- Backdrop overlay interaction patterns

## Quick Start

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  
  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="container">
      {/* Toggle Button */}
      <ButtonComponent 
        cssClass="e-primary" 
        onClick={handleToggle}
      >
        Toggle Sidebar
      </ButtonComponent>

      {/* Sidebar Component */}
      <SidebarComponent
        id="sidebar"
        width="250px"
        type="Over"
        isOpen={isOpen}
        change={() => setIsOpen(!isOpen)}
        showBackdrop={true}
        closeOnDocumentClick={true}
      >
        <div className="sidebar-content">
          <h3>Navigation Menu</h3>
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div>
      </SidebarComponent>

      {/* Main Content */}
      <div className="main-content">
        <h1>Main Content Area</h1>
        <p>Content shifts when type is "Push"</p>
      </div>
    </div>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Responsive Auto Sidebar
Automatically switches between Over (mobile) and Push (desktop) modes based on viewport.

```jsx
<SidebarComponent
  type="Auto"
  width="250px"
  isOpen={true}
  showBackdrop={true}
/>
```

### Pattern 2: Mobile Drawer Menu
Floating sidebar that closes on backdrop click or escape key.

```jsx
<SidebarComponent
  type="Over"
  width="280px"
  showBackdrop={true}
  closeOnDocumentClick={true}
  position="Left"
/>
```

### Pattern 3: Docked Navigation Panel
Persistent sidebar with fixed width that shows as icon bar when docked.

```jsx
<SidebarComponent
  enableDock={true}
  dockSize="50px"
  width="250px"
  type="Push"
/>
```

### Pattern 4: RTL Navigation (Arabic/Hebrew)
Right-aligned sidebar for right-to-left languages.

```jsx
<SidebarComponent
  position="Right"
  enableRtl={true}
  type="Over"
/>
```

## Key Properties Overview

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| **type** | `SidebarType` | `'Auto'` | Display mode: Over, Push, Slide, Auto |
| **isOpen** | `boolean` | `false` | Controls sidebar open/closed state |
| **position** | `SidebarPosition` | `'Left'` | Sidebar placement: Left or Right |
| **width** | `string \| number` | `'auto'` | Sidebar width (pixels or percentage) |
| **target** | `HTMLElement \| string` | `null` | Container to render sidebar inside |
| **showBackdrop** | `boolean` | `false` | Show overlay when open |
| **closeOnDocumentClick** | `boolean` | `false` | Close on content area click |
| **animate** | `boolean` | `true` | Enable open/close animations |
| **enableDock** | `boolean` | `false` | Enable dock/minimize mode |
| **dockSize** | `string \| number` | `'auto'` | Width when docked |
| **enableGestures** | `boolean` | `true` | Touch swipe gestures |
| **enableRtl** | `boolean` | `false` | Right-to-left layout |

## Common Use Cases

- **Admin Dashboard Navigation** - Top header with collapsible sidebar menu
- **Mobile App Navigation** - Hamburger menu with drawer sidebar
- **E-commerce Product Filter** - Left sidebar with expandable categories
- **Documentation Sites** - Persistent table of contents sidebar
- **Settings Panels** - Floating right sidebar for preferences
- **Multi-panel Layouts** - Multiple sidebars on different sides

---
