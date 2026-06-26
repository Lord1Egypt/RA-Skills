# Drag-Drop and Reordering in Syncfusion React TreeView

## Table of Contents
1. [Overview](#overview)
2. [Enabling Drag and Drop](#enabling-drag-and-drop)
3. [Single-Node Drag and Drop](#single-node-drag-and-drop)
4. [Multi-Node Drag and Drop](#multi-node-drag-and-drop)
5. [Drop Indicators](#drop-indicators)
6. [Drop Validation and Prevention](#drop-validation-and-prevention)
7. [Restrict Drag and Drop](#restrict-drag-and-drop)
8. [Drag Area Property](#drag-area-property)
9. [Drag and Drop Events](#drag-and-drop-events)
10. [Preventing Drag Operations](#preventing-drag-operations)
11. [Preventing Drop Operations](#preventing-drop-operations)
12. [Custom Drag Indicators](#custom-drag-indicators)
13. [Real-World Examples](#real-world-examples)
14. [Troubleshooting](#troubleshooting)

---

## Overview

Drag and drop functionality enables intuitive reordering of tree nodes. Syncfusion React TreeView provides:
- Single and multi-node dragging
- Visual drop indicators
- Event-based validation
- Customizable drag areas
- Restriction rules per node type
- Full event lifecycle control

This feature is essential for file managers, task managers, org chart editors, and any application requiring node reorganization.

---

## Enabling Drag and Drop

### Basic Drag and Drop Setup

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Documents', parentID: '01', expanded: true },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' },
  { id: '05', name: 'Downloads', parentID: '01', expanded: true },
  { id: '06', name: 'Software.exe', parentID: '05' }
];

export default function BasicDragDropExample() {
  const treeRef = useRef(null);

  const handleNodeDropped = (args) => {
    console.log('Node dropped:', {
      draggedNode: args.draggedNode,
      dropTarget: args.dropTarget,
      position: args.position
    });
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropped={handleNodeDropped}
    />
  );
}
```

### Drag and Drop with Visual Feedback

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './drag-drop-feedback.css';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Documents', parentID: '01', expanded: true },
  { id: '03', name: 'Resume.docx', parentID: '02' },
  { id: '04', name: 'CoverLetter.docx', parentID: '02' },
  { id: '05', name: 'Downloads', parentID: '01' }
];

export default function DragDropFeedbackExample() {
  const treeRef = useRef(null);
  const [dragState, setDragState] = useState({ isDragging: false, draggedItem: null });

  const handleDragStart = (args) => {
    setDragState({
      isDragging: true,
      draggedItem: args.draggedNode?.textContent
    });
  };

  const handleDragStop = (args) => {
    setDragState({ isDragging: false, draggedItem: null });
  };

  const handleDropped = (args) => {
    console.log(`Dropped "${args.draggedNodeData?.name}" on "${args.dropTarget?.textContent}"`);
  };

  return (
    <div>
      <div className="drag-drop-status">
        {dragState.isDragging && (
          <div className="dragging-indicator">
            Dragging: {dragState.draggedItem}
          </div>
        )}
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDragStart={handleDragStart}
        nodeDragStop={handleDragStop}
        nodeDropped={handleDropped}
      />
    </div>
  );
}
```

```css
/* drag-drop-feedback.css */
.drag-drop-status {
  padding: 10px;
  margin-bottom: 10px;
}

.dragging-indicator {
  background-color: #FFF3CD;
  border-left: 4px solid #FFC107;
  padding: 10px;
  border-radius: 4px;
  color: #856404;
  font-weight: bold;
}
```

---

## Single-Node Drag and Drop

### Dragging and Dropping Individual Nodes

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Project A', expanded: true },
  { id: '02', name: 'Task 1', parentID: '01' },
  { id: '03', name: 'Task 2', parentID: '01' },
  { id: '04', name: 'Project B', expanded: true },
  { id: '05', name: 'Task 3', parentID: '04' },
  { id: '06', name: 'Task 4', parentID: '04' }
];

export default function SingleNodeDragDropExample() {
  const treeRef = useRef(null);
  const [moveHistory, setMoveHistory] = useState([]);

  const handleNodeDropped = (args) => {
    const draggedData = args.draggedNodeData;
    const dropTargetData = args.dropTarget;
    const position = args.position; // before, after, inside

    const moveRecord = {
      timestamp: new Date().toLocaleTimeString(),
      node: draggedData?.name,
      from: draggedData?.parentID,
      to: dropTargetData?.getAttribute('data-uid'),
      position: position
    };

    setMoveHistory([...moveHistory, moveRecord]);
    console.log('Move recorded:', moveRecord);
  };

  return (
    <div>
      <div className="move-history">
        <h3>Move History</h3>
        <ul>
          {moveHistory.map((move, index) => (
            <li key={index}>
              {move.node} moved {move.position} {move.to} at {move.timestamp}
            </li>
          ))}
        </ul>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

### Dragging to Specific Targets

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const taskData = [
  { id: '01', name: 'Backlog', expanded: true, type: 'status' },
  { id: '02', name: 'Task 1 - Write docs', parentID: '01' },
  { id: '03', name: 'In Progress', expanded: true, type: 'status' },
  { id: '04', name: 'Task 2 - Review PR', parentID: '03' },
  { id: '05', name: 'Done', expanded: true, type: 'status' },
  { id: '06', name: 'Task 3 - Deploy', parentID: '05' }
];

export default function TargetedDragDropExample() {
  const treeRef = useRef(null);

  const moveTaskToStatus = (taskId, statusId) => {
    // Find the node and trigger programmatic drop
    const taskNode = treeRef.current?.getNode(taskId);
    const statusNode = treeRef.current?.getNode(statusId);
    
    if (taskNode && statusNode) {
      console.log(`Moving task to status: ${statusId}`);
      // Simulate drag and drop
    }
  };

  const handleNodeDropped = (args) => {
    const targetData = args.dropTarget;
    const draggedData = args.draggedNodeData;
    const isStatusNode = taskData.find(d => d.id === targetData?.getAttribute('data-uid'))?.type === 'status';

    if (!isStatusNode) {
      args.cancel = true;
      alert('Tasks can only be moved to status containers');
    }
  };

  return (
    <div>
      <div className="quick-move">
        <button onClick={() => moveTaskToStatus('02', '03')}>
          Move Task 1 to In Progress
        </button>
        <button onClick={() => moveTaskToStatus('04', '05')}>
          Move Task 2 to Done
        </button>
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: taskData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

---

## Multi-Node Drag and Drop

### Enable Multi-Selection for Dragging

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Folder A', expanded: true },
  { id: '02', name: 'File 1', parentID: '01' },
  { id: '03', name: 'File 2', parentID: '01' },
  { id: '04', name: 'File 3', parentID: '01' },
  { id: '05', name: 'Folder B', expanded: true },
  { id: '06', name: 'File 4', parentID: '05' }
];

export default function MultiNodeDragDropExample() {
  const treeRef = useRef(null);

  const handleNodeDropped = (args) => {
    const draggedNode = args.draggedNode;
    const draggedNodeData = args.draggedNodeData;
    const dropTarget = args.dropTarget;
    const dropIndex = args.dropIndex;

    console.log('Multi-node drop:', {
      primaryNode: draggedNodeData?.name,
      targetLocation: dropTarget?.textContent,
      dropIndex: dropIndex
    });
  };

  const selectMultipleForMove = () => {
    // Select multiple nodes
    treeRef.current?.selectNodes(['02', '03', '04']);
  };

  return (
    <div>
      <button onClick={selectMultipleForMove}>Select Multiple Files</button>
      <p>Tip: Use Ctrl+Click to select multiple nodes, then drag any selected node</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        allowMultiSelection={true}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

### Batch Move Operations

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const fileData = [
  { id: '01', name: 'Current Projects', expanded: true },
  { id: '02', name: 'Project X', parentID: '01' },
  { id: '03', name: 'Project Y', parentID: '01' },
  { id: '04', name: 'Project Z', parentID: '01' },
  { id: '05', name: 'Archive', expanded: true }
];

export default function BatchMoveExample() {
  const treeRef = useRef(null);
  const [moveLog, setMoveLog] = useState([]);

  const handleNodeDropped = (args) => {
    const draggedNodeData = args.draggedNodeData;
    const targetId = args.dropTarget?.getAttribute('data-uid');
    const position = args.position;

    const logEntry = {
      item: draggedNodeData?.name,
      targetId,
      position,
      timestamp: new Date().toLocaleTimeString()
    };

    setMoveLog([...moveLog, logEntry]);
  };

  const archiveSelected = () => {
    const selected = treeRef.current?.getSelectedNodes() || [];
    console.log(`Archiving ${selected.length} items`);
    // Implement batch archive logic
  };

  return (
    <div>
      <button onClick={archiveSelected}>Archive Selected</button>
      <div className="move-log">
        <h3>Move Log</h3>
        {moveLog.map((log, i) => (
          <div key={i}>
            {log.item} → {log.position} {log.timestamp}
          </div>
        ))}
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: fileData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        allowMultiSelection={true}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

---

## Drop Indicators

### Understanding Drop Indicators

Drop indicators show where a node will be placed:
- **Plus (+)** - Drop inside (as child)
- **Minus (−)** - Drop before (as sibling above)
- **In-between line** - Drop after (as sibling below)

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './drop-indicators.css';

const data = [
  { id: '01', name: 'Parent 1', expanded: true },
  { id: '02', name: 'Child 1.1', parentID: '01' },
  { id: '03', name: 'Child 1.2', parentID: '01' },
  { id: '04', name: 'Parent 2', expanded: true },
  { id: '05', name: 'Child 2.1', parentID: '04' }
];

export default function DropIndicatorsExample() {
  const treeRef = useRef(null);

  const handleDragging = (args) => {
    const dropIndicator = args.dropIndicator;
    console.log('Drop indicator:', dropIndicator); // 'Plus', 'Minus', or null
  };

  const handleNodeDropped = (args) => {
    const position = args.position; // 'before', 'after', 'inside'
    console.log('Dropped at position:', position);
  };

  return (
    <div>
      <div className="indicator-legend">
        <h3>Drop Indicators</h3>
        <div>
          <span className="indicator plus">+</span> Drop as child (inside)
        </div>
        <div>
          <span className="indicator minus">−</span> Drop as sibling (before)
        </div>
        <div className="indicator line">Line</div> Drop as sibling (after)
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDragging={handleDragging}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

```css
/* drop-indicators.css */
.indicator-legend {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.indicator-legend div {
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  font-weight: bold;
  border-radius: 50%;
  background-color: #e3f2fd;
  color: #1976d2;
}

.indicator.plus {
  background-color: #c8e6c9;
  color: #388e3c;
}

.indicator.minus {
  background-color: #ffccbc;
  color: #e64a19;
}

.indicator.line {
  width: 100%;
  height: 2px;
  background-color: #1976d2;
}
```

### Customizing Drop Behavior

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Folder', expanded: true, type: 'folder' },
  { id: '02', name: 'SubFolder', parentID: '01', type: 'folder' },
  { id: '03', name: 'File.txt', parentID: '02', type: 'file' }
];

export default function CustomDropBehaviorExample() {
  const treeRef = useRef(null);

  const handleDragging = (args) => {
    const draggedNode = args.draggedNodeData;
    const dropTarget = args.dropTarget;

    // Only allow dropping files inside folders
    const targetNode = data.find(d => d.id === dropTarget?.getAttribute('data-uid'));
    
    if (draggedNode?.type === 'file' && targetNode?.type !== 'folder') {
      args.dropIndicator = 'None'; // Prevent drop
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDragging={handleDragging}
    />
  );
}
```

---

## Drop Validation and Prevention

### Validate Drop Operations

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Source', expanded: true },
  { id: '02', name: 'Item 1', parentID: '01' },
  { id: '03', name: 'Target', expanded: true },
  { id: '04', name: 'Item 2', parentID: '03' },
  { id: '05', name: 'Restricted', expanded: true, cannotReceive: true }
];

export default function DropValidationExample() {
  const treeRef = useRef(null);

  const canDropNode = (draggedId, targetId) => {
    const draggedNode = data.find(d => d.id === draggedId);
    const targetNode = data.find(d => d.id === targetId);

    // Cannot drop onto restricted nodes
    if (targetNode?.cannotReceive) {
      return false;
    }

    // Cannot drop node onto itself
    if (draggedId === targetId) {
      return false;
    }

    // Cannot create circular dependency
    const isAncestor = isNodeAncestorOf(draggedId, targetId);
    if (isAncestor) {
      return false;
    }

    return true;
  };

  const isNodeAncestorOf = (potentialAncestor, descendant) => {
    let current = data.find(d => d.id === descendant)?.parentID;
    while (current) {
      if (current === potentialAncestor) return true;
      current = data.find(d => d.id === current)?.parentID;
    }
    return false;
  };

  const handleNodeDropping = (args) => {
    const draggedId = args.draggedNodeData?.id;
    const targetId = args.dropTarget?.getAttribute('data-uid');

    if (!canDropNode(draggedId, targetId)) {
      args.cancel = true;
      alert('Cannot drop node at this location');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

### Prevent Drop with Confirmation

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DropConfirmationExample() {
  const treeRef = useRef(null);

  const handleNodeDropping = (args) => {
    args.cancel = true; // Temporarily cancel

    const draggedName = args.draggedNodeData?.name;
    const targetName = args.dropTarget?.textContent;

    const confirmed = window.confirm(
      `Move "${draggedName}" to "${targetName}"?`
    );

    if (confirmed) {
      // Allow the drop by not canceling
      args.cancel = false;
      console.log('Drop confirmed');
    } else {
      console.log('Drop cancelled by user');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

---

## Restrict Drag and Drop

### Prevent Specific Node Types from Being Dragged

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Root', expanded: true, draggable: false },
  { id: '02', name: 'Folder A', parentID: '01', draggable: true },
  { id: '03', name: 'System File', parentID: '02', draggable: false },
  { id: '04', name: 'User File', parentID: '02', draggable: true }
];

export default function RestrictDragExample() {
  const treeRef = useRef(null);

  const handleNodeDragStart = (args) => {
    const nodeData = args.draggedNodeData;

    if (!nodeData?.draggable) {
      args.cancel = true;
      console.log('This node cannot be dragged');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDragStart={handleNodeDragStart}
    />
  );
}
```

### Restrict Drop Targets

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Locked Folder', expanded: true, acceptDrop: false },
  { id: '02', name: 'Item 1', parentID: '01' },
  { id: '03', name: 'Public Folder', expanded: true, acceptDrop: true },
  { id: '04', name: 'Item 2', parentID: '03' }
];

export default function RestrictDropTargetExample() {
  const treeRef = useRef(null);

  const handleNodeDropping = (args) => {
    const targetData = data.find(d => d.id === args.dropTarget?.getAttribute('data-uid'));

    if (!targetData?.acceptDrop) {
      args.cancel = true;
      console.log('Cannot drop here');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

### Conditional Restrictions

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Department A', expanded: true, type: 'department' },
  { id: '02', name: 'Employee 1', parentID: '01', type: 'employee', salary: 50000 },
  { id: '03', name: 'Department B', expanded: true, type: 'department' },
  { id: '04', name: 'Manager 1', parentID: '03', type: 'manager', salary: 100000 }
];

export default function ConditionalRestrictionsExample() {
  const treeRef = useRef(null);

  const canMoveBetweenDepartments = (draggedNode, targetNode) => {
    // Managers can only move to departments
    if (draggedNode.type === 'manager' && targetNode.type !== 'department') {
      return false;
    }

    // Cannot move high-salary employees easily
    if (draggedNode.salary > 75000) {
      return confirm('Moving high-salary employee. Confirm?');
    }

    return true;
  };

  const handleNodeDropping = (args) => {
    const draggedNode = args.draggedNodeData;
    const targetNode = data.find(d => d.id === args.dropTarget?.getAttribute('data-uid'));

    if (!canMoveBetweenDepartments(draggedNode, targetNode)) {
      args.cancel = true;
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

---

## Drag Area Property

### Restrict Dragging to Specific Area

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Desktop', expanded: true },
  { id: '02', name: 'Folder A', parentID: '01' },
  { id: '03', name: 'File 1.txt', parentID: '02' }
];

export default function DragAreaExample() {
  const treeRef = useRef(null);
  const dragAreaRef = useRef(null);

  return (
    <div ref={dragAreaRef} className="drag-area" style={{ border: '2px dashed blue', padding: '10px' }}>
      <p>Dragging only works within this blue bordered area</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        dragArea={dragAreaRef.current?.getBoundingClientRect()}
      />
    </div>
  );
}
```

### Dynamic Drag Area Adjustment

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DynamicDragAreaExample() {
  const treeRef = useRef(null);
  const containerRef = useRef(null);
  const [dragEnabled, setDragEnabled] = useState(true);

  const adjustDragArea = () => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      console.log('Drag area updated:', rect);
      // Update drag area based on container size
    }
  };

  React.useEffect(() => {
    window.addEventListener('resize', adjustDragArea);
    return () => window.removeEventListener('resize', adjustDragArea);
  }, []);

  return (
    <div ref={containerRef}>
      <button onClick={() => setDragEnabled(!dragEnabled)}>
        Toggle Drag ({dragEnabled ? 'On' : 'Off'})
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowDragAndDrop={dragEnabled}
      />
    </div>
  );
}
```

---

## Drag and Drop Events

### Complete Event Lifecycle

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'Source', expanded: true },
  { id: '02', name: 'Item 1', parentID: '01' },
  { id: '03', name: 'Target', expanded: true }
];

export default function DragDropEventLifecycleExample() {
  const treeRef = useRef(null);
  const [eventLog, setEventLog] = useState([]);

  const logEvent = (eventName, details) => {
    const timestamp = new Date().toLocaleTimeString();
    setEventLog(prev => [...prev, `[${timestamp}] ${eventName}: ${details}`]);
  };

  const handleNodeDragStart = (args) => {
    logEvent('nodeDragStart', `Starting drag of "${args.draggedNodeData?.name}"`);
  };

  const handleNodeDragging = (args) => {
    logEvent('nodeDragging', `Dragging over "${args.dropTarget?.textContent}"`);
  };

  const handleNodeDragStop = (args) => {
    logEvent('nodeDragStop', 'Drag stopped');
  };

  const handleNodeDropping = (args) => {
    logEvent('nodeDropping', `Attempting to drop "${args.draggedNodeData?.name}"`);
  };

  const handleNodeDropped = (args) => {
    logEvent('nodeDropped', `Dropped at position: ${args.position}`);
  };

  return (
    <div>
      <div className="event-log" style={{ 
        height: '200px', 
        overflow: 'auto', 
        border: '1px solid #ccc', 
        padding: '10px',
        marginBottom: '10px',
        backgroundColor: '#f9f9f9'
      }}>
        {eventLog.map((event, i) => (
          <div key={i} style={{ fontSize: '12px', fontFamily: 'monospace' }}>
            {event}
          </div>
        ))}
      </div>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDragStart={handleNodeDragStart}
        nodeDragging={handleNodeDragging}
        nodeDragStop={handleNodeDragStop}
        nodeDropping={handleNodeDropping}
        nodeDropped={handleNodeDropped}
      />
    </div>
  );
}
```

### Event Arguments Reference

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function EventArgsReferenceExample() {
  const treeRef = useRef(null);

  const handleNodeDropped = (args) => {
    // Verified DragAndDropEventArgs properties
    const eventDetails = {
      // Primary properties
      draggedNode: args.draggedNode,                    // HTML element of dragged node
      draggedNodeData: args.draggedNodeData,            // Data object of dragged node
      clonedNode: args.clonedNode,                      // Clone element being dragged
      dropTarget: args.dropTarget,                      // Target node element
      dropTargetData: args.dropTargetData,              // Data object of target
      dropIndicator: args.dropIndicator,                // 'Plus', 'Minus', null
      position: args.position,                          // 'before', 'after', 'inside'
      dropIndex: args.dropIndex,                        // Index position in target
      dropLevel: args.dropLevel,                        // Nesting level of drop target
      
      // Event control
      cancel: args.cancel,                              // Cancel the drop operation
      
      // Original event reference
      target: args.target,                              // Original DOM event target
      helper: args.helper                               // Helper element during drag
    };

    console.log('Complete Event Args:', eventDetails);
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowDragAndDrop={true}
      nodeDropped={handleNodeDropped}
    />
  );
}
```

### Using Drop Index and Level

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DropIndexAndLevelExample() {
  const treeRef = useRef(null);

  const handleNodeDropped = (args) => {
    const draggedItem = args.draggedNodeData?.name;
    const position = args.position;
    const dropIndex = args.dropIndex;
    const dropLevel = args.dropLevel;
    const targetItem = args.dropTargetData?.name;

    const dropInfo = {
      item: draggedItem,
      movedTo: targetItem,
      position: position,
      indexInTarget: dropIndex,
      nestingLevel: dropLevel,
      timestamp: new Date().toISOString()
    };

    console.log('Drop Details:', dropInfo);
    
    // Save to database
    fetch('/api/move-node', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dropInfo)
    });
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowDragAndDrop={true}
      nodeDropped={handleNodeDropped}
    />
  );
}
```

---

## Preventing Drag Operations

### Cancel Drag on Specific Conditions

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const data = [
  { id: '01', name: 'System Files', expanded: true, locked: true },
  { id: '02', name: 'config.ini', parentID: '01' },
  { id: '03', name: 'User Files', expanded: true, locked: false },
  { id: '04', name: 'document.txt', parentID: '03' }
];

export default function PreventDragExample() {
  const treeRef = useRef(null);

  const handleNodeDragStart = (args) => {
    const nodeData = args.draggedNodeData;

    // Prevent dragging locked nodes
    if (nodeData?.locked) {
      args.cancel = true;
      console.log('Cannot drag locked node');
    }

    // Prevent dragging if not authorized
    const userRole = 'viewer'; // Should come from auth
    if (userRole === 'viewer') {
      args.cancel = true;
      alert('You do not have permission to drag nodes');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDragStart={handleNodeDragStart}
    />
  );
}
```

### Prevent Drag Based on Selection State

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function PreventDragSelectionExample() {
  const treeRef = useRef(null);

  const handleNodeDragStart = (args) => {
    const selectedNodes = treeRef.current?.getSelectedNodes() || [];

    // Prevent dragging if too many nodes selected
    if (selectedNodes.length > 10) {
      args.cancel = true;
      alert('Cannot drag more than 10 nodes at once');
    }

    // Prevent dragging if mixed types are selected
    const types = new Set(
      selectedNodes.map(id => {
        const node = treeRef.current?.getNode(id);
        return node?.classList.contains('folder') ? 'folder' : 'file';
      })
    );

    if (types.size > 1) {
      args.cancel = true;
      alert('Cannot drag mixed node types');
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
      allowDragAndDrop={true}
      allowMultiSelection={true}
      nodeDragStart={handleNodeDragStart}
    />
  );
}
```

---

## Preventing Drop Operations

### Detailed Drop Prevention Logic

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const hierarchyData = [
  { id: '01', name: 'Company', expanded: true, level: 0 },
  { id: '02', name: 'Department', parentID: '01', level: 1 },
  { id: '03', name: 'Team', parentID: '02', level: 2 },
  { id: '04', name: 'Member', parentID: '03', level: 3 }
];

export default function DropPreventionLogicExample() {
  const treeRef = useRef(null);

  const handleNodeDropping = (args) => {
    const draggedData = args.draggedNodeData;
    const targetData = args.dropTargetData;
    const position = args.position;

    // Prevent moving to self
    if (draggedData.id === targetData?.id) {
      args.cancel = true;
      return;
    }

    // Prevent circular hierarchy
    if (isDescendantOf(draggedData.id, targetData?.id)) {
      args.cancel = true;
      console.log('Cannot create circular hierarchy');
      return;
    }

    // Enforce hierarchy rules
    if (draggedData.level > targetData?.level && position === 'inside') {
      args.cancel = true;
      console.log('Cannot move to lower hierarchy level');
      return;
    }

    // Prevent dropping at restricted levels
    if (targetData?.level === 0 && position === 'inside') {
      args.cancel = true;
      console.log('Cannot add children to root');
      return;
    }
  };

  const isDescendantOf = (potentialAncestor, targetId) => {
    let current = hierarchyData.find(d => d.id === targetId)?.parentID;
    while (current) {
      if (current === potentialAncestor) return true;
      current = hierarchyData.find(d => d.id === current)?.parentID;
    }
    return false;
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: hierarchyData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

### Drop Prevention with Feedback

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

export default function DropPreventionFeedbackExample() {
  const treeRef = useRef(null);

  const handleNodeDropping = (args) => {
    const draggedItem = args.draggedNodeData?.name;
    const targetItem = args.dropTargetData?.name;

    // Simulate validation
    const isValid = Math.random() > 0.5; // Random for demo

    if (!isValid) {
      args.cancel = true;
      alert(`Cannot move "${draggedItem}" to "${targetItem}"`);
    }
  };

  const handleNodeDragging = (args) => {
    // Show visual feedback during drag
    const targetItem = args.dropTarget?.textContent;
    console.log('Hovering over:', targetItem);
  };

  return (
    <div>
      <p>Try dragging - random success/failure for demo</p>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: [], id: 'id', text: 'name', parentID: 'parentID' }}
        allowDragAndDrop={true}
        nodeDragging={handleNodeDragging}
        nodeDropping={handleNodeDropping}
      />
    </div>
  );
}
```

---

## Custom Drag Indicators

### Custom Visual Indicators

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './custom-indicators.css';

const data = [
  { id: '01', name: 'Project A', expanded: true },
  { id: '02', name: 'Task 1', parentID: '01' },
  { id: '03', name: 'Project B', expanded: true },
  { id: '04', name: 'Task 2', parentID: '03' }
];

export default function CustomIndicatorsExample() {
  const treeRef = useRef(null);
  const [dragIndicator, setDragIndicator] = React.useState(null);

  const handleNodeDragging = (args) => {
    const position = args.position;
    const targetNode = args.dropTarget;

    // Set custom indicator based on position
    let indicator = '→ Drop here';
    if (args.dropIndicator === 'Plus') indicator = '↓ Add as child';
    if (args.dropIndicator === 'Minus') indicator = '← Insert before';

    setDragIndicator({
      text: indicator,
      element: targetNode,
      position: position
    });

    // Add custom CSS class to target
    targetNode?.classList.add('drag-over');
  };

  const handleNodeDragStop = (args) => {
    setDragIndicator(null);
    document.querySelectorAll('.drag-over').forEach(el => {
      el.classList.remove('drag-over');
    });
  };

  return (
    <div>
      {dragIndicator && (
        <div className="custom-indicator">
          {dragIndicator.text}
        </div>
      )}
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDragging={handleNodeDragging}
        nodeDragStop={handleNodeDragStop}
      />
    </div>
  );
}
```

```css
/* custom-indicators.css */
.custom-indicator {
  position: fixed;
  padding: 8px 12px;
  background-color: #2196F3;
  color: white;
  border-radius: 4px;
  font-size: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  pointer-events: none;
  z-index: 1000;
}

.drag-over {
  background-color: #E3F2FD;
  border-left: 3px solid #2196F3;
}

.drag-over > .e-full-row {
  background-color: #BBDEFB;
}
```

---

## Real-World Examples

### Example 1: File Manager with Drag-Drop

```tsx
import React, { useRef, useState } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const fileSystemData = [
  { id: '01', name: 'My Computer', expanded: true, type: 'root' },
  { id: '02', name: 'Desktop', parentID: '01', type: 'folder', expandable: true },
  { id: '03', name: 'Desktop Item.txt', parentID: '02', type: 'file' },
  { id: '04', name: 'Documents', parentID: '01', type: 'folder', expandable: true },
  { id: '05', name: 'Resume.docx', parentID: '04', type: 'file' },
  { id: '06', name: 'Trash', parentID: '01', type: 'trash', acceptAnything: true }
];

export default function FileManagerExample() {
  const treeRef = useRef(null);
  const [actionLog, setActionLog] = useState([]);

  const logAction = (message) => {
    setActionLog(prev => [...prev, {
      time: new Date().toLocaleTimeString(),
      message
    }]);
  };

  const handleNodeDropped = (args) => {
    const draggedData = args.draggedNodeData;
    const targetData = args.dropTargetData;

    logAction(`Moved "${draggedData?.name}" to "${targetData?.name}"`);
  };

  const handleNodeDropping = (args) => {
    const draggedData = args.draggedNodeData;
    const targetData = args.dropTargetData;

    // Can't drag root
    if (draggedData?.type === 'root') {
      args.cancel = true;
      return;
    }

    // Can't drop files directly in root
    if (draggedData?.type === 'file' && targetData?.type === 'root') {
      args.cancel = true;
      return;
    }
  };

  return (
    <div style={{ display: 'flex', gap: '20px' }}>
      <div style={{ flex: 1 }}>
        <TreeViewComponent
          ref={treeRef}
          fields={{ dataSource: fileSystemData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
          allowDragAndDrop={true}
          nodeDropped={handleNodeDropped}
          nodeDropping={handleNodeDropping}
        />
      </div>
      <div style={{ flex: 1 }}>
        <h3>Action Log</h3>
        <div style={{ height: '400px', overflow: 'auto', border: '1px solid #ccc', padding: '10px' }}>
          {actionLog.map((action, i) => (
            <div key={i} style={{ marginBottom: '8px', fontSize: '12px' }}>
              <strong>{action.time}:</strong> {action.message}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### Example 2: Organization Restructuring

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const orgStructure = [
  { id: '01', name: 'Company', expanded: true, type: 'company' },
  { id: '02', name: 'Engineering', parentID: '01', type: 'department', expanded: true },
  { id: '03', name: 'Frontend Team', parentID: '02', type: 'team', expanded: true },
  { id: '04', name: 'Developer 1', parentID: '03', type: 'employee' },
  { id: '05', name: 'Backend Team', parentID: '02', type: 'team', expanded: true },
  { id: '06', name: 'Developer 2', parentID: '05', type: 'employee' },
  { id: '07', name: 'Sales', parentID: '01', type: 'department', expanded: true },
  { id: '08', name: 'Sales Rep', parentID: '07', type: 'employee' }
];

export default function OrgRestructuringExample() {
  const treeRef = useRef(null);
  const [changes, setChanges] = React.useState([]);

  const handleNodeDropped = (args) => {
    const draggedNode = args.draggedNodeData;
    const targetNode = args.dropTargetData;
    const position = args.position;

    const change = {
      item: draggedNode?.name,
      fromParent: draggedNode?.parentID,
      toParent: position === 'inside' ? targetNode?.id : targetNode?.parentID,
      position: position
    };

    setChanges([...changes, change]);
  };

  const handleNodeDropping = (args) => {
    const draggedData = args.draggedNodeData;
    const targetData = args.dropTargetData;

    // Employees can only move between teams
    if (draggedData?.type === 'employee' && targetData?.type !== 'team') {
      args.cancel = true;
    }

    // Departments cannot be moved inside teams
    if (draggedData?.type === 'department' && targetData?.type === 'team') {
      args.cancel = true;
    }
  };

  const applyChanges = () => {
    console.log('Applying changes:', changes);
    alert(`Applied ${changes.length} organizational changes`);
  };

  return (
    <div>
      <button onClick={applyChanges} disabled={changes.length === 0}>
        Apply Changes ({changes.length})
      </button>
      <TreeViewComponent
        ref={treeRef}
        fields={{ dataSource: orgStructure, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
        allowDragAndDrop={true}
        nodeDropped={handleNodeDropped}
        nodeDropping={handleNodeDropping}
      />
    </div>
  );
}
```

### Example 3: Task Reordering with Priority

```tsx
import React, { useRef } from 'react';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

const taskData = [
  { id: '01', name: 'High Priority', expanded: true, priority: 1 },
  { id: '02', name: 'Task Alpha', parentID: '01', priority: 1 },
  { id: '03', name: 'Task Beta', parentID: '01', priority: 1 },
  { id: '04', name: 'Medium Priority', expanded: true, priority: 2 },
  { id: '05', name: 'Task Gamma', parentID: '04', priority: 2 },
  { id: '06', name: 'Low Priority', expanded: true, priority: 3 },
  { id: '07', name: 'Task Delta', parentID: '06', priority: 3 }
];

export default function TaskReorderingExample() {
  const treeRef = useRef(null);

  const handleNodeDropping = (args) => {
    const draggedPriority = args.draggedNodeData?.priority;
    const targetPriority = args.dropTargetData?.priority;

    // Cannot move task to higher priority section without approval
    if (draggedPriority > targetPriority) {
      const confirmed = window.confirm(
        'Move to higher priority? This may require approval.'
      );
      if (!confirmed) {
        args.cancel = true;
      }
    }
  };

  return (
    <TreeViewComponent
      ref={treeRef}
      fields={{ dataSource: taskData, id: 'id', text: 'name', parentID: 'parentID', expanded: 'expanded' }}
      allowDragAndDrop={true}
      nodeDropping={handleNodeDropping}
    />
  );
}
```

---

## Troubleshooting

### Issue: Drag and drop not working

**Solution:** Verify `allowDragAndDrop` is enabled:

```tsx
<TreeViewComponent
  allowDragAndDrop={true}  // Must be explicitly true
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
/>
```

### Issue: Multi-node dragging not working

**Solution:** Enable both `allowDragAndDrop` and `allowMultiSelection`:

```tsx
<TreeViewComponent
  allowDragAndDrop={true}
  allowMultiSelection={true}
  fields={{ dataSource: data, id: 'id', text: 'name', parentID: 'parentID' }}
/>
```

### Issue: Drop indicator not showing

**Solution:** Check CSS and ensure `nodeDragging` event is handling indicators:

```tsx
const handleNodeDragging = (args) => {
  console.log('Drop indicator:', args.dropIndicator); // Verify value
};
```

### Issue: Programmatic validation not working

**Solution:** Ensure `args.cancel` is set before event handler returns:

```tsx
const handleNodeDropping = (args) => {
  if (shouldPreventDrop(args)) {
    args.cancel = true; // Set immediately
  }
  // Don't return early
};
```

### Issue: Drop operations not persisting

**Solution:** Implement `nodeDropped` event with backend integration:

```tsx
const handleNodeDropped = (args) => {
  // Send to server
  saveNodeMove({
    nodeId: args.draggedNodeData?.id,
    newParentId: args.dropTargetData?.id,
    position: args.position
  });
};
```

---

## Best Practices

1. **Always validate before allowing drops** - Prevents data inconsistencies
2. **Provide clear visual feedback** - Users must know drop will succeed
3. **Use `nodeDropping` for prevention** - Cancel before the operation completes
4. **Combine with multi-selection** - Enable batch operations
5. **Log drag-drop actions** - Essential for audit trails
6. **Test edge cases** - Root nodes, circular dependencies, permission conflicts
7. **Handle undo/redo** - Consider rollback capabilities
8. **Optimize for performance** - Use `dragArea` to constrain overhead
9. **Provide keyboard alternatives** - Don't rely solely on drag-drop
10. **Document restrictions clearly** - Prevent user frustration

