# Advanced Features

## Table of Contents
- [Template Customization](#template-customization)
- [Template Context](#template-context)
- [Reverse Property](#reverse-property)
- [Complex Template Examples](#complex-template-examples)
- [When to Use Templates](#when-to-use-templates)

## Template Customization

The Timeline component's `template` property enables complete custom rendering of timeline items, replacing the default structure entirely. This provides maximum flexibility for complex layouts.

### Basic Template Structure

Templates receive context with item data and can return any JSX:

```tsx
const templateFunction = (props: any) => (
  <div className={`template-container item-${props.itemIndex}`}>
    <div className="content-container">
      <div className="timeline-content">{props.item.content}</div>
    </div>
    <div className="content-connector"></div>
    <div className="progress-line">
      <span className="indicator"></span>
    </div>
  </div>
);

<TimelineComponent template={templateFunction}>
  <ItemsDirective>
    <ItemDirective content="Event 1" />
    <ItemDirective content="Event 2" />
  </ItemsDirective>
</TimelineComponent>
```

### Global vs Item-Level Templates

**Global template** (via TimelineComponent `template`):
- Applied to all items automatically
- Controls entire item rendering
- Best for consistent layouts

**Item-level template** (via ItemDirective `content`):
- Applied to individual item content only
- Doesn't replace dot or structure
- Best for content-specific customization

```tsx
// Global template - replaces entire item structure
<TimelineComponent template={globalTemplate}>

// Item-level template - replaces content only
<ItemDirective content={itemContentTemplate} />
```

## Template Context

The template function receives context with the following properties:

### Available Context Properties

```tsx
interface TemplateContext {
  item: TimelineItemModel;        // Current item data
  itemIndex: number;               // Zero-based index of the item
}
```

### Item Model Properties

```tsx
interface TimelineItemModel {
  content?: string | Function;     // Main content
  oppositeContent?: string | Function;  // Secondary content
  dotCss?: string;                 // CSS class for dot
  cssClass?: string;               // CSS class for item
  disabled?: boolean;              // Disabled state
}
```

### Accessing Context in Template

Templates receive `props` object with structure:

```tsx
interface TemplateProps {
  item: TimelineItemModel;        // Current item object
  itemIndex: number;               // Index (0-based)
}
```

**Example accessing context:**

```tsx
const template = (props: any) => {
  // props.itemIndex - number (0, 1, 2, 3...)
  // props.item - the TimelineItemModel object
  // props.item.content - main content
  // props.item.oppositeContent - opposite side content
  // props.item.dotCss - dot styling classes
  // props.item.cssClass - item styling classes
  // props.item.disabled - disabled state
  
  return (
    <div>
      <h4>Item #{props.itemIndex}</h4>
      <p>{props.item.content}</p>
      <small>{props.item.oppositeContent}</small>
    </div>
  );
};

// Usage in both pattern approaches:

// Pattern 1 - Global template
<TimelineComponent template={template}>
  <ItemsDirective>...</ItemsDirective>
</TimelineComponent>

// Pattern 2 - Global template with items array
<TimelineComponent template={template} items={items} />
```

**Context Properties in Detail:**

| Property | Type | Description |
|----------|------|-------------|
| `props.itemIndex` | number | Zero-based index of current item (0, 1, 2...) |
| `props.item.content` | string/JSX | Main event text/template |
| `props.item.oppositeContent` | string/JSX | Secondary content (opposite side) |
| `props.item.dotCss` | string | CSS classes for dot (icons, colors) |
| `props.item.cssClass` | string | CSS classes for item styling |
| `props.item.disabled` | boolean | Whether item is disabled |

## Reverse Property

The `reverse` property inverts the display order of timeline items, making the last item appear first. This is useful for activity feeds, audit logs, and reverse chronological displays.

### Basic Reverse Example

```tsx
<TimelineComponent reverse={true}>
  <ItemsDirective>
    <ItemDirective content='Latest action' />
    <ItemDirective content='Previous action' />
    <ItemDirective content='Earlier action' />
  </ItemsDirective>
</TimelineComponent>
```

**Result:** Items display in reverse order (newest first).

### Reverse with Alignment

```tsx
<TimelineComponent 
  reverse={true}
  align='Alternate'
  orientation='Vertical'
>
  <ItemsDirective>
    <ItemDirective content='User logged out' oppositeContent='2:30 PM' />
    <ItemDirective content='User updated profile' oppositeContent='2:15 PM' />
    <ItemDirective content='User logged in' oppositeContent='1:00 PM' />
  </ItemsDirective>
</TimelineComponent>
```

### Use Cases for Reverse

```tsx
// Activity Feed (newest first)
function ActivityFeed() {
  return (
    <TimelineComponent reverse={true} align='Before'>
      <ItemsDirective>
        <ItemDirective 
          content='John commented' 
          oppositeContent='Just now' 
        />
        <ItemDirective 
          content='Jane submitted PR' 
          oppositeContent='5 min ago' 
        />
        <ItemDirective 
          content='Build passed' 
          oppositeContent='10 min ago' 
        />
      </ItemsDirective>
    </TimelineComponent>
  );
}

// Audit Log (most recent first)
function AuditLog() {
  return (
    <TimelineComponent reverse={true} align='Before'>
      <ItemsDirective>
        <ItemDirective 
          content='Admin deleted user' 
          oppositeContent='2:45 PM' 
        />
        <ItemDirective 
          content='Admin updated permissions' 
          oppositeContent='2:30 PM' 
        />
        <ItemDirective 
          content='New user created' 
          oppositeContent='2:00 PM' 
        />
      </ItemsDirective>
    </TimelineComponent>
  );
}
```

## Complex Template Examples

### Example 1: Card-Style Timeline

```tsx
interface TimelineEvent {
  title: string;
  description: string;
  date: string;
  status: 'success' | 'pending' | 'warning';
  author?: string;
}

const events: TimelineEvent[] = [
  {
    title: 'Project Approved',
    description: 'Client approved final design and approved budget',
    date: 'Mar 15, 2026',
    status: 'success',
    author: 'Project Manager'
  },
  {
    title: 'Design Review',
    description: 'Stakeholders reviewed and approved design mockups',
    date: 'Mar 10, 2026',
    status: 'success',
    author: 'Design Lead'
  },
  {
    title: 'Requirements Gathering',
    description: 'Collected business requirements from stakeholders',
    date: 'Mar 1, 2026',
    status: 'success',
    author: 'Business Analyst'
  }
];

function CardTimeline() {
  const cardTemplate = (props: any) => {
    const event = events[props.itemIndex];
    
    return (
      <div className="card-wrapper">
        <div className={`card card-${event.status}`}>
          <div className="card-header">
            <span className={`status-badge badge-${event.status}`}>
              {event.status}
            </span>
            <span className="card-date">{event.date}</span>
          </div>
          
          <div className="card-body">
            <h5 className="card-title">{event.title}</h5>
            <p className="card-description">{event.description}</p>
            {event.author && (
              <small className="card-author">by {event.author}</small>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div style={{ height: '600px', padding: '20px' }}>
      <TimelineComponent 
        template={cardTemplate}
        cssClass='card-timeline'
      >
        <ItemsDirective>
          {events.map((event, index) => (
            <ItemDirective key={index} content={event.title} />
          ))}
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

**CSS for Card Timeline:**

```css
.card-timeline {
  --dot-size: 16px;
  padding: 20px;
}

.card-wrapper {
  margin: 20px 0;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.card-success {
  border-left: 4px solid #28a745;
}

.card-pending {
  border-left: 4px solid #ffc107;
}

.card-warning {
  border-left: 4px solid #dc3545;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.status-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.badge-success {
  background-color: #d4edda;
  color: #155724;
}

.badge-pending {
  background-color: #fff3cd;
  color: #856404;
}

.badge-warning {
  background-color: #f8d7da;
  color: #721c24;
}

.card-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.card-description {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.card-author {
  color: #999;
  display: block;
}
```

### Example 2: Progress Timeline with Percentage

```tsx
interface ProjectPhase {
  name: string;
  progress: number;
  startDate: string;
  endDate: string;
}

const phases: ProjectPhase[] = [
  { name: 'Planning', progress: 100, startDate: 'Jan 1', endDate: 'Jan 15' },
  { name: 'Design', progress: 100, startDate: 'Jan 16', endDate: 'Feb 15' },
  { name: 'Development', progress: 65, startDate: 'Feb 16', endDate: 'Apr 15' },
  { name: 'Testing', progress: 0, startDate: 'Apr 16', endDate: 'May 15' }
];

function ProgressTimeline() {
  const progressTemplate = (props: any) => {
    const phase = phases[props.itemIndex];
    
    return (
      <div className="progress-item">
        <div className="progress-header">
          <h4>{phase.name}</h4>
          <span className="progress-percent">{phase.progress}%</span>
        </div>
        
        <div className="progress-bar-container">
          <div 
            className="progress-bar" 
            style={{ width: `${phase.progress}%` }}
          />
        </div>
        
        <div className="progress-dates">
          <span>{phase.startDate} - {phase.endDate}</span>
        </div>
      </div>
    );
  };

  return (
    <div style={{ height: '500px', padding: '20px' }}>
      <TimelineComponent 
        template={progressTemplate}
        orientation='Vertical'
        align='Before'
      >
        <ItemsDirective>
          {phases.map((phase, index) => (
            <ItemDirective key={index} content={phase.name} />
          ))}
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

**CSS for Progress Timeline:**

```css
.progress-item {
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-header h4 {
  margin: 0;
  font-size: 14px;
}

.progress-percent {
  font-weight: bold;
  color: #0066cc;
}

.progress-bar-container {
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #0066cc, #00d4ff);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-dates {
  font-size: 12px;
  color: #999;
}
```

## When to Use Templates

### Use Global Template When:
- ✅ Completely custom item structure needed
- ✅ Complex layouts beyond content + oppositeContent
- ✅ Interactive elements within items
- ✅ Consistent layout for all items
- ✅ Performance optimization needed (virtual rendering)

**Example:**

```tsx
// Full custom rendering needed
const customTemplate = (props: any) => (
  <div className="complex-item">
    <aside className="sidebar">
      <img src={props.item.imageUrl} />
    </aside>
    <main className="content">
      <h3>{props.item.title}</h3>
      <p>{props.item.description}</p>
      <button>Details</button>
    </main>
  </div>
);

<TimelineComponent template={customTemplate} />
```

### Use Item Content Template When:
- ✅ Only content needs customization
- ✅ Default dot and connector are fine
- ✅ Rich content formatting needed
- ✅ Templates vary per item
- ✅ Simpler implementation

**Example:**

```tsx
// Only content is different per item
<ItemDirective 
  content={(props: any) => (
    <div>
      <h4>Event Title</h4>
      <p>Description here</p>
    </div>
  )}
/>
```

### Use Standard Properties When:
- ✅ Simple text content sufficient
- ✅ Default styling meets requirements
- ✅ Performance is critical
- ✅ Minimal customization needed

**Example:**

```tsx
// Keep it simple
<ItemDirective 
  content="Simple event"
  oppositeContent="Date"
/>
```

### Performance Considerations

**Template Performance Tips:**
1. Avoid heavy computations in template functions
2. Memoize template functions if complex
3. Use CSS for styling over inline styles
4. Consider virtual scrolling for 100+ items
5. Profile with browser DevTools

**Example with Memoization:**

```tsx
const memoizedTemplate = React.useMemo(() => {
  return (props: any) => {
    // Complex template logic here
    return <div>Content</div>;
  };
}, [dependencies]);

<TimelineComponent template={memoizedTemplate} />
```
