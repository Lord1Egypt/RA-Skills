# Kanban Events: Handling User Interactions and Data Changes

## Table of Contents
- [Overview](#overview)
- [Card Events](#card-events)
- [Dialog Events](#dialog-events)
- [Drag-Drop Events](#drag-drop-events)
- [Data Events](#data-events)
- [Lifecycle Events](#lifecycle-events)
- [Event Patterns](#event-patterns)

## Overview

Kanban events fire in response to user actions (clicks, drags, edits) and data changes. Hook into events to implement custom workflows, validation, logging, and integrations.

**Import event types for proper TypeScript support:**

```tsx
import { 
  CardClickEventArgs, 
  DialogEventArgs, 
  DragEventArgs, 
  ActionEventArgs 
} from '@syncfusion/ej2-react-kanban';
```

**Example:**

```tsx
const handleCardClick = (args: CardClickEventArgs): void => {
  console.log('Card clicked:', args.data);
};

<KanbanComponent
  cardClick={handleCardClick}
>
  {/* ... */}
</KanbanComponent>
```

## Card Events

### cardClick

**Type:** `EmitType<CardClickEventArgs>`

Fires when user single-clicks a card.

```tsx
const handleCardClick = (args: CardClickEventArgs): void => {
  console.log('Card:', args.data.Id);
  console.log('Element:', args.element);
  console.log('Mouse event:', args.event);
  
  // Highlight card
  args.element.style.outline = '2px solid blue';
};

<KanbanComponent cardClick={handleCardClick}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:**
- `data`: Card object clicked
- `element`: DOM element of card
- `event`: MouseEvent
- `cancel`: Set to true to prevent default action
- `name`: Event name

**Use when:**
- Opening card details sidebar
- Showing card preview tooltip
- Collecting analytics

### cardDoubleClick

**Type:** `EmitType<CardClickEventArgs>`

Fires when user double-clicks a card. By default, opens the edit dialog automatically.

```tsx
import { CardClickEventArgs } from '@syncfusion/ej2-react-kanban';

const handleCardDoubleClick = (args: CardClickEventArgs): void => {
  console.log('Editing:', args.data.Summary);
  // Dialog opens automatically - no need to call openDialog()
  
  // Prevent default dialog and open custom form instead
  // args.cancel = true;
  // showCustomEditForm(args.data);
};

<KanbanComponent cardDoubleClick={handleCardDoubleClick}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:** Same as cardClick

**Important Notes:**
- The edit dialog opens **automatically** when a card is double-clicked
- To prevent the default dialog and use a custom form, set `args.cancel = true`
- Do NOT call `kanbanRef.current.openDialog()` in this event - it's redundant

**Use when:**
- Logging edit attempts
- Preventing default dialog for certain cards
- Custom edit workflows
- Conditional editing (only admins can edit)

### cardRendered

**Type:** `EmitType<CardRenderedEventArgs>`

Fires before each card renders. Allows customizing individual cards.

```tsx
const handleCardRendered = (args: CardRenderedEventArgs): void => {
  const card = args.data;
  
  // Color-code by priority
  if (card.Priority === 'Critical') {
    args.element.style.backgroundColor = '#ffebee';
    args.element.style.borderLeft = '5px solid #d32f2f';
  } else if (card.Priority === 'High') {
    args.element.style.borderLeft = '5px solid #ff9800';
  }
  
  // Add custom badge for overdue
  if (new Date(card.DueDate) < new Date()) {
    args.element.setAttribute('data-overdue', 'true');
  }
};

<KanbanComponent cardRendered={handleCardRendered}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:**
- `data`: Card object being rendered
- `element`: DOM element created
- `cancel`: Set to true to skip rendering

**Use when:**
- Applying conditional styling
- Adding badges or indicators
- Highlighting based on field values
- Custom formatting

### cardSelectionChanging

**Type:** `EmitType<CardSelectionEventArgs>`

Fires when card selection is about to change.

```tsx
const handleSelectionChanging = (args: CardSelectionEventArgs): void => {
  console.log('Selected:', args.selectedCards);
  console.log('Previous:', args.previousSelection);
  
  // Prevent deselecting the only card
  if (args.previousSelection.length === 1 && args.selectedCards.length === 0) {
    args.cancel = true;
  }
};

<KanbanComponent cardSelectionChanging={handleSelectionChanging}>
  {/* ... */}
</KanbanComponent>
```

## Dialog Events

### dialogOpen

**Type:** `EmitType<DialogEventArgs>`

Fires before the add/edit dialog opens.

```tsx
import { DialogEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDialogOpen = (args: DialogEventArgs): void => {
  console.log('Action:', args.requestType);  // 'Add' or 'Edit'
  console.log('Data:', args.data);
  
  // Prevent dialog from opening
  if (args.requestType === 'Edit' && !isUserManager()) {
    args.cancel = true;
    alert('Only managers can edit cards');
  }
  
  // Customize dialog behavior
  if (args.requestType === 'Add') {
    args.data.CreatedBy = currentUser;
    args.data.CreatedDate = new Date();
  }
};

<KanbanComponent dialogOpen={handleDialogOpen}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:**
- `data`: Card object
- `element`: Dialog element
- `requestType`: 'Add' or 'Edit'
- `cancel`: Set true to prevent opening

**Use when:**
- Validating before edit
- Pre-filling form fields
- Restricting edit access
- Custom dialog workflows

### dialogClose

**Type:** `EmitType<DialogEventArgs>`

Fires when the dialog closes (after Add/Edit completes or is cancelled).

```tsx
const handleDialogClose = (): void => {
  console.log('Dialog closed');
  
  // Refresh or sync state after dialog closes
  refreshKanbanData();
};

<KanbanComponent dialogClose={handleDialogClose}>
  {/* ... */}
</KanbanComponent>
```

**Note:** The dialog closes automatically after a successful Add or Edit action. The `requestType` ('Add' or 'Edit') is available in `dialogOpen` event, not `dialogClose`.

## Drag-Drop Events

### dragStart

**Type:** `EmitType<DragEventArgs>`

Fires when dragging a card begins.

```tsx
import { DragEventArgs } from '@syncfusion/ej2-react-kanban';

const handleDragStart = (args: DragEventArgs): void => {
  const card = args.data;
  console.log('Started dragging:', card.Id);
  
  // Prevent dragging completed items
  if (card.Status === 'Done') {
    args.cancel = true;
  }
  
  // Prevent dragging critical items without approval
  if (card.Priority === 'Critical' && !card.ApprovedBy) {
    args.cancel = true;
    alert('This item requires approval before moving');
  }
};

<KanbanComponent dragStart={handleDragStart}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:**
- `data`: Card being dragged
- `element`: Card DOM element
- `event`: Mouse/Pointer event
- `dropIndex`: Target index
- `cancel`: Set true to prevent drag

**Use when:**
- Validation before drag
- Preventing drag of certain cards
- Loggin drag events

### drag

**Type:** `EmitType<DragEventArgs>`

Fires while dragging (continuously during drag).

```tsx
const handleDrag = (args: DragEventArgs): void => {
  // Called many times during drag - keep lightweight
  console.log('Dragging...');
};

<KanbanComponent drag={handleDrag}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Creating custom drag feedback
- Calculating drop zones
- Lightweight animations

### dragStop

**Type:** `EmitType<DragEventArgs>`

Fires when drag ends (card dropped or cancelled).

```tsx
const handleDragStop = (args: DragEventArgs): void => {
  const card = args.data;
  const newStatus = card.Status;
  
  console.log(`Moved ${card.Id} to ${newStatus}`);
  
  // Prevent drop into Done without completion
  if (newStatus === 'Done' && card.CompletionPercent < 100) {
    args.cancel = true;
    alert('Complete 100% of work before moving to Done');
    return;
  }
  
  // Save to server
  fetch(`/api/tasks/${card.Id}`, {
    method: 'PUT',
    body: JSON.stringify({ Status: newStatus })
  });
};

<KanbanComponent dragStop={handleDragStop}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:** Same as dragStart

**Use when:**
- Validating drop position
- Saving status changes
- Workflow enforcement
- Audit logging

## Data Events

### dataBinding

**Type:** `EmitType<Object>`

Fires before data is bound to Kanban (initial load or refresh).

```tsx
const handleDataBinding = (): void => {
  console.log('Data binding starting...');
  // Show spinner
  kanbanRef.current.showSpinner();
};

<KanbanComponent dataBinding={handleDataBinding}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Showing loading indicator
- Pre-fetching related data
- Tracking data loads

### dataBound

**Type:** `EmitType<Object>`

Fires after data is bound and rendered.

```tsx
const handleDataBound = (): void => {
  console.log('Data binding complete');
  // Hide spinner
  kanbanRef.current.hideSpinner();
};

<KanbanComponent dataBound={handleDataBound}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Hiding loading spinner
- Post-processing rendered data
- Updating related UI

### actionBegin

**Type:** `EmitType<ActionEventArgs>`

Fires at the beginning of any action (add, edit, delete, drag).

```tsx
import { ActionEventArgs } from '@syncfusion/ej2-react-kanban';

const handleActionBegin = (args: ActionEventArgs): void => {
  const action = args.requestType;  // 'cardCreate', 'cardChange', 'cardDelete', etc.
  
  console.log('Action:', action);
  console.log('Added:', args.addedRecords);
  console.log('Changed:', args.changedRecords);
  console.log('Deleted:', args.deletedRecords);
  
  // Prevent duplicate card creation
  if (action === 'cardCreate') {
    const isDuplicate = data.some(c => c.Id === args.addedRecords[0].Id);
    if (isDuplicate) {
      args.cancel = true;
    }
  }
};

<KanbanComponent actionBegin={handleActionBegin}>
  {/* ... */}
</KanbanComponent>
```

**Event Arguments:**
- `requestType`: 'cardCreate', 'cardChange', 'cardDelete', 'cardDrop'
- `addedRecords`: New cards
- `changedRecords`: Modified cards
- `deletedRecords`: Removed cards
- `cancel`: Set true to prevent action

**Use when:**
- Validation before actions
- Preventing invalid operations
- Logging all changes

### actionComplete

**Type:** `EmitType<ActionEventArgs>`

Fires after action completes successfully.

```tsx
import { ActionEventArgs } from '@syncfusion/ej2-react-kanban';

const handleActionComplete = (args: ActionEventArgs): void => {
  const action = args.requestType;
  
  console.log(`${action} completed`);
  
  // Update related UI or refresh dependent data
  if (action === 'cardDrop') {
    refreshProjectStats();
  }
};

<KanbanComponent actionComplete={handleActionComplete}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Refreshing dependent data
- Updating UI after changes
- Success notifications

### actionFailure

**Type:** `EmitType<ActionEventArgs>`

Fires when an action fails (e.g., API call fails).

```tsx
const handleActionFailure = (args: ActionEventArgs): void => {
  console.error('Action failed:', args);
  console.error('Error:', args.error);
  
  alert('Could not save changes. Please try again.');
  
  // Revert UI if needed
  kanbanRef.current.refreshUI();
};

<KanbanComponent actionFailure={handleActionFailure}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Handling API errors
- Showing error messages
- Reverting changes on failure

### dataSourceChanged

**Type:** `EmitType<DataSourceChangedEventArgs>`

Fires on create/update/delete for DataManager-based sources.

```tsx
const handleDataSourceChanged = (args: DataSourceChangedEventArgs): void => {
  const requestType = args.requestType;
  
  if (requestType === 'save') {
    // Save to server
    setTimeout(() => {
      args.done();  // Signal completion
    }, 1000);
  }
};

<KanbanComponent dataSourceChanged={handleDataSourceChanged}>
  {/* ... */}
</KanbanComponent>
```

**Important:** Must call `args.done()` when async operation completes.

## Lifecycle Events

### created

**Type:** `EmitType<Object>`

Fires when Kanban component is fully initialized.

```tsx
const handleCreated = (): void => {
  console.log('Kanban created and ready');
  
  // Initialize custom features
  loadUserPreferences();
  applyCustomCSS();
};

<KanbanComponent created={handleCreated}>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- Setting up custom functionality
- Applying user preferences
- First-time initialization

## Event Patterns

### Pattern 1: Complete Card Validation

```tsx
const handleActionBegin = (args: ActionEventArgs): void => {
  if (args.requestType === 'cardCreate') {
    const card = args.addedRecords[0];
    
    // Validate: required fields
    if (!card.Id || !card.Summary) {
      args.cancel = true;
      alert('ID and Summary are required');
      return;
    }
    
    // Validate: summary length
    if (card.Summary.length < 5) {
      args.cancel = true;
      alert('Summary must be at least 5 characters');
      return;
    }
  }
};
```

### Pattern 2: Audit Trail

```tsx
const auditLog: any[] = [];

const handleActionBegin = (args: ActionEventArgs): void => {
  auditLog.push({
    timestamp: new Date(),
    action: args.requestType,
    userId: currentUser,
    cards: args.addedRecords || args.changedRecords || args.deletedRecords
  });
};

const handleExportAudit = (): void => {
  console.table(auditLog);
};
```

### Pattern 3: Real-Time Notification

```tsx
const handleActionComplete = (args: ActionEventArgs): void => {
  if (args.requestType === 'cardChange') {
    args.changedRecords.forEach(card => {
      notifyTeam(`Card ${card.Id} status changed to ${card.Status}`);
    });
  }
};
```

### Pattern 4: Prevent Work Overload

```tsx
const handleDragStop = (args: DragEventArgs): void => {
  const card = args.data;
  const targetColumn = card.Status;
  
  const columnCards = kanbanRef.current.getColumnData(targetColumn);
  const assigneeCards = columnCards.filter(c => 
    c.Assignee === card.Assignee
  );
  
  if (assigneeCards.length > 5) {
    args.cancel = true;
    alert(`${card.Assignee} already has 5+ items in ${targetColumn}`);
  }
};
```

### Pattern 5: Smart Edit Prevention

```tsx
const handleDialogOpen = (args: DialogEventArgs): void => {
  if (args.requestType === 'Edit') {
    const card = args.data;
    const canEdit = 
      currentUser === card.Assignee || 
      isManager(currentUser) ||
      isAdmin(currentUser);
    
    if (!canEdit) {
      args.cancel = true;
      alert('You can only edit tasks assigned to you');
    }
  }
};
```
