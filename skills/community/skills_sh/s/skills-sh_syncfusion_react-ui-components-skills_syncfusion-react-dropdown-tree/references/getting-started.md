# Getting Started with Dropdown Tree

## Table of Contents

- [Dependencies](#dependencies)
- [Project Setup](#project-setup)
- [Installation](#installation)
- [Basic Implementation](#basic-implementation)
- [Styling](#styling)
- [Minimal Example](#minimal-example)

## Dependencies

The Dropdown Tree component requires the following packages:

```javascript
|-- @syncfusion/ej2-react-dropdowns
    |-- @syncfusion/ej2-base
    |-- @syncfusion/ej2-data
    |-- @syncfusion/ej2-react-base
    |-- @syncfusion/ej2-dropdowns
        |-- @syncfusion/ej2-lists
        |-- @syncfusion/ej2-inputs
        |-- @syncfusion/ej2-navigations
        |-- @syncfusion/ej2-popups
            |-- @syncfusion/ej2-buttons
```

These are automatically installed when you install the main package.

## Project Setup

### Using Vite (Recommended)

Vite provides a faster development environment and optimized builds.

**Create a new React project:**

```bash
npm create vite@latest my-app -- --template react
cd my-app
npm run dev
```

**Or with TypeScript:**

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

### Using Create React App

For traditional Create React App setup:

```bash
npx create-react-app my-app
cd my-app
npm start
```

## Installation

Install the Dropdown Tree package from npm:

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

This single command installs all required dependencies listed above.

## Basic Implementation

### Step 1: Import Components and Styles

```jsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import '@syncfusion/ej2-dropdowns/styles/material.css'; // or other themes
```

### Step 2: Prepare Data

Create your hierarchical data source:

```jsx
const treeData = [
  { id: '1', name: 'Electronics', expanded: true },
  { id: '2', name: 'Laptops', parentId: '1' },
  { id: '3', name: 'Desktops', parentId: '1' },
  { id: '4', name: 'Appliances' },
  { id: '5', name: 'Refrigerators', parentId: '4' },
];
```

### Step 3: Create the Component

```jsx
function App() {
  return (
    <DropDownTreeComponent
      id="dropdowntree"
      fields={{
        dataSource: treeData,
        value: 'id',
        text: 'name',
        parentValue: 'parentId',
        hasChildren: 'isParent'
      }}
      placeholder="Select an item"
    />
  );
}

export default App;
```

## Styling

### Available Themes

Import the appropriate theme CSS:

```jsx
// Material theme (default)
import '@syncfusion/ej2-dropdowns/styles/material.css';

// Bootstrap theme
import '@syncfusion/ej2-dropdowns/styles/bootstrap.css';

// Tailwind theme
import '@syncfusion/ej2-dropdowns/styles/tailwind.css';

// Fluent theme
import '@syncfusion/ej2-dropdowns/styles/fluent.css';
```

### Global Styles

Apply theme globally in your main CSS file or app entry:

```css
@import '@syncfusion/ej2-dropdowns/styles/material.css';
```

### Custom CSS

Override component styles with custom CSS:

```css
.e-dropdowntree .e-list-item {
  padding: 10px 15px;
  font-size: 14px;
}

.e-dropdowntree .e-input {
  border-radius: 4px;
}
```

## Minimal Example

Complete working example with TypeScript:

```tsx
import { DropDownTreeComponent } from '@syncfusion/ej2-react-dropdowns';
import '@syncfusion/ej2-dropdowns/styles/material.css';
import React from 'react';

const App: React.FC = () => {
  const hierarchicalData = [
    {
      id: '1',
      name: 'Bookstore',
      expanded: true,
    },
    {
      id: '2',
      name: 'Books',
      parentId: '1',
    },
    {
      id: '3',
      name: 'Fiction',
      parentId: '2',
    },
    {
      id: '4',
      name: 'Science Fiction',
      parentId: '3',
    },
    {
      id: '5',
      name: 'Fantasy',
      parentId: '3',
    },
    {
      id: '6',
      name: 'Non-Fiction',
      parentId: '2',
    },
    {
      id: '7',
      name: 'Biography',
      parentId: '6',
    },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Dropdown Tree - Basic Example</h2>
      <DropDownTreeComponent
        id="dropdowntree"
        fields={{
          dataSource: hierarchicalData,
          value: 'id',
          text: 'name',
          parentValue: 'parentId',
        }}
        placeholder="Select a category"
        popupHeight="250px"
      />
    </div>
  );
};

export default App;
```

### Rendering Output

The component renders as:
- An input field with dropdown icon
- Placeholder text when empty
- Selected value when item is chosen
- Popup tree when clicked

### First Interaction

1. Click the dropdown input
2. Tree expands showing all available items
3. Click an item to select it
4. Selected value displays in the input field
5. Click again to change selection

### Troubleshooting

**Component not rendering?**
- Verify `DropDownTreeComponent` import is correct
- Ensure CSS file is imported before the component
- Check that dataSource contains valid data

**Styles not applying?**
- Import CSS after component imports
- Verify theme CSS path is correct
- Check browser console for 404 errors

**Data not displaying?**
- Ensure field mapping matches your data structure
- Verify `dataSource` prop is set
- Check that value/text/parentValue field names exist in data
