# Accessibility

## Table of Contents
- [Compliance Standards](#compliance-standards)
- [ARIA Attributes](#aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Color Contrast](#color-contrast)
- [Right-to-Left (RTL) Support](#right-to-left-rtl-support)
- [Mobile Device Accessibility](#mobile-device-accessibility)
- [Accessibility Best Practices Checklist](#accessibility-best-practices-checklist)
- [Accessibility Testing](#accessibility-testing)
- [Resources](#resources)

## Compliance Standards

The Timeline component meets major accessibility standards:

| Standard | Support | Details |
|----------|---------|---------|
| WCAG 2.2 | ✅ Full | Web Content Accessibility Guidelines Level AA compliance |
| Section 508 | ✅ Full | U.S. federal accessibility requirement |
| Right-to-Left (RTL) | ✅ Full | Bidirectional text and layout support |
| Mobile Device Support | ✅ Full | Touch-friendly interactions and responsive design |
| Color Contrast | ✅ Full | WCAG AA minimum contrast ratios (4.5:1 for text) |
| Accessibility Checker | ✅ Validated | Tested with automated accessibility tools |
| Axe-core | ✅ Validated | Automated accessibility testing suite |

## ARIA Attributes

The Timeline component uses WAI-ARIA attributes to communicate semantic meaning to screen readers.

### Navigation Role

```tsx
<TimelineComponent role="navigation">
  <ItemsDirective>
    <ItemDirective content="Event 1" />
    <ItemDirective content="Event 2" />
  </ItemsDirective>
</TimelineComponent>
```

**Role:** `navigation` - Identifies the component as a navigational element.

### ARIA Labels

```tsx
// Add accessible label to container
<div id="timeline-container" role="region" aria-label="Project Timeline">
  <TimelineComponent>
    <ItemsDirective>
      <ItemDirective content="Phase 1" aria-label="Phase 1: Planning" />
      <ItemDirective content="Phase 2" aria-label="Phase 2: Development" />
    </ItemsDirective>
  </TimelineComponent>
</div>
```

**aria-label:** Provides accessible name when visible text isn't clear.

### Semantic HTML

Use semantic HTML to enhance accessibility:

```tsx
<section aria-labelledby="timeline-title">
  <h2 id="timeline-title">Project Milestones</h2>
  
  <TimelineComponent role="list">
    <ItemsDirective>
      <ItemDirective role="listitem" content="Milestone 1" />
      <ItemDirective role="listitem" content="Milestone 2" />
    </ItemsDirective>
  </TimelineComponent>
</section>
```

## Keyboard Navigation

Timeline components support keyboard interaction for users who cannot use a mouse.

### Keyboard Support

- **Tab:** Navigate between timeline items
- **Shift+Tab:** Navigate backwards through items
- **Enter/Space:** Activate interactive elements

### Implementing Keyboard Navigation

```tsx
function AccessibleTimeline() {
  const [focusedIndex, setFocusedIndex] = React.useState(0);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        setFocusedIndex(Math.min(index + 1, 3));
        e.preventDefault();
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        setFocusedIndex(Math.max(index - 1, 0));
        e.preventDefault();
        break;
      case 'Enter':
        handleItemSelect(index);
        break;
    }
  };

  const handleItemSelect = (index: number) => {
    // Handle item selection
  };

  return (
    <div 
      role="list"
      onKeyDown={(e) => handleKeyDown(e, focusedIndex)}
      style={{ height: '330px' }}
    >
      <TimelineComponent>
        <ItemsDirective>
          {['Step 1', 'Step 2', 'Step 3', 'Step 4'].map((item, index) => (
            <ItemDirective 
              key={index}
              content={item}
              role="listitem"
              tabIndex={focusedIndex === index ? 0 : -1}
            />
          ))}
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

## Screen Reader Support

Screen readers rely on semantic HTML and ARIA to convey content structure and meaning.

### Best Practices for Screen Readers

**1. Use semantic headings:**

```tsx
<div>
  <h2>Timeline Title</h2>
  <TimelineComponent>
    <ItemsDirective>
      <ItemDirective content="Event 1" />
    </ItemsDirective>
  </TimelineComponent>
</div>
```

**2. Provide descriptive labels:**

```tsx
<TimelineComponent 
  aria-label="Project development timeline showing planning, design, development, and deployment phases"
>
  <ItemsDirective>
    <ItemDirective 
      content="Planning" 
      aria-describedby="phase1-desc"
    />
    <div id="phase1-desc" style={{ display: 'none' }}>
      Initial project planning and requirements gathering phase
    </div>
  </ItemsDirective>
</TimelineComponent>
```

**3. Ensure meaningful content:**

```tsx
// ✅ Good - Clear, descriptive content
<ItemDirective content="Project approved by stakeholders" oppositeContent="March 15, 2026" />

// ❌ Poor - Vague, unclear meaning
<ItemDirective content="Done" oppositeContent="Date 1" />
```

**4. Test with screen readers:**

- NVDA (Windows, free)
- JAWS (Windows, commercial)
- VoiceOver (macOS, built-in)
- TalkBack (Android, built-in)

## Color Contrast

Ensure sufficient color contrast for readability, especially for users with low vision.

### WCAG AA Requirements

- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text:** Minimum 3:1 contrast ratio

### Checking Contrast

```tsx
// Good contrast examples
const goodContrast = {
  dark: '#000000',        // Black on white = 21:1 ✅
  blue: '#0066cc',        // Blue on white = 8.6:1 ✅
  gray: '#666666',        // Gray on white = 7:1 ✅
};

// Poor contrast (avoid)
const poorContrast = {
  light: '#cccccc',       // Light gray on white = 1.8:1 ❌
  tan: '#e8dcc8',         // Tan on white = 2:1 ❌
};
```

### Implementing Good Contrast

```tsx
<TimelineComponent 
  cssClass='high-contrast-theme'
  style={{ backgroundColor: '#ffffff' }}
>
  <ItemsDirective>
    <ItemDirective 
      content="Important Event"
      cssClass="text-dark"
      style={{ color: '#000000' }}
    />
  </ItemsDirective>
</TimelineComponent>
```

**CSS for contrast:**

```css
.high-contrast-theme .e-timeline-dot {
  background-color: #000000;
  border-color: #000000;
}

.high-contrast-theme .text-dark {
  color: #000000;
  background-color: #ffffff;
}

.high-contrast-theme .e-timeline-connector {
  border-color: #000000;
}
```

## Right-to-Left (RTL) Support

Timeline automatically reverses layout for right-to-left languages like Arabic, Hebrew, and Urdu.

### Enabling RTL

```tsx
// Set HTML direction
<html dir="rtl" lang="ar">
  <TimelineComponent>
    <ItemsDirective>
      <ItemDirective content="الحدث الأول" />
      <ItemDirective content="الحدث الثاني" />
    </ItemsDirective>
  </TimelineComponent>
</html>
```

Or via CSS:

```css
body {
  direction: rtl;
  text-align: right;
}
```

### RTL Considerations

- Timeline flows right-to-left automatically
- Content alignment reverses appropriately
- Alignment modes adapt (Before becomes After, etc.)
- Text directionality is preserved

```tsx
// RTL automatically handled
<TimelineComponent orientation='Vertical' align='Before'>
  {/* In RTL context, this renders with appropriate direction */}
</TimelineComponent>
```

## Mobile Device Accessibility

Timeline supports accessible touch interactions and responsive layouts for mobile devices.

### Touch-Friendly Design

```tsx
function MobileAccessibleTimeline() {
  return (
    <div 
      style={{ 
        height: '100vh',
        padding: '10px'
      }}
    >
      <TimelineComponent 
        orientation='Vertical'
        align='Before'
        cssClass='mobile-timeline'
      >
        <ItemsDirective>
          <ItemDirective 
            content="Milestone 1"
            oppositeContent="March 2026"
            style={{ minHeight: '60px' }} // Touch-friendly size
          />
          <ItemDirective 
            content="Milestone 2"
            oppositeContent="April 2026"
            style={{ minHeight: '60px' }}
          />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

**CSS for mobile:**

```css
@media (max-width: 768px) {
  .mobile-timeline .e-timeline-item {
    min-height: 60px;
  }

  .mobile-timeline .e-timeline-dot {
    --dot-size: 18px;
  }

  .mobile-timeline .e-timeline-content {
    font-size: 16px;
  }
}
```

### Responsive Text Sizing

```css
/* Readable font sizes on all devices */
.e-timeline-content {
  font-size: clamp(14px, 2vw, 16px);
}

.e-timeline-item {
  padding: clamp(8px, 2vw, 16px);
}
```

## Accessibility Best Practices Checklist

- [ ] Use semantic HTML (`<section>`, `<h2>`, `<article>`)
- [ ] Provide `aria-label` for container or list
- [ ] Ensure text contrast meets WCAG AA (4.5:1 minimum)
- [ ] Support keyboard navigation (Tab, Arrow keys)
- [ ] Test with screen readers (NVDA, JAWS, VoiceOver)
- [ ] Use meaningful, descriptive content
- [ ] Ensure color isn't the only differentiator
- [ ] Include alt text for images in dots
- [ ] Support RTL languages if applicable
- [ ] Test on mobile devices
- [ ] Provide visible focus indicators
- [ ] Use `disabled` state for unavailable items

## Accessibility Testing

### Automated Testing

Use accessibility testing tools to validate compliance:

```bash
# Install Axe-core
npm install --save-dev axe-core

# Install Accessibility Checker
npm install --save-dev accessibility-checker
```

### Manual Testing

1. **Keyboard navigation:** Navigate using only Tab, Shift+Tab, and Arrow keys
2. **Screen reader:** Test with NVDA, JAWS, or VoiceOver
3. **Color contrast:** Verify contrast ratios with tools like WebAIM
4. **Zoom:** Test at 200% zoom level
5. **Responsive:** Test on mobile and tablet sizes
6. **Focus:** Verify visible focus indicators on all interactive elements

### Example Test Case

```tsx
// Test component with accessibility features
function AccessibleTimelineTest() {
  return (
    <div 
      role="region" 
      aria-label="Project Timeline"
      style={{ height: '400px' }}
    >
      <h2 id="timeline-title">Development Phases</h2>
      
      <TimelineComponent 
        role="list"
        aria-describedby="timeline-title"
      >
        <ItemsDirective>
          <ItemDirective 
            role="listitem"
            content="Planning"
            oppositeContent="Week 1"
            aria-label="Planning phase: Week 1"
          />
          <ItemDirective 
            role="listitem"
            content="Development"
            oppositeContent="Weeks 2-4"
            aria-label="Development phase: Weeks 2 to 4"
          />
        </ItemsDirective>
      </TimelineComponent>
    </div>
  );
}
```

## Resources

- [WCAG 2.2 Guidelines](url)
- [Section 508 Compliance](url)
- [WAI-ARIA Authoring Practices](url)
- [WebAIM Contrast Checker](url)
- [NVDA Screen Reader](url)
