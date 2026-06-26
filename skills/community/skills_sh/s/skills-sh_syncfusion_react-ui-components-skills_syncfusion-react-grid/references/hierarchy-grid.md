# Hierarchy Grid in React Grid

## Table of Contents
- [Rules](#rules)
- [Overview](#overview)
- [Child Grid (childGrid prop)](#child-grid-childgrid-prop)
- [Master-Detail Structure](#master-detail-structure)
- [Nested Grid](#nested-grid)
- [Expand/Collapse](#expandcollapse)

## Rules

> ⚠️ Use either `childGrid` or `detailTemplate` — not both at the same time.

## Overview

Hierarchy grids display parent-child relationships by expanding detail rows to show related data.

## Enabling Hierarchy (DetailRow)

To enable master-detail (hierarchy) behavior using the built-in DetailRow feature, import the `DetailRow` module and inject it into the grid. This registers the service that manages detail rows.

```tsx
import { GridComponent, Inject, DetailRow } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={masterData} detailTemplate={detailTemplate}>
  <Inject services={[DetailRow]} />
</GridComponent>
```

The `detailTemplate` can return another `GridComponent` (or any JSX) to render child data for each master row.

## Child Grid (childGrid prop)

The preferred way to configure a hierarchy grid is via the `childGrid` prop on `<GridComponent>`. Unlike `detailTemplate`, this approach uses a plain options object (not JSX) and automatically handles parent-child linking via `queryString`.

### Basic Setup

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, DetailRow } from '@syncfusion/ej2-react-grids';

const childGridOptions = {
  columns: [
    { field: 'OrderID', headerText: 'Order ID', textAlign: 'Right', width: 120 },
    { field: 'CustomerID', headerText: 'Customer ID', width: 150 },
    { field: 'ShipCity', headerText: 'Ship City', width: 150 },
    { field: 'ShipName', headerText: 'Ship Name', width: 150 }
  ],
  dataSource: data,
  queryString: 'EmployeeID'  // Links parent EmployeeID to child EmployeeID
};

<GridComponent dataSource={employeeData} childGrid={childGridOptions} height={315}>
  <ColumnsDirective>
    <ColumnDirective field='EmployeeID' headerText='Employee ID' width='120' textAlign='Right' />
    <ColumnDirective field='FirstName' headerText='First Name' width='150' />
    <ColumnDirective field='City' headerText='City' width='150' />
    <ColumnDirective field='Country' headerText='Country' width='150' />
  </ColumnsDirective>
  <Inject services={[DetailRow]} />
</GridComponent>
```

> ⚠️ `queryString` must match the field name that exists in **both** parent and child data sources. Without it, no child rows will be displayed.

> ⚠️ `childGrid` and `detailTemplate` are mutually exclusive — hierarchical binding is not supported when `detailTemplate` is enabled.

### Different Field Names in Parent and Child

When parent and child use different key field names, use the child grid's `load` event:

```tsx
const childGridOptions = {
  columns: [/* ... */],
  dataSource: childdata,
  queryString: 'ID',  // field name in child
  load() {
    // Map parent's EmployeeID to child's ID field
    this.parentDetails.parentKeyFieldValue =
      this.parentDetails.parentRowData['EmployeeID'];
  }
};
```

### Aggregates in Child Grid

```tsx
const childGridOptions = {
  columns: [
    { field: 'OrderID', headerText: 'Order ID', textAlign: 'Right', width: 120 },
    { field: 'Freight', headerText: 'Freight', format: 'C2', width: 120, textAlign: 'Right' },
  ],
  dataSource: data,
  queryString: 'EmployeeID',
  aggregates: [
    {
      columns: [{ type: 'Sum', field: 'Freight', format: 'C2', footerTemplate: 'Sum: ${Sum}' }]
    },
    {
      columns: [{ type: 'Max', field: 'Freight', format: 'C2', footerTemplate: 'Max: ${Max}' }]
    }
  ]
};

// Inject Aggregate along with DetailRow
<Inject services={[DetailRow, Aggregate]} />
```

### Adding Records in Child Grid

To preserve the parent-child relationship when adding records, assign the `queryString` value via `actionBegin`:

```tsx
const childGridOptions = {
  actionBegin(args) {
    if (args.requestType === 'add') {
      // 'this' refers to child grid instance
      args.data['EmployeeID'] = this.parentDetails.parentKeyFieldValue;
    }
  },
  columns: [
    { field: 'OrderID', headerText: 'Order ID', isPrimaryKey: true, textAlign: 'Right', width: 120 },
    { field: 'EmployeeID', headerText: 'Employee ID', allowEditing: false, textAlign: 'Right', width: 120 },
    { field: 'ShipCity', headerText: 'Ship City', width: 150 },
  ],
  dataSource: data,
  editSettings: { allowEditing: true, allowAdding: true, allowDeleting: true },
  queryString: 'EmployeeID',
  toolbar: ['Add', 'Edit', 'Delete', 'Update', 'Cancel'],
};

<Inject services={[DetailRow, Edit, Toolbar]} />
```

### Accessing Parent Details in Child Grid

Use the child grid's `created` event to access parent row data:

```tsx
const childGridOptions = {
  created() {
    const parentRowData = this.parentDetails.parentRowData;
    console.log('Parent EmployeeID:', parentRowData.EmployeeID);
  },
  // ...
};
```

### Dynamic Data Binding via detailDataBound

For more control, bind child data dynamically using `detailDataBound`:

```tsx
import { DataManager, Query } from '@syncfusion/ej2-data';

const detailDataBound = (args) => {
  const empId = args.childGrid.parentDetails.parentRowData.EmployeeID;
  const matched = new DataManager(data).executeLocal(
    new Query().where('EmployeeID', 'equal', empId, true)
  );
  args.childGrid.dataSource = matched;
};

<GridComponent dataSource={employeeData} childGrid={childGridOptions} detailDataBound={detailDataBound}>
  {/* columns */}
  <Inject services={[DetailRow]} />
</GridComponent>
```

### Expand/Collapse All Programmatically

```tsx
const gridRef = useRef(null);

// Expand all child grids
gridRef.current.detailRowModule.expandAll();

// Collapse all child grids
gridRef.current.detailRowModule.collapseAll();

// Expand specific row by index (0-based)
gridRef.current.detailRowModule.expand(2);
```

> ⚠️ `expandAll()` and `collapseAll()` are not recommended for large datasets — they can be slow due to UI updates.

### Expand Child Grid Initially

```tsx
const gridRef = useRef(null);

const onDataBound = () => {
  gridRef.current.detailRowModule.expand(2); // expand 3rd row on load
};

<GridComponent ref={gridRef} dataSource={employeeData} childGrid={childGridOptions} dataBound={onDataBound}>
  {/* columns */}
  <Inject services={[DetailRow]} />
</GridComponent>
```

### Prevent Expand/Collapse via Events

```tsx
const detailExpand = (args) => {
  if (args.rowData.FirstName === 'Nancy') {
    args.cancel = true; // prevent expand
  }
};

const detailCollapse = (args) => {
  if (args.rowData.FirstName === 'Andrew') {
    args.cancel = true; // prevent collapse
  }
};

<GridComponent
  dataSource={employeeData}
  childGrid={childGridOptions}
  detailExpand={detailExpand}
  detailCollapse={detailCollapse}
>
  {/* columns */}
  <Inject services={[DetailRow]} />
</GridComponent>
```

## Master-Detail Structure

### Basic Hierarchy Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

const masterData = [
  { OrderID: 10248, CustomerID: 'VINET', ShipCity: 'Reims' },
  { OrderID: 10249, CustomerID: 'TOMSP', ShipCity: 'Münster' }
];

const detailData = {
  10248: [
    { ProductID: 1, ProductName: 'Chai', Quantity: 5 },
    { ProductID: 2, ProductName: 'Chang', Quantity: 15 }
  ],
  10249: [
    { ProductID: 3, ProductName: 'Aniseed Syrup', Quantity: 6 }
  ]
};

const detailTemplate = (props) => {
  const childData = detailData[props.OrderID] || [];

  return (
    <GridComponent dataSource={childData}>
      <ColumnsDirective>
        <ColumnDirective field='ProductID' headerText='Product ID' width='100' />
        <ColumnDirective field='ProductName' headerText='Product' width='120' />
        <ColumnDirective field='Quantity' headerText='Qty' width='80' />
      </ColumnsDirective>
    </GridComponent>
  );
};

<GridComponent dataSource={masterData} detailTemplate={detailTemplate}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='ShipCity' headerText='Ship City' width='120' />
  </ColumnsDirective>
  <Inject services={[DetailRow]} />
</GridComponent>
```

## Nested Grid

### Multi-Level Hierarchy

```tsx
const level1Template = (props) => {
  const level2Data = getLevel2Data(props.OrderID);

  const level2Template = (props2) => {
    const level3Data = getLevel3Data(props2.DetailID);
    return (
      <GridComponent dataSource={level3Data}>
        <ColumnsDirective>
          <ColumnDirective field='ItemID' headerText='Item' width='100' />
          <ColumnDirective field='ItemName' headerText='Name' width='150' />
          <ColumnDirective field='Amount' headerText='Amount' width='100' format='C2' />
        </ColumnsDirective>
      </GridComponent>
    );
  };

  return (
    <GridComponent dataSource={level2Data} detailTemplate={level2Template}>
      <ColumnsDirective>
        <ColumnDirective field='DetailID' headerText='Detail ID' width='100' />
        <ColumnDirective field='DetailName' headerText='Detail' width='150' />
      </ColumnsDirective>
      <Inject services={[DetailRow]} />
    </GridComponent>
  );
};

<GridComponent dataSource={masterData} detailTemplate={level1Template}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
  <Inject services={[DetailRow]} />
</GridComponent>
```

## Expand/Collapse

### Control Detail Expansion

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const expandAllDetails = () => {
    gridRef.current.detailRowModule.detailsExpand([0, 1, 2]);
  };

  const collapseAllDetails = () => {
    gridRef.current.detailRowModule.detailsCollapse([0, 1, 2]);
  };

  const expandRowDetail = (rowIndex) => {
    gridRef.current.detailRowModule.detailsExpand([rowIndex]);
  };

  return (
    <div>
      <button onClick={expandAllDetails}>Expand All</button>
      <button onClick={collapseAllDetails}>Collapse All</button>
      <button onClick={() => expandRowDetail(0)}>Expand Row 0</button>

      <GridComponent ref={gridRef} dataSource={masterData} detailTemplate={detailTemplate}>
        {/* columns */}
        <Inject services={[DetailRow]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Detail Expand/Collapse Events

```tsx
const detailDataBound = (args) => {
  console.log('Detail row data bound:', args.data);
};

const detailExpand = (args) => {
  console.log('Expanding row:', args.rowIndex);
};

const detailCollapse = (args) => {
  console.log('Collapsing row:', args.rowIndex);
};

<GridComponent
  dataSource={masterData}
  detailTemplate={detailTemplate}
  detailDataBound={detailDataBound}
  detailExpand={detailExpand}
  detailCollapse={detailCollapse}
>
  {/* columns */}
</GridComponent>
```

### Load Detail Data on Demand

```tsx
const detailTemplate = (props) => {
  const [childData, setChildData] = React.useState([]);

  React.useEffect(() => {
    // Load child data only when detail row expands
    const fetchChildData = async () => {
      const data = await fetchByOrderId(props.OrderID);
      setChildData(data);
    };

    fetchChildData();
  }, [props.OrderID]);

  return (
    <GridComponent dataSource={childData}>
      <ColumnsDirective>
        <ColumnDirective field='ProductID' headerText='Product ID' width='100' />
        <ColumnDirective field='ProductName' headerText='Product' width='120' />
      </ColumnsDirective>
    </GridComponent>
  );
};
```
