# Getting Started with TreeMap

## Table of Contents

- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Package Setup](#package-setup)
  - [Basic Project Setup](#basic-project-setup)
  - [TypeScript Setup](#typescript-setup)
- [Module Injection](#module-injection)
  - [Available Modules](#available-modules)
- [First TreeMap Render](#first-treemap-render)
  - [Minimal Example](#minimal-example)
  - [Understanding the Props](#understanding-the-props)
- [Binding Data](#binding-data)
  - [Flat Data Structure](#flat-data-structure)
  - [Hierarchical Data Structure](#hierarchical-data-structure)
  - [Data Binding Tips](#data-binding-tips)
- [Next Steps](#next-steps)

## Installation

Install the Syncfusion React TreeMap package using npm:

```bash
npm install @syncfusion/ej2-react-treemap --save
```

### Dependencies

The TreeMap package has the following peer dependencies:

```
@syncfusion/ej2-treemap
@syncfusion/ej2-base
@syncfusion/ej2-data
@syncfusion/ej2-pdf-export
@syncfusion/ej2-svg-base
@syncfusion/ej2-react-base
```

These are automatically installed with the main package.

## Package Setup

### Basic Project Setup

For optimal development experience, use Vite instead of Create React App:

```bash
# Create a new Vite React app
npm create vite@latest my-treemap-app -- --template react
cd my-treemap-app

# Install Syncfusion TreeMap
npm install @syncfusion/ej2-react-treemap --save

# Start development server
npm run dev
```

### TypeScript Setup

For TypeScript projects:

```bash
npm create vite@latest my-treemap-app -- --template react-ts
cd my-treemap-app
npm install @syncfusion/ej2-react-treemap --save
npm run dev
```

## Module Injection

TreeMap uses feature-based modules. Import and inject required feature modules for your use case:

```jsx
import { TreeMapComponent, Inject } from '@syncfusion/ej2-react-treemap';
import {
  TreeMapHighlight,
  TreeMapSelection,
  TreeMapLegend,
  TreeMapTooltip
} from '@syncfusion/ej2-react-treemap';

export function MyTreeMap() {
  return (
    <TreeMapComponent>
      <Inject services={[TreeMapHighlight, TreeMapSelection, TreeMapLegend, TreeMapTooltip]} />
    </TreeMapComponent>
  );
}
```

### Available Modules

| Module | Feature | When to Use |
|--------|---------|-----------|
| `TreeMapHighlight` | Highlight items on hover | Interactive visualization |
| `TreeMapSelection` | Select items with click | Data selection interactions |
| `TreeMapLegend` | Display legend | Large datasets with categories |
| `TreeMapTooltip` | Show tooltips on hover | Detailed information display |

**Note:** Inject modules only when needed to minimize bundle size.

## First TreeMap Render

### Minimal Example

```jsx
import * as React from 'react';
import { TreeMapComponent } from '@syncfusion/ej2-react-treemap';

export function TreeMapBasic() {
  const data = [
    { Title: 'Apple', Sales: 5000 },
    { Title: 'Mango', Sales: 3000 },
    { Title: 'Orange', Sales: 2300 },
    { Title: 'Banana', Sales: 500 },
    { Title: 'Grape', Sales: 4300 },
    { Title: 'Papaya', Sales: 1200 },
    { Title: 'Melon', Sales: 4500 }
  ];

  return (
    <TreeMapComponent
      height="350px"
      dataSource={data}
      weightValuePath="Sales"
      leafItemSettings={{
        labelPath: 'Title'
      }}
    />
  );
}
```

**Result:** Renders a TreeMap with rectangular items sized by Sales value, labeled with Title.

### Understanding the Props

- **height:** Container height (required)
- **dataSource:** Array of data objects to visualize
- **weightValuePath:** Property name determining rectangle size
- **leafItemSettings:** Configuration for leaf (lowest level) items
  - **labelPath:** Property name for item labels

## Binding Data

### Flat Data Structure

Flat data has no nesting—all items at the same level:

```jsx
const flatData = [
  { Product: 'Laptop', Sales: 2500 },
  { Product: 'Phone', Sales: 3200 },
  { Product: 'Tablet', Sales: 1800 },
  { Product: 'Watch', Sales: 900 }
];

<TreeMapComponent
  dataSource={flatData}
  weightValuePath="Sales"
  leafItemSettings={{ labelPath: 'Product' }}
/>
```

**Use case:** Simple category-based comparisons without hierarchy.

### Hierarchical Data Structure

Hierarchical data contains parent-child relationships:

```jsx
const hierarchicalData = [
  { Category: 'Fruits', Type: 'Tropical', Item: 'Mango', Sales: 3000 },
  { Category: 'Fruits', Type: 'Tropical', Item: 'Banana', Sales: 500 },
  { Category: 'Fruits', Type: 'Citrus', Item: 'Orange', Sales: 2300 },
  { Category: 'Fruits', Type: 'Citrus', Item: 'Lemon', Sales: 1200 }
];

import { LevelsDirective, LevelDirective } from '@syncfusion/ej2-react-treemap';

<TreeMapComponent
  dataSource={hierarchicalData}
  weightValuePath="Sales"
  leafItemSettings={{ labelPath: 'Item' }}
>
  <LevelsDirective>
    <LevelDirective groupPath="Category" />
    <LevelDirective groupPath="Type" />
  </LevelsDirective>
</TreeMapComponent>
```

**Use case:** Exploring nested categories (e.g., regions → states → cities).

### Data Binding Tips

- **weightValuePath:** Must reference a numeric property for proper sizing
- **labelPath in leafItemSettings:** Required to display item labels
- **groupPath in Levels:** Define hierarchy order (top level first)
- **Empty data:** TreeMap renders empty but no error occurs

## Next Steps

- **Color Mapping:** See [color-mapping.md](color-mapping.md) for applying colors to items
- **Hierarchies:** See [drilldown.md](drilldown.md) for multi-level exploration
- **Layouts:** See [layouts.md](layouts.md) for different spatial arrangements
