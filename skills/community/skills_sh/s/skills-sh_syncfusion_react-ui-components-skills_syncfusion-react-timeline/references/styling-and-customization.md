# Styling and Customization

## Table of Contents
- [Connector Styling](#connector-styling)
- [Dot Styling](#dot-styling)
- [CSS Custom Properties](#css-custom-properties)
- [Outline Class](#outline-class)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)

## Connector Styling

The connector is the line connecting timeline dots. Customize it globally or per-item.

### Common Connector Styling

Apply the same style to all connectors:

```tsx
<TimelineComponent cssClass='custom-connector'>
  <ItemsDirective>
    <ItemDirective content='Eat' />
    <ItemDirective content='Code' />
    <ItemDirective content='Repeat' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS:**

```css
.custom-connector .e-timeline-connector {
  border-color: #0066cc;
  border-width: 3px;
}

.custom-connector .e-timeline-dot {
  background-color: #0066cc;
  border-color: #0066cc;
}
```

### Individual Connector Styling

Apply unique styles to specific item connectors:

```tsx
<TimelineComponent cssClass='gradient-timeline'>
  <ItemsDirective>
    <ItemDirective content='Start' cssClass='state-initial' />
    <ItemDirective content='Middle' cssClass='state-intermediate' />
    <ItemDirective content='End' cssClass='state-final' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS:**

```css
.gradient-timeline .state-initial .e-timeline-connector {
  border-color: #e74c3c;
}

.gradient-timeline .state-intermediate .e-timeline-connector {
  border-color: #f39c12;
}

.gradient-timeline .state-final .e-timeline-connector {
  border-color: #27ae60;
}
```

**Result:** Connectors change color based on status (red → yellow → green progression).

### Dashed vs Solid Connectors

```css
/* Solid connector (default) */
.solid-connector .e-timeline-connector {
  border-style: solid;
  border-width: 2px;
}

/* Dashed connector */
.dashed-connector .e-timeline-connector {
  border-style: dashed;
  border-width: 2px;
  border-color: #999;
}

/* Dotted connector */
.dotted-connector .e-timeline-connector {
  border-style: dotted;
  border-width: 2px;
  border-color: #999;
}
```

## Dot Styling

Comprehensive customization for timeline dots using CSS classes and custom properties.

### Dot Color Customization

```tsx
<TimelineComponent cssClass='dot-color'>
  <ItemsDirective>
    <ItemDirective content='Ordered' cssClass='state-completed' />
    <ItemDirective content='Shipped' cssClass='state-progress' />
    <ItemDirective content='Delivered' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS:**

```css
.dot-color .state-completed {
  --dot-color: #28a745;
}

.dot-color .state-progress {
  --dot-color: #ffc107;
}

.dot-color .e-timeline-item:not(.state-completed):not(.state-progress) {
  --dot-color: #ccc;
}
```

### Dot Size Variations

```tsx
<TimelineComponent cssClass='dot-size'>
  <ItemsDirective>
    <ItemDirective content='Ordered' cssClass='x-small' />
    <ItemDirective content='Shipped' cssClass='small' />
    <ItemDirective content='In Transit' cssClass='medium' />
    <ItemDirective content='Delivered' cssClass='large' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS:**

```css
.dot-size .x-small {
  --dot-size: 8px;
}

.dot-size .small {
  --dot-size: 12px;
}

.dot-size .medium {
  --dot-size: 18px;
}

.dot-size .large {
  --dot-size: 28px;
}
```

### Dot Shadow and Border Effects

```tsx
<TimelineComponent cssClass='dot-shadow'>
  <ItemsDirective>
    <ItemDirective content='Ordered' />
    <ItemDirective content='Shipped' />
    <ItemDirective content='Delivered' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS with Shadow:**

```css
.dot-shadow .e-timeline-dot {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  border: 2px solid #fff;
}

.dot-shadow .e-timeline-dot::after {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
```

**CSS with Outline:**

```css
.dot-outline .e-timeline-dot {
  --dot-outer-space: 4px;
  --dot-border: 2px solid #ccc;
  background-color: transparent;
}
```

### Dot Variants (Filled, Outline, Flat)

```tsx
<TimelineComponent cssClass='dot-variant'>
  <ItemsDirective>
    <ItemDirective content='Filled' cssClass='dot-filled' />
    <ItemDirective content='Flat' cssClass='dot-flat' />
    <ItemDirective content='Outlined' cssClass='dot-outlined' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS:**

```css
/* Filled variant (default) */
.dot-variant .dot-filled .e-timeline-dot {
  background-color: #0066cc;
  border: none;
}

/* Flat variant */
.dot-variant .dot-flat .e-timeline-dot {
  background-color: #e8f4fd;
  border: 1px solid #0066cc;
}

/* Outlined variant */
.dot-variant .dot-outlined .e-timeline-dot {
  background-color: transparent;
  border: 2px solid #0066cc;
}
```

## CSS Custom Properties

Syncfusion Timeline supports CSS custom properties (CSS variables) for fine-grained control.

### Available Custom Properties

| Property | Default | Purpose |
|----------|---------|---------|
| `--dot-size` | 16px | Diameter of timeline dots |
| `--dot-color` | #0066cc | Fill color of dots |
| `--dot-border` | 1px solid transparent | Border style for dots |
| `--dot-outer-space` | 0 | Outer spacing/glow effect |
| `--connector-color` | #0066cc | Color of connecting line |

### Using CSS Variables

```tsx
<TimelineComponent style={{ '--dot-size': '24px', '--dot-color': '#ff6b6b' } as React.CSSProperties}>
  <ItemsDirective>
    <ItemDirective content='Event 1' />
    <ItemDirective content='Event 2' />
  </ItemsDirective>
</TimelineComponent>
```

Or in CSS:

```css
.my-timeline {
  --dot-size: 20px;
  --dot-color: #0066cc;
  --connector-color: #0066cc;
}
```

### Responsive Variables

```css
/* Desktop */
.timeline-container {
  --dot-size: 20px;
}

/* Tablet */
@media (max-width: 768px) {
  .timeline-container {
    --dot-size: 16px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .timeline-container {
    --dot-size: 12px;
  }
}
```

## Outline Class

Apply the `e-outline` class to the TimelineComponent for an outline-style dot appearance:

```tsx
<TimelineComponent cssClass='e-outline'>
  <ItemsDirective>
    <ItemDirective content='Shipped' />
    <ItemDirective content='Departed' />
    <ItemDirective content='Arrived' />
    <ItemDirective content='Out for Delivery' />
  </ItemsDirective>
</TimelineComponent>
```

**Result:** Dots display with transparent fill and visible borders instead of solid fills.

**When to use e-outline:**
- Light/minimal design aesthetic
- Reduce visual emphasis on dots
- Consistent with outline UI patterns
- Better contrast on dark backgrounds

## Complete Examples

### Status-Based Timeline with Colors

```tsx
function StatusTimeline() {
  const items = [
    { content: 'Ordered', status: 'completed' },
    { content: 'Confirmed', status: 'completed' },
    { content: 'Processing', status: 'completed' },
    { content: 'Shipped', status: 'in-progress' },
    { content: 'Delivered', status: 'pending' }
  ];

  return (
    <div style={{ height: '400px' }}>
      <TimelineComponent cssClass='status-timeline'>
        <ItemsDirective>
          {items.map((item, index) => (
            <ItemDirective
              key={index}
              content={item.content}
              cssClass={`status-${item.status}`}
            />
          ))}
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

**CSS:**

```css
.status-timeline .status-completed {
  --dot-color: #28a745;
}

.status-timeline .status-in-progress {
  --dot-color: #ffc107;
  animation: pulse 2s infinite;
}

.status-timeline .status-pending {
  --dot-color: #ccc;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

### Process Flow with Icons and Styling

```tsx
function ProcessFlow() {
  return (
    <div style={{ height: '350px' }}>
      <TimelineComponent 
        cssClass='process-flow'
        orientation='Horizontal'
        align='Alternate'
      >
        <ItemsDirective>
          <ItemDirective 
            content='Planning' 
            dotCss='e-icons e-diagram-sketch'
            cssClass='step-1'
          />
          <ItemDirective 
            content='Design' 
            dotCss='e-icons e-palette'
            cssClass='step-2'
          />
          <ItemDirective 
            content='Development' 
            dotCss='e-icons e-code'
            cssClass='step-3'
          />
          <ItemDirective 
            content='Testing' 
            dotCss='e-icons e-check'
            cssClass='step-4'
          />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

**CSS:**

```css
.process-flow {
  --dot-size: 24px;
}

.process-flow .step-1 { --dot-color: #3498db; }
.process-flow .step-2 { --dot-color: #9b59b6; }
.process-flow .step-3 { --dot-color: #e74c3c; }
.process-flow .step-4 { --dot-color: #27ae60; }

.process-flow .e-timeline-connector {
  border-width: 3px;
}
```

## Best Practices

### 1. Color Semantics
Use colors consistently with meaning:
- Green for success/completed
- Yellow/orange for in-progress/warning
- Red for error/failed
- Gray for disabled/pending

### 2. Accessibility
- Ensure sufficient color contrast (WCAG AA: 4.5:1)
- Don't rely on color alone; use icons or text
- Test with colorblind-friendly palettes

### 3. Performance
- Use CSS classes over inline styles when possible
- Limit animations to critical items
- Avoid excessive shadow/blur effects on many items

### 4. Responsive Design
```css
@media (max-width: 768px) {
  .timeline-container {
    --dot-size: 14px;
  }
  
  .timeline-connector {
    border-width: 1px;
  }
}
```

### 5. Consistency
- Use same color scheme across all timelines
- Maintain dot size ratios
- Keep connector styles uniform
- Match surrounding design system

### 6. Customization Strategy
1. Set global styles via TimelineComponent `cssClass`
2. Use per-item `cssClass` for variations
3. Apply `dotCss` for dot-specific styling
4. Use CSS custom properties for theming
