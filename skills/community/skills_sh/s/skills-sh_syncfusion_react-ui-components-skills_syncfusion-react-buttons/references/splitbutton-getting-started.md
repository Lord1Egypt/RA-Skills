# Getting Started with SplitButton Component

## Table of Contents
- [Installation](#installation)
- [Module Setup](#module-setup)
- [CSS Imports](#css-imports)
- [Basic Implementation](#basic-implementation)
- [Component Registration](#component-registration)
- [Running the Application](#running-the-application)

## Installation

Install the Syncfusion SplitButton package using npm or ng add:

```bash
# Using npm
npm install @syncfusion/ej2-react-splitbuttons

# Or using ng add (recommended)
ng add @syncfusion/ej2-react-splitbuttons
```

### Dependencies

The SplitButton component requires the following:
- `@syncfusion/ej2-base` - Core utilities
- `@syncfusion/ej2-buttons` - Button controls
- React 16.8+ (for hooks support)

```bash
npm install @syncfusion/ej2-base @syncfusion/ej2-buttons
```

## Module Setup

### Using SplitButtonComponent (Recommended)

Import `SplitButtonComponent` in your React component:

```tsx
// App.tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
};

export default App;
```

### Functional Component Setup (Hooks)

```tsx
// SaveButton.tsx
import React, { useState } from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { ItemModel } from '@syncfusion/ej2-react-splitbuttons';

interface SaveButtonProps {
  onSave?: (action: string) => void;
}

const SaveButton: React.FC<SaveButtonProps> = ({ onSave }) => {
  const [items] = useState<ItemModel[]>([
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ]);

  const handleSelect = (args: any) => {
    console.log('Selected:', args.item.text);
    onSave?.(args.item.text);
  };

  const handleClick = () => {
    console.log('Primary action clicked');
    onSave?.('Save');
  };

  return (
    <SplitButtonComponent
      items={items}
      click={handleClick}
      select={handleSelect}
      cssClass="e-primary"
      iconCss="e-icons e-save"
    >
      Save
    </SplitButtonComponent>
  );
};

export default SaveButton;
```

### Class Component Setup

```tsx
// SaveButtonClass.tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { ItemModel } from '@syncfusion/ej2-react-splitbuttons';

interface State {
  items: ItemModel[];
}

class SaveButtonClass extends React.Component<{}, State> {
  constructor(props: {}) {
    super(props);
    this.state = {
      items: [
        { text: 'Save' },
        { text: 'Save As' },
        { text: 'Save All' }
      ]
    };
  }

  handleSelect = (args: any) => {
    console.log('Selected:', args.item.text);
  };

  handleClick = () => {
    console.log('Primary action clicked');
  };

  render() {
    return (
      <SplitButtonComponent
        items={this.state.items}
        click={this.handleClick}
        select={this.handleSelect}
        cssClass="e-primary"
      >
        Save
      </SplitButtonComponent>
    );
  }
}

export default SaveButtonClass;
```

## CSS Imports

Import the SplitButton theme CSS. Choose one of the available themes:

### In Component

```tsx
// App.tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material3.css';

function App() {
  const items = [{ text: 'Save' }, { text: 'Save As' }];
  
  return (
    <SplitButtonComponent items={items}>
      Save
    </SplitButtonComponent>
  );
}

export default App;
```

### In Global Styles

```css
/* index.css or styles.css */
@import '../node_modules/@syncfusion/ej2-base/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-react-splitbuttons/styles/material3.css';
```

### Available Themes

- **material3.css** - Material Design 3 (default, recommended)
- **bootstrap5.css** - Bootstrap 5 theme
- **bootstrap4.css** - Bootstrap 4 theme
- **fluent.css** - Microsoft Fluent Design
- **fabric.css** - Office Fabric theme
- **tailwind.css** - Tailwind CSS theme
- **highcontrast.css** - High contrast accessibility theme

**Choose one theme per application to avoid conflicts.**

### Theme Colors Available

```css
/* Material3 theme colors */
.e-primary    /* Blue */
.e-success    /* Green */
.e-info       /* Cyan */
.e-warning    /* Orange */
.e-danger     /* Red */
```

## Basic Implementation

### Simple SplitButton

```tsx
// App.tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material.css';

function App() {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  const handleMenuSelect = (args: any) => {
    alert(`You selected: ${args.item.text}`);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Save Options</h2>
      <SplitButtonComponent
        items={items}
        select={handleMenuSelect}
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default App;
```

### SplitButton with Icon

```tsx
// IconedSplitButton.tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material.css';

function IconedSplitButton() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-save"
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default IconedSplitButton;
```

### SplitButton with Event Handling

```tsx
// EventHandlingSplitButton.tsx
import React, { useState } from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material.css';

function EventHandlingSplitButton() {
  const [status, setStatus] = useState('Ready');

  const items = [
    { text: 'Send Now' },
    { text: 'Schedule Send' },
    { text: 'Send Test' }
  ];

  const handlePrimaryClick = () => {
    setStatus('Sending email...');
    console.log('Email sent immediately');
    setTimeout(() => setStatus('Email sent successfully!'), 1500);
  };

  const handleMenuSelect = (args: any) => {
    setStatus(`${args.item.text} initiated`);
    console.log('Menu item:', args.item.text);
  };

  const handleBeforeOpen = (args: any) => {
    console.log('Dropdown menu is about to open');
  };

  const handleOpen = (args: any) => {
    console.log('Dropdown menu opened');
  };

  const handleClose = (args: any) => {
    console.log('Dropdown menu closed');
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Email Actions</h2>
      <SplitButtonComponent
        items={items}
        click={handlePrimaryClick}
        select={handleMenuSelect}
        beforeOpen={handleBeforeOpen}
        open={handleOpen}
        close={handleClose}
        cssClass="e-primary"
        iconCss="e-icons e-mail"
      >
        Send
      </SplitButtonComponent>
      <p style={{ marginTop: '20px', fontSize: '16px' }}>
        Status: <strong>{status}</strong>
      </p>
    </div>
  );
}

export default EventHandlingSplitButton;
```

## Component Registration

### Register with useRef (for imperative access)

```tsx
import React, { useRef, useEffect } from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function RefAccessExample() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  useEffect(() => {
    if (splitBtnRef.current) {
      console.log('SplitButton instance:', splitBtnRef.current);
    }
  }, []);

  const handleButtonClick = () => {
    if (splitBtnRef.current) {
      // Access component methods
      console.log('Element:', splitBtnRef.current.element);
    }
  };

  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <div>
      <SplitButtonComponent
        ref={splitBtnRef}
        items={items}
        cssClass="e-primary"
      >
        Action
      </SplitButtonComponent>
      <button onClick={handleButtonClick} style={{ marginLeft: '10px' }}>
        Log Component
      </button>
    </div>
  );
}

export default RefAccessExample;
```

### Register with useEffect (lifecycle hooks)

```tsx
import React, { useEffect, useRef } from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function LifecycleExample() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  useEffect(() => {
    // Component mounted
    console.log('SplitButton mounted');

    return () => {
      // Component unmounted
      console.log('SplitButton unmounted');
    };
  }, []);

  const items = [{ text: 'Save' }, { text: 'Save As' }];

  const handleCreated = () => {
    console.log('SplitButton component created');
  };

  const handleDestroy = () => {
    console.log('SplitButton component destroyed');
  };

  return (
    <SplitButtonComponent
      ref={splitBtnRef}
      items={items}
      created={handleCreated}
      destroy={handleDestroy}
    >
      Save
    </SplitButtonComponent>
  );
}

export default LifecycleExample;
```

## Running the Application

### Development Server

```bash
# Start the development server
npm start

# Or with custom port
npm start -- --port 3000

# Navigate to
http://localhost:3000
```

### Build for Production

```bash
# Create optimized production build
npm run build

# Output goes to build/ folder
npm install -g serve
serve -s build

# Navigate to
http://localhost:3000
```

### With TypeScript

```bash
# Create React App with TypeScript
npx create-react-app my-app --template typescript
cd my-app

# Install Syncfusion SplitButton
npm install @syncfusion/ej2-react-splitbuttons

# Start development server
npm start
```

### With Vite

```bash
# Create Vite + React + TypeScript project
npm create vite@latest my-app -- --template react-ts
cd my-app

# Install Syncfusion SplitButton
npm install @syncfusion/ej2-react-splitbuttons

# Install dependencies
npm install

# Start development server
npm run dev
```

## Troubleshooting

### Issue: "Cannot find module '@syncfusion/ej2-react-splitbuttons'"
**Solution:**
- Run `npm install @syncfusion/ej2-react-splitbuttons`
- Verify package.json has the dependency
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### Issue: CSS/Styles not applied

**Solution:**
- Verify CSS import path in component or global styles
- Check theme file exists in `node_modules/@syncfusion/ej2-buttons/styles/`
- Ensure `@import` statement comes before component styles
- Import icons CSS if using icons: `@import '@syncfusion/ej2-icons/styles/material.css';`

### Issue: Menu items not displaying

**Solution:**
- Verify `items` array is passed correctly
- Check items have `text` property
- Ensure CSS is imported for dropdown styling
- Check browser console for errors

### Issue: Events not firing

**Solution:**
- Verify event handler function is defined correctly
- Check function parameters match event type
- Use arrow functions to maintain `this` context in class components
- Verify no typos in event names (click, select, beforeOpen, etc.)

### Issue: Icons not showing

**Solution:**
- Import Syncfusion icons CSS: `@import '@syncfusion/ej2-icons/styles/material.css';`
- Verify icon class names are correct (e.g., 'e-icons e-save')
- Check icon font files are in node_modules

### Issue: TypeScript errors with imports

**Solution:**
- Update imports to use correct types:
  ```tsx
  import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
  import { ItemModel } from '@syncfusion/ej2-react-splitbuttons';
  ```
- Install type definitions: `npm install --save-dev @types/react`

## Next Steps

1. **Styling & Appearance** → Read [types-and-styles.md](types-and-styles.md) for button styles and customization
2. **Features** → Read [splitbutton-features.md](splitbutton-features.md) for advanced features and events
3. **API Reference** → Read [api-reference.md](api-reference.md) for complete property documentation
4. **Customization** → Read [customization.md](customization.md) for advanced styling and templates
5. **Accessibility** → Read [accessibility.md](accessibility.md) for WCAG compliance

## Complete Example Project

```bash
# Create new React project
npx create-react-app splitbutton-demo
cd splitbutton-demo

# Add Syncfusion SplitButton
npm install @syncfusion/ej2-react-splitbuttons

# Start development server
npm start
```

### Minimal Working Example

**src/App.tsx:**
```tsx
import React from 'react';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material3.css';
import './App.css';

function App() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  const handleSelect = (args: any) => {
    console.log('Selected:', args.item.text);
  };

  return (
    <div className="app-container">
      <h1>SplitButton Demo</h1>
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        select={handleSelect}
        iconCss="e-icons e-save"
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default App;
```

**src/App.css:**
```css
.app-container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.app-container h1 {
  color: #333;
  margin-bottom: 20px;
}
```

Your SplitButton is now ready to use!
