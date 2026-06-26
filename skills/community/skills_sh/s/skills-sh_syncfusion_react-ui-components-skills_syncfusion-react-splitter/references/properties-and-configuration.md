# Splitter Properties and Configuration

## Table of Contents
- [Splitter Component Properties](#splitter-component-properties)
- [Pane Properties](#pane-properties)
- [Common Configuration Patterns](#common-configuration-patterns)

## Splitter Component Properties

The `SplitterComponent` provides configuration options to customize the layout, behavior, and appearance of the splitter.

### orientation

**Type:** `'Horizontal' | 'Vertical'`

**Description:** Specifies the layout direction of the panes. Use "Horizontal" for left-to-right layout and "Vertical" for top-to-bottom layout.

**Example:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  return (
    <SplitterComponent id="splitter" height="250px" width="600px" orientation="Horizontal">
      <PanesDirective>
        <PaneDirective />
        <PaneDirective />
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:** Set orientation when initializing the splitter to control the pane arrangement.

---

### height and width

**Type:** `string`

**Description:** Specifies the height and width of the Splitter component. Accepts both pixel and percentage values.

**Example:**

```tsx
<SplitterComponent height="400px" width="100%">
  <PanesDirective>
    <PaneDirective size='200px' />
    <PaneDirective size='200px' />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Always set explicit height for vertical splitters to ensure proper rendering.

---

### separatorSize

**Type:** `number`

**Description:** Specifies the size (in pixels) of the separator bar between panes.

**Example:**

```tsx
<SplitterComponent height="250px" width="600px" separatorSize={4}>
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**Default:** 4 pixels  
**When to Use:** Customize for better visual separation or to match design specifications.

---

### cssClass

**Type:** `string`

**Description:** Specifies one or more CSS class names to customize the Splitter styling.

**Example:**

```tsx
<SplitterComponent cssClass="custom-splitter dark-theme" height="250px" width="600px">
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Apply custom CSS classes for theme switching and styling customization.

---

### enableRtl

**Type:** `boolean`

**Description:** Enables right-to-left rendering for RTL languages (Arabic, Hebrew, etc.).

**Example:**

```tsx
<SplitterComponent enableRtl={true} height="250px" width="600px">
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Enable RTL for applications supporting RTL languages.

---

### enableReversePanes

**Type:** `boolean`

**Description:** Reverses the order of panes in the DOM without reversing the visual order. Useful for accessibility and flexible layouts.

**Example:**

```tsx
<SplitterComponent enableReversePanes={true} height="250px" width="600px">
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Reorder panes for different screen layouts or accessibility requirements.

---

### enabled

**Type:** `boolean`

**Description:** Enables or disables the Splitter component. When disabled, users cannot interact with the component.

**Default:** `true`

**Example:**

```tsx
<SplitterComponent enabled={false} height="250px" width="600px">
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Disable the splitter during data loading or validation states.

---

### enablePersistence

**Type:** `boolean`

**Description:** Enables persistence of the Splitter state (pane sizes, collapsed states) between page reloads using browser storage.

**Default:** `false`

**Example:**

```tsx
<SplitterComponent enablePersistence={true} height="250px" width="600px" id="splitter-persistence">
  <PanesDirective>
    <PaneDirective size='250px' collapsible={true} />
    <PaneDirective size='250px' collapsible={true} />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Persist user layout preferences across browser sessions.

**Note:** Component must have an `id` attribute for persistence to work.

---

### enableHtmlSanitizer

**Type:** `boolean`

**Description:** Defines whether to allow HTML content sanitization. When enabled, prevents cross-site scripting (XSS) attacks by sanitizing HTML content in panes.

**Default:** `true`

**Example:**

```tsx
<SplitterComponent enableHtmlSanitizer={true} height="250px" width="600px">
  <PanesDirective>
    <PaneDirective content="<div>Safe HTML Content</div>" />
    <PaneDirective content="<p>More content</p>" />
  </PanesDirective>
</SplitterComponent>
```

**When to Use:** Always keep enabled for security. Disable only when you control all content sources.

**Security Note:** XSS attacks can compromise your application. Only disable sanitization for trusted content sources.

---

### locale

**Type:** `string`

**Description:** Overrides the global culture and localization for the Splitter component.

**Example:**

```tsx
<SplitterComponent locale="fr-FR" height="250px" width="600px">
  <PanesDirective>
    <PaneDirective size='250px' />
    <PaneDirective size='250px' />
  </PanesDirective>
</SplitterComponent>
```

**Default:** `'en-US'`  
**When to Use:** Set locale for localized components and text.

---

### paneSettings

**Type:** `PanePropertiesModel[]`

**Description:** Specifies an array of pane properties for programmatic pane configuration. This is an alternative to using `<PaneDirective>` elements, useful when panes are generated dynamically or configured from data structures.

**Example - Array-Based Configuration:**

```tsx
import { SplitterComponent, PanesDirective, PaneDirective } from '@syncfusion/ej2-react-layouts';
import { PanePropertiesModel } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  const paneSettings: PanePropertiesModel[] = [
    {
      size: '200px',
      min: '100px',
      max: '300px',
      content: 'Pane 1',
      collapsible: true,
      resizable: true
    },
    {
      size: '250px',
      min: '150px',
      max: '400px',
      content: 'Pane 2',
      collapsible: true,
      resizable: true
    },
    {
      size: 'auto',
      min: '200px',
      content: 'Pane 3',
      resizable: true
    }
  ];

  return (
    <SplitterComponent height="400px" width="100%" paneSettings={paneSettings}>
      <PanesDirective>
        {paneSettings.map((pane, index) => (
          <PaneDirective key={index} {...pane} />
        ))}
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**Example - Dynamic Configuration from API:**

```tsx
const [paneSettings, setPaneSettings] = React.useState<PanePropertiesModel[]>([]);

React.useEffect(() => {
  // Fetch pane configuration from API
  fetchPaneConfig().then(config => {
    setPaneSettings(config);
  });
}, []);

return (
  <SplitterComponent height="400px" width="100%" paneSettings={paneSettings}>
    <PanesDirective>
      {paneSettings.map((pane, index) => (
        <PaneDirective key={index} {...pane} />
      ))}
    </PanesDirective>
  </SplitterComponent>
);
```

**When to Use:**
- When panes are generated dynamically from data
- Loading pane configuration from an API or database
- Programmatic layout configuration
- Data-driven UI patterns

**Note:** `paneSettings` array elements follow the same structure as `PanePropertiesModel` (size, min, max, collapsed, collapsible, resizable, content, cssClass).

---

## Pane Properties

Each pane in the Splitter is configured using `PaneDirective` with the following properties:

### size

**Type:** `string`

**Description:** Specifies the size of the pane using pixels (e.g., "200px") or percentage (e.g., "50%").

**Example:**

```tsx
<PanesDirective>
  <PaneDirective size='250px'>
    <div>Fixed 250px pane</div>
  </PaneDirective>
  <PaneDirective size='50%'>
    <div>50% width pane</div>
  </PaneDirective>
</PanesDirective>
```

**When to Use:** Always specify size for all panes or use percentages for responsive layouts.

---

### min and max

**Type:** `string`

**Description:** Set minimum and maximum size constraints for resizable panes. Prevents panes from becoming too small or too large.

**Example:**

```tsx
<PanesDirective>
  <PaneDirective size='200px' min='100px' max='400px'>
    <div>Constrained pane (100px - 400px)</div>
  </PaneDirective>
</PanesDirective>
```

**When to Use:** Always set min/max for resizable panes to prevent layout issues.

---

### collapsed

**Type:** `boolean`

**Description:** Sets the initial collapsed state of the pane. When true, the pane is hidden at component initialization.

**Default:** `false`

**Example:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  return (
    <SplitterComponent height="250px" width="600px">
      <PanesDirective>
        <PaneDirective collapsed={false}>
          <div>Visible pane</div>
        </PaneDirective>
        <PaneDirective collapsed={true}>
          <div>Hidden pane (start collapsed)</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:** Hide secondary panes to save space on initial load.

---

### collapsible

**Type:** `boolean`

**Description:** Allows users to collapse/expand the pane by clicking the gripper icon on the separator.

**Default:** `false`

**Example:**

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from "react";

function App() {
  return (
    <SplitterComponent height="250px" width="600px">
      <PanesDirective>
        <PaneDirective collapsible={true}>
          <div>Collapsible pane 1</div>
        </PaneDirective>
        <PaneDirective collapsible={true}>
          <div>Collapsible pane 2</div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default App;
```

**When to Use:** Enable collapsing for optional content areas and secondary panels.

---

### resizable

**Type:** `boolean`

**Description:** Controls whether users can manually resize the pane using the separator.

**Default:** `true`

**Example:**

```tsx
<PanesDirective>
  <PaneDirective size='200px' resizable={true}>
    <div>Resizable pane</div>
  </PaneDirective>
  <PaneDirective size='200px' resizable={false}>
    <div>Fixed-size pane (cannot resize)</div>
  </PaneDirective>
</PanesDirective>
```

**When to Use:** Set `resizable={false}` for navigation panes that should maintain fixed width.

---

### content

**Type:** `string | HTMLElement | JSX.Element`

**Description:** Specifies the content of the pane as plain text, HTML markup, or a React component.

**Example - Text Content:**

```tsx
<PaneDirective content="Simple text content" />
```

**Example - HTML Content:**

```tsx
<PaneDirective content="<div><h3>Title</h3><p>Content here</p></div>" />
```

**Example - React Component:**

```tsx
const MyComponent = () => <div><h3>React Component</h3></div>;

<PaneDirective content={MyComponent} />
```

**When to Use:** Use inline JSX for dynamic content, HTML for static markup, and text for simple labels.

---

### cssClass

**Type:** `string`

**Description:** Applies custom CSS classes to the individual pane for styling customization.

**Example:**

```tsx
<PanesDirective>
  <PaneDirective cssClass="sidebar-pane custom-styling">
    <div>Styled pane</div>
  </PaneDirective>
  <PaneDirective cssClass="main-content">
    <div>Main area</div>
  </PaneDirective>
</PanesDirective>
```

**When to Use:** Apply different styles to different panes for visual distinction.

---

## Common Configuration Patterns

### Basic Two-Pane Layout

```tsx
<SplitterComponent height="400px" width="100%" orientation="Horizontal">
  <PanesDirective>
    <PaneDirective size='250px'>
      <div>Left panel</div>
    </PaneDirective>
    <PaneDirective size='auto'>
      <div>Main content (takes remaining space)</div>
    </PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Three-Pane Dashboard Layout

```tsx
<SplitterComponent height="500px" width="100%" orientation="Horizontal">
  <PanesDirective>
    <PaneDirective size='20%'>
      <div>Sidebar</div>
    </PaneDirective>
    <PaneDirective size='60%' min='40%' max='80%'>
      <div>Main content</div>
    </PaneDirective>
    <PaneDirective size='20%'>
      <div>Details panel</div>
    </PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Collapsible Navigation + Resizable Content

```tsx
<SplitterComponent height="400px" width="100%">
  <PanesDirective>
    <PaneDirective size='250px' collapsible={true} resizable={true}>
      <div>Navigation (collapsible)</div>
    </PaneDirective>
    <PaneDirective size='auto' resizable={true} min='200px'>
      <div>Content (resizable)</div>
    </PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### Responsive Vertical Layout

```tsx
<SplitterComponent height="600px" width="100%" orientation="Vertical">
  <PanesDirective>
    <PaneDirective size='70%'>
      <div>Editor area</div>
    </PaneDirective>
    <PaneDirective size='30%' min='20%' max='50%'>
      <div>Output/Console</div>
    </PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

---

## Property Quick Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `orientation` | string | 'Horizontal' | Pane layout direction |
| `height` | string | '100%' | Component height |
| `width` | string | '100%' | Component width |
| `separatorSize` | number | 4 | Separator thickness |
| `enabled` | boolean | true | Enable/disable component |
| `enableRtl` | boolean | false | RTL language support |
| `enablePersistence` | boolean | false | Save state between reloads |
| `enableHtmlSanitizer` | boolean | true | XSS protection |
| `locale` | string | 'en-US' | Localization |
| `cssClass` | string | '' | Custom CSS classes |
| `enableReversePanes` | boolean | false | Reverse pane order |
| **Pane Properties** | | | |
| `size` | string | 'auto' | Pane size (px or %) |
| `min` | string | '0' | Minimum pane size |
| `max` | string | undefined | Maximum pane size |
| `collapsed` | boolean | false | Initial collapsed state |
| `collapsible` | boolean | false | Allow user collapse |
| `resizable` | boolean | true | Allow user resize |
| `content` | string/JSX | '' | Pane content |
| `cssClass` | string | '' | Pane CSS classes |

