---
name: syncfusion-react-ribbon
description: Implement the Syncfusion React Ribbon component. Use this skill for creating Ribbon UIs with tabs, groups, items, Classic or Simplified layouts, file menu and backstage view, contextual tabs, galleries, KeyTips, accessibility, theming, responsive behavior, customization, and troubleshooting in React.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React Ribbon

## Component Overview

The Syncfusion React Ribbon component is a professional, feature-rich toolbar designed for creating command-centric user interfaces inspired by Microsoft Office. It provides an intuitive hierarchical structure that organizes related commands into visually distinct tabs and groups, enabling users to quickly discover and execute actions.

## Key Capabilities

- **Tabbed Ribbon Interface**: Organize commands into logical tabs for easy navigation and grouping
- **Dual Layout Modes**: Support for Classic (multi-row) and Simplified (single-row) layouts with dynamic switching
- **Multiple Item Types**: Buttons, checkboxes, dropdowns, split buttons, combo boxes, color pickers, group buttons, galleries, and custom templates
- **Responsive Resizing**: Automatically adjust item sizes (Large, Medium, Small) based on available space
- **File Menu & Backstage View**: Complete file menu with traditional File menu or modern backstage interface
- **Contextual Tabs**: Show/hide tabs dynamically based on user selection or application state
- **Gallery Support**: Visual selection galleries with grouping, filtering, and custom item templates
- **KeyTips & Keyboard Navigation**: Accessibility-first keyboard navigation with KeyTip support
- **Group Overflow Management**: Control group priority and dedicated overflow popups for better space utilization
- **Rich Customization**: Custom CSS classes, item templates, icons, and layout control
- **Comprehensive Event Handling**: itemClick, tabSelected, fileMenuSelect, and more for precise control
- **Multi-Theme Support**: Material, Bootstrap, Fluent, and Tailwind CSS themes with dark mode
- **RTL & Accessibility**: Full right-to-left language support and WCAG compliance with ARIA attributes
- **Help Pane Integration**: Built-in help pane for contextual assistance and documentation


**Hierarchical Structure:**
- **Ribbon** (root container) - Main toolbar component
  - **Tabs** (e.g., Home, Insert, View, Design) - Logical command groupings
    - **Groups** (e.g., Clipboard, Font, Styles) - Related command categories
      - **Collections** (logical item containers) - Item arrangement helpers
        - **Items** (buttons, dropdowns, galleries, color pickers, etc.) - Individual commands and controls

## Documentation

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic ribbon component implementation
- CSS imports and themes
- First working example
- TypeScript configuration

### Ribbon Structure

📄 **Read:** [references/ribbon-structure.md](references/ribbon-structure.md)
- Tabs creation and configuration
- Groups organization and hierarchy
- Collections and item containers
- Tab header properties
- Group headers and icons
- Item size and orientation

### Items and Groups

📄 **Read:** [references/items-and-groups.md](references/items-and-groups.md)
- Built-in item types (Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, Template)
- Item properties and icons
- Item sizes (Large, Medium, Small) and active size control
- Item CSS customization with custom classes
- Item tooltips with RibbonTooltipSettings
- Item templates for custom rendering
- Disabled state and display options
- Group orientation (Row vs Column)
- Group overflow behavior and priority

### Tabs and Groups Configuration

📄 **Read:** [references/tabs-and-groups.md](references/tabs-and-groups.md)
- Adding and managing tabs
- Tab-level configuration and CSS customization
- Tab styling with custom classes and themes
- Group properties and organization
- Group headers and icons
- Group collapsibility and launcher icons
- Dynamic tab/group management

### Layouts and Display Modes

📄 **Read:** [references/layouts-display-modes.md](references/layouts-display-modes.md)
- Classic layout (traditional multi-row format)
- Simplified layout (single-row compact format)
- Layout switching and the layout switcher button
- Display options for items (Auto, Classic, Simplified, Overflow)
- Responsive resizing behavior
- Item size adaptation during resizing
- Minimized state (ribbon collapse)

### File Menu and Backstage

📄 **Read:** [references/file-menu-backstage.md](references/file-menu-backstage.md)
- File menu configuration and visibility
- File menu item templates for custom rendering
- File menu popup templates
- File menu animation settings
- File menu tooltip configuration
- Complete event handling (beforeOpen, open, beforeClose, close, beforeItemRender, select)
- Backstage view implementation
- Backstage items configuration with advanced options
- Backstage dimensions (width, height) and positioning
- Backstage KeyTip integration
- Backstage tooltip settings
- Footer items and separators
- Back button customization
- Custom backstage templates
- Navigation within backstage

### Contextual Tabs and Gallery

📄 **Read:** [references/contextual-tabs-gallery.md](references/contextual-tabs-gallery.md)
- Creating contextual tabs
- Controlling contextual tab visibility
- Showing/hiding contextual tabs programmatically
- Gallery item configuration
- Gallery groups and items
- Gallery item templates
- Gallery filtering and selection
- Popup width and height

### Events and Accessibility

📄 **Read:** [references/events-accessibility.md](references/events-accessibility.md)
- Ribbon events (itemClick, tabSelected, etc.)
- Event handling and callbacks
- Keyboard shortcuts with KeyTips
- KeyTip configuration
- Accessibility compliance (WCAG)
- ARIA attributes
- Screen reader support
- RTL support
- Focus management
- Keyboard navigation

### Customization and Theming

📄 **Read:** [references/customization-theming.md](references/customization-theming.md)
- Available built-in themes (Material, Bootstrap, Fluent, Tailwind)
- Importing and applying themes
- CSS customization
- Custom icon fonts
- Theme Studio integration
- Dark mode support
- Responsive design considerations
- Custom CSS classes

### Tooltips and Help Pane

📄 **Read:** [references/tooltips-help-pane.md](references/tooltips-help-pane.md)
- Tooltip implementation for items
- Custom tooltip templates
- Help pane configuration
- Help pane templates and content
- Contextual help integration

### Troubleshooting

📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common issues and solutions
- Performance optimization tips
- Styling and display issues
- Event handling problems
- Module injection troubleshooting
- Responsive behavior issues

## Quick Start

### Basic Ribbon with Tabs and Groups

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective } from "@syncfusion/ej2-react-ribbon";
import "@syncfusion/ej2-base/styles/tailwind3.css";
import "@syncfusion/ej2-buttons/styles/tailwind3.css";
import "@syncfusion/ej2-popups/styles/tailwind3.css";
import "@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
import "@syncfusion/ej2-inputs/styles/tailwind3.css";
import "@syncfusion/ej2-lists/styles/tailwind3.css";
import "@syncfusion/ej2-dropdowns/styles/tailwind3.css";
import "@syncfusion/ej2-navigations/styles/tailwind3.css";
import "@syncfusion/ej2-ribbon/styles/tailwind3.css";

function App() {
  return (
    <RibbonComponent id="ribbon">
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
  );
}

export default App;
```

### Ribbon with File Menu

```tsx
import { RibbonComponent, RibbonTabsDirective, RibbonTabDirective, RibbonGroupsDirective, RibbonGroupDirective, RibbonCollectionsDirective, RibbonCollectionDirective, RibbonItemsDirective, RibbonItemDirective, RibbonFileMenu, Inject } from "@syncfusion/ej2-react-ribbon";
import { MenuItemModel } from '@syncfusion/ej2-navigations';

function App() {
  const fileOptions: MenuItemModel[] = [
    { text: "New", iconCss: "e-icons e-file-new", id: "new" },
    { text: "Open", iconCss: "e-icons e-folder-open", id: "open" },
    { text: "Save", iconCss: "e-icons e-save", id: "save" },
    { text: "Save as", iconCss: "e-icons e-save", id: "saveas" }
  ];

  return (
    <RibbonComponent id="ribbon" fileMenu={{ visible: true, menuItems: fileOptions }}>
      <RibbonTabsDirective>
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
          </RibbonGroupsDirective>
        </RibbonTabDirective>
      </RibbonTabsDirective>
      <Inject services={[RibbonFileMenu]} />
    </RibbonComponent>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Multi-Tab Ribbon with Multiple Item Types

Structure a professional ribbon with multiple tabs containing different item types (buttons, dropdowns, combos).

### Pattern 2: Responsive Ribbon with Classic and Simplified Layouts

Create a ribbon that switches between Classic (multi-row) and Simplified (single-row) layouts based on screen size or user preference.

### Pattern 3: Context-Aware Ribbon

Show/hide contextual tabs dynamically when users select specific objects or content types.

### Pattern 4: File Menu with Backstage View

Combine file menu with backstage for comprehensive document management and application settings.

### Pattern 5: Gallery-Based Item Selection

Use galleries to provide visual selection of styles, templates, or formatting options.

## Key Props and Features

**RibbonComponent:**
- `fileMenu` - Configure file menu visibility and items
- `backStageMenu` - Enable and configure backstage view
- `activeLayout` - Set layout mode (Classic, Simplified)
- `isMinimized` - Programmatically minimize/expand ribbon
- `hideLayoutSwitcher` - Hide the layout switcher button

**RibbonTabDirective:**
- `header` - Tab title text
- `cssClass` - Custom CSS classes for tab styling

**RibbonGroupDirective:**
- `header` - Group title
- `orientation` - Item alignment (Row, Column)
- `groupIconCss` - Custom icon for group overflow
- `showLauncherIcon` - Show launcher icon
- `enableGroupOverflow` - Dedicated overflow popup for group
- `isCollapsible` - Allow group to collapse on resize
- `priority` - Collapse/expand priority

**RibbonItemDirective:**
- `type` - Item type (Button, CheckBox, DropDown, SplitButton, ComboBox, ColorPicker, GroupButton, Gallery, Template)
- `allowedSizes` - Permitted item sizes (Large, Medium, Small)
- `activeSize` - Current display size of the item
- `cssClass` - Custom CSS classes for item styling
- `ribbonTooltipSettings` - Tooltip configuration with title and content
- `itemTemplate` - Custom template for item rendering
- `displayOptions` - Visibility in layouts (Auto, Classic, Simplified, Overflow)
- `disabled` - Enable/disable item
- Settings objects: `buttonSettings`, `dropDownSettings`, `splitButtonSettings`, etc.


**For complete examples and advanced scenarios, explore individual reference files above.**
