---
name: syncfusion-react-splitter
description: "Implement Syncfusion React Splitter component for flexible, resizable panel layouts. Guide covers layout configuration, pane sizing, collapse/expand, resize events, content types, accessibility, and RTL support. Use this skill when building multi-panel interfaces with dynamic resizing capabilities."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion React Splitter

The Splitter component creates flexible, resizable panel layouts with advanced configuration options. This skill guides you through installation, layout patterns, customization, and accessibility features.

## When to Use This Skill

Use the Splitter component when you need to:
- Create flexible layouts with multiple resizable panels
- Build split-screen interfaces (code editors, dashboards, file explorers)
- Allow users to adjust pane sizes dynamically
- Display collapsible panes with expand/collapse functionality
- Support different layout orientations (horizontal, vertical, nested)
- Implement responsive multi-panel layouts
- Add custom content types (HTML, components, selectors) to panes

## Component Overview

**SplitterComponent** provides a container for multiple panes that users can resize by dragging separators. Each pane is defined with `<PaneDirective>` within `<PanesDirective>`.

**Key Features:**
- Multiple layout orientations (horizontal, vertical, nested)
- Dynamic pane resizing with constraints
- Expand/collapse pane functionality
- Multiple content types (HTML, components, CSS selectors)
- Events for resize, expand, collapse operations
- Add/remove panes dynamically at runtime
- Accessibility and RTL support
- Theme customization

**Installation:** `npm install @syncfusion/ej2-react-layouts --save`

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Basic Splitter initialization with PanesDirective
- First working example
- Import statements and dependencies

### API Reference: Properties and Configuration
📄 **Read:** [references/properties-and-configuration.md](references/properties-and-configuration.md)
- Complete SplitterComponent properties (orientation, height, width, separatorSize, etc.)
- All PaneDirective properties (size, min, max, collapsed, collapsible, resizable, content, cssClass)
- enablePersistence for state persistence
- enableHtmlSanitizer for security
- Common configuration patterns and examples

### API Reference: Methods
📄 **Read:** [references/methods-reference.md](references/methods-reference.md)
- addPane() - Dynamically add new panes with PanePropertiesModel
- removePane() - Remove panes by index
- collapse() - Programmatically collapse panes
- expand() - Programmatically expand panes
- destroy() - Component cleanup and resource release
- Real-world examples with working code

### API Reference: Events
📄 **Read:** [references/events-reference.md](references/events-reference.md)
- created - Component initialization
- beforeCollapse / collapsed - Collapse events with cancellation
- beforeExpand / expanded - Expand events with data loading
- resizeStart / resizing / resizeStop - Resize lifecycle
- Event handling patterns and state management

### Pane Layout Configuration
📄 **Read:** [references/pane-layout-configuration.md](references/pane-layout-configuration.md)
- Horizontal and vertical layouts
- Multiple panes and nested splitters
- Pane properties and configuration
- Layout patterns for common use cases

### Pane Sizing and Separation
📄 **Read:** [references/pane-sizing-and-separation.md](references/pane-sizing-and-separation.md)
- Fixed pane sizing
- Percentage-based sizing
- Min and max size constraints
- Separator styling and customization
- Dynamic size adjustments

### Expand and Collapse Functionality
📄 **Read:** [references/expand-collapse-functionality.md](references/expand-collapse-functionality.md)
- Collapsed state initialization
- Button integration for expand/collapse
- User-driven vs programmatic collapse
- Event handling patterns

### Resize Behavior
📄 **Read:** [references/resize-behavior.md](references/resize-behavior.md)
- Resize events and lifecycle
- Preventing resize on specific panes
- Dynamic resize configuration
- Resize constraints and validation
- Event data and handling

### Pane Content and Styling
📄 **Read:** [references/pane-content-and-styling.md](references/pane-content-and-styling.md)
- HTML content in panes
- React component content in panes
- CSS selector-based content
- Pane template usage
- Custom styling and classes

### Accessibility and Globalization
📄 **Read:** [references/accessibility-and-globalization.md](references/accessibility-and-globalization.md)
- WCAG compliance and keyboard navigation
- ARIA attributes and screen reader support
- RTL (Right-to-Left) support
- Internationalization and locale
- Focus management and accessibility patterns

### Style Customization
📄 **Read:** [references/style-customization.md](references/style-customization.md)
- CSS customization and custom classes
- Theme variables and CSS imports
- Gripper and separator styling
- Responsive design patterns
- Dark mode and theme switching

## Quick Start Example

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";
import './App.css';

function App() {
  return (
    <div className='App'>
      <SplitterComponent>
        <PanesDirective>
          <PaneDirective size='200px'>
            <div>Left Panel</div>
          </PaneDirective>
          <PaneDirective size='300px'>
            <div>Right Panel</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default App;
```

## Common Patterns

### Two-Column Layout
```tsx
<SplitterComponent orientation='Horizontal'>
  <PanesDirective>
    <PaneDirective size='25%'><div>Left</div></PaneDirective>
    <PaneDirective size='75%'><div>Main Content</div></PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Vertical Split with Collapse
```tsx
<SplitterComponent orientation='Vertical'>
  <PanesDirective>
    <PaneDirective size='50%' collapsed={true}><div>Top</div></PaneDirective>
    <PaneDirective size='50%'><div>Bottom</div></PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Three-Panel Dashboard
```tsx
<SplitterComponent orientation='Horizontal'>
  <PanesDirective>
    <PaneDirective size='20%'><div>Sidebar</div></PaneDirective>
    <PaneDirective size='60%'><div>Main Content</div></PaneDirective>
    <PaneDirective size='20%'><div>Right Panel</div></PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Nested Splitters
Combine horizontal and vertical splitters for complex layouts like code editors with file explorer, editor, and console panels.

## Key Props

| Prop | Type | Description | When to Use |
|------|------|-------------|------------|
| `orientation` | 'Horizontal' \| 'Vertical' | Layout direction | When configuring panel direction |
| `size` | string (PaneDirective) | Pane width/height (px, %) | When setting pane dimensions |
| `min` | string (PaneDirective) | Minimum pane size | When preventing pane from shrinking too small |
| `max` | string (PaneDirective) | Maximum pane size | When limiting pane expansion |
| `collapsed` | boolean (PaneDirective) | Initial collapsed state | When panes should start hidden |
| `collapsible` | boolean (PaneDirective) | Allow user to collapse | When collapsing should be user-driven |
| `resizable` | boolean (PaneDirective) | Allow user to resize | When preventing manual resizing |

## Common Use Cases

**File Explorer + Editor:** Left sidebar (fixed 250px) with collapsible file tree, main editor area with resizing

**Dashboard:** Top bar (fixed height), left sidebar (collapsible nav), main content, right details panel

**Chat Interface:** Left contact list (fixed width), chat area (resizable), right info panel

**Code Editor:** Left explorer (collapsible), center editor (main), bottom console (collapsible)

**Email Client:** Left folders (fixed), center list (resizable), right preview (resizable)
