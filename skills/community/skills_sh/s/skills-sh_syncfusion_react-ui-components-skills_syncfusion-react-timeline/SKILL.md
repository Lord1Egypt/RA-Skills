---
name: syncfusion-react-timeline
description: "Implement Syncfusion React Timeline component for displaying chronological sequences of events with customizable layouts, styling, and interactivity. Use this skill when creating timelines, displaying event sequences, showing milestone progression, creating activity feeds, or building chronological data visualizations. This covers career histories, project roadmaps, process flows, shipping tracking, and time-based event displays."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Layout Components"
---

# Implementing Syncfusion React Timeline

The Timeline component displays events or steps in chronological order with visual indicators. It supports vertical and horizontal layouts, multiple alignment modes, customizable dots and connectors, templates, and events for complete flexibility.

## When to Use This Skill

**Use the Timeline component when:**
- Displaying event sequences chronologically (project milestones, shipping tracking, activity logs)
- Creating career progression or timeline visualizations
- Building step-by-step process flows
- Showing company history or project roadmap
- Implementing event feeds with timestamps
- Displaying before/after comparisons in alternate layouts
- Customizing visual indicators (icons, images, colors) for events

**Choose Timeline over alternatives:**
- **vs Stepper:** Timeline shows completed events; Stepper guides users through steps
- **vs List:** Timeline emphasizes chronological relationships and connections
- **vs Chart:** Timeline focuses on event sequence; Chart focuses on data relationships

## Quick Start Example

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-react-layouts';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-layouts/styles/tailwind3.css';

function App() {
  return (
    <div style={{ height: '350px' }}>
      <TimelineComponent>
        <ItemsDirective>
          <ItemDirective content="Shipped" />
          <ItemDirective content="Departed" />
          <ItemDirective content="Arrived" />
          <ItemDirective content="Out for Delivery" />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
export default App;
```

## Component Overview

**TimelineComponent** is the root container that manages the timeline layout and behavior.

**Key Properties:**
- `orientation`: Layout direction (`Vertical` | `Horizontal`)
- `align`: Content positioning (`Before` | `After` | `Alternate` | `AlternateReverse`)
- `reverse`: Invert display order (most recent first)
- `cssClass`: Apply custom styles
- `template`: Custom rendering for timeline items

**ItemsDirective & ItemDirective** define timeline items within the component.

**Item Properties:**
- `content`: Main event text or template
- `oppositeContent`: Secondary text on opposite side
- `dotCss`: CSS class for dot styling (icons, images, custom appearance)
- `cssClass`: Individual item styling
- `disabled`: Disable interaction and dim appearance

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm and package dependencies
- CSS imports and theme setup
- Basic TimelineComponent structure
- ItemsDirective and ItemDirective usage
- Running your first timeline application

### Layout Configuration
📄 **Read:** [references/layout-configuration.md](references/layout-configuration.md)
- Orientation options (Vertical, Horizontal)
- Alignment modes (Before, After, Alternate, AlternateReverse)
- Content positioning strategies
- Choosing the right layout for your use case
- Code examples for each layout combination

### Items and Content
📄 **Read:** [references/items-and-content.md](references/items-and-content.md)
- Adding string content
- Template-based rich content
- Opposite content configuration
- Dot customization with icons, images, and text
- Disabling individual items
- Per-item CSS classes

### Styling and Customization
📄 **Read:** [references/styling-and-customization.md](references/styling-and-customization.md)
- Connector styling (common and per-item)
- Dot color, size, shadow, outline, and variants
- CSS custom properties for dots
- e-outline class usage
- Complete customization examples

### Events and Callbacks
📄 **Read:** [references/events-and-callbacks.md](references/events-and-callbacks.md)
- `created` event when component renders
- `beforeItemRender` event for item customization
- Event handling patterns and use cases

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Template property for complete custom rendering
- Template context (item, itemIndex)
- Reverse property for newest-first display
- Complex template patterns
- When to use templates vs built-in properties

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- ARIA attributes and roles
- Keyboard navigation support
- RTL (Right-to-Left) language support
- Mobile device accessibility

## Common Patterns

### Pattern 1: Vertical Timeline with Before Alignment
```tsx
<TimelineComponent orientation='Vertical' align='Before'>
  <ItemsDirective>
    <ItemDirective content='Step 1' oppositeContent='Description' />
    <ItemDirective content='Step 2' oppositeContent='Description' />
  </ItemsDirective>
</TimelineComponent>
```

### Pattern 2: Horizontal Alternate Layout
```tsx
<TimelineComponent orientation='Horizontal' align='Alternate'>
  <ItemsDirective>
    <ItemDirective content='Event 1' oppositeContent='Date 1' />
    <ItemDirective content='Event 2' oppositeContent='Date 2' />
  </ItemsDirective>
</TimelineComponent>
```

### Pattern 3: Timeline with Custom Dots and Icons
```tsx
<TimelineComponent>
  <ItemsDirective>
    <ItemDirective content='Shipped' dotCss='e-icons e-package' />
    <ItemDirective content='Delivered' dotCss='e-icons e-check' cssClass='state-completed' />
  </ItemsDirective>
</TimelineComponent>
```

### Pattern 4: Activity Feed with Reverse Order
```tsx
<TimelineComponent reverse={true}>
  <ItemsDirective>
    <ItemDirective content='Latest activity' />
    <ItemDirective content='Previous activity' />
  </ItemsDirective>
</TimelineComponent>
```

## Key Props Summary

| Prop | Type | Values | Purpose |
|------|------|--------|---------|
| `orientation` | string | `Vertical` (default), `Horizontal` | Layout direction |
| `align` | string | `Before`, `After`, `Alternate`, `AlternateReverse` | Content positioning |
| `reverse` | boolean | `true`, `false` (default) | Reverse item order |
| `cssClass` | string | CSS class name | Global styling |
| `template` | function | React function | Custom item rendering |
| `content` (item) | string \| function | Text or template | Event text/content |
| `oppositeContent` (item) | string \| function | Text or template | Secondary content |
| `dotCss` (item) | string | CSS class | Dot styling |
| `disabled` (item) | boolean | `true`, `false` | Disable item |
| `cssClass` (item) | string | CSS class | Per-item styling |

## Troubleshooting

**Timeline not displaying:**
- Ensure CSS imports are included (tailwind3.css or your theme)
- Container must have explicit height: `style={{ height: '350px' }}`
- ItemsDirective must contain ItemDirective children

**Items not centered vertically:**
- Add `height` to TimelineComponent container
- Adjust with CSS custom properties: `--dot-size`, `--dot-outer-space`

**Content positioning unexpected:**
- Verify `align` property: `Before`, `After`, `Alternate`, `AlternateReverse`
- Check `oppositeContent` is defined for two-sided layouts
- Confirm `orientation` matches your layout intent

**Dots not visible:**
- Verify dots have `e-outline` class or custom CSS styling
- Check `dotCss` property contains valid CSS class names
- Ensure theme CSS includes dot styles

**Templates not rendering:**
- Verify template function returns valid JSX
- Check context properties: `props.item`, `props.itemIndex`
- Ensure function signature matches: `(props: any) => JSX.Element`
