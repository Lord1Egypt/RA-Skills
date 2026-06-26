# Styling and Customization

## Table of Contents
- [CSS Selectors Overview](#css-selectors-overview)
- [Customizing the Track](#customizing-the-track)
- [Customizing the Handle](#customizing-the-handle)
- [Customizing Limits](#customizing-limits)
- [Customizing Ticks](#customizing-ticks)
- [Customizing Buttons](#customizing-buttons)
- [Built-in Themes](#built-in-themes)
- [Advanced Styling](#advanced-styling)
- [Responsive Styling](#responsive-styling)

## CSS Selectors Overview

The RangeSlider component renders with specific CSS classes that can be targeted for customization.

### Main Slider Structure

```html
<div class="e-control-wrapper e-slider-container e-horizontal">
  <div class="e-slider">
    <!-- Track and handles -->
  </div>
  <!-- Ticks, buttons, tooltips -->
</div>
```

### Key CSS Classes

| Class | Element | Purpose |
|-------|---------|---------|
| `.e-slider-container` | Wrapper | Main container |
| `.e-slider` | Track area | Slider track container |
| `.e-slider-track` | Track line | Horizontal/vertical line |
| `.e-handle` | Handle | Draggable handle/thumb |
| `.e-limits` | Limits | Limited area background |
| `.e-scale` | Ticks | Tick marks container |
| `.e-tick` | Tick mark | Individual tick |
| `.e-slider-button` | Button | Inc/dec buttons |

## Customizing the Track

The track is the horizontal or vertical line where handles slide.

### Change Track Color

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: #007bff;
    height: 3px;
}
```

### Track Color for Vertical Slider

```css
.e-control-wrapper.e-slider-container.e-vertical .e-slider-track {
    background: #007bff;
    width: 3px;
}
```

### Full Track Customization

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: linear-gradient(to right, #ff6b6b, #4ecdc4);
    height: 6px;
    border-radius: 3px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### Complete Example

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import './SliderStyles.css';

function StyledTrackSlider() {
  return (
    <SliderComponent
      id="styled-slider"
      value={50}
      min={0}
      max={100}
    />
  );
}

export default StyledTrackSlider;
```

**SliderStyles.css:**
```css
/* Custom track styling */
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: linear-gradient(to right, #667eea, #764ba2);
    height: 4px;
    border-radius: 2px;
}
```

## Customizing the Handle

The handle is the draggable thumb that slides along the track.

### Change Handle Color

```css
.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background-color: #f9920b;
    border-radius: 50%;
    border: 0;
}
```

### Handle with Border

```css
.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background-color: #007bff;
    border: 3px solid white;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
```

### Range Slider: Different Handle Colors

Color first and second handles differently:

```css
/* First handle (start) */
.e-control-wrapper.e-slider-container .e-slider .e-handle.e-handle-start {
    background-color: #5cb85c;
}

/* Second handle (end) */
.e-control-wrapper.e-slider-container .e-slider .e-handle.e-handle-end {
    background-color: #d9534f;
}
```

### Handle Hover Effect

```css
.e-control-wrapper.e-slider-container .e-slider .e-handle:hover {
    background-color: #ff9800;
    transform: scale(1.2);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
```

### Handle Focus Effect

```css
.e-control-wrapper.e-slider-container .e-slider .e-handle:focus {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
}
```

## Customizing Limits

Limits are the restricted/grayed-out areas on the slider.

### Change Limited Area Color

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-limits {
    background-color: rgba(69, 100, 233, 0.46);
}
```

### Multiple Limit Colors

For different restriction areas:

```css
/* First limit area */
.e-control-wrapper.e-slider-container .e-limits:first-of-type {
    background-color: rgba(220, 53, 69, 0.3);  /* Red - restricted */
}

/* Second limit area */
.e-control-wrapper.e-slider-container .e-limits:last-of-type {
    background-color: rgba(220, 53, 69, 0.3);
}
```

### Limit with Pattern

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-limits {
    background: repeating-linear-gradient(
        45deg,
        #ff6b6b,
        #ff6b6b 10px,
        #ff8888 10px,
        #ff8888 20px
    );
    opacity: 0.5;
}
```

## Customizing Ticks

Ticks are scale markers on the slider.

### Major and Minor Ticks

```css
/* Major ticks */
.e-scale .e-tick.e-major {
    width: 2px;
    height: 10px;
    background: #333;
}

/* Minor ticks */
.e-scale .e-tick {
    width: 1px;
    height: 5px;
    background: #999;
}
```

### Tick Text/Labels

```css
.e-scale .e-tick-text {
    font-size: 12px;
    color: #555;
    font-weight: 500;
}
```

### Custom Tick Icons

```css
.e-scale .e-tick.e-custom::before {
    content: '◆';
    position: absolute;
    color: #007bff;
}
```

### Colored Ticks by Position

```css
/* First quarter - green */
.e-scale .e-tick:nth-child(1),
.e-scale .e-tick:nth-child(2) {
    background: #28a745;
}

/* Middle quarters - yellow */
.e-scale .e-tick:nth-child(3),
.e-scale .e-tick:nth-child(4),
.e-scale .e-tick:nth-child(5) {
    background: #ffc107;
}

/* Last quarter - red */
.e-scale .e-tick:nth-child(6) {
    background: #dc3545;
}
```

## Customizing Buttons

Buttons are the increment/decrement controls shown with `showButtons={true}`.

### Change Button Appearance

```css
.e-control-wrapper.e-slider-container .e-slider-button {
    background: #007bff;
    color: white;
    height: 30px;
    width: 30px;
    border-radius: 50%;
    border: none;
}
```

### Button Hover State

```css
.e-control-wrapper.e-slider-container .e-slider-button:hover {
    background: #0056b3;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
```

### Button Focus State

```css
.e-control-wrapper.e-slider-container .e-slider-button:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
}
```

## Built-in Themes

Syncfusion provides pre-built themes that handle styling automatically.

### Available Themes

```tsx
// Import one theme stylesheet:

// Material Design (default)
import '@syncfusion/ej2-react-inputs/styles/material.css';

// Material Dark
import '@syncfusion/ej2-react-inputs/styles/material-dark.css';

// Bootstrap 5
import '@syncfusion/ej2-react-inputs/styles/bootstrap5.css';

// Bootstrap Dark
import '@syncfusion/ej2-react-inputs/styles/bootstrap-dark.css';

// Fluent Design
import '@syncfusion/ej2-react-inputs/styles/fluent.css';

// Tailwind CSS 3
import '@syncfusion/ej2-react-inputs/styles/tailwind3.css';

// Fabric Design
import '@syncfusion/ej2-react-inputs/styles/fabric.css';

// High Contrast
import '@syncfusion/ej2-react-inputs/styles/highcontrast.css';
```

### Switching Themes

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function ThemedSlider() {
  const [theme, setTheme] = useState('material');

  return (
    <div>
      <select onChange={(e) => setTheme(e.target.value)}>
        <option value="material">Material</option>
        <option value="bootstrap5">Bootstrap 5</option>
        <option value="fluent">Fluent</option>
        <option value="tailwind3">Tailwind</option>
      </select>

      <SliderComponent
        id="slider"
        value={50}
        className={`e-theme-${theme}`}
      />
    </div>
  );
}

export default ThemedSlider;
```

## Advanced Styling

### Complete Custom Slider

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';
import './AdvancedSliderStyles.css';

function AdvancedStyledSlider() {
  return (
    <div className="advanced-slider-container">
      <SliderComponent
        id="advanced"
        type="Range"
        value={[25, 75]}
        min={0}
        max={100}
        tooltip={{ isVisible: true, showOn: 'Always' }}
        ticks={{
          placement: 'After',
          largeStep: 25,
          smallStep: 5,
          showSmallTicks: true
        }}
      />
    </div>
  );
}

export default AdvancedStyledSlider;
```

**AdvancedSliderStyles.css:**
```css
.advanced-slider-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

/* Track */
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
  background: rgba(255, 255, 255, 0.3);
  height: 6px;
  border-radius: 3px;
}

/* Handles */
.e-control-wrapper.e-slider-container .e-slider .e-handle {
  background: white;
  border: 4px solid #667eea;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  width: 24px;
  height: 24px;
  transition: all 0.3s ease;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

/* Limits fill */
.e-control-wrapper.e-slider-container.e-horizontal .e-limits {
  background: rgba(255, 255, 255, 0.1);
}

/* Ticks */
.e-scale .e-tick {
  background: rgba(255, 255, 255, 0.6);
}

.e-scale .e-tick-text {
  color: white;
  font-weight: 600;
}

/* Tooltip */
.e-slider-tooltip {
  background: white;
  color: #667eea;
  border-radius: 6px;
  padding: 8px 12px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
```

### Gradient Track

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: linear-gradient(
        to right,
        #ff6b6b 0%,
        #ffd93d 50%,
        #6bcf7f 100%
    );
    height: 8px;
    border-radius: 4px;
}
```

### Neon Style

```css
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: #00ff00;
    height: 3px;
    box-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background: #00ff00;
    border: 2px solid #00ff00;
    box-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00;
}
```

### Neumorphic Design

```css
.e-control-wrapper.e-slider-container {
    background: #e0e5ec;
}

.e-control-wrapper.e-slider-container .e-slider {
    background: #e0e5ec;
    box-shadow: inset 2px 2px 5px #b8b9be,
                inset -3px -3px 7px #ffffff;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background: linear-gradient(135deg, #ffffff 0%, #e0e5ec 100%);
    box-shadow: 2px 2px 5px #b8b9be,
                -3px -3px 7px #ffffff;
}
```

## Responsive Styling

### Mobile Adjustments

```css
/* Larger handles for touch */
@media (max-width: 768px) {
    .e-control-wrapper.e-slider-container .e-slider .e-handle {
        width: 32px;
        height: 32px;
    }

    .e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
        height: 6px;
    }

    /* Larger buttons */
    .e-control-wrapper.e-slider-container .e-slider-button {
        width: 40px;
        height: 40px;
    }
}
```

### Vertical Slider on Mobile

```css
/* Stack vertically on small screens */
@media (max-width: 600px) {
    .slider-container {
        height: 300px;
    }

    .e-slider-container {
        height: 100%;
    }
}
```

### Container Sizing

```css
/* Responsive slider width */
.slider-wrapper {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
}

@media (max-width: 480px) {
    .slider-wrapper {
        max-width: 100%;
        padding: 0 16px;
    }
}
```

## CSS Variables (Theme Customization)

Use CSS custom properties for easier theme switching:

```css
:root {
    --slider-track-bg: #007bff;
    --slider-handle-bg: #f9920b;
    --slider-handle-border: white;
    --slider-limit-bg: rgba(69, 100, 233, 0.46);
    --slider-tick-color: #333;
}

.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: var(--slider-track-bg);
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background-color: var(--slider-handle-bg);
    border-color: var(--slider-handle-border);
}
```

## Common Patterns

### Pattern 1: Material Design

```css
.e-control-wrapper.e-slider-container .e-slider-track {
    background: #1976d2;
    height: 4px;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background: #1976d2;
    width: 20px;
    height: 20px;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle:focus {
    box-shadow: 0 0 0 8px rgba(25, 118, 210, 0.2);
}
```

### Pattern 2: Minimal/Clean

```css
.e-control-wrapper.e-slider-container .e-slider-track {
    background: #e0e0e0;
    height: 2px;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background: white;
    border: 2px solid #999;
    width: 16px;
    height: 16px;
}
```

### Pattern 3: Colorful/Gradient

```css
.e-control-wrapper.e-slider-container .e-slider-track {
    background: linear-gradient(
        to right,
        #ff6b6b,
        #ffd93d,
        #6bcf7f,
        #4ecdc4,
        #667eea
    );
    height: 6px;
}

.e-control-wrapper.e-slider-container .e-slider .e-handle {
    background: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
```

## Troubleshooting

### Styles Not Applying

**Problem:** Custom CSS doesn't affect slider

**Solution:** Ensure specificity matches Syncfusion selectors:
```css
/* May not work */
.slider-track { background: blue; }

/* Works - matches Syncfusion structure */
.e-control-wrapper.e-slider-container.e-horizontal .e-slider-track {
    background: blue;
}
```

### Overriding Theme

**Problem:** Theme CSS overrides custom styles

**Solution:** Use `!important` or import custom CSS after theme:
```tsx
import '@syncfusion/ej2-react-inputs/styles/material.css';
import './CustomSliderStyles.css';  // Import last
```

## Next Steps

1. Choose a built-in theme matching your design
2. Override specific elements as needed with CSS
3. Test responsive behavior on different screen sizes
4. Review [accessibility.md](accessibility.md) for semantic styling
5. Ensure sufficient color contrast for accessibility
