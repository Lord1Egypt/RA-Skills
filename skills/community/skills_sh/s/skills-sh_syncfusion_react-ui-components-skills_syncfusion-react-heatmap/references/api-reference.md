---
title: HeatMap API Reference
---

# HeatMap API Reference

This document summarizes the primary component props, methods, events and commonly used nested models for the Syncfusion React HeatMap (`HeatMapComponent`) based on the official API.

## Component Summary
- Package: `@syncfusion/ej2-react-heatmap`
- Component API: https://ej2.syncfusion.com/react/documentation/api/heatmap/index-default
- Component tag: `HeatMapComponent`

## Key Props (common)
- `dataSource` (Array|Object) — 2D array or data object for cells. Example: `[[1,2],[3,4]]`.
- `xAxis` ([AxisModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/axismodel)) — column axis configuration (`labels`, `valueType`, `interval`, `labelFormat`).
- `yAxis` ([AxisModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/axismodel)) — row axis configuration (`labels`, `valueType`).
- `cellSettings` ([CellSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/cellsettingsmodel)) — controls cell rendering: `showLabel`, `border`, `format`, `enableCellHighlight`.
- `paletteSettings` ([PaletteSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/palettesettingsmodel)) — color palette and ranges for values.
- `legendSettings` ([LegendSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/legendsettingsmodel)) — legend visibility, position, width, format.
- `tooltipSettings` ([TooltipSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/tooltipsettingsmodel)) — control tooltip enablement and format.
- `titleSettings` ([TitleModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/titlemodel)) — title text, alignment, and style.
- `margin` ([MarginModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/marginmodel)) — spacing around the chart: `left`, `right`, `top`, `bottom`.
- `renderingMode` ([DrawType](https://ej2.syncfusion.com/react/documentation/api/heatmap/drawtype)) — rendering engine: `'SVG'` (default) or `'Canvas'` (useful for very large datasets).
- `showTooltip` (boolean) — enable/disable tooltips.
- `enableHtmlSanitizer` (boolean) — sanitize returned HTML in labels/tooltips when enabled.
- `enablePersistence` (boolean) — persist component state across reloads.
- `enableRtl` (boolean) — enable right-to-left layout.
- `height` / `width` (string) — component dimensions (e.g., `'400px'`, `'100%'`).

## Important Methods
- Full methods reference: https://ej2.syncfusion.com/react/documentation/api/heatmap/index-default#methods
- `clearSelection()` — clears any selected cells.
- `destroy()` — clean up the component and detach events.
- `export(type, fileName, orientation?)` — export the heatmap as `PNG|JPEG|SVG|PDF` (type string), optional `fileName` and PDF `orientation`.
- `print()` — print the heatmap.
- `refresh()` — re-render the component after programmatic changes.

## Events
- `cellClick` ([ICellClickEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/icellclickeventargs)) — fired when a cell is clicked. Common args: `rowIndex`, `columnIndex`, `value`, `cell`, `x`, `y`.
- `cellDoubleClick` ([ICellClickEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/icellclickeventargs)) — fired on double-click.
- `cellRender` ([ICellEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/icelleventargs)) — called per-cell during rendering; allow customizing `displayText` or cell styles.
- `cellSelected` ([ISelectedEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/iselectedeventargs)) — fired when selection changes.
- `legendRender` ([ILegendRenderEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/ilegendrendereventargs)) — legend item rendering hook.
- `load` / `loaded` ([ILoadedEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/iloadedeventargs)) — lifecycle events during load/after load.
- `resized` ([IResizeEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/iresizeeventargs)) — after component is resized.
- `tooltipRender` ([ITooltipEventArgs](https://ej2.syncfusion.com/react/documentation/api/heatmap/itooltipeventargs)) — customize tooltip content/format before shown.
- `created` — called after component initialization.

## Common Nested Models (short)

- [CellSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/cellsettingsmodel)
  - `showLabel` (boolean) — show cell labels
  - `format` (string) — format string for display text
  - `border` ({ width:number, color:string }) — cell border

- [LegendSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/legendsettingsmodel)
  - `visible` (boolean)
  - `position` (string) — `'Top'|'Bottom'|'Left'|'Right'`
  - `width` (string|number)

- [PaletteSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/palettesettingsmodel)
  - `palette` (Array) — entries: `{ value, color }` or range objects
  - `type` (string) — `'Gradient'|'Fixed'`

- [AxisModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/axismodel) (xAxis / yAxis)
  - `labels` (Array) — explicit labels for categories
  - `valueType` (string) — `'Numeric'|'Category'|'DateTime'`
  - `labelFormat` (string) — formatting for labels

- [TooltipSettingsModel](https://ej2.syncfusion.com/react/documentation/api/heatmap/tooltipsettingsmodel)
  - `visible` (boolean)
  - `format` (string) — tooltip display format

## Example Snippet (props + events)
```jsx
<HeatMapComponent
  id="heatmap"
  dataSource={data}
  xAxis={{ labels: ['A','B','C'] }}
  yAxis={{ labels: ['X','Y'] }}
  cellSettings={{ showLabel: true, border: { width: 1, color: '#fff' } }}
  legendSettings={{ visible: true, position: 'Bottom' }}
  paletteSettings={{ palette: [{ value: 0, color: '#eef' }, { value: 100, color: '#c33' }], type: 'Gradient' }}
  renderingMode="Canvas"
  cellClick={(args) => console.log('Cell:', args)}
  cellRender={(args) => { args.displayText = args.value + '%'; }}
  created={() => console.log('created')}
>
  <Inject services={[Legend, Tooltip, Adaptor]} />
</HeatMapComponent>
```

## Notes & Tips
- For very large data sets prefer `renderingMode='Canvas'` for performance.
- Use `cellRender` to customize displayed labels without altering data.
- `export()` supports common raster/vector formats; pass `'PDF'` with orientation when needed.

For the authoritative, full API (every prop, event, model and types), refer to the official Syncfusion documentation: https://ej2.syncfusion.com/react/documentation/api/heatmap/index-default
