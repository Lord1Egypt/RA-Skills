# Getting Started with Tabs

## Table of Contents
- [Dependencies](#dependencies)
- [Project Setup](#project-setup)
- [CSS Imports](#css-imports)
- [Basic Tab Initialization](#basic-tab-initialization)
- [Running the Application](#running-the-application)

## Dependencies

The Tab component requires the `@syncfusion/ej2-react-navigations` package and its dependencies. The complete dependency tree is:

```
@syncfusion/ej2-react-navigations
├── @syncfusion/ej2-base
├── @syncfusion/ej2-react-base
└── @syncfusion/ej2-navigations
    ├── @syncfusion/ej2-buttons
    └── @syncfusion/ej2-popups
```

Install the required package:

```bash
npm install @syncfusion/ej2-react-navigations --save
```

This single command installs all required dependencies automatically.

## Project Setup

### Option 1: Setup with Vite (Recommended)

Vite provides faster development builds and smaller bundle sizes compared to Create React App.

**Create a new React application:**

```bash
npm create vite@latest my-tab-app -- --template react
cd my-tab-app
npm run dev
```

**For TypeScript support:**

```bash
npm create vite@latest my-tab-app -- --template react-ts
cd my-tab-app
npm run dev
```

**Install Syncfusion Tab package:**

```bash
npm install @syncfusion/ej2-react-navigations --save
```

### Option 2: Setup with Create React App

If you prefer Create React App, follow the official setup:

```bash
npx create-react-app my-tab-app
cd my-tab-app
npm install @syncfusion/ej2-react-navigations --save
npm start
```

> For detailed Create React App setup, refer to the [official Create React App documentation](https://ej2.syncfusion.com/react/documentation/getting-started/create-app).

## CSS Imports

The Tab component requires CSS files for styling. Add these imports to your `src/App.css` file:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-navigations/styles/tailwind3.css';
```

Then import the CSS in your `src/App.tsx` (or `src/App.jsx`):

```jsx
import './App.css';
```

**Why these imports?**

- **ej2-base**: Core Syncfusion styles and utilities
- **ej2-buttons**: Required for button styling in Tab icons
- **ej2-popups**: Required for dropdown/popup overflow functionality
- **ej2-react-navigations**: Tab-specific component styles

## Basic Tab Initialization

### Step 1: Import Tab Components

In your `src/App.tsx` file, import the necessary components:

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import './App.css';
```

### Step 2: Create Tab Items

Define your tab data structure with headers and content:

```jsx
const tabItems = [
  {
    header: { text: 'Home' },
    content: 'Welcome to the home tab. You can add any content here.'
  },
  {
    header: { text: 'Profile' },
    content: 'User profile information goes here.'
  },
  {
    header: { text: 'Settings' },
    content: 'Application settings and preferences.'
  }
];
```

### Step 3: Render the Tab Component

Create your React component:

```jsx
export default function App() {
  const tabItems = [
    {
      header: { text: 'Home' },
      content: 'Welcome to the home tab'
    },
    {
      header: { text: 'Profile' },
      content: 'User profile information'
    },
    {
      header: { text: 'Settings' },
      content: 'Application settings'
    }
  ];

  return (
    <div className="App">
      <h1>Tab Component Example</h1>
      <TabComponent>
        <TabItemsDirective>
          {tabItems.map((item, index) => (
            <TabItemDirective 
              key={index} 
              header={item.header} 
              content={item.content} 
            />
          ))}
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Complete App.tsx Example

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-react-navigations/styles/tailwind3.css';
import './App.css';

export default function App() {
  const tabItems = [
    {
      header: { text: 'HTML' },
      content: 'HTML is the standard markup language for creating web pages.'
    },
    {
      header: { text: 'CSS' },
      content: 'CSS is used for styling and layout of web pages.'
    },
    {
      header: { text: 'JavaScript' },
      content: 'JavaScript is a programming language for interactive web pages.'
    }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>My First Tab Component</h1>
      <TabComponent>
        <TabItemsDirective>
          {tabItems.map((item, index) => (
            <TabItemDirective 
              key={index}
              header={item.header}
              content={item.content}
            />
          ))}
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

## Running the Application

### With Vite:

```bash
npm run dev
```

Output:
```
  VITE v5.0.0  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Open your browser to `http://localhost:5173/` to see your Tab component.

### With Create React App:

```bash
npm start
```

The app will automatically open in your default browser at `http://localhost:3000/`.

## Minimal Working Example (MWE)

If you want the absolute minimum code to get started:

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-react-navigations/styles/tailwind3.css';

export default function App() {
  return (
    <TabComponent>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content='Content 1' />
        <TabItemDirective header={{ text: 'Tab 2' }} content='Content 2' />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

This renders a basic Tab component with two tabs and default styling.

## Next Steps

- **For styling**: Read the header-styling.md guide to customize tab appearance
- **For responsive layouts**: Read orientation-overflow.md to control header position and overflow handling
- **For advanced content**: Read content-rendering.md to understand performance implications of different rendering modes
