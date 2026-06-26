---
name: syncfusion-react-kanban
description: Implement Syncfusion React Kanban component for flexible task management and workflow visualization. Use this when building kanban boards, workflow stages, or card-based task management systems. This skill covers drag-and-drop card operations, swimlane organization, WIP limit validation, custom card templates, event handling, and API data binding for React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "data-visualization"
---

# Implementing Syncfusion React Kanban

A comprehensive skill for working with Syncfusion's React Kanban component to build flexible task management boards with cards, columns, swimlanes, and drag-and-drop interactions.

## When to Use This Skill

Use this skill when you need to:
- Install and set up the Kanban component with Syncfusion
- Create a basic Kanban board with columns and cards
- Organize cards in swimlanes (group by category/assignee)
- Implement drag-and-drop functionality between columns and swimlanes
- Configure card displays with headers, content, templates, and tags
- Bind data from arrays or APIs (DataManager, OData, REST)
- Handle user interactions (card selection, drag events, double-click to edit)
- Add dialogs for card creation and editing
- Customize appearance with themes, CSS, and responsive design
- Validate card counts with WIP (work-in-progress) min/max limits
- Configure sorting, filtering, and search functionality
- Apply custom tooltips, templates, and styling
- Implement virtual scrolling for large datasets
- Save board state and configuration

## Component Overview

The Kanban component provides a visual task management system with these core concepts:

**Cards**: Represent tasks or items. Each card displays a header (from a field) and content (from another field). Cards can have tags, custom templates, and be selected individually or in groups.

**Columns**: Define workflow stages (e.g., "To Do", "In Progress", "Done"). Each column has a header, can display item counts, and control drag/drop behavior independently.

**Swimlanes**: Optional horizontal grouping layers that organize cards by category (e.g., by user, priority, or team). Swimlanes help with organization and can have custom headers.

**Drag-and-Drop**: Built-in support for moving cards between columns, within columns, across swimlanes, or to external sources. Fully configurable per column.

**Data Binding**: Connect to static arrays or dynamic sources (DataManager with OData/REST APIs) for real-time updates.

**Templates**: Customize card layout, column headers, swimlane headers, tooltips, and dialogs with your own HTML/JSX.

## Documentation and Navigation Guide

Choose the reference that matches your current need:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing @syncfusion/ej2-react-kanban
- CSS theme imports (Material, Bootstrap, Fluent, Tailwind)
- Basic Kanban component setup
- Configuring dataSource and field mappings
- First working example

### Core Structure (Cards, Columns, Key Fields)
📄 **Read:** [references/core-structure.md](references/core-structure.md)
- Card properties and cardSettings configuration
- Column definition and properties
- keyField mapping (linking cards to columns)
- showHeader, showAddButton, showItemCount
- Card templates and styling options
- When to use default vs custom card layouts

### Swimlanes (Grouping Cards by Category)
📄 **Read:** [references/swimlanes.md](references/swimlanes.md)
- What swimlanes are and when to use them
- swimlaneSettings configuration
- Grouping cards by category, user, priority, or team
- Swimlane headers and custom rendering
- Nested vs flat layout variations

### Drag-and-Drop (Moving Cards and Managing Flow)
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Internal drag-and-drop (column-to-column, within columns)
- External drag-and-drop (Kanban-to-Kanban, to external sources)
- allowDragAndDrop, allowDrag, allowDrop per column
- transitionColumns to control valid transitions
- Drag event handlers and preventing drops

### Data Binding (Connecting to Data Sources)
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to static JSON arrays
- DataManager integration with OData and REST APIs
- Remote data sources and refresh patterns
- Modifying data and triggering updates
- Real-time data synchronization

### Templates and Dialogs (Custom Content and Card Editing)
📄 **Read:** [references/dialogs-and-templates.md](references/dialogs-and-templates.md)
- Card templates (custom card layout)
- Column header templates
- Swimlane header templates
- Tooltip templates and configuration
- Dialog setup for adding/editing cards
- Template syntax and event handling

### Sorting, Filtering, and Work-in-Progress (WIP) Validation
📄 **Read:** [references/sorting-filtering-and-search.md](references/sorting-filtering-and-search.md)
- Sort settings and card ordering
- Min/max card count per column (WIP limits)
- Allow sorting and searching
- Filtering and search patterns
- Selection modes (Single/Multiple)
- Handling validation errors

### Customization and Styling (Themes, Responsive, Advanced Features)
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- Built-in themes (Material, Bootstrap, Fluent, Tailwind)
- CSS customization and variables
- Responsive design behavior
- Virtual scrolling for large datasets
- Persistence (saving card state to storage)
- Localization (multi-language support)
- Accessibility (ARIA, keyboard navigation)

### Properties (Configuration and Settings)
📄 **Read:** [references/properties.md](references/properties.md)
- All configurable properties with type definitions
- cardSettings, columns, swimlaneSettings configuration
- Core properties (allowDragAndDrop, keyField, dataSource)
- Dialog settings and advanced options
- Complete configuration examples
- Decision trees for common configuration patterns

### Methods (Programmatic Control and Actions)
📄 **Read:** [references/methods.md](references/methods.md)
- Card management (addCard, updateCard, deleteCard)
- Column management (addColumn, deleteColumn, hideColumn, showColumn)
- Data access methods (getSelectedCards, getCardDetails, getColumnData, getSwimlaneData)
- UI control methods (showSpinner, hideSpinner, refreshUI, openDialog, closeDialog)
- Common programmatic patterns (bulk operations, reordering, duplication)
- Using refs to access methods from parent components

### Events (Handling User Interactions and Data Changes)
📄 **Read:** [references/events.md](references/events.md)
- Card events (cardClick, cardDoubleClick, cardRendered, cardSelectionChanging)
- Dialog events (dialogOpen, dialogClose)
- Drag-drop events (dragStart, drag, dragStop)
- Data events (dataBinding, dataBound, actionBegin, actionComplete, actionFailure)
- Lifecycle events (created)
- Event validation and prevention patterns

## Quick Start Example

Here's a minimal Kanban board with 3 columns and 5 cards:

```tsx
import React from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';
import '@syncfusion/ej2-react-kanban/styles/material.css';


export default function KanbanQuickStart(): JSX.Element {
  const kanbanData: { [key: string]: Object } = [
    { Id: '1', Status: 'Open', Summary: 'Analyze requirements' },
    { Id: '2', Status: 'Open', Summary: 'Design UI mockups' },
    { Id: '3', Status: 'InProgress', Summary: 'Implement backend API' },
    { Id: '4', Status: 'InProgress', Summary: 'Build frontend components' },
    { Id: '5', Status: 'Closed', Summary: 'Deploy to production' }
  ];

  return (
    <KanbanComponent
      dataSource={kanbanData}
      keyField="Status"
      cardSettings={{ contentField: 'Summary' }}
    >
      <ColumnsDirective>
        <ColumnDirective key="0" keyField="Open" headerText="Open" />
        <ColumnDirective key="1" keyField="InProgress" headerText="In Progress" />
        <ColumnDirective key="2" keyField="Closed" headerText="Closed" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}
```

**What this does:**
- Creates 3 workflow columns (Open, InProgress, Closed)
- Maps cards to columns using the `Status` field
- Displays 5 cards with their Summary text
- Enables drag-and-drop by default

## Common Patterns

### Pattern 1: Add Swimlanes to Group Cards by User

```tsx
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

<KanbanComponent
  dataSource={kanbanData}
  keyField="Status"
  cardSettings={{ contentField: 'Summary' }}
  swimlaneSettings={{ keyField: 'Assignee' }}
>
  <ColumnsDirective>
    <ColumnDirective keyField="Open" headerText="Open" />
    <ColumnDirective keyField="InProgress" headerText="In Progress" />
    <ColumnDirective keyField="Closed" headerText="Closed" />
  </ColumnsDirective>
</KanbanComponent>
```

Cards are now grouped horizontally by the `Assignee` field, making it easy to see each user's tasks.

### Pattern 2: Prevent Drag-Drop in Specific Columns

```tsx
import { ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

<ColumnsDirective>
  <ColumnDirective keyField="Open" headerText="Open" allowDrag={true} allowDrop={true} />
  <ColumnDirective keyField="Closed" headerText="Closed" allowDrag={false} allowDrop={false} />
</ColumnsDirective>
```

Users can drag cards into "Open", but once in "Closed", cards are locked (read-only).

### Pattern 3: Validate Card Counts with WIP Limits

```tsx
import { ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

<ColumnsDirective>
  <ColumnDirective 
    keyField="InProgress" 
    headerText="In Progress" 
    maxCount={5}
    minCount={1}
  />
</ColumnsDirective>
```

The board will warn users if column has fewer than 1 or more than 5 cards, enforcing work-in-progress limits.

### Pattern 4: Handle Card Double-Click to Edit

```tsx
import { CardClickEventArgs } from '@syncfusion/ej2-react-kanban';

const handleCardDoubleClick = (args: CardClickEventArgs): void => {
  console.log('Card clicked:', args.data);
  // Open a dialog or form to edit the card
};

<KanbanComponent
  dataSource={kanbanData}
  cardDoubleClick={handleCardDoubleClick}
>
  {/* ... */}
</KanbanComponent>
```

This pattern enables inline editing workflows.

### Pattern 5: Bind Kanban to a Remote API

```tsx
import { DataManager, UrlAdaptor } from '@syncfusion/ej2-data';

const dataManager: DataManager = new DataManager({
  url: 'https://api.example.com/tasks',
  adaptor: new UrlAdaptor()
});

<KanbanComponent
  dataSource={dataManager}
  keyField="Status"
  cardSettings={{ contentField: 'Summary' }}
>
  {/* ... */}
</KanbanComponent>
```
