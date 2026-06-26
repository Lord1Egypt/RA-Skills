# Filter Types: Bar, Menu, and Excel

Choose filter type by use case:

| Type | UI | Best For | When to Use |
|------|-----|----------|-----------|
| **FilterBar** | Inline cells | Quick text search | Simple queries, speed-focused, small datasets |
| **Menu** | Dropdown dialog | Structured operators | Complex conditions, power users, typed data |
| **Excel** | Checkbox list | Multi-select | Large categorical data, ENUM values |

## Table of Contents
- [1. FilterBar Filter](#1-filterbar-filter) — Template lifecycle (create/read/write/destroy)
- [2. Menu Filter](#2-menu-filter) — Custom operators, filter.ui, MultiSelect
- [3. Excel Filter](#3-excel-filter) — ENUM filtering, remote datasource, infinite scroll

---

## 1. FilterBar Filter

### When to Use?
- Users need quick text-based search with instant feedback
- Dataset < 10k rows (no performance issues)
- Simple string matching, not complex boolean logic
- Mobile-friendly, minimal UI footprint

### Setup
```tsx
<GridComponent dataSource={data} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

### Filter Expressions (Built-in Operators)
| Expression | Meaning | Example |
|-----------|---------|---------|
| `=value` | Equals | `=VINET` |
| `!=value` | Not equals | `!=USA` |
| `>value` / `<value` | Greater/Less than | `>100` |
| `*value` | Starts with | `*VIN` |
| `%value` | Ends with | `%ET` |

### Modes: Immediate vs OnEnter
```tsx
// Immediate (default) - Filter as you type
const filterSettings = { mode: 'Immediate' };

// OnEnter - Filter on Enter key press (better for large datasets)
const filterSettings = { mode: 'OnEnter' };

<GridComponent dataSource={data} filterSettings={filterSettings}>
  {/* columns */}
</GridComponent>
```

### Template Lifecycle (create/read/write/destroy)

Replace default text input with custom components:

```tsx
const dateFilterTemplate = {
  create: (args) => {
    // Step 1: Initialize component once
    const dateElement = document.createElement('input');
    args.target.appendChild(dateElement);
    new DatePicker().appendTo(dateElement);
  },
  
  write: (args) => {
    // Step 2: Display existing filter value (if any)
    const datePicker = dateElement.ej2_instances[0];
    datePicker.value = args.filteredValue;
  },
  
  read: (args) => {
    // Step 3: Called when user applies filter - extract value
    const datePicker = dateElement.ej2_instances[0];
    args.fltrObj.filterByColumn(args.column.field, 'equal', datePicker.value);
  },
  
  destroy: () => {
    // Step 4: Optional cleanup
    if (dateElement?.ej2_instances?.[0]) {
      dateElement.ej2_instances[0].destroy();
    }
  }
};

<ColumnDirective field='OrderDate' filterBarTemplate={dateFilterTemplate} />
```

**Lifecycle Flow:** `create()` runs once → `write()` syncs previous filter (if exists) → `read()` extracts new value → `destroy()` cleans up.

---

## 2. Menu Filter

### When to Use?
- Need specific operators for typed data (dates: before/after; numbers: >, <, between)
- Power users want complex boolean filtering
- Different data types need different comparison logic

### Setup
```tsx
const filterSettings = { type: 'Menu' };

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='Freight' type='number' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

### Custom Components via filter.ui

Replace default input (AutoComplete, DatePicker) with custom UI:

```tsx
const customDropDown = {
  ui: {
    create: (args) => {
      // Initialize custom component
      const input = document.createElement('input');
      args.target.appendChild(input);
      new DropdownList({
        dataSource: ['USA', 'Canada', 'UK'],
        placeholder: 'Select country'
      }).appendTo(input);
    },
    
    read: (args) => {
      // Called on Apply - extract value and filter
      const ddl = input.ej2_instances[0];
      args.fltrObj.filterByColumn(args.column.field, args.operator, ddl.value);
    },
    
    write: (args) => {
      // Sync existing filter to component
      const ddl = input.ej2_instances[0];
      ddl.value = args.filteredValue;
    }
  }
};

<ColumnDirective field='ShipCountry' filter={customDropDown} />
```

### Customize Operators per Data Type

Limit available operators for specific column types:

```tsx
const filterSettings = {
  type: 'Menu',
  operators: {
    stringOperator: [
      { value: 'startsWith', text: 'Starts With' },
      { value: 'contains', text: 'Contains' },
      { value: 'equal', text: 'Equals' }
    ],
    numberOperator: [
      { value: 'equal', text: 'Equal' },
      { value: 'greaterThan', text: '>' },
      { value: 'lessThan', text: '<' }
    ],
    dateOperator: [
      { value: 'equal', text: '=' },
      { value: 'greaterThan', text: 'After' }
    ]
  }
};
```

### Multiple Values Filter (MultiSelect)

Filter with multiple selected values simultaneously:

```tsx
const multiSelectFilter = {
  ui: {
    create: (args) => {
      const input = document.createElement('input');
      args.target.appendChild(input);
      new MultiSelect({
        dataSource: ['VINET', 'TOMSP', 'HANAR'],
        mode: 'Delimiter',
        allowFiltering: true
      }).appendTo(input);
    },
    read: (args) => {
      const multi = input.ej2_instances[0];
      args.fltrObj.filterByColumn(args.column.field, args.operator, multi.value);
    }
  }
};

<ColumnDirective field='CustomerID' filter={multiSelectFilter} />
```

### Custom Inputs via filter.params

Modify default component behavior:

```tsx
// Disable AutoComplete autofill
<ColumnDirective field='CustomerID' filter={{ params: { autofill: false } }} />

// Hide numeric spin buttons
<ColumnDirective field='Freight' filter={{ params: { showSpinButton: false } }} />

// DatePicker with week numbers
<ColumnDirective field='OrderDate' filter={{ params: { weekNumber: true } }} />
```

---

## 3. Excel/CheckBox Filter

### When to Use?
- Select from predefined values (categorical, ENUM types)
- Large datasets with Status, Category, Priority columns
- Multi-select common (filter "Shipped" OR "Pending")
- Dataset > 10k unique values per column (use infinite scrolling)

### Excel Filter Setup
```tsx
const filterSettings = { type: 'Excel' };  // or 'CheckBox'

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='Status' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

### CheckBox Filter Setup
```tsx
const filterSettings = { type: 'CheckBox' };  // or 'Excel'

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true}>
  <ColumnsDirective>
    <ColumnDirective field='Status' />
  </ColumnsDirective>
  <Inject services={[Filter]} />
</GridComponent>
```

### Custom Remote Datasource Binding

Use different data for filter options vs grid display:

```tsx
const handleActionBegin = (args) => {
  if (args.requestType === 'filterBeforeOpen') {
    // Override filter datasource with remote API
    args.filterModel.options.dataSource = new DataManager({
      url: 'url',
      adaptor: new WebApiAdaptor()
    });
  }
};

<GridComponent dataSource={gridData} actionBegin={handleActionBegin}
  filterSettings={{ type: 'Excel' }} allowFiltering={true}>
  {/* Grid shows local ProductID, filter options from remote API */}
</GridComponent>
```

### ENUM Column Filtering

Filter columns with fixed enum values (Status, Priority) with custom rendering:

```tsx
const statusColors = {
  Pending: '#FFC107', Shipped: '#2196F3',
  Delivered: '#4CAF50', Cancelled: '#F44336'
};

const enumTemplate = (props) => (
  <div>
    <span style={{
      display: 'inline-block',
      width: '12px', height: '12px',
      backgroundColor: statusColors[props.Status],
      marginRight: '8px', borderRadius: '2px'
    }}></span>
    {props.Status}
  </div>
);

<ColumnDirective field='Status' filter={{ itemTemplate: enumTemplate }} />
```

### Infinite Scrolling for Large Data

Load checkbox values on-demand as user scrolls:

```tsx
const filterSettings = {
  type: 'Excel',
  enableInfiniteScrolling: true,
  itemsCount: 50  // Load 50 values at a time
};

<GridComponent dataSource={data} filterSettings={filterSettings}>
  {/* Dialog loads first 50, scrolling loads next 50 automatically */}
</GridComponent>
```

### Customize Checkbox Count (Default: 1000)

```tsx
const handleActionBegin = (args) => {
  if (args.requestType === 'filterchoicerequest' || args.requestType === 'filtersearchbegin') {
    args.filterChoiceCount = 3000;  // Show 3000 instead of default 1000
  }
};

<GridComponent actionBegin={handleActionBegin} filterSettings={{ type: 'Excel' }}>
  {/* columns */}
</GridComponent>
```

### Custom Item Templates for Checkboxes

Display formatted text/icons in checkbox list:

```tsx
// Simple custom text
const simpleTemplate = (props) => props.Delivered ? '✓ Delivered' : '✗ Not Delivered';

// With icons
const iconTemplate = (props) => (
  <div>
    <span>{{ Beverages: '🍹', Seafood: '🐟' }[props.Category] || '📦'}</span>
    {props.Category}
  </div>
);

<ColumnDirective field='Category' filter={{ itemTemplate: iconTemplate }} />
```

### Hide Search or Sort

```tsx
// Hide search box
<ColumnDirective field='Status' filter={{ hideSearchbox: true }} />

// Hide sort options (CSS)
.e-excel-ascending, .e-excel-descending { display: none; }
```

---

## Initial Filters (All Types)

Set default filters programmatically:

```tsx
const filterSettings = {
  type: 'Menu',
  columns: [
    { field: 'CustomerID', operator: 'startsWith', value: 'A' },
    { field: 'Freight', operator: 'greaterThan', value: 50 }
  ]
};

<GridComponent dataSource={data} filterSettings={filterSettings} allowFiltering={true}>
  {/* Filters apply on load */}
</GridComponent>
```

---

## Programmatic Filter Methods

```tsx
// Apply filter programmatically
grid.filterByColumn('CustomerID', 'startsWith', 'A');

// Clear single column
grid.removeFilteredColsByField('CustomerID');

// Clear all
grid.clearFiltering();

// Get current filters
const current = grid.filterSettings.columns;
```

---

## Comparison: FilterBar vs Menu vs Excel

| Feature | FilterBar | Menu | Excel |
|---------|-----------|------|-------|
| UI | Inline cells | Dialog | Checkbox list |
| Operators | Limited (=,!=,>,<,*,%) | Full set | All unique values |
| Custom templates | Yes (create/read/write) | Yes (filter.ui) | Yes (itemTemplate) |
| Large data | Slow | Good | Excellent (+ scrolling) |
| Learning curve | Low | Medium | Low |
| Mobile friendly | Yes | Moderate | Good |
