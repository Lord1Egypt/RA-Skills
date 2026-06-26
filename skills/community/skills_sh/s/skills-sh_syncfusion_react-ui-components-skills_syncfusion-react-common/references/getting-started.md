# Getting Started with Syncfusion React Components

## Table of Contents
- [Overview](#overview)
- [Framework Integration](#framework-integration)
- [Next.js Setup](#nextjs-setup)
- [Remix Setup](#remix-setup)
- [Vite Setup](#vite-setup)
- [Preact Setup](#preact-setup)
- [SharePoint Setup](#sharepoint-setup)

## Overview

Syncfusion React components are available as npm packages and work seamlessly with modern JavaScript frameworks. This guide covers installation, CSS imports, and initialization for popular frameworks.

## Framework Integration

### Syncfusion Package Installation

All Syncfusion React components are distributed via npm at [npmjs.com](https://www.npmjs.com/search?q=ej2-react). Install the required component package:

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### CSS Theme Import

Choose one theme and import it in your main CSS file or entry point:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-grids/styles/tailwind3.css";
```

**Available themes:** tailwind3, bootstrap5.3, fluent2, material3, etc.. (replace theme name in CSS path)

## Next.js Setup

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### Step 2: Import Styles in app/globals.css

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
@import "../node_modules/@syncfusion/ej2-react-grids/styles/tailwind3.css";
```

### Step 3: Create Datasource File (app/datasource.ts)

```typescript
export let data: Object[] = [
    {
        OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5,
        ShipName: 'Vins et alcools Chevalier', ShipCity: 'Reims',
        ShipCountry: 'France', Freight: 32.38
    },
    {
        OrderID: 10249, CustomerID: 'TOMSP', EmployeeID: 6,
        ShipName: 'Toms Spezialitäten', ShipCity: 'Münster',
        ShipCountry: 'Germany', Freight: 11.61
    }
];
```

### Step 4: Add Component in app/page.tsx

```typescript
'use client'
import {
  ColumnDirective, ColumnsDirective, GridComponent,
  Inject, Page, Sort, Filter, Group
} from '@syncfusion/ej2-react-grids';
import { data } from "./datasource";

export default function Home() {
  const pageSettings: object = { pageSize: 6 };
  const filterSettings: object = { type: 'Excel' };

  return (
    <GridComponent
      dataSource={data}
      allowGrouping={true}
      allowSorting={true}
      allowFiltering={true}
      allowPaging={true}
      pageSettings={pageSettings}
      filterSettings={filterSettings}
    >
      <ColumnsDirective>
        <ColumnDirective field="OrderID" width="100" textAlign="Right" />
        <ColumnDirective field="CustomerID" width="100" />
        <ColumnDirective field="EmployeeID" width="100" textAlign="Right" />
        <ColumnDirective field="Freight" width="100" format="C2" textAlign="Right" />
        <ColumnDirective field="ShipCountry" width="100" />
      </ColumnsDirective>
      <Inject services={[Page, Sort, Filter, Group]} />
    </GridComponent>
  );
}
```

## Remix Setup

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### Step 2: Configure vite.config.ts

```typescript
import { defineConfig } from "vite";

export default defineConfig({
  ssr: {
    noExternal: [/@syncfusion/]
  }
});
```

### Step 3: Import Styles in ~/app/routes/_index.tsx

```typescript
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-calendars/styles/tailwind3.css';
import '@syncfusion/ej2-dropdowns/styles/tailwind3.css';
import '@syncfusion/ej2-inputs/styles/tailwind3.css';
import '@syncfusion/ej2-navigations/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
import '@syncfusion/ej2-react-grids/styles/tailwind3.css';
```

### Step 4: Add Component

```typescript
import { ColumnDirective, ColumnsDirective, GridComponent, Inject, Page, Sort } from '@syncfusion/ej2-react-grids';
import { data } from '../datasource';

export default function Index() {
  return (
    <GridComponent dataSource={data} allowPaging={true}>
      <ColumnsDirective>
        <ColumnDirective field="OrderID" width="100" textAlign="Right" />
        <ColumnDirective field="CustomerID" width="100" />
        <ColumnDirective field="EmployeeID" width="100" textAlign="Right" />
        <ColumnDirective field="Freight" width="100" format="C2" textAlign="Right" />
        <ColumnDirective field="ShipCountry" width="100" />
      </ColumnsDirective>
      <Inject services={[Page, Sort]} />
    </GridComponent>
  );
}
```

## Vite Setup

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### Step 2: Import Styles in src/App.css

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-grids/styles/tailwind3.css";
```

### Step 3: Add Component in src/App.jsx

```typescript
import './App.css'
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';

function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5, ShipCountry: 'France', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', EmployeeID: 6, ShipCountry: 'Germany', Freight: 11.61 },
    { OrderID: 10250, CustomerID: 'HANAR', EmployeeID: 4, ShipCountry: 'Brazil', Freight: 65.83 }
  ];

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' width='100' textAlign="Right" />
        <ColumnDirective field='CustomerID' width='100' />
        <ColumnDirective field='EmployeeID' width='100' textAlign="Right" />
        <ColumnDirective field='Freight' width='100' format="C2" textAlign="Right" />
        <ColumnDirective field='ShipCountry' width='100' />
      </ColumnsDirective>
    </GridComponent>
  );
}

export default App;
```
## Preact Setup

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### Step 2: Import Styles in src/style.css

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-grids/styles/tailwind3.css";
```

### Step 3: Add Component in src/index.jsx

```typescript
import { render } from 'preact';
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';
import './style.css';

export function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5, ShipCountry: 'France', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', EmployeeID: 6, ShipCountry: 'Germany', Freight: 11.61 },
    { OrderID: 10250, CustomerID: 'HANAR', EmployeeID: 4, ShipCountry: 'Brazil', Freight: 65.83 }
  ];

  return (
    <GridComponent dataSource={data}>
      <ColumnsDirective>
        <ColumnDirective field='OrderID' width='100' textAlign="Right" />
        <ColumnDirective field='CustomerID' width='100' />
        <ColumnDirective field='EmployeeID' width='100' textAlign="Right" />
        <ColumnDirective field='Freight' width='100' format="C2" textAlign="Right" />
        <ColumnDirective field='ShipCountry' width='100' />
      </ColumnsDirective>
    </GridComponent>
  );
}

render(<App />, document.getElementById('app'));
```

## SharePoint Setup

### Step 1: Install Package

```bash
npm install @syncfusion/ej2-react-grids@latest --save
```

### Step 2: Import Styles in App.tsx

Import theme CSS in your SharePoint component file:

```typescript
require('@syncfusion/ej2-react-grids/styles/tailwind3.css');
```

### Step 3: Add Component in ~/src/webparts/app/components/App.tsx

```typescript
import * as React from 'react';
import { ColumnDirective, ColumnsDirective, GridComponent } from '@syncfusion/ej2-react-grids';

require('@syncfusion/ej2-react-grids/styles/tailwind3.css');

export default class App extends React.Component {
  public render(): React.ReactElement {
    const data = [
      { OrderID: 10248, CustomerID: 'VINET', EmployeeID: 5, ShipCountry: 'France', Freight: 32.38 },
      { OrderID: 10249, CustomerID: 'TOMSP', EmployeeID: 6, ShipCountry: 'Germany', Freight: 11.61 },
      { OrderID: 10250, CustomerID: 'HANAR', EmployeeID: 4, ShipCountry: 'Brazil', Freight: 65.83 }
    ];

    return (
      <GridComponent dataSource={data}>
        <ColumnsDirective>
          <ColumnDirective field='OrderID' width='100' textAlign="Right" />
          <ColumnDirective field='CustomerID' width='100' />
          <ColumnDirective field='EmployeeID' width='100' textAlign="Right" />
          <ColumnDirective field='Freight' width='100' format="C2" textAlign="Right" />
          <ColumnDirective field='ShipCountry' width='100' />
        </ColumnsDirective>
      </GridComponent>
    );
  }
}
```
