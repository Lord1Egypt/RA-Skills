---
name: validation-patterns
description: 'Validation Patterns in React TreeGrid - custom validation rules, cross-field validation, async validation, server-side validation, and error messaging.'
---

# Validation Patterns

## Table of Contents
- [Basic Column Validation](#basic-column-validation)
- [Custom Validation Rules](#custom-validation-rules)
- [Cross-field Validation](#cross-field-validation)
- [Async Validation](#async-validation)
- [Server-side Validation](#server-side-validation)
- [Validation in Dialog Edit](#validation-in-dialog-edit)
- [Conditional Validation](#conditional-validation)
- [Error Message Display](#error-message-display)
- [Best Practices](#best-practices)
- [Key APIs](#key-apis)
- [Common Patterns](#common-patterns)

Complete guide to data validation in TreeGrid.

## Basic Column Validation

Add validation rules to columns:

```tsx
import React from 'react';
import { TreeGridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-treegrid';

export default function App() {
  const data = [
    { TaskID: 1, TaskName: 'Planning', Budget: 10000, Priority: 'High', Children: [] }
  ];

  return (
    <TreeGridComponent
      dataSource={data}
      childMapping="Children"
      editSettings={{ mode: 'Dialog', allowEditing: true }}
      toolbar={['Edit', 'Update', 'Cancel']}
    >
      <ColumnsDirective>
        <ColumnDirective 
          field="TaskID" 
          headerText="Task ID" 
          width={80}
          validationRules={{ required: true, min: 1 }}
        />
        <ColumnDirective 
          field="TaskName" 
          headerText="Task Name" 
          width={160}
          validationRules={{ required: true, minLength: 3, maxLength: 100 }}
        />
        <ColumnDirective 
          field="Budget" 
          headerText="Budget" 
          width={120}
          validationRules={{ required: true, min: 0, max: 1000000 }}
        />
        <ColumnDirective 
          field="Priority" 
          headerText="Priority" 
          width={100}
          validationRules={{ required: true }}
        />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </TreeGridComponent>
  );
}
```

### Validation Rule Types

```tsx
// Common validation rules:
validationRules={{
  required: true,         // Field is required
  min: 0,                // Minimum value
  max: 100,              // Maximum value
  minLength: 3,          // Minimum length
  maxLength: 50,         // Maximum length
  pattern: /^[A-Z]/,     // Regex pattern
  email: true,           // Email format
  date: true,            // Date format
  url: true              // URL format
}}
```

## Custom Validation Rules

Implement custom validation logic:

```tsx
const customValidator = (args) => {
  const value = args.value;
  
  if (!value) {
    args.isValid = false;
    args.errorMessage = 'This field is required';
    return;
  }
  
  if (value.length < 3) {
    args.isValid = false;
    args.errorMessage = 'Minimum 3 characters required';
    return;
  }
  
  // Custom logic
  if (value.includes('XXX')) {
    args.isValid = false;
    args.errorMessage = 'Invalid characters used';
    return;
  }
  
  args.isValid = true;
};

<ColumnDirective 
  field="TaskName" 
  headerText="Task Name" 
  validationRules={{ required: true, custom: customValidator }}
/>
```

## Cross-field Validation

Validate based on multiple fields:

```tsx
const validateDateRange = (args, rowData) => {
  const startDate = rowData.StartDate;
  const endDate = args.value;  // Current field being edited
  
  if (endDate && startDate && endDate < startDate) {
    args.isValid = false;
    args.errorMessage = 'End date must be after start date';
    return;
  }
  
  args.isValid = true;
};

<ColumnDirective 
  field="EndDate" 
  headerText="End Date" 
  validationRules={{
    required: true,
    custom: (args) => validateDateRange(args, currentRowData)
  }}
/>
```

## Async Validation

Validate with server call:

```tsx
const validateTaskNameAsync = async (args) => {
  const taskName = args.value;
  
  try {
    const response = await fetch(`/api/tasks/check-name`, {
      method: 'POST',
      body: JSON.stringify({ taskName })
    });
    
    const result = await response.json();
    
    if (result.exists) {
      args.isValid = false;
      args.errorMessage = 'Task name already exists';
    } else {
      args.isValid = true;
    }
  } catch (error) {
    console.error('Validation error:', error);
    args.isValid = false;
    args.errorMessage = 'Could not validate';
  }
};

<ColumnDirective 
  field="TaskName" 
  headerText="Task Name" 
  validationRules={{
    required: true,
    custom: validateTaskNameAsync
  }}
/>
```

## Server-side Validation

Validate on server after save:

```tsx
<TreeGridComponent
  dataSource={dataManager}
  childMapping="Children"
  editSettings={{ mode: 'Dialog' }}
  actionComplete={(args) => {
    if (args.requestType === 'save') {
      // Server validated and returned errors
      if (args.response && args.response.errors) {
        console.error('Server validation errors:', args.response.errors);
        
        // Show error messages
        args.response.errors.forEach(error => {
          alert(`${error.field}: ${error.message}`);
        });
      }
    }
  }}
  actionFailure={(args) => {
    // Handle validation failure
    console.error('Validation failed:', args.error);
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Validation in Dialog Edit

Handle validation in edit dialog:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  editSettings={{ mode: 'Dialog' }}
  dialogTemplate={(props) => {
    const [errors, setErrors] = React.useState({});
    
    const validateForm = () => {
      const newErrors = {};
      
      if (!props.TaskName) {
        newErrors.TaskName = 'Task name is required';
      }
      if (!props.Budget || props.Budget < 0) {
        newErrors.Budget = 'Budget must be positive';
      }
      
      setErrors(newErrors);
      return Object.keys(newErrors).length === 0;
    };
    
    const handleSave = () => {
      if (validateForm()) {
        // Save to server
      }
    };
    
    return (
      <div>
        <div>
          <label>Task Name</label>
          <input defaultValue={props.TaskName} />
          {errors.TaskName && <span style={{color: 'red'}}>{errors.TaskName}</span>}
        </div>
        <div>
          <label>Budget</label>
          <input type="number" defaultValue={props.Budget} />
          {errors.Budget && <span style={{color: 'red'}}>{errors.Budget}</span>}
        </div>
        <button onClick={handleSave}>Save</button>
      </div>
    );
  }}
>
  {/* columns */}
</TreeGridComponent>
```

## Conditional Validation

Validate based on row conditions:

```tsx
const validateBudget = (args, rowData) => {
  // Budget is required only for approved tasks
  if (rowData.Status === 'Approved' && !args.value) {
    args.isValid = false;
    args.errorMessage = 'Budget required for approved tasks';
    return;
  }
  
  // Budget must be >= 1000 for high priority
  if (rowData.Priority === 'High' && args.value < 1000) {
    args.isValid = false;
    args.errorMessage = 'High priority tasks require budget >= 1000';
    return;
  }
  
  args.isValid = true;
};

<ColumnDirective 
  field="Budget" 
  headerText="Budget" 
  validationRules={{
    custom: (args) => validateBudget(args, currentRowData)
  }}
/>
```

## Error Message Display

Customize error message display:

```tsx
<TreeGridComponent
  dataSource={data}
  childMapping="Children"
  validationSettings={{
    showErrorMessage: true,  // Show validation errors
    errorPosition: 'TopLeft' // 'TopLeft', 'BottomRight'
  }}
  cellSave={(args) => {
    if (!args.isValid) {
      console.log('Validation failed for:', args.column.field);
      console.log('Error:', args.errorMessage);
    }
  }}
>
  {/* columns with validation rules */}
</TreeGridComponent>
```

## Best Practices

```tsx
// Good validation strategy:
1. Client-side: Quick feedback (required, format, length)
2. Server-side: Business logic (uniqueness, constraints)
3. Async: Check availability (user exists, code is unique)
4. Clear Messages: Specific error messages for users
5. Visual Feedback: Highlight invalid fields
6. User Recovery: Allow correction without data loss
```

## Key APIs

| Property/Method | Type | Description |
|---|---|---|
| `validationRules` | object | Validation configuration |
| `required` | boolean | Field is mandatory |
| `min/max` | number | Min/max value |
| `minLength/maxLength` | number | String length |
| `pattern` | regex | Regex validation |
| `custom` | function | Custom validator |
| `cellSave` | event | On cell validation |
| `actionFailure` | event | On validation error |

## Common Patterns

1. **Progressive Validation**: Validate as user types
2. **Field Dependencies**: Validate based on other fields
3. **Tiered Validation**: Client-side then server-side
4. **Error Recovery**: Provide helpful error messages
5. **User Guidance**: Show validation hints before error

