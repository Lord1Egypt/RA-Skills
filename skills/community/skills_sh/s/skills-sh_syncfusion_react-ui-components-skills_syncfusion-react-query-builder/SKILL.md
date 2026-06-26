---
name: syncfusion-react-query-builder
description: Comprehensive guide to implementing Syncfusion React Query Builder component. Use this skill when building advanced filter interfaces, creating complex data query systems, or implementing dynamic rule-based filtering. This skill covers query builder configuration, SQL query conversion, drag-and-drop filtering, customization, and state management.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Forms"
---

# Implementing Syncfusion React Query Builder

A comprehensive guide for implementing and customizing the Syncfusion React Query Builder component. The Query Builder is a powerful UI component for creating and managing complex filter conditions, with support for rule-based queries, multiple data types, SQL generation, and extensive customization options.

## Component Overview

The Query Builder component provides a graphical interface for creating and editing complex filter rules. It outputs structured JSON that can be converted to SQL, Mongo queries, or custom predicates for filtering data. Key capabilities include:

- **Rule Management:** Create, edit, delete, and nest rules and groups
- **Multiple Data Types:** Support for string, number, date, boolean, and custom types
- **Operator Support:** 16+ built-in operators (equal, contains, between, in, etc.)
- **Query Conversion:** Convert to SQL, Mongo, or parameterized queries
- **Customization:** Custom templates, themes, and styling
- **Accessibility:** WCAG compliant with keyboard navigation and screen reader support
- **Advanced Features:** Drag-and-drop, state persistence, cloning, locking

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic component initialization
- CSS imports and themes
- Creating your first Query Builder
- Column definition basics
- Running the application

### Columns and Operators
📄 **Read:** [references/columns-and-operators.md](references/columns-and-operators.md)
- Defining column schema with ColumnsModel
- Auto-generating columns from data sources
- Configuring labels and field mappings
- Supported operators by data type
- Setting step and format properties
- Column validation configuration

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding local data arrays
- Remote data with DataManager
- ODataV4Adaptor integration
- Dynamic data updates
- Using DataManager with Query Builder
- Handling data source changes

### Rules and Filtering
📄 **Read:** [references/rules-and-filtering.md](references/rules-and-filtering.md)
- Understanding rule structure (RuleModel)
- Creating rules programmatically with addRules
- Creating groups with addGroups
- Deleting rules and groups
- Managing nested rule hierarchies
- Drag-and-drop rule management
- Show buttons configuration

### Query Conversion
📄 **Read:** [references/query-conversion.md](references/query-conversion.md)
- Converting rules to SQL with getSqlFromRules
- Generating Mongo queries with getMongoQuery
- Creating parameterized SQL queries
- Named parameter SQL generation
- Converting predicates for DataManager
- Importing rules from SQL queries
- Handling localization in SQL conversion

### Templates and Customization
📄 **Read:** [references/templates-and-customization.md](references/templates-and-customization.md)
- Creating custom header templates
- Custom component injection into templates
- Styling with CSS classes and cssClass property
- Theme Studio integration
- Custom operator definitions
- Handling actionBegin events for customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Display modes (Horizontal and Vertical layouts)
- Cloning rules and groups with cloneRule/cloneGroup
- Locking rules and groups for read-only access
- Separate connectors for visual distinction
- Restricting group operations
- RTL (Right-to-Left) support
- State persistence with enablePersistence
- Sort direction configuration
- Summary view display
- Accessibility and keyboard navigation

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete properties list with types and defaults
- All methods with parameters and return types
- Event handlers and event arguments
- Model interfaces (RuleModel, ColumnsModel, ShowButtonsModel)
- Return type definitions and data structures
- Property usage patterns

## Quick Start Example

```tsx
import { ColumnsModel, QueryBuilderComponent, RuleModel } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';

function App() {
  const columnData: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'Employee ID', type: 'number' },
    { field: 'FirstName', label: 'First Name', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'HireDate', label: 'Hire Date', type: 'date', format: 'dd/MM/yyyy' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  const initialRules: RuleModel = {
    condition: 'and',
    rules: [
      {
        field: 'EmployeeID',
        label: 'Employee ID',
        operator: 'equal',
        type: 'number',
        value: 1001
      }
    ]
  };

  return (
    <QueryBuilderComponent 
      width="100%" 
      columns={columnData} 
      rule={initialRules}
    />
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Retrieving Filtered Results as SQL

```tsx
let qryBldrObj: QueryBuilderComponent;

function generateSQL() {
  const sqlQuery = qryBldrObj.getSqlFromRules();
  console.log('Generated SQL:', sqlQuery);
  // Send to backend for execution
}
```

### Pattern 2: Programmatically Adding Rules

```tsx
function addFilter() {
  qryBldrObj.addRules([
    {
      field: 'Country',
      label: 'Country',
      operator: 'equal',
      type: 'string',
      value: 'USA'
    }
  ], 'group0');
}
```

### Pattern 3: Converting SQL Back to Rules

```tsx
function importFilter(sqlString: string) {
  qryBldrObj.setRulesFromSql(sqlString);
}
```

### Pattern 4: Displaying Summary View

```tsx
<QueryBuilderComponent 
  columns={columnData}
  summaryView={true}  // Shows query summary at the bottom
/>
```

## Key Props Cheat Sheet

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `columns` | ColumnsModel[] | - | Defines available fields and operators |
| `rule` | RuleModel | {} | Initial filter rules |
| `dataSource` | Object[] \| DataManager | [] | Data for binding |
| `displayMode` | 'Horizontal' \| 'Vertical' | 'Horizontal' | Layout orientation |
| `allowDragAndDrop` | boolean | false | Enable drag-drop rule management |
| `enablePersistence` | boolean | false | Save state to localStorage |
| `enableRtl` | boolean | false | Right-to-left layout |
| `allowValidation` | boolean | false | Validate rule conditions |
| `summaryView` | boolean | false | Show filtered query summary |
| `showButtons` | ShowButtonsModel | defaults | Control add/delete button visibility |
| `maxGroupCount` | number | 5 | Maximum nested group depth |
| `readonly` | boolean | false | Make component read-only |

## Common Use Cases

### Use Case 1: Advanced Search Filter

Create a filter interface for users to build complex search queries with multiple conditions:

1. Define columns for searchable fields
2. Initialize with empty or default rules
3. Set `showButtons` to enable rule management
4. Retrieve SQL on form submission
5. Execute query on backend

**Read:** [references/rules-and-filtering.md](references/rules-and-filtering.md) and [references/query-conversion.md](references/query-conversion.md)

### Use Case 2: Data-Driven Dashboard

Build a dashboard where users filter data across multiple columns:

1. Bind DataManager with remote service
2. Configure columns based on data types
3. Enable drag-and-drop for better UX
4. Use getPredicate() to filter DataManager
5. Display filtered results dynamically

**Read:** [references/data-binding.md](references/data-binding.md) and [references/rules-and-filtering.md](references/rules-and-filtering.md)

### Use Case 3: Query Template System

Allow users to save and load filter templates:

1. Set `enablePersistence={true}` for automatic state saving
2. Or manually save `getRules()` to database
3. Load rules with `setRules()` when needed
4. Display saved templates in a dropdown

**Read:** [references/advanced-features.md](references/advanced-features.md)

### Use Case 4: Report Builder

Create a report filter UI with custom templates:

1. Design custom header template for branding
2. Use custom operators for domain-specific filtering
3. Enable validation with `allowValidation`
4. Display `summaryView` for clarity
5. Generate SQL for report execution

**Read:** [references/templates-and-customization.md](references/templates-and-customization.md) and [references/advanced-features.md](references/advanced-features.md)

## Next Steps

1. **Getting Started:** Install the package and create your first Query Builder
2. **Define Columns:** Configure the fields users can filter on
3. **Bind Data:** Connect to local or remote data sources
4. **Build UI:** Add rules and groups with drag-and-drop support
5. **Generate Queries:** Convert rules to SQL or other formats
6. **Customize:** Apply themes, templates, and accessibility features

---

**Need help?** Check the specific reference files above for detailed examples and implementation patterns.
