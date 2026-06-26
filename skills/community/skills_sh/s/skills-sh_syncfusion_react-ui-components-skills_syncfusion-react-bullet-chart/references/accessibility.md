# Accessibility in React Bullet Chart

## Table of Contents
- [Overview](#overview)
- [Accessibility Standards Compliance](#accessibility-standards-compliance)
- [Accessibility Features](#accessibility-features)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Interaction](#keyboard-interaction)
- [Accessibility Testing](#accessibility-testing)
- [Best Practices](#best-practices)
- [Additional Resources](#additional-resources)

## Overview

The Bullet Chart component follows accessibility guidelines and standards to ensure it can be used by people with disabilities. The component is designed to be accessible through screen readers, keyboard navigation, and meets various accessibility compliance requirements.

## Accessibility Standards Compliance

The Bullet Chart component follows these accessibility standards:

- **[ADA](https://www.ada.gov)**: Americans with Disabilities Act compliance
- **[Section 508](https://www.section508.gov)**: U.S. federal accessibility standard
- **[WCAG 2.2](https://www.w3.org/TR/WCAG22)**: Web Content Accessibility Guidelines 2.2
- **[WCAG roles](https://www.w3.org/TR/wai-aria#roles)**: Proper ARIA role usage

### Accessibility Compliance Table

| Accessibility Criteria | Compatibility |
| ---------------------- | ------------- |
| **WCAG 2.2 Support** | ✓ Full Support |
| **Section 508 Support** | ✓ Full Support |
| **Screen Reader Support** | ✓ Full Support |
| **Right-To-Left Support** | ✓ Full Support |
| **Color Contrast** | ✓ Full Support |
| **Mobile Device Support** | ✓ Full Support |
| **Keyboard Navigation Support** | ✓ Full Support |
| **Accessibility Checker Validation** | ✓ Full Support |
| **Axe-core Accessibility Validation** | ✓ Full Support |

**Legend:**
- ✓ **Full Support**: All features of the component meet the requirement
- ~ **Partial Support**: Some features do not meet the requirement
- ✗ **Not Supported**: The component does not meet the requirement

## Accessibility Features

### WCAG 2.2 Compliance

The Bullet Chart meets WCAG 2.2 Level AA standards, including:
- Perceivable content for all users
- Operable interface components
- Understandable information and UI
- Robust content that works with assistive technologies

### Section 508 Compliance

Full compliance with U.S. federal Section 508 standards for electronic and information technology accessibility.

### Screen Reader Support

The Bullet Chart provides full screen reader support, allowing users with visual impairments to understand the chart's data through:
- Descriptive ARIA labels
- Proper semantic structure
- Meaningful text alternatives

**Example with screen reader support:**
```tsx
<BulletChartComponent
    id="bulletChart"
    dataSource={data}
    valueField="value"
    targetField="target"
    title="Revenue Performance"       // Read by screen readers
    subtitle="Q1 2024"                // Additional context
    minimum={0}
    maximum={300}
/>
```

### Right-to-Left (RTL) Support

Full support for RTL languages (Arabic, Hebrew, etc.) through the `enableRtl` property.

```tsx
<BulletChartComponent
    enableRtl={true}
    title="الإيرادات"
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

### Color Contrast

The component ensures sufficient color contrast ratios to meet WCAG requirements:
- Minimum 4.5:1 contrast ratio for normal text
- Minimum 3:1 contrast ratio for graphical objects
- High contrast theme available

### Mobile Device Support

Fully responsive and touch-friendly for mobile devices:
- Touch-optimized interactions
- Responsive sizing
- Mobile-friendly tooltips

### Keyboard Navigation Support

Complete keyboard navigation support for users who cannot use a mouse (see Keyboard Interaction section below).

## WAI-ARIA Attributes

The Bullet Chart component follows [WAI-ARIA](https://www.w3.org/WAI/ARIA/apg/patterns/alert) patterns and uses appropriate ARIA attributes.

### ARIA Roles

**img (role)**
The chart uses the `img` role to indicate it's a graphical representation:
```html
<div role="img" aria-label="Revenue Performance Bullet Chart">
  <!-- Chart content -->
</div>
```

**button (role)**
Interactive elements use the `button` role for proper accessibility:
```html
<button role="button" aria-label="Print Chart">Print</button>
```

### ARIA Attributes

**aria-label (attribute)**
Provides accessible names for elements:
```tsx
<BulletChartComponent
    id="bulletChart"
    title="Revenue Performance"    // Used as aria-label
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

**aria-pressed (attribute)**
Indicates the pressed state of toggle buttons in the chart's UI.

### Implementing ARIA Labels

```tsx
import { BulletChartComponent } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Quarterly Revenue Performance"  // Primary label
                subtitle="Q1 2024 - Target $250K"      // Additional context
                minimum={0}
                maximum={300}
            />
        </div>
    );
}
```

## Keyboard Interaction

The Bullet Chart follows [keyboard interaction](https://www.w3.org/WAI/ARIA/apg/patterns/alert#keyboardinteraction) guidelines, making it accessible for users who rely on keyboard navigation.

### Supported Keyboard Shortcuts

| Key Combination | Action |
| --------------- | ------ |
| **Tab** | Moves focus to the next element in the Bullet Chart |
| **Shift + Tab** | Moves focus to the previous element in the Bullet Chart |
| **Ctrl + P** | Prints the Bullet Chart |

### Keyboard Navigation Example

```tsx
import { BulletChartComponent, BulletTooltip, Inject } from "@syncfusion/ej2-react-charts";

function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Revenue Performance"
                tooltip={{ enable: true }}    // Accessible via keyboard
                minimum={0}
                maximum={300}
            >
                <Inject services={[BulletTooltip]} />
            </BulletChartComponent>
        </div>
    );
}
```

Users can:
1. **Tab** to focus on the chart
2. **Tab** to cycle through interactive elements
3. **Ctrl + P** to print the chart
4. **Shift + Tab** to navigate backwards

## Accessibility Testing

The Bullet Chart's accessibility is validated using industry-standard testing tools.

### Accessibility Checker

The component is tested with the [accessibility-checker](https://www.npmjs.com/package/accessibility-checker) npm package during automated testing.

**Install and use:**
```bash
npm install accessibility-checker --save-dev
```

### Axe-core Testing

The component is validated with [axe-core](https://www.npmjs.com/package/axe-core), a leading accessibility testing engine.

**Install and use:**
```bash
npm install axe-core --save-dev
```

### Sample Accessibility Demo

Syncfusion provides an accessibility sample to evaluate the Bullet Chart with accessibility tools:

[Open Accessibility Sample](https://ej2.syncfusion.com/accessibility/bullet-chart.html)

This sample allows you to:
- Test with screen readers
- Verify keyboard navigation
- Check color contrast
- Validate ARIA attributes

## Best Practices

### Color and Contrast

**Do:**
- Use sufficient color contrast (4.5:1 minimum for text, 3:1 for graphics)
- Provide alternative indicators beyond color (patterns, labels)
- Test with color blindness simulators
- Use the HighContrast theme for accessibility-focused applications

```tsx
<BulletChartComponent
    theme="HighContrast"           // High contrast for accessibility
    dataLabel={{ enable: true }}   // Labels provide non-color info
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

**Don't:**
- Rely solely on color to convey information
- Use low-contrast color combinations
- Assume all users can distinguish colors

### Screen Reader Optimization

**Do:**
- Provide descriptive titles and subtitles
- Use meaningful data labels
- Keep chart descriptions concise but informative

```tsx
<BulletChartComponent
    title="Revenue vs Target - Q1 2024"    // Descriptive
    subtitle="Actual: $270K, Target: $250K, Status: Exceeded"
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

**Don't:**
- Use vague titles like "Chart 1"
- Omit context in titles
- Use abbreviations without explanation

### Keyboard Accessibility

**Do:**
- Ensure all interactive features are keyboard-accessible
- Maintain logical tab order
- Provide keyboard shortcuts documentation

**Don't:**
- Create keyboard traps (where users can't tab out)
- Require mouse-only interactions
- Override default keyboard behavior without alternatives

### Responsive Design

**Do:**
- Test on multiple device sizes
- Ensure touch targets are at least 44×44 pixels
- Make charts responsive with percentage widths

```tsx
<BulletChartComponent
    width="100%"                   // Responsive width
    height="120px"                 // Sufficient height for touch
    dataSource={data}
    valueField="value"
    targetField="target"
/>
```

**Don't:**
- Use fixed small sizes that don't scale
- Create touch targets smaller than 44×44 pixels
- Assume all users have large screens

### Alternative Content

**Do:**
- Provide data tables as alternatives
- Offer downloadable data
- Include text summaries of key insights

```tsx
function App() {
    const data = [
        { value: 270, target: 250 }
    ];

    return (
        <div>
            <BulletChartComponent
                id="bulletChart"
                dataSource={data}
                valueField="value"
                targetField="target"
                title="Revenue Performance"
            />
            
            {/* Alternative text description */}
            <div className="sr-only">
                Revenue Performance: Actual value $270K exceeded 
                target of $250K by $20K (8% above target).
            </div>
        </div>
    );
}
```

**Don't:**
- Rely solely on visual representation
- Hide critical information in graphics only
- Forget alternative text for complex charts

## Additional Resources

### Syncfusion Accessibility Guide

For comprehensive information about accessibility across all Syncfusion React components:
- [Accessibility in Syncfusion React components](../common/accessibility)

### External Resources

- **WCAG Guidelines**: [www.w3.org/WAI/WCAG22/quickref/](https://www.w3.org/WAI/WCAG22/quickref/)
- **ARIA Authoring Practices**: [www.w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/)
- **Section 508**: [www.section508.gov](https://www.section508.gov)
- **WebAIM**: [webaim.org](https://webaim.org)

### Testing Tools

- **NVDA Screen Reader**: [www.nvaccess.org](https://www.nvaccess.org)
- **JAWS Screen Reader**: [www.freedomscientific.com/products/software/jaws/](https://www.freedomscientific.com/products/software/jaws/)
- **Axe DevTools**: Browser extension for accessibility testing
- **WAVE**: [wave.webaim.org](https://wave.webaim.org)

## Implementation Checklist

- [ ] Use descriptive titles and subtitles
- [ ] Enable data labels for non-visual value representation
- [ ] Ensure sufficient color contrast (4.5:1 minimum)
- [ ] Test with screen readers (NVDA, JAWS)
- [ ] Verify keyboard navigation (Tab, Shift+Tab, Ctrl+P)
- [ ] Test with accessibility-checker or axe-core
- [ ] Provide alternative text descriptions
- [ ] Use HighContrast theme for accessibility-focused apps
- [ ] Test on mobile devices with touch interactions
- [ ] Validate ARIA attributes are present
- [ ] Ensure responsive sizing for all devices
- [ ] Don't rely solely on color to convey information
- [ ] Provide data table alternatives when appropriate
- [ ] Test with color blindness simulators
- [ ] Document keyboard shortcuts for users
