# Rules and Filtering

Learn how to create, manage, and manipulate filter rules and groups programmatically, including drag-and-drop support and button configuration.

## Table of Contents
- [Understanding Rule Structure](#understanding-rule-structure)
- [Creating Rules](#creating-rules)
- [Managing Rules](#managing-rules)
- [Creating Groups](#creating-groups)
- [Managing Groups](#managing-groups)
- [Nested Hierarchies](#nested-hierarchies)
- [Show Buttons Configuration](#show-buttons-configuration)
- [Drag and Drop](#drag-and-drop)

## Understanding Rule Structure

Rules represent individual filter conditions. The `RuleModel` interface defines the structure:

```tsx
interface RuleModel {
  condition?: string;           // 'and' or 'or' (for groups)
  rules?: RuleModel[];          // Child rules (for groups)
  field?: string;               // Column field name
  label?: string;               // Display label
  operator?: string;            // Operator: 'equal', 'contains', etc.
  type?: string;                // Data type
  value?: any;                  // Filter value
  not?: boolean;                // NOT condition (optional)
}
```

### Simple Rule

```tsx
const simpleRule: RuleModel = {
  field: 'EmployeeID',
  label: 'Employee ID',
  operator: 'equal',
  type: 'number',
  value: 1001
};
```

### Rule with NOT Condition

```tsx
const notRule: RuleModel = {
  field: 'Status',
  label: 'Status',
  operator: 'equal',
  type: 'string',
  value: 'Inactive',
  not: true  // NOT Status = 'Inactive'
};
```

## Creating Rules

### Initial Rules on Load

Set initial rules with the `rule` property:

```tsx
import { QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  const initialRule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'EmployeeID',
        label: 'Employee ID',
        operator: 'equal',
        type: 'number',
        value: 1001
      },
      {
        field: 'Title',
        label: 'Title',
        operator: 'equal',
        type: 'string',
        value: 'Sales Manager'
      }
    ]
  };

  return (
    <QueryBuilderComponent
      width="100%"
      columns={columns}
      rule={initialRule}
    />
  );
}

export default App;
```

### Programmatic Rule Creation

Add rules at runtime using the `addRules` method:

```tsx
let qryBldrObj: QueryBuilderComponent;

function addNewRule(): void {
  const newRule: RuleModel = {
    field: 'Country',
    label: 'Country',
    operator: 'equal',
    type: 'string',
    value: 'USA'
  };
  
  qryBldrObj.addRules([newRule], 'group0');
}

return (
  <div>
    <QueryBuilderComponent
      ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      columns={columns}
      rule={initialRule}
    />
    <button onClick={addNewRule}>Add Country Filter</button>
  </div>
);
```

### Adding Multiple Rules

```tsx
function addMultipleRules(): void {
  const newRules: RuleModel[] = [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      operator: 'greaterthan',
      type: 'number',
      value: 1000
    },
    {
      field: 'Title',
      label: 'Title',
      operator: 'contains',
      type: 'string',
      value: 'Manager'
    }
  ];
  
  qryBldrObj.addRules(newRules, 'group0');
}
```

## Managing Rules

### Retrieving Rules

Get the current rule set:

```tsx
function getRulesData(): void {
  const rules = qryBldrObj.getRules();
  console.log('Current rules:', rules);
}
```

### Getting a Single Rule

```tsx
function getSingleRule(ruleId: string): void {
  const rule = qryBldrObj.getRule(ruleId);
  console.log('Rule:', rule);
}
```

### Setting Rules

Replace all rules with new ones:

```tsx
function updateRules(): void {
  const newRules: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      }
    ]
  };
  
  qryBldrObj.setRules(newRules);
}
```

### Deleting Rules

Remove individual rules by ID:

```tsx
function deleteRule(ruleId: string): void {
  qryBldrObj.deleteRules([ruleId]);
}

function deleteMultipleRules(ruleIds: string[]): void {
  qryBldrObj.deleteRules(ruleIds);
}
```

### Cloning Rules

Create a copy of a rule:

```tsx
function cloneExistingRule(ruleId: string): void {
  // Clones ruleId and adds to group0
  qryBldrObj.cloneRule(ruleId, 'group0', 0);
}
```

Parameters:
- `ruleID` - ID of the rule to clone
- `groupID` - Target group for the cloned rule
- `index` - Position in the group (optional)

## Creating Groups

Groups combine multiple rules with a condition (AND/OR). Creating a group:

```tsx
function addNewGroup(): void {
  const newGroup: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'FirstName',
        label: 'First Name',
        operator: 'startswith',
        type: 'string',
        value: 'v'
      }
    ]
  };
  
  qryBldrObj.addGroups([newGroup], 'group0');
}
```

### Initial Group Structure

```tsx
const initialRule: RuleModel = {
  condition: 'and',
  rules: [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      operator: 'equal',
      type: 'number',
      value: 1001
    },
    {
      condition: 'or',  // Nested group
      rules: [
        {
          field: 'Title',
          label: 'Title',
          operator: 'equal',
          type: 'string',
          value: 'Manager'
        },
        {
          field: 'Title',
          label: 'Title',
          operator: 'equal',
          type: 'string',
          value: 'Developer'
        }
      ]
    }
  ]
};
```

This creates:
```
(EmployeeID = 1001) AND (Title = 'Manager' OR Title = 'Developer')
```

## Managing Groups

### Retrieving Groups

Get a specific group:

```tsx
function getGroupData(groupId: string): void {
  const group = qryBldrObj.getGroup(groupId);
  console.log('Group:', group);
}
```

### Deleting Groups

Remove groups by ID:

```tsx
function deleteGroup(groupId: string): void {
  qryBldrObj.deleteGroups([groupId]);
}

function deleteMultipleGroups(groupIds: string[]): void {
  qryBldrObj.deleteGroups(groupIds);
}
```

### Cloning Groups

Create a copy of a group:

```tsx
function cloneExistingGroup(groupId: string): void {
  qryBldrObj.cloneGroup(groupId, 'group0', 0);
}
```

Parameters:
- `groupID` - ID of the group to clone
- `parentGroupID` - Target parent group
- `index` - Position in parent (optional)

### Locking Groups

Make groups read-only:

```tsx
function lockGroup(groupId: string): void {
  qryBldrObj.lockGroup(groupId);
  // Users cannot edit or delete this group
}
```

## Nested Hierarchies

### Creating Complex Nested Rules

```tsx
const complexRule: RuleModel = {
  condition: 'and',
  rules: [
    // Simple rule
    {
      field: 'Country',
      label: 'Country',
      operator: 'equal',
      type: 'string',
      value: 'USA'
    },
    // OR Group with nested rules
    {
      condition: 'or',
      rules: [
        {
          field: 'Title',
          label: 'Title',
          operator: 'equal',
          type: 'string',
          value: 'Manager'
        },
        {
          field: 'Title',
          label: 'Title',
          operator: 'equal',
          type: 'string',
          value: 'Developer'
        }
      ]
    },
    // Another AND Group
    {
      condition: 'and',
      rules: [
        {
          field: 'Salary',
          label: 'Salary',
          operator: 'greaterthan',
          type: 'number',
          value: 50000
        },
        {
          field: 'YearsWorked',
          label: 'Years Worked',
          operator: 'greaterthanorequal',
          type: 'number',
          value: 5
        }
      ]
    }
  ]
};

// Result: (Country = 'USA') AND (Title = 'Manager' OR Title = 'Developer') AND (Salary > 50000 AND YearsWorked >= 5)
```

### Max Group Depth

Limit nesting with `maxGroupCount`:

```tsx
<QueryBuilderComponent
  columns={columns}
  maxGroupCount={3}  // Maximum 3 levels of nesting
/>
```

## Show Buttons Configuration

Control which buttons appear in the Query Builder:

```tsx
import { ShowButtonsModel } from '@syncfusion/ej2-react-querybuilder';

const buttonOptions: ShowButtonsModel = {
  ruleDelete: true,      // Show delete button for rules
  groupInsert: true,     // Show add group button
  groupDelete: true      // Show delete button for groups
};

<QueryBuilderComponent
  columns={columns}
  showButtons={buttonOptions}
/>
```

### Enabling All Buttons

```tsx
const buttonOptions: ShowButtonsModel = {
  ruleDelete: true,
  groupInsert: true,
  groupDelete: true
};
```

### Hiding Delete Buttons

```tsx
const buttonOptions: ShowButtonsModel = {
  ruleDelete: false,
  groupInsert: true,
  groupDelete: false
};
```

### Dynamic Button Control

```tsx
let qryBldrObj: QueryBuilderComponent;

function updateButtons(): void {
  qryBldrObj.showButtons = {
    ruleDelete: true,
    groupInsert: true,
    groupDelete: true
  };
}
```

## Drag and Drop

Enable drag-and-drop for reordering rules and groups:

```tsx
<QueryBuilderComponent
  columns={columns}
  allowDragAndDrop={true}
/>
```

### Drag Event Handling

```tsx
function onDragStart(args: DragEventArgs): void {
  console.log('Dragging:', args.rule);
}

function onDrag(args: DragEventArgs): void {
  console.log('During drag:', args);
}

function onDrop(args: DropEventArgs): void {
  console.log('Dropped at:', args.targetID);
}

<QueryBuilderComponent
  allowDragAndDrop={true}
  dragStart={onDragStart}
  drag={onDrag}
  drop={onDrop}
/>
```

## Complete Example

```tsx
import { ColumnsModel, QueryBuilderComponent, RuleModel, ShowButtonsModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  let qryBldrObj: QueryBuilderComponent;

  const columns: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  const initialRule: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'Country',
        label: 'Country',
        operator: 'equal',
        type: 'string',
        value: 'USA'
      }
    ]
  };

  const buttonOptions: ShowButtonsModel = {
    ruleDelete: true,
    groupInsert: true,
    groupDelete: true
  };

  function addRule(): void {
    qryBldrObj.addRules([
      {
        field: 'Title',
        label: 'Title',
        operator: 'contains',
        type: 'string',
        value: 'Manager'
      }
    ], 'group0');
  }

  function getRules(): void {
    const rules = qryBldrObj.getRules();
    console.log('Current Rules:', rules);
  }

  function resetRules(): void {
    qryBldrObj.reset();
  }

  return (
    <div>
      <QueryBuilderComponent
        width="100%"
        columns={columns}
        rule={initialRule}
        showButtons={buttonOptions}
        allowDragAndDrop={true}
        ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
      />
      <div>
        <button onClick={addRule}>Add Title Filter</button>
        <button onClick={getRules}>Get Rules</button>
        <button onClick={resetRules}>Reset Filters</button>
      </div>
    </div>
  );
}

export default App;
```

This example demonstrates:
- Initial rule with nested structure
- Controlled button visibility
- Drag-and-drop support
- Programmatic rule management
