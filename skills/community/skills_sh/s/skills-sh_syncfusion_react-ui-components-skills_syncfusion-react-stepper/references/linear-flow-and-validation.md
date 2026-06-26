# Linear Flow and Validation

## Table of Contents
- [Linear Stepper](#linear-stepper)
- [Non-Linear Navigation](#non-linear-navigation)
- [Step Validation States](#step-validation-states)
- [Combining Linear Flow with Validation](#combining-linear-flow-with-validation)
- [Resetting Stepper](#resetting-stepper)

## Linear Stepper

Linear steppers enforce sequential navigation, requiring users to complete each step before advancing to the next one. This is ideal for guided workflows like wizards.

### Enabling Linear Mode

```jsx
<StepperComponent linear={true}>
  <StepsDirective>
    <StepDirective label="Step 1" />
    <StepDirective label="Step 2" />
    <StepDirective label="Step 3" />
    <StepDirective label="Step 4" />
  </StepsDirective>
</StepperComponent>
```

**Behavior:**
- Users can only advance to the next step
- Users cannot skip steps
- Users cannot navigate to completed steps unless they go backward sequentially
- Each step must be marked as valid to proceed

### Linear Checkout Flow Example

```jsx
import React, { useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function CheckoutWizard() {
  const [formData, setFormData] = useState({
    email: '',
    address: '',
    payment: ''
  });

  const handleStepChanging = (args) => {
    // Validate current step before allowing transition
    if (args.previousStep === 0 && !formData.email) {
      alert('Please enter your email');
      args.cancel = true;
    }
    if (args.previousStep === 1 && !formData.address) {
      alert('Please enter your address');
      args.cancel = true;
    }
    if (args.previousStep === 2 && !formData.payment) {
      alert('Please select a payment method');
      args.cancel = true;
    }
  };

  return (
    <StepperComponent linear={true} stepChanging={handleStepChanging}>
      <StepsDirective>
        <StepDirective label="Email" />
        <StepDirective label="Address" />
        <StepDirective label="Payment" />
        <StepDirective label="Review" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

## Non-Linear Navigation

Non-linear steppers allow users to navigate freely between steps without enforcing order.

### Enabling Non-Linear Mode

```jsx
<StepperComponent linear={false}>
  <StepsDirective>
    <StepDirective label="Contact" />
    <StepDirective label="Shipping" />
    <StepDirective label="Payment" />
    <StepDirective label="Review" />
  </StepsDirective>
</StepperComponent>
```

**Behavior (Default):**
- Users can click any step to jump to it
- Users can go forward and backward freely
- No forced step order
- Ideal for forms where all steps are independent

### Non-Linear Example: Multi-Tab Form

```jsx
function MultiTabForm() {
  return (
    <StepperComponent linear={false}>
      <StepsDirective>
        <StepDirective iconCss="sf-icon-user" label="Personal Info" />
        <StepDirective iconCss="sf-icon-building" label="Company Details" />
        <StepDirective iconCss="sf-icon-settings" label="Preferences" />
        <StepDirective iconCss="sf-icon-save" label="Review & Submit" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Switching Between Modes Dynamically

```jsx
function App() {
  const [isLinear, setIsLinear] = useState(true);
  const stepperRef = React.useRef(null);

  const toggleLinearMode = () => {
    setIsLinear(!isLinear);
    // Reset stepper when switching modes
    if (stepperRef.current) {
      stepperRef.current.activeStep = 0;
    }
  };

  return (
    <div>
      <label>
        <input 
          type="checkbox" 
          checked={isLinear} 
          onChange={toggleLinearMode}
        />
        Linear Mode
      </label>

      <StepperComponent ref={stepperRef} linear={isLinear}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}
```

## Step Validation States

Mark steps as valid or invalid to indicate completion status:

### Validation Properties

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      label="Completed" 
      isValid={true}
    />
    <StepDirective 
      label="Error" 
      isValid={false}
    />
    <StepDirective 
      label="Pending" 
      isValid={null}
    />
  </StepsDirective>
</StepperComponent>
```

**Values:**
- `true` - Step is valid, shows checkmark/success icon
- `false` - Step has error, shows cross/error icon
- `null` - Step is pending, shows default indicator

### Visual Indicators

The validation state displays differently based on step type:

```jsx
// Default type: Validation icon appears in indicator
<StepperComponent stepType="Default">
  <StepsDirective>
    <StepDirective iconCss="sf-icon-cart" label="Cart" isValid={true} />
    <StepDirective iconCss="sf-icon-transport" label="Delivery" isValid={false} />
  </StepsDirective>
</StepperComponent>

// Label type: Validation icon appears with label
<StepperComponent stepType="Label">
  <StepsDirective>
    <StepDirective label="Cart" isValid={true} />
    <StepDirective label="Delivery" isValid={false} />
  </StepsDirective>
</StepperComponent>

// Indicator type: Only validation icon shows
<StepperComponent stepType="Indicator">
  <StepsDirective>
    <StepDirective text="1" isValid={true} />
    <StepDirective text="2" isValid={false} />
  </StepsDirective>
</StepperComponent>
```

### Dynamic Validation Based on User Input

```jsx
function App() {
  const [steps, setSteps] = useState([
    { label: 'Email', isValid: null },
    { label: 'Address', isValid: null },
    { label: 'Payment', isValid: null }
  ]);

  const [formData, setFormData] = useState({
    email: '',
    address: '',
    payment: ''
  });

  const validateEmail = (value) => {
    const newSteps = [...steps];
    newSteps[0].isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? true : false;
    setSteps(newSteps);
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setFormData({ ...formData, email: value });
    validateEmail(value);
  };

  return (
    <div>
      <StepperComponent>
        <StepsDirective>
          {steps.map((step, index) => (
            <StepDirective key={index} label={step.label} isValid={step.isValid} />
          ))}
        </StepsDirective>
      </StepperComponent>

      <input 
        type="email" 
        value={formData.email}
        onChange={handleEmailChange}
        placeholder="Enter email"
      />
    </div>
  );
}
```

## Combining Linear Flow with Validation

Enforce sequential navigation only for valid steps:

```jsx
function App() {
  const stepperRef = React.useRef(null);
  const [stepValidation, setStepValidation] = useState([
    { label: 'Step 1', isValid: null },
    { label: 'Step 2', isValid: null },
    { label: 'Step 3', isValid: null }
  ]);

  const handleStepChanging = (args) => {
    // Only allow transition if current step is valid
    const currentValidation = stepValidation[args.previousStep];
    
    if (currentValidation.isValid === false) {
      alert('Please fix the errors in the current step');
      args.cancel = true;
    }
  };

  const validateStep = (stepIndex) => {
    const newValidation = [...stepValidation];
    newValidation[stepIndex].isValid = true;
    setStepValidation(newValidation);
  };

  const invalidateStep = (stepIndex) => {
    const newValidation = [...stepValidation];
    newValidation[stepIndex].isValid = false;
    setStepValidation(newValidation);
  };

  return (
    <div>
      <StepperComponent 
        ref={stepperRef}
        linear={true} 
        stepChanging={handleStepChanging}
      >
        <StepsDirective>
          {stepValidation.map((step, index) => (
            <StepDirective 
              key={index}
              label={step.label} 
              isValid={step.isValid}
            />
          ))}
        </StepsDirective>
      </StepperComponent>

      <button onClick={() => validateStep(stepperRef.current.activeStep)}>
        Complete Step
      </button>
      <button onClick={() => invalidateStep(stepperRef.current.activeStep)}>
        Mark Error
      </button>
    </div>
  );
}
```

## Resetting Stepper

Use the `reset()` method to return the stepper to its initial state:

### Basic Reset

```jsx
function App() {
  const stepperRef = React.useRef(null);

  const handleReset = () => {
    stepperRef.current.reset();
  };

  return (
    <div>
      <StepperComponent ref={stepperRef}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
      <button onClick={handleReset}>Reset Stepper</button>
    </div>
  );
}
```

### Reset with Form Clear

```jsx
function App() {
  const stepperRef = React.useRef(null);
  const [formData, setFormData] = useState({
    field1: '',
    field2: '',
    field3: ''
  });

  const handleResetWizard = () => {
    // Reset stepper
    stepperRef.current.reset();
    
    // Clear form data
    setFormData({
      field1: '',
      field2: '',
      field3: ''
    });
    
    // Show confirmation
    alert('Wizard has been reset');
  };

  return (
    <div>
      <StepperComponent ref={stepperRef} linear={true}>
        <StepsDirective>
          <StepDirective label="Information" />
          <StepDirective label="Details" />
          <StepDirective label="Confirm" />
        </StepsDirective>
      </StepperComponent>
      
      <input 
        value={formData.field1}
        onChange={(e) => setFormData({ ...formData, field1: e.target.value })}
      />
      
      <button onClick={handleResetWizard}>Reset All</button>
    </div>
  );
}
```

## Best Practices

**Linear Mode:**
- ✅ Use for guided workflows and wizards
- ✅ Combine with validation on `stepChanging` event
- ✅ Provide clear validation feedback
- ✅ Allow optional steps with `optional={true}`

**Non-Linear Mode:**
- ✅ Use for independent form sections
- ✅ Ideal for settings or configuration panels
- ✅ Allows users to review and edit any section

**Validation:**
- ✅ Use `isValid={true}` for completed steps
- ✅ Use `isValid={false}` for steps with errors
- ✅ Use `isValid={null}` for pending steps
- ✅ Update validation as user fills form
