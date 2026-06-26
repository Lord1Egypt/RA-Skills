# Orientations and Step Types

## Table of Contents
- [Orientations](#orientations)
- [Step Types](#step-types)
- [Label Positioning](#label-positioning)
- [RTL Support](#rtl-support)
- [Responsive Design](#responsive-design)

## Orientations

The Stepper supports two layout orientations: horizontal and vertical.

### Horizontal Orientation (Default)

Steps are displayed in a left-to-right (or right-to-left) linear arrangement:

```jsx
<StepperComponent orientation="horizontal">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Use Case:** Wide screens, simple linear workflows, checkout flows

### Vertical Orientation

Steps are displayed from top to bottom in a vertical stack:

```jsx
<StepperComponent orientation="vertical">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Use Case:** Mobile screens, complex workflows, space-constrained layouts

## Step Types

The Stepper supports three different visual representations for steps:

### Default Type (Icon + Label)

Displays both the icon and label for each step:

```jsx
<StepperComponent stepType="Default">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Features:**
- Most informative visual representation
- Clear labeling and iconography
- Best for complex workflows

### Label Type (Label Only)

Displays only the step label, hiding icons:

```jsx
<StepperComponent stepType="Label">
  <StepsDirective>
    <StepDirective label="Cart" />
    <StepDirective label="Delivery" />
    <StepDirective label="Payment" />
    <StepDirective label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Features:**
- Minimal, text-focused design
- Good for text-heavy workflows
- Cleaner appearance without icons

### Indicator Type (Icon Only)

Displays only the step indicator (icon or number), hiding labels:

```jsx
<StepperComponent stepType="Indicator">
  <StepsDirective>
    <StepDirective text="1" />
    <StepDirective text="2" />
    <StepDirective text="3" />
    <StepDirective text="4" />
  </StepsDirective>
</StepperComponent>
```

**Features:**
- Compact, space-efficient design
- Icons or numbered indicators
- Best for mobile screens or compact spaces

## Label Positioning

Control where labels appear relative to the step indicator using the `labelPosition` property (only applies to Default and Label step types):

### Top Position

```jsx
<StepperComponent labelPosition="Top">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
  </StepsDirective>
</StepperComponent>
```

### Bottom Position (Default)

```jsx
<StepperComponent labelPosition="Bottom">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
  </StepsDirective>
</StepperComponent>
```

### Start Position (Left/Right in RTL)

```jsx
<StepperComponent labelPosition="Start">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
  </StepsDirective>
</StepperComponent>
```

### End Position (Right/Left in RTL)

```jsx
<StepperComponent labelPosition="End">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
  </StepsDirective>
</StepperComponent>
```

## RTL Support

Enable right-to-left layout for Arabic, Hebrew, and other RTL languages using the `enableRtl` property:

```jsx
<StepperComponent enableRtl={true}>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="السلة" />
    <StepDirective iconCss="sf-icon-transport" label="التوصيل" />
    <StepDirective iconCss="sf-icon-payment" label="الدفع" />
    <StepDirective iconCss="sf-icon-success" label="التأكيد" />
  </StepsDirective>
</StepperComponent>
```

**Effects:**
- Steps flow right-to-left
- Labels positioned on opposite sides
- Navigation reversed
- Text direction automatically adjusted

### Global RTL Configuration

Set RTL for your entire application:

```jsx
import { enableRtl } from '@syncfusion/ej2-base';
enableRtl(true);
```

## Responsive Design

### Responsive Orientation Switching

Automatically switch orientation based on screen size:

```jsx
import React, { useState, useEffect } from 'react';

function App() {
  const [orientation, setOrientation] = useState('horizontal');

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setOrientation('vertical');
      } else {
        setOrientation('horizontal');
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Set initial orientation

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <StepperComponent orientation={orientation}>
      <StepsDirective>
        <StepDirective iconCss="sf-icon-cart" label="Cart" />
        <StepDirective iconCss="sf-icon-transport" label="Delivery" />
        <StepDirective iconCss="sf-icon-payment" label="Payment" />
        <StepDirective iconCss="sf-icon-success" label="Confirmation" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Responsive Step Type Switching

Change step type for mobile:

```jsx
function App() {
  const [stepType, setStepType] = useState('Default');

  useEffect(() => {
    const handleResize = () => {
      setStepType(window.innerWidth < 640 ? 'Indicator' : 'Default');
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <StepperComponent stepType={stepType}>
      <StepsDirective>
        <StepDirective text="1" label="Cart" />
        <StepDirective text="2" label="Delivery" />
        <StepDirective text="3" label="Payment" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### CSS Media Queries for Custom Styling

```css
/* Desktop */
@media (min-width: 768px) {
  .e-stepper {
    padding: 20px;
  }
}

/* Tablet */
@media (min-width: 600px) and (max-width: 767px) {
  .e-stepper {
    padding: 15px;
  }
}

/* Mobile */
@media (max-width: 599px) {
  .e-stepper {
    padding: 10px;
  }
}
```

## Common Combinations

### Mobile-Optimized Checkout
```jsx
<StepperComponent
  orientation="vertical"
  stepType="Indicator"
  labelPosition="End"
>
  {/* steps */}
</StepperComponent>
```

### Desktop-Optimized Progress
```jsx
<StepperComponent
  orientation="horizontal"
  stepType="Default"
  labelPosition="Bottom"
>
  {/* steps */}
</StepperComponent>
```

### Minimal Space-Efficient
```jsx
<StepperComponent
  orientation="horizontal"
  stepType="Indicator"
  labelPosition="Top"
>
  {/* steps */}
</StepperComponent>
```

## Troubleshooting

**Issue: Orientation not changing**
- ✅ Verify `orientation` property is set correctly ("horizontal" or "vertical")
- ✅ Check CSS isn't forcing a specific layout
- ✅ Ensure component re-renders after state change

**Issue: Labels overlapping**
- ✅ Try different `labelPosition` values
- ✅ Use shorter label text
- ✅ Switch to `Indicator` step type to hide labels

**Issue: RTL not working**
- ✅ Verify `enableRtl={true}` is set
- ✅ Check language/text is actually RTL
- ✅ Inspect with DevTools to confirm direction property
