# Icon Library Usage

## Table of Contents

- [Installation and Setup](#installation-and-setup)
- [Using Icons](#using-icons)
- [Icon Sizing](#icon-sizing)
- [Icon Customization](#icon-customization)
- [Common Icon Classes](#common-icon-classes)
- [Icons in Syncfusion Components](#icons-in-syncfusion-components)
- [Available Icons by Theme](#available-icons-by-theme)

## Overview

Syncfusion provides a comprehensive icon library with pre-designed, font-based icons embedded in themes. Icons ensure visual consistency across components and are available via npm or CDN.

## Installation and Setup

### Using npm

Install the icon package:

```bash
npm install @syncfusion/ej2-icons@latest
```

Import icon styles in your CSS file:

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-icons/styles/material3.css";
```

**Available themes:** `material3.css`, `fluent2.css`, `bootstrap5.css`, `tailwind3.css`, `material.css`, `bootstrap.css`, `fabric.css`, `highcontrast.css`

### Using CDN

> **⚠️ Important:** The CDN version MUST match your installed npm package version to avoid style issues.

**Find your installed version:**

```bash
npm list @syncfusion/ej2-icons
```

**Use the matching CDN version:**

```html
<!-- Replace {VERSION} with your installed package version -->
<link href="https://cdn.syncfusion.com/ej2/{VERSION}/ej2-icons/styles/material3.css" rel="stylesheet"/>

<!-- Example: If your version is 33.1.44 -->
<link href="https://cdn.syncfusion.com/ej2/33.1.44/ej2-icons/styles/material3.css" rel="stylesheet"/>
```

## Using Icons

### Basic Icon Usage

Icons require two CSS classes:
1. **`e-icons`** - Base class providing font styling
2. **Icon-specific class** - Defines the glyph (e.g., `e-paste`, `e-search`, `e-edit`)

```jsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import '@syncfusion/ej2-material3-theme/material3.css';
import '@syncfusion/ej2-icons/styles/material3.css';

function App() {
  return (
    <div>
      {/* Standalone icons */}
      <span className="e-icons e-paste"></span>
      <span className="e-icons e-search"></span>
      <span className="e-icons e-edit"></span>
      
      {/* Icons in buttons */}
      <ButtonComponent iconCss="e-icons e-save">Save</ButtonComponent>
      <ButtonComponent iconCss="e-icons e-delete">Delete</ButtonComponent>
    </div>
  );
}
```

### Custom Icon Font-Size

```css
/* Custom sizing beyond utility classes */
.icon-xl { font-size: 32px; }
.icon-xxl { font-size: 48px; }
.icon-inline { font-size: inherit; }  /* Match parent text size */
```

```jsx
<span className="e-icons e-star icon-xl"></span>
<span className="e-icons e-star icon-xxl"></span>
<h2>Heading <span className="e-icons e-info icon-inline"></span></h2>
```

## Icon Sizing

Use utility classes: `e-small` (8px), `e-medium` (16px), `e-large` (24px)

```jsx
<span className="e-icons e-small e-search"></span>
<span className="e-icons e-medium e-search"></span>
<span className="e-icons e-large e-search"></span>
```

### Responsive Sizing

```css
.icon-responsive { font-size: 16px; }
@media (min-width: 768px) { .icon-responsive { font-size: 20px; } }
@media (min-width: 1024px) { .icon-responsive { font-size: 24px; } }
```

## Icon Customization

### Color Customization

```css
.icon-primary { color: #6200ee; }
.icon-success { color: #4caf50; }
.icon-error { color: #f44336; }
```

```jsx
<span className="e-icons e-check icon-success"></span>
<span className="e-icons e-close icon-error"></span>
```

### Background and Padding

```css
.icon-badge {
  display: inline-flex;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #6200ee;
  color: white;
}
```

### CSS Effects

```css
.icon-hover { transition: all 0.3s ease; cursor: pointer; }
.icon-hover:hover { color: #6200ee; transform: scale(1.2); }

.icon-rotate { animation: rotate 2s linear infinite; }
@keyframes rotate { to { transform: rotate(360deg); } }

.icon-pulse { animation: pulse 1.5s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
```

## Common Icon Classes

### Navigation Icons
- `e-menu` - Hamburger menu
- `e-close` - Close/X button
- `e-chevron-left`, `e-chevron-right` - Navigation arrows
- `e-chevron-up`, `e-chevron-down` - Vertical navigation
- `e-expand`, `e-collapse` - Expand/collapse controls
- `e-arrow-left`, `e-arrow-right` - Back/forward arrows

### Action Icons
- `e-edit` - Edit/pencil
- `e-delete` - Delete/trash
- `e-save` - Save/disk
- `e-copy`, `e-paste`, `e-cut` - Clipboard operations
- `e-search` - Search/magnifier
- `e-filter` - Filter/funnel
- `e-add`, `e-plus` - Add/create new
- `e-remove`, `e-minus` - Remove/subtract

### Status Icons
- `e-check` - Success/checkmark
- `e-close` - Error/X
- `e-warning` - Warning/alert
- `e-info` - Information
- `e-lock`, `e-unlock` - Security status
- `e-eye`, `e-eye-slash` - Visibility toggle

### File and Media Icons
- `e-folder`, `e-folder-open` - Folder states
- `e-file` - Generic file
- `e-upload`, `e-download` - Transfer operations
- `e-image` - Image file
- `e-video` - Video file
- `e-music` - Audio file

### UI Controls
- `e-settings` - Settings/gear
- `e-more-vert`, `e-more-horiz` - More options menu
- `e-refresh` - Refresh/reload
- `e-calendar` - Calendar/date
- `e-clock` - Clock/time
- `e-bell` - Notifications
- `e-user` - User/profile

### Usage Examples

```jsx
{/* Navigation */}
<button><span className="e-icons e-menu"></span></button>
<button><span className="e-icons e-chevron-left"></span> Back</button>

{/* Actions */}
<span className="e-icons e-search"></span>
<span className="e-icons e-edit"></span>
<span className="e-icons e-delete"></span>

{/* Status indicators */}
<span className="e-icons e-check icon-success"></span>
<span className="e-icons e-warning icon-warning"></span>
```

## Icons in Syncfusion Components

### Buttons

```jsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

<ButtonComponent iconCss="e-icons e-save">Save</ButtonComponent>
<ButtonComponent iconCss="e-icons e-download" iconPosition="Right">Download</ButtonComponent>
<ButtonComponent iconCss="e-icons e-search" />  {/* Icon only */}
```

## Available Icons by Theme

Each theme includes 200+ icons. View complete icon galleries:

- **Material 3:** [https://ej2.syncfusion.com/products/icons/material3/demo.html](https://ej2.syncfusion.com/products/icons/material3/demo.html)
- **Fluent 2:** [https://ej2.syncfusion.com/products/icons/fluent2/demo.html](https://ej2.syncfusion.com/products/icons/fluent2/demo.html)
- **Bootstrap 5:** [https://ej2.syncfusion.com/products/icons/bootstrap5/demo.html](https://ej2.syncfusion.com/products/icons/bootstrap5/demo.html)
- **Tailwind 3:** [https://ej2.syncfusion.com/products/icons/tailwind3/demo.html](https://ej2.syncfusion.com/products/icons/tailwind3/demo.html)

**All themes share the same icon class names** (e.g., `e-search` works across all themes), but glyph designs vary per theme aesthetic.
