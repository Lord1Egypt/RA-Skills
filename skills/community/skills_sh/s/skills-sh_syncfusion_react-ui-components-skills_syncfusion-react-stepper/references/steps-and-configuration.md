# Steps and Configuration

## Table of Contents
- [API Patterns](#api-patterns)
- [Adding Steps - Component Pattern](#adding-steps---component-pattern)
- [Adding Steps - Property Pattern](#adding-steps---property-pattern)
- [Step Properties](#step-properties)
- [Setting Active Step](#setting-active-step)
- [Step Status](#step-status)
- [Disabled Steps](#disabled-steps)
- [Optional Steps](#optional-steps)
- [Read-Only Mode](#read-only-mode)
- [CSS Class Customization](#css-class-customization)

## API Patterns

Syncfusion React Stepper supports two implementation patterns. Choose based on your preference:

### Pattern Comparison

| Aspect | Component-Based | Property-Based |
|--------|-----------------|-----------------|
| **Syntax** | Uses `StepsDirective` and `StepDirective` | Uses `steps` array property |
| **Flexibility** | More JSX control, easier to mix with React logic | Cleaner for simple lists |
| **Performance** | Better for dynamic step additions | Better for large step lists |
| **Recommended** | Complex wizards with conditional steps | Static or data-driven steppers |

## Adding Steps - Component Pattern

Use the `StepsDirective` container and `StepDirective` components to add steps to your Stepper. Each `StepDirective` represents a single step in the workflow.

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective />
    <StepDirective />
    <StepDirective />
    <StepDirective />
  </StepsDirective>
</StepperComponent>
```

## Adding Steps - Property Pattern

Define steps as an array and pass to the `steps` property:

```jsx
import React from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const steps = [
    { label: 'Step 1' },
    { label: 'Step 2' },
    { label: 'Step 3' },
    { label: 'Step 4' }
  ];

  return <StepperComponent steps={steps} />;
}

export default App;
```

## Step Properties

Each `StepDirective` supports the following properties for customization:

### Icon CSS

Display an icon for each step using the `iconCss` property:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" />
    <StepDirective iconCss="sf-icon-transport" />
    <StepDirective iconCss="sf-icon-payment" />
    <StepDirective iconCss="sf-icon-success" />
  </StepsDirective>
</StepperComponent>
```

### Label

Display descriptive text below or beside the step indicator using the `label` property:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

### Text Content

Display text instead of icons using the `text` property (useful for numbered steps or indicators):

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective text="1" label="Account" />
    <StepDirective text="2" label="Profile" />
    <StepDirective text="3" label="Verification" />
    <StepDirective text="4" label="Complete" />
  </StepsDirective>
</StepperComponent>
```

**Note:** When both `label` and `text` are defined, the `label` takes priority for display.

### Combined Example

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      iconCss="sf-icon-home" 
      label="Shipping Address"
      text="1"
    />
    <StepDirective 
      iconCss="sf-icon-creditcard" 
      label="Payment Method"
      text="2"
    />
    <StepDirective 
      iconCss="sf-icon-check" 
      label="Review Order"
      text="3"
    />
  </StepsDirective>
</StepperComponent>
```

## Setting Active Step

Control which step is currently active using the `activeStep` property:

```jsx
<StepperComponent activeStep={1}>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Usage:** The `activeStep` is zero-indexed. In the example above, "Delivery" (index 1) is the active step.

### Dynamic Active Step

```jsx
import React, { useState } from 'react';

function App() {
  const [activeStep, setActiveStep] = useState(0);

  return (
    <div>
      <StepperComponent activeStep={activeStep}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
      
      <button onClick={() => setActiveStep(activeStep + 1)}>
        Next
      </button>
    </div>
  );
}
```

## Step Status

Define the completion status of each step using the `status` property. Valid values: `'NotStarted'`, `'InProgress'`, `'Completed'`.

### Component Pattern

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      iconCss="sf-icon-cart" 
      label="Cart"
      status="Completed"
    />
    <StepDirective 
      iconCss="sf-icon-transport" 
      label="Delivery"
      status="InProgress"
    />
    <StepDirective 
      iconCss="sf-icon-payment" 
      label="Payment"
      status="NotStarted"
    />
  </StepsDirective>
</StepperComponent>
```

### Property Pattern

```jsx
const steps = [
  { label: 'Cart', status: 'Completed' },
  { label: 'Delivery', status: 'InProgress' },
  { label: 'Payment', status: 'NotStarted' }
];

<StepperComponent steps={steps} />
```

### Dynamic Status Update

```jsx
const [stepStatus, setStepStatus] = React.useState([
  'Completed', 'InProgress', 'NotStarted'
]);

const steps = [
  { label: 'Step 1', status: stepStatus[0] },
  { label: 'Step 2', status: stepStatus[1] },
  { label: 'Step 3', status: stepStatus[2] }
];

return <StepperComponent steps={steps} />;
```

## Disabled Steps

Prevent user interaction with specific steps using the `disabled` property:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective 
      iconCss="sf-icon-payment" 
      label="Payment" 
      disabled={true}
    />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Use Case:** Disable payment step until shipping address is confirmed.

### Disable Multiple Steps

```jsx
const disabledSteps = [2, 3]; // Disable steps at index 2 and 3

<StepsDirective>
  {steps.map((step, index) => (
    <StepDirective 
      key={index}
      label={step.label}
      disabled={disabledSteps.includes(index)}
    />
  ))}
</StepsDirective>
```

## Optional Steps

Mark steps as optional to indicate they don't need to be completed:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective 
      iconCss="sf-icon-gift" 
      label="Gift Wrap" 
      optional={true}
    />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
  </StepsDirective>
</StepperComponent>
```

**Visual Indicator:** Optional steps display an "optional" label or indicator depending on the step type.

## Read-Only Mode

Disable all user interactions with the Stepper using the `readOnly` property:

```jsx
<StepperComponent readOnly={true}>
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" />
    <StepDirective iconCss="sf-icon-payment" label="Payment" />
    <StepDirective iconCss="sf-icon-success" label="Confirmation" />
  </StepsDirective>
</StepperComponent>
```

**Use Case:** Display stepper as a progress indicator without allowing step changes.

## CSS Class Customization

Apply custom CSS classes to steps for additional styling:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      iconCss="sf-icon-cart" 
      label="Cart"
      cssClass="step-active"
    />
    <StepDirective 
      iconCss="sf-icon-transport" 
      label="Delivery"
      cssClass="step-completed"
    />
    <StepDirective 
      iconCss="sf-icon-payment" 
      label="Payment"
      cssClass="step-pending"
    />
  </StepsDirective>
</StepperComponent>
```

Define CSS classes:

```css
.step-active {
  background-color: #007bff;
  color: white;
}

.step-completed {
  background-color: #28a745;
  color: white;
}

.step-pending {
  background-color: #f5f5f5;
  color: #666;
}
```

## Validation States

Mark steps as valid or invalid to show validation results:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      iconCss="sf-icon-cart" 
      label="Cart"
      isValid={true}
    />
    <StepDirective 
      iconCss="sf-icon-transport" 
      label="Delivery"
      isValid={false}
    />
    <StepDirective 
      iconCss="sf-icon-payment" 
      label="Payment"
      isValid={null}
    />
  </StepsDirective>
</StepperComponent>
```

**Values:**
- `true` - Shows success/checkmark indicator
- `false` - Shows error/cross indicator
- `null` - Default state, no validation indicator

## Troubleshooting

**Issue: Steps not appearing**
- ✅ Ensure `StepsDirective` and `StepDirective` are imported
- ✅ Verify at least one `StepDirective` is defined
- ✅ Check parent `StepperComponent` is rendered

**Issue: Active step not updating**
- ✅ Verify `activeStep` index is valid (0 to steps.length - 1)
- ✅ If using state, ensure state update triggers re-render
- ✅ Check browser DevTools for errors

**Issue: Disabled steps still clickable**
- ✅ Verify `disabled={true}` is set on the step
- ✅ Check CSS isn't overriding disabled styles
- ✅ If using `readOnly`, ensure entire stepper isn't read-only
