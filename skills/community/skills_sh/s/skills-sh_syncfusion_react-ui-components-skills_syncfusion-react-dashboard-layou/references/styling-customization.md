# Styling and CSS Customization

## Table of Contents
- [Overview](#overview)
- [CSS Selectors Reference](#css-selectors-reference)
- [Theme System](#theme-system)
- [Header Styling](#header-styling)
- [Content Area Styling](#content-area-styling)
- [Resize Handle Styling](#resize-handle-styling)
- [Panel Background & Borders](#panel-background--borders)
- [Dragging State Styling](#dragging-state-styling)
- [Advanced Customization](#advanced-customization)

## Overview

Dashboard Layout provides comprehensive CSS customization capabilities. Every visual aspect—from panel backgrounds to resize handles—can be styled using CSS selectors. The component uses standard CSS classes that integrate with popular theme systems (Tailwind, Bootstrap, Material, Fluent).

### Styling Approach

Dashboard Layout styling follows these principles:
- **CSS Class-based**: All styling via `.e-` prefixed classes
- **Selector Specificity**: Override styles with appropriate CSS specificity
- **Theme Integration**: Works with all Syncfusion themes
- **Responsive Friendly**: CSS media queries for breakpoints

## CSS Selectors Reference

### Main Container

```css
/* Dashboard Layout main container */
.e-dashboard-layout {
  /* Base layout styles */
}

/* Entire layout wrapper */
.e-layout {
  width: 100%;
  height: 100%;
}
```

### Panel Selectors

```css
/* All panels container */
.e-layout > .e-panel {
  position: absolute;
  border: 1px solid #d9d9d9;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

/* Panel header */
.e-panel .e-panel-header {
  background: #f5f5f5;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  cursor: move;
  user-select: none;
}

/* Panel header text */
.e-panel .e-panel-header .e-header-text {
  font-weight: 600;
  font-size: 14px;
  color: #333333;
}

/* Panel content area */
.e-panel .e-panel-content {
  padding: 16px;
  overflow: auto;
  height: 100%;
}

/* Nested content container */
.e-panel-content > * {
  /* Applied to direct children of content area */
}
```

### Resize Handle Selectors

```css
/* All resize handles container */
.e-panel .e-resize-handle {
  position: absolute;
  background: transparent;
  cursor: pointer;
}

/* South-east corner (default) */
.e-panel .e-south-east {
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: se-resize;
  background: linear-gradient(135deg, transparent 50%, #2196F3 50%);
}

/* South handle (bottom edge) */
.e-panel .e-south {
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 6px;
  cursor: s-resize;
  background: #e0e0e0;
}

/* East handle (right edge) */
.e-panel .e-east {
  top: 50%;
  right: 0;
  transform: translateY(-50%);
  width: 6px;
  height: 40px;
  cursor: e-resize;
  background: #e0e0e0;
}

/* West handle (left edge) */
.e-panel .e-west {
  top: 50%;
  left: 0;
  transform: translateY(-50%);
  width: 6px;
  height: 40px;
  cursor: w-resize;
  background: #e0e0e0;
}

/* North handle (top edge) */
.e-panel .e-north {
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 6px;
  cursor: n-resize;
  background: #e0e0e0;
}

/* North-west handle (top-left) */
.e-panel .e-north-west {
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  cursor: nw-resize;
  background: linear-gradient(135deg, #2196F3 50%, transparent 50%);
}

/* South-west handle (bottom-left) */
.e-panel .e-south-west {
  bottom: 0;
  left: 0;
  width: 20px;
  height: 20px;
  cursor: sw-resize;
}
```

### Interaction State Selectors

```css
/* Panel being dragged */
.e-panel.e-dragging {
  opacity: 0.8;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

/* Panel being resized */
.e-panel.e-resizing {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

/* Placeholder/ghost when dragging */
.e-dashboard-layout .e-placeholder {
  border: 2px dashed #2196F3;
  background: rgba(33, 150, 243, 0.1);
  border-radius: 4px;
}
```

## Theme System

Dashboard Layout integrates with Syncfusion's theme system:

```tsx
// Tailwind 3 theme
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-react-layouts/styles/tailwind3.css';

// Bootstrap 5.3 theme
import '@syncfusion/ej2-base/styles/bootstrap5.3.css';
import '@syncfusion/ej2-react-layouts/styles/bootstrap5.3.css';

// Material 3 theme
import '@syncfusion/ej2-base/styles/material3.css';
import '@syncfusion/ej2-react-layouts/styles/material3.css';

// Fluent 2 theme
import '@syncfusion/ej2-base/styles/fluent2.css';
import '@syncfusion/ej2-react-layouts/styles/fluent2.css';
```

### Theme-Specific Overrides

Each theme provides base colors that can be customized:

```css
/* Tailwind theme customization */
:root {
  --primary: #2196F3;
  --secondary: #f44336;
  --success: #4caf50;
  --warning: #ff9800;
  --danger: #f44336;
}

/* Apply theme colors to dashboard */
.e-dashboard-layout .e-panel {
  border-color: var(--primary);
}

.e-dashboard-layout .e-panel:hover {
  box-shadow: 0 2px 8px rgba(33, 150, 243, 0.2);
}
```

## Header Styling

Customize panel headers with detailed styling:

```css
/* Custom header background */
.e-panel .e-panel-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 16px;
  font-weight: 600;
  border-bottom: none;
  border-radius: 4px 4px 0 0;
}

/* Header text styling */
.e-panel .e-panel-header .e-header-text {
  color: white;
  font-size: 15px;
  letter-spacing: 0.3px;
}

/* Header with icon */
.e-panel .e-panel-header::before {
  content: '📊';
  margin-right: 8px;
  font-size: 18px;
}

/* Header hover effect */
.e-panel .e-panel-header:hover {
  background: linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%);
}
```

## Content Area Styling

Style the main content panel area:

```css
/* Content area with custom padding and colors */
.e-panel .e-panel-content {
  background: #fafafa;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #424242;
}

/* Scrollable content */
.e-panel .e-panel-content {
  overflow-y: auto;
  overflow-x: hidden;
}

/* Content with custom scrollbar */
.e-panel .e-panel-content::-webkit-scrollbar {
  width: 8px;
}

.e-panel .e-panel-content::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.e-panel .e-panel-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.e-panel .e-panel-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Content typography */
.e-panel .e-panel-content h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #212121;
}

.e-panel .e-panel-content p {
  margin: 0 0 8px 0;
  font-size: 14px;
}
```

## Resize Handle Styling

Customize resize handle appearance:

```css
/* Make resize handles more visible */
.e-panel .e-south-east {
  background: linear-gradient(135deg, transparent 60%, #2196F3 60%);
  opacity: 0;
  transition: opacity 0.2s ease;
}

/* Show resize handles on panel hover */
.e-panel:hover .e-south-east,
.e-panel:hover .e-east,
.e-panel:hover .e-west,
.e-panel:hover .e-north {
  opacity: 1;
}

/* Animated resize handle */
.e-panel .e-resize-handle {
  transition: all 0.2s ease;
}

.e-panel .e-resize-handle:hover {
  background-color: rgba(33, 150, 243, 0.3);
}

/* Large resize handles for touch devices */
@media (max-width: 768px) {
  .e-panel .e-resize-handle {
    width: 40px !important;
    height: 40px !important;
  }
  
  .e-panel .e-south-east {
    bottom: -10px;
    right: -10px;
  }
}
```

## Panel Background & Borders

Create distinctive panel appearances:

```css
/* Minimalist panels */
.e-panel {
  border: none;
  border-left: 4px solid #2196F3;
  box-shadow: none;
  border-radius: 0;
}

/* Card-style panels */
.e-panel {
  border: none;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.e-panel:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.3s ease;
}

/* Gradient background panels */
.e-panel {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Translucent panels */
.e-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Dark theme panels */
.e-dashboard-layout.dark .e-panel {
  background: #424242;
  border-color: #616161;
  color: #ffffff;
}

.e-dashboard-layout.dark .e-panel-header {
  background: #212121;
  border-bottom-color: #424242;
  color: #ffffff;
}

.e-dashboard-layout.dark .e-panel-content {
  background: #424242;
  color: #e0e0e0;
}
```

## Dragging State Styling

Visual feedback during drag operations:

```css
/* Dragging state */
.e-dashboard-layout .e-panel.e-dragging {
  opacity: 0.7;
  box-shadow: 0 5px 15px rgba(33, 150, 243, 0.4);
  z-index: 10000;
  transform: scale(1.02);
}

/* Drag placeholder */
.e-dashboard-layout .e-placeholder {
  border: 2px dashed #2196F3;
  background: rgba(33, 150, 243, 0.08);
  border-radius: 4px;
  animation: placeholder-pulse 0.6s ease-in-out infinite;
}

@keyframes placeholder-pulse {
  0%, 100% {
    opacity: 1;
    border-color: #2196F3;
  }
  50% {
    opacity: 0.6;
    border-color: #90caf9;
  }
}

/* Collision preview */
.e-dashboard-layout .e-panel.e-collision {
  opacity: 0.5;
  background: #f5f5f5;
}
```

## Advanced Customization

### Custom CSS Classes

```tsx
// Apply custom class to dashboard
<DashboardLayoutComponent
  id='dashboard'
  className='my-custom-dashboard'
  panels={panels}
  columns={5}
/>

// CSS
.my-custom-dashboard .e-panel {
  /* Custom panel styling */
}

.my-custom-dashboard .e-panel-header {
  /* Custom header styling */
}
```

### Scoped Styling for Individual Panels

```tsx
const panels = [
  {
    id: 'premium-panel',
    header: 'Premium Data',
    content: '<div>Premium content</div>',
    cssClass: 'premium-panel',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  },
  {
    id: 'standard-panel',
    header: 'Standard Data',
    content: '<div>Standard content</div>',
    cssClass: 'standard-panel',
    row: 0,
    col: 2,
    sizeX: 2,
    sizeY: 2
  }
];

// CSS
.e-panel.premium-panel {
  border: 2px solid gold;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.e-panel.premium-panel .e-panel-header {
  background: linear-gradient(90deg, #ffd700, #ffed4e);
  color: #333;
}

.e-panel.standard-panel {
  border: 1px solid #e0e0e0;
}
```

### Dynamic Styling with State

```tsx
function DashboardWithDynamicStyles() {
  const [theme, setTheme] = useState('light');

  return (
    <div className={`dashboard-wrapper ${theme}`}>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
      <DashboardLayoutComponent
        id='dashboard'
        className={`dashboard-${theme}`}
        panels={panels}
        columns={5}
      />
    </div>
  );
}

// CSS
.dashboard-wrapper.light .dashboard-light .e-panel {
  background: white;
  color: #333;
}

.dashboard-wrapper.dark .dashboard-dark .e-panel {
  background: #424242;
  color: #fff;
}
```

### CSS Grid Integration

```css
/* Use CSS Grid for layout */
.e-dashboard-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.e-dashboard-layout .e-panel {
  box-sizing: border-box;
}
```

### Responsive Styling

```css
/* Desktop */
@media (min-width: 1200px) {
  .e-panel {
    min-height: 400px;
  }
  
  .e-panel-header {
    padding: 16px;
  }
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1199px) {
  .e-panel {
    min-height: 300px;
  }
  
  .e-panel-header {
    padding: 12px;
  }
}

/* Mobile */
@media (max-width: 767px) {
  .e-panel {
    min-height: 250px;
    margin-bottom: 10px;
  }
  
  .e-panel-header {
    padding: 10px;
    font-size: 13px;
  }
  
  .e-panel-content {
    padding: 10px;
    font-size: 13px;
  }
}
```

### Print Styling

```css
@media print {
  .e-dashboard-layout .e-panel {
    page-break-inside: avoid;
    box-shadow: none;
    border: 1px solid #000;
  }
  
  .e-dashboard-layout .e-resize-handle {
    display: none;
  }
  
  .e-dashboard-layout .e-panel-header {
    background: #fff;
    color: #000;
    border: 1px solid #000;
  }
}
```
