# Positioning and Layout

## Table of Contents
- [Position Overview](#position-overview)
- [Top AppBar (Default)](#top-appbar-default)
- [Bottom AppBar](#bottom-appbar)
- [Sticky AppBar](#sticky-appbar)
- [Spacer for Content Alignment](#spacer-for-content-alignment)
- [Separator for Visual Grouping](#separator-for-visual-grouping)
- [Responsive Design](#responsive-design)

## Position Overview

The AppBar position can be controlled using:
- **`position` prop:** Sets vertical position ("Top" | "Bottom")
- **`isSticky` prop:** Makes AppBar fixed during scroll (boolean)

| Position | Use Case |
|----------|----------|
| **Top** | Default, main navigation, most common |
| **Bottom** | Mobile apps, action bars, floating actions |
| **Sticky** | Keep navigation visible while scrolling content |

## Top AppBar (Default)

Top positioning is the default behavior. The AppBar sits at the top of your content.

**When to use:**
- Main application header
- Navigation menus
- Logo and branding placement
- Desktop applications

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <AppBarComponent colorMode="Primary">
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
      </AppBarComponent>
      
      <div className="appbar-content" style={{ padding: '20px', fontSize: '12px' }}>
        <p>Main content of your application goes here.</p>
        <p>Scroll down to see more content while AppBar stays at top.</p>
        {/* Add more content */}
      </div>
    </>
  );
}

export default App;
```

**Key Points:**
- Default position value is "Top"
- Content flows below the AppBar
- No prop needed to set top position

## Bottom AppBar

Bottom positioning places the AppBar at the bottom of your content. Use for mobile action bars or floating action buttons.

**When to use:**
- Mobile apps (bottom navigation is standard)
- Action bars (Save, Cancel, Delete buttons)
- Floating action buttons
- Secondary navigation

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <div className="main-content" style={{ height: '400px', padding: '20px' }}>
        <h2>Document or Form Content</h2>
        <p>Your main content goes here.</p>
      </div>
      
      <AppBarComponent colorMode="Primary" position="Bottom">
        <ButtonComponent cssClass="e-inherit">Cancel</ButtonComponent>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit" isPrimary>Save</ButtonComponent>
      </AppBarComponent>
    </>
  );
}

export default App;
```

**Common Patterns:**
- **Mobile navigation:** Bottom AppBar with home, search, profile buttons
- **Document editor:** Bottom AppBar with Save/Cancel/Delete
- **List with actions:** Bottom AppBar with select, delete, share options

## Sticky AppBar

Sticky AppBar stays fixed at the top (or bottom) of the viewport while you scroll the content beneath it.

**When to use:**
- Keep navigation always accessible
- Long scrolling pages or documents
- Fixed toolbars that users always need access to
- Sticky headers in dashboards

### Method 1: Using `isSticky` Prop

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <AppBarComponent colorMode="Primary" isSticky>
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>My App</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">Profile</ButtonComponent>
      </AppBarComponent>
      
      <div style={{ padding: '20px' }}>
        <h2>Scroll Down to See Sticky AppBar</h2>
        {/* Long content that scrolls */}
        {Array.from({length: 30}).map((_, i) => (
          <p key={i}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
            Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </p>
        ))}
      </div>
    </>
  );
}

export default App;
```

### Sticky + Bottom Position

Combine sticky with bottom position for action bars:

```tsx
<AppBarComponent 
  colorMode="Primary" 
  position="Bottom" 
  isSticky
>
  <ButtonComponent cssClass="e-inherit">Discard</ButtonComponent>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit" isPrimary>Submit</ButtonComponent>
</AppBarComponent>
```

## Spacer for Content Alignment

The spacer (`e-appbar-spacer`) creates flexible horizontal spacing to push content to edges.

**When to use:**
- Logo/brand on left, navigation in center, user profile on right
- Left-aligned menu button, right-aligned search box
- Centering content with balanced spacing

### Single Spacer (Right-Align)

```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>My App</span>
  <div className="e-appbar-spacer"></div>
  {/* Everything below pushes to the right */}
  <ButtonComponent cssClass="e-inherit">Settings</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">Logout</ButtonComponent>
</AppBarComponent>
```

### Multiple Spacers (Distributed Layout)

```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <div className="e-appbar-spacer"></div>
  {/* Center content */}
  <span>Centered Title</span>
  <div className="e-appbar-spacer"></div>
  {/* Right-aligned buttons */}
  <ButtonComponent cssClass="e-inherit">Help</ButtonComponent>
</AppBarComponent>
```

**Key Points:**
- `<div className="e-appbar-spacer"></div>` takes remaining horizontal space
- Multiple spacers distribute content evenly
- No width/flex properties needed—spacer handles it

## Separator for Visual Grouping

The separator (`e-appbar-separator`) displays a vertical line to visually group related buttons or content.

**When to use:**
- Group editing tools (Cut, Copy, Paste)
- Separate navigation from actions (Menu | Home, About | Settings, Logout)
- Organize toolbar buttons into logical sections

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary" mode="Dense">
      {/* Editing tools group */}
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
      
      {/* Visual separator */}
      <div className="e-appbar-separator"></div>
      
      {/* Formatting group */}
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-bold"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-italic"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-underline"></ButtonComponent>
      
      {/* Another separator */}
      <div className="e-appbar-separator"></div>
      
      {/* Alignment group */}
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-align-left"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-align-center"></ButtonComponent>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-align-right"></ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

## Responsive Design

Use media queries to adjust AppBar layout for different screen sizes.

### Example: Responsive Navigation

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React, { useState } from "react";
import './App.css';

const App = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="brand">My Brand</span>
      
      {/* Visible on desktop, hidden on mobile */}
      <div className="nav-desktop">
        <ButtonComponent cssClass="e-inherit">Home</ButtonComponent>
        <ButtonComponent cssClass="e-inherit">About</ButtonComponent>
        <ButtonComponent cssClass="e-inherit">Services</ButtonComponent>
      </div>
      
      <div className="e-appbar-spacer"></div>
      
      <ButtonComponent cssClass="e-inherit">Contact</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**App.css:**
```css
/* Desktop: Show navigation buttons */
@media (min-width: 768px) {
  .nav-desktop {
    display: flex;
    gap: 10px;
  }
}

/* Mobile: Hide navigation buttons */
@media (max-width: 767px) {
  .nav-desktop {
    display: none;
  }
}

.brand {
  margin-left: 10px;
  font-weight: bold;
}
```

### Responsive Bottom AppBar

For mobile-first apps, switch to bottom AppBar on mobile and top on desktop:

```tsx
const App = () => {
  const isMobile = window.innerWidth < 768;
  
  return (
    <AppBarComponent 
      colorMode="Primary"
      position={isMobile ? "Bottom" : "Top"}
    >
      {/* AppBar content */}
    </AppBarComponent>
  );
}
```

## Complete Example: Full-Featured Layout

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      {/* Main Navigation AppBar - Sticky at top */}
      <AppBarComponent 
        colorMode="Primary" 
        isSticky
      >
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span className="logo">MyApp</span>
        
        <div className="e-appbar-spacer"></div>
        <div className="e-appbar-separator"></div>
        
        <ButtonComponent cssClass="e-inherit">Profile</ButtonComponent>
      </AppBarComponent>
      
      {/* Main content with long scrolling */}
      <div style={{ padding: '20px', minHeight: '2000px' }}>
        <h2>Long Content Area</h2>
        {/* Your page content */}
      </div>
      
      {/* Bottom Action AppBar - Fixed at bottom */}
      <AppBarComponent 
        colorMode="Primary" 
        position="Bottom"
      >
        <ButtonComponent cssClass="e-inherit">Cancel</ButtonComponent>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit" isPrimary>Save</ButtonComponent>
      </AppBarComponent>
    </>
  );
}

export default App;
```

This creates a sophisticated layout with sticky top navigation and fixed bottom actions.
