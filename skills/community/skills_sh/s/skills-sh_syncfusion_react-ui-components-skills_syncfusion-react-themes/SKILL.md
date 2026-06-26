---
name: syncfusion-react-themes
description: Use this skill when users need to apply themes, customize appearance, switch dark mode, use CSS variables, configure icons, or modify visual styling for Syncfusion React components. Covers icon library, size modes, and Theme Studio integration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Theming and Appearance"
---

# Themes in Syncfusion React Components

Syncfusion React components provide comprehensive theming support with modern, customizable themes. This skill guides you through applying themes, customizing appearance, implementing dark mode, using CSS variables, managing icons, and creating custom themes for consistent, professional React applications.

## Table of Contents

- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Patterns](#common-patterns)

## Documentation and Navigation Guide

### Built-in Themes
📄 **Read:** [references/built-in-themes.md](references/built-in-themes.md)
- Available 10+ themes
- Applying themes via npm packages, CDN, or individual component styles
- Optimized (lite) CSS files for reduced bundle size

### Dark Mode Implementation
📄 **Read:** [references/dark-mode.md](references/dark-mode.md)
- Global dark mode with `e-dark-mode` class
- Per-component dark mode
- Runtime theme switching with checkboxes or toggle buttons

### CSS Variables Customization
📄 **Read:** [references/css-variables.md](references/css-variables.md)
- CSS variable structure for each theme (Material 3, Fluent 2, Bootstrap 5.3, Tailwind 3.4)
- Customizing primary, success, warning, danger, info colors
- Runtime color modification with JavaScript
- Theme-specific variable formats (RGB vs hex values)

### Icon Library
📄 **Read:** [references/icons.md](references/icons.md)
- Setting up the icon library (npm or CDN)
- Using icons with `e-icons` class
- Icon sizing (small, medium, large)
- Customizing icon color and appearance
- Available icon sets per theme

### Size Modes
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Normal vs touch (bigger) size modes
- Enabling size modes globally or per-component
- Runtime size mode switching

### Advanced Features
📄 **Read:** [references/advanced-theming.md](references/advanced-theming.md)
- Styled-components integration
- Font customization across all components
- Theme Studio for custom theme creation

## Quick Start

### Install and Apply a Theme

**Step 1: Install Syncfusion React Package**

```bash
npm install @syncfusion/ej2-react-buttons --save
```

**Step 2: Import Theme CSS**

**Option 1: Import from npm (Recommended)**

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

**Option 2: Use CDN**

> **⚠️ Important:** The CDN version MUST match your installed npm package version to avoid style and rendering issues.

To find your installed version:

```bash
npm list @syncfusion/ej2-react-buttons
```

Then use the matching CDN version:

```html
<!-- index.html -->
<!-- Replace {VERSION} with your installed package version (e.g., 28.1.33, 33.1.44) -->
<link href="https://cdn.syncfusion.com/ej2/{VERSION}/tailwind3.css" rel="stylesheet"/>

<!-- Example: If your package version is 33.1.44 -->
<link href="https://cdn.syncfusion.com/ej2/33.1.44/tailwind3.css" rel="stylesheet"/>
```

> **Note:** Using npm imports (Option 1) is recommended as it automatically keeps CSS and JavaScript versions in sync.

## Common Patterns

### Pattern 1: Apply Dark Mode Globally

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

### Pattern 2: Customize Primary Color with CSS Variables

**For Fluent 2 Theme:**

```css
/* src/App.css */
:root {
  --color-sf-primary: #ff6b35;  /* Custom orange */
}
```

**For Material 3 Theme (uses RGB values):**

```css
/* src/App.css */
:root {
  --color-sf-primary: 255, 107, 53;  /* RGB: Custom orange */
}
```

### Pattern 3: Enable Touch Mode Globally

```html
<!-- index.html -->
<body class="e-bigger">
  <div id="root"></div>
</body>
```

Or per-component:

```typescript
<ButtonComponent cssClass="e-bigger">Touch-Friendly Button</ButtonComponent>
```

### Pattern 4: Use Optimized CSS for Faster Loading

```css
/* src/App.css - Lite version without bigger mode styles */
@import "@syncfusion/ej2/tailwind3-lite.css";
```

### Pattern 5: Use Icons from Syncfusion Library

**Install icons package:**

```bash
npm install @syncfusion/ej2-icons
```

**Import icon styles:**

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-icons/styles/tailwind3.css";
```

**Use icons in components:**

```typescript
<span className="e-icons e-cut"></span>
<span className="e-icons e-medium e-copy"></span>
<span className="e-icons e-large e-paste"></span>
```
