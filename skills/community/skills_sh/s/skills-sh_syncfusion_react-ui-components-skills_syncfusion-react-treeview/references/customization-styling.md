# TreeView Customization and Styling Guide

## Table of Contents

1. [Introduction](#introduction)
2. [CSS Class Customization](#css-class-customization)
3. [Level-Wise Styling](#level-wise-styling)
4. [Custom Expand/Collapse Icons](#custom-expandcollapse-icons)
5. [Dynamic Icon Assignment](#dynamic-icon-assignment)
6. [Full Row Selection Styling](#full-row-selection-styling)
7. [Multi-Line Text Wrapping](#multi-line-text-wrapping)
8. [Hover Effects and Animations](#hover-effects-and-animations)
9. [Font Styling by Level](#font-styling-by-level)
10. [Theme Customization](#theme-customization)
11. [Ripple Effects](#ripple-effects)
12. [CSS Classes Reference](#css-classes-reference)
13. [Real-World Examples](#real-world-examples)
14. [Troubleshooting CSS Issues](#troubleshooting-css-issues)
15. [Best Practices](#best-practices)

---

## Introduction

The Syncfusion React TreeView component provides extensive customization and styling capabilities. You can apply custom CSS classes, customize icons, modify hover effects, and implement theme-based styling to match your application's design requirements.

### Key Styling Features
- Custom CSS classes via `cssClass` property
- Level-wise styling with automatic CSS selectors
- Dynamic icon assignment per node
- Full row selection highlighting
- Multi-line text wrapping support
- Theme customization with CSS variables
- Ripple effects for better UX

---

## CSS Class Customization

### Using the cssClass Property

The `cssClass` property allows you to apply custom CSS classes to the entire TreeView component.

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';
import './custom-styles.css';

function App() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="custom-treeview-dark-theme"
    />
  );
}

export default App;
```

### Multiple CSS Classes

Apply multiple classes for compositional styling:

```tsx
<TreeViewComponent
  fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name' }}
  cssClass="custom-treeview compact-mode high-contrast"
/>
```

### Custom CSS Stylesheet

```css
/* custom-styles.css */
.custom-treeview-dark-theme {
  background-color: #1e1e1e;
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.custom-treeview-dark-theme .e-treeview {
  border: 1px solid #333;
  border-radius: 4px;
}

.compact-mode .e-list-item {
  padding: 4px 8px;
  line-height: 24px;
}

.high-contrast .e-list-item {
  border: 1px solid #666;
  margin: 2px 0;
}
```

---

## Level-Wise Styling

TreeView automatically applies level-based CSS classes for easy level-specific styling.

### Available Level Classes

- `.e-level-1` - First level items
- `.e-level-2` - Second level items
- `.e-level-3` - Third level items
- And so on (`.e-level-n` for nth level)

### Styling by Level

```tsx
function LevelStyledTreeView() {
  const data = [
    { id: 1, name: 'Department', hasChild: true },
    { id: 2, pid: 1, name: 'Team', hasChild: true },
    { id: 3, pid: 2, name: 'Member' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="org-chart-view"
    />
  );
}
```

### Level-Specific CSS

```css
/* Level 1: Departments (larger, bold) */
.org-chart-view .e-level-1 {
  font-size: 16px;
  font-weight: bold;
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 8px 12px;
}

.org-chart-view .e-level-1 .e-text-content {
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Level 2: Teams (medium) */
.org-chart-view .e-level-2 {
  font-size: 14px;
  font-weight: 500;
  background-color: #f3e5f5;
  color: #7b1fa2;
  padding: 6px 10px;
  margin-left: 10px;
}

/* Level 3: Members (regular) */
.org-chart-view .e-level-3 {
  font-size: 13px;
  font-weight: 400;
  color: #424242;
  padding: 4px 8px;
}

.org-chart-view .e-level-3 .e-text-content {
  font-style: italic;
}
```

### Dynamic Level Styling Based on Count

```css
/* Highlight levels with many children */
.org-chart-view .e-list-parent.e-level-2 {
  border-left: 4px solid #ff9800;
}

/* Leaf nodes styling */
.org-chart-view .e-list-item:not(.e-list-parent) {
  opacity: 0.85;
}

.org-chart-view .e-list-item:not(.e-list-parent):hover {
  opacity: 1;
}
```

---

## Custom Expand/Collapse Icons

### Using Template for Custom Icons

```tsx
import { TreeViewComponent } from '@syncfusion/ej2-react-navigations';

function CustomIconTreeView() {
  const data = [
    { id: 1, name: 'Folder 1', hasChild: true, icon: 'folder' },
    { id: 2, pid: 1, name: 'File 1.txt', icon: 'document' },
    { id: 3, name: 'Folder 2', hasChild: true, icon: 'folder' }
  ];

  const nodeTemplate = (props) => (
    <div className="node-container">
      <i className={`icon-${props.icon}`}></i>
      <span>{props.name}</span>
    </div>
  );

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      nodeTemplate={nodeTemplate}
    />
  );
}

export default CustomIconTreeView;
```

### CSS for Custom Icon Styling

```css
.node-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.node-container .icon-folder {
  font-size: 18px;
  color: #ff9800;
}

.node-container .icon-document {
  font-size: 16px;
  color: #2196f3;
}

/* Override default expand/collapse icons */
.e-treeview .e-icon-collapsible::before,
.e-treeview .e-icon-expandable::before {
  font-family: 'Material Icons';
  font-size: 20px;
}

.e-treeview .e-icon-collapsible::before {
  content: 'expand_less';
  color: #ff6f00;
}

.e-treeview .e-icon-expandable::before {
  content: 'expand_more';
  color: #0277bd;
}
```

### Custom Animation on Expand/Collapse

```css
.e-treeview .e-list-item > .e-icons {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.e-treeview .e-list-item.e-node-collapsed > .e-icons {
  transform: rotate(0deg);
}

.e-treeview .e-list-item:not(.e-node-collapsed) > .e-icons {
  transform: rotate(90deg);
}
```

---

## Dynamic Icon Assignment

### Icon CSS Field Approach

```tsx
function DynamicIconTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true, iconCss: 'e-icons e-folder' },
    { id: 2, pid: 1, name: 'Item 1.1', iconCss: 'e-icons e-file' },
    { id: 3, name: 'Item 2', hasChild: true, iconCss: 'e-icons e-folder-open' }
  ];

  return (
    <TreeViewComponent
      fields={{
        dataSource: data,
        id: 'id',
        parentID: 'pid',
        text: 'name',
        hasChildren: 'hasChild',
        iconCss: 'iconCss'
      }}
    />
  );
}

export default DynamicIconTreeView;
```

### Runtime Icon Updates

```tsx
function DynamicIconUpdateTreeView() {
  const treeRef = useRef(null);

  const data = [
    { id: 1, name: 'Document', hasChild: true },
    { id: 2, pid: 1, name: 'Report.pdf' },
    { id: 3, pid: 1, name: 'Guide.docx' }
  ];

  const updateNodeIcon = (nodeId, newIcon) => {
    const treeInstance = treeRef.current.ej2_instances[0];
    const node = document.getElementById(nodeId);
    if (node) {
      const iconElement = node.querySelector('.e-icons');
      if (iconElement) {
        iconElement.className = `e-icons ${newIcon}`;
      }
    }
  };

  return (
    <>
      <TreeViewComponent
        ref={treeRef}
        fields={{
          dataSource: data,
          id: 'id',
          parentID: 'pid',
          text: 'name',
          hasChildren: 'hasChild'
        }}
      />
      <button onClick={() => updateNodeIcon('1', 'e-folder-open')}>
        Update to Folder Open
      </button>
    </>
  );
}

export default DynamicIconUpdateTreeView;
```

### Icon Color Coding by Type

```css
.e-icons.e-folder {
  color: #ff9800;
}

.e-icons.e-folder-open {
  color: #ffc107;
}

.e-icons.e-file {
  color: #2196f3;
}

.e-icons.e-image {
  color: #4caf50;
}

.e-icons.e-video {
  color: #f44336;
}

.e-icons.e-audio {
  color: #9c27b0;
}
```

---

## Full Row Selection Styling

### Enabling Full Row Select

```tsx
function FullRowSelectTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2', hasChild: true }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      fullRowSelect={true}
      cssClass="full-row-selection-view"
    />
  );
}

export default FullRowSelectTreeView;
```

### Full Row Selection Styling

```css
/* Full row selection background */
.full-row-selection-view .e-fullrow.e-selectable.e-active {
  background-color: #bbdefb;
  color: #1565c0;
}

/* Full row hover effect */
.full-row-selection-view .e-fullrow:hover {
  background-color: #e3f2fd;
  border-left: 4px solid #1976d2;
  padding-left: calc(8px - 4px);
}

/* Selected state with active indicator */
.full-row-selection-view .e-fullrow.e-active {
  border-left: 4px solid #1565c0;
  box-shadow: inset 0 0 0 1px #90caf9;
  font-weight: 500;
}

/* Focus ring for accessibility */
.full-row-selection-view .e-fullrow.e-node-focus {
  outline: 2px solid #1976d2;
  outline-offset: -2px;
}
```

### Multi-Row Selection Styling

```tsx
function MultiSelectStyleTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      fullRowSelect={true}
      allowMultiSelection={true}
      cssClass="multi-select-view"
    />
  );
}

export default MultiSelectStyleTreeView;
```

```css
/* Multiple selected items */
.multi-select-view .e-fullrow.e-active {
  background: linear-gradient(90deg, #c8e6c9 0%, #81c784 100%);
  color: #1b5e20;
  transition: all 0.2s ease;
}

.multi-select-view .e-fullrow.e-active::before {
  content: '✓';
  position: absolute;
  left: 8px;
  font-weight: bold;
  color: #2e7d32;
}

.multi-select-view .e-fullrow.e-active:nth-child(odd) {
  background: linear-gradient(90deg, #bbdefb 0%, #64b5f6 100%);
  color: #01579b;
}

.multi-select-view .e-fullrow.e-active:nth-child(odd)::before {
  content: '✓';
  color: #0d47a1;
}
```

---

## Multi-Line Text Wrapping

### Enabling Text Wrapping

```tsx
function MultiLineTreeView() {
  const data = [
    {
      id: 1,
      name: 'This is a very long text that should wrap to multiple lines when the TreeView is rendered with allowTextWrap enabled',
      hasChild: true
    },
    {
      id: 2,
      pid: 1,
      name: 'Another long item text that demonstrates multi-line wrapping functionality in the TreeView component'
    }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      allowTextWrap={true}
      cssClass="multi-line-view"
    />
  );
}

export default MultiLineTreeView;
```

### Multi-Line Wrapping Styles

```css
.multi-line-view .e-text-content {
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
  line-height: 1.4;
  padding: 8px 4px;
}

.multi-line-view .e-list-item {
  height: auto;
  min-height: 36px;
}

.multi-line-view .e-icons {
  align-self: flex-start;
  margin-top: 4px;
}

/* Ellipsis for long single lines */
.multi-line-view.text-ellipsis .e-text-content {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}
```

---

## Hover Effects and Animations

### Basic Hover Effects

```css
.e-treeview .e-list-item:hover {
  background-color: #f5f5f5;
  transition: all 0.2s ease;
  border-radius: 4px;
}

.e-treeview .e-list-item:hover .e-text-content {
  color: #1976d2;
  font-weight: 500;
}

.e-treeview .e-list-item:hover .e-icons {
  opacity: 1;
  transform: scale(1.1);
}
```

### Advanced Hover with Gradient

```css
.e-treeview.advanced-hover .e-list-item:hover {
  background: linear-gradient(90deg, #e0e0e0 0%, transparent 100%);
  padding-left: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.e-treeview.advanced-hover .e-list-item:hover::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: #1976d2;
}

.e-treeview.advanced-hover .e-list-item:hover .e-text-content {
  color: #0d47a1;
  font-weight: 600;
  letter-spacing: 0.5px;
}
```

### Icon Visibility Toggle on Hover

```css
/* Hide icons by default */
.e-treeview.icon-hover-reveal .e-icons {
  opacity: 0;
  width: 0;
  transition: all 0.3s ease;
}

/* Show icons on hover */
.e-treeview.icon-hover-reveal .e-list-item:hover .e-icons {
  opacity: 1;
  width: auto;
}

.e-treeview.icon-hover-reveal .e-list-item:hover .e-text-content {
  margin-left: 8px;
}

/* Always show for expanded items */
.e-treeview.icon-hover-reveal .e-list-parent > .e-icons {
  opacity: 1;
  width: auto;
}
```

### Smooth Expand/Collapse Animation

```tsx
function AnimatedExpandTreeView() {
  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="animated-expand"
      nodeChecked={(args) => console.log('Node:', args)}
    />
  );
}
```

```css
.animated-expand .e-list-item.e-list-parent .e-ul {
  overflow: hidden;
  animation: slideDown 0.3s ease-out;
}

.animated-expand .e-list-item.e-node-collapsed .e-ul {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    max-height: 1000px;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 1;
    max-height: 1000px;
    transform: translateY(0);
  }
  to {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
}
```

---

## Font Styling by Level

### Bold Headers by Level

```tsx
function FontStyledTreeView() {
  const data = [
    { id: 1, name: 'Category', level: 1, hasChild: true },
    { id: 2, pid: 1, name: 'Subcategory', level: 2, hasChild: true },
    { id: 3, pid: 2, name: 'Item', level: 3 }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="font-styled-tree"
    />
  );
}

export default FontStyledTreeView;
```

### Comprehensive Font Styling

```css
/* Level 1: Primary headers - Large, bold, uppercase */
.font-styled-tree .e-level-1 .e-text-content {
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #1565c0;
}

/* Level 2: Secondary headers - Medium, bold */
.font-styled-tree .e-level-2 .e-text-content {
  font-size: 15px;
  font-weight: 600;
  color: #1976d2;
}

/* Level 3: Tertiary - Regular weight */
.font-styled-tree .e-level-3 .e-text-content {
  font-size: 14px;
  font-weight: 400;
  color: #424242;
}

/* Level 4 and beyond: Light weight */
.font-styled-tree .e-level-4 .e-text-content,
.font-styled-tree .e-level-5 .e-text-content {
  font-size: 13px;
  font-weight: 300;
  color: #757575;
  font-style: italic;
}

/* Emphasis on parent nodes */
.font-styled-tree .e-list-parent > .e-text-content {
  font-weight: 600;
}

/* Light weight for leaf nodes */
.font-styled-tree .e-list-item:not(.e-list-parent) .e-text-content {
  font-weight: 400;
}
```

### Color Progression by Level

```css
.font-styled-tree .e-level-1 {
  color: #0d47a1;
}

.font-styled-tree .e-level-2 {
  color: #1565c0;
}

.font-styled-tree .e-level-3 {
  color: #1976d2;
}

.font-styled-tree .e-level-4 {
  color: #42a5f5;
}

.font-styled-tree .e-level-5 {
  color: #64b5f6;
}
```

---

## Theme Customization

### Using CSS Variables for Theming

```tsx
function ThemedTreeView() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const root = document.documentElement;
    if (theme === 'light') {
      root.style.setProperty('--treeview-bg', '#ffffff');
      root.style.setProperty('--treeview-text', '#000000');
      root.style.setProperty('--treeview-accent', '#1976d2');
    } else if (theme === 'dark') {
      root.style.setProperty('--treeview-bg', '#1e1e1e');
      root.style.setProperty('--treeview-text', '#ffffff');
      root.style.setProperty('--treeview-accent', '#64b5f6');
    }
  }, [theme]);

  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' }
  ];

  return (
    <>
      <button onClick={() => setTheme('light')}>Light Theme</button>
      <button onClick={() => setTheme('dark')}>Dark Theme</button>
      <TreeViewComponent
        fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
        cssClass={`treeview-${theme}`}
      />
    </>
  );
}

export default ThemedTreeView;
```

### CSS Variables Definition

```css
:root {
  --treeview-bg: #ffffff;
  --treeview-text: #000000;
  --treeview-accent: #1976d2;
  --treeview-hover-bg: #f5f5f5;
  --treeview-selected-bg: #bbdefb;
  --treeview-border: #e0e0e0;
  --treeview-spacing: 8px;
  --treeview-radius: 4px;
}

.treeview-light {
  --treeview-bg: #ffffff;
  --treeview-text: #212121;
  --treeview-accent: #1976d2;
  --treeview-hover-bg: #f5f5f5;
  --treeview-selected-bg: #bbdefb;
}

.treeview-dark {
  --treeview-bg: #1e1e1e;
  --treeview-text: #e0e0e0;
  --treeview-accent: #64b5f6;
  --treeview-hover-bg: #2d2d2d;
  --treeview-selected-bg: #1976d2;
}

/* Apply CSS variables */
.e-treeview {
  background-color: var(--treeview-bg);
  color: var(--treeview-text);
  border: 1px solid var(--treeview-border);
  border-radius: var(--treeview-radius);
}

.e-treeview .e-list-item {
  padding: var(--treeview-spacing);
}

.e-treeview .e-list-item:hover {
  background-color: var(--treeview-hover-bg);
}

.e-treeview .e-list-item.e-active {
  background-color: var(--treeview-selected-bg);
  color: var(--treeview-accent);
}
```

---

## Ripple Effects

### Enabling Ripple Effects

```tsx
function RippleEffectTreeView() {
  const data = [
    { id: 1, name: 'Item 1', hasChild: true },
    { id: 2, pid: 1, name: 'Item 1.1' },
    { id: 3, name: 'Item 2' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      enableRipple={true}
      cssClass="ripple-enabled"
    />
  );
}

export default RippleEffectTreeView;
```

### Ripple Effect Styling

```css
.ripple-enabled .e-list-item::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(25, 118, 210, 0.3);
  transform: translate(-50%, -50%);
  animation: ripple-animation 0.6s ease-out;
}

@keyframes ripple-animation {
  to {
    width: 100%;
    height: 100%;
    opacity: 0;
  }
}

.ripple-enabled .e-list-item.e-active::after {
  background: rgba(25, 118, 210, 0.5);
}

/* Color variations for ripple */
.ripple-enabled.theme-success .e-list-item::after {
  background: rgba(76, 175, 80, 0.3);
}

.ripple-enabled.theme-danger .e-list-item::after {
  background: rgba(244, 67, 54, 0.3);
}

.ripple-enabled.theme-warning .e-list-item::after {
  background: rgba(255, 152, 0, 0.3);
}
```

---

## CSS Classes Reference

### Complete CSS Classes Table

| CSS Class | Purpose | Applied To |
|-----------|---------|-----------|
| `.e-treeview` | Root container | Main TreeView element |
| `.e-list-item` | Individual node item | Each tree node |
| `.e-list-parent` | Parent node container | Nodes with children |
| `.e-text-content` | Node text wrapper | Text content of nodes |
| `.e-icons` | Icon container | Expand/collapse icons |
| `.e-icon-collapsible` | Collapsed state icon | When parent is collapsed |
| `.e-icon-expandable` | Expanded state icon | When parent is expanded |
| `.e-checkbox-wrapper` | Checkbox container | Checkbox elements |
| `.e-level-1` to `.e-level-n` | Level styling | Nodes at specific levels |
| `.e-node-focus` | Focus indicator | Focused nodes |
| `.e-active` | Selected state | Selected nodes |
| `.e-fullrow` | Full row selection | When fullRowSelect enabled |
| `.e-node-collapsed` | Collapsed state | Collapsed parent nodes |

### Usage Examples

```css
/* Hide expand/collapse icons for leaf nodes */
.e-list-item:not(.e-list-parent) .e-icons {
  visibility: hidden;
}

/* Custom styling for parent nodes only */
.e-list-parent {
  font-weight: 600;
  background-color: #f9f9f9;
}

/* Highlight all level-2 items */
.e-level-2 {
  border-left: 3px solid #ff9800;
  padding-left: 8px;
}

/* Focus ring for accessibility */
.e-node-focus {
  outline: 2px solid #1976d2;
  outline-offset: -2px;
  border-radius: 2px;
}

/* Checkbox styling */
.e-checkbox-wrapper {
  margin-right: 8px;
}

.e-checkbox-wrapper input[type='checkbox']:checked + label::after {
  background-color: #4caf50;
}
```

---

## Real-World Examples

### File Explorer Styling

```tsx
function FileExplorerTreeView() {
  const data = [
    { id: 1, name: 'Documents', hasChild: true, type: 'folder' },
    { id: 2, pid: 1, name: 'Work', hasChild: true, type: 'folder' },
    { id: 3, pid: 2, name: 'Project.pdf', type: 'pdf' },
    { id: 4, pid: 2, name: 'Report.docx', type: 'doc' },
    { id: 5, pid: 1, name: 'Personal', hasChild: true, type: 'folder' },
    { id: 6, pid: 5, name: 'Photo.jpg', type: 'image' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass="file-explorer-theme"
      nodeTemplate={(props) => (
        <div className="file-node">
          <i className={`icon-${props.type}`}></i>
          <span>{props.name}</span>
        </div>
      )}
    />
  );
}

export default FileExplorerTreeView;
```

```css
.file-explorer-theme {
  background-color: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-family: 'Segoe UI', sans-serif;
}

.file-explorer-theme .e-list-item {
  border-bottom: 1px solid #eeeeee;
}

.file-explorer-theme .e-list-item:hover {
  background-color: #e8e8e8;
  border-left: 3px solid #1976d2;
  padding-left: 5px;
}

.file-node {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-node .icon-folder {
  color: #ff9800;
  font-size: 16px;
}

.file-node .icon-pdf {
  color: #f44336;
}

.file-node .icon-doc {
  color: #2196f3;
}

.file-node .icon-image {
  color: #4caf50;
}

.file-explorer-theme .e-level-2 {
  padding-left: 32px;
}

.file-explorer-theme .e-level-3 {
  padding-left: 56px;
}
```

### Organization Chart Colors

```tsx
function OrgChartTreeView() {
  const data = [
    { id: 1, name: 'CEO', role: 'executive', hasChild: true },
    { id: 2, pid: 1, name: 'VP Engineering', role: 'management', hasChild: true },
    { id: 3, pid: 2, name: 'Senior Developer', role: 'senior', hasChild: true },
    { id: 4, pid: 3, name: 'Junior Developer', role: 'junior' }
  ];

  return (
    <TreeViewComponent
      fields={{ dataSource: data, id: 'id', parentID: 'pid', text: 'name', hasChildren: 'hasChild' }}
      cssClass={`org-chart-${data[0].role}`}
    />
  );
}

export default OrgChartTreeView;
```

```css
.org-chart-executive .e-level-1 {
  background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
  color: white;
  font-size: 16px;
  font-weight: bold;
  padding: 12px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.org-chart-executive .e-level-2 {
  background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 10px;
  margin: 4px 0;
}

.org-chart-executive .e-level-3 {
  background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
  color: white;
  font-size: 13px;
  padding: 8px;
}

.org-chart-executive .e-level-4 {
  background-color: #e3f2fd;
  color: #0d47a1;
  font-size: 12px;
  padding: 6px;
}
```

---

## Troubleshooting CSS Issues

### Common Issues and Solutions

#### Issue 1: Styles Not Applying

```tsx
// Problem: CSS class not being applied
<TreeViewComponent
  cssClass="my-style"
  // ... other props
/>

// Solution: Ensure CSS is imported and has correct specificity
```

```css
/* Make sure selectors have enough specificity */
.my-style .e-treeview .e-list-item {
  color: red; /* With !important if needed */
}

/* Or use more specific selector */
.my-style.e-treeview .e-list-item {
  color: red;
}
```

#### Issue 2: Level Classes Not Working

```tsx
// Verify data is properly hierarchical
const data = [
  { id: 1, name: 'Level 1', hasChild: true },
  { id: 2, pid: 1, name: 'Level 2' } // Proper parent-child relationship
];

return (
  <TreeViewComponent
    fields={{
      dataSource: data,
      id: 'id',
      parentID: 'pid', // MUST be set correctly
      text: 'name',
      hasChildren: 'hasChild'
    }}
  />
);
```

#### Issue 3: Hover Effects Flickering

```css
/* Solution: Use pointer-events to prevent hover flicker */
.e-treeview .e-list-item {
  transition: all 0.2s ease; /* Smooth transition */
  pointer-events: auto;
}

.e-treeview .e-list-item:hover {
  transition-duration: 0.15s; /* Slightly faster on hover */
}

/* Prevent rapid state changes */
.e-treeview .e-list-item * {
  pointer-events: none;
}
```

#### Issue 4: Icon Not Visible

```tsx
// Verify iconCss field is properly mapped
const data = [
  { id: 1, name: 'Item', icon: 'e-icons e-folder' } // Correct format
];

<TreeViewComponent
  fields={{
    iconCss: 'icon' // Map to correct field
  }}
/>
```

#### Issue 5: Performance with Large Datasets

```css
/* Optimize rendering with will-change */
.e-treeview .e-list-item {
  will-change: transform, opacity;
}

/* Use GPU acceleration */
.e-treeview {
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* Debounce hover effects */
.e-treeview .e-list-item:hover {
  transition: all 0.3s ease; /* Longer duration for performance */
}
```

### Debugging Tips

```tsx
// Add data attributes for debugging
function DebugTreeView() {
  const nodeTemplate = (props) => (
    <div data-level={props.level} data-id={props.id}>
      {props.name}
    </div>
  );

  return (
    <TreeViewComponent
      fields={{ /* ... */ }}
      nodeTemplate={nodeTemplate}
    />
  );
}
```

```css
/* Debug CSS issues with visual indicators */
.debug-mode .e-list-item {
  border: 1px solid red;
  background-color: rgba(255, 0, 0, 0.05);
}

.debug-mode .e-level-1 {
  outline: 2px dashed blue;
}

.debug-mode .e-level-2 {
  outline: 2px dashed green;
}

.debug-mode .e-level-3 {
  outline: 2px dashed orange;
}
```

---

## Best Practices

### Do's

✅ **Use CSS variables for theming** - Makes theme changes centralized and easy
```css
:root { --primary: #1976d2; }
.element { color: var(--primary); }
```

✅ **Apply level-based styling** - Improves visual hierarchy
```css
.e-level-1 { font-size: 16px; font-weight: bold; }
.e-level-2 { font-size: 14px; font-weight: 500; }
```

✅ **Use transitions for smoothness** - Improves UX
```css
.e-list-item { transition: all 0.2s ease; }
```

✅ **Test with keyboard navigation** - Ensure accessibility
```css
.e-node-focus { outline: 2px solid #1976d2; }
```

✅ **Provide sufficient contrast** - WCAG compliance
```css
.e-list-item { color: #212121; background: #ffffff; } /* 8.59:1 contrast */
```

### Don'ts

❌ **Avoid inline styles** - Use classes for maintainability
```tsx
// Bad
<div style={{color: 'red'}}>Item</div>

// Good
<div className="item-text">Item</div>
```

❌ **Don't hide expand/collapse icons** - Harms usability
```css
/* Bad */
.e-icons { display: none; }

/* Good - if needed, use visibility for layout */
.e-icons { visibility: hidden; }
```

❌ **Avoid hardcoded colors** - Use CSS variables
```css
/* Bad */
.e-list-item { color: #1976d2; }

/* Good */
.e-list-item { color: var(--primary); }
```

❌ **Don't overuse animations** - Can impact performance
```css
/* Bad */
* { transition: all 0.1s ease; }

/* Good */
.e-list-item { transition: background-color 0.2s ease; }
```

### Performance Tips

1. **Use CSS Grid/Flexbox** instead of floats for layout
2. **Minimize repaints** by batching style changes
3. **Use will-change** sparingly for frequently animated elements
4. **Lazy-load styles** for large datasets
5. **Profile with DevTools** to identify bottlenecks
