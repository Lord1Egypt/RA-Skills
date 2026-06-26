# Accessibility

## Table of Contents
- [Accessibility Compliance](#accessibility-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Focus Management](#focus-management)
- [Color and Contrast](#color-and-contrast)
- [Mobile Accessibility](#mobile-accessibility)
- [Testing Accessibility](#testing-accessibility)
- [Best Practices](#best-practices)

## Accessibility Compliance

The RangeSlider component meets major accessibility standards:

| Standard | Status | Details |
|----------|--------|---------|
| **WCAG 2.2** | ✅ Full Support | Web Content Accessibility Guidelines |
| **Section 508** | ✅ Full Support | US Federal accessibility requirement |
| **ADA** | ✅ Full Support | Americans with Disabilities Act |
| **ARIA** | ✅ Full Support | Accessible Rich Internet Applications |
| **Keyboard Navigation** | ✅ Full Support | All features accessible via keyboard |
| **Screen Reader** | ✅ Full Support | Works with NVDA, JAWS, VoiceOver |
| **Mobile Accessibility** | ✅ Full Support | Touch-friendly, large hit areas |

## WAI-ARIA Attributes

The RangeSlider automatically includes ARIA attributes for assistive technologies.

### ARIA Attributes Applied

```html
<!-- Example rendered slider -->
<div class="e-slider-container" role="slider">
  <div class="e-slider">
    <div class="e-handle" 
         role="slider" 
         aria-valuemin="0" 
         aria-valuemax="100" 
         aria-valuenow="50" 
         aria-valuetext="50"
         aria-orientation="horizontal"
         tabindex="0"
         aria-label="Value Slider">
    </div>
  </div>
</div>
```

### ARIA Roles and Properties

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `role` | `"slider"` | Identifies as slider control |
| `aria-valuemin` | Number | Minimum selectable value |
| `aria-valuemax` | Number | Maximum selectable value |
| `aria-valuenow` | Number | Current value |
| `aria-valuetext` | String | Human-readable value (e.g., "50%") |
| `aria-orientation` | `"horizontal"` \| `"vertical"` | Slider direction |
| `aria-label` | String | Descriptive label for screen readers |
| `tabindex` | `"0"` | Focusable with Tab key |

### Adding Descriptive Labels

```tsx
import React from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function AccessibleSlider() {
  return (
    <div>
      <label htmlFor="budget-slider">
        Select Your Budget (in dollars)
      </label>
      <SliderComponent
        id="budget-slider"
        type="Range"
        value={[100, 500]}
        min={0}
        max={1000}
        aria-label="Budget range selector"
        aria-describedby="budget-help"
      />
      <div id="budget-help">
        Use arrow keys to adjust, Enter to confirm
      </div>
    </div>
  );
}

export default AccessibleSlider;
```

## Keyboard Navigation

Users can fully control the slider using keyboard only (no mouse required).

### Keyboard Shortcuts

| Key | Behavior | Platform |
|-----|----------|----------|
| **Right Arrow** | Increase value by 1 | Horizontal |
| **Left Arrow** | Decrease value by 1 | Horizontal |
| **Up Arrow** | Increase value by 1 | Vertical |
| **Down Arrow** | Decrease value by 1 | Vertical |
| **Page Up** | Increase by largeStep | Both |
| **Page Down** | Decrease by largeStep | Both |
| **Home** | Move to minimum value | Both |
| **End** | Move to maximum value | Both |
| **Tab** | Focus slider | Both |
| **Enter/Space** | Activate (range-specific) | Both |

### Keyboard Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function KeyboardControlledSlider() {
  const [value, setValue] = useState(50);
  const [feedback, setFeedback] = useState('');

  function handleChange(e) {
    setValue(e.value as number);
    setFeedback(`Value changed to ${e.value}`);
  }

  return (
    <div>
      <h2>Keyboard-Controlled Slider</h2>
      <p>Use arrow keys, Home, End, Page Up/Down</p>
      
      <SliderComponent
        id="keyboard-slider"
        value={value}
        change={handleChange}
        min={0}
        max={100}
        step={1}
        ticks={{
          placement: 'After',
          largeStep: 10
        }}
        aria-label="Use keyboard to control"
      />
      
      <p aria-live="polite" aria-atomic="true">
        {feedback}
      </p>
    </div>
  );
}

export default KeyboardControlledSlider;
```

### Range Slider Keyboard Behavior

For `type="Range"` sliders with two handles:

1. **Tab to first handle:** Focus on first (start) handle
2. **Arrow keys:** Adjust first handle
3. **Tab to second handle:** Focus moves to second handle
4. **Arrow keys:** Adjust second handle
5. **Home/End:** Move focused handle to min/max

## Screen Reader Support

### Screen Reader Testing

Test with popular screen readers:

- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (Mac, iOS, built-in)
- **TalkBack** (Android, built-in)

### What Screen Readers Announce

```
"Budget range slider, horizontal, range mode
Current values: 100 to 500
Minimum 0, maximum 1000
Use arrow keys to adjust
First handle: 100 dollars
Second handle: 500 dollars"
```

### Improving Screen Reader Experience

Provide clear labels and descriptions:

```tsx
<div>
  <label htmlFor="price-range">
    Select Price Range
  </label>
  <p id="price-info">
    Select minimum and maximum price using arrow keys.
    Current selection: ${min} to ${max}
  </p>
  <SliderComponent
    id="price-range"
    type="Range"
    value={[min, max]}
    aria-describedby="price-info"
    aria-label="Price range"
  />
  <output id="price-output" aria-live="polite">
    ${min} - ${max}
  </output>
</div>
```

### aria-live Regions

Use `aria-live` to announce value changes:

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function LiveRegionSlider() {
  const [value, setValue] = useState(50);

  return (
    <div>
      <SliderComponent
        id="slider"
        value={value}
        change={(e) => setValue(e.value as number)}
      />
      
      {/* Screen readers announce value changes */}
      <div aria-live="polite" aria-atomic="true">
        Current value: {value}
      </div>
    </div>
  );
}

export default LiveRegionSlider;
```

## Focus Management

### Default Focus Behavior

The slider is automatically focusable:

```tsx
<SliderComponent
  id="slider"
  value={50}
  // Automatically has tabindex="0"
/>
```

### Managing Focus Programmatically

```tsx
import React, { useRef } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function FocusManagementSlider() {
  const sliderRef = useRef(null);

  const focusSlider = () => {
    // Bring focus to slider
    const sliderElement = document.getElementById('my-slider');
    sliderElement?.focus();
  };

  return (
    <div>
      <button onClick={focusSlider}>
        Focus Slider
      </button>
      
      <SliderComponent
        id="my-slider"
        value={50}
      />
    </div>
  );
}

export default FocusManagementSlider;
```

### Focus Visible Styling

Style focus state for keyboard users:

```css
.e-control-wrapper.e-slider-container .e-slider .e-handle:focus-visible {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
}
```

## Color and Contrast

### Color Contrast Requirements

RangeSlider meets WCAG AA standards:
- **Normal text:** 4.5:1 contrast ratio minimum
- **Large text:** 3:1 contrast ratio minimum
- **UI components:** 3:1 contrast ratio minimum

### Checking Contrast

Ensure custom styling maintains contrast:

```css
/* ✅ Good: 7.1:1 contrast ratio */
.e-slider-track {
    background: #0066cc;  /* Dark blue */
}

body {
    background: #ffffff;  /* White */
}

/* ❌ Poor: 1.2:1 contrast ratio */
.e-slider-track {
    background: #f0f0f0;  /* Light gray */
}

body {
    background: #e0e0e0;  /* Similar gray */
}
```

### Color-Blind Friendly Patterns

Don't rely on color alone to convey information:

```tsx
// ✅ Good: Color + pattern + text
<div style={{
  background: 'linear-gradient(to right, #ff6b6b, #ff8888)',
  borderLeft: '4px solid #cc0000'
}}>
  Limited range
</div>

// ❌ Avoid: Color only
<div style={{ background: '#ff6b6b' }}>
  Limited range
</div>
```

## Mobile Accessibility

### Touch Targets

Ensure handles are large enough for touch:

```css
/* Minimum 44x44 pixels for touch */
.e-control-wrapper.e-slider-container .e-slider .e-handle {
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
}
```

### Mobile Example

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function MobileAccessibleSlider() {
  const [value, setValue] = useState([30, 70]);

  return (
    <div style={{
      padding: '20px',
      maxWidth: '100%',
      WebkitUserSelect: 'none'  // Prevent text selection during drag
    }}>
      <label htmlFor="mobile-range">
        Select Range (Touch or Keyboard)
      </label>
      
      <SliderComponent
        id="mobile-range"
        type="Range"
        value={value}
        change={(e) => setValue(e.value as number[])}
        tooltip={{ isVisible: true, showOn: 'Always' }}
        aria-label="Adjustable range selector"
      />
      
      <p>Selected: {value[0]} - {value[1]}</p>
    </div>
  );
}

export default MobileAccessibleSlider;
```

### Zoom Support

Slider should work at 200% zoom:

```css
/* Allow responsive scaling */
.e-slider-container {
    width: 100%;
}

/* Ensure handles remain clickable at zoom */
.e-slider .e-handle {
    min-width: 24px;
    min-height: 24px;
}
```

## Testing Accessibility

### Automated Testing

Use accessibility checkers:

```bash
# npm packages
npm install axe-core accessibility-checker
```

```tsx
import { axe } from 'jest-axe';

test('slider is accessible', async () => {
  const { container } = render(
    <SliderComponent id="test-slider" value={50} />
  );
  
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] **Keyboard:** Tab to slider, use arrow keys
- [ ] **Screen reader:** Test with NVDA/JAWS
- [ ] **Focus visible:** Tab shows clear focus indicator
- [ ] **Contrast:** Check with color contrast analyzer
- [ ] **Mobile:** Test touch targets at 44x44px minimum
- [ ] **Zoom:** Test at 200% zoom level
- [ ] **Labels:** All inputs have associated labels
- [ ] **Feedback:** Value changes announced

### Testing Tools

1. **axe DevTools** - Browser extension
2. **WAVE** - WebAIM accessibility checker
3. **NVDA** - Free screen reader
4. **Lighthouse** - Chrome DevTools built-in

## Best Practices

### Pattern 1: Complete Accessible Slider

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function CompleteAccessibleSlider() {
  const [value, setValue] = useState([25, 75]);
  const [announcement, setAnnouncement] = useState('');

  function handleChange(e) {
    const [min, max] = e.value as number[];
    setValue([min, max]);
    setAnnouncement(`Range updated: ${min} to ${max}`);
  }

  return (
    <div>
      {/* Visible label */}
      <label htmlFor="accessible-range">
        Select Price Range
      </label>

      {/* Help text */}
      <p id="range-help">
        Use arrow keys to adjust the range.
        Press Home to go to minimum, End to go to maximum.
      </p>

      {/* Slider component */}
      <SliderComponent
        id="accessible-range"
        type="Range"
        value={value}
        change={handleChange}
        min={0}
        max={100}
        step={5}
        tooltip={{
          isVisible: true,
          showOn: 'Always'
        }}
        aria-describedby="range-help"
        aria-label="Adjustable price range"
      />

      {/* Live region for announcements */}
      <div aria-live="polite" aria-atomic="true">
        {announcement}
      </div>

      {/* Display current value */}
      <output>${value[0]} - ${value[1]}</output>
    </div>
  );
}

export default CompleteAccessibleSlider;
```

### Pattern 2: Accessible Form Integration

```tsx
import React, { useState } from 'react';
import { SliderComponent } from '@syncfusion/ej2-react-inputs';

function AccessibleForm() {
  const [budget, setBudget] = useState([1000, 5000]);
  const [errors, setErrors] = useState('');

  function handleBudgetChange(e) {
    const [min, max] = e.value as number[];
    
    if (min >= max) {
      setErrors('Minimum budget must be less than maximum');
    } else {
      setBudget([min, max]);
      setErrors('');
    }
  }

  return (
    <form>
      <fieldset>
        <legend>Budget Settings</legend>

        <div>
          <label htmlFor="budget-range">
            Project Budget Range (USD)
          </label>

          <SliderComponent
            id="budget-range"
            type="Range"
            value={budget}
            change={handleBudgetChange}
            min={500}
            max={50000}
            step={500}
            aria-describedby={errors ? 'budget-error' : undefined}
            aria-invalid={errors ? 'true' : 'false'}
          />

          {errors && (
            <div id="budget-error" role="alert" style={{ color: 'red' }}>
              {errors}
            </div>
          )}

          <p>
            Selected: ${budget[0].toLocaleString()} - 
            ${budget[1].toLocaleString()}
          </p>
        </div>

        <button type="submit">Save Settings</button>
      </fieldset>
    </form>
  );
}

export default AccessibleForm;
```

### Common Pitfalls to Avoid

1. **Missing labels:** Always provide visible labels
2. **No keyboard support:** Ensure full keyboard navigation
3. **Poor contrast:** Test color combinations
4. **Small touch targets:** Keep handles 44x44px minimum
5. **No ARIA:** Add descriptions for complex interactions
6. **Outdated screen readers:** Test with modern readers

## Compliance Checklist

- [ ] Component has `role="slider"`
- [ ] `aria-valuemin`, `aria-valuemax`, `aria-valuenow` present
- [ ] Keyboard navigation works (arrows, Home, End, Page Up/Down)
- [ ] Focus visible with clear outline
- [ ] All labels associated with controls
- [ ] Contrast ratio ≥ 3:1 for UI components
- [ ] Touch targets ≥ 44x44 pixels
- [ ] Screen reader announces changes
- [ ] Tested with at least one screen reader
- [ ] Works at 200% zoom level

## Resources

- [W3C WAI-ARIA Slider Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/slider/)
- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [Deque Accessibility University](https://dequeuniversity.com/)

## Next Steps

1. Add descriptive labels to your sliders
2. Test with keyboard-only navigation
3. Verify color contrast meets WCAG standards
4. Test with a screen reader
5. Check focus indicators are visible
6. Ensure touch targets are appropriately sized
7. Review [SKILL.md](../SKILL.md) for complete implementation guide
