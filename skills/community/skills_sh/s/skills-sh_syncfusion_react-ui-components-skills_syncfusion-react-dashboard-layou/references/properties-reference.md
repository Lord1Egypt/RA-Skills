# Dashboard Layout Properties Reference

## Table of Contents
- [Overview](#overview)
- [Layout Properties](#layout-properties)
- [Interaction Properties](#interaction-properties)
- [Customization Properties](#customization-properties)
- [Advanced Properties](#advanced-properties)
- [Common Property Patterns](#common-property-patterns)

## Overview

Dashboard Layout component provides comprehensive properties to control layout behavior, grid configuration, panel interactions, and responsiveness. This reference document covers all available properties with descriptions and default values.

## Layout Properties

### columns
- **Type:** `number`
- **Default:** `1`
- **Description:** Defines the number of columns to be created in the DashboardLayout.

**Example:**
```tsx
<DashboardLayoutComponent columns={5} panels={panels}>
</DashboardLayoutComponent>
```

### cellSpacing
- **Type:** `number[]`
- **Default:** `[5, 5]`
- **Description:** Defines the spacing between the panels. Accepts horizontal and vertical spacing values.

**Example:**
```tsx
<DashboardLayoutComponent cellSpacing={[10, 10]} panels={panels}>
</DashboardLayoutComponent>
```

### cellAspectRatio
- **Type:** `number`
- **Default:** `1`
- **Description:** Defines the cell aspect ratio of the panel. Controls the height-to-width ratio of grid cells.

**Example:**
```tsx
<DashboardLayoutComponent cellAspectRatio={1.5} panels={panels}>
</DashboardLayoutComponent>
```

### panels
- **Type:** `PanelModel[]`
- **Default:** `null`
- **Description:** Defines the panels property of the DashboardLayout component. Array of panel configurations.

**Example:**
```tsx
const panels = [
  { id: 'panel1', row: 0, col: 0, sizeX: 2, sizeY: 1, header: 'Panel 1' },
  { id: 'panel2', row: 0, col: 2, sizeX: 2, sizeY: 1, header: 'Panel 2' }
];

<DashboardLayoutComponent panels={panels}>
</DashboardLayoutComponent>
```

## Interaction Properties

### allowDragging
- **Type:** `boolean`
- **Default:** `true`
- **Description:** If set to true, allows dragging and reordering of panels within the dashboard.

**Example:**
```tsx
<DashboardLayoutComponent allowDragging={true} panels={panels}>
</DashboardLayoutComponent>
```

### allowResizing
- **Type:** `boolean`
- **Default:** `false`
- **Description:** If set to true, allows resizing of panels. Must be enabled to use resize functionality.

**Example:**
```tsx
<DashboardLayoutComponent allowResizing={true} panels={panels}>
</DashboardLayoutComponent>
```

### allowFloating
- **Type:** `boolean`
- **Default:** `true`
- **Description:** If set to true, automatically moves panels upwards to fill empty cells while dragging or resizing panels. Enables smart layout optimization.

**Example:**
```tsx
<DashboardLayoutComponent allowFloating={true} panels={panels}>
</DashboardLayoutComponent>
```

### draggableHandle
- **Type:** `string`
- **Default:** `null`
- **Description:** Defines a CSS selector for the draggable handle. Only elements matching this selector can be used to drag panels.

**Example:**
```tsx
<DashboardLayoutComponent 
  draggableHandle='.e-panel-header' 
  panels={panels}
>
</DashboardLayoutComponent>
```

### resizableHandles
- **Type:** `string[]`
- **Default:** `['e-south-east']`
- **Description:** Defines the resizing handle directions. Possible values: 'e-south-east', 'e-south', 'e-east', etc.

**Example:**
```tsx
<DashboardLayoutComponent 
  resizableHandles={['e-south-east', 'e-south', 'e-east']}
  allowResizing={true}
  panels={panels}
>
</DashboardLayoutComponent>
```

## Customization Properties

### showGridLines
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enables or disables the grid lines for the Dashboard Layout panels. Useful for visual debugging and layout alignment.

**Example:**
```tsx
<DashboardLayoutComponent showGridLines={true} panels={panels}>
</DashboardLayoutComponent>
```

### enableRtl
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enable or disable rendering component in right-to-left direction for Arabic, Hebrew, and other RTL languages.

**Example:**
```tsx
<DashboardLayoutComponent enableRtl={true} panels={panels}>
</DashboardLayoutComponent>
```

### enableHtmlSanitizer
- **Type:** `boolean`
- **Default:** `true`
- **Description:** Defines whether to allow cross-scripting or sanitize HTML content. Set to false only if you trust the content source.

**Example:**
```tsx
<DashboardLayoutComponent enableHtmlSanitizer={true} panels={panels}>
</DashboardLayoutComponent>
```

## Advanced Properties

### mediaQuery
- **Type:** `string`
- **Default:** `'max-width:600px'`
- **Description:** Defines the media query value where the dashboard layout becomes a stacked layout (single column) when the resolution meets the condition.

**Example:**
```tsx
<DashboardLayoutComponent 
  mediaQuery='max-width:768px'
  columns={5}
  panels={panels}
>
</DashboardLayoutComponent>
```

**Use Case:** When screen width is less than 768px, the layout automatically stacks into a single column for mobile responsiveness.

### enablePersistence
- **Type:** `boolean`
- **Default:** `false`
- **Description:** Enable or disable persisting component's state (panel positions and sizes) between page reloads using browser localStorage.

**Example:**
```tsx
<DashboardLayoutComponent 
  enablePersistence={true}
  id='dashboardLayout'
  panels={panels}
>
</DashboardLayoutComponent>
```

**Note:** Requires a unique component ID for persistence to work correctly.

## Common Property Patterns

### Basic Grid Setup
```tsx
<DashboardLayoutComponent
  columns={5}
  cellSpacing={[5, 5]}
  panels={panels}
>
</DashboardLayoutComponent>
```

### Full Interactive Dashboard
```tsx
<DashboardLayoutComponent
  id='dashboard'
  columns={5}
  cellSpacing={[10, 10]}
  allowDragging={true}
  allowResizing={true}
  allowFloating={true}
  enablePersistence={true}
  panels={panels}
>
</DashboardLayoutComponent>
```

### Responsive Mobile-Friendly Layout
```tsx
<DashboardLayoutComponent
  columns={5}
  mediaQuery='max-width:600px'
  enableRtl={false}
  panels={panels}
>
</DashboardLayoutComponent>
```

### Styled Debug Dashboard
```tsx
<DashboardLayoutComponent
  columns={5}
  showGridLines={true}
  cellAspectRatio={1.5}
  panels={panels}
>
</DashboardLayoutComponent>
```
