# Getting Started with Sankey Chart

## Table of Contents
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Installing Syncfusion Sankey Package](#installing-syncfusion-sankey-package)
  - [Package Dependencies](#package-dependencies)
- [Setting Up Your React Environment](#setting-up-your-react-environment)
  - [Using Vite (Recommended)](#using-vite-recommended)
  - [Using Create React App](#using-create-react-app)
- [Basic Sankey Component Setup](#basic-sankey-component-setup)
  - [Minimal Example](#minimal-example)
- [Module Injection](#module-injection)
  - [Available Modules](#available-modules)
  - [Injecting Modules](#injecting-modules)
- [Real-World Example with Data](#real-world-example-with-data)
- [Running Your Application](#running-your-application)
- [Next Steps](#next-steps)

## Installation and Setup

### Prerequisites
- Node.js version 14 or later
- React 16.8 or higher
- Basic knowledge of React and TypeScript (recommended)
- A code editor like Visual Studio Code

### Installing Syncfusion Sankey Package

All Essential JS 2 packages are published in the [npmjs.com](https://www.npmjs.com/~syncfusionorg) public registry.

Install the React Charts package containing the Sankey component:

```bash
npm install @syncfusion/ej2-react-charts --save
```

The `--save` flag includes the package in your `package.json` dependencies.

### Package Dependencies

The Sankey Chart relies on several Syncfusion packages:

```
@syncfusion/ej2-react-charts
  ├── @syncfusion/ej2-base
  ├── @syncfusion/ej2-data
  ├── @syncfusion/ej2-charts
  ├── @syncfusion/ej2-react-base
  ├── @syncfusion/ej2-pdf-export
  ├── @syncfusion/ej2-file-utils
  ├── @syncfusion/ej2-compression
  └── @syncfusion/ej2-svg-base
```

All dependencies are automatically installed with the main package.

## Setting Up Your React Environment

### Using Vite (Recommended)

Vite provides fast development with instant HMR (Hot Module Replacement):

```bash
npm create vite@latest my-sankey-app
```

When prompted, select React and your preferred variant (JavaScript or TypeScript).

**For TypeScript:**
```bash
npm create vite@latest my-sankey-app -- --template react-ts
cd my-sankey-app
npm run dev
```

**For JavaScript:**
```bash
npm create vite@latest my-sankey-app -- --template react
cd my-sankey-app
npm run dev
```

### Using Create React App

Alternatively, use create-react-app (slower build but widely familiar):

```bash
npx create-react-app my-sankey-app
cd my-sankey-app
npm start
```

## Basic Sankey Component Setup

### Minimal Example

Create a basic Sankey chart in your `App.tsx` or `App.jsx`:

```tsx
import React from 'react';
import {
  SankeyComponent,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective,
  Inject
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <SankeyComponent
        width="90%"
        height="420px"
        title="Simple Sankey Chart"
      >
        <SankeyNodesCollectionDirective>
          <SankeyNodeDirective id="A" label={{ text: 'Node A' }} />
          <SankeyNodeDirective id="B" label={{ text: 'Node B' }} />
          <SankeyNodeDirective id="C" label={{ text: 'Node C' }} />
        </SankeyNodesCollectionDirective>
        <SankeyLinksCollectionDirective>
          <SankeyLinkDirective sourceId="A" targetId="B" value={100} />
          <SankeyLinkDirective sourceId="B" targetId="C" value={80} />
        </SankeyLinksCollectionDirective>
      </SankeyComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Understanding the Structure

- **SankeyComponent** - The main container for the diagram
- **SankeyNodeDirective** - Defines individual nodes (categories)
- **SankeyLinkDirective** - Defines connections between nodes with flow values
- **width/height** - Dimensions for the chart (supports %, px)
- **title** - Display text shown above the diagram

## Module Injection

The Sankey Chart requires explicit module injection to enable features like tooltips, legends, and export functionality.

### Available Modules

```tsx
import {
  SankeyTooltip,      // Enable tooltip on hover
  SankeyLegend,       // Show legend
  SankeyExport        // Enable export functionality
} from '@syncfusion/ej2-react-charts';
```

### Injecting Modules

Add modules to your component using the `<Inject>` component:

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="Chart with Features"
  tooltip={{ enable: true }}
  legendSettings={{ visible: true }}
>
  <SankeyNodesCollectionDirective>
    {/* nodes */}
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    {/* links */}
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend, SankeyExport]} />
</SankeyComponent>
```

## Real-World Example with Data

Here's a practical energy flow diagram:

```tsx
import React from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function EnergyFlowDashboard() {
  return (
    <div className="control-pane">
      <div className="control-section">
        <SankeyComponent
          width="90%"
          height="450px"
          title="2024 Energy Consumption"
          subTitle="By Source and Sector"
          tooltip={{ enable: true }}
          legendSettings={{ visible: true, position: 'Bottom' }}
        >
          <SankeyNodesCollectionDirective>
            <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
            <SankeyNodeDirective id="Wind" label={{ text: 'Wind' }} />
            <SankeyNodeDirective id="Natural Gas" label={{ text: 'Natural Gas' }} />
            <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
            <SankeyNodeDirective id="Residential" label={{ text: 'Residential' }} />
            <SankeyNodeDirective id="Commercial" label={{ text: 'Commercial' }} />
            <SankeyNodeDirective id="Industrial" label={{ text: 'Industrial' }} />
          </SankeyNodesCollectionDirective>
          <SankeyLinksCollectionDirective>
            <SankeyLinkDirective sourceId="Solar" targetId="Generation" value={450} />
            <SankeyLinkDirective sourceId="Wind" targetId="Generation" value={200} />
            <SankeyLinkDirective sourceId="Natural Gas" targetId="Generation" value={800} />
            <SankeyLinkDirective sourceId="Generation" targetId="Residential" value={300} />
            <SankeyLinkDirective sourceId="Generation" targetId="Commercial" value={400} />
            <SankeyLinkDirective sourceId="Generation" targetId="Industrial" value={350} />
          </SankeyLinksCollectionDirective>
          <Inject services={[SankeyTooltip, SankeyLegend]} />
        </SankeyComponent>
      </div>
    </div>
  );
}

export default EnergyFlowDashboard;
ReactDOM.render(<EnergyFlowDashboard />, document.getElementById("charts"));
```

## Running Your Application

Start the development server:

```bash
npm run dev
```

Your Sankey Chart will be available at `http://localhost:5173` (Vite) or `http://localhost:3000` (Create React App).

## Next Steps

- **Configure Nodes & Links** - Learn about node positioning and link styling in [Nodes and Links Configuration](nodes-and-links.md)
- **Add Labels** - Customize text and positioning in [Labels and Positioning](labels-and-positioning.md)
- **Enable Interactivity** - Add tooltips and events in [Interactivity and Events](interactivity.md)
