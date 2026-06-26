# Labels and Annotations in Syncfusion React Diagram

## Table of Contents
- [Annotation Fundamentals](#annotation-fundamentals)
- [Creating Annotations](#creating-annotations)
- [Node Annotation Positioning](#node-annotation-positioning)
- [Connector Annotation Positioning](#connector-annotation-positioning)
- [Annotation Style](#annotation-style)
- [Text Wrapping and Overflow](#text-wrapping-and-overflow)
- [Templates](#templates)
- [Hyperlinks](#hyperlinks)
- [Interactive Annotations](#interactive-annotations)
- [Annotation Events](#annotation-events)
- [Runtime Operations](#runtime-operations)
- [Advanced Properties](#advanced-properties)
- [Troubleshooting](#troubleshooting)

---

## Annotation Fundamentals

Annotations are text blocks displayed over nodes and connectors. Both nodes and connectors accept multiple annotations via an `annotations` array. Each annotation has independent style, position, and interaction settings.

> **ID rules:** Annotation IDs must start with a letter. No spaces, underscores, or special characters.

---

## Creating Annotations

### Node annotation

```tsx
import { DiagramComponent, NodeModel } from '@syncfusion/ej2-react-diagrams';

const nodes: NodeModel[] = [
  {
    id: 'n1',
    offsetX: 250, offsetY: 250,
    width: 120, height: 60,
    annotations: [{ content: 'Decision' }]  // defaults to center
  }
];
```

### Connector annotation

```tsx
import { ConnectorModel } from '@syncfusion/ej2-react-diagrams';

const connectors: ConnectorModel[] = [
  {
    sourcePoint: { x: 100, y: 100 },
    targetPoint: { x: 300, y: 300 },
    type: 'Orthogonal',
    annotations: [{ content: 'Yes', offset: 0.5 }]  // 0–1 along the connector path
  }
];
```

### Multiple annotations per element

```tsx
annotations: [
  { content: 'Left', offset: { x: 0.12, y: 0.1 } },
  { content: 'Center', offset: { x: 0.5, y: 0.5 } },
  { content: 'Right', offset: { x: 0.82, y: 0.9 } }
]
```

---

## Node Annotation Positioning

Node annotations use a **two-step** positioning system:
1. **`offset`** — fractional `{x, y}` within the node boundary; `(0,0)` = top-left, `(1,1)` = bottom-right, default `(0.5, 0.5)` = center
2. **`horizontalAlignment` / `verticalAlignment`** — how the annotation box aligns at the computed offset point

### Common positions

| Position | `offset` | Notes |
|----------|----------|-------|
| Center | `{ x: 0.5, y: 0.5 }` | Default |
| Top center | `{ x: 0.5, y: 0 }` | + `verticalAlignment: 'Bottom'` to appear outside above |
| Bottom center | `{ x: 0.5, y: 1 }` | + `verticalAlignment: 'Top'` to appear outside below |
| Left center | `{ x: 0, y: 0.5 }` | + `horizontalAlignment: 'Right'` to appear outside left |
| Right center | `{ x: 1, y: 0.5 }` | + `horizontalAlignment: 'Left'` to appear outside right |

```tsx
annotations: [{
  content: 'External label',
  offset: { x: 0.5, y: 1 },
  verticalAlignment: 'Top',    // places label below the node
  margin: { top: 8 }           // adds extra spacing
}]
```

### Fixed size annotations

```tsx
annotations: [{
  content: 'Long annotation content',
  offset: { x: 0, y: 1 },
  width: 120,
  height: 50
}]
```

### Update positioning at runtime

```tsx
diagramRef.current!.nodes[0].annotations[0].offset = { x: 0, y: 0.5 };
diagramRef.current!.nodes[0].annotations[0].horizontalAlignment = 'Right';
diagramRef.current!.dataBind();
```

---

## Connector Annotation Positioning

Connector annotations use a numeric `offset` (0–1) along the path from source to target:

| `offset` | Position |
|----------|----------|
| `0` | At source point |
| `0.5` | Midpoint (default) |
| `1` | At target point |

### Alignment options

```tsx
annotations: [
  { content: 'Start', offset: 0, alignment: 'Before' },   // before midpoint
  { content: 'End',   offset: 1, alignment: 'After' }    // after midpoint
]
```

### Displacement (shift perpendicular to path)

```tsx
annotations: [{
  content: 'Label',
  alignment: 'After',
  displacement: { x: 50, y: 50 }  // only valid with 'Before' or 'After'
}]
```

### Rotate annotation with connector

```tsx
annotations: [{ content: 'Flow label', segmentAngle: true, offset: 0.3 }]
```

### Drag limit (constrain label dragging on connector)

```tsx
import { AnnotationConstraints } from '@syncfusion/ej2-react-diagrams';

annotations: [{
  content: 'Draggable label',
  constraints: AnnotationConstraints.Interaction | AnnotationConstraints.Drag,
  dragLimit: { left: 20, right: 20, top: 10, bottom: 10 }
}]
```

---

## Annotation Style

### Basic text styling

```tsx
annotations: [{
  content: 'Styled Label',
  style: {
    color: '#1565C0',          // text color
    fontSize: 13,
    fontFamily: 'Segoe UI',
    bold: true,
    italic: false,
    textDecoration: 'None',    // 'Underline' | 'LineThrough' | 'Overline' | 'None'
    textAlign: 'Center',       // 'Left' | 'Center' | 'Right' | 'Justify'
    fill: 'transparent',       // background fill of annotation box
    strokeColor: 'transparent',
    opacity: 1
  }
}]
```

### Rotation

```tsx
annotations: [{ content: 'Rotated', rotateAngle: 45 }]
```

### Rotation reference

Controls whether the annotation rotates with its parent node or stays fixed on the page:

```tsx
annotations: [{ content: 'Fixed', rotationReference: 'Page' }]  // 'Page' | 'Parent'
```

---

## Text Wrapping and Overflow

### Text wrapping

| `textWrapping` | Behavior |
|----------------|---------|
| `'WrapWithOverflow'` | Wraps; very long words may overflow (default) |
| `'Wrap'` | Wraps strictly within bounds |
| `'NoWrap'` | Single line; truncates if too wide |

### Text overflow

| `textOverflow` | Behavior |
|----------------|---------|
| `'Wrap'` | Shows all text with vertical overflow (default) |
| `'Clip'` | Clips at boundary |
| `'Ellipsis'` | Shows `...` when truncated |

```tsx
annotations: [{
  content: 'A very long annotation that wraps',
  style: {
    textWrapping: 'Wrap',
    textOverflow: 'Ellipsis'
  }
}]
```

---

## Templates

### String template (HTML/SVG inline)

```tsx
annotations: [{
  template: '<div><input type="button" value="Submit" /></div>',
  width: 100,
  height: 40
}]
```

> Always specify `width` and `height` when using templates.

### Functional template

```tsx
function annotationTemplate(props: any) {
  return (
    <div style={{ width: '100px', overflow: 'hidden' }}>
      <input type="button" value={props.id} />
    </div>
  );
}

<DiagramComponent
  annotationTemplate={annotationTemplate.bind(this)}
  ...
/>
```

---

## Hyperlinks

```tsx
import { DiagramComponent } from '@syncfusion/ej2-react-diagrams';

// Node annotation hyperlink
annotations: [{
  hyperlink: {
    link: 'https://example.com',
    content: 'Visit Site',           // display text
    color: '#1565C0',
    hyperlinkOpenState: 'NewWindow',  // 'NewWindow' | 'NewTab' | 'CurrentPage'
    textDecoration: 'Underline'
  }
}]
```

---

## Interactive Annotations

### Enable interaction

Labels are static by default. Enable dragging, resizing, and rotating with `AnnotationConstraints.Interaction`:

```tsx
import { AnnotationConstraints } from '@syncfusion/ej2-react-diagrams';

annotations: [{
  content: 'Draggable',
  constraints: AnnotationConstraints.Interaction
}]
```

### Read-only annotation

```tsx
annotations: [{
  content: 'Cannot edit',
  constraints: AnnotationConstraints.ReadOnly
}]
```

### Programmatic editing

```tsx
diagramRef.current!.startTextEdit(diagramRef.current!.nodes[0]);
```

Interactive editing: double-click on a label, or select it and press **F2**.

---

## Annotation Events

| Event | Trigger |
|-------|---------|
| `doubleClick` | User double-clicks — opens edit mode |
| `textEdit` | Edit session ends (focus lost) |
| `keyDown` | Key pressed while annotation focused |
| `keyUp` | Key released while annotation focused |
| `selectionChange` | Annotation selected/deselected |

### Text edit event

```tsx
<DiagramComponent
  textEdit={(args) => {
    console.log('Old text:', args.oldValue);
    console.log('New text:', args.newValue);
    // Revert if empty
    if (args.newValue.trim() === '') {
      args.cancel = true;
    }
  }}
/>
```

### Prevent edit on double-click

```tsx
<DiagramComponent
  doubleClick={(args) => {
    args.cancel = true;  // blocks editing
  }}
/>
```

---

## Runtime Operations

### Add annotation

```tsx
import { ShapeAnnotationModel } from '@syncfusion/ej2-react-diagrams';

const annotation: ShapeAnnotationModel[] = [{
  id: 'label2',
  content: 'New Annotation'
}];

diagramRef.current!.addLabels(diagramRef.current!.nodes[0], annotation);
diagramRef.current!.dataBind();
```

### Update annotation

```tsx
diagramRef.current!.nodes[0].annotations[0].content = 'Updated text';
diagramRef.current!.dataBind();
```

### Remove annotation

```tsx
const node = diagramRef.current!.nodes[0];
diagramRef.current!.removeLabels(node, node.annotations);
```

---

## Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `content` | `string` | Annotation text |
| `offset` | `PointModel` (node) / `number` (connector) | Position |
| `horizontalAlignment` | `'Left' \| 'Center' \| 'Right' \| 'Stretch'` | Horizontal align at offset point |
| `verticalAlignment` | `'Top' \| 'Center' \| 'Bottom' \| 'Stretch'` | Vertical align at offset point |
| `margin` | `MarginModel` | Spacing around the annotation |
| `style` | `TextStyleModel` | Font, color, wrapping, alignment |
| `rotateAngle` | `number` | Rotation degrees |
| `rotationReference` | `'Page' \| 'Parent'` | Fixed or follows node rotation |
| `visibility` | `boolean` | Show/hide annotation |
| `constraints` | `AnnotationConstraints` | Interaction flags |
| `dragLimit` | `MarginModel` | Drag boundary for connector labels |
| `template` | `string` | HTML/SVG inline template |
| `hyperlink` | `HyperlinkModel` | Clickable link inside label |
| `alignment` | `'Before' \| 'Center' \| 'After'` | Connector path alignment |
| `displacement` | `PointModel` | Perpendicular offset from path |
| `segmentAngle` | `boolean` | Rotate annotation with connector angle |

---

## Troubleshooting

**Annotation not visible**
- Check `visibility` is not `false`
- For connectors, verify `offset` is between 0 and 1

**Text cut off / overflowing**
- Set explicit `width` and `height` on the annotation
- Adjust `textWrapping` to `'Wrap'` and `textOverflow` to `'Clip'` or `'Ellipsis'`

**Annotation doesn't move after `offset` change**
- Must call `diagramRef.current!.dataBind()` after every runtime change

**Template not rendering correctly**
- Always specify `width` and `height` on the annotation when using `template`

**Label editing with F2 not working**
- Ensure `AnnotationConstraints.ReadOnly` is NOT set on that annotation

**Related docs:**
- Nodes → [nodes.md](nodes.md)
- Connectors → [connectors.md](connectors.md)
