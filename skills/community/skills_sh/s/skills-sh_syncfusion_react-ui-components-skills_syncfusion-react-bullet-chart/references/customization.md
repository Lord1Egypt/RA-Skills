# Customization Options in React Bullet Chart

## Table of Contents
- [Overview](#overview)
- [Orientation](#orientation)
  - [Horizontal Orientation](#horizontal-orientation-default)
  - [Vertical Orientation](#vertical-orientation)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Animation](#animation)
- [Theme Support](#theme-support)
- [Complete Examples](#complete-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The Bullet Chart provides several customization options to adapt its appearance and behavior to match your application's requirements, including orientation, RTL support, animations, and theming.

## Orientation

The Bullet Chart can be rendered in either horizontal or vertical orientation using the `orientation` property.

### Horizontal Orientation (Default)

By default, the Bullet Chart renders in horizontal orientation, with the value bar extending left to right.

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Revenue"
            orientation="Horizontal"    // Default
            minimum={0}
            maximum={300}
            interval={50}
        />
    );
}
```

**When to use Horizontal:**
- Standard dashboard layouts
- Reading left-to-right progression
- When width is more available than height
- Most common use case

### Vertical Orientation

Set `orientation` to "Vertical" to render the chart vertically, with the value bar extending bottom to top.

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue"
    orientation="Vertical"      // Vertical rendering
    minimum={0}
    maximum={300}
    interval={50}
/>
```

**When to use Vertical:**
- Limited horizontal space
- Aligning with vertical data flow
- Creating columnar dashboard layouts
- Emphasizing vertical growth

### Complete Orientation Example

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div style={{ display: 'flex', gap: '40px' }}>
            {/* Horizontal */}
            <div>
                <h3>Horizontal</h3>
                <BulletChartComponent
                    id="horizontal"
                    dataSource={data}
                    valueField="value"
                    targetField="target"
                    title="Revenue"
                    orientation="Horizontal"
                    minimum={0}
                    maximum={300}
                    width="400px"
                    height="100px"
                >
                    <BulletRangeCollectionDirective>
                        <BulletRangeDirective end={150} color="red" />
                        <BulletRangeDirective end={250} color="yellow" />
                        <BulletRangeDirective end={300} color="green" />
                    </BulletRangeCollectionDirective>
                </BulletChartComponent>
            </div>

            {/* Vertical */}
            <div>
                <h3>Vertical</h3>
                <BulletChartComponent
                    id="vertical"
                    dataSource={data}
                    valueField="value"
                    targetField="target"
                    title="Revenue"
                    orientation="Vertical"
                    minimum={0}
                    maximum={300}
                    width="100px"
                    height="400px"
                >
                    <BulletRangeCollectionDirective>
                        <BulletRangeDirective end={150} color="red" />
                        <BulletRangeDirective end={250} color="yellow" />
                        <BulletRangeDirective end={300} color="green" />
                    </BulletRangeCollectionDirective>
                </BulletChartComponent>
            </div>
        </div>
    );
}
```

## Right-to-Left (RTL) Support

Enable right-to-left rendering for RTL languages (Arabic, Hebrew, etc.) using the `enableRtl` property.

### Enable RTL

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="الإيرادات"           // Arabic title
    enableRtl={true}            // Enable RTL
    minimum={0}
    maximum={300}
/>
```

### Complete RTL Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div dir="rtl">
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="أداء الإيرادات"
                enableRtl={true}
                minimum={0}
                maximum={300}
                interval={50}
                width="600px"
                height="100px"
            />
        </div>
    );
}
```

**When to use RTL:**
- Applications supporting RTL languages
- Middle Eastern markets
- Mirrored layouts for design purposes
- Internationalization (i18n) requirements

## Animation

Configure animations for the actual bar and target bar using the `animation` property. You can control the duration and delay of animations.

### Basic Animation

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    animation={{
        enable: true,
        duration: 1000,         // Animation duration in milliseconds
        delay: 0                // Delay before animation starts
    }}
    minimum={0}
    maximum={300}
/>
```

### Custom Duration and Delay

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    animation={{
        enable: true,
        duration: 1500,         // 1.5 seconds
        delay: 500              // Start after 0.5 seconds
    }}
    minimum={0}
    maximum={300}
/>
```

### Disable Animation

```tsx
<BulletChartComponent
    animation={{
        enable: false           // No animation
    }}
/>
```

### Complete Animation Example

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Animated Chart"
            
            // Animation configuration
            animation={{
                enable: true,
                duration: 1200,     // Smooth 1.2s animation
                delay: 0
            }}
            
            minimum={0}
            maximum={300}
            interval={50}
            width="600px"
            height="100px"
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" />
                <BulletRangeDirective end={250} color="#F39C12" />
                <BulletRangeDirective end={300} color="#27AE60" />
            </BulletRangeCollectionDirective>
        </BulletChartComponent>
    );
}
```

**Animation Properties:**
- **enable**: Boolean to turn animation on/off
- **duration**: Length of animation in milliseconds (500-2000 typical)
- **delay**: Wait time before animation starts in milliseconds

## Theme Support

Apply Syncfusion themes to match your application's design using the `theme` property.

### Available Themes

- **Material**: Google's Material Design
- **Bootstrap**: Bootstrap styling
- **Fabric**: Microsoft Fabric UI
- **Tailwind**: Tailwind CSS styling
- **Bootstrap4**: Bootstrap 4 theme
- **Material3**: Material Design 3
- **Fluent**: Microsoft Fluent Design
- **HighContrast**: High contrast for accessibility

### Apply Theme

```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    theme="Material"            // Material Design theme
    minimum={0}
    maximum={300}
/>
```

### Theme Examples

```tsx
// Material theme
<BulletChartComponent
    theme="Material"
    dataSource={data}
    valueField="value"
    targetField="target"
/>

// Bootstrap theme
<BulletChartComponent
    theme="Bootstrap"
    dataSource={data}
    valueField="value"
    targetField="target"
/>

// High contrast theme for accessibility
<BulletChartComponent
    theme="HighContrast"
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

### Complete Theme Example

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Revenue Performance"
            theme="Bootstrap"           // Bootstrap theme
            minimum={0}
            maximum={300}
            interval={50}
            width="600px"
            height="100px"
        />
    );
}
```

**Note:** Ensure you've imported the corresponding theme CSS file in your application for the theme to apply correctly.

## Complete Examples

### Vertical RTL Chart with Animation

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div dir="rtl">
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="المبيعات"
                
                // Customization
                orientation="Vertical"
                enableRtl={true}
                theme="Material"
                animation={{
                    enable: true,
                    duration: 1000,
                    delay: 200
                }}
                
                minimum={0}
                maximum={300}
                interval={50}
                width="120px"
                height="400px"
            >
                <BulletRangeCollectionDirective>
                    <BulletRangeDirective end={150} color="red" opacity={0.4} />
                    <BulletRangeDirective end={250} color="yellow" opacity={0.4} />
                    <BulletRangeDirective end={300} color="green" opacity={0.4} />
                </BulletRangeCollectionDirective>
            </BulletChartComponent>
        </div>
    );
}
```

### Fully Customized Dashboard Chart

```tsx
import { 
    BulletChartComponent,
    BulletRangeCollectionDirective,
    BulletRangeDirective,
    BulletTooltip,
    Inject
} from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <BulletChartComponent
            id="bulletChart"
            dataSource={data}
            valueField="value"
            targetField="target"
            title="Q1 Revenue Performance"
            subtitle="In Thousands USD"
            
            // Layout
            orientation="Horizontal"
            width="100%"
            height="120px"
            
            // Customization
            theme="Bootstrap4"
            enableRtl={false}
            animation={{
                enable: true,
                duration: 800,
                delay: 0
            }}
            
            // Styling
            valueFill="#5B5FC7"
            valueHeight={18}
            targetColor="#424242"
            targetWidth={5}
            
            // Axis
            minimum={0}
            maximum={300}
            interval={50}
            
            // Tooltip
            tooltip={{ enable: true }}
        >
            <BulletRangeCollectionDirective>
                <BulletRangeDirective end={150} color="#E74C3C" opacity={0.3} />
                <BulletRangeDirective end={250} color="#F39C12" opacity={0.3} />
                <BulletRangeDirective end={300} color="#27AE60" opacity={0.3} />
            </BulletRangeCollectionDirective>
            <Inject services={[BulletTooltip]} />
        </BulletChartComponent>
    );
}
```

## Best Practices

### Orientation
- Use **Horizontal** for most cases (more natural reading)
- Use **Vertical** when horizontal space is limited
- Maintain consistent orientation across related charts
- Adjust dimensions appropriately for orientation

### RTL Support
- Enable only for RTL language content
- Test with actual RTL text, not just enableRtl flag
- Wrap in `<div dir="rtl">` for proper browser support
- Ensure all text elements render correctly

### Animation
- **Duration**: 600-1200ms for smooth feel
- **Delay**: 0-200ms, use delays for sequential charts
- **Disable** for performance-critical dashboards
- **Disable** for static reports or print views

### Themes
- Choose theme matching your application framework
- **Material/Material3**: For Material Design apps
- **Bootstrap/Bootstrap4**: For Bootstrap apps
- **Fluent**: For Microsoft-style apps
- **HighContrast**: For accessibility requirements
- Import correct CSS for chosen theme

## Troubleshooting

**Issue: Orientation not changing**
- Verify orientation value is "Horizontal" or "Vertical" (case-sensitive)
- Check for typos in property name
- Adjust width/height for vertical orientation (more height, less width)
- Clear browser cache if changes not reflecting

**Issue: RTL not working**
- Ensure enableRtl is boolean true, not string "true"
- Add `dir="rtl"` to parent container
- Check if RTL CSS is loaded
- Verify text content is actually in RTL language

**Issue: Animation not smooth**
- Reduce duration (try 600-1000ms)
- Check for performance issues (too many charts)
- Ensure browser supports CSS transitions
- Test in different browsers

**Issue: Animation stuttering**
- Disable animations on other elements during bullet chart animation
- Reduce number of simultaneous animations
- Check CPU/GPU usage
- Simplify chart configuration

**Issue: Theme not applying**
- Verify theme CSS file is imported
- Check theme name matches exactly (case-sensitive)
- Ensure no conflicting CSS overrides
- Import theme CSS before custom styles

**Issue: Theme colors wrong**
- Verify correct theme CSS is loaded
- Check for CSS specificity conflicts
- Clear browser cache
- Inspect element to see computed styles

**Issue: Vertical chart looks wrong**
- Swap width and height values (height should be larger)
- Check title positioning for vertical charts
- Adjust interval if labels overlap
- Increase chart height for better visibility
