# Smith Chart API Reference (expanded)

This document expands the quick cheat-sheet into a property-by-property reference for the commonly used public API of the React `SmithchartComponent`, `SeriesDirective`, and related option objects used in the reference examples. Where available, a typical default value is provided; if a default is implementation-dependent or not documented clearly in the examples, the Default column shows `—`.

## SmithchartComponent — Core Props

Property | Type | Default | Description
---|---:|---|---
`id` | string | `''` | Unique DOM id used for export/print operations and targeting the component.
`width` | string | `'100%'` | Chart width (e.g. `'700px'`, `'100%'`).
`height` | string | `'100%'` | Chart height (e.g. `'400px'`, `'100%'`).
`title` | object | `{}` | Title configuration: `text`, `subtitle`, `font`, `textAlignment`, `enableTrim`, `maximumWidth`, `visible`. See [TitleModel](https://ej2.syncfusion.com/react/documentation/api/smithchart/titlemodel).
`legendSettings` | object | `{ visible: false }` | Legend options: `visible`, `position`, `alignment`, `shape`, `width`, `height`, `itemPadding`, `shapePadding`, `toggleVisibility`. See [SmithchartLegendSettingsModel](https://ej2.syncfusion.com/react/documentation/api/smithchart/smithchartlegendsettingsmodel).
`horizontalAxis` | object | `{}` | Horizontal axis configuration: `labelPosition`, `labelIntersectAction`, `labelStyle`, `majorGridLines`, `minorGridLines`, `axisLine`. See [SmithchartAxisModel](https://ej2.syncfusion.com/react/documentation/api/smithchart/smithchartaxismodel).
`radialAxis` | object | `{}` | Radial axis configuration (same shape as `horizontalAxis`). See [SmithchartAxisModel](https://ej2.syncfusion.com/react/documentation/api/smithchart/smithchartaxismodel).
`background` | string | `''` | Background color for the chart plot area.
`enableSmartLabels` | boolean | `false` | Enable smart label placement globally (per-series override possible).
`theme` | string | `''` | Theme name when using Syncfusion CSS themes (e.g., `material`, `bootstrap`).
`tooltip` | object | `{ visible: false }` | Global tooltip options; series-level `tooltip` overrides take precedence.
`useGroupingSeparator` | boolean | `false` | Whether numeric values use group separators in labels/tooltips.

Methods
- `export(type: string, fileName: string)` — Export the chart to `'PNG' | 'JPEG' | 'SVG' | 'PDF'` using `fileName` (without extension).
- `print(id?: string)` — Print the chart. Optionally pass the chart container id.

Notes
- Some features require explicit injection of modules via `<Inject services={[...]} />`, for example `SmithchartLegend` and `TooltipRender`.

## SeriesDirective / SeriesCollectionDirective — Series Props

Property | Type | Default | Description
---|---:|---|---
`name` | string | `''` | Series name displayed in the legend.
`points` | array | `[]` | Array of point objects `{ resistance, reactance }` when providing inline points.
`dataSource` | array | `[]` | External data array; use `resistance`/`reactance` to map fields.
`resistance` | string | `'resistance'` | Field name in `dataSource` used as resistance values.
`reactance` | string | `'reactance'` | Field name in `dataSource` used as reactance values.
`fill` | string | `''` | Series line color.
`width` | number | `2` | Series line width in pixels.
`opacity` | number | `1` | Line opacity (0–1).
`visibility` | string | `'Visible'` | Visibility state (`'Visible' | 'Hidden'`).
`marker` | object | `{ visible: false }` | Marker settings: `visible`, `width`, `height`, `shape`, `fill`, `border`, `opacity`, `dataLabel`.
`tooltip` | object | `{ visible: false }` | Per-series tooltip options (overrides global `tooltip`).
`enableSmartLabels` | boolean | `false` | Enable smart labels for this series.

## Marker and DataLabel options

Property | Type | Default | Description
---|---:|---|---
`marker.visible` | boolean | `false` | Show markers for the series.
`marker.width` / `marker.height` | number | `6` | Marker dimensions in pixels (common examples use 8–12px).
`marker.shape` | string | `'Circle'` | `'Circle' | 'Rectangle' | 'Triangle' | 'Diamond' | 'Pentagon' | 'InvertedTriangle'`.
`marker.fill` | string | `''` | Marker fill color.
`marker.border` | object | `{ width: 0, color: '' }` | Marker border settings.
`marker.opacity` | number | `1` | Marker opacity.
`marker.dataLabel.visible` | boolean | `false` | Show data labels attached to markers.
`marker.dataLabel.textStyle` | object | `{}` | Data label font settings: `size`, `color`, `fontFamily`, `fontWeight`, `opacity`.

## Legend settings

Property | Type | Default | Description
---|---:|---|---
`legendSettings.visible` | boolean | `false` | Show legend.
`legendSettings.position` | string | `'Bottom'` | `'Top'|'Bottom'|'Left'|'Right'|'Custom'`.
`legendSettings.alignment` | string | `'Center'` | `'Near'|'Center'|'Far'`.
`legendSettings.shape` | string | `'Circle'` | Legend marker shape.
`legendSettings.toggleVisibility` | boolean | `true` | Allow clicking legend items to hide/show series.

## Tooltip settings and notes

- Inject `TooltipRender` to enable tooltip rendering. Common per-series tooltip option is:

Property | Type | Default | Description
---|---:|---|---
`tooltip.visible` | boolean | `false` | Show tooltip for the series.

Tooltips typically display series name, resistance, and reactance values.

## Axis configuration (horizontalAxis / radialAxis)

Property | Type | Default | Description
---|---:|---|---
`labelPosition` | string | `'Outside'` | `'Inside' | 'Outside'`.
`labelIntersectAction` | string | `'None'` | `'None' | 'Hide'`.
`labelStyle` | object | `{}` | Font and color settings for axis labels.
`majorGridLines` / `minorGridLines` | object | `{ visible: false }` | Gridline settings: `visible`, `width`, `dashArray`, `opacity`, `count` (minor).
`axisLine` | object | `{ visible: true }` | Axis line customization: `visible`, `width`, `dashArray`.

## Methods (component-level links)

- See the full component method list on the official API page: [SmithchartComponent API](https://ej2.syncfusion.com/react/documentation/api/smithchart/).
- `export(type, fileName, orientation?)` — Export the chart. Docs: [export method](https://ej2.syncfusion.com/react/documentation/api/smithchart/#methods).
- `print(id?)` — Print the chart. Docs: [print / beforePrint event docs](https://ej2.syncfusion.com/react/documentation/api/smithchart/).

## Events

The Smithchart component exposes several lifecycle and render events. Links point to the event argument types in the official API.

- `animationComplete` — [ISmithchartAnimationCompleteEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartanimationcompleteeventargs)
- `axisLabelRender` — [ISmithchartAxisLabelRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartaxislabelrendereventargs)
- `beforePrint` — [ISmithchartPrintEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartprinteventargs)
- `legendRender` — [ISmithchartLegendRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartlegendrendereventargs)
- `load` — [ISmithchartLoadEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartloadeventargs)
- `loaded` — [ISmithchartLoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartloadedeventargs)
- `seriesRender` — [ISmithchartSeriesRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithchartseriesrendereventargs)
- `subtitleRender` — [ISubTitleRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/isubtitlerendereventargs)
- `textRender` — [ISmithchartTextRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithcharttextrendereventargs)
- `titleRender` — [ITitleRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ititlerendereventargs)
- `tooltipRender` — [ISmithChartTooltipEventArgs](https://ej2.syncfusion.com/react/documentation/api/smithchart/ismithcharttooltipeventargs)

## Print / Export examples (usage)

```tsx
// Exporting
chartRef.current.export('PNG', 'impedance-analysis');

// Printing
chartRef.current.print('smithchart');
```

## Typical imports

```ts
import {
  SmithchartComponent,
  SeriesCollectionDirective,
  SeriesDirective,
  Inject,
  SmithchartLegend,
  TooltipRender
} from '@syncfusion/ej2-react-charts';
```

---

If you'd like, I can now cross-check each property against the official API page and replace any `—` defaults with the exact documented defaults. Should I perform that authoritative validation and update the table? 