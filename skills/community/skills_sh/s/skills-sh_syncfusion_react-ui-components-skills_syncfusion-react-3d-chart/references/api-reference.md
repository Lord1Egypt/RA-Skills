# Chart3D API Reference

This file summarizes the public API for `Chart3DComponent` from `@syncfusion/ej2-react-charts`.

## Key Props
- `axes` ([Chart3DAxisModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3daxismodel)[]) — Axis collection (primaryXAxis, primaryYAxis, etc.)
- `series` ([Chart3DSeriesModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dseriesmodel)[]) — Series collection
- `dataSource` (any[]) — Data for the chart
- `depth` (number) — 3D depth
- `rotation` (number) — Horizontal rotation angle
- `tilt` (number) — Vertical tilt angle
- `enableRotation` (boolean) — Enable mouse/touch rotation
- `enableExport` (boolean) — Enable export features
- `legendSettings` ([Chart3DLegendSettingsModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dlegendsettingsmodel)) — Legend configuration
- `tooltip` ([Chart3DTooltipSettingsModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dtooltipsettingsmodel)) — Tooltip configuration
- `palettes` (string[]) — Color palettes for series
- `wallColor` (string) — Wall color
- `wallSize` (number) — Wall thickness
- `selectedDataIndexes` ([IndexesModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/indexesmodel)[][]) — Selected points

## Methods
- `addSeries(seriesCollection: [Chart3DSeriesModel](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dseriesmodel)[]): void` — Add series at runtime
- `removeSeries(index: number): void` — Remove series by index
- `createChartSvg(): void` — Force SVG creation (useful before export)
- `export(type: [ExportType](https://ej2.syncfusion.com/react/documentation/api/chart3d/exporttype), fileName: string): void` — Export chart
- `print(id: string | string[] | Element): void` — Print the chart
- `destroy(): void` — Cleanup

## Events
- `load` ([Chart3DLoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dloadedeventargs)), `loaded` ([Chart3DLoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dloadedeventargs)) — Component lifecycle events
- `beforeExport` ([Chart3DExportEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dexporteventargs)), `afterExport` ([IAfterExportEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/iafterexporteventargs)) — Export lifecycle
- `beforePrint` ([Chart3DPrintEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dprinteventargs)), `resized` ([Chart3DResizeEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dresizeeventargs)) — Print/resize events
- `axisLabelRender` ([Chart3DAxisLabelRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3daxislabelrendereventargs)) — Modify axis label before render
- `pointRender` ([Chart3DPointRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dpointrendereventargs)), `pointClick` ([Chart3DPointEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dpointeventargs)), `pointMove` ([Chart3DPointEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dpointeventargs)) — Per-point rendering and interaction
- `chart3DMouseClick`, `chart3DMouseMove`, `chart3DMouseDown`, `chart3DMouseUp`, `chart3DMouseLeave` ([Chart3DMouseEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dmouseeventargs)) — Mouse interaction events
- `legendClick` ([Chart3DLegendClickEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dlegendclickeventargs)), `legendRender` ([Chart3DLegendRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dlegendrendereventargs)) — Legend events
- `seriesRender` ([Chart3DSeriesRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dseriesrendereventargs)), `selectionComplete` ([Chart3DSelectionCompleteEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dselectioncompleteeventargs)), `tooltipRender` ([Chart3DTooltipRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dtooltiprendereventargs)), `textRender` ([Chart3DTextRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/chart3d/chart3dtextrendereventargs)) — Rendering and selection events

## Child Directives / Subcomponents
- `AnnotationsDirective` / `AnnotationDirective`
- `ColumnsDirective` / `ColumnDirective`
- `RowsDirective` / `RowDirective`
- `RangeColorSettingsDirective` / `RangeColorSettingDirective`
- `TrendlinesDirective` / `TrendlineDirective`
- `MultiLevelLabelsDirective` / `MultiLevelLabelDirective`

### Usage Snippet

```tsx
import {
  Chart3DComponent,
  Chart3DSeriesCollectionDirective,
  Chart3DSeriesDirective,
  Inject,
  ColumnSeries3D,
  Category3D,
  Tooltip3D
} from '@syncfusion/ej2-react-charts';

<Chart3DComponent
  id="chart3d"
  enableRotation={true}
  depth={100}
  rotation={10}
  tilt={8}
  tooltip={{ enable: true }}
>
  <Inject services={[ColumnSeries3D, Category3D, Tooltip3D]} />
  <Chart3DSeriesCollectionDirective>
    <Chart3DSeriesDirective
      dataSource={data}
      xName="x"
      yName="y"
      type="Column"
    />
  </Chart3DSeriesCollectionDirective>
</Chart3DComponent>
```

## Notes

- For full API details (complete typings, interfaces and event argument shapes), consult the official API documentation: https://ej2.syncfusion.com/react/documentation/api/chart3d/index-default
