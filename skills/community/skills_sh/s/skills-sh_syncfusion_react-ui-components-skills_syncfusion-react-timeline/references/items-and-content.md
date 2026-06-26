# Items and Content

## Table of Contents
- [Using Items Property](#using-items-property)
- [String Content](#string-content)
- [Template-Based Content](#template-based-content)
- [Opposite Content](#opposite-content)
- [Dot Customization](#dot-customization)
- [Disabling Items](#disabling-items)
- [Per-Item CSS Classes](#per-item-css-classes)

## Using Items Property

The `items` property accepts an array of `TimelineItemModel` objects for data-driven timelines.

### Basic Items Array

```tsx
import { TimelineComponent, TimelineItemModel } from '@syncfusion/ej2-react-layouts';

function App() {
  const items: TimelineItemModel[] = [
    { content: 'Shipped' },
    { content: 'Departed' },
    { content: 'Arrived' },
    { content: 'Out for Delivery' }
  ];

  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent items={items} />
    </div>
  );
}
export default App;
```

### Items with Opposite Content

```tsx
const items: TimelineItemModel[] = [
  { content: 'Breakfast', oppositeContent: '8:00 AM' },
  { content: 'Lunch', oppositeContent: '1:00 PM' },
  { content: 'Dinner', oppositeContent: '8:00 PM' }
];

<TimelineComponent items={items} />
```

### Items with Dot Customization

```tsx
const items: TimelineItemModel[] = [
  { content: 'Completed', dotCss: 'e-icons e-check' },
  { content: 'In Progress', dotCss: 'e-icons e-clock' },
  { content: 'Pending', dotCss: 'e-icons e-calendar' }
];

<TimelineComponent items={items} />
```

### Items with Styling

```tsx
const items: TimelineItemModel[] = [
  { content: 'Success', cssClass: 'status-success' },
  { content: 'Error', cssClass: 'status-error', disabled: true },
  { content: 'Warning', cssClass: 'status-warning' }
];

<TimelineComponent items={items} />
```

### Dynamic Items from API

```tsx
import { TimelineComponent, TimelineItemModel } from '@syncfusion/ej2-react-layouts';
import { useEffect, useState } from 'react';

function App() {
  const [items, setItems] = useState<TimelineItemModel[]>([]);

  useEffect(() => {
    // Fetch from API
    fetch('/api/timeline-events')
      .then(res => res.json())
      .then(data => setItems(data));
  }, []);

  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent items={items} />
    </div>
  );
}
```

**When to use items property:**
- Data from API or database
- Dynamic item count
- State-driven updates
- Simple data structures

## String Content

The simplest way to add content to timeline items is using string values via the `content` property.

### Basic String Content

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-react-layouts';

function App() {
  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent>
        <ItemsDirective>
          <ItemDirective content='Shipped' />
          <ItemDirective content='Departed' />
          <ItemDirective content='Arrived' />
          <ItemDirective content='Out for Delivery' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
export default App;
```

**Result:** Each item displays as plain text centered on its content area.

### Multiline String Content

Use newline characters for multiple lines:

```tsx
<ItemDirective content='Step 1&#10;Initialize' />
```

Or in JavaScript template literals:

```tsx
const description = `Shipped
From Warehouse A
Ready for transport`;

<ItemDirective content={description} />
```

**When to use string content:**
- Simple text labels
- Status indicators (Pending, In Progress, Completed)
- Event names
- Single-line descriptions

## Template-Based Content

For rich formatting, custom layouts, and dynamic data, use template functions with the `content` property.

### Template Function Basics

The template function receives `props` and returns JSX:

```tsx
const contentTemplate = (props: any) => (
  <div className="content-container">
    <div className="title">{props.item.content}</div>
    <span className="description">Additional info</span>
  </div>
);

<ItemDirective content={contentTemplate} />
```

### Complete Template Example

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective, TimelineItemModel } from '@syncfusion/ej2-react-layouts';

function App() {
  const events: TimelineItemModel[] = [
    { 
      content: 'Shipped',
      description: 'Package details received',
      info: 'Awaiting dispatch'
    },
    { 
      content: 'Departed',
      description: 'In-transit',
      info: 'International warehouse'
    },
    { 
      content: 'Arrived',
      description: 'Package at nearest hub',
      info: 'New York - US'
    }
  ];

  const contentTemplate = (data: any) => (
    <div className="content-container">
      <div className="title">{data.title || data.content}</div>
      <span className="description">{data.description}</span>
      <div className="info">{data.info}</div>
    </div>
  );

  return (
    <div className="container" style={{ height: '330px' }}>
      <TimelineComponent id="timeline">
        <ItemsDirective>
          {events.map((item, index) => (
            <ItemDirective 
              key={index} 
              content={() => contentTemplate(item)}
            />
          ))}
          <ItemDirective content="Out for Delivery" />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
export default App;
```

### Template with Styling

```tsx
const contentTemplate = (props: any) => (
  <div style={{ padding: '10px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>
    <h4 style={{ margin: '0 0 5px 0' }}>{props.item.content}</h4>
    <p style={{ margin: '0', fontSize: '12px', color: '#666' }}>
      Additional details about the event
    </p>
  </div>
);
```

**When to use templates:**
- Rich formatted content (multiple elements, styling)
- Dynamic content from data sources
- Complex layouts (images, badges, icons)
- Responsive content based on screen size
- Interactive elements within items

## Opposite Content

Use `oppositeContent` to display supplementary information on the opposite side of the timeline (configurable via `align` property).

### Basic Opposite Content

```tsx
<TimelineComponent align='Before'>
  <ItemsDirective>
    <ItemDirective content='Breakfast' oppositeContent='8:00 AM' />
    <ItemDirective content='Lunch' oppositeContent='1:00 PM' />
    <ItemDirective content='Dinner' oppositeContent='8:00 PM' />
  </ItemsDirective>
</TimelineComponent>
```

**Result:** Main content on left, times on right (Vertical + Before).

### Opposite Content as Template

Templates work for `oppositeContent` too:

```tsx
const dateTemplate = (props: any) => (
  <div style={{ fontWeight: 'bold', color: '#0066cc' }}>
    {new Date(props.item.date).toLocaleDateString()}
  </div>
);

<ItemDirective 
  content='Project completed'
  oppositeContent={dateTemplate}
/>
```

### Common Opposite Content Patterns

```tsx
// Timestamps
<ItemDirective content='Status Update' oppositeContent='2:30 PM' />

// Dates
<ItemDirective content='Milestone' oppositeContent='March 15, 2026' />

// Status badges
<ItemDirective 
  content='Deployment' 
  oppositeContent='✓ Success' 
/>

// User info
<ItemDirective 
  content='Review completed'
  oppositeContent='By John Doe'
/>
```

**When to use opposite content:**
- Timestamps with events
- Dates with milestones
- Metadata alongside main content
- Parallel information display
- Creating balanced two-sided layouts

## Dot Customization

The `dotCss` property lets you apply CSS classes to customize dot appearance. Combine with CSS custom properties or classes for icons, images, text, and colors.

### Icons in Dots

Apply icon font classes to display icons in dots:

```tsx
<TimelineComponent>
  <ItemsDirective>
    <ItemDirective content='Shipped' dotCss='e-icons e-package' />
    <ItemDirective content='In Transit' dotCss='e-icons e-truck' />
    <ItemDirective content='Delivered' dotCss='e-icons e-check' />
  </ItemsDirective>
</TimelineComponent>
```

**Common Syncfusion Icons:**
- `e-check` - Checkmark
- `e-package` - Package
- `e-truck` - Truck/vehicle
- `e-location` - Map pin
- `e-clock` - Clock
- `e-user` - User

### Images as Dots

Use CSS background-image to display custom images:

**CSS:**
```css
.dot-image {
  background-image: url('path/to/image.jpg');
  background-size: cover;
  background-position: center;
}
```

**React:**
```tsx
<ItemDirective content='Avatar' dotCss='dot-image' />
```

### Text in Dots

Display text or numbers in dots:

**CSS:**
```css
.dot-text::before {
  content: '1';
  color: white;
  font-weight: bold;
}
```

**React:**
```tsx
<ItemDirective content='Step 1' dotCss='dot-text' />
```

### Color Customization

**CSS:**
```css
.dot-color-primary {
  --dot-color: #0066cc;
}

.dot-color-success {
  --dot-color: #28a745;
}

.dot-color-warning {
  --dot-color: #ffc107;
}
```

**React:**
```tsx
<ItemDirective content='Ordered' cssClass='state-completed' dotCss='dot-color-success' />
<ItemDirective content='Processing' cssClass='state-progress' dotCss='dot-color-warning' />
```

### Size Customization

Use CSS custom property `--dot-size`:

**CSS:**
```css
.dot-x-small {
  --dot-size: 8px;
}

.dot-small {
  --dot-size: 12px;
}

.dot-medium {
  --dot-size: 20px;
}

.dot-large {
  --dot-size: 28px;
}
```

**React:**
```tsx
<TimelineComponent cssClass='dot-size'>
  <ItemsDirective>
    <ItemDirective content='Ordered' cssClass='x-small' />
    <ItemDirective content='Shipped' cssClass='small' />
    <ItemDirective content='Delivered' cssClass='medium' />
    <ItemDirective content='Reviewed' cssClass='large' />
  </ItemsDirective>
</TimelineComponent>
```

**When to customize dots:**
- Status indicators (use different colors/icons)
- Process steps (numbered dots)
- User avatars (images)
- Visual hierarchy (size variations)
- Semantic meaning (icon = action type)

## Disabling Items

Use the `disabled` property to disable individual items, making them appear dimmed and non-interactive:

```tsx
<TimelineComponent>
  <ItemsDirective>
    <ItemDirective content='Completed' />
    <ItemDirective content='In Progress' />
    <ItemDirective content='Pending' disabled={true} />
    <ItemDirective content='Not Started' disabled={true} />
  </ItemsDirective>
</TimelineComponent>
```

**Default:** `disabled={false}` (enabled)

**When to disable:**
- Show locked or unavailable steps
- Indicate incomplete phases
- Gray out future milestones
- Show unavailable options
- Prevent user interaction on certain items

**Visual Effect:** Disabled items appear with reduced opacity and no interaction states.

## Per-Item CSS Classes

Apply custom styles to individual items using the `cssClass` property:

```tsx
<TimelineComponent>
  <ItemsDirective>
    <ItemDirective content='Success' cssClass='state-success' />
    <ItemDirective content='Error' cssClass='state-error' />
    <ItemDirective content='Warning' cssClass='state-warning' />
  </ItemsDirective>
</TimelineComponent>
```

**CSS for per-item styling:**

```css
.state-success {
  color: #28a745;
}

.state-error {
  color: #dc3545;
}

.state-warning {
  color: #ffc107;
}

/* Custom connectors */
.custom-connector::after {
  border-color: #0066cc;
}

/* Custom backgrounds */
.highlight {
  background-color: #f0f8ff;
  padding: 10px;
  border-radius: 4px;
}
```

**Common patterns:**
- Status colors (success, error, warning, info)
- Highlighting important items
- Custom spacing or layout
- Theme variations per item
- Responsive adjustments

**Combining with dotCss:**

```tsx
<ItemDirective 
  content='Completed'
  dotCss='e-icons e-check dot-color-success'
  cssClass='state-completed'
/>
```

This combines dot customization with item-level styling for cohesive visual design.
