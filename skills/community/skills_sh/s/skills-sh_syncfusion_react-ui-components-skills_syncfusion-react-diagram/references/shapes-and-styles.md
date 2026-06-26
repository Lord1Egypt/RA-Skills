# Shapes and Styles in Syncfusion React Diagram

## Table of Contents
- [Node Shape Types](#node-shape-types)
- [Basic Shapes](#basic-shapes)
- [Flow Shapes](#flow-shapes)
- [Path Shapes](#path-shapes)
- [Text Nodes](#text-nodes)
- [Image Nodes](#image-nodes)
- [HTML Nodes](#html-nodes)
- [Native (SVG) Nodes](#native-svg-nodes)
- [Node Style Properties](#node-style-properties)
- [Gradients](#gradients)
- [Shadow Effects](#shadow-effects)
- [Node Templates](#node-templates)
- [getNodeDefaults Pattern](#getnodedefaults-pattern)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## Node Shape Types

Every node has a `shape` property that defines its visual form. The `type` field inside `shape` selects the shape category:

| `shape.type` | Description |
|-------------|-------------|
| `'Basic'` | Predefined geometric shapes (default if omitted) |
| `'Flow'` | Flowchart process shapes |
| `'Path'` | Custom SVG path geometry |
| `'Text'` | Text-only node |
| `'Image'` | Image node (URL, local, or Base64) |
| `'HTML'` | HTML content embedded in the diagram |
| `'Native'` | SVG content embedded in the diagram |
| `'Bpmn'` | BPMN business process shapes |
| `'UmlActivity'` / `'UmlClassifier'` | UML diagram shapes |

---

## Basic Shapes

Predefined geometric shapes. The `shape.shape` property picks the variant. Default is `'Rectangle'`.

```tsx
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'rect',
    offsetX: 150, offsetY: 150,
    width: 100, height: 60,
    shape: { type: 'Basic', shape: 'Rectangle', cornerRadius: 8 }
  },
  {
    id: 'ellipse',
    offsetX: 320, offsetY: 150,
    width: 100, height: 60,
    shape: { type: 'Basic', shape: 'Ellipse' }
  },
  {
    id: 'diamond',
    offsetX: 490, offsetY: 150,
    width: 80, height: 80,
    shape: { type: 'Basic', shape: 'Diamond' }
  }
];
```

### Common Basic shape values

`Rectangle` | `Ellipse` | `Triangle` | `Diamond` | `Parallelogram` | `Trapezoid` | `Pentagon` | `Hexagon` | `Heptagon` | `Octagon` | `Star` | `Plus` | `Cross` | `LeftArrow` | `RightArrow` | `UpArrow` | `DownArrow` | `Cylinder`

---

## Flow Shapes

Standardized flowchart shapes following ISO/ANSI conventions. Default shape is `'Process'`.

```tsx
const nodes: NodeModel[] = [
  { id: 'start', offsetX: 150, offsetY: 100, width: 120, height: 50,
    shape: { type: 'Flow', shape: 'Terminator' },
    annotations: [{ content: 'Start' }] },
  { id: 'decision', offsetX: 150, offsetY: 220, width: 120, height: 60,
    shape: { type: 'Flow', shape: 'Decision' },
    annotations: [{ content: 'Check?' }] },
  { id: 'process', offsetX: 150, offsetY: 340, width: 120, height: 50,
    shape: { type: 'Flow', shape: 'Process' },
    annotations: [{ content: 'Action' }] }
];
```

### Common Flow shape values

`Process` | `Decision` | `Terminator` | `Document` | `Data` | `Database` | `DirectData` | `InternalStorage` | `PaperTap` | `ManualInput` | `Sort` | `MultiDocument` | `OffPageReference` | `Annotation` | `Delay`

---

## Path Shapes

Custom SVG path data defines any arbitrary shape. Use standard SVG path syntax in the `data` property.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'custom',
    offsetX: 250, offsetY: 200,
    width: 100, height: 100,
    shape: {
      type: 'Path',
      data: 'M35.2441,25 L22.7161,49.9937 L22.7161,0.00657536 L35.2441,25 z M22.7167,25 L-0.00131226,25'
    }
  }
];
```

---

## Text Nodes

Displays styled text content without a visible shape background.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'label',
    offsetX: 250, offsetY: 100,
    width: 200, height: 40,
    shape: { type: 'Text', content: 'Section Header' },
    style: { fill: 'none', strokeColor: 'none' }   // transparent background
  }
];
```

---

## Image Nodes

Embed images using URLs, local paths, or Base64 encoded data.

```tsx
// URL image
const nodes: NodeModel[] = [
  {
    id: 'img',
    offsetX: 200, offsetY: 200,
    width: 120, height: 120,
    shape: {
      type: 'Image',
      source: 'https://example.com/logo.png',
      scale: 'Meet',    // 'None' | 'Meet' | 'Slice' | 'Stretch'
    },
    style: { fill: 'none' }
  }
];
```

### Image scale options

| `scale` | Behavior |
|---------|---------|
| `'None'` | Natural size; may overflow node |
| `'Meet'` | Fits inside while preserving aspect ratio (letterbox) |
| `'Slice'` | Fills node while preserving aspect ratio (cropped) |
| `'Stretch'` | Stretches to fill the node exactly |

> **Note:** Image nodes exported to PNG/JPEG require the page to be served from a web server (not `file://`).

---

## HTML Nodes

Embeds any HTML content inside the node boundary.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'htmlNode',
    offsetX: 250, offsetY: 200,
    width: 150, height: 60,
    shape: {
      type: 'HTML',
      content: '<div style="background:#6BA5D7;height:100%;padding:8px;text-align:center;"><b>HTML Node</b></div>'
    }
  }
];
```

### Functional HTML template

```tsx
function nodeContent(node: NodeModel) {
  const bg = node.id === 'admin' ? '#E53935' : '#1E88E5';
  return (
    <div style={{ background: bg, height: '100%', color: 'white', padding: '8px' }}>
      {(node as any).data?.label}
    </div>
  );
}

const nodes: NodeModel[] = [
  { id: 'admin', offsetX: 150, offsetY: 200, width: 120, height: 60,
    shape: { type: 'HTML', content: nodeContent as any } }
];
```

> **Note:** HTML and Native nodes cannot be exported to image formats (PNG/JPEG/BMP).

---

## Native (SVG) Nodes

Embeds raw SVG markup inside the node.

```tsx
const nodes: NodeModel[] = [
  {
    id: 'svgNode',
    offsetX: 200, offsetY: 200,
    width: 100, height: 100,
    shape: {
      type: 'Native',
      scale: 'Stretch',
      content: '<g><circle cx="50" cy="50" r="45" fill="#1E88E5"/><text x="50" y="55" text-anchor="middle" fill="white" font-size="14">SVG</text></g>'
    }
  }
];
```

---

## Node Style Properties

Apply visual styles via the `style` property:

```tsx
const nodes: NodeModel[] = [
  {
    id: 'styled',
    offsetX: 250, offsetY: 200,
    width: 120, height: 60,
    style: {
      fill: '#1E88E5',          // fill color
      strokeColor: '#0D47A1',   // border color
      strokeWidth: 2,           // border thickness
      strokeDashArray: '4 2',   // dashed border
      opacity: 0.9,             // 0–1
    }
  }
];
```

### Visibility

```tsx
{ id: 'hidden', visible: false, ... }   // hidden but still in DOM
```

### Corner radius (rectangle only)

```tsx
shape: { type: 'Basic', shape: 'Rectangle', cornerRadius: 12 }
```

### Z-index (stacking order)

```tsx
{ id: 'front', zIndex: 10, ... }   // higher = rendered on top
```

### Rotation

```tsx
{ id: 'rotated', rotateAngle: 45, ... }
```

### Pivot point (rotation anchor)

```tsx
// Default pivot (0.5, 0.5) = center; (0,0) = top-left corner
{ id: 'n1', pivot: { x: 0, y: 0 }, ... }
```

---

## Gradients

### Linear gradient

```tsx
import { NodeModel, LinearGradientModel } from '@syncfusion/ej2-react-diagrams';

const linearGradient: LinearGradientModel = {
  type: 'Linear',
  x1: 0,   y1: 0,     // start point (% of node size)
  x2: 100, y2: 100,   // end point
  stops: [
    { color: '#ffffff', offset: 0 },
    { color: '#1E88E5', offset: 100 }
  ]
};

const nodes: NodeModel[] = [
  { id: 'n1', offsetX: 200, offsetY: 200, width: 120, height: 60,
    style: { gradient: linearGradient } }
];
```

### Radial gradient

```tsx
import { RadialGradientModel } from '@syncfusion/ej2-react-diagrams';

const radialGradient: RadialGradientModel = {
  type: 'Radial',
  cx: 50, cy: 50,   // center of outer circle
  fx: 25, fy: 25,   // center of inner circle (focal point)
  r: 50,             // radius
  stops: [
    { color: '#ffffff', offset: 0 },
    { color: '#43A047', offset: 100 }
  ]
};
```

---

## Shadow Effects

Add a drop shadow to a node. Must enable via `NodeConstraints.Shadow`.

```tsx
import { DiagramComponent, NodeModel, NodeConstraints } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'shadowNode',
    offsetX: 250, offsetY: 200,
    width: 120, height: 60,
    constraints: NodeConstraints.Default | NodeConstraints.Shadow,
    shadow: {
      angle: 45,        // degrees
      distance: 10,     // pixels
      opacity: 0.6,
      color: '#455A64'
    }
  }
];
```

---

## Node Templates

### `nodeTemplate` prop (diagram-wide)

Define a single template function applied to all HTML nodes:

```tsx
function diagramTemplate(node: NodeModel) {
  const data = (node as any).data;
  return (
    <div style={{ background: '#1E88E5', color: 'white', height: '100%', padding: '8px' }}>
      <strong>{data?.name}</strong>
    </div>
  );
}

<DiagramComponent
  nodeTemplate={diagramTemplate.bind(this)}
  nodes={nodes}
/>
```

---

## getNodeDefaults Pattern

Apply consistent defaults to every node without repeating properties:

```tsx
<DiagramComponent
  getNodeDefaults={(obj: NodeModel): NodeModel => {
    // Apply to ALL nodes
    obj.style = {
      fill: '#ECEFF1',
      strokeColor: '#90A4AE',
      strokeWidth: 1.5
    };
    obj.width = obj.width ?? 120;
    obj.height = obj.height ?? 50;
    return obj;
  }}
/>
```

### Role-based colors via `getNodeDefaults`

```tsx
getNodeDefaults={(obj: NodeModel): NodeModel => {
  const role = (obj as any).data?.role;
  switch (role) {
    case 'manager':   obj.style = { fill: '#1565C0', strokeColor: '#0D47A1' }; break;
    case 'employee':  obj.style = { fill: '#1E88E5', strokeColor: '#1565C0' }; break;
    default:          obj.style = { fill: '#ECEFF1', strokeColor: '#90A4AE' };
  }
  return obj;
}}
```

---

## Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `shape.type` | `string` | Shape category (`'Basic'`, `'Flow'`, `'Path'`, etc.) |
| `shape.shape` | `string` | Specific shape variant within the category |
| `shape.cornerRadius` | `number` | Rounds rectangle corners (Basic/Flow only) |
| `shape.data` | `string` | SVG path string for Path shapes |
| `shape.source` | `string` | URL or Base64 for Image shapes |
| `shape.scale` | `'None' \| 'Meet' \| 'Slice' \| 'Stretch'` | Image/SVG scaling |
| `shape.content` | `string \| function` | Text content for Text/HTML/Native shapes |
| `style.fill` | `string \| GradientModel` | Fill color or gradient |
| `style.strokeColor` | `string` | Border color |
| `style.strokeWidth` | `number` | Border thickness |
| `style.strokeDashArray` | `string` | Dashed border pattern |
| `style.opacity` | `number` | Transparency (0–1) |
| `style.gradient` | `GradientModel` | Linear or radial gradient |
| `shadow` | `ShadowModel` | Drop shadow config |
| `constraints` | `NodeConstraints` | Enable/disable shadow and other behaviors |
| `rotateAngle` | `number` | Rotation in degrees |
| `pivot` | `PointModel` | Rotation anchor (0–1 relative) |
| `zIndex` | `number` | Stacking order |
| `visible` | `boolean` | Show/hide node |
| `addInfo` | `any` | Custom metadata |

---

## Troubleshooting

**Shape not appearing**
- Ensure `shape.type` exactly matches a valid type string (case-sensitive: `'Basic'`, `'Flow'`, etc.)
- Default shape is `Rectangle` when `shape.shape` is omitted for Basic type

**Image not loading**
- Confirm the URL is accessible; Base64 works without server requirements
- Serve HTML from a web server for local images (Chrome/Firefox restrict `file://` canvas access)

**HTML node not rendering correctly**
- Ensure the HTML node has explicit `width` and `height`
- HTML nodes cannot be exported — use `'Basic'` or `'Native'` shapes for export-compatible diagrams

**Gradient not showing**
- Verify `stops` array has at least 2 entries with valid `color` and `offset` values
- `offset` values are percentages (0–100), not fractions (0–1)

**Shadow not visible**
- Add `NodeConstraints.Shadow` to the node's `constraints` — shadow is disabled by default

**Related docs:**
- Nodes → [nodes.md](nodes.md)
- BPMN shapes → [bpmn-diagrams.md](bpmn-diagrams.md)
- UML shapes → [uml-diagrams.md](uml-diagrams.md)
