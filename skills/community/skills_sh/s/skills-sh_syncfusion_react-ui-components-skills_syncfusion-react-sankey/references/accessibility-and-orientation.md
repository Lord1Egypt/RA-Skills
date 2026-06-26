# Accessibility and Orientation

## Table of Contents
- [RTL (Right-to-Left) Support](#rtl-right-to-left-support)
  - [Enabling RTL](#enabling-rtl)
  - [RTL with Dynamic Language](#rtl-with-dynamic-language)
  - [RTL Layout Considerations](#rtl-layout-considerations)
- [WCAG Accessibility Compliance](#wcag-accessibility-compliance)
  - [Semantic Structure](#semantic-structure)
  - [Color Contrast](#color-contrast)
  - [Keyboard Navigation](#keyboard-navigation)
  - [Alt Text and Descriptions](#alt-text-and-descriptions)
- [Screen Reader Support](#screen-reader-support)
  - [ARIA Labels](#aria-labels)
  - [Screen Reader Friendly Tooltips](#screen-reader-friendly-tooltips)
- [Responsive Design](#responsive-design)
  - [Mobile Accessibility](#mobile-accessibility)
  - [Touch-Friendly Interactions](#touch-friendly-interactions)
- [Focus Management](#focus-management)
  - [Visible Focus Indicators](#visible-focus-indicators)
- [Complete Accessible Example](#complete-accessible-example)
- [Best Practices](#best-practices)

## RTL (Right-to-Left) Support

Support international applications with RTL layout for languages like Arabic, Hebrew, and Persian.

### Enabling RTL

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  title="مخطط سانكي"
  enableRtl={true}
>
  {/* nodes and links */}
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### RTL with Dynamic Language

```tsx
import React, { useState } from 'react';
import {
  SankeyComponent, Inject, SankeyTooltip, SankeyLegend, SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function MultiLanguageSankey() {
  const [language, setLanguage] = useState('en');

  const translations = {
    en: {
      title: 'Energy Flow',
      solar: 'Solar',
      wind: 'Wind',
      output: 'Output'
    },
    ar: {
      title: 'تدفق الطاقة',
      solar: 'الطاقة الشمسية',
      wind: 'الرياح',
      output: 'الإنتاج'
    }
  };

  const currentTranslation = translations[language];
  const isRTL = language === 'ar';

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      <select onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="ar">العربية</option>
      </select>

      <SankeyComponent
        width="90%"
        height="420px"
        title={currentTranslation.title}
        enableRtl={isRTL}
      >
        <SankeyNodesCollectionDirective>
          <SankeyNodeDirective 
            id="Solar" 
            label={{ text: currentTranslation.solar }}
          />
          <SankeyNodeDirective 
            id="Wind" 
            label={{ text: currentTranslation.wind }}
          />
          <SankeyNodeDirective 
            id="Output" 
            label={{ text: currentTranslation.output }}
          />
        </SankeyNodesCollectionDirective>
        <SankeyLinksCollectionDirective>
          <SankeyLinkDirective sourceId="Solar" targetId="Output" value={100} />
          <SankeyLinkDirective sourceId="Wind" targetId="Output" value={80} />
        </SankeyLinksCollectionDirective>
        <Inject services={[SankeyTooltip, SankeyLegend]} />
      </SankeyComponent>
    </div>
  );
}

export default MultiLanguageSankey;
ReactDOM.render(<MultiLanguageSankey />, document.getElementById("charts"));
```

### RTL Layout Considerations

When enabling RTL:
- Legend positioning adapts automatically
- Node labels align right
- Links flow from right to left
- Navigation direction reverses

```tsx
<SankeyComponent
  width="90%"
  height="420px"
  enableRtl={true}
  legendSettings={{
    visible: true,
    position: 'Bottom'  // Automatically adapted for RTL
  }}
  labelSettings={{
    visible: true
    // Text alignment handled automatically
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

## WCAG Accessibility Compliance

Ensure your Sankey diagram meets Web Content Accessibility Guidelines (WCAG) 2.1 standards.

### WCAG Level AA Compliance

#### 1. Semantic Structure

Use proper HTML markup:

```tsx
<section aria-label="Energy Flow Sankey Diagram">
  <h2>Energy Consumption 2024</h2>
  <SankeyComponent
    width="90%"
    height="420px"
    role="img"
    aria-label="Sankey chart showing energy flow from sources to consumption sectors"
  >
    {/* nodes and links */}
  </SankeyComponent>
  <p>Chart description for screen readers</p>
</section>
```

#### 2. Color Contrast

Ensure sufficient color contrast ratios:

```tsx
// WCAG AA requires 4.5:1 contrast ratio for normal text
// WCAG AAA requires 7:1 ratio

const accessibleColors = {
  darkBlue: '#003366',        // High contrast
  lightText: '#FFFFFF',       // 21:1 ratio with dark blue
  darkText: '#000000',        // Maximum contrast
  mediumGray: '#666666',
  lightGray: '#CCCCCC'
};

<SankeyComponent
  linkStyle={{
    opacity: 0.7  // Higher opacity for better visibility
  }}
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective 
      id="A" 
      color={accessibleColors.darkBlue}
      label={{
        fill: accessibleColors.lightText
      }}
    />
  </SankeyNodesCollectionDirective>
</SankeyComponent>
```

#### 3. Keyboard Navigation

Enable keyboard access:

We do not expose a dedicated API like `allowKeyboardInteraction` for keyboard navigation. The desired navigation behavior is achieved through standard Tab and arrow key actions.

| Press        | To do this                                                                   |
|--------------|------------------------------------------------------------------------------|
| Alt + J      | Moves the focus to the Sankey Chart element.                                 |
| Tab          | Moves the focus to the next element in the chart.                            |
| Shift + Tab  | Moves the focus to the previous element in the chart.                        |
| Down Arrow   | Moves the focus to the node or link below the selected element.              |
| Up Arrow     | Moves the focus to the node or link above the selected element.              |
| Left Arrow   | Moves the focus to the next node or link from the selected element.          |
| Right Arrow  | Moves the focus to the previous node or link from the selected element.      |
| ESC          | Cancels the tooltip for the node or link.                                    |
| Ctrl + P     | Prints the Sankey Chart.                                                     |


```tsx
function AccessibleSankey() {
  return (
    <div>
      <SankeyComponent
        width="90%"
        height="420px"
        title="Keyboard Navigable Sankey"
      >
        {/* nodes and links */}
      </SankeyComponent>
    </div>
  );
}
export default AccessibleSankey;
```

#### 4. Alt Text and Descriptions

Provide text alternatives:

```tsx
<figure>
  <SankeyComponent
    width="90%"
    height="420px"
    title="Energy Flow Analysis"
    role="img"
    aria-label="Sankey diagram depicting energy sources (Solar, Wind, Gas) flowing to consumption sectors (Residential, Commercial, Industrial)"
  >
    {/* nodes and links */}
  </SankeyComponent>
  <figcaption>
    Energy distribution showing 450 units from Solar, 200 from Wind, 
    and 800 from Natural Gas, distributed among residential (300), 
    commercial (400), and industrial (350) sectors.
  </figcaption>
</figure>
```

## Screen Reader Support

### ARIA Labels

```tsx
<SankeyComponent
  aria-label="Energy consumption Sankey diagram"
  role="img"
>
  <SankeyNodesCollectionDirective>
    <SankeyNodeDirective
      id="Solar"
      aria-label="Solar energy source"
      label={{ text: 'Solar' }}
    />
  </SankeyNodesCollectionDirective>
  <Inject services={[SankeyTooltip, SankeyLegend]} />
</SankeyComponent>
```

### Screen Reader Friendly Tooltips

```tsx
<SankeyComponent
  tooltip={{
    enable: true,
    template: `
      <div role="tooltip">
        <span aria-live="polite">
          Flow from {source} to {target}: {value} units
        </span>
      </div>
    `
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

## Responsive Design

### Mobile Accessibility

```tsx
import { Browser } from '@syncfusion/ej2-base';

<SankeyComponent
  width={Browser.isDevice ? '100%' : '90%'}
  height={Browser.isDevice ? '700px' : '500px'}
  labelSettings={{
    visible: !Browser.isDevice,  // Hide labels on mobile
    fontSize: Browser.isDevice ? 10 : 12
  }}
  tooltip={{
    enable: true  // Rely on tooltips for mobile info
  }}
  legendSettings={{
    visible: true,
    position: Browser.isDevice ? 'Bottom' : 'Right',
    itemPadding: Browser.isDevice ? 4 : 8
  }}
>
  {/* nodes and links */}
</SankeyComponent>
```

### Touch-Friendly Interactions

```tsx
function TouchAccessibleSankey() {
  const [selectedNode, setSelectedNode] = React.useState(null);

  const onNodeClick = (args) => {
    // Works for both mouse click and touch
    setSelectedNode(args.data.id);
  };

  return (
    <div>
      <SankeyComponent
        width="100%"
        height="600px"
        nodeClick={onNodeClick}
      >
        {/* nodes and links */}
      </SankeyComponent>

      {selectedNode && (
        <div
          role="region"
          aria-live="polite"
          aria-label={`Information for ${selectedNode}`}
        >
          <h3>Selected: {selectedNode}</h3>
          {/* Details about selected node */}
        </div>
      )}
    </div>
  );
}

export default TouchAccessibleSankey;
```

## Focus Management

### Visible Focus Indicators

```tsx
<div style={{
  outline: 'none'
}}>
  <SankeyComponent
    width="90%"
    height="420px"
    title="Focusable Chart"
    tabIndex={0}
    style={{
      outline: '3px solid #0066CC',
      outlineOffset: '2px'
    }}
  >
    {/* nodes and links */}
  </SankeyComponent>
</div>

<style>{`
  .sankey-chart:focus {
    outline: 3px solid #0066CC;
    outline-offset: 2px;
  }
`}</style>
```

## Complete Accessible Example

```tsx
import React from 'react';
import { Browser } from '@syncfusion/ej2-base';
import {
  SankeyComponent,
  Inject,
  SankeyTooltip,
  SankeyLegend,
  SankeyExport,
  SankeyNodeDirective,
  SankeyNodesCollectionDirective,
  SankeyLinkDirective,
  SankeyLinksCollectionDirective,
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from 'react-dom';

function FullyAccessibleSankey() {
  return (
    <SankeyComponent
      id="sankey-container"
      width="90%"
      height={Browser.isDevice ? '600' : '450'}
      title="California Energy Consumption in 2023"
      subTitle="Source: Lawrence Livermore National Laboratory"
      linkStyle={{ opacity: 0.6, curvature: 0.55, colorType: 'Source' }}
      labelSettings={{ visible: true }}
      tooltip={{ enable: true }}
      legendSettings={{ visible: true }}
    >
      <Inject services={[SankeyTooltip, SankeyLegend, SankeyExport]} />
      <SankeyNodesCollectionDirective>
        <SankeyNodeDirective id="Solar" label={{ text: 'Solar' }} />
        <SankeyNodeDirective id="Generation" label={{ text: 'Generation' }} />
        <SankeyNodeDirective id="Consumption" label={{ text: 'Consumption' }} />
      </SankeyNodesCollectionDirective>
      <SankeyLinksCollectionDirective>
        <SankeyLinkDirective
          sourceId="Solar"
          targetId="Generation"
          value={450}
        />
        <SankeyLinkDirective
          sourceId="Generation"
          targetId="Consumption"
          value={400}
        />
      </SankeyLinksCollectionDirective>
    </SankeyComponent>
  );
}

export default FullyAccessibleSankey;
ReactDOM.render(<FullyAccessibleSankey />, document.getElementById('charts'));
```

## Best Practices

1. **Test with screen readers** - Use NVDA, JAWS, or VoiceOver
2. **Keyboard navigation** - Support all interactions via keyboard
3. **Color alone** - Never use color as only means of conveying info
4. **Focus visible** - Always show focus indicators
5. **ARIA labels** - Provide context for dynamic content
6. **Text alternatives** - Include data tables or descriptions
7. **Mobile first** - Design for touch and small screens
8. **Regular audits** - Test accessibility regularly
