# Cell Configuration and Grid Sizing

## Table of Contents
- [Overview](#overview)
- [Grid Columns](#grid-columns)
- [Cell Sizing Basics](#cell-sizing-basics)
- [Cell Aspect Ratio](#cell-aspect-ratio)
- [Cell Spacing](#cell-spacing)
- [Cell Calculation Examples](#cell-calculation-examples)
- [Responsive Cell Configuration](#responsive-cell-configuration)
- [Advanced Grid Patterns](#advanced-grid-patterns)
- [Best Practices](#best-practices)

## Overview

Dashboard Layout uses a grid-based system where panels are positioned in rows and columns. Cell configuration determines the visual dimensions of individual cells, affecting how panels are sized and positioned. Proper cell configuration is essential for creating well-proportioned, responsive dashboards.

### Grid System Fundamentals

```
Dashboard (e.g., 1000px wide)
├─ Column 1 (200px) │ Column 2 (200px) │ Column 3 (200px) │ Column 4 (200px) │ Column 5 (200px)
│                   │                  │                  │                  │
├─ Row 1 (200px)    │ Panel 1 (2x2)               │ Panel 2 (1x2)    │
│
├─ Row 2 (200px)    │ [spans columns 1-2]        │ [spans columns 4-5]
│
├─ Row 3 (200px)    │ Panel 3 (4x1)                              │
│
└─ Row 4 (200px)
```

## Grid Columns

The `columns` property defines how many equal cells comprise each row:

```typescript
<DashboardLayoutComponent
  columns={5}  // 5 equal cells per row
  panels={panels}
/>
```

### Column Distribution

When `columns={5}`:
- Each row is divided into 5 equal cells
- Each cell width = Parent Width / 5
- Cell height = Cell Width (by default, unless cellAspectRatio is set)

### Column Examples

```tsx
function GridColumnExamples() {
  return (
    <div>
      {/* 2-column grid (wide panels) */}
      <DashboardLayoutComponent
        id='grid-2'
        columns={2}
        panels={panels}
      />

      {/* 4-column grid (medium panels) */}
      <DashboardLayoutComponent
        id='grid-4'
        columns={4}
        panels={panels}
      />

      {/* 6-column grid (narrow panels) */}
      <DashboardLayoutComponent
        id='grid-6'
        columns={6}
        panels={panels}
      />

      {/* 12-column grid (Bootstrap-like) */}
      <DashboardLayoutComponent
        id='grid-12'
        columns={12}
        panels={panels}
      />
    </div>
  );
}
```

### Column Sizing Impact

| Columns | Per-Column Width (1000px) | Typical Use |
|---------|--------------------------|------------|
| 2 | 500px | Large panels |
| 3 | 333px | Dashboard sections |
| 4 | 250px | Standard layout |
| 5 | 200px | Default |
| 6 | 166px | Compact layout |
| 8 | 125px | Very compact |
| 12 | 83px | Fine-grained control |

## Cell Sizing Basics

### Panel Size in Cells

Panels are sized using grid units (cells):

```typescript
interface PanelModel {
  sizeX: number;  // Width in cells (columns)
  sizeY: number;  // Height in cells (rows)
}

const panels = [
  {
    id: 'wide-panel',
    sizeX: 4,  // Spans 4 columns
    sizeY: 2,  // Spans 2 rows
    row: 0,
    col: 0
  }
];
```

### Size Examples

```tsx
function CellSizeDemo() {
  const panels = [
    {
      id: 'small',
      header: 'Small (1x1)',
      content: 'Small panel',
      sizeX: 1,
      sizeY: 1,
      row: 0,
      col: 0
    },
    {
      id: 'wide',
      header: 'Wide (3x1)',
      content: 'Wide panel',
      sizeX: 3,
      sizeY: 1,
      row: 0,
      col: 1
    },
    {
      id: 'tall',
      header: 'Tall (1x3)',
      content: 'Tall panel',
      sizeX: 1,
      sizeY: 3,
      row: 0,
      col: 4
    },
    {
      id: 'large',
      header: 'Large (2x2)',
      content: 'Large panel',
      sizeX: 2,
      sizeY: 2,
      row: 1,
      col: 0
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      columns={5}
      panels={panels}
    />
  );
}
```

## Cell Aspect Ratio

The `cellAspectRatio` property defines the relationship between cell width and height:

```typescript
// Property signature
cellAspectRatio: number;  // Ratio of width to height (e.g., 100/50 = 2:1)
```

### Default Behavior

By default, `cellAspectRatio` is 1:1 (square cells):
```tsx
<DashboardLayoutComponent
  columns={5}
  cellAspectRatio={1}  // Default: 1:1 (width:height)
  panels={panels}
/>
```

### Aspect Ratio Examples

```tsx
function AspectRatioExamples() {
  return (
    <div>
      {/* Square cells (1:1) */}
      <div className="grid-container">
        <h3>Square Cells (1:1)</h3>
        <DashboardLayoutComponent
          id='square'
          columns={4}
          cellAspectRatio={1}  // width:height = 1:1
          panels={panels}
        />
      </div>

      {/* Wide cells (2:1) */}
      <div className="grid-container">
        <h3>Wide Cells (2:1)</h3>
        <DashboardLayoutComponent
          id='wide'
          columns={4}
          cellAspectRatio={2}  // width:height = 2:1
          panels={panels}
        />
      </div>

      {/* Tall cells (1:2) */}
      <div className="grid-container">
        <h3>Tall Cells (1:2)</h3>
        <DashboardLayoutComponent
          id='tall'
          columns={4}
          cellAspectRatio={0.5}  // width:height = 1:2
          panels={panels}
        />
      </div>

      {/* Custom ratio (4:3 - 16:12) */}
      <div className="grid-container">
        <h3>Custom Cells (4:3)</h3>
        <DashboardLayoutComponent
          id='custom'
          columns={4}
          cellAspectRatio={4/3}  // width:height = 4:3
          panels={panels}
        />
      </div>
    </div>
  );
}
```

### Calculating Actual Dimensions

Given:
- Parent width: 1000px
- Columns: 5
- cellAspectRatio: 100/50 (2:1)

Calculations:
```
Cell Width = 1000px / 5 = 200px
Cell Height = Cell Width / Aspect Ratio = 200px / 2 = 100px
Panel (2x2): 400px × 200px
```

## Cell Spacing

The `cellSpacing` property adds gaps between panels:

```typescript
// Property signature
cellSpacing: [number, number];  // [horizontal, vertical] in pixels
```

### Spacing Configuration

```tsx
function CellSpacingExamples() {
  return (
    <div>
      {/* No spacing */}
      <DashboardLayoutComponent
        id='no-space'
        columns={5}
        cellSpacing={[0, 0]}
        panels={panels}
      />

      {/* 10px spacing in all directions */}
      <DashboardLayoutComponent
        id='small-space'
        columns={5}
        cellSpacing={[10, 10]}
        panels={panels}
      />

      {/* 20px horizontal, 10px vertical */}
      <DashboardLayoutComponent
        id='custom-space'
        columns={5}
        cellSpacing={[20, 10]}
        panels={panels}
      />

      {/* Large spacing (20px) */}
      <DashboardLayoutComponent
        id='large-space'
        columns={5}
        cellSpacing={[20, 20]}
        panels={panels}
      />
    </div>
  );
}
```

### Impact on Layout

```
No Spacing (cellSpacing=[0, 0]):
┌──────┬──────┬──────┐
│      │      │      │
├──────┼──────┼──────┤
│      │      │      │
└──────┴──────┴──────┘

With Spacing (cellSpacing=[10, 10]):
┌──────┐  ┌──────┐  ┌──────┐
│      │  │      │  │      │
└──────┘  └──────┘  └──────┘
   ↕ 10px spacing
┌──────┐  ┌──────┐  ┌──────┐
│      │  │      │  │      │
└──────┘  └──────┘  └──────┘
```

## Cell Calculation Examples

### Example 1: Basic Layout

```tsx
function BasicLayoutCalculation() {
  const config = {
    parentWidth: 1200,
    columns: 6,
    cellSpacing: [10, 10],
    cellAspectRatio: 100/75  // 4:3 ratio
  };

  // Calculations
  const cellWidth = config.parentWidth / config.columns;  // 200px
  const cellHeight = cellWidth / (100/75);                // 150px
  
  // Example panel
  const panel = {
    sizeX: 3,  // 3 cells wide
    sizeY: 2   // 2 cells tall
  };

  const panelWidth = (panel.sizeX * cellWidth) + ((panel.sizeX - 1) * config.cellSpacing[0]);
  // = (3 * 200) + (2 * 10) = 620px
  
  const panelHeight = (panel.sizeY * cellHeight) + ((panel.sizeY - 1) * config.cellSpacing[1]);
  // = (2 * 150) + (1 * 10) = 310px

  return (
    <div>
      <p>Cell Width: {cellWidth}px</p>
      <p>Cell Height: {cellHeight}px</p>
      <p>Panel (3x2) Size: {panelWidth}px × {panelHeight}px</p>
      <DashboardLayoutComponent
        id='dashboard'
        columns={config.columns}
        cellSpacing={config.cellSpacing}
        cellAspectRatio={config.cellAspectRatio}
        panels={panels}
      />
    </div>
  );
}
```

### Example 2: Responsive Layout

```tsx
function ResponsiveLayoutCalculation() {
  const [screenSize, setScreenSize] = useState({
    width: window.innerWidth,
    columns: 5
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      let columns = 5;

      if (width < 640) columns = 2;      // Mobile
      else if (width < 1024) columns = 3; // Tablet
      else if (width < 1280) columns = 4; // Desktop
      else columns = 6;                   // Large desktop

      setScreenSize({ width, columns });
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div>
      <p>Screen: {screenSize.width}px, Columns: {screenSize.columns}</p>
      <DashboardLayoutComponent
        id='dashboard'
        columns={screenSize.columns}
        cellSpacing={[10, 10]}
        panels={panels}
      />
    </div>
  );
}
```

## Responsive Cell Configuration

### Media Query Based Configuration

```tsx
function MediaQueryDashboard() {
  const [config, setConfig] = useState({
    columns: 5,
    cellAspectRatio: 100/75,
    cellSpacing: [10, 10]
  });

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;

      if (width < 480) {
        // Mobile (extra small)
        setConfig({
          columns: 1,
          cellAspectRatio: 100/100,
          cellSpacing: [5, 5]
        });
      } else if (width < 768) {
        // Mobile (small)
        setConfig({
          columns: 2,
          cellAspectRatio: 100/100,
          cellSpacing: [8, 8]
        });
      } else if (width < 1024) {
        // Tablet
        setConfig({
          columns: 3,
          cellAspectRatio: 100/75,
          cellSpacing: [10, 10]
        });
      } else {
        // Desktop
        setConfig({
          columns: 5,
          cellAspectRatio: 100/75,
          cellSpacing: [15, 15]
        });
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <DashboardLayoutComponent
      id='dashboard'
      columns={config.columns}
      cellAspectRatio={config.cellAspectRatio}
      cellSpacing={config.cellSpacing}
      panels={panels}
    />
  );
}
```

### CSS Container Queries (Modern Approach)

```tsx
function ContainerQueryDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  return (
    <div className='dashboard-container'>
      <DashboardLayoutComponent
        ref={dashboardRef}
        id='dashboard'
        columns={5}
        cellAspectRatio={100/75}
        cellSpacing={[10, 10]}
        panels={panels}
      />
    </div>
  );
}

// CSS
.dashboard-container {
  container-type: inline-size;
}

/* Mobile layout */
@container (max-width: 640px) {
  .e-dashboard-layout {
    --grid-columns: 2;
  }
}

/* Tablet layout */
@container (640px < width < 1024px) {
  .e-dashboard-layout {
    --grid-columns: 3;
  }
}
```

## Advanced Grid Patterns

### Pattern 1: Masonry Layout

```tsx
function MasonryDashboard() {
  const panels = [
    // Column 1
    { id: 'p1', sizeX: 1, sizeY: 2, row: 0, col: 0 },
    { id: 'p2', sizeX: 1, sizeY: 1, row: 2, col: 0 },

    // Column 2
    { id: 'p3', sizeX: 1, sizeY: 1, row: 0, col: 1 },
    { id: 'p4', sizeX: 1, sizeY: 2, row: 1, col: 1 },

    // Column 3
    { id: 'p5', sizeX: 1, sizeY: 3, row: 0, col: 2 }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      columns={3}
      cellAspectRatio={100/100}
      cellSpacing={[10, 10]}
      allowFloating={true}
      panels={panels}
    />
  );
}
```

### Pattern 2: Hero + Grid

```tsx
function HeroGridDashboard() {
  const panels = [
    // Hero section (full width)
    {
      id: 'hero',
      header: 'Main Dashboard',
      sizeX: 5,
      sizeY: 2,
      row: 0,
      col: 0
    },

    // Supporting panels (3-column grid below)
    { id: 'p1', sizeX: 1, sizeY: 1, row: 2, col: 0 },
    { id: 'p2', sizeX: 2, sizeY: 1, row: 2, col: 1 },
    { id: 'p3', sizeX: 2, sizeY: 1, row: 2, col: 3 }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      columns={5}
      cellSpacing={[10, 10]}
      panels={panels}
    />
  );
}
```

### Pattern 3: Nested Grids

```tsx
function NestedGridDashboard() {
  const panels = [
    // Large panel acts as container
    {
      id: 'container',
      header: 'Analytics Section',
      content: `
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; height: 100%;">
          <div>Metric 1</div>
          <div>Metric 2</div>
          <div>Metric 3</div>
          <div>Metric 4</div>
        </div>
      `,
      sizeX: 3,
      sizeY: 2,
      row: 0,
      col: 0
    },
    // Adjacent small panels
    { id: 'side1', sizeX: 1, sizeY: 1, row: 0, col: 3 },
    { id: 'side2', sizeX: 1, sizeY: 1, row: 1, col: 3 }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      columns={4}
      cellSpacing={[10, 10]}
      panels={panels}
    />
  );
}
```

## Best Practices

### 1. Choose Appropriate Column Count

```tsx
// ✅ RECOMMENDED: Match your design system
// Use 2, 3, 4, 5, or 12 columns (common grid systems)
<DashboardLayoutComponent columns={5} panels={panels} />

// ❌ AVOID: Too many columns makes layout complex
<DashboardLayoutComponent columns={24} panels={panels} />
```

### 2. Set Consistent Cell Aspect Ratio

```tsx
// ✅ RECOMMENDED: Standard aspect ratios
const ratios = {
  square: 1,           // 1:1
  widescreen: 16/9,    // 16:9
  cinema: 21/9,        // 21:9
  photoWide: 3/2,      // 3:2
  video: 4/3,          // 4:3
  golden: 1.618        // Golden ratio
};

<DashboardLayoutComponent 
  cellAspectRatio={ratios.video}
  panels={panels}
/>
```

### 3. Use Appropriate Spacing

```tsx
// ✅ RECOMMENDED: 10-20px spacing for visual clarity
<DashboardLayoutComponent
  cellSpacing={[15, 15]}  // Balanced spacing
  panels={panels}
/>

// ⚠️ TOO MUCH: Creates large gaps
<DashboardLayoutComponent
  cellSpacing={[40, 40]}
  panels={panels}
/>

// ⚠️ TOO LITTLE: Panels appear cramped
<DashboardLayoutComponent
  cellSpacing={[0, 0]}
  panels={panels}
/>
```

### 4. Plan Responsive Breakpoints

```tsx
// ✅ RECOMMENDED: Standard breakpoints
const breakpoints = {
  xs: { width: 320, columns: 1 },
  sm: { width: 640, columns: 2 },
  md: { width: 1024, columns: 3 },
  lg: { width: 1280, columns: 5 },
  xl: { width: 1920, columns: 6 }
};
```

### 5. Document Grid Configuration

```tsx
interface DashboardConfig {
  // Grid settings
  columns: number;
  cellAspectRatio: number;
  cellSpacing: [number, number];

  // Behavior
  allowDragging: boolean;
  allowResizing: boolean;
  allowFloating: boolean;

  // Documentation
  description: string;
  breakpoint: string;
}

const desktopConfig: DashboardConfig = {
  columns: 5,
  cellAspectRatio: 100/75,
  cellSpacing: [15, 15],
  allowDragging: true,
  allowResizing: true,
  allowFloating: true,
  description: 'Full-featured desktop layout',
  breakpoint: '>= 1280px'
};
```
