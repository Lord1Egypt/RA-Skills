---
name: syncfusion-react-dashboard-layout
description: Build responsive, interactive dashboard layouts with Syncfusion React Dashboard Layout component. Implement draggable and resizable panels, responsive grid systems, dynamic panel management, and state persistence. This skill covers multi-column layouts, floating panel arrangement, extensive customization, drag-drop panel rearrangement, and state management for React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion React Dashboard Layout

Syncfusion React Dashboard Layout is a powerful component for building responsive, interactive dashboard interfaces with draggable and resizable panels. It provides a flexible grid-based system for organizing content, automatic floating arrangement, and comprehensive state management.

**Key Capabilities:**
- Multi-column grid layouts with flexible cell sizing
- Drag-and-drop panel repositioning
- Resizable panels with size constraints
- Automatic floating arrangement (fills empty spaces)
- Responsive design with media queries
- Dynamic panel add/remove/update operations
- State persistence across sessions
- Comprehensive event system for monitoring changes
- Accessibility support and RTL rendering

## Documentation and Navigation Guide

Choose the reference that matches your current task:

### 🚀 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- CSS theme imports and configuration
- Creating your first dashboard
- Basic panel implementation
- Common setup issues and solutions

### 🎯 Core Concepts
📄 **Read:** [references/core-functionality.md](references/core-functionality.md)
- Panel creation and configuration (PanelModel interface)
- Basic dragging and positioning
- Basic resizing with constraints
- Grid configuration fundamentals
- Complete component overview

📄 **Read:** [references/properties-reference.md](references/properties-reference.md)
- All 15 component properties documented
- Layout properties (columns, cellSpacing, cellAspectRatio)
- Customization options (enableRtl, enablePersistence, showGridLines)
- Advanced properties (mediaQuery, draggableHandle, resizableHandles)
- Complete property reference with patterns

### 🎨 User Interface & Customization
📄 **Read:** [references/panel-templates.md](references/panel-templates.md)
- Panel structure and composition
- Header templates (text, HTML, interactive)
- Content templates (HTML strings, JSX, Syncfusion components)
- Embedding charts, grids, and widgets
- Dynamic content updates
- Template best practices and optimization

📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- Complete CSS selector reference
- Theme system integration (Tailwind, Bootstrap, Material, Fluent)
- Header and content area styling
- Resize handle styling and customization
- Panel backgrounds, borders, and gradients
- Dragging and interaction state styling
- Advanced customization patterns

### 🎮 Interaction & Behavior
📄 **Read:** [references/dragging-behavior.md](references/dragging-behavior.md)
- Enable and configure drag functionality
- Drag events (dragStart, drag, dragStop)
- Collision detection and panel pushing
- Custom drag handles (header-only, icon-only, multiple)
- Preventing specific panels from dragging
- Visual feedback and placeholder styling
- Programmatic panel movement
- Undo/redo implementation

📄 **Read:** [references/resizing-floating.md](references/resizing-floating.md)
- Enable and configure resize functionality
- Resize handle directions (SE, E, W, N, S, NW, NE, SW)
- Size constraints (minSizeX, minSizeY, maxSizeX, maxSizeY)
- Resize events (resizeStart, resize, resizeStop)
- Floating behavior and gap filling
- Programmatic resizing (resizePanel method)
- Responsive resizing and aspect ratio maintenance
- Best practices for resizing

### ⚙️ Configuration & Layout
📄 **Read:** [references/cell-configuration.md](references/cell-configuration.md)
- Grid columns and cell distribution
- Cell sizing basics (sizeX, sizeY)
- Cell aspect ratio configuration
- Cell spacing and gap management
- Cell calculation examples
- Responsive cell configuration
- Masonry, hero, and nested grid patterns

📄 **Read:** [references/responsive-design.md](references/responsive-design.md)
- Built-in responsive behavior
- Media query configuration and custom breakpoints
- Standard breakpoint systems
- Adaptive layouts for different screen sizes
- Mobile-first approach
- Touch device support and optimization
- Testing responsive layouts
- Performance optimization for responsiveness

### 💾 Advanced Features
📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- Serialize method for saving layout
- Save/restore state patterns
- localStorage integration
- sessionStorage integration
- Database API integration
- Advanced state management (Redux, Context API)
- Versioning and migration
- Error recovery and backups

📄 **Read:** [references/methods-reference.md](references/methods-reference.md)
- All 9 component methods documented
- Panel management: addPanel, removePanel, removeAll, updatePanel
- Layout manipulation: movePanel, resizePanel
- Serialization: serialize method
- Utility methods: refreshDraggableHandle, destroy
- Complete method examples and use cases

📄 **Read:** [references/events-reference.md](references/events-reference.md)
- All 10 component events documented
- Lifecycle events: created, destroyed
- Interaction events: dragStart, drag, dragStop, resizeStart, resize, resizeStop
- Change event: monitoring panel additions, removals, position changes
- Event arguments and properties
- Complete event handling patterns

### ♿ Compliance & Accessibility
📄 **Read:** [references/accessibility-wcag.md](references/accessibility-wcag.md)
- WCAG 2.2 Level AA compliance
- Section 508 standards compliance
- WAI-ARIA implementation (roles, properties, states)
- Keyboard navigation and accessibility
- Screen reader support
- RTL (right-to-left) language support
- Testing and validation procedures
- Accessibility audit checklist

## Quick Start Example

Create an interactive dashboard in minutes:

```tsx
import React, { useRef } from 'react';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';

function Dashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  const panels = [
    {
      id: 'sales',
      header: 'Sales',
      content: '<div style="padding: 20px;">Sales data</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'users',
      header: 'Users',
      content: '<div style="padding: 20px;">User analytics</div>',
      row: 0,
      col: 2,
      sizeX: 2,
      sizeY: 2
    },
    {
      id: 'reports',
      header: 'Reports',
      content: '<div style="padding: 20px;">Report metrics</div>',
      row: 2,
      col: 0,
      sizeX: 4,
      sizeY: 1
    }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        columns={5}
        cellSpacing={[10, 10]}
        panels={panels}
        allowDragging={true}
        allowResizing={true}
        allowFloating={true}
        enablePersistence={true}
      >
      </DashboardLayoutComponent>
    </div>
  );
}

export default Dashboard;
```

## Common Patterns

### Pattern 1: Responsive Dashboard with Mobile Support

**📖 Read:** [responsive-design.md](references/responsive-design.md) for comprehensive mobile adaptation patterns

```tsx
<DashboardLayoutComponent
  id='responsive-dashboard'
  columns={5}
  mediaQuery='max-width:768px'  // Single column on tablets/mobile
  cellSpacing={[10, 10]}
  allowDragging={true}
  allowResizing={true}
  panels={panels}
>
</DashboardLayoutComponent>
```

**Key Features:**
- Responsive column adjustment based on screen size
- Mobile-first design with media queries
- Touch optimization for mobile devices
- See `responsive-design.md` for breakpoint configuration and testing

### Pattern 2: Save and Restore User Layout

**📖 Read:** [state-persistence.md](references/state-persistence.md) for complete state serialization and storage options

```tsx
const handleSaveLayout = () => {
  const layout = dashboardRef.current?.serialize();
  localStorage.setItem('userDashboard', JSON.stringify(layout));
};

const handleRestoreLayout = () => {
  const saved = localStorage.getItem('userDashboard');
  if (saved) {
    const layout = JSON.parse(saved);
    dashboardRef.current?.removeAll();
    layout.forEach(panel => {
      dashboardRef.current?.addPanel(panel);
    });
  }
};
```

**Key Features:**
- serialize() method exports current layout state
- localStorage for client-side persistence
- See `state-persistence.md` for API integration, Redux/Context patterns, and auto-save

### Pattern 3: Dynamic Panel Management

**📖 Read:** [core-functionality.md](references/core-functionality.md) for panel addition/removal and runtime management

```tsx
const handleAddPanel = () => {
  dashboardRef.current?.addPanel({
    id: `panel-${Date.now()}`,
    header: 'New Panel',
    content: 'Panel content',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1
  });
};

const handleRemovePanel = (panelId: string) => {
  dashboardRef.current?.removePanel(panelId);
};
```

**Key Features:**
- Runtime panel creation and deletion
- Unique panel IDs and positioning
- Event handling for panel changes
- See `methods-reference.md` for all available panel methods

### Pattern 4: Constrained Panel Sizes

**📖 Read:** [cell-configuration.md](references/cell-configuration.md) and [resizing-floating.md](references/resizing-floating.md) for size constraints and resizing behavior

```tsx
const constrainedPanels = [
  {
    id: 'fixed-panel',
    header: 'Fixed Size',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1,
    minSizeX: 2,  // Cannot shrink
    maxSizeX: 2,  // Cannot expand
    minSizeY: 1,
    maxSizeY: 1
  },
  {
    id: 'flexible-panel',
    header: 'Flexible',
    row: 0,
    col: 2,
    sizeX: 2,
    sizeY: 1,
    minSizeX: 1,  // Can shrink to 1 cell
    maxSizeX: 4   // Can expand to 4 cells
  }
];
```

**Key Features:**
- minSizeX/Y and maxSizeX/Y constraints
- Fixed vs. flexible panel sizing
- Programmatic size updates via resizePanel()
- See `cell-configuration.md` for grid calculations and `resizing-floating.md` for advanced resize patterns

### Pattern 5: Monitor Layout Changes

**📖 Read:** [events-reference.md](references/events-reference.md) for all available events and handlers

```tsx
const handleChange = (args: ChangeEventArgs) => {
  console.log('Panels added:', args.addedPanels);
  console.log('Panels removed:', args.removedPanels);
  console.log('Panels position changed:', args.changedPanels);
  console.log('User interaction:', args.isInteracted);
};

<DashboardLayoutComponent
  panels={panels}
  change={handleChange}
>
</DashboardLayoutComponent>
```

**Key Features:**
- Change event fires on any layout modification
- Access to added, removed, and repositioned panels
- User interaction detection
- See `events-reference.md` for drag, resize, and other event handlers

## Key API Overview

### Component Properties
**📖 Full Reference:** [properties-reference.md](references/properties-reference.md)

- **columns** - Number of grid columns (default: 1) → See `cell-configuration.md`
- **cellSpacing** - Spacing between panels [horizontal, vertical] → See `cell-configuration.md`
- **panels** - Array of PanelModel objects defining layout → See `panel-templates.md`
- **allowDragging** - Enable panel drag-and-drop (default: true) → See `dragging-behavior.md`
- **allowResizing** - Enable panel resizing (default: false) → See `resizing-floating.md`
- **allowFloating** - Auto-fill empty spaces (default: true) → See `resizing-floating.md`
- **enablePersistence** - Save layout state (default: false) → See `state-persistence.md`
- **mediaQuery** - Responsive breakpoint for mobile layouts → See `responsive-design.md`
- **draggableHandle** - Custom drag handle selector → See `dragging-behavior.md`
- **resizableHandles** - Resize handle directions → See `resizing-floating.md`
- **cssClass** - Custom CSS classes → See `styling-customization.md`

### Core Methods
**📖 Full Reference:** [methods-reference.md](references/methods-reference.md)

- **addPanel(panel)** - Add new panel at runtime → See `core-functionality.md`
- **removePanel(id)** - Remove panel by ID → See `core-functionality.md`
- **removeAll()** - Clear all panels → See `core-functionality.md`
- **updatePanel(panel)** - Modify existing panel → See `core-functionality.md`
- **movePanel(id, row, col)** - Change panel position → See `dragging-behavior.md`
- **resizePanel(id, sizeX, sizeY)** - Adjust panel dimensions → See `resizing-floating.md`
- **serialize()** - Get current layout state → See `state-persistence.md`

### Important Events
**📖 Full Reference:** [events-reference.md](references/events-reference.md)

- **created** - Component initialized
- **dragStart** / **drag** / **dragStop** - Drag operations → See `dragging-behavior.md`
- **resizeStart** / **resize** / **resizeStop** - Resize operations → See `resizing-floating.md`
- **change** - Layout changed (additions, removals, movements) → See `events-reference.md`

### Styling & Customization
**📖 Full Reference:** [styling-customization.md](references/styling-customization.md)

- CSS selectors for all panel elements
- Theme customization (Tailwind, Bootstrap, Material, Fluent)
- Responsive styling patterns
- Accessibility styling (WCAG 2.2)

## Common Use Cases

**🎯 Creating Dashboards:** Implement customizable dashboard layouts with multiple content panels organized in a grid.
- Read: [core-functionality.md](references/core-functionality.md), [panel-templates.md](references/panel-templates.md)

**🎯 User-Customizable Layouts:** Allow users to rearrange and resize dashboard panels to their preference with automatic saving.
- Read: [dragging-behavior.md](references/dragging-behavior.md), [resizing-floating.md](references/resizing-floating.md), [state-persistence.md](references/state-persistence.md)

**🎯 Responsive Interfaces:** Build layouts that adapt from multi-column desktop views to single-column mobile views.
- Read: [responsive-design.md](references/responsive-design.md), [cell-configuration.md](references/cell-configuration.md)

**🎯 Real-Time Monitoring:** Display multiple real-time data sources in resizable panels with live updates.
- Read: [panel-templates.md](references/panel-templates.md) (component embedding), [events-reference.md](references/events-reference.md)

**🎯 Admin Panels:** Create administrative interfaces with draggable widgets for system monitoring and control.
- Read: [dragging-behavior.md](references/dragging-behavior.md), [styling-customization.md](references/styling-customization.md), [accessibility-wcag.md](references/accessibility-wcag.md)

**🎯 Data Visualization:** Organize multiple charts, tables, and metrics in flexible, responsive panel layouts.
- Read: [panel-templates.md](references/panel-templates.md) (embedding charts/grids), [styling-customization.md](references/styling-customization.md)

## Panel Model Interface

```typescript
interface PanelModel {
  id: string;              // Unique identifier (required)
  row: number;             // Row position (required)
  col: number;             // Column position (required)
  sizeX: number;           // Width in cells (default: 1)
  sizeY: number;           // Height in cells (default: 1)
  header?: string | HTMLElement | Function;
  content?: string | HTMLElement | Function;
  cssClass?: string;       // Custom CSS classes
  enabled?: boolean;       // Enable/disable (default: true)
  minSizeX?: number;       // Minimum width (default: 1)
  minSizeY?: number;       // Minimum height (default: 1)
  maxSizeX?: number;       // Maximum width
  maxSizeY?: number;       // Maximum height
  zIndex?: number;         // Stacking order
}
```

## Quick Reference Guide

| Task | Read This Documentation |
|------|------------------------|
| **Get Started** | [getting-started.md](references/getting-started.md) - Installation, setup, themes |
| **Learn Panel Management** | [core-functionality.md](references/core-functionality.md) - Create, update, remove panels |
| **Customize Panel Content** | [panel-templates.md](references/panel-templates.md) - Headers, templates, component embedding |
| **Make It Draggable** | [dragging-behavior.md](references/dragging-behavior.md) - Drag events, collision, custom handles |
| **Make It Resizable** | [resizing-floating.md](references/resizing-floating.md) - Resize handles, constraints, floating |
| **Configure Grid System** | [cell-configuration.md](references/cell-configuration.md) - Columns, spacing, aspect ratio, responsive grids |
| **Make It Responsive** | [responsive-design.md](references/responsive-design.md) - Breakpoints, mobile, touch optimization |
| **Save User Layouts** | [state-persistence.md](references/state-persistence.md) - serialize(), localStorage, API, Redux, Context |
| **Style & Theme** | [styling-customization.md](references/styling-customization.md) - CSS selectors, themes, responsive styling |
| **Make It Accessible** | [accessibility-wcag.md](references/accessibility-wcag.md) - WCAG 2.2, WAI-ARIA, screen readers, RTL |
| **API Reference** | [properties-reference.md](references/properties-reference.md), [methods-reference.md](references/methods-reference.md), [events-reference.md](references/events-reference.md) |
| **Advanced Patterns** | [advanced-features.md](references/advanced-features.md) - Custom integrations, performance optimization |

## Implementation Roadmap

**Phase 1 - Foundation (Start Here):**
1. Read [getting-started.md](references/getting-started.md) for setup
2. Review [core-functionality.md](references/core-functionality.md) for panel basics
3. Check [properties-reference.md](references/properties-reference.md) for all available options

**Phase 2 - Interaction (Build Functionality):**
4. Implement dragging: [dragging-behavior.md](references/dragging-behavior.md)
5. Implement resizing: [resizing-floating.md](references/resizing-floating.md)
6. Configure grid: [cell-configuration.md](references/cell-configuration.md)

**Phase 3 - Content (Customize Visuals):**
7. Create panel templates: [panel-templates.md](references/panel-templates.md)
8. Apply styling: [styling-customization.md](references/styling-customization.md)

**Phase 4 - Polish (Production Ready):**
9. Optimize for mobile: [responsive-design.md](references/responsive-design.md)
10. Add accessibility: [accessibility-wcag.md](references/accessibility-wcag.md)
11. Implement persistence: [state-persistence.md](references/state-persistence.md)

**Phase 5 - Advanced (Expert Features):**
12. Explore patterns: [advanced-features.md](references/advanced-features.md)
13. Refer to event/method APIs: [events-reference.md](references/events-reference.md), [methods-reference.md](references/methods-reference.md)
