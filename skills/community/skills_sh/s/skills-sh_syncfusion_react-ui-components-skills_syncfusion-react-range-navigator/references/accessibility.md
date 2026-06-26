# Accessibility

The Range Navigator component follows accessibility guidelines and standards, including ADA, Section 508, WCAG 2.2, and WAI-ARIA roles, ensuring it's usable by people with disabilities and assistive technologies.

## Table of contents
- [Accessibility Compliance](#accessibility-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
  - [ARIA Roles Used](#aria-roles-used)
  - [Basic Implementation with ARIA](#basic-implementation-with-aria)
- [Keyboard Navigation](#keyboard-navigation)
  - [Supported Keyboard Shortcuts](#supported-keyboard-shortcuts)
  - [Enabling Keyboard Navigation](#enabling-keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
  - [Screen Reader Compatibility](#screen-reader-compatibility)
  - [Implementing for Screen Readers](#implementing-for-screen-readers)
- [Color Contrast](#color-contrast)
  - [Contrast Requirements](#contrast-requirements)
  - [High Contrast Theme](#high-contrast-theme)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Mobile Device Support](#mobile-device-support)
- [Accessibility Testing](#accessibility-testing)
  - [Automated Testing Tools](#automated-testing-tools)
  - [Running Accessibility Tests](#running-accessibility-tests)
- [Best Practices for Accessibility](#best-practices-for-accessibility)
- [Complete Accessible Example](#complete-accessible-example)
- [Accessibility Compliance Summary](#accessibility-compliance-summary)
- [Resources](#resources)
- [Testing Resources](#testing-resources)
- [Key Points](#key-points)

## Accessibility Compliance

The Range Navigator component meets the following accessibility standards:

| Accessibility Criteria | Support Level |
|------------------------|---------------|
| WCAG 2.2 Support | ✅ Full Support |
| Section 508 Support | ✅ Full Support |
| Screen Reader Support | ✅ Full Support |
| Right-to-Left Support | ✅ Full Support |
| Color Contrast | ✅ Full Support |
| Mobile Device Support | ✅ Full Support |
| Keyboard Navigation | ✅ Full Support |
| Accessibility Checker Validation | ✅ Full Support |
| Axe-core Validation | ✅ Full Support |

**Legend:**
- ✅ Full Support - All features meet the requirement
- ⚠️ Partial Support - Some features meet the requirement
- ❌ Not Supported - Component does not meet the requirement

## WAI-ARIA Attributes

The Range Navigator component implements WAI-ARIA patterns to ensure proper accessibility for screen readers and assistive technologies.

### ARIA Roles Used

- **region**: Identifies the Range Navigator as a distinct region
- **aria-label**: Provides accessible names for interactive elements

### Basic Implementation with ARIA

```tsx
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective,
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from 'react-dom';
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 },
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById('charts'));
```

The Range Navigator automatically includes appropriate ARIA attributes for accessibility.

## Keyboard Navigation

The Range Navigator supports comprehensive keyboard navigation, following keyboard interaction guidelines for assistive technologies.

### Supported Keyboard Shortcuts

| Key | Action |
|-----|--------|
| <kbd>Tab</kbd> | Moves focus to the Range Navigator element |
| <kbd>Ctrl</kbd> + <kbd>P</kbd> | Prints the Range Navigator |

### Enabling Keyboard Navigation

Keyboard navigation is enabled by default. Users can:
1. Tab to focus the Range Navigator
2. Use additional keyboard shortcuts for interaction

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <div>
      <h2>Accessible Range Navigator</h2>
      <p>Press Tab to focus the Range Navigator, Ctrl+P to print</p>
      
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Screen Reader Support

The Range Navigator provides full screen reader support, ensuring users with visual impairments can navigate and interact with the component.

### Screen Reader Compatibility

- **JAWS**: Full support
- **NVDA**: Full support
- **VoiceOver**: Full support (macOS, iOS)
- **TalkBack**: Full support (Android)
- **Narrator**: Full support (Windows)

### Implementing for Screen Readers

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  RangeTooltip, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <div role="main" aria-label="Data Visualization">
      <h2 id="chart-title">Sales Range Navigator</h2>
      <p id="chart-description">
        Select a date range to filter sales data from January to April 2023
      </p>
      
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
        tooltip={{ enable: true }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip ]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Color Contrast

The Range Navigator ensures WCAG 2.2 AAA color contrast requirements are met.

### Contrast Requirements

- **Normal Text**: Minimum 4.5:1 contrast ratio
- **Large Text**: Minimum 3:1 contrast ratio
- **UI Components**: Minimum 3:1 contrast ratio

### High Contrast Theme

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      labelFormat="MMM"
      theme="HighContrast"
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="date"
          yName="value"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Right-to-Left (RTL) Support

The Range Navigator fully supports RTL languages. For detailed RTL implementation, see the RTL reference documentation.

```tsx
<RangeNavigatorComponent
  id="rangeNavigator"
  enableRtl={true}
  valueType="DateTime"
>
  {/* RTL layout enabled */}
</RangeNavigatorComponent>
```

## Mobile Device Support

The Range Navigator is fully responsive and accessible on mobile devices with:
- Touch gesture support
- Mobile-friendly sizing
- Responsive layout
- Optimized performance

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <div style={{ maxWidth: '100%', padding: '10px' }}>
      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM"
      >
        <Inject services={[AreaSeries, DateTime]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={data}
            xName="date"
            yName="value"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Accessibility Testing

The Range Navigator has been validated using:

### Automated Testing Tools

1. **Accessibility Checker**
   - NPM package: `accessibility-checker`
   - Validates against WCAG 2.2 standards

2. **Axe-core**
   - NPM package: `axe-core`
   - Comprehensive accessibility testing

### Running Accessibility Tests

```bash
# Install testing tools
npm install --save-dev accessibility-checker axe-core

# Run accessibility tests
npm run accessibility-test
```

## Best Practices for Accessibility

### 1. Provide Context

Always provide descriptive labels and context for the Range Navigator:

```tsx
<div>
  <h2 id="navigator-title">Sales Data Navigator</h2>
  <p id="navigator-description">
    Use the sliders to select a date range for viewing sales data
  </p>
  
  <RangeNavigatorComponent
    id="rangeNavigator"
    // Component configuration
  />
</div>
```

### 2. Enable Tooltips

Tooltips provide additional context for screen reader users:

```tsx
<RangeNavigatorComponent
  tooltip={{ 
    enable: true,
    displayMode: 'Always'
  }}
>
</RangeNavigatorComponent>
```

### 3. Sufficient Color Contrast

Ensure custom colors meet WCAG contrast requirements:

```tsx
<RangeNavigatorComponent
  navigatorStyleSettings={{
    selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
    thumb: {
      fill: '#1976D2',  // High contrast color
      border: { width: 2, color: '#ffffff' }
    }
  }}
>
</RangeNavigatorComponent>
```

### 4. Keyboard Accessibility

Ensure all functionality is accessible via keyboard:

```tsx
// Default keyboard navigation is enabled
// No additional configuration needed
```

### 5. Alternative Text

Provide meaningful descriptions for data:

```tsx
<div>
  <h2>Stock Price Range</h2>
  <p>
    Interactive range selector showing stock prices from January to December 2023.
    Current selected range: March to October 2023.
  </p>
  
  <RangeNavigatorComponent
    id="rangeNavigator"
    // Configuration
  />
</div>
```

## Complete Accessible Example

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  RangeTooltip, 
  PeriodSelector, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const stockData = [
    { date: new Date(2023, 0, 1), price: 100 },
    { date: new Date(2023, 1, 1), price: 110 },
    { date: new Date(2023, 2, 1), price: 105 },
    { date: new Date(2023, 3, 1), price: 115 },
    { date: new Date(2023, 4, 1), price: 120 },
    { date: new Date(2023, 5, 1), price: 125 }
  ];

  return (
    <div role="main" aria-labelledby="chart-title">
      <h1 id="chart-title">Stock Price Range Navigator</h1>
      <p id="chart-description">
        This interactive chart allows you to select a date range to analyze stock prices.
        Use Tab to focus the navigator, and Ctrl+P to print.
      </p>

      <RangeNavigatorComponent
        id="rangeNavigator"
        valueType="DateTime"
        labelFormat="MMM yyyy"
        
        // Accessibility features
        tooltip={{ 
          enable: true,
          displayMode: 'Always'
        }}
        
        // High contrast colors
        navigatorStyleSettings={{
          selectedRegionColor: 'rgba(33, 150, 243, 0.4)',
          thumb: {
            fill: '#1976D2',
            border: { width: 3, color: '#ffffff' }
          }
        }}
        
        // Period selector for keyboard users
        periodSelectorSettings={{
          periods: [
            { intervalType: 'Months', interval: 1, text: '1M' },
            { intervalType: 'Months', interval: 3, text: '3M' },
            { intervalType: 'Months', interval: 6, text: '6M' }
          ]
        }}
      >
        <Inject services={[AreaSeries, DateTime, RangeTooltip, PeriodSelector]} />
        <RangenavigatorSeriesCollectionDirective>
          <RangenavigatorSeriesDirective
            dataSource={stockData}
            xName="date"
            yName="price"
            type="Area"
          />
        </RangenavigatorSeriesCollectionDirective>
      </RangeNavigatorComponent>

      <div aria-live="polite" aria-atomic="true">
        <p>Use the range navigator above to select a date range for detailed analysis.</p>
      </div>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Accessibility Compliance Summary

| Standard | Compliance | Notes |
|----------|------------|-------|
| WCAG 2.2 Level A | ✅ Fully Compliant | All criteria met |
| WCAG 2.2 Level AA | ✅ Fully Compliant | All criteria met |
| WCAG 2.2 Level AAA | ✅ Fully Compliant | All criteria met |
| Section 508 | ✅ Fully Compliant | All requirements met |
| ADA | ✅ Fully Compliant | Meets ADA standards |

## Resources

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22)
- [Section 508 Standards](https://www.section508.gov)
- [WAI-ARIA Patterns](https://www.w3.org/TR/wai-aria)
- [Syncfusion Accessibility Documentation](https://ej2.syncfusion.com/react/documentation/common/accessibility)

## Testing Resources

- [Accessibility Checker (NPM)](https://www.npmjs.com/package/accessibility-checker)
- [Axe-core (NPM)](https://www.npmjs.com/package/axe-core)
- [Syncfusion Accessibility Sample](https://ej2.syncfusion.com/accessibility/range-navigator.html)

## Key Points

1. **Full Compliance**: Range Navigator meets WCAG 2.2, Section 508, and ADA standards
2. **Keyboard Navigation**: Complete keyboard support with Tab and Ctrl+P shortcuts
3. **Screen Readers**: Compatible with all major screen readers
4. **Color Contrast**: Meets AAA contrast requirements
5. **Mobile**: Fully accessible on mobile devices
6. **RTL Support**: Complete right-to-left language support
7. **Testing**: Validated with automated accessibility tools
8. **Best Practices**: Follow accessibility guidelines for custom implementations

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

Accessibility-related complex API references and behaviors:
- [`enableRtl`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#enableRtl) (RTL behavior), [`enablePersistence`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#enablePersistence) (persistence across sessions)
- Tooltip accessibility props: [`tooltip`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#tooltip) settings and `displayMode`
- Events and lifecycle: [`load`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#load), [`loaded`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#loaded), [`changed`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#changed), [`resized`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#resized) (useful for accessibility announcements)

