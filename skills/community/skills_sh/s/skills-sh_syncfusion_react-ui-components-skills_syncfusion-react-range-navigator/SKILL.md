---
name: syncfusion-react-range-navigator
description: Implements the Syncfusion React Range Navigator component for scrolling and navigating through data with range selection. Use this when users need time-based navigation, financial data visualization, or chart integration with a range selector control. Supports numeric, logarithmic, and DateTime data binding, multiple series types, period selector, lightweight mode, tooltips, RTL, and export/print functionality.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Syncfusion React Range Navigator

A comprehensive skill for implementing the Syncfusion React Range Navigator component - a powerful data visualization control that allows users to scroll and navigate through data with range selection capabilities. This component easily combines with other controls like Charts and Data Grids to create rich dashboards.

## When to Use This Skill

Use this skill when you need to:
- Install and set up the Range Navigator component in a React application
- Implement range selection and navigation for time-series or numeric data
- Display financial data, stock charts, or large datasets requiring navigation
- Configure data binding with numeric, logarithmic, or DateTime value types
- Customize series types (Line, Area, StepLine)
- Add period selectors for predefined time intervals
- Enable lightweight mode without chart data
- Customize navigator appearance (thumbs, borders, regions)
- Configure tooltips for range selection
- Customize labels, grid lines, and tick lines
- Enable accessibility features or RTL support
- Export or print Range Navigator charts
- Integrate Range Navigator with other chart components

## Component Overview

**Range Navigator** is a data visualization control that provides intuitive range selection and navigation capabilities for large datasets. It displays a condensed view of data with interactive sliders that allow users to select specific ranges. The component is particularly useful for:

- **Financial Data Visualization:** Stock price analysis, trading data, market trends
- **Time-Series Navigation:** Historical data exploration, date range selection
- **Large Dataset Filtering:** Scroll through extensive data collections efficiently
- **Dashboard Integration:** Combine with Charts, Grids, and other components

**Key Features:**
- Multiple data source support (local and remote)
- Interactive tooltip and animation
- Lightweight mode for mobile devices
- Period selector for custom time intervals
- Multiple axis and series types
- Export to image formats (PNG, JPEG, SVG, PDF)

## Documentation and Navigation Guide

### API Reference

📄 **Read:** [references/api.md](references/api.md)
- Comprehensive API summary: props, methods, events, styling classes, and a short usage example. Links to official docs.

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependencies (@syncfusion/ej2-react-charts package)
- Setting up development environment (Vite/Create React App)
- Adding CSS stylesheets and themes
- Basic Range Navigator implementation
- Module injection (AreaSeries, DateTime, RangeTooltip)
- Populating with data (dataSource, xName, yName)
- Enabling tooltip
- Running your first application

### Data Binding and Value Types

📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Numeric value type (default Double type)
- Range configuration (minimum, maximum, interval)
- Numeric label formatting (n1, n2, p1, c1, custom formats)
- Logarithmic axis for magnitude data
- Logarithmic range and base customization
- DateTime value type for time-series data
- DateTime interval types (Auto, Years, Quarter, Months, Weeks, Days, Hours, Minutes, Seconds)
- DateTime label formatting
- Complete format reference tables

### Series Types

📄 **Read:** [references/series-types.md](references/series-types.md)
- Line series (default, LineSeries module)
- Area series (AreaSeries module)
- StepLine series (StepLineSeries module)
- Module injection for each series type
- Configuration and implementation examples

### Customization

📄 **Read:** [references/customization.md](references/customization.md)
- Navigator appearance (navigatorStyleSettings)
- Selected and unselected region colors
- Thumb customization (Circle/Rectangle shapes, size, border, fill)
- Border customization (width, color)
- Deferred update for performance optimization
- Allow snapping for precise selection
- Animation duration control

### Period Selector

📄 **Read:** [references/period-selector.md](references/period-selector.md)
- Configuring predefined time periods
- Period array (interval, text, intervalType)
- Module injection (PeriodSelector)
- Positioning (Top or Bottom)
- Height customization
- Disabling range selector (period selector only mode)
- Interval types (Auto, Years, Quarter, Months, Weeks, Days, Hours, Minutes, Seconds)

### Lightweight Mode

📄 **Read:** [references/lightweight.md](references/lightweight.md)
- Lightweight Range Navigator without chart data
- When to use lightweight mode
- Mobile-friendly implementation
- Basic configuration

### Tooltip

📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling and disabling tooltip
- Tooltip customization (fill, opacity, textStyle)
- Label format for tooltips
- Date and time format options
- Complete format reference table

### Labels

📄 **Read:** [references/labels.md](references/labels.md)
- Multilevel labels (enableGrouping for DateTime)
- Grouping by intervals (Auto, Years, Quarter, Months, Weeks, Days, Hours, Minutes, Seconds)
- Smart labels to avoid overlapping (labelIntersectAction)
- Label positioning (inside or outside)
- Label style customization (font, color, family, weight, size)

### Grid Lines and Tick Lines

📄 **Read:** [references/grid-and-tick.md](references/grid-and-tick.md)
- Grid line customization (majorGridLines)
- Grid line width, color, and dashArray
- Tick line customization (majorTickLines)
- Tick line width, color, and dashArray
- Configuration examples

### Accessibility

📄 **Read:** [references/accessibility.md](references/accessibility.md)
- Keyboard navigation support
- Screen reader compatibility
- WCAG 2.0 compliance
- Accessibility features and best practices

### Right-to-Left (RTL) Support

📄 **Read:** [references/rtl.md](references/rtl.md)
- Enabling RTL mode (enableRtl property)
- RTL layout behavior
- Implementation examples

### Export and Print

📄 **Read:** [references/export-print.md](references/export-print.md)
- Export to image formats (PNG, JPEG, SVG, PDF)
- Print functionality
- Export/print method usage
- Configuration options

## Quick Start Example

```tsx
import * as React from 'react';
import { RangeNavigatorComponent, AreaSeries, DateTime, RangeTooltip, Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

// Register your Syncfusion license key
import { registerLicense } from '@syncfusion/ej2-base';
registerLicense('YOUR_LICENSE_KEY');

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 },
    { x: new Date(2018, 6, 1), y: 38 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      valueType="DateTime"
      value={[new Date(2018, 1, 1), new Date(2018, 4, 1)]}
      tooltip={{ enable: true }}
    >
      <Inject services={[AreaSeries, DateTime, RangeTooltip]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## Common Patterns

### Pattern 1: Time-Series Data Navigation

**When user needs:** Navigate through time-series data with date range selection

**Implementation:**
```tsx
import * as React from 'react';
import { RangeNavigatorComponent, AreaSeries, DateTime, RangeTooltip, Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 },
    { x: new Date(2018, 6, 1), y: 38 }
  ];
  return (
    <RangeNavigatorComponent
      valueType="DateTime"
      intervalType="Months"
      labelFormat="MMM"
      value={[new Date(2018, 0, 1), new Date(2018, 6, 1)]}
      tooltip={{ enable: true, displayMode: 'Always' }}>
      <Inject services={[AreaSeries, DateTime, RangeTooltip]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"/>
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  )
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

### Pattern 2: Financial Data with Period Selector

**When user needs:** Stock chart navigation with predefined time periods (1M, 3M, 6M, YTD, 1Y)

**Implementation:**
```tsx
import * as React from 'react';
import {
  RangeNavigatorComponent,
  AreaSeries,
  DateTime,
  RangeTooltip,
  PeriodSelector,
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective,
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from 'react-dom';

function App() {
  const data = [
    { x: new Date(2018, 0, 1), y: 35 },
    { x: new Date(2018, 1, 1), y: 28 },
    { x: new Date(2018, 2, 1), y: 34 },
    { x: new Date(2018, 3, 1), y: 32 },
    { x: new Date(2018, 4, 1), y: 40 },
    { x: new Date(2018, 5, 1), y: 42 },
    { x: new Date(2018, 6, 1), y: 38 }
  ];
  return (
    <RangeNavigatorComponent
      valueType="DateTime"
      value={[new Date(2023, 0, 1), new Date(2023, 11, 31)]}
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 1, text: '1M' },
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'YTD' },
        ],
        position: 'Top',
      }}
    >
      <Inject
        services={[
          AreaSeries,
          DateTime,
          RangeTooltip,
          PeriodSelector,
        ]}
      />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective
          dataSource={data}
          xName="x"
          yName="y"
          type="Area"
        />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById('charts'));
```

### Pattern 3: Custom Styling and Appearance

**When user needs:** Customize navigator colors, thumbs, and borders

**Implementation:**
```tsx
<RangeNavigatorComponent
  navigatorStyleSettings={{
    selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
    unselectedRegionColor: 'transparent',
    thumb: {
      type: 'Circle',
      fill: '#2196F3',
      border: { width: 2, color: '#ffffff' },
      height: 20,
      width: 20
    }
  }}
  navigatorBorder={{ width: 2, color: '#2196F3' }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

### Pattern 4: Lightweight Mode for Mobile

**When user needs:** Simple range selector without chart data for mobile devices

**Implementation:**
```tsx
<RangeNavigatorComponent
  valueType="DateTime"
  value={[new Date(2018, 0, 1), new Date(2018, 6, 1)]}
  intervalType="Months"
>
  <Inject services={[DateTime]} />
  {/* No series - lightweight mode */}
</RangeNavigatorComponent>
```

### Pattern 5: Logarithmic Scale for Large Ranges

**When user needs:** Handle data with values spanning multiple orders of magnitude

**Implementation:**
```tsx
import { RangeNavigatorComponent, LineSeries, Logarithmic, Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective } from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";

<RangeNavigatorComponent
  valueType="Logarithmic"
  logBase={10}
  minimum={100}
  maximum={100000}
  interval={1}
>
  <Inject services={[LineSeries, Logarithmic]} />
  <RangenavigatorSeriesCollectionDirective>
    <RangenavigatorSeriesDirective
      dataSource={logData}
      xName="x"
      yName="y"
      type="Line"
    />
  </RangenavigatorSeriesCollectionDirective>
</RangeNavigatorComponent>
```

## Key Props

### Core Configuration
- **valueType**: `'Double' | 'DateTime' | 'Logarithmic'` - Axis value type (default: 'Double')
- **value**: `number[] | Date[]` - Initial selected range [start, end]
- **minimum**: `number | Date` - Minimum value of the axis
- **maximum**: `number | Date` - Maximum value of the axis
- **interval**: `number` - Axis interval
- **intervalType**: Interval type for DateTime ('Auto' | 'Years' | 'Quarter' | 'Months' | 'Weeks' | 'Days' | 'Hours' | 'Minutes' | 'Seconds')

### Series Configuration
- **series**: Array of series objects with dataSource, xName, yName, type
- **dataSource**: Data array for the series
- **xName**: Field name for x-axis values
- **yName**: Field name for y-axis values
- **type**: `'Line' | 'Area' | 'StepLine'` - Series rendering type

### Appearance
- **navigatorStyleSettings**: Customize selected/unselected regions and thumbs
- **navigatorBorder**: Border width and color
- **theme**: `'Material' | 'Bootstrap' | 'Fabric' | 'Fluent' | 'Tailwind'`

### Features
- **tooltip**: Tooltip configuration (enable, fill, opacity, textStyle, labelFormat)
- **periodSelectorSettings**: Period selector configuration (periods, position, height)
- **enableDeferredUpdate**: Trigger change event after drag completion (default: false)
- **allowSnapping**: Snap slider to nearest interval (default: false)
- **enableGrouping**: Enable multilevel labels for DateTime (default: false)
- **groupBy**: Grouping interval type for multilevel labels
- **labelPosition**: `'Outside' | 'Inside'` - Label position
- **enableRtl**: Enable right-to-left rendering

### Events
- **changed**: Fired when range selection changes
- **load**: Fired before rendering
- **loaded**: Fired after rendering
- **tooltipRender**: Fired before tooltip renders

## Common Use Cases

### Use Case 1: Stock Chart with Range Navigation
Implement a financial stock chart with range selection for analyzing price trends over time. Use DateTime axis, Area series, and period selector for quick time range selection.

### Use Case 2: Dashboard Data Filtering
Integrate Range Navigator with Data Grid to filter large datasets based on date or numeric ranges. Use the `changed` event to update the grid data source.

### Use Case 3: Historical Data Analysis
Analyze historical sales, weather, or analytics data by providing intuitive range selection with tooltips showing exact values.

### Use Case 4: Mobile-Friendly Navigation
Use lightweight mode for mobile applications where chart rendering is not needed, providing simple range selection UI.

### Use Case 5: Multi-Magnitude Data Visualization
Display scientific or financial data spanning multiple orders of magnitude (10^-6 to 10^6) using logarithmic scale.

## Module Injection Requirements

The Range Navigator requires module injection for specific features:

```tsx
import { Inject } from '@syncfusion/ej2-react-charts';

// For Area series
import { AreaSeries } from '@syncfusion/ej2-react-charts';
<Inject services={[AreaSeries]} />

// For DateTime axis
import { DateTime } from '@syncfusion/ej2-react-charts';
<Inject services={[DateTime]} />

// For tooltips
import { RangeTooltip } from '@syncfusion/ej2-react-charts';
<Inject services={[RangeTooltip]} />

// For period selector
import { PeriodSelector } from '@syncfusion/ej2-react-charts';
<Inject services={[PeriodSelector]} />

// For logarithmic scale
import { Logarithmic } from '@syncfusion/ej2-react-charts';
<Inject services={[Logarithmic]} />

// For line series
import { LineSeries } from '@syncfusion/ej2-react-charts';
<Inject services={[LineSeries]} />

// For step line series
import { StepLineSeries } from '@syncfusion/ej2-react-charts';
<Inject services={[StepLineSeries]} />
```

**Always inject all required modules** in a single Inject component based on the features you're using.
