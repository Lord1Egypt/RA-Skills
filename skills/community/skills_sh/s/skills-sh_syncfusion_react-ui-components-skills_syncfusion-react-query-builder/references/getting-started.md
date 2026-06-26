# Getting Started with Query Builder

Learn how to install, set up, and create your first Query Builder component in a React application.

## Table of Contents
- [Installation](#installation)
- [CSS Setup](#css-setup)
- [Basic Component](#basic-component)
- [Column Configuration](#column-configuration)
- [Running Your App](#running-your-app)

## Installation

Install the Query Builder package and its dependencies using npm:

```bash
npm install @syncfusion/ej2-react-querybuilder --save
```

This command installs the Query Builder package into your project's `node_modules` folder and adds it to your `package.json` dependencies.

> **Note:** The `--save` flag automatically updates your `package.json` file.

## CSS Setup

The Query Builder requires CSS files for styling. Add these imports to your `src/App.css` or main CSS file:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-querybuilder/styles/tailwind3.css";
```

Then import your CSS file in your React component:

```tsx
import './App.css';
```

> **Theme Options:** Available themes include `material.css`, `bootstrap.css`, `bootstrap4.css`, `fabric.css`, `highcontrast.css`, and `tailwind3.css`. Choose the one that matches your design system.

## Basic Component

Create a simple Query Builder with basic columns in your `src/App.tsx`:

```tsx
import { ColumnsModel, QueryBuilderComponent } from '@syncfusion/ej2-react-querybuilder';
import React from 'react';
import './App.css';

function App() {
  const columnData: ColumnsModel[] = [
    { field: 'EmployeeID', label: 'EmployeeID', type: 'number' },
    { field: 'FirstName', label: 'FirstName', type: 'string' },
    { field: 'Title', label: 'Title', type: 'string' },
    { field: 'HireDate', label: 'HireDate', type: 'date', format: 'dd/MM/yyyy' },
    { field: 'Country', label: 'Country', type: 'string' }
  ];

  return (
    <QueryBuilderComponent width="100%" columns={columnData} />
  );
}

export default App;
```

This creates a Query Builder with 5 columns available for filtering:
- **EmployeeID** (number) - For numeric filtering
- **FirstName** (string) - For text filtering
- **Title** (string) - For job title filtering
- **HireDate** (date) - For date range filtering
- **Country** (string) - For location filtering

## Column Configuration

### ColumnsModel Properties

Each column in the `columns` array should have these basic properties:

| Property | Type | Description |
|----------|------|-------------|
| `field` | string | The data field name this column represents (required) |
| `label` | string | Display label shown in the UI dropdown |
| `type` | string | Data type: 'string', 'number', 'date', 'boolean' |
| `format` | string | Format pattern (e.g., 'dd/MM/yyyy' for dates) |
| `values` | string[] | Array of values for boolean or enum types |

### Complete Column Example

```tsx
const columnData: ColumnsModel[] = [
  {
    field: 'EmployeeID',
    label: 'Employee ID',
    type: 'number'
  },
  {
    field: 'FirstName',
    label: 'First Name',
    type: 'string'
  },
  {
    field: 'TitleOfCourtesy',
    label: 'Title Of Courtesy',
    type: 'boolean',
    values: ['Mr.', 'Mrs.', 'Ms.']
  },
  {
    field: 'HireDate',
    label: 'Hire Date',
    type: 'date',
    format: 'dd/MM/yyyy'
  },
  {
    field: 'Country',
    label: 'Country',
    type: 'string'
  },
  {
    field: 'City',
    label: 'City',
    type: 'string'
  }
];
```

### Auto-Generation of Columns

If you don't provide columns explicitly, the Query Builder can automatically generate them from your data source:

```tsx
import { employeeData } from './datasource';

function App() {
  return (
    <QueryBuilderComponent width="100%" dataSource={employeeData} />
  );
}
```

> **How It Works:** The component infers the column type from the first record in the data source. This is useful for quick prototyping but manual column definition is recommended for production apps.

## Running Your App

### Development Server

Start the development server using Vite or Create React App:

**With Vite:**
```bash
npm run dev
```

**With Create React App:**
```bash
npm start
```

The application opens in your browser (usually `http://localhost:5173` for Vite or `http://localhost:3000` for CRA).

### What You See

You should see a Query Builder interface with:
- A **Field** dropdown for selecting which column to filter
- An **Operator** dropdown for choosing the comparison type
- A **Value** input for entering the filter value
- **Add Rule** and **Add Group** buttons (if enabled)
- **Delete** buttons for removing conditions

### First Test

1. Open the application in your browser
2. Click the **Field** dropdown and select a column (e.g., "EmployeeID")
3. Leave the operator as "equal"
4. Enter a value (e.g., "1001")
5. Click **Add Rule** to add another condition
6. Notice the AND/OR toggle between conditions

## Next Steps

- **Configure Data:** Bind actual data using the `dataSource` property
- **Handle Changes:** Add event listeners with the `change` event
- **Extract Results:** Use `getSqlFromRules()` to get the filter as SQL
- **Customize:** Add templates and styling for your UI

For more details, see:
- [Columns and Operators](columns-and-operators.md) for advanced column configuration
- [Data Binding](data-binding.md) for connecting to data sources
- [Rules and Filtering](rules-and-filtering.md) for managing complex queries
