---
name: syncfusion-react-buttons
description: Comprehensive guide for implementing Syncfusion React button components including Button, ButtonGroup, DropDownButton, Floating Action Button, ProgressButton, SplitButton, Speed Dial, Switch, RadioButton, and Chips. Use this when adding styled buttons, toggle behavior, icon support, grouped selections, dropdown action menus, programmatic control floating primary actions, expandable speed dial menus, compact interactive elements with avatars and drag-and-drop, or single/multiple selection capabilities to a React application.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Buttons"
---

# Syncfusion React Buttons

> 📌 **Agent Notice:** `📄 Read:` links in Navigation Guide sections are reference pointers for passive file reading only. They do not imply automatic tool invocation, command execution, or action chaining.

---

## Button

The Syncfusion `ButtonComponent` is a graphical user interface element that triggers an action on click. It supports text, icons, or both, with extensive styling, accessibility, and behavioral options.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/button-getting-started.md](references/button-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Rendering the first ButtonComponent
- Enabling ripple effects
- Basic click handling

#### Types and Styles
📄 **Read:** [references/button-types-and-styles.md](references/button-types-and-styles.md)
- Predefined color styles (primary, success, info, warning, danger, link)
- Flat, outline, round, and toggle button types
- Basic HTML button types (submit, reset)
- Icon buttons (font icons, SVG)
- Icon positioning (left/right)
- Button sizes (small, normal)

#### How-To Patterns
📄 **Read:** [references/button-how-to.md](references/button-how-to.md)
- Create a block (full-width) button
- Create a rounded-corner button
- Add a navigation link to a button
- Customize button appearance with CSS
- Style native input and anchor elements as buttons
- Set the disabled state
- Enable right-to-left (RTL) support
- Add a tooltip on hover
- Implement a repeat button

#### Style and Appearance
📄 **Read:** [references/button-style-and-appearance.md](references/button-style-and-appearance.md)
- Available CSS classes and their purposes
- Overriding default styles
- Custom theme creation with Theme Studio

#### Accessibility
📄 **Read:** [references/button-accessibility.md](references/button-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes
- Keyboard navigation
- Screen reader support

#### API Reference
📄 **Read:** [references/button-api.md](references/button-api.md)
- All properties, methods, and events
- Property types, defaults, and constraints

---

### Quick Start

> ⚠️ Run the following command manually in your terminal. Do not execute automatically.

```bash
# Run in your terminal
npm install @syncfusion/ej2-react-buttons --save
```

```tsx
// src/App.css
// @import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
// @import "../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css";

import { enableRipple } from '@syncfusion/ej2-base';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <div>
      <ButtonComponent>Default</ButtonComponent>
      <ButtonComponent cssClass='e-primary'>Primary</ButtonComponent>
      <ButtonComponent cssClass='e-success'>Success</ButtonComponent>
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Styled Button
```tsx
<ButtonComponent cssClass='e-primary'>Save</ButtonComponent>
<ButtonComponent cssClass='e-danger'>Delete</ButtonComponent>
<ButtonComponent cssClass='e-flat'>Flat</ButtonComponent>
<ButtonComponent cssClass='e-outline'>Outline</ButtonComponent>
```

#### Icon Button
```tsx
<ButtonComponent iconCss='e-icons e-save'>Save</ButtonComponent>
<ButtonComponent iconCss='e-icons e-delete' iconPosition='Right'>Delete</ButtonComponent>
```

#### Toggle Button
```tsx
const [active, setActive] = React.useState(false);
<ButtonComponent isToggle={true} cssClass='e-flat'
  onClick={() => setActive(!active)}>
  {active ? 'Pause' : 'Play'}
</ButtonComponent>
```

#### Disabled Button
```tsx
<ButtonComponent disabled={true}>Disabled</ButtonComponent>
```

#### Block (Full-Width) Button
```tsx
<ButtonComponent cssClass='e-block e-primary'>Full Width</ButtonComponent>
```

---

## ButtonGroup

The ButtonGroup is a pure CSS component that groups a series of buttons together in a horizontal (default) or vertical layout. It supports normal button behavior as well as radio-type (single selection) and checkbox-type (multiple selection) behaviors. Buttons can be nested with DropDownButton and SplitButton components.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/buttongroup-getting-started.md](references/buttongroup-getting-started.md)
- Installation and package setup
- Adding CSS references and theme imports
- Basic ButtonGroup implementation
- Running the application

#### Types and Styles
📄 **Read:** [references/buttongroup-types-and-styles.md](references/buttongroup-types-and-styles.md)
- Outline ButtonGroup (`e-outline`)
- Predefined color styles (`e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`)
- Mixing styles within a group

#### Selection and Nesting
📄 **Read:** [references/buttongroup-selection-and-nesting.md](references/buttongroup-selection-and-nesting.md)
- Single selection (radio type)
- Multiple selection (checkbox type)
- Setting initial selected state
- Nesting DropDownButton inside ButtonGroup
- Nesting SplitButton inside ButtonGroup

#### How-To Guide
📄 **Read:** [references/buttongroup-how-to.md](references/buttongroup-how-to.md)
- Add icons to buttons (`iconCss`)
- Rounded corners (`e-round-corner`)
- Disable individual or all buttons
- Enable ripple effect
- Enable RTL support
- Vertical orientation (`e-vertical`)
- Form submit with radio/checkbox ButtonGroup
- Initialize using `createButtonGroup` utility function

#### Style and Appearance
📄 **Read:** [references/buttongroup-style-and-appearance.md](references/buttongroup-style-and-appearance.md)
- Available CSS classes for customization
- Overriding hover, focus, active states
- Theme Studio integration

#### Accessibility
📄 **Read:** [references/buttongroup-accessibility.md](references/buttongroup-accessibility.md)
- WCAG 2.2, Section 508 compliance
- Keyboard navigation shortcuts
- Screen reader support

---

### Quick Start

```tsx
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div className='e-btn-group'>
      <ButtonComponent>HTML</ButtonComponent>
      <ButtonComponent>CSS</ButtonComponent>
      <ButtonComponent>Javascript</ButtonComponent>
    </div>
  );
}
export default App;
```

Required CSS imports in `src/App.css`:
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

---

### Common Patterns

#### Radio (single-select) ButtonGroup
```tsx
<div className='e-btn-group'>
  <input type="radio" id="radioleft" name="align" value="left" />
  <label className="e-btn" htmlFor="radioleft">Left</label>
  <input type="radio" id="radiomiddle" name="align" value="middle" />
  <label className="e-btn" htmlFor="radiomiddle">Center</label>
  <input type="radio" id="radioright" name="align" value="right" />
  <label className="e-btn" htmlFor="radioright">Right</label>
</div>
```

#### Checkbox (multi-select) ButtonGroup
```tsx
<div className='e-btn-group'>
  <input type="checkbox" id="checkbold" name="font" value="bold" />
  <label className="e-btn" htmlFor="checkbold">Bold</label>
  <input type="checkbox" id="checkitalic" name="font" value="italic" />
  <label className="e-btn" htmlFor="checkitalic">Italic</label>
  <input type="checkbox" id="checkline" name="font" value="underline" />
  <label className="e-btn" htmlFor="checkline">Underline</label>
</div>
```

#### Vertical ButtonGroup
```tsx
<div className='e-btn-group e-vertical'>
  <ButtonComponent>HTML</ButtonComponent>
  <ButtonComponent>CSS</ButtonComponent>
  <ButtonComponent>Javascript</ButtonComponent>
</div>
```

---

### Key Props

| Prop / Class | Component | Description |
|---|---|---|
| `cssClass` | `ButtonComponent` | Apply style classes (`e-outline`, `e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`) |
| `iconCss` | `ButtonComponent` | CSS class(es) for button icon |
| `disabled` | `ButtonComponent` | Disables the button |
| `isPrimary` | `ButtonComponent` | Marks button as primary |
| `e-btn-group` | container div | Required wrapper class for ButtonGroup |
| `e-outline` | container div + buttons | Outline style for the group |
| `e-round-corner` | container div | Rounded corners for the group |
| `e-vertical` | container div | Vertical layout |
| `e-rtl` | container div | Right-to-left layout |

---

## DropDownButton

The Syncfusion `DropDownButtonComponent` renders a button that toggles a contextual popup menu with a list of action items. It supports icons, separators, templates, animations, accessibility, and extensive customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/dropdownbutton-getting-started.md](references/dropdownbutton-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Rendering the first DropDownButtonComponent
- Binding data source with `items`
- Minimal working example

#### Popup Items and Navigation
📄 **Read:** [references/dropdownbutton-popup-items.md](references/dropdownbutton-popup-items.md)
- Adding icons to popup items with `iconCss`
- Navigation URLs via `url` on items
- Separators to group popup items
- Item templates with `beforeItemRender`
- Popup (target) templates
- Underline characters in item text

#### Icons and Layout
📄 **Read:** [references/dropdownbutton-icons-and-layout.md](references/dropdownbutton-icons-and-layout.md)
- Button icons with `iconCss` and `iconPosition`
- Icon-only buttons with `e-caret-hide`
- Sprite image icons
- Vertical button layout with `e-vertical`
- Customizing icon size and button width

#### Appearance and Styling
📄 **Read:** [references/dropdownbutton-appearance-and-styling.md](references/dropdownbutton-appearance-and-styling.md)
- CSS class overrides (color styles, sizes, states)
- Rounded corners with `e-round-corner`
- Hide dropdown arrow with `e-caret-hide`
- Popup width with `popupWidth`
- Theme Studio customization
- Animation settings for popup open/close

#### Events and Interactivity
📄 **Read:** [references/dropdownbutton-events-and-interactivity.md](references/dropdownbutton-events-and-interactivity.md)
- Handling `select` event on item click
- `beforeOpen` / `beforeClose` for dynamic caret icon
- `open` event for custom popup positioning
- Disabling the button with `disabled`
- RTL support with `enableRtl`
- Opening a dialog on item select
- Dynamic `addItems` / `removeItems` methods
- `toggle` method for programmatic open/close

#### Item Template
📄 **Read:** [references/dropdownbutton-item-template.md](references/dropdownbutton-item-template.md)
- `itemTemplate` property for custom item rendering
- Rendering links, icons, and rich content inside items

#### ListView Integration
📄 **Read:** [references/dropdownbutton-listview-integration.md](references/dropdownbutton-listview-integration.md)
- Using `target` property with a ListView element
- Grouped popup items with category headers

#### Accessibility
📄 **Read:** [references/dropdownbutton-accessibility.md](references/dropdownbutton-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes (`role`, `aria-haspopup`, `aria-expanded`)
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/dropdownbutton-api.md](references/dropdownbutton-api.md)
- All properties: `items`, `cssClass`, `iconCss`, `iconPosition`, `disabled`, `enableRtl`, `animationSettings`, `popupWidth`, `target`, `itemTemplate`, `content`, `closeActionEvents`, `createPopupOnClick`, `enableHtmlSanitizer`, `enablePersistence`, `locale`
- All events: `beforeClose`, `beforeOpen`, `beforeItemRender`, `close`, `open`, `select`, `created`
- All methods: `addItems`, `removeItems`, `toggle`, `focusIn`, `destroy`, `getPersistData`
- Type definitions: `ItemModel`, `MenuEventArgs`, `OpenCloseMenuEventArgs`, `BeforeOpenCloseMenuEventArgs`

---

### Quick Start

```tsx
import { DropDownButtonComponent, ItemModel } from '@syncfusion/ej2-react-splitbuttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  const items: ItemModel[] = [
    { text: 'Cut' },
    { text: 'Copy' },
    { text: 'Paste' },
  ];

  return (
    <DropDownButtonComponent items={items}>
      Clipboard
    </DropDownButtonComponent>
  );
}

export default App;
```

---

### Common Patterns

#### Button with icon and popup icons
```tsx
const items: ItemModel[] = [
  { text: 'Edit',   iconCss: 'ddb-icons e-edit' },
  { text: 'Delete', iconCss: 'ddb-icons e-delete' },
];
<DropDownButtonComponent items={items} iconCss="ddb-icons e-message">
  Message
</DropDownButtonComponent>
```

#### Grouped items with separator
```tsx
const items: ItemModel[] = [
  { text: 'Cut',   iconCss: 'e-db-icons e-cut' },
  { text: 'Copy',  iconCss: 'e-icons e-copy' },
  { separator: true },
  { text: 'Font',  iconCss: 'e-db-icons e-font' },
];
```

#### Handling item selection
```tsx
import { MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';

function onSelect(args: MenuEventArgs) {
  console.log('Selected:', args.item.text);
}
<DropDownButtonComponent items={items} select={onSelect}>
  Actions
</DropDownButtonComponent>
```

---

## Floating Action Button

The Syncfusion React `FabComponent` is a circular button that floats above the UI and represents the primary action in an application. It supports flexible **positioning**, **icon + text content**, **predefined styles**, full **accessibility compliance**, and CSS customization.

**Package:** `@syncfusion/ej2-react-buttons`

### Navigation Guide

#### Getting Started
📄 **Read:** [references/floating-action-button-getting-started.md](references/floating-action-button-getting-started.md)
- Installing `@syncfusion/ej2-react-buttons`
- CSS theme imports for Tailwind3
- Minimal `FabComponent` setup
- Using `target` to position relative to a container
- Handling the click event

#### Icons and Content
📄 **Read:** [references/floating-action-button-icons.md](references/floating-action-button-icons.md)
- `iconCss` prop for icon-only FAB
- `content` prop for text label
- `iconPosition` for icon-left vs icon-right layout
- Combined icon + text examples

#### Positions
📄 **Read:** [references/floating-action-button-positions.md](references/floating-action-button-positions.md)
- `position` prop with all nine predefined values (TopLeft → BottomRight)
- `target` prop to scope FAB to a container
- Custom CSS position using `cssClass`

#### Styles and Appearance
📄 **Read:** [references/floating-action-button-styles.md](references/floating-action-button-styles.md)
- Predefined `cssClass` values: `e-primary`, `e-outline`, `e-info`, `e-success`, `e-warning`, `e-danger`
- CSS class override reference table
- Show text on hover with CSS transition
- Outline color customization

#### Events
📄 **Read:** [references/floating-action-button-events.md](references/floating-action-button-events.md)
- `onClick` event for click handling
- `created` event for post-render initialization

#### Accessibility
📄 **Read:** [references/floating-action-button-accessibility.md](references/floating-action-button-accessibility.md)
- WCAG 2.2 / Section 508 compliance
- WAI-ARIA attributes (`aria-label`, `aria-disabled`, `role="button"`)
- Keyboard navigation (Enter, Space, Tab, Escape)
- RTL support via `enableRtl`
- Screen reader support

#### API Reference
📄 **Read:** [references/floating-action-button-api.md](references/floating-action-button-api.md)
- All properties: `content`, `cssClass`, `disabled`, `enableHtmlSanitizer`, `enablePersistence`, `enableRtl`, `iconCss`, `iconPosition`, `isPrimary`, `isToggle`, `position`, `target`, `visible`
- Methods: `click()`, `destroy()`, `focusIn()`, `getPersistData()`, `refreshPosition()`
- Events: `created`, `onClick`

---

### Quick Start

> ⚠️ Run the following command manually in your terminal. Do not execute automatically.

```bash
# Run in your terminal
npm install @syncfusion/ej2-react-buttons --save
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  return (
    <div>
      <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}></div>
      <FabComponent id="fab" content="Add" target="#targetElement" />
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Icon-Only FAB (most common)
```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px' }}></div>
      <FabComponent id="fab" iconCss="e-icons e-edit" target="#target" />
    </div>
  );
}
export default App;
```

#### FAB with Click Handler
```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  function handleClick(): void {
    alert('FAB clicked!');
  }

  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px' }}></div>
      <FabComponent id="fab" iconCss="e-icons e-edit" content="Edit" onClick={handleClick} target="#target" />
    </div>
  );
}
export default App;
```

#### FAB with Custom Style
```tsx
import { FabComponent } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';

function App() {
  return (
    <div>
      <div id="target" style={{ position: 'relative', minHeight: '350px' }}></div>
      <FabComponent id="fab" iconCss="e-icons e-delete" cssClass="e-danger" target="#target" />
    </div>
  );
}
export default App;
```

---

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `iconCss` | `string` | `''` | CSS class for the FAB icon |
| `content` | `string` | `''` | Text label displayed on/beside the FAB |
| `iconPosition` | `'Left' \| 'Right'` | `'Left'` | Icon placement relative to text |
| `position` | `FabPosition` | `'BottomRight'` | Predefined position within target/viewport |
| `target` | `string \| HTMLElement` | `''` | Container element selector for FAB scoping |
| `cssClass` | `string` | `''` | Custom CSS class(es) for styling |
| `disabled` | `boolean` | `false` | Disables the FAB |
| `visible` | `boolean` | `true` | Shows or hides the FAB |
| `isPrimary` | `boolean` | `true` | Applies primary styling |
| `enableRtl` | `boolean` | `false` | Right-to-left rendering |
| `enableHtmlSanitizer` | `boolean` | `true` | Sanitizes HTML in `content` |

---

## Speed Dial

The Syncfusion `SpeedDialComponent` is a floating action button (FAB) that reveals a set of contextual action items when clicked or hovered. It supports Linear and Radial display modes, flexible positioning, templates, animations, modal overlay, and full accessibility.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/speeddial-getting-started.md](references/speeddial-getting-started.md)
- Installation and package setup
- CSS imports and theme configuration
- Rendering the first SpeedDialComponent
- Basic items configuration
- Target element setup

#### Items Configuration
📄 **Read:** [references/speeddial-items.md](references/speeddial-items.md)
- SpeedDialItemModel fields (text, iconCss, id, title, disabled)
- Icon only, text only, icon with text combinations
- Disabling individual items
- Animation effects (Fade, Zoom, etc.)
- Item templates overview

#### Display Modes
📄 **Read:** [references/speeddial-display-modes.md](references/speeddial-display-modes.md)
- Linear mode (default) and direction values (Up, Down, Left, Right, Auto)
- Radial mode overview and usage

#### Radial Menu
📄 **Read:** [references/speeddial-radial-menu.md](references/speeddial-radial-menu.md)
- Setting mode to Radial
- radialSettings: direction (Clockwise, AntiClockwise, Auto)
- startAngle and endAngle configuration
- offset to control item distance from button

#### Positions and Visibility Control
📄 **Read:** [references/speeddial-positions.md](references/speeddial-positions.md)
- Position values (TopLeft, TopCenter, TopRight, MiddleLeft, MiddleCenter, MiddleRight, BottomLeft, BottomCenter, BottomRight)
- Target element relative positioning
- opensOnHover for hover-based open behavior
- Programmatic show() and hide() methods
- refreshPosition() after layout changes

#### Styles and Appearance
📄 **Read:** [references/speeddial-styles.md](references/speeddial-styles.md)
- openIconCss and closeIconCss for button icons
- content property for text button
- Predefined cssClass values (e-primary, e-outline, e-info, e-success, e-warning, e-danger)
- disabled and visible properties
- Tooltip via title attribute
- Custom CSS overrides

#### Templates
📄 **Read:** [references/speeddial-template.md](references/speeddial-template.md)
- itemTemplate for custom item rendering
- popupTemplate for full popup customization
- JSX function template pattern

#### Events
📄 **Read:** [references/speeddial-events.md](references/speeddial-events.md)
- clicked, created, beforeOpen, onOpen, beforeClose, onClose, beforeItemRender
- Event argument types: SpeedDialItemEventArgs, SpeedDialBeforeOpenCloseEventArgs, SpeedDialOpenCloseEventArgs
- Cancel pattern for beforeOpen and beforeClose

#### Modal
📄 **Read:** [references/speeddial-modal.md](references/speeddial-modal.md)
- Enabling modal overlay
- Interaction blocking behavior
- Close on backdrop click

#### Accessibility
📄 **Read:** [references/speeddial-accessibility.md](references/speeddial-accessibility.md)
- WCAG 2.2, Section 508 compliance
- WAI-ARIA attributes (role, aria-expanded, aria-label, etc.)
- Keyboard navigation shortcuts
- Screen reader support
- RTL support via enableRtl

#### API Reference
📄 **Read:** [references/speeddial-api.md](references/speeddial-api.md)
- All properties, methods, and events with types and defaults

---

### Quick Start

> ⚠️ Run the following command manually in your terminal. Do not execute automatically.

```bash
# Run in your terminal
npm install @syncfusion/ej2-react-buttons --save
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
```

```tsx
import { SpeedDialComponent, SpeedDialItemModel } from '@syncfusion/ej2-react-buttons';
import * as React from 'react';
import './App.css';

function App() {
  const items: SpeedDialItemModel[] = [
    { text: 'Cut', iconCss: 'e-icons e-cut' },
    { text: 'Copy', iconCss: 'e-icons e-copy' },
    { text: 'Paste', iconCss: 'e-icons e-paste' }
  ];

  return (
    <div id="targetElement" style={{ position: 'relative', minHeight: '350px', border: '1px solid' }}>
      <SpeedDialComponent
        id='speeddial'
        content='Edit'
        openIconCss='e-icons e-edit'
        closeIconCss='e-icons e-close'
        items={items}
        target="#targetElement"
      />
    </div>
  );
}
export default App;
```

---

### Common Patterns

#### Icon-only items with tooltip
```tsx
const items: SpeedDialItemModel[] = [
  { iconCss: 'e-icons e-cut', title: 'Cut' },
  { iconCss: 'e-icons e-copy', title: 'Copy' },
  { iconCss: 'e-icons e-paste', title: 'Paste' }
];
<SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' items={items} target="#targetElement" />
```

#### Radial mode
```tsx
import { RadialSettingsModel } from '@syncfusion/ej2-react-buttons';
const radialSettings: RadialSettingsModel = { direction: 'AntiClockwise', offset: '80px' };
<SpeedDialComponent id='speeddial' openIconCss='e-icons e-edit' items={items}
  mode='Radial' radialSettings={radialSettings} target="#targetElement" />
```

#### Handle item click
```tsx
import { SpeedDialItemEventArgs } from '@syncfusion/ej2-react-buttons';
function itemClick(args: SpeedDialItemEventArgs) {
  console.log('Clicked:', args.item.text);
}
<SpeedDialComponent id='speeddial' items={items} content='Edit' clicked={itemClick} target="#targetElement" />
```

#### Modal with overlay
```tsx
<SpeedDialComponent id='speeddial' items={items} openIconCss='e-icons e-edit'
  modal={true} target="#targetElement" />
```

#### Programmatic open/close
```tsx
let speeddialRef: SpeedDialComponent;
<SpeedDialComponent id='speeddial' items={items} openIconCss='e-icons e-edit'
  target="#targetElement" ref={scope => { speeddialRef = scope; }} />
// Open:  speeddialRef.show();
// Close: speeddialRef.hide();
```
## Implementing the Syncfusion React ProgressButton

The `ProgressButtonComponent` from `@syncfusion/ej2-react-splitbuttons` provides a button that
visualises the progression of a background operation — complete with an animated spinner, a
background progress bar fill, and content/style hooks at every stage of the operation.

### Navigation Guide

| Task | Read |
|---|---|
| Install package and first render | [`references/getting-started.md`](references/progressbutton-getting-started.md) |
| Spinner position/size/template + progress bar + animations + step/percent/start/stop | [`references/spinner-and-progress.md`](references/progressbutton-spinner-and-progress.md) |
| CSS classes, theming, Theme Studio | [`references/style-and-appearance.md`](references/progressbutton-style-and-appearance.md) |
| ARIA attributes, keyboard shortcuts, screen-reader compliance | [`references/accessibility.md`](references/progressbutton-accessibility.md) |
| Enable the background progress fill | [`references/how-to-enable-progress-in-button.md`](references/progressbutton-how-to-enable-progress-in-button.md) |
| Hide the spinner (show only progress bar) | [`references/how-to-hide-spinner.md`](references/progressbutton-how-to-hide-spinner.md) |
| Vertical, top, or reverse progress fill | [`references/how-to-customize-progress-using-cssclass.md`](references/progressbutton-how-to-customize-progress-using-cssclass.md) |
| Change button text / CSS class while progress runs | [`references/how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md`](references/progressbutton-how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md) |
| Trace / handle lifecycle events | [`references/how-to-trace-events-of-progress-button.md`](references/progressbutton-how-to-trace-events-of-progress-button.md) |
| Full API reference (all props, events, methods, types) | [`references/api.md`](references/progressbutton-api.md) |

---

### Quick Start

```bash
npm install @syncfusion/ej2-react-splitbuttons --save
```

```tsx
// src/App.tsx
import { ProgressButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import './App.css';

function App() {
  return <ProgressButtonComponent content="Submit" />;
}
export default App;
```

```css
/* src/App.css */
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css";
```

---

### Common Patterns

#### Progress bar + hidden spinner

```tsx
<ProgressButtonComponent
  content="Upload"
  enableProgress={true}
  cssClass="e-hide-spinner"
  duration={4000}
/>
```

#### Custom spinner (right, small, templated)

```tsx
import { SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';

const spinSettings: SpinSettingsModel = {
  position: 'Right',
  width: 20,
  template: '<div class="my-spinner"></div>'
};

<ProgressButtonComponent content="Submit" spinSettings={spinSettings} />
```

#### Slide animation with centered spinner

```tsx
import { AnimationSettingsModel, SpinSettingsModel } from '@syncfusion/ej2-react-splitbuttons';

const spinSettings: SpinSettingsModel = { position: 'Center' };
const animationSettings: AnimationSettingsModel = {
  effect: 'SlideLeft',
  duration: 500,
  easing: 'linear'
};

<ProgressButtonComponent
  content="Slide Left"
  enableProgress={true}
  spinSettings={spinSettings}
  animationSettings={animationSettings}
/>
```

#### Start / stop programmatic control

```tsx
let progressBtn: ProgressButtonComponent;

<ProgressButtonComponent
  content="Download"
  enableProgress={true}
  duration={4000}
  cssClass="e-hide-spinner"
  ref={(scope) => { progressBtn = scope as ProgressButtonComponent; }}
/>

// Pause:  progressBtn.stop();
// Resume: progressBtn.start();
// Finish: progressBtn.progressComplete();
```

#### Lifecycle events

```tsx
<ProgressButtonComponent
  content="Progress"
  enableProgress={true}
  begin={(args) => console.log('started', args.percent)}
  progress={(args) => console.log('progress', args.percent)}
  end={(args) => console.log('done', args.percent)}
  fail={(args) => console.log('failed', args)}
/>
```

---

### Reference Files

| File | Contents |
|---|---|
| [`references/getting-started.md`](references/progressbutton-getting-started.md) | Installation, CSS imports, first component |
| [`references/spinner-and-progress.md`](references/progressbutton-spinner-and-progress.md) | Spinner config, animation, step, dynamic %, start/stop |
| [`references/style-and-appearance.md`](references/progressbutton-style-and-appearance.md) | CSS class table, theming |
| [`references/accessibility.md`](references/progressbutton-accessibility.md) | ARIA, keyboard nav, compliance matrix |
| [`references/how-to-enable-progress-in-button.md`](references/progressbutton-how-to-enable-progress-in-button.md) | `enableProgress` how-to |
| [`references/how-to-hide-spinner.md`](references/progressbutton-how-to-hide-spinner.md) | `e-hide-spinner` how-to |
| [`references/how-to-customize-progress-using-cssclass.md`](references/progressbutton-how-to-customize-progress-using-cssclass.md) | Vertical / top / reverse fill |
| [`references/how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md`](references/progressbutton-how-to-change-text-content-and-styles-of-the-progressbutton-during-progress.md) | Dynamic text/style during progress |
| [`references/how-to-trace-events-of-progress-button.md`](references/progressbutton-how-to-trace-events-of-progress-button.md) | Event tracing example |
| [`references/api.md`](references/progressbutton-api.md) | Full API: props, events, methods, types |

## Switch

The Syncfusion `SwitchComponent` is a graphical toggle control that switches between checked (on) and unchecked (off) states. It is part of the `@syncfusion/ej2-react-buttons` package and supports text labels, size variants, disabled state, form submission, RTL, programmatic control, and full CSS customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/switch-getting-started.md)
- Package installation and npm setup
- CSS theme imports
- Basic `SwitchComponent` rendering
- Checked state initialization
- Running the application

#### Features and Configuration
📄 **Read:** [references/features.md](references/switch-features.md)
- `onLabel` / `offLabel` text labels
- `disabled` property
- `name` and `value` for form submission
- `cssClass` for custom styling
- `enableRtl` for right-to-left support
- `enablePersistence` to persist state across reloads
- `htmlAttributes` for additional HTML attributes
- `locale` for localization

#### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/switch-events-and-methods.md)
- `change` event and `ChangeEventArgs`
- `beforeChange` event to cancel state transitions
- `created` lifecycle event
- `toggle()` method for programmatic state control
- `click()`, `focusIn()`, and `destroy()` methods
- Using `ref` to call methods imperatively

#### How-To Recipes
📄 **Read:** [references/how-to.md](references/switch-how-to.md)
- Change switch size (small vs default)
- Prevent state change using `beforeChange`
- Set text labels (ON/OFF)
- Enable ripple on label click
- Enable RTL layout
- Set disabled state
- Submit name and value in a form
- Programmatic toggle via `toggle()` method

#### Style and Appearance
📄 **Read:** [references/style-and-appearance.md](references/switch-style-and-appearance.md)
- CSS class reference table
- Customizing bar and handle shape
- Customizing switch colors
- Small size variant
- Using Theme Studio

#### API Reference
📄 **Read:** [references/api.md](references/switch-api.md)
- All properties with types and defaults
- All methods with return types
- All events with argument interfaces
- `ChangeEventArgs` and `BeforeChangeEventArgs`

### Quick Start

```tsx
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';

enableRipple(true);

function App() {
  return <SwitchComponent checked={true} />;
}
export default App;
```

Install the package first:
```bash
npm install @syncfusion/ej2-react-buttons --save
```

### Common Patterns

#### Switch with ON/OFF text labels
```tsx
<SwitchComponent onLabel="ON" offLabel="OFF" checked={true} />
```
> Note: Text labels are not supported in Material themes.

#### Handle state changes
```tsx
import { ChangeEventArgs, SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  function onChange(args: ChangeEventArgs) {
    console.log('Switch is now:', args.checked);
  }
  return <SwitchComponent change={onChange} />;
}
```

#### Disabled switch
```tsx
<SwitchComponent disabled={true} />
```

#### Small size switch
```tsx
<SwitchComponent cssClass="e-small" />
```

#### Programmatic toggle
```tsx
import { useRef } from 'react';
import { SwitchComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const switchRef = useRef<SwitchComponent>(null);

  function handleToggle() {
    switchRef.current?.toggle();
  }

  return (
    <>
      <SwitchComponent ref={switchRef} checked={false} />
      <button onClick={handleToggle}>Toggle</button>
    </>
  );
}
```

#### Form submission with name and value
```tsx
<SwitchComponent name="wifi" value="enabled" checked={true} />
```

### Key Props at a Glance

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `checked` | boolean | false | Initial checked state |
| `disabled` | boolean | false | Disables user interaction |
| `cssClass` | string | '' | Custom CSS class (use `e-small` for small size) |
| `onLabel` | string | '' | Label when checked |
| `offLabel` | string | '' | Label when unchecked |
| `name` | string | '' | Form field name |
| `value` | string | '' | Form field value |
| `enableRtl` | boolean | false | Right-to-left layout |
| `enablePersistence` | boolean | false | Persist state on reload |

## SplitButton

A comprehensive skill for implementing the SplitButton component in React applications. The SplitButton combines a primary action button with a dropdown menu for secondary actions.

### Components Covered
A button that displays a primary action and a dropdown menu of secondary actions.

**Common Use Cases:**
- **Save variants:** Save, Save As, Save All
- **Send variants:** Send, Schedule Send, Send All
- **Download variants:** Download, Download All, Export
- **Share options:** Share, Share Link, Share Email
- **Print options:** Print, Print Preview, Print Settings

### Documentation

#### Getting Started
📄 **Read:** [references/getting-started.md](references/splitbutton-getting-started.md)
- Installation and package setup
- Basic SplitButton implementation
- CSS imports and themes
- First working example
- Module setup (standalone and module-based)

#### Types and Styles
📄 **Read:** [references/types-and-styles.md](references/splitbutton-types-and-styles.md)
- Button styles (primary, success, info, warning, danger, link)
- Button types (flat, outline, round)
- Icon positioning (left, right, top, bottom)
- Size variations (small, medium, large)
- Styled anchor elements
- RTL support

#### SplitButton Features
📄 **Read:** [references/splitbutton-features.md](references/splitbutton-features.md)
- Dropdown menu items
- Icon and text combinations
- Disabled state
- Event handling (click, select, before open)
- Dynamic item manipulation
- Keyboard navigation
- Tooltips and titles

#### API Reference
📄 **Read:** [references/api-reference.md](references/splitbutton-api-reference.md)
- Complete properties documentation
- Methods and their usage
- Event handlers and callbacks
- Model interfaces
- Type definitions
- Quick reference tables

#### Customization
📄 **Read:** [references/customization.md](references/splitbutton-customization.md)
- Custom CSS classes
- Theming and color schemes
- Custom icons and fonts
- Custom templates for items
- Responsive design
- Animation and transitions
- Item separators and grouping

#### Accessibility
📄 **Read:** [references/accessibility.md](references/splitbutton-accessibility.md)
- WCAG 2.1 compliance
- Keyboard navigation patterns
- ARIA attributes
- Screen reader support
- Focus management
- Accessible labels and descriptions

### Quick Start

#### Basic SplitButton

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material.css';

function App() {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  const handleClick = (args) => {
    console.log('Primary action clicked');
  };

  const handleSelect = (args) => {
    console.log('Menu item selected:', args.item.text);
  };

  return (
    <SplitButtonComponent
      items={items}
      onClick={handleClick}
      select={handleSelect}
    >
      Save
    </SplitButtonComponent>
  );
}

export default App;
```

#### SplitButton with Icons

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import '@syncfusion/ej2-react-splitbuttons/styles/material.css';

function SaveButton() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      iconCss="e-icons e-save"
      cssClass="e-primary"
    >
      Save
    </SplitButtonComponent>
  );
}

export default SaveButton;
```

#### SplitButton with Event Handling

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function EventHandlingExample() {
  const [lastAction, setLastAction] = useState('');

  const items = [
    { text: 'Send Now' },
    { text: 'Schedule Send' },
    { text: 'Send Test' }
  ];

  const handlePrimaryClick = () => {
    setLastAction('Primary action: Send Now');
    console.log('Email sent immediately');
  };

  const handleMenuSelect = (args) => {
    setLastAction(`Menu selected: ${args.item.text}`);
    console.log('Selected:', args.item.text);
  };

  const handleBeforeOpen = (args) => {
    console.log('Dropdown menu opening');
  };

  return (
    <div>
      <SplitButtonComponent
        items={items}
        onClick={handlePrimaryClick}
        select={handleMenuSelect}
        beforeOpen={handleBeforeOpen}
        cssClass="e-primary"
      >
        Send
      </SplitButtonComponent>
      <p>{lastAction}</p>
    </div>
  );
}

export default EventHandlingExample;
```

#### SplitButton with Dynamic Items

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef, useState } from 'react';

function DynamicItemsExample() {
  const [items, setItems] = useState([
    { text: 'Option 1' },
    { text: 'Option 2' }
  ]);

  const splitBtnRef = useRef(null);

  const addItem = () => {
    const newItem = { text: `Option ${items.length + 1}` };
    setItems([...items, newItem]);
  };

  const removeItem = () => {
    if (items.length > 1) {
      setItems(items.slice(0, -1));
    }
  };

  return (
    <div>
      <SplitButtonComponent
        ref={splitBtnRef}
        items={items}
        cssClass="e-primary"
      >
        Action
      </SplitButtonComponent>
      <div style={{ marginTop: '20px' }}>
        <button onClick={addItem}>Add Item</button>
        <button onClick={removeItem} style={{ marginLeft: '10px' }}>
          Remove Item
        </button>
      </div>
    </div>
  );
}

export default DynamicItemsExample;
```

#### SplitButton with Custom Template

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function CustomTemplateExample() {
  const items = [
    { text: 'Bold', icon: 'B' },
    { text: 'Italic', icon: 'I' },
    { text: 'Underline', icon: 'U' }
  ];

  const itemTemplate = (props) => {
    return (
      <div style={{ display: 'flex', alignItems: 'center', padding: '8px' }}>
        <span style={{ 
          fontWeight: props.icon === 'B' ? 'bold' : 'normal',
          fontStyle: props.icon === 'I' ? 'italic' : 'normal',
          textDecoration: props.icon === 'U' ? 'underline' : 'none',
          marginRight: '8px'
        }}>
          {props.icon}
        </span>
        <span>{props.text}</span>
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
    >
      Format Text
    </SplitButtonComponent>
  );
}

export default CustomTemplateExample;
```

### Common Patterns

#### Save Variant Pattern

```tsx
const items = [
  { text: 'Save', iconCss: 'e-icons e-save' },
  { separator: true },
  { text: 'Save As', iconCss: 'e-icons e-save-as' },
  { text: 'Save All', iconCss: 'e-icons e-save-all' }
];
```

#### Download Pattern

```tsx
const items = [
  { text: 'Download PDF' },
  { text: 'Download Excel' },
  { text: 'Download CSV' },
  { separator: true },
  { text: 'Download All' }
];
```

#### Share Pattern

```tsx
const items = [
  { text: 'Share Link', iconCss: 'e-icons e-link' },
  { text: 'Email', iconCss: 'e-icons e-mail' },
  { text: 'Print', iconCss: 'e-icons e-print' },
  { text: 'Export', iconCss: 'e-icons e-export' }
];
```

#### State Management Pattern

```tsx
const [isLoading, setIsLoading] = useState(false);

const handleAction = async (args) => {
  setIsLoading(true);
  try {
    // Perform action
    await performAction(args.item.text);
  } finally {
    setIsLoading(false);
  }
};
```

### Key Properties Overview

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `items` | `ItemModel[]` | `[]` | Dropdown menu items |
| `cssClass` | `string` | `''` | CSS classes for styling |
| `iconCss` | `string` | `''` | Icon CSS for primary button |
| `iconPosition` | `string` | `'Left'` | Icon position (Left, Right, Top, Bottom) |
| `disabled` | `boolean` | `false` | Disable the button |
| `enableRtl` | `boolean` | `false` | Enable RTL mode |
| `created` | `function` | - | Event on component creation |
| `click` | `function` | - | Primary button click handler |
| `select` | `function` | - | Menu item selection handler |
| `beforeOpen` | `function` | - | Before dropdown opens |
| `beforeClose` | `function` | - | Before dropdown closes |
| `open` | `function` | - | After dropdown opens |
| `close` | `function` | - | After dropdown closes |

### Next Steps

1. **Installation & Setup** → Read [getting-started.md](references/splitbutton-getting-started.md)
2. **Styling Options** → Read [types-and-styles.md](references/splitbutton-types-and-styles.md)
3. **Features** → Read [splitbutton-features.md](references/splitbutton-features.md)
4. **Complete API** → Read [api-reference.md](references/splitbutton-api-reference.md)
5. **Advanced Customization** → Read [customization.md](references/splitbutton-customization.md)
6. **Accessibility** → Read [accessibility.md](references/splitbutton-accessibility.md)

### Troubleshooting Quick Links

- **Items not showing?** → Check [references/getting-started.md#css-imports](references/splitbutton-getting-started.md)
- **Events not firing?** → Check [references/splitbutton-features.md#event-handling](references/splitbutton-features.md)
- **Styling issues?** → Check [references/types-and-styles.md](references/splitbutton-types-and-styles.md)
- **Accessibility concerns?** → Check [references/accessibility.md](references/splitbutton-accessibility.md)

### Resources

- **Official Documentation:** [Syncfusion React SplitButton](https://ej2.syncfusion.com/react/documentation/split-button)
- **API Reference:** [Syncfusion SplitButton API](https://ej2.syncfusion.com/react/documentation/api/split-button/)
- **Live Demos:** [Syncfusion React Demos](https://ej2.syncfusion.com/home/react.html)

## RadioButton

A skill for implementing the Syncfusion React `RadioButtonComponent` — a graphical UI element that lets users select exactly one option from a group. Supports checked/unchecked states, label positioning, small size, form integration, RTL, disabled state, and full CSS customization.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/radiobutton-getting-started.md)
- Package installation and CSS import
- Basic `RadioButtonComponent` rendering
- Grouping radio buttons with `name` prop
- Quick Vite + React project setup
- Enabling ripple effect

#### Label and Size
📄 **Read:** [references/label-and-size.md](references/radiobutton-label-and-size.md)
- Adding captions with the `label` property
- Positioning labels before/after with `labelPosition`
- Applying small size with `cssClass="e-small"`
- Default vs. compact size variants

#### Features and State
📄 **Read:** [references/features-and-state.md](references/radiobutton-features-and-state.md)
- Setting checked/unchecked state with `checked`
- Disabling a RadioButton with `disabled`
- Grouping and form submission with `name` and `value`
- RTL layout with `enableRtl`
- Handling state change via the `change` event
- Listening to component lifecycle with `created`

#### Style and Appearance
📄 **Read:** [references/style-and-appearance.md](references/radiobutton-style-and-appearance.md)
- Overriding default CSS classes
- Creating semantic color variants (primary, success, warning, etc.)
- Using `cssClass` for custom styles
- Theme Studio integration for global theming
- CSS class reference table

#### Accessibility
📄 **Read:** [references/accessibility.md](references/radiobutton-accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (`role`, `aria-checked`, `aria-disabled`)
- Keyboard navigation shortcuts
- Screen reader support

#### API Reference
📄 **Read:** [references/api.md](references/radiobutton-api.md)
- All properties: `checked`, `disabled`, `label`, `labelPosition`, `name`, `value`, `cssClass`, `enableRtl`, `enablePersistence`, `enableHtmlSanitizer`, `htmlAttributes`, `locale`
- Methods: `click()`, `destroy()`, `focusIn()`, `getSelectedValue()`
- Events: `change` (ChangeArgs), `created`

### Quick Start

```tsx
import { enableRipple } from '@syncfusion/ej2-base';
import { RadioButtonComponent } from '@syncfusion/ej2-react-buttons';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-buttons/styles/tailwind3.css';

enableRipple(true);

function App() {
  return (
    <ul>
      <li><RadioButtonComponent label="Option 1" name="group1" checked={true} /></li>
      <li><RadioButtonComponent label="Option 2" name="group1" /></li>
      <li><RadioButtonComponent label="Option 3" name="group1" /></li>
    </ul>
  );
}
export default App;
```

### Common Patterns

#### Controlled state with change handler
```tsx
import { RadioButtonComponent, ChangeArgs } from '@syncfusion/ej2-react-buttons';
import { useState } from 'react';

function App() {
  const [selected, setSelected] = useState('monthly');

  const handleChange = (args: ChangeArgs) => {
    setSelected(args.value);
  };

  return (
    <ul>
      <li>
        <RadioButtonComponent
          label="Monthly"
          name="plan"
          value="monthly"
          checked={selected === 'monthly'}
          change={handleChange}
        />
      </li>
      <li>
        <RadioButtonComponent
          label="Yearly"
          name="plan"
          value="yearly"
          checked={selected === 'yearly'}
          change={handleChange}
        />
      </li>
    </ul>
  );
}
```

#### Form submission with name/value
```tsx
<form>
  <RadioButtonComponent name="payment" value="card"    label="Credit Card" checked={true} />
  <RadioButtonComponent name="payment" value="bank"    label="Net Banking" />
  <RadioButtonComponent name="payment" value="cod"     label="Cash on Delivery" />
  <button type="submit">Submit</button>
</form>
```

#### Disabled option in a group
```tsx
<RadioButtonComponent label="Available"   name="seat" />
<RadioButtonComponent label="Unavailable" name="seat" disabled={true} />
```

#### Small compact size
```tsx
<RadioButtonComponent label="Compact" name="size" cssClass="e-small" />
```

#### RTL support
```tsx
<RadioButtonComponent label="خيار 1" name="rtl" enableRtl={true} />
```

### Key Props Summary

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `label` | string | `''` | Caption displayed next to the button |
| `name` | string | `''` | Groups buttons as mutually exclusive |
| `value` | string | `''` | Form value submitted when checked |
| `checked` | boolean | `false` | Sets checked state |
| `disabled` | boolean | `false` | Prevents user interaction |
| `labelPosition` | `'Before'` \| `'After'` | `'After'` | Label placement |
| `cssClass` | string | `''` | Custom CSS class(es) |
| `enableRtl` | boolean | `false` | Right-to-left layout |
| `enablePersistence` | boolean | `false` | Persists state across page reloads |

### Decision Guide

- **User picks one of many options** → Use `name` to group + `value` for each option
- **Pre-select a default** → Set `checked={true}` on the desired option
- **Read which option is selected** → Use `change` event (`args.value`) or call `getSelectedValue()`
- **Prevent selection of an option** → Use `disabled={true}`
- **Dense UI layout** → Add `cssClass="e-small"`
- **RTL language UI** → Use `enableRtl={true}`
- **Custom color/branding** → Use `cssClass` with custom CSS rules (see style-and-appearance.md)

## Chips

The Syncfusion React Chips (`ChipListComponent`) component renders compact, interactive elements representing inputs, attributes, or actions. It supports single/multiple selection, deletion, drag-and-drop, avatars, icons, templates, and rich styling.

### Navigation Guide

#### Getting Started
📄 **Read:** [references/getting-started.md](references/chips-getting-started.md)
- Installation and package setup (`@syncfusion/ej2-react-buttons`)
- CSS/theme imports
- Rendering a basic chip or chip list
- Single chip vs. chip list with `ChipsDirective` / `ChipDirective`
- Running the application

#### Types and Selection
📄 **Read:** [references/types-and-selection.md](references/chips-types-and-selection.md)
- Four chip types: Input, Choice, Filter, Action
- Single selection (`selection="Single"`) — choice chips
- Multiple selection (`selection="Multiple"`) — filter chips
- Deletable chips (`enableDelete`)
- Pre-selecting chips with `selectedChips`
- Click events (`onClick`) for action chips

#### Customization
📄 **Read:** [references/customization.md](references/chips-customization.md)
- Predefined styles: `e-primary`, `e-success`, `e-info`, `e-warning`, `e-danger`
- Leading icon (`leadingIconCss`, `leadingIconUrl`)
- Avatar image (`avatarIconCss`) and avatar text (`avatarText`)
- Trailing icon (`trailingIconCss`, `trailingIconUrl`)
- Outline chip (`cssClass="e-outline"`)
- Custom chip template (`template` prop)
- `htmlAttributes` for custom HTML attributes

#### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/chips-drag-and-drop.md)
- Enabling drag and drop (`allowDragAndDrop`)
- Restricting drag area (`dragArea`)
- Drag events: `dragStart`, `dragging`, `dragStop`
- Cross-container drag and drop

#### Style Customization
📄 **Read:** [references/style.md](references/chips-style.md)
- CSS overrides for chip text, icon, delete button
- Outline chip border styling
- Selected chip background and color
- Avatar text background styling
- Chip height/size customization

#### Accessibility
📄 **Read:** [references/accessibility.md](references/chips-accessibility.md)
- WCAG 2.2, Section 508, ADA compliance
- WAI-ARIA attributes (`role`, `aria-selected`, `aria-disabled`, etc.)
- Keyboard navigation shortcuts
- RTL support, screen reader support

#### API Reference
📄 **Read:** [references/api.md](references/chips-api.md)
- All properties: `text`, `chips`, `selection`, `enableDelete`, `cssClass`, `selectedChips`, `enabled`, `enableRtl`, `enablePersistence`, `allowDragAndDrop`, `dragArea`, `htmlAttributes`, `leadingIconCss`, `leadingIconUrl`, `avatarIconCss`, `avatarText`, `trailingIconCss`, `trailingIconUrl`
- Methods: `add()`, `remove()`, `find()`, `getSelectedChips()`, `select()`, `destroy()`
- Events: `click`, `beforeClick`, `created`, `delete`, `deleted`, `dragStart`, `dragging`, `dragStop`

### Quick Start

```tsx
import { ChipListComponent, ChipsDirective, ChipDirective } from '@syncfusion/ej2-react-buttons';
import { enableRipple } from '@syncfusion/ej2-base';
import * as React from 'react';
import './App.css';

enableRipple(true);

function App() {
  return (
    <ChipListComponent id="chip-list">
      <ChipsDirective>
        <ChipDirective text="Angular" />
        <ChipDirective text="React" />
        <ChipDirective text="Vue" />
      </ChipsDirective>
    </ChipListComponent>
  );
}
export default App;
```

CSS (App.css):
```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css';
```

### Common Patterns

#### Filter chips (multi-select)
```tsx
<ChipListComponent selection="Multiple">
  <ChipsDirective>
    <ChipDirective text="React" />
    <ChipDirective text="Angular" />
    <ChipDirective text="Vue" />
  </ChipsDirective>
</ChipListComponent>
```

#### Deletable chips with event
```tsx
<ChipListComponent enableDelete={true} delete={(e) => console.log('Deleting:', e.text)}>
  <ChipsDirective>
    <ChipDirective text="Tag One" />
    <ChipDirective text="Tag Two" />
  </ChipsDirective>
</ChipListComponent>
```

#### Chips with avatar initials
```tsx
<ChipListComponent>
  <ChipsDirective>
    <ChipDirective text="Andrew" avatarText="A" />
    <ChipDirective text="Laura" avatarText="L" />
  </ChipsDirective>
</ChipListComponent>
```

#### Programmatic control (add/remove chips via ref)
```tsx
const chipRef = React.useRef<ChipListComponent>(null);

// Add a chip
chipRef.current?.add('New Tag');

// Remove chip at index 0
chipRef.current?.remove([0]);

// Get selected
const selected = chipRef.current?.getSelectedChips();
```
