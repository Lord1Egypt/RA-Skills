---
name: syncfusion-react-stepper
description: "Implement and configure the Syncfusion React Stepper component for guided workflows. Use this skill when creating step-by-step navigation flows, multi-step forms, wizards, or process guides in React. This skill covers step configuration, orientation (horizontal/vertical), events, validation, animations, templates, accessibility, and globalization support for linear or non-linear workflows."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion React Stepper

The Stepper component guides users through a multi-step workflow or process with visual indicators, step labels, and flexible configuration. It's ideal for wizards, checkout flows, onboarding processes, and any guided user experience requiring sequential navigation.

## When to Use This Skill

Use the Stepper component when you need to:
- Guide users through multi-step processes (checkout, registration, setup wizards)
- Display step-by-step workflows with progress indication
- Validate user input before advancing to the next step
- Support linear or non-linear navigation patterns
- Customize appearance with icons, labels, and templates
- Localize content for different languages/regions

## Component Overview

**Key Capabilities:**
- **Step Navigation:** Horizontal and vertical orientations, sequential or free navigation
- **Step Types:** Default (icons + labels), label-only, or indicator-only modes
- **Events:** Track step changes, validations, and interactions
- **Styling:** Animations, templates, custom CSS, and tooltips
- **Accessibility:** Full keyboard navigation and ARIA support
- **Globalization:** Multi-language support and RTL compatibility

## Documentation and Navigation Guide

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies
- CSS imports and theme setup
- Creating your first stepper
- Initial configuration and rendering

### Core Configuration: Steps and Properties
📄 **Read:** [references/steps-and-configuration.md](references/steps-and-configuration.md)
- Adding and defining steps with StepDirective
- Icon CSS, text, and label properties
- Active step management
- Disabled states and customization
- CSS class configuration

### Layout & Appearance: Orientations and Types
📄 **Read:** [references/orientations-and-types.md](references/orientations-and-types.md)
- Horizontal and vertical orientations
- Step type modes (Default, Label, Indicator)
- Label positioning (Top, Bottom, Start, End)
- RTL support and responsive design

### Interaction & Behavior: Events
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Lifecycle events: created, stepChanged, stepChanging
- User interaction events: stepClick, beforeStepRender
- Event arguments and handling patterns
- Preventing unwanted transitions

### Workflow Control: Linear Flow and Validation
📄 **Read:** [references/linear-flow-and-validation.md](references/linear-flow-and-validation.md)
- Linear stepper configuration for sequential navigation
- Step validation and status management
- Preventing invalid transitions
- Resetting stepper state

### Advanced Styling & Customization
📄 **Read:** [references/animation-template-tooltip.md](references/animation-template-tooltip.md)
- Animation configuration and timing
- Template customization for steps
- Tooltip integration and display
- Custom content rendering

### Methods and Advanced Patterns
📄 **Read:** [references/methods-and-advanced.md](references/methods-and-advanced.md)
- Component methods (reset, etc.)
- Both API patterns (component-based vs property-based)
- Advanced use cases and patterns
- Performance optimization tips

### Best Practices: Accessibility & Localization
📄 **Read:** [references/accessibility-globalization.md](references/accessibility-globalization.md)
- WCAG compliance and ARIA attributes
- Keyboard navigation guidelines
- Globalization and localization
- RTL support implementation

## Quick Start Examples

### Pattern 1: Component-Based (StepsDirective)

```jsx
import React from 'react';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-navigations/styles/tailwind3.css';

function App() {
  return (
    <div>
      <StepperComponent>
        <StepsDirective>
          <StepDirective iconCss="sf-icon-cart" label="Cart" />
          <StepDirective iconCss="sf-icon-transport" label="Delivery" />
          <StepDirective iconCss="sf-icon-payment" label="Payment" />
          <StepDirective iconCss="sf-icon-success" label="Confirmation" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}

export default App;
```

### Pattern 2: Property-Based (steps Array)

```jsx
import React from 'react';
import { StepperComponent } from '@syncfusion/ej2-react-navigations';
import '@syncfusion/ej2-base/styles/tailwind3.css';
import '@syncfusion/ej2-navigations/styles/tailwind3.css';

function App() {
  const steps = [
    { iconCss: 'sf-icon-cart', label: 'Cart' },
    { iconCss: 'sf-icon-transport', label: 'Delivery' },
    { iconCss: 'sf-icon-payment', label: 'Payment' },
    { iconCss: 'sf-icon-success', label: 'Confirmation' }
  ];

  return (
    <div>
      <StepperComponent steps={steps} />
    </div>
  );
}

export default App;
```

## Common Patterns

### Pattern 1: Wizard with Validation
```jsx
const [activeStep, setActiveStep] = React.useState(0);
const stepperRef = React.useRef(null);

const handleStepChanging = (args) => {
  // Validate current step before advancing
  if (!validateStep(activeStep)) {
    args.cancel = true; // Prevent transition
  }
};

<StepperComponent 
  ref={stepperRef}
  stepChanging={handleStepChanging}
>
  {/* steps */}
</StepperComponent>
```

### Pattern 2: Linear vs Non-Linear Navigation
```jsx
// Linear: Users must complete steps sequentially
<StepperComponent linear={true}>

// Non-linear: Users can skip to any step
<StepperComponent linear={false}>
```

### Pattern 3: Responsive Orientation
```jsx
// Auto-switch orientation based on screen size
const [orientation, setOrientation] = React.useState('horizontal');

React.useEffect(() => {
  const handleResize = () => {
    setOrientation(window.innerWidth < 768 ? 'vertical' : 'horizontal');
  };
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

<StepperComponent orientation={orientation}>
```

## Key Props and Configuration

### Component Properties

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `activeStep` | number | 0 | Currently active step index |
| `animation` | StepperAnimationSettingsModel | undefined | Animation configuration (enable, duration, delay) |
| `cssClass` | string | '' | CSS class for custom styling |
| `enablePersistence` | boolean | false | Persist component state between page reloads |
| `enableRtl` | boolean | false | Enable right-to-left layout |
| `labelPosition` | string | 'Bottom' | Label placement: 'Top', 'Bottom', 'Start', 'End' |
| `linear` | boolean | false | Enforce sequential step navigation |
| `locale` | string | 'en-US' | Localization culture code |
| `orientation` | string | 'horizontal' | Layout direction: 'horizontal' or 'vertical' |
| `readOnly` | boolean | false | Disable user interaction |
| `showTooltip` | boolean | true | Show tooltips on hover |
| `stepType` | string | 'Default' | Visual mode: 'Default', 'Label', 'Indicator' |
| `steps` | StepModel[] | [] | Array of step objects (property-based pattern) |
| `template` | string \| function | undefined | Custom template for steps |
| `tooltipTemplate` | string \| function | undefined | Custom template for tooltips |

### Step Properties (StepModel)

| Property | Type | Purpose |
|----------|------|---------|
| `cssClass` | string | CSS class for individual step styling |
| `disabled` | boolean | Disable the step |
| `iconCss` | string | Icon CSS class for the step |
| `isValid` | boolean | Validation status of the step |
| `label` | string | Step label text |
| `optional` | boolean | Mark step as optional |
| `status` | string | Step status: 'NotStarted', 'InProgress', 'Completed' |
| `text` | string | Text content (usually number) |

### Animation Settings

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `enable` | boolean | true | Enable animations |
| `duration` | number | 400 | Animation duration in milliseconds |
| `delay` | number | 0 | Delay before animation starts |

### Events

| Event | Fires | Use For | Arguments |
|-------|-------|---------|-----------|
| `created` | After component initialization | Setup, initialization | Event |
| `stepChanged` | After step changes | Update UI, load content | StepperChangedEventArgs |
| `stepChanging` | Before step changes | Validate, prevent transitions | StepperChangingEventArgs |
| `stepClick` | User clicks step | Track interactions | StepperClickEventArgs |
| `beforeStepRender` | Before rendering each step | Customize step appearance | StepperRenderingEventArgs |

### Methods

| Method | Parameters | Returns | Purpose |
|--------|-----------|---------|---------|
| `reset()` | none | void | Reset stepper to initial state (activeStep: 0) |
| `nextStep()` | none | void | Move to next step programmatically |
| `previousStep()` | none | void | Move to previous step programmatically |
| `refreshProgressbar()` | none | void | Refresh progress bar on container resize |
| `destroy()` | none | void | Destroy component and release resources |

**Event Arguments Reference:**
- **StepperChangedEventArgs:** activeStep, previousStep, isInteracted, name, event, element
- **StepperChangingEventArgs:** activeStep, previousStep, cancel, isInteracted, name, event, element
- **StepperClickEventArgs:** activeStep, name, event, element
- **StepperRenderingEventArgs:** activeStep, name, element

## Common Use Cases

- **E-Commerce Checkout:** Multi-step checkout flow with order review, shipping, payment
- **User Registration:** Multi-step signup with email, profile, verification
- **Setup Wizards:** Software onboarding with configuration steps
- **Survey Forms:** Step-by-step questionnaire with progress indication
- **Installation Guides:** Installation steps with instructions and validation
