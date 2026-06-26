# Right-to-Left (RTL) Support

The Range Navigator supports right-to-left (RTL) rendering for languages that read from right to left, such as Arabic, Hebrew, Persian, and Urdu. RTL support ensures proper text direction, layout mirroring, and cultural appropriateness.

## Table of contents
- [Enabling RTL](#enabling-rtl)
- [RTL Behavior](#rtl-behavior)
- [RTL with Different Value Types](#rtl-with-different-value-types)
  - [DateTime with RTL](#datetime-with-rtl)
  - [Numeric with RTL](#numeric-with-rtl)
- [RTL with Tooltip](#rtl-with-tooltip)
- [RTL with Period Selector](#rtl-with-period-selector)
- [Dynamic RTL Switching](#dynamic-rtl-switching)
- [RTL with Localization](#rtl-with-localization)
- [Complete RTL Example](#complete-rtl-example)
- [RTL with Custom Styling](#rtl-with-custom-styling)
- [Browser Compatibility](#browser-compatibility)
- [When to Use RTL](#when-to-use-rtl)
- [Best Practices](#best-practices)
- [Configuration Summary](#configuration-summary)
- [Key Points](#key-points)
- [API Links](#api-links)

## Enabling RTL

Enable RTL mode using the `enableRtl` property:

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
    { date: new Date(2023, 3, 1), value: 115 },
    { date: new Date(2023, 4, 1), value: 120 },
    { date: new Date(2023, 5, 1), value: 125 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      enableRtl={true}
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
ReactDOM.render(<App />, document.getElementById("charts"));
```

## RTL Behavior

When RTL is enabled:

1. **Layout Mirroring**: The entire Range Navigator layout is mirrored horizontally
2. **Slider Direction**: Sliders move from right to left
3. **Labels**: Text labels maintain proper RTL text direction
4. **Tooltip**: Tooltip position adjusts for RTL layout
5. **Period Selector**: Buttons are arranged right to left

## RTL with Different Value Types

### DateTime with RTL

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
      enableRtl={true}
      valueType="DateTime"
      labelFormat="MMM yyyy"
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

### Numeric with RTL

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { x: 0, y: 10 },
    { x: 10, y: 30 },
    { x: 20, y: 25 },
    { x: 30, y: 45 },
    { x: 40, y: 35 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      enableRtl={true}
      valueType="Double"
    >
      <Inject services={[AreaSeries]} />
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

## RTL with Tooltip

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
    <RangeNavigatorComponent
      id="rangeNavigator"
      enableRtl={true}
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
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## RTL with Period Selector

```tsx
import { 
  RangeNavigatorComponent, 
  AreaSeries, 
  DateTime, 
  PeriodSelector, 
  Inject,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective 
} from '@syncfusion/ej2-react-charts';
import * as ReactDOM from "react-dom";
import * as React from 'react';

function App() {
  const data = [
    { date: new Date(2020, 0, 1), value: 100 },
    { date: new Date(2020, 3, 1), value: 110 },
    { date: new Date(2020, 6, 1), value: 105 },
    { date: new Date(2020, 9, 1), value: 115 },
    { date: new Date(2021, 0, 1), value: 120 },
    { date: new Date(2021, 3, 1), value: 130 }
  ];

  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      enableRtl={true}
      valueType="DateTime"
      labelFormat="MMM yyyy"
      periodSelectorSettings={{
        periods: [
          { intervalType: 'Months', interval: 3, text: '3M' },
          { intervalType: 'Months', interval: 6, text: '6M' },
          { intervalType: 'Years', interval: 1, text: '1Y' },
          { text: 'All' }
        ],
        position: 'Top'
      }}
    >
      <Inject services={[AreaSeries, DateTime, PeriodSelector]} />
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

## Dynamic RTL Switching

Allow users to toggle between LTR and RTL modes:

```tsx
import { useState } from 'react';
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
  const [rtlEnabled, setRtlEnabled] = useState(false);

  const data = [
    { date: new Date(2023, 0, 1), value: 100 },
    { date: new Date(2023, 1, 1), value: 110 },
    { date: new Date(2023, 2, 1), value: 105 },
    { date: new Date(2023, 3, 1), value: 115 }
  ];

  return (
    <div dir={rtlEnabled ? 'rtl' : 'ltr'}>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => setRtlEnabled(!rtlEnabled)}>
          Toggle RTL (Currently: {rtlEnabled ? 'RTL' : 'LTR'})
        </button>
      </div>

      <RangeNavigatorComponent
        id="rangeNavigator"
        enableRtl={rtlEnabled}
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

## RTL with Localization

Combine RTL with localized content for complete internationalization:

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
    <div dir="rtl" lang="ar">
      <h2>مخطط المدى الزمني</h2>
      <p>اختر نطاقًا زمنيًا لعرض البيانات</p>

      <RangeNavigatorComponent
        id="rangeNavigator"
        enableRtl={true}
        valueType="DateTime"
        labelFormat="MMM yyyy"
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

## Complete RTL Example

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
    { date: new Date(2023, 5, 1), price: 125 },
    { date: new Date(2023, 6, 1), price: 130 },
    { date: new Date(2023, 7, 1), price: 128 },
    { date: new Date(2023, 8, 1), price: 135 },
    { date: new Date(2023, 9, 1), price: 140 },
    { date: new Date(2023, 10, 1), price: 138 },
    { date: new Date(2023, 11, 1), price: 145 }
  ];

  return (
    <div dir="rtl" className="App">
      <h2>متصفح نطاق أسعار الأسهم</h2>
      
      <RangeNavigatorComponent
        id="rangeNavigator"
        enableRtl={true}
        valueType="DateTime"
        labelFormat="MMM yyyy"
        value={[new Date(2023, 2, 1), new Date(2023, 9, 1)]}
        tooltip={{ 
          enable: true,
          displayMode: 'Always'
        }}
        periodSelectorSettings={{
          periods: [
            { intervalType: 'Months', interval: 1, text: '1M' },
            { intervalType: 'Months', interval: 3, text: '3M' },
            { intervalType: 'Months', interval: 6, text: '6M' },
            { intervalType: 'Years', interval: 1, text: '1Y' },
            { text: 'All' }
          ],
          position: 'Top'
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

      <p>استخدم أشرطة التمرير لتحديد نطاق التاريخ</p>
    </div>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById("charts"));
```

## RTL with Custom Styling

```tsx
<RangeNavigatorComponent
  id="rangeNavigator"
  enableRtl={true}
  valueType="DateTime"
  navigatorStyleSettings={{
    selectedRegionColor: 'rgba(33, 150, 243, 0.3)',
    thumb: {
      type: 'Circle',
      width: 20,
      height: 20,
      fill: '#2196F3',
      border: { width: 2, color: '#ffffff' }
    }
  }}
  navigatorBorder={{ width: 2, color: '#2196F3' }}
>
  {/* Series configuration */}
</RangeNavigatorComponent>
```

## Browser Compatibility

RTL support is fully compatible with all modern browsers:
- Chrome
- Firefox
- Safari
- Edge
- Opera

## When to Use RTL

**Enable RTL when:**
- Application targets RTL language users (Arabic, Hebrew, etc.)
- UI needs to match cultural reading patterns
- Compliance with regional accessibility standards

**Key RTL Languages:**
- Arabic (العربية)
- Hebrew (עברית)
- Persian/Farsi (فارسی)
- Urdu (اردو)
- Pashto (پښتو)
- Sindhi (سنڌي)

## Best Practices

1. **Container Direction**: Set `dir="rtl"` on parent container
2. **Language Attribute**: Add `lang` attribute for proper language identification
3. **Test Thoroughly**: Verify all interactions work correctly in RTL mode
4. **Consistent Application**: Apply RTL across entire application, not just components
5. **Text Content**: Ensure all text content is properly localized
6. **Icons and Images**: Consider mirroring directional icons
7. **Testing**: Test with actual RTL language speakers

## Configuration Summary

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| enableRtl | Boolean | false | Enable right-to-left rendering |

## Key Points

1. **Simple Enablement**: Set `enableRtl={true}` to enable RTL mode
2. **Full Support**: All Range Navigator features work in RTL mode
3. **Layout Mirroring**: Entire layout is automatically mirrored
4. **Works with All Features**: Compatible with tooltips, period selector, all value types
5. **Cultural Appropriateness**: Ensures proper display for RTL language users
6. **Accessibility**: Maintains full accessibility in RTL mode
7. **Dynamic Switching**: Can toggle RTL mode at runtime
8. **Browser Support**: Works across all modern browsers

## API Links

Full Range Navigator API: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

RTL-related complex API references:
- `enableRtl` (boolean) — enable right-to-left rendering and behavior
- `dir` and localization considerations are handled at the container level; see the API page for rendering adjustments and supported behaviors

Detailed API anchors:
- [`enableRtl`](https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default#enableRtl)


