# Layouts and Display Modes

## Table of Contents
- [Layout Overview](#layout-overview)
- [Classic Layout](#classic-layout)
- [Simplified Layout](#simplified-layout)
- [Layout Switching](#layout-switching)
- [Display Options](#display-options)
- [Item Sizing in Layouts](#item-sizing-in-layouts)
- [Responsive Behavior](#responsive-behavior)
- [Minimized State](#minimized-state)
- [Hide Layout Switcher](#hide-layout-switcher)

## Layout Overview

The Ribbon supports two layouts:

| Layout | Description | Use Case |
|--------|-------------|----------|
| **Classic** | Traditional multi-row format with items stacked vertically | Desktop applications, large screens |
| **Simplified** | Single-row compact format | Tablet, responsive, space-constrained |

## Classic Layout

The default layout that organizes items and groups in traditional multi-row format:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonItemSize } from "@syncfusion/ej2-react-ribbon";
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

function App() {
  const pasteOptions: ItemModel[] = [
    { text: "Keep Source Format" },
    { text: "Merge format" },
    { text: "Keep text only" }
  ];

  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="SplitButton" allowedSizes={RibbonItemSize.Large}
                      splitButtonSettings={{ iconCss: "e-icons e-paste", items: pasteOptions, content: "Paste" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Explicit Selection:**

```tsx
<RibbonComponent id="ribbon">
  {/* Classic is default, but can be explicit */}
  {/* activeLayout property is optional for Classic */}
</RibbonComponent>
```

## Simplified Layout

Compact single-row layout for constrained spaces:

```tsx
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

function App() {
  const pasteOptions: ItemModel[] = [
    { text: "Keep Source Format" },
    { text: "Merge format" },
    { text: "Keep text only" }
  ];

  return (
    <RibbonComponent id="ribbon" activeLayout='Simplified'>
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="SplitButton"
                      splitButtonSettings={{ iconCss: "e-icons e-paste", items: pasteOptions, content: "Paste" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Simplified Layout Characteristics:**
- Single row of items
- GroupButton items render as dropdowns
- More compact display
- Ideal for mobile and responsive designs

## Layout Switching

Users can switch layouts via the layout switcher button in the ribbon header.

**Enable/Disable Layout Switcher:**

```tsx
// Hide layout switcher (users cannot switch)
<RibbonComponent id="ribbon" hideLayoutSwitcher={true}>
  {/* Tabs and groups */}
</RibbonComponent>

// Show layout switcher (default)
<RibbonComponent id="ribbon" hideLayoutSwitcher={false}>
  {/* Tabs and groups */}
</RibbonComponent>
```

## Display Options

Control which layouts each item appears in:

```tsx
import { DisplayMode } from "@syncfusion/ej2-react-ribbon";

// Display only in Classic layout
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Classic}
  buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
</RibbonItemDirective>

// Display only in Simplified layout
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Simplified}
  buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
</RibbonItemDirective>

// Display only in overflow popup
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Overflow}
  buttonSettings={{ iconCss: "e-icons e-paste", content: "Paste" }}>
</RibbonItemDirective>

// Display in all layouts (default)
<RibbonItemDirective type="Button" 
  displayOptions={DisplayMode.Auto}
  buttonSettings={{ iconCss: "e-icons e-bold", content: "Bold" }}>
</RibbonItemDirective>
```

**Display Mode Options:**
- `DisplayMode.Auto` - Appear in all layouts
- `DisplayMode.Classic` - Classic layout only
- `DisplayMode.Simplified` - Simplified layout only
- `DisplayMode.Overflow` - Overflow popup only

## Item Sizing in Layouts

Item sizes adjust automatically based on available space:

```tsx
import { RibbonItemSize } from "@syncfusion/ej2-react-ribbon";

// Large size (large icon + text)
<RibbonItemDirective type="SplitButton" 
  allowedSizes={RibbonItemSize.Large}
  splitButtonSettings={{ content: "Paste" }}>
</RibbonItemDirective>

// Medium size (small icon + text)
<RibbonItemDirective type="Button" 
  allowedSizes={RibbonItemSize.Medium}
  buttonSettings={{ content: "Copy" }}>
</RibbonItemDirective>

// Small size (icon only)
<RibbonItemDirective type="Button" 
  allowedSizes={RibbonItemSize.Small}
  buttonSettings={{ content: "Cut" }}>
</RibbonItemDirective>
```

**Automatic Size Transition:**

During ribbon resizing:
1. Items start at their maximum allowed size (Large)
2. As space decreases: Large → Medium → Small
3. Items that don't fit move to overflow

## Responsive Behavior

Handle responsive ribbon resizing with group configuration:

```tsx
// Non-collapsible groups stay visible
<RibbonGroupDirective header="Font" isCollapsible={false}>
  {/* Always visible */}
</RibbonGroupDirective>

// Collapsible groups collapse when space is limited
<RibbonGroupDirective header="Clipboard" isCollapsible={true} priority={1}>
  {/* Collapses when needed */}
</RibbonGroupDirective>

// Set priority for collapse order
<RibbonGroupDirective header="Editor" priority={2}>
  {/* Collapses first */}
</RibbonGroupDirective>
```

## Minimized State

Collapse the ribbon to show only tab headers, saving vertical space:

```tsx
// Default (minimized=false)
<RibbonComponent id="ribbon">
  {/* Ribbon expanded */}
</RibbonComponent>

// Start minimized
<RibbonComponent id="ribbon" isMinimized='true'>
  {/* Ribbon collapsed initially */}
</RibbonComponent>

// Toggle minimized state programmatically
import { useRef } from 'react';

function App() {
  let ribbonObj = useRef<RibbonComponent>(null);

  const toggleMinimized = () => {
    if (ribbonObj.current) {
      ribbonObj.current.isMinimized = !ribbonObj.current.isMinimized;
    }
  };

  return (
    <div>
      <button onClick={toggleMinimized}>Toggle Minimize</button>
      <RibbonComponent id="ribbon" ref={ribbonObj}>
        {/* Tabs and groups */}
      </RibbonComponent>
    </div>
  );
}
```

**Minimized Behavior:**
- Double-click tab header to minimize/expand
- Click collapse/expand icon in ribbon header
- Clicking a tab header temporarily shows content
- Content hides when clicking elsewhere

## Hide Layout Switcher

Hide the layout switcher button if switching isn't needed:

```tsx
import { useRef } from 'react';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  let ribbonObj = useRef<RibbonComponent>(null);

  const onChange = (args) => {
    if (ribbonObj.current) {
      ribbonObj.current.hideLayoutSwitcher = !args.checked;
    }
  };

  return (
    <div>
      <CheckBoxComponent label="Show/Hide Layout Switcher" checked={true} change={onChange}></CheckBoxComponent>
      <RibbonComponent id="ribbon" ref={ribbonObj} hideLayoutSwitcher={false}>
        {/* Tabs and groups */}
      </RibbonComponent>
    </div>
  );
}
```

## Complete Responsive Example

```tsx
<RibbonComponent id="ribbon" activeLayout='Classic' hideLayoutSwitcher={false}>
  <RibbonTabsDirective>
    <RibbonTabDirective header="Home">
      <RibbonGroupsDirective>
        {/* High priority - collapses last */}
        <RibbonGroupDirective header="Clipboard" priority={0} isCollapsible={false}>
          {/* Items */}
        </RibbonGroupDirective>

        {/* Medium priority */}
        <RibbonGroupDirective header="Font" priority={1}>
          {/* Items */}
        </RibbonGroupDirective>

        {/* Low priority - collapses first */}
        <RibbonGroupDirective header="Styles" priority={2}>
          {/* Items with Simplified display */}
          <RibbonItemDirective type="Button" 
            displayOptions={DisplayMode.Simplified}
            buttonSettings={{ content: "Style" }}>
          </RibbonItemDirective>
        </RibbonGroupDirective>
      </RibbonGroupsDirective>
    </RibbonTabDirective>
  </RibbonTabsDirective>
</RibbonComponent>
```

## Best Practices

1. **Layout Switcher:** Provide layout switcher for desktop applications
2. **Display Options:** Use for layout-specific items
3. **Non-Collapsible Groups:** Keep essential groups visible
4. **Size Consistency:** Set appropriate `allowedSizes` for all items
5. **Priority Planning:** Set group priority based on importance
6. **Mobile Considerations:** Use Simplified layout on mobile devices
