# Advanced Patterns and Use Cases

## Table of Contents
- [Multi-Step Form Wizard](#multi-step-form-wizard)
- [E-Commerce Checkout](#e-commerce-checkout)
- [Progress Tracker](#progress-tracker)
- [Setup Wizard](#setup-wizard)
- [Performance Optimization](#performance-optimization)
- [Common Gotchas](#common-gotchas)

## Multi-Step Form Wizard

A complete form spread across multiple steps with validation:

```jsx
import React, { useState } from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

function FormWizard() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    country: '',
    terms: false
  });

  const [stepValidation, setStepValidation] = useState([
    { isValid: null },
    { isValid: null },
    { isValid: null },
    { isValid: null }
  ]);

  const validateStep = (stepIndex) => {
    let isValid = false;
    
    if (stepIndex === 0) {
      isValid = formData.firstName && formData.lastName;
    } else if (stepIndex === 1) {
      isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email) && formData.phone;
    } else if (stepIndex === 2) {
      isValid = formData.address && formData.city && formData.country;
    } else if (stepIndex === 3) {
      isValid = formData.terms === true;
    }
    
    return isValid;
  };

  const handleStepChanging = (args) => {
    const isValid = validateStep(args.previousStep);
    if (!isValid) {
      alert('Please fill all required fields');
      args.cancel = true;
      return;
    }
    
    // Update validation state
    const newValidation = [...stepValidation];
    newValidation[args.previousStep].isValid = true;
    setStepValidation(newValidation);
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = () => {
    if (validateStep(3)) {
      console.log('Form submitted:', formData);
      alert('Form successfully submitted!');
    }
  };

  return (
    <div className="form-wizard">
      <StepperComponent linear={true} stepChanging={handleStepChanging}>
        <StepsDirective>
          <StepDirective 
            label="Personal Info" 
            isValid={stepValidation[0].isValid}
            iconCss="sf-icon-user"
          />
          <StepDirective 
            label="Contact" 
            isValid={stepValidation[1].isValid}
            iconCss="sf-icon-phone"
          />
          <StepDirective 
            label="Address" 
            isValid={stepValidation[2].isValid}
            iconCss="sf-icon-building"
          />
          <StepDirective 
            label="Confirm" 
            isValid={stepValidation[3].isValid}
            iconCss="sf-icon-check"
          />
        </StepsDirective>
      </StepperComponent>

      <div className="form-content" style={{ marginTop: '20px' }}>
        {/* Step 1: Personal Info */}
        {/* Step 2: Contact */}
        {/* Step 3: Address */}
        {/* Step 4: Confirmation */}
      </div>

      <button onClick={handleSubmit} style={{ marginTop: '20px' }}>
        Submit
      </button>
    </div>
  );
}
```

## E-Commerce Checkout

Realistic checkout flow with order review and payment:

```jsx
function CheckoutFlow() {
  const [cart, setCart] = useState([
    { id: 1, name: 'Product 1', price: 29.99 },
    { id: 2, name: 'Product 2', price: 49.99 }
  ]);

  const [checkout, setCheckout] = useState({
    email: '',
    shippingAddress: '',
    shippingMethod: '',
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  const handleStepChanged = (args) => {
    if (args.activeStep === 2) {
      // Pre-fill shipping methods on step 3
      console.log('Loading shipping options...');
    }
  };

  return (
    <div className="checkout">
      <div className="checkout-header">
        <h2>Checkout Process</h2>
        <p>Total: ${total.toFixed(2)}</p>
      </div>

      <StepperComponent stepChanged={handleStepChanged} linear={true}>
        <StepsDirective>
          <StepDirective 
            label="Cart Review" 
            iconCss="sf-icon-cart"
          />
          <StepDirective 
            label="Shipping" 
            iconCss="sf-icon-truck"
          />
          <StepDirective 
            label="Payment" 
            iconCss="sf-icon-credit-card"
          />
          <StepDirective 
            label="Confirmation" 
            iconCss="sf-icon-success"
          />
        </StepsDirective>
      </StepperComponent>

      <div className="cart-summary">
        <h3>Order Summary</h3>
        {cart.map(item => (
          <div key={item.id} className="cart-item">
            <span>{item.name}</span>
            <span>${item.price.toFixed(2)}</span>
          </div>
        ))}
        <div className="cart-total">
          <strong>Total: ${total.toFixed(2)}</strong>
        </div>
      </div>
    </div>
  );
}
```

## Progress Tracker

Display progress without allowing backward navigation:

```jsx
function ProgressTracker() {
  const [progress, setProgress] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  const steps = [
    { label: 'Initializing', duration: 2000 },
    { label: 'Processing', duration: 3000 },
    { label: 'Finalizing', duration: 1000 },
    { label: 'Complete', duration: 0 }
  ];

  React.useEffect(() => {
    if (progress < steps.length - 1) {
      setIsProcessing(true);
      const timer = setTimeout(() => {
        setProgress(progress + 1);
        setIsProcessing(false);
      }, steps[progress].duration);
      
      return () => clearTimeout(timer);
    }
  }, [progress]);

  return (
    <div>
      <StepperComponent 
        activeStep={progress}
        readOnly={true}
        orientation="vertical"
      >
        <StepsDirective>
          {steps.map((step, index) => (
            <StepDirective 
              key={index}
              label={step.label}
              isValid={progress > index ? true : progress === index ? null : false}
            />
          ))}
        </StepsDirective>
      </StepperComponent>

      {isProcessing && <p>Processing... {steps[progress].label}</p>}
      {progress === steps.length - 1 && <p>✓ All done!</p>}
    </div>
  );
}
```

## Setup Wizard

Guided application setup with optional steps:

```jsx
function SetupWizard() {
  const [setupConfig, setSetupConfig] = useState({
    basicSetup: false,
    advancedSetup: false,
    integrations: false,
    customization: false
  });

  const handleStepClick = (args) => {
    console.log(`User viewing step: ${args.activeStep}`);
  };

  return (
    <div className="setup-wizard">
      <h2>Application Setup</h2>
      
      <StepperComponent stepClick={handleStepClick} linear={false}>
        <StepsDirective>
          <StepDirective 
            label="Basic Configuration"
            iconCss="sf-icon-settings"
            text="1"
          />
          <StepDirective 
            label="Advanced Settings"
            iconCss="sf-icon-sliders"
            text="2"
            optional={true}
          />
          <StepDirective 
            label="Integrations"
            iconCss="sf-icon-connection"
            text="3"
            optional={true}
          />
          <StepDirective 
            label="Customization"
            iconCss="sf-icon-palette"
            text="4"
            optional={true}
          />
          <StepDirective 
            label="Complete"
            iconCss="sf-icon-check"
            text="5"
          />
        </StepsDirective>
      </StepperComponent>

      <div style={{ marginTop: '20px' }}>
        <p>You can skip optional steps and come back later.</p>
        <p>Completed steps: {Object.values(setupConfig).filter(v => v).length}</p>
      </div>
    </div>
  );
}
```

## Performance Optimization

### Lazy Load Content

```jsx
function LazyLoadingStepper() {
  const [loadedSteps, setLoadedSteps] = useState([0]); // Initially load first step

  const handleStepChanged = (args) => {
    // Load step content on demand
    if (!loadedSteps.includes(args.activeStep)) {
      setLoadedSteps([...loadedSteps, args.activeStep]);
      console.log(`Loading content for step ${args.activeStep}`);
    }
  };

  const loadStepContent = (stepIndex) => {
    if (!loadedSteps.includes(stepIndex)) {
      return <p>Loading...</p>;
    }
    return <p>Content for step {stepIndex + 1}</p>;
  };

  return (
    <>
      <StepperComponent stepChanged={handleStepChanged}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>

      <div>
        {loadStepContent(0)}
      </div>
    </>
  );
}
```

### Memoize Template

```jsx
import React, { useMemo } from 'react';

function StepperWithMemoTemplate() {
  const memoTemplate = useMemo(() => {
    return ({ step, currentStep }) => (
      <div className="step-template">
        <span className={step.iconCss}></span>
        <span>{step.label}</span>
      </div>
    );
  }, []);

  return (
    <StepperComponent template={memoTemplate}>
      <StepsDirective>
        {/* steps */}
      </StepsDirective>
    </StepperComponent>
  );
}
```

## Common Gotchas

### Gotcha 1: Linear Mode Still Allows Backward Navigation

**Problem:** Linear mode doesn't prevent going back
```jsx
// This still allows backward movement
<StepperComponent linear={true}>
```

**Solution:** Use stepChanging event to prevent backward:
```jsx
const handleStepChanging = (args) => {
  if (args.activeStep < args.previousStep) {
    args.cancel = true; // Prevent going back
  }
};

<StepperComponent linear={true} stepChanging={handleStepChanging}>
```

### Gotcha 2: State Not Syncing with Active Step

**Problem:** Component shows step 1 but state says step 3
```jsx
// DON'T: State and component out of sync
const [activeStep, setActiveStep] = useState(3);
<StepperComponent activeStep={activeStep}>
```

**Solution:** Use ref for direct access or keep synchronized:
```jsx
// DO: Use ref for stepper
const stepperRef = useRef(null);
const handleNext = () => {
  stepperRef.current.activeStep += 1;
};
```

### Gotcha 3: Validation State Not Visual

**Problem:** isValid set but no visual change
```jsx
// isValid state doesn't auto-update visually
isValid={formData.email ? true : false}
```

**Solution:** Update within stepChanging event:
```jsx
const handleStepChanging = (args) => {
  const newValidation = [...validation];
  newValidation[args.previousStep].isValid = isFieldValid(args.previousStep);
  setValidation(newValidation);
};
```

### Gotcha 4: Template Not Updating

**Problem:** Template shows old data
```jsx
// Template captures data at render time
const getTemplate = ({ step }) => {
  // This might be stale
  return <div>{externalData.value}</div>;
};
```

**Solution:** Include dependencies in template function:
```jsx
const getTemplate = ({ step }) => {
  // This will update when externalData changes
  return <div>{externalData.value}</div>;
};

// Ensure component re-renders: pass dependencies
<StepperComponent key={externalData.id} template={getTemplate}>
```

### Gotcha 5: Events Firing Multiple Times

**Problem:** Event handlers called unexpectedly
```jsx
// Event might fire multiple times during renders
const handleStepChanged = (args) => {
  fetchData(); // Fires too often
};
```

**Solution:** Use useCallback and refs:
```jsx
const handleStepChanged = useCallback((args) => {
  if (lastStepRef.current !== args.activeStep) {
    fetchData();
    lastStepRef.current = args.activeStep;
  }
}, []);
```

## Best Practices Summary

**Performance:**
- ✅ Use ref access for frequent updates
- ✅ Lazy load step content
- ✅ Memoize template functions
- ✅ Debounce event handlers if needed

**UX:**
- ✅ Provide clear validation feedback
- ✅ Show progress indication
- ✅ Allow reviewing completed steps
- ✅ Mark optional steps clearly

**Code:**
- ✅ Keep validation logic DRY
- ✅ Test keyboard navigation
- ✅ Handle edge cases (empty steps, rapid clicks)
- ✅ Provide meaningful error messages
