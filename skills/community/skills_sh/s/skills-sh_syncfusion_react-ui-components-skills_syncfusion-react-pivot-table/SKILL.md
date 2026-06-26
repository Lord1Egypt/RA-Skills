---
name: syncfusion-react-pivot-table
description: Use this skill when users ask how to build or customize Syncfusion PivotView pivot tables in React. Trigger for React pivot grid/OLAP, aggregation, data binding (JSON/remote), drill-down/drill-through, grouping, filtering, conditional formatting, exports (Excel/PDF/CSV), or pivot charts. React-only, not Angular/Vue/Blazor.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Implementing PivotView in React

The Syncfusion React PivotView component enables powerful data analysis and reporting capabilities. It allows users to organize, analyze, and summarize multidimensional data through interactive pivot tables with features like grouping, filtering, aggregation, drill-down analysis, and export functionality.

> ⚠️ **Important:** Always verify API class names, properties, and method signatures by consulting the **reference files in this skill** (`references/*.md`). These are maintained with verified, working examples. Do not assume API details from other sources.

## ⚠️ Security Warning: Data Source Validation

**CRITICAL SECURITY NOTICE:** When implementing pivot tables, always use trusted data sources. **Never** fetch or bind data from untrusted or user-provided URLs without proper validation and sanitization.

### Security Best Practices:

1. **Use Local Data**: Prefer local, in-memory data sources for maximum security
2. **Validate Remote Sources**: Only connect to authenticated and authorized API endpoints under your control
3. **Sanitize User Input**: Never allow users to specify arbitrary URLs or data sources
4. **Implement Authentication**: Always use authentication headers and secure API endpoints
5. **Content Validation**: Validate and sanitize all data received from external sources before binding
6. **Use HTTPS**: Always use HTTPS for remote data connections
7. **Rate Limiting**: Implement rate limiting on API endpoints to prevent abuse

### Security Risks:

- **Indirect Prompt Injection**: Untrusted third-party data can contain malicious content that manipulates AI agent behavior
- **Data Exfiltration**: Malicious data sources could attempt to extract sensitive information
- **Code Injection**: Untrusted data may contain scripts or harmful content

### Recommended Approach:

✅ **DO**: Use controlled, authenticated backend APIs
✅ **DO**: Implement server-side data validation
✅ **DO**: Use environment variables for API endpoints
✅ **DO**: Whitelist allowed data sources

❌ **DON'T**: Accept user-provided URLs
❌ **DON'T**: Bind to public, untrusted endpoints
❌ **DON'T**: Skip data validation and sanitization
❌ **DON'T**: Use HTTP for sensitive data

## When to Use This Skill

Use this skill when you need to:
- Create interactive pivot tables for data analysis
- Set up data aggregation and summarization
- Build dynamic reporting dashboards
- Configure row/column grouping with hierarchies
- Implement data filtering and sorting
- Add drill-down/drill-through capabilities
- Export reports to Excel or PDF
- Optimize performance for large datasets
- Style and format pivot table display
- Persist pivot table state across sessions

## Navigation Guide

### Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation, package setup, basic component creation, CSS imports, NextJS integration

📄 **Read (optional):** [references/nextjs-integration.md](references/nextjs-integration.md)
- Next.js App Router and Pages Router setup, dynamic imports, SSR considerations, API routes, deployment

### Data Management
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- JSON data binding, CSV data binding, remote data binding, field mapping, DataManager setup

📄 **Read:** [references/connecting-to-databases.md](references/connecting-to-databases.md)
- Database connections, Web API setup, SQL Server, MySQL, PostgreSQL, MongoDB, Oracle, Elasticsearch, Snowflake

📄 **Read:** [references/connecting-to-data-source.md](references/connecting-to-data-source.md)
- OLAP connections, server-side engine configuration, real-time data updates

### Visualization & Interaction
📄 **Read:** [references/pivot-chart.md](references/pivot-chart.md)
- Integrating pivot charts, chart types, visualization options, chart customization

📄 **Read:** [references/classic-layout.md](references/classic-layout.md)
- Classic layout configuration, layout switching, UI control options

📄 **Read:** [references/drill.md](references/drill.md)
- Drill-down and drill-through functionality, editing, navigation controls, event handling

### Data Organization & Display
📄 **Read:** [references/field-list.md](references/field-list.md)
- In-built field list (popup), stand-alone field list (fixed), field list modes, UI interactions, configuration options

📄 **Read:** [references/grouping-bar.md](references/grouping-bar.md)
- Grouping bar configuration, drag-and-drop operations, filter/sort/remove icons, fields panel, value type icon, exclusion options

📄 **Read:** [references/data-shaping.md](references/data-shaping.md)
- Aggregation functions, calculated fields (defining and editing), summary customization options

📄 **Read:** [references/aggregation.md](references/aggregation.md)
- 25+ aggregation types (Sum, Average, Count, etc.), advanced aggregations, base field configuration, runtime modification

📄 **Read:** [references/calculated-field.md](references/calculated-field.md)
- Interactive calculated field dialog, formula syntax and operators, code-based methods, format settings

📄 **Read:** [references/grouping.md](references/grouping.md)
- Data grouping feature, number grouping with ranges, date grouping with hierarchies, programmatic configuration, ungrouping

📄 **Read:** [references/data-formatting.md](references/data-formatting.md)
- Number formatting, conditional formatting, cell styling, tooltip customization

📄 **Read:** [references/grid-customization.md](references/grid-customization.md)
- Cell templates, row heights, column widths, text alignment, column resizing and reordering, dimension configuration

📄 **Read:** [references/row-and-column.md](references/row-and-column.md)
- Cell template customization, dimension configuration, row height, column width, resizing, reordering, text alignment

📄 **Read:** [references/filtering-and-sorting.md](references/filtering-and-sorting.md)
- Member filtering, label filtering, value filtering, sorting operations, filter customization

📄 **Read separately if needed:**
- [references/member-filtering.md](references/member-filtering.md) - Select/exclude specific members, interactive filter dialogs
- [references/label-filtering.md](references/label-filtering.md) - Filter by text patterns, date ranges, numeric ranges
- [references/value-filtering.md](references/value-filtering.md) - Filter by aggregated values, Top/Bottom N, percentage filtering
- [references/value-sorting.md](references/value-sorting.md) - Sort by measure values, ranking analysis, multi-level sorting

📄 **Read:** [references/show-hide-totals.md](references/show-hide-totals.md)
- Grand totals display, group totals configuration, subtotal calculation options

📄 **Read:** [references/state-persistence.md](references/state-persistence.md)
- Save and load pivot table state, persistence configuration, state management patterns

📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Toolbar controls, button customization, toolbar events and actions

📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Tooltip configuration, custom tooltip templates, tooltip formatting

📄 **Read:** [references/hyperlink.md](references/hyperlink.md)
- Hyperlink configuration, cell linking, navigation setup, link customization

### Navigation & Analysis
📄 **Read:** [references/drill.md](references/drill.md)
- Drill-down and drill-through functionality, hierarchical data exploration, editing capabilities

📄 **Read separately if needed:**
- [references/drill-down.md](references/drill-down.md) - Drill-down specific features
- [references/drill-through.md](references/drill-through.md) - Drill-through and raw data exploration

### Export & Output
📄 **Read:** [references/export.md](references/export.md)
- Excel export, PDF export, export configurations, custom export handlers

📄 **Read separately if needed:**
- [references/excel-export.md](references/excel-export.md) - Excel export details
- [references/pdf-export.md](references/pdf-export.md) - PDF export details

📄 **Read:** [references/print.md](references/print.md)
- Pivot table printing, chart printing, print configurations, browser compatibility

### Advanced & Performance
📄 **Read:** [references/defer-update.md](references/defer-update.md)
- Deferred layout updates, Apply button, batch field operations, performance optimization for large datasets

📄 **Read:** [references/performance.md](references/performance.md)
- Virtual scrolling, paging configuration, performance best practices, data compression

📄 **Read separately if needed:**
- [references/virtual-scrolling.md](references/virtual-scrolling.md) - Efficient rendering of 100K+ rows, virtual scroll settings, responsive optimization

## Quick Start

```css
/* App.css */
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-pivotview/styles/tailwind3.css';
```

```typescript
import { PivotViewComponent, Inject, GroupingBar, FieldList, IDataSet } from '@syncfusion/ej2-react-pivotview';
import './App.css';

const pivotData: IDataSet[] = [
  { Country: 'USA', Product: 'Laptops', Sales: 5000, Year: 2020 },
  { Country: 'USA', Product: 'Mobiles', Sales: 3000, Year: 2020 },
  { Country: 'Canada', Product: 'Laptops', Sales: 2500, Year: 2020 },
  { Country: 'Canada', Product: 'Mobiles', Sales: 1500, Year: 2020 }
];

function cellTemplate(props: any): JSX.Element {
  return (
    <span style={{ fontWeight: 'bold', color: '#333' }}>
      {props.cellInfo?.value}
    </span>
  );
}

function App() {
  const dataSourceSettings: DataSourceSettingsModel = {
    dataSource: pivotData as IDataSet[],
    rows: [{ name: 'Country' }],
    columns: [{ name: 'Product' }],
    values: [{ name: 'Sales', caption: 'Total Sales' }],
    showGrandTotals: true
  };

  return (
    <PivotViewComponent
      id="pivotview"
      dataSourceSettings={dataSourceSettings}
      cellTemplate={cellTemplate}
      showGroupingBar={true}
      showFieldList={true}
      height={350}
    >
      <Inject services={[GroupingBar, FieldList]} />
    </PivotViewComponent>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Basic Pivot Table with Row and Column Fields
```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }, { name: 'Region' }],
  columns: [{ name: 'Year' }, { name: 'Quarter' }],
  values: [{ name: 'Sales', caption: 'Total Sales' }]
};
```

### Pattern 2: Adding Filters and Aggregation
```typescript
const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [
    { name: 'Sales', type: 'Sum' },
    { name: 'Quantity', type: 'Avg' }
  ],
  filters: [{ name: 'Year' }]
};
```

### Pattern 3: Calculated Fields
```typescript
import { PivotViewComponent, Inject, CalculatedField, FieldList } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';

const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [
    { name: 'Sold', caption: 'Units Sold' },
    { name: 'Amount', caption: 'Amount' },
    { name: 'Total', caption: 'Total', type: 'CalculatedField' }  // ← Must add to values
  ],
  calculatedFieldSettings: [
    {
      name: 'Total',
      formula: '"Sum(Amount)"+"Sum(Sold)"'  // ← Formula with aggregation functions
    }
  ]
};
```

### Pattern 4: Cell Template with Conditional Formatting
```typescript
function cellTemplate(props: any): JSX.Element {
  const value = props.cellInfo?.value;
  const isTotal = props.cellInfo?.isGrandTotal || props.cellInfo?.isDeserialized;
  
  const getStyle = () => {
    const numValue = parseFloat(value);
    if (numValue > 4000) return { color: '#4CAF50', fontWeight: 'bold' }; // Green for high values
    if (numValue < 1000) return { color: '#f44336', fontWeight: 'bold' }; // Red for low values
    return { color: '#333' };
  };

  return (
    <span style={getStyle()}>
      {isTotal ? <strong>{value}</strong> : value}
    </span>
  );
}

const dataSourceSettings: DataSourceSettingsModel = {
  dataSource: data as IDataSet[],
  rows: [{ name: 'Country' }],
  columns: [{ name: 'Product' }],
  values: [{ name: 'Sales' }]
};
```

## Key Props & Configuration

| Property | Type | Description |
|----------|------|-----------|
| `dataSourceSettings` | object | Configures data source, fields, rows, columns, values, filters, aggregations, calculated fields, and formatting |
| `cellTemplate` | function | Custom cell rendering function that returns JSX.Element for value cells |
| `gridSettings` | GridSettings | Configures row height, column width, text wrapping, resizing, reordering |
| `height` | string/number | Component height in pixels or percentage |
| `width` | string/number | Component width in pixels or percentage |
| `showGroupingBar` | boolean | Shows/hides the grouping bar for drag-and-drop field management |
| `showFieldList` | boolean | Shows/hides the field list panel (built-in or side panel) |
| `allowCalculatedField` | boolean | Enables calculated field creation and editing via Field List dialog |
| `allowExcelExport` | boolean | Enables Excel export functionality |
| `allowPdfExport` | boolean | Enables PDF export functionality |
| `allowMemberFilter` | boolean | Enables member filtering in Field List (select/deselect members) |
| `allowLabelFilter` | boolean | Enables label filtering (filter by text/label values) |
| `allowValueFilter` | boolean | Enables value filtering (filter by aggregated values) |
| `allowDrillThrough` | boolean | Enables drill-through functionality to view pivot data |
| `allowConditionalFormatting` | boolean | Enables conditional formatting for cells based on values |
| `allowDeferLayoutUpdate` | boolean | Batches field operations in Field List, apply only on "Apply" click |
| `enableVirtualization` | boolean | Enables virtual scrolling for large datasets |
| `enablePaging` | boolean | Enables paging for row/column distribution |
| `showToolbar` | boolean | Shows/hides the toolbar with preset actions |
| `pageSettings` | PageSettings | Configures row and column page sizes for paging |

### GridSettings Configuration
- `rowHeight`: Specifies row height in pixels
- `columnWidth`: Sets default column width
- `allowResizing`: Enables column/row resizing
- `allowReordering`: Allows drag-and-drop field reordering
- `allowTextWrap`: Enables text wrapping in cells
- `columnRender`: Event handler for column customization (e.g., text alignment)

## Related Skills
- Syncfusion React Grid - For general data grid functionality
- React Data Binding - For data source management patterns
