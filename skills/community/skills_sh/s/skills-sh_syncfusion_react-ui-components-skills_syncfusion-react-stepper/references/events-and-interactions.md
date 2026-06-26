# Events and Interactions

## Table of Contents
- [Event Types](#event-types)
- [Created Event](#created-event)
- [Step Changed Event](#step-changed-event)
- [Step Changing Event](#step-changing-event)
- [Step Click Event](#step-click-event)
- [Before Step Render Event](#before-step-render-event)
- [Event Handling Patterns](#event-handling-patterns)

## Event Types

The Stepper component triggers five main events during its lifecycle and user interactions:

| Event | When It Fires | Purpose |
|-------|---------------|---------|
| `created` | Component initialization complete | Setup, initialization logic |
| `stepChanged` | After step has changed | Update UI, load content |
| `stepChanging` | Before step is about to change | Validate, prevent transitions |
| `stepClick` | User clicks a step | Track interactions, analytics |
| `beforeStepRender` | Before rendering each step | Customize step appearance |

## Created Event

Fires when the Stepper component has finished rendering and is ready for interaction.

### Basic Usage

```jsx
function App() {
  const handleCreated = () => {
    console.log('Stepper component created and ready');
  };

  return (
    <StepperComponent created={handleCreated}>
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Practical Example: Initialization

```jsx
function App() {
  const stepperRef = React.useRef(null);

  const handleCreated = () => {
    // Set initial properties after creation
    if (stepperRef.current) {
      console.log('Stepper initialized with', stepperRef.current.steps.length, 'steps');
    }
  };

  return (
    <StepperComponent ref={stepperRef} created={handleCreated}>
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
        <StepDirective label="Step 3" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

## Step Changed Event

Fires after the active step has successfully changed.

### Event Arguments

```typescript
interface StepperChangedEventArgs {
  activeStep: number;     // Index of the new active step
  previousStep: number;   // Index of the previous step
  isInteracted: boolean;  // true if user interacted, false if programmatic
  name: string;          // Event name: "stepChanged"
  event: Event;          // DOM event object
  element?: HTMLElement; // The changed step element
}
```

### Basic Usage

```jsx
function App() {
  const handleStepChanged = (args) => {
    console.log(`Step changed from ${args.previousStep} to ${args.activeStep}`);
  };

  return (
    <StepperComponent stepChanged={handleStepChanged}>
      <StepsDirective>
        <StepDirective label="Cart" />
        <StepDirective label="Delivery" />
        <StepDirective label="Payment" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Practical Example: Load Content Based on Step

```jsx
function App() {
  const [stepContent, setStepContent] = React.useState('');

  const handleStepChanged = (args) => {
    const contents = [
      'Review your shopping cart',
      'Enter shipping address',
      'Select payment method'
    ];
    setStepContent(contents[args.activeStep] || '');
  };

  return (
    <div>
      <StepperComponent stepChanged={handleStepChanged}>
        <StepsDirective>
          <StepDirective label="Cart" />
          <StepDirective label="Delivery" />
          <StepDirective label="Payment" />
        </StepsDirective>
      </StepperComponent>
      <div className="content-panel">
        {stepContent}
      </div>
    </div>
  );
}
```

## Step Changing Event

Fires **before** the step is about to change. Cancel the navigation to prevent the change.

### Event Arguments

```typescript
interface StepperChangingEventArgs {
  activeStep: number;     // Index of the step being changed to
  previousStep: number;   // Index of the current step
  cancel: boolean;        // Set to true to prevent the change
  isInteracted: boolean;  // true if user interacted, false if programmatic
  name: string;          // Event name: "stepChanging"
  event: Event;          // DOM event object
  element?: HTMLElement; // The step element being changed to
}
```

### Basic Usage

```jsx
function App() {
  const handleStepChanging = (args) => {
    console.log(`Attempting to change from ${args.previousStep} to ${args.activeStep}`);
  };

  return (
    <StepperComponent stepChanging={handleStepChanging}>
      <StepsDirective>
        <StepDirective label="Cart" />
        <StepDirective label="Delivery" />
        <StepDirective label="Payment" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Practical Example: Validation Before Transition

```jsx
function App() {
  const [formData, setFormData] = React.useState({
    email: '',
    address: '',
    payment: ''
  });

  const handleStepChanging = (args) => {
    if (args.previousStep === 0 && !formData.email) {
      alert('Please enter your email address');
      args.cancel = true; // Prevent transition
    }
    if (args.previousStep === 1 && !formData.address) {
      alert('Please enter your shipping address');
      args.cancel = true;
    }
    if (args.previousStep === 2 && !formData.payment) {
      alert('Please select a payment method');
      args.cancel = true;
    }
  };

  return (
    <StepperComponent stepChanging={handleStepChanging}>
      <StepsDirective>
        <StepDirective label="Contact Info" />
        <StepDirective label="Shipping" />
        <StepDirective label="Payment" />
        <StepDirective label="Review" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Complex Validation Pattern

```jsx
function validateStep(stepIndex, formData) {
  const validations = [
    { field: 'email', errorMsg: 'Email is required' },
    { field: 'address', errorMsg: 'Address is required' },
    { field: 'payment', errorMsg: 'Payment method is required' }
  ];
  
  if (stepIndex < validations.length) {
    const validation = validations[stepIndex];
    if (!formData[validation.field]) {
      return { valid: false, message: validation.errorMsg };
    }
  }
  return { valid: true };
}

const handleStepChanging = (args) => {
  const validation = validateStep(args.previousStep, formData);
  if (!validation.valid) {
    alert(validation.message);
    args.cancel = true;
  }
};
```

## Step Click Event

Fires when the user clicks on a step.

### Event Arguments

```typescript
interface StepperClickEventArgs {
  activeStep: number;    // Index of the clicked step
  name: string;         // Event name: "stepClick"
  event: Event;         // DOM event object
  element?: HTMLElement; // The clicked step element
}
```

### Basic Usage

```jsx
function App() {
  const handleStepClick = (args) => {
    console.log(`User clicked on step ${args.activeStep}`);
  };

  return (
    <StepperComponent stepClick={handleStepClick}>
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
        <StepDirective label="Step 3" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Practical Example: Analytics Tracking

```jsx
function App() {
  const handleStepClick = (args) => {
    // Track user interaction for analytics
    analytics.track('step_clicked', {
      stepIndex: args.activeStep,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <StepperComponent stepClick={handleStepClick}>
      <StepsDirective>
        <StepDirective label="Cart" />
        <StepDirective label="Delivery" />
        <StepDirective label="Payment" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

## Before Step Render Event

Fires before each step is rendered, allowing you to customize the step appearance.

### Event Arguments

```typescript
interface StepperRenderingEventArgs {
  activeStep: number;    // Index of the step being rendered
  name: string;         // Event name: "beforeStepRender"
  element?: HTMLElement; // The step element being rendered
}
```

### Basic Usage

```jsx
function App() {
  const handleBeforeStepRender = (args) => {
    console.log(`Rendering step ${args.currentStep}`);
  };

  return (
    <StepperComponent beforeStepRender={handleBeforeStepRender}>
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Practical Example: Dynamic Styling

```jsx
function App() {
  const handleBeforeStepRender = (args) => {
    if (args.element) {
      // Add custom classes based on step index
      if (args.activeStep === 0) {
        args.element.classList.add('first-step');
      } else if (args.activeStep === 3) {
        args.element.classList.add('last-step');
      }
    }
  };

  return (
    <StepperComponent beforeStepRender={handleBeforeStepRender}>
      <StepsDirective>
        <StepDirective label="Start" />
        <StepDirective label="Middle 1" />
        <StepDirective label="Middle 2" />
        <StepDirective label="Complete" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

## Event Handling Patterns

### Pattern 1: Multiple Events Combined

```jsx
function App() {
  const [status, setStatus] = React.useState('');

  const handleCreated = () => {
    setStatus('Stepper ready');
  };

  const handleStepChanging = (args) => {
    setStatus(`Validating transition from step ${args.previousStep}...`);
  };

  const handleStepChanged = (args) => {
    setStatus(`Now on step ${args.activeStep}`);
  };

  return (
    <div>
      <StepperComponent
        created={handleCreated}
        stepChanging={handleStepChanging}
        stepChanged={handleStepChanged}
      >
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
      <p>Status: {status}</p>
    </div>
  );
}
```

### Pattern 2: Conditional Event Handling

```jsx
function App() {
  const stepperRef = React.useRef(null);

  const handleStepClick = (args) => {
    // Only allow clicking completed steps
    if (args.activeStep > currentStep) {
      stepperRef.current.activeStep = currentStep;
    }
  };

  return (
    <StepperComponent ref={stepperRef} stepClick={handleStepClick}>
      {/* steps */}
    </StepperComponent>
  );
}
```

### Pattern 3: Preventing Backward Navigation

```jsx
function App() {
  const handleStepChanging = (args) => {
    // Prevent users from going back
    if (args.activeStep < args.previousStep) {
      args.cancel = true;
      alert('You cannot go back in this wizard');
    }
  };

  return (
    <StepperComponent stepChanging={handleStepChanging}>
      {/* steps */}
    </StepperComponent>
  );
}
```

## Troubleshooting

**Issue: Event handler not firing**
- ✅ Verify event name is spelled correctly (e.g., `stepChanged`, not `onStepChanged`)
- ✅ Ensure handler function is properly defined
- ✅ Check that the event trigger condition is met

**Issue: Cancel not working in stepChanging**
- ✅ Verify `args.cancel = true` is set before event completes
- ✅ Check that step is not disabled
- ✅ Ensure linear mode isn't preventing the behavior
