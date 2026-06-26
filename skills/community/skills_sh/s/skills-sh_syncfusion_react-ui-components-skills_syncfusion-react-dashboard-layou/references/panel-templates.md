# Panel Templates and Content

## Table of Contents
- [Overview](#overview)
- [Panel Structure](#panel-structure)
- [Header Templates](#header-templates)
- [Content Templates](#content-templates)
- [JSX Content Rendering](#jsx-content-rendering)
- [Embedding Syncfusion Components](#embedding-syncfusion-components)
- [Dynamic Content Updates](#dynamic-content-updates)
- [Template Best Practices](#template-best-practices)

## Overview

Dashboard Layout panels support flexible content rendering through HTML strings, JSX components, and Syncfusion widgets. Panel templates define the visual structure and content that appears within each panel, including headers (optional), content area, and custom styling.

### Panel Composition

Each panel consists of:
- **Header** (optional): Title bar with custom content
- **Content Area**: Main panel body containing data or widgets
- **Panel Wrapper**: Container managing styling and interactions

### Template Types Supported

| Type | Usage | Performance |
|------|-------|-------------|
| HTML String | Simple static content | ⚡ Fastest |
| JSX Component | Dynamic React components | 🔄 Moderate |
| Syncfusion Control | Charts, Grids, DataGrids | 📊 Feature-rich |
| Mixed Content | Combination of above | 🎨 Most flexible |

## Panel Structure

### Basic Panel Model with Templates

```typescript
interface PanelModel {
  id?: string;                    // Unique panel identifier
  header?: string;                // Header text or HTML
  content?: string | JSX.Element; // Panel content
  row?: number;                   // Row position (0-based)
  col?: number;                   // Column position (0-based)
  sizeX?: number;                 // Width in grid cells
  sizeY?: number;                 // Height in grid cells
  minSizeX?: number;              // Minimum width
  minSizeY?: number;              // Minimum height
  maxSizeX?: number;              // Maximum width
  maxSizeY?: number;              // Maximum height
}
```

### Creating Panels with Content

```tsx
const panels = [
  {
    id: 'panel-1',
    header: 'Sales Report',
    content: '<div class="content">Revenue: $50,000</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];
```

## Header Templates

Headers provide visual identification and optional interactive controls for panels.

### Simple Text Headers

```tsx
const panels = [
  {
    id: 'dashboard-stats',
    header: 'Dashboard Statistics',
    content: '<div class="stats">Stats content here</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];

<DashboardLayoutComponent panels={panels} />
```

### HTML Headers with Custom Styling

```tsx
const panels = [
  {
    id: 'chart-panel',
    header: '<div class="custom-header"><span>📊 Sales Chart</span></div>',
    content: '<div class="chart-content">Chart here</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];
```

### Headers with Interactive Elements

```tsx
const panels = [
  {
    id: 'interactive-panel',
    header: `
      <div class="header-container">
        <span class="title">Panel Title</span>
        <button class="refresh-btn" onclick="refreshData()">🔄</button>
      </div>
    `,
    content: '<div id="panel-content">Content here</div>',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 2
  }
];
```

### Header Properties via PanelModel

The `header` property accepts:
- **String**: Simple text (e.g., "Panel Title")
- **HTML**: Full HTML markup with styling
- **Custom Content**: Interactive elements and icons

**Best Practices:**
- Keep headers concise (single line recommended)
- Use consistent icon sets (emoji or icon libraries)
- Avoid complex nested structures in headers

## Content Templates

Content templates define the main panel body, supporting various rendering approaches.

### HTML String Content

The simplest approach for static or data-driven content:

```tsx
const panels = [
  {
    id: 'stats-panel',
    header: 'System Statistics',
    content: `
      <div class="stats-wrapper">
        <div class="stat-item">
          <label>CPU Usage</label>
          <span class="value">45%</span>
        </div>
        <div class="stat-item">
          <label>Memory Usage</label>
          <span class="value">62%</span>
        </div>
        <div class="stat-item">
          <label>Disk Usage</label>
          <span class="value">78%</span>
        </div>
      </div>
    `,
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1
  }
];
```

### Dynamic Content with Data Binding

```tsx
function Dashboard() {
  const [stats, setStats] = useState({ cpu: 45, memory: 62, disk: 78 });

  const panels = [
    {
      id: 'stats-panel',
      header: 'System Stats',
      content: `
        <div class="stats-container">
          <p>CPU: ${stats.cpu}%</p>
          <p>Memory: ${stats.memory}%</p>
          <p>Disk: ${stats.disk}%</p>
        </div>
      `,
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
    />
  );
}
```

## JSX Content Rendering

For complex React components, render JSX-based content:

```tsx
function Dashboard() {
  const [data, setData] = useState([]);

  // Custom React component for panel content
  const PanelContent = ({ title, items }) => (
    <div className="panel-content">
      <h3>{title}</h3>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  );

  // Convert to HTML string
  const contentHtml = ReactDOM.renderToString(
    <PanelContent 
      title="Recent Items" 
      items={['Item 1', 'Item 2', 'Item 3']}
    />
  );

  const panels = [
    {
      id: 'content-panel',
      header: 'Content List',
      content: contentHtml,
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
    />
  );
}
```

## Embedding Syncfusion Components

Dashboard Layout panels can host any Syncfusion component (Charts, Grids, etc.):

### Embedding a Chart

```tsx
import { ChartComponent, SeriesCollectionDirective, SeriesDirective, Inject, Legend, Tooltip, LineSeries } from '@syncfusion/ej2-react-charts';
import { DashboardLayoutComponent } from '@syncfusion/ej2-react-layouts';

function DashboardWithChart() {
  const chartContent = `
    <div id="chart-container" style="height: 100%; width: 100%;"></div>
  `;

  const panels = [
    {
      id: 'chart-panel',
      header: 'Revenue Trend',
      content: chartContent,
      row: 0,
      col: 0,
      sizeX: 3,
      sizeY: 2
    }
  ];

  React.useEffect(() => {
    const data = [
      { x: 'Jan', y: 25 },
      { x: 'Feb', y: 30 },
      { x: 'Mar', y: 28 }
    ];

    // Mount chart to container after panel renders
    const root = ReactDOM.createRoot(document.getElementById('chart-container'));
    root.render(
      <ChartComponent id='line-chart' title='Sales Trend' tooltip={{ enable: true }}>
        <Inject services={[Legend, Tooltip, LineSeries]} />
        <SeriesCollectionDirective>
          <SeriesDirective dataSource={data} xName='x' yName='y' type='Line' />
        </SeriesCollectionDirective>
      </ChartComponent>
    );
  }, []);

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      cellSpacing={[10, 10]}
    />
  );
}
```

### Embedding a DataGrid

```tsx
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page, Search, Toolbar } from '@syncfusion/ej2-react-grids';

function DashboardWithGrid() {
  const gridContent = `
    <div id="grid-container" style="height: 100%; width: 100%;"></div>
  `;

  const panels = [
    {
      id: 'grid-panel',
      header: 'Data Table',
      content: gridContent,
      row: 0,
      col: 0,
      sizeX: 4,
      sizeY: 3
    }
  ];

  React.useEffect(() => {
    const data = [
      { id: 1, name: 'John', dept: 'Sales', salary: 50000 },
      { id: 2, name: 'Jane', dept: 'HR', salary: 48000 },
      { id: 3, name: 'Bob', dept: 'IT', salary: 65000 }
    ];

    const root = ReactDOM.createRoot(document.getElementById('grid-container'));
    root.render(
      <GridComponent dataSource={data} allowPaging={true}>
        <ColumnsDirective>
          <ColumnDirective field='id' headerText='ID' width='80' />
          <ColumnDirective field='name' headerText='Name' width='100' />
          <ColumnDirective field='dept' headerText='Department' width='100' />
          <ColumnDirective field='salary' headerText='Salary' width='100' />
        </ColumnsDirective>
        <Inject services={[Page, Search, Toolbar]} />
      </GridComponent>
    );
  }, []);

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      cellSpacing={[10, 10]}
    />
  );
}
```

## Dynamic Content Updates

Update panel content after creation using `updatePanel` method:

```tsx
function Dashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [counter, setCounter] = useState(0);

  const panels = [
    {
      id: 'counter-panel',
      header: 'Counter',
      content: `<div class="counter">Count: ${counter}</div>`,
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    }
  ];

  const updateContent = () => {
    const newCount = counter + 1;
    setCounter(newCount);

    // Update panel content programmatically
    const updatedPanel = {
      id: 'counter-panel',
      header: 'Counter',
      content: `<div class="counter">Count: ${newCount}</div>`,
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    };

    dashboardRef.current?.updatePanel(updatedPanel);
  };

  return (
    <div>
      <button onClick={updateContent}>Increment</button>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        panels={panels}
        columns={5}
      />
    </div>
  );
}
```

## Template Best Practices

### 1. Performance Optimization

```tsx
// ❌ AVOID: Recreating panels on every render
function BadDashboard() {
  const panels = [
    {
      id: 'panel1',
      content: '<div>Content</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    }
  ];

  return <DashboardLayoutComponent panels={panels} />;
}

// ✅ RECOMMENDED: Memoize panel definitions
function GoodDashboard() {
  const panels = useMemo(() => [
    {
      id: 'panel1',
      content: '<div>Content</div>',
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 1
    }
  ], []);

  return <DashboardLayoutComponent panels={panels} />;
}
```

### 2. Content Sizing

```tsx
// ✅ RECOMMENDED: Content with proper height
const panels = [
  {
    id: 'chart-panel',
    header: 'Chart',
    content: '<div style="height: 100%; overflow: auto;">Content</div>',
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 3
  }
];
```

### 3. Error Handling

```tsx
function SafeDashboard() {
  const panels = [
    {
      id: 'safe-panel',
      header: 'Data Panel',
      content: (() => {
        try {
          return generateComplexContent();
        } catch (e) {
          return `<div class="error">Error: ${e.message}</div>`;
        }
      })(),
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return <DashboardLayoutComponent panels={panels} />;
}
```

### 4. Accessibility

```tsx
// ✅ RECOMMENDED: Semantic HTML with ARIA labels
const panels = [
  {
    id: 'accessible-panel',
    header: `<div role="heading" aria-level="2">Sales Data</div>`,
    content: `
      <div role="main" aria-label="Sales information">
        <table aria-label="Sales table">
          <tr><td>Q1</td><td>$50,000</td></tr>
          <tr><td>Q2</td><td>$55,000</td></tr>
        </table>
      </div>
    `,
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 2
  }
];
```

### 5. Mobile Responsiveness

```tsx
function ResponsiveDashboard() {
  const isMobile = window.innerWidth < 768;

  const panels = [
    {
      id: 'responsive-panel',
      header: 'Dashboard',
      content: '<div>Content adapts to screen size</div>',
      row: 0,
      col: 0,
      sizeX: isMobile ? 1 : 2,
      sizeY: isMobile ? 1 : 2
    }
  ];

  return (
    <DashboardLayoutComponent
      panels={panels}
      columns={isMobile ? 2 : 5}
      mediaQuery="max-width: 768px"
    />
  );
}
```

### 6. Styling Content

```tsx
// ✅ RECOMMENDED: Use CSS classes for maintainability
const panels = [
  {
    id: 'styled-panel',
    header: 'Styled Panel',
    content: `
      <div class="panel-content">
        <div class="metric">
          <span class="label">Revenue</span>
          <span class="value">$100,000</span>
        </div>
      </div>
    `,
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 1
  }
];

// CSS
// .panel-content { padding: 20px; }
// .metric { display: flex; justify-content: space-between; }
// .value { font-weight: bold; color: #2196F3; }
```
