# ProgressBar API Reference

This file provides expanded property signatures for the Syncfusion React `ProgressBarComponent` and direct links to each referenced type on the official docs.

Source: https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default

## Overview
Represents `ProgressBarComponent` (Linear / Circular / Semi-Circular) used to visualize progress.

## Properties (with signatures and links)
- `animation?: AnimationModel` — [AnimationModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/animationmodel): { enable?: boolean; duration?: number; delay?: number } — Animation settings for the progress bar.
- `annotations?: ProgressAnnotationSettingsModel[]` — [ProgressAnnotationSettingsModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/progressannotationsettingsmodel): Annotation configuration objects.
- `cornerRadius?: CornerType` — [CornerType](https://ej2.syncfusion.com/react/documentation/api/progressbar/cornertype): Corner type for ends (e.g., `Auto`, `Round`). Default: `Auto`.
- `enablePersistence?: boolean` — Persist component state between reloads. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `enablePieProgress?: boolean` — Enable pie view for circular type. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `enableProgressSegments?: boolean` — Enable segmented rendering. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `enableRtl?: boolean` — Right-to-left rendering. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `endAngle?: number` — End angle for circular progress. Default: `0`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `gapWidth?: number` — Gap width between segments. Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `height?: string` — CSS height (e.g., `"100px"` or `"50%"`). Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `innerRadius?: string` — inner radius for circular (e.g., `"70%"`). Default: `"100%"`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `isActive?: boolean` — Active state. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `isGradient?: boolean` — Enable gradient fill. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `isIndeterminate?: boolean` — Indeterminate mode (spinner-like). Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `isStriped?: boolean` — Striped appearance. Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `labelOnTrack?: boolean` — Show label on the track. Default: `true`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `labelStyle?: FontModel` — [FontModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/fontmodel): Styling for label text.
- `locale?: string` — Locale string override (e.g., `"en-US"`). ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `margin?: MarginModel` — [MarginModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/marginmodel): Margin settings.
- `maximum?: number` — Maximum progress value. Default: `100`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `minimum?: number` — Minimum progress value. Default: `0`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `progressAnnotationModule?: ProgressAnnotation` — [ProgressAnnotation](https://ej2.syncfusion.com/react/documentation/api/progressbar/progressannotation) — Internal annotation module reference.
- `progressColor?: string` — Progress fill color (CSS color string). Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `progressThickness?: number` — Progress fill thickness in pixels. Default: `0`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `progressTooltipModule?: ProgressTooltip` — [ProgressTooltip](https://ej2.syncfusion.com/react/documentation/api/progressbar/progresstooltip) — Internal tooltip module reference.
- `radius?: string` — Track radius for circular type. Default: `"100%"`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `rangeColors?: RangeColorModel[]` — [RangeColorModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/rangecolormodel): Colors applied to value ranges.
- `role?: ModeType` — [ModeType](https://ej2.syncfusion.com/react/documentation/api/progressbar/modetype): Role/mode for linear progress.
- `secondaryProgress?: number` — Secondary/buffer progress value. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `secondaryProgressColor?: string` — Color for secondary progress. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `secondaryProgressThickness?: number` — Thickness for secondary progress. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `segmentColor?: string[]` — Array of colors used for segments. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `segmentCount?: number` — Number of segments. Default: `1`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `showProgressValue?: boolean` — Display progress text value (percentage). Default: `false`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `startAngle?: number` — Start angle for circular progress. Default: `0`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `theme?: ProgressTheme` — [ProgressTheme](https://ej2.syncfusion.com/react/documentation/api/progressbar/progresstheme): Theme style (Default: `Fabric`).
- `tooltip?: TooltipSettingsModel` — [TooltipSettingsModel](https://ej2.syncfusion.com/react/documentation/api/progressbar/tooltipsettingsmodel): Tooltip customization options.
- `trackColor?: string` — Track color (CSS color string). Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `trackThickness?: number` — Track thickness in pixels. Default: `0`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `type?: ProgressType` — [ProgressType](https://ej2.syncfusion.com/react/documentation/api/progressbar/progresstype): `Linear` | `Circular` | `Semi-Circular`. Default: `Linear`.
- `value?: number` — Current progress value (between `minimum` and `maximum`). Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))
- `width?: string` — CSS width (e.g., `"100%"` or `"200px"`). Default: `null`. ([docs](https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#properties))

## Methods
- `destroy(): void` — Destroy the widget and free resources. (https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default#methods)

## Events (with links)
- `animationComplete` — EmitType<IProgressValueEventArgs> — Fired after animation completes. (https://ej2.syncfusion.com/react/documentation/api/progressbar/iprogressvalueeventargs)
- `load` — EmitType<ILoadedEventArgs> — Fired before the ProgressBar is rendered. (https://ej2.syncfusion.com/react/documentation/api/progressbar/iloadedeventargs)
- `loaded` — EmitType<ILoadedEventArgs> — Fired after the ProgressBar is loaded. (https://ej2.syncfusion.com/react/documentation/api/progressbar/iloadedeventargs)
- `mouseClick` — EmitType<IMouseEventArgs> — Mouse click event. (https://ej2.syncfusion.com/react/documentation/api/progressbar/imouseeventargs)
- `mouseDown` — EmitType<IMouseEventArgs> — Mouse down event. (https://ej2.syncfusion.com/react/documentation/api/progressbar/imouseeventargs)
- `mouseLeave` — EmitType<IMouseEventArgs> — Mouse leave event. (https://ej2.syncfusion.com/react/documentation/api/progressbar/imouseeventargs)
- `mouseMove` — EmitType<IMouseEventArgs> — Mouse move event. (https://ej2.syncfusion.com/react/documentation/api/progressbar/imouseeventargs)
- `mouseUp` — EmitType<IMouseEventArgs> — Mouse up event. (https://ej2.syncfusion.com/react/documentation/api/progressbar/imouseeventargs)
- `progressCompleted` — EmitType<IProgressValueEventArgs> — Fired when progress reaches completion. (https://ej2.syncfusion.com/react/documentation/api/progressbar/iprogressvalueeventargs)
- `textRender` — EmitType<ITextRenderEventArgs> — Fired before label text renders. (https://ej2.syncfusion.com/react/documentation/api/progressbar/itextrendereventargs)
- `tooltipRender` — EmitType<ITooltipRenderEventArgs> — Fired before tooltip renders. (https://ej2.syncfusion.com/react/documentation/api/progressbar/itooltiprendereventargs)
- `valueChanged` — EmitType<IProgressValueEventArgs> — Fired after value changes. (https://ej2.syncfusion.com/react/documentation/api/progressbar/iprogressvalueeventargs)

## Property Usage Guide

### Essential Properties

**For Basic Usage:**
```tsx
<ProgressBarComponent
  id="progress"              // Unique identifier
  type="Linear"              // Linear | Circular | Semicircle
  value={65}                 // 0-100 (current progress)
  height="30"                // CSS height value
/>
```

**For User Feedback:**
```tsx
<ProgressBarComponent
  value={progress}
  showProgressValue={true}   // Display percentage text
  progressValueFormat="N0 '%'"  // Format: "65 %"
/>
```

**For Animations:**
```tsx
<ProgressBarComponent
  value={progress}
  animation={{
    enable: true,
    duration: 1500,          // ms (animation time)
    delay: 0                 // ms (before animation)
  }}
/>
```

**For Indeterminate (Loading):**
```tsx
<ProgressBarComponent
  isIndeterminate={true}    // Spinner mode
  type="Circular"
  animation={{
    enable: true,
    duration: 2000
  }}
/>
```

**For Dual Progress (Buffer):**
```tsx
<ProgressBarComponent
  value={40}                // Actual progress
  secondaryProgress={75}    // Buffer/estimated progress
/>
```

### Styling Properties

```tsx
<ProgressBarComponent
  progressColor="#4CAF50"        // Progress fill color
  trackColor="#e0e0e0"           // Track background color
  progressThickness={4}          // Thickness in pixels
  trackThickness={4}
  isStriped={true}               // Striped pattern
  isGradient={true}              // Gradient effect
  cssClass="custom-class"        // Custom CSS class
/>
```

### Advanced Properties

```tsx
<ProgressBarComponent
  cornerRadius="Round"           // Round | Auto
  enableRtl={false}              // Right-to-left support
  enablePieProgress={true}       // Pie view for circular
  enableProgressSegments={true}  // Segmented rendering
  segmentCount={10}              // Number of segments
/>
```

## Quick Notes

- **Basic progress:** Use `value` prop (0-100)
- **Unknown duration:** Use `isIndeterminate={true}`
- **Buffered scenarios:** Use `secondaryProgress` for dual progress
- **Animations:** Configure via `animation` object (enable, duration, delay)
- **Accessibility:** Always include `aria-label` and role attributes
- **Performance:** Disable animations for real-time updates (>100/sec)
- **Mobile:** Use `Semicircle` type for space-constrained layouts


## Event Handlers

```tsx
// Animation and value changes
onProgressStart={() => {}}           // When animation starts
onProgressComplete={() => {}}        // When reaching 100%
onAnimationComplete={() => {}}       // When animation finishes
onValueChanged={(args) => {}}        // When value changes
onTextRender={(args) => {}}         // Before text renders
onTooltipRender={(args) => {}}      // Before tooltip renders

// Mouse events
onMouseClick={(args) => {}}
onMouseDown={(args) => {}}
onMouseUp={(args) => {}}
onMouseMove={(args) => {}}
onMouseLeave={(args) => {}}

// Lifecycle
onLoad={(args) => {}}                // Before component renders
onLoaded={(args) => {}}              // After component renders
```

## Common Patterns

```tsx
// File Upload Progress
<ProgressBarComponent type="Linear" value={uploadPercent} showProgressValue={true} />

// Loading Spinner
<ProgressBarComponent type="Circular" isIndeterminate={true} height="100px" />

// Streaming/Buffer
<ProgressBarComponent value={played} secondaryProgress={buffered} />

// Multi-step Process
<ProgressBarComponent value={(currentStep / totalSteps) * 100} />
```

## API Documentation Links

- Main API Index: https://ej2.syncfusion.com/react/documentation/api/progressbar/index-default
- ProgressBar Component: https://ej2.syncfusion.com/react/documentation/api/progressbar/progressbarcomponent
- Event Arguments: https://ej2.syncfusion.com/react/documentation/api/progressbar/iprogressvalueeventargs
- Animation Model: https://ej2.syncfusion.com/react/documentation/api/progressbar/animationmodel
