````markdown
# TreeMap API Quick Reference

This reference summarizes the main properties, methods, and events of the Syncfusion React `TreeMap` component. For the full API and exact type definitions, see: https://ej2.syncfusion.com/react/documentation/api/treemap/index-default

## Properties (high-level)
- `allowImageExport` (boolean) — Enable exporting the TreeMap as an image. Default: `false`
- `allowPdfExport` (boolean) — Enable exporting the TreeMap as PDF. Default: `false`
- `allowPrint` (boolean) — Enable printing via the `print` API. Default: `false`
- `background` (string) — Background color of the TreeMap container.
- `border` (object) — Global border settings for the component (e.g., `{ color: string, width: number }`).
- `breadcrumbConnector` (string) — Separator shown between breadcrumb items when `enableBreadcrumb` is true.
- `colorValuePath` (string) — Data field used for color mapping (continuous palettes).
- `dataSource` (Array|DataManager) — The data source for TreeMap (flat array or hierarchical structure).
- `description` (string) — Description text used for accessibility.
- `drillDownView` (boolean) — Use drill-down view layout when `enableDrillDown` is enabled. Default: `false`
- `enableBreadcrumb` (boolean) — Show breadcrumb navigation for drill-down. Default: `false`
- `enableDrillDown` (boolean) — Enable click-to-drill down interactions. Default: `false`
- `enableHtmlSanitizer` (boolean) — Sanitize HTML in templates/tooltips to avoid XSS. Default: `true`
- `enablePersistence` (boolean) — Persist component state between page reloads. Default: `false`
- `enableRtl` (boolean) — Enable right-to-left rendering. Default: `false`
- `equalColorValuePath` (string[]) — Field(s) to use for categorical/equal color mapping.
- `format` (string) — Format string for labels or values.
- `height` (string|number) — Height of the TreeMap (e.g., `350px` or `100%`).
- `highlightSettings` (object) — Settings for highlight behavior and styling.
- `initialDrillDown` (object) — Configuration for initial drill-down state.
- `layoutType` (string) — Layout algorithm: `Squarified` (default), `SliceAndDiceHorizontal`, `SliceAndDiceVertical`, `SliceAndDiceAuto`, etc.
- `leafItemSettings` (object) — Configuration for leaf items (e.g., `labelPath`, `border`, `colorMapping`, `gap`, `showLabels`).
- `legendSettings` (object) — Legend configuration (position, size, title, etc.).
- `levels` (array) — Array of level configuration objects for grouped hierarchies (`LevelSettingsModel[]`).
- `locale` (string) — Current locale used for formatting and messages.
- `margin` (object) — Margin settings for the TreeMap (`{ top, right, bottom, left }`).
- `palette` (string[]) — Array of colors used for filling items when color mapping is not explicit.
- `query` (Query) — External `Query` (DataManager) used for remote data operations.
- `rangeColorValuePath` (string[]) — Field(s) used for range color mapping.
- `renderDirection` (string) — Rendering direction (e.g., `TopLeftBottomRight`).
- `selectionSettings` (object) — Selection-related settings (mode, enable, etc.).
- `tabIndex` (number) — Tab index for keyboard navigation. Default: `0`
- `theme` (string) — Theme name (e.g., `Material`, `Bootstrap`).
- `titleSettings` (object) — Title and subtitle configuration.
- `tooltipSettings` (object) — Tooltip configuration (templates, enable, format).
- `useGroupingSeparator` (boolean) — Use grouping separator for numbers (e.g., `1,000`). Default: `true`
- `weightValuePath` (string) — Data field used to compute area/weight for each item.
- `width` (string|number) — Width of the TreeMap.

## Methods
- `destroy()` — Destroys the TreeMap instance and removes event listeners.
- `doubleClickOnTreeMap(e)` — Programmatically trigger double-click handling on the TreeMap.
- `export(type, fileName, orientation, allowDownload)` — Export the TreeMap in `PNG|JPEG|SVG|PDF`. Returns a Promise for some export flows (PDF).
- `print(id)` — Print TreeMap by passing an element id, DOM element, or list of ids.
- `selectItem(levelOrder, isSelected)` — Select or deselect items using a `levelOrder` array identifying the item's path.

## Events
- `beforePrint` — Fired before printing/export is performed.
- `click` / `itemClick` — Fired when an item is clicked (include item details in args).
- `doubleClick` — Fired when an item is double-clicked.
- `drillStart` / `drillEnd` — Fired when drill-down begins and completes.
- `itemRendering` — Fired when an item is being rendered (use this to customize fill/label at render time).
- `itemHighlight` — Fired when an item is highlighted (hover or programmatic).
- `itemMove` — Fired when an item is moved (drag/drop related scenarios).
- `itemSelected` — Fired after an item is selected.
- `legendItemRendering` / `legendRendering` — Events during legend rendering.
- `load` / `loaded` — Lifecycle events fired before/after the component load.
- `mouseMove` / `rightClick` — Pointer interaction events providing mouse coordinates and target item.
- `resize` — Fired when component size changes.
- `tooltipRendering` — Fired when preparing tooltip content; modify tooltip text/template here.


## Example — programmatic export & selection

```jsx
import React, { useRef } from 'react';
const treemapRef = useRef(null);

// Export as PDF
treemapRef.current?.export('PDF', 'MyTreeMap');

// Select item by level order (example path)
treemapRef.current?.selectItem(['Country','State','City'], true);
```

---

For complete and typed API definitions, including nested models (`LeafItemSettingsModel`, `LevelSettingsModel`, `LegendSettingsModel`, etc.), consult the official docs: https://ej2.syncfusion.com/react/documentation/api/treemap/index-default

## Online references for complex models, methods and events
Use the links below to jump to the official, typed API documentation for complex nested models, key methods, and events used by `TreeMap`.

- `LeafItemSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/leafitemsettingsmodel
- `LevelSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/levelsettingsmodel
- `LegendSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/legendsettingsmodel
- `TooltipSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/tooltipsettingsmodel
- `SelectionSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/selectionsettingsmodel
- `HighlightSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/highlightsettingsmodel
- `TitleSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/titlesettingsmodel
- `MarginModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/marginmodel
- `InitialDrillSettingsModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/initialdrillsettingsmodel
- `BorderModel`: https://ej2.syncfusion.com/react/documentation/api/treemap/bordermodel
- `Query` (DataManager query): https://ej2.syncfusion.com/react/documentation/api/data/data-manager#query

- Methods (TreeMap): https://ej2.syncfusion.com/react/documentation/api/treemap/index-default#methods
- Events (TreeMap): https://ej2.syncfusion.com/react/documentation/api/treemap/index-default#events

If you need inline anchor links for any additional nested model or a specific event signature, tell me which ones and I'll add them.
```
