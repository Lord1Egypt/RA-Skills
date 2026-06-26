# Customization and Theming

## Table of Contents
- [Built-in Themes](#built-in-themes)
- [Applying Themes](#applying-themes)
- [Theme Switching](#theme-switching)
- [CSS Customization](#css-customization)
- [Dark Mode](#dark-mode)
- [Custom Icons](#custom-icons)

## Built-in Themes

Syncfusion provides multiple professional themes:

| Theme | CSS File | Description |
|-------|----------|-------------|
| Material | material.css | Material Design theme |
| Bootstrap | bootstrap.css | Bootstrap classic theme |
| Bootstrap 4 | bootstrap4.css | Bootstrap 4 theme |
| Fluent | fluent.css | Microsoft Fluent Design |
| Tailwind | tailwind3.css | Tailwind CSS theme |

## Applying Themes

Import theme CSS in your application:

```css
/* App.css */

/* Material Theme */
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/material.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-ribbon/styles/material.css";
```

Or use Tailwind theme:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css";
```

## Theme Switching

Switch themes dynamically:

```tsx
import { useRef, useState } from 'react';
import { RibbonComponent } from "@syncfusion/ej2-react-ribbon";
import "./App.css";

function App() {
  const [theme, setTheme] = useState('material');
  const ribbonRef = useRef<RibbonComponent>(null);

  const switchTheme = (newTheme: string) => {
    setTheme(newTheme);
    
    // Update stylesheets
    const baseLink = document.querySelector('[data-theme-base]');
    const ribbonLink = document.querySelector('[data-theme-ribbon]');
    
    if (baseLink && ribbonLink) {
      baseLink.setAttribute('href', `/styles/${newTheme}/ej2-base.css`);
      ribbonLink.setAttribute('href', `/styles/${newTheme}/ej2-ribbon.css`);
    }
  };

  return (
    <div>
      <div style={{ padding: '10px', marginBottom: '10px' }}>
        <button onClick={() => switchTheme('material')}>Material</button>
        <button onClick={() => switchTheme('bootstrap')}>Bootstrap</button>
        <button onClick={() => switchTheme('fluent')}>Fluent</button>
        <button onClick={() => switchTheme('tailwind3')}>Tailwind</button>
      </div>
      
      <RibbonComponent id="ribbon" ref={ribbonRef}>
        {/* Ribbon content */}
      </RibbonComponent>
    </div>
  );
}

export default App;
```

## CSS Customization

Override theme styles with custom CSS:

```css
/* Custom Ribbon Styles */

/* Override ribbon background */
.e-ribbon {
  background-color: #f5f5f5;
  border-bottom: 2px solid #007bff;
}

/* Override tab header styles */
.e-ribbon .e-tab-header {
  background-color: #ffffff;
  color: #333333;
}

/* Override active tab styles */
.e-ribbon .e-tab-header .e-active {
  background-color: #007bff;
  color: #ffffff;
}

/* Override group header */
.e-ribbon-group-header {
  font-weight: bold;
  color: #555555;
  border-bottom: 1px solid #dddddd;
}

/* Override item buttons */
.e-ribbon .e-btn {
  padding: 8px 12px;
  border-radius: 4px;
}

/* Override item icons */
.e-ribbon .e-icon {
  font-size: 18px;
}
```

## Dark Mode

Implement dark mode support:

```tsx
import { useEffect, useState } from 'react';
import { RibbonComponent } from "@syncfusion/ej2-react-ribbon";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const root = document.documentElement;
    if (isDarkMode) {
      root.classList.add('dark-mode');
    } else {
      root.classList.remove('dark-mode');
    }
  }, [isDarkMode]);

  return (
    <div>
      <button onClick={() => setIsDarkMode(!isDarkMode)}>
        {isDarkMode ? 'Light Mode' : 'Dark Mode'}
      </button>
      
      <RibbonComponent id="ribbon">
        {/* Ribbon content */}
      </RibbonComponent>
    </div>
  );
}

export default App;
```

**Dark Mode CSS:**

```css
/* Dark Mode Styles */
:root.dark-mode {
  --ribbon-bg: #2d2d2d;
  --ribbon-text: #f0f0f0;
  --ribbon-border: #444444;
  --ribbon-hover: #3d3d3d;
}

:root.dark-mode .e-ribbon {
  background-color: var(--ribbon-bg);
  color: var(--ribbon-text);
  border-color: var(--ribbon-border);
}

:root.dark-mode .e-ribbon-tab {
  background-color: var(--ribbon-bg);
  color: var(--ribbon-text);
}

:root.dark-mode .e-ribbon-tab:hover {
  background-color: var(--ribbon-hover);
}

:root.dark-mode .e-ribbon-group-header {
  background-color: var(--ribbon-bg);
  color: var(--ribbon-text);
  border-color: var(--ribbon-border);
}

:root.dark-mode .e-btn {
  background-color: var(--ribbon-bg);
  color: var(--ribbon-text);
  border-color: var(--ribbon-border);
}

:root.dark-mode .e-btn:hover {
  background-color: var(--ribbon-hover);
}
```

## Custom Icons

Use custom icon fonts or SVG icons:

```tsx
// Using custom icon class
<RibbonItemDirective 
  type="Button" 
  buttonSettings={{ 
    iconCss: "custom-icon-copy",  // Custom CSS class
    content: "Copy" 
  }}>
</RibbonItemDirective>

// Using SVG icons
<RibbonItemDirective 
  type="Button" 
  buttonSettings={{ 
    iconCss: "e-icons e-custom-svg",
    content: "Custom Action" 
  }}>
</RibbonItemDirective>
```

**Custom Icon Styles:**

```css
/* Custom Icon Font */
@font-face {
  font-family: 'CustomIcons';
  src: url('/fonts/custom-icons.woff') format('woff');
}

.custom-icon-copy::before {
  font-family: 'CustomIcons';
  content: '\e101';  /* Character code for copy icon */
  font-size: 16px;
}

/* SVG Icons */
.e-custom-svg::before {
  content: url('/icons/custom.svg');
  width: 16px;
  height: 16px;
  display: inline-block;
}
```

## Complete Theme Example

```tsx
import { useRef, useState } from 'react';
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import "./App.css";

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [theme, setTheme] = useState('material');
  const ribbonRef = useRef<RibbonComponent>(null);

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    const root = document.documentElement;
    if (!isDarkMode) {
      root.classList.add('dark-mode');
    } else {
      root.classList.remove('dark-mode');
    }
  };

  const switchTheme = (newTheme: string) => {
    setTheme(newTheme);
    // Update theme stylesheets
    const links = document.querySelectorAll('[data-theme]');
    links.forEach(link => {
      link.setAttribute('href', `/styles/${newTheme}/${link.dataset.theme}.css`);
    });
  };

  return (
    <div>
      <div style={{ padding: '15px', marginBottom: '15px', borderBottom: '1px solid #ddd' }}>
        <div style={{ marginBottom: '10px' }}>
          <strong>Theme:</strong>
          <button onClick={() => switchTheme('material')} style={{ marginLeft: '10px' }}>Material</button>
          <button onClick={() => switchTheme('bootstrap')} style={{ marginLeft: '5px' }}>Bootstrap</button>
          <button onClick={() => switchTheme('fluent')} style={{ marginLeft: '5px' }}>Fluent</button>
        </div>
        
        <div>
          <strong>Mode:</strong>
          <button onClick={toggleDarkMode} style={{ marginLeft: '10px' }}>
            {isDarkMode ? 'Switch to Light' : 'Switch to Dark'}
          </button>
        </div>
      </div>

      <RibbonComponent id="ribbon" ref={ribbonRef}>
        <RibbonTabsDirective>
          <RibbonTabDirective header="Home">
            <RibbonGroupsDirective>
              <RibbonGroupDirective header="Clipboard">
                <RibbonCollectionsDirective>
                  <RibbonCollectionDirective>
                    <RibbonItemsDirective>
                      <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                      </RibbonItemDirective>
                      <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
                      </RibbonItemDirective>
                      <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-paste", content: "Paste" }}>
                      </RibbonItemDirective>
                    </RibbonItemsDirective>
                  </RibbonCollectionDirective>
                </RibbonCollectionsDirective>
              </RibbonGroupDirective>
            </RibbonGroupsDirective>
          </RibbonTabDirective>
        </RibbonTabsDirective>
      </RibbonComponent>
    </div>
  );
}

export default App;
```

## Best Practices

1. **Consistency:** Use one theme throughout application
2. **Accessibility:** Ensure dark mode has sufficient contrast
3. **Performance:** Load only required theme files
4. **Custom Icons:** Use icon fonts for scalability
5. **Testing:** Test all themes with various browsers
6. **Documentation:** Document custom CSS overrides
