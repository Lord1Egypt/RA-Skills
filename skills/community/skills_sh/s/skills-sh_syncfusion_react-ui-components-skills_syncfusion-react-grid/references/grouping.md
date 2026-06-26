# Grouping in React Grid

## Table of Contents
- [Overview](#overview)
- [Enable Grouping](#enable-grouping)
- [Group Configuration](#group-configuration)
- [Initial Grouping](#initial-grouping)
- [Group Features](#group-features)
- [Lazy Load Grouping](#lazy-load-grouping)

## Overview

Grouping organizes data into hierarchical groups based on one or more columns, enabling better data analysis and presentation. Users can expand/collapse groups and view aggregated data per group.

## Enable Grouping

### Basic Grouping Setup

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Group } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data} allowGrouping={true}>
  <ColumnsDirective>
    <ColumnDirective field='ShipCountry' headerText='Ship Country' width='150' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='Freight' headerText='Freight' width='100' format='C2' />
  </ColumnsDirective>
  <Inject services={[Group]} />
</GridComponent>
```

### Enable Group Drop Area

Allow users to drag columns to group:

```tsx
const groupSettings = {
  showDropArea: true  // Show group drop area at top
};

<GridComponent
  dataSource={data}
  allowGrouping={true}
  groupSettings={groupSettings}
>
  {/* columns */}
  <Inject services={[Group]} />
</GridComponent>
```

## Group Configuration

### Configure Group Settings

```tsx
const groupSettings = {
  showDropArea: true,
  showGroupedColumn: true,  // Show grouped column
};

<GridComponent
  dataSource={data}
  groupSettings={groupSettings}
  allowGrouping={true}
>
  {/* columns */}
  <Inject services={[Group]} />
</GridComponent>
```

## Initial Grouping

Group by specific columns on grid load:

```tsx
const groupSettings = {
  columns: ['ShipCountry', 'CustomerID']  // Group by these columns
};

<GridComponent
  dataSource={data}
  groupSettings={groupSettings}
  allowGrouping={true}
>
  {/* columns */}
  <Inject services={[Group]} />
</GridComponent>
```

## Group Features

### Programmatic Grouping

```tsx
import React, { useRef } from 'react';

function App() {
  const gridRef = useRef(null);

  const groupByCountry = () => {
    gridRef.current.groupColumn('ShipCountry');
  };

  const removeGrouping = () => {
    gridRef.current.ungroupColumn('ShipCountry');
  };

  return (
    <div>
      <button onClick={groupByCountry}>Group by Country</button>
      <button onClick={removeGrouping}>Remove Grouping</button>

      <GridComponent ref={gridRef} dataSource={data} allowGrouping={true}>
        {/* columns */}
        <Inject services={[Group]} />
      </GridComponent>
    </div>
  );
}

export default App;
```

### Prevent Grouping for Specific Columns

```tsx
<ColumnDirective
  field='InternalID'
  headerText='ID'
  allowGrouping={false}  // Cannot drag to group
  width='100'
/>
```

### Custom Group Caption

```tsx
const captionTemplate = (props) => {
  return (
    <div>
      <strong>{props.key}</strong> - {props.count} records
    </div>
  );
};

const groupSettings = {
  captionTemplate: captionTemplate
};

<GridComponent groupSettings={groupSettings}>
  {/* columns */}
</GridComponent>
```

## Lazy Load Grouping

Load grouped data on demand for performance:

```tsx
import { Group, LazyLoadGroup } from '@syncfusion/ej2-react-grids';

const groupSettings = {
  columns: ['ShipCountry'],
  enableLazyLoading : true  // Load groups lazily
};

<GridComponent
  dataSource={remoteDataManager}
  groupSettings={groupSettings}
  allowGrouping={true}
>
  {/* columns */}
  <Inject services={[Group, LazyLoadGroup]} />
</GridComponent>
```

### Group with Aggregates

```tsx
import { AggregatesDirective, AggregateDirective, AggregateColumnsDirective, AggregateColumnDirective } from '@syncfusion/ej2-react-grids';

<GridComponent
  dataSource={data}
  allowGrouping={true}
  groupSettings={{ columns: ['ShipCountry'] }}
>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
  <AggregatesDirective>
    <AggregateDirective>
      <AggregateColumnsDirective>
        <AggregateColumnDirective
          field='Freight'
          type='Sum'
          groupFooterTemplate={`Group Total: \${Sum}`}
        />
      </AggregateColumnsDirective>
    </AggregateDirective>
  </AggregatesDirective>
  <Inject services={[Group, Aggregate]} />
</GridComponent>
```

### Get Current Grouping State

```tsx
const getGroupInfo = () => {
  return gridRef.current.groupSettings.columns;
  // Returns: ['ShipCountry', 'CustomerID']
};
```

### Handle Group Events

```tsx
const onActionComplete = (args) => {
  console.log('Grouping changed');
  console.log('Grouped columns:', args.data);
};

<GridComponent
  dataSource={data}
  allowGrouping={true}
  actionComplete={onActionComplete}
>
  {/* columns */}
  <Inject services={[Group]} />
</GridComponent>
```

### Group Expand/Collapse Events

```tsx
import { ChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, Group, GroupSettingsModel } from '@syncfusion/ej2-react-grids';
import * as React from 'react';
import { data } from './datasource';

function App() {
  let grid: GridComponent | null;
  const groupOptions: GroupSettingsModel = {
    columns: ['CustomerID', 'ShipCity'],
    showDropArea: false
  };
  const onSwitchChange = (args: ChangeEventArgs) => {
    if (args.checked) {
      (grid as GridComponent).groupCollapseAll();
    }
    else {
      (grid as GridComponent).groupExpandAll();
    }
  }
  return (
    <div>
      <div style={{display: "flex", margin: "10px"}}>
        <label style={{ marginRight: "5px" }}>Expand or collapse rows</label>
        <SwitchComponent change={onSwitchChange}></SwitchComponent>
      </div>
      <GridComponent ref={g => grid = g} dataSource={data} allowGrouping={true} groupSettings={groupOptions} height={315}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' headerText='Order ID' width='120' textAlign="Right" />
          <ColumnDirective field='CustomerID' headerText='Customer ID' width='150' />
          <ColumnDirective field='ShipCity' headerText='Ship City' width='150' />
          <ColumnDirective field='ShipName' headerText='Ship Name' width='150' />
        </ColumnsDirective>
        <Inject services={[Group]} />
      </GridComponent ></div>)
};
export default App;
```

### Lazy Load Details in Groups

```tsx
const detailTemplate = (props) => {
  const [details, setDetails] = useState(null);

  useEffect(() => {
    // Load details only when group is expanded
    fetch(`/api/orders/${props.key}`)
      .then(res => res.json())
      .then(data => setDetails(data));
  }, []);

  if (!details) return <p>Loading...</p>;

  return (
    <GridComponent dataSource={details}>
      {/* columns for details */}
    </GridComponent>
  );
};

<GridComponent
  dataSource={data}
  allowGrouping={true}
  groupSettings={{ columns: ['ShipCountry'] }}
  detailTemplate={detailTemplate}
>
  {/* columns */}
  <Inject services={[Group, DetailRow]} />
</GridComponent>
```
