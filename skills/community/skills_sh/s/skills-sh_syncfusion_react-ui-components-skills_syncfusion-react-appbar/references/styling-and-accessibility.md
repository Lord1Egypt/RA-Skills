# Styling and Accessibility

## Table of Contents
- [CSS Customization](#css-customization)
- [Available CSS Classes](#available-css-classes)
- [CssClass Property](#cssclass-property)
- [HTML Attributes](#html-attributes)
- [Accessibility Features](#accessibility-features)
- [WCAG 2.2 Compliance](#wcag-22-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Color Contrast](#color-contrast)
- [Mobile and RTL Support](#mobile-and-rtl-support)

## CSS Customization

The AppBar component provides CSS classes for styling different aspects of the component. You can override these classes to customize appearance.

### Basic Customization

```css
/* Main AppBar container */
.e-appbar {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
}

/* Prominent AppBar */
.e-appbar.e-prominent {
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Dense AppBar */
.e-appbar.e-dense {
  height: 48px;
}

/* Light color mode */
.e-appbar.e-light {
  background-color: #f8f9fa;
  color: #333;
}

/* Dark color mode */
.e-appbar.e-dark {
  background-color: #212529;
  color: #fff;
}
```

## Available CSS Classes

The AppBar generates specific CSS classes based on its properties:

| CSS Class | Purpose | When Applied |
|-----------|---------|--------------|
| `.e-appbar` | Main AppBar container | Always |
| `.e-appbar.e-prominent` | Prominent height mode | `mode="Prominent"` |
| `.e-appbar.e-dense` | Dense height mode | `mode="Dense"` |
| `.e-appbar.e-light` | Light background color | `colorMode="Light"` |
| `.e-appbar.e-dark` | Dark background color | `colorMode="Dark"` |
| `.e-appbar.e-primary` | Primary brand color | `colorMode="Primary"` |
| `.e-appbar.e-inherit` | Inherit from parent | `colorMode="Inherit"` |
| `.e-appbar-spacer` | Flexible horizontal spacing | On spacer elements |
| `.e-appbar-separator` | Vertical divider line | On separator elements |

## CssClass Property

Use the `cssClass` prop to apply custom classes to the AppBar:

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary" 
      cssClass="custom-appbar"
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-home"></ButtonComponent>
      <span>Custom Styled AppBar</span>
    </AppBarComponent>
  );
}

export default App;
```

**App.css:**
```css
/* Override default styling with custom class */
.custom-appbar {
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  border-bottom: 3px solid #ff6b6b;
  padding: 12px 24px;
}

.custom-appbar .e-inherit {
  font-weight: 500;
}
```

### Multi-Class Styling

Apply multiple classes for complex customization:

```tsx
<AppBarComponent 
  colorMode="Primary" 
  mode="Prominent"
  cssClass="custom-appbar elevated-shadow gradient-bg"
>
  {/* Content */}
</AppBarComponent>
```

**App.css:**
```css
.custom-appbar {
  /* Custom styling */
}

.elevated-shadow {
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}
```

## HTML Attributes

Set HTML attributes on the AppBar using the standard JSX attributes:

### ARIA Labels for Accessibility

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary"
      role="banner"
      aria-label="Main application navigation bar"
    >
      <ButtonComponent 
        cssClass="e-inherit" 
        iconCss="e-icons e-menu"
        aria-label="Open navigation menu"
      ></ButtonComponent>
      
      <span>Application Title</span>
      
      <div className="e-appbar-spacer"></div>
      
      <ButtonComponent 
        cssClass="e-inherit" 
        aria-label="User account menu"
      >
        Account
      </ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

### Data Attributes for Custom Functionality

```tsx
<AppBarComponent 
  colorMode="Primary"
  data-testid="main-appbar"
  data-analytics="navigation"
>
  {/* Content */}
</AppBarComponent>
```

## Accessibility Features

The AppBar component is built with accessibility in mind and supports:

### WCAG 2.2 Compliance

| Feature | Support | Details |
|---------|---------|---------|
| Level A | ✓ | Basic accessibility guidelines |
| Level AA | ✓ | Enhanced contrast and navigation |
| Level AAA | ✓ | Maximum accessibility compliance |

### Section 508 Support

✓ Fully compliant with Section 508 accessibility standards

### Screen Reader Support

✓ All AppBar content is announced correctly by screen readers

### Keyboard Navigation

✓ Full keyboard support with Tab navigation between controls

### Color Contrast

✓ All color modes meet WCAG contrast requirements

## WCAG 2.2 Compliance

The AppBar meets WCAG 2.2 standards across all levels:

```tsx
// Compliant AppBar structure
<AppBarComponent 
  colorMode="Primary"
  role="banner"
  aria-label="Application navigation"
>
  <ButtonComponent 
    cssClass="e-inherit"
    iconCss="e-icons e-menu"
    aria-label="Toggle navigation menu"
  ></ButtonComponent>
  
  <nav aria-label="Main navigation">
    <span>Navigation Items</span>
  </nav>
  
  <div className="e-appbar-spacer"></div>
  
  <div role="navigation" aria-label="User menu">
    <ButtonComponent>Profile</ButtonComponent>
  </div>
</AppBarComponent>
```

### Sufficient Color Contrast

All color modes provide sufficient contrast ratios:
- **Light mode:** Dark text on light background (✓ 4.5:1)
- **Dark mode:** Light text on dark background (✓ 4.5:1)
- **Primary mode:** Adjusted text on brand color (✓ 4.5:1)

## Keyboard Navigation

The AppBar fully supports keyboard navigation:

### Navigation Keys

| Key | Action |
|-----|--------|
| **Tab** | Move focus to next interactive element |
| **Shift + Tab** | Move focus to previous interactive element |
| **Enter** | Activate focused button or menu |
| **Space** | Activate focused button |
| **Arrow Keys** | Navigate menu items (when menu is open) |
| **Esc** | Close open menus or dropdowns |

### Example: Keyboard-Accessible AppBar

```tsx
import { AppBarComponent, MenuComponent, MenuItemModel } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const menuItems: MenuItemModel[] = [
    {
      text: 'File',
      items: [
        { text: 'New (Ctrl+N)' },
        { text: 'Open (Ctrl+O)' },
        { text: 'Save (Ctrl+S)' }
      ]
    },
    {
      text: 'Edit',
      items: [
        { text: 'Undo (Ctrl+Z)' },
        { text: 'Redo (Ctrl+Y)' },
        { text: 'Cut (Ctrl+X)' }
      ]
    }
  ];

  return (
    <AppBarComponent colorMode="Primary">
      {/* Keyboard accessible menu */}
      <MenuComponent 
        cssClass="e-inherit"
        items={menuItems}
      ></MenuComponent>
      
      {/* Keyboard accessible buttons */}
      <ButtonComponent 
        cssClass="e-inherit"
        tabIndex={0}
        aria-label="Save document (Ctrl+S)"
      >
        Save
      </ButtonComponent>
      
      <ButtonComponent 
        cssClass="e-inherit"
        tabIndex={0}
        aria-label="Print document (Ctrl+P)"
      >
        Print
      </ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

## Screen Reader Support

The AppBar is fully compatible with screen readers (NVDA, JAWS, VoiceOver):

### Screen Reader Announcements

```tsx
<AppBarComponent 
  colorMode="Primary"
  role="banner"
  aria-label="Application header and main navigation"
>
  <ButtonComponent 
    cssClass="e-inherit"
    iconCss="e-icons e-menu"
    aria-label="Open navigation menu"
    title="Open navigation menu"  // Tooltip for mouse users
  ></ButtonComponent>
  
  <span aria-live="polite">Application Status</span>
  
  <div className="e-appbar-spacer"></div>
  
  <ButtonComponent 
    cssClass="e-inherit"
    iconCss="e-icons e-user"
    aria-label="User account menu"
    aria-haspopup="menu"
    aria-expanded="false"
  ></ButtonComponent>
</AppBarComponent>
```

### Screen Reader Testing

The AppBar is validated with:
- **NVDA** (Windows)
- **JAWS** (Windows)
- **VoiceOver** (macOS/iOS)

All content is properly announced and navigable.

## Color Contrast

All AppBar color modes meet WCAG AA standards (4.5:1 contrast ratio):

### Contrast Verification

```tsx
// Light Mode - Dark text on light background
<AppBarComponent colorMode="Light">
  {/* Contrast ratio: 5.2:1 - WCAG AAA ✓ */}
</AppBarComponent>

// Dark Mode - Light text on dark background
<AppBarComponent colorMode="Dark">
  {/* Contrast ratio: 5.1:1 - WCAG AAA ✓ */}
</AppBarComponent>

// Primary Mode - Theme color with adjusted text
<AppBarComponent colorMode="Primary">
  {/* Contrast ratio: 4.8:1 - WCAG AA ✓ */}
</AppBarComponent>
```

### Custom Color Verification

When customizing colors, ensure sufficient contrast:

```css
/* Good: High contrast */
.custom-appbar {
  background-color: #0066cc;  /* Blue */
  color: #ffffff;             /* White */
  /* Contrast ratio: 8.5:1 ✓ */
}

/* Bad: Insufficient contrast */
.custom-appbar {
  background-color: #cccccc;  /* Light gray */
  color: #999999;             /* Medium gray */
  /* Contrast ratio: 1.4:1 ✗ */
}
```

Use a contrast checker tool: url

## Mobile and RTL Support

The AppBar fully supports mobile layouts and right-to-left languages:

### Mobile Support

The AppBar responds to touch interactions and mobile viewports:

```tsx
const App = () => {
  const isMobile = window.innerWidth < 768;
  
  return (
    <AppBarComponent 
      colorMode="Primary"
      mode={isMobile ? "Dense" : "Regular"}  // Compact on mobile
      position={isMobile ? "Top" : "Top"}
    >
      {/* Mobile-optimized content */}
    </AppBarComponent>
  );
}
```

### Right-to-Left (RTL) Support

The AppBar automatically mirrors layout for RTL languages:

```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const isRTL = true; // Set based on language
  
  return (
    <div dir={isRTL ? "rtl" : "ltr"}>
      <AppBarComponent colorMode="Primary">
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>التطبيق</span> {/* Arabic text */}
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">تسجيل الدخول</ButtonComponent>
      </AppBarComponent>
    </div>
  );
}

export default App;
```

**CSS for RTL:**
```css
[dir="rtl"] .e-appbar {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .e-appbar-separator {
  transform: scaleX(-1);
}
```

### Device Support

✓ Desktop browsers  
✓ Tablet/iPad  
✓ Mobile phones  
✓ Touch screens  
✓ Keyboard navigation  

## Accessibility Validation Tools

The AppBar is validated using automated accessibility testing:

### Tools Used

- **Accessibility Checker** - Automatic compliance validation
- **Axe-core** - Accessibility audit tool
- **WAVE** - Web accessibility evaluation tool

### Running Accessibility Tests

```bash
# Install accessibility checker
npm install accessibility-checker

# Run validation
npx accessibility-checker --url url
```

### Manual Testing Checklist

- [ ] Tab through all controls - all interactive elements accessible
- [ ] Test with screen reader - all content announced correctly
- [ ] Test with keyboard only - all functionality accessible
- [ ] Test color contrast - meets WCAG AA minimum
- [ ] Test with browser zoom - layout responsive at 200%
- [ ] Test RTL mode - layout mirrors correctly
- [ ] Test on mobile - touch interactions work
- [ ] Test with high contrast mode - visually distinct

## Complete Accessible AppBar Example

```tsx
import { AppBarComponent, MenuComponent, MenuItemModel } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  const navItems: MenuItemModel[] = [
    { text: 'Home' },
    { text: 'About' },
    { text: 'Services' },
    { text: 'Contact' }
  ];

  return (
    <>
      {/* Accessible AppBar */}
      <AppBarComponent 
        colorMode="Primary"
        role="banner"
        aria-label="Application header and main navigation"
      >
        {/* Menu button */}
        <ButtonComponent 
          cssClass="e-inherit"
          iconCss="e-icons e-menu"
          aria-label="Open navigation menu"
          title="Open navigation menu"
        ></ButtonComponent>
        
        {/* Brand/title */}
        <h1 className="app-title" aria-label="My Application">
          My Application
        </h1>
        
        {/* Navigation menu */}
        <nav aria-label="Main navigation">
          <MenuComponent 
            cssClass="e-inherit"
            items={navItems}
          ></MenuComponent>
        </nav>
        
        {/* Spacer for layout */}
        <div className="e-appbar-spacer"></div>
        
        {/* User controls */}
        <div role="group" aria-label="User controls">
          <ButtonComponent 
            cssClass="e-inherit"
            aria-label="User settings"
          >
            Settings
          </ButtonComponent>
          <ButtonComponent 
            cssClass="e-inherit"
            aria-label="Logout"
          >
            Logout
          </ButtonComponent>
        </div>
      </AppBarComponent>
      
      {/* Page content */}
      <main className="app-content">
        <h2>Welcome</h2>
        <p>Your application content goes here.</p>
      </main>
    </>
  );
}

export default App;
```

**App.css:**
```css
.app-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.app-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Focus indicators for keyboard navigation */
.e-appbar button:focus,
.e-appbar a:focus {
  outline: 2px solid #fff;
  outline-offset: 2px;
}
```

This example demonstrates best practices for accessible AppBar implementation.
