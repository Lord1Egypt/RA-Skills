---
name: column
description: 'Column Configuration in React TreeGrid - column definitions, tree column index, formatting, templates, foreign keys, and column headers.'
---

# Column

## Table of Contents
- [Overview](#overview)
- [Column Definitions](#column-definitions)
- [Tree Column Index](#tree-column-index)
- [Column Formatting](#column-formatting)
- [Column Templates](#column-templates)
- [Foreign Key Columns](#foreign-key-columns)
- [Column Headers](#column-headers)

## Overview

Columns define the schema for rendering TreeGrid data. Each column maps to a data source property and controls display format, editing behavior, and rendering.

**Key Concepts:**
- Column definitions via `ColumnDirective` component
- `field` property maps to data source property
- `treeColumnIndex` designates the column with expand/collapse icons
- `childMapping` defines parent-child relationships

## Column Definitions

Define columns using `ColumnDirective` component:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    {
      TaskID: 1,
      TaskName: 'Planning',
      StartDate: new Date(2018, 2, 3),
      EndDate: new Date(2018, 2, 7),
      Priority: 'High',
      Children: [
        { TaskID: 2, TaskName: 'Plan timeline', StartDate: new Date(2018, 2, 3), Priority: 'Normal' }
      ]
    }
  ];

  return (
    <TreeGridComponent dataSource={data} childMapping="Children" treeColumnIndex={1}>
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} type="number" />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="StartDate" headerText="Start Date" type="date" format="yMd" width={120} />
        <ColumnDirective field="EndDate" headerText="End Date" type="date" format="yMd" width={120} />
        <ColumnDirective field="Priority" headerText="Priority" width={100} />
      </ColumnsDirective>
    </TreeGridComponent>
  );
}
```

## Tree Column Index

The `treeColumnIndex` property designates which column displays expand/collapse icons:

```tsx
// Tree icons appear in TaskName column (index 1)
<TreeGridComponent dataSource={data} childMapping="Children" treeColumnIndex={1}>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} /> {/* Tree column here */}
    <ColumnDirective field="Priority" headerText="Priority" width={100} />
  </ColumnsDirective>
</TreeGridComponent>
```

**Default**: `treeColumnIndex={0}` (first column)

## Column Formatting

Format column values using `format` and `type` properties:

```tsx
<ColumnsDirective>
  {/* Number formatting */}
  <ColumnDirective field="Budget" headerText="Budget" type="number" format="N2" width={100} />
  
  {/* Currency formatting */}
  <ColumnDirective field="Price" headerText="Price" type="number" format="C2" width={100} />
  
  {/* Percentage formatting */}
  <ColumnDirective field="Progress" headerText="Progress" type="number" format="P0" width={100} />
  
  {/* Date formatting */}
  <ColumnDirective field="StartDate" headerText="Start Date" type="date" format="yMd" width={120} />
  <ColumnDirective field="EndDate" headerText="End Date" type="date" format="dd/MM/yyyy" width={120} />
</ColumnsDirective>
```

**Format Strings**:
- Number: `N` (N2, N3, etc.)
- Currency: `C` (C2, C3, etc.)
- Percentage: `P` (P0, P2, etc.)
- Date: `yMd`, `dd/MM/yyyy`, `MMM d, yyyy`

## Column Templates

Use templates for custom column rendering:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Status: 'In Progress', Progress: 45, Children: [] }
  ];

  const statusTemplate = (props) => {
    const statusColor = props.Status === 'Completed' ? 'green' : props.Status === 'In Progress' ? 'orange' : 'red';
    return (
      <div style={{ backgroundColor: statusColor, color: 'white', padding: '5px' }}>
        {props.Status}
      </div>
    );
  };

  const progressTemplate = (props) => {
    return (
      <div style={{ width: '100px', backgroundColor: '#f0f0f0', borderRadius: '3px' }}>
        <div style={{ width: props.Progress + '%', backgroundColor: 'blue', height: '20px', textAlign: 'center' }}>
          {props.Progress}%
        </div>
      </div>
    );
  };

  return (
    <TreeGridComponent dataSource={data} childMapping="Children" treeColumnIndex={1}>
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="Task ID" width={80} />
        <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
        <ColumnDirective field="Status" headerText="Status" width={100} template={statusTemplate} />
        <ColumnDirective field="Progress" headerText="Progress" width={150} template={progressTemplate} />
      </ColumnsDirective>
      <Inject services={[Page]} />
    </TreeGridComponent>
  );
}
```

## Foreign Key Columns

Map columns to related data using foreign key references:

```tsx
import * as React from 'react';
import { foreignKeyData } from './datasource';
import { dropData } from './datasource';
import { DataManager, Query } from '@syncfusion/ej2-data';
import { ColumnsDirective, ColumnDirective, TreeGridComponent, Inject } from '@syncfusion/ej2-react-treegrid';
import { Edit, Page, Toolbar } from '@syncfusion/ej2-react-treegrid';
/* tslint:disable */
function App() {
    let treegrid;
    const editSettings = { allowEditing: true, allowAdding: true, allowDeleting: true, mode: 'Cell' };
    const toolbarOptions = ['Add', 'Delete', 'Update', 'Cancel'];
    const queryCellInfo = (args) => {
        if (args.column.field === "EmployeeID") {
            for (var i = 0; i < dropData.length; i++) {
                let data = args.data;
                if (data[args.column.field] === dropData[i]["EmployeeID"]) {
                    args.cell.innerText = dropData[i]["EmployeeName"]; // assign the foreignkey field value to the innertext
                }
            }
        }
    };
    // Bind ForeignKey DataSource for dropdown using editParams
    const employeeParams = {
        params: {
            dataSource: new DataManager(dropData),
            fields: { text: "EmployeeName", value: "EmployeeID" },
            query: new Query()
        }
    };
    return (<TreeGridComponent dataSource={foreignKeyData} treeColumnIndex={0} childMapping='Children' height={280} toolbar={toolbarOptions} editSettings={editSettings} ref={g => treegrid = g} queryCellInfo={queryCellInfo}>
        <ColumnsDirective>
          <ColumnDirective field='EmpID' headerText='EmpID' isPrimaryKey={true} width='70'></ColumnDirective>
          <ColumnDirective field='Name' headerText='Employee Name' width='70' isPrimaryKey={true}></ColumnDirective>
          <ColumnDirective field='Contact' headerText='Contact' width='90' textAlign='Right'/>
          <ColumnDirective field='DOB' headerText='DOB' width='70' format='yMd' textAlign='Right' editType='datepickeredit'></ColumnDirective>
          <ColumnDirective field='EmployeeID' headerText='Employee ID' width='70' editType='dropdownedit' edit={employeeParams}></ColumnDirective>
          <ColumnDirective field='Country' headerText='Country' width='90' textAlign='Right'/>
        </ColumnsDirective>
        <Inject services={[Page, Edit, Toolbar]}/>
      </TreeGridComponent>);
}
;
export default App;
```

## Column Headers

Customize column headers with custom classes and orientation:

```tsx
<TreeGridComponent 
  dataSource={data} 
  childMapping="Children" 
  treeColumnIndex={1}
>
  <ColumnsDirective>
    <ColumnDirective field="TaskID" headerText="Task ID" width={80} headerTemplate={<span style={{ color: 'red' }}>Task ID</span>} />
    <ColumnDirective field="TaskName" headerText="Task Name" width={160} />
  </ColumnsDirective>
</TreeGridComponent>
```

## Key APIs

| Property | Type | Description |
|----------|------|-------------|
| `field` | string | Maps to data source property (required) |
| `headerText` | string | Column header display text |
| `type` | string | Data type: 'date', 'number', 'boolean', 'string' |
| `format` | string | Display format (N2, C2, yMd, etc.) |
| `width` | number/string | Column width in pixels or percentage |
| `allowSorting` | boolean | Enable/disable sorting (default: true) |
| `allowFiltering` | boolean | Enable/disable filtering (default: true) |
| `template` | JSX | Custom rendering for cells |
| `headerTemplate` | JSX | Custom rendering for header |
| `treeColumnIndex` | number | Column index for tree expand/collapse icons |
| `allowSearch` | boolean | Include in search (default: true) |

## Common Patterns

1. **Read-only Display**: Set `allowEditing={false}`
2. **Hidden Columns**: Set `visible={false}`
3. **Custom Alignment**: Use `textAlign="center"` or `textAlign="right"`
4. **Dynamic Width**: Use responsive width calculations
5. **Multi-level Headers**: Group columns with header template

