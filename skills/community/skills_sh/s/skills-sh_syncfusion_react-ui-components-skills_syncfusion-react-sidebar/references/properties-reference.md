# Properties Reference

## Table of Contents
- [Overview](#overview)
- [Core Properties](#core-properties)
  - [target](#target)
  - [width](#width)
  - [position](#position)
  - [type](#type)
  - [isOpen](#isopen)
- [Display Properties](#display-properties)
  - [showBackdrop](#showbackdrop)
  - [animate](#animate)
  - [zIndex](#zindex)
- [Behavior Properties](#behavior-properties)
  - [closeOnDocumentClick](#closeondocumentclick)
  - [enableGestures](#enablegestures)
  - [enableRtl](#enablertl)
  - [mediaQuery](#mediaquery)
  - [enableDock](#enabledock)
  - [dockSize](#docksize)
  - [enablePersistence](#enablepersistence)
- [Quick Reference Table](#quick-reference-table)

---

## Overview

The Sidebar component provides 18 properties to control appearance, behavior, and state. This reference covers all properties with types, defaults, and practical examples.

---

## Core Properties

### target

**Type:** `HTMLElement | string`  
**Default:** `null`

Specifies the container element where the sidebar should be rendered. This allows placing the sidebar inside a specific DOM element instead of the document body.

**Use Cases:**
- Rendering sidebar within a specific container
- Multiple sidebars in different containers
- Custom layout patterns

**Example:**
```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const containerRef = useRef(null);

  return (
    <div>
      {/* Target container for sidebar */}
      <div ref={containerRef} className="sidebar-container" style={{ position: 'relative', height: '500px' }}>
        <SidebarComponent
          target={containerRef.current}
          width="250px"
          type="Push"
        >
          <div>Sidebar content inside target container</div>
        </SidebarComponent>
      </div>
    </div>
  );
}

export default App;
```

---

### width

**Type:** `string | number`  
**Default:** `'auto'`

Sets the width of the sidebar. Can be specified in pixels (e.g., `'250px'`) or percentage (e.g., `'25%'`).

**Example:**
```jsx
<SidebarComponent width="280px" />
<SidebarComponent width="25%" />
<SidebarComponent width={250} />
```

---

### position

**Type:** `'Left' | 'Right'`  
**Default:** `'Left'`

Determines sidebar placement relative to main content.

**Example:**
```jsx
// Left-aligned sidebar (default)
<SidebarComponent position="Left" />

// Right-aligned sidebar (for RTL or alternative layouts)
<SidebarComponent position="Right" />
```

---

### type

**Type:** `'Over' | 'Push' | 'Slide' | 'Auto'`  
**Default:** `'Auto'`

Specifies how the sidebar interacts with main content:
- **Over** - Floats above content, no content movement
- **Push** - Pushes content aside when open
- **Slide** - Translates content without resizing
- **Auto** - Over on mobile, Push on desktop

**Example:**
```jsx
// Floating drawer menu (mobile pattern)
<SidebarComponent type="Over" />

// Sidebar with content shift (desktop pattern)
<SidebarComponent type="Push" />

// Responsive behavior
<SidebarComponent type="Auto" />
```

---

### isOpen

**Type:** `boolean`  
**Default:** `false`

Controls the open/closed state of the sidebar. For `Auto` type, this property is ignored on mobile (type becomes Over regardless).

**Example:**
```jsx
import { useState } from 'react';

function App() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <SidebarComponent
      isOpen={isOpen}
      change={(args) => setIsOpen(args.element.classList.contains('e-open'))}
    >
      Content
    </SidebarComponent>
  );
}
```

---

## Display Properties

### showBackdrop

**Type:** `boolean`  
**Default:** `false`

Displays a semi-transparent overlay behind the sidebar when open. Commonly used with `Over` type sidebars.

**Example:**
```jsx
<SidebarComponent
  type="Over"
  showBackdrop={true}
  closeOnDocumentClick={true}
/>
```

**CSS Styling:**
```css
.e-sidebar-overlay {
  background-color: rgba(0, 0, 0, 0.5);
  opacity: 0.5;
}
```

---

### animate

**Type:** `boolean`  
**Default:** `true`

Enables smooth CSS transitions when opening/closing the sidebar.

**Example:**
```jsx
// With animation
<SidebarComponent animate={true} />

// Without animation (instant)
<SidebarComponent animate={false} />
```

---

### zIndex

**Type:** `string | number`  
**Default:** `1000`

Sets the CSS z-index for the sidebar (applicable to `Over` type). Controls layering above other elements.

**Example:**
```jsx
<SidebarComponent
  type="Over"
  zIndex={9999}
  showBackdrop={true}
/>
```

---

## Behavior Properties

### closeOnDocumentClick

**Type:** `boolean`  
**Default:** `false`

Automatically closes the sidebar when clicking on the main content area. Useful for drawer/modal-like behavior.

**Example:**
```jsx
<SidebarComponent
  type="Over"
  closeOnDocumentClick={true}
/>
```

---

### enableGestures

**Type:** `boolean`  
**Default:** `true`

Enables touch swipe gestures on mobile devices to open/close the sidebar.

**Example:**
```jsx
<SidebarComponent
  enableGestures={true}  // Swipe to open/close
  type="Over"
/>
```

---

### enableRtl

**Type:** `boolean`  
**Default:** `false`

Renders the sidebar in right-to-left (RTL) mode for Arabic, Hebrew, and other RTL languages.

**Example:**
```jsx
<SidebarComponent
  enableRtl={true}
  position="Right"
/>
```

---

### mediaQuery

**Type:** `string | MediaQueryList`  
**Default:** `null`

CSS media query string that triggers sidebar state. Sidebar auto-opens when media query matches.

**Example:**
```jsx
// Open sidebar on screens wider than 768px
<SidebarComponent
  mediaQuery="(min-width: 768px)"
  isOpen={false}
  type="Over"
/>

// Custom breakpoint
<SidebarComponent
  mediaQuery="(max-width: 600px)"
/>
```

---

### enableDock

**Type:** `boolean`  
**Default:** `false`

Enables dock/minimize mode - sidebar collapses to a narrow panel showing only icons.

**Example:**
```jsx
<SidebarComponent
  enableDock={true}
  dockSize="50px"
  width="250px"
/>
```

---

### dockSize

**Type:** `string | number`  
**Default:** `'auto'`

Width of the sidebar when docked (only applicable when `enableDock={true}`).

**Example:**
```jsx
<SidebarComponent
  enableDock={true}
  dockSize="50px"       // Icon-only bar
  width="250px"         // Expanded width
  type="Push"
/>
```

---

### enablePersistence

**Type:** `boolean`  
**Default:** `false`

Saves sidebar state (position and type) to browser storage and restores it on page reload.

**Example:**
```jsx
<SidebarComponent
  enablePersistence={true}
  position="Left"
  type="Auto"
/>
```

---

## Quick Reference Table

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| **target** | `HTMLElement \| string` | `null` | Container element |
| **width** | `string \| number` | `'auto'` | Sidebar width |
| **position** | `'Left' \| 'Right'` | `'Left'` | Placement |
| **type** | `'Over' \| 'Push' \| 'Slide' \| 'Auto'` | `'Auto'` | Display mode |
| **isOpen** | `boolean` | `false` | Open state |
| **showBackdrop** | `boolean` | `false` | Overlay |
| **animate** | `boolean` | `true` | Animations |
| **zIndex** | `string \| number` | `1000` | Layer |
| **closeOnDocumentClick** | `boolean` | `false` | Auto-close |
| **enableGestures** | `boolean` | `true` | Touch swipe |
| **enableRtl** | `boolean` | `false` | RTL mode |
| **mediaQuery** | `string \| MediaQueryList` | `null` | Responsive |
| **enableDock** | `boolean` | `false` | Dock mode |
| **dockSize** | `string \| number` | `'auto'` | Dock width |
| **enablePersistence** | `boolean` | `false` | Save state |

---
