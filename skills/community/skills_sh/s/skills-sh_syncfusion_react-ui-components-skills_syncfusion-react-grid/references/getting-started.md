# Getting Started with React Grid

## Table of Contents
- [Installation](#installation)
- [Setup for Local Development](#setup-for-local-development)
- [Adding Syncfusion React Grid Packages](#adding-syncfusion-react-grid-packages)
- [CSS References](#css-references)
- [Basic Grid Setup](#basic-grid-setup)
- [Module Injection](#module-injection)
- [First Grid Example](#first-grid-example)

## Installation

The Syncfusion React Grid is available through the npm package registry. Before installation, ensure you have Node.js and npm installed on your machine.

### Install via npm

```bash
npm install @syncfusion/ej2-react-grids --save
```

The `--save` flag adds the package to your project's `package.json` dependencies.

### Verify Installation

After installation, verify that the package is included in your `package.json`:

```json
{
  "dependencies": {
    "@syncfusion/ej2-react-grids": "latest"
  }
}
```

## Setup for Local Development

### Using Vite (Recommended)

Vite provides faster development environments with smaller bundle sizes compared to traditional tools.

```bash
npm create vite@latest my-grid-app -- --template react-ts
cd my-grid-app
npm run dev
```

### Using Create React App

For traditional React app setup:

```bash
npx create-react-app my-grid-app
cd my-grid-app
npm install @syncfusion/ej2-react-grids
```

### Using Next.js

For Next.js projects:

```bash
npx create-next-app@latest my-grid-app
cd my-grid-app
npm install @syncfusion/ej2-react-grids
```

## Adding Syncfusion React Grid Packages

Install the grid package along with required dependencies:

```bash
npm install @syncfusion/ej2-react-grids @syncfusion/ej2-base --save
```

## CSS References

> **CSS Quick Reference:** Always import **all** required Syncfusion CSS files in your `App.css` (or equivalent). Each feature depends on a specific package's CSS:
> - **Pager** (page number buttons, navigation) → `@syncfusion/ej2-react-grids/styles/material3.css` — **missing this is the most common cause of unstyled pagers**
> - **Toolbar** → `@syncfusion/ej2-navigations/styles/material3.css`
> - **Filter/Edit inputs** → `@syncfusion/ej2-inputs/styles/material3.css`
> - **Dialog editing, filter menus** → `@syncfusion/ej2-popups/styles/material3.css`

The Grid component requires CSS files for styling. Add the following imports to your main CSS file or App component:

### Material 3 Theme (Default)

```css
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-calendars/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';  
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-notifications/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-react-grids/styles/material3.css';
```

Import CSS in your App.tsx:

```tsx
import './App.css';
```

### Other Available Themes

- Bootstrap: `bootstrap.css`
- Fabric: `fabric.css`
- Bootstrap 5: `bootstrap5.css`
- Material: `material.css`
- Tailwind CSS: `tailwind.css`

## Basic Grid Setup

### Minimal Grid Component

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';
import React from 'react';

const data = [
  { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
  { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 },
  { OrderID: 10250, CustomerID: 'HANAR', Freight: 65.83 }
];

function App() {
  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default App;
```

### Key Components

- **GridComponent**: The main container for the data grid
- **ColumnsDirective**: Container for all column definitions
- **ColumnDirective**: Individual column configuration

## Module Injection

React Grid features are modular and require injection to enable them. This reduces bundle size by loading only needed features.

### Inject Services

```tsx
import { Inject, Page, Sort, Filter, Group } from '@syncfusion/ej2-react-grids';

<GridComponent dataSource={data}>
  <ColumnsDirective>
    {/* columns */}
  </ColumnsDirective>
  <Inject services={[Page, Sort, Filter, Group]} />
</GridComponent>
```

### Common Modules

| Module | Purpose | Import |
|--------|---------|--------|
| `Page` | Enable paging | `import { Page } from '@syncfusion/ej2-react-grids'` |
| `Sort` | Enable sorting | `import { Sort } from '@syncfusion/ej2-react-grids'` |
| `Filter` | Enable filtering | `import { Filter } from '@syncfusion/ej2-react-grids'` |
| `Group` | Enable grouping | `import { Group } from '@syncfusion/ej2-react-grids'` |
| `Edit` | Enable editing | `import { Edit } from '@syncfusion/ej2-react-grids'` |
| `Aggregate` | Enable aggregates | `import { Aggregate } from '@syncfusion/ej2-react-grids'` |
| `ExcelExport` | Enable Excel export | `import { ExcelExport } from '@syncfusion/ej2-react-grids'` |
| `PdfExport` | Enable PDF export | `import { PdfExport } from '@syncfusion/ej2-react-grids'` |
| `Scroll` | Virtual scrolling | Built-in |

## First Grid Example

```tsx
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, Page, Sort, Filter } from '@syncfusion/ej2-react-grids';
import React from 'react';
import './App.css';

const data = [
  {
    OrderID: 10248,
    CustomerID: 'VINET',
    EmployeeID: 5,
    OrderDate: new Date(1996, 6, 4),
    Freight: 32.38,
    ShipCountry: 'France'
  },
  {
    OrderID: 10249,
    CustomerID: 'TOMSP',
    EmployeeID: 6,
    OrderDate: new Date(1996, 6, 5),
    Freight: 11.61,
    ShipCountry: 'Germany'
  },
  {
    OrderID: 10250,
    CustomerID: 'HANAR',
    EmployeeID: 4,
    OrderDate: new Date(1996, 6, 8),
    Freight: 65.83,
    ShipCountry: 'Brazil'
  }
];

function App() {
  return (
    <GridComponent
      dataSource={data}
      allowPaging={true}
      allowSorting={true}
      allowFiltering={true}
      pageSettings={{ pageSize: 10 }}
    >
      <ColumnsDirective>
        <ColumnDirective field='OrderID' headerText='Order ID' width='100' textAlign='Right' />
        <ColumnDirective field='CustomerID' headerText='Customer' width='120' />
        <ColumnDirective field='OrderDate' headerText='Order Date' width='130' type='date' format='yMd' />
        <ColumnDirective field='Freight' headerText='Freight' width='120' format='C2' textAlign='Right' />
        <ColumnDirective field='ShipCountry' headerText='Ship Country' width='150' />
      </ColumnsDirective>
      <Inject services={[Page, Sort, Filter]} />
    </GridComponent>
  );
}

export default App;
```
