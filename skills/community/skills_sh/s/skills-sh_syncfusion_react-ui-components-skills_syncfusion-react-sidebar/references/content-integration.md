# Content Integration

## Table of Contents
- [ListView Integration](#listview-integration)
- [TreeView Integration](#treeview-integration)
- [Custom HTML Content](#custom-html-content)
- [Dynamic Data Binding](#dynamic-data-binding)
- [Menu Structures](#menu-structures)

---

## ListView Integration

### Basic ListView in Sidebar

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ListViewComponent } from '@syncfusion/ej2-react-lists';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const sidebarRef = useRef(null);
  
  const listItems = [
    { text: 'Home', id: '1' },
    { text: 'Profile', id: '2' },
    { text: 'Settings', id: '3' },
    { text: 'Logout', id: '4' }
  ];

  const handleListClick = (args) => {
    console.log('Selected:', args.text);
    sidebarRef.current?.hide();
  };

  return (
    <div>
      <ButtonComponent onClick={() => sidebarRef.current?.toggle()}>
        ☰ Menu
      </ButtonComponent>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="280px"
      >
        <h3>Navigation</h3>
        <ListViewComponent
          dataSource={listItems}
          click={handleListClick}
        />
      </SidebarComponent>

      <div className="content">
        <h1>Main Content</h1>
      </div>
    </div>
  );
}

export default App;
```

### ListView with Icons and Actions

```jsx
function SidebarWithListView() {
  const [selectedItem, setSelectedItem] = React.useState(null);
  const sidebarRef = React.useRef(null);

  const listItems = [
    { 
      text: 'Home',
      icon: '🏠',
      id: 'home'
    },
    { 
      text: 'Products',
      icon: '📦',
      id: 'products'
    },
    { 
      text: 'Orders',
      icon: '📋',
      id: 'orders'
    },
    { 
      text: 'Settings',
      icon: '⚙️',
      id: 'settings'
    },
    { 
      text: 'Logout',
      icon: '🚪',
      id: 'logout'
    }
  ];

  const handleItemSelect = (args) => {
    setSelectedItem(args.text);
    sidebarRef.current?.hide();
  };

  const itemTemplate = (props) => {
    return (
      <div className="list-item-template">
        <span className="item-icon">{props.icon}</span>
        <span className="item-text">{props.text}</span>
      </div>
    );
  };

  return (
    <div>
      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="300px"
        showBackdrop={true}
      >
        <h3>Menu</h3>
        <ListViewComponent
          dataSource={listItems}
          template={itemTemplate}
          click={handleItemSelect}
          cssClass="sidebar-list"
        />
      </SidebarComponent>

      <div className="content">
        <h1>Selected: {selectedItem || 'None'}</h1>
      </div>
    </div>
  );
}
```

### CSS for List Styling

```css
.sidebar-list .e-list-item {
  padding: 12px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sidebar-list .e-list-item:hover {
  background-color: #f5f5f5;
  border-left: 4px solid #1976d2;
  padding-left: 16px;
}

.sidebar-list .e-list-item.e-active {
  background-color: #e3f2fd;
  color: #1976d2;
}

.list-item-template {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-icon {
  font-size: 20px;
}

.item-text {
  flex: 1;
}
```

---

## TreeView Integration

### Basic TreeView in Sidebar

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const sidebarRef = useRef(null);

  const treeData = [
    {
      id: '1',
      text: 'Products',
      expanded: true,
      children: [
        { id: '1-1', text: 'Electronics' },
        { id: '1-2', text: 'Clothing' },
        { id: '1-3', text: 'Books' }
      ]
    },
    {
      id: '2',
      text: 'Services',
      expanded: false,
      children: [
        { id: '2-1', text: 'Consulting' },
        { id: '2-2', text: 'Support' }
      ]
    },
    {
      id: '3',
      text: 'Settings'
    }
  ];

  const handleNodeClick = (args) => {
    console.log('Clicked:', args.node.textContent);
  };

  return (
    <div>
      <ButtonComponent onClick={() => sidebarRef.current?.toggle()}>
        ☰ Menu
      </ButtonComponent>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="300px"
      >
        <h3>Navigation</h3>
        <TreeViewComponent
          fields={{ dataSource: treeData, id: 'id', text: 'text', child: 'children' }}
          nodeClicked={handleNodeClick}
        />
      </SidebarComponent>

      <div className="content">
        <h1>Hierarchical Navigation</h1>
      </div>
    </div>
  );
}

export default App;
```

### TreeView with Multi-level Categories

```jsx
function SidebarWithHierarchy() {
  const sidebarRef = React.useRef(null);
  const [expandedNodes, setExpandedNodes] = React.useState(['1']);

  const categoryData = [
    {
      id: '1',
      text: '🏢 Business',
      expanded: true,
      children: [
        {
          id: '1-1',
          text: '👥 Teams',
          children: [
            { id: '1-1-1', text: '📌 Management' },
            { id: '1-1-2', text: '👨‍💼 Sales' },
            { id: '1-1-3', text: '🛠️ Engineering' }
          ]
        },
        {
          id: '1-2',
          text: '📊 Reports',
          children: [
            { id: '1-2-1', text: '📈 Analytics' },
            { id: '1-2-2', text: '💰 Finance' }
          ]
        }
      ]
    },
    {
      id: '2',
      text: '⚙️ Administration',
      children: [
        { id: '2-1', text: '🔐 Security' },
        { id: '2-2', text: '👤 Users' },
        { id: '2-3', text: '🎨 Settings' }
      ]
    }
  ];

  const handleNodeClick = (args) => {
    // Navigate or perform action
    console.log('Navigate to:', args.node.textContent);
  };

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Push"
      width="320px"
    >
      <TreeViewComponent
        fields={{ dataSource: categoryData, id: 'id', text: 'text', child: 'children' }}
        nodeClicked={handleNodeClick}
        cssClass="sidebar-tree"
      />
    </SidebarComponent>
  );
}
```

### CSS for TreeView Styling

```css
.sidebar-tree .e-treeview {
  border: none;
  background: transparent;
}

.sidebar-tree .e-treeview .e-list-item {
  padding: 8px 16px;
  color: #555;
}

.sidebar-tree .e-treeview .e-list-item:hover {
  background-color: #f5f5f5;
}

.sidebar-tree .e-treeview .e-list-item.e-active {
  background-color: #e3f2fd;
  border-left: 4px solid #1976d2;
  color: #1976d2;
}

.sidebar-tree .e-treeview .e-icon {
  margin-right: 10px;
  font-size: 18px;
}
```

---

## Custom HTML Content

### Complex Content Structure

```jsx
function SidebarWithCustomContent() {
  const sidebarRef = React.useRef(null);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      width="300px"
    >
      {/* Header Section */}
      <div className="sidebar-header">
        <img src="logo.png" alt="Logo" className="logo" />
        <h3>Dashboard</h3>
      </div>

      {/* User Section */}
      <div className="user-section">
        <img src="avatar.jpg" alt="User" className="avatar" />
        <div className="user-info">
          <p className="user-name">John Doe</p>
          <p className="user-role">Administrator</p>
        </div>
      </div>

      {/* Navigation Sections */}
      <div className="nav-section">
        <h4 className="section-title">Main</h4>
        <nav className="nav">
          <a href="#dashboard" className="nav-link active">
            <span className="icon">📊</span>
            <span>Dashboard</span>
          </a>
          <a href="#analytics" className="nav-link">
            <span className="icon">📈</span>
            <span>Analytics</span>
          </a>
        </nav>
      </div>

      <div className="nav-section">
        <h4 className="section-title">Management</h4>
        <nav className="nav">
          <a href="#users" className="nav-link">
            <span className="icon">👥</span>
            <span>Users</span>
          </a>
          <a href="#settings" className="nav-link">
            <span className="icon">⚙️</span>
            <span>Settings</span>
          </a>
        </nav>
      </div>

      {/* Footer Section */}
      <div className="sidebar-footer">
        <a href="#logout" className="logout-btn">
          🚪 Logout
        </a>
      </div>
    </SidebarComponent>
  );
}
```

### CSS for Custom Content

```css
.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
  text-align: center;
}

.sidebar-header .logo {
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.user-section .avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.user-info {
  flex: 1;
}

.user-name {
  font-weight: 600;
  color: #333;
  margin: 0;
}

.user-role {
  color: #999;
  font-size: 12px;
  margin: 0;
}

.nav-section {
  padding: 20px 0;
}

.section-title {
  font-size: 12px;
  text-transform: uppercase;
  color: #999;
  margin: 0 20px 10px;
  letter-spacing: 1px;
}

.nav {
  display: flex;
  flex-direction: column;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: #555;
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background-color: #f5f5f5;
  border-left-color: #1976d2;
}

.nav-link.active {
  background-color: #e3f2fd;
  color: #1976d2;
  border-left-color: #1976d2;
}

.nav-link .icon {
  font-size: 18px;
}

.sidebar-footer {
  padding: 15px 20px;
  border-top: 1px solid #e0e0e0;
  margin-top: 20px;
}

.logout-btn {
  display: block;
  padding: 10px 15px;
  background-color: #f5f5f5;
  color: #d32f2f;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #ffebee;
  color: #c62828;
}
```

---

## Dynamic Data Binding

### Load Data from API

```jsx
import React, { useRef, useEffect, useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ListViewComponent } from '@syncfusion/ej2-react-lists';

function SidebarWithDynamicData() {
  const sidebarRef = useRef(null);
  const [navItems, setNavItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch navigation items from API
    fetch('/api/navigation')
      .then(res => res.json())
      .then(data => {
        setNavItems(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load navigation:', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <SidebarComponent type="Over" width="280px">
      <h3>Navigation</h3>
      <ListViewComponent dataSource={navItems} />
    </SidebarComponent>
  );
}

export default SidebarWithDynamicData;
```

### Real-time Updates

```jsx
function SidebarWithRealtimeData() {
  const [menuItems, setMenuItems] = useState([
    { id: '1', text: 'Inbox', badge: 5 },
    { id: '2', text: 'Sent', badge: 0 }
  ]);

  // Update in real-time (e.g., WebSocket)
  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/notifications');
    
    ws.onmessage = (event) => {
      const notification = JSON.parse(event.data);
      setMenuItems(prev => prev.map(item => 
        item.id === notification.itemId 
          ? { ...item, badge: item.badge + 1 }
          : item
      ));
    };

    return () => ws.close();
  }, []);

  const itemTemplate = (props) => (
    <div className="nav-item-with-badge">
      <span>{props.text}</span>
      {props.badge > 0 && (
        <span className="badge">{props.badge}</span>
      )}
    </div>
  );

  return (
    <ListViewComponent
      dataSource={menuItems}
      template={itemTemplate}
    />
  );
}
```

---

## Menu Structures

### Dropdown Menu Pattern

```jsx
function SidebarWithDropdowns() {
  const [expandedMenus, setExpandedMenus] = React.useState({});

  const toggleMenu = (menuId) => {
    setExpandedMenus(prev => ({
      ...prev,
      [menuId]: !prev[menuId]
    }));
  };

  return (
    <div className="sidebar-menu">
      {/* Collapsible Menu Item */}
      <div className="menu-section">
        <button 
          className="menu-header"
          onClick={() => toggleMenu('products')}
        >
          📦 Products
          <span className={`arrow ${expandedMenus.products ? 'open' : ''}`}>▼</span>
        </button>
        {expandedMenus.products && (
          <div className="submenu">
            <a href="#electronics">Electronics</a>
            <a href="#clothing">Clothing</a>
            <a href="#books">Books</a>
          </div>
        )}
      </div>

      <div className="menu-section">
        <button 
          className="menu-header"
          onClick={() => toggleMenu('services')}
        >
          🔧 Services
          <span className={`arrow ${expandedMenus.services ? 'open' : ''}`}>▼</span>
        </button>
        {expandedMenus.services && (
          <div className="submenu">
            <a href="#consulting">Consulting</a>
            <a href="#support">Support</a>
          </div>
        )}
      </div>
    </div>
  );
}
```

### CSS for Menu Structures

```css
.menu-section {
  border-bottom: 1px solid #f0f0f0;
}

.menu-header {
  width: 100%;
  background: none;
  border: none;
  padding: 12px 20px;
  text-align: left;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  color: #555;
  transition: all 0.3s ease;
}

.menu-header:hover {
  background-color: #f5f5f5;
}

.arrow {
  transition: transform 0.3s ease;
  font-size: 12px;
}

.arrow.open {
  transform: rotate(180deg);
}

.submenu {
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
  animation: slideDown 0.3s ease;
}

.submenu a {
  padding: 10px 40px;
  color: #777;
  text-decoration: none;
  display: block;
  border-left: 3px solid transparent;
  transition: all 0.3s ease;
}

.submenu a:hover {
  background-color: #f0f0f0;
  color: #1976d2;
  border-left-color: #1976d2;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 500px;
  }
}
```

---
