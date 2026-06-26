# Kanban Properties: Configuration and Settings

## Table of Contents
- [Overview](#overview)
- [Core Properties](#core-properties)
- [Card Configuration](#card-configuration)
- [Column Configuration](#column-configuration)
- [Swimlane Configuration](#swimlane-configuration)
- [Dialog Configuration](#dialog-configuration)
- [Advanced Properties](#advanced-properties)
- [Complete Configuration Example](#complete-configuration-example)

## Overview

Kanban properties control how the board behaves, appears, and processes data. Properties are set via component attributes and configure everything from drag-drop behavior to WIP limits.

## Core Properties

### allowDragAndDrop

**Type:** `boolean`  
**Default:** `true`

Enables or disables drag-and-drop functionality globally across the Kanban board.

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

<KanbanComponent
  allowDragAndDrop={true}  // Enable drag-drop
  keyField="Status"
  dataSource={data}
>
  {/* ... */}
</KanbanComponent>
```

**Use when:**
- You want to prevent users from moving cards
- You need read-only boards
- You want to lock cards until a condition is met

**Related:** `allowDrag` and `allowDrop` on individual columns provide finer control

### keyField

**Type:** `string`  
**Default:** None (REQUIRED)

Specifies the field in your data source that determines column assignment.

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

const data = [
  { Id: 1, Status: 'Open', Summary: 'Task A' },     // Status = 'Open' → Open column
  { Id: 2, Status: 'InProgress', Summary: 'Task B' } // Status = 'InProgress' → In Progress
];

<KanbanComponent keyField="Status" dataSource={data}>
  {/* ... */}
</KanbanComponent>
```

**Critical:** Must match a field name in your data objects.

### dataSource

**Type:** `DataManager |  Record[]`  
**Default:** `[]`

Provides data to populate the Kanban board. Can be a static array or DataManager for remote data.

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';
import { DataManager, ODataAdaptor } from '@syncfusion/ej2-data';

// Static array
<KanbanComponent dataSource={[
  { Id: 1, Status: 'Open', Summary: 'Task' }
]}>
  {/* ... */}
</KanbanComponent>

// Dynamic with DataManager
const dataManager: DataManager = new DataManager({
  url: 'https://api.example.com/tasks',
  adaptor: new ODataAdaptor()
});

<KanbanComponent dataSource={dataManager}>
  {/* ... */}
</KanbanComponent>
```

### allowSorting

**Type:** `boolean`  
**Default:** `false`

Allows user to click column headers to sort cards.

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

<KanbanComponent allowSorting={true} sortSettings={{ field: 'Priority' }}>
  {/* Column headers become clickable to sort */}
</KanbanComponent>
```

### allowSelection

**Type:** `boolean`  
**Default:** `true`

Enables card selection functionality (single or multiple).

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

<KanbanComponent 
  allowSelection={true}
  cardSettings={{ selectionType: 'Multiple' }}
>
  {/* Users can select cards */}
</KanbanComponent>
```

### allowKeyboard

**Type:** `boolean`  
**Default:** `true`

Enables keyboard navigation (arrow keys, Tab, Enter, Space).

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';

<KanbanComponent allowKeyboard={true}>
  {/* Users can navigate with keyboard */}
</KanbanComponent>
```

## Card Configuration

### cardSettings

**Type:** `CardSettingsModel`  

Configures how cards are displayed, including header, content, templates, and behavior.

```tsx
import { CardSettingsModel } from '@syncfusion/ej2-react-kanban';

<KanbanComponent
  cardSettings={{
    headerField: 'Id',           // Field for card header/ID
    contentField: 'Summary',     // Field for main content
    showHeader: true,            // Display card header
    selectionType: 'Single',     // Single or Multiple selection
    tagsField: 'Tags',          // Field for tags display
    grabberField: 'Priority',   // Field for left-side indicator
    footerCssField: 'Status'    // Field for footer styling
  }}
>
  {/* ... */}
</KanbanComponent>
```

**Key Sub-properties:**

| Property | Type | Purpose |
|----------|------|---------|
| `headerField` | string | Unique card identifier (required) |
| `contentField` | string | Main card text display |
| `template` | Function | Custom card JSX renderer |
| `showHeader` | boolean | Toggle header visibility |
| `selectionType` | 'Single'\|'Multiple' | Selection mode |
| `tagsField` | string | Display comma-separated tags |
| `grabberField` | string | Visual left-edge indicator field |
| `footerCssField` | string | Footer CSS class field |

### allowPrint

**Type:** `boolean`  
**Default:** `true`

Allows printing the Kanban board.

```tsx
<KanbanComponent allowPrint={true}>
  {/* Users can print the board */}
</KanbanComponent>
```

## Column Configuration

### columns

**Type:** `ColumnsModel[]`  
**Default:** `[]`

Defines all columns in the Kanban board with their properties.

```tsx
import { ColumnsModel } from '@syncfusion/ej2-react-kanban';

const columns: ColumnsModel[] = [
  { 
    headerText: 'To Do', 
    keyField: 'Open',
    showAddButton: true,
    showItemCount: true,
    maxCount: 10,
    minCount: 1
  },
  { 
    headerText: 'In Progress', 
    keyField: 'InProgress',
    allowDrag: true,
    allowDrop: true,
    maxCount: 5
  },
  { 
    headerText: 'Done', 
    keyField: 'Close',
    allowDrag: false
  }
];

<KanbanComponent columns={columns}>
  {/* ... */}
</KanbanComponent>
```

**Column Sub-properties:**

| Property | Type | Description |
|----------|------|-------------|
| `headerText` | string | Column display name |
| `keyField` | string\|number | Column key (required) |
| `allowDrag` | boolean | Allow dragging FROM this column |
| `allowDrop` | boolean | Allow dropping INTO this column |
| `allowToggle` | boolean | Allow expand/collapse |
| `isExpanded` | boolean | Initial expanded state (default: true) |
| `minCount` | number | Minimum cards required (WIP) |
| `maxCount` | number | Maximum cards allowed (WIP) |
| `showAddButton` | boolean | Show + button |
| `showItemCount` | boolean | Show card count badge |
| `template` | Function | Custom column header JSX |
| `transitionColumns` | string[] | Allowed target columns |

## Swimlane Configuration

### swimlaneSettings

**Type:** `SwimlaneSettingsModel`  

Configures swimlane grouping to organize cards horizontally by categories.

```tsx
import { SwimlaneSettingsModel } from '@syncfusion/ej2-react-kanban';

const swimlaneSettings: SwimlaneSettingsModel = {
  keyField: 'Assignee',        // Group by this field
  textField: 'AssigneeName',   // Display this field
  template: customTemplate,    // Custom swimlane header
  allowDragAndDrop: true,      // Drag across swimlanes
  showEmptyRow: true,          // Show empty swimlanes
  showItemCount: true          // Show swimlane card count
};

<KanbanComponent swimlaneSettings={swimlaneSettings}>
  {/* ... */}
</KanbanComponent>
```

**Sub-properties:**

| Property | Type | Purpose |
|----------|------|---------|
| `keyField` | string | Field to group by (required) |
| `textField` | string | Display name field (optional) |
| `template` | Function | Custom swimlane header JSX |
| `allowDragAndDrop` | boolean | Allow cross-swimlane drag |
| `showEmptyRow` | boolean | Display empty swimlanes |
| `showItemCount` | boolean | Show card counts |

## Dialog Configuration

### dialogSettings

**Type:** `DialogSettingsModel`  

Configures the dialog for adding and editing cards.

```tsx
import { DialogSettingsModel, DialogFieldsModel } from '@syncfusion/ej2-react-kanban';

const dialogSettings: DialogSettingsModel = {
  fields: [
    { text: 'Task ID', key: 'Id', type: 'TextBox' } as DialogFieldsModel,
    { text: 'Summary', key: 'Summary', type: 'TextArea' } as DialogFieldsModel,
    { text: 'Status', key: 'Status', type: 'DropDown' } as DialogFieldsModel,
    { text: 'Priority', key: 'Priority', type: 'Numeric' } as DialogFieldsModel,
    { text: 'Assignee', key: 'Assignee', type: 'DropDown' } as DialogFieldsModel
  ],
  template: customDialogTemplate  // Custom dialog JSX
};

<KanbanComponent dialogSettings={dialogSettings}>
  {/* ... */}
</KanbanComponent>
```

**Field Type Options:**
- `TextBox` - Single-line text input
- `TextArea` - Multi-line text
- `Numeric` - Number input
- `DropDown` - Select list

## Advanced Properties

### sortSettings

**Type:** `SortSettingsModel`  

Defines default card sorting behavior.

```tsx
import { SortSettingsModel } from '@syncfusion/ej2-react-kanban';

const sortSettings: SortSettingsModel = {
  field: 'Priority',
  direction: 'Descending'
};

<KanbanComponent sortSettings={sortSettings}>
  {/* Cards sorted by Priority (High → Low) */}
</KanbanComponent>
```

### constraintType

**Type:** `'Column' | 'Swimlane'`  
**Default:** `'Column'`

Specifies whether min/max constraints apply to columns or swimlanes.

```tsx
type ConstraintType = 'Column' | 'Swimlane';

<KanbanComponent constraintType="Column">
  {/* WIP limits apply per column */}
</KanbanComponent>

<KanbanComponent constraintType="Swimlane">
  {/* WIP limits apply per swimlane */}
</KanbanComponent>
```

### locale

**Type:** `string`  
**Default:** `'en-US'`

Sets the language for Kanban UI text.

```tsx
<KanbanComponent locale="es">
  {/* Spanish localization */}
</KanbanComponent>
```

**Supported locales:**
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `zh` - Chinese

### enableVirtualization

**Type:** `boolean`  
**Default:** `false`

Enables virtual rendering for large datasets (renders only visible cards).

```tsx
<KanbanComponent enableVirtualization={true}>
  {/* Efficiently handles 1000+ cards */}
</KanbanComponent>
```

### height

**Type:** `string | number`  
**Default:** `'auto'`

Sets the Kanban board height.

```tsx
<KanbanComponent height="600px">
  {/* Fixed height of 600px */}
</KanbanComponent>

<KanbanComponent height="100%">
  {/* Full parent height */}
</KanbanComponent>
```

### width

**Type:** `string | number`  
**Default:** `'100%'`

Sets the Kanban board width.

```tsx
<KanbanComponent width="1200px">
  {/* Fixed width */}
</KanbanComponent>
```