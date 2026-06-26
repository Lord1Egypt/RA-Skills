---
name: syncfusion-react-treegrid
description: Implements Syncfusion React TreeGrid for hierarchical data with sorting, filtering, editing, exporting, paging, virtual scrolling, and advanced features. Supports configuration, CRUD, aggregates, templates, state persistence, and performance optimization in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Syncfusion React TreeGrid

A comprehensive skill for implementing and customizing Syncfusion's React TreeGrid component. TreeGrid visualizes self-referential hierarchical data in a tabular layout with expand/collapse functionality, enterprise features like virtual scrolling, and comprehensive export options.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [TreeGrid Overview](#treegrid-overview)
- [Data Structure Rules](#data-structure-rules)
- [Documentation Navigation Guide](#documentation-navigation-guide)
- [Quick Start Example](#quick-start-example)


## When to Use This Skill

Use this skill when you need to:
- Display hierarchical or tree-structured data (organizational charts, file systems, bill of materials)
- Configure columns with proper data binding and formatting
- Implement data editing (cell, row, dialog, batch, template modes)
- Add sorting, filtering, and searching capabilities
- Handle row and cell operations (selection, templates, spanning)
- Optimize performance with virtual scrolling or infinite scrolling
- Configure paging and scrolling strategies
- Export data to PDF, Excel, or CSV formats
- Implement state persistence and aggregation
- Customize appearance with themes and styling
- Support accessibility and internationalization (RTL, localization)

## TreeGrid Overview

The TreeGrid is optimized for displaying self-referential hierarchical data with:
- **Auto-expand/collapse** functionality for collapsible rows
- **Enterprise features**: virtual scrolling, aggregates, state persistence
- **Adaptive UI** for mobile and small screens
- **Comprehensive export**: PDF, Excel, CSV formats
- **Full accessibility**: WCAG compliance, keyboard navigation, ARIA support
- **Internationalization**: RTL support, locale customization

## Data Structure Rules

### Rule 1: childMapping is MANDATORY for Hierarchical Data
**Severity**: 🔴 CRITICAL - Grid will not expand/collapse without this

**Requirement**:
```jsx
// ✅ REQUIRED - Must match data property name exactly
<TreeGridComponent 
  dataSource={data}
  childMapping='subtasks'>
  <ColumnsDirective>
    {/* Columns */}
  </ColumnsDirective>
</TreeGridComponent>

// ❌ WRONG - Will not work
<TreeGridComponent 
  dataSource={data}>
  {/* No childMapping = No expansion possible */}
</TreeGridComponent>
```

**Data Format**:
```jsx
// ✅ CORRECT - childMapping matches 'subtasks' property
const data = [
  {
    TaskID: 1,
    TaskName: 'Parent',
    subtasks: [  // Must match childMapping value exactly
      { TaskID: 2, TaskName: 'Child' }
    ]
  }
];
```

**Exception**: Use `idMapping` + `parentIdMapping` for flat parent-child structure:
```jsx
// Alternative: Flat structure with parent IDs
<TreeGridComponent 
  dataSource={flatData}
  idMapping='TaskID'
  parentIdMapping='ParentID'
  hasChildMapping='isParent'>
</TreeGridComponent>
```

---

### Rule 2: Data Type Matching is MANDATORY
**Severity**: 🟠 IMPORTANT - Type mismatches cause rendering/sorting issues

**Requirement**:
```jsx
// ✅ CORRECT - Type matches column definition
const data = [
  {
    TaskID: 1,              // number type
    TaskName: 'Planning',   // string type
    StartDate: new Date(),  // Date object for date columns
  }
];

// Column definition must match data types
<ColumnsDirective>
  <ColumnDirective field='TaskID' headerText='ID' type='number'></ColumnDirective>
  <ColumnDirective field='TaskName' headerText='Task' type='string'></ColumnDirective>
  <ColumnDirective field='StartDate' headerText='Date' type='date' format='yMd'></ColumnDirective>
</ColumnsDirective>

// ❌ WRONG - Type mismatch
const data = [
  {
    TaskID: '1',            // String instead of number
    StartDate: '02/03/2024' // String instead of Date object
  }
];
```
## Complete Props Reference

📄 **Property and Methods:** [references/programmatic-api.md](references/programmatic-api.md)

**📄 Events Reference**
📖 [references/events-reference.md](references/events-reference.md)
- Complete event reference guide
- Data events (actionBegin, actionComplete, actionFailure)
- Editing events (cellEdit, cellSave, beforeEdit)
- Selection events (rowSelected, rowDeselected, cellSelected)
- Expand/collapse events
- Column events (drag, drop, resize, hide, show)
- Row events and utilities

---

## Documentation Navigation Guide

### Data Binding

📖 [references/data-binding.md](references/data-binding.md)
- Local vs. remote data sources
- Self-referential parent-child relationships
- DataManager integration
- ExpandStateMapping for initial expand state
- Complex data binding for nested objects

### Column Configuration

📖 [references/column.md](references/column.md)
- Column definitions and field mapping
- Tree column index setup
- Data types and formatting
- Column templates and custom rendering
- Headers and styling
- Foreign key columns

### Row Operations 
📖 [references/row.md](references/row.md)
- Row templates and custom rendering
- Row height configuration
- Row spanning
- Detail templates for nested content
- Row drag-and-drop
- Indent and outdent operations

### Cell Operations 
📖 [references/cell.md](references/cell.md)
- Cell editing
- Cell templates, styling and attributes
- Cell selection
- Cell formatting


### Editing
📖 [references/editing.md](references/editing.md)
- Cell editing mode
- Row editing mode
- Dialog editing
- Batch editing
- Template editing
- Validation rules and custom validators
- Command column editing
- Server-side persistence

### Sorting

📖 [references/sorting.md](references/sorting.md)
- Single and multi-column sorting
- Initial sort order configuration
- Custom sort comparers
- Sorting with templates
- Programmatic sorting

### Filtering
📖 [references/filtering.md](references/filtering.md)
- Filter bar mode
- Filter menu mode
- Excel-like filtering
- Custom filters
- Programmatic filtering
- Filter templates

### Searching
📖 [references/searching.md](references/searching.md)
- Global search across all columns
- Search highlight
- Programmatic search
- Search with templates

### Selection
📖 [references/selection.md](references/selection.md)
- Row selection (single and multiple)
- Cell selection
- Checkbox selection
- Selection mode configuration
- Programmatic selection
- Selection change events

### Display & Layout (Performance & Presentation)

**📄 Paging**
📖 [references/paging.md](references/paging.md)
- Pager configuration and options
- Page size settings
- Initial page settings
- Pager template customization
- Programmatic pagination

**📄 Scrolling**
📖 [references/scrolling.md](references/scrolling.md)
- Vertical and horizontal scrolling
- Scroll height configuration
- Scroll position control
- Sticky headers
- Responsive scrolling

**📄 Frozen Rows and Columns**
📖 [references/frozen-rows-columns.md](references/frozen-rows-columns.md)
- Freeze header rows
- Freeze columns
- Freeze direction
- Lock columns
- IsFrozen property usage

**📄 Virtual Scrolling & Infinite Scrolling**
📖 [references/virtual-scrolling-infinite-scrolling.md](references/virtual-scrolling-infinite-scrolling.md)
- Virtual scrolling for large datasets
- Infinite scrolling configuration
- Row height for virtual scroll
- ViewportIndex and ViewportStartIndex
- Performance optimization with virtual scroll

### Aggregates
📖 [references/aggregates.md](references/aggregates.md)
- Standard aggregates (Sum, Average, Min, Max, Count)
- Custom aggregates
- Footer aggregates
- Group aggregates
- Hierarchical aggregates for child data

### State Persistence
📖 [references/state-persistence.md](references/state-persistence.md)
- Global state persistence
- Local state persistence
- ExpandState tracking
- Persist sort, filter, and paging
- State restoration on reload

### Toolbar
📖 [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items
- Custom toolbar items
- Toolbar item types (Button, Separator, Dropdown)
- Toolbar item click handling
- Toolbar template customization

### Context Menu
📖 [references/context-menu.md](references/context-menu.md)
- Built-in context menu items
- Custom context menu items
- Menu item click handling
- Copy/Edit/Delete operations
- Header context menu

### Adaptive View
📖 [references/adaptive-view.md](references/adaptive-view.md)
- Adaptive UI for small screens
- Full-screen dialogs
- Horizontal row rendering
- Responsive column adjustments
- Mobile optimization

### Loading Animation
📖 [references/loading-animation.md](references/loading-animation.md)
- Loading indicator display
- Custom loading spinner
- Loading state management
- Spinner animation control

### Export & Print

**📄 PDF Export**
📖 [references/pdf-export.md](references/pdf-export.md)
- PDF export configuration
- Export options (columns, format)
- Headers and footers
- Page orientation and size
- Server-side export
- Exporting hierarchical data

**📄 Excel Export**
📖 [references/excel-export.md](references/excel-export.md)
- Excel export configuration
- Export options (columns, formatting)
- Cell styling in export
- Headers and footers
- Server-side export
- Exporting hierarchical levels

**📄 Print**
📖 [references/print.md](references/print.md)
- Print configuration
- Print with custom layout
- Print specific ranges
- Print hierarchy levels
- Print preview

### Clipboard 
📖 [references/clipboard.md](references/clipboard.md)
- Copy cell content to clipboard
- Copy entire rows
- Paste operations
- Copy hierarchy with levels
- Clipboard event handling

### Column Features (Advanced)

**📄 Column Reorder**
📖 [references/column-reorder.md](references/column-reorder.md)
- Enable column drag-and-drop reordering
- Prevent specific columns from reordering
- Reorder events and callbacks
- Programmatic column reordering

**📄 Column Resize**
📖 [references/column-resize.md](references/column-resize.md)
- Enable column drag resize
- Auto-fit columns to content
- Column width constraints (min/max)
- Resize events
- Programmatic width changes
- Save/restore column widths

**📄 Column Menu**
📖 [references/column-menu.md](references/column-menu.md)
- Built-in column menu items
- Sort, filter, and column chooser from menu
- Custom menu items
- Menu events and handlers
- Conditional menu items

**📄 Column Chooser**
📖 [references/column-chooser.md](references/column-chooser.md)
- Toggle column visibility
- Column chooser dialog configuration
- Show/hide columns programmatically
- Column visibility events
- Save/restore column visibility

**📄 Command Column**
📖 [references/command-column.md](references/command-column.md)
- Built-in command buttons (Edit, Delete, Save, Cancel)
- Custom command buttons
- Command click handlers
- Icon customization
- Row action patterns

### Server Integration 
📖 [references/server-integration.md](references/server-integration.md)
- Remote data binding with DataManager
- Server-side CRUD operations
- Server-side filtering and sorting
- Server-side paging
- Custom request/response handling
- Error handling strategies
- Batch operations

### Validation Patterns
📖 [references/validation-patterns.md](references/validation-patterns.md)
- Column validation rules
- Custom validation logic
- Cross-field validation
- Async validation (API calls)
- Server-side validation
- Dialog form validation
- Conditional validation
- Error message display

### Performance Optimization
📖 [references/performance-optimization.md](references/performance-optimization.md)
- Virtual scrolling for large datasets (100k+ rows)
- Infinite scrolling with caching
- Bundle size optimization
- Disabling unnecessary features
- Server-side operations optimization
- Memoization and rendering optimization
- Template optimization
- Event handler optimization
- Benchmarking and performance monitoring
- Performance checklist

### Customization 

📖 [references/styling-appearance.md](references/styling-appearance.md)
- CSS class customization
- Theme selection (Material, Bootstrap, Fluent, Tailwind)
- CSS variable overrides
- Component-specific styling
- Dark mode support
- Row styling
- Cell styling

### Globalization

📖 [references/globalization.md](references/globalization.md)
- Internationalization (i18n)
- Localization (l10n) for UI text
- Right-to-left (RTL) support
- Date formatting per locale
- Number formatting per locale
- Currency localization

### Accessibility
📖 [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 Level AA compliance
- Keyboard navigation (all shortcuts)
- ARIA attributes and screen reader support
- Expand/collapse keyboard shortcuts
- Editing keyboard navigation
- Selection shortcuts

## Quick Start Example

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-treegrid';
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

interface ITreeData {
  TaskID?: number;
  TaskName?: string;
  parentID: number | null;
  Children?: ITreeData[];
}

export default function App() {
  const data: ITreeData[] = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      parentID: null,
      Children: [{ TaskID: 2, TaskName: 'Plan timeline', parentID: 1 }]
    }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      treeColumnIndex={1}
      height="auto"
      allowPaging={true}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </TreeGridComponent>
  );
}
```

### Core Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `dataSource` | Array \| DataManager | `[]` | Data source for TreeGrid |
| `childMapping` | string | `null` | Property name for child records (e.g., "Children") |
| `idMapping` | string | `null` | Property name for unique ID (flat data) |
| `parentIdMapping` | string | `null` | Property name for parent ID (flat data) |
| `hasChildMapping` | string | `null` | Property for lazy load indicator |
| `treeColumnIndex` | number | `0` | Column index for tree expand icons |
| `expandStateMapping` | string | `null` | Property for initial expand state |