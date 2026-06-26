# CircularChart3DComponent API Reference

This file summarizes the public API (properties, methods, and events) for the `CircularChart3DComponent` based on the official Syncfusion documentation: https://ej2.syncfusion.com/react/documentation/api/circularchart3d/index-default

## Properties

- `background: string` — Chart background color (CSS color). Default: `null`
- `backgroundImage: string` — Background image URL. Default: `null`
- `border: BorderModel` — Border customization (color, width). See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/bordermodel
- `circularChartDataLabel3DModule: CircularChartDataLabel3D` — Data label module.
- `circularChartExport3DModule: CircularChartExport3D` — Export module. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchartexport3d
- `circularChartHighlight3DModule: CircularChartHighlight3D` — Highlight module.
- `circularChartLegend3DModule: CircularChartLegend3D` — Legend module.
- `circularChartSelection3DModule: CircularChartSelection3D` — Selection module. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchartselection3d
- `circularChartTooltip3DModule: CircularChartTooltip3D` — Tooltip module. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularcharttooltip3d
- `dataSource: Object | DataManager` — Data source for the chart. Default: `''`
- `depth: number` — Depth of the circular 3D chart. Default: `50`
- `enableAnimation: boolean` — Enable animations. Default: `true`
- `enableExport: boolean` — Enable export. Default: `false`
- `enablePersistence: boolean` — Persist state between reloads. Default: `false`
- `enableRotation: boolean` — Enable rotation. Default: `false`
- `enableRtl: boolean` — Right-to-left rendering. Default: `false`
- `height: string` — Height (e.g., `100px` or `100%`). Default: `null`
- `highlightColor: string` — Color used for highlight. Default: `''`
- `highlightMode: CircularChart3DHighlightMode` — `None` | `Point`. Default: `None`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dhighlightmode
- `highlightPattern: SelectionPattern` — Highlight pattern (see docs). Default: `None`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/selectionpattern
- `isMultiSelect: boolean` — Enable multi-selection (requires `selectionMode = Point`). Default: `false`
- `legendSettings: CircularChart3DLegendSettingsModel` — Legend options. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dlegendsettingsmodel
- `locale: string` — Locale override. Default: `''`
- `margin: MarginModel` — Chart margins. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/marginmodel
- `rotation: number` — Rotation angle. Default: `0`
- `selectedDataIndexes: IndexesModel[]` — Point indexes to select on load. Default: `[]`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/indexesmodel
- `selectionMode: CircularChart3DSelectionMode` — `None` | `Point`. Default: `None`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dselectionmode
- `selectionPattern: SelectionPattern` — Selection pattern (see docs). Default: `None`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/selectionpattern
- `series: CircularChart3DSeriesModel[]` — Series configuration array. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dseriesmodel
- `subTitle: string` — Chart subtitle. Default: `null`
- `subTitleStyle: FontModel` — Subtitle style options. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/fontmodel
- `theme: CircularChart3DTheme` — Theme. Default: `Material`. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dtheme
- `tilt: number` — Slope angle. Default: `0`
- `title: string` — Chart title. Default: `null`
- `titleStyle: FontModel` — Title style options. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/fontmodel
- `tooltip: CircularChart3DTooltipSettingsModel` — Tooltip options. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dtooltipsettingsmodel
- `useGroupingSeparator: boolean` — Use grouping separators for numbers. Default: `false`
- `width: string` — Width (e.g., `100px` or `100%`). Default: `null`

## Methods

- `export(type: ExportType, fileName: string): void` — Export the chart to image formats (PNG, JPEG, SVG). See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/index-default#methods
- `pdfExport(fileName?: string, orientation?: PdfPageOrientation, controls?: CircularChart3D[], width?: number, height?: number, isVertical?: boolean, header?: IPDFArgs, footer?: IPDFArgs, exportToMultiplePage?: boolean): void` — Export chart(s) to PDF. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/index-default#methods
- `print(id?: string[] | string | Element): void` — Print the chart or element. See https://ej2.syncfusion.com/react/documentation/api/circularchart3d/index-default#methods


## Events

- `afterExport` — Fires after export completes. ([CircularChart3DAfterExportEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dafterexporteventargs)
- `beforeExport` — Fires before export starts. ([CircularChart3DExportEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dexporteventargs)
- `beforePrint` — Fires before print. ([CircularChart3DPrintEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dprinteventargs)
- `beforeResize` — Fires before resizing. ([CircularChart3DBeforeResizeEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dbeforeresizeeventargs)
- `circularChart3DMouseClick` — Fires on chart mouse click. ([CircularChart3DMouseEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dmouseeventargs)
- `circularChart3DMouseDown` — Fires on mouse down. ([CircularChart3DMouseEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dmouseeventargs)
- `circularChart3DMouseLeave` — Fires on mouse leave. ([CircularChart3DMouseEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dmouseeventargs)
- `circularChart3DMouseMove` — Fires on mouse move/hover. ([CircularChart3DMouseEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dmouseeventargs)
- `circularChart3DMouseUp` — Fires on mouse up. ([CircularChart3DMouseEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dmouseeventargs)
- `legendClick` — Fires when legend is clicked. ([CircularChart3DLegendClickEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dlegendclickeventargs)
- `legendRender` — Fires before legend render. ([CircularChart3DLegendRenderEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dlegendrendereventargs)
- `load` — Fires before control is loaded. ([CircularChart3DLoadedEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dloadedeventargs)
- `loaded` — Fires after control is loaded. ([CircularChart3DLoadedEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dloadedeventargs)
- `pointClick` — Fires when a point is clicked. ([CircularChart3DPointEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dpointeventargs)
- `pointMove` — Fires when hovering a point. ([CircularChart3DPointEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dpointeventargs)
- `pointRender` — Fires before a point is rendered. ([CircularChart3DPointRenderEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dpointrendereventargs)
- `resized` — Fires after chart resize. ([CircularChart3DResizeEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dresizeeventargs)
- `selectionComplete` — Fires after selection completes. ([CircularChart3DSelectionCompleteEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dselectioncompleteeventargs)
- `seriesRender` — Fires before a series is rendered. ([CircularChart3DSeriesRenderEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dseriesrendereventargs)
- `textRender` — Fires before data label text render. ([CircularChart3DTextRenderEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dtextrendereventargs)
- `tooltipRender` — Fires when tooltip is ready. ([CircularChart3DTooltipRenderEventArgs] https://ej2.syncfusion.com/react/documentation/api/circularchart3d/circularchart3dtooltiprendereventargs)

## Notes

- This summary follows the official Syncfusion API page for `CircularChart3DComponent`. For detailed types and link targets (models and event args), refer to the official docs: https://ej2.syncfusion.com/react/documentation/api/circularchart3d/index-default
