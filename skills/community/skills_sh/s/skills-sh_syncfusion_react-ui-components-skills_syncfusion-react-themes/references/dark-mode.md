# Dark Mode Implementation

## Table of Contents
- [Overview](#overview)
- [Global Dark Mode](#global-dark-mode)
- [Per-Component Dark Mode](#per-component-dark-mode)
- [Runtime Theme Switching](#runtime-theme-switching)

## Overview

Syncfusion React themes support both light and dark variants. Dark mode is toggled by applying the `e-dark-mode` CSS class to the `<body>` element or specific component containers.

**Supported themes with dark variants:**
- Tailwind 3.4 → tailwind3.css (light), tailwind3-dark.css (dark)
- Bootstrap 5.3 → bootstrap5.3.css (light), bootstrap5.3-dark.css (dark)
- Fluent 2 → fluent2.css (light), fluent2-dark.css (dark)
- Material 3 → material3.css (light), material3-dark.css (dark)

**How it works:**
- Import ONE theme CSS file (e.g., `tailwind3.css`)
- Apply `e-dark-mode` class to switch to dark variant
- Remove `e-dark-mode` class to return to light variant
- No need to import separate dark CSS files

## Global Dark Mode

Apply dark mode to all Syncfusion components by adding `e-dark-mode` to the `<body>` element.

### Static Dark Mode

```html
<!-- index.html -->
<body class="e-dark-mode">
  <div id="root"></div>
</body>
```

### Dynamic Dark Mode with State

```typescript
import React, { useState } from 'react';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleDarkModeToggle = (event) => {
    const checked = event.checked ?? false;
    setIsDarkMode(checked);
    
    if (checked) {
      document.body.classList.add('e-dark-mode');
    } else {
      document.body.classList.remove('e-dark-mode');
    }
  };

  return (
    <div>
      <CheckBoxComponent 
        label="Enable Dark Mode" 
        checked={isDarkMode} 
        change={handleDarkModeToggle}
      />
      <ButtonComponent cssClass="e-primary">Sample Button</ButtonComponent>
    </div>
  );
}

export default App;
```

## Per-Component Dark Mode

Apply dark mode to specific components or sections by adding `e-dark-mode` to the component's container.

```typescript
import React from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  return (
    <div>
      <h2>Light Mode Section</h2>
      <div>
        <ButtonComponent cssClass="e-primary">Light Button</ButtonComponent>
      </div>
      
      <h2>Dark Mode Section</h2>
      <div className="e-dark-mode">
        <ButtonComponent cssClass="e-primary">Dark Button</ButtonComponent>
      </div>
    </div>
  );
}

export default App;
```

### Multiple Sections with Different Modes

```typescript
import React from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { GridComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-grids';

function App() {
  const data = [
    { OrderID: 10248, CustomerID: 'VINET', Freight: 32.38 },
    { OrderID: 10249, CustomerID: 'TOMSP', Freight: 11.61 }
  ];

  return (
    <div>
      {/* Light mode navigation */}
      <div className="nav-section">
        <ButtonComponent>Home</ButtonComponent>
        <ButtonComponent>About</ButtonComponent>
      </div>
      
      {/* Dark mode content area */}
      <div className="e-dark-mode content-section">
        <GridComponent dataSource={data}>
          <ColumnsDirective>
            <ColumnDirective field='OrderID' width='100' />
            <ColumnDirective field='CustomerID' width='100' />
            <ColumnDirective field='Freight' width='100' format="C2" />
          </ColumnsDirective>
        </GridComponent>
      </div>
    </div>
  );
}

export default App;
```

## Runtime Theme Switching

### With localStorage Persistence

```typescript
import React, { useState, useEffect } from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Initialize from localStorage
    const saved = localStorage.getItem('darkMode');
    return saved === 'true';
  });

  useEffect(() => {
    // Apply dark mode class on mount and when changed
    if (isDarkMode) {
      document.body.classList.add('e-dark-mode');
    } else {
      document.body.classList.remove('e-dark-mode');
    }
    
    // Save to localStorage
    localStorage.setItem('darkMode', isDarkMode.toString());
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div>
      <ButtonComponent onClick={toggleDarkMode}>
        Toggle {isDarkMode ? 'Light' : 'Dark'} Mode
      </ButtonComponent>
    </div>
  );
}

export default App;
```

### With System Preference Detection

```typescript
import React, { useState, useEffect } from 'react';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Check system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    // Listen for system preference changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e) => {
      setIsDarkMode(e.matches);
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  useEffect(() => {
    // Apply dark mode class
    if (isDarkMode) {
      document.body.classList.add('e-dark-mode');
    } else {
      document.body.classList.remove('e-dark-mode');
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div>
      <p>Current mode: {isDarkMode ? 'Dark' : 'Light'}</p>
      <ButtonComponent onClick={toggleDarkMode}>
        Override System Preference
      </ButtonComponent>
    </div>
  );
}

export default App;
```
