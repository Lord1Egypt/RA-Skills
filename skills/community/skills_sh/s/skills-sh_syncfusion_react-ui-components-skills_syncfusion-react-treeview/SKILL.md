---
name: syncfusion-react-treeview
description: Implement Syncfusion React TreeView component for hierarchical data display with node selection, drag-drop reordering, inline editing, and custom templating. Use this when building organizational charts, file systems, navigation trees, or any multi-level hierarchical interface. Covers selection modes, checkboxes, filtering, sorting, keyboard navigation, accessibility, and performance optimization with stateless templates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Syncfusion React TreeView - Comprehensive Implementation Guide

Master the Syncfusion React TreeView component for building powerful hierarchical data interfaces with advanced features, performance optimization, and enterprise-grade functionality.

## Quick Start Navigation

**Just Getting Started?**  
→ Read [Getting Started](references/getting-started.md) - Installation, setup, first TreeView

**Need to Display Hierarchical Data?**  
→ See [Data Binding](references/data-binding.md) - All binding patterns (hierarchical, self-referential, remote, load-on-demand)

**Working with Node Templates?**  
→ Check [Templates and Rendering](references/templates-and-rendering.md) - nodeTemplate, **statelessTemplates (performance)**, drawNode callback, JSX/HTML templates

**Want to CRUD Nodes Programmatically?**  
→ Learn [Node Operations](references/node-operations.md) - Add, remove, update, move, refresh nodes dynamically

**Need Checkboxes or Multi-Select?**  
→ Read [Selection and Checking](references/selection-and-checking.md) - Single/multi-selection, checkboxes, parent-child sync, three-state

**Implementing Drag-Drop?**  
→ See [Drag-Drop and Reordering](references/drag-drop-and-reordering.md) - Single/multi-node drag, validation, restrictions

**Allowing Node Editing?**  
→ Check [Inline Editing](references/inline-editing.md) - Edit modes, validation, edit events, keyboard shortcuts

**Need to Filter or Search?**  
→ Learn [Filtering and Searching](references/filtering-and-searching.md) - Text filtering, parent chain inclusion, Predicate queries, dynamic filtering

**Want Custom Sorting?**  
→ See [Sorting and Ordering](references/sorting-and-ordering.md) - Global sort, level-wise sorting, custom algorithms, sortOrder property

**Customizing Appearance?**  
→ Read [Customization and Styling](references/customization-styling.md) - CSS, icons, level-based styling, full-row selection, hover effects

**Keyboard Navigation & A11y?**  
→ Check [Keyboard Navigation and Accessibility](references/keyboard-and-accessibility.md) - Shortcuts, ARIA, screen readers, WCAG 2.1 compliance

**Advanced Features Needed?**  
→ See [Advanced Features](references/advanced-features.md) - Load-on-demand, state persistence, RTL, localization, accordion pattern

**Working with Context Menus?**  
→ Learn [Context Menu Integration](references/context-menu-integration.md) - Menu operations, node management via menu, menu state

---

## Component Overview

The **TreeViewComponent** from `@syncfusion/ej2-react-navigations` is a versatile hierarchical data display component with enterprise features:

### Core Capabilities

| Capability | Details |
|-----------|---------|
| **Data Display** | Hierarchical, self-referential, remote (OData/WebAPI), load-on-demand |
| **Node Operations** | Create, Read, Update, Delete (CRUD) nodes dynamically |
| **Selection** | Single/multiple selection, checkboxes, three-state, auto parent-child sync |
| **Editing** | Inline editing with validation, programmatic edit control |
| **Customization** | Node templates (including **stateless optimization**), custom icons, CSS styling by level |
| **Interaction** | Drag-drop (single/multi), context menus, tooltips, keyboard shortcuts |
| **Performance** | Load-on-demand, stateless templates, filtering, sorting optimization |
| **Accessibility** | WCAG 2.1 keyboard navigation, ARIA attributes, screen reader support |
| **Internationalization** | RTL support, localization, multiple language packs |
| **State Management** | Session persistence, programmatic node access |

### Key Properties Overview

```tsx
<TreeViewComponent
  // Data
  fields={{ dataSource, id, text, parentID, child, hasChildren, expanded }}
  
  // Selection & Checking
  allowMultiSelection={true}
  showCheckBox={true}
  autoCheck={true}
  checkedNodes={[]}
  selectedNodes={[]}
  
  // Interaction
  allowDragAndDrop={true}
  allowEditing={true}
  
  // Customization
  nodeTemplate={templateFunction}
  statelessTemplates={['nodeTemplate']} // NEW: Performance optimization
  cssClass="custom"
  
  // Display
  allowTextWrap={true}
  fullRowSelect={true}
  
  // Behavior
  loadOnDemand={true}
  expandOn="Click"  // or "DoubleClick" or "None" (accordion)
  sortOrder="Ascending"
  
  // Persistence & Internationalization
  enablePersistence={true}
  enableRtl={false}
  locale="en-US"
  
  // Events
  onNodeSelected={handleSelect}
  onNodeExpanded={handleExpand}
  onNodeDropped={handleDrop}
  // ... many more events
/>
```

---

## Complete Feature Map

### 1. Data Binding (5 Methods)
- ✅ Hierarchical nested arrays
- ✅ Self-referential (parentID) model
- ✅ Remote OData v4
- ✅ Remote Web API
- ✅ Load-on-demand lazy loading

### 2. Node Operations (11 Methods)
- ✅ addNodes() - Create nodes
- ✅ removeNodes() - Delete nodes
- ✅ updateNode() - Modify node text
- ✅ refreshNode() - Refresh from backend
- ✅ moveNodes() - Move to different parent
- ✅ getNode() - Get node by element
- ✅ getTreeData() - Get all data
- ✅ beginEdit()/endEdit() - Programmatic edit control
- ✅ expandAll()/collapseAll() - Bulk operations
- ✅ selectNodes()/clearSelection() - Selection control

### 3. Node Templates (3 Types)
- ✅ **String templates** with ${...} interpolation
- ✅ **HTML element ID** references
- ✅ **JSX function** components
- ✅ **statelessTemplates** - Performance optimization (ignore state updates)
- ✅ **drawNode** callback - Alternative custom rendering method

### 4. Selection System (2 Modes)
- ✅ Single selection
- ✅ Multi-selection with Ctrl/Shift keyboard
- ✅ Checkbox mode with three-state support
- ✅ Parent-child auto-sync (autoCheck)
- ✅ Independent checkbox mode (autoCheck=false)

### 5. Drag-Drop (2 Scopes)
- ✅ Single-node drag
- ✅ Multi-node drag (requires allowMultiSelection)
- ✅ Drop validation with indicators (+, -, in-between)
- ✅ Restrict drag-drop per node type
- ✅ Custom drag area (dragArea property)

### 6. Editing
- ✅ Inline edit (double-click or F2)
- ✅ Input validation
- ✅ Programmatic edit (beginEdit/endEdit)
- ✅ Edit event cancellation

### 7. Filtering & Searching (Advanced)
- ✅ Text-based filtering
- ✅ Parent chain inclusion in results
- ✅ DataManager with Predicate queries
- ✅ Dynamic filter updates

### 8. Sorting (2 Levels)
- ✅ Global sorting (ascending/descending)
- ✅ Level-wise custom sorting
- ✅ DataManager Query integration
- ✅ Custom sort algorithms

### 9. Customization
- ✅ CSS class styling by level
- ✅ Custom expand/collapse icons
- ✅ Dynamic icon per node
- ✅ Full-row selection styling
- ✅ Multi-line text wrapping
- ✅ Icon visibility toggle (hover effects)

### 10. Keyboard Navigation (15+ Shortcuts)
- ✅ Arrow keys for navigation
- ✅ Home/End for first/last node
- ✅ F2 for inline edit
- ✅ Enter to confirm/select
- ✅ Escape to cancel
- ✅ Ctrl+Click for multi-select
- ✅ Shift+Click for range select

### 11. Accessibility
- ✅ WCAG 2.1 AA keyboard support
- ✅ ARIA attributes (roles, properties, states)
- ✅ Screen reader announcements
- ✅ Focus management
- ✅ Semantic HTML structure

### 12. Advanced Features
- ✅ Load-on-demand with lazy loading
- ✅ State persistence across sessions
- ✅ RTL (right-to-left) support
- ✅ Localization (16+ languages)
- ✅ Accordion pattern (expandOn='None')
- ✅ Event cancellation (preventable events)
- ✅ Virtual scrolling for large datasets

### 13. Integration
- ✅ Context menu integration
- ✅ Toolbar integration
- ✅ Tooltip support
- ✅ Data operations via menu

### 14. Events (19 Events)
- ✅ created, dataBound
- ✅ nodeSelected, nodeSelecting, nodeClicked, nodeDoubleClicked
- ✅ nodeExpanded, nodeExpanding, nodeCollapsed, nodeCollapsing
- ✅ nodeEdited, nodeEditing
- ✅ nodeDragStart, nodeDragging, nodeDragStop, nodeDropped
- ✅ nodeChecked, nodeChecking
- ✅ drawNode, keyPress

---

## Skill Progression Path

### Beginner Level (Start Here)
1. **Getting Started** - Installation, basic component, hierarchical data
2. **Data Binding** - Learn all 5 binding patterns
3. **Basic Selection** - Single selection, onClick handling

### Intermediate Level
4. **Checkboxes** - Multi-selection with checkboxes, parent-child sync
5. **Node Operations** - Dynamic CRUD operations
6. **Inline Editing** - Text editing with validation
7. **Drag-Drop** - Reordering and moving nodes
8. **Templates** - nodeTemplate basics, JSX templates

### Advanced Level
9. **Templates - Advanced** - **statelessTemplates optimization**, drawNode callback
10. **Filtering & Search** - Complex filtering with parent traversal
11. **Sorting** - Custom level-wise sorting
12. **Advanced Features** - Load-on-demand caching, persistence, RTL
13. **Keyboard & A11y** - WCAG compliance, screen reader support
14. **Context Menu** - Menu-driven operations
15. **Performance** - Optimization strategies for large datasets

---

## Documentation Reference

| Section | Purpose | Audience | Prerequisites |
|---------|---------|----------|---------------|
| [Getting Started](references/getting-started.md) | Installation, basic setup | Beginners | None |
| [Data Binding](references/data-binding.md) | 5 binding patterns | All users | Basic React/JSX |
| [Templates and Rendering](references/templates-and-rendering.md) | **NEW: Complete template coverage including statelessTemplates & drawNode** | Intermediate+ | Data Binding knowledge |
| [Node Operations](references/node-operations.md) | CRUD operations | Intermediate | Basic setup |
| [Selection and Checking](references/selection-and-checking.md) | Selection modes, checkboxes | Intermediate | Basic setup |
| [Drag-Drop and Reordering](references/drag-drop-and-reordering.md) | Drag-drop functionality | Intermediate | Basic setup |
| [Inline Editing](references/inline-editing.md) | Node text editing | Intermediate | Basic setup |
| [Filtering and Searching](references/filtering-and-searching.md) | **NEW: Advanced filtering patterns** | Advanced | Data Binding |
| [Sorting and Ordering](references/sorting-and-ordering.md) | **NEW: Custom sorting algorithms** | Advanced | Data Binding |
| [Customization and Styling](references/customization-styling.md) | CSS, icons, appearance | Intermediate+ | Basic CSS |
| [Keyboard Navigation and Accessibility](references/keyboard-and-accessibility.md) | **NEW: Keyboard shortcuts & WCAG compliance** | Advanced | UI/UX knowledge |
| [Advanced Features](references/advanced-features.md) | **NEW: Load-on-demand, persistence, RTL, localization** | Advanced | Intermediate TreeView |
| [Context Menu Integration](references/context-menu-integration.md) | Context menu patterns | Advanced | Basic setup |

---

## Quick Example

```tsx
import * as React from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-react-navigations/styles/tree-view.css';

function App() {
  const hierarchicalData = [
    {
      id: 1,
      name: 'Syncfusion',
      expanded: true,
      child: [
        { id: 2, name: 'React Components' },
        { id: 3, name: 'Angular Components' },
      ]
    },
    {
      id: 4,
      name: 'Essential Studio',
      child: [
        { id: 5, name: 'Web' },
        { id: 6, name: 'Desktop' }
      ]
    }
  ];

  const fields = {
    dataSource: hierarchicalData,
    id: 'id',
    text: 'name',
    child: 'child'
  };

  const handleNodeSelected = (args) => {
    console.log('Selected:', args.nodeData.name);
  };

  return (
    <TreeViewComponent
      fields={fields}
      allowDragAndDrop={true}
      allowEditing={true}
      showCheckBox={true}
      onNodeSelected={handleNodeSelected}
    />
  );
}

export default App;
```

---

## When to Use This Skill

**Use TreeView when you need:**
- Hierarchical multi-level data display (org charts, file systems, navigation)
- Single or multiple node selection with optional checkboxes
- Drag-and-drop node reordering or moving
- In-place node text editing with validation
- Custom node appearance with templates or icons
- Keyboard-accessible navigation (WCAG 2.1)
- Large datasets with load-on-demand or lazy loading
- Node filtering or searching with parent chain inclusion
- Context menu-driven operations
- State persistence across browser sessions
- RTL language support for international apps
- Performance-optimized rendering with stateless templates

**Don't use TreeView for:**
- Simple flat lists → Use DropDownList or ListView instead
- Single-level navigation → Use NavBar or Breadcrumb instead
- Only displaying static data → Use plain HTML/CSS
- Simple data tables → Use DataGrid instead

---

## Architecture Overview

```
TreeViewComponent
├── Data Layer
│   ├── Hierarchical Structure
│   ├── Self-Referential Model
│   ├── Remote Data (OData, WebAPI)
│   └── Load-on-Demand
│
├── Node Management
│   ├── CRUD Operations (add, remove, update, move)
│   ├── Dynamic Refresh
│   └── Programmatic Access
│
├── User Interaction
│   ├── Selection (Single/Multi)
│   ├── Checking (Three-state)
│   ├── Editing (Inline)
│   ├── Drag-Drop (Single/Multi)
│   └── Keyboard Navigation
│
├── Customization
│   ├── Templates (String/HTML/JSX)
│   ├── Stateless Templates (Performance)
│   ├── drawNode Callback (Custom Rendering)
│   ├── Icons & Styling
│   └── CSS Customization by Level
│
├── Advanced Features
│   ├── Filtering & Searching
│   ├── Sorting (Global & Level-wise)
│   ├── Load-on-Demand Caching
│   ├── State Persistence
│   ├── RTL & Localization
│   ├── Accordion Pattern
│   └── Performance Optimization
│
├── Integration
│   ├── Context Menu
│   ├── Toolbar
│   ├── Tooltips
│   └── Data Coordination
│
├── Accessibility
│   ├── Keyboard Shortcuts (15+)
│   ├── ARIA Attributes
│   ├── Screen Reader Support
│   └── WCAG 2.1 Compliance
│
└── Event System
    ├── Data Events (created, dataBound)
    ├── Selection Events (nodeSelected, nodeSelecting)
    ├── Expansion Events (nodeExpanded, nodeExpanding)
    ├── Editing Events (nodeEdited, nodeEditing)
    ├── Drag-Drop Events (nodeDragStart, nodeDragging, nodeDropped)
    ├── Checkbox Events (nodeChecked, nodeChecking)
    ├── Custom Rendering (drawNode)
    └── Keyboard Events (keyPress)
```

---

## What's Covered in This Comprehensive Skill

✅ **Complete API Reference** - 11 methods, 19 events, 35+ properties  
✅ **All Data Binding Patterns** - Hierarchical, self-referential, remote, load-on-demand  
✅ **Advanced Templating** - nodeTemplate, **statelessTemplates, drawNode callback**  
✅ **Selection Systems** - Single/multi-select, checkboxes, three-state, auto-sync  
✅ **Complete Drag-Drop** - Single/multi-node, validation, restrictions  
✅ **Filtering & Sorting** - Advanced patterns including level-wise sorting  
✅ **Editing** - Inline editing with validation and event control  
✅ **Customization** - Templates, icons, CSS by level, full-row selection  
✅ **Keyboard Navigation** - 15+ shortcuts, WCAG 2.1 compliance  
✅ **Accessibility** - ARIA, screen reader support, focus management  
✅ **Advanced Features** - Load-on-demand, persistence, RTL, localization, accordion  
✅ **Integration** - Context menu, toolbar, tooltip patterns  
✅ **Performance** - Stateless templates, large dataset optimization  
✅ **Real-World Patterns** - 50+ working code examples  
✅ **Event System** - Event cancellation, preventable events, custom handlers  

---

## Next Steps

1. **Start with [Getting Started](references/getting-started.md)** to install and set up
2. **Pick your use case** from the Quick Start Navigation above
3. **Reference the specific guide** for detailed patterns and examples
4. **Combine features** as needed for your specific requirement

---

**Status:** ✅ Comprehensive TreeView Implementation Guide  
**API Coverage:** 100% (All methods, events, and properties documented)  
**Code Examples:** 50+ working patterns  
**Version:** 2.0 (Enhanced with statelessTemplates, drawNode, advanced filtering, etc.)
