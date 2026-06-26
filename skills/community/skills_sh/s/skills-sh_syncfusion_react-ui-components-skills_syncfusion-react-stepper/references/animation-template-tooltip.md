# Animation, Template, and Tooltip

## Table of Contents
- [Animation](#animation)
- [Template Customization](#template-customization)
- [Tooltip Integration](#tooltip-integration)
- [Advanced Customization](#advanced-customization)

## Animation

Animate the stepper progress state with smooth transitions between steps.

### Enabling Animation

Animation is enabled by default. Control it with the `animation` property:

```jsx
<StepperComponent animation={{ enable: true, duration: 2000, delay: 0 }}>
  <StepsDirective>
    <StepDirective label="Step 1" />
    <StepDirective label="Step 2" />
    <StepDirective label="Step 3" />
  </StepsDirective>
</StepperComponent>
```

### Animation Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enable` | boolean | true | Enable/disable animations |
| `duration` | number | 2000 | Animation duration in milliseconds |
| `delay` | number | 0 | Delay before animation starts (milliseconds) |

### Disabling Animation

```jsx
<StepperComponent animation={{ enable: false }}>
  <StepsDirective>
    <StepDirective label="Step 1" />
    <StepDirective label="Step 2" />
    <StepDirective label="Step 3" />
  </StepsDirective>
</StepperComponent>
```

### Custom Animation Configuration

```jsx
// Fast animation: 500ms
<StepperComponent animation={{ enable: true, duration: 500, delay: 0 }}>
  {/* steps */}
</StepperComponent>

// Slow animation: 3000ms with 200ms delay
<StepperComponent animation={{ enable: true, duration: 3000, delay: 200 }}>
  {/* steps */}
</StepperComponent>

// No animation, instant transition
<StepperComponent animation={{ enable: false }}>
  {/* steps */}
</StepperComponent>
```

### Practical Example: Progressive Animation

```jsx
function App() {
  const [animationSpeed, setAnimationSpeed] = useState(2000);

  return (
    <div>
      <div>
        <label>Animation Speed (ms):</label>
        <input 
          type="number" 
          value={animationSpeed}
          onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
          min="0"
          step="100"
        />
      </div>

      <StepperComponent 
        animation={{ 
          enable: true, 
          duration: animationSpeed, 
          delay: 0 
        }}
      >
        <StepsDirective>
          <StepDirective label="Cart" />
          <StepDirective label="Delivery" />
          <StepDirective label="Payment" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}
```

## Template Customization

Customize the appearance of steps using custom templates.

### Basic Template

Define a template function that receives the step object:

```jsx
function App() {
  const getTemplate = ({ step, currentStep }) => {
    return (
      <div className="custom-step">
        <span className={step.iconCss}></span>
        <span className="label">{step.label}</span>
      </div>
    );
  };

  return (
    <StepperComponent template={getTemplate}>
      <StepsDirective>
        <StepDirective iconCss="sf-icon-cart" label="Cart" />
        <StepDirective iconCss="sf-icon-transport" label="Delivery" />
        <StepDirective iconCss="sf-icon-payment" label="Payment" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Template Context

The template function receives:
- `step`: Current step object with properties (label, iconCss, text, etc.)
- `currentStep`: Index of the current step in the loop

### Advanced Template with Status

```jsx
function App() {
  const getTemplate = ({ step, currentStep }) => {
    let statusClass = 'pending';
    
    if (step.isValid === true) {
      statusClass = 'completed';
    } else if (step.isValid === false) {
      statusClass = 'error';
    }

    return (
      <div className={`template-step ${statusClass}`}>
        <div className="step-header">
          <span className={step.iconCss}></span>
          <span className="step-number">{currentStep + 1}</span>
        </div>
        <div className="step-content">
          <p className="step-label">{step.label}</p>
          <p className="step-description">
            {statusClass === 'completed' && '✓ Completed'}
            {statusClass === 'error' && '✗ Error'}
            {statusClass === 'pending' && '○ Pending'}
          </p>
        </div>
      </div>
    );
  };

  return (
    <StepperComponent template={getTemplate}>
      <StepsDirective>
        <StepDirective iconCss="sf-icon-cart" label="Cart" isValid={true} />
        <StepDirective iconCss="sf-icon-transport" label="Delivery" isValid={false} />
        <StepDirective iconCss="sf-icon-payment" label="Payment" isValid={null} />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### CSS for Template

```css
.template-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.template-step.completed {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.template-step.error {
  background-color: #ffebee;
  color: #c62828;
}

.template-step.pending {
  background-color: #f5f5f5;
  color: #666;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.step-content {
  margin-top: 8px;
  text-align: center;
  font-size: 12px;
}

.step-label {
  margin: 0;
  font-weight: 600;
}

.step-description {
  margin: 4px 0 0 0;
  font-size: 11px;
  opacity: 0.8;
}
```

## Tooltip Integration

Add tooltips to steps for additional information:

### Using Title Attribute

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective 
      iconCss="sf-icon-cart" 
      label="Cart"
      title="Review and modify your shopping cart"
    />
    <StepDirective 
      iconCss="sf-icon-transport" 
      label="Delivery"
      title="Enter your shipping address"
    />
    <StepDirective 
      iconCss="sf-icon-payment" 
      label="Payment"
      title="Choose your payment method"
    />
  </StepsDirective>
</StepperComponent>
```

### Custom Tooltip with Syncfusion Tooltip Component

```jsx
import { TooltipComponent } from '@syncfusion/ej2-react-popups';

function App() {
  return (
    <StepperComponent>
      <StepsDirective>
        <StepDirective 
          iconCss="sf-icon-cart" 
          label="Cart"
        />
        <StepDirective 
          iconCss="sf-icon-transport" 
          label="Delivery"
        />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Tooltip via Template

```jsx
function App() {
  const getTemplate = ({ step, currentStep }) => {
    const tooltips = [
      'Review items in your cart',
      'Enter shipping address',
      'Select payment method',
      'Confirm your order'
    ];

    return (
      <div className="step-with-tooltip">
        <span className={step.iconCss}></span>
        <span className="step-label">{step.label}</span>
        <div className="tooltip-hint" title={tooltips[currentStep]}>
          ?
        </div>
      </div>
    );
  };

  return (
    <StepperComponent template={getTemplate}>
      <StepsDirective>
        <StepDirective iconCss="sf-icon-cart" label="Cart" />
        <StepDirective iconCss="sf-icon-transport" label="Delivery" />
        <StepDirective iconCss="sf-icon-payment" label="Payment" />
        <StepDirective iconCss="sf-icon-success" label="Confirm" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### CSS for Tooltip

```css
.step-with-tooltip {
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.tooltip-hint {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background-color: #2196F3;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  cursor: help;
}

.tooltip-hint:hover::after {
  content: attr(title);
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 1000;
  font-size: 12px;
}
```

## Advanced Customization

### Combining Animation, Template, and Tooltip

```jsx
function App() {
  const [activeStep, setActiveStep] = useState(0);

  const getTemplate = ({ step, currentStep }) => {
    const helpText = [
      'Add items to your cart',
      'Provide delivery details',
      'Choose payment option',
      'Review and submit'
    ];

    return (
      <div className="advanced-step-template">
        <div className="step-indicator">
          <span className={step.iconCss}></span>
          <span className="step-number">{currentStep + 1}</span>
        </div>
        <div className="step-info">
          <p className="step-title">{step.label}</p>
          <p className="step-help">{helpText[currentStep]}</p>
        </div>
      </div>
    );
  };

  return (
    <StepperComponent
      activeStep={activeStep}
      template={getTemplate}
      animation={{ enable: true, duration: 1500, delay: 100 }}
      stepChanged={(args) => setActiveStep(args.activeStep)}
    >
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

### Advanced CSS

```css
.advanced-step-template {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.advanced-step-template:hover {
  background-color: #f0f0f0;
}

.step-indicator {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f5f5;
  border-radius: 50%;
}

.step-number {
  position: absolute;
  font-weight: bold;
  font-size: 14px;
}

.step-info {
  flex: 1;
}

.step-title {
  margin: 0;
  font-weight: 600;
  font-size: 14px;
}

.step-help {
  margin: 4px 0 0 0;
  font-size: 12px;
  color: #999;
}
```

## Troubleshooting

**Issue: Animation too slow/fast**
- ✅ Adjust `duration` property (in milliseconds)
- ✅ Typical range: 500-3000ms

**Issue: Template not rendering**
- ✅ Verify template function returns JSX
- ✅ Check that step properties are accessible
- ✅ Ensure no console errors

**Issue: Tooltip not showing**
- ✅ Verify `title` attribute is set on step
- ✅ Check CSS z-index if tooltip is hidden behind other elements
- ✅ Ensure parent container overflow is not hidden
