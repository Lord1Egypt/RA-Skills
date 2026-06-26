# API Reference

## Table of Contents
- [Overview](#overview)
- [Properties](#properties)
- [Events](#events)
- [Common Property Combinations](#common-property-combinations)

## Overview

The AppBarComponent provides a comprehensive set of properties and events to customize and control the behavior of your navigation bar. This reference covers all available APIs with detailed explanations and practical examples.

---

## Properties

### colorMode

**Type:** `AppBarColor` (enum)  
**Default:** `"Light"`  
**Possible Values:** `"Light"` | `"Dark"` | `"Primary"` | `"Inherit"`

Specifies the color mode that defines the background and text colors of the AppBar component.

| Value | Description | Use Case |
|-------|-------------|----------|
| **Light** | Light background with dark text | Default, minimal designs, accessibility |
| **Dark** | Dark background with light text | Modern, night mode, high contrast |
| **Primary** | Primary brand color background | Main navigation, emphasis, branding |
| **Inherit** | Inherits from parent element | Custom theming, context-aware styling |

**Example 1: Light Color Mode**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Light">
      <ButtonComponent cssClass="e-inherit">Home</ButtonComponent>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent isPrimary>Login</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Dark Color Mode**
```tsx
<AppBarComponent colorMode="Dark">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Dark Navigation</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">Settings</ButtonComponent>
</AppBarComponent>
```

**Example 3: Primary Color Mode**
```tsx
<AppBarComponent colorMode="Primary">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>My Application</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">Logout</ButtonComponent>
</AppBarComponent>
```

**Example 4: Inherit Color Mode**
```tsx
import React from "react";

const App = () => {
  return (
    <div style={{ backgroundColor: '#ff6b6b', color: 'white' }}>
      <AppBarComponent colorMode="Inherit">
        <span>Custom Colored AppBar</span>
      </AppBarComponent>
    </div>
  );
}

export default App;
```

---

### mode

**Type:** `AppBarMode` (enum)  
**Default:** `"Regular"`  
**Possible Values:** `"Regular"` | `"Prominent"` | `"Dense"`

Specifies the height mode of the AppBar component. The mode controls the vertical space available for content.

| Mode | Height | Use Case |
|------|--------|----------|
| **Regular** | Default (~56px) | Standard navigation bars, most applications |
| **Prominent** | Large (~128px) | Large titles, branding, hero sections |
| **Dense** | Compact (~48px) | Toolbars, tight spaces, mobile layouts |

**Example 1: Regular Mode (Default)**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent colorMode="Primary" mode="Regular">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span className="regular">Regular AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Prominent Mode**
```tsx
<AppBarComponent colorMode="Primary" mode="Prominent" cssClass="prominent-appbar">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span className="prominent">AppBar with Prominent Mode</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
</AppBarComponent>
```

**CSS for Prominent Mode:**
```css
.prominent-appbar.e-prominent {
  height: 200px;  /* Custom height adjustment */
}

.prominent {
  align-self: center;
  font-size: 24px;
  font-weight: bold;
}
```

**Example 3: Dense Mode**
```tsx
<AppBarComponent colorMode="Primary" mode="Dense">
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-cut"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-copy"></ButtonComponent>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-paste"></ButtonComponent>
  <div className="e-appbar-separator"></div>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-bold"></ButtonComponent>
</AppBarComponent>
```

---

### position

**Type:** `AppBarPosition` (enum)  
**Default:** `"Top"`  
**Possible Values:** `"Top"` | `"Bottom"`

Specifies the vertical position of the AppBar within the viewport.

| Position | Description | Use Case |
|----------|-------------|----------|
| **Top** | AppBar positioned at top of content | Main navigation, headers |
| **Bottom** | AppBar positioned at bottom of content | Mobile action bars, footer navigation |

**Example 1: Top Position (Default)**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <AppBarComponent colorMode="Primary" position="Top">
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>My App</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">FREE TRIAL</ButtonComponent>
      </AppBarComponent>
      
      <div style={{ padding: '20px' }}>
        <h2>Main Content</h2>
        <p>Your content goes here.</p>
      </div>
    </>
  );
}

export default App;
```

**Example 2: Bottom Position**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <div style={{ padding: '20px', minHeight: '400px' }}>
        <h2>Document Content</h2>
        <p>Your document or form content goes here.</p>
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

---

### isSticky

**Type:** `boolean`  
**Default:** `false`

Defines whether the AppBar position is fixed to the viewport while scrolling page content. When set to `true`, the AppBar will remain visible at its position (top or bottom) while the user scrolls.

**Use Cases:**
- Keep main navigation always accessible while scrolling long pages
- Fixed toolbars that users need constant access to
- Sticky headers in dashboards and admin panels

**Example 1: Sticky Top AppBar**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <>
      <AppBarComponent colorMode="Primary" isSticky>
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>Sticky Navigation</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">Profile</ButtonComponent>
      </AppBarComponent>
      
      <div className="appbar-content" style={{ padding: '20px' }}>
        <h2>Scroll Down to See Sticky AppBar</h2>
        {Array.from({ length: 30 }).map((_, i) => (
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

**Example 2: Sticky Bottom AppBar (Mobile Action Bar)**
```tsx
<>
  <div style={{ padding: '20px', minHeight: '600px' }}>
    <h2>Form Content</h2>
    <p>Fill out the form above...</p>
  </div>
  
  <AppBarComponent 
    colorMode="Primary" 
    position="Bottom" 
    isSticky
  >
    <ButtonComponent cssClass="e-inherit">Clear</ButtonComponent>
    <div className="e-appbar-spacer"></div>
    <ButtonComponent cssClass="e-inherit" isPrimary>Submit</ButtonComponent>
  </AppBarComponent>
</>
```

---

### cssClass

**Type:** `string`  
**Default:** `undefined`

Accepts single or multiple CSS classes (separated by spaces) to be applied to the AppBar container for custom styling and theming.

**Use Cases:**
- Apply custom CSS rules for AppBar styling
- Create theme variants
- Add specific styling for different sections
- Combine with media queries for responsive design

**Example 1: Single Custom Class**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";
import './App.css';

const App = () => {
  return (
    <AppBarComponent colorMode="Primary" cssClass="custom-appbar">
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-home"></ButtonComponent>
      <span>Custom Styled AppBar</span>
    </AppBarComponent>
  );
}

export default App;
```

**CSS Styling:**
```css
.custom-appbar {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-bottom: 3px solid #ff6b6b;
  padding: 12px 24px;
}

.custom-appbar .e-inherit {
  font-weight: 500;
  letter-spacing: 0.5px;
}
```

**Example 2: Multiple Classes**
```tsx
<AppBarComponent 
  colorMode="Primary" 
  mode="Prominent"
  cssClass="elevated-shadow gradient-bg rounded-corners"
>
  <span>Multi-Class AppBar</span>
</AppBarComponent>
```

**CSS Styling:**
```css
.elevated-shadow {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.rounded-corners {
  border-radius: 8px;
}
```

---

### htmlAttributes

**Type:** `Record<string, any>`  
**Default:** `{}`

Accepts HTML attributes and custom attributes (as a Record/object) to be applied directly to the AppBar DOM element. Useful for accessibility attributes, data attributes, and other custom properties.

**Use Cases:**
- Add ARIA labels for screen readers
- Set data attributes for testing
- Add custom attributes for analytics
- Implement accessibility features

**Example 1: ARIA Labels for Accessibility**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary"
      htmlAttributes={{
        'role': 'banner',
        'aria-label': 'Main application navigation bar',
        'aria-description': 'Navigation bar containing main menu and user options'
      }}
    >
      <ButtonComponent 
        cssClass="e-inherit" 
        iconCss="e-icons e-menu"
        aria-label="Toggle navigation menu"
      ></ButtonComponent>
      
      <span>Application</span>
      
      <div className="e-appbar-spacer"></div>
      
      <ButtonComponent 
        cssClass="e-inherit"
        aria-label="User profile menu"
        aria-haspopup="menu"
      >
        Profile
      </ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Data Attributes for Testing**
```tsx
<AppBarComponent 
  colorMode="Primary"
  htmlAttributes={{
    'data-testid': 'main-appbar',
    'data-component': 'appbar',
    'data-version': '1.0',
    'data-analytics': 'navigation-bar'
  }}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Test AppBar</span>
</AppBarComponent>
```

**Example 3: Mixed Attributes**
```tsx
<AppBarComponent 
  colorMode="Primary"
  htmlAttributes={{
    'role': 'navigation',
    'aria-label': 'Main navigation',
    'data-testid': 'nav-appbar',
    'id': 'app-navigation',
    'title': 'Application Navigation Bar'
  }}
>
  {/* Content */}
</AppBarComponent>
```

---

### enableRtl

**Type:** `boolean`  
**Default:** `false`

Enable or disable rendering the AppBar component in right-to-left direction. Essential for supporting RTL languages like Arabic, Hebrew, and Persian.

**Use Cases:**
- Support for Arabic (ar), Hebrew (he), Persian (fa) languages
- Bidirectional text support
- Regional application localization

**Example 1: RTL Support with Arabic**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const isArabic = true;  // Set based on language selection
  
  return (
    <div dir={isArabic ? "rtl" : "ltr"}>
      <AppBarComponent 
        colorMode="Primary"
        enableRtl={isArabic}
      >
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>{isArabic ? 'التطبيق' : 'Application'}</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">
          {isArabic ? 'تسجيل الدخول' : 'Login'}
        </ButtonComponent>
      </AppBarComponent>
    </div>
  );
}

export default App;
```

**Example 2: Dynamic RTL Toggle**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React, { useState } from "react";

const App = () => {
  const [isRTL, setIsRTL] = useState(false);
  
  const toggleRTL = () => {
    setIsRTL(!isRTL);
  };
  
  return (
    <div dir={isRTL ? "rtl" : "ltr"}>
      <AppBarComponent 
        colorMode="Primary"
        enableRtl={isRTL}
      >
        <ButtonComponent 
          cssClass="e-inherit" 
          onClick={toggleRTL}
        >
          {isRTL ? 'LTR' : 'RTL'}
        </ButtonComponent>
        <span>{isRTL ? 'اتجاه النص' : 'Text Direction'}</span>
      </AppBarComponent>
    </div>
  );
}

export default App;
```

---

### enablePersistence

**Type:** `boolean`  
**Default:** `false`

Enable or disable persisting the AppBar component's state between page reloads. When enabled, the component state is saved to browser storage (localStorage) and restored on subsequent page loads.

**Use Cases:**
- Maintain AppBar state across page refreshes
- Preserve user preferences for AppBar configuration
- Store layout preferences persistently

**Example 1: Enable Persistence**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React, { useState } from "react";

const App = () => {
  const [colorMode, setColorMode] = useState<string>("Primary");
  
  const toggleColorMode = () => {
    const newMode = colorMode === "Primary" ? "Dark" : "Primary";
    setColorMode(newMode);
  };
  
  return (
    <AppBarComponent 
      colorMode={colorMode as any}
      enablePersistence={true}
    >
      <ButtonComponent 
        cssClass="e-inherit" 
        onClick={toggleColorMode}
      >
        Toggle Theme
      </ButtonComponent>
      <span>State will persist after reload</span>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: With User Preferences**
```tsx
<AppBarComponent 
  colorMode="Primary"
  mode="Regular"
  enablePersistence={true}
  htmlAttributes={{
    'data-persist-key': 'appbar-state'
  }}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Persistent AppBar Configuration</span>
</AppBarComponent>
```

---

### locale

**Type:** `string`  
**Default:** `"en-US"`

Overrides the global culture and localization value for the AppBar component. Allows you to set language-specific formatting and content for this component instance without affecting other components.

**Supported Locales:**
- `"en-US"` - English (United States)
- `"de-DE"` - German (Germany)
- `"fr-FR"` - French (France)
- `"es-ES"` - Spanish (Spain)
- `"ar-AR"` - Arabic
- `"ja-JP"` - Japanese
- `"zh-CN"` - Chinese (Simplified)
- And many more language-region combinations

**Example 1: German Locale**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary"
      locale="de-DE"
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span>Deutsch AppBar</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">Anmelden</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Arabic Locale with RTL**
```tsx
<AppBarComponent 
  colorMode="Primary"
  locale="ar-AR"
  enableRtl={true}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>تطبيقي</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">تسجيل الدخول</ButtonComponent>
</AppBarComponent>
```

**Example 3: Dynamic Locale Switching**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React, { useState } from "react";

const App = () => {
  const [locale, setLocale] = useState<string>("en-US");
  
  const locales = [
    { code: "en-US", label: "English" },
    { code: "de-DE", label: "Deutsch" },
    { code: "fr-FR", label: "Français" },
    { code: "es-ES", label: "Español" }
  ];
  
  return (
    <>
      <AppBarComponent 
        colorMode="Primary"
        locale={locale}
      >
        <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
        <span>Language Settings</span>
        <div className="e-appbar-spacer"></div>
        <ButtonComponent cssClass="e-inherit">Options</ButtonComponent>
      </AppBarComponent>
      
      <div style={{ padding: '20px' }}>
        <h3>Select Language:</h3>
        {locales.map(loc => (
          <ButtonComponent
            key={loc.code}
            onClick={() => setLocale(loc.code)}
            isPrimary={locale === loc.code}
            style={{ marginRight: '10px' }}
          >
            {loc.label}
          </ButtonComponent>
        ))}
      </div>
    </>
  );
}

export default App;
```

---

## Events

### created

**Type:** `EmitType<Event>`  
**Triggers:** After the AppBar component is created and initialized

The `created` event fires once the AppBar component has been fully created and all initialization is complete. Use this event to perform any setup operations after the component is ready.

**Event Arguments:**
- `args: Event` - Standard React/JavaScript Event object

**Example 1: Basic Created Event**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const handleCreated = (args: any) => {
    console.log('AppBar component has been created:', args);
    // Perform initialization tasks here
  };
  
  return (
    <AppBarComponent 
      colorMode="Primary"
      created={handleCreated}
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span>AppBar with Created Event</span>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Logging Component Metadata**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const handleCreated = (args: any) => {
    console.log('AppBar Created Event Details:');
    console.log('- Event Type:', args.type);
    console.log('- Timestamp:', new Date().toISOString());
    console.log('- Component initialized successfully');
    
    // You can initialize custom behavior here
    localStorage.setItem('appbar-created-at', new Date().toISOString());
  };
  
  return (
    <AppBarComponent 
      colorMode="Primary"
      created={handleCreated}
    >
      <ButtonComponent cssClass="e-inherit">Navigation</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 3: Setup Analytics on Component Creation**
```tsx
<AppBarComponent 
  colorMode="Primary"
  created={(args) => {
    // Track component initialization
    if (window.analytics) {
      window.analytics.trackEvent('appbar_initialized', {
        timestamp: new Date().toISOString(),
        colorMode: 'Primary',
        component: 'AppBar'
      });
    }
  }}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Tracked AppBar</span>
</AppBarComponent>
```

---

### destroyed

**Type:** `EmitType<Event>`  
**Triggers:** When the AppBar component is destroyed/unmounted

The `destroyed` event fires when the AppBar component is being removed from the DOM or destroyed. Use this event to perform cleanup operations, unsubscribe from events, or save state.

**Event Arguments:**
- `args: Event` - Standard React/JavaScript Event object

**Example 1: Basic Destroyed Event**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  const handleDestroyed = (args: any) => {
    console.log('AppBar component is being destroyed:', args);
    // Perform cleanup tasks here
  };
  
  return (
    <AppBarComponent 
      colorMode="Primary"
      destroyed={handleDestroyed}
    >
      <ButtonComponent cssClass="e-inherit">Navigation</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

**Example 2: Cleanup and Logging**
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React, { useState } from "react";

const App = () => {
  const [isAppBarVisible, setIsAppBarVisible] = useState(true);
  
  const handleDestroyed = (args: any) => {
    console.log('AppBar Destroyed Event:');
    console.log('- Component cleanup started');
    console.log('- Timestamp:', new Date().toISOString());
    
    // Remove from localStorage or perform cleanup
    localStorage.removeItem('appbar-state');
    
    console.log('- Cleanup completed');
  };
  
  return (
    <>
      {isAppBarVisible && (
        <AppBarComponent 
          colorMode="Primary"
          destroyed={handleDestroyed}
        >
          <ButtonComponent cssClass="e-inherit">Navigation</ButtonComponent>
        </AppBarComponent>
      )}
      
      <div style={{ padding: '20px' }}>
        <ButtonComponent 
          onClick={() => setIsAppBarVisible(!isAppBarVisible)}
          isPrimary
        >
          {isAppBarVisible ? 'Hide' : 'Show'} AppBar
        </ButtonComponent>
      </div>
    </>
  );
}

export default App;
```

**Example 3: Save State on Destroy**
```tsx
<AppBarComponent 
  colorMode="Primary"
  destroyed={(args) => {
    // Save component state before destruction
    const appbarState = {
      colorMode: 'Primary',
      lastActive: new Date().toISOString(),
      sessionDuration: calculateSessionDuration()
    };
    
    // Send to server or save locally
    localStorage.setItem('last-appbar-state', JSON.stringify(appbarState));
    
    console.log('AppBar state saved before destruction');
  }}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>AppBar with State Management</span>
</AppBarComponent>
```

---

## Common Property Combinations

### Combination 1: Professional Enterprise Navigation
```tsx
import { AppBarComponent } from "@syncfusion/ej2-react-navigations";
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import React from "react";

const App = () => {
  return (
    <AppBarComponent 
      colorMode="Primary"
      mode="Regular"
      position="Top"
      isSticky={true}
      cssClass="enterprise-appbar"
      htmlAttributes={{
        'role': 'navigation',
        'aria-label': 'Main application navigation',
        'data-component': 'enterprise-navbar'
      }}
      enablePersistence={true}
      enableRtl={false}
      locale="en-US"
      created={(args) => console.log('Enterprise AppBar ready')}
    >
      <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
      <span>Enterprise Application</span>
      <div className="e-appbar-spacer"></div>
      <ButtonComponent cssClass="e-inherit">Profile</ButtonComponent>
    </AppBarComponent>
  );
}

export default App;
```

### Combination 2: Mobile-First Design
```tsx
<AppBarComponent 
  colorMode="Dark"
  mode="Dense"
  position="Top"
  isSticky={true}
  cssClass="mobile-appbar"
  htmlAttributes={{
    'data-device': 'mobile'
  }}
  enableRtl={false}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>Mobile App</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-user"></ButtonComponent>
</AppBarComponent>
```

### Combination 3: Multilingual RTL Support
```tsx
<AppBarComponent 
  colorMode="Primary"
  mode="Regular"
  position="Top"
  enableRtl={true}
  locale="ar-AR"
  htmlAttributes={{
    'dir': 'rtl',
    'aria-label': 'شريط التنقل الرئيسي'
  }}
>
  <ButtonComponent cssClass="e-inherit" iconCss="e-icons e-menu"></ButtonComponent>
  <span>تطبيق متعدد اللغات</span>
  <div className="e-appbar-spacer"></div>
  <ButtonComponent cssClass="e-inherit">الإعدادات</ButtonComponent>
</AppBarComponent>
```

### Combination 4: Custom Themed Prominent Header
```tsx
<AppBarComponent 
  colorMode="Inherit"
  mode="Prominent"
  cssClass="custom-hero-appbar gradient-bg"
  htmlAttributes={{
    'data-section': 'hero',
    'data-testid': 'hero-appbar'
  }}
  created={(args) => console.log('Hero AppBar initialized')}
>
  <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
    <h1>Welcome to Our Platform</h1>
  </div>
</AppBarComponent>
```

**CSS for Custom Theme:**
```css
.custom-hero-appbar.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.custom-hero-appbar h1 {
  margin: 0;
  font-size: 2rem;
}
```

---

## Summary Table

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `colorMode` | AppBarColor | `"Light"` | Background and text color scheme |
| `mode` | AppBarMode | `"Regular"` | Height mode (Regular, Prominent, Dense) |
| `position` | AppBarPosition | `"Top"` | Vertical position (Top, Bottom) |
| `isSticky` | boolean | `false` | Fixed positioning while scrolling |
| `cssClass` | string | `undefined` | Custom CSS classes for styling |
| `htmlAttributes` | Record | `{}` | HTML attributes to apply to element |
| `enableRtl` | boolean | `false` | Right-to-left text direction |
| `enablePersistence` | boolean | `false` | Persist state between page reloads |
| `locale` | string | `"en-US"` | Language and culture settings |

| Event | Trigger | Use Case |
|-------|---------|----------|
| `created` | After component initialization | Setup, initialization tasks |
| `destroyed` | When component is removed | Cleanup, state saving |
