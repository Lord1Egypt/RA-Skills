# Size and Color Modes

## Table of Contents
- [Mode Property Overview](#mode-property-overview)
- [Regular Mode (Default)](#regular-mode-default)
- [Prominent Mode](#prominent-mode)
- [Dense Mode](#dense-mode)
- [ColorMode Property Overview](#colormode-property-overview)
- [Light Color Mode](#light-color-mode)
- [Dark Color Mode](#dark-color-mode)
- [Primary Color Mode](#primary-color-mode)
- [Inherit Color Mode](#inherit-color-mode)
- [Mode and ColorMode Combinations](#mode-and-colormode-combinations)

## Mode Property Overview

The `mode` prop controls the height/size of the AppBar. Choose based on your content and visual hierarchy needs.

| Mode | Height | Use Case |
|------|--------|----------|
| **Regular** | Default (~56px) | Standard navigation, most common |
| **Prominent** | Large (~128px) | Large titles, branding, hero sections |
| **Dense** | Compact (~48px) | Toolbars, tight spaces, mobile |

## Regular Mode (Default)

Regular mode is the default height, suitable for most applications.

**When to use:**
- Standard navigation bars
- Most web applications
- Desktop apps
- When you don't need extra vertical space

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="regular">Regular AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Characteristics:**
- Default height provides good balance
- Suitable for icons + text content
- Works well with regular-sized buttons
- Recommended height: ~56px

## Prominent Mode

Prominent mode has extra height, ideal for large titles, branding, or hero sections.

**When to use:**
- Main page headers with large titles
- Application branding with logos
- Hero sections with background images
- Sections requiring visual hierarchy

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary" 
      mode="Prominent" 
      cssClass="prominent-appbar"
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="prominent">AppBar with Prominent Mode</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

### Customizing Prominent Height

By default, prominent mode has a standard height. Customize it with CSS:

```css
/* Adjust the height of prominent AppBar */
.prominent-appbar.e-prominent {
  height: 200px; /* Custom height */
}

.prominent {
  align-self: center;  /* Vertically center text */
  white-space: normal; /* Allow text wrapping */
  font-size: 24px;     /* Larger font for prominent mode */
}
```

### Prominent with Background Image

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary" 
      mode="Prominent" 
      cssClass="prominent-hero"
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="hero-title">Welcome to Our App</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">Get Started</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**App.css:**
```css
.prominent-hero {
  background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
              url('hero-image.jpg') center/cover;
  height: 250px;
}

.hero-title {
  font-size: 28px;
  color: white;
  font-weight: bold;
}
```

## Dense Mode

Dense mode has reduced height, perfect for tight spaces and toolbars.

**When to use:**
- Compact toolbars
- Mobile layouts (save vertical space)
- Multiple AppBars on same page
- Document editors with tool palettes

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary" mode="Dense">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="dense">Dense AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Characteristics:**
- Compact height (~48px)
- Saves vertical screen real estate
- Better for mobile devices
- Good for stacked toolbars

### Dense Toolbar Example

```tsx
<AppBarComponent colorMode="Dark" mode="Dense">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
  <div className="e-appbar-separator"></div>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-undo"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-redo"></ButtonComponent>
</AppBarComponent>
```

## ColorMode Property Overview

The `colorMode` prop controls the background and text colors. Choose to match your brand or visual hierarchy.

| ColorMode | Background | Use Case |
|-----------|-----------|----------|
| **Light** | Light/white | Default, minimal, clean look |
| **Dark** | Dark/black | Modern, high contrast, night mode |
| **Primary** | Primary brand color | Emphasis, main navigation |
| **Inherit** | Parent element color | Custom theming, context-aware |

## Light Color Mode (Default)

Light mode displays with a light background and dark text. It's the default and most accessible.

**When to use:**
- Default navigation bars
- When you need minimal visual emphasis
- Accessibility priority
- Clean, minimalist designs

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Light">
      <a href="/" role="link" aria-label="Syncfusion">
        <div className="syncfusion-logo"></div>
      </a>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent isPrimary>Sign In</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Characteristics:**
- Light/white background
- Dark text for contrast
- Most accessible by default
- Professional appearance

## Dark Color Mode

Dark mode displays with a dark background and light text. Great for modern, high-contrast designs.

**When to use:**
- Dark/night mode interfaces
- Modern applications
- High contrast needs
- Gaming or media applications

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Dark">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span>Dark Mode AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-setting"></ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Characteristics:**
- Dark/black background
- Light/white text
- High contrast, modern look
- Reduces eye strain in low-light environments

## Primary Color Mode

Primary mode uses your brand's primary color for maximum visual impact and navigation emphasis.

**When to use:**
- Main application navigation
- Brand emphasis
- Call-to-action headers
- Primary navigation bars

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span>Primary AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Characteristics:**
- Brand primary color background
- Automatically adjusted text color
- Strong visual emphasis
- Most commonly used in modern apps

## Inherit Color Mode

Inherit mode takes colors from the parent element, allowing you to create custom themes and context-aware AppBars.

**When to use:**
- Custom color schemes
- Dynamic theming
- Context-aware styling
- Advanced customization

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  return (
    <div className="custom-appbar-container">
      <AppBarComponent colorMode="Inherit">
        <a href="/" role="link">
          <div className="syncfusion-logo"></div>
        </a>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent isPrimary>Sign In</ButtonComponent>
      </AppBarComponent>
    </div>
  );
}

export default App;
```

**App.css:**
```css
.custom-appbar-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.custom-appbar-container .e-appbar {
  /* AppBar inherits background and color from parent */
  background: inherit;
  color: inherit;
}
```

## Mode and ColorMode Combinations

Combine mode and colorMode for different effects:

### Example 1: Prominent Dark Header
```tsx
<AppBarComponent 
  mode="Prominent" 
  colorMode="Dark" 
  cssClass="prominent-dark"
>
  <span>Large Dark Header</span>
</AppBarComponent>
```

### Example 2: Dense Primary Toolbar
```tsx
<AppBarComponent 
  mode="Dense" 
  colorMode="Primary"
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
</AppBarComponent>
```

### Example 3: Regular Light Navigation
```tsx
<AppBarComponent colorMode="Light">
  <ButtonComponent cssClass="e-inherit">Home</ButtonComponent>
  <ButtonComponent cssClass="e-inherit">About</ButtonComponent>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent>Login</ButtonComponent>
</AppBarComponent>
```

### Example 4: Dense Inherit (Custom)
```tsx
<div style={{ background: '#ff6b6b', color: 'white' }}>
  <AppBarComponent mode="Dense" colorMode="Inherit">
    <span>Custom Colored Compact Bar</span>
  </AppBarComponent>
</div>
```

## Complete Example: Multiple AppBars with Different Modes

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      {/* Main Navigation - Regular Primary */}
      <AppBarComponent colorMode="Primary">
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>My Application</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">Account</ButtonComponent>
      </AppBarComponent>
      
      {/* Secondary Toolbar - Dense Dark */}
      <AppBarComponent mode="Dense" colorMode="Dark">
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
      </AppBarComponent>
      
      {/* Hero Section - Prominent Light */}
      <AppBarComponent mode="Prominent" colorMode="Light">
        <span className="hero-text">Welcome to Our Service</span>
      </AppBarComponent>
      
      <div style={{ padding: '20px' }}>
        <h2>Page Content</h2>
        <p>Your main content goes here.</p>
      </div>
    </>
  );
}

export default App;
```

This demonstrates how different combinations create visual hierarchy and serve different purposes in your application.
