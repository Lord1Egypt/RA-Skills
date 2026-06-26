# Events and Callbacks

## Table of Contents
- [Created Event](#created-event)
- [BeforeItemRender Event](#beforeitemrender-event)
- [Event Handling Patterns](#event-handling-patterns)
- [Practical Event Use Cases](#practical-event-use-cases)
- [Tips and Troubleshooting](#tips-and-troubleshooting)

## Created Event

The `created` event fires when the TimelineComponent finishes rendering and is ready for interaction. Use this event to perform initialization tasks after the component is fully loaded.

### Basic Created Event

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective } from '@syncfusion/ej2-react-layouts';

function App() {
  const handleCreated = () => {
    console.log('Timeline component created and ready');
    // Perform post-initialization tasks
  };

  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent created={handleCreated}>
        <ItemsDirective>
          <ItemDirective content='Planning' />
          <ItemDirective content='Developing' />
          <ItemDirective content='Testing' />
          <ItemDirective content='Launch' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
export default App;
```

### Common Created Event Use Cases

**Initialize external libraries after timeline loads:**

```tsx
const handleCreated = () => {
  // Initialize tooltips
  const tooltips = new Tooltip('#timeline [title]');
  
  // Setup event listeners
  document.querySelectorAll('.e-timeline-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
      // Custom hover behavior
    });
  });
};
```

**Trigger animations or visual effects:**

```tsx
const handleCreated = () => {
  // Add animation class to items
  const items = document.querySelectorAll('.e-timeline-item');
  items.forEach((item, index) => {
    setTimeout(() => {
      item.classList.add('fade-in');
    }, index * 100);
  });
};
```

**Load data from API:**

```tsx
const [loading, setLoading] = React.useState(true);

const handleCreated = async () => {
  try {
    const response = await fetch('/api/timeline-events');
    const data = await response.json();
    // Update state with fetched data
    setLoading(false);
  } catch (error) {
    console.error('Failed to load timeline data:', error);
  }
};
```

## BeforeItemRender Event

The `beforeItemRender` event fires before rendering each timeline item. Use this event to dynamically customize individual items based on data or conditions.

### Basic BeforeItemRender Event

```tsx
import { TimelineComponent, ItemsDirective, ItemDirective, TimelineRenderingEventArgs } from '@syncfusion/ej2-react-layouts';

function App() {
  const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
    console.log('Rendering item:', args.item.content);
    // Customize item before rendering
  };

  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent beforeItemRender={handleBeforeItemRender}>
        <ItemsDirective>
          <ItemDirective content='Planning' />
          <ItemDirective content='Developing' />
          <ItemDirective content='Testing' />
          <ItemDirective content='Launch' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
export default App;
```

### TimelineRenderingEventArgs Properties

The event argument provides:
- `item` - The current TimelineItem being rendered
- `itemIndex` - The index of the current item (0-based)
- `element` - The DOM element for the item (if available)

### Dynamic Content Customization

```tsx
const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  // Customize based on item index
  if (args.itemIndex === 0) {
    args.item.cssClass = 'first-item';
  }
  
  if (args.itemIndex === args.itemIndex - 1) {
    args.item.cssClass = 'last-item';
  }
};
```

### Conditional Styling Based on Data

```tsx
interface TimelineEvent {
  content: string;
  status: 'completed' | 'in-progress' | 'pending';
  importance: 'high' | 'normal' | 'low';
}

const events: TimelineEvent[] = [
  { content: 'Kickoff', status: 'completed', importance: 'high' },
  { content: 'Design Review', status: 'completed', importance: 'high' },
  { content: 'Development', status: 'in-progress', importance: 'high' },
  { content: 'Testing', status: 'pending', importance: 'normal' }
];

const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  const event = events[args.itemIndex];
  
  // Apply status-based styling
  args.item.cssClass = `status-${event.status}`;
  
  // Highlight important items
  if (event.importance === 'high') {
    args.item.dotCss = (args.item.dotCss || '') + ' dot-highlight';
  }
};

function App() {
  return (
    <div id='timeline' style={{ height: '330px' }}>
      <TimelineComponent beforeItemRender={handleBeforeItemRender}>
        <ItemsDirective>
          {events.map((event, index) => (
            <ItemDirective key={index} content={event.content} />
          ))}
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

### CSS for Status Styling

```css
.status-completed {
  --dot-color: #28a745;
}

.status-in-progress {
  --dot-color: #ffc107;
}

.status-pending {
  --dot-color: #ccc;
}

.dot-highlight {
  --dot-size: 24px;
  box-shadow: 0 0 12px rgba(255, 107, 107, 0.5);
}
```

## Event Handling Patterns

### Multiple Events

```tsx
function TimelineWithEvents() {
  const handleCreated = () => {
    console.log('Timeline ready');
  };

  const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
    // Add alternating row styling
    if (args.itemIndex % 2 === 0) {
      args.item.cssClass = (args.item.cssClass || '') + ' even-item';
    }
  };

  return (
    <div style={{ height: '400px' }}>
      <TimelineComponent 
        created={handleCreated}
        beforeItemRender={handleBeforeItemRender}
      >
        <ItemsDirective>
          <ItemDirective content='Event 1' />
          <ItemDirective content='Event 2' />
          <ItemDirective content='Event 3' />
          <ItemDirective content='Event 4' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

### Event with State Management

```tsx
function TimelineWithState() {
  const [initialized, setInitialized] = React.useState(false);
  const [itemCount, setItemCount] = React.useState(0);

  const handleCreated = () => {
    setInitialized(true);
    console.log('Timeline initialized');
  };

  const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
    setItemCount(args.itemIndex + 1);
    
    // Add animation class
    args.item.cssClass = (args.item.cssClass || '') + ' animate-item';
  };

  return (
    <div>
      <div>Status: {initialized ? 'Ready' : 'Loading'}</div>
      <div>Items rendered: {itemCount}</div>
      <div style={{ height: '350px' }}>
        <TimelineComponent 
          created={handleCreated}
          beforeItemRender={handleBeforeItemRender}
        >
          <ItemsDirective>
            <ItemDirective content='Step 1' />
            <ItemDirective content='Step 2' />
            <ItemDirective content='Step 3' />
          </ItemsDirective>
        </TimelineComponent>
      </div>
    </div>
  );
}
```

## Practical Event Use Cases

### Use Case 1: Log Analytics

```tsx
const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  // Track which timeline items are rendered
  analytics.track('timeline_item_render', {
    itemIndex: args.itemIndex,
    content: args.item.content
  });
};

const handleCreated = () => {
  // Track when timeline component loads
  analytics.track('timeline_component_created', {
    timestamp: new Date().toISOString()
  });
};
```

### Use Case 2: Lazy Load Images

```tsx
const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  // Mark images for lazy loading
  if (args.itemIndex > 5) {
    args.item.cssClass = (args.item.cssClass || '') + ' lazy-load';
  }
};
```

### Use Case 3: Highlight Current Item

```tsx
const [currentIndex, setCurrentIndex] = React.useState(0);

const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  if (args.itemIndex === currentIndex) {
    args.item.cssClass = (args.item.cssClass || '') + ' highlighted';
  }
};
```

### Use Case 4: Theme-Based Customization

```tsx
const [theme, setTheme] = React.useState('light');

const handleBeforeItemRender = (args: TimelineRenderingEventArgs) => {
  args.item.cssClass = (args.item.cssClass || '') + ` theme-${theme}`;
};
```

## Tips and Troubleshooting

**Event not firing?**
- Ensure callback function is properly defined
- Check for TypeScript type errors (use `TimelineRenderingEventArgs` type)
- Verify component is rendering (check console for errors)

**How to cancel default behavior?**
- Set `args.cancel = true` if the event supports it
- Check Syncfusion documentation for cancellable events

**Performance with many items?**
- Use `beforeItemRender` for selective item customization
- Avoid heavy operations in event handlers
- Consider virtual scrolling for 100+ items

**Accessing rendered DOM?**
- Use `args.element` to get the rendered DOM element (if available)
- Reference: `document.querySelectorAll('.e-timeline-item')` after `created` event
