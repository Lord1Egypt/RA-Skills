# Advanced Features

Master advanced Query Builder features including display modes, state persistence, locking, cloning, RTL support, and accessibility.

## Table of Contents
- [Display Modes](#display-modes)
- [State Persistence](#state-persistence)
- [Locking Rules and Groups](#locking-rules-and-groups)
- [Clone Operations](#clone-operations)
- [Separate Connectors](#separate-connectors)
- [RTL Support](#rtl-support)
- [Sort Direction](#sort-direction)
- [Summary View](#summary-view)
- [Restrict Operations](#restrict-operations)
- [Accessibility Features](#accessibility-features)

## Display Modes

The Query Builder supports two layout orientations to accommodate different UI preferences.

### Horizontal Display (Default)

```tsx
<QueryBuilderComponent
  displayMode="Horizontal"
  columns={columns}
/>
```

Layout:
```
[Field] [Operator] [Value] [Add Rule] [Add Group] [Delete]
```

### Vertical Display

```tsx
<QueryBuilderComponent
  displayMode="Vertical"
  columns={columns}
/>
```

Layout:
```
Field:      [Dropdown]
Operator:   [Dropdown]
Value:      [Input]
            [Add Rule] [Add Group] [Delete]
```

### Complete Display Mode Example

```tsx
import { DisplayMode } from '@syncfusion/ej2-react-querybuilder';
import React, { useState } from 'react';

function App() {
  const [displayMode, setDisplayMode] = useState<DisplayMode>('Horizontal');

  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' }
  ];

  return (
    <div>
      <div>
        <button onClick={() => setDisplayMode('Horizontal')}>
          Horizontal Layout
        </button>
        <button onClick={() => setDisplayMode('Vertical')}>
          Vertical Layout
        </button>
      </div>
      <QueryBuilderComponent
        displayMode={displayMode}
        columns={columns}
      />
    </div>
  );
}

export default App;
```

## State Persistence

Automatically save and restore the Query Builder's filter state using browser local storage.

### Enable Persistence

```tsx
<QueryBuilderComponent
  columns={columns}
  enablePersistence={true}
/>
```

When enabled:
- Filter rules are saved to `localStorage`
- State is restored on page reload
- Perfect for multi-step workflows

### Persistence Example

```tsx
function App() {
  const columns: ColumnsModel[] = [
    { field: 'TaskID', label: 'Task ID', type: 'number' },
    { field: 'Name', label: 'Name', type: 'string' },
    { field: 'Category', label: 'Category', type: 'string' }
  ];

  const initialRules: RuleModel = {
    condition: 'or',
    rules: [{
      field: 'Category',
      label: 'Category',
      operator: 'equal',
      type: 'string',
      value: 'Active'
    }]
  };

  return (
    <QueryBuilderComponent
      width="100%"
      enablePersistence={true}
      columns={columns}
      rule={initialRules}
    />
  );
}
```

### Manual State Management

Save and load rules manually:

```tsx
let qryBldrObj: QueryBuilderComponent;

function saveRules(): void {
  const rules = qryBldrObj.getRules();
  localStorage.setItem('queryBuilderRules', JSON.stringify(rules));
}

function loadRules(): void {
  const savedRules = localStorage.getItem('queryBuilderRules');
  if (savedRules) {
    qryBldrObj.setRules(JSON.parse(savedRules));
  }
}

return (
  <div>
    <QueryBuilderComponent
      ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      columns={columns}
    />
    <button onClick={saveRules}>Save Filters</button>
    <button onClick={loadRules}>Load Filters</button>
  </div>
);
```

## Locking Rules and Groups

Make rules and groups read-only to prevent user modifications.

### Lock Individual Rules

```tsx
let qryBldrObj: QueryBuilderComponent;

function lockRule(ruleId: string): void {
  qryBldrObj.lockRule(ruleId);
  // User cannot edit or delete this rule
}

function unlockRule(ruleId: string): void {
  // Unlock by deleting and re-adding
  qryBldrObj.deleteRules([ruleId]);
}
```

### Lock Groups

```tsx
function lockGroup(groupId: string): void {
  qryBldrObj.lockGroup(groupId);
  // User cannot edit or delete this group or its contents
}
```

### Locking Example

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  const initialRule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      },
      {
        field: 'Status',
        label: 'Status',
        operator: 'equal',
        type: 'string',
        value: 'Active'
      }
    ]
  };

  React.useEffect(() => {
    // Lock first rule (Country filter)
    if (qryBldrObj) {
      const rules = qryBldrObj.getRules();
      if (rules.rules && rules.rules.length > 0) {
        const firstRuleId = rules.rules[0].field;
        setTimeout(() => qryBldrObj.lockRule(firstRuleId), 100);
      }
    }
  }, [qryBldrObj]);

  return (
    <QueryBuilderComponent
      columns={columns}
      rule={initialRule}
      ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
    />
  );
}
```

## Clone Operations

Duplicate rules and groups to quickly build complex filters.

### Clone Rule

Create a copy of a rule and add it to a group:

```tsx
function cloneRule(ruleId: string): void {
  qryBldrObj.cloneRule(ruleId, 'group0', 0);
}

// Parameters:
// ruleID - ID of the rule to clone
// groupID - Target group for the cloned rule
// index - Position in the group (optional)
```

### Clone Group

Duplicate an entire group:

```tsx
function cloneGroup(groupId: string): void {
  qryBldrObj.cloneGroup(groupId, 'group0', 0);
}

// Parameters:
// groupID - ID of the group to clone
// parentGroupID - Target parent group
// index - Position in parent (optional)
```

### Clone Example

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  const initialRule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Department',
        label: 'Department',
        operator: 'equal',
        type: 'string',
        value: 'Sales'
      }
    ]
  };

  function duplicateLastRule(): void {
    const rules = qryBldrObj.getRules();
    if (rules.rules && rules.rules.length > 0) {
      const lastRule = rules.rules[rules.rules.length - 1];
      qryBldrObj.cloneRule(lastRule.field as string, 'group0');
    }
  }

  return (
    <div>
      <QueryBuilderComponent
        columns={columns}
        rule={initialRule}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <button onClick={duplicateLastRule}>Clone Last Rule</button>
    </div>
  );
}
```

## Separate Connectors

Display separate connectors (AND/OR) between rules for better visual distinction.

### Enable Separate Connectors

```tsx
<QueryBuilderComponent
  columns={columns}
  enableSeparateConnector={true}
/>
```

**Without:**
```
[Rule 1] AND [Rule 2] AND [Rule 3]
```

**With:**
```
[Rule 1]
    AND
[Rule 2]
    AND
[Rule 3]
```

### Example with Separate Connectors

```tsx
<QueryBuilderComponent
  width="100%"
  columns={columns}
  enableSeparateConnector={true}
  displayMode="Vertical"
/>
```

## RTL Support

Enable right-to-left (RTL) layout for languages like Arabic, Farsi, and Urdu.

### Enable RTL

```tsx
<QueryBuilderComponent
  enableRtl={true}
  columns={columns}
/>
```

### RTL with Localization

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'ar-AE': {
    'querybuilder': {
      'AddCondition': 'اضافة الشرط',
      'AddGroup': 'إضافة مجموعة',
      'DeleteRule': 'حذف القاعدة',
      'DeleteGroup': 'حذف المجموعة',
      'SelectField': 'اختر حقل',
      'SelectOperator': 'اختر مشغل',
      'Equal': 'يساوي',
      'NotEqual': 'لا يساوي',
      'Contains': 'يحتوي على',
      'Between': 'بين',
      'In': 'في'
    }
  }
});

function App() {
  return (
    <QueryBuilderComponent
      locale="ar-AE"
      enableRtl={true}
      columns={columns}
    />
  );
}
```

## Sort Direction

Control the sort order of column names in the field dropdown.

### Sort Options

```tsx
type SortDirection = 'Default' | 'Ascending' | 'Descending';
```

### Example

```tsx
<QueryBuilderComponent
  columns={columns}
  sortDirection="Ascending"
/>
```

**Default:** Shows fields in definition order
**Ascending:** Alphabetical A-Z
**Descending:** Alphabetical Z-A

## Summary View

Display a text summary of the filter query below the Query Builder.

### Enable Summary View

```tsx
<QueryBuilderComponent
  columns={columns}
  summaryView={true}
/>
```

**Output Example:**
```
(EmployeeID = 1001) AND (Title LIKE '%Manager%')
```

### Summary View Example

```tsx
function App() {
  const initialRule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      },
      {
        field: 'Salary',
        label: 'Salary',
        operator: 'greaterthan',
        type: 'number',
        value: 50000
      }
    ]
  };

  return (
    <QueryBuilderComponent
      width="100%"
      columns={columns}
      rule={initialRule}
      summaryView={true}
    />
  );
}
```

## Restrict Operations

Control which operations are available to users.

### Disable Drag and Drop

```tsx
<QueryBuilderComponent
  allowDragAndDrop={false}
  columns={columns}
/>
```

### Disable Button Controls

```tsx
const buttonOptions: ShowButtonsModel = {
  ruleDelete: false,      // Hide delete rule button
  groupInsert: false,     // Hide add group button
  groupDelete: false      // Hide delete group button
};

<QueryBuilderComponent
  showButtons={buttonOptions}
  columns={columns}
/>
```

### Read-Only Mode

```tsx
<QueryBuilderComponent
  readonly={true}
  columns={columns}
/>
```

In readonly mode:
- Users cannot add, edit, or delete rules
- They can view the existing query
- Perfect for displaying saved filters

### Max Group Depth

Limit nested group depth:

```tsx
<QueryBuilderComponent
  maxGroupCount={3}  // Maximum 3 levels of nesting
  columns={columns}
/>
```

## Accessibility Features

The Query Builder is fully accessible and compliant with WCAG standards.

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Move focus to next/previous element |
| `Enter` | Select/activate focused button |
| `Space` | Toggle checkbox or activate button |
| `Arrow Keys` | Navigate dropdown options |

### Screen Reader Support

```tsx
<QueryBuilderComponent
  columns={columns}
  // Automatically includes ARIA attributes
/>
```

### Accessibility Example

```tsx
function App() {
  return (
    <div>
      <label htmlFor="qb-filter">Filter Employees</label>
      <QueryBuilderComponent
        id="qb-filter"
        columns={columns}
        // ARIA labels are automatically added
      />
    </div>
  );
}
```

## Complete Advanced Features Example

```tsx
import { ColumnsModel, QueryBuilderComponent, RuleModel, ShowButtonsModel } from '@syncfusion/ej2-react-querybuilder';
import { L10n } from '@syncfusion/ej2-base';
import React from 'react';

// Setup RTL
L10n.load({
  'ar-AE': {
    'querybuilder': {
      'AddCondition': 'اضافة الشرط',
      'AddGroup': 'إضافة مجموعة'
    }
  }
});

function App() {
  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  const initialRule: RuleModel = {
    condition: 'and',
    rules: [{
      field: 'Country',
      label: 'Country',
      operator: 'equal',
      type: 'string',
      value: 'USA'
    }]
  };

  const buttonOptions: ShowButtonsModel = {
    ruleDelete: true,
    groupInsert: true,
    groupDelete: true
  };

  return (
    <div>
      <QueryBuilderComponent
        width="100%"
        columns={columns}
        rule={initialRule}
        displayMode="Vertical"
        enablePersistence={true}
        enableSeparateConnector={true}
        enableRtl={false}
        sortDirection="Ascending"
        summaryView={true}
        showButtons={buttonOptions}
        maxGroupCount={5}
        allowDragAndDrop={true}
      />
    </div>
  );
}

export default App;
```

This example combines:
- Vertical display mode
- State persistence
- Separate connectors
- Column sorting
- Summary view
- Drag-and-drop
- Button controls
- Nesting limit
