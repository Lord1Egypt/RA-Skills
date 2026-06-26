# Events and Accessibility

## Table of Contents
- [Ribbon Events](#ribbon-events)
- [KeyTips (Keyboard Shortcuts)](#keytips-keyboard-shortcuts)
- [KeyTip Configuration](#keytip-configuration)
- [Accessibility Features](#accessibility-features)
- [WCAG Compliance](#wcag-compliance)
- [RTL Support](#rtl-support)

## Ribbon Events

Handle ribbon interactions through events:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective } from "@syncfusion/ej2-react-ribbon";
import { useRef } from 'react';

function App() {
  let ribbonObj = useRef<RibbonComponent>(null);

  const onItemClick = (args) => {
    console.log("Item clicked:", args.item);
  };

  const onTabSelected = (args) => {
    console.log("Tab selected:", args.tabIndex);
  };

  return (
    <RibbonComponent 
      id="ribbon"
      ref={ribbonObj}
      itemClick={onItemClick}
      tabSelected={onTabSelected}>
      <RibbonTabsDirective>
        {/* Tabs */}
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**Common Events:**
- `itemClick` - When any ribbon item is clicked
- `tabSelected` - When tab selection changes
- `beforeItemRender` - Before item rendering
- `minimized` - When ribbon minimize state changes

## KeyTips (Keyboard Shortcuts)

Enable keyboard access to ribbon commands via KeyTips:

```tsx
<RibbonItemDirective 
  type="Button" 
  keyTip="C"
  buttonSettings={{ 
    iconCss: "e-icons e-copy", 
    content: "Copy" 
  }}>
</RibbonItemDirective>

<RibbonItemDirective 
  type="Button" 
  keyTip="X"
  buttonSettings={{ 
    iconCss: "e-icons e-cut", 
    content: "Cut" 
  }}>
</RibbonItemDirective>
```

**KeyTip Access:**
1. Press `Alt` to display KeyTip letters
2. Type the letter to activate the command

## KeyTip Configuration

Configure KeyTip display and behavior:

```tsx
import { RibbonTabDirective } from "@syncfusion/ej2-react-ribbon";

// Tab with KeyTip
<RibbonTabDirective header="Home" keyTip="H">
  {/* Groups and items */}
</RibbonTabDirective>

// Group with KeyTip
<RibbonGroupDirective header="Clipboard" keyTip="C">
  {/* Items */}
</RibbonGroupDirective>

// Item with KeyTip (already shown above)
```

**KeyTip Best Practices:**
- Use intuitive letters (C for Copy, P for Paste)
- Avoid duplicate KeyTips within same context
- Display KeyTips on Alt press for discoverability

## Accessibility Features

Implement WCAG-compliant accessibility:

```tsx
// Provide alt text for icons
<RibbonItemDirective 
  type="Button"
  keyTip="C"
  buttonSettings={{ 
    iconCss: "e-icons e-copy", 
    content: "Copy",
    ariaLabel: "Copy selected content"  // Screen reader text
  }}>
</RibbonItemDirective>

// Use disabled state appropriately
<RibbonItemDirective 
  type="Button"
  disabled={!selectedContent}
  buttonSettings={{ 
    iconCss: "e-icons e-copy", 
    content: "Copy" 
  }}>
</RibbonItemDirective>

// Provide descriptive titles
<RibbonGroupDirective 
  header="Clipboard"
  title="Clipboard commands - Cut, Copy, Paste">
  {/* Items */}
</RibbonGroupDirective>
```

**ARIA Attributes:**
- `ariaLabel` - Descriptive label for screen readers
- `role` - ARIA role (automatically set)
- `aria-disabled` - Disabled state indication

## WCAG Compliance

Ensure WCAG 2.1 Level AA compliance:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent 
      id="ribbon"
      role="toolbar"
      ariaLabel="Main toolbar with formatting and editing commands">
      <RibbonTabsDirective>
        <RibbonTabDirective 
          header="Home" 
          keyTip="H"
          ariaLabel="Home tab with editing commands">
          <RibbonGroupsDirective>
            <RibbonGroupDirective 
              header="Clipboard"
              ariaLabel="Clipboard operations: Cut, Copy, Paste">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button"
                      keyTip="X"
                      buttonSettings={{ 
                        iconCss: "e-icons e-cut", 
                        content: "Cut",
                        ariaLabel: "Cut (Ctrl+X)"
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button"
                      keyTip="C"
                      buttonSettings={{ 
                        iconCss: "e-icons e-copy", 
                        content: "Copy",
                        ariaLabel: "Copy (Ctrl+C)"
                      }}>
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

**WCAG Requirements Met:**
- Keyboard accessibility (KeyTips, Tab navigation)
- ARIA labels for screen readers
- Color contrast compliance
- Focus indicators
- Semantic HTML structure

## RTL Support

Enable right-to-left language support:

```tsx
<RibbonComponent 
  id="ribbon"
  enableRtl={true}>
  <RibbonTabsDirective>
    {/* Tabs and content - automatically mirrored */}
  </RibbonTabsDirective>
</RibbonComponent>
```

**RTL Behavior:**
- All components mirror horizontally
- Text alignment reverses
- Icons position reverses
- Menus expand from right side

## Keyboard Navigation

Support full keyboard navigation:

```
Alt         - Display KeyTips
Arrow Keys  - Navigate tabs and items
Enter       - Activate button/item
Esc         - Close menus
Tab         - Move to next focusable element
Shift+Tab   - Move to previous focusable element
```

## Complete Accessible Example

```tsx
function App() {
  const handleItemClick = (args) => {
    console.log(`${args.item.content} clicked`);
  };

  const handleTabSelected = (args) => {
    console.log(`Tab ${args.tabIndex} selected`);
  };

  return (
    <RibbonComponent 
      id="ribbon"
      enableRtl={false}
      role="toolbar"
      ariaLabel="Document editing toolbar"
      itemClick={handleItemClick}
      tabSelected={handleTabSelected}>
      
      <RibbonTabsDirective>
        <RibbonTabDirective 
          header="Home" 
          keyTip="H"
          ariaLabel="Home tab">
          <RibbonGroupsDirective>
            <RibbonGroupDirective 
              header="Clipboard"
              ariaLabel="Clipboard operations">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button"
                      keyTip="X"
                      buttonSettings={{ 
                        iconCss: "e-icons e-cut", 
                        content: "Cut",
                        ariaLabel: "Cut selected content"
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button"
                      keyTip="C"
                      buttonSettings={{ 
                        iconCss: "e-icons e-copy", 
                        content: "Copy",
                        ariaLabel: "Copy selected content"
                      }}>
                    </RibbonItemDirective>
                    <RibbonItemDirective 
                      type="Button"
                      keyTip="V"
                      buttonSettings={{ 
                        iconCss: "e-icons e-paste", 
                        content: "Paste",
                        ariaLabel: "Paste from clipboard"
                      }}>
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

## Best Practices

1. **KeyTips:** Provide for all important commands
2. **Labels:** Use descriptive ARIA labels
3. **Contrast:** Ensure color contrast ratios meet WCAG AA
4. **Keyboard:** Support full keyboard navigation
5. **Focus:** Make focus indicators clearly visible
6. **RTL:** Test RTL implementations thoroughly
7. **Screen Readers:** Test with NVDA, JAWS, VoiceOver
