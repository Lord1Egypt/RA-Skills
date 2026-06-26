# Frozen Columns in React Grid

## Table of Contents
- [Overview](#overview)
- [Freeze Columns](#freeze-columns)
- [Freeze Rows](#freeze-rows)
- [Freeze Headers](#freeze-headers)
- [Configuration](#configuration)

## Overview

Freezing keeps columns or rows visible while scrolling horizontally or vertically, useful for reference columns or headers.

## Freeze Columns

### Freeze Specific Columns

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} width='100%' height='400'>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' isFrozen={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' isFrozen={true} />
    <ColumnDirective field='OrderDate' headerText='Order Date' width='130' type='date' />
    <ColumnDirective field='ShipCity' headerText='Ship City' width='150' />
    <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
  </ColumnsDirective>
</GridComponent>
```

### Freeze First N Columns

```tsx
<GridComponent dataSource={data} frozenColumns={2}>  {/* First 2 columns frozen */}
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='OrderDate' headerText='Order Date' width='130' />
    <ColumnDirective field='Freight' headerText='Freight' width='120' />
  </ColumnsDirective>
</GridComponent>
```

## Freeze Rows

### Pin Rows to Top

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, ContextMenu, ContextMenuItem, Inject, Page } from '@syncfusion/ej2-react-grids';
import { taskData } from './datasource';
import * as React from 'react';

function App() {
    const isRowPinned=(data: object)=>
    {
      if (data && data.Status === 'Open' && data.Priority === 'Critical') {
        return true;
      }
      return false;
    }
    const contextMenuItems: ContextMenuItem[] = ['PinRow', 'UnpinRow'];
    return (<div className='control-pane'>
      <div className='control-section'>
        <GridComponent dataSource={taskData} allowPaging={true} contextMenuItems={contextMenuItems} height='230' isRowPinned={isRowPinned}>
          <ColumnsDirective>
            <ColumnDirective field='TaskID' headerText='Task ID' width={100} textAlign='Right' isPrimaryKey={true} />
            <ColumnDirective field='Title' headerText='Title' width={100} />
            <ColumnDirective field='Status' headerText='Status' width={100} />
            <ColumnDirective field='Assignee' headerText='Assignee' width={100} />
            <ColumnDirective field='Priority' headerText='Priority' width={100} />
          </ColumnsDirective>
          <Inject services={[ContextMenu, Page]}/>
        </GridComponent>
      </div>
    </div>);
}

export default App;
```

## Freeze Headers

### Freeze Column Headers

Headers automatically freeze when grid has height set:

```tsx
<GridComponent dataSource={data} height='400'>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    {/* Headers stay visible when scrolling */}
  </ColumnsDirective>
</GridComponent>
```

## Configuration

### Multiple Frozen Sections

```tsx
<GridComponent
  dataSource={data}
  frozenColumns={2}  // Left frozen columns
  frozenRows={3}     // Top frozen rows
  height='400'
  width='100%'
>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
</GridComponent>
```

### Freeze with Virtual Scrolling

```tsx
<GridComponent
  dataSource={largeData}
  enableVirtualization={true}
  frozenColumns={2}
  height='500'
>
  {/* columns with first 2 frozen */}
</GridComponent>
```

### Combine with Other Features

```tsx
<GridComponent
  dataSource={data}
  frozenColumns={2}
  allowSorting={true}
  allowFiltering={true}
  allowGrouping={true}
  height='400'
>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='120' />
  </ColumnsDirective>
  <Inject services={[Sort, Filter, Group]} />
</GridComponent>
```

### Hidden Frozen Column Header

```tsx
const columnTemplate = (props) => {
  return <span>Frozen</span>;
};

<ColumnDirective
  field='OrderID'
  headerText='Order ID'
  width='100'
  isFrozen={true}
  headerTemplate={columnTemplate}
/>
```

### Frozen Column Events

```tsx
const queryColumnInfo = (args) => {
  if (args.column.field === 'OrderID') {
    args.column.isFrozen = true;
  }
};

<GridComponent queryColumnInfo={queryColumnInfo}>
  {/* columns */}
</GridComponent>
```

## Performance and Scrolling Behavior

### Frozen Columns with Virtual Scrolling

```tsx
function GridWithFrozenAndVirtual() {
  return (
    <GridComponent
      dataSource={largeData}  // 100K+ records
      height='600'
      width='100%'
      frozenColumns={2}
      enableVirtualization={true}
      pageSettings={{ pageSize: 50 }}
    >
      <ColumnsDirective>
        {/* Frozen columns - always visible when scrolling right */}
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isFrozen={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' isFrozen={true} />
        
        {/* Regular scrollable columns */}
        <ColumnDirective field='OrderDate' headerText='Order Date' type='date' format='yMd' width='130' />
        <ColumnDirective field='ShipCity' headerText='Ship City' width='150' />
        <ColumnDirective field='ShipCountry' headerText='Ship Country' width='150' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='120' />
        <ColumnDirective field='ShipName' headerText='Ship Name' width='150' />
      </ColumnsDirective>
      <Inject services={[VirtualScroll]} />
    </GridComponent>
  );
}

export default GridWithFrozenAndVirtual;
```

### Performance Considerations

```tsx
// Best Practices for Frozen Columns:

// ✅ DO: Freeze only 1-3 reference columns
const goodConfig = {
  frozenColumns: 2  // OrderID, CustomerID
};

// ❌ DON'T: Freeze too many columns (creates horizontal scrolling of frozen area)
const badConfig = {
  frozenColumns: 10  // Too many!
};

// ✅ DO: Use with reasonable dataset sizes
const appropriateSize = {
  recordCount: 10000,  // Use frozen with pagination or virtual scroll
  frozenColumns: 2
};

// ❌ DON'T: Freeze without height constraint
const problematicSetup = (
  <GridComponent frozenColumns={2}>
    {/* Missing height - may cause layout issues */}
  </GridComponent>
);

// ✅ DO: Set explicit height and width
const optimalSetup = (
  <GridComponent
    frozenColumns={2}
    height='600px'
    width='100%'
  >
    {/* Properly constrained */}
  </GridComponent>
);
```

### Frozen Columns with Sorting and Filtering

```tsx
function GridWithFrozenAndFeatures() {
  return (
    <GridComponent
      dataSource={data}
      frozenColumns={2}
      allowSorting={true}
      allowFiltering={true}
      allowGrouping={true}
      allowSelection={true}
      height='500'
    >
      <ColumnsDirective>
        {/* Frozen reference columns */}
        <ColumnDirective
          field='OrderID'
          headerText='Order ID'
          width='100'
          isFrozen={true}
          isPrimaryKey={true}
        />
        <ColumnDirective
          field='CustomerID'
          headerText='Customer'
          width='120'
          isFrozen={true}
        />
        
        {/* Sortable/Filterable columns */}
        <ColumnDirective
          field='OrderDate'
          headerText='Order Date'
          type='date'
          format='yMd'
          width='130'
          allowSorting={true}
          allowFiltering={true}
        />
        <ColumnDirective
          field='ShipCountry'
          headerText='Country'
          width='130'
          allowGrouping={true}
        />
        <ColumnDirective
          field='Freight'
          headerText='Freight'
          format='C2'
          width='120'
          allowSorting={true}
        />
      </ColumnsDirective>
      <Inject services={[Sort, Filter, Group, Selection]} />
    </GridComponent>
  );
}

export default GridWithFrozenAndFeatures;
```

### Dynamic Frozen Column Toggle

```tsx
function GridWithToggleFrozen() {
  const gridRef = useRef(null);
  const [frozenColumnCount, setFrozenColumnCount] = useState(2);

  const toggleFreeze = () => {
    const newCount = frozenColumnCount === 2 ? 3 : 2;
    setFrozenColumnCount(newCount);
    gridRef.current.frozenColumns = newCount;
  };

  return (
    <div>
      <button onClick={toggleFreeze} style={{ marginBottom: '10px' }}>
        Toggle Frozen Columns ({frozenColumnCount})
      </button>
      <GridComponent
        ref={gridRef}
        dataSource={data}
        frozenColumns={frozenColumnCount}
        height='500'
        width='100%'
      >
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
          <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
          <ColumnDirective field='OrderDate' headerText='Order Date' type='date' format='yMd' width='130' />
          <ColumnDirective field='ShipCity' headerText='Ship City' width='150' />
          <ColumnDirective field='ShipCountry' headerText='Ship Country' width='150' />
          <ColumnDirective field='Freight' headerText='Freight' format='C2' width='120' />
        </ColumnsDirective>
      </GridComponent>
    </div>
  );
}

export default GridWithToggleFrozen;
```

### Frozen Rows and Columns Combined

```tsx
function GridWithFrozenRowsAndColumns() {
  return (
    <GridComponent
      dataSource={data}
      frozenColumns={2}
      frozenRows={2}
      height='600'
      width='100%'
      allowSorting={true}
      allowFiltering={true}
    >
      <ColumnsDirective>
        {/* Reference columns - always visible horizontally */}
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' isFrozen={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' isFrozen={true} />
        
        {/* Data columns - may scroll vertically and horizontally */}
        <ColumnDirective field='OrderDate' headerText='Order Date' type='date' format='yMd' width='130' />
        <ColumnDirective field='ShipCity' headerText='City' width='120' />
        <ColumnDirective field='ShipCountry' headerText='Country' width='130' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='120' />
      </ColumnsDirective>
      <Inject services={[Sort, Filter]} />
    </GridComponent>
  );
}

export default GridWithFrozenRowsAndColumns;
```

### Memory Optimization with Frozen Columns

```tsx
// For large datasets with frozen columns:

function OptimizedGridWithFrozen() {
  return (
    <GridComponent
      dataSource={largeData}
      frozenColumns={2}
      enableVirtualization={true}  // Critical for large datasets
      virtualScrollSettings={{
        enableWindowVirtualization: true
      }}
      height='600'
      width='100%'
      allowPaging={true}
      pageSettings={{ pageSize: 50 }}
    >
      <ColumnsDirective>
        {/* Keep frozen columns simple and light */}
        <ColumnDirective field='OrderID' headerText='Order ID' width='80' isFrozen={true} />
        <ColumnDirective field='CustomerID' headerText='Customer' width='100' isFrozen={true} />
        
        {/* Heavy data moved to scrollable area */}
        <ColumnDirective field='OrderDate' headerText='Date' type='date' format='yMd' width='100' />
        <ColumnDirective field='ShipAddress' headerText='Address' width='200' />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' width='100' />
      </ColumnsDirective>
      <Inject services={[VirtualScroll, Page]} />
    </GridComponent>
  );
}

export default OptimizedGridWithFrozen;
```
