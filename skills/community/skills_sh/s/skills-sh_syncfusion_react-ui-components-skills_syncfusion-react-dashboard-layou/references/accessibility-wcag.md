# Accessibility and WCAG Compliance

## Table of Contents
- [Overview](#overview)
- [WCAG 2.2 Compliance](#wcag-22-compliance)
- [Section 508 Standards](#section-508-standards)
- [WAI-ARIA Implementation](#wai-aria-implementation)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [RTL Support](#rtl-support)
- [Testing and Validation](#testing-and-validation)

## Overview

Dashboard Layout is designed with accessibility as a core principle, following industry standards and best practices. The component supports WCAG 2.2 Level AA compliance, Section 508 accessibility standards, and full WAI-ARIA implementation.

### Accessibility Standards Supported

| Standard | Version | Coverage | Status |
|----------|---------|----------|--------|
| WCAG | 2.2 | Level AA | ✅ Full |
| Section 508 | 2023 | Technical Standards | ✅ Full |
| WAI-ARIA | 1.2 | Authoring Practices | ✅ Full |
| ATAG | 2.0 | Authoring Tools | ✅ Supported |

## WCAG 2.2 Compliance

Dashboard Layout implements all WCAG 2.2 Level AA requirements:

### Perceivable

**1.4.3 Contrast (Minimum)**
- Text contrast ratio: 4.5:1 for normal text
- UI component contrast: 3:1 minimum
- Decorative elements: no contrast requirement

```css
/* High contrast panel header */
.e-panel .e-panel-header {
  background: #212121;
  color: #ffffff;
  /* Contrast ratio: 21:1 ✅ */
}

.e-panel .e-panel-content {
  background: #ffffff;
  color: #333333;
  /* Contrast ratio: 10.5:1 ✅ */
}
```

**1.4.11 Non-Text Contrast**
- All UI controls meet 3:1 minimum contrast
- Graphical elements clearly distinguishable

```tsx
// Resize handle with high contrast
const panels = [
  {
    id: 'accessible-panel',
    header: 'Accessible Panel',
    content: '<div>Content</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];

// CSS
.e-panel .e-south-east {
  background: linear-gradient(135deg, transparent 50%, #0066cc 50%);
  /* Clear contrast against white background */
}
```

### Operable

**2.1.1 Keyboard (Level A)**
- All functionality available via keyboard
- No keyboard trap
- Focus order logical and intuitive

**2.4.3 Focus Order**
- Tab navigation follows logical reading order
- Focus is always visible

```tsx
function AccessibleDashboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      tabIndex={0}
      /* Focus management automatic */
    />
  );
}
```

**2.4.7 Focus Visible**
- Focus indicator always visible
- Minimum 2px wide outline

```css
/* Visible focus indicator */
.e-panel:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

.e-panel .e-panel-header:focus-visible {
  outline: 2px solid #0066cc;
}

.e-panel .e-resize-handle:focus-visible {
  outline: 2px solid #0066cc;
  border-radius: 2px;
}
```

### Understandable

**3.2.1 On Focus**
- Dashboard doesn't change context on focus
- No automatic submissions or navigations

**3.2.4 Consistent Identification**
- Components consistently identified
- Resize handles always in same location
- Drag handles always accessible

### Robust

**4.1.3 Status Messages**
- Live regions announce changes
- Drag and drop events communicated

```tsx
// Announce panel changes to screen readers
function AccessibleDashboard() {
  const handlePanelRemove = (args: any) => {
    const announcement = `Panel ${args.id} removed`;
    const liveRegion = document.getElementById('announcements');
    if (liveRegion) {
      liveRegion.textContent = announcement;
    }
  };

  return (
    <>
      <div id='announcements' aria-live='polite' aria-atomic='true' role='status'/>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        change={handlePanelRemove}
        columns={5}
      />
    </>
  );
}
```

## Section 508 Standards

Section 508 Amendment to the Rehabilitation Act requires federal agencies to ensure IT is accessible:

### Technical Standards Compliance

**§ 1194.22 – Web-based Intranet and Internet Information**

```tsx
// Accessible panel with semantic structure
function AccessibleWebDashboard() {
  const panels = [
    {
      id: 'report-panel',
      header: 'Sales Report',
      content: `
        <section aria-label="Sales Report Section">
          <article role="article">
            <h2>Q1 Results</h2>
            <p>Sales exceeded targets by 15%</p>
            <table role="presentation" aria-label="Sales data table">
              <thead>
                <tr>
                  <th>Region</th>
                  <th>Revenue</th>
                  <th>Growth</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>North</td>
                  <td>$50,000</td>
                  <td>+12%</td>
                </tr>
              </tbody>
            </table>
          </article>
        </section>
      `,
      row: 0,
      col: 0,
      sizeX: 3,
      sizeY: 2
    }
  ];

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      enableRtl={false}
    />
  );
}
```

**Color Not Sole Identifier**
- Don't use color alone to convey information
- Use text labels, patterns, or icons

```tsx
// ❌ AVOID: Color-only identification
const colorOnlyPanel = (
  <div style={{ color: 'red' }}>Error status</div>
);

// ✅ RECOMMENDED: Color + Text + Icon
const accessiblePanel = (
  <div style={{ color: 'red' }}>
    <span aria-label="Error">❌</span> Error: Data load failed
  </div>
);
```

## WAI-ARIA Implementation

Dashboard Layout uses WAI-ARIA to enhance semantic meaning:

### Roles

```tsx
// Panel as list item
const ariaRolePanel = (
  <div role='listitem' aria-label='Dashboard panel'>
    {/* Panel content */}
  </div>
);

// Dashboard as list
const ariaDashboard = (
  <div role='list' aria-label='Dashboard panels'>
    {/* Multiple panels with role='listitem' */}
  </div>
);

// Resize handle role
const resizeHandleRole = (
  <div
    role='slider'
    aria-label='Panel resize handle'
    aria-valuemin='0'
    aria-valuemax='5'
    aria-valuenow='2'
  />
);
```

### ARIA Properties

**aria-grabbed** - Indicates draggable state
```tsx
// Draggable panel indication
function DraggablePanel() {
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div
      role='listitem'
      aria-grabbed={isDragging}
      aria-dropeffect='move'
      onMouseDown={() => setIsDragging(true)}
      onMouseUp={() => setIsDragging(false)}
    >
      Panel Content
    </div>
  );
}
```

**aria-label & aria-labelledby**
```tsx
// Explicit labeling
const panels = [
  {
    id: 'sales-panel',
    header: 'Sales Dashboard',
    content: '<div role="region" aria-labelledby="sales-header">Sales data</div>',
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];

// Or using aria-label
<DashboardLayoutComponent
  id='dashboard'
  aria-label='Main dashboard with draggable sales panels'
  panels={panels}
/>
```

**aria-live** - Announce dynamic changes
```tsx
function AccessibleDashboard() {
  return (
    <>
      <div
        id='panel-announcements'
        aria-live='polite'
        aria-atomic='true'
        role='status'
        className='sr-only'
      />
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        change={(args) => {
          const region = document.getElementById('panel-announcements');
          region!.textContent = `Panel ${args.id} ${args.type}`;
        }}
      />
    </>
  );
}
```

**aria-disabled** - Disabled state
```tsx
// Prevent dragging with ARIA
<div
  role='button'
  aria-disabled='true'
  aria-label='Cannot drag this panel'
  className='e-panel disabled'
>
  Locked Panel
</div>
```

## Keyboard Navigation

### Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| Tab | Navigate between panels | General |
| Shift+Tab | Navigate backwards | General |
| Enter | Activate focused panel | Panel header |
| Space | Toggle panel state | Panel header |
| Arrow Keys | Adjust size (resize mode) | Resize handle |
| Escape | Cancel drag/resize | During operation |

### Implementation Example

```tsx
function AccessibleDashboardWithKeyboard() {
  const dashboardRef = useRef<DashboardLayoutComponent>(null);
  const [focusedPanelId, setFocusedPanelId] = useState<string | null>(null);

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      // Cancel ongoing operations
      setFocusedPanelId(null);
    }
    
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      // Adjust panel size
      e.preventDefault();
      const increment = e.key === 'ArrowUp' ? 1 : -1;
      // Update panel dimensions
    }
  };

  return (
    <DashboardLayoutComponent
      ref={dashboardRef}
      id='dashboard'
      panels={panels}
      columns={5}
      tabIndex={0}
      onKeyDown={handleKeyDown}
    />
  );
}
```

### Focus Management

```tsx
function DashboardWithFocusManagement() {
  const firstPanelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Set initial focus on first panel
    firstPanelRef.current?.focus();
  }, []);

  return (
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
      /* First panel receives initial focus */
    />
  );
}
```

## Screen Reader Support

### Semantic HTML Structure

```tsx
// Proper semantic structure
const panels = [
  {
    id: 'main-report',
    header: 'Main Report',
    content: `
      <main role='main' aria-label='Main dashboard report'>
        <section aria-labelledby='report-title'>
          <h2 id='report-title'>Q1 Performance</h2>
          <article>
            <p>Report content with semantic structure</p>
          </article>
        </section>
      </main>
    `,
    row: 0,
    col: 0,
    sizeX: 3,
    sizeY: 2
  }
];
```

### Screen Reader Testing

**Testing Tools:**
- NVDA (Windows) - Free, open source
- JAWS (Windows) - Commercial
- VoiceOver (Mac/iOS) - Built-in
- TalkBack (Android) - Built-in

```tsx
// Test with screen reader announcements
function ScreenReaderTestDashboard() {
  const [message, setMessage] = useState('');

  return (
    <>
      {/* Hidden but announced to screen readers */}
      <div role='status' aria-live='polite' aria-atomic='true'>
        {message}
      </div>

      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        change={(args) => {
          setMessage(`Panel changed: ${args.id}`);
        }}
      />
    </>
  );
}
```

### Alt Text for Images in Panels

```tsx
const panels = [
  {
    id: 'image-panel',
    header: 'Product Image',
    content: `
      <figure>
        <img
          src='product.jpg'
          alt='Premium dashboard widget with blue gradient'
          style='max-width: 100%; height: auto;'
        />
        <figcaption>Product featured in Q1 campaign</figcaption>
      </figure>
    `,
    row: 0,
    col: 0,
    sizeX: 2,
    sizeY: 2
  }
];
```

## RTL Support

Dashboard Layout supports Right-to-Left languages (Arabic, Hebrew, Farsi, etc.):

```tsx
// Enable RTL mode
<DashboardLayoutComponent
  id='dashboard'
  panels={panels}
  columns={5}
  enableRtl={true}
/>
```

### RTL Styling

```css
/* RTL-aware styling */
[dir='rtl'] .e-panel .e-panel-header {
  text-align: right;
  padding-right: 16px;
  padding-left: 12px;
}

[dir='rtl'] .e-panel .e-south-west {
  right: auto;
  left: 0;
}

[dir='rtl'] .e-panel .e-south-east {
  right: auto;
  left: 0;
}
```

### Language-Specific Considerations

```tsx
function MultilingualDashboard() {
  const [language, setLanguage] = useState('en');
  const isRTL = language === 'ar' || language === 'he';

  const panels = [
    {
      id: 'multilingual-panel',
      header: getHeaderText(language),
      content: getContentText(language),
      row: 0,
      col: 0,
      sizeX: 2,
      sizeY: 2
    }
  ];

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'} lang={language}>
      <DashboardLayoutComponent
        id='dashboard'
        panels={panels}
        columns={5}
        enableRtl={isRTL}
      />
    </div>
  );
}
```

## Testing and Validation

### Automated Testing

```tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('Dashboard should not have accessibility violations', async () => {
  const { container } = render(
    <DashboardLayoutComponent
      id='dashboard'
      panels={panels}
      columns={5}
    />
  );

  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- ✅ Tab through all panels - can you navigate all interactive elements?
- ✅ Drag panels with keyboard - Tab to handle, use arrow keys
- ✅ Resize with keyboard - Focus handle, arrow keys adjust size
- ✅ Screen reader testing - Announcement of panel changes
- ✅ Color contrast - Use color contrast analyzer (>4.5:1)
- ✅ Zoom testing - Set zoom to 200%, layout should adapt
- ✅ RTL testing - Switch to RTL mode, verify mirroring
- ✅ Focus visible - Tab through, outline always visible
- ✅ Keyboard traps - Escape should cancel operations
- ✅ Alternative text - Images have descriptive alt text

### Accessibility Audit Tools

- **Axe DevTools** - Browser extension for violations
- **Lighthouse** - Built into Chrome DevTools
- **WAVE** - WebAIM accessibility checker
- **Color Contrast Analyzer** - Contrast verification
- **Screen readers** - NVDA, VoiceOver, JAWS

### WCAG 2.2 Audit Checklist

```markdown
## Critical (Must Fix)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicator always visible (min 2px)
- [ ] Color contrast minimum 4.5:1
- [ ] No keyboard traps
- [ ] Meaningful alt text on images

## Important (Should Fix)
- [ ] Logical tab order
- [ ] ARIA roles correctly implemented
- [ ] Live regions announce changes
- [ ] Error messages clear and actionable
- [ ] Resize handles clearly identifiable

## Nice to Have
- [ ] High contrast mode support
- [ ] Text resize support (up to 200%)
- [ ] Customizable colors
- [ ] Reduced motion support
```

### ARIA Validation

```tsx
// Ensure all required ARIA attributes present
function ValidateAriaCompliance() {
  const requiredAttributes = {
    'role': true,
    'aria-label': true,
    'aria-labelled-by': true,
    'aria-live': true
  };

  const panel = document.querySelector('.e-panel');
  
  Object.keys(requiredAttributes).forEach(attr => {
    if (requiredAttributes[attr]) {
      if (!panel?.hasAttribute(attr)) {
        console.warn(`Missing ${attr} attribute`);
      }
    }
  });
}
```
