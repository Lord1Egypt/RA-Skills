# Core Structure: Cards, Columns, and Key Fields

## Table of Contents
- [Overview](#overview)
- [Key Field Mapping](#key-field-mapping)
- [Card Settings](#card-settings)
- [Column Configuration](#column-configuration)
- [Single-Key vs Multi-Key Mapping](#single-key-vs-multi-key-mapping)
- [Advanced Card Configuration](#advanced-card-configuration)

## Overview

The Kanban board's core structure consists of three main concepts:

1. **Key Field**: The field in your data that determines column assignment
2. **Cards**: Visual items representing tasks, mapped to columns by their key field value
3. **Columns**: Workflow stages that organize cards horizontally

Understanding how these three work together is essential for building effective Kanban boards.

## Key Field Mapping

The `keyField` property on `KanbanComponent` specifies which field in your data to use for column assignment:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App() {
  let data = extend([], kanbanData, null, true);
  
  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**How it works:**
- Kanban reads the `Status` field from each data item
- If `Status === 'Open'`, the card appears in the "To Do" column
- If `Status === 'InProgress'`, the card appears in the "In Progress" column
- If `Status === 'Closed'`, the card appears in the "Done" column

**Example data:**
```js
const data = [
  { Id: 1, Status: 'Open', Summary: 'Task A' },      // → To Do column
  { Id: 2, Status: 'InProgress', Summary: 'Task B' }, // → In Progress column
  { Id: 3, Status: 'Closed', Summary: 'Task C' }      // → Done column
];
```

## Card Settings

Configure what displays on each card using `cardSettings`:

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

<KanbanComponent
  cardSettings={{
    headerField: 'Id',           // Field for card header
    contentField: 'Summary',     // Field for card body
    showHeader: true,            // Toggle header visibility
    selectionType: 'Single',     // Single or Multiple card selection
    tagsField: 'Tags',          // Field for tags display
    grabberField: 'Priority'    // Field for visual indicator
  }}
>
  {/* ... */}
</KanbanComponent>
```

### Required Fields
- **headerField** (MANDATORY): Must be unique for each card. Acts as card ID. Examples: `Id`, `TaskId`, `Ticket`
- **contentField**: The main text displayed in the card. Examples: `Summary`, `Title`, `Description`

### Optional Fields
- **showHeader**: `true`/`false` — Display or hide the header section
- **selectionType**: `'Single'` (default) or `'Multiple'` — How many cards user can select
- **tagsField**: Display comma-separated tags below content. Example: `'Tags'` displays `'bug,urgent'`
- **grabberField**: Visual indicator like priority color. Display color-coded field in left margin

### Example with All Settings

```tsx
import * as React from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

const data: = [
  {
    Id: 'PROJ-101',
    Status: 'Open',
    Summary: 'Design new dashboard',
    Tags: 'design,ui',
    Priority: 'High',
    Assignee: 'Sarah'
  },
  {
    Id: 'PROJ-102',
    Status: 'InProgress',
    Summary: 'Implement API endpoints',
    Tags: 'backend,api',
    Priority: 'Critical',
    Assignee: 'John'
  }
];

<KanbanComponent
  dataSource={data}
  keyField="Status"
  cardSettings={{
    headerField: 'Id',
    contentField: 'Summary',
    showHeader: true,
    tagsField: 'Tags',
    grabberField: 'Priority'
  }}
>
  <ColumnsDirective>
    <ColumnDirective keyField="Open" headerText="To Do" />
    <ColumnDirective keyField="InProgress" headerText="In Progress" />
  </ColumnsDirective>
</KanbanComponent>
```

**Display result:**
- Card header: `PROJ-101` and `PROJ-102`
- Card content: "Design new dashboard" and "Implement API endpoints"
- Tags: "design,ui" and "backend,api"
- Grabber (left edge): Colored by Priority value

## Column Configuration

Define columns with `ColumnDirective`:

```tsx
import { ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

<ColumnsDirective>
  <ColumnDirective 
    keyField="Open" 
    headerText="To Do"
    showAddButton={true}          // Show + button to add cards
    showItemCount={true}          // Show card count
    allowDrag={true}              // Allow dragging from this column
    allowDrop={true}              // Allow dropping into this column
    maxCount={10}                 // Max cards allowed (WIP limit)
    minCount={1}                  // Min cards required
  />
</ColumnsDirective>
```

### Column Properties
- **keyField** (required): Value to match in data's key field
- **headerText**: Display name for the column
- **showAddButton**: Display "+" button for adding new cards
- **showItemCount**: Display card count badge
- **allowDrag**: Enable/disable dragging from this column
- **allowDrop**: Enable/disable dropping into this column
- **maxCount/minCount**: Work-in-progress (WIP) limits
## Stacked Headers

Stacked headers allow grouping multiple columns under a common header, providing a hierarchical organization of workflow stages.

### Configuring Stacked Headers

Use the `stackedHeaders` property or the `StackedHeadersDirective` to group related columns:

```tsx
import { KanbanComponent, StackedHeadersDirective, StackedHeaderDirective } from '@syncfusion/ej2-react-kanban';

<KanbanComponent 
  id="kanban" 
  keyField="Status" 
  dataSource={data}
>
  <StackedHeadersDirective>
    <StackedHeaderDirective text="To Do Details" keyFields="Open, Backlog" />
    <StackedHeaderDirective text="Progress Details" keyFields="InProgress, Testing" />
  </StackedHeadersDirective>
  <ColumnsDirective>
    <ColumnDirective headerText="To Do" keyField="Open" />
    <ColumnDirective headerText="Backlog" keyField="Backlog" />
    <ColumnDirective headerText="In Progress" keyField="InProgress" />
    <ColumnDirective headerText="Testing" keyField="Testing" />
    <ColumnDirective headerText="Done" keyField="Close" />
  </ColumnsDirective>
</KanbanComponent>
```

**Key Properties:**
- **text**: The label displayed for the grouped columns.
- **keyFields**: A comma-separated string containing the `keyField` values of the columns to be grouped.

### Use Cases for Stacked Headers
- Grouping sub-stages of a large workflow (e.g., "Development" and "Testing" under "Engineering").
- Organizing multiple status columns under descriptive categories.
- Managing complex boards with many columns by adding a secondary header layer.
## Single-Key vs Multi-Key Mapping

### Single-Key Mapping (Default)
One column per key value:

```tsx
<ColumnsDirective>
  <ColumnDirective keyField="Open" headerText="To Do" />
  <ColumnDirective keyField="InProgress" headerText="In Progress" />
  <ColumnDirective keyField="Closed" headerText="Done" />
</ColumnsDirective>
```

Data with `Status: 'Open'` goes to "To Do", `Status: 'InProgress'` goes to "In Progress", etc.

### Multi-Key Mapping
Multiple key values in one column:

```tsx
<ColumnsDirective>
  <ColumnDirective keyField="Open, Backlog" headerText="To Do" />
  <ColumnDirective keyField="InProgress" headerText="In Progress" />
  <ColumnDirective keyField="Closed" headerText="Done" />
</ColumnsDirective>
```

Cards with `Status: 'Open'` OR `Status: 'Backlog'` both appear in "To Do" column.

**Use case:** Group related statuses together (e.g., "New, Unassigned" → "Open" column)

## Advanced Card Configuration

### Hide Card Header

```tsx
cardSettings={{
  headerField: 'Id',
  contentField: 'Summary',
  showHeader: false  // Only content displays
}}
```

Cards display only the content field, no header section.

### Handle Card Selection

Enable multi-select for bulk operations:

```tsx
cardSettings={{
  selectionType: 'Multiple'
}}
```

Users click checkboxes to select multiple cards for batch actions.

### Card-Level Customization with Methods

Add or update cards programmatically:

```tsx
import * as React from 'react';
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleAddCard = (): void => {
  const newCard = {
    Id: 'TASK-999',
    Status: 'Open',
    Summary: 'New task added'
  };
  kanbanRef.current?.addCard(newCard);
};

<KanbanComponent ref={kanbanRef}>
  {/* ... */}
</KanbanComponent>
```

### Common Column Patterns

**Read-only done column:**
```tsx
<ColumnDirective 
  keyField="Closed" 
  headerText="Done"
  allowDrag={false}
  allowDrop={false}
/>
```

**Accumulation with WIP limit:**
```tsx
<ColumnDirective 
  keyField="InProgress" 
  headerText="In Progress"
  maxCount={5}
  minCount={1}
/>
```

**Hidden column (visible but stacked):**
```tsx
<ColumnDirective 
  keyField="OnHold" 
  headerText="On Hold"
  isExpanded={false}  // Collapsed by default
/>
```
