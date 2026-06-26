# Appearance and Styling

## Table of Contents
- [Link Styling](#link-styling)
  - [Link Style Properties](#link-style-properties)
  - [Basic Link Styling Example](#basic-link-styling-example)
  - [Opacity Variations](#opacity-variations)
  - [Curvature Variations](#curvature-variations)
  - [Color Type Strategies](#color-type-strategies)
    - [Source Color (Default)](#source-color-default)
    - [Target Color](#target-color)
- [Node Appearance](#node-appearance)
  - [Node Color Assignment](#node-color-assignment)
  - [Node Label Styling](#node-label-styling)
- [Theme Customization](#theme-customization)
- [Color Schemes](#color-schemes)
  - [Professional Color Palette](#professional-color-palette)
  - [Energy Sector Color Scheme](#energy-sector-color-scheme)
  - [Heat Map Color Scheme](#heat-map-color-scheme)
- [Theming](#theming)
  - [Chart Background and Borders](#chart-background-and-borders)
  - [Text Styling (Titles and Labels)](#text-styling-titles-and-labels)
- [Responsive Styling](#responsive-styling)
  - [Adaptive Sizing](#adaptive-sizing)
  - [Dark Mode Support](#dark-mode-support)
- [Best Practices](#best-practices)

## Link Styling

Customize how links (connections between nodes) appear in your diagram.

### Link Style Properties

```tsx
<SankeyComponent
  linkStyle={{
    opacity: 0.6,           // Transparency: 0 (invisible) to 1 (opaque)
    curvature: 0.55,        // Curve intensity: 0 (straight) to 1 (highly curved)
    colorType: 'Source'     // Color inheritance: 'Source' or 'Target'
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Basic Link Styling Example

```tsx
<SankeyComponent
  title="Styled Links"
  linkStyle={{
    opacity: 0.5,
    curvature: 0.6,
    colorType: 'Source'
  }}
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="A" color="#FF6B6B" />
    <SankeyNodeDirective id="B" color="#4ECDC4" />
    <SankeyNodeDirective id="C" color="#45B7D1" />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    <SankeyLinkDirective sourceId="A" targetId="C" value={100} />
    <SankeyLinkDirective sourceId="B" targetId="C" value={75} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Opacity Variations

Control transparency for different visual effects:

| Opacity | Effect | Use Case |
|---------|--------|----------|
| 0.3 | Very transparent | Background flows, less important data |
| 0.5 | Semi-transparent | Standard visualization |
| 0.7 | Mostly opaque | Emphasized flows |
| 1.0 | Fully opaque | Critical data, high contrast |

```tsx
<SankeyComponent
  title="Opacity Levels"
  linkStyle={{
    opacity: 0.6,          // Start with 0.6
    curvature: 0.55
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Curvature Variations

Adjust link curves for different visual preferences:

| Curvature | Shape | Best For |
|-----------|-------|----------|
| 0 | Straight lines | Linear flows, simple diagrams |
| 0.3 | Slight curves | Moderate complexity |
| 0.55 | Medium curves | Balanced appearance (default) |
| 0.8 | Heavy curves | Dense diagrams, clarity |
| 1.0 | Maximum curves | Artistic effect |

```tsx
<SankeyComponent
  title="Different Curvatures"
>
  <SankeyNodesCollectionDirective>
    {/* nodes */}
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    {/* links */}
  </SankeyLinksCollectionDirective>
</SankeyComponent>
```

### Color Type Strategies

#### Source Color (Default)

Links inherit color from their source node:

```tsx
<SankeyComponent
  linkStyle={{
    colorType: 'Source'
  }}
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective id="Solar" color="#FFD700" />
    <SankeyNodeDirective id="Wind" color="#87CEEB" />
    <SankeyNodeDirective id="Output" color="#C0C0C0" />
  </SankeyNodesCollectionDirective>
  <SankeyLinksCollectionDirective>
    {/* Links from Solar appear gold, from Wind appear blue */}
    <SankeyLinkDirective sourceId="Solar" targetId="Output" value={450} />
    <SankeyLinkDirective sourceId="Wind" targetId="Output" value={200} />
  </SankeyLinksCollectionDirective>
  <Inject services={[SankeyTooltip]} />
</SankeyComponent>
```

#### Target Color

Links inherit color from destination node:

```tsx
<SankeyComponent
  linkStyle={{
    colorType: 'Target'
  }}
>
  {/* All links pointing to same destination get same color */}
</SankeyComponent>
```

## Node Appearance

### Node Color Assignment

```tsx
<SankeyNodesCollectionDirective>
  <SankeyNodeDirective 
    id="Solar"
    color="#FFD700"           // Gold
    label={{ text: 'Solar' }}
  />
  <SankeyNodeDirective 
    id="Wind"
    color="#87CEEB"           // Sky blue
    label={{ text: 'Wind' }}
  />
</SankeyNodesCollectionDirective>
```

### Node Label Styling

```tsx
<SankeyNodeDirective
  id="Node1"
  label={{
    text: 'Styled Label',
    fill: '#333333',          // Text color
    fontSize: 12,
    fontFamily: 'Arial',
    textOpacity: 0.9
  }}
/>
```

## Theme Customization

**Available themes (18+ including dark & high contrast):**
- Material, MaterialDark, Material3, Material3Dark
- Fabric, FabricDark
- Bootstrap, BootstrapDark, Bootstrap4, Bootstrap5, Bootstrap5Dark, Bootstrap5.3, Bootstrap5.3Dark
- Tailwind, TailwindDark
- Fluent, FluentDark, Fluent2, Fluent2Dark, Fluent2HighContrast
- HighContrast, HighContrastLight

Switch via the `theme` prop:

```tsx
<SankeyComponent theme='Material3Dark'>
  {/* Sankey content */}
</SankeyComponent>
```

## Color Schemes

### Professional Color Palette

```tsx
const professionalColors = {
  primary: ['#0066CC', '#003399', '#003366'],
  secondary: ['#FF6B6B', '#FF8787', '#FFB3B3'],
  neutral: ['#666666', '#999999', '#CCCCCC']
};

<SankeyNodesCollectionDirective>
  <SankeyNodeDirective id="A" color={professionalColors.primary[0]} />
  <SankeyNodeDirective id="B" color={professionalColors.primary[1]} />
  <SankeyNodeDirective id="C" color={professionalColors.secondary[0]} />
</SankeyNodesCollectionDirective>
```

### Energy Sector Color Scheme

```tsx
const energyColors = {
  renewable: {
    solar: '#FFD700',
    wind: '#87CEEB',
    hydro: '#20B2AA'
  },
  fossil: {
    coal: '#696969',
    gas: '#FFA07A',
    oil: '#8B4513'
  },
  output: {
    residential: '#FF69B4',
    commercial: '#00CED1',
    industrial: '#9370DB'
  }
};

<SankeyNodesCollectionDirective>
  <SankeyNodeDirective id="Solar" color={energyColors.renewable.solar} />
  <SankeyNodeDirective id="Wind" color={energyColors.renewable.wind} />
  <SankeyNodeDirective id="Coal" color={energyColors.fossil.coal} />
  <SankeyNodeDirective id="Residential" color={energyColors.output.residential} />
</SankeyNodesCollectionDirective>
```

### Heat Map Color Scheme

Use gradient colors to represent intensity:

```tsx
function getColorForValue(value, min, max) {
  const ratio = (value - min) / (max - min);
  
  // Red (low) to Green (high)
  if (ratio < 0.5) {
    return '#FF6B6B';  // Red
  } else if (ratio < 0.75) {
    return '#FFD700';  // Yellow
  } else {
    return '#32CD32';  // Green
  }
}

const minValue = 50;
const maxValue = 500;

<SankeyNodesCollectionDirective>
  <SankeyNodeDirective 
    id="HighValue" 
    color={getColorForValue(450, minValue, maxValue)}
  />
  <SankeyNodeDirective 
    id="LowValue" 
    color={getColorForValue(100, minValue, maxValue)}
  />
</SankeyNodesCollectionDirective>
```

## Theming

### Chart Background and Borders

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="Themed Chart"
  background="#F5F5F5"
  border={{
    color: '#CCCCCC',
    width: 1
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Text Styling (Titles and Labels)

```tsx
<SankeyComponent
  title="Styled Title"
  subTitle="Styled Subtitle"
  titleStyle={{
    fontFamily: 'Segoe UI',
    size: '16px',
    bold: true,
    color: '#2E3440'
  }}
  subTitleStyle={{
    fontFamily: 'Segoe UI',
    size: '12px',
    color: '#555555'
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

## Responsive Styling

### Adaptive Sizing

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  width={Browser.isDevice ? '100%' : '90%'}
  height={Browser.isDevice ? '600px' : '420px'}
  labelSettings={{
    fontSize: Browser.isDevice ? 10 : 12
  }}
  linkStyle={{
    opacity: Browser.isDevice ? 0.7 : 0.6,
    curvature: Browser.isDevice ? 0.7 : 0.55
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Dark Mode Support

```tsx
import React, { useState } from 'react';

function ThemedSankey() {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const themes = {
    light: {
      background: '#FFFFFF',
      linkOpacity: 0.6,
      linkColor: 'Source',
      nodeColors: ['#FF6B6B', '#4ECDC4', '#45B7D1'],
      textColor: '#333333'
    },
    dark: {
      background: '#1E1E1E',
      linkOpacity: 0.5,
      linkColor: 'Source',
      nodeColors: ['#FF7675', '#55EFC4', '#74B9FF'],
      textColor: '#ECEFF4'
    }
  };

  const theme = isDarkMode ? themes.dark : themes.light;

  return (
    <div>
      <button onClick={() => setIsDarkMode(!isDarkMode)}>
        Toggle Dark Mode
      </button>

      <SankeyComponent
        background={theme.background}
        linkStyle={{
          opacity: theme.linkOpacity,
          colorType: theme.linkColor
        }}
      >
        <SankeyNodesCollectionDirective>
          {theme.nodeColors.map((color, i) => (
            <SankeyNodeDirective
              key={i}
              id={`Node${i}`}
              color={color}
              label={{ 
                text: `Node ${i}`,
                fill: theme.textColor
              }}
            />
          ))}
        </SankeyNodesCollectionDirective>
        <Inject services={[SankeyTooltip, SankeyLegend]} />
      </SankeyComponent>
    </div>
  );
}

export default ThemedSankey;
```

## Best Practices

1. **Maintain contrast** - Ensure text is readable against backgrounds
2. **Use consistent colors** - Related items should have similar hues
3. **Limit palette** - 5-8 colors maximum for clarity
4. **Test on different devices** - Verify styling on mobile/tablet
5. **Accessibility first** - Avoid color-only distinctions
6. **Performance** - Complex CSS can slow rendering
7. **Responsive design** - Adapt styling for different screen sizes
8. **Meaningful colors** - Use colors that convey semantic meaning
