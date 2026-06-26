# Design Patterns

## Table of Contents
- [AppBar with Menu Component](#appbar-with-menu-component)
- [AppBar with Button and DropDownButton](#appbar-with-button-and-dropdownbutton)
- [AppBar with Sidebar](#appbar-with-sidebar)
- [Common Layout Patterns](#common-layout-patterns)
- [Navigation Best Practices](#navigation-best-practices)

## AppBar with Menu Component

Integrate the Menu component with AppBar for dropdown navigation menus. The `e-inherit` CSS class ensures the Menu inherits AppBar styling.

**When to use:**
- Multi-level navigation hierarchies
- Dropdown menus with submenus
- Grouped navigation options
- Professional menu structures

### Basic Menu Integration

```tsx
import { AppBarComponent, MenuComponent, MenuItemModel } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const companyMenuItems: MenuItemModel[] = [
    {
      text: 'Company',
      items: [
        { text: 'About Us' },
        { text: 'Customers' },
        { text: 'Blog' },
        { text: 'Careers' }
      ]
    }
  ];

  const productMenuItems: MenuItemModel[] = [
    {
      text: 'Products',
      items: [
        { text: 'Developer Tools' },
        { text: 'Analytics' },
        { text: 'Reporting' },
        { text: 'Help Desk' }
      ]
    }
  ];

  const supportMenuItems: MenuItemModel[] = [
    {
      text: 'Support',
      items: [
        { text: 'Documentation' },
        { text: 'API Reference' },
        { text: 'Contact Us' }
      ]
    }
  ];

  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      
      {/* Menus inherit AppBar styling */}
      <MenuComponent cssClass="e-inherit" items={companyMenuItems}></MenuComponent>
      <MenuComponent cssClass="e-inherit" items={productMenuItems}></MenuComponent>
      <MenuComponent cssClass="e-inherit" items={supportMenuItems}></MenuComponent>
      
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">Login</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

### Menu with Icons and Event Handling

```tsx
import { AppBarComponent, MenuComponent, MenuItemModel } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const fileMenuItems: MenuItemModel[] = [
    {
      text: 'New',
      iconCss: 'e-icons e-file',
      items: [
        { text: 'Document', iconCss: 'e-icons e-document' },
        { text: 'Spreadsheet', iconCss: 'e-icons e-spreadsheet' },
        { text: 'Presentation', iconCss: 'e-icons e-presentation' }
      ]
    },
    {
      text: 'Open',
      iconCss: 'e-icons e-folder-open'
    },
    {
      text: 'Save',
      iconCss: 'e-icons e-save'
    },
    { separator: true },
    {
      text: 'Exit',
      iconCss: 'e-icons e-exit'
    }
  ];

  const handleMenuSelect = (args: any) => {
    console.log('Selected:', args.item.text);
  };

  return (
    <AppBarComponent colorMode="Dark" mode="Dense">
      <MenuComponent 
        cssClass="e-inherit" 
        items={fileMenuItems}
        select={handleMenuSelect}
      ></MenuComponent>
      
      <div className="e-appbar-separator"></div>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-undo"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-redo"></ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Key Points:**
- Use `cssClass="e-inherit"` to inherit AppBar styling
- Menu automatically positions dropdown below trigger
- Separator between menu groups improves visual hierarchy
- Icons in menu items enhance recognition

## AppBar with Button and DropDownButton

Combine AppBar with Button and DropDownButton components for flexible content layouts.

**When to use:**
- Quick action buttons
- Dropdown selections without full menu
- Call-to-action buttons
- Split buttons for primary + secondary actions

### DropDownButton in AppBar

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import React from "react";

const App = () => {
  const productItems: ItemModel[] = [
    { text: 'Developer Tools' },
    { text: 'Analytics Platform' },
    { text: 'Reporting Suite' },
    { text: 'E-Signature' },
    { text: 'Help Desk' }
  ];

  const accountItems: ItemModel[] = [
    { text: 'Profile' },
    { text: 'Settings' },
    { text: 'Preferences' },
    { separator: true },
    { text: 'Logout' }
  ];

  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      
      <DropDownButtonComponent 
        cssClass="e-inherit" 
        items={productItems}
      >
        Products
      </DropDownButtonComponent>
      
      <ButtonComponent cssClass="e-inherit">Documentation</ButtonComponent>
      
      <div className="e-appbar-spacer"></div>
      <div className="e-appbar-separator"></div>
      
      <DropDownButtonComponent 
        cssClass="e-inherit" 
        items={accountItems}
        iconCss="e-icons e-user"
      >
        Account
      </DropDownButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

### Multiple Dropdowns with Separators

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import React from "react";

const App = () => {
  const viewOptions: ItemModel[] = [
    { text: 'Grid View' },
    { text: 'List View' },
    { text: 'Kanban View' }
  ];

  const sortOptions: ItemModel[] = [
    { text: 'By Name' },
    { text: 'By Date' },
    { text: 'By Priority' }
  ];

  const filterOptions: ItemModel[] = [
    { text: 'Active' },
    { text: 'Archived' },
    { text: 'All' }
  ];

  return (
    <AppBarComponent colorMode="Primary" mode="Dense">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      
      {/* View Controls */}
      <DropDownButtonComponent 
        cssClass="e-inherit" 
        items={viewOptions}
        iconCss="e-icons e-list"
      >
        View
      </DropDownButtonComponent>
      
      <div className="e-appbar-separator"></div>
      
      {/* Data Controls */}
      <DropDownButtonComponent 
        cssClass="e-inherit" 
        items={sortOptions}
        iconCss="e-icons e-sort"
      >
        Sort
      </DropDownButtonComponent>
      
      <DropDownButtonComponent 
        cssClass="e-inherit" 
        items={filterOptions}
        iconCss="e-icons e-filter"
      >
        Filter
      </DropDownButtonComponent>
      
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit" isPrimary>Export</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

## AppBar with Sidebar

Combine AppBar with Sidebar for responsive navigation. Common on mobile apps where sidebar toggles on menu click.

**When to use:**
- Mobile-friendly navigation
- Collapsible menus
- Navigation drawers
- Responsive layouts

### Basic Sidebar Toggle

```tsx
import React, { useState, useRef } from "react";
import { AppBarComponent, SidebarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import './App.css';

const App = () => {
  const [isOpen, setIsOpen] = useState(true);
  const sidebarRef = useRef<SidebarComponent>(null);

  const toggleSidebar = () => {
    if (sidebarRef.current) {
      sidebarRef.current.toggle();
    }
  };

  return (
    <div id="responsive-wrapper">
      {/* AppBar Header */}
      <AppBarComponent>
        <ButtonComponent 
          cssClass="e-inherit" 
          iconCss="e-icons e-menu"
          onClick={toggleSidebar}
        ></ButtonComponent>
        <div className="e-folder">
          <div className="e-folder-name">My Application</div>
        </div>
      </AppBarComponent>

      {/* Sidebar Navigation */}
      <SidebarComponent 
        ref={sidebarRef}
        width="250px"
        target=".main-content"
        mediaQuery="(min-width: 600px)"
        isOpen={isOpen}
      >
        <div className="sidebar-menu">
          <div className="menu-section">
            <h4>Navigation</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#services">Services</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>
        </div>
      </SidebarComponent>

      {/* Main Content */}
      <div className="main-content" style={{ padding: '20px' }}>
        <h2>Main Content Area</h2>
        <p>Click the menu icon to toggle sidebar on mobile devices.</p>
      </div>
    </div>
  );
}

export default App;
```

### Sidebar with TreeView Navigation

```tsx
import React, { useState, useRef } from "react";
import { AppBarComponent, SidebarComponent, TreeViewComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import { TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import './App.css';

const App = () => {
  const [isOpen, setIsOpen] = useState(true);
  const sidebarRef = useRef<SidebarComponent>(null);

  const navData: { [key: string]: Object }[] = [
    { nodeId: '01', nodeText: 'Getting Started' },
    { nodeId: '02', nodeText: 'Installation' },
    {
      nodeId: '03',
      nodeText: 'Components',
      nodeChild: [
        { nodeId: '03-01', nodeText: 'Grid' },
        { nodeId: '03-02', nodeText: 'Chart' },
        { nodeId: '03-03', nodeText: 'Calendar' },
        { nodeId: '03-04', nodeText: 'Button' }
      ]
    },
    { nodeId: '04', nodeText: 'API Reference' },
    { nodeId: '05', nodeText: 'Support' }
  ];

  const toggleSidebar = () => {
    if (sidebarRef.current) {
      sidebarRef.current.toggle();
    }
  };

  const treeFields = {
    dataSource: navData,
    id: 'nodeId',
    text: 'nodeText',
    child: 'nodeChild'
  };

  return (
    <div id="responsive-wrapper">
      {/* AppBar */}
      <AppBarComponent>
        <ButtonComponent 
          cssClass="e-inherit"
          iconCss="e-icons e-menu"
          onClick={toggleSidebar}
        ></ButtonComponent>
        <div className="e-folder">
          <div className="e-folder-name">Documentation</div>
        </div>
      </AppBarComponent>

      {/* Sidebar with TreeView */}
      <SidebarComponent 
        ref={sidebarRef}
        width="220px"
        target=".main-sidebar-content"
        mediaQuery="(min-width: 600px)"
        isOpen={isOpen}
      >
        <div className="res-main-menu">
          <div className="table-content">
            <TextBoxComponent placeholder="Search..."></TextBoxComponent>
            <p className="main-menu-header">TABLE OF CONTENTS</p>
          </div>
          <div>
            <TreeViewComponent 
              cssClass="main-treeview"
              fields={treeFields}
              expandOn='Click'
            />
          </div>
        </div>
      </SidebarComponent>

      {/* Main Content */}
      <div className="main-sidebar-content" id="main-text">
        <div className="sidebar-content">
          <h2>Component Documentation</h2>
          <p>Select a topic from the sidebar to view documentation.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
```

## Common Layout Patterns

### Pattern 1: E-commerce Header
```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span className="logo">ShopHub</span>
  
  <ButtonComponent cssClass="e-inherit">Home</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">Shop</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">Sale</ButtonComponent>
  
  <div className="e-appbar-spacer"></div>
  <div className="e-appbar-separator"></div>
  
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-search"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-shopping-cart"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-user"></ButtonComponent>
</AppBarComponent>
```

### Pattern 2: Admin Dashboard Header
```tsx
<AppBarComponent colorMode="Dark">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Dashboard</span>
  
  <div className="e-appbar-spacer"></div>
  
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-bell"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-mail"></ButtonComponent>
  <div className="e-appbar-separator"></div>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-user"></ButtonComponent>
</AppBarComponent>
```

### Pattern 3: Document Editor Toolbar
```tsx
<AppBarComponent colorMode="Primary" mode="Dense">
  {/* File Operations */}
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-new"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-open"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-save"></ButtonComponent>
  
  <div className="e-appbar-separator"></div>
  
  {/* Edit Operations */}
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-undo"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-redo"></ButtonComponent>
  
  <div className="e-appbar-separator"></div>
  
  {/* Formatting */}
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-bold"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-italic"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-underline"></ButtonComponent>
</AppBarComponent>
```

## Navigation Best Practices

### 1. Use e-inherit for Component Styling
```tsx
// ✓ Correct: Components inherit AppBar styles
<MenuComponent cssClass="e-inherit" items={menuItems}></MenuComponent>
<ButtonComponent cssClass="e-inherit">Button</ButtonComponent>

// ✗ Incorrect: Components styled separately
<MenuComponent items={menuItems}></MenuComponent>  // Won't match AppBar
```

### 2. Organize Content with Spacer and Separator
```tsx
// Good structure: Left navigation | Right actions
<AppBarComponent>
  <ButtonComponent>Menu</ButtonComponent>
  <MenuComponent>Navigation</MenuComponent>
  
  <div className="e-appbar-spacer"></div>     {/* Push right */}
  <div className="e-appbar-separator"></div>  {/* Visual break */}
  
  <ButtonComponent>Settings</ButtonComponent>
  <ButtonComponent>Logout</ButtonComponent>
</AppBarComponent>
```

### 3. Responsive Sidebar Toggle
```tsx
// Always provide toggle capability on mobile
<ButtonComponent 
  cssClass="e-inherit"
  iconCss="e-icons e-menu"
  onClick={() => sidebarRef.current?.toggle()}
></ButtonComponent>
```

### 4. Color Mode for Visual Hierarchy
```tsx
// Use different colors for different sections
<AppBarComponent colorMode="Primary">
  {/* Main navigation */}
</AppBarComponent>

<AppBarComponent colorMode="Dark" mode="Dense">
  {/* Secondary toolbar */}
</AppBarComponent>

<AppBarComponent colorMode="Light">
  {/* Footer toolbar */}
</AppBarComponent>
```

### 5. Consistent Icon Usage
```tsx
// Use consistent icon library (e-icons)
<ButtonComponent iconCss='e-icons e-menu'></ButtonComponent>  // ✓ Correct
<ButtonComponent iconCss='e-icons e-home'></ButtonComponent>
<ButtonComponent iconCss='custom-icon'></ButtonComponent>     // ✗ Inconsistent
```

These patterns provide solid foundations for building professional AppBar-based navigation systems.
