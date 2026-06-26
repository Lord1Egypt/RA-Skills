---
name: shopify-draggable
description: Implement drag-and-drop interactions with @shopify/draggable. Supports Draggable (basic drag), Sortable (reordering), Droppable (drop zones), Swappable (swapping), Plugins (mirror/snapping/collision/scroll, etc.), Sensors (mouse/touch/force touch). 
metadata:
  openclaw:
    emoji: 🖱️
---

# @shopify/draggable — Drag & Drop Interaction Skill

> Built on Shopify's @shopify/draggable (MIT license, v1.2.1).
> Pure JS library, zero runtime dependencies, supports ES modules and UMD.

## Use cases

sortable lists, droppable panels, custom drag interactions, kanban/grid drag-and-drop reorganization. No longer maintained, now community-maintained.

## Install

```bash
npm install @shopify/draggable
```

Or via CDN (recommended for prototyping):

```html
<script type="module">
import { Draggable, Sortable, Droppable, Swappable } from 'https://cdn.jsdelivr.net/npm/@shopify/draggable/build/esm/index.mjs';
</script>
```

## Module Overview

| Module | Class | Purpose |
|--------|-------|---------|
| Base | `Draggable` | Core drag engine, manages mirror, sensors, and events |
| Sorting | `Sortable` | Reorder on drag, tracks old and new indices |
| Drop Zone | `Droppable` | Drag elements into/out of specific dropzones |
| Swap | `Swappable` | Swap two element positions on drag (no sorting) |

## Quick Start

### Basic Drag

```javascript
import Draggable from '@shopify/draggable';

const draggable = new Draggable(document.querySelectorAll('.container'), {
  draggable: '.draggable-source',
});

draggable.on('drag:start', (event) => {
  console.log('Started dragging:', event.source);
});

draggable.on('drag:stop', () => {
  console.log('Drag ended');
});
```

### Sortable List

```javascript
import Sortable from '@shopify/draggable';

const sortable = new Sortable(document.querySelectorAll('.list'), {
  draggable: '.list-item',
  delay: { mouse: 200, touch: 300 },
});

sortable.on('sortable:stop', (event) => {
  console.log(`Moved from index ${event.oldIndex} to ${event.newIndex}`);
});
```

### Drag into Drop Zone

```javascript
import Droppable from '@shopify/draggable';

const droppable = new Droppable(document.querySelectorAll('.source-container'), {
  draggable: '.card',
  dropzone: '.dropzone',
});

droppable.on('droppable:dropped', (event) => {
  console.log('Dropped into dropzone:', event.dropzone);
});

droppable.on('droppable:returned', (event) => {
  console.log('Returned to original position');
});
```

### Element Swap

```javascript
import Swappable from '@shopify/draggable';

const swappable = new Swappable(document.querySelectorAll('.grid'), {
  draggable: '.grid-item',
});

swappable.on('swappable:swapped', (event) => {
  console.log('Swapped element:', event.swappedElement);
});
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `draggable` | `String` | `'.draggable-source'` | CSS selector for draggable elements |
| `handle` | `String\|null` | `null` | CSS selector for drag handle |
| `delay` | `Object` | `{}` | Delay before drag starts (`{ mouse: ms, touch: ms }`) |
| `distance` | `Number` | `0` | Minimum pixels to move before dragging |
| `placedTimeout` | `Number` | `800` | Delay before removing placed CSS classes (ms) |
| `plugins` | `Array` | `[]` | Additional plugins |
| `sensors` | `Array` | `[]` | Additional sensors |
| `classes` | `Object` | see below | Custom CSS class names |
| `announcements` | `Object` | see below | Accessibility announcements |

### CSS Class Map

```javascript
const defaultClasses = {
  'container:dragging': 'draggable-container--is-dragging',
  'source:dragging':    'draggable-source--is-dragging',
  'source:placed':      'draggable-source--placed',
  'container:placed':   'draggable-container--placed',
  'body:dragging':      'draggable--is-dragging',
  'draggable:over':     'draggable--over',
  'container:over':     'draggable-container--over',
  'source:original':    'draggable--original',
  mirror:               'draggable-mirror',
};
```

Droppable additional classes:

| Identifier | Default Class | Description |
|------------|---------------|-------------|
| `droppable:active` | `draggable-dropzone--active` | Accepting drop zones |
| `droppable:occupied` | `draggable-dropzone--occupied` | Occupied drop zones |

### Excluding Default Plugins/Sensors

```javascript
new Draggable(containers, {
  exclude: {
    plugins: [],     // List of plugin constructors
    sensors: [],     // List of sensor constructors
  },
});
```

## Events API

### Base Events (All Modules)

| Event | Trigger |
|-------|---------|
| `drag:start` | Drag started |
| `drag:move` | Drag moving |
| `drag:over` | Hovering over another draggable element |
| `drag:over:container` | Hovering over another container |
| `drag:out` | Moved out of an element |
| `drag:out:container` | Moved out of a container |
| `drag:stop` | Drag stopped |
| `drag:pressure` | Pressure change (Force Touch) |
| `drag:stopped` | Drag fully ended |

### Common Event Properties

```javascript
draggable.on('drag:start', (event) => {
  event.source;           // Cloned source element
  event.originalSource;   // Original element (display:none)
  event.sourceContainer;  // Source container
  event.sensorEvent;      // Original sensor event
  event.cancel();         // Cancel the drag
});
```

### Sortable Events

| Event | Additional Properties |
|-------|-----------------------|
| `sortable:start` | `startIndex`, `startContainer` |
| `sortable:sort` | `currentIndex`, `source`, `over` |
| `sortable:sorted` | `oldIndex`, `newIndex`, `oldContainer`, `newContainer` |
| `sortable:stop` | `oldIndex`, `newIndex`, `oldContainer`, `newContainer` |

### Droppable Events

| Event | Additional Properties |
|-------|-----------------------|
| `droppable:start` | `dragEvent`, `dropzone` |
| `droppable:dropped` | `dragEvent`, `dropzone` |
| `droppable:returned` | `dragEvent`, `dropzone` |
| `droppable:stop` | `dragEvent`, `dropzone` |

### Swappable Events

| Event | Additional Properties |
|-------|-----------------------|
| `swappable:start` | `dragEvent` |
| `swappable:swap` | `dragEvent`, `over`, `overContainer` |
| `swappable:swapped` | `dragEvent`, `swappedElement` |
| `swappable:stop` | `dragEvent` |

## Plugins

| Plugin | Class | Function |
|--------|-------|----------|
| **Announcement** | `Draggable.Plugins.Announcement` | Live accessibility announcements during drag |
| **Focusable** | `Draggable.Plugins.Focusable` | Keyboard focus management |
| **Mirror** | `Draggable.Plugins.Mirror` | Shows mirror element while dragging (enabled by default) |
| **Scrollable** | `Draggable.Plugins.Scrollable` | Auto-scroll container when dragging near edge |
| **Collidable** | `Plugins.Collidable` | Collision detection (requires separate import) |
| **ResizeMirror** | `Plugins.ResizeMirror` | Auto-resize mirror element |
| **Snappable** | `Plugins.Snappable` | Snap to specific positions |
| **SwapAnimation** | `Plugins.SwapAnimation` | Swap animation |
| **SortAnimation** | `Plugins.SortAnimation` | Sort animation |

### Collidable

```javascript
import { Plugins } from '@shopify/draggable';
import Collidable from '@shopify/draggable/build/esm/Plugins/Collidable';

new Draggable(containers, {
  plugins: [Collidable],
});
```

Collidable events: `collidable:in` (entered collision), `collidable:out` (left collision).

### Snappable

```javascript
import Snappable from '@shopify/draggable/build/esm/Plugins/Snappable';
new Draggable(containers, {
  plugins: [Snappable],
});
```

## Sensors

| Sensor | Description | Default |
|--------|-------------|---------|
| `MouseSensor` | Mouse drag | ✅ |
| `TouchSensor` | Touch drag | ✅ |
| `ForceTouchSensor` | Force Touch pressure | ❌ |
| `DragSensor` | Native HTML5 Drag & Drop | ❌ |

```javascript
import { Draggable } from '@shopify/draggable';
import ForceTouchSensor from '@shopify/draggable/build/esm/Draggable/Sensors/ForceTouchSensor';

new Draggable(containers, {
  sensors: [ForceTouchSensor],
});
```

## Instance Methods

| Method | Description |
|--------|-------------|
| `addPlugin(...plugins)` | Add plugins |
| `removePlugin(...plugins)` | Remove plugins |
| `addSensor(...sensors)` | Add sensors |
| `removeSensor(...sensors)` | Remove sensors |
| `addContainer(...containers)` | Dynamically add containers |
| `removeContainer(...containers)` | Dynamically remove containers |
| `on(type, ...callbacks)` | Bind event listener |
| `off(type, callback)` | Unbind event listener |
| `trigger(event)` | Trigger an event |
| `isDragging()` | Check if currently dragging |
| `getDraggableElements()` | Get all draggable elements |
| `cancel()` | Immediately cancel current drag |
| `destroy()` | Destroy the instance |

## Common Patterns

### Drag with Handle

```javascript
new Sortable(document.querySelectorAll('.list'), {
  draggable: '.list-item',
  handle: '.drag-handle',   // Only .drag-handle can trigger drag
});
```

### Delay & Minimum Distance (Prevent Accidental Drag)

```javascript
new Draggable(containers, {
  delay: { mouse: 100, touch: 200 },
  distance: 5,            // Must move 5px before dragging
});
```

### Cross-Container Sorting

```javascript
const sortable = new Sortable(document.querySelectorAll('.column'), {
  draggable: '.card',
  delay: { touch: 200 },
});
// Cross-container drag is supported automatically
```

### Prevent Specific Drags

```javascript
draggable.on('drag:start', (event) => {
  if (event.source.dataset.draggable === 'false') {
    event.cancel();
  }
});
```

### Custom Mirror Style

```javascript
import Draggable from '@shopify/draggable';

const draggable = new Draggable(containers, {
  classes: {
    mirror: 'my-custom-mirror',
  },
});

// Or customize via CSS
// .draggable-mirror { opacity: 0.7; transform: scale(1.05); }
```

## Lifecycle

```
constructor()
  ↓
draggable:initialized
  ↓
drag:start ──→ drag:move ──→ drag:stop ──→ drag:stopped
  ↓              ↓              ↓
Plugin events  sortable:sorted  sortable:stop
  ↓           droppable:       droppable:stop
cancel()      dropped          swappable:stop
              swappable:
              swapped
  ↓
destroy()
```

## Notes

- Draggable **does not perform sorting by itself** — Sortable, Droppable, and Swappable are its subclasses
- The source element is set to `display: none` during drag; the mirror takes its visual place
- **No longer maintained** by the original Shopify authors; now community-maintained. Evaluate risk for production use
- TypeScript type definitions are bundled — no need to install `@types` separately
- Does not support IE11; targets ES6 modern browsers
- Use jsdelivr for CDN; avoid unpkg (incompatible paths)