# Visual Appearance & Customization in React Linear Gauge

See API Reference: [API Reference](api-reference.md)

## Table of Contents

- [Title](#title)
  - [Title Styling](#title-styling)
- [Gauge Dimensions](#gauge-dimensions)
  - [Using Container Div](#using-container-div)
  - [Using Component Props](#using-component-props)
  - [Margin and Padding](#margin-and-padding)
  - [Responsive Sizing](#responsive-sizing)
- [Background and Border](#background-and-border)
  - [Basic Background](#basic-background)
  - [Border Styling](#border-styling)
  - [Advanced Background](#advanced-background)
  - [Shadow Effect](#shadow-effect)
- [Themes and Color Schemes](#themes-and-color-schemes)
  - [Material Theme](#material-theme)
  - [Bootstrap Theme](#bootstrap-theme)
  - [Bootstrap 5 Theme](#bootstrap-5-theme)
  - [Fabric Theme](#fabric-theme)
  - [Tailwind CSS Theme](#tailwind-css-theme)
  - [High Contrast Theme](#high-contrast-theme)
- [Responsive Design](#responsive-design)
  - [Mobile-First Layout](#mobile-first-layout)
  - [Container Queries](#container-queries-modern-css)
  - [Media Queries](#media-queries)
- [CSS Class Customization](#css-class-customization)
  - [Using CSS Modules](#using-css-modules)
  - [Using Inline Styles](#using-inline-styles)
- [RTL Support](#rtl-support)
  - [Enable RTL](#enable-rtl)
  - [RTL in HTML](#rtl-in-html)
  - [Dynamic RTL Toggle](#dynamic-rtl-toggle)
- [Common Customization Patterns](#common-customization-patterns)
  - [Pattern 1: Modern Dashboard Gauge](#pattern-1-modern-dashboard-gauge)
  - [Pattern 2: Minimal/Clean Design](#pattern-2-minimalclean-design)
  - [Pattern 3: Dark Mode](#pattern-3-dark-mode)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Title

Add meaningful headings to your gauge:

```tsx
import React from 'react';
import { LinearGaugeComponent } from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <LinearGaugeComponent 
      title="Linear Gauge"
    >
      {/* axes, pointers, ranges */}
    </LinearGaugeComponent>
  );
}

export default App;
```

### Title Styling

```tsx
<LinearGaugeComponent 
  title="Temperature Monitor"
  titleStyle={{
    fontFamily: 'Arial',
    fontStyle: 'italic',
    fontWeight: 'bold',
    size: '18px',
    color: '#1976D2'
  }}
>
  {/* configuration */}
</LinearGaugeComponent>
```

**Title Style Properties:**
- `fontFamily` - Font name
- `fontStyle` - 'normal', 'italic', 'oblique'
- `fontWeight` - 'normal', 'bold', or numeric (100-900)
- `size` - Font size
- `color` - Text color (hex, rgb, or name)

## Gauge Dimensions

Control the size of the gauge container:

### Using Container Div

```tsx
<div style={{ height: '400px', width: '100%' }}>
  <LinearGaugeComponent>
    {/* configuration */}
  </LinearGaugeComponent>
</div>
```

### Using Component Props

```tsx
<LinearGaugeComponent
  width="100%"
  height="400px"
>
  {/* configuration */}
</LinearGaugeComponent>
```

### Margin and Padding

```tsx
<LinearGaugeComponent
  width="100%"
  height="500px"
  margin={{
    left: 20,
    right: 20,
    top: 20,
    bottom: 20
  }}
>
  {/* configuration */}
</LinearGaugeComponent>
```

### Responsive Sizing

```tsx
<div style={{ 
  height: '100vh',      // Full viewport height
  width: '100%'         // Full width
}}>
  <LinearGaugeComponent>
    {/* configuration */}
  </LinearGaugeComponent>
</div>
```

## Background and Border

Customize the gauge background and border:

### Basic Background

```tsx
<LinearGaugeComponent
  background="#FFFFFF"
>
  {/* configuration */}
</LinearGaugeComponent>
```

### Border Styling

```tsx
<LinearGaugeComponent
  border={{
    color: '#D3D3D3',   // Border color
    width: 2            // Border width
  }}
>
  {/* configuration */}
</LinearGaugeComponent>
```

### Advanced Background

```tsx
<LinearGaugeComponent
  background="linear-gradient(to bottom, #f5f5f5, #ffffff)"
  border={{
    color: '#1976D2',
    width: 2
  }}
>
  {/* configuration */}
</LinearGaugeComponent>
```

### Shadow Effect

```tsx
<div style={{
  padding: '10px',
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  borderRadius: '4px'
}}>
  <LinearGaugeComponent>
    {/* configuration */}
  </LinearGaugeComponent>
</div>
```

## Themes and Color Schemes

Syncfusion provides built-in themes. Import the appropriate theme CSS:

### Material Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/material.css';
```

### Bootstrap Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/bootstrap.css';
```

### Bootstrap 5 Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/bootstrap5.css';
```

### Fabric Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/fabric.css';
```

### Tailwind CSS Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/tailwind.css';
```

### High Contrast Theme

```tsx
import '@syncfusion/ej2-lineargauge/styles/highcontrast.css';
```

## Responsive Design

### Mobile-First Layout

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [orientation, setOrientation] = React.useState('Horizontal');

  React.useEffect(() => {
    // Detect screen size
    const handleResize = () => {
      if (window.innerWidth < 600) {
        setOrientation('Vertical');
      } else {
        setOrientation('Horizontal');
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div style={{ 
      width: '100%', 
      height: '100vh',
      padding: '10px',
      boxSizing: 'border-box'
    }}>
      <LinearGaugeComponent orientation={orientation}>
        {/* axes, pointers */}
      </LinearGaugeComponent>
    </div>
  );
}

export default App;
```

### Container Queries (Modern CSS)

```tsx
<div style={{
  containerType: 'size',
  width: '100%',
  height: '100vh'
}}>
  <LinearGaugeComponent width="100%" height="100%">
    {/* configuration */}
  </LinearGaugeComponent>
</div>
```

### Media Queries

```tsx
export function App() {
  const [width, setWidth] = React.useState('600px');
  const [height, setHeight] = React.useState('400px');

  React.useEffect(() => {
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    
    const handleChange = (e) => {
      if (e.matches) {
        setWidth('100%');
        setHeight('500px');
      } else {
        setWidth('600px');
        setHeight('400px');
      }
    };

    mediaQuery.addListener(handleChange);
    handleChange(mediaQuery);
    
    return () => mediaQuery.removeListener(handleChange);
  }, []);

  return (
    <LinearGaugeComponent width={width} height={height}>
      {/* configuration */}
    </LinearGaugeComponent>
  );
}
```

## CSS Class Customization

### Using CSS Modules

```tsx
// GaugeCustom.module.css
.gaugeContainer {
  background: linear-gradient(to bottom, #f0f0f0, #ffffff);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.gaugeTitle {
  color: #1976D2;
  font-weight: bold;
}
```

```tsx
// App.tsx
import styles from './GaugeCustom.module.css';
import { LinearGaugeComponent } from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <div className={styles.gaugeContainer}>
      <LinearGaugeComponent title="My Gauge">
        {/* configuration */}
      </LinearGaugeComponent>
    </div>
  );
}
```

### Using Inline Styles

```tsx
const gaugeStyle = {
  container: {
    background: '#f9f9f9',
    borderRadius: '8px',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
  },
  title: {
    color: '#1976D2',
    fontWeight: 'bold',
    marginBottom: '10px'
  }
};

export function App() {
  return (
    <div style={gaugeStyle.container}>
      <h2 style={gaugeStyle.title}>System Monitor</h2>
      <LinearGaugeComponent>
        {/* configuration */}
      </LinearGaugeComponent>
    </div>
  );
}
```

## RTL Support

Support right-to-left languages like Arabic and Hebrew:

### Enable RTL

```tsx
<LinearGaugeComponent enableRtl={true}>
  {/* configuration */}
</LinearGaugeComponent>
```

### RTL in HTML

```html
<html dir="rtl">
  <body>
    <div id="root"></div>
  </body>
</html>
```

### Dynamic RTL Toggle

```tsx
import React, { useState } from 'react';
import { LinearGaugeComponent } from '@syncfusion/ej2-react-lineargauge';

export function App() {
  const [rtl, setRtl] = useState(false);

  return (
    <div>
      <button onClick={() => setRtl(!rtl)}>
        {rtl ? 'English (LTR)' : 'العربية (RTL)'}
      </button>
      
      <LinearGaugeComponent enableRtl={rtl}>
        {/* configuration */}
      </LinearGaugeComponent>
    </div>
  );
}
```

## Common Customization Patterns

### Pattern 1: Modern Dashboard Gauge

```tsx
import React from 'react';
import { LinearGaugeComponent, AxesDirective, AxisDirective,
         RangesDirective, RangeDirective, PointersDirective, PointerDirective } 
  from '@syncfusion/ej2-react-lineargauge';

export function App() {
  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      borderRadius: '12px',
      color: 'white'
    }}>
      <LinearGaugeComponent
        title="CPU Usage"
        background='rgba(255, 255, 255, 0.95)'
        border={{ color: '#E0E0E0', width: 1 }}
        width="100%"
        height="300px"
      >
        <AxesDirective>
          <AxisDirective minimum={0} maximum={100} labelStyle={{ format: '{value}%' }}>
            <RangesDirective>
              <RangeDirective start={0} end={50} color='#4CAF50' />
              <RangeDirective start={50} end={75} color='#FFC107' />
              <RangeDirective start={75} end={100} color='#F44336' />
            </RangesDirective>
            <PointersDirective>
              <PointerDirective value={65} />
            </PointersDirective>
          </AxisDirective>
        </AxesDirective>
      </LinearGaugeComponent>
    </div>
  );
}
```

### Pattern 2: Minimal/Clean Design

```tsx
<LinearGaugeComponent
  title="Minimal Gauge"
  background="transparent"
  border={{ color: 'transparent' }}
  titleStyle={{ color: '#333' }}
  margin={{ top: 0, bottom: 0, left: 0, right: 0 }}
>
  {/* axes, pointers */}
</LinearGaugeComponent>
```

### Pattern 3: Dark Mode

```tsx
<LinearGaugeComponent
  background="#1E1E1E"
  border={{ color: '#333333', width: 1 }}
  titleStyle={{ color: '#FFFFFF' }}
>
  <AxesDirective>
    <AxisDirective 
      line={{ color: '#666666' }}
    >
      {/* ranges, pointers */}
    </AxisDirective>
  </AxesDirective>
</LinearGaugeComponent>
```

## Troubleshooting

**Q: Gauge not taking full width**
- Set `width="100%"` on component or parent div
- Verify parent container has explicit width

**Q: Title/labels cut off**
- Increase `height` of gauge
- Adjust `margin` to provide more space

**Q: Theme not applying**
- Verify CSS import is at top of file
- Check for conflicting global styles
- Clear browser cache

**Q: RTL text not rendering**
- Set `enableRtl={true}` on component
- Set `dir="rtl"` on HTML element
- Use appropriate font family for language

## Next Steps

- Read **Advanced Features** for animations and interactions
- Read **Accessibility** for inclusive design practices
- Read **Internationalization** for multi-language support
