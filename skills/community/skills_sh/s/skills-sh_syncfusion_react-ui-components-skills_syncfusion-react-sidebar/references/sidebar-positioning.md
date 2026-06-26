# Sidebar Positioning & Behavior

## Table of Contents
- [Sidebar Types](#sidebar-types)
- [Position (Left/Right)](#position-leftright)
- [Width Configuration](#width-configuration)
- [Dock Mode](#dock-mode)
- [Multiple Sidebars](#multiple-sidebars)
- [Responsive Auto Mode](#responsive-auto-mode)

---

## Sidebar Types

The `type` property controls how the sidebar interacts with main content.

### Type: Over (Floating)

**Behavior:** Sidebar floats above the main content without pushing or shifting it.

**Best For:**
- Mobile drawer menus
- Modal-like sidebars
- Floating panels

**Example:**
```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="app">
      <ButtonComponent onClick={() => setIsOpen(!isOpen)}>
        ☰ Menu
      </ButtonComponent>

      <SidebarComponent
        type="Over"
        width="280px"
        isOpen={isOpen}
        change={() => setIsOpen(!isOpen)}
        showBackdrop={true}
        closeOnDocumentClick={true}
      >
        <h3>Over Type Sidebar</h3>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </SidebarComponent>

      <div className="content">
        <h1>Main Content Area</h1>
        <p>Content remains in same position when sidebar opens.</p>
      </div>
    </div>
  );
}

export default App;
```

### Type: Push (Content Shift)

**Behavior:** Sidebar pushes main content aside when open. Content width reduces to accommodate sidebar.

**Best For:**
- Desktop navigation layouts
- Persistent sidebars
- Dashboard layouts

**Example:**
```jsx
<SidebarComponent
  type="Push"
  width="250px"
  position="Left"
  isOpen={true}
  animate={true}
>
  <h3>Push Type Sidebar</h3>
  <ul>
    <li><a href="#profile">Profile</a></li>
    <li><a href="#settings">Settings</a></li>
    <li><a href="#logout">Logout</a></li>
  </ul>
</SidebarComponent>
```

### Type: Slide (Translate)

**Behavior:** Sidebar slides in without pushing content. Main content stays full-width but may be covered by sidebar.

**Best For:**
- Side panels
- Secondary navigation
- Complementary content areas

**Example:**
```jsx
<SidebarComponent
  type="Slide"
  width="300px"
  position="Right"
>
  <h3>Slide Type Sidebar</h3>
  <p>Sidebar slides without affecting main content layout.</p>
</SidebarComponent>
```

### Type: Auto (Responsive)

**Behavior:** Automatically switches type based on screen size.
- Mobile (< 768px): Over type
- Desktop (≥ 768px): Push type

**Best For:**
- Responsive applications
- Mobile-first designs

**Example:**
```jsx
<SidebarComponent
  type="Auto"
  width="250px"
  isOpen={false}
  mediaQuery="(min-width: 768px)"
>
  <h3>Auto Type Sidebar</h3>
  <p>Over on mobile, Push on desktop.</p>
</SidebarComponent>
```

**Type Comparison Table:**

| Type | Interaction | Content Movement | Use Case |
|------|-------------|------------------|----------|
| **Over** | Float above | None | Mobile menus |
| **Push** | Side-by-side | Shifts right | Desktop nav |
| **Slide** | Slide in | None/Covered | Panels |
| **Auto** | Responsive | Depends on screen | Responsive apps |

---

## Position (Left/Right)

The `position` property determines sidebar placement relative to content.

### Position: Left (Default)

**Standard for LTR languages (English, French, etc.)**

```jsx
<SidebarComponent
  position="Left"
  width="250px"
  type="Push"
>
  {/* Left-aligned sidebar */}
</SidebarComponent>
```

### Position: Right

**Standard for RTL languages (Arabic, Hebrew) or alternative layouts**

```jsx
<SidebarComponent
  position="Right"
  width="250px"
  type="Push"
  enableRtl={true}
>
  {/* Right-aligned sidebar */}
</SidebarComponent>
```

### CSS Layout with Left/Right Positioning

```css
/* Left positioned sidebar */
.sidebar-left {
  display: flex;
  flex-direction: row;
}

.sidebar-left .e-sidebar {
  order: 1;
}

.sidebar-left .main-content {
  order: 2;
  flex: 1;
}

/* Right positioned sidebar */
.sidebar-right {
  display: flex;
  flex-direction: row-reverse;
}

.sidebar-right .e-sidebar {
  order: 2;
}

.sidebar-right .main-content {
  order: 1;
  flex: 1;
}
```

---

## Width Configuration

### Fixed Width in Pixels

```jsx
<SidebarComponent width="250px" />
<SidebarComponent width="300px" />
```

### Responsive Width

```jsx
<SidebarComponent width="25%" />
<SidebarComponent width="100%" />
```

### Dynamic Width Based on Content

```jsx
<SidebarComponent width="auto">
  {/* Width auto-adjusts to content */}
</SidebarComponent>
```

### Width Adjustment Example

```jsx
function App() {
  const [sidebarWidth, setSidebarWidth] = useState('250px');

  const handleResize = () => {
    if (window.innerWidth < 768) {
      setSidebarWidth('80vw');  // 80% of viewport on mobile
    } else {
      setSidebarWidth('250px');  // Fixed on desktop
    }
  };

  React.useEffect(() => {
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <SidebarComponent width={sidebarWidth}>
      Responsive Sidebar
    </SidebarComponent>
  );
}
```

---

## Dock Mode

**Dock Mode** allows sidebars to collapse to a narrow "icon bar" while keeping functionality.

### Basic Dock Setup

```jsx
<SidebarComponent
  enableDock={true}
  dockSize="50px"       // Width when docked
  width="250px"         // Width when expanded
  type="Push"
>
  {/* Sidebar content */}
</SidebarComponent>
```

### Icon-Based Dock Navigation

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [isDocked, setIsDocked] = useState(false);

  return (
    <SidebarComponent
      enableDock={true}
      dockSize="50px"
      width="250px"
      type="Push"
    >
      {/* Icon bar when docked */}
      <div className="dock-icons">
        <a href="#home" className="nav-icon" title="Home">
          🏠
        </a>
        <a href="#search" className="nav-icon" title="Search">
          🔍
        </a>
        <a href="#profile" className="nav-icon" title="Profile">
          👤
        </a>
        <a href="#settings" className="nav-icon" title="Settings">
          ⚙️
        </a>
      </div>

      {/* Full labels when expanded */}
      <div className="expanded-menu" style={{ display: isDocked ? 'none' : 'block' }}>
        <nav>
          <a href="#home">🏠 Home</a>
          <a href="#search">🔍 Search</a>
          <a href="#profile">👤 Profile</a>
          <a href="#settings">⚙️ Settings</a>
        </nav>
      </div>
    </SidebarComponent>
  );
}

export default App;
```

### Dock CSS Styling

```css
/* Icon bar styling */
.e-sidebar.e-dock .dock-icons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 10px;
}

.e-sidebar.e-dock .dock-icons .nav-icon {
  font-size: 24px;
  cursor: pointer;
  padding: 10px;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.e-sidebar.e-dock .dock-icons .nav-icon:hover {
  background-color: #e3f2fd;
}

.e-sidebar.e-dock .expanded-menu {
  display: none;
}

/* When expanded */
.e-sidebar:not(.e-dock) .expanded-menu {
  display: block;
  padding: 20px;
}

.e-sidebar:not(.e-dock) .dock-icons {
  display: none;
}
```

---

## Multiple Sidebars

### Left and Right Sidebars

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [leftOpen, setLeftOpen] = useState(false);
  const [rightOpen, setRightOpen] = useState(false);

  return (
    <div className="multi-sidebar-layout">
      {/* Left Sidebar */}
      <SidebarComponent
        type="Push"
        position="Left"
        width="250px"
        isOpen={leftOpen}
        change={() => setLeftOpen(!leftOpen)}
      >
        <h3>Navigation</h3>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#products">Products</a></li>
          <li><a href="#services">Services</a></li>
        </ul>
      </SidebarComponent>

      {/* Main Content */}
      <main className="main-content">
        <h1>Main Content Area</h1>
        <p>Content between two sidebars</p>
      </main>

      {/* Right Sidebar */}
      <SidebarComponent
        type="Over"
        position="Right"
        width="280px"
        isOpen={rightOpen}
        change={() => setRightOpen(!rightOpen)}
        showBackdrop={true}
      >
        <h3>Properties</h3>
        <div className="properties-panel">
          <p>Right sidebar content here</p>
        </div>
      </SidebarComponent>
    </div>
  );
}

export default App;
```

### CSS for Multiple Sidebars

```css
.multi-sidebar-layout {
  display: flex;
  min-height: 100vh;
}

.multi-sidebar-layout .e-sidebar:first-child {
  order: 1;
}

.multi-sidebar-layout .main-content {
  order: 2;
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.multi-sidebar-layout .e-sidebar:last-child {
  order: 3;
}
```

---

## Responsive Auto Mode

### MediaQuery Configuration

```jsx
// Open on screens wider than 768px
<SidebarComponent
  type="Auto"
  mediaQuery="(min-width: 768px)"
  isOpen={false}
  width="250px"
/>
```

### Responsive Sidebar with Breakpoints

```jsx
import React, { useState, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [sidebarConfig, setSidebarConfig] = useState({
    type: 'Over',
    isOpen: false,
    width: '280px'
  });

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1200) {
        // Large screens: Push mode, always open
        setSidebarConfig({
          type: 'Push',
          isOpen: true,
          width: '280px'
        });
      } else if (window.innerWidth >= 768) {
        // Medium screens: Push mode, manual toggle
        setSidebarConfig({
          type: 'Push',
          isOpen: false,
          width: '250px'
        });
      } else {
        // Small screens: Over mode, modal-like
        setSidebarConfig({
          type: 'Over',
          isOpen: false,
          width: '80vw'
        });
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <SidebarComponent
      type={sidebarConfig.type}
      isOpen={sidebarConfig.isOpen}
      width={sidebarConfig.width}
      showBackdrop={sidebarConfig.type === 'Over'}
      closeOnDocumentClick={sidebarConfig.type === 'Over'}
    >
      Responsive Sidebar
    </SidebarComponent>
  );
}

export default App;
```

### CSS Media Queries for Responsive Layout

```css
/* Mobile */
@media (max-width: 767px) {
  .e-sidebar {
    width: 80vw !important;
    type: 'Over';
  }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1199px) {
  .e-sidebar {
    width: 250px !important;
  }
}

/* Desktop */
@media (min-width: 1200px) {
  .e-sidebar {
    width: 280px !important;
    display: flex; /* Always visible */
  }
}
```

---

## Complete Responsive Example

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const [config, setConfig] = useState({
    type: 'Over',
    isOpen: false,
    width: '280px'
  });
  const sidebarRef = useRef(null);

  useEffect(() => {
    const updateSidebar = () => {
      const width = window.innerWidth;
      if (width >= 1024) {
        setConfig({ type: 'Push', isOpen: true, width: '280px' });
      } else if (width >= 768) {
        setConfig({ type: 'Push', isOpen: false, width: '250px' });
      } else {
        setConfig({ type: 'Over', isOpen: false, width: '75vw' });
      }
    };

    updateSidebar();
    window.addEventListener('resize', updateSidebar);
    return () => window.removeEventListener('resize', updateSidebar);
  }, []);

  return (
    <div className="responsive-layout">
      <header>
        <ButtonComponent onClick={() => setConfig(c => ({ ...c, isOpen: !c.isOpen }))}>
          ☰ Menu
        </ButtonComponent>
        <h1>Responsive Sidebar App</h1>
      </header>

      <SidebarComponent
        ref={sidebarRef}
        type={config.type}
        isOpen={config.isOpen}
        width={config.width}
        showBackdrop={config.type === 'Over'}
        closeOnDocumentClick={config.type === 'Over'}
      >
        <nav className="sidebar-nav">
          <a href="#home">Home</a>
          <a href="#products">Products</a>
          <a href="#services">Services</a>
          <a href="#about">About</a>
        </nav>
      </SidebarComponent>

      <main>
        <h2>Welcome</h2>
        <p>Resize the browser to see responsive behavior.</p>
      </main>
    </div>
  );
}

export default App;
```

---
