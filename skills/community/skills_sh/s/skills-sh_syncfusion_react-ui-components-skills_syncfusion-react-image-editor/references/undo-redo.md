# Undo and Redo

## History Capacity

The Image Editor maintains a 16-step history. Once the limit is reached, the oldest action is removed.

## Undo Operations

### Undo Last Action

Revert the most recent edit:

```tsx
function undoLastAction(): void {
  imgObj.undo();
}
```

### Multiple Undo

Step back through history:

```tsx
function undoMultiple(steps: number): void {
  for (let i = 0; i < steps; i++) {
    imgObj.undo();
  }
}

// Undo last 3 actions
undoMultiple(3);
```

### Keyboard Shortcut

Use Ctrl+Z:

```tsx
// Built-in support - users can press Ctrl+Z
// No code needed
```

## Redo Operations

### Redo Last Undone Action

Reapply the most recently undone edit:

```tsx
function redoLastAction(): void {
  imgObj.redo();
}
```

### Multiple Redo

Step forward through history:

```tsx
function redoMultiple(steps: number): void {
  for (let i = 0; i < steps; i++) {
    imgObj.redo();
  }
}

// Redo last 2 actions
redoMultiple(2);
```

### Keyboard Shortcut

Use Ctrl+Y:

```tsx
// Built-in support - users can press Ctrl+Y
// No code needed
```

## Undo/Redo Patterns

### Toggle Between States

Switch between original and edited:

```tsx
let isUndone = false;

function toggleState(): void {
  if (isUndone) {
    imgObj.redo();
  } else {
    imgObj.undo();
  }
  isUndone = !isUndone;
}
```

### Clear History

Reset undo/redo stack:

```tsx
function clearHistory(): void {
  imgObj.reset(); // Resets to original state
}
```

### Track Edit Count

Monitor number of changes:

```tsx
let editCount = 0;

// Increment on edit operations
function editAction(): void {
  editCount++;
  console.log('Edits made:', editCount);
}

function undoAction(): void {
  if (editCount > 0) {
    editCount--;
  }
  imgObj.undo();
}
```

### Save Before Major Edit

Checkpoint system:

```tsx
let checkpointImage: ImageData;

function createCheckpoint(): void {
  checkpointImage = imgObj.getImageData();
}

function revertToCheckpoint(): void {
  // Cannot directly restore ImageData, so use undo
  // Or implement custom save/load logic
  imgObj.undo();
}
```

## Built-in Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+S | Save |
| Ctrl+O | Open |
| Delete | Delete selected annotation |
| Enter | Apply crop/resize |
| Escape | Cancel operations |

## Advanced Patterns

### Undo/Redo History Display

Show action history:

```tsx
let actionHistory: string[] = [];

function recordAction(description: string): void {
  actionHistory.push(description);
}

function displayHistory(): void {
  console.log('Edit history:');
  actionHistory.forEach((action, index) => {
    console.log(`${index + 1}. ${action}`);
  });
}

// Usage
recordAction('Rotated 90°');
recordAction('Added text "Title"');
recordAction('Applied Sepia filter');
displayHistory();
```

### Conditional Undo

Only undo specific action types:

```tsx
let lastAction: string | null = null;

function recordAndExecute(actionType: string, action: () => void): void {
  lastAction = actionType;
  action();
}

function undoIfType(type: string): void {
  if (lastAction === type) {
    imgObj.undo();
    lastAction = null;
  }
}

// Usage
recordAndExecute('text', () => {
  const dim = imgObj.getImageDimension();
  imgObj.drawText(dim.x, dim.y, 'Sample');
});

undoIfType('text'); // Only undo if last action was text
```

### Batch Undo

Undo multiple related actions as one:

```tsx
function batchEdit(): void {
  imgObj.rotate(90);
  imgObj.flip('Horizontal');
  imgObj.zoom(1.5);
}

function undoBatch(): void {
  // Need to undo 3 times
  for (let i = 0; i < 3; i++) {
    imgObj.undo();
  }
}
```

### Undo Within Limits

Prevent undoing beyond available history:

```tsx
let undoCount = 0;
const maxUndo = 16;

function safeUndo(): void {
  if (undoCount < maxUndo) {
    imgObj.undo();
    undoCount++;
  } else {
    console.log('Maximum undo reached');
  }
}
```

### Redo Validation

Check if redo is available:

```tsx
function canRedo(): boolean {
  // Image Editor doesn't expose history state directly
  // This is a conceptual pattern
  return undoCount > 0;
}

function smartRedo(): void {
  if (canRedo()) {
    imgObj.redo();
  }
}
```

### Persistent History

Save history to localStorage:

```tsx
function saveHistory(): void {
  const history = actionHistory;
  localStorage.setItem('editHistory', JSON.stringify(history));
}

function loadHistory(): void {
  const saved = localStorage.getItem('editHistory');
  if (saved) {
    actionHistory = JSON.parse(saved);
  }
}
```

### Combined Operations

Treat related edits as single unit:

```tsx
let groupedEdits: (() => void)[] = [];

function beginGroup(): void {
  groupedEdits = [];
}

function addToGroup(edit: () => void): void {
  groupedEdits.push(edit);
}

function executeGroup(): void {
  groupedEdits.forEach(edit => edit());
}

function undoGroup(): void {
  // Undo all grouped edits
  for (let i = 0; i < groupedEdits.length; i++) {
    imgObj.undo();
  }
}

// Usage
beginGroup();
addToGroup(() => imgObj.rotate(90));
addToGroup(() => imgObj.drawText(50, 50, 'Text'));
addToGroup(() => imgObj.zoom(1.5));
executeGroup();

// Single undo removes all 3
undoGroup();
```
