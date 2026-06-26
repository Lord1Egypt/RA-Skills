# Pane Content and Styling

## Table of Contents
- [HTML Content in Panes](#html-content-in-panes)
- [React Component Content](#react-component-content)
- [CSS Selector-Based Content](#css-selector-based-content)
- [Pane Template Usage](#pane-template-usage)
- [Custom Styling](#custom-styling)

## HTML Content in Panes

Add simple HTML content directly inside PaneDirective.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function HTMLContent() {
  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '20px' }}>
            <h3>Navigation</h3>
            <ul>
              <li><a href='#'>Home</a></li>
              <li><a href='#'>About</a></li>
              <li><a href='#'>Contact</a></li>
            </ul>
          </div>
        </PaneDirective>

        <PaneDirective size='300px'>
          <div style={{ padding: '20px' }}>
            <h2>Welcome</h2>
            <p>This is a simple HTML content pane.</p>
            <button onClick={() => alert('Clicked!')}>Click Me</button>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default HTMLContent;
```

**Use Cases:**
- Navigation menus
- Simple text content
- Static layouts
- Basic lists and forms

## React Component Content

Use React components as pane content for complex, interactive panels.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

// Sidebar component
function Sidebar() {
  const [activeItem, setActiveItem] = React.useState('home');

  const items = [
    { id: 'home', label: '🏠 Home' },
    { id: 'projects', label: '📁 Projects' },
    { id: 'settings', label: '⚙️ Settings' },
    { id: 'help', label: '❓ Help' }
  ];

  return (
    <div style={{ padding: '15px', height: '100%', overflowY: 'auto' }}>
      <h3>Menu</h3>
      {items.map(item => (
        <div
          key={item.id}
          onClick={() => setActiveItem(item.id)}
          style={{
            padding: '10px',
            margin: '5px 0',
            backgroundColor: activeItem === item.id ? '#007bff' : '#f0f0f0',
            color: activeItem === item.id ? 'white' : 'black',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          {item.label}
        </div>
      ))}
    </div>
  );
}

// Main content component
function MainContent({ title }: { title: string }) {
  const [count, setCount] = React.useState(0);

  return (
    <div style={{ padding: '20px' }}>
      <h2>{title}</h2>
      <p>Interactive React component content</p>
      <p>Counter: {count}</p>
      <button 
        onClick={() => setCount(count + 1)}
        style={{
          padding: '8px 16px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Increment
      </button>
    </div>
  );
}

// Main splitter component
function ComponentContent() {
  const [activeSection, setActiveSection] = React.useState('home');

  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective size='200px'>
          <Sidebar />
        </PaneDirective>

        <PaneDirective size='300px'>
          <MainContent title={activeSection.toUpperCase()} />
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default ComponentContent;
```

**Advantages:**
- Full React state management
- Event handlers and hooks
- Complex UI logic
- Reusable component patterns

## CSS Selector-Based Content

Reference external HTML elements using CSS selectors.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function SelectorContent() {
  return (
    <div>
      {/* Hidden content elements */}
      <div id='sidebar-content' style={{ display: 'none' }}>
        <h3>Sidebar Content</h3>
        <p>This content is referenced by selector</p>
        <ul>
          <li>Item 1</li>
          <li>Item 2</li>
          <li>Item 3</li>
        </ul>
      </div>

      <div id='main-content' style={{ display: 'none' }}>
        <h2>Main Area</h2>
        <p>Content loaded from selector #main-content</p>
      </div>

      {/* Splitter using selectors */}
      <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
        <PanesDirective>
          <PaneDirective 
            size='250px'
            content='#sidebar-content'
          >
          </PaneDirective>

          <PaneDirective 
            size='300px'
            content='#main-content'
          >
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default SelectorContent;
```

**Use Cases:**
- Template-based content
- Server-rendered HTML
- Pre-existing DOM elements
- HTML-first development

## Pane Template Usage

Define content templates for dynamic rendering.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function PaneTemplates() {
  const renderSidebarTemplate = () => (
    <div style={{ padding: '15px', height: '100%' }}>
      <h4>Filter</h4>
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input type='checkbox' defaultChecked /> Active
        </label>
      </div>
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input type='checkbox' /> Archived
        </label>
      </div>
      <div>
        <label>
          <input type='checkbox' /> Deleted
        </label>
      </div>
    </div>
  );

  const renderMainTemplate = () => (
    <div style={{ padding: '20px' }}>
      <h3>Results</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #ddd' }}>
            <th style={{ padding: '10px', textAlign: 'left' }}>Name</th>
            <th style={{ padding: '10px', textAlign: 'left' }}>Status</th>
            <th style={{ padding: '10px', textAlign: 'left' }}>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr style={{ borderBottom: '1px solid #eee' }}>
            <td style={{ padding: '10px' }}>Item 1</td>
            <td style={{ padding: '10px' }}>Active</td>
            <td style={{ padding: '10px' }}>2026-03-10</td>
          </tr>
          <tr style={{ borderBottom: '1px solid #eee' }}>
            <td style={{ padding: '10px' }}>Item 2</td>
            <td style={{ padding: '10px' }}>Active</td>
            <td style={{ padding: '10px' }}>2026-03-09</td>
          </tr>
        </tbody>
      </table>
    </div>
  );

  return (
    <SplitterComponent orientation='Horizontal' style={{ height: '400px' }}>
      <PanesDirective>
        <PaneDirective size='200px'>
          {renderSidebarTemplate()}
        </PaneDirective>

        <PaneDirective size='300px'>
          {renderMainTemplate()}
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default PaneTemplates;
```

## Custom Styling

Style panes with CSS classes and inline styles.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './custom-styles.css';

function CustomStyling() {
  return (
    <SplitterComponent 
      orientation='Horizontal' 
      style={{ height: '400px' }}
      className='custom-splitter'
    >
      <PanesDirective>
        <PaneDirective size='250px' className='sidebar-pane'>
          <div style={{ padding: '20px', height: '100%' }}>
            <h3>Styled Sidebar</h3>
            <p>Custom CSS applied</p>
          </div>
        </PaneDirective>

        <PaneDirective size='300px' className='content-pane'>
          <div style={{ padding: '20px', height: '100%' }}>
            <h3>Styled Content</h3>
            <p>Custom CSS applied</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default CustomStyling;
```

### CSS File: custom-styles.css

```css
/* Splitter container styles */
.custom-splitter {
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

/* Sidebar pane styles */
.custom-splitter .sidebar-pane {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.custom-splitter .sidebar-pane > div {
  color: white;
}

.custom-splitter .sidebar-pane h3 {
  margin-top: 0;
  font-size: 18px;
}

/* Content pane styles */
.custom-splitter .content-pane {
  background: #f9f9f9;
}

.custom-splitter .content-pane h3 {
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

/* Separator styling */
.custom-splitter .e-splitter-bar {
  background: linear-gradient(90deg, #e0e0e0, #f0f0f0);
  width: 4px;
  cursor: col-resize;
  transition: all 0.3s ease;
}

.custom-splitter .e-splitter-bar:hover {
  background: linear-gradient(90deg, #2196f3, #1976d2);
  width: 5px;
}

/* Dark mode styles */
.custom-splitter.dark-theme .sidebar-pane {
  background: #1e1e1e;
}

.custom-splitter.dark-theme .content-pane {
  background: #2d2d2d;
  color: #e0e0e0;
}
```

### Example: Theme Switching

```tsx
function ThemedSplitter() {
  const [isDark, setIsDark] = React.useState(false);

  return (
    <div>
      <button onClick={() => setIsDark(!isDark)}>
        {isDark ? '☀️ Light' : '🌙 Dark'} Mode
      </button>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px', marginTop: '10px' }}
        className={isDark ? 'custom-splitter dark-theme' : 'custom-splitter'}
      >
        <PanesDirective>
          <PaneDirective size='250px' className='sidebar-pane'>
            <div style={{ padding: '20px' }}>Sidebar</div>
          </PaneDirective>
          <PaneDirective size='300px' className='content-pane'>
            <div style={{ padding: '20px' }}>Content</div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}
```

## Best Practices

1. **Match content type to pane purpose** - Simple HTML or complex components
2. **Optimize rendering** - Use React.memo for expensive components
3. **Handle overflow** - Set appropriate `overflow` CSS properties
4. **Maintain consistency** - Apply unified styling across panes
5. **Consider accessibility** - Ensure content is keyboard accessible
6. **Test responsiveness** - Verify content fits at minimum pane sizes
