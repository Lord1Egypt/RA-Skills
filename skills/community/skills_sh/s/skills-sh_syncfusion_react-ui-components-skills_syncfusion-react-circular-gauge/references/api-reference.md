# Circular Gauge API Reference

This file summarizes the main component-level API for `CircularGaugeComponent`.
Use it as a quick lookup for props, methods and events. For full details, consult the official docs.

## Component Props

### Core

* `axes: AxisModel[]` — Axis configuration array
* `background: string` — Gauge background color
* `border: BorderModel` — Border configuration
* `centerX / centerY: string` — Gauge center position (%, px)

---

### Interaction & Behavior

* `enablePointerDrag: boolean` — Enable pointer dragging
* `enableRangeDrag: boolean` — Enable range dragging
* `enableRtl: boolean` — Enable RTL layout
* `enablePersistence: boolean` — Persist state across reloads
* `enableGroupingSeparator: boolean` — Format labels with grouping separators
* `enableAnimation: boolean` — Enable animations
* `enableBorderOnMouseMove: boolean` — Highlight border on hover
* `enableHtmlSanitizer: boolean` — Sanitize HTML content

---

### Layout & Appearance

* `height / width: string | number` — Dimensions
* `margin: MarginModel` — Outer margin
* `moveToCenter: boolean` — Move gauge to center
* `radius: string` — Radius of the gauge
* `theme: GaugeTheme` — Theme name
* `title: string` — Title text
* `titleStyle: FontModel` — Title styling

---

### Export & Utilities

* `allowImageExport: boolean` — Enable image export
* `allowPdfExport: boolean` — Enable PDF export
* `allowPrint: boolean` — Enable printing
* `allowMargin: boolean` — Auto margin calculation

---

### Accessibility

* `description: string` — Accessibility description
* `tabIndex: number` — Keyboard navigation index

---

### Localization

* `locale: string` — Locale code

---

### Tooltip & Legend

* `tooltip: TooltipSettingsModel` — Tooltip configuration
* `legendSettings: LegendSettingsModel` — Legend configuration

---

### Animation

* `animationDuration: number` — Global animation duration (ms)

---

## Notes

* `enableGroupingSeparator` replaces incorrect `useGroupingSeparator`
* `axes` is required for rendering
* Properties like `enableAnimation` and `radius` are commonly used but often missed


## Methods
 - `destroy(): void` — Destroys the widget and removes event handlers (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `export(type: 'PNG'|'JPEG'|'SVG'|'PDF', fileName?: string, orientation?: any, allowDownload?: boolean): Promise<any>` — Export gauge (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `print(id?: string | string[] | Element): void` — Print gauge element(s) (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `setAnnotationValue(axisIndex: number, annotationIndex: number, content: string | Function): void` — Update annotation content (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `setPointerValue(axisIndex: number, pointerIndex: number, value: number): void` — Set pointer value programmatically (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `setRangeValue(axisIndex: number, rangeIndex: number, start: number, end: number): void` — Update range start/end values (see Methods: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default#methods)
 - `refresh(): void` — Refreshes the gauge and re-renders the component

## Events (selected)
- `animationComplete` — Fired after animations complete (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/ianimationcompleteeventargs)
 - `annotationRender` — Fired when an annotation is rendered (use to customize content) (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iannotationrendereventargs)
 - `axisLabelRender` — Fired when axis label is rendered (can cancel or modify label) (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iaxislabelrendereventargs)
 - `beforePrint` — Fired before printing (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iprinteventargs)
 - `dragStart` / `dragMove` / `dragEnd` — Pointer drag lifecycle events (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/ipointerdrageventargs)
 - `gaugeMouseDown` / `gaugeMouseMove` / `gaugeMouseUp` / `gaugeMouseLeave` — Mouse interaction events (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/imouseeventargs)
 - `legendRender` — Fired before legend item render (use to customize legend) (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/ilegendrendereventargs)
 - `load` — Fired before the gauge is rendered (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iloadedeventargs)
 - `loaded` — Fired after the gauge is rendered (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iloadedeventargs)
 - `radiusCalculate` — Fired during radius calculation (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iradiuscalculateeventargs)
 - `resized` — Fired after gauge is resized (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/iresizeeventargs)
 - `tooltipRender` — Fired before tooltip shows (modify or cancel) (args: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/itooltiprendereventargs)
 - `tooltipRenderComplete` — Fired after tooltip is rendered

## Child Directives & Models
- `AxesDirective` / `AxisDirective` — Axis configuration wrapper
- `PointersDirective` / `PointerDirective` — Pointer definitions (properties: `value`, `type`, `radius`, `pointerWidth`, `color`, `enableDrag`, `cap`, `needleTail`, `imageUrl`, etc.)
- `RangesDirective` / `RangeDirective` — Range definitions (properties: `start`, `end`, `color`, `startWidth`, `endWidth`, `opacity`, `roundedCorners`)
- `AnnotationsDirective` / `AnnotationDirective` — Annotations (properties: `content`, `angle`, `radius`, `textStyle`, `imageUrl`)


## Quick examples
- Programmatically update pointer value:

```tsx
// set pointer value for axis 0, pointer 0
gaugeRef.current?.setPointerValue(0, 0, 75);
```

- Update an annotation HTML content:

```tsx
gaugeRef.current?.setAnnotationValue(0, 0, `<div style="font-size:14px;">Value: ${value}</div>`);
```

- Export gauge as PNG:

```tsx
await gaugeRef.current?.export('PNG', 'my-gauge');
```

---

For full, authoritative reference with complete type definitions and examples, see the official docs: https://ej2.syncfusion.com/react/documentation/api/circular-gauge/index-default
