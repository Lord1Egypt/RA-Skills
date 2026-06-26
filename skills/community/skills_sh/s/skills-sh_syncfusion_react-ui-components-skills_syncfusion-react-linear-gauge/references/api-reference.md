# Linear Gauge API Reference (React)

This file summarizes the main API surface of the Syncfusion React `LinearGauge` component for quick reference. For full docs see: https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default

## Component
`LinearGaugeComponent` (from `@syncfusion/ej2-react-lineargauge`)

## Key Properties (selected)
- `allowImageExport` (boolean)
- `allowPdfExport` (boolean)
- `allowPrint` (boolean)
- `animationDuration` (number)
- `annotations` (AnnotationModel[]) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/annotationmodel
- `axes` (AxisModel[]) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/axismodel
- `background` (string)
- `border` (BorderModel) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/bordermodel
- `container` (ContainerModel) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/containermodel
- `description` (string)
- `edgeLabelPlacement` (string)
- `enablePersistence` (boolean)
- `enableRtl` (boolean)
- `format` (string)
- `height` (string)
- `margin` (MarginModel) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/marginmodel
- `orientation` (string)
- `rangePalettes` (string[][])
- `theme` (string)
- `title` (string)
- `titleStyle` (FontModel) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/fontmodel
- `tooltip` (TooltipSettingsModel) — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/tooltipsettingsmodel
- `useGroupingSeparator` (boolean)
- `width` (string)

## Methods
- `destroy(): void` — destroy the widget — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default#destroy
- `export(type, fileName, orientation, allowDownload): Promise` — export image/PDF — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default#export
- `print(id?: string | string[] | Element): void` — print the gauge — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default#print
- `setAnnotationValue(annotationIndex, content, axisValue): void` — update annotation — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default#setannotationvalue
- `setPointerValue(axisIndex, pointerIndex, value): void` — set pointer value programmatically — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default#setpointervalue

## Events
- `animationComplete` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/ianimationcompleteeventargs
- `annotationRender` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iannotationrendereventargs
- `axisLabelRender` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iaxislabelrendereventargs
- `beforePrint` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iprinteventargs
- `dragEnd`, `dragMove`, `dragStart` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/ipointerdrageventargs
- `gaugeMouseDown`, `gaugeMouseLeave`, `gaugeMouseMove`, `gaugeMouseUp` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/imouseeventargs
- `load` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iloadeventargs
- `loaded` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iloadedeventargs
- `resized` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/iresizeeventargs
- `tooltipRender` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/itooltiprendereventargs
- `valueChange` — https://ej2.syncfusion.com/react/documentation/api/linear-gauge/ivaluechangeeventargs

## Child directives
- `AnnotationsDirective` > `AnnotationDirective`
- `RangesDirective` > `RangeDirective`
- `PointersDirective` > `PointerDirective`

## Short usage example
```tsx
<LinearGaugeComponent
  allowImageExport
  allowPdfExport
  allowPrint
  animationDuration={1500}
  axes={[{ minimum: 0, maximum: 100 }]}
  annotations={[{ axisIndex:0, axisValue:50, content:'<div>50</div>' }]}
  annotationRender={handleAnnotationRender}
  axisLabelRender={handleAxisLabelRender}
/>
```

## Notes
- Configure ranges, pointers and annotations using the corresponding directives.
- Use `enableDrag` on pointers to allow user interactions; handle `valueChange` to sync state.
- Themes supported (material, bootstrap, fluent, tailwind, etc.) — use the global CSS/theme package.

For complete type definitions, refer to the Syncfusion API docs: https://ej2.syncfusion.com/react/documentation/api/linear-gauge/index-default
