# Chip Drag and Drop

## Table of Contents
- [Overview](#overview)
- [Enabling Drag and Drop](#enabling-drag-and-drop)
- [Restricting the Drag Area](#restricting-the-drag-area)
- [Cross-Container Drag and Drop](#cross-container-drag-and-drop)
- [Drag and Drop Events](#drag-and-drop-events)
- [Preventing Drag or Drop](#preventing-drag-or-drop)
- [Customizing the Drag Clone](#customizing-the-drag-clone)

---

## Overview

The Chips component supports drag-and-drop reordering. Users can pick up a chip and drop it at a new position within the same `ChipListComponent` or move it across multiple `ChipListComponent` containers.

A visual indicator line appears between chips during dragging to show the insertion point.

---

## Enabling Drag and Drop

Set `allowDragAndDrop={true}` on `ChipListComponent`:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="draggable-chips" allowDragAndDrop={true}>
      <ChipsDirective>
        <ChipDirective text="Report" cssClass="e-info" />
        <ChipDirective text="Meeting" cssClass="e-warning" />
        <ChipDirective text="Review" cssClass="e-warning" />
        <ChipDirective text="Budget" cssClass="e-danger" />
        <ChipDirective text="Design" cssClass="e-primary" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

- `allowDragAndDrop={true}` — enables drag-and-drop reordering within the chip list.
- Default is `false`.

---

## Restricting the Drag Area

Use `dragArea` to confine dragging within a specific container. Accepts a CSS selector string or an `HTMLElement`.

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div id="drag-boundary" style={{ border: '2px dashed #ccc', padding: '16px' }}>
      <ChipListComponent
        id="bounded-chips"
        allowDragAndDrop={true}
        dragArea="#drag-boundary"
      >
        <ChipsDirective>
          <ChipDirective text="Task A" />
          <ChipDirective text="Task B" />
          <ChipDirective text="Task C" />
        </ChipsDirective>
      </ChipListComponent>
    </div>
  );
}
export default App;
```

- `dragArea` — accepts an element ID (`"#drag-boundary"`), a CSS class (`.my-container"`), or an `HTMLElement` reference.
- By default, `dragArea` is `null` (no boundary restriction — chips can be dragged anywhere on the page).

---

## Cross-Container Drag and Drop

Enable drag and drop across multiple `ChipListComponent` instances by enabling `allowDragAndDrop` on all participating containers:

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  return (
    <div id="chip-workspace" style={{ display: 'flex', gap: '24px' }}>
      {/* Source list */}
      <div>
        <h4>To-Do</h4>
        <ChipListComponent id="todo-list" allowDragAndDrop={true}>
          <ChipsDirective>
            <ChipDirective text="Report" cssClass="e-info" />
            <ChipDirective text="Meeting" cssClass="e-warning" />
            <ChipDirective text="Review" cssClass="e-warning" />
            <ChipDirective text="Budget" cssClass="e-danger" />
            <ChipDirective text="Design" cssClass="e-primary" />
            <ChipDirective text="Presentation" cssClass="e-success" />
          </ChipsDirective>
        </ChipListComponent>
      </div>

      {/* Target list (empty, accepts drops) */}
      <div>
        <h4>Done</h4>
        <ChipListComponent id="done-list" allowDragAndDrop={true} />
      </div>
    </div>
  );
}
export default App;
```

- Both containers must have `allowDragAndDrop={true}`.
- Chips dragged from one list drop into the other seamlessly.
- The empty `ChipListComponent` acts as a drop target.

---

## Drag and Drop Events

Three events fire during the drag lifecycle:

| Event | When it fires | Use case |
|-------|--------------|----------|
| `dragStart` | User begins dragging a chip | Prevent drag for specific chips |
| `dragging` | Chip is being dragged (continuous) | Customize the drag clone appearance |
| `dragStop` | Drag operation ends (chip dropped) | Prevent drop, run post-drop logic |

```tsx
import {
  ChipListComponent,
  ChipsDirective,
  ChipDirective
} from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';

enableRipple(true);

function App() {
  function onDragStart(args: any) {
    console.log('Drag started:', args);
    // args.cancel = true; // Prevent dragging this chip
  }

  function onDragging(args: any) {
    console.log('Dragging...', args);
    // Customize clone appearance here
  }

  function onDragStop(args: any) {
    console.log('Drag stopped:', args);
    // args.cancel = true; // Prevent the drop
  }

  return (
    <ChipListComponent
      id="event-chips"
      allowDragAndDrop={true}
      dragStart={onDragStart}
      dragging={onDragging}
      dragStop={onDragStop}
    >
      <ChipsDirective>
        <ChipDirective text="Report" cssClass="e-info" />
        <ChipDirective text="Meeting" cssClass="e-warning" />
        <ChipDirective text="Review" cssClass="e-primary" />
        <ChipDirective text="Budget" cssClass="e-danger" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

Each event receives a `DragAndDropEventArgs` object.

---

## Preventing Drag or Drop

To block drag-and-drop for specific chips (e.g., locked items), use the `dragStart` or `dragStop` event and set `args.cancel = true`:

```tsx
function onDragStart(args: any) {
  // Prevent dragging chips with "e-danger" class
  if (args.element && args.element.classList.contains('e-danger')) {
    args.cancel = true;
  }
}
```

To block dropping into a specific container, use `dragStop`:

```tsx
function onDragStop(args: any) {
  // Prevent drop into the "done-list"
  if (args.droppedElement && args.droppedElement.id === 'done-list') {
    args.cancel = true;
  }
}
```

---

## Customizing the Drag Clone

During the drag, the component creates a visual clone of the chip. Use the `dragging` event to customize its appearance:

```tsx
function onDragging(args: any) {
  if (args.clonedElement) {
    args.clonedElement.style.opacity = '0.5';
    args.clonedElement.style.transform = 'rotate(3deg)';
  }
}
```
