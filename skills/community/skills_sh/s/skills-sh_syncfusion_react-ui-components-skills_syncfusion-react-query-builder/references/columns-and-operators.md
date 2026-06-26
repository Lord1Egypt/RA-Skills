# Columns and Operators

Configure column definitions that control how fields appear and behave in the Query Builder, including available operators, validation, and formatting.

## Table of Contents
- [Column Schema Overview](#column-schema-overview)
- [Auto-Generation](#auto-generation)
- [Supported Operators](#supported-operators)
- [Labels and Field Mapping](#labels-and-field-mapping)
- [Data Types and Formatting](#data-types-and-formatting)
- [Validation](#validation)
- [Custom Operators](#custom-operators)
- [Step and Format](#step-and-format)

## Column Schema Overview

Column definitions define the schema for the Query Builder and control how fields appear and behave. The `field` property is essential for binding data source values to query builder columns.

```tsx
interface ColumnsModel {
  field: string;           // Required: data field name
  label: string;           // Display label in UI
  type: string;            // Data type: 'string' | 'number' | 'date' | 'boolean'
  operators?: any[];       // Available operators for this column
  values?: any[];          // Predefined values (for boolean/enum)
  format?: string;         // Date/number format string
  step?: number;           // Step increment for number fields
  validation?: any;        // Validation rules for the field
}
```

### Basic Column Definition

```tsx
const columns: ColumnsModel[] = [
  { 
    field: 'EmployeeID', 
    label: 'Employee ID', 
    type: 'number' 
  },
  { 
    field: 'FirstName', 
    label: 'First Name', 
    type: 'string' 
  },
  { 
    field: 'Country', 
    label: 'Country', 
    type: 'string' 
  }
];
```

## Auto-Generation

When the `columns` property is empty or undefined during initialization, the Query Builder automatically generates columns from all fields in the `dataSource`.

```tsx
import { employeeData } from './datasource';

function App() {
  return (
    <QueryBuilderComponent 
      width="100%" 
      dataSource={employeeData}
      // columns property omitted - will auto-generate from dataSource
    />
  );
}
```

**How Auto-Generation Works:**
- The component inspects the first record in the data source
- Detects the data type of each field
- Creates ColumnsModel entries automatically
- Assigns the field name as both field and label

> **Note:** The column type is inferred from the first record's data type. If the first record is missing a field, that field won't be included in auto-generated columns.

## Supported Operators

Define available operators for each column using the `operators` property. The following operators are supported based on data type:

### Operator Type Compatibility

| Operator | Description | String | Number | Date | Boolean |
|----------|-------------|--------|--------|------|---------|
| `startswith` | Value begins with string | ✓ | - | - | - |
| `endswith` | Value ends with string | ✓ | - | - | - |
| `contains` | Value contains string | ✓ | - | - | - |
| `equal` | Value equals | ✓ | ✓ | ✓ | ✓ |
| `notequal` | Value does not equal | ✓ | ✓ | ✓ | ✓ |
| `greaterthan` | Value is greater than | - | ✓ | ✓ | - |
| `greaterthanorequal` | Value is >= | - | ✓ | ✓ | - |
| `lessthan` | Value is less than | - | ✓ | ✓ | - |
| `lessthanorequal` | Value is <= | - | ✓ | ✓ | - |
| `between` | Value is between two values | - | ✓ | ✓ | - |
| `notbetween` | Value is not between two values | - | ✓ | ✓ | - |
| `in` | Value is in list | ✓ | ✓ | - | - |
| `notin` | Value is not in list | ✓ | ✓ | - | - |
| `isnull` | Value is null | ✓ | ✓ | ✓ | ✓ |
| `isnotnull` | Value is not null | ✓ | ✓ | ✓ | ✓ |

### Restricting Operators per Column

```tsx
const columns: ColumnsModel[] = [
  {
    field: 'EmployeeID',
    label: 'Employee ID',
    type: 'number',
    operators: [
      { key: 'Equal', value: 'equal' },
      { key: 'Greater than', value: 'greaterthan' },
      { key: 'Less than', value: 'lessthan' }
    ]
  },
  {
    field: 'FirstName',
    label: 'First Name',
    type: 'string',
    operators: [
      { key: 'Contains', value: 'contains' },
      { key: 'Starts with', value: 'startswith' },
      { key: 'Ends with', value: 'endswith' }
    ]
  }
];
```

## Labels and Field Mapping

The `field` property maps to your data source, while `label` is the display text shown to users.

```tsx
const columns: ColumnsModel[] = [
  {
    field: 'EmpID',          // Maps to data source field
    label: 'Employee ID'     // User-friendly display label
  },
  {
    field: 'EmpName',
    label: 'Employee Name'
  },
  {
    field: 'DeptCode',
    label: 'Department'
  }
];
```

> **Important:** If the column field is not in the data source, the column values will remain empty.

## Data Types and Formatting

### String Type

```tsx
{
  field: 'FirstName',
  label: 'First Name',
  type: 'string'
  // No additional formatting needed
}
```

### Number Type

```tsx
{
  field: 'Salary',
  label: 'Annual Salary',
  type: 'number',
  format: 'C2'  // Currency format with 2 decimal places
}
```

Supported number formats:
- `N2` - Number with 2 decimal places
- `C2` - Currency with 2 decimal places
- `P0` - Percentage with 0 decimal places

### Date Type

```tsx
{
  field: 'HireDate',
  label: 'Hire Date',
  type: 'date',
  format: 'dd/MM/yyyy'  // Date format string
}
```

Supported date formats:
- `dd/MM/yyyy` - Day/Month/Year
- `MM/dd/yyyy` - Month/Day/Year
- `yyyy-MM-dd` - ISO format
- `dd MMM yyyy` - Day Month Year

### Boolean Type

```tsx
{
  field: 'IsActive',
  label: 'Active Status',
  type: 'boolean',
  values: ['Active', 'Inactive']  // Display values
}
```

## Validation

Enable validation to ensure users enter valid data. Use the `allowValidation` property on the Query Builder and set validation rules per column.

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  const columns: ColumnsModel[] = [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      type: 'number',
      validation: { isRequired: true }  // Field is required
    },
    {
      field: 'FirstName',
      label: 'First Name',
      type: 'string',
      validation: { isRequired: true }
    }
  ];

  function validateRules(): void {
    const isValid = qryBldrObj.validateFields();
    if (isValid) {
      console.log('Rules are valid');
    } else {
      console.log('Please fix validation errors');
    }
  }

  return (
    <div>
      <QueryBuilderComponent
        width="100%"
        columns={columns}
        allowValidation={true}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={validateRules}>Validate</button>
    </div>
  );
}
```

### Validation Properties

```tsx
validation: {
  isRequired: true              // Field must have a value
  min?: number;                 // Minimum value/length
  max?: number;                 // Maximum value/length
  pattern?: string;             // Regex pattern
  customError?: string;         // Custom error message
}
```

> **Note:** Validation for Field values is automatic. You must manually configure validation for Operator and Value fields through the `validation` property.

## Custom Operators

Add custom operators specific to your domain or use case:

```tsx
const columns: ColumnsModel[] = [
  {
    field: 'Status',
    label: 'Status',
    type: 'string',
    operators: [
      { key: 'Equal', value: 'equal' },
      { key: 'Not Equal', value: 'notequal' },
      { key: 'Is Active', value: 'isactive' },       // Custom
      { key: 'Is Inactive', value: 'isinactive' }    // Custom
    ]
  }
];
```

Then handle custom operators in the `actionBegin` event:

```tsx
function onActionBegin(args: ActionEventArgs): void {
  if (args.requestType === 'rule-change') {
    if (args.rule?.operator === 'isactive') {
      args.rule.value = 'Active';
    }
  }
}
```

## Step and Format

### Step Property (Number Fields)

Set step increments for numeric input fields:

```tsx
const columns: ColumnsModel[] = [
  {
    field: 'Quantity',
    label: 'Quantity',
    type: 'number',
    step: 10  // Increment/decrement by 10
  },
  {
    field: 'Price',
    label: 'Price',
    type: 'number',
    step: 0.01  // Increment/decrement by 0.01
  }
];
```

The step value controls:
- How much the value changes when using spinner buttons
- The keyboard arrow key increment amount
- The mouse wheel scroll increment

### Format Property

Format controls how values are displayed and entered:

**Date Formatting:**
```tsx
{
  field: 'OrderDate',
  label: 'Order Date',
  type: 'date',
  format: 'dd/MM/yyyy'
}
```

**Number Formatting:**
```tsx
{
  field: 'Revenue',
  label: 'Revenue',
  type: 'number',
  format: 'C2'  // $1,000.00
}
```

## Complete Example

```tsx
import { ColumnsModel, QueryBuilderComponent } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  const columns: ColumnsModel[] = [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      type: 'number',
      operators: [
        { key: 'Equal', value: 'equal' },
        { key: 'Greater than', value: 'greaterthan' },
        { key: 'Less than', value: 'lessthan' }
      ],
      validation: { isRequired: true }
    },
    {
      field: 'FirstName',
      label: 'First Name',
      type: 'string',
      validation: { isRequired: true }
    },
    {
      field: 'HireDate',
      label: 'Hire Date',
      type: 'date',
      format: 'dd/MM/yyyy'
    },
    {
      field: 'Salary',
      label: 'Salary',
      type: 'number',
      step: 1000,
      format: 'C2'
    },
    {
      field: 'IsActive',
      label: 'Active',
      type: 'boolean',
      values: ['Yes', 'No']
    }
  ];

  return (
    <QueryBuilderComponent
      width="100%"
      columns={columns}
      allowValidation={true}
    />
  );
}

export default App;
```

This example shows:
- Number field with restricted operators
- String field with required validation
- Date field with formatting
- Number field with currency formatting and step increment
- Boolean field with custom display values
