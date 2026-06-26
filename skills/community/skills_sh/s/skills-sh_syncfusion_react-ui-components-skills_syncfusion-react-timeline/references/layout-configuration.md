# Layout Configuration

## Table of Contents
- [Orientation Overview](#orientation-overview)
- [Alignment Overview](#alignment-overview)
- [Vertical with Before](#vertical-with-before)
- [Vertical with After](#vertical-with-after)
- [Vertical Alternate](#vertical-alternate)
- [Horizontal Layouts](#horizontal-layouts)
- [Choosing Your Layout](#choosing-your-layout)
- [Globalization & Persistence](#globalization--persistence)

## Orientation Overview

The `orientation` property controls whether items flow vertically or horizontally. The default is `Vertical`.

### Vertical Orientation

Timeline items display top-to-bottom in a vertical stack:

```tsx
<TimelineComponent orientation='Vertical'>
  <ItemsDirective>
    <ItemDirective content='Day 1, 4:00 PM' oppositeContent='Check-in' />
    <ItemDirective content='Day 1, 7:00 PM' oppositeContent='Dinner' />
    <ItemDirective content='Day 2, 5:30 AM' oppositeContent='Sunrise' />
    <ItemDirective content='Day 2, 8:00 AM' oppositeContent='Breakfast' />
  </ItemsDirective>
</TimelineComponent>
```

**Best for:**
- Long lists of events
- Mobile-first designs
- Chronological activity feeds
- Single-column layouts

### Horizontal Orientation

Timeline items display left-to-right in a horizontal sequence:

```tsx
<TimelineComponent orientation='Horizontal'>
  <ItemsDirective>
    <ItemDirective content='Day 1, 4:00 PM' oppositeContent='Check-in' />
    <ItemDirective content='Day 1, 7:00 PM' oppositeContent='Dinner' />
    <ItemDirective content='Day 2, 5:30 AM' oppositeContent='Sunrise' />
    <ItemDirective content='Day 2, 8:00 AM' oppositeContent='Breakfast' />
  </ItemsDirective>
</TimelineComponent>
```

**Best for:**
- Wide desktop screens
- Process flow visualization
- Milestone progression
- Project roadmaps
- Limited number of events (3-8 items)

## Alignment Overview

The `align` property controls how content is positioned relative to the timeline axis. There are four alignment modes.

### Before Alignment

Content appears on one consistent side throughout the timeline.

**Vertical + Before:** Content on left, oppositeContent on right
**Horizontal + Before:** Content on top, oppositeContent on bottom

```tsx
<TimelineComponent orientation='Vertical' align='Before'>
  <ItemsDirective>
    <ItemDirective content='ReactJs' oppositeContent='Owned by Facebook' />
    <ItemDirective content='Angular' oppositeContent='Owned by Google' />
    <ItemDirective content='VueJs' oppositeContent='Owned by Evan you' />
    <ItemDirective content='Svelte' oppositeContent='Owned by Rich Harris' />
  </ItemsDirective>
</TimelineComponent>
```

**Use Before when:**
- Comparing main events with supplementary info
- One side needs emphasis
- Consistent layout aids readability

### After Alignment

Content positioning is reversed compared to Before alignment.

**Vertical + After:** Content on right, oppositeContent on left
**Horizontal + After:** Content on bottom, oppositeContent on top

```tsx
<TimelineComponent orientation='Vertical' align='After'>
  <ItemsDirective>
    <ItemDirective content='ReactJs' oppositeContent='Owned by Facebook' />
    <ItemDirective content='Angular' oppositeContent='Owned by Google' />
    <ItemDirective content='VueJs' oppositeContent='Owned by Evan you' />
    <ItemDirective content='Svelte' oppositeContent='Owned by Rich Harris' />
  </ItemsDirective>
</TimelineComponent>
```

**Use After when:**
- You want reversed positioning
- Mirror layout of Before alignment
- Different visual emphasis needed

### Alternate Alignment

Items alternate positions side-to-side, creating a zigzag pattern for visual variety.

```tsx
<TimelineComponent orientation='Vertical' align='Alternate'>
  <ItemsDirective>
    <ItemDirective content='ReactJs' oppositeContent='Owned by Facebook' />
    <ItemDirective content='Angular' oppositeContent='Owned by Google' />
    <ItemDirective content='VueJs' oppositeContent='Owned by Evan you' />
    <ItemDirective content='Svelte' oppositeContent='Owned by Rich Harris' />
  </ItemsDirective>
</TimelineComponent>
```

**Use Alternate when:**
- Displaying balanced comparisons
- Showing two parallel tracks
- Creating symmetrical timelines
- Highlighting alternating event types

### AlternateReverse Alignment

Inverse of Alternate, starting on the opposite side and reversing the alternation pattern.

```tsx
<TimelineComponent orientation='Vertical' align='Alternatereverse'>
  <ItemsDirective>
    <ItemDirective content='ReactJs' oppositeContent='Owned by Facebook' />
    <ItemDirective content='Angular' oppositeContent='Owned by Google' />
    <ItemDirective content='VueJs' oppositeContent='Owned by Evan you' />
    <ItemDirective content='Svelte' oppositeContent='Owned by Rich Harris' />
  </ItemsDirective>
</TimelineComponent>
```

**Use AlternateReverse when:**
- You need opposite alternation pattern
- Starting position differs from Alternate
- Different visual flow desired

## Horizontal Layouts

### Horizontal with Alternate (Most Common)

Ideal for milestone progression and roadmaps:

```tsx
<TimelineComponent orientation='Horizontal' align='Alternate'>
  <ItemsDirective>
    <ItemDirective content='Planning' oppositeContent='Q1' />
    <ItemDirective content='Development' oppositeContent='Q2' />
    <ItemDirective content='Testing' oppositeContent='Q3' />
    <ItemDirective content='Launch' oppositeContent='Q4' />
  </ItemsDirective>
</TimelineComponent>
```

**Benefits:**
- Balanced visual layout
- Utilizes width effectively
- Professional appearance
- Good for presentations

## Choosing Your Layout

| Use Case | Orientation | Align | Reason |
|----------|-------------|-------|--------|
| Activity feed | Vertical | Before | Simple chronological list |
| Career timeline | Vertical | Alternate | Balanced comparison |
| Project roadmap | Horizontal | Alternate | Wide display, milestone focus |
| Process flow | Horizontal | Before | Sequential steps, one-sided |
| Before/after | Vertical | Alternate | Visual comparison |
| Shipping tracking | Vertical | Before | Simple progression |
| Company history | Vertical | Alternate | Balanced timeline |

## Content Positioning Rules

### Important Positioning Rules

1. **oppositeContent only displays when align mode supports it:**
   - `Before`: Main content left/top, opposite right/bottom
   - `After`: Main content right/bottom, opposite left/top
   - `Alternate`: Alternates sides for both content and opposite
   - `AlternateReverse`: Reverse alternation starting position

2. **Container must have height:** Timeline won't flow without explicit height

3. **Horizontal timelines need width:** Ensure parent container has sufficient width

4. **Orientation + Align combine:** Both properties work together for final layout

**Example: Responsive Design**

```tsx
function ResponsiveTimeline() {
  const isSmallScreen = window.innerWidth < 768;
  
  return (
    <div style={{ height: isSmallScreen ? '600px' : '400px' }}>
      <TimelineComponent 
        orientation={isSmallScreen ? 'Vertical' : 'Horizontal'}
        align={isSmallScreen ? 'Before' : 'Alternate'}
      >
        <ItemsDirective>
          <ItemDirective content='Event 1' oppositeContent='Date 1' />
          <ItemDirective content='Event 2' oppositeContent='Date 2' />
          <ItemDirective content='Event 3' oppositeContent='Date 3' />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

This switches to Vertical/Before on mobile for better readability.

## Globalization & Persistence

### Locale Property

Set the component locale for multilingual support:

```tsx
<TimelineComponent locale='es'>
  <ItemsDirective>
    <ItemDirective content='Evento 1' />
    <ItemDirective content='Evento 2' />
  </ItemsDirective>
</TimelineComponent>
```

**Supported locales:** en-US (default), es, fr, de, ja, ar, and many more.

### Enable RTL (Right-to-Left)

Enable RTL layout for languages like Arabic, Hebrew, and Urdu:

```tsx
<TimelineComponent enableRtl={true}>
  <ItemsDirective>
    <ItemDirective content='الحدث الأول' />
    <ItemDirective content='الحدث الثاني' />
  </ItemsDirective>
</TimelineComponent>
```

Combine with locale: `<TimelineComponent enableRtl={true} locale='ar'>`

### Enable Persistence

Persist component state between page reloads:

```tsx
<TimelineComponent enablePersistence={true}>
  <ItemsDirective>
    <ItemDirective content='Step 1' />
    <ItemDirective content='Step 2' />
  </ItemsDirective>
</TimelineComponent>
```

**Use case:** Multi-step wizards where users return to their position later.
