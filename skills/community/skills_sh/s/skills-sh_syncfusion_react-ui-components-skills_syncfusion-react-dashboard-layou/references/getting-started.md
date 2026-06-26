# Getting Started with Dashboard Layout

## Table of Contents
- [Installation](#installation)
- [Setup & Configuration](#setup--configuration)
- [Basic Implementation](#basic-implementation)
- [Adding Panels](#adding-panels)
- [First Dashboard](#first-dashboard)
- [Common Setup Issues](#common-setup-issues)

## Installation

### Dependencies

The Dashboard Layout component requires the following packages:

```
@syncfusion/ej2-react-layouts
├── @syncfusion/ej2-react-base
│   ├── @syncfusion/ej2-base
│   └── react (>=16.8)
└── @syncfusion/ej2-layouts
```

### Package Installation

Install the Syncfusion React layouts package using npm:

```bash
npm install @syncfusion/ej2-react-layouts --save
```

Or using yarn:

```bash
yarn add @syncfusion/ej2-react-layouts
```

## Setup & Configuration

### Import Dashboard Layout Component

```tsx
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';
```

### Import CSS Styles

Add the required CSS imports to your main component or App.tsx file:

```tsx
// Import base theme (choose one)
import '@syncfusion/ej2-base/styles/tailwind3.css';
// OR
// import '@syncfusion/ej2-base/styles/bootstrap5.css';
// import '@syncfusion/ej2-base/styles/fluent2.css';
// import '@syncfusion/ej2-base/styles/material3.css';

// Import Dashboard Layout styles
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';
// OR
// import '@syncfusion/ej2-react-layouts/styles/bootstrap5.css';
// import '@syncfusion/ej2-react-layouts/styles/fluent2.css';
// import '@syncfusion/ej2-react-layouts/styles/material3.css';
```

**Note:** Choose only one theme. Using multiple themes simultaneously may cause styling conflicts.

### Theme Options

- **tailwind3** - Tailwind CSS 3 theme (recommended)
- **bootstrap5** - Bootstrap 5 theme
- **fluent2** - Microsoft Fluent 2 theme
- **material3** - Material Design 3 theme

### Using CSS Resource Generator (CRG)

For optimal bundle size, use Syncfusion's Custom Resource Generator to include only required component styles:

1. Visit: url
2. Select React platform
3. Select Dashboard Layout component
4. Choose your theme
5. Download the combined CSS file
6. Import the generated CSS file in your project

## Basic Implementation

### Minimal Dashboard Layout

Create your first Dashboard Layout with default settings:

```tsx
import React from 'react';
import { DashboardLayoutComponent, PanelDirective, PanelsDirective } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';

function App() {
  return (
    <DashboardLayoutComponent
      id='default_dashboard'
      columns={5}
    >
    </DashboardLayoutComponent>
  );
}

export default App;
```

### Dashboard Layout with Panels

Add panels to your dashboard using the panels property:

```tsx
import React from 'react';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

function App() {
  const panels = [
    {
      id: 'panel1',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1,
      header: 'Panel 1',
      content: 'Welcome to Syncfusion React Dashboard Layout'
    },
    {
      id: 'panel2',
      row: 0,
      col: 2,
      sizeX: 2,
      sizeY: 1,
      header: 'Panel 2',
      content: 'This is panel 2'
    }
  ];

  return (
    <DashboardLayoutComponent
      id='default_dashboard'
      columns={5}
      panels={panels}
    >
    </DashboardLayoutComponent>
  );
}

export default App;
```

## Adding Panels

### Static Panels (Defined Upfront)

Define all panels in the panels array:

```tsx
const staticPanels = [
  {
    id: 'analytics',
    header: 'Analytics',
    content: '<div>Analytics dashboard</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  },
  {
    id: 'metrics',
    header: 'Key Metrics',
    content: '<div>Key metrics panel</div>',
    row: 0,
    col: 2,
    sizeX: 2,
    sizeY: 2
  },
  {
    id: 'reports',
    header: 'Reports',
    content: '<div>Reports panel</div>',
    row: 2,
    col: 0,
    sizeX: 4,
    sizeY: 1
  }
];

<DashboardLayoutComponent columns={5} panels={staticPanels}>
</DashboardLayoutComponent>
```

### Dynamic Panels (HTML Attribute Method)

Define panels directly in HTML using data attributes:

```tsx
<DashboardLayoutComponent id='layout' columns={5} cellSpacing={[5, 5]}>
  <div id='panel1' className='e-panel' data-row='0' data-col='0' data-sizex='2' data-sizey='1'>
    <div className='e-panel-header'>
      Panel 1
      <span className='e-icons e-close' />
    </div>
    <div className='e-panel-content'>
      Content for panel 1
    </div>
  </div>

  <div id='panel2' className='e-panel' data-row='0' data-col='2' data-sizex='2' data-sizey='1'>
    <div className='e-panel-header'>
      Panel 2
      <span className='e-icons e-close' />
    </div>
    <div className='e-panel-content'>
      Content for panel 2
    </div>
  </div>
</DashboardLayoutComponent>
```

## First Dashboard

### Complete Functional Dashboard Example

```tsx
import React, { useRef, useState } from 'react';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';

function Dashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  
  const [panels] = useState([
    {
      id: 'panel1',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2,
      header: 'Sales Overview',
      content: (
        <div style={{ padding: '20px' }}>
          <h3>Total Sales: $150,000</h3>
          <p>This month's revenue</p>
        </div>
      )
    },
    {
      id: 'panel2',
      row: 0,
      col: 2,
      sizeX: 2,
      sizeY: 2,
      header: 'User Activity',
      content: (
        <div style={{ padding: '20px' }}>
          <h3>Active Users: 2,450</h3>
          <p>Currently online</p>
        </div>
      )
    },
    {
      id: 'panel3',
      row: 2,
      col: 0,
      sizeX: 3,
      sizeY: 1,
      header: 'Performance Metrics',
      content: (
        <div style={{ padding: '20px' }}>
          <p>System uptime: 99.9%</p>
          <p>Response time: 45ms</p>
        </div>
      )
    }
  ]);

  const handleDragStop = () => {
    console.log('Panel rearranged');
  };

  const handleChange = (args: any) => {
    console.log('Layout changed:', args);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>My Dashboard</h1>
      
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        columns={5}
        cellSpacing={[10, 10]}
        panels={panels}
        allowDragging={true}
        dragStop={handleDragStop}
        change={handleChange}
      >
      </DashboardLayoutComponent>
    </div>
  );
}

export default Dashboard;
```

### Dashboard with Customization

```tsx
<DashboardLayoutComponent
  id='custom_dashboard'
  columns={5}
  cellSpacing={[15, 15]}
  cellAspectRatio={1.5}
  allowDragging={true}
  allowResizing={true}
  allowFloating={true}
  enablePersistence={true}
  showGridLines={false}
  mediaQuery='max-width:600px'
  panels={panels}
>
</DashboardLayoutComponent>
```

## Common Setup Issues

### Issue: Styles Not Applying

**Problem:** Dashboard Layout appears without any styling.

**Solution:** Ensure CSS imports are in correct order:
```tsx
// Base styles first
import '@syncfusion/ej2-base/styles/tailwind3.css';
// Then component styles
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';
```

### Issue: Panels Not Displaying

**Problem:** Panel array is defined but panels don't render.

**Solution:** Verify panel configuration:
```tsx
// Ensure panels have required properties
const panels = [
  {
    id: 'unique-id',      // Required: Unique identifier
    row: 0,               // Required: Row position
    col: 0,               // Required: Column position
    sizeX: 2,             // Optional: Width (default: 1)
    sizeY: 1,             // Optional: Height (default: 1)
    header: 'Title',      // Optional: Panel header
    content: 'Content'    // Optional: Panel content
  }
];
```

### Issue: "Cannot read property 'current' of undefined"

**Problem:** useRef is undefined or ref is not properly attached.

**Solution:** Properly import and use useRef:
```tsx
import { useRef } from 'react';

const dashboardRef = useRef<DashboardLayoutComponent>(null);

<DashboardLayoutComponent ref={dashboardRef} panels={panels}>
</DashboardLayoutComponent>
```

### Issue: TypeScript Errors

**Problem:** TypeScript complains about PanelModel or component types.

**Solution:** Import types explicitly:
```tsx
import { 
  DashboardLayoutComponent, 
  PanelModel 
} from '@syncfusion/ej2-react-layouts';

const panels: PanelModel[] = [...];
```

### Issue: Layout Breaks on Mobile

**Problem:** Dashboard doesn't respond well on small screens.

**Solution:** Use mediaQuery property:
```tsx
<DashboardLayoutComponent
  columns={5}
  mediaQuery='max-width:768px'  // Stacks to single column on tablets
  panels={panels}
>
</DashboardLayoutComponent>
```
