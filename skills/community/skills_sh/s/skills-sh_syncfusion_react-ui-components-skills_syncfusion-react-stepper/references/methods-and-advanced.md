```markdown
# Methods and Advanced Patterns

## Table of Contents
- [Component Methods](#component-methods)
  - [reset()](#reset)
  - [nextStep()](#nextstep)
  - [previousStep()](#previousstep)
  - [refreshProgressbar()](#refreshprogressbar)
  - [destroy()](#destroy)
- [Both API Patterns - Complete Guide](#both-api-patterns---complete-guide)
- [Advanced Pattern Examples](#advanced-pattern-examples)
- [Performance Optimization](#performance-optimization)
- [Common Gotchas](#common-gotchas)

## Component Methods

### reset()

Reset the Stepper component to its initial state. This method sets the active step to 0 and clears any step states.

**Syntax:**
```typescript
stepperRef.current.reset(): void
```

**Example - Component Pattern:**
```jsx
import React, { useRef } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);

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

export default App;
```

**Example - Property Pattern:**
```jsx
import React, { useRef } from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);
  const steps = [
    { label: 'Step 1' },
    { label: 'Step 2' },
    { label: 'Step 3' }
  ];

  const handleReset = () => {
    stepperRef.current.reset();
  };

  return (
    <div>
      <StepperComponent ref={stepperRef} steps={steps} />
      <button onClick={handleReset}>Reset Stepper</button>
    </div>
  );
}

export default App;
```

**Use Cases:**
- Reset multi-step form after submission
- Clear wizard state when user clicks "Start Over"
- Reset state on navigation or modal close

### nextStep()

Move to the next step from the current step in the Stepper.

**Syntax:**
```typescript
stepperRef.current.nextStep(): void
```

**Example:**
```jsx
import React, { useRef } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);

  const handleNextStep = () => {
    stepperRef.current.nextStep();
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
      <button onClick={handleNextStep}>Next Step</button>
    </div>
  );
}

export default App;
```

**Use Cases:**
- Navigate forward programmatically
- "Next" button functionality
- Automatic step progression after validation

### previousStep()

Move to the previous step from the current step in the Stepper.

**Syntax:**
```typescript
stepperRef.current.previousStep(): void
```

**Example:**
```jsx
import React, { useRef } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);

  const handlePreviousStep = () => {
    stepperRef.current.previousStep();
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
      <button onClick={handlePreviousStep}>Previous Step</button>
    </div>
  );
}

export default App;
```

**Use Cases:**
- Navigate backward programmatically
- "Back" button functionality
- Allow users to edit previous steps

### refreshProgressbar()

Refreshes the position of the progress bar programmatically when the dimensions of the parent container are changed (e.g., on window resize).

**Syntax:**
```typescript
stepperRef.current.refreshProgressbar(): void
```

**Example:**
```jsx
import React, { useRef, useEffect } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);

  useEffect(() => {
    // Refresh progress bar on window resize
    const handleResize = () => {
      if (stepperRef.current) {
        stepperRef.current.refreshProgressbar();
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <StepperComponent ref={stepperRef}>
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
        <StepDirective label="Step 3" />
      </StepsDirective>
    </StepperComponent>
  );
}

export default App;
```

**Example - Responsive Container:**
```jsx
import React, { useRef, useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(100);

  const handleWidthChange = (newWidth) => {
    setContainerWidth(newWidth);
    // Refresh progress bar after container width changes
    setTimeout(() => {
      if (stepperRef.current) {
        stepperRef.current.refreshProgressbar();
      }
    }, 0);
  };

  return (
    <div>
      <div style={{ width: `${containerWidth}%`, overflow: 'auto' }}>
        <StepperComponent ref={stepperRef}>
          <StepsDirective>
            <StepDirective label="Step 1" />
            <StepDirective label="Step 2" />
            <StepDirective label="Step 3" />
          </StepsDirective>
        </StepperComponent>
      </div>
      <button onClick={() => handleWidthChange(50)}>50%</button>
      <button onClick={() => handleWidthChange(100)}>100%</button>
    </div>
  );
}

export default App;
```

**Use Cases:**
- Adjust progress bar on responsive layout changes
- Update layout after modal resize
- Recalculate position after DOM reflow

### destroy()

Destroy the Stepper control and release all resources.

**Syntax:**
```typescript
stepperRef.current.destroy(): void
```

**Example:**
```jsx
import React, { useRef, useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function App() {
  const stepperRef = useRef(null);
  const [isDestroyed, setIsDestroyed] = useState(false);

  const handleDestroy = () => {
    if (stepperRef.current) {
      stepperRef.current.destroy();
      setIsDestroyed(true);
    }
  };

  if (isDestroyed) {
    return <p>Stepper has been destroyed</p>;
  }

  return (
    <div>
      <StepperComponent ref={stepperRef}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
      <button onClick={handleDestroy}>Destroy Stepper</button>
    </div>
  );
}

export default App;
```

**Example - Cleanup on Unmount:**
```jsx
import React, { useRef, useEffect } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function StepperModal({ isOpen, onClose }) {
  const stepperRef = useRef(null);

  useEffect(() => {
    // Cleanup when modal closes
    return () => {
      if (stepperRef.current && isOpen) {
        stepperRef.current.destroy();
      }
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="modal">
      <StepperComponent ref={stepperRef}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
        </StepsDirective>
      </StepperComponent>
      <button onClick={onClose}>Close</button>
    </div>
  );
}

export default StepperModal;
```

**Use Cases:**
- Clean up resources when component unmounts
- Remove event listeners
- Prepare for component disposal
- Free memory in Single Page Applications (SPAs)

### Methods Summary Table

| Method | Parameters | Returns | Purpose |
|--------|-----------|---------|---------|
| `reset()` | none | void | Reset to first step and clear state |
| `nextStep()` | none | void | Move to next step programmatically |
| `previousStep()` | none | void | Move to previous step programmatically |
| `refreshProgressbar()` | none | void | Update progress bar on container resize |
| `destroy()` | none | void | Destroy component and release resources |

## Both API Patterns - Complete Guide

### Pattern 1: Component-Based (StepsDirective)

**Advantages:**
- More flexible JSX control
- Easier to add conditional rendering of steps
- Better for complex workflows with dynamic steps
- Mix React logic directly in JSX

**Full Example:**
```jsx
import React, { useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function CheckoutWizard() {
  const [formData, setFormData] = useState({
    email: '',
    address: '',
    payment: ''
  });

  const [completedSteps, setCompletedSteps] = useState({
    0: false,
    1: false,
    2: false
  });

  const handleStepChanging = (args) => {
    // Validate before allowing transition
    if (args.activeStep === 0 && !formData.email) {
      args.cancel = true;
      alert('Please enter email');
    }
  };

  const handleStepChanged = (args) => {
    setCompletedSteps({
      ...completedSteps,
      [args.previousStep]: true
    });
  };

  return (
    <div>
      <StepperComponent 
        stepChanging={handleStepChanging}
        stepChanged={handleStepChanged}
      >
        <StepsDirective>
          <StepDirective 
            iconCss="sf-icon-mail" 
            label="Email"
            status={completedSteps[0] ? 'Completed' : 'NotStarted'}
          />
          <StepDirective 
            iconCss="sf-icon-home" 
            label="Address"
            status={completedSteps[1] ? 'Completed' : 'NotStarted'}
          />
          <StepDirective 
            iconCss="sf-icon-payment" 
            label="Payment"
            status={completedSteps[2] ? 'Completed' : 'NotStarted'}
          />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}

export default CheckoutWizard;
```

### Pattern 2: Property-Based (steps Array)

**Advantages:**
- Cleaner, more declarative code
- Better for data-driven steppers
- Easier to manage large step lists
- Better performance with many steps

**Full Example:**
```jsx
import React, { useState } from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';

function CheckoutWizard() {
  const [activeStep, setActiveStep] = useState(0);
  const [stepStatus, setStepStatus] = useState(['NotStarted', 'NotStarted', 'NotStarted']);

  const steps = [
    { 
      label: 'Email',
      iconCss: 'sf-icon-mail',
      status: stepStatus[0]
    },
    { 
      label: 'Address',
      iconCss: 'sf-icon-home',
      status: stepStatus[1]
    },
    { 
      label: 'Payment',
      iconCss: 'sf-icon-payment',
      status: stepStatus[2]
    }
  ];

  const handleStepChanging = (args) => {
    if (args.activeStep === 0) {
      args.cancel = true;
      alert('Validate email first');
    }
  };

  const handleStepChanged = (args) => {
    // Update status
    const newStatus = [...stepStatus];
    newStatus[args.previousStep] = 'Completed';
    setStepStatus(newStatus);
    setActiveStep(args.activeStep);
  };

  return (
    <StepperComponent 
      steps={steps}
      activeStep={activeStep}
      stepChanged={handleStepChanged}
      stepChanging={handleStepChanging}
    />
  );
}

export default CheckoutWizard;
```

### Pattern Comparison in Real Code

| Scenario | Component Pattern | Property Pattern |
|----------|-------------------|------------------|
| **Conditional steps** | Easy: `{showOptional && <StepDirective ... />}` | Harder: Manage array filtering |
| **Many steps (50+)** | Less efficient | More efficient |
| **Data-driven steps** | Requires mapping logic | Natural fit |
| **Inline styling** | Mixed with JSX | Separated concerns |

## Advanced Pattern Examples

### Example 1: Linear Wizard with Validation

Using component pattern with linear flow:

```jsx
import React, { useState, useRef } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function LinearWizard() {
  const stepperRef = useRef(null);
  const [formErrors, setFormErrors] = useState({});

  const validateStep = (stepIndex) => {
    const errors = {};
    if (stepIndex === 0 && !formData.email) {
      errors.email = 'Email required';
    }
    if (stepIndex === 1 && !formData.phone) {
      errors.phone = 'Phone required';
    }
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleStepChanging = (args) => {
    if (!validateStep(args.activeStep)) {
      args.cancel = true;
    }
  };

  return (
    <StepperComponent 
      ref={stepperRef}
      linear={true}
      stepChanging={handleStepChanging}
    >
      <StepsDirective>
        <StepDirective label="Contact" iconCss="sf-icon-mail" />
        <StepDirective label="Address" iconCss="sf-icon-home" />
        <StepDirective label="Review" iconCss="sf-icon-check" />
      </StepsDirective>
    </StepperComponent>
  );
}

export default LinearWizard;
```

### Example 2: Dynamic Steps from API

Using property pattern with fetched data:

```jsx
import React, { useState, useEffect } from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';

function DynamicStepper() {
  const [steps, setSteps] = useState([]);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    // Fetch steps from API
    fetch('/api/workflow-steps')
      .then(res => res.json())
      .then(data => setSteps(data))
      .catch(err => console.error(err));
  }, []);

  const handleStepChanged = (args) => {
    setActiveStep(args.activeStep);
    // Update step status based on business logic
  };

  if (steps.length === 0) {
    return <div>Loading...</div>;
  }

  return (
    <StepperComponent 
      steps={steps}
      activeStep={activeStep}
      stepChanged={handleStepChanged}
    />
  );
}

export default DynamicStepper;
```

### Example 3: Conditional Steps with Component Pattern

```jsx
import React, { useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function ConditionalStepper() {
  const [isExpress, setIsExpress] = useState(false);

  return (
    <div>
      <label>
        <input 
          type="checkbox" 
          checked={isExpress}
          onChange={(e) => setIsExpress(e.target.checked)}
        />
        Express Checkout
      </label>

      <StepperComponent>
        <StepsDirective>
          <StepDirective label="Cart" iconCss="sf-icon-cart" />
          {isExpress && (
            <StepDirective label="Express" iconCss="sf-icon-bolt" />
          )}
          <StepDirective label="Payment" iconCss="sf-icon-payment" />
          {!isExpress && (
            <StepDirective label="Delivery" iconCss="sf-icon-transport" />
          )}
          <StepDirective label="Confirm" iconCss="sf-icon-check" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}

export default ConditionalStepper;
```

## Performance Optimization

### Tip 1: Use Property Pattern for Large Lists

For 50+ steps, use the property-based pattern:

```jsx
// ✅ Better performance
const largeStepList = Array.from({ length: 100 }, (_, i) => ({
  label: `Step ${i + 1}`,
  text: String(i + 1)
}));

<StepperComponent steps={largeStepList} />
```

### Tip 2: Memoize Callbacks

```jsx
const handleStepChanging = useCallback((args) => {
  // Validation logic
}, [dependencies]);

<StepperComponent stepChanging={handleStepChanging} />
```

### Tip 3: Use enablePersistence for UX

```jsx
<StepperComponent 
  enablePersistence={true}
  steps={steps}
/>
```

## Common Gotchas

### Gotcha 1: activeStep Index Out of Range

❌ **Wrong:**
```jsx
<StepperComponent activeStep={999}>
  <StepsDirective>
    <StepDirective label="Step 1" />
    <StepDirective label="Step 2" />
  </StepsDirective>
</StepperComponent>
```

✅ **Correct:**
```jsx
const activeStep = Math.min(userStep, totalSteps - 1);
<StepperComponent activeStep={activeStep}>
```

### Gotcha 2: Changing steps Array Without Key

❌ **Wrong:**
```jsx
const steps = [
  { label: 'Step 1' },
  { label: 'Step 2' }
];

// Later modifying array...
steps[0].label = 'Updated';
setSteps(steps); // Component won't update!
```

✅ **Correct:**
```jsx
const newSteps = [...steps];
newSteps[0].label = 'Updated';
setSteps(newSteps); // Triggers re-render
```

### Gotcha 3: Event Arguments Structure

❌ **Wrong:**
```jsx
const handleStepChanged = (args) => {
  console.log(args.step); // ❌ undefined
};
```

✅ **Correct:**
```jsx
const handleStepChanged = (args) => {
  console.log(args.activeStep); // ✅ current step
  console.log(args.previousStep); // ✅ previous step
  console.log(args.isInteracted); // ✅ user interaction
};
```

### Gotcha 4: Ref Access Before Mount

❌ **Wrong:**
```jsx
const stepperRef = useRef(null);
stepperRef.current.reset(); // ❌ Error: ref is null
```

✅ **Correct:**
```jsx
const handleReset = () => {
  if (stepperRef.current) {
    stepperRef.current.reset(); // ✅ Check ref exists
  }
};
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Steps not rendering | Import `StepsDirective` and `StepDirective`; check `steps` prop exists |
| Events not firing | Verify event names (camelCase); check callback function signature |
| activeStep not changing | Verify index is 0-based and within range; check re-render triggers |
| reset() not working | Ensure using ref with `useRef`; call within event handler, not render |
| Performance issues | Switch to property pattern; memoize callbacks; check re-render count |

```
