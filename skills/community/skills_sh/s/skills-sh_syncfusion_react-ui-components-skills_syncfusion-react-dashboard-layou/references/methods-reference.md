# Dashboard Layout Methods Reference

## Table of Contents
- [Overview](#overview)
- [Panel Management Methods](#panel-management-methods)
- [Layout Manipulation Methods](#layout-manipulation-methods)
- [Serialization Methods](#serialization-methods)
- [Utility Methods](#utility-methods)
- [Common Method Patterns](#common-method-patterns)

## Overview

Dashboard Layout provides comprehensive methods for programmatic control over panels and layout. These methods enable dynamic panel management, position manipulation, and state serialization.

## Panel Management Methods

### addPanel

Allows to add a new panel to the DashboardLayout dynamically.

**Signature:**
```tsx
addPanel(panel: PanelModel): void
```

**Parameters:**
- `panel` (`PanelModel`): Defines the panel object with required properties.

**Example:**
```tsx
const dashboardRef = useRef<DashboardLayoutComponent>(null);

const handleAddPanel = () => {
  const newPanel: PanelModel = {
    id: 'panel-new',
    header: 'New Panel',
    content: 'Panel content here',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1
  };
  
  dashboardRef.current?.addPanel(newPanel);
};

<DashboardLayoutComponent 
  ref={dashboardRef}
  panels={panels}
>
</DashboardLayoutComponent>
```

### removePanel

Removes a specific panel from the DashboardLayout by its ID.

**Signature:**
```tsx
removePanel(id: string): void
```

**Parameters:**
- `id` (`string`): The panel ID to be removed.

**Example:**
```tsx
const handleRemovePanel = () => {
  dashboardRef.current?.removePanel('panel1');
};
```

### removeAll

Removes all panels from the DashboardLayout at once.

**Signature:**
```tsx
removeAll(): void
```

**Example:**
```tsx
const handleRemoveAllPanels = () => {
  dashboardRef.current?.removeAll();
};
```

### updatePanel

Allows to update an existing panel in the DashboardLayout.

**Signature:**
```tsx
updatePanel(panel: PanelModel): void
```

**Parameters:**
- `panel` (`PanelModel`): The updated panel object with the same ID.

**Example:**
```tsx
const handleUpdatePanel = () => {
  const updatedPanel: PanelModel = {
    id: 'panel1',
    header: 'Updated Header',
    content: 'Updated content',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 2
  };
  
  dashboardRef.current?.updatePanel(updatedPanel);
};
```

## Layout Manipulation Methods

### movePanel

Moves a panel to a new position in the DashboardLayout specified by row and column.

**Signature:**
```tsx
movePanel(id: string, row: number, col: number): void
```

**Parameters:**
- `id` (`string`): The panel ID to move.
- `row` (`number`): Target row position.
- `col` (`number`): Target column position.

**Example:**
```tsx
const handleMovePanel = () => {
  // Move panel1 to row 1, column 2
  dashboardRef.current?.movePanel('panel1', 1, 2);
};
```

**Use Case:** Programmatically rearrange panels based on user preferences or logic.

### resizePanel

Resizes a specific panel to new dimensions.

**Signature:**
```tsx
resizePanel(id: string, sizeX: number, sizeY: number): void
```

**Parameters:**
- `id` (`string`): The panel ID to resize.
- `sizeX` (`number`): New width in cells.
- `sizeY` (`number`): New height in cells.

**Example:**
```tsx
const handleResizePanel = () => {
  // Resize panel1 to 3 columns x 2 rows
  dashboardRef.current?.resizePanel('panel1', 3, 2);
};
```

**Use Case:** Automatically adjust panel sizes based on content or user actions.

## Serialization Methods

### serialize

Returns the current panels configuration as a `PanelModel[]` array. Useful for saving layout state.

**Signature:**
```tsx
serialize(): PanelModel[]
```

**Returns:** Array of `PanelModel` objects representing current panel configuration.

**Example:**
```tsx
const handleSaveLayout = () => {
  const currentLayout = dashboardRef.current?.serialize();
  
  // Save to localStorage
  localStorage.setItem('dashboardLayout', JSON.stringify(currentLayout));
  
  // Or send to server
  fetch('/api/save-layout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(currentLayout)
  });
};
```

**Use Case:** Persist user's custom dashboard layout for later restoration.

## Utility Methods

### refreshDraggableHandle

Updates the draggable handle when draggable panel elements are bound dynamically. Use this when you update the draggable handle CSS selector or dynamically add/remove draggable elements.

**Signature:**
```tsx
refreshDraggableHandle(): void
```

**Example:**
```tsx
const handleAddDraggableElements = () => {
  // After adding new draggable elements to panels
  dashboardRef.current?.refreshDraggableHandle();
};
```

**Use Case:** Update draggable handles after dynamic template changes.

### destroy

Destroys the DashboardLayout component and removes event listeners.

**Signature:**
```tsx
destroy(): void
```

**Example:**
```tsx
useEffect(() => {
  return () => {
    // Cleanup on unmount
    dashboardRef.current?.destroy();
  };
}, []);
```

## Common Method Patterns

### Complete Panel Lifecycle Management

```tsx
import { useRef } from 'react';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

export const DashboardManager = () => {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  // Add new panel
  const addNewPanel = () => {
    dashboardRef.current?.addPanel({
      id: `panel-${Date.now()}`,
      header: 'New Dashboard Item',
      content: '<div>Content here</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    });
  };

  // Remove specific panel
  const removeSpecificPanel = (panelId: string) => {
    dashboardRef.current?.removePanel(panelId);
  };

  // Update panel header
  const updatePanelHeader = (panelId: string, newHeader: string) => {
    const panels = dashboardRef.current?.serialize();
    const panelToUpdate = panels?.find(p => p.id === panelId);
    
    if (panelToUpdate) {
      panelToUpdate.header = newHeader;
      dashboardRef.current?.updatePanel(panelToUpdate);
    }
  };

  // Rearrange panels
  const rearrangePanels = () => {
    dashboardRef.current?.movePanel('panel1', 1, 2);
    dashboardRef.current?.movePanel('panel2', 0, 0);
  };

  // Save layout to storage
  const saveLayout = () => {
    const layout = dashboardRef.current?.serialize();
    localStorage.setItem('myDashboard', JSON.stringify(layout));
  };

  return (
    <div>
      <button onClick={addNewPanel}>Add Panel</button>
      <button onClick={() => removeSpecificPanel('panel1')}>Remove Panel 1</button>
      <button onClick={rearrangePanels}>Rearrange</button>
      <button onClick={saveLayout}>Save Layout</button>
      
      <DashboardLayoutComponent 
        ref={dashboardRef}
        columns={5}
        panels={initialPanels}
      >
      </DashboardLayoutComponent>
    </div>
  );
};
```

### Layout Save and Restore

```tsx
// Save current layout
const saveCurrentLayout = () => {
  const layout = dashboardRef.current?.serialize();
  const layoutJSON = JSON.stringify(layout, null, 2);
  
  // Download as file or save to DB
  const blob = new Blob([layoutJSON], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'dashboard-layout.json';
  link.click();
};

// Restore layout from saved state
const restoreLayout = (layoutJSON: string) => {
  const layout = JSON.parse(layoutJSON);
  dashboardRef.current?.removeAll();
  
  layout.forEach((panelConfig: PanelModel) => {
    dashboardRef.current?.addPanel(panelConfig);
  });
};
```

### Programmatic Layout Adjustment

```tsx
// Maximize a panel
const maximizePanel = (panelId: string) => {
  dashboardRef.current?.resizePanel(panelId, 5, 3);
  dashboardRef.current?.movePanel(panelId, 0, 0);
};

// Reset all panels to default size
const resetAllPanels = () => {
  const panels = dashboardRef.current?.serialize();
  panels?.forEach(panel => {
    dashboardRef.current?.resizePanel(panel.id, 2, 1);
  });
};
```
