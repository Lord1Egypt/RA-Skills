# Getting Started with React Sidebar

## Table of Contents
- [Installation](#installation)
  - [1. Install Syncfusion Packages](#1-install-syncfusion-packages)
  - [2. Import CSS Styles](#2-import-css-styles)
  - [3. Import Components](#3-import-components)
- [Basic Sidebar Implementation](#basic-sidebar-implementation)
  - [Minimal Example](#minimal-example)
  - [With State Management](#with-state-management)
  - [With Toggle Button](#with-toggle-button)
- [Theme Configuration](#theme-configuration)
- [RTL (Right-to-Left) Support](#rtl-right-to-left-support)
- [Responsive Sidebar](#responsive-sidebar)
- [Complete Setup Example](#complete-setup-example)

---

## Installation

### 1. Install Syncfusion Packages

Install the required packages using npm:

```bash
npm install @syncfusion/ej2-react-navigations
npm install @syncfusion/ej2-react-buttons
```

For Material or Bootstrap themes:
```bash
npm install @syncfusion/ej2-base
npm install @syncfusion/ej2-theme-bootstrap5
npm install @syncfusion/ej2-theme-material
```

### 2. Import CSS Styles

Add theme CSS imports to your application entry point (`index.js` or `main.jsx`):

```jsx
// Default theme
import '@syncfusion/ej2-navigations/styles/material.css';

// Or choose another theme:
// import '@syncfusion/ej2-navigations/styles/bootstrap5.css';
// import '@syncfusion/ej2-navigations/styles/fluent.css';
// import '@syncfusion/ej2-navigations/styles/tailwind.css';

// Import base styles
import '@syncfusion/ej2-base/styles/material.css';
```

### 3. Import Components

```jsx
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
```

---

## Basic Sidebar Implementation

### Minimal Example

```jsx
import React from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-navigations/styles/material.css';

function App() {
  return (
    <SidebarComponent width="250px">
      <h3>Sidebar Content</h3>
      <p>This is a basic sidebar.</p>
    </SidebarComponent>
  );
}

export default App;
```

### With State Management

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="container">
      <ButtonComponent onClick={handleToggle}>
        Toggle Sidebar
      </ButtonComponent>

      <SidebarComponent
        width="250px"
        isOpen={isOpen}
        change={() => setIsOpen(!isOpen)}
        type="Over"
      >
        <h3>Navigation</h3>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#services">Services</a></li>
        </ul>
      </SidebarComponent>

      <div className="main-content">
        <h1>Main Content Area</h1>
      </div>
    </div>
  );
}

export default App;
```

---

## CSS Theme Configuration

### Theme Options

Syncfusion provides multiple built-in themes:

| Theme | CSS File | Best For |
|-------|----------|----------|
| Material | `material.css` | Modern Material Design |
| Bootstrap | `bootstrap5.css` | Bootstrap-styled apps |
| Fluent | `fluent.css` | Microsoft Fluent Design |
| Tailwind | `tailwind.css` | Tailwind CSS projects |

### Applying Themes

```jsx
// In index.js or main.jsx

// Material Theme (Default)
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-base/styles/material.css';

// Bootstrap Theme
// import '@syncfusion/ej2-navigations/styles/bootstrap5.css';
// import '@syncfusion/ej2-base/styles/bootstrap5.css';
```

### Custom Theme with CSS

```css
/* Custom styles in your CSS file */

/* Sidebar background */
.e-sidebar {
  background-color: #f5f5f5;
  border-right: 1px solid #ddd;
}

/* Sidebar header */
.e-sidebar h3 {
  color: #333;
  padding: 20px;
  border-bottom: 1px solid #ddd;
}

/* Navigation links */
.e-sidebar ul li a {
  color: #555;
  padding: 12px 20px;
  display: block;
  text-decoration: none;
  transition: background-color 0.3s;
}

.e-sidebar ul li a:hover {
  background-color: #e3f2fd;
  color: #1976d2;
}
```

---

## Initial State Management

### Control Sidebar Open State

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  // Start with sidebar open
  const [isOpen, setIsOpen] = useState(true);

  const handleChange = (args) => {
    const sidebarElement = args.element;
    const nowOpen = sidebarElement.classList.contains('e-open');
    setIsOpen(nowOpen);
  };

  return (
    <SidebarComponent
      isOpen={isOpen}
      change={handleChange}
      type="Push"
      width="250px"
    >
      {/* Content */}
    </SidebarComponent>
  );
}

export default App;
```

### Using useRef for Direct Control

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleShowClick = () => {
    if (sidebarRef.current) {
      sidebarRef.current.show();
    }
  };

  const handleHideClick = () => {
    if (sidebarRef.current) {
      sidebarRef.current.hide();
    }
  };

  const handleToggleClick = () => {
    if (sidebarRef.current) {
      sidebarRef.current.toggle();
    }
  };

  return (
    <div>
      <div>
        <button onClick={handleShowClick}>Show</button>
        <button onClick={handleHideClick}>Hide</button>
        <button onClick={handleToggleClick}>Toggle</button>
      </div>

      <SidebarComponent
        ref={sidebarRef}
        width="250px"
        type="Over"
      >
        Sidebar Content
      </SidebarComponent>
    </div>
  );
}

export default App;
```

---

## RTL (Right-to-Left) Support

### Enable RTL for Arabic/Hebrew Languages

```jsx
<SidebarComponent
  enableRtl={true}
  position="Right"
  type="Over"
  width="250px"
>
  محتوى الشريط الجانبي {/* Arabic content */}
</SidebarComponent>
```

### RTL CSS Adjustments

```css
/* RTL specific styles */
body[dir="rtl"] .e-sidebar {
  border-right: none;
  border-left: 1px solid #ddd;
}

body[dir="rtl"] .e-sidebar ul {
  text-align: right;
}
```

---

## Responsive Sidebar Implementation

### Responsive Layout with Bootstrap

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="container-fluid">
      {/* Header */}
      <header className="navbar navbar-light bg-light">
        <div className="container-fluid">
          <ButtonComponent
            cssClass="btn-primary"
            onClick={() => setIsOpen(!isOpen)}
          >
            ☰ Menu
          </ButtonComponent>
          <span className="navbar-brand">My App</span>
        </div>
      </header>

      <div className="row">
        {/* Sidebar - Responsive */}
        <div className="col-md-3">
          <SidebarComponent
            width="100%"
            isOpen={isOpen}
            type="Over"
            showBackdrop={true}
            closeOnDocumentClick={true}
          >
            <ul className="list-unstyled">
              <li><a href="#home">Home</a></li>
              <li><a href="#products">Products</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </SidebarComponent>
        </div>

        {/* Main Content - Responsive */}
        <div className="col-md-9">
          <h1>Main Content</h1>
          <p>Content area that adapts to screen size.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
```

---

## Complete Setup Example

```jsx
import React, { useState, useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import '@syncfusion/ej2-navigations/styles/material.css';
import '@syncfusion/ej2-base/styles/material.css';
import './App.css';

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const sidebarRef = useRef(null);

  const handleToggle = () => {
    if (sidebarRef.current) {
      sidebarRef.current.toggle();
    }
  };

  const handleChange = (args) => {
    const isOpen = args.element.classList.contains('e-open');
    setIsOpen(isOpen);
  };

  const handleNavItemClick = (e) => {
    if (e.target.tagName === 'A') {
      // Close sidebar on navigation
      if (sidebarRef.current) {
        sidebarRef.current.hide();
      }
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <ButtonComponent
          cssClass="e-btn e-icon-btn e-primary"
          onClick={handleToggle}
          title="Toggle Navigation"
        >
          <span className="e-btn-icon e-icons e-menu"></span>
        </ButtonComponent>
        <h1 className="app-title">My Application</h1>
      </header>

      {/* Main Layout */}
      <div className="app-layout">
        {/* Sidebar */}
        <SidebarComponent
          ref={sidebarRef}
          id="sidebar"
          width="280px"
          type="Over"
          isOpen={isOpen}
          position="Left"
          change={handleChange}
          showBackdrop={true}
          closeOnDocumentClick={true}
          animate={true}
        >
          <div className="sidebar-content" onClick={handleNavItemClick}>
            <h3>Navigation Menu</h3>
            <nav className="nav-menu">
              <a href="#home" className="nav-item">🏠 Home</a>
              <a href="#products" className="nav-item">📦 Products</a>
              <a href="#services" className="nav-item">🔧 Services</a>
              <a href="#about" className="nav-item">ℹ️ About Us</a>
              <a href="#contact" className="nav-item">📧 Contact</a>
            </nav>
          </div>
        </SidebarComponent>

        {/* Main Content */}
        <main className="main-content">
          <h2>Welcome to the Application</h2>
          <p>This is the main content area. Click the menu button to toggle the sidebar.</p>
        </main>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>&copy; 2024 My Application. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
```

### Corresponding CSS (App.css)

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #1976d2;
  color: white;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-title {
  margin: 0;
  font-size: 24px;
}

.app-layout {
  display: flex;
  flex: 1;
}

.sidebar-content {
  padding: 20px;
}

.sidebar-content h3 {
  color: #1976d2;
  margin-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 10px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-item {
  display: block;
  padding: 12px 15px;
  color: #555;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: #e3f2fd;
  color: #1976d2;
  padding-left: 20px;
}

.main-content {
  flex: 1;
  padding: 30px;
  background-color: white;
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.main-content h2 {
  color: #1976d2;
  margin-bottom: 15px;
}

.app-footer {
  background-color: #f0f0f0;
  padding: 20px;
  text-align: center;
  color: #666;
  border-top: 1px solid #ddd;
}

/* Responsive Design */
@media (max-width: 768px) {
  .app-header {
    flex-direction: row;
  }

  .main-content {
    margin: 10px;
    padding: 15px;
  }
}
```

---
