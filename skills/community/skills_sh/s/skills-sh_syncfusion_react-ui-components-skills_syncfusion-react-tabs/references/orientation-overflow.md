# Orientation & Overflow Modes

## Table of Contents
- [Header Placement Positions](#header-placement-positions)
- [Overflow Modes](#overflow-modes)
- [Scrollable Mode](#scrollable-mode)
- [Popup Mode](#popup-mode)
- [Responsive Configuration](#responsive-configuration)

## Header Placement Positions

Control where tab headers appear relative to content using the `headerPlacement` property.

### Position: Top (Default)

Headers are arranged horizontally above the content.

```jsx
<TabComponent headerPlacement="Top">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

**Use cases:**
- Standard navigation layouts
- Web applications with horizontal navigation
- Desktop interfaces

### Position: Bottom

Headers are arranged horizontally below the content.

```jsx
<TabComponent headerPlacement="Bottom">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

**Use cases:**
- Bottom navigation bars
- Mobile-style navigation
- Status indicators at bottom

### Position: Left

Headers are arranged vertically on the left side, content on the right.

```jsx
<TabComponent headerPlacement="Left">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Dashboard' }} content="Dashboard content" />
    <TabItemDirective header={{ text: 'Users' }} content="Users content" />
    <TabItemDirective header={{ text: 'Reports' }} content="Reports content" />
    <TabItemDirective header={{ text: 'Settings' }} content="Settings content" />
  </TabItemsDirective>
</TabComponent>
```

**Use cases:**
- Sidebar navigation layouts
- Wide-screen applications
- Multi-level navigation menus

### Position: Right

Headers are arranged vertically on the right side, content on the left.

```jsx
<TabComponent headerPlacement="Right">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Overview' }} content="Overview content" />
    <TabItemDirective header={{ text: 'Details' }} content="Details content" />
    <TabItemDirective header={{ text: 'History' }} content="History content" />
  </TabItemsDirective>
</TabComponent>
```

**Use cases:**
- Right-to-left (RTL) language layouts
- Right-side navigation panels
- Asymmetric design patterns

## Overflow Modes

When tab headers exceed the available space, the component handles overflow using different modes.

### Mode: Scrollable (Default)

**How it works:**
- Single-line horizontal display with navigation arrows
- Left/right arrow buttons at start/end of header
- Click or hold arrow to scroll through tabs
- Touch/swipe support on mobile devices

```jsx
<TabComponent overflowMode="Scrollable">
  <TabItemsDirective>
    {Array.from({ length: 20 }, (_, i) => (
      <TabItemDirective 
        key={i}
        header={{ text: `Tab ${i + 1}` }} 
        content={`Content ${i + 1}`} 
      />
    ))}
  </TabItemsDirective>
</TabComponent>
```

**Visual behavior:**
- Left navigation arrow initially disabled
- Right arrow enabled when tabs overflow right
- Arrows toggle based on scroll position

**Mobile behavior:**
- No navigation arrows on touch devices
- Swipe left/right to scroll through tabs
- Smooth momentum scrolling

**Advantages:**
- All tab headers visible (with navigation)
- Compact vertical footprint
- Intuitive scrolling interaction

**Disadvantages:**
- May be slow to reach tabs far to the right
- Navigation arrows take screen space

### Mode: Popup

**How it works:**
- Only tabs fitting available space are displayed
- Overflow tabs moved to dropdown menu
- Dropdown icon at header end to view hidden tabs
- Scrollable dropdown if many tabs exceed visible area

```jsx
<TabComponent overflowMode="Popup">
  <TabItemsDirective>
    {Array.from({ length: 20 }, (_, i) => (
      <TabItemDirective 
        key={i}
        header={{ text: `Tab ${i + 1}` }} 
        content={`Content ${i + 1}`} 
      />
    ))}
  </TabItemsDirective>
</TabComponent>
```

**Visual behavior:**
- Visible tabs displayed in header
- Dropdown icon appears when tabs overflow
- Click dropdown to see hidden tabs
- Popup scrolls if many hidden tabs

**Mobile behavior:**
- Same dropdown interaction
- Tap dropdown arrow to show hidden tabs
- Scrollable list if dropdown exceeds screen height

**Advantages:**
- Cleaner header appearance
- Fast access to any tab via dropdown
- Compact for many tabs

**Disadvantages:**
- Hidden tabs not immediately visible
- Extra click/tap needed to access hidden tabs

## Scrollable Mode

### Configuration

```jsx
<TabComponent 
  overflowMode="Scrollable"
  width="800px"
  height="300px"
>
  <TabItemsDirective>
    {/* Tab items */}
  </TabItemsDirective>
</TabComponent>
```

### Navigation Control

**Programmatic scrolling:**
```jsx
import React, { useRef } from 'react';

export default function ScrollableTabExample() {
  const tabRef = useRef(null);

  const handleScroll = (direction) => {
    // Tab component provides scroll methods
    // Use tabRef.current to access component
  };

  return (
    <div>
      <button onClick={() => handleScroll('left')}>← Scroll Left</button>
      <button onClick={() => handleScroll('right')}>Scroll Right →</button>
      
      <TabComponent ref={tabRef} overflowMode="Scrollable">
        <TabItemsDirective>
          {/* Tabs */}
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Touch and Swipe Support

Scrollable mode automatically supports touch gestures:

- **Swipe left**: Scroll tabs to right
- **Swipe right**: Scroll tabs to left
- **Momentum scrolling**: Smooth deceleration after swipe

No additional configuration needed—works automatically on touch devices.

## Popup Mode

### Dropdown Behavior

When overflowMode="Popup", hidden tabs appear in a dropdown:

```jsx
<TabComponent overflowMode="Popup">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Home' }} content="Home content" />
    <TabItemDirective header={{ text: 'About' }} content="About content" />
    {/* More tabs that may overflow */}
  </TabItemsDirective>
</TabComponent>
```

**Dropdown features:**
- Click dropdown arrow to open/close menu
- Keyboard navigation in dropdown (arrow keys)
- Click tab in dropdown to switch to it
- Dropdown closes after tab selection

### Dropdown Scrolling

If many tabs overflow:

```jsx
<TabComponent 
  overflowMode="Popup"
  width="600px"
>
  <TabItemsDirective>
    {Array.from({ length: 50 }, (_, i) => (
      <TabItemDirective 
        key={i}
        header={{ text: `Tab ${i + 1}` }} 
        content={`Content ${i + 1}`} 
      />
    ))}
  </TabItemsDirective>
</TabComponent>
```

**Behavior:**
- First tabs fit in header area
- Remaining tabs scroll in popup dropdown
- Dropdown scrollbar appears automatically if needed

## Responsive Configuration

### Width and Height

Control tab container dimensions:

```jsx
<TabComponent 
  width="100%"
  height="400px"
  overflowMode="Scrollable"
>
  <TabItemsDirective>
    {/* Tabs */}
  </TabItemsDirective>
</TabComponent>
```

**Valid values:**
- Pixel values: `"800px"`, `"400px"`
- Percentage: `"100%"`, `"50%"`
- CSS units: `"20em"`, `"5rem"`

### Dynamic Width Adjustment

```jsx
import React, { useState } from 'react';

export default function ResponsiveTab() {
  const [containerWidth, setContainerWidth] = useState('100%');

  return (
    <div>
      <button onClick={() => setContainerWidth('600px')}>Narrow</button>
      <button onClick={() => setContainerWidth('100%')}>Full Width</button>
      
      <TabComponent 
        width={containerWidth}
        overflowMode="Scrollable"
      >
        <TabItemsDirective>
          {/* Tabs */}
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Vertical Overflow (Left/Right Placement)

When using `headerPlacement="Left"` or `"Right"`, overflow is vertical:

```jsx
<TabComponent 
  headerPlacement="Left"
  overflowMode="Scrollable"
  height="300px"
>
  <TabItemsDirective>
    {Array.from({ length: 20 }, (_, i) => (
      <TabItemDirective 
        key={i}
        header={{ text: `Tab ${i + 1}` }} 
        content={`Content ${i + 1}`} 
      />
    ))}
  </TabItemsDirective>
</TabComponent>
```

**Behavior:**
- Headers arranged vertically
- Up/down navigation arrows for overflow
- Swipe up/down on mobile

## Real-World Examples

### Example 1: Full-Width Responsive Tabs

```jsx
<TabComponent 
  width="100%" 
  overflowMode="Scrollable"
  headerPlacement="Top"
>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Products' }} content="Products catalog" />
    <TabItemDirective header={{ text: 'Pricing' }} content="Pricing information" />
    <TabItemDirective header={{ text: 'Features' }} content="Feature comparison" />
    <TabItemDirective header={{ text: 'Documentation' }} content="Docs and guides" />
    <TabItemDirective header={{ text: 'Support' }} content="Support resources" />
  </TabItemsDirective>
</TabComponent>
```

### Example 2: Sidebar Navigation with Vertical Tabs

```jsx
<div style={{ display: 'flex', height: '100vh' }}>
  <TabComponent 
    headerPlacement="Left"
    overflowMode="Scrollable"
    height="100%"
    width="250px"
  >
    <TabItemsDirective>
      <TabItemDirective 
        header={{ text: 'Dashboard', iconCss: 'e-icons e-dashboard' }}
        content="Dashboard metrics"
      />
      <TabItemDirective 
        header={{ text: 'Users', iconCss: 'e-icons e-people' }}
        content="User management"
      />
      {/* More tabs */}
    </TabItemsDirective>
  </TabComponent>
  
  <div style={{ flex: 1, padding: '20px' }}>
    {/* Main content */}
  </div>
</div>
```

### Example 3: Compact Popup Dropdown

```jsx
<TabComponent 
  overflowMode="Popup"
  width="500px"
  className="e-background"
>
  <TabItemsDirective>
    {Array.from({ length: 15 }, (_, i) => (
      <TabItemDirective 
        key={i}
        header={{ text: `Section ${i + 1}` }} 
        content={`Content for section ${i + 1}`} 
      />
    ))}
  </TabItemsDirective>
</TabComponent>
```

## Best Practices

1. **Choose mode based on tab count:**
   - **Scrollable** for up to 10-12 tabs
   - **Popup** for 10+ tabs to keep header clean

2. **Use appropriate placement:**
   - **Top**: Standard horizontal navigation
   - **Left**: Sidebar layouts for multi-section apps
   - **Bottom**: Mobile-friendly or tab toolbars

3. **Set reasonable container width:**
   - Allow tabs to fit naturally
   - Avoid forcing overflow on desktop
   - Use responsive sizing (100%) for flexibility

4. **Test on multiple devices:**
   - Desktop mouse/arrow interactions
   - Mobile swipe/touch interactions
   - Tablet intermediate sizes
