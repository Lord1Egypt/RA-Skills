# Style Customization

## Table of Contents
- [CSS Customization](#css-customization)
- [Theme Variables](#theme-variables)
- [Gripper and Separator Styling](#gripper-and-separator-styling)
- [Responsive Design Patterns](#responsive-design-patterns)
- [Dark Mode and Theme Switching](#dark-mode-and-theme-switching)

## CSS Customization

Override default Splitter styles with custom CSS classes.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './splitter-styles.css';

function CSSCustomization() {
  return (
    <SplitterComponent 
      orientation='Horizontal'
      style={{ height: '400px' }}
      className='custom-splitter'
    >
      <PanesDirective>
        <PaneDirective size='250px' className='sidebar-pane'>
          <div>
            <h3>Customized Sidebar</h3>
            <p>Has custom background and styles</p>
          </div>
        </PaneDirective>

        <PaneDirective size='300px' className='main-pane'>
          <div>
            <h3>Customized Content</h3>
            <p>All styles are overridable</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default CSSCustomization;
```

### CSS File: splitter-styles.css

```css
/* Splitter container */
.custom-splitter {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* Sidebar pane */
.custom-splitter .sidebar-pane {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
}

.custom-splitter .sidebar-pane > div {
  height: 100%;
  padding: 20px;
  color: white;
  overflow-y: auto;
}

.custom-splitter .sidebar-pane h3 {
  margin-top: 0;
  font-size: 18px;
  font-weight: 600;
}

/* Main pane */
.custom-splitter .main-pane {
  background: #fafafa;
  padding: 0;
}

.custom-splitter .main-pane > div {
  height: 100%;
  padding: 20px;
  overflow-y: auto;
}

.custom-splitter .main-pane h3 {
  color: #333;
  margin-top: 0;
}

/* Separator bar */
.custom-splitter .e-splitter-bar {
  background: linear-gradient(90deg, #e0e0e0, #f5f5f5);
  width: 4px;
  cursor: col-resize;
  transition: all 0.2s ease;
}

.custom-splitter .e-splitter-bar:hover {
  background: linear-gradient(90deg, #667eea, #764ba2);
  width: 6px;
}

/* Pane scrollbar styling */
.custom-splitter .e-pane {
  scrollbar-width: thin;
  scrollbar-color: #ccc #f0f0f0;
}

.custom-splitter .e-pane::-webkit-scrollbar {
  width: 8px;
}

.custom-splitter .e-pane::-webkit-scrollbar-track {
  background: #f0f0f0;
}

.custom-splitter .e-pane::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 4px;
}
```

## Theme Variables

Use CSS custom properties for dynamic theming.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './theme-variables.css';

function ThemeVariables() {
  const [theme, setTheme] = React.useState('light');

  React.useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }, [theme]);

  return (
    <div>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
      </button>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px', marginTop: '15px' }}
        className='themed-splitter'
      >
        <PanesDirective>
          <PaneDirective size='250px'>
            <div style={{ padding: '20px' }}>
              <h3>Themed Sidebar</h3>
              <p>Uses CSS custom properties</p>
            </div>
          </PaneDirective>

          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>Themed Content</h3>
              <p>Dynamically switches themes</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default ThemeVariables;
```

### CSS File: theme-variables.css

```css
:root {
  /* Light theme (default) */
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #333333;
  --text-secondary: #666666;
  --border-color: #ddd;
  --separator-color: #e0e0e0;
  --hover-color: #f0f0f0;
}

[data-theme='dark'] {
  /* Dark theme */
  --primary-color: #7c3aed;
  --secondary-color: #6d28d9;
  --bg-primary: #1a1a1a;
  --bg-secondary: #2d2d2d;
  --text-primary: #e0e0e0;
  --text-secondary: #b0b0b0;
  --border-color: #444;
  --separator-color: #555;
  --hover-color: #3d3d3d;
}

.themed-splitter {
  background: var(--bg-primary);
  border-color: var(--border-color);
}

.themed-splitter .e-pane {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.themed-splitter .e-splitter-bar {
  background: var(--separator-color);
}

.themed-splitter .e-splitter-bar:hover {
  background: var(--primary-color);
}

.themed-splitter h3 {
  color: var(--text-primary);
}

.themed-splitter p {
  color: var(--text-secondary);
}
```

## Gripper and Separator Styling

Customize the separator bar and gripper icons.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './separator-styles.css';

function SeparatorStyling() {
  return (
    <SplitterComponent 
      orientation='Horizontal'
      style={{ height: '400px' }}
      className='custom-separator'
    >
      <PanesDirective>
        <PaneDirective size='250px'>
          <div style={{ padding: '20px' }}>
            <h3>Left Pane</h3>
            <p>Drag the stylized separator</p>
          </div>
        </PaneDirective>

        <PaneDirective size='300px'>
          <div style={{ padding: '20px' }}>
            <h3>Right Pane</h3>
            <p>Notice the custom gripper</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default SeparatorStyling;
```

### CSS File: separator-styles.css

```css
/* Custom separator bar - minimal */
.custom-separator .e-splitter-bar {
  width: 3px;
  background: #ccc;
  cursor: col-resize;
  position: relative;
  transition: all 0.2s ease;
}

.custom-separator .e-splitter-bar:hover {
  width: 4px;
  background: #999;
}

.custom-separator .e-splitter-bar::before {
  content: '⋮⋮';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
  font-size: 14px;
  user-select: none;
  pointer-events: none;
}

/* Custom gripper - arrow style */
.custom-separator.arrow-grip .e-splitter-bar::before {
  content: '❮  ❯';
  font-size: 12px;
}

/* Custom gripper - bars style */
.custom-separator.bars-grip .e-splitter-bar::before {
  content: '▮ ▮ ▮';
  letter-spacing: 2px;
}

/* Vertical splitter bar customization */
.custom-separator.vertical .e-splitter-bar {
  width: 100%;
  height: 3px;
  cursor: row-resize;
}

.custom-separator.vertical .e-splitter-bar::before {
  content: '⋯';
  font-size: 16px;
}

/* Animated separator */
.custom-separator.animated .e-splitter-bar {
  background: linear-gradient(90deg, #e0e0e0, #f5f5f5, #e0e0e0);
  background-size: 200% 100%;
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0%, 100% {
    background-position: 0 0;
  }
  50% {
    background-position: 100% 0;
  }
}
```

## Responsive Design Patterns

Make splitter layouts responsive for different screen sizes.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './responsive-splitter.css';

function ResponsiveSplitter() {
  const [screenSize, setScreenSize] = React.useState(window.innerWidth);

  React.useEffect(() => {
    const handleResize = () => setScreenSize(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const getOrientation = () => screenSize < 768 ? 'Vertical' : 'Horizontal';
  const getSidebarSize = () => {
    if (screenSize < 480) return '100%'; // Stack on mobile
    if (screenSize < 768) return '40%';  // Tablet
    return '30%'; // Desktop
  };

  return (
    <div className='responsive-container'>
      <SplitterComponent 
        orientation={getOrientation()}
        style={{ height: '500px' }}
        className='responsive-splitter'
      >
        <PanesDirective>
          <PaneDirective size={getSidebarSize()} collapsible={screenSize < 768}>
            <div style={{ padding: '20px' }}>
              <h3>Navigation</h3>
              <p>Responsive panel</p>
            </div>
          </PaneDirective>

          <PaneDirective size='auto'>
            <div style={{ padding: '20px' }}>
              <h3>Content</h3>
              <p>Screen width: {screenSize}px</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default ResponsiveSplitter;
```

### CSS File: responsive-splitter.css

```css
.responsive-container {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.responsive-splitter {
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

/* Mobile (< 480px) */
@media (max-width: 480px) {
  .responsive-splitter .e-splitter-bar {
    width: 100%;
    height: 4px;
  }

  .responsive-splitter .e-pane {
    padding: 10px !important;
  }

  .responsive-splitter h3 {
    font-size: 16px;
    margin: 0 0 10px 0;
  }
}

/* Tablet (480px - 768px) */
@media (min-width: 480px) and (max-width: 768px) {
  .responsive-splitter {
    height: 400px;
  }

  .responsive-splitter .e-pane {
    padding: 15px;
    font-size: 14px;
  }
}

/* Desktop (> 768px) */
@media (min-width: 768px) {
  .responsive-splitter {
    height: 500px;
  }

  .responsive-splitter .e-splitter-bar {
    width: 4px;
  }

  .responsive-splitter .e-pane {
    padding: 20px;
  }
}
```

## Dark Mode and Theme Switching

Implement comprehensive dark mode support.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';
import './dark-mode.css';

function DarkModeTheme() {
  const [isDarkMode, setIsDarkMode] = React.useState(false);

  React.useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.classList.add('dark-mode');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark-mode');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  React.useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      setIsDarkMode(true);
    }
  }, []);

  return (
    <div className='theme-wrapper'>
      <div className='theme-toggle'>
        <button 
          onClick={() => setIsDarkMode(!isDarkMode)}
          className='toggle-button'
        >
          {isDarkMode ? '☀️ Light' : '🌙 Dark'} Mode
        </button>
      </div>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px' }}
        className='themed-component'
      >
        <PanesDirective>
          <PaneDirective size='250px'>
            <div style={{ padding: '20px' }}>
              <h3>Dark Mode Sidebar</h3>
              <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
              </ul>
            </div>
          </PaneDirective>

          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>Dark Mode Content</h3>
              <p>Toggle dark mode to see theme change</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default DarkModeTheme;
```

### CSS File: dark-mode.css

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #333333;
  --text-secondary: #666666;
  --border-color: #ddd;
  --splitter-bg: #e0e0e0;
}

.dark-mode {
  --bg-primary: #121212;
  --bg-secondary: #1e1e1e;
  --text-primary: #e0e0e0;
  --text-secondary: #b0b0b0;
  --border-color: #333;
  --splitter-bg: #2d2d2d;
}

.theme-wrapper {
  padding: 20px;
}

.theme-toggle {
  margin-bottom: 20px;
}

.toggle-button {
  padding: 10px 20px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.toggle-button:hover {
  background: var(--border-color);
}

.themed-component {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.themed-component .e-pane {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.themed-component .e-splitter-bar {
  background: var(--splitter-bg);
}

.themed-component h3 {
  color: var(--text-primary);
  margin-top: 0;
}

.themed-component p {
  color: var(--text-secondary);
}

.themed-component ul {
  list-style: none;
  padding: 0;
}

.themed-component li {
  padding: 8px;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-color);
}
```

## Best Practices

1. **Use CSS variables** for dynamic theming
2. **Mobile-first approach** - Design for mobile, enhance for desktop
3. **Test contrast** - Ensure sufficient color contrast in all themes
4. **Preserve functionality** - Styling shouldn't break interaction
5. **Respect user preferences** - Check `prefers-color-scheme`
6. **Performance** - Minimize CSS repaints during resize
