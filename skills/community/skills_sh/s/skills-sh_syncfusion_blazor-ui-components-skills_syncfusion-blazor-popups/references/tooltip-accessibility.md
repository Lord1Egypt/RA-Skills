# Tooltip Accessibility

## Table of Contents
- [Overview](#overview)
- [Accessibility Standards Compliance](#accessibility-standards-compliance)
- [WAI-ARIA Attributes](#wai-aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Color Contrast](#color-contrast)
- [Mobile Device Accessibility](#mobile-device-accessibility)
- [Best Practices](#best-practices)
- [Testing for Accessibility](#testing-for-accessibility)

## Overview

The Syncfusion Blazor Tooltip component is designed to meet modern accessibility standards, ensuring usability for all users including those with disabilities. The component provides built-in support for:

- **WCAG 2.2** (Web Content Accessibility Guidelines)
- **Section 508** compliance
- **WAI-ARIA** patterns and attributes
- **Keyboard navigation**
- **Screen reader** compatibility
- **RTL** (Right-to-Left) language support
- **Color contrast** requirements
- **Mobile device** accessibility

## Accessibility Standards Compliance

### Compliance Table

| Accessibility Criteria | Compatibility |
| ----------------------- | ------------- |
| **WCAG 2.2 Support** | Level AA |
| **Section 508 Support** | ✓ Full Support |
| **Screen Reader Support** | ✓ Full Support |
| **Right-To-Left Support** | ✓ Full Support |
| **Color Contrast** | ✓ Meets Requirements |
| **Mobile Device Support** | ✓ Full Support |
| **Keyboard Navigation Support** | ✓ Full Support |
| **Axe-core Accessibility Validation** | ✓ Validated |

### WCAG 2.2 Level AA

The Tooltip component meets WCAG 2.2 Level AA standards:
- **Perceivable**: Content is presented in ways all users can perceive
- **Operable**: UI components are operable via keyboard and other input methods
- **Understandable**: Information and operation are understandable
- **Robust**: Content works with current and future assistive technologies

### Section 508

Compliant with U.S. Section 508 standards for federal accessibility requirements:
- Electronic and information technology accessibility
- Keyboard accessibility
- Screen reader compatibility
- Color contrast requirements

### Axe-core Validation

The component has been validated using axe-core, an automated accessibility testing engine that checks for:
- ARIA implementation
- Keyboard accessibility
- Color contrast
- Semantic HTML
- Focus management

## WAI-ARIA Attributes

The Tooltip follows WAI-ARIA tooltip pattern specifications.

### role="tooltip"

The tooltip element uses the ARIA `tooltip` role:

```html
<div class="e-tooltip-wrap e-popup" role="tooltip">
    <div class="e-tip-content">Tooltip content</div>
</div>
```

**Purpose:** Identifies the element as a tooltip to assistive technologies.

### aria-describedby

When a tooltip opens, the `aria-describedby` attribute is added to the target element:

```html
<!-- Before tooltip opens -->
<button id="saveBtn">Save</button>

<!-- After tooltip opens -->
<button id="saveBtn" aria-describedby="tooltip-123">Save</button>

<div id="tooltip-123" role="tooltip" aria-hidden="false">
    Save your changes
</div>
```

**Purpose:** Establishes relationship between target and tooltip content for screen readers.

### aria-hidden

The tooltip's `aria-hidden` attribute changes based on visibility:

```html
<!-- Tooltip closed -->
<div class="e-tooltip-wrap" role="tooltip" aria-hidden="true">
    ...
</div>

<!-- Tooltip open -->
<div class="e-tooltip-wrap" role="tooltip" aria-hidden="false">
    ...
</div>
```

**Purpose:** Indicates whether the tooltip is visible to assistive technologies.

### Multiple aria-describedby Values

When a target already has `aria-describedby`, the tooltip ID is appended:

```html
<!-- Existing aria-describedby -->
<input id="email" aria-describedby="email-instructions" />

<!-- After tooltip opens -->
<input id="email" aria-describedby="email-instructions tooltip-456" />
```

**Purpose:** Preserves existing accessibility relationships while adding tooltip.

### Implementation Example

```razor
@using Syncfusion.Blazor.Popups
@using Syncfusion.Blazor.Buttons

<SfTooltip Target="#accessibleBtn" Content="This button saves your work">
    <SfButton ID="accessibleBtn" Content="Save"></SfButton>
</SfTooltip>

<!-- Rendered with ARIA attributes automatically -->
```

## Keyboard Navigation

The Tooltip component supports full keyboard accessibility.

### Supported Keyboard Shortcuts

| Key | Action |
| --- | ------ |
| **Tab** | Moves focus to next focusable element. If target receives focus, tooltip opens (with OpensOn="Auto" or "Focus"). |
| **Shift + Tab** | Moves focus to previous focusable element. Tooltip closes when target loses focus. |
| **Escape** | Closes the open tooltip. |
| **Enter / Space** | If target is a button or link, activates it. Tooltip behavior depends on OpensOn setting. |

### Focus Mode Example

```razor
<SfTooltip Target=".help-input" Content="Enter your email address" OpensOn="Focus">
    <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" class="help-input" type="email" />
    </div>
    <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" class="help-input" type="password" />
    </div>
</SfTooltip>
```

**Behavior:**
1. Press `Tab` to focus first input
2. Tooltip appears automatically
3. Press `Tab` again to move to next input
4. First tooltip closes, second tooltip opens
5. Press `Escape` to close tooltip (if sticky)

### Keyboard Navigation Best Practices

**Ensure targets are focusable:**
```razor
<!-- ✅ Focusable by default -->
<button>Button</button>
<input type="text" />
<a href="#">Link</a>

<!-- ✅ Made focusable with tabindex -->
<div tabindex="0">Custom element</div>

<!-- ❌ Not keyboard accessible -->
<div onclick="...">Non-focusable div</div>
```

**Use appropriate OpensOn modes:**
```razor
<!-- Good for keyboard users -->
<SfTooltip Target="#btn" OpensOn="Focus">
    <button id="btn">Action</button>
</SfTooltip>

<!-- Also good - responds to both hover and focus -->
<SfTooltip Target="#btn2" OpensOn="Hover Focus">
    <button id="btn2">Action</button>
</SfTooltip>
```

### Sticky Mode Keyboard Access

For sticky tooltips, ensure close button is keyboard accessible:

```razor
<SfTooltip Target="#infoBtn" Content="Detailed information" 
           OpensOn="Click" IsSticky="true">
    <button id="infoBtn">Information</button>
</SfTooltip>
```

**Behavior:**
1. `Tab` to button
2. Press `Enter` or `Space` to open tooltip
3. Close button automatically receives focus
4. Press `Enter` or `Escape` to close

## Screen Reader Support

The Tooltip component works with major screen readers:
- **JAWS** (Job Access With Speech)
- **NVDA** (NonVisual Desktop Access)
- **VoiceOver** (macOS/iOS)
- **TalkBack** (Android)
- **Narrator** (Windows)

### How Screen Readers Announce Tooltips

**With Focus mode:**
```razor
<SfTooltip Target="#saveBtn" Content="Saves your document" OpensOn="Focus">
    <button id="saveBtn">Save</button>
</SfTooltip>
```

Screen reader announces: "Save button, Saves your document"

**With aria-label:**
```razor
<SfTooltip Target="#iconBtn" Content="Settings menu">
    <button id="iconBtn" aria-label="Open settings">⚙️</button>
</SfTooltip>
```

Screen reader announces: "Open settings button, Settings menu"

### Best Practices for Screen Readers

**Use clear, concise tooltip text:**
```razor
<!-- ✅ Good -->
<SfTooltip Content="Delete this item permanently">
    <button>Delete</button>
</SfTooltip>

<!-- ❌ Avoid redundancy -->
<SfTooltip Content="Click this button to delete this item">
    <button>Delete</button>
</SfTooltip>
```

**Don't repeat button text:**
```razor
<!-- ❌ Redundant -->
<SfTooltip Content="Save button">
    <button>Save</button>
</SfTooltip>

<!-- ✅ Adds value -->
<SfTooltip Content="Saves changes to the server">
    <button>Save</button>
</SfTooltip>
```

**Provide context, not instructions:**
```razor
<!-- ✅ Good -->
<SfTooltip Content="Last saved 5 minutes ago">
    <button>💾</button>
</SfTooltip>

<!-- ❌ Unnecessary -->
<SfTooltip Content="Click to save">
    <button>Save</button>
</SfTooltip>
```

## Right-to-Left (RTL) Support

The Tooltip component fully supports RTL languages (Arabic, Hebrew, etc.).

### Enabling RTL

RTL is typically enabled at the application level:

```razor
<!-- In App.razor or layout -->
<div dir="rtl">
    <SfTooltip Target="#btn" Content="محتوى تلميح الأداة">
        <button id="btn">زر</button>
    </SfTooltip>
</div>
```

### RTL Behavior

- **Positioning**: Left/Right positions are mirrored
- **Arrows**: Point in appropriate direction for RTL
- **Text alignment**: Content aligns right by default
- **Animations**: Slide directions are reversed

### RTL Example

```razor
<div dir="rtl" lang="ar">
    <SfTooltip Target=".arabic-btn" Content="احفظ عملك" Position="Position.RightCenter">
        <button class="arabic-btn">حفظ</button>
    </SfTooltip>
</div>
```

In RTL mode, `Position.RightCenter` displays on the left side (mirrored).

## Color Contrast

The Tooltip component meets WCAG 2.2 color contrast requirements.

### Contrast Requirements

**Level AA Standards:**
- **Normal text**: Minimum 4.5:1 contrast ratio
- **Large text** (18pt+ or 14pt+ bold): Minimum 3:1 contrast ratio
- **UI components**: Minimum 3:1 contrast ratio

### Default Theme Contrast

Syncfusion themes are designed to meet contrast requirements:

```razor
<!-- Default bootstrap5 theme has compliant contrast -->
<link href="_content/Syncfusion.Blazor.Themes/bootstrap5.css" rel="stylesheet" />
```

### Custom Styling with Good Contrast

```razor
<SfTooltip Target="#btn" CssClass="high-contrast-tooltip" Content="Accessible content">
    <button id="btn">Button</button>
</SfTooltip>

<style>
    /* ✅ Good contrast: White text on dark background -->
    .high-contrast-tooltip.e-tooltip-wrap.e-popup {
        background-color: #2d2d2d; /* Dark gray */
    }
    
    .high-contrast-tooltip.e-tooltip-wrap .e-tip-content {
        color: #ffffff; /* White */
        /* Contrast ratio: 12.6:1 (Passes AAA) */
    }
</style>
```

### Testing Contrast

Use browser dev tools or online tools:
- Chrome DevTools: Inspect element → Accessibility pane
- Online: WebAIM Contrast Checker
- Browser extensions: axe DevTools, WAVE

### Avoid Low Contrast

```razor
<style>
    /* ❌ Poor contrast - fails WCAG -->
    .bad-contrast.e-tooltip-wrap.e-popup {
        background-color: #cccccc; /* Light gray */
    }
    
    .bad-contrast.e-tooltip-wrap .e-tip-content {
        color: #999999; /* Medium gray */
        /* Contrast ratio: 2.4:1 (Fails) */
    }
</style>
```

## Mobile Device Accessibility

The Tooltip component is accessible on mobile devices.

### Touch Accessibility

**Tap and Hold:**
```razor
<!-- Opens on tap and hold (mobile) or hover (desktop) -->
<SfTooltip Target="#mobileBtn" Content="Mobile accessible tooltip">
    <button id="mobileBtn">Tap and hold</button>
</SfTooltip>
```

**Single Tap:**
```razor
<!-- Opens on single tap (mobile) or click (desktop) -->
<SfTooltip Target="#tapBtn" Content="Tap to see info" OpensOn="Click">
    <button id="tapBtn">Tap me</button>
</SfTooltip>
```

### Touch Target Size

Ensure adequate touch target sizes (minimum 44x44 pixels):

```razor
<SfTooltip Target=".mobile-icon" Content="Help">
    <button class="mobile-icon" style="min-width: 44px; min-height: 44px; padding: 10px;">
        ❓
    </button>
</SfTooltip>
```

### Mobile Screen Reader

Works with TalkBack (Android) and VoiceOver (iOS):

```razor
<!-- Accessible on mobile screen readers -->
<SfTooltip Target="#mobileAction" Content="Saves your progress" OpensOn="Click">
    <button id="mobileAction">Save</button>
</SfTooltip>
```

### Responsive Tooltip Sizing

```razor
<SfTooltip Target="#responsiveBtn" CssClass="mobile-friendly" Content="Mobile optimized">
    <button id="responsiveBtn">Action</button>
</SfTooltip>

<style>
    @media (max-width: 768px) {
        .mobile-friendly.e-tooltip-wrap {
            max-width: 90vw !important;
        }
        
        .mobile-friendly.e-tooltip-wrap .e-tip-content {
            font-size: 16px !important; /* Readable on mobile */
            padding: 12px !important;
        }
    }
</style>
```

## Best Practices

### Essential Information

❌ **Don't:** Put critical information only in tooltips
```razor
<!-- Bad: Essential action in tooltip only -->
<SfTooltip Content="Click three times to activate">
    <button>Activate</button>
</SfTooltip>
```

✅ **Do:** Use tooltips to supplement visible information
```razor
<!-- Good: Tooltip adds context -->
<button>Activate (3 clicks required)</button>
<SfTooltip Target="#activate" Content="Multiple clicks prevent accidental activation">
    <button id="activate">Activate (3 clicks required)</button>
</SfTooltip>
```

### Timing

Provide adequate time to read tooltips:
```razor
<!-- Good: Delay before closing gives time to read -->
<SfTooltip Target="#info" Content="Longer description" CloseDelay="1000">
    <button id="info">Info</button>
</SfTooltip>
```

### Focus Management

Ensure logical focus order:
```razor
<SfTooltip Target=".form-field" OpensOn="Focus">
    <label for="field1">Field 1:</label>
    <input id="field1" class="form-field" tabindex="1" />
    
    <label for="field2">Field 2:</label>
    <input id="field2" class="form-field" tabindex="2" />
</SfTooltip>
```

### Semantic HTML

Use semantic HTML elements:
```razor
<!-- ✅ Good: Semantic button -->
<SfTooltip Content="Delete item">
    <button type="button">Delete</button>
</SfTooltip>

<!-- ❌ Avoid: Non-semantic div styled as button -->
<SfTooltip Content="Delete item">
    <div onclick="..." style="cursor: pointer;">Delete</div>
</SfTooltip>
```

### Alternative Access

Provide alternatives to tooltips:
```razor
<!-- Tooltip + visible help text -->
<div class="form-group">
    <label for="email">Email:</label>
    <input id="email" type="email" />
    <small class="help-text">We'll never share your email.</small>
    <SfTooltip Target="#email" Content="Format: user@example.com" OpensOn="Focus">
    </SfTooltip>
</div>
```

## Testing for Accessibility

### Automated Testing

**Use axe DevTools:**
```bash
# Install axe-core for testing
dotnet add package Deque.AxeCore.Playwright
```

**In your tests:**
```csharp
// Run accessibility audit
var axeResults = await new AxeBuilder(page).Analyze();
Assert.Empty(axeResults.Violations);
```

### Manual Testing

**Keyboard Navigation:**
1. Tab through all interactive elements
2. Verify tooltips open on focus
3. Test Escape key closes tooltips
4. Check focus visible indicators

**Screen Reader:**
1. Enable screen reader (NVDA, JAWS, VoiceOver)
2. Navigate with Tab key
3. Verify tooltip content is announced
4. Check aria-describedby associations

**Color Contrast:**
1. Use Chrome DevTools Accessibility pane
2. Check contrast ratios meet 4.5:1 minimum
3. Test with different themes
4. Verify in high contrast mode

**Mobile:**
1. Test on actual mobile devices
2. Verify tap and hold behavior
3. Check touch target sizes
4. Test with mobile screen readers

### Accessibility Checklist

- [ ] All interactive tooltips are keyboard accessible
- [ ] Tooltip targets are focusable (button, input, a, or tabindex="0")
- [ ] Escape key closes tooltips
- [ ] Screen reader announces tooltip content
- [ ] ARIA attributes are correct (role, aria-describedby, aria-hidden)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Touch targets are at least 44x44 pixels
- [ ] Tooltips don't contain essential information not available elsewhere
- [ ] RTL languages are supported if applicable
- [ ] Mobile screen readers work correctly
- [ ] Focus order is logical
- [ ] Semantic HTML is used for targets
- [ ] axe-core tests pass

### Resources

**Tools:**
- [axe DevTools](https://www.deque.com/axe/devtools/) - Browser extension for accessibility testing
- [WAVE](https://wave.webaim.org/) - Web accessibility evaluation tool
- [Chrome Lighthouse](https://developers.google.com/web/tools/lighthouse) - Accessibility audit
- [NVDA](https://www.nvaccess.org/) - Free screen reader

**Guidelines:**
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) - Web Content Accessibility Guidelines
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) - ARIA patterns
- [Section 508](https://www.section508.gov/) - U.S. federal accessibility standards

**Syncfusion Resources:**
- [Syncfusion Blazor Accessibility Sample](https://blazor.syncfusion.com/accessibility/tooltip) - Live demo
- [Syncfusion Accessibility Documentation](https://blazor.syncfusion.com/documentation/common/accessibility) - Comprehensive guide
