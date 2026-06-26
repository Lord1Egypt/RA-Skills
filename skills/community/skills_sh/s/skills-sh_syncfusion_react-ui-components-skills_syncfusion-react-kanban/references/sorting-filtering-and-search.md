# Sorting, Filtering, and Work-in-Progress (WIP) Validation

## Table of Contents
- [Overview](#overview)
- [Sorting Cards](#sorting-cards)
- [WIP Limits (Min/Max Card Count)](#wip-limits-minmax-card-count)
- [Card Selection](#card-selection)
- [Filtering and Search](#filtering-and-search)
- [Validation Patterns](#validation-patterns)
- [Troubleshooting](#troubleshooting)

## Overview

Kanban supports sorting cards by a single field through the `sortSettings` property. For multi-field sorting, you must pre-sort the data before passing it to the component. Additionally, you can enforce work-in-progress (WIP) limits to prevent overload, enable selection of multiple cards for batch operations, and implement filtering to focus on specific tasks.

## Sorting Cards

### Basic Sorting

Control card order with `sortSettings`:

```tsx
import { SortSettingsModel } from '@syncfusion/ej2-react-kanban';

const sortSettings: SortSettingsModel = {
  field: 'Priority',           // Sort by Priority field
  direction: 'Descending'      // High priority first
};

<KanbanComponent sortSettings={sortSettings}>
  {/* ... */}
</KanbanComponent>
```

### Multi-Field Sorting

**Note:** The `SortSettingsModel` currently supports sorting by a **single field only**. To achieve multi-field sorting, you must manually sort the data in your component before passing it to the Kanban component:

```tsx
import { SortSettingsModel } from '@syncfusion/ej2-react-kanban';

// Sort data by Priority first, then by DueDate
const sortedTasks = [...tasks].sort((a, b) => {
  // First sort by Priority (Descending)
  if (a.Priority !== b.Priority) {
    const priorityOrder = { 'High': 1, 'Medium': 2, 'Low': 3 };
    return (priorityOrder[a.Priority] || 999) - (priorityOrder[b.Priority] || 999);
  }
  // Then sort by DueDate (Ascending)
  return new Date(a.DueDate).getTime() - new Date(b.DueDate).getTime();
});

const sortSettings: SortSettingsModel = {
  field: 'Priority',
  direction: 'Descending'
};

<KanbanComponent dataSource={sortedTasks} sortSettings={sortSettings}>
  {/* ... */}
</KanbanComponent>
```

**Result:**
1. Cards sorted by Priority (High → Low)
2. Within each priority, sorted by DueDate (Early → Late)
3. Kanban respects the pre-sorted data order

### Enable User Sorting

Allow users to click column headers to sort:

```tsx
import { SortSettingsModel } from '@syncfusion/ej2-react-kanban';

const sortSettings: SortSettingsModel = {
  field: 'Id',
  direction: 'Ascending'
};

<KanbanComponent
  allowSorting={true}
  sortSettings={sortSettings}
>
  {/* Users can click headers to re-sort */}
</KanbanComponent>
```

### Sorting Strategies

**By Priority:**
```jsx
sortSettings={{ field: 'Priority', direction: 'Descending' }}
```
High-priority tasks float up.

**By Due Date:**
```jsx
sortSettings={{ field: 'DueDate', direction: 'Ascending' }}
```
Soonest deadlines first.

**By Estimated Effort:**
```jsx
sortSettings={{ field: 'EstimateHours', direction: 'Ascending' }}
```
Quick wins first (useful for sprint planning).

**By Card ID (Rank):**
```jsx
sortSettings={{ field: 'RankId', direction: 'Ascending' }}
```
Maintain manual ordering by rank.

## WIP Limits (Min/Max Card Count)

Prevent columns from becoming bottlenecks with Work-in-Progress limits:

### Max Limit (Column Overload Prevention)

```jsx
<ColumnDirective 
  keyField="InProgress" 
  headerText="In Progress"
  maxCount={5}  // Max 5 cards at a time
/>
```

**Behavior:**
- Kanban allows dragging up to 5 cards into column
- If attempting to exceed limit, shows warning or prevents drop
- Helps prevent team overcommitment

### Min Limit (Bottleneck Detection)

```jsx
<ColumnDirective 
  keyField="InProgress" 
  headerText="In Progress"
  minCount={1}  // At least 1 card should be in progress
/>
```

**Behavior:**
- Warns if column has fewer cards than minimum
- Signals understaffed or idle column
- Helps balance work across team

### Combined Min and Max

```jsx
<ColumnDirective 
  keyField="InProgress" 
  headerText="In Progress"
  minCount={2}  // At least 2 tasks
  maxCount={8}  // No more than 8 tasks
/>
```

**Sweet spot:** 2-8 tasks keeps team focused and balanced.

### Visual Indicators

Access count info via custom templates:

```jsx
const columnHeaderTemplate = (props) => {
  const count = props.cardCount || 0;
  const max = props.maxCount;
  const isWarning = max && count >= max * 0.8;  // 80% of max
  const isExceeded = max && count > max;
  
  return (
    <div style={{
      backgroundColor: isExceeded ? '#ffebee' : isWarning ? '#fff3e0' : 'transparent',
      padding: '8px',
      borderRadius: '4px'
    }}>
      <strong>{props.headerText}</strong>
      <div style={{ fontSize: '12px', marginTop: '4px' }}>
        {count}{max ? `/${max}` : ''} items
      </div>
      {isExceeded && (
        <div style={{ color: 'red', fontSize: '12px', fontWeight: 'bold' }}>
          Over limit!
        </div>
      )}
    </div>
  );
};

<ColumnDirective 
  keyField="InProgress"
  template={columnHeaderTemplate}
/>
```

## Card Selection

Enable users to select multiple cards for bulk operations:

### Single Selection (Default)

```jsx
<KanbanComponent
  cardSettings={{
    selectionType: 'Single'
  }}
>
  {/* Users can select one card at a time */}
</KanbanComponent>
```

### Multiple Selection

```jsx
<KanbanComponent
  cardSettings={{
    selectionType: 'Multiple'
  }}
  cardSelectionChanging={(args) => {
    console.log('Selected cards:', args.selectedCards);
  }}
>
  {/* Users can Ctrl+Click or Shift+Click to select multiple */}
</KanbanComponent>
```

### Bulk Operations on Selected Cards

```jsx
const handleBulkAssign = () => {
  const selectedCards = kanbanRef.current.getSelectedCards();
  
  selectedCards.forEach(card => {
    card.Assignee = 'Sarah';
    kanbanRef.current.updateCard(card);
  });
};

<button onClick={handleBulkAssign}>Assign to Sarah</button>
```

## Filtering and Search

### Card-Level Filtering

```jsx
const handleSearch = (searchText) => {
  const filtered = data.filter(card =>
    card.Summary.toLowerCase().includes(searchText.toLowerCase()) ||
    card.Id.toString().includes(searchText)
  );
  setData(filtered);
};

<input
  type="text"
  placeholder="Search tasks..."
  onChange={(e) => handleSearch(e.target.value)}
  style={{ marginBottom: '20px', padding: '8px', width: '300px' }}
/>
<KanbanComponent dataSource={data}>
  {/* Filtered data shows */}
</KanbanComponent>
```

### Status-Based Filtering

Show specific columns or hide:

```jsx
const [showOnlyActive, setShowOnlyActive] = useState(false);

const getVisibleColumns = () => {
  if (showOnlyActive) {
    return ['Open', 'InProgress'];  // Only show active work
  }
  return ['Open', 'InProgress', 'Closed'];
};

<KanbanComponent>
  <ColumnsDirective>
    {getVisibleColumns().map(status => (
      <ColumnDirective key={status} keyField={status} headerText={status} />
    ))}
  </ColumnsDirective>
</KanbanComponent>

<label>
  <input
    type="checkbox"
    checked={showOnlyActive}
    onChange={(e) => setShowOnlyActive(e.target.checked)}
  />
  Show Active Work Only
</label>
```

### Priority-Based Display

Highlight or filter by priority:

```jsx
const handleFilterByPriority = (priority) => {
  const filtered = data.filter(card => card.Priority === priority);
  setData(filtered);
};

<div style={{ marginBottom: '20px' }}>
  <button onClick={() => handleFilterByPriority('Critical')}>Show Critical</button>
  <button onClick={() => handleFilterByPriority('High')}>Show High</button>
  <button onClick={() => setData(initialData)}>Show All</button>
</div>

<KanbanComponent dataSource={data}>
  {/* ... */}
</KanbanComponent>
```

### Assignee Filter

```jsx
const [selectedAssignee, setSelectedAssignee] = useState(null);

const filtered = selectedAssignee
  ? data.filter(card => card.Assignee === selectedAssignee)
  : data;

const assignees = [...new Set(data.map(d => d.Assignee))];

<div style={{ marginBottom: '20px' }}>
  <select value={selectedAssignee || ''} onChange={(e) => setSelectedAssignee(e.target.value || null)}>
    <option value="">All Assignees</option>
    {assignees.map(name => <option key={name} value={name}>{name}</option>)}
  </select>
</div>

<KanbanComponent dataSource={filtered}>
  {/* ... */}
</KanbanComponent>
```

## Validation Patterns

### Prevent Moving to Done Without Completion

```jsx
const handleDragStop = (args) => {
  if (args.data.Status === 'Closed' && args.data.CompletionPercentage < 100) {
    args.cancel = true;
    alert('Task must be 100% complete before closing');
  }
};

<KanbanComponent dragStop={handleDragStop}>
  {/* ... */}
</KanbanComponent>
```

### Enforce Status Workflow

```jsx
const validTransitions = {
  'Open': ['InProgress'],
  'InProgress': ['Testing', 'Open'],
  'Testing': ['Closed', 'InProgress'],
  'Closed': []
};

<ColumnDirective 
  keyField="Open"
  transitionColumns={validTransitions['Open']}
/>
<ColumnDirective 
  keyField="InProgress"
  transitionColumns={validTransitions['InProgress']}
/>
```

## Troubleshooting

### Sorting not working
- Ensure field name matches data property exactly
- Verify sort direction is 'Ascending' or 'Descending' (case-sensitive)
- Check that field values are consistent type (not mixed strings/numbers)
- Remember: only **single-field sorting** is supported via `sortSettings`
- For multi-field sorting, pre-sort your data array before passing to `dataSource`

### WIP limits not enforcing
- Verify `maxCount`/`minCount` are set on `ColumnDirective`, not `KanbanComponent`
- Check that drag events aren't being cancelled elsewhere
- Monitor console for validation errors

### Selection not working
- Confirm `selectionType: 'Multiple'` is set
- Verify `cardSelectionChanging` event is properly bound
- Check that cards are not disabled or read-only

### Filter not showing results
- Ensure filter logic matches actual data values
- Check for case sensitivity (use `.toLowerCase()`)
- Verify filtered data array still passed to `dataSource`
