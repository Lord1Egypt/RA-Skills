# Kanban Methods: Programmatic Control and Actions

## Table of Contents
- [Overview](#overview)
- [Card Management Methods](#card-management-methods)
- [Column Management Methods](#column-management-methods)
- [Data Access Methods](#data-access-methods)
- [UI Control Methods](#ui-control-methods)
- [Dialog Methods](#dialog-methods)
- [Common Patterns](#common-patterns)

## Overview

Kanban methods allow you to programmatically control the board, manage cards and columns, access data, and manipulate the UI. Access methods via a ref to the KanbanComponent.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

// Later in code:
kanbanRef.current?.addCard(newCard);
kanbanRef.current?.deleteColumn(0);
```

## Card Management Methods

### addCard()

**Signature:** `addCard(cardData: Record | Record[], index?: number): void`

Adds one or more cards to the Kanban board and data source.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// Card shape: { Id, Status, Summary, Priority? }
const kanbanRef = useRef<KanbanComponent>(null);

const handleAddCard = (): void => {
  const newCard = {
    Id: 'TASK-100',
    Status: 'Open',
    Summary: 'New task',
    Priority: 'High'
  };
  
  kanbanRef.current?.addCard(newCard);
};

// Add multiple cards
const handleAddMultiple = (): void => {
  const cards = [
    { Id: 'T1', Status: 'Open', Summary: 'Task 1' },
    { Id: 'T2', Status: 'Open', Summary: 'Task 2' }
  ];
  
  kanbanRef.current?.addCard(cards);
};
```

**Parameters:**
- `cardData` (required): Single card object or array of cards
- `index` (optional): Position in column to insert

**Returns:** `void`

**Use when:**
- User submits a form to create a new task
- Importing cards from CSV/API
- Programmatically populating the board

### updateCard()

**Signature:** `updateCard(cardData: Record | Record[], index?: number): void`

Updates existing cards with new values.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// Card shape: { Id, Status, Summary, Priority? }
const kanbanRef = useRef<KanbanComponent>(null);

const handleUpdateCard = (cardId: string, newValues: Record<string, any>): void => {
  const cardToUpdate: KanbanCard = {
    Id: cardId,
    Status: 'InProgress',
    Summary: 'Updated task'
  };
  
  kanbanRef.current?.updateCard(cardToUpdate);
};

// Update multiple cards at once
const handleBulkUpdate = (): void => {
  const updates: Partial<KanbanCard>[] = [
    { Id: 'T1', Priority: 'High' } as KanbanCard,
    { Id: 'T2', Priority: 'Critical' } as KanbanCard
  ];
  
  kanbanRef.current?.updateCard(updates);
};
```

**Parameters:**
- `cardData`: Card to update (must include original ID/headerField)
- `index` (optional): Position to move card

**Returns:** `void`

**Important:** Changes made to card objects directly may not update the UI. Always use `updateCard()` to ensure proper refresh.

### deleteCard()

**Signature:** `deleteCard(cardData: string | number | Record | Record[]): void`

Removes one or more cards from the Kanban and data source.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

interface KanbanCard {
  Id: string;
  [key: string]: any;
}

const kanbanRef = useRef<KanbanComponent>(null);

const handleDeleteCard = (cardId: string): void => {
  // Delete by ID
  kanbanRef.current?.deleteCard(cardId);
};

// Delete by card object
const handleDeleteByObject = (card: any): void => {
  kanbanRef.current?.deleteCard(card);
};

// Delete multiple cards
const handleBulkDelete = (): void => {
  const cardIds = ['T1', 'T2', 'T3'];
  cardIds.forEach(id => kanbanRef.current?.deleteCard(id));
};

// Delete selected cards
const handleDeleteSelected = (): void => {
  const selected = kanbanRef.current?.getSelectedCards() || [];
  selected.forEach(element => {
    const cardData = kanbanRef.current?.getCardDetails(element);
    if (cardData) {
      kanbanRef.current?.deleteCard(cardData);
    }
  });
};
```

**Parameters:**
- `cardData`: Card ID (string/number) or card object(s)

**Returns:** `void`

**Use when:**
- User clicks delete button on a card
- Archiving completed tasks
- Bulk removal of cards

## Column Management Methods

### addColumn()

**Signature:** `addColumn(columnOptions: ColumnsModel, index: number): void`

Dynamically adds a new column to the Kanban board.

```tsx
import { useRef } from 'react';
import { KanbanComponent, ColumnsModel } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleAddColumn = (): void => {
  const newColumn: ColumnsModel = {
    headerText: 'Blocked',
    keyField: 'Blocked',
    maxCount: 5,
    showItemCount: true
  };
  
  // Add at position 2 (0-indexed)
  kanbanRef.current?.addColumn(newColumn, 2);
};

// Add column at end
const handleAddAtEnd = (newColumn: ColumnsModel): void => {
  kanbanRef.current?.addColumn(newColumn, 999);
};
```

**Parameters:**
- `columnOptions` (required): Column configuration object
- `index` (required): Position to insert column

**Returns:** `void`

**ColumnsModel properties:**
```ts
{
  headerText?: string;
  keyField: string | number;  // Required
  template?: Function;
  allowToggle?: boolean;
  isExpanded?: boolean;
  minCount?: number;
  maxCount?: number;
  showAddButton?: boolean;
  showItemCount?: boolean;
  allowDrag?: boolean;
  allowDrop?: boolean;
  transitionColumns?: string[];
}
```

### deleteColumn()

**Signature:** `deleteColumn(index: number): void`

Removes a column from the Kanban board.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleDeleteColumn = (columnIndex: number): void => {
  kanbanRef.current?.deleteColumn(columnIndex);
};

// Delete first column
handleDeleteColumn(0);

// Delete last column (if 4 columns total)
handleDeleteColumn(3);
```

**Parameters:**
- `index` (required): Position of column to delete (0-indexed)

**Returns:** `void`

**Warning:** Cards in deleted column are preserved in data but become invisible. Consider using `hideColumn()` for temporary hiding.

### hideColumn()

**Signature:** `hideColumn(key: string | number): void`

Hides a column without deleting it or its cards.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleHideColumn = (): void => {
  // Hide by keyField value
  kanbanRef.current?.hideColumn('OnHold');
};
```

**Parameters:**
- `key`: Column's keyField value

**Returns:** `void`

**Use when:**
- User unchecks column visibility in settings
- Temporarily filtering out certain statuses
- Keeping data but hiding from view

### showColumn()

**Signature:** `showColumn(key: string | number): void`

Unhides a previously hidden column.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleShowColumn = (): void => {
  kanbanRef.current?.showColumn('OnHold');
};
```

**Parameters:**
- `key`: Column's keyField value

**Returns:** `void`

## Data Access Methods

### getSelectedCards()

**Signature:** `getSelectedCards(): HTMLElement[]`

Returns array of DOM elements of currently selected cards.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

// Card data shape: { [key: string]: any }
const kanbanRef = useRef<KanbanComponent>(null);

const handleGetSelected = (): void => {
  const selectedElements = kanbanRef.current?.getSelectedCards() || [];
  
  selectedElements.forEach((element: HTMLElement) => {
    const cardData = kanbanRef.current?.getCardDetail(element);
    console.log('Selected:', cardData);
  });
};

// Count selected cards
const selectedCount = (kanbanRef.current?.getSelectedCards() || []).length;
```

**Parameters:** None

**Returns:** `HTMLElement[]`

**Use when:**
- Implementing bulk actions
- Showing count of selected items
- Preparing batch operations

### getCardDetails()

**Signature:** `getCardDetails(target: Element): Record`

Gets card data object from a DOM element.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

interface KanbanCard {
  Id: string;
  Status: string;
  [key: string]: any;
}

const kanbanRef = useRef<KanbanComponent>(null);

const handleCardClick = (element: HTMLElement): void => {
  const cardData = kanbanRef.current?.getCardDetail(element) as any;
  console.log('Card ID:', cardData.Id);
  console.log('Status:', cardData.Status);
};

// Get details of selected card
const selected = kanbanRef.current?.getSelectedCards() || [];
if (selected.length > 0) {
  const data = kanbanRef.current?.getCardDetail(selected[0]) as any;
}
```

**Parameters:**
- `target`: DOM element of the card (usually from event)

**Returns:** `Record` - Original card data object

### getColumnData()

**Signature:** `getColumnData(columnKey: string | number, dataSource?: Record[]): Record[]`

Returns all cards in a specific column.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

interface KanbanCard {
  Id: string;
  Status: string;
  [key: string]: any;
}

const kanbanRef = useRef<KanbanComponent>(null);

const handleGetColumnCards = (): void => {
  // Get all cards in 'InProgress' column
  const inProgressCards = kanbanRef.current?.getColumnData('InProgress') || [];
  console.log('In Progress cards:', inProgressCards);
  console.log('Count:', inProgressCards.length);
};

// Use with custom data source
const customData: any[] = [...];
const customColumnCards = kanbanRef.current?.getColumnData('Open', customData) || [];
```

**Parameters:**
- `columnKey` (required): Column's keyField value
- `dataSource` (optional): Custom array (uses component's data if not provided)

**Returns:** `Record[]` - Array of cards in that column

**Use when:**
- Calculating column metrics
- Filtering cards by status
- Preparing data for export

### getSwimlaneData()

**Signature:** `getSwimlaneData(keyField: string): Record[]`

Returns all cards in a specific swimlane.

```jsx
const handleGetSwimlaneCards = () => {
  // Get all cards assigned to Sarah
  const sarahCards = kanbanRef.current.getSwimlaneData('Sarah');
  console.log("Sarah's cards:", sarahCards);
  console.log("Workload:", sarahCards.length);
};

// Calculate total effort in swimlane
const swimlaneCards = kanbanRef.current.getSwimlaneData('John');
const totalEffort = swimlaneCards.reduce((sum, card) => 
  sum + (card.EstimateHours || 0), 0
);
console.log('Total effort:', totalEffort, 'hours');
```

**Parameters:**
- `keyField` (required): Swimlane key value

**Returns:** `Record[]` - Array of cards in swimlane

## UI Control Methods

### showSpinner()

**Signature:** `showSpinner(): void`

Displays a loading spinner on the Kanban board.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

const handleSaveToServer = async (): Promise<void> => {
  kanbanRef.current?.showSpinner();
  
  try {
    await fetch('/api/save', { method: 'POST', body: JSON.stringify(data) });
  } finally {
    kanbanRef.current?.hideSpinner();
  }
};
```

**Parameters:** None

**Returns:** `void`

**Use when:**
- Loading data from server
- Saving bulk changes
- Long-running operations

### hideSpinner()

**Signature:** `hideSpinner(): void`

Hides the loading spinner.

```tsx
import { useRef } from 'react';
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const kanbanRef = useRef<KanbanComponent>(null);

// See showSpinner() example above
kanbanRef.current?.hideSpinner();
```

**Parameters:** None

**Returns:** `void`

### refreshUI()

**Signature:** `refreshUI(args: ActionEventArgs, index?: number): void`

Refreshes the Kanban UI after making data changes programmatically.

```jsx
const handleRefreshUI = () => {
  const updates = {
    addedRecords: [newCard1, newCard2],
    changedRecords: [updatedCard],
    deletedRecords: [deletedCard]
  };
  
  kanbanRef.current.refreshUI(updates);
};
```

**Parameters:**
- `args`: ActionEventArgs object with added/changed/deleted records
- `index` (optional): Specific card index to refresh

**Returns:** `void`

### refreshHeader()

**Signature:** `refreshHeader(): void`

Refreshes only the column headers (useful after changing header templates).

```jsx
const handleUpdateHeaders = () => {
  kanbanRef.current.refreshHeader();
};
```

**Parameters:** None

**Returns:** `void`

### destroy()

**Signature:** `destroy(): void`

Completely removes the Kanban component from the DOM and detaches all event handlers.

```jsx
useEffect(() => {
  return () => {
    // Cleanup on unmount
    kanbanRef.current.destroy();
  };
}, []);
```

**Parameters:** None

**Returns:** `void`

**Use when:**
- Component unmounts
- Recycling DOM for large lists

## Dialog Methods

### openDialog()

**Signature:** `openDialog(action: 'Add' | 'Edit', data?: Record): void`

Manually opens the card creation or editing dialog.

```jsx
const handleOpenAddDialog = () => {
  kanbanRef.current.openDialog('Add');
};

const handleOpenEditDialog = (cardData) => {
  kanbanRef.current.openDialog('Edit', cardData);
};

// From button click
const handleEditButton = (element) => {
  const cardData = kanbanRef.current.getCardDetails(element);
  kanbanRef.current.openDialog('Edit', cardData);
};
```

**Parameters:**
- `action` (required): 'Add' or 'Edit'
- `data` (optional): Card data to edit

**Returns:** `void`

### closeDialog()

**Signature:** `closeDialog(): void`

Manually closes the dialog.

```jsx
const handleCloseDialog = () => {
  kanbanRef.current.closeDialog();
};
```

**Parameters:** None

**Returns:** `void`

## Common Patterns

### Pattern 1: Build Custom Card Duplication

```jsx
const handleDuplicateCard = (cardElement) => {
  const original = kanbanRef.current.getCardDetails(cardElement);
  
  const duplicate = {
    ...original,
    Id: `${original.Id}-copy`,
    Summary: `${original.Summary} (Copy)`
  };
  
  kanbanRef.current.addCard(duplicate);
};
```

### Pattern 2: Bulk Update on Drag

```jsx
const handleBulkStatusUpdate = (status) => {
  const selected = kanbanRef.current.getSelectedCards();
  
  selected.forEach(element => {
    const card = kanbanRef.current.getCardDetails(element);
    card.Status = status;
    kanbanRef.current.updateCard(card);
  });
};
```

### Pattern 3: Archive Old Cards

```jsx
const handleArchiveOldCards = () => {
  const allCards = kanbanRef.current.getColumnData('Done');
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - 30);
  
  const oldCards = allCards.filter(card => 
    new Date(card.CompletedDate) < cutoffDate
  );
  
  oldCards.forEach(card => kanbanRef.current.deleteCard(card.Id));
  console.log(`Archived ${oldCards.length} cards`);
};
```

### Pattern 4: Reorder Cards in Column

```jsx
const handlePrioritizeCard = (cardElement) => {
  const card = kanbanRef.current.getCardDetails(cardElement);
  kanbanRef.current.deleteCard(card.Id);
  kanbanRef.current.addCard(card, 0);  // Move to top
};
```

### Pattern 5: Export Column Data

```jsx
const handleExportColumn = (columnKey) => {
  const cards = kanbanRef.current.getColumnData(columnKey);
  const csv = cards.map(c => `${c.Id},${c.Summary},${c.Status}`).join('\n');
  
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${columnKey}-export.csv`;
  a.click();
};
```
