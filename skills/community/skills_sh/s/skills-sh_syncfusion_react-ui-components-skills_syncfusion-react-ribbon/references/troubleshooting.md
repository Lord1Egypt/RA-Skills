# Troubleshooting Guide

## Table of Contents
- [Common Issues](#common-issues)
- [Styling Issues](#styling-issues)
- [Performance Issues](#performance-issues)
- [Component Rendering](#component-rendering)
- [Event Handling](#event-handling)
- [Module Injection](#module-injection)
- [Responsive Issues](#responsive-issues)

## Common Issues

### Ribbon component not rendering

**Problem:** Ribbon appears blank or invisible

**Solutions:**

1. **Verify HTML container:**
```tsx
// In your HTML/index.html
<div id="root"></div>

// In your React component
<div id="element">
  <RibbonComponent id="ribbon">
    {/* Tabs */}
  </RibbonComponent>
</div>
```

2. **Check imports:**
```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective } from "@syncfusion/ej2-react-ribbon";
```

3. **Verify CSS imports:**
```css
@import "../node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css";
```

### Tabs or groups not appearing

**Problem:** Ribbon renders but tabs/groups are missing

**Solutions:**

```tsx
// Correct structure
<RibbonComponent id="ribbon">
  <RibbonTabsDirective>
    <RibbonTabDirective header="Home">
      <RibbonGroupsDirective>
        <RibbonGroupDirective header="Clipboard">
          {/* Items */}
        </RibbonGroupDirective>
      </RibbonGroupsDirective>
    </RibbonTabDirective>
  </RibbonTabsDirective>
</RibbonComponent>

// INCORRECT - Missing directives
<RibbonComponent id="ribbon">
  <RibbonTabDirective header="Home">  // ERROR: No RibbonTabsDirective!
  </RibbonTabDirective>
</RibbonComponent>
```

## Styling Issues

### Theme not applied

**Problem:** Styles don't match expected theme

**Solutions:**

1. **Import all required CSS files:**
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

2. **Clear browser cache:**
```bash
# Hard refresh in browser: Ctrl+Shift+Delete or Cmd+Shift+Delete
# Or clear node_modules and reinstall:
rm -rf node_modules
npm install
```

3. **Check theme file path:**
```
✓ Correct: ../node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css
✗ Wrong: ./node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css
```

### Custom styles not working

**Problem:** Custom CSS overrides not applied

**Solutions:**

1. **Import custom CSS AFTER Syncfusion CSS:**
```css
/* App.css */
@import "../node_modules/@syncfusion/ej2-ribbon/styles/tailwind3.css";

/* Custom styles - imported AFTER */
.e-ribbon {
  background-color: #f5f5f5;
}
```

2. **Use !important for high specificity:**
```css
.custom-ribbon .e-ribbon {
  background-color: #f5f5f5 !important;
}
```

3. **Check CSS selector specificity:**
```tsx
// Add class to ribbon for custom styling
<RibbonComponent id="ribbon" className="custom-ribbon">
  {/* Content */}
</RibbonComponent>
```

### Icons not displaying

**Problem:** Icons show as blank or broken

**Solutions:**

1. **Verify icon class:**
```tsx
// Correct icon format
buttonSettings={{ iconCss: "e-icons e-cut" }}

// INCORRECT
buttonSettings={{ iconCss: "e-cut" }}  // Missing "e-icons" prefix
```

2. **Import icon fonts:**
```css
/* Already included in Syncfusion CSS imports */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
/* This includes icon fonts */
```

3. **Check icon availability:**
```
Common icons: e-cut, e-copy, e-paste, e-bold, e-italic, e-underline, e-table, e-image
See Syncfusion icon documentation: https://ej2.syncfusion.com/react/documentation/icon/
```

## Performance Issues

### Ribbon renders slowly

**Problem:** Initial load or interaction is sluggish

**Solutions:**

1. **Lazy-load components:**
```tsx
const RibbonComponent = lazy(() => import('@syncfusion/ej2-react-ribbon'));

<Suspense fallback={<div>Loading ribbon...</div>}>
  <RibbonComponent id="ribbon">
    {/* Tabs */}
  </RibbonComponent>
</Suspense>
```

2. **Minimize initial items:**
```tsx
// Load contextual tabs only when needed
<RibbonContextualTabDirective visible={false}>
  {/* Tabs appear only when triggered */}
</RibbonContextualTabDirective>
```

3. **Use React.memo for tabs:**
```tsx
const HomeTab = React.memo(({ data }) => (
  <RibbonTabDirective header="Home">
    {/* Content */}
  </RibbonTabDirective>
));
```

### Memory leaks in long-running applications

**Problem:** Memory usage increases over time

**Solutions:**

1. **Cleanup event listeners:**
```tsx
useEffect(() => {
  const handleResize = () => {
    // Handle resize
  };

  window.addEventListener('resize', handleResize);
  
  return () => {
    window.removeEventListener('resize', handleResize);
  };
}, []);
```

2. **Properly dispose Ribbon:**
```tsx
useEffect(() => {
  return () => {
    if (ribbonRef.current) {
      ribbonRef.current.destroy();
    }
  };
}, []);
```

## Component Rendering

### Items not clickable

**Problem:** Button clicks don't trigger events

**Solutions:**

1. **Add click handler:**
```tsx
<RibbonItemDirective 
  type="Button"
  buttonSettings={{ 
    iconCss: "e-icons e-cut", 
    content: "Cut" 
  }}
  onClick={() => console.log('Cut clicked')}>
</RibbonItemDirective>
```

2. **Use itemClick event on ribbon:**
```tsx
<RibbonComponent 
  id="ribbon"
  itemClick={(args) => {
    console.log('Item clicked:', args.item);
  }}>
  {/* Content */}
</RibbonComponent>
```

### Disabled items still clickable

**Problem:** Setting `disabled={true}` doesn't prevent clicks

**Solutions:**

```tsx
// Correct: Set disabled directly on item
<RibbonItemDirective 
  type="Button"
  disabled={true}
  buttonSettings={{ content: "Cut" }}>
</RibbonItemDirective>

// INCORRECT: Set on settings object
<RibbonItemDirective 
  type="Button"
  buttonSettings={{ content: "Cut", disabled: true }}>  // This won't work
</RibbonItemDirective>
```

## Event Handling

### Event not firing

**Problem:** Click or tab selection events don't trigger

**Solutions:**

1. **Verify event name:**
```tsx
// Correct event names
<RibbonComponent 
  id="ribbon"
  itemClick={handleItemClick}      // Correct
  tabSelected={handleTabSelected}  // Correct
  onClick={handleClick}             // Wrong - doesn't work on Ribbon
>
```

2. **Check event handler binding:**
```tsx
const [activeTab, setActiveTab] = useState(0);

const handleTabSelected = (args) => {
  setActiveTab(args.tabIndex);
  console.log('Tab selected:', args.tabIndex);
};

<RibbonComponent id="ribbon" tabSelected={handleTabSelected}>
```

## Module Injection

### ColorPicker not working

**Problem:** ColorPicker items don't render

**Solutions:**

```tsx
import { RibbonComponent, RibbonColorPicker, Inject } from "@syncfusion/ej2-react-ribbon";

// Don't forget Inject!
<RibbonComponent id="ribbon">
  {/* Items */}
  <Inject services={[RibbonColorPicker]} />
</RibbonComponent>
```

### FileMenu not showing

**Problem:** File menu doesn't appear even with visible={true}

**Solutions:**

```tsx
import { RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";

<RibbonComponent id="ribbon" fileMenu={{ visible: true, menuItems: [] }}>
  {/* Content */}
  <Inject services={[RibbonFileMenu]} />
</RibbonComponent>
```

### Contextual tabs not appearing

**Problem:** RibbonContextualTab imports work but tabs don't show

**Solutions:**

```tsx
import { RibbonContextualTab, Inject } from "@syncfusion/ej2-react-ribbon";

<RibbonComponent id="ribbon">
  <RibbonContextualTabsDirective>
    {/* Tabs */}
  </RibbonContextualTabsDirective>
  <Inject services={[RibbonContextualTab]} />
</RibbonComponent>
```

## Responsive Issues

### Items overflow incorrectly

**Problem:** Items don't collapse properly when resizing

**Solutions:**

1. **Set group collapsibility:**
```tsx
// Allow group to collapse
<RibbonGroupDirective header="Clipboard" isCollapsible={true}>

// Prevent collapse (stay visible)
<RibbonGroupDirective header="Font" isCollapsible={false}>
```

2. **Set item sizes:**
```tsx
import { RibbonItemSize } from "@syncfusion/ej2-react-ribbon";

<RibbonItemDirective 
  type="Button"
  allowedSizes={RibbonItemSize.Large}
  buttonSettings={{ content: "Button" }}>
</RibbonItemDirective>
```

### Layout switcher missing

**Problem:** Users can't switch between Classic and Simplified layouts

**Solutions:**

```tsx
// Enable layout switcher
<RibbonComponent id="ribbon" hideLayoutSwitcher={false}>
  {/* Content */}
</RibbonComponent>

// If explicitly hidden, make sure property is false
// NOT: hideLayoutSwitcher={true}
```

## Debug Tips

### Enable console logging

```tsx
function App() {
  const ribbonRef = useRef<RibbonComponent>(null);

  useEffect(() => {
    if (ribbonRef.current) {
      console.log('Ribbon instance:', ribbonRef.current);
      console.log('Ribbon properties:', {
        activeLayout: ribbonRef.current.activeLayout,
        isMinimized: ribbonRef.current.isMinimized,
      });
    }
  }, []);

  return (
    <RibbonComponent id="ribbon" ref={ribbonRef}>
      {/* Content */}
    </RibbonComponent>
  );
}
```

### Check TypeScript errors

```tsx
// TypeScript will catch many issues at compile time
// Use strict mode for better error detection
```

## Getting Help

1. **Check official documentation:** https://ej2.syncfusion.com/react/documentation/ribbon/
2. **Syncfusion support:** https://www.syncfusion.com/support/
3. **Stack Overflow:** Tag questions with `syncfusion` and `ej2-ribbon`
4. **GitHub issues:** https://github.com/syncfusion/ej2-react-ui-components/issues

## Best Practices to Avoid Issues

1. **Always import required modules**
2. **Use TypeScript for type safety**
3. **Test on multiple browsers**
4. **Verify CSS imports completeness**
5. **Use React DevTools for debugging**
6. **Check browser console for errors**
7. **Keep Syncfusion packages updated**
8. **Test responsive behavior**

See other reference guides for feature-specific troubleshooting.
