# Global and Local Configuration in React Grid

## Table of Contents
- [Overview](#overview)
- [Global Settings](#global-settings)
- [Local Column Configuration](#local-column-configuration)
- [Configuration Precedence](#configuration-precedence)

## Overview

Grid configuration can be set globally on the component or locally on individual columns. Local settings override global settings.

## Global Settings

### Grid-Level Configuration

Global settings apply to all columns:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

const globalConfig = {
  allowSorting: true,
  allowFiltering: true,
  allowGrouping: true,
  allowSelection: true,
  allowPaging: true,
  pageSettings: { pageSize: 12 },
  height: '500px',
  width: '100%'
};

<GridComponent dataSource={data} {...globalConfig}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' />
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter, Group]} />
</GridComponent>
```

### Common Global Properties

```tsx
const globalSettings = {
  // Selection settings
  allowSelection: true,
  selectionSettings: { type: 'Multiple', mode: 'Row' },

  // Sorting settings
  allowSorting: true,
  allowMultiSorting: true,
  sortSettings: { columns: [] },

  // Filtering settings
  allowFiltering: true,
  filterSettings: { type: 'FilterBar' },

  // Grouping settings
  allowGrouping: true,
  groupSettings: { showDropArea: true },

  // Paging
  allowPaging: true,
  pageSettings: { pageSize: 12, pageCount: 5 },

  // Display
  height: '500px',
  width: '100%',
  rowHeight: 36,

  // Features
  allowExcelExport: true,
  allowPdfExport: true,
  allowPrinting: true,
  enableVirtualization: true
};
```

## Local Column Configuration

### Column-Level Settings

Settings specific to individual columns:

```tsx
<ColumnsDirective>
  {/* Column 1: Sortable, not filterable */}
  <ColumnDirective
    field='OrderID'
    headerText='Order ID'
    width='100'
    allowSorting={true}
    allowFiltering={false}
    allowGrouping={false}
  />

  {/* Column 2: Filterable, not sortable */}
  <ColumnDirective
    field='CustomerID'
    headerText='Customer'
    width='120'
    allowSorting={false}
    allowFiltering={true}
    allowGrouping={true}
  />

  {/* Column 3: Frozen, not editable */}
  <ColumnDirective
    field='OrderDate'
    headerText='Order Date'
    width='130'
    type='date'
    isFrozen={true}
    allowEditing={false}
  />
</ColumnsDirective>
```

### Local Column Priority Settings

```tsx
<ColumnDirective
  field='Freight'
  headerText='Freight'
  width='100'
  format='C2'
  textAlign='Right'
  allowSorting={true}
  allowFiltering={true}
  allowEditing={true}
  allowGrouping={true}
  displayAsCheckBox={false}
  visible={true}
/>
```

## Configuration Precedence

### Precedence Order

Local (Column) > Global (Grid) > Defaults

```tsx
// Global setting: All columns sorting enabled
<GridComponent allowSorting={true}>
  <ColumnsDirective>
    {/* Uses global sorting: true */}
    <ColumnDirective field='OrderID' />

    {/* Overrides global with local sorting: false */}
    <ColumnDirective field='CustomerID' allowSorting={false} />

    {/* Uses global sorting: true */}
    <ColumnDirective field='Freight' />
  </ColumnsDirective>
</GridComponent>
```

### Configuration Examples

```tsx
<GridComponent
  dataSource={data}
  // Global settings
  allowSorting={true}
  allowFiltering={true}
  allowGrouping={true}
  allowSelection={true}
  selectionSettings={{ type: 'Multiple', mode: 'Row' }}
  pageSettings={{ pageSize: 20 }}
  height='500'
>
  <ColumnsDirective>
    {/* Inherits all global settings */}
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />

    {/* local: Sorting disabled, but filtering/grouping enabled (global) */}
    <ColumnDirective
      field='CustomerID'
      headerText='Customer'
      width='120'
      allowSorting={false}
    />

    {/* Local: Custom format, frozen */}
    <ColumnDirective
      field='Freight'
      headerText='Freight'
      width='100'
      format='C2'
      isFrozen={true}
      allowGrouping={false}
    />

    {/* Local: Read-only, not editable */}
    <ColumnDirective
      field='OrderDate'
      headerText='Order Date'
      type='date'
      allowEditing={false}
      allowFiltering={false}
    />
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter, Group]} />
</GridComponent>
```

### Override Global Settings Per Column

```tsx
const columns = data.map(field => ({
  field: field,
  allowSorting: field !== 'InternalNotes',
  allowFiltering: field !== 'InternalID',
  allowGrouping: field !== 'CreatedDate'
}));

<GridComponent dataSource={data}>
  <ColumnsDirective>
    {columns.map(col => (
      <ColumnDirective key={col.field} {...col} />
    ))}
  </ColumnsDirective>
</GridComponent>
```

## Advanced Override Patterns

### Dynamic Global Configuration

```tsx
import React, { useState } from 'react';

function GridWithDynamicConfig() {
  const [config, setConfig] = useState({
    allowSorting: true,
    allowFiltering: true,
    allowGrouping: false,
    pageSize: 20
  });

  const toggleFeature = (feature) => {
    setConfig(prev => ({
      ...prev,
      [feature]: !prev[feature]
    }));
  };

  return (
    <div>
      <button onClick={() => toggleFeature('allowSorting')}>Toggle Sorting</button>
      <button onClick={() => toggleFeature('allowFiltering')}>Toggle Filtering</button>

      <GridComponent
        dataSource={data}
        allowSorting={config.allowSorting}
        allowFiltering={config.allowFiltering}
        allowGrouping={config.allowGrouping}
        pageSettings={{ pageSize: config.pageSize }}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithDynamicConfig;
```

### Conditional Column Configuration

```tsx
import React, { useState } from 'react';

function GridWithConditionalColumns() {
  const [userRole, setUserRole] = useState('viewer'); // 'viewer', 'editor', 'admin'

  const getColumnConfig = (field, role) => {
    const baseConfig = {
      field: field,
      headerText: field,
      width: 100
    };

    switch(role) {
      case 'viewer':
        return { ...baseConfig, allowEditing: false, allowFiltering: true };
      case 'editor':
        return { ...baseConfig, allowEditing: true, allowFiltering: true, allowSorting: true };
      case 'admin':
        return { ...baseConfig, allowEditing: true, allowFiltering: true, allowSorting: true, allowGrouping: true };
      default:
        return baseConfig;
    }
  };

  const columns = ['OrderID', 'CustomerID', 'Freight'];

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        {columns.map(field => (
          <ColumnDirective key={field} {...getColumnConfig(field, userRole)} />
        ))}
      </ColumnsDirective>
      <Inject services={[Page, Sort, Filter, Group, Edit]} />
    </GridComponent>
  );
}

export default GridWithConditionalColumns;
```

### Environment-Based Configuration

```tsx
// config.js
const gridConfig = {
  development: {
    allowSorting: true,
    allowFiltering: true,
    allowGrouping: true,
    enableVirtualization: false,
    pageSettings: { pageSize: 10 }
  },
  production: {
    allowSorting: true,
    allowFiltering: false,
    allowGrouping: false,
    enableVirtualization: true,
    pageSettings: { pageSize: 50 }
  }
};

export const getGridConfig = () => {
  const env = process.env.NODE_ENV || 'production';
  return gridConfig[env];
};

// In component
import { getGridConfig } from './config';

<GridComponent dataSource={data} {...getGridConfig()}>
  {/* columns */}
</GridComponent>
```

### Theme-Based Configuration

```tsx
function GridWithThemeConfig() {
  const [theme, setTheme] = useState('light');

  const themeConfig = {
    light: {
      height: '500px',
      style: { backgroundColor: '#ffffff', color: '#000000' }
    },
    dark: {
      height: '500px',
      style: { backgroundColor: '#1e1e1e', color: '#ffffff' }
    }
  };

  const config = themeConfig[theme];

  return (
    <div>
      <button onClick={() => setTheme('light')}>Light Theme</button>
      <button onClick={() => setTheme('dark')}>Dark Theme</button>

      <GridComponent
        dataSource={data}
        {...config}
      >
        {/* columns */}
      </GridComponent>
    </div>
  );
}

export default GridWithThemeConfig;
```

## Best Practices

### Configuration Checklist

1. **Define Global Defaults** - Set common behavior at grid level
2. **Override Selectively** - Use local config only when needed
3. **Document Precedence** - Document which settings override others
4. **Constants for Configs** - Store repeated configs as constants
5. **Lazy Load Complex Configs** - Load heavy configs on demand
6. **Test Precedence** - Verify local settings override globals
7. **Version Control** - Track config changes in git

### Configuration Template

```tsx
const defaultGridConfig = {
  // Layout
  height: '600px',
  width: '100%',
  rowHeight: 36,

  // Features
  allowPaging: true,
  allowSorting: true,
  allowFiltering: true,
  allowGrouping: true,
  allowSelection: true,
  allowExcelExport: true,
  allowPdfExport: true,

  // Settings
  pageSettings: { pageSize: 20, pageCount: 5 },
  sortSettings: { columns: [] },
  filterSettings: { type: 'FilterBar' },
  selectionSettings: { type: 'Multiple', mode: 'Row' },

  // Performance
  enableVirtualization: false,
  enableInfiniteScrolling: false
};

export const createGridConfig = (overrides = {}) => ({
  ...defaultGridConfig,
  ...overrides
});
```
