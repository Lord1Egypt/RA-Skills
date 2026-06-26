# Getting Started with Syncfusion React Kanban

## Table of Contents
- [Installation](#installation)
- [CSS Imports](#css-imports)
- [Basic Setup](#basic-setup)
- [Data Binding](#data-binding)
- [First Working Example](#first-working-example)
- [Troubleshooting](#troubleshooting)

## Installation

Install the Kanban component package using npm:

```bash
npm install @syncfusion/ej2-react-kanban
```

This installs the core Kanban component and its dependencies.

## CSS Imports

Import the required CSS files in your `src/App.css` or main component file. Choose the theme that matches your design:

### Tailwind Theme (Default)
```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-layouts/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-kanban/styles/tailwind3.css';
```

### Other Available Themes
- **Material**: Replace `tailwind3` with `material` in all imports
- **Bootstrap**: Replace `tailwind3` with `bootstrap` in all imports
- **Bootstrap4**: Replace `tailwind3` with `bootstrap4`
- **Fluent**: Replace `tailwind3` with `fluent`
- **High Contrast**: Replace `tailwind3` with `highcontrast`

## Basic Setup

Import the required Kanban components and create your first board:

```typescript
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";

function App() {
  return (
    <KanbanComponent id="kanban" keyField="Status">
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**What this does:**
- Creates a Kanban board with 3 workflow columns
- `keyField="Status"` tells Kanban to look for a `Status` field in your data to determine which column a card belongs to
- Each `ColumnDirective` defines a column with a header and a key value

## Data Binding

Connect your Kanban to data using the `dataSource` and `cardSettings` properties:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App(): JSX.Element {
  const data = extend([], kanbanData, null, true);

  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**Key Properties:**
- `dataSource`: Array of objects or DataManager instance containing your cards
- `keyField`: The field name that determines column mapping (e.g., "Status")
- `cardSettings.headerField`: The field displayed at the top of each card
- `cardSettings.contentField`: The field displayed in the card body

## First Working Example

Here's a complete, working example with sample data:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App(): JSX.Element {
  // Data structure: { Id: string, Status: string, Summary: string }
  const data = extend([], kanbanData, null, true);

  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**What you get:**
- A 4-column Kanban board (To Do, In Progress, Testing, Done)
- Cards distributed across columns based on Status field
- Drag-and-drop enabled by default
- Clean, responsive layout

## Enable Swimlane

Swimlanes allow you to group cards by categories (e.g., by assignee, priority, project). Enable swimlanes by mapping `swimlaneSettings.keyField` to a field in your data:

```tsx
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { extend } from '@syncfusion/ej2-base';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from "@syncfusion/ej2-react-kanban";
import { kanbanData } from './datasource';

function App(): JSX.Element {
  // Data structure: { Id: string, Status: string, Summary: string, Assignee: string }
  const data = extend([], kanbanData, null, true);

  return (
    <KanbanComponent 
      id="kanban" 
      keyField="Status" 
      dataSource={data} 
      cardSettings={{ contentField: "Summary", headerField: "Id" }} 
      swimlaneSettings={{ keyField: "Assignee" }}
    >
      <ColumnsDirective>
        <ColumnDirective headerText="To Do" keyField="Open" />
        <ColumnDirective headerText="In Progress" keyField="InProgress" />
        <ColumnDirective headerText="Testing" keyField="Testing" />
        <ColumnDirective headerText="Done" keyField="Close" />
      </ColumnsDirective>
    </KanbanComponent>
  );
}

export default App;

ReactDOM.render(<App />, document.getElementById('kanban'));
```

**Effect:** Cards are now grouped by the `Assignee` field, creating separate rows for each assignee with their tasks across all columns.

## Troubleshooting

### Cards not showing
- Verify `keyField` on `KanbanComponent` matches the field name in your data
- Ensure `cardSettings.headerField` and `contentField` point to existing fields
- Check that column `keyField` values match the data field values (e.g., "Open" in both)

### Styles not applying
- Confirm CSS imports are in correct order (base → buttons → kanban)
- Check that CSS imports use correct path from `node_modules`
- Verify theme name is consistent (material, bootstrap, etc.)

### Columns not rendering
- At least one `ColumnDirective` must be declared
- Each column must have both `headerText` and `keyField`
- `keyField` must match values in your data's `keyField` property

### Data not updating
- For static data, simply pass the array to `dataSource`
- For dynamic data, use `DataManager` (covered in data-binding.md)
- Import `extend` from `@syncfusion/ej2-base` to safely copy data without mutations
