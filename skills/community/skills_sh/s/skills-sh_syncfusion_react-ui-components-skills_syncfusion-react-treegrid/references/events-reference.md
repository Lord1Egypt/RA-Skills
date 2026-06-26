---
name: events-catalog
description: 'Complete event reference for TreeGrid - actionBegin, actionComplete, actionFailure, expand/collapse events, and requestType values.'
---

# Events Reference (Events Catalog)

## Table of Contents
- [Event Handling Rules](#event-handling-rules)
- [Core Action Events](#core-action-events)
- [Data Events](#data-events)
- [Row Events](#row-events)
- [Cell Events](#cell-events)
- [Column Events](#column-events)
- [Editing Events](#editing-events)
- [Selection Events](#selection-events)
- [Expand/Collapse Events](#expandcollapse-events)
- [Drag & Drop Events](#drag--drop-events)
- [RequestType Values](#requesttype-values)
- [Tree-Specific Events](#tree-specific-events)
- [Event Arguments Reference](#event-arguments-reference)
- [Complete Event Example](#complete-event-example)


## Event Handling Rules

### Rule 1: Event Names Follow Specific camelCase Pattern
**Severity**: 🟠 IMPORTANT - Event names must match exactly (case-sensitive)

**Correct Event Names in React**:
```jsx
// ✅ CORRECT - Exact event names (camelCase)
<TreeGridComponent
  onRowSelecting={(args) => handleRowSelecting(args)}
  onRowSelected={(args) => handleRowSelected(args)}
  onRowDeselecting={(args) => handleRowDeselecting(args)}
  onRowDeselected={(args) => handleRowDeselected(args)}
  
  onRowDragStart={(args) => handleRowDragStart(args)}
  onRowDrag={(args) => handleRowDrag(args)}
  onRowDrop={(args) => handleRowDrop(args)}
  onRowDragStop={(args) => handleRowDragStop(args)}
  
  onDataBound={(args) => handleDataBound(args)}
  onDataSourceChanged={(args) => handleDataSourceChanged(args)}
  onDataStateChange={(args) => handleDataStateChange(args)}
  
  onActionBegin={(args) => handleActionBegin(args)}
  onActionComplete={(args) => handleActionComplete(args)}
  onActionFailure={(args) => handleActionFailure(args)}
  
  onQueryCellInfo={(args) => handleQueryCellInfo(args)}
  onRowDataBound={(args) => handleRowDataBound(args)}
  
  onRecordDoubleClick={(args) => handleRecordDoubleClick(args)}
  onCellSave={(args) => handleCellSave(args)}>
</TreeGridComponent>

// ❌ WRONG - Incorrect event names (won't fire)
<TreeGridComponent
  onrowdragstart={handleRowDragStart}      // lowercase 'r' and 'd' - WON'T FIRE
  ondragStart={handleDragStart}            // Should be onRowDragStart - WON'T FIRE
  onRowDragStart={handleRowDragStart}      // Correct format
  ondatabound={handleDataBound}            // Should be onDataBound - WON'T FIRE
  onDataBound={handleDataBound}            // Correct format
/>
```

**Event Handler Patterns in React**:
```jsx
// ✅ CORRECT - Event handlers with type annotations
const handleRowSelecting = (args: RowSelectingEventArgs) => {
  console.log('Row selecting:', args.rowIndex);
};

const handleActionComplete = (args: ActionCompleteEventArgs) => {
  if (args.requestType === 'save') {
    console.log('Record saved:', args.data);
  }
};

<TreeGridComponent
  onRowSelecting={handleRowSelecting}
  onActionComplete={handleActionComplete}>
</TreeGridComponent>

// ✅ ALTERNATIVE - Inline arrow functions
<TreeGridComponent
  onRowSelecting={(args) => {
    console.log('Selected:', args.rowIndex);
  }}
  onActionComplete={(args) => {
    if (args.requestType === 'save') {
      // Handle save
    }
  }}>
</TreeGridComponent>
```

---

### Rule 2: Event Handler State Updates in CRUD Operations
**Severity**: 🟠 IMPORTANT - Async operations require proper state handling

**Requirement in React**:
```jsx
// ✅ CORRECT - Handle async CRUD with proper state update
import { useState } from 'react';

export default function GridWithCRUD() {
  const [data, setData] = useState(initialData);
  
  // Handle data source changes (CRUD operations)
  const handleDataSourceChanged = async (args) => {
    if (args.action === 'add') {
      try {
        // Make API call
        const response = await fetch('/api/tasks', {
          method: 'POST',
          body: JSON.stringify(args.data)
        });
        
        const newRecord = await response.json();
        
        // Update state with server response
        setData(prevData => [...prevData, newRecord]);
        
        // Refresh grid
        gridRef.current?.refresh();
        
      } catch (error) {
        console.error('Add failed:', error);
      }
    } 
    else if (args.action === 'edit') {
      try {
        await fetch(`/api/tasks/${args.data.TaskID}`, {
          method: 'PUT',
          body: JSON.stringify(args.data)
        });
        
        // Update state
        setData(prevData => 
          prevData.map(item => 
            item.TaskID === args.data.TaskID ? args.data : item
          )
        );
        
      } catch (error) {
        console.error('Edit failed:', error);
      }
    } 
    else if (args.action === 'delete') {
      try {
        await fetch(`/api/tasks/${args.data[0].TaskID}`, {
          method: 'DELETE'
        });
        
        // Update state
        setData(prevData => 
          prevData.filter(item => item.TaskID !== args.data[0].TaskID)
        );
        
      } catch (error) {
        console.error('Delete failed:', error);
      }
    }
  };
  
  return (
    <TreeGridComponent 
      dataSource={data}
      editSettings={{ mode: 'Dialog', allowEditing: true, allowAdding: true, allowDeleting: true }}
      onActionComplete={handleDataSourceChanged}>
      <ColumnsDirective>
        <ColumnDirective field='TaskID' isPrimaryKey={true}></ColumnDirective>
      </ColumnsDirective>
      <Inject services={[Edit]} />
    </TreeGridComponent>
  );
}

// ❌ WRONG - Not updating state after CRUD
const handleActionComplete = (args) => {
  if (args.action === 'add') {
    fetch('/api/tasks', { method: 'POST', body: JSON.stringify(args.data) });
    // Missing: Update state! Grid won't reflect changes.
  }
};

// ❌ WRONG - Mutating state directly
const handleActionComplete = (args) => {
  if (args.action === 'add') {
    data.push(args.data);  // DON'T mutate directly!
    // Should use: setData([...data, args.data])
  }
};
```

---

### Rule 3: Event Args Validation and Error Prevention
**Severity**: 🟠 IMPORTANT - Validate event arguments to prevent silent failures

**Requirement in React**:
```jsx
// ✅ CORRECT - Validate and prevent default behavior when needed
<TreeGridComponent
  onRowSelecting={(args) => {
    // Validate before allowing selection
    if (!isValidRow(args.rowData)) {
      args.cancel = true;  // ✅ Prevent selection
    }
  }}
  onBeginEdit={(args) => {
    // Check if user has permission
    if (!hasEditPermission(args.rowData)) {
      args.cancel = true;  // ✅ Prevent edit
    }
  }}
  onBeginDelete={(args) => {
    // Show confirmation
    if (!confirm(`Delete row ${args.index}?`)) {
      args.cancel = true;  // ✅ Prevent deletion
    }
  }}>
</TreeGridComponent>

// ✅ ALTERNATIVE - Use actionBegin for multi-step validation
const handleActionBegin = (args) => {
  if (args.requestType === 'save') {
    // Validation before save
    if (!validateRecord(args.data)) {
      args.cancel = true;  // ✅ Cancel save
      alert('Please fix validation errors');
      return;
    }
  }
};

<TreeGridComponent onActionBegin={handleActionBegin} />

// ❌ WRONG - Allowing invalid operations
const handleRowSelecting = (args) => {
  if (!isValidRow(args.rowData)) {
    // Missing: args.cancel = true
    // Row will be selected even though it's invalid!
  }
};

// ❌ WRONG - Not handling async properly
const handleBeginDelete = async (args) => {
  const confirmed = await showConfirmationDialog();
  if (!confirmed) {
    args.cancel = true;  // May not work as expected
  }
};
```

---


## Property Naming Rules

### Rule 1: Property Names are Case-Sensitive in React
**Severity**: 🔴 CRITICAL - Case mismatch causes silent failures (properties just ignored)

**Correct Property Names in React (camelCase)**:
```jsx
// ✅ CORRECT - Exact casing (camelCase for properties)
<TreeGridComponent 
  allowPaging={true}
  allowSorting={true}
  allowFiltering={true}
  allowRowDragAndDrop={true}      // Capital 'R', 'D', 'A', capital 'D' in second word
  enableVirtualization={true}
  enableInfiniteScrolling={true}
  enablePersistence={true}
  enableAdaptiveUI={true}          // Capital 'A' and 'U'
  showColumnMenu={true}
  childMapping='subtasks'
  idMapping='TaskID'
  parentIdMapping='ParentID'
  hasChildMapping='IsParent'>
</TreeGridComponent>

// ❌ WRONG - Incorrect casing (property is silently ignored!)
<TreeGridComponent 
  allowpaging={true}              // lowercase 'p' - IGNORED
  allowsorting={true}              // lowercase 's' - IGNORED
  allowfiltering={true}            // lowercase 'f' - IGNORED
  allowRowDragandDrop={true}       // lowercase 'a' in 'and' - IGNORED!
  enablevirtualization={true}      // lowercase 'v' - IGNORED
  childmapping='subtasks'          // lowercase 'c' and 'm' - IGNORED
  idmapping='TaskID'               // lowercase 'i' and 'm' - IGNORED
/>
```

**Column Property Casing (Must Match Exactly)**:
```jsx
// ✅ CORRECT - Exact camelCase for column properties
<ColumnDirective
  isPrimaryKey={true}       // Capital 'I' and 'P'
  isFrozen={true}
  isIdentity={true}
  allowSorting={true}       // Capital 'A' and 'S'
  allowFiltering={true}
  allowSearching={true}
  enableGrouping={true}
  displayAsCheckBox={true}  // Capital 'D', 'A', 'C', 'B'
  allowReordering={true}
  allowResizing={true}
  showColumnMenu={true}
/>

// ❌ WRONG - Will be ignored if casing is wrong
<ColumnDirective
  isprimarykey={true}       // ALL lowercase - IGNORED
  isfrozen={true}
  allowsorting={true}       // Wrong casing - IGNORED
  displayascheckbox={true}  // Wrong casing - IGNORED
/>
```

**Common Case Errors**:
```jsx
// WRONG: These will silently fail
allowRowDragandDrop={true}  // Should be allowRowDragAndDrop (capital A, D, D)
enableInfiniteScrolling={true}  // Not enableInfiniteScrollinG
enableadaptiveUI={true}     // Not enableAdaptiveUI (capital A, U)
ShowColumnMenu={true}       // Not showColumnMenu (lowercase s)
AllowPaging={true}          // Not allowPaging (lowercase a, p)

// CORRECT: These work
allowRowDragAndDrop={true}
enableInfiniteScrolling={true}
enableAdaptiveUI={true}
showColumnMenu={true}
allowPaging={true}
```

---


## Event Communication Pattern

TreeGrid uses a three-phase event system:

1. **actionBegin** (Before) - Cancel or mutate data before action
2. **actionComplete** (After) - React after successful action
3. **actionFailure** (Error) - Handle failures

## Core Action Events

### actionBegin

**Phase**: Before action executes  
**Type**: `ActionEventArgs`  
**Purpose**: Validate, cancel, or modify data before action

```tsx
const handleActionBegin = (args: ActionEventArgs) => {
  console.log('Action Type:', args.requestType);
  
  // Cancel action conditionally
  if (args.requestType === 'delete' && !canDelete(args.data)) {
    args.cancel = true;
    toast.error('Cannot delete this item');
  }
  
  // Modify data before save
  if (args.requestType === 'save') {
    args.data.modifiedDate = new Date();
    args.data.modifiedBy = currentUser.id;
  }
};

<TreeGridComponent actionBegin={handleActionBegin} />
```

### actionComplete

**Phase**: After action completes successfully  
**Type**: `ActionEventArgs`  
**Purpose**: React to successful action, sync with server, update UI

```tsx
const handleActionComplete = (args: ActionEventArgs) => {
  if (args.requestType === 'save') {
    // Sync to server
    syncToServer(args.data)
      .then(() => toast.success('Saved successfully'))
      .catch(err => console.error(err));
  }
  
  if (args.requestType === 'delete') {
    toast.info('Item deleted');
    refreshAnalytics();
  }
  
  if (args.requestType === 'expand') {
    // Track expand events
    trackEvent('tree-node-expanded', { id: args.data.TaskID });
  }
};

<TreeGridComponent actionComplete={handleActionComplete} />
```

### actionFailure

**Phase**: When action fails  
**Type**: `FailureEventArgs`  
**Purpose**: Handle errors, show messages, rollback

```tsx
const handleActionFailure = (args: FailureEventArgs) => {
  console.error('TreeGrid Error:', args.error);
  
  if (args.error?.status === 401) {
    redirectToLogin();
  } else if (args.error?.status === 403) {
    toast.error('Permission denied');
  } else {
    toast.error(`Error: ${args.error?.message || 'Unknown error'}`);
  }
};

<TreeGridComponent actionFailure={handleActionFailure} />
```

## requestType Values

Use `args.requestType` to identify the action:

### CRUD Operations

| requestType | Trigger | Available in actionBegin | Available in actionComplete |
|-------------|---------|-------------------------|----------------------------|
| `save` | Row saved after edit | ✅ Yes (can cancel) | ✅ Yes |
| `add` | New row added | ✅ Yes (can cancel) | ✅ Yes |
| `delete` | Row deleted | ✅ Yes (can cancel) | ✅ Yes |
| `beginEdit` | Edit started | ✅ Yes (can cancel) | ✅ Yes |
| `cancel` | Edit cancelled | ❌ No | ✅ Yes |

### Tree Operations

| requestType | Trigger | Available in actionBegin | Available in actionComplete |
|-------------|---------|-------------------------|----------------------------|
| `expand` | Node expanded | ✅ Yes (can cancel) | ✅ Yes |
| `collapse` | Node collapsed | ✅ Yes (can cancel) | ✅ Yes |

### Data Operations

| requestType | Trigger | Available in actionBegin | Available in actionComplete |
|-------------|---------|-------------------------|----------------------------|
| `sorting` | Column sorted | ✅ Yes (can cancel) | ✅ Yes |
| `filtering` | Filter applied | ✅ Yes (can cancel) | ✅ Yes |
| `searching` | Search performed | ✅ Yes (can cancel) | ✅ Yes |
| `paging` | Page changed | ✅ Yes (can cancel) | ✅ Yes |
| `refresh` | Grid refreshed | ❌ No | ✅ Yes |

## Tree-Specific Events

### expanding

**Phase**: Before node expands  
**Type**: `RowExpandingEventArgs`  
**Purpose**: Lazy load children, validate before expand

```tsx
const handleExpanding = (args: RowExpandingEventArgs) => {
  const node = args.data;
  
  // Lazy load children if not already loaded
  if (!node.Children || node.Children.length === 0) {
    args.cancel = true; // Cancel default expand
    
    fetchChildren(node.TaskID).then(children => {
      node.Children = children;
      treeGridRef.current.refresh();
    });
  }
};

<TreeGridComponent expanding={handleExpanding} />
```

### expanded

**Phase**: After node expands  
**Type**: `RowExpandedEventArgs`  
**Purpose**: Track state, analytics

```tsx
const handleExpanded = (args: RowExpandedEventArgs) => {
  // Save expand state
  saveExpandState(args.data.TaskID, true);
  
  // Track analytics
  trackEvent('node-expanded', { id: args.data.TaskID });
};

<TreeGridComponent expanded={handleExpanded} />
```

### collapsing

**Phase**: Before node collapses  
**Type**: `RowCollapsingEventArgs`  
**Purpose**: Confirm unsaved changes

```tsx
const handleCollapsing = (args: RowCollapsingEventArgs) => {
  if (hasUnsavedChanges(args.data)) {
    args.cancel = true;
    showConfirmDialog('You have unsaved changes. Collapse anyway?')
      .then(confirmed => {
        if (confirmed) {
          discardChanges(args.data);
          treeGridRef.current.collapseRow(args.row);
        }
      });
  }
};

<TreeGridComponent collapsing={handleCollapsing} />
```

### collapsed

**Phase**: After node collapses  
**Type**: `RowCollapsedEventArgs`  
**Purpose**: Track state, cleanup

```tsx
const handleCollapsed = (args: RowCollapsedEventArgs) => {
  // Save collapse state
  saveExpandState(args.data.TaskID, false);
};

<TreeGridComponent collapsed={handleCollapsed} />
```

## Selection Events

### rowSelecting

**Phase**: Before row selection  
**Type**: `RowSelectingEventArgs`  
**Purpose**: Conditional selection, validation

```tsx
const handleRowSelecting = (args: RowSelectingEventArgs) => {
  // Prevent selection of certain rows
  if (args.data.isDisabled) {
    args.cancel = true;
    toast.info('This item cannot be selected');
  }
};

<TreeGridComponent rowSelecting={handleRowSelecting} />
```

### rowSelected

**Phase**: After row selected  
**Type**: `RowSelectEventArgs`  
**Purpose**: Update UI, fetch details, navigation

```tsx
const handleRowSelected = (args: RowSelectEventArgs) => {
  const selectedData = args.data;
  
  // Fetch additional details
  fetchTaskDetails(selectedData.TaskID)
    .then(details => setSelectedTaskDetails(details));
  
  // Update URL or navigate
  navigate(`/tasks/${selectedData.TaskID}`);
};

<TreeGridComponent rowSelected={handleRowSelected} />
```

### rowDeselecting / rowDeselected

Similar pattern for deselection events.

## Cell Events

### cellEdit

**Phase**: Before cell edit starts  
**Type**: `CellEditArgs`  
**Purpose**: Custom validation, conditional edit

```tsx
const handleCellEdit = (args: CellEditArgs) => {
  // Prevent editing certain cells
  if (args.columnName === 'Status' && args.rowData.isLocked) {
    args.cancel = true;
  }
};

<TreeGridComponent cellEdit={handleCellEdit} />
```

### cellSave

**Phase**: Before cell value saves  
**Type**: `CellSaveArgs`  
**Purpose**: Transform data, validate

```tsx
const handleCellSave = (args: CellSaveArgs) => {
  // Transform value before save
  if (args.columnName === 'TaskName') {
    args.value = args.value.trim().toUpperCase();
  }
  
  // Validate
  if (args.columnName === 'Duration' && args.value < 0) {
    args.cancel = true;
    toast.error('Duration cannot be negative');
  }
};

<TreeGridComponent cellSave={handleCellSave} />
```

### cellSaved

**Phase**: After cell value saved  
**Type**: `CellSaveArgs`  
**Purpose**: React to save, update related fields

```tsx
const handleCellSaved = (args: CellSaveArgs) => {
  // Update related calculations
  if (args.columnName === 'Duration') {
    recalculateEndDate(args.rowData);
  }
};

<TreeGridComponent cellSaved={handleCellSaved} />
```

## Render Events

### rowDataBound

**Phase**: During row render  
**Type**: `RowDataBoundEventArgs`  
**Purpose**: Custom row styling (NO API CALLS)

⚠️ **WARNING**: Fires on every render. Do NOT make API calls here!

```tsx
const handleRowDataBound = (args: RowDataBoundEventArgs) => {
  // ✅ CORRECT - Styling only
  if (args.data.Priority === 'High') {
    args.row.classList.add('high-priority-row');
  }
  
  // ❌ WRONG - API call will fire constantly!
  // fetch(`/api/status/${args.data.id}`).then(...); // DON'T DO THIS!
};

<TreeGridComponent rowDataBound={handleRowDataBound} />
```

### queryCellInfo

**Phase**: During cell render  
**Type**: `QueryCellInfoEventArgs`  
**Purpose**: Custom cell styling (NO API CALLS)

⚠️ **WARNING**: Fires on every cell render. Do NOT make API calls here!

```tsx
const handleQueryCellInfo = (args: QueryCellInfoEventArgs) => {
  // ✅ CORRECT - Styling based on existing data
  if (args.column.field === 'Status') {
    if (args.data.Status === 'Completed') {
      args.cell.style.backgroundColor = '#d4edda';
    } else if (args.data.Status === 'Blocked') {
      args.cell.style.backgroundColor = '#f8d7da';
    }
  }
  
  // ❌ WRONG - API call
  // fetchCellData(args.data.id).then(...); // DON'T DO THIS!
};

<TreeGridComponent queryCellInfo={handleQueryCellInfo} />
```

## Data Events

### dataSourceChanged

**Phase**: After dataSource changes  
**Type**: `DataSourceChangedEventArgs`  
**Purpose**: React to data changes

```tsx
const handleDataSourceChanged = (args: DataSourceChangedEventArgs) => {
  console.log('Data source updated');
  updateAnalytics();
};

<TreeGridComponent dataSourceChanged={handleDataSourceChanged} />
```

### dataBound

**Phase**: After data binding completes  
**Type**: `Object`  
**Purpose**: Post-render operations

```tsx
const handleDataBound = () => {
  console.log('Data binding complete');
  // Safe to perform operations after initial render
  applyCustomizations();
};

<TreeGridComponent dataBound={handleDataBound} />
```

## Complete Event Example

```tsx
import React, { useRef } from 'react';
import { TreeGridComponent, Inject, Edit, Toolbar } from '@syncfusion/ej2-react-treegrid';
import { ActionEventArgs, FailureEventArgs } from '@syncfusion/ej2-treegrid';

function TreeGridWithEvents() {
  const treeGridRef = useRef<TreeGridComponent>(null);

  const handleActionBegin = (args: ActionEventArgs) => {
    // Validation and mutation before action
    if (args.requestType === 'save') {
      if (!args.data.TaskName) {
        args.cancel = true;
        toast.error('Task name is required');
        return;
      }
      args.data.modifiedDate = new Date();
    }
    
    if (args.requestType === 'delete') {
      if (args.data.Children?.length > 0) {
        args.cancel = true;
        toast.error('Cannot delete item with children');
      }
    }
  };

  const handleActionComplete = (args: ActionEventArgs) => {
    // React after successful action
    if (args.requestType === 'save') {
      syncToServer(args.data).catch(err => {
        console.error('Sync failed:', err);
        toast.error('Failed to sync with server');
      });
    }
    
    if (args.requestType === 'delete') {
      toast.success('Item deleted successfully');
    }
  };

  const handleActionFailure = (args: FailureEventArgs) => {
    console.error('Action failed:', args.error);
    toast.error(`Error: ${args.error?.message || 'Unknown error'}`);
  };

  const handleExpanding = (args) => {
    // Lazy load children
    if (args.data.hasChildren && !args.data.Children) {
      args.cancel = true;
      fetchChildren(args.data.TaskID).then(children => {
        args.data.Children = children;
        treeGridRef.current.refresh();
      });
    }
  };

  return (
    <TreeGridComponent
      ref={treeGridRef}
      dataSource={data}
      childMapping="Children"
      treeColumnIndex={1}
      editSettings={{ allowEditing: true, allowAdding: true, allowDeleting: true }}
      toolbar={['Add', 'Edit', 'Delete', 'Update', 'Cancel']}
      actionBegin={handleActionBegin}
      actionComplete={handleActionComplete}
      actionFailure={handleActionFailure}
      expanding={handleExpanding}
    >
      <ColumnsDirective>
        <ColumnDirective field="TaskID" headerText="ID" isPrimaryKey={true} />
        <ColumnDirective field="TaskName" headerText="Task Name" />
      </ColumnsDirective>
      <Inject services={[Edit, Toolbar]} />
    </TreeGridComponent>
  );
}
```

## Best Practices

1. **Always handle actionFailure** for error recovery
2. **Use actionBegin for validation** and cancellation
3. **Use actionComplete for side effects** (API calls, notifications)
4. **Check requestType** to identify specific actions
5. **Never make API calls** in `rowDataBound` or `queryCellInfo`
6. **Use refs** for imperative operations after events
7. **Memoize event handlers** with `useCallback` for performance

