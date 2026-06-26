# Bullet Chart API Reference (React)

This file summarizes the primary API surface for `BulletChartComponent` from `@syncfusion/ej2-react-charts` used throughout the skill references.

## Import

```tsx
import {
  BulletChartComponent,
  BulletRangeCollectionDirective,
  BulletRangeDirective,
  Inject,
  BulletTooltip,
  BulletChartLegend
} from '@syncfusion/ej2-react-charts';
```

## Key Props (selected)

`dataSource: any[]` — Data array for the chart

- `valueField: string` — Field name for the actual/feature measure
- `targetField: string` — Field name for the comparative/target measure
- `valueFill: string | string[]` — Fill color (or data field name) for the value bar
- `valueHeight: number` — Height/thickness of the value bar in pixels
- `valueBorder: { color?: string; width?: number }` — Border for the value bar — see BorderModel: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bordermodel
- `type: 'Rect' | 'Dot'` — Shape of the value bar — see FeatureType enum: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/index-default
- `targetTypes: Array<'Rect'|'Circle'|'Cross'>` — Marker shapes for target — see TargetType enum: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/index-default
- `targetColor: string` — Color for the target marker
- `targetWidth: number` — Width for the target marker
- `ranges: RangeModel[]` — Array of range definitions (use `BulletRangeDirective`) — see RangeModel: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/rangemodel
- `minimum: number` — Minimum value for the quantitative scale
- `maximum: number` — Maximum value for the quantitative scale
- `interval: number` — Axis interval
- `tooltip: BulletTooltipSettingsModel` — Tooltip configuration (`enable`, `template`, etc.) — see BulletTooltipSettingsModel: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bullettooltipsettingsmodel
- `dataLabel: BulletDataLabelModel` — Data label configuration — see BulletDataLabelModel: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bulletdatalabelmodel
- `legendSettings: BulletChartLegendSettingsModel` — Legend settings — see: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bulletchartlegendsettingsmodel
- `majorTickLines: MajorTickLinesSettingsModel` — Major tick styling — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/majorticklinessettingsmodel
- `minorTickLines: MinorTickLinesSettingsModel` — Minor tick styling — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/minorticklinessettingsmodel
- `categoryLabelStyle: BulletLabelStyleModel` — Category label style — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bulletlabelstylemodel
- `labelStyle: BulletLabelStyleModel` — Axis label style — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/bulletlabelstylemodel
- `margin: MarginModel` — Chart margins — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/marginmodel
- `animation: AnimationModel` — Animation options — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/animationmodel
- `enableRtl: boolean` — Right-to-left layout
- `orientation: 'Horizontal' | 'Vertical'` — Chart orientation — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/index-default
- `theme: string` — Syncfusion theme name — https://ej2.syncfusion.com/react/documentation/api/bullet-chart/charttheme

## Methods

The component methods are documented on the Bullet Chart API page: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/

- `createSvg(): void` — (Internal) create the SVG tree; can be invoked after render — see component API
- `destroy(): void` — Clean up the component and event handlers — see component API
- `export(type: ExportType, fileName: string, orientation?: any, controls?: any[], width?: number, height?: number, isVertical?: boolean): void` — Export to image/PDF — see component API
- `print(id?: string | string[] | Element): void` — Print the chart — see component API

## Events (selected)

The events and their argument interfaces are documented on the Bullet Chart API pages:

- `beforePrint(args: IPrintEventArgs)` — Triggers before printing starts. See Print events in component API: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/
- `bulletChartMouseClick(args: IBulletMouseEventArgs)` — Triggers on chart element click — args: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/ibulletmouseeventargs
- `legendRender(args: IBulletLegendRenderEventArgs)` — Triggers before the legend is rendered — args: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/ibulletlegendrendereventargs
- `load(args: IBulletLoadedEventArgs)` — Triggers before Bullet Chart loads — args: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/ibulletloadedeventargs
- `loaded(args: IBulletLoadedEventArgs)` — Triggers after Bullet Chart rendering — args: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/ibulletloadedeventargs
- `tooltipRender(args: IBulletchartTooltipEventArgs)` — Triggers before the tooltip is shown — args: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/ibulletcharttooltipeventargs

## Directives

`BulletRangeCollectionDirective` — Parent directive for ranges (use with `BulletRangeDirective`)

`BulletRangeDirective` — Child directive that defines `end`, `color`, `opacity` for a range — see RangeModel: https://ej2.syncfusion.com/react/documentation/api/bullet-chart/rangemodel

## Quick usage snippet

```tsx
<BulletChartComponent
  id="bullet-chart"
  dataSource={data}
  valueField="value"
  targetField="target"
  valueFill="color"
  valueHeight={16}
  valueBorder={{ color: '#222', width: 1 }}
  type="Rect"
  tooltip={{ enable: true }}
  load={handleLoad}
  loaded={handleLoaded}
  tooltipRender={handleTooltipRender}
>
  <Inject services={[BulletTooltip, BulletChartLegend]} />
  <BulletRangeCollectionDirective>
    <BulletRangeDirective end={150} color="#f44336" />
    <BulletRangeDirective end={250} color="#ffb300" />
    <BulletRangeDirective end={300} color="#4caf50" />
  </BulletRangeCollectionDirective>
</BulletChartComponent>
```

For detailed types and the complete API surface consult the official Syncfusion docs: https://ej2.syncfusion.com/react/documentation/bullet-chart/getting-started
