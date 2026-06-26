# Templates and Customization

Learn how to customize the Query Builder with templates, styling, themes, and custom components.

## Table of Contents
- [Overview](#overview)
- [Header Templates](#header-templates)
- [CSS Class Styling](#css-class-styling)
- [Theme Studio Integration](#theme-studio-integration)
- [Custom Operators](#custom-operators)
- [Event-Based Customization](#event-based-customization)

## Overview

The Query Builder offers multiple ways to customize appearance and behavior:

- **Header Templates** - Custom components in the header area
- **CSS Styling** - Override default styles
- **Theme Studio** - Create custom themes visually
- **Custom Operators** - Add domain-specific operators
- **Event Handlers** - Respond to user actions

## Header Templates

### Basic Header Template

Use the `headerTemplate` property to create custom headers:

```tsx
import { QueryBuilderComponent } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function CustomHeader(props: any) {
  return (
    <div className="custom-header">
      <span>{props.condition}</span>
      <button>Custom Action</button>
    </div>
  );
}

function App() {
  return (
    <QueryBuilderComponent
      columns={columns}
      headerTemplate={(props) => <CustomHeader {...props} />}
    />
  );
}

export default App;
```

### Header Template with Condition Control

```tsx
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';

function AdvancedHeader(props: any) {
  const handleConditionChange = (e: any) => {
    props.condition = e.value;
  };

  const handleNotChange = (e: any) => {
    props.not = e.checked;
  };

  return (
    <div className="e-custom-header">
      <DropDownListComponent
        dataSource={['AND', 'OR']}
        value={props.condition}
        change={handleConditionChange}
      />
      <CheckBoxComponent
        checked={props.not}
        change={handleNotChange}
        label="NOT"
      />
    </div>
  );
}

<QueryBuilderComponent
  columns={columns}
  headerTemplate={(props) => <AdvancedHeader {...props} />}
/>
```

### Event-Based Template Creation

```tsx
function App() {
  let qryBldrObj: QueryBuilderComponent;

  function onActionBegin(args: any) {
    if (args.requestType === 'header-template-create') {
      const element = document.createElement('div');
      element.innerHTML = `
        <div class="custom-header">
          <span>Custom Condition: ${args.rule?.condition}</span>
        </div>
      `;
      args.element = element;
    }
  }

  return (
    <QueryBuilderComponent
      columns={columns}
      actionBegin={onActionBegin}
      ref={(scope) => { qryBldrObj = scope as QueryBuilderComponent; }}
    />
  );
}
```

## CSS Class Styling

### Available CSS Classes

| CSS Class | Target |
|-----------|--------|
| `.e-query-builder` | Main container |
| `.e-group-header` | Group header area |
| `.e-group-body` | Group body area |
| `.e-rule-container` | Individual rule container |
| `.e-group-container` | Group container |
| `.e-btn` | Condition button (AND/OR) |
| `.e-dropdown-btn` | Add Group/Condition button |
| `.e-deletegroup` | Delete Group button |
| `.e-rule-delete` | Delete Condition button |
| `.e-rule-list` | Rule list container |
| `.e-rule-list > ::after` | Group joining lines |
| `.e-rule-container.e-joined-rule` | Condition joining lines |

### Custom Styling Example

```css
/* Main Query Builder */
.e-query-builder {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 16px;
}

/* Condition button (AND/OR) */
.e-group-header .e-btn {
  background-color: #2196F3;
  border: 1px solid #1976D2;
  color: white;
  font-weight: bold;
  border-radius: 4px;
}

.e-group-header .e-btn:hover {
  background-color: #1976D2;
}

/* Delete buttons */
.e-query-builder .e-rule-delete,
.e-query-builder .e-deletegroup {
  background-color: #f44336;
  border-color: #d32f2f;
}

.e-query-builder .e-rule-delete:hover,
.e-query-builder .e-deletegroup:hover {
  background-color: #d32f2f;
}

/* Group joining lines */
.e-query-builder .e-rule-list > ::before,
.e-query-builder .e-rule-list > ::after {
  border-color: #ccc;
}

.e-query-builder .e-rule-container.e-joined-rule {
  border-left: 2px solid #2196F3;
}
```

### Applying Custom Styles

```tsx
import './custom-styles.css';

<QueryBuilderComponent
  columns={columns}
  cssClass="custom-query-builder"
/>
```

### Dynamic CSS Class Application

```tsx
<QueryBuilderComponent
  columns={columns}
  cssClass={isDarkMode ? 'qb-dark-theme' : 'qb-light-theme'}
/>
```

## Theme Studio Integration

### Available Built-in Themes

The Query Builder supports several built-in themes:

- **Material** - Material Design
- **Bootstrap** - Bootstrap 5
- **Bootstrap4** - Bootstrap 4
- **Fabric** - Microsoft Fabric
- **High Contrast** - Accessibility focused
- **Tailwind** - Tailwind CSS

### Using Built-in Themes

Import the CSS file in your main style:

```css
/* Material Theme */
@import "@syncfusion/ej2-querybuilder/styles/material.css";

/* Bootstrap Theme */
@import "@syncfusion/ej2-querybuilder/styles/bootstrap.css";

/* Tailwind Theme */
@import "@syncfusion/ej2-querybuilder/styles/tailwind3.css";
```

### Creating Custom Themes with Theme Studio

1. Visit [Theme Studio](https://ej2.syncfusion.com/themestudio/?theme=material)
2. Customize colors and styling
3. Download the custom theme CSS
4. Import in your project

```css
@import "./custom-theme.css";
```

### CSS Variables for Theming

Override theme colors using CSS variables:

```css
:root {
  --qb-primary-color: #2196F3;
  --qb-text-color: #333;
  --qb-border-color: #ccc;
  --qb-button-bg: #f5f5f5;
  --qb-hover-bg: #e0e0e0;
}

.e-query-builder {
  --qb-primary-color: var(--qb-primary-color);
}
```

## Custom Operators

### Adding Custom Operators

```tsx
const columns: ColumnsModel[] = [
  {
    field: 'Status',
    label: 'Status',
    type: 'string',
    operators: [
      { key: 'Equal', value: 'equal' },
      { key: 'Not Equal', value: 'notequal' },
      { key: 'Is Active', value: 'isactive' },         // Custom
      { key: 'Is Inactive', value: 'isinactive' }      // Custom
    ]
  }
];
```

### Handling Custom Operators

```tsx
function onActionBegin(args: ActionEventArgs): void {
  if (args.requestType === 'rule-change') {
    const rule = args.rule;
    
    if (rule?.operator === 'isactive') {
      rule.value = 'Active';
      rule.operator = 'equal';
    } else if (rule?.operator === 'isinactive') {
      rule.value = 'Inactive';
      rule.operator = 'equal';
    }
  }
}

<QueryBuilderComponent
  columns={columns}
  actionBegin={onActionBegin}
/>
```

### Custom Operator with Special Logic

```tsx
function onActionBegin(args: ActionEventArgs): void {
  if (args.requestType === 'rule-change' && args.rule?.operator === 'custom-range') {
    // Handle custom range operator
    if (args.rule.value && typeof args.rule.value === 'string') {
      const [min, max] = args.rule.value.split('-');
      args.rule.value = { min: parseInt(min), max: parseInt(max) };
    }
  }
}

<QueryBuilderComponent
  columns={columns}
  actionBegin={onActionBegin}
/>
```

## Event-Based Customization

### ActionBegin Event

Responds to user actions like field/operator/value changes:

```tsx
function onActionBegin(args: ActionEventArgs): void {
  console.log('Action Type:', args.requestType);
  
  switch (args.requestType) {
    case 'rule-change':
      console.log('Rule changed:', args.rule);
      break;
    case 'condition-change':
      console.log('Condition changed:', args.condition);
      break;
    case 'header-template-create':
      console.log('Header template created');
      break;
  }
}

<QueryBuilderComponent
  columns={columns}
  actionBegin={onActionBegin}
/>
```

### Change Event

Triggers when rules are modified:

```tsx
function onChange(args: ChangeEventArgs): void {
  console.log('Rules changed:', args.rule);
  console.log('Parent ID:', args.groupID);
}

<QueryBuilderComponent
  columns={columns}
  change={onChange}
/>
```

### BeforeChange Event

Triggers before changes are applied:

```tsx
function onBeforeChange(args: ChangeEventArgs): void {
  // Prevent certain changes
  if (args.rule?.operator === 'forbidden') {
    args.cancel = true;
    console.log('This operator is not allowed');
  }
}

<QueryBuilderComponent
  columns={columns}
  beforeChange={onBeforeChange}
/>
```

### RuleChange Event

Triggers when rules change with detailed information:

```tsx
function onRuleChange(args: RuleChangeEventArgs): void {
  console.log('Previous value:', args.previousRule);
  console.log('New value:', args.rule);
  console.log('Parent group:', args.groupID);
}

<QueryBuilderComponent
  columns={columns}
  ruleChange={onRuleChange}
/>
```

## Complete Customization Example

```tsx
import { ColumnsModel, QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';
import './custom-styles.css';

function App() {
  const columns: ColumnsModel[] = [
    {
      field: 'EmployeeID',
      label: 'Employee ID',
      type: 'number'
    },
    {
      field: 'Status',
      label: 'Status',
      type: 'string',
      operators: [
        { key: 'Equal', value: 'equal' },
        { key: 'Is Active', value: 'isactive' }
      ]
    }
  ];

  function customHeader(props: any) {
    return (
      <div className="custom-qb-header">
        <strong>{props.condition?.toUpperCase()}</strong>
        <span className="rule-count">
          {props.ruleCount || 0} conditions
        </span>
      </div>
    );
  }

  function onActionBegin(args: any): void {
    if (args.requestType === 'rule-change') {
      if (args.rule?.operator === 'isactive') {
        args.rule.value = 'Active';
        args.rule.operator = 'equal';
      }
    }
  }

  function onChange(args: any): void {
    console.log('Updated rules:', args.rule);
  }

  return (
    <div className="app-container">
      <QueryBuilderComponent
        width="100%"
        columns={columns}
        cssClass="custom-query-builder"
        headerTemplate={customHeader}
        actionBegin={onActionBegin}
        change={onChange}
      />
    </div>
  );
}

export default App;
```

**CSS:**
```css
.app-container {
  padding: 20px;
}

.custom-query-builder {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  padding: 20px;
}

.custom-query-builder .e-group-header .e-btn {
  background-color: #667eea;
  border: none;
  color: white;
  font-weight: bold;
}

.custom-qb-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.rule-count {
  background-color: #764ba2;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}
```

This example demonstrates:
- Custom header template
- Custom CSS styling
- Custom operators with logic
- Event-based customization
- Complete theme integration
