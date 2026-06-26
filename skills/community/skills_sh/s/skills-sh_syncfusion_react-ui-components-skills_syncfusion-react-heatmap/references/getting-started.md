# Getting Started with React HeatMap Chart

## Table of Contents

- [Dependencies](#dependencies)
- [Installation](#installation)
  - [Step 1: Install the HeatMap Package](#step-1-install-the-heatmap-package)
  - [Step 2: Install Required Peer Dependencies (if not already installed)](#step-2-install-required-peer-dependencies-if-not-already-installed)
- [Project Setup](#project-setup)
  - [Option A: Using Vite (Recommended - Faster Development)](#option-a-using-vite-recommended---faster-development)
  - [Option B: Using Create React App](#option-b-using-create-react-app)
- [Adding to Your Project](#adding-to-your-project)
  - [Step 1: Import Theme CSS](#step-1-import-theme-css)
  - [Step 2: Import HeatMap Component](#step-2-import-heatmap-component)
- [Basic Implementation](#basic-implementation)
  - [Minimal Example (Empty HeatMap)](#minimal-example-empty-heatmap)
  - [Complete Basic Example with Data](#complete-basic-example-with-data)
  - [CSS Import Pattern](#css-import-pattern)
- [Running the Application](#running-the-application)
  - [For Vite](#for-vite)
  - [For Create React App](#for-create-react-app)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Dependencies

The HeatMap component requires the following npm packages:

```
@syncfusion/ej2-react-heatmap
├── @syncfusion/ej2-heatmap (core library)
├── @syncfusion/ej2-base
├── @syncfusion/ej2-data
├── @syncfusion/ej2-svg-base
└── @syncfusion/ej2-react-base
```

These are installed automatically when you add `@syncfusion/ej2-react-heatmap`.

## Installation

### Step 1: Install the HeatMap Package

```bash
npm install @syncfusion/ej2-react-heatmap --save
```

### Step 2: Install Required Peer Dependencies (if not already installed)

```bash
npm install @syncfusion/ej2-react-base --save
```

## Project Setup

### Option A: Using Vite (Recommended - Faster Development)

Create a new Vite React project:

```bash
npm create vite@latest my-heatmap-app -- --template react
cd my-heatmap-app
npm install
```

For TypeScript support:

```bash
npm create vite@latest my-heatmap-app -- --template react-ts
cd my-heatmap-app
npm install
```

### Option B: Using Create React App

```bash
npx create-react-app my-heatmap-app
cd my-heatmap-app
```

Then install HeatMap:

```bash
npm install @syncfusion/ej2-react-heatmap --save
```

## Adding to Your Project

### Step 1: Import Theme CSS

Add the Syncfusion theme CSS to your application entry point.

**For Vite (in `src/main.jsx` or `src/main.tsx`):**

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import '@syncfusion/ej2-base/styles/material.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**For Create React App (in `src/index.js`):**

```jsx
import '@syncfusion/ej2-base/styles/material.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

**Available Themes:**
- `material.css` (Material Design)
- `bootstrap5.css` (Bootstrap 5)
- `fabric.css` (Fluent Design)
- `tailwind.css` (Tailwind CSS)
- `fluent2.css` (Fluent 2)

Choose one theme based on your design preference.

### Step 2: Import HeatMap Component

In your component file (e.g., `App.jsx`):

```jsx
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';
```

## Basic Implementation

### Minimal Example (Empty HeatMap)

```jsx
import * as React from 'react';
import { HeatMapComponent } from '@syncfusion/ej2-react-heatmap';
import '@syncfusion/ej2-base/styles/material.css';

export function App() {
  return (
    <div>
      <h1>HeatMap Example</h1>
      <HeatMapComponent id='heatmap'></HeatMapComponent>
    </div>
  );
}

export default App;
```

### Complete Basic Example with Data

```jsx
import * as React from 'react';
import { HeatMapComponent, Inject, Legend, Tooltip } from '@syncfusion/ej2-react-heatmap';
import '@syncfusion/ej2-base/styles/material.css';

export function App() {
  const data = [
    [73, 39, 26, 39, 94],
    [93, 58, 53, 38, 26],
    [54, 39, 26, 40, 42]
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>Sales Performance HeatMap</h1>
      <HeatMapComponent 
        id='heatmap'
        dataSource={data}
        xAxis={{
          labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
        }}
        yAxis={{
          labels: ['Region A', 'Region B', 'Region C']
        }}
        title={{ text: 'Sales Data Across Regions' }}
      >
        <Inject services={[Legend, Tooltip]} />
      </HeatMapComponent>
    </div>
  );
}

export default App;
```

**What's happening:**
- `data`: 2D array with 3 rows and 5 columns
- `xAxis.labels`: Column headers (quarters)
- `yAxis.labels`: Row headers (regions)
- `<Inject services={[Legend, Tooltip]} />`: Enables legend and tooltips
- `title`: Adds a descriptive title to the heatmap

### CSS Import Pattern

```jsx
// At the top of your file, after other imports
import '@syncfusion/ej2-base/styles/material.css';

// Components don't need individual CSS imports
// The base theme CSS handles all Syncfusion components
```

## Running the Application

### For Vite:

```bash
npm run dev
```

The application opens at `http://localhost:5173` by default.

### For Create React App:

```bash
npm start
```

The application opens at `http://localhost:3000` by default.

## Troubleshooting

**Issue:** Styles not appearing or component looks unstyled
- **Solution:** Make sure you've imported the CSS file (`material.css` or your chosen theme) at the top of your entry point before rendering components.

**Issue:** HeatMapComponent not found error
- **Solution:** Verify the import is correct:
  ```jsx
  import { HeatMapComponent } from '@syncfusion/ej2-react-heatmap';
  ```

**Issue:** Blank heatmap with no data
- **Solution:** Provide a `dataSource` prop with 2D array data or JSON format data.

**Issue:** Dependency errors
- **Solution:** Run `npm install` again or clear node_modules:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

## Next Steps

Once your basic setup is complete:
1. **Learn about data formats** → Read [data-binding.md](data-binding.md)
2. **Configure axes** → Read [axes-configuration.md](axes-configuration.md)
3. **Customize appearance** → Read [legend-and-appearance.md](legend-and-appearance.md)
4. **Add interaction** → Read [interaction-and-selection.md](interaction-and-selection.md)
