---
title: Range Navigator API Reference
---

# Range Navigator — API Reference

Official docs: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default

## Overview

This file summarizes the key public API surface for the Syncfusion React `RangeNavigatorComponent` used by the skill content: main props, methods, events, styling classes and a short usage example.

## Key Props (selected)
- `valueType` — `'Double' | 'DateTime' | 'Logarithmic'` (default: `Double`)
- `value` — `number[] | Date[]` — initial selected range `[start, end]`
- `minimum` / `maximum` — `number | Date`
- `interval` — `number` — axis interval
- `intervalType` — DateTime interval types (`Auto`, `Years`, `Months`, ...)
- `series` — `RangeNavigatorSeriesModel[]` — array of series definitions
- `dataSource` — `Object[] | DataManager` — series data source
- `xName` / `yName` — field names for series
- `navigatorStyleSettings` — customize selected/unselected regions and thumbs
- `navigatorBorder` — border config for navigator
- `tooltip` — `RangeTooltip` — tooltip configuration
- `periodSelectorSettings` — `PeriodSelectorSettingsModel`
- `enableDeferredUpdate`, `allowSnapping`, `enableGrouping`, `enablePersistence`, `enableRtl` — boolean feature flags

## Methods (selected)
- `destroy()` — cleanup component instance
- `export(type, fileName, orientation, controls, width, height, isVertical)` — export to image/PDF
- `print(id)` — print the component
- `renderChart(resize)` — re-render chart

## Events
- `changed` — fired when the selected range changes (use to filter other components)
- `load` / `loaded` — lifecycle events
- `beforeResize` / `resized` — resize lifecycle
- `labelRender` — customize label text
- `tooltipRender` — intercept tooltip content

## Styling classes
- `.e-rangeselector`
- `.e-rangeselector-content`
- `.e-rangeselector-label`
- `.e-rangeselector-thumb`
- `.e-rangeselector-tooltip`

## Short Usage (React)

```tsx
import React, { useRef } from 'react';
import {
  RangeNavigatorComponent,
  RangenavigatorSeriesCollectionDirective,
  RangenavigatorSeriesDirective,
  Inject,
  AreaSeries,
  DateTime
} from '@syncfusion/ej2-react-charts';

const MyRange = ({ data }) => {
  const ref = useRef(null);
  return (
    <RangeNavigatorComponent
      id="rangeNavigator"
      ref={ref}
      valueType="DateTime"
      value={[new Date(2020,0,1), new Date(2020,5,1)]}
      tooltip={{ enable: true }}
    >
      <Inject services={[AreaSeries, DateTime]} />
      <RangenavigatorSeriesCollectionDirective>
        <RangenavigatorSeriesDirective dataSource={data} xName="x" yName="y" type="Area" />
      </RangenavigatorSeriesCollectionDirective>
    </RangeNavigatorComponent>
  );
};

export default MyRange;
```

## Notes and links
- For full, authoritative API details see the official documentation: https://ej2.syncfusion.com/react/documentation/api/range-navigator/index-default
