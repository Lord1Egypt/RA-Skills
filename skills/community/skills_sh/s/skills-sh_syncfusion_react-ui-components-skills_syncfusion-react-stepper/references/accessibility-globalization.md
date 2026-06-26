# Accessibility and Globalization

## Table of Contents
- [Accessibility Overview](#accessibility-overview)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Localization](#localization)
- [RTL Support](#rtl-support)
- [Testing Accessibility](#testing-accessibility)

## Accessibility Overview

The Stepper component meets comprehensive accessibility standards including WCAG 2.2, Section 508, and ADA compliance.

### Accessibility Compliance

| Standard | Support |
|----------|---------|
| WCAG 2.2 | ✓ Full Support |
| Section 508 | ✓ Full Support |
| Screen Readers | ✓ Supported |
| Keyboard Navigation | ✓ Supported |
| Color Contrast | ✓ Compliant |
| Right-to-Left | ✓ Supported |
| Mobile Devices | ✓ Supported |

## WAI-ARIA Attributes

The Stepper component automatically includes ARIA attributes for screen readers:

### ARIA Labels

```jsx
<StepperComponent>
  <StepsDirective>
    {/* Each step automatically gets aria-label */}
    <StepDirective label="Step 1" />
    <StepDirective label="Step 2" />
  </StepsDirective>
</StepperComponent>
```

**Rendered ARIA:**
```html
<div role="tablist">
  <div role="tab" aria-label="Step 1" aria-current="true">...</div>
  <div role="tab" aria-label="Step 2" aria-current="false">...</div>
</div>
```

### ARIA Current

The `aria-current="page"` attribute identifies the active step:

```jsx
// Automatically applied by component
<div role="tab" aria-current="page" aria-label="Step 2">...</div>
```

### ARIA Disabled

Disabled steps have the `aria-disabled` attribute:

```jsx
<StepperComponent>
  <StepsDirective>
    <StepDirective label="Available" />
    <StepDirective label="Disabled" disabled={true} />
  </StepsDirective>
</StepperComponent>
```

**Rendered:**
```html
<div role="tab" aria-label="Available">...</div>
<div role="tab" aria-label="Disabled" aria-disabled="true">...</div>
```

## Keyboard Navigation

Users can navigate the Stepper entirely with keyboard:

### Keyboard Shortcuts

#### Horizontal Stepper
| Key | Action |
|-----|--------|
| **Left Arrow** | Move to previous step |
| **Right Arrow** | Move to next step |
| **Home** | Jump to first step |
| **End** | Jump to last step |
| **Enter / Space** | Activate focused step |
| **Tab** | Move focus to next interactive element |
| **Shift+Tab** | Move focus to previous interactive element |

#### Vertical Stepper
| Key | Action |
|-----|--------|
| **Up Arrow** | Move to previous step |
| **Down Arrow** | Move to next step |
| **Home** | Jump to first step |
| **End** | Jump to last step |
| **Enter / Space** | Activate focused step |

### Example: Keyboard Navigation

```jsx
function App() {
  return (
    <div>
      <p>Use arrow keys to navigate</p>
      <StepperComponent orientation="horizontal">
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
```

**User Journey:**
1. Tab → Focus on first step
2. Right Arrow → Move to next step
3. Right Arrow → Move to next step
4. Home → Jump back to first step
5. End → Jump to last step

## Localization

Support multiple languages by defining locale translations:

### Basic Localization

```jsx
import { L10n } from '@syncfusion/ej2-base';

// Define locale translations
L10n.load({
  'fr-FR': {
    'stepper': {
      'optional': 'Facultatif'
    }
  },
  'de-DE': {
    'stepper': {
      'optional': 'Optional'
    }
  },
  'es-ES': {
    'stepper': {
      'optional': 'Opcional'
    }
  }
});

function App() {
  return (
    <StepperComponent locale="fr-FR">
      <StepsDirective>
        <StepDirective label="Étape 1" />
        <StepDirective label="Étape 2" optional={true} />
        <StepDirective label="Étape 3" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Locale Switching

```jsx
function App() {
  const [locale, setLocale] = React.useState('en-US');

  const locales = {
    'en-US': 'English',
    'fr-FR': 'Français',
    'de-DE': 'Deutsch',
    'es-ES': 'Español'
  };

  // Define translations
  React.useEffect(() => {
    L10n.load({
      'fr-FR': { 'stepper': { 'optional': 'Facultatif' } },
      'de-DE': { 'stepper': { 'optional': 'Optional' } },
      'es-ES': { 'stepper': { 'optional': 'Opcional' } }
    });
  }, []);

  return (
    <div>
      <select value={locale} onChange={(e) => setLocale(e.target.value)}>
        {Object.entries(locales).map(([code, name]) => (
          <option key={code} value={code}>{name}</option>
        ))}
      </select>

      <StepperComponent locale={locale}>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" optional={true} />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
    </div>
  );
}
```

### Supported Locales

Default English locale: `en-US`

You can extend with any locale:
- `fr-FR` (French)
- `de-DE` (German)
- `es-ES` (Spanish)
- `ar-AE` (Arabic)
- `ja-JP` (Japanese)
- `zh-CN` (Chinese)
- And many others...

## RTL Support

Enable right-to-left layout for RTL languages:

### Basic RTL

```jsx
<StepperComponent enableRtl={true}>
  <StepsDirective>
    <StepDirective label="الخطوة 1" />
    <StepDirective label="الخطوة 2" />
    <StepDirective label="الخطوة 3" />
  </StepsDirective>
</StepperComponent>
```

### RTL with Localization

```jsx
import { L10n } from '@syncfusion/ej2-base';

function App() {
  L10n.load({
    'ar-AE': {
      'stepper': {
        'optional': 'اختياري'
      }
    }
  });

  return (
    <StepperComponent enableRtl={true} locale="ar-AE">
      <StepsDirective>
        <StepDirective label="الإشارة الأولى" />
        <StepDirective label="الإشارة الثانية" optional={true} />
        <StepDirective label="الإشارة الثالثة" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### Global RTL Configuration

Enable RTL for entire application:

```jsx
import { enableRtl } from '@syncfusion/ej2-base';

// Enable RTL globally
enableRtl(true);

function App() {
  return (
    <StepperComponent>
      {/* All Syncfusion components will be RTL */}
      <StepsDirective>
        <StepDirective label="Step 1" />
        <StepDirective label="Step 2" />
      </StepsDirective>
    </StepperComponent>
  );
}
```

### RTL Effects

When RTL is enabled:
- Steps flow right-to-left
- Navigation arrows reverse
- Labels position on opposite side
- Text direction automatically adjusted
- Layout mirrors appropriately

## Testing Accessibility

### Automated Testing

Use tools to validate accessibility:

```bash
# Install accessibility checker
npm install accessibility-checker

# Install axe-core
npm install axe-core
```

### Manual Testing Checklist

- [ ] **Keyboard Navigation:** Test all arrow keys, Home, End, Enter/Space
- [ ] **Screen Reader:** Test with NVDA, JAWS, or VoiceOver
- [ ] **Color Contrast:** Use contrast analyzer (WCAG AA or AAA)
- [ ] **Focus Indicators:** Verify visible focus rings
- [ ] **Labels:** Confirm aria-labels are descriptive
- [ ] **RTL:** Test with RTL language
- [ ] **Mobile:** Test with mobile screen readers

### Testing with Screen Readers

#### Using NVDA (Windows)
1. Download [NVDA](url)
2. Start NVDA
3. Open browser and navigate to stepper
4. Use NVDA shortcuts to explore component

#### Using JAWS (Windows)
1. Open JAWS
2. Open application with stepper
3. Use JAWS navigation keys (arrow keys, etc.)

#### Using VoiceOver (Mac)
1. Enable VoiceOver: Cmd + F5
2. Use VO shortcuts to navigate
3. Test keyboard navigation

### Code Example: Testing

```jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { StepperComponent, StepsDirective, StepDirective } from '@syncfusion/ej2-react-navigations';

describe('Stepper Accessibility', () => {
  test('should have proper ARIA labels', () => {
    render(
      <StepperComponent>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
        </StepsDirective>
      </StepperComponent>
    );

    const steps = screen.getAllByRole('tab');
    expect(steps[0]).toHaveAttribute('aria-label', 'Step 1');
    expect(steps[1]).toHaveAttribute('aria-label', 'Step 2');
  });

  test('should navigate with keyboard arrows', async () => {
    const user = userEvent.setup();
    const { container } = render(
      <StepperComponent>
        <StepsDirective>
          <StepDirective label="Step 1" />
          <StepDirective label="Step 2" />
          <StepDirective label="Step 3" />
        </StepsDirective>
      </StepperComponent>
    );

    const firstStep = screen.getByRole('tab', { name: 'Step 1' });
    await user.click(firstStep);
    await user.keyboard('{ArrowRight}');

    const secondStep = screen.getByRole('tab', { name: 'Step 2' });
    expect(secondStep).toHaveFocus();
  });
});
```

## Best Practices

**Accessibility:**
- ✅ Always use descriptive labels
- ✅ Test with keyboard navigation
- ✅ Verify with screen readers
- ✅ Maintain color contrast ratios (WCAG AA)
- ✅ Provide meaningful aria-labels for complex steps

**Localization:**
- ✅ Define all locale translations upfront
- ✅ Test RTL layouts thoroughly
- ✅ Provide localized error messages
- ✅ Consider text length in different languages

**RTL:**
- ✅ Test navigation in RTL mode
- ✅ Verify icon positioning
- ✅ Check label alignment
- ✅ Ensure proper text direction (auto-set by component)
