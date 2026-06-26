# Header Styling & Customization

## Table of Contents
- [Built-In Header Styles](#built-in-header-styles)
- [Icon Positioning](#icon-positioning)
- [Icon Customization](#icon-customization)
- [Custom Styling](#custom-styling)
- [Styling Examples](#styling-examples)

## Built-In Header Styles

The Tab component provides predefined CSS classes to style tab headers. Apply these classes directly to the `TabComponent` element.

### Style Class: `e-fill`

**Effect**: Selected tab header background is solid fill with highlight

```jsx
<TabComponent className="e-fill">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

**When to use**: For prominent active tab indication with solid background color.

### Style Class: `e-background`

**Effect**: Tab header has solid fill background, selected header has highlighted border

```jsx
<TabComponent className="e-background">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

**When to use**: For subtle tab indication with border highlighting.

### Style Class: `e-background e-accent`

**Effect**: Tab header has solid fill background, selected header highlighted with accent color

```jsx
<TabComponent className="e-background e-accent">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

**When to use**: For branded or accent-colored tab highlighting. Most visually distinctive option.

### Default Style (No Class)

Without any class, the Tab component uses default styling with underline indication for active tabs.

```jsx
<TabComponent>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
  </TabItemsDirective>
</TabComponent>
```

**When to use**: For minimal, clean interface with simple underline styling.

## Icon Positioning

Each tab header item can position its icon using the `iconPosition` property defined within the header model. This property works in conjunction with the `iconCss` property to customize icon placement.

### Icon Positions

| Position | Description | Use Case |
|----------|-------------|----------|
| `Left` | Icon on the left of text (default) | Standard icon-text layout |
| `Right` | Icon on the right of text | Right-aligned icon design |
| `Top` | Icon above text | Vertical icon-text stacking |
| `Bottom` | Icon below text | Icon below label design |

### Example: Icon Position Configuration (Left)

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function IconPositionLeftExample() {
  return (
    <TabComponent>
      <TabItemsDirective>
        <TabItemDirective 
          header={{ 
            text: 'Home', 
            iconCss: 'e-icons e-home',
            iconPosition: 'Left'
          }} 
          content="Home content" 
        />
        <TabItemDirective 
          header={{ 
            text: 'Profile', 
            iconCss: 'e-icons e-user',
            iconPosition: 'Left'
          }} 
          content="Profile content" 
        />
        <TabItemDirective 
          header={{ 
            text: 'Settings', 
            iconCss: 'e-icons e-settings',
            iconPosition: 'Left'
          }} 
          content="Settings content" 
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### Icon Position: Top

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function IconPositionTopExample() {
  return (
    <TabComponent>
      <TabItemsDirective>
        <TabItemDirective 
          header={{ 
            text: 'Dashboard', 
            iconCss: 'e-icons e-dashboard',
            iconPosition: 'Top'
          }} 
          content="Dashboard content" 
        />
        <TabItemDirective 
          header={{ 
            text: 'Analytics', 
            iconCss: 'e-icons e-chart-pie',
            iconPosition: 'Top'
          }} 
          content="Analytics content" 
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### Icon Position: Dynamic Change

```jsx
import React, { useRef } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';

export default function DynamicIconPositionExample() {
  const tabRef = useRef(null);
  const dropRef = useRef(null);

  const handlePositionChange = () => {
    const newPosition = dropRef.current.value;
    const items = tabRef.current.items;
    
    for (let i = 0; i < items.length; i++) {
      items[i].header.iconPosition = newPosition;
    }
  };

  const positionOptions = [
    { text: 'Left', value: 'Left' },
    { text: 'Right', value: 'Right' },
    { text: 'Top', value: 'Top' },
    { text: 'Bottom', value: 'Bottom' }
  ];

  return (
    <div>
      <label>Select Icon Position:</label>
      <DropDownListComponent 
        ref={dropRef}
        dataSource={positionOptions}
        fields={{ text: 'text', value: 'value' }}
        value="Left"
        change={handlePositionChange}
      />
      
      <TabComponent ref={tabRef}>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ 
              text: 'Messages', 
              iconCss: 'e-icons e-message',
              iconPosition: 'Left'
            }} 
            content="Messages content" 
          />
          <TabItemDirective 
            header={{ 
              text: 'Users', 
              iconCss: 'e-icons e-people',
              iconPosition: 'Left'
            }} 
            content="Users content" 
          />
          <TabItemDirective 
            header={{ 
              text: 'Settings', 
              iconCss: 'e-icons e-settings',
              iconPosition: 'Left'
            }} 
            content="Settings content" 
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

## Icon Customization

Use the `iconCss` property in the header object to specify custom icon CSS classes.

### Available Icon Classes

Syncfusion provides icon classes prefixed with `e-icons e-`. Common examples:

- `e-icons e-home` - Home icon
- `e-icons e-user` - User/Profile icon
- `e-icons e-settings` - Settings icon
- `e-icons e-mail` - Mail/Message icon
- `e-icons e-chart-pie` - Chart icon
- `e-icons e-dashboard` - Dashboard icon
- `e-icons e-folder` - Folder icon
- `e-icons e-file` - File icon

### Example: Icon-Heavy Tab

```jsx
<TabComponent className="e-fill" iconPosition="Top">
  <TabItemsDirective>
    <TabItemDirective 
      header={{ 
        text: 'Dashboard', 
        iconCss: 'e-icons e-dashboard' 
      }} 
      content="Dashboard metrics and analytics" 
    />
    <TabItemDirective 
      header={{ 
        text: 'Users', 
        iconCss: 'e-icons e-people' 
      }} 
      content="User management" 
    />
    <TabItemDirective 
      header={{ 
        text: 'Reports', 
        iconCss: 'e-icons e-report' 
      }} 
      content="Report generation and viewing" 
    />
    <TabItemDirective 
      header={{ 
        text: 'Settings', 
        iconCss: 'e-icons e-settings' 
      }} 
      content="System configuration" 
    />
  </TabItemsDirective>
</TabComponent>
```

## Custom Styling

### CSS Selectors for Tab Components

Beyond built-in classes, you can apply custom CSS:

**Tab container:**
```css
.e-tab {
  border: 5px solid rgb(173, 255, 47);
}
```

**Tab header section:**
```css
.e-tab .e-tab-header {
  background: #badfba !important;
}
```

**Tab header items/toolbar:**
```css
.e-tab .e-tab-header .e-toolbar-items {
  background: #9faed8;
  border: 2px solid blue;
}
```

**Tab header icons:**
```css
.e-tab .e-tab-header .e-toolbar-item .e-tab-icon {
  color: #badfba !important;
}
```

**Tab content section:**
```css
.e-tab .e-content {
  background: #d1f6d1 !important;
}
```

**Tab content items:**
```css
.e-tab .e-content .e-item {
  color: #a78515;
  font-size: 14px;
}
```

**Tab hover state:**
```css
.e-tab .e-tab-header .e-toolbar-item .e-tab-wrap:hover {
  background: #d1f6d1 !important;
}
```

**Tab popup icon (overflow):**
```css
.e-tab .e-tab-header .e-tab-wrap .e-popup-icon:hover {
  background: #d1f6d1 !important;
}
```

## Styling Examples

### Example 1: Modern Professional Style

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function ProfessionalTab() {
  return (
    <div style={{ padding: '20px' }}>
      <style>{`
        .professional-tab .e-tab-header {
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .professional-tab .e-tab-header .e-toolbar-item .e-tab-text {
          color: white;
          font-weight: 500;
          padding: 12px 20px;
        }
        
        .professional-tab .e-tab-header .e-toolbar-item.e-active .e-tab-text {
          border-bottom: 3px solid white;
        }
        
        .professional-tab .e-content {
          background: #f8f9fa;
          padding: 20px;
        }
      `}</style>
      
      <TabComponent className="professional-tab">
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Overview' }}
            content="Account overview and quick statistics"
          />
          <TabItemDirective 
            header={{ text: 'Activity' }}
            content="Recent activity and logs"
          />
          <TabItemDirective 
            header={{ text: 'Settings' }}
            content="Account settings and preferences"
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Example 2: Icon Tabs with Background

```jsx
<TabComponent className="e-background e-accent" iconPosition="Top">
  <TabItemsDirective>
    <TabItemDirective 
      header={{ 
        text: 'Orders', 
        iconCss: 'e-icons e-cart' 
      }}
      content="Order management and history"
    />
    <TabItemDirective 
      header={{ 
        text: 'Payments', 
        iconCss: 'e-icons e-money' 
      }}
      content="Payment methods and history"
    />
    <TabItemDirective 
      header={{ 
        text: 'Shipments', 
        iconCss: 'e-icons e-shipping' 
      }}
      content="Shipment tracking and status"
    />
  </TabItemsDirective>
</TabComponent>
```

### Example 3: Minimal Clean Style

```jsx
<TabComponent>
  <TabItemsDirective>
    <TabItemDirective 
      header={{ text: 'Description' }}
      content="Product description goes here"
    />
    <TabItemDirective 
      header={{ text: 'Reviews' }}
      content="Customer reviews section"
    />
    <TabItemDirective 
      header={{ text: 'Specifications' }}
      content="Technical specifications"
    />
  </TabItemsDirective>
</TabComponent>
```

## Best Practices

1. **Choose style class based on importance**: Use `e-fill` for primary navigation, default for secondary
2. **Icon positioning**: Use `Left` or `Right` for horizontal layouts, `Top` or `Bottom` for compact designs
3. **Consistency**: Apply consistent styling across all tabs in your application
4. **Accessibility**: Ensure sufficient color contrast and don't rely on color alone to indicate state
5. **Performance**: Use CSS classes instead of inline styles for better performance and maintainability
