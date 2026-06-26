# Styling and Appearance in React Grid

## Table of Contents
- [Overview](#overview)
- [Themes](#themes)
- [CSS Customization](#css-customization)
- [Dark Mode](#dark-mode)
- [Size Modes](#size-modes)

## Overview

The grid provides comprehensive theming and customization options to match your application's design.

## Themes

### Available Themes

```tsx
// Material 3 (Default)
@import '../node_modules/@syncfusion/ej2-react-grids/styles/material3.css';

// Bootstrap
@import '../node_modules/@syncfusion/ej2-react-grids/styles/bootstrap.css';

// Bootstrap 5
@import '../node_modules/@syncfusion/ej2-react-grids/styles/bootstrap5.css';

// Fabric
@import '../node_modules/@syncfusion/ej2-react-grids/styles/fabric.css';

// Tailwind CSS
@import '../node_modules/@syncfusion/ej2-react-grids/styles/tailwind.css';
```

### Switch Themes Dynamically

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);
  const [theme, setTheme] = React.useState('material3');

  const switchTheme = (themeName) => {
    // Remove current theme
    const link = document.querySelector('link[data-theme]');
    if (link) link.remove();

    // Add new theme
    const newLink = document.createElement('link');
    newLink.rel = 'stylesheet';
    newLink.href = `/styles/${themeName}.css`;
    newLink.setAttribute('data-theme', themeName);
    document.head.appendChild(newLink);

    setTheme(themeName);
  };

  return (
    <div>
      <select onChange={(e) => switchTheme(e.target.value)}>
        <option value='material3'>Material 3</option>
        <option value='bootstrap'>Bootstrap</option>
        <option value='bootstrap5'>Bootstrap 5</option>
        <option value='fabric'>Fabric</option>
      </select>

      <GridComponent ref={gridRef} dataSource={data}>
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default App;
```

## CSS Customization

### Custom Row Styling

```tsx
const rowTemplate = (props) => {
  const className = props.Freight > 50 ? 'high-value' : 'normal-value';
  
  return (
    <tr className={className}>
      <td>{props.OrderID}</td>
      <td>{props.CustomerID}</td>
      <td>${props.Freight.toFixed(2)}</td>
    </tr>
  );
};

<GridComponent
  dataSource={data}
  rowTemplate={rowTemplate}
>
  {/* columns */}
  <style>{`
    .high-value {
      background-color: #ffe6e6;
      font-weight: bold;
    }
    .normal-value {
      background-color: #ffffff;
    }
  `}</style>
</GridComponent>
```

### Alternating Row Colors

```tsx
const gridStyle = `
  .e-grid .e-table tbody tr:nth-child(odd) {
    background-color: #f9f9f9;
  }
  .e-grid .e-table tbody tr:nth-child(even) {
    background-color: #ffffff;
  }
  .e-grid .e-table tbody tr:hover {
    background-color: #e3f2fd;
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{gridStyle}</style>
</GridComponent>
```

### Column Cell Styling

```tsx
const queryCellInfo = (args) => {
  if (args.column.field === 'Freight') {
    if (args.data.Freight > 50) {
      args.cell.style.backgroundColor = '#ffcccc';
      args.cell.style.color = '#cc0000';
      args.cell.style.fontWeight = 'bold';
    }
  }
};

<GridComponent queryCellInfo={queryCellInfo}>
  {/* columns */}
</GridComponent>
```

## Dark Mode

### Enable Dark Theme

```tsx
// Import dark theme CSS
@import '../node_modules/@syncfusion/ej2-react-grids/styles/material3-dark.css';

// Or Material Dark variant
@import '../node_modules/@syncfusion/ej2-react-grids/styles/material-dark.css';
```

### Toggle Dark Mode

```tsx
const toggleDarkMode = () => {
  const htmlElement = document.documentElement;
  const isDark = htmlElement.getAttribute('data-theme') === 'dark';

  if (isDark) {
    htmlElement.removeAttribute('data-theme');
  } else {
    htmlElement.setAttribute('data-theme', 'dark');
  }
};

<button onClick={toggleDarkMode}>Toggle Dark Mode</button>
```

## Size Modes

### Compact Mode

```tsx
<GridComponent
  dataSource={data}
  enableRtl={false}
  rowHeight={32}  // Smaller row height
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' width='80' />  // Smaller width
    <ColumnDirective field='CustomerID' width='100' />
  </ColumnsDirective>
</GridComponent>
```

### Spacious Mode

```tsx
<GridComponent
  dataSource={data}
  style={{ fontSize: '16px' }}
  rowHeight={48}  // Larger row height
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' width='120' />
    <ColumnDirective field='CustomerID' width='150' />
  </ColumnsDirective>
</GridComponent>
```

### Custom Font and Colors

```tsx
const customStyle = `
  .e-grid {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    color: #333;
  }
  
  .e-grid .e-th {
    background-color: #2c3e50;
    color: #ffffff;
    font-weight: 600;
  }

  .e-grid .e-td {
    border-bottom: 1px solid #ecf0f1;
  }

  .e-grid.e-alt-row {
    background-color: #f8f9fa;
  }

  .e-grid .e-pagercontainer {
    background-color: #f5f5f5;
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{customStyle}</style>
</GridComponent>
```

## CSS Class Reference Guide

### Grid Container
```css
.e-grid             /* Main grid container */
.e-gridheader       /* Header container */
.e-gridcontent      /* Content/Body container */
.e-footer           /* Footer container */
```

### Header Styling
```css
.e-headercell       /* Header cell */
.e-headercell.e-sort      /* Header with sort */
.e-headercell.e-groupcaption  /* Group caption header */
.e-headertext       /* Header text content */
```

### Row and Cell Styling
```css
.e-row              /* Data row */
.e-row:hover        /* Hovered row */
.e-selectionbackground  /* Selected row background */
.e-selectionfocus   /* Selected cell focus */
.e-grid td          /* Table data cell */
.e-gridcell         /* Grid cell */
.e-gridcontent .e-selectionbackground /* Selected cell */
```

### Edit Mode Classes
```css
.e-inlineEdit       /* Inline edit mode */
.e-dialog           /* Dialog edit mode */
.e-batchedit        /* Batch edit mode */
.e-editedrow        /* Currently edited row */
.e-inline-edit-content /* Edit content area */
```

### Pagination and Toolbar
```css
.e-pagercontainer   /* Pager container */
.e-numericitem      /* Page number item */
.e-pagercontainer .e-pagerjump   /* Jump to page */
.e-toolbar          /* Toolbar container */
.e-toolbar .e-toolbar-item        /* Toolbar button */
.e-toolbar .e-toolbar-item.e-active /* Active toolbar item */
```

### Filter and Sort
```css
.e-filterbar        /* Filter bar row */
.e-filterinput      /* Filter input field */
.e-sortnumber       /* Sort number indicator */
.e-ascending        /* Ascending sort arrow */
.e-descending       /* Descending sort arrow */
.e-filterclear      /* Filter clear button */
```

### Selection and Grouping
```css
.e-selectioncheckbox /* Selection checkbox */
.e-groupheader      /* Group header */
.e-groupremovefocus /* Group remove focus */
.e-groupcaption     /* Group caption */
.e-groupcaptioncell /* Group caption cell */
```

### State Classes
```css
.e-disabled         /* Disabled state */
.e-readonly         /* Read-only state */
.e-loading          /* Loading state */
.e-altrow           /* Alternate row */
```

## Advanced Styling Examples

### Highlight Status Columns

```tsx
const queryCellInfo = (args) => {
  if (args.column.field === 'Status') {
    switch (args.data.Status) {
      case 'Active':
        args.cell.style.backgroundColor = '#d4edda';
        args.cell.style.color = '#155724';
        args.cell.style.fontWeight = 'bold';
        break;
      case 'Pending':
        args.cell.style.backgroundColor = '#fff3cd';
        args.cell.style.color = '#856404';
        break;
      case 'Inactive':
        args.cell.style.backgroundColor = '#f8d7da';
        args.cell.style.color = '#721c24';
        break;
    }
  }
};

<GridComponent queryCellInfo={queryCellInfo}>
  {/* columns */}
</GridComponent>
```

### Custom Header Styling

```tsx
const headerCellInfo = (args) => {
  args.cell.style.backgroundColor = '#1976d2';
  args.cell.style.color = '#ffffff';
  args.cell.style.fontSize = '14px';
  args.cell.style.fontWeight = '600';
  args.cell.style.padding = '12px';
  args.cell.style.textAlign = 'center';
};

<GridComponent queryCellInfo={headerCellInfo}>
  {/* columns */}
</GridComponent>
```

### Row Selection Styling

```tsx
const recordClick = (args) => {
  args.rowElement.style.backgroundColor = '#bbdefb';
};

const rowDataBound = (args) => {
  if (args.data.IsSelected) {
    args.row.classList.add('custom-selected');
  }
};

const customStyle = `
  .custom-selected {
    background-color: #1976d2 !important;
    color: white;
  }
  
  .custom-selected td {
    color: white;
  }
`;

<GridComponent
  recordClick={recordClick}
  rowDataBound={rowDataBound}
>
  {/* columns */}
  <style>{customStyle}</style>
</GridComponent>
```

### Zebra Striping with Custom Colors

```tsx
const zebraStripeStyle = `
  .e-grid .e-table tbody tr:nth-child(odd) {
    background-color: #ffffff;
  }
  
  .e-grid .e-table tbody tr:nth-child(even) {
    background-color: #f5f5f5;
  }
  
  .e-grid .e-table tbody tr:hover {
    background-color: #e8f4f8 !important;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
  }
  
  .e-grid .e-table thead tr {
    background-color: #263238;
    color: white;
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{zebraStripeStyle}</style>
</GridComponent>
```

### Responsive Font Sizes

```tsx
const responsiveStyle = `
  /* Large screens */
  @media (min-width: 1200px) {
    .e-grid {
      font-size: 14px;
    }
    .e-grid .e-th {
      padding: 12px;
    }
  }
  
  /* Tablets */
  @media (min-width: 768px) and (max-width: 1199px) {
    .e-grid {
      font-size: 13px;
    }
    .e-grid .e-th {
      padding: 10px;
    }
  }
  
  /* Mobile */
  @media (max-width: 767px) {
    .e-grid {
      font-size: 12px;
    }
    .e-grid .e-th {
      padding: 8px;
    }
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{responsiveStyle}</style>
</GridComponent>
```

### Border and Separator Customization

```tsx
const borderStyle = `
  .e-grid {
    border: 1px solid #d0d0d0;
  }
  
  .e-grid .e-gridheader {
    border-bottom: 2px solid #1976d2;
  }
  
  .e-grid .e-table th,
  .e-grid .e-table td {
    border-right: 1px solid #e0e0e0;
  }
  
  .e-grid .e-table th:last-child,
  .e-grid .e-table td:last-child {
    border-right: none;
  }
  
  .e-grid .e-table td {
    border-bottom: 1px solid #f0f0f0;
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{borderStyle}</style>
</GridComponent>
```

## Material Design Integration

### Material Icons

```tsx
import { Icon } from '@syncfusion/ej2-base';

const toolbarItems = [
  { 
    id: 'grid-add', 
    text: 'Add', 
    tooltipText: 'Add new row',
    prefixIcon: 'e-icon-add'
  },
  { 
    id: 'grid-edit', 
    text: 'Edit', 
    tooltipText: 'Edit selected row',
    prefixIcon: 'e-icon-edit'
  },
  { 
    id: 'grid-delete', 
    text: 'Delete', 
    tooltipText: 'Delete selected row',
    prefixIcon: 'e-icon-delete'
  }
];

<GridComponent toolbar={toolbarItems}>
  {/* columns */}
</GridComponent>
```

### Material Color Palette

```tsx
const materialColors = `
  :root {
    --primary-color: #1976d2;
    --primary-dark: #1565c0;
    --primary-light: #42a5f5;
    --accent-color: #ff4081;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --danger-color: #f44336;
    --info-color: #2196f3;
  }
  
  .e-grid .e-th {
    background-color: var(--primary-color);
    color: white;
  }
  
  .e-grid .e-row:hover {
    background-color: #f5f5f5;
  }
  
  .e-grid .e-selectionbackground {
    background-color: var(--primary-light) !important;
  }
`;

<GridComponent dataSource={data}>
  {/* columns */}
  <style>{materialColors}</style>
</GridComponent>
```
