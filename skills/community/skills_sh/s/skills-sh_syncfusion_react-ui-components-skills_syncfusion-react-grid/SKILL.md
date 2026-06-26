---
name: syncfusion-react-grid
description: Implements Syncfusion React Grid component for feature-rich data tables and grids. Use this when working with data display, sorting, filtering, grouping, aggregates, editing, or exporting. This skill covers grid configuration, CRUD operations, virtual scrolling or infinite scrolling,  hierarchy grids, state persistence, and advanced data management features for data-intensive applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Syncfusion React Grid

The Syncfusion React Grid is a comprehensive, feature-rich component for displaying and manipulating tabular data. It provides extensive functionality for data binding, paging, sorting, filtering, grouping, editing, exporting, scrolling modes, row/column customization, and advanced state management to handle datasets of any size and complexity efficiently.

## ⚠️ Security & Trust Boundary
 
- The Grid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Mandatory Rules for Inbuilt API](#mandatory-rules-for-inbuilt-api)
- [Feature/Skill Navigation Guide](#feature-navigation-guide)
- [Quick Start Example](#quick-start-example)

## When to Use This Skill

Use the Syncfusion React Grid when you need to:

- **Display tabular data** with rows and columns in a React application
- **Handle large datasets** efficiently with paging, virtual scrolling, or infinite scrolling
- **Enable sorting, filtering, and searching** for single or multiple columns
- **Edit data inline** with multiple edit modes (Inline, Batch, Dialog)
- **Export data** to Excel or PDF formats with customization
- **Group and aggregate data** with summaries and calculations
- **Customize rows and cells** with templates and styling
- **Manage complex column configurations** (frozen columns, spanning, reordering, resizing)
- **Optimize performance** when rendering thousands of records
- **Persist grid state** for user preferences and configuration
- **Provide responsive data views** for different screen sizes

## Component Overview

The Grid component provides:

- **Data Binding**: Support for local arrays, remote data sources, and DataManager integration
- **Paging**: Client-side pagination with customizable page size and navigation
- **Sorting**: Single and multi-column sorting with custom comparers
- **Filtering**: Multiple filter modes (Filter Bar, Filter Menu, Excel-like filter)
- **Searching**: Global search across columns
- **Grouping**: Group data by columns with aggregates and lazy loading
- **Selection**: Row, cell, and column selection with checkbox support
- **Editing**: Inline, Batch, and Dialog modes with validation and templates
- **Aggregates**: Sum, Average, Count, Min, Max with footer, group, and caption display
- **Exporting**: Excel and PDF export with templates and server-side support
- **Scrolling**: Standard, Virtual, and Infinite scrolling modes
- **Row Customization**: Templates, detail views, drag-drop, pinning, spanning
- **Column Customization**: Templates, resizing, reordering, freezing, spanning
- **Performance**: Optimized rendering for large datasets
- **Responsive Design**: Adaptive layouts for different screen sizes
- **Module System**: Feature-based modules to reduce bundle size

## Mandatory Rules for Inbuilt API

**CRITICAL**: Follow these rules when using Grid's inbuilt API (137+ methods, 65+ events, 95+ properties):

### Rule 1: Module Injection Required for Feature Methods
Methods only work if their module is injected. No error thrown if module missing.

| Method | Required Module | Example |
|--------|----------------|---------|
| `goToPage()` | `Page` | `<Inject services={[Page]} />` |
| `sortColumn()` | `Sort` | `<Inject services={[Sort]} />` |
| `filterByColumn()` | `Filter` | `<Inject services={[Filter]} />` |
| `addRecord()`, `deleteRecord()` | `Edit` | `<Inject services={[Edit]} />` |

### Rule 2: Properties vs Methods - Know the Difference
- **Properties**: Set via JSX props (`<GridComponent allowPaging={true} />`)
- **Methods**: Call via ref (`gridRef.current.goToPage(2)`)
- Can't set properties via methods or call methods via props

---

📄 **Full Properties API Reference:** [references/properties-configuration.md](references/properties-configuration.md) 
📄 **Full Methods API Reference:** [references/programmatic-api.md](references/programmatic-api.md)
📄 **Full Events API Reference:** [references/events-catalog.md](references/events-catalog.md)
📄 **Backend Integration:** [references/adaptors.md](references/adaptors.md)

---

## Feature Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic component initialization
- CSS imports and theme configuration
- Simple data binding example
- Module injection

### Data Management
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding with arrays
- Remote data with DataManager
- Loading indicators (Spinner, Shimmer)
- Data source configuration

### Column Configuration
📄 **Read:** [references/columns.md](references/columns.md)
- Column definition and properties
- Column types (string, number, date, boolean, checkbox)
- Column width and auto-fit
- Column templates and custom rendering
- Column features (spanning, reordering, resizing, freezing)

### Aggregation & Summaries
📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Footer aggregates (Sum, Avg, Count, Min, Max, etc.)
- Group footer aggregates
- Group caption aggregates
- Custom aggregate functions
- Reactive aggregate updates

### Navigation & Pagination
📄 **Read:** [references/paging.md](references/paging.md)
- Enable and configure paging
- Page size and navigation
- Page change events
- Customizing pager UI
- Query string integration

### Sorting Data
📄 **Read:** [references/sorting.md](references/sorting.md)
- Single and multi-column sorting
- Sort direction control
- Initial sort configuration
- Custom comparers
- Prevent sorting for specific columns

### Filtering

**Start here:** 📄 Read [references/filter-setup.md](references/filter-setup.md) — Enable filtering, choose filter type (FilterBar, Menu, Excel, CheckBox)

**Choose your type:**
- 📄 Read [references/filter-types.md](references/filter-types.md) — All 3 filter types: FilterBar (inline text), Menu (operators), Excel (checkboxes)
- 📄 Read [references/filter-operators.md](references/filter-operators.md) — All 21+ operators, syntax, wildcards, AND/OR logic

### Searching

📄 **Read:** [references/searching.md](references/searching.md)
- Grid search functionality
- Global search across columns
- Search with filter integration
- Case-sensitive search options

### Grouping Data
📄 **Read:** [references/grouping.md](references/grouping.md)
- Enable grouping by columns
- Group by multiple columns
- Caption templates
- Group footer aggregates
- Lazy-load grouping for performance

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Row, cell, column selection modes
- Checkbox selection
- Multiple selection handling
- Selection events and methods
- Programmatic selection

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- Enable editing (allowEditing, allowAdding, allowDeleting)
- Edit modes: Inline, Batch, Dialog
- Edit triggers (double-click, toolbar, keyboard)
- Custom edit templates
- Validation rules and error handling
- Primary key configuration

> ⚠️ `isPrimaryKey={true}` is required on the key column — editing silently fails without it.

### Row Features
📄 **Read:** [references/row.md](references/row.md)
- Row templates
- Detail templates (expand/collapse)
- Row drag and drop
- Row pinning
- Row spanning
- Row selection and events

### Exporting
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Basic Excel export functionality
- Export options and configuration
- Exporting with column templates
- Server-side export
- Formatting and styling in exports

📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PDF export setup
- Headers and footers
- Export options and customization
- Exporting with templates
- Server-side PDF export
- Page orientation and sizing

### Scrolling Modes
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Standard scrolling
- Virtual scrolling (performance optimization)
- Infinite scrolling
- Scrollbar customization
- Height and width configuration

> ⚠️ `height` is required — scroll is silently disabled without it. Do NOT combine with `allowPaging` in virtual scrolling and infinite scrolling.

| Rows | Mode | Key Config |
|---|---|---|
| < 1,000 | `allowPaging` | `Page` module |
| 1K – 100K | `enableVirtualization` + `height` | `VirtualScroll`, no paging |
| Continuous | `enableInfiniteScrolling` + `height` | `InfiniteScroll` |
| 100K+ grouped | `enableVirtualization` + `lazyLoadGrouping` | `VirtualScroll`, `Group` |

### Freezing & Pinning
📄 **Read:** [references/frozen.md](references/frozen.md)
- Freeze columns
- Freeze rows
- Freeze headers
- Row pinning
- Frozen column behavior

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items
- Custom toolbar buttons
- Toolbar icons and events
- Edit toolbar integration
- Toolbar item templates

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Built-in context menu items
- Custom context menus
- Context menu configuration
- Context menu events

### Cell Operations
📄 **Read:** [references/cell.md](references/cell.md)
- Cell editing and selection
- Cell templates
- Cell value formatting
- Cell ranges and operations
- Cell focus and navigation

📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy and paste functionality
- Clipboard events
- Custom clipboard actions
- Copy column headers
- Paste from external sources

### Printing
📄 **Read:** [references/print.md](references/print.md)
- Print grid
- Print templates
- Print customization
- Print specific rows/columns
- Print orientation and sizing

### Styling & Appearance
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- CSS customization
- Themes (Material, Bootstrap, Fabric)
- Dark mode support
- Inline styling and classes
- Custom color schemes
- Component size modes

> ⚠️ `rowDataBound` and `queryCellInfo` fire on every render — no API calls inside them.
> ❌ **Never** add both a column `template` and a `rowDataBound` handler targeting the same field — this produces duplicate, conflicting styling logic.

### Hierarchy & Nested Data
📄 **Read:** [references/hierarchy-grid.md](references/hierarchy-grid.md)
- Parent-child data structures
- Child grid
- Expand and collapse behavior
- Nested grid templates
- Detail row templates
- Hierarchical data configuration

### Adaptive Mode
📄 **Read:** [references/adaptive.md](references/adaptive.md)
- **enableAdaptiveUI**: Render filter, sort, column chooser, and edit dialogs in full-screen mode for better mobile usability. Apply `e-bigger` class to parent element.
- **Vertical row rendering**: Set `rowRenderingMode="Vertical"` to display row elements vertically instead of horizontally (default is Horizontal).
- **Vertical rendering features**: Supports paging, sorting, filtering, selection, dialog editing, aggregates, infinite scroll, and toolbar options.
- **rowRenderingMode note**: Column Menu (grouping, sorting, autofit, filter, column chooser) only works in Horizontal mode.
- **AdaptiveUIMode property**: Use `"Mobile"` to render adaptive layout only on mobile screens, or `"Both"` (default) for both mobile and desktop.
- **Mobile screen optimization**: Render adaptive dialogs and vertical layouts automatically when enableAdaptiveUI is enabled.

### Configuration Management
📄 **Read:** [references/global-local.md](references/global-local.md)
- Global grid settings
- Local column configuration
- Configuration precedence
- Configuration merging

📄 **Read:** [references/state-management.md](references/state-management.md)
- Persist grid state
- Save and restore grid state manually
- Restore grid to initial state
- Prevent specific properties from persisting
- Persist column templates and header text

⚠️ **Rule**: `enablePersistence={true}` must be enable when use state management in grid. 

### Module System & Architecture
📄 **Read:** [references/modules.md](references/modules.md)
- Grid module architecture and feature-based modules
- 30+ available modules and their dependencies
- Module injection patterns
- Feature-module mapping
- Bundle optimization and lazy loading
- Conditional module loading
- Every feature in the Syncfusion React Grid requires **explicit module injection** via `<Inject services={[...]} />`. Without injection, the feature is silently ignored — no error is thrown.
 
⚠️ **Rule**: `<Inject services={[...]} />` must be the **last child** inside `<GridComponent>`.

### Data Connectivity & Adaptors
📄 **Read:** [references/adaptors.md](references/adaptors.md)
- 7 adaptor types for backend integration
- UrlAdaptor, ODataV4Adaptor, WebApiAdaptor, GraphQLAdaptor
- Custom adaptors and RemoteSaveAdaptor
- Backend configuration examples (C#, Node.js)
- Request/response format specifications
- Error handling and adaptor comparison

### Performance Optimization
📄 **Read:** [references/performance.md](references/performance.md)
- Virtual scrolling for 10,000+ records
- Infinite scrolling and progressive loading
- Memory management and cleanup strategies
- Bundle size optimization
- Event debouncing and throttling
- Performance benchmarking and monitoring

### Accessibility & Compliance
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA implementation and screen readers
- Keyboard navigation (Tab, arrows, Enter, Escape)
- Color contrast and focus management
- Accessibility testing tools (axe, NVDA, JAWS)
- Semantic HTML practices

### Data Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Built-in validators (required, min, max, pattern)
- Custom validation functions
- Async validation with server checks
- Validation events and error display
- Server-side validation with ASP.NET
- Validation rules by column type

### Command Column & Row Actions
📄 **Read:** [references/command-column.md](references/command-column.md)
- Built-in commands (Edit, Delete, Save, Cancel)
- Custom command buttons
- Role-based and status-based commands
- Command click events
- Conditional command visibility
- CSS styling and icons

### Localization & Internationalization
📄 **Read:** [references/localization.md](references/localization.md)
- Multi-language support (60+ languages)
- Locale setup and culture configuration
- Number, date, and currency formatting
- RTL support (Arabic, Hebrew, Farsi)
- Custom localization and translation
- Language switcher implementation

### Responsive Design & Mobile
📄 **Read:** [references/responsive-design.md](references/responsive-design.md)
- Adaptive UI for mobile/tablet/desktop
- Responsive media queries and breakpoints
- Column visibility hiding rules
- Touch interactions (swipe, long-press)
- Mobile optimization strategies
- Device-specific styling patterns

### API Reference & Properties

📄 **Read:** [references/properties-configuration.md](references/properties-configuration.md)
- All 95+ configurable properties organized by category
- Quick reference table for quick lookup
- When to use each property
- Module requirements per property

### Programmatic Control (Methods)
 
📄 **Read:** [references/programmatic-api.md](references/programmatic-api.md)
- All 137+ Grid methods by category (data, row, column, sort, filter, group, page, edit, export)
- Method signatures and parameters
- Return values and usage patterns
- Module requirements per method

### Event Communication (Events)
 
📄 **Read:** [references/events-catalog.md](references/events-catalog.md)
- All 65+ Grid events with timing and use cases
- Wire `actionBegin` to **cancel** or **mutate before** an action (`args.cancel = true`, `args.data.field = value`)
- Wire `actionComplete` to **react after** (API call, toast, refresh, toolbar restore)
- Must wire `actionFailure` for error handling
- Use `args.requestType` to identify the action


### Advanced Patterns & Real-World Scenarios

📄 **Real-Time Updates:** [references/real-time-updates.md](references/real-time-updates.md)
- Auto-refresh, WebSocket, and SignalR integration patterns
- Push vs. pull data strategies
- Connection management and reconnection logic

📄 **Performance Monitoring:** [references/performance-monitoring.md](references/performance-monitoring.md)
- Measure grid operation times
- Identify rendering bottlenecks
- Optimization checklist
- Memory usage tracking

📄 **Testing Grids:** [references/testing-grids.md](references/testing-grids.md)
- Unit testing with Jest and React Testing Library
- Integration testing scenarios
- Snapshot testing
- Best practices for grid testing

## Quick Start Example

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';
import React from 'react';
import '../styles/App.css';

const gridRef = useRef<GridComponent | null>(null);
// Sample data
const data = [
  {
    OrderID: 10248,
    CustomerID: 'VINET',
    EmployeeID: 5,
    OrderDate: new Date(1996, 6, 4)
  },
  {
    OrderID: 10249,
    CustomerID: 'TOMSP',
    EmployeeID: 6,
    OrderDate: new Date(1996, 6, 5)
  },
];

function App() {
  return (
    <GridComponent
      ref={gridRef}
      dataSource={data}
      allowPaging={true}
      allowSorting={true}
      allowFiltering={true}
      pageSettings={{ pageSize: 10 }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' textAlign='Right' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='OrderDate' headerText='Order Date' width='130' type='date' format='yMd' />
      </ColumnsDirective>
      <Inject services={[Page, Sort, Filter]} />
    </GridComponent>
  );
}

export default App;
```

