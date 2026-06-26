---
title: diagram-settings
description: Configure layers, virtualization, grid lines, rulers, scroll settings, page settings, tooltips, overview panel, localization, and accessibility in the Syncfusion React Diagram component.
---

# Diagram Settings

## Table of Contents

- [Layers](#layers)
- [Virtualization](#virtualization)
- [Grid Lines and Snapping](#grid-lines-and-snapping)
- [Ruler](#ruler)
- [Scroll Settings](#scroll-settings)
- [Page Settings](#page-settings)
- [Tooltip](#tooltip)
- [Overview Panel](#overview-panel)
- [Localization](#localization)
- [Accessibility](#accessibility)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Layers

Layers group diagram elements into named categories for selective visibility, locking, and z-order control. Each layer has `id`, `objects` (array of element IDs), `visible`, `lock`, `zIndex`, and `addInfo` properties.

### Define Layers

```tsx
<DiagramComponent
  layers={[
    { id: 'layer1', objects: ['node1', 'node2'], visible: true, lock: false },
    { id: 'layer2', objects: ['node3', 'connector1'], visible: true, lock: true },
  ]}
/>
```

### Layer Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `id` | string | — | Unique layer identifier |
| `objects` | string[] | `[]` | IDs of nodes/connectors in this layer |
| `visible` | boolean | `true` | Show/hide all elements in layer |
| `lock` | boolean | `false` | Prevent selection and interaction |
| `zIndex` | number | — | Stacking order (higher = in front) |
| `addInfo` | object | — | Custom metadata attached to the layer |

### Runtime Layer Methods

```tsx
// Add a new layer with optional objects
diagramInstance.addLayer({ id: 'newLayer', visible: true, lock: false }, [
  { id: 'con1', type: 'Straight', sourceID: 'node1', targetID: 'node2' }
]);

// Remove a layer by ID
diagramInstance.removeLayer('layer1');

// Move objects from one layer to another
// Parameter 1 - An array of object IDs represented as strings to be moved
// parameter 2 -  The ID of the target layer to which the objects should be moved.
diagramInstance.moveObjects(['node1', 'node2'], 'layer2');

// Clone a layer with all its elements
diagramInstance.cloneLayer('layer1');

// Z-order control
diagramInstance.bringLayerForward('layer1');
diagramInstance.sendLayerBackward('layer1');

// Active layer management
diagramInstance.getActiveLayer();           // Returns current active layer
diagramInstance.setActiveLayer('layer2');   // New objects are added to this layer
```

> The active layer is the layer with the highest z-index. New runtime-added objects are assigned to the active layer automatically.

---

## Virtualization

Enable virtualization for large diagrams (100+ nodes/connectors) to render only visible elements, significantly improving performance.

```tsx
import { DiagramComponent, DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  constraints={DiagramConstraints.Default | DiagramConstraints.Virtualization}
/>
```

Virtualization provides:
- Reduced memory usage (only visible objects loaded)
- Faster initial rendering
- Smooth scrolling and panning
- Consistent performance as diagram size grows

---

## Grid Lines and Snapping

Grid lines and snapping require injecting the `Snapping` module. Configure via `snapSettings`.

```tsx
import { DiagramComponent, SnapConstraints, SnapSettingsModel } from '@syncfusion/ej2-react-diagrams';
import { Snapping } from '@syncfusion/ej2-react-diagrams';

const snapSettings: SnapSettingsModel = {
  constraints: SnapConstraints.ShowLines | SnapConstraints.SnapToLines,
  horizontalGridlines: { lineColor: '#e0e0e0', lineDashArray: '2 2' },
  verticalGridlines: { lineColor: '#e0e0e0', lineDashArray: '2 2' },
  snapObjectDistance: 5,
  snapAngle: 5,
  snapLineColor: '#07EDE1',
};

<DiagramComponent snapSettings={snapSettings} />
```

### Snap Constraints

| Constraint | Description |
|------------|-------------|
| `SnapConstraints.ShowLines` | Display grid lines |
| `SnapConstraints.SnapToLines` | Snap elements to grid intersections |
| `SnapConstraints.SnapToObject` | Snap to neighboring elements with smart guides |
| `SnapConstraints.All` | Enable all snapping features (default) |
| `SnapConstraints.None` | Disable all grid and snapping |

### Dot Grid Pattern

```tsx
const snapSettings: SnapSettingsModel = {
  constraints: SnapConstraints.ShowLines,
  gridType: 'Dots',  // Default is 'Lines'
  horizontalGridlines: { dotIntervals: [3, 20, 1, 20], lineColor: 'blue' },
  verticalGridlines: { dotIntervals: [3, 20, 1, 20], lineColor: 'blue' },
};
```

### Custom Snap Interval

```tsx
// Objects snap every 10px instead of to nearest gridline
horizontalGridlines: { snapIntervals: [10] },
verticalGridlines: { snapIntervals: [10] },
```

---

## Ruler

Display horizontal and vertical measurement guides with `rulerSettings`.

```tsx
<DiagramComponent
  rulerSettings={{
    showRulers: true,
    horizontalRuler: {
      interval: 8,
      segmentWidth: 100,
      thickness: 35,
      tickAlignment: 'RightOrBottom',
      markerColor: 'red',
    },
    verticalRuler: {
      interval: 10,
      segmentWidth: 200,
      thickness: 35,
      tickAlignment: 'LeftOrTop',
    },
  }}
/>
```

| Property | Description |
|----------|-------------|
| `showRulers` | Toggle ruler visibility |
| `interval` | Spacing between tick marks |
| `segmentWidth` | Width of each ruler segment |
| `thickness` | Ruler display area height/width |
| `tickAlignment` | `'LeftOrTop'` \| `'RightOrBottom'` |
| `markerColor` | Color of the cursor position indicator (default: red) |
| `arrangeTick` | Callback function to customize individual tick appearance |

---

## Scroll Settings

Control scroll behavior, viewport, zoom limits, and auto-scroll via `scrollSettings`.

```tsx
<DiagramComponent
  scrollSettings={{
    scrollLimit: 'Infinity',    // 'Infinity' | 'Diagram' | 'Limited'
    canAutoScroll: true,
    autoScrollBorder: { left: 15, right: 15, top: 15, bottom: 15 },
    autoScrollFrequency: 50,   // ms between auto-scroll ticks
    padding: { left: 100, top: 100 },
    scrollableArea: new Rect(0, 0, 2000, 2000),  // used with scrollLimit:'Limited'
    minZoom: 0.2,
    maxZoom: 5,
  }}
/>
```

### Programmatic Scroll and Zoom

```tsx
// Set initial scroll position
diagramInstance.scrollSettings.horizontalOffset = 100;
diagramInstance.scrollSettings.verticalOffset = 100;
diagramInstance.dataBind();

// Zoom programmatically
diagramInstance.zoomTo({ type: 'ZoomIn', zoomFactor: 0.2, focusPoint: { x: 0.5, y: 0.5 } });
diagramInstance.zoomTo({ type: 'ZoomOut', zoomFactor: 0.2 });

// Reset zoom and scroll to defaults
diagramInstance.reset();

// Update viewport after container resize
diagramInstance.updateViewPort();
```

### Scroll Change Event

```tsx
<DiagramComponent
  scrollChange={(args) => {
    console.log(args.panState, args.ScrollOffset);
  }}
/>
```

> For `canAutoScroll` to work, `scrollLimit` must be set to `'Infinity'`.

---

## Page Settings

Configure page size, orientation, background, margins, multiple pages, and boundary constraints.

```tsx
<DiagramComponent
  pageSettings={{
    width: 816,
    height: 1056,
    orientation: 'Portrait',      // 'Portrait' | 'Landscape'
    multiplePage: true,
    showPageBreaks: true,
    boundaryConstraints: 'Page',  // 'Infinity' | 'Diagram' | 'Page'
    background: {
      color: '#f5f5f5',
      source: 'https://example.com/bg.jpg',  // optional background image
      scale: 'Meet',
      align: 'XMinYMin',
    },
    margin: { left: 10, top: 10, right: 10, bottom: 10 },
    fitOptions: {
      canFit: true,
      canZoomIn: true,
      region: 'Content',    // 'Content' | 'PageSettings' | 'CustomBounds'
      mode: 'Page',         // 'Page' | 'Width' | 'Height'
      margin: { left: 50, right: 50, top: 50, bottom: 50 },
    },
  }}
/>
```

| Property | Description |
|----------|-------------|
| `width` / `height` | Page dimensions in pixels |
| `orientation` | Swaps width/height when changed |
| `multiplePage` | Extend canvas across multiple pages |
| `showPageBreaks` | Render visual page break lines |
| `boundaryConstraints` | `'Infinity'` (no restriction) \| `'Diagram'` \| `'Page'` |
| `background.color` | Page background fill color |
| `background.source` | Background image URL |
| `fitOptions.canFit` | Center content in viewport on load |

---

## Tooltip

### Default Interaction Tooltip

The diagram displays position/size/angle during drag, resize, and rotate automatically. Disable with:

```tsx
import { SelectorConstraints } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  selectedItems={{ constraints: SelectorConstraints.All & ~SelectorConstraints.ToolTip }}
/>
```

### Diagram-Level Tooltip (Mouse Hover)

```tsx
import { DiagramConstraints } from '@syncfusion/ej2-react-diagrams';

<DiagramComponent
  constraints={DiagramConstraints.Default | DiagramConstraints.Tooltip}
  tooltip={{ content: 'Diagram tooltip', position: 'BottomRight' }}
/>
```

### Per-Node/Connector Tooltip

```tsx
import { NodeConstraints, ConnectorConstraints } from '@syncfusion/ej2-react-diagrams';

// Node with tooltip
{
  id: 'node1',
  constraints: NodeConstraints.Default | NodeConstraints.Tooltip,
  tooltip: {
    content: 'My Node',
    position: 'BottomRight',
    relativeMode: 'Object',   // 'Object' | 'Mouse'
    isSticky: false,          // Keep visible after mouse-out
    showTipPointer: true,
    width: 200,
    height: 60,
    animation: {
      open: { effect: 'ZoomIn', duration: 300, delay: 0 },
      close: { effect: 'ZoomOut', duration: 200, delay: 0 },
    },
  },
}

// Port tooltip
{
  constraints: PortConstraints.Default | PortConstraints.ToolTip,
  tooltip: { content: 'Port tooltip' },
}

// Annotation tooltip
{
  constraints: AnnotationConstraints.Tooltip,
  tooltip: { content: 'Annotation tooltip', position: 'TopRight', relativeMode: 'Object' },
}
```

### Programmatic Tooltip Control

```tsx
diagramInstance.showTooltip(diagramInstance.nodes[0]);
diagramInstance.hideTooltip(diagramInstance.nodes[0]);
// Use openOn: 'Custom' on tooltip to prevent auto-hover trigger
```

---

## Overview Panel

Display a miniature preview of the full diagram for navigation. The overview viewport rectangle supports drag, resize, and click to navigate.

```tsx
import { OverviewComponent } from '@syncfusion/ej2-react-diagrams';

// In your component render:
<div style={{ display: 'flex' }}>
  <DiagramComponent id="container" width={'70%'} height={'600px'} />
  <OverviewComponent
    id="overview"
    sourceID="container"   // Must match DiagramComponent id
    width={'300px'}
    height={'150px'}
  />
</div>
```

Overview interactions:
- **Drag** the viewport rectangle to pan the main diagram
- **Resize** the rectangle to zoom in/out
- **Click** a location to navigate instantly
- **Click and drag** to define a new viewport region

---

## Localization

Localize context menu items and symbol palette search text using `L10n.load()` and `setCulture()`.

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";
import { DiagramComponent,DiagramContextMenu,Diagram,NodeModel } from "@syncfusion/ej2-react-diagrams";
Diagram.Inject(DiagramContextMenu);
import { L10n, setCulture } from '@syncfusion/ej2-base';
setCulture('de');

L10n.load({
  'de-DE': {
    diagram: {
      Cut: 'Corte',
      Copy: 'Copia',
      Paste: 'Pasta',
      Undo: 'Deshacer',
      Redo: 'Rehacer',
      SelectAll: 'Seleccionar todo',
      Grouping: 'Agrupación',
      Group: 'Grupo',
      Ungroup: 'Desagrupar',
      Order: 'Fin',
      BringToFront: 'Traer a delante',
      MoveForward: 'Movimiento adelante',
      SendToBack: 'Enviar a espalda',
      SendBackward: 'Enviar hacia atrás',
    },
  },
});
let node:NodeModel [] = [
    {
      id: 'Node1',
      offsetX: 300,
      offsetY: 288,
      annotations: [{ content: 'Node1' }],
    },
    {
      id: 'Node2',
      offsetX: 150,
      offsetY: 250,
      annotations: [{ content: 'Node2' }],
    },
  ];
function App() {
    return (<DiagramComponent id="container" width={'100%'} height={'600px'} 
    locale='de-DE'
     //Enables the context menu
     contextMenuSettings={{
        show: true
    }}
    nodes={node}
    getNodeDefaults={(node:NodeModel) => {
        node.width = 100;
        node.height = 100;
        node.shape = { type: 'Basic', shape: 'Ellipse' };
    }}
    />);
}
const root = ReactDOM.createRoot(document.getElementById('diagram'));
root.render(<App />);
```

> Use `locale` prop on both `DiagramComponent` and `SymbolPaletteComponent` independently.

---

## Accessibility

The diagram provides WAI-ARIA compliance through `aria-label` attributes on interactive resize/rotate thumbs and connector endpoints.

### Accessibility Compliance Summary

| Feature | Support |
|---------|---------|
| WCAG 2.2 | Partial |
| Screen Reader | ✅ Full |
| Color Contrast | ✅ Full |
| Mobile Device | ✅ Full |
| Keyboard Navigation | Partial |
| Right-to-Left | ❌ Not supported |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Select all |
| `Ctrl+X` / `Ctrl+C` / `Ctrl+V` | Cut / Copy / Paste |
| `Ctrl+Z` / `Ctrl+Y` | Undo / Redo |
| `Delete` | Delete selected |
| Arrow keys | Nudge selected object |
| `Enter` | Start annotation edit |
| `Escape` | End annotation edit |
| `Ctrl++` / `Ctrl+-` | Zoom in / Zoom out |
| `Ctrl+mouse wheel` | Zoom in/out |

---

## Best Practices

- Use **layers** to separate background template elements (locked) from editable content layers.
- Enable **virtualization** for any diagram with 100+ elements to maintain responsive performance.
- Set `preventDefaults: true` in `serializationSettings` when layers add many nodes to reduce load time.
- Use `scrollLimit: 'Diagram'` for fixed-size diagrams; use `'Infinity'` for open-ended canvases.
- Enable `showPageBreaks: true` whenever using `multiplePage: true` to give visual layout guidance.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Locked layer elements still appear draggable | Confirm `lock: true` is set on the layer, not just the node |
| Virtualization causes elements to disappear | Ensure `DiagramConstraints.Virtualization` is OR'd with `DiagramConstraints.Default` |
| Grid lines not visible | Inject `Snapping` module; set `snapSettings.constraints` to include `SnapConstraints.ShowLines` |
| Auto-scroll not triggering | `canAutoScroll: true` requires `scrollLimit: 'Infinity'` |
| Overview not reflecting diagram | Verify `sourceID` on `OverviewComponent` exactly matches the `id` on `DiagramComponent` |
| Context menu not localized | Call `setCulture()` before rendering; set `locale` prop on the component |
