# Validation in React Grid

## Quick Start

Validation ensures data quality before saving. Define `validationRules` on columns:

```tsx
<ColumnDirective field='OrderID' validationRules={{ required: true, number: true }} />
```

---

## Table of Contents
1. [Mandatory Rules](#mandatory-rules-for-grid-validation)
2. [Built-in Validators](#built-in-validators)
3. [Custom Validation](#custom-validation)
4. [Dynamic Rules](#dynamic-rules)
5. [Error Positioning](#error-positioning)
6. [CRUD Error Handling](#crud-error-handling)
7. [Duplicate Detection](#duplicate-detection)

---

## Mandatory Rules for Grid Validation

### Rule 1: Use `validationRules` Property (NOT edit.params)


```tsx
// ❌ WRONG - old approach
<ColumnDirective 
  field='OrderID' 
  edit={{ params: { required: true } }}
/>

// ✅ CORRECT - new approach
<ColumnDirective 
  field='OrderID' 
  validationRules={{ required: true }}
/>
```

### Rule 2: Custom Functions Use Array Syntax

```tsx
// ❌ WRONG
const rules = {
  custom: {
    validator: validateFn,
    message: 'Error'
  }
};

// ✅ CORRECT
const rules = {
  minLength: [validateFn, 'Error message']
};
```

### Rule 3: Access FormValidator via editModule

```tsx
// Access form object for dynamic rule management
const formObj = grid.editModule.formObj;
formObj.addRules('FieldName', { required: true });
formObj.removeRules('FieldName', ['required']);
formObj.validate();
```

### Rule 4: Manual Validation in Events

```tsx
// In actionBegin for save
const onActionBegin = (args) => {
  if (args.requestType === 'save') {
    // Trigger validation
    const isValid = grid.editModule.formObj.validate();
    if (!isValid) {
      args.cancel = true;  // Prevent save
    }
  }
};
```

---

## Built-in Validators

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-grids';

function App() {
  const editSettings = { allowEditing: true, allowAdding: true };
  const toolbarOptions = ['Add', 'Edit', 'Update', 'Cancel'];

  return (
    <GridComponent dataSource={data} editSettings={editSettings} toolbar={toolbarOptions}>
      <ColumnsDirective>
        <ColumnDirective 
          field='OrderID' 
          validationRules={{ required: true, number: true }}
          isPrimaryKey={true}
        />
        <ColumnDirective 
          field='CustomerID' 
          validationRules={{ required: true, minLength: 3 }}
        />
        <ColumnDirective 
          field='Freight' 
          validationRules={{ required: true, min: 1, max: 1000 }}
          editType='numericedit'
        />
        <ColumnDirective 
          field='OrderDate' 
          validationRules={{ required: true, min: new Date(2020,0,1), max: new Date() }}
          type='date' 
          format='yMd'
        />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </GridComponent>
  );
}
```

| Validator | Example | Purpose |
|-----------|---------|---------|
| `required` | `{ required: true }` | Field must have value |
| `number` | `{ number: true }` | Value must be numeric |
| `min` | `{ min: 1 }` | Minimum numeric/date value |
| `max` | `{ max: 1000 }` | Maximum numeric/date value |
| `minLength` | `{ minLength: 5 }` | Min string length |
| `maxLength` | `{ maxLength: 50 }` | Max string length |
| `pattern` | `{ pattern: /^[0-9]+$/ }` | Regex match |

---

## Custom Validation

Custom functions return `true` (valid) or `false` (invalid). Syntax: `{ ruleName: [customFn, 'message'] }`

```tsx
const validateFreight = (args) => args['value'] >= 1 && args['value'] <= 1000;
const validateEmail = (args) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(args['value']);
const validateMinLength = (args) => args['value'].length >= 5;

const rules = {
  freight: { 
    required: true,
    min: [validateFreight, 'Freight must be 1-1000']
  },
  email: {
    required: true,
    pattern: [validateEmail, 'Enter valid email']
  },
  customerID: {
    required: true,
    minLength: [validateMinLength, 'Must be 5+ characters']
  }
};

<ColumnDirective field='Freight' validationRules={rules.freight} />
```

**Dependent Validation** — Validate based on another column:

```tsx
let selectedRole = '';

const validateSalaryByRole = (args) => {
  const roles = {
    'Manager': { min: 50000, max: 100000 },
    'Engineer': { min: 25000, max: 60000 },
    'Sales': { min: 20000, max:45000 }
  };
  const range = roles[selectedRole];
  return range ? args.value >= range.min && args.value <= range.max : true;
};

const onRoleChange = (args) => {
  selectedRole = args.value;  // Store for dependent validation
};

<ColumnDirective 
  field='Role' 
  editType='dropdownedit'
  edit={{ params: { change: onRoleChange } }}
/>
<ColumnDirective 
  field='Salary'
  validationRules={{ 
    required: [validateSalaryByRole, 'Invalid salary for role'] 
  }}
/>
```

---

## Dynamic Rules

Add/remove validation rules at runtime:

```tsx
function App() {
  let grid;
  
  const onActionComplete = (args) => {
    const formObj = grid.editModule.formObj;
    
    if (args.requestType === 'beginEdit' || args.requestType === 'add') {
      // Add rule during edit
      formObj.addRules('CustomerID', { 
        required: true, 
        minLength: [5, 'Must be 5+ chars']
      });
    } else if (args.requestType === 'save') {
      // Validate before save
      if (!formObj.validate()) {
        args.cancel = true;  // Prevent save
      }
    }
  };

  return (
    <GridComponent ref={(g) => grid = g} dataSource={data} 
      editSettings={{ allowEditing: true, allowAdding: true }}
      actionComplete={onActionComplete} toolbar={['Add', 'Edit', 'Update', 'Cancel']}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' isPrimaryKey={true} />
        <ColumnDirective field='CustomerID' />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </GridComponent>
  );
}
```

**Key Methods:**
- `formObj.addRules(fieldName, rules)` - Add validation rules
- `formObj.removeRules(fieldName, ruleNames)` - Remove rules
- `formObj.validate()` - Trigger form validation

---

## Error Positioning

Customize error message placement using `customPlacement` event:

```tsx
const onActionComplete = (args) => {
  if (args.requestType === 'beginEdit' || args.requestType === 'add') {
    const formObj = grid.editModule.formObj;
    
    formObj.customPlacement = (input, error) => {
      // Position error to left of input
      const inputEl = document.querySelector(`#Grid${input.name}`);
      if (inputEl && error) {
        const rect = inputEl.getBoundingClientRect();
        error.style.left = (rect.left - 200) + 'px';
        error.style.top = rect.top + 'px';
        error.style.position = 'fixed';
      }
    };
  }
};

<GridComponent actionComplete={onActionComplete} dialogSettings={{ maxHeight: '500px' }}>
  {/* columns */}
</GridComponent>
```

---

## CRUD Error Handling

Handle failed validation or server errors with `actionFailure` event:

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

function App() {
  const data = new DataManager({
    url: 'url',
    insertUrl: 'url/insert',
    updateUrl: 'url/update',
    removeUrl: 'url/delete',
    adaptor: new UrlAdaptor()
  });

  const onActionFailure = (args) => {
    // Extract error from response
    if (args?.error?.[0]?.error?.json) {
      args.error[0].error.json().then((response) => {
        console.error('Validation Error:', response.message);
        // Display error toast/alert
      });
    }
  };

  return (
    <GridComponent dataSource={data} actionFailure={onActionFailure}
      editSettings={{ allowEditing: true, allowAdding: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' validationRules={{ required: true }} isPrimaryKey={true} />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </GridComponent>
  );
}
```

**Server Response Format:**
```csharp
[HttpPost("insert")]
public IActionResult Insert([FromBody] Order order)
{
  if (string.IsNullOrEmpty(order.OrderID)) {
    return BadRequest(new { message = "Order ID required" });
  }
  // Insert...
  return Ok(new { message = "Success" });
}
```

---

## Duplicate Detection

Validate for unique values:

```tsx
const validateUniqueOrderID = (args) => {
  return grid.dataSource.every(row =>
    row['OrderID'] + '' !== args['value'] || 
    row['OrderID'] === grid.editModule.editModule.args.rowData['OrderID']
  );
};

const orderIDRules = {
  required: true,
  min: [validateUniqueOrderID, 'OrderID already exists']
};

const onActionBegin = (args) => {
  if (args.requestType === 'save') {
    grid.editModule.formObj.addRules('OrderID', orderIDRules);
    if (!grid.editModule.formObj.validate()) {
      args.cancel = true;
    }
    grid.editModule.formObj.removeRules('OrderID');
  }
};

<GridComponent dataSource={data} actionBegin={onActionBegin} 
  editSettings={{ allowEditing: true, allowAdding: true }}
  toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}>
  <ColumnsDirective>
    <ColumnDirective field='OrderID' isPrimaryKey={true} />
  </ColumnsDirective>
  <Inject services={[Edit, Toolbar]} />
</GridComponent>
```

---

## Integration

Validation works with:
- **Editing modes**: Inline, Dialog, Batch
- **Events**: Use `actionBegin` to prevent save on validation failure
- **Filtering & Sorting**: Filters applied to validated data only
- **Export**: Exports only valid/current grid state

