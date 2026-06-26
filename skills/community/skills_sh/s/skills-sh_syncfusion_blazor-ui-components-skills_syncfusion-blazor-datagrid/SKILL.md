---
name: syncfusion-blazor-datagrid
description: Implements the Syncfusion Blazor DataGrid (SfGrid) for efficient tabular operations such as sorting, filtering, paging, grouping, editing, aggregates, virtualization, lazy‑load grouping, and row or column spanning. Use this skill when building data‑grid workflows in Blazor Server, WebAssembly, Web App, or MAUI applications. Supports Excel/PDF export, virtual or infinite scrolling, customizable templates, and grid state persistence for consistent and optimized data‑grid behavior.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

***

# Implementing Syncfusion Blazor DataGrid

The Syncfusion Blazor DataGrid (`SfGrid<TValue>`) is a high-performance, feature-rich component for displaying and manipulating tabular data. It supports data binding, sorting, filtering, grouping, paging, editing, selection, aggregates, export, virtual/infinite scrolling, templates, and more.

**NuGet:** `Syncfusion.Blazor.Grid` + `Syncfusion.Blazor.Themes`  
**Namespace:** `Syncfusion.Blazor.Grids`

## When to Use This Skill

Use this skill when you need to:
- Set up and configure a DataGrid in Blazor Server, WebAssembly, Web App, or MAUI
- Bind local or remote data (OData, HTTP, SfDataManager)
- Configure columns (type, format, template, frozen, reorder, resize, chooser)
- Implement sorting, filtering (FilterBar/Menu/Excel/CheckBox), or searching
- Enable grouping with lazy load or caption templates
- Configure paging with custom templates or SfPager
- Set up virtual scrolling, infinite scrolling for large datasets
- Implement editing (Normal/Dialog/Batch/Command column) with validation
- Configure selection (row, cell, checkbox) with programmatic control
- Use clipboard copy, AutoFill, or Paste features
- Add aggregates (footer, group, caption, reactive)
- Use row/column templates, detail template, row drag-drop
- Configure toolbar, context menu, column menu, column chooser
- Export data to Excel or PDF
- Manage print functionality
- Optimize performance (SetRowDataAsync, PreventRender)
- Handle DataGrid events
- Manage state persistence (EnablePersistence)
- Customize styling and appearance
- Enable adaptive UI for mobile/responsive layouts

# 🔒 Mandatory Key Rules

These rules govern how this skill MUST behave. They are mandatory and must be strictly followed.

## 1. Purpose and Responsibility

Your responsibility is to interpret any natural‑language user request and provide:

*   Accurate
*   Complete
*   Validated

information about all supported aspects of the **Syncfusion Blazor DataGrid**, including:

*   Public APIs
*   Properties
*   Events
*   Features
*   Behaviors

## 2. Accuracy and API Compliance

The Skill MUST:

*   Use **only officially supported** Syncfusion DataGrid features.
*   **NEVER** invent APIs, methods, properties, events, behaviors, or future features.
*   **NEVER** provide unsupported or hypothetical code samples.
*   ALWAYS follow official Syncfusion component design patterns.

If a feature is **not supported**:

*   Clearly state the limitation.
*   Suggest a supported alternative when possible.

## 3. Interpreting Natural-Language Requests

When user requests are incomplete:

*   Infer reasonable assumptions using official Grid best practices.
*   Fill missing gaps with accurate and relevant information.
*   Request clarification **only** when essential.

## 4. Response Quality Requirements

Every response MUST:

*   Be technically accurate
*   Be complete and well‑structured
*   Include required dependencies and configuration notes
*   Follow real, documented Syncfusion API behavior
*   Avoid contradictions or ambiguity

## 5. Handling Unsupported User Requests

If the user asks for an unsupported capability:

*   Explicitly state that it is not supported
*   Suggest official alternatives or valid workarounds
*   NEVER simulate or fabricate impossible functionality

## 6. Design Pattern Enforcement

The Skill MUST follow Syncfusion official patterns, including:

*   Correct component structure (`SfGrid`, `GridColumn`, `GridEditSettings`, etc.)
*   Proper async event and API usage
*   Valid configuration properties and enums
*   Supported data‑binding approaches
*   Real event patterns and names

## 7. Quality, Completeness & Reliability

The Skill MUST:

*   Use only validated and real Grid capabilities
*   Provide actionable and implementation‑ready guidance
*   Ensure clarity so users can follow without guesswork
*   Maintain clean, readable, and professional formatting

## 8. No-Hallucination Safeguard

The Skill MUST NOT:

*   Invent non‑existent APIs or behavior
*   Suggest unsupported modes, features, or configuration
*   Provide incorrect, misleading, or unverifiable code
*   Describe undocumented internal behavior

If unsure:

*   Ask for clarification **OR**
*   Clearly state the limitation

## 9. Event Name Verification Requirement

**CRITICAL:** Event names MUST be verified against `references/events.md` BEFORE providing code examples. All grid events MUST be defined inside the `<GridEvents>` component

**Common Mistakes to Avoid:**

*   ❌ `OnSortChange` - Does NOT exist. Use `Sorting`, `Sorted` instead
*   ❌ `OnFilterChange` - Does NOT exist. Use `Filtering`, `Filtered` instead
*   ❌ `OnPageChange` - Does NOT exist. Use `PageChanging`, `PageChanged` instead
*   ❌ `OnGroupChange` - Does NOT exist. Use `Grouping`, `Grouped` instead

**Rule:** ALWAYS cross-reference `references/events.md` for:

*   Exact event names (case-sensitive)
*   Event argument types
*   Whether events are cancelable
*   When they fire (before/after operation)

**Verification Checklist Before Providing Event Code:**

1. Check if event name exists in `references/events.md`
2. Verify the correct `EventArgs` type
3. Confirm `Cancelable` status (✅ or ❌)
4. Test against actual Syncfusion documentation
5. Never assume naming conventions (e.g., `On` prefix, `Change` suffix)

---

## Strict Rules for Grid Events

### 1. **Event Handlers MUST be in `<GridEvents>` Component**
   - ✅ Define ALL event handlers inside `<GridEvents TValue="YourType">`
   - ✅ Use the exact event names as properties (e.g., `DataBound`, `RowSelecting`, `Grouped`)
   - ❌ DO NOT use `@onEventName` syntax on `<SfGrid>`
   - ❌ DO NOT define event handlers on any root element

### 2. **Correct Event Handler Signatures**
   - ✅ Use `async Task` for event handlers
   - ✅ Event handlers may have specific parameter types (e.g., `GridEventArgs`, `RowSelectEventArgs`)
   - ✅ Some events have no parameters (e.g., `DataBound()`, `Created()`)
   - ❌ Do not use synchronous `void` methods for async operations

### 3. **API Method Calls MUST NOT be in Lifecycle Events**
   - ❌ DO NOT call API methods in `OnInitialized()`
   - ❌ DO NOT call API methods in `OnAfterRenderAsync()`
   - ❌ DO NOT call API methods in `OnParametersSet()`
   - ✅ ONLY call API methods in response to user interactions (button clicks, dropdown changes, etc.)
   - ✅ API methods CAN be called inside GridEvents handlers

### 4. **Use Async/Await Pattern**
   - ✅ Always use `await` with async API methods
   - ✅ Define event handlers as `async Task`
   - ✅ Mark code block methods as `async Task`
   - ❌ Do not use synchronous method calls for async operations

### 5. **Grid Reference Required for API Calls**
   - ✅ Use `@ref="Grid"` to get the Grid instance
   - ✅ Use the reference to call API methods (e.g., `await Grid.GroupColumnAsync()`)
   - ❌ Do not attempt to call methods without a reference

### 6. **Event Types Must Match GridEvents TValue**
   - ✅ Set `TValue="YourDataType"` to match your data model
   - ✅ All event handlers will be properly typed with this model
   - ❌ Do not use generic or wrong type for TValue

---

## Navigation Guide

### Setup & Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet install, `_Imports.razor`, `Program.cs`, theme/script setup, basic grid

📄 **Read:** [references/getting-started-app-types.md](references/getting-started-app-types.md)
- Server App, Web App (Auto/WASM), MAUI variants

### Data
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local (List, ExpandoObject, DynamicObject, DataTable, ObservableCollection)

### Connecting to Adaptors (Remote Data)
📄 **Read:** [references/odatav4-adaptor.md](references/odatav4-adaptor.md)
- OData V4 service setup, ODataConventionModelBuilder, [EnableQuery], automatic $filter/$orderby/$skip/$top, CRUD with PATCH/DELETE

📄 **Read:** [references/web-api-adaptor.md](references/web-api-adaptor.md)
- Web API with { Items, Count } response, manual $filter/$orderby/$skip/$top QueryString parsing, CRUD with GET/POST/PUT/DELETE
- **Security note:** Do NOT bind `SfDataManager.Url` to arbitrary user-supplied URLs. Use an operator-configured string variable (for example `Url="@DataApiUrl"` where `DataApiUrl` is read from `ALLOWED_API_URL` in configuration), an internal proxy/gateway, field/operator whitelists, and server-side validation/sanitization. See [references/web-api-adaptor.md](references/web-api-adaptor.md) `Security Considerations` for examples.

📄 **Read:** [references/url-adaptor.md](references/url-adaptor.md)
- Custom API with { result, count } response, DataManagerRequest POST body, DataOperations helpers, InsertUrl/UpdateUrl/RemoveUrl/CrudUrl/BatchUrl
- **Security note:** Use a configuration-backed URL variable (for example `Url="@DataApiUrl"` where `DataApiUrl` is read from `ALLOWED_API_URL` in configuration), avoid user-supplied endpoints, and route third-party requests through an internal proxy/gateway. See [references/url-adaptor.md](references/url-adaptor.md) for examples and configuration snippets.

📄 **Read:** [references/custom-adaptor.md](references/custom-adaptor.md)
- DataAdaptor abstract class, override Read/Insert/Update/Remove/BatchUpdate, service injection, adaptor as component, custom parameters via Query.AddParams
- **Security note:** When implementing `CustomAdaptor`, do not trust `dm.Params` or user-supplied endpoints. Use operator-configured endpoints, validate `dm.Params`, whitelist fields/operators, and route third-party calls through a proxy. See [references/custom-adaptor.md](references/custom-adaptor.md) `Security Considerations` for examples.

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- ColumnType, Format, TextAlign, frozen, reorder, resize, chooser, stacked headers, column menu, foreign key

📄 **Read:** [references/cell.md](references/cell.md)
- QueryCellInfo, CustomAttributes, ClipMode, GridLines, tooltips

### Sorting, Filtering, Searching
📄 **Read:** [references/sorting.md](references/sorting.md)
- AllowSorting, multi-sort, SortColumnAsync, ClearSortingAsync

📄 **Read:** [references/filtering.md](references/filtering.md)
- AllowFiltering, FilterType (FilterBar/Menu/Excel/CheckBox), operators, FilterByColumnAsync

📄 **Read:** [references/searching.md](references/searching.md)
- Toolbar Search, SearchAsync, GridSearchSettings

### Grouping & Paging
📄 **Read:** [references/grouping.md](references/grouping.md)
- AllowGrouping, lazy load grouping, CaptionTemplate, programmatic group/ungroup

📄 **Read:** [references/paging.md](references/paging.md)
- AllowPaging, GridPageSettings, pager template, GoToPageAsync

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Height/Width, sticky header, ScrollIntoViewAsync

📄 **Read:** [references/virtual-scrolling.md](references/virtual-scrolling.md)
- EnableVirtualization, EnableColumnVirtualization, OverscanCount, limitations

📄 **Read:** [references/infinite-scrolling.md](references/infinite-scrolling.md)
- EnableInfiniteScrolling, GridInfiniteScrollSettings, cache mode, limitations

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- GridEditSettings, EditMode (Normal/Dialog/Batch/CommandColumn), ValidationRules, EditType, EditTemplate, CRUD methods

 **Read:** [references/editing-patterns.md](references/editing-patterns.md)
- Cancel edit based on condition, disable editing for specific rows
- Provide new/edited item via events, default column values, new row position
- Always-show add-new-row form, delete multiple rows, single-click editing
- Save new row at a specific index, inline template editing

📄 **Read:** [references/editing-validation.md](references/editing-validation.md)
- Per-column `ValidationRules`, Data Annotation attributes (`[Required]`, `[Range]`, etc.)
- Custom validation attributes, complex type validation, custom validator component


### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- AllowSelection, SelectionMode, SelectionType, checkbox selection, programmatic selection

📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Clipboard copy (Ctrl+C / Ctrl+Shift+H), CopyAsync, AutoFill drag handle, Paste (Ctrl+V), batch editing requirements

### Aggregates
📄 **Read:** [references/aggregates.md](references/aggregates.md)
- GridAggregates, AggregateType, FooterTemplate, GroupFooterTemplate, GroupCaptionTemplate, reactive aggregates

### Row Features & Templates
📄 **Read:** [references/row-features.md](references/row-features.md)
- RowDataBound, row drag-drop, row height, row spanning, RowTemplate

📄**Read:** [references/templates-structural.md](references/templates-structural.md)
- ColumnTemplate (image, hyperlink, checkbox, SfChip), HeaderTemplate, RowTemplate, RowTemplate formatting, DetailTemplate, expand/collapse APIs, expand on load, hide expand icon, custom CSS icons, hierarchical nested Grid

📄 **Read:** [references/templates-interactive.md](references/templates-interactive.md)
- ToolbarTemplate, Column EditTemplate, GridEditSettings Template, disable inputs on add vs edit, triple underscore nested binding, focus editor on dialog open, RowUpdating transform, FooterTemplate, CaptionTemplate, custom Blazor component in caption, locale customization, PagerTemplate

### Toolbar, Context Menu
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in/custom toolbar items, OnToolbarClick, ToolbarTemplate

📄 **Read:** [references/context-menu.md](references/context-menu.md)
- ContextMenuItems, custom items, ContextMenuItemClicked

### Export & Print
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- AllowExcelExport, ExportToExcelAsync, ExcelExportProperties, theme/template export

📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- AllowPdfExport, ExportToPdfAsync, PdfExportProperties, template PDF export

📄 **Read:** [references/print.md](references/print.md)
- PrintAsync, PrintMode

### Performance, Events, State
📄 **Read:** [references/performance.md](references/performance.md)
- SetRowDataAsync, PreventRender, WebAssembly optimization, column virtualization tips

📄 **Read:** [references/events.md](references/events.md)
- Complete GridEvents<TValue> reference: all edit, selection, filter, sort, group, page, toolbar, export events

📄 **Read:** [references/state-management.md](references/state-management.md)
- EnablePersistence, GetPersistDataAsync, SetPersistDataAsync, ResetPersistDataAsync

### Styling & Adaptive UI
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- CSS classes for grid, header, rows, filtering, editing, grouping, aggregates

📄 **Read:** [references/adaptive-layout.md](references/adaptive-layout.md)
- EnableAdaptiveUI, RowRenderingMode, AdaptiveUIMode, mobile-responsive patterns

## Quick Start

```razor
@page "/datagrid-demo"
@using Syncfusion.Blazor.Grids

<SfGrid DataSource="@Orders" AllowPaging="true" AllowSorting="true" AllowFiltering="true">
    <GridPageSettings PageSize="10"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="OrderID"    HeaderText="Order ID"   IsPrimaryKey="true" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="CustomerID" HeaderText="Customer"   Width="150"></GridColumn>
        <GridColumn Field="Freight"    HeaderText="Freight"    Format="C2" Width="120" TextAlign="TextAlign.Right"></GridColumn>
        <GridColumn Field="OrderDate"  HeaderText="Order Date" Format="d"  Width="150" Type="ColumnType.Date"></GridColumn>
        <GridColumn Field="ShipCountry" HeaderText="Ship Country" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>

@code {
    public List<Order> Orders = new List<Order>
    {
        new Order { OrderID = 10248, CustomerID = "VINET", Freight = 32.38, OrderDate = new DateTime(1996,7,4), ShipCountry = "France" },
        new Order { OrderID = 10249, CustomerID = "TOMSP", Freight = 11.61, OrderDate = new DateTime(1996,7,5), ShipCountry = "Germany" },
    };
    public class Order
    {
        public int OrderID { get; set; }
        public string CustomerID { get; set; }
        public double Freight { get; set; }
        public DateTime OrderDate { get; set; }
        public string ShipCountry { get; set; }
    }
}
```

## Common Patterns

### Grid with Editing + Toolbar
```razor
<SfGrid DataSource="@Orders" Toolbar="@(new List<string>() { "Add","Edit","Delete","Update","Cancel" })">
    <GridEditSettings AllowAdding="true" AllowEditing="true" AllowDeleting="true" Mode="EditMode.Normal"></GridEditSettings>
    <GridColumns>
        <GridColumn Field="OrderID" IsPrimaryKey="true" ValidationRules="@(new ValidationRules{Required=true})"></GridColumn>
        <GridColumn Field="CustomerID" ValidationRules="@(new ValidationRules{Required=true})"></GridColumn>
        <GridColumn Field="Freight" EditType="EditType.NumericEdit"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Grid with Grouping + Paging
```razor
<SfGrid DataSource="@Orders" AllowGrouping="true" AllowPaging="true">
    <GridGroupSettings Columns="@(new string[]{"ShipCountry"})"></GridGroupSettings>
    <GridPageSettings PageSize="10"></GridPageSettings>
    <GridColumns>
        <GridColumn Field="OrderID" Width="120"></GridColumn>
        <GridColumn Field="CustomerID" Width="150"></GridColumn>
        <GridColumn Field="ShipCountry" Width="150"></GridColumn>
    </GridColumns>
</SfGrid>
```

### Grid Reference for Programmatic Control
```razor
<SfGrid @ref="Grid" DataSource="@Orders">...</SfGrid>
@code {
    SfGrid<Order> Grid;
    // Programmatic operations:
    // await Grid.SortColumnAsync("OrderID", SortDirection.Ascending, false);
    // await Grid.FilterByColumnAsync("ShipCountry", "equal", "France");
    // await Grid.GoToPageAsync(2);
    // await Grid.StartEditAsync();
    // await Grid.SelectRowAsync(0);
}
```

## Key Properties at a Glance

| Property | Description |
|---|---|
| `DataSource` | Bind `IEnumerable<T>` or `DataManagerRequest` |
| `AllowPaging` | Enable paging |
| `AllowSorting` | Enable sorting |
| `AllowFiltering` | Enable column filtering |
| `AllowGrouping` | Enable row grouping |
| `AllowSelection` | Enable row/cell selection |
| `Height` / `Width` | Fixed dimensions for scrolling |
| `Toolbar` | Built-in or custom toolbar items |
| `EnableVirtualization` | Row virtualization for large data |
| `EnableInfiniteScrolling` | Infinite scroll loading |
| `EnablePersistence` | Save state to localStorage |
| `EnableAdaptiveUI` | Mobile-responsive rendering |
````
