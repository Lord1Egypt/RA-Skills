# Columns in React Grid

## Table of Contents
- [Column Definition](#column-definition)
- [Column Types](#column-types)
- [Column Width](#column-width)
- [Column Templates](#column-templates)
- [Column Customization](#column-customization)
- [Advanced Column Features](#advanced-column-features)

## Column Definition

Columns are defined using `ColumnDirective` components within `ColumnsDirective`. Each column maps to a field in your data source.

### Basic Column Setup

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
    <ColumnDirective field='OrderDate' headerText='Order Date' width='130' type='date' />
    <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
  </ColumnsDirective>
</GridComponent>
```

### Key Properties

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `field` | string | Maps to data source field (required) | `field='OrderID'` |
| `headerText` | string | Column header label | `headerText='Order ID'` |
| `width` | string \| number | Column width | `width='100'` or `width='20%'` |
| `type` | string | Data type for formatting | `type='date'` |
| `format` | string | Number/date format | `format='C2'` |
| `textAlign` | string | Text alignment | `textAlign='Right'` |
| `allowSorting` | boolean | Enable sorting | `allowSorting={true}` |
| `allowFiltering` | boolean | Enable filtering | `allowFiltering={true}` |
| `isPrimaryKey` | boolean | Mark as primary key | `isPrimaryKey={true}` |
| `visible` | boolean | Show/hide column | `visible={true}` |
| `allowGrouping` | boolean | Enable grouping | `allowGrouping={true}` |

## Column Types

### String Type

Text values (default):

```tsx
<ColumnDirective field='CustomerID' headerText='Customer' type='string' />
```

### Number Type

Numeric values:

```tsx
<ColumnDirective field='Freight' headerText='Freight' type='number' format='C2' />
```

### Date Type

Date values:

```tsx
<ColumnDirective field='OrderDate' headerText='Order Date' type='date' format='yMd' />
```

### DateTime Type

Date and time values:

```tsx
<ColumnDirective field='OrderDate' headerText='Order Date' type='datetime' format='MM/dd/yyyy hh:mm a' />
```

### Boolean Type

True/false values:

```tsx
<ColumnDirective field='Verified' headerText='Verified' type='boolean' displayAsCheckBox={true} />
```

### Checkbox Type

Selection checkboxes:

```tsx
<ColumnDirective type='checkbox' width='50' />
```

## Column Width

### Pixel Width

Fixed width in pixels:

```tsx
<ColumnDirective field='OrderID' headerText='Order ID' width='100' />
```

### Percentage Width

Responsive width as percentage:

```tsx
<ColumnDirective field='OrderID' headerText='Order ID' width='20%' />
<ColumnDirective field='CustomerID' headerText='Customer' width='30%' />
<ColumnDirective field='Freight' headerText='Freight' width='25%' />
<ColumnDirective field='ShipCity' headerText='Ship City' width='25%' />
```

### Auto Width

Automatically sized based on content:

```tsx
<ColumnDirective field='CustomerName' headerText='Customer' width='auto' />
```

### Column Resize

Allow users to resize columns:

```tsx
<GridComponent allowResizing={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' allowResizing={true} />
  </ColumnsDirective>
</GridComponent>
```

### Auto-Fit Columns

Automatically fit columns to content:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Resize } from '@syncfusion/ej2-react-grids';

<GridComponent allowResizing={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' autoFit={true} />
  </ColumnsDirective>
  <Inject services={[Resize]} />
</GridComponent>
```

## Column Templates

### Cell Template

Custom cell rendering:

```tsx
const cellTemplate = (props) => {
  return (
    <div>
      <strong>${props.Freight}</strong>
    </div>
  );
};

<ColumnDirective field='Freight' headerText='Freight' template={cellTemplate} width='150' />
```

### Header Template

Custom header rendering:

```tsx
const headerTemplate = () => {
  return <div><strong>Freight Amount</strong></div>;
};

<ColumnDirective field='Freight' headerText='Freight' headerTemplate={headerTemplate} width='150' />
```

### Edit Template

Custom editor for inline editing:

```tsx
const editTemplate = (props) => {
  return (
    <input
      type='number'
      value={props.Freight}
      onChange={(e) => props.Freight = parseFloat(e.target.value)}
    />
  );
};

<ColumnDirective
  field='Freight'
  headerText='Freight'
  template={cellTemplate}
  editTemplate={editTemplate}
  width='150'
/>
```

## Column Customization

### Column Reordering

Allow users to reorder columns:

```tsx
<GridComponent allowReordering={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' allowReordering={true} />
  </ColumnsDirective>
</GridComponent>
```

### Column Spanning

Merge cells across columns:

```tsx
const gridRef = useRef(null);

const queryCellInfo = (args) => {
  if (args.data.OrderID === 10248) {
    args.colSpan = 2; // Span 2 columns
  }
};

<GridComponent ref={gridRef} queryCellInfo={queryCellInfo}>
  {/* columns */}
</GridComponent>
```

### Frozen Columns

Keep columns visible while scrolling:

```tsx
<ColumnDirective field='OrderID' headerText='Order ID' width='100' isFrozen={true} />
<ColumnDirective field='CustomerID' headerText='Customer' width='120' />
```

### Hidden Columns

Hide columns from display:

```tsx
<ColumnDirective field='InternalNotes' headerText='Notes' visible={false} width='200' />
```

## Advanced Column Features

### Column Menu

Enable column operations menu with filtering, sorting, grouping:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Filter, Sort, Group, ColumnMenu } from '@syncfusion/ej2-react-grids';

<GridComponent showColumnMenu={true} allowFiltering={true} allowSorting={true} allowGrouping={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
  </ColumnsDirective>
  <Inject services={[Filter, Sort, Group, ColumnMenu]} />
</GridComponent>
```

**Column Menu Options:**
- Filter
- Sort Ascending/Descending
- Group by column
- AutoFit
- Column Chooser
- Custom menu items

### Foreign Key Column

Display related data from another source:

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, ForeignKey } from '@syncfusion/ej2-react-grids';

const employeeData = [
  { EmployeeID: 1, EmployeeName: 'Nancy Davolio' },
  { EmployeeID: 2, EmployeeName: 'Andrew Fuller' },
  { EmployeeID: 3, EmployeeName: 'Janet Leverling' }
];

function App() {
  return (
    <GridComponent dataSource={orders}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective
          field='EmployeeID'
          headerText='Employee'
          foreignKeyField='EmployeeID'
          foreignKeyValue='EmployeeName'
          dataSource={employeeData}
          width='150'
        />
        <ColumnDirective field='Freight' headerText='Freight' format='C2' />
      </ColumnsDirective>
      <Inject services={[ForeignKey]} />
    </GridComponent>
  );
}

export default App;
```

**Foreign Key Features:**
- Edit with dropdown selection
- Display lookup value instead of ID
- Works with filtering and sorting
- Supports hierarchical data

### Column Chooser

Allow users to show/hide columns dynamically:

```tsx
import { GridComponent, Inject, ColumnChooser, ColumnMenu } from '@syncfusion/ej2-react-grids';

<GridComponent toolbar={['ColumnChooser']} showColumnMenu={true}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' headerText='Order ID' width='100' showColumnChooser={true} />
    <ColumnDirective field='CustomerID' headerText='Customer' width='120' showColumnChooser={true} />
    <ColumnDirective field='OrderDate' headerText='Order Date' width='130' showColumnChooser={true} />
  </ColumnsDirective>
  <Inject services={[ColumnChooser, ColumnMenu]} />
</GridComponent>
```

### Multi-Column Header

Group columns under a single header:

```tsx
<GridComponent dataSource={data}>
  <ColumnsDirective>
    <ColumnDirective headerText='Order Details' columns={[
      { field: 'OrderID', headerText: 'Order ID', width: '100' },
      { field: 'OrderDate', headerText: 'Order Date', width: '130' }
    ]} />
    <ColumnDirective headerText='Shipping' columns={[
      { field: 'ShipCity', headerText: 'City', width: '120' },
      { field: 'ShipCountry', headerText: 'Country', width: '150' }
    ]} />
  </ColumnsDirective>
</GridComponent>
```

### Column Styling

Apply custom CSS classes and styling:

```tsx
<ColumnDirective
  field='Freight'
  headerText='Freight'
  customClass='high-value-cell'
  cssClass='freight-column'
  width='120'
/>

<style>{`
  .freight-column {
    background-color: #f0f0f0;
  }
  
  .high-value-cell {
    color: green;
    font-weight: bold;
  }
`}</style>
```

### Format Columns

Apply number and date formatting:

```tsx
// Currency format
<ColumnDirective field='Freight' format='C2' />

// Date format
<ColumnDirective field='OrderDate' format='yMd' />

// Percent format
<ColumnDirective field='Percentage' format='P2' />

// Custom number format
<ColumnDirective field='Quantity' format='N3' /> {/* 1,234.567 */}
```

### Column Validation

Validate column data during editing:

```tsx
<GridComponent editSettings={{ mode: 'Dialog', allowEditing: true }}>
  <ColumnsDirective>
    <ColumnDirective
      field='OrderID'
      headerText='Order ID'
      isprimarykey={true}
      validationRules={{ required: true }}
    />
    <ColumnDirective
      field='Freight'
      headerText='Freight'
      validationRules={{ min: 0, max: 10000, required: true }}
    />
    <ColumnDirective
      field='CustomerID'
      headerText='Customer'
      validationRules={{ required: true, minLength: 3, maxLength: 5 }}
    />
  </ColumnsDirective>
</GridComponent>
```

### Row Spanning

Span a cell across multiple rows:

```tsx
const gridRef = useRef(null);

const rowDataBound = (args) => {
  if (args.data.OrderID === 10248) {
    args.rowSpan = { OrderID: 2 }; // Span 2 rows
  }
};

<GridComponent ref={gridRef} rowDataBound={rowDataBound}>
  {/* columns */}
</GridComponent>
```

### Column Lock

Lock columns from interacting with other columns:

```tsx
<ColumnDirective field='OrderID' headerText='Order ID' allowGrouping={false} allowSorting={false} />
```

### Stack Column

Stack columns for responsive views:

```tsx
<GridComponent dataSource={stackedHeaderData}>
  <ColumnsDirective>
    <ColumnDirective
      field="CustomerID"
      headerText="Customer ID"
      width="160"
      textAlign="Right"
      isPrimaryKey={true}
    ></ColumnDirective>
    <ColumnDirective
      field="CustomerName"
      headerText="Name"
      width="150"
      minWidth="120"
    ></ColumnDirective>
    <ColumnDirective
      columns={[
        {
          field: 'OrderID',
          headerText: 'ID',
          textAlign: 'Right',
          width: 110,
        },
        {
          field: 'OrderDate',
          headerText: 'Date',
          textAlign: 'Right',
          width: 110,
        },
      ]}
      headerText="Order Details"
      textAlign="Center"
    />
  </ColumnsDirective>
</GridComponent>
```
