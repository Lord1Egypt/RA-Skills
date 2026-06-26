# Tabs and Groups Configuration

## Table of Contents
- [Tab Management](#tab-management)
- [Adding Multiple Tabs](#adding-multiple-tabs)
- [Tab CSS Customization](#tab-css-customization)
- [Group Management](#group-management)
- [Group Headers and Icons](#group-headers-and-icons)
- [Group Orientation](#group-orientation)
- [Collapsible Groups](#collapsible-groups)
- [Group Priority](#group-priority)
- [Launcher Icons](#launcher-icons)
- [Group Overflow](#group-overflow)

## Tab Management

Tabs are the primary organizational level in a ribbon. Define tabs using `RibbonTabsDirective` and `RibbonTabDirective`:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home"></RibbonTabDirective>
        <RibbonTabDirective header="Insert"></RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}
```

**Tab Properties:**
- `header` (string, required) - Tab title displayed to users
- `id` (string, optional) - Unique identifier for programmatic access

## Adding Multiple Tabs

Create multiple tabs to organize ribbon commands by function:

```tsx
function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective header="Home" id="home-tab">
          <RibbonGroupsDirective>
            {/* Home tab groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        <RibbonTabDirective header="Insert" id="insert-tab">
          <RibbonGroupsDirective>
            {/* Insert tab groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        <RibbonTabDirective header="Design" id="design-tab">
          <RibbonGroupsDirective>
            {/* Design tab groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        <RibbonTabDirective header="View" id="view-tab">
          <RibbonGroupsDirective>
            {/* View tab groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}
```

## Tab CSS Customization

Apply custom CSS classes to individual tabs for styling and visual customization:

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        {/* Default tab */}
        <RibbonTabDirective header="Home" id="home-tab">
          <RibbonGroupsDirective>
            {/* Groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        {/* Tab with custom CSS class */}
        <RibbonTabDirective 
          header="Insert" 
          id="insert-tab"
          cssClass="custom-tab">
          <RibbonGroupsDirective>
            {/* Groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        {/* Tab with multiple classes */}
        <RibbonTabDirective 
          header="Design" 
          id="design-tab"
          cssClass="custom-tab highlighted-tab">
          <RibbonGroupsDirective>
            {/* Groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        {/* Conditionally styled tab */}
        <RibbonTabDirective 
          header="View" 
          id="view-tab"
          cssClass={isAdvancedMode ? "advanced-tab" : "basic-tab"}>
          <RibbonGroupsDirective>
            {/* Groups */}
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
    </RibbonComponent>
  );
}

export default App;
```

**cssClass Property:**
- **Type:** `string`
- **Purpose:** Apply custom CSS classes to tab for styling
- **Use Cases:** Custom colors, emphasis, conditional styling, theme variations

### Custom Tab Styling

**CSS Example:**

```css
/* Custom tab styles */
.custom-tab .e-tab-header {
  background-color: #e3f2fd;
  border-radius: 4px 4px 0 0;
}

.custom-tab .e-tab-header:hover {
  background-color: #bbdefb;
}

/* Highlighted tab */
.highlighted-tab .e-tab-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: bold;
}

.highlighted-tab .e-tab-header:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Active tab styling */
.custom-tab .e-tab-header.e-active {
  background-color: #2196f3;
  color: white;
  border-bottom: 3px solid #1976d2;
}

/* Advanced tab styling */
.advanced-tab .e-tab-header {
  background-color: #fff3e0;
  border-left: 3px solid #ff9800;
}

.advanced-tab .e-tab-header.e-active {
  background-color: #ffb74d;
  color: #000;
}

/* Basic tab styling */
.basic-tab .e-tab-header {
  background-color: #f5f5f5;
  color: #666;
}
```

### Tab with Icon and Custom Styling

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import './customTabs.css';

function App() {
  return (
    <RibbonComponent id="ribbon">
      <RibbonTabsDirective>
        <RibbonTabDirective 
          header="Home" 
          id="home-tab"
          cssClass="home-tab">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Clipboard">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        <RibbonTabDirective 
          header="Insert" 
          id="insert-tab"
          cssClass="insert-tab premium-tab">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Tables">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      buttonSettings={{ iconCss: "e-icons e-table", content: "Table" }}>
                    </RibbonItemDirective>
                  </RibbonItemsDirective>
                </RibbonCollectionDirective>
              </RibbonCollectionsDirective>
            </RibbonGroupDirective>
          </RibbonGroupsDirective>
        </RibbonTabDirective>

        <RibbonTabDirective 
          header="Advanced" 
          id="advanced-tab"
          cssClass="advanced-tab">
          <RibbonGroupsDirective>
            <RibbonGroupDirective header="Developer">
              <RibbonCollectionsDirective>
                <RibbonCollectionDirective>
                  <RibbonItemsDirective>
                    <RibbonItemDirective 
                      type="Button" 
                      buttonSettings={{ iconCss: "e-icons e-code", content: "Code" }}>
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

**customTabs.css:**

```css
/* Home tab - default styling */
.home-tab .e-tab-header {
  background-color: #ffffff;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.home-tab .e-tab-header.e-active {
  border-bottom: 2px solid #2196f3;
  background-color: #f5f5f5;
}

/* Insert tab - premium feature */
.insert-tab.premium-tab .e-tab-header {
  position: relative;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #000;
  font-weight: 600;
  padding-right: 30px;
}

.insert-tab.premium-tab .e-tab-header::after {
  content: '★';
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #ff6b6b;
  font-size: 14px;
}

.insert-tab.premium-tab .e-tab-header.e-active {
  background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
}

/* Advanced tab - developer mode */
.advanced-tab .e-tab-header {
  background-color: #263238;
  color: #4caf50;
  border-left: 3px solid #4caf50;
  font-family: 'Courier New', monospace;
}

.advanced-tab .e-tab-header:hover {
  background-color: #37474f;
  color: #66bb6a;
}

.advanced-tab .e-tab-header.e-active {
  background-color: #1b2327;
  color: #81c784;
  border-bottom: 2px solid #4caf50;
}
```

### Dynamic Tab Styling Based on State

```tsx
import { useState } from 'react';
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective } from "@syncfusion/ej2-react-ribbon";

function App() {
  const [activeMode, setActiveMode] = useState<'light' | 'dark'>('light');
  const [isPremium, setIsPremium] = useState(false);

  const getTabClass = (tabName: string) => {
    let classes = [`${tabName}-tab`];
    
    if (activeMode === 'dark') {
      classes.push('dark-mode-tab');
    }
    
    if (isPremium && tabName === 'insert') {
      classes.push('premium-unlocked');
    }
    
    return classes.join(' ');
  };

  return (
    <div>
      <div style={{ padding: '10px', marginBottom: '10px' }}>
        <button onClick={() => setActiveMode(activeMode === 'light' ? 'dark' : 'light')}>
          Toggle {activeMode === 'light' ? 'Dark' : 'Light'} Mode
        </button>
        <button onClick={() => setIsPremium(!isPremium)} style={{ marginLeft: '10px' }}>
          {isPremium ? 'Disable' : 'Enable'} Premium
        </button>
      </div>

      <RibbonComponent id="ribbon">
        <RibbonTabsDirective>
          <RibbonTabDirective 
            header="Home" 
            cssClass={getTabClass('home')}>
            <RibbonGroupsDirective>
              {/* Groups */}
            </RibbonGroupsDirective>
          </RibbonTabDirective>

          <RibbonTabDirective 
            header="Insert" 
            cssClass={getTabClass('insert')}>
            <RibbonGroupsDirective>
              {/* Groups */}
            </RibbonGroupsDirective>
          </RibbonTabDirective>
        </RibbonTabsDirective>
      </RibbonComponent>
    </div>
  );
}

export default App;
```

**Dynamic Styles CSS:**

```css
/* Dark mode tab styles */
.dark-mode-tab .e-tab-header {
  background-color: #1e1e1e;
  color: #e0e0e0;
  border-color: #333;
}

.dark-mode-tab .e-tab-header.e-active {
  background-color: #2d2d2d;
  color: #ffffff;
  border-bottom: 2px solid #64b5f6;
}

/* Premium unlocked styling */
.premium-unlocked .e-tab-header {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(56, 239, 125, 0.7);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(56, 239, 125, 0);
  }
}
```

### Best Practices for Tab Styling

1. **Consistency:** Use a cohesive color scheme across all custom tabs
2. **Active State:** Ensure active tabs are clearly distinguishable
3. **Hover Effects:** Provide visual feedback on hover
4. **Accessibility:** Maintain sufficient color contrast (WCAG AA: 4.5:1)
5. **Performance:** Avoid heavy animations on tab headers
6. **Responsive:** Test custom styles with different ribbon layouts
7. **Theme Integration:** Align custom styles with application theme

### Tab Styling with State Indicators

```tsx
// Tab with notification badge
<RibbonTabDirective 
  header="Messages" 
  id="messages-tab"
  cssClass="messages-tab has-notifications">
  <RibbonGroupsDirective>
    {/* Groups */}
  </RibbonGroupsDirective>
</RibbonTabDirective>
```

**Badge CSS:**

```css
.messages-tab.has-notifications .e-tab-header {
  position: relative;
}

.messages-tab.has-notifications .e-tab-header::before {
  content: '';
  position: absolute;
  top: 5px;
  right: 5px;
  width: 8px;
  height: 8px;
  background-color: #f44336;
  border-radius: 50%;
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
```

## Group Management

Groups organize related commands within tabs. Each tab can contain multiple groups:

```tsx
import { RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";

<RibbonTabDirective header="Home">
  <RibbonGroupsDirective>
    <RibbonGroupDirective header="Clipboard">
      <RibbonCollectionsDirective>
        <RibbonCollectionDirective>
          <RibbonItemsDirective>
            <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
            </RibbonItemDirective>
          </RibbonItemsDirective>
        </RibbonCollectionDirective>
      </RibbonCollectionsDirective>
    </RibbonGroupDirective>

    <RibbonGroupDirective header="Font">
      {/* Font group items */}
    </RibbonGroupDirective>

    <RibbonGroupDirective header="Paragraph">
      {/* Paragraph group items */}
    </RibbonGroupDirective>
  </RibbonGroupsDirective>
</RibbonTabDirective>
```

## Group Headers and Icons

Set group titles and customize the group icon:

```tsx
// Basic group with header
<RibbonGroupDirective header="Clipboard">
  {/* Items */}
</RibbonGroupDirective>

// Group with custom overflow icon
<RibbonGroupDirective 
  header="Clipboard" 
  groupIconCss="e-icons e-paste">
  {/* Items */}
</RibbonGroupDirective>

// Group with icon only
<RibbonGroupDirective 
  header="Font" 
  groupIconCss="e-icons e-bold">
  {/* Items */}
</RibbonGroupDirective>
```

**Properties:**
- `header` (string, required) - Group title
- `groupIconCss` (string) - CSS class for overflow button icon (defaults to group icon if available)

The `groupIconCss` appears when the group collapses during ribbon resizing.

## Group Orientation

Control how items are arranged within a group:

```tsx
import { RibbonItemSize } from "@syncfusion/ej2-react-ribbon";

// Column orientation (default) - items stack vertically
<RibbonGroupDirective header="Clipboard" orientation="Column">
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

// Row orientation - items arrange horizontally
<RibbonGroupDirective header="Font" orientation="Row">
  <RibbonCollectionsDirective>
    <RibbonCollectionDirective>
      <RibbonItemsDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontStyle, index: 2 }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontSize, index: 4 }}>
        </RibbonItemDirective>
      </RibbonItemsDirective>
    </RibbonCollectionDirective>
  </RibbonCollectionsDirective>
</RibbonGroupDirective>
```

**Orientation Constraints:**
- **Column:** Multiple collections OK; each collection can have 1 large or 3 small/medium items
- **Row:** Maximum 3 collections; each collection can have any number of items

## Collapsible Groups

Control whether groups collapse during ribbon resizing:

```tsx
import { ItemModel } from "@syncfusion/ej2-splitbuttons";

const pasteOptions: ItemModel[] = [
  { text: "Keep Source Format" },
  { text: "Merge format" },
  { text: "Keep text only" }
];

// Collapsible group (default - isCollapsible={true})
<RibbonGroupDirective header="Clipboard" groupIconCss="e-icons e-paste" isCollapsible={true}>
  {/* Items */}
</RibbonGroupDirective>

// Non-collapsible group (stays visible)
<RibbonGroupDirective header="Font" isCollapsible={false}>
  <RibbonCollectionsDirective>
    <RibbonCollectionDirective>
      <RibbonItemsDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontStyle, index: 2, width: "150px", allowFiltering: true }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontSize, index: 4, width: "65px", allowFiltering: true }}>
        </RibbonItemDirective>
      </RibbonItemsDirective>
    </RibbonCollectionDirective>
  </RibbonCollectionsDirective>
</RibbonGroupDirective>
```

**Behavior:**
- **`isCollapsible={true}`** (default): Group collapses into an overflow button when space is limited
- **`isCollapsible={false}`**: Group always remains visible; items resize instead

## Group Priority

Define the order in which groups collapse or expand during ribbon resizing:

```tsx
<RibbonGroupDirective header="Clipboard" priority={2} groupIconCss="e-icons e-paste">
  {/* Collapses 2nd */}
</RibbonGroupDirective>

<RibbonGroupDirective header="Font" priority={0} isCollapsible={false}>
  {/* Never collapses (not collapsible) */}
</RibbonGroupDirective>

<RibbonGroupDirective header="Editor" priority={1} groupIconCss="e-icons e-edit">
  {/* Collapses 3rd */}
</RibbonGroupDirective>
```

**Priority Behavior:**
- **Higher priority value** → Collapses first (priority 2 before priority 1)
- **Lower priority value** → Expands first (priority 0 expands before priority 1)
- Groups with same priority collapse/expand in document order

## Launcher Icons

Display a launcher icon that can trigger additional options dialogs:

```tsx
<RibbonGroupDirective 
  header="Clipboard" 
  groupIconCss="e-icons e-paste"
  showLauncherIcon={true}>
  {/* Items */}
</RibbonGroupDirective>
```

**Customize Launcher Icon:**

```tsx
<RibbonComponent id="ribbon" launcherIconCss="e-icons e-description">
  {/* Ribbon tabs and groups */}
</RibbonComponent>
```

**Properties:**
- `showLauncherIcon` (boolean) - Show launcher icon for group (default: false)
- `launcherIconCss` (on Ribbon) - CSS class for launcher icon (applied to all groups)

## Group Overflow

Create dedicated overflow popups for individual groups:

```tsx
import { RibbonColorPicker, Inject } from "@syncfusion/ej2-react-ribbon";

<RibbonGroupDirective 
  header="Font" 
  groupIconCss="e-icons e-bold" 
  enableGroupOverflow={true}>
  <RibbonCollectionsDirective>
    <RibbonCollectionDirective>
      <RibbonItemsDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontStyle, index: 2 }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontSize, index: 4 }}>
        </RibbonItemDirective>
      </RibbonItemsDirective>
    </RibbonCollectionDirective>
    <RibbonCollectionDirective>
      <RibbonItemsDirective>
        <RibbonItemDirective type="ColorPicker" allowedSizes={RibbonItemSize.Small} colorPickerSettings={{ value: "#123456" }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-bold", content: "Bold" }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-italic", content: "Italic" }}>
        </RibbonItemDirective>
        <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Small} buttonSettings={{ iconCss: "e-icons e-underline", content: "Underline" }}>
        </RibbonItemDirective>
      </RibbonItemsDirective>
    </RibbonCollectionDirective>
  </RibbonCollectionsDirective>
</RibbonGroupDirective>

<Inject services={[RibbonColorPicker]} />
```

**`enableGroupOverflow` Options:**
- **`true`**: Group has its own dedicated overflow popup when items don't fit
- **`false`** (default): Overflow items go to ribbon's main overflow area

## Complete Multi-Group Example

```tsx
<RibbonTabDirective header="Home">
  <RibbonGroupsDirective>
    {/* Priority 2 - Collapses first */}
    <RibbonGroupDirective header="Clipboard" 
      groupIconCss="e-icons e-paste" 
      priority={2}
      showLauncherIcon={true}>
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
            <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Medium} buttonSettings={{ iconCss: "e-icons e-cut", content: "Cut" }}>
            </RibbonItemDirective>
            <RibbonItemDirective type="Button" allowedSizes={RibbonItemSize.Medium} buttonSettings={{ iconCss: "e-icons e-copy", content: "Copy" }}>
            </RibbonItemDirective>
          </RibbonItemsDirective>
        </RibbonCollectionDirective>
      </RibbonCollectionsDirective>
    </RibbonGroupDirective>

    {/* Non-collapsible group - Priority 0 */}
    <RibbonGroupDirective header="Font" 
      groupIconCss="e-icons e-bold" 
      priority={0}
      isCollapsible={false}
      orientation="Row">
      <RibbonCollectionsDirective>
        <RibbonCollectionDirective>
          <RibbonItemsDirective>
            <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontStyle, index: 2, width: "150px", allowFiltering: true }}>
            </RibbonItemDirective>
            <RibbonItemDirective type="ComboBox" comboBoxSettings={{ dataSource: fontSize, index: 4, width: "65px", allowFiltering: true }}>
            </RibbonItemDirective>
          </RibbonItemsDirective>
        </RibbonCollectionDirective>
      </RibbonCollectionsDirective>
    </RibbonGroupDirective>

    {/* Priority 1 - Collapses last */}
    <RibbonGroupDirective header="Editor" 
      groupIconCss="e-icons e-edit" 
      priority={1}>
      <RibbonCollectionsDirective>
        <RibbonCollectionDirective>
          <RibbonItemsDirective>
            <RibbonItemDirective type="Button" buttonSettings={{ iconCss: "e-icons e-edit", content: "Editor" }}>
            </RibbonItemDirective>
          </RibbonItemsDirective>
        </RibbonCollectionDirective>
      </RibbonCollectionsDirective>
    </RibbonGroupDirective>
  </RibbonGroupsDirective>
</RibbonTabDirective>
```

## Best Practices

1. **Logical Organization:** Group related commands
2. **Icon Consistency:** Use icons from e-icons library
3. **Priority Planning:** Set priority based on importance
4. **Collapsibility:** Keep essential items visible with `isCollapsible={false}`
5. **Launcher Icons:** Use for groups with additional options dialogs
