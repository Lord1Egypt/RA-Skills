---
name: syncfusion-react-tabs
description: |
  Implement and customize Tab components in Syncfusion React applications. Use this skill whenever the user needs to create tabbed interfaces, manage tab content rendering, configure header positioning, enable drag-and-drop reordering, or customize tab styling. Essential for building navigation layouts, content organization, responsive tab controls, localized tabs, and accessible tab interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Navigation"
---

# Implementing Tabs in Syncfusion React

The Tab component organizes related content into tabbed sections with headers, allowing users to switch between views. This comprehensive skill guides you through setup, customization, content rendering strategies, API methods, events, accessibility, animations, persistence, and advanced features like drag-and-drop reordering.

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
- [Key Properties Overview](#key-properties-overview)
- [Methods & API Reference](#methods--api-reference)
- [Events & Event Arguments](#events--event-arguments)
- [Animation & Advanced Settings](#animation--advanced-settings)
- [Related Skills](#related-skills)

## When to Use This Skill

- **Creating tabbed interfaces** with header-based navigation
- **Organizing content** into logical sections or views
- **Building responsive layouts** with scrollable or popup overflow handling
- **Customizing header styling** and icon positioning
- **Managing content rendering** performance (lazy loading, dynamic, or initial render)
- **Implementing drag-and-drop** tab reordering for user customization
- **Adding localization support** for international applications
- **Ensuring accessibility compliance** (WCAG, ARIA, keyboard navigation)
- **Styling tabs** with custom CSS or theme customization
- **Programmatically managing tabs** (add, remove, select, hide/show)
- **Handling tab-related events** (selection, drag-drop, add, remove)
- **Preserving user preferences** with state persistence
- **Implementing smooth animations** and transitions

## Component Overview

The Tab component is a navigation control that displays content organized into tabs. Each tab has a header and associated content. Tabs support:

- **Multiple header positions** (top, bottom, left, right)
- **Overflow handling** (scrollable navigation or popup mode)
- **Flexible content rendering** (on-demand, dynamic, or initial load)
- **Drag-and-drop reordering** for interactive tab management
- **Full accessibility** with ARIA attributes and keyboard navigation
- **Extensive customization** via CSS and theme options
- **Internationalization** through localization APIs
- **Animation effects** for content transitions
- **State persistence** across page reloads
- **HTML sanitization** for security

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

- Package dependencies and installation
- Vite and Create React App setup
- CSS imports and theme configuration
- Basic tab initialization with JSON items
- Minimal working example and running the app

**When to read:** Start here to set up a basic Tab component in your React application.

### Header Styling & Customization
📄 **Read:** [references/header-styling.md](references/header-styling.md)

- Built-in header style classes (e-fill, e-background, e-accent)
- Icon positioning options (left, right, top, bottom)
- Icon and header customization with CSS classes
- Code examples for styled headers
- Styling content and hover states

**When to read:** Use this when you need to customize tab header appearance, add icons, or apply predefined styles.

### Orientation & Overflow Modes
📄 **Read:** [references/orientation-overflow.md](references/orientation-overflow.md)

- Header placement positions (top, bottom, left, right)
- Scrollable mode with navigation arrows
- Popup mode with dropdown display
- Touch and swipe support
- Width constraints and responsive behavior

**When to read:** Use this when you need to control header position, handle many tabs with overflow, or build responsive layouts.

### Content Rendering Strategies
📄 **Read:** [references/content-rendering.md](references/content-rendering.md)

- On-demand rendering (lazy loading, default mode)
- Dynamic rendering for state-isolated tabs
- Initial rendering for state preservation
- Performance vs. state considerations
- Choosing the right rendering mode

**When to read:** Use this to optimize tab content performance or preserve user interactions across tab switches.

### Drag and Drop Reordering
📄 **Read:** [references/drag-drop-reordering.md](references/drag-drop-reordering.md)

- Enabling drag-and-drop with allowDragAndDrop
- Handling drag events (onDragStart, dragging, dragged)
- Preventing drag/drop for specific items
- Tab-to-tab drag and drop
- Dragging tabs to external sources (TreeView)
- Drag area constraints

**When to read:** Use this to allow users to reorder tabs or integrate tab dragging with other components.

### Accessibility & Localization
📄 **Read:** [references/accessibility-localization.md](references/accessibility-localization.md)

- WCAG 2.2 and Section 508 compliance
- ARIA attributes and roles for tabs
- Keyboard navigation (arrows, Home, End, Enter, Escape)
- Screen reader support
- Localization with L10n class
- Right-to-left (RTL) language support

**When to read:** Use this when building accessible applications or supporting multiple languages.

## Quick Start Example

Here's a minimal Tab component setup:

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';
import '@syncfusion/ej2-popups/styles/tailwind3.css';
import '@syncfusion/ej2-react-navigations/styles/tailwind3.css';

export default function TabExample() {
  const tabItems = [
    {
      header: { text: 'Home' },
      content: 'Welcome to the home tab'
    },
    {
      header: { text: 'Profile' },
      content: 'User profile information'
    },
    {
      header: { text: 'Settings' },
      content: 'Application settings'
    }
  ];

  return (
    <TabComponent>
      <TabItemsDirective>
        {tabItems.map((item, index) => (
          <TabItemDirective key={index} header={item.header} content={item.content} />
        ))}
      </TabItemsDirective>
    </TabComponent>
  );
}
```

## Common Patterns

### Pattern 1: Styled Tabs with Icons
```jsx
<TabComponent className="e-fill">
  <TabItemsDirective>
    <TabItemDirective 
      header={{ text: 'Home', iconCss: 'e-icons e-home' }} 
      content="Home content" 
    />
    <TabItemDirective 
      header={{ text: 'Profile', iconCss: 'e-icons e-user' }} 
      content="Profile content" 
    />
  </TabItemsDirective>
</TabComponent>
```

### Pattern 2: Vertical Tabs on the Left
```jsx
<TabComponent headerPlacement="Left">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

### Pattern 3: Lazy-Loaded Content (Default)
```jsx
<TabComponent>
  <TabItemsDirective>
    <TabItemDirective 
      header={{ text: 'Lazy Tab' }} 
      content={() => <ExpensiveComponent />} 
    />
  </TabItemsDirective>
</TabComponent>
```

### Pattern 4: Draggable Tabs
```jsx
<TabComponent allowDragAndDrop={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

## Key Properties Overview

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `headerPlacement` | String | `'Top'` | Position of tab headers: `Top`, `Bottom`, `Left`, `Right` |
| `overflowMode` | String | `'Scrollable'` | Overflow handling: `Scrollable` or `Popup` |
| `loadOn` | String | `'Demand'` | Content rendering: `Demand`, `Dynamic`, or `Init` |
| `allowDragAndDrop` | Boolean | `false` | Enable tab reordering via drag and drop |
| `showCloseButton` | Boolean | `false` | Display close button on tab headers |
| `locale` | String | `'en-US'` | Localization culture code (e.g., `'fr-FR'`) |
| `width` | String/Number | `'100%'` | Tab container width |
| `height` | String/Number | `'auto'` | Tab container height |
| `heightAdjustMode` | String | `'Content'` | Height adjustment mode: `None`, `Auto`, `Content`, `Fill` |
| `selectedItem` | Number | `0` | Index of the active tab |
| `enablePersistence` | Boolean | `false` | Persist selected tab state across reloads |
| `enableHtmlSanitizer` | Boolean | `true` | Sanitize HTML content for security |
| `cssClass` | String | `''` | Custom CSS classes to apply to component |
| `enableRtl` | Boolean | `false` | Enable right-to-left layout |
| `scrollStep` | Number | `null` | Distance to scroll when using scroll arrows |
| `reorderActiveTab` | Boolean | `true` | Reorder to show active tab in header area |
| `clearTemplates` | Boolean | `true` | Clear templates when items change dynamically |
| `dragArea` | String | `null` | Restrict drag area for tab reordering |
| `swipeMode` | String | `'Both'` | Swipe detection: `Both`, `Touch`, `Mouse`, `None` |
| `animation` | TabAnimationSettingsModel | Default | Animation settings for tab transitions |

## Methods & API Reference

### addTab(items, index)

Adds new items to the Tab component. The items are inserted at the specified index.

**Parameters:**
- `items` - Array of `TabItemModel` objects to add
- `index` (optional) - Position where items should be inserted. Default is 0.

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AddTabExample() {
  const tabRef = useRef(null);

  const handleAddTab = () => {
    const newItems = [
      {
        header: { text: 'New Tab' },
        content: 'This is dynamically added content'
      }
    ];
    // Add at the end (index 2 if there are 2 existing tabs)
    tabRef.current.addTab(newItems, 2);
  };

  return (
    <div>
      <button onClick={handleAddTab}>Add Tab</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### removeTab(index)

Removes a tab item at the specified index.

**Parameters:**
- `index` - The index of the tab to remove

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RemoveTabExample() {
  const tabRef = useRef(null);

  const handleRemoveTab = (tabIndex) => {
    tabRef.current.removeTab(tabIndex);
  };

  return (
    <div>
      <button onClick={() => handleRemoveTab(1)}>Remove Tab 2</button>
      <TabComponent ref={tabRef} showCloseButton={true}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### select(args, event)

Selects a tab by index or DOM element. Programmatically switches to a different tab.

**Parameters:**
- `args` - Index (number) or HTMLElement of the tab to select
- `event` (optional) - DOM event object

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function SelectTabExample() {
  const tabRef = useRef(null);

  const handleSelectTab = (index) => {
    tabRef.current.select(index);
  };

  return (
    <div>
      <div>
        <button onClick={() => handleSelectTab(0)}>Select Tab 1</button>
        <button onClick={() => handleSelectTab(1)}>Select Tab 2</button>
        <button onClick={() => handleSelectTab(2)}>Select Tab 3</button>
      </div>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### enableTab(index, value)

Enables or disables a specific tab item. Disabled tabs cannot be selected but remain visible.

**Parameters:**
- `index` - Index of the tab to enable/disable
- `value` - Boolean. `true` to enable, `false` to disable

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function EnableTabExample() {
  const tabRef = useRef(null);

  const toggleTabEnabled = (index) => {
    const isCurrentlyEnabled = !tabRef.current.items[index].isDisabled;
    tabRef.current.enableTab(index, isCurrentlyEnabled);
  };

  return (
    <div>
      <button onClick={() => toggleTabEnabled(1)}>Toggle Tab 2 Enable</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### hideTab(index, value)

Shows or hides a tab item at the specified index. Hidden tabs are removed from the DOM.

**Parameters:**
- `index` - Index of the tab to show/hide
- `value` (optional) - Boolean. `true` to hide, `false` to show. Default is `true`

**Returns:** `void`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function HideTabExample() {
  const tabRef = useRef(null);
  const [visibleTabs, setVisibleTabs] = useState([true, true, true]);

  const toggleTabVisibility = (index) => {
    const newVisibleTabs = [...visibleTabs];
    newVisibleTabs[index] = !newVisibleTabs[index];
    setVisibleTabs(newVisibleTabs);
    tabRef.current.hideTab(index, !newVisibleTabs[index]);
  };

  return (
    <div>
      <div>
        <button onClick={() => toggleTabVisibility(0)}>
          Toggle Tab 1 Visibility
        </button>
        <button onClick={() => toggleTabVisibility(1)}>
          Toggle Tab 2 Visibility
        </button>
      </div>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### getItemIndex(tabItemId)

Gets the index of a tab item by its ID.

**Parameters:**
- `tabItemId` - The ID of the tab item

**Returns:** `number` - The index of the tab, or -1 if not found

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function GetItemIndexExample() {
  const tabRef = useRef(null);

  const findTabIndex = () => {
    const itemId = 'tab_2';
    const index = tabRef.current.getItemIndex(itemId);
    console.log(`Tab with ID '${itemId}' is at index: ${index}`);
  };

  return (
    <div>
      <button onClick={findTabIndex}>Find Tab Index</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective id="tab_1" header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective id="tab_2" header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective id="tab_3" header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### refresh()

Refreshes the entire Tab component. Useful after dynamically changing items or properties.

**Parameters:** None

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RefreshTabExample() {
  const tabRef = useRef(null);

  const handleRefresh = () => {
    tabRef.current.refresh();
    console.log('Tab component refreshed');
  };

  return (
    <div>
      <button onClick={handleRefresh}>Refresh Tab</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### refreshActiveTab()

Refreshes only the content of the currently active tab. Does not reload other tabs.

**Parameters:** None

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RefreshActiveTabExample() {
  const tabRef = useRef(null);

  const handleRefreshActive = () => {
    tabRef.current.refreshActiveTab();
    console.log('Active tab content refreshed');
  };

  return (
    <div>
      <button onClick={handleRefreshActive}>Refresh Active Tab</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Dynamically updated content" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### refreshActiveTabBorder()

Refreshes the active tab's visual indicator (underline/border). Useful after styling changes.

**Parameters:** None

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RefreshBorderExample() {
  const tabRef = useRef(null);

  const handleRefreshBorder = () => {
    tabRef.current.refreshActiveTabBorder();
  };

  return (
    <div>
      <button onClick={handleRefreshBorder}>Refresh Border</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### refreshOverflow()

Reorganizes and adjusts the Tab headers to fit the available width without re-rendering the entire component. Useful for responsive layouts.

**Parameters:** None

**Returns:** `void`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RefreshOverflowExample() {
  const tabRef = useRef(null);
  const [tabCount, setTabCount] = useState(3);

  const handleWindowResize = () => {
    if (tabRef.current) {
      tabRef.current.refreshOverflow();
    }
  };

  React.useEffect(() => {
    window.addEventListener('resize', handleWindowResize);
    return () => window.removeEventListener('resize', handleWindowResize);
  }, []);

  const addMoreTabs = () => {
    const newTab = {
      header: { text: `Tab ${tabCount + 1}` },
      content: `Content ${tabCount + 1}`
    };
    tabRef.current.addTab([newTab]);
    setTabCount(tabCount + 1);
    tabRef.current.refreshOverflow();
  };

  return (
    <div>
      <button onClick={addMoreTabs}>Add Tab & Refresh Overflow</button>
      <TabComponent ref={tabRef} width="100%">
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### disable(value)

Disables or enables the entire Tab component.

**Parameters:**
- `value` - Boolean. `true` to disable, `false` to enable

**Returns:** `void`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DisableTabExample() {
  const tabRef = useRef(null);
  const [isDisabled, setIsDisabled] = useState(false);

  const toggleDisable = () => {
    tabRef.current.disable(!isDisabled);
    setIsDisabled(!isDisabled);
  };

  return (
    <div>
      <button onClick={toggleDisable}>
        {isDisabled ? 'Enable' : 'Disable'} Tab Component
      </button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### destroy()

Removes the component from the DOM and detaches all event handlers, attributes, and classes.

**Parameters:** None

**Returns:** `void`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DestroyTabExample() {
  const tabRef = useRef(null);

  const handleDestroy = () => {
    tabRef.current.destroy();
    console.log('Tab component destroyed');
  };

  return (
    <div>
      <button onClick={handleDestroy}>Destroy Tab</button>
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

## Events & Event Arguments

The Tab component provides comprehensive event support for handling user interactions and component state changes.

### selected

Fired after a tab item is selected. Used to execute actions when the user switches to a different tab.

**Event Arguments:** `SelectEventArgs`

**SelectEventArgs Properties:**
- `selectedIndex` (number) - Index of the newly selected tab
- `selectedItem` (HTMLElement) - DOM element of the selected tab
- `selectedContent` (HTMLElement) - Content area of the selected tab
- `previousIndex` (number) - Index of the previously selected tab
- `previousItem` (HTMLElement) - DOM element of the previous tab
- `isInteracted` (boolean) - Whether selection was triggered by user interaction (true) or programmatically (false)
- `isSwiped` (boolean) - Whether selection was triggered by swipe gesture
- `preventFocus` (boolean) - Set to true to prevent focus on selected tab
- `cancel` (boolean) - Set to true to prevent the selection

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function SelectedEventExample() {
  const tabRef = useRef(null);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handleTabSelected = (args) => {
    console.log('Tab selected:', {
      selectedIndex: args.selectedIndex,
      previousIndex: args.previousIndex,
      isInteracted: args.isInteracted,
      isSwiped: args.isSwiped
    });
    setSelectedIndex(args.selectedIndex);
  };

  return (
    <div>
      <p>Currently selected tab index: {selectedIndex}</p>
      <TabComponent ref={tabRef} selected={handleTabSelected}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### selecting

Fired before a tab item is selected. Use this to prevent selection under certain conditions.

**Event Arguments:** `SelectingEventArgs` (same properties as `SelectEventArgs`)

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function SelectingEventExample() {
  const handleTabSelecting = (args) => {
    // Prevent selection of tab at index 1
    if (args.selectedIndex === 1) {
      console.log('Tab 2 selection prevented');
      args.cancel = true;
    }
  };

  return (
    <TabComponent selecting={handleTabSelecting}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2 (Locked)' }} content="Content 2" />
        <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### added

Fired after a new tab item is added to the component.

**Event Arguments:** `AddEventArgs`

**AddEventArgs Properties:**
- `addedItems` (TabItemModel[]) - Array of added tab items
- `name` (string) - Name of the event
- `cancel` (boolean) - Set to true to prevent the action

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AddedEventExample() {
  const tabRef = useRef(null);

  const handleTabAdded = (args) => {
    console.log('Tabs added:', args.addedItems.length);
    console.log('First added item header:', args.addedItems[0].header.text);
  };

  const handleAddTab = () => {
    const newItems = [
      {
        header: { text: 'Newly Added Tab' },
        content: 'This tab was added dynamically'
      }
    ];
    tabRef.current.addTab(newItems);
  };

  return (
    <div>
      <button onClick={handleAddTab}>Add Tab</button>
      <TabComponent ref={tabRef} added={handleTabAdded}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### adding

Fired before a new tab item is added. Use this to validate or modify items before addition.

**Event Arguments:** `AddEventArgs`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AddingEventExample() {
  const tabRef = useRef(null);
  const maxTabs = 5;

  const handleTabAdding = (args) => {
    const totalTabs = tabRef.current.items.length + args.addedItems.length;
    if (totalTabs > maxTabs) {
      console.log(`Cannot exceed ${maxTabs} tabs`);
      args.cancel = true;
    }
  };

  const handleAddTab = () => {
    const newItems = [
      {
        header: { text: `Tab ${tabRef.current.items.length + 1}` },
        content: 'New content'
      }
    ];
    tabRef.current.addTab(newItems);
  };

  return (
    <div>
      <button onClick={handleAddTab}>Add Tab (Max 5)</button>
      <TabComponent ref={tabRef} adding={handleTabAdding}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### removed

Fired after a tab item is removed from the component.

**Event Arguments:** `RemoveEventArgs`

**RemoveEventArgs Properties:**
- `removedItem` (HTMLElement) - DOM element of the removed tab
- `index` (number) - Index of the removed tab
- `name` (string) - Name of the event

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RemovedEventExample() {
  const tabRef = useRef(null);
  const [removedCount, setRemovedCount] = useState(0);

  const handleTabRemoved = (args) => {
    console.log(`Tab at index ${args.index} was removed`);
    setRemovedCount(removedCount + 1);
  };

  const handleRemoveTab = (index) => {
    tabRef.current.removeTab(index);
  };

  return (
    <div>
      <p>Tabs removed: {removedCount}</p>
      <button onClick={() => handleRemoveTab(0)}>Remove First Tab</button>
      <TabComponent ref={tabRef} removed={handleTabRemoved}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### removing

Fired before a tab item is removed. Use this to prevent removal under certain conditions.

**Event Arguments:** `RemoveEventArgs`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RemovingEventExample() {
  const handleTabRemoving = (args) => {
    const confirmed = window.confirm('Are you sure you want to remove this tab?');
    if (!confirmed) {
      args.cancel = true;
    }
  };

  return (
    <TabComponent removing={handleTabRemoving} showCloseButton={true}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### onDragStart

Fired before dragging a tab item. Use this to prevent dragging specific tabs or customize drag behavior.

**Event Arguments:** `DragEventArgs`

**DragEventArgs Properties:**
- `draggedItem` (HTMLElement) - The tab being dragged
- `clonedElement` (HTMLElement) - Clone of the dragged element
- `event` (MouseEvent) - The drag event
- `index` (number) - Index of the dragged tab
- `cancel` (boolean) - Set to true to prevent dragging
- `name` (string) - Name of the event
- `target` (HTMLElement) - Target element
- `droppedItem` (HTMLElement) - The item being dropped on

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function OnDragStartExample() {
  const handleDragStart = (args) => {
    // Prevent dragging the first tab (index 0)
    if (args.index === 0) {
      args.cancel = true;
      console.log('First tab cannot be dragged');
    }
  };

  return (
    <TabComponent allowDragAndDrop={true} onDragStart={handleDragStart}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1 (Locked)' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
        <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### dragging

Fired while a tab is being dragged.

**Event Arguments:** `DragEventArgs`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DraggingEventExample() {
  const [dragStatus, setDragStatus] = useState('');

  const handleDragging = (args) => {
    setDragStatus(`Dragging tab at index ${args.index}`);
  };

  return (
    <div>
      <p>Drag status: {dragStatus}</p>
      <TabComponent allowDragAndDrop={true} dragging={handleDragging}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### dragged

Fired after a tab has been successfully dropped to a new position.

**Event Arguments:** `DragEventArgs`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DraggedEventExample() {
  const [dropMessage, setDropMessage] = useState('');

  const handleDragged = (args) => {
    setDropMessage(`Tab dropped at new position. Index: ${args.index}`);
    console.log('Tab reordered successfully');
  };

  return (
    <div>
      <p>{dropMessage}</p>
      <TabComponent allowDragAndDrop={true} dragged={handleDragged}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
          <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### created

Fired after the Tab component is completely rendered and initialized.

**Event Arguments:** `Event`

**Example:**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function CreatedEventExample() {
  const tabRef = useRef(null);

  const handleCreated = () => {
    console.log('Tab component created and initialized');
    console.log('Total tabs:', tabRef.current.items.length);
  };

  return (
    <TabComponent ref={tabRef} created={handleCreated}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### destroyed

Fired when the Tab component is destroyed and removed from the DOM.

**Event Arguments:** `Event`

**Example:**

```jsx
import React, { useRef, useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DestroyedEventExample() {
  const [showTab, setShowTab] = useState(true);

  const handleDestroyed = () => {
    console.log('Tab component destroyed');
    alert('Tab component has been removed from DOM');
  };

  return (
    <div>
      <button onClick={() => setShowTab(!showTab)}>
        {showTab ? 'Destroy' : 'Create'} Tab
      </button>
      {showTab && (
        <TabComponent destroyed={handleDestroyed}>
          <TabItemsDirective>
            <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
            <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
          </TabItemsDirective>
        </TabComponent>
      )}
    </div>
  );
}
```

## Animation & Advanced Settings

The Tab component supports advanced features including animations, HTML sanitization, and state persistence.

### Animation Configuration

Control how tab content transitions between selections using the `animation` property.

**Animation Settings:**
- `previous` - Animation effect when navigating to previous tab
- `next` - Animation effect when navigating to next tab
- Each animation has: `effect`, `duration` (ms), `easing`

**Available Animation Effects:**
- `SlideLeftIn` - Slide from right to left
- `SlideRightIn` - Slide from left to right
- `SlideUpIn` - Slide from bottom to top
- `SlideDownIn` - Slide from top to bottom
- `FadeIn` - Fade in effect
- `FadeOut` - Fade out effect
- `FadeZoomIn` - Fade with zoom in
- `FadeZoomOut` - Fade with zoom out
- `ZoomIn` - Zoom in effect
- `ZoomOut` - Zoom out effect
- `None` - No animation

**Example: Custom Animation**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AnimationExample() {
  const tabRef = useRef(null);

  const animationSettings = {
    previous: { effect: 'SlideLeftIn', duration: 600, easing: 'ease' },
    next: { effect: 'SlideRightIn', duration: 600, easing: 'ease' }
  };

  return (
    <TabComponent ref={tabRef} animation={animationSettings}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Twitter' }} content="Twitter is an online social networking service..." />
        <TabItemDirective header={{ text: 'Facebook' }} content="Facebook is an online social networking service..." />
        <TabItemDirective header={{ text: 'WhatsApp' }} content="WhatsApp Messenger is a proprietary cross-platform instant messaging client..." />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

**Example: Disabling Animation**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function NoAnimationExample() {
  const animationSettings = {
    previous: { effect: 'None' },
    next: { effect: 'None' }
  };

  return (
    <TabComponent animation={animationSettings}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### HTML Sanitization

Protect against XSS attacks by enabling HTML sanitization. The `enableHtmlSanitizer` property controls whether untrusted HTML is sanitized.

**Example: HTML Sanitization**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function HtmlSanitizationExample() {
  return (
    <div>
      {/* Sanitization enabled (default) - malicious scripts are removed */}
      <h2>With Sanitization (Safe)</h2>
      <TabComponent enableHtmlSanitizer={true}>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Safe Content' }} 
            content="<b>Bold text</b> - This is safe HTML"
          />
          <TabItemDirective 
            header={{ text: 'Dangerous Script' }} 
            content="<img src=x onerror='alert(\"XSS\")' /> - Script will be removed"
          />
        </TabItemsDirective>
      </TabComponent>

      {/* Sanitization disabled - use only with trusted content */}
      <h2>Without Sanitization (Use with Caution)</h2>
      <TabComponent enableHtmlSanitizer={false}>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Trusted Content Only' }} 
            content="<b>Only use when content is from trusted sources</b>"
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### State Persistence

The `enablePersistence` property allows the Tab component to persist the selected tab across page reloads.

**Example: State Persistence**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function PersistenceExample() {
  return (
    <div>
      <p>
        Select a different tab and refresh the page. 
        The previously selected tab will be restored.
      </p>
      <TabComponent enablePersistence={true} selectedItem={0}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'Twitter' }} content="Twitter is an online social networking service that enables users to send and read short 140-character messages..." />
          <TabItemDirective header={{ text: 'Facebook' }} content="Facebook is an online social networking service headquartered in Menlo Park, California..." />
          <TabItemDirective header={{ text: 'WhatsApp' }} content="WhatsApp Messenger is a proprietary cross-platform instant messaging client for smartphones..." />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

**Persisted State:**
- `selectedItem` - The index of the currently active tab

The persistence uses browser local storage to save and restore the state.

### Swipe Navigation

The `swipeMode` property enables or disables tab navigation using swipe gestures. This is particularly useful for mobile devices and touch interfaces, but can be customized to prevent accidental swipes.

**SwipeMode Options:**
- `Both` (default) - Allows swipe with both touch and mouse
- `Touch` - Allows swipe with touch gestures only
- `Mouse` - Allows swipe with mouse gestures only
- `None` - Disables swipe navigation completely

**Example: Disable Swipe to Prevent Accidental Tab Changes**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function SwipeModeExample() {
  return (
    <div>
      <h3>Form Tab - Swipe Disabled to Prevent Data Loss</h3>
      <TabComponent heightAdjustMode='Auto' swipeMode='None'>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Personal Info' }} 
            content="Fill out your personal information without accidental swipes"
          />
          <TabItemDirective 
            header={{ text: 'Address' }} 
            content="Enter your address details"
          />
          <TabItemDirective 
            header={{ text: 'Confirmation' }} 
            content="Review and confirm your information"
          />
        </TabItemsDirective>
      </TabComponent>

      <h3>Mobile Navigation - Touch Swipe Only</h3>
      <TabComponent swipeMode='Touch'>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Twitter' }} 
            content="Twitter content - Swipe on mobile only"
          />
          <TabItemDirective 
            header={{ text: 'Facebook' }} 
            content="Facebook content - Swipe on mobile only"
          />
          <TabItemDirective 
            header={{ text: 'WhatsApp' }} 
            content="WhatsApp content - Swipe on mobile only"
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

**Example: Disable Swipe for Mouse, Allow Touch**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function TouchSwipeExample() {
  return (
    <TabComponent swipeMode='Touch'>
      <TabItemsDirective>
        <TabItemDirective 
          header={{ text: 'Dashboard' }} 
          content="Dashboard content - Swipe available on touch devices"
        />
        <TabItemDirective 
          header={{ text: 'Analytics' }} 
          content="Analytics content"
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### Tab Scroll Step Customization

The `scrollStep` property controls the distance (in pixels) that tab headers scroll when you click the left and right navigation arrows. This is useful for fine-tuning the scroll behavior when tabs overflow.

**Example: Custom Scroll Step**

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function ScrollStepExample() {
  const htmlContent = () => {
    return <div>
      HyperText Markup Language, commonly referred to as HTML, is the standard markup language used to create web pages.
    </div>;
  };
  const csharpContent = () => {
    return <div>
      C# is intended to be a simple, modern, general-purpose, object-oriented programming language.
    </div>;
  };
  const javaContent = () => {
    return <div>
      Java is a set of computer software and specifications developed by Sun Microsystems.
    </div>;
  };
  const vbNetContent = () => {
    return <div>
      The command-line compiler, VBC.EXE, is installed as part of the freeware .NET Framework SDK.
    </div>;
  };
  const xamarinContent = () => {
    return <div>
      Xamarin is a software company created in May 2011 by the engineers that created Mono.
    </div>;
  };
  const aspNetcontent = () => {
    return <div>
      ASP.NET is an open-source server-side web application framework designed for web development.
    </div>;
  };
  const mvcContent = () => {
    return <div>
      The ASP.NET MVC is a web application framework developed by Microsoft.
    </div>;
  };
  const jsContent = () => {
    return <div>
      JavaScript (JS) is an interpreted computer programming language.
    </div>;
  };

  return (
    <div>
      <h3>Tab Scroll Step: 50px per click</h3>
      <p>Click the left/right navigation arrows - tabs scroll 50 pixels at a time</p>
      
      <TabComponent height="250px" scrollStep={50}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'HTML' }} content={htmlContent} />
          <TabItemDirective header={{ text: 'C#' }} content={csharpContent} />
          <TabItemDirective header={{ text: 'Java' }} content={javaContent} />
          <TabItemDirective header={{ text: 'VB.Net' }} content={vbNetContent} />
          <TabItemDirective header={{ text: 'Xamarin' }} content={xamarinContent} />
          <TabItemDirective header={{ text: 'ASP.NET' }} content={aspNetcontent} />
          <TabItemDirective header={{ text: 'ASP.NET MVC' }} content={mvcContent} />
          <TabItemDirective header={{ text: 'JavaScript' }} content={jsContent} />
        </TabItemsDirective>
      </TabComponent>

      <h3>Tab Scroll Step: 100px per click (Faster)</h3>
      <p>Larger scroll step for quicker tab navigation</p>
      
      <TabComponent height="250px" scrollStep={100}>
        <TabItemsDirective>
          <TabItemDirective header={{ text: 'HTML' }} content={htmlContent} />
          <TabItemDirective header={{ text: 'C#' }} content={csharpContent} />
          <TabItemDirective header={{ text: 'Java' }} content={javaContent} />
          <TabItemDirective header={{ text: 'VB.Net' }} content={vbNetContent} />
          <TabItemDirective header={{ text: 'Xamarin' }} content={xamarinContent} />
          <TabItemDirective header={{ text: 'ASP.NET' }} content={aspNetcontent} />
          <TabItemDirective header={{ text: 'ASP.NET MVC' }} content={mvcContent} />
          <TabItemDirective header={{ text: 'JavaScript' }} content={jsContent} />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Advanced Settings: CSS Classes and RTL

**Custom CSS Classes**

Apply custom styling using the `cssClass` property:

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import './CustomTab.css';

export default function CustomCssExample() {
  return (
    <TabComponent cssClass="custom-tab-theme">
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
        <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

**RTL (Right-to-Left) Support**

Enable RTL layout for Arabic, Hebrew, and other RTL languages:

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function RTLExample() {
  return (
    <TabComponent enableRtl={true}>
      <TabItemsDirective>
        <TabItemDirective header={{ text: 'ملخص' }} content="محتوى في اللغة العربية" />
        <TabItemDirective header={{ text: 'تفاصيل' }} content="المزيد من المحتوى" />
        <TabItemDirective header={{ text: 'الإعدادات' }} content="إعدادات التطبيق" />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

**Combined Advanced Example**

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AdvancedSettingsExample() {
  const tabRef = useRef(null);

  const handleTabSelecting = (args) => {
    console.log(`Switching from tab ${args.previousIndex} to tab ${args.selectedIndex}`);
  };

  const animationSettings = {
    previous: { effect: 'SlideLeftIn', duration: 500, easing: 'ease-out' },
    next: { effect: 'SlideRightIn', duration: 500, easing: 'ease-out' }
  };

  return (
    <TabComponent
      ref={tabRef}
      headerPlacement="Top"
      overflowMode="Scrollable"
      enablePersistence={true}
      enableHtmlSanitizer={true}
      enableRtl={false}
      cssClass="advanced-tab-demo"
      animation={animationSettings}
      heightAdjustMode="Auto"
      selecting={handleTabSelecting}
    >
      <TabItemsDirective>
        <TabItemDirective 
          header={{ text: 'Overview', iconCss: 'e-icons e-home' }} 
          content="Welcome to the overview tab" 
        />
        <TabItemDirective 
          header={{ text: 'Profile', iconCss: 'e-icons e-user' }} 
          content="User profile information" 
        />
        <TabItemDirective 
          header={{ text: 'Settings', iconCss: 'e-icons e-settings' }} 
          content="Application settings" 
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

## Related Skills

- [Implementing Accordion](../implementing-accordion/) - Similar navigation component for collapsible content
- [Implementing Sidebars](../implementing-sidebars/) - Complementary navigation pattern
- [Implementing Breadcrumbs](../implementing-breadcrumbs/) - Navigation context alongside tabs
```
