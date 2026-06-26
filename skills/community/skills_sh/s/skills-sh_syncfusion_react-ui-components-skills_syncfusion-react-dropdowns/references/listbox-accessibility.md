# Accessibility in React ListBox

## Table of Contents
- [Accessibility Standards](#accessibility-standards)
- [ARIA Attributes](#aria-attributes)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Color and Contrast](#color-and-contrast)
- [RTL Support](#rtl-support)
- [Testing for Accessibility](#testing-for-accessibility)
- [Troubleshooting](#troubleshooting)

---

## Accessibility Standards

The ListBox component is built to comply with major accessibility standards:

| Standard | Support |
|----------|---------|
| WCAG 2.2 AA | ✅ Full Support |
| Section 508 (US) | ✅ Full Support |
| ADA (Americans with Disabilities Act) | ✅ Compliant |
| ARIA 1.2 | ✅ Full Support |
| Screen Readers | ✅ NVDA, JAWS, VoiceOver |
| Keyboard Navigation | ✅ Full Support |
| Color Contrast | ✅ WCAG AA (4.5:1 minimum) |
| Mobile Accessibility | ✅ Touch-friendly |

---

## ARIA Attributes

The ListBox automatically includes proper ARIA attributes. You can enhance them with custom properties:

### ListBox Container

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'React', id: '2' },
    { text: 'Vue', id: '3' }
  ];

  return (
    <ListBoxComponent 
      dataSource={data}
      fields={{ text: 'text', value: 'id' }}
      aria-label="Select a JavaScript framework"
      aria-description="Choose your preferred front-end framework from the list"
    />
  );
}

export default App;
```

### ARIA Attributes Applied Automatically

The component applies these ARIA attributes automatically:

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `role` | `listbox` | Identifies the component as a listbox |
| `aria-label` | Custom text | Provides accessible name |
| `aria-multiselectable` | `true`/`false` | Indicates if multiple selection is allowed |
| `aria-selected` | `true`/`false` | Indicates if item is selected |
| `aria-disabled` | `true`/`false` | Indicates if item is disabled |

---

## Keyboard Navigation

### Default Keyboard Shortcuts

Users can navigate the ListBox without a mouse:

| Key | Action |
|-----|--------|
| **Arrow Up** | Select previous item |
| **Arrow Down** | Select next item |
| **Space** | Toggle selection (multiple mode) |
| **Enter** | Select item (single mode) |
| **Home** | Go to first item |
| **End** | Go to last item |
| **Page Up** | Scroll up one page |
| **Page Down** | Scroll down one page |
| **Shift + Arrow** | Extend selection (multiple mode) |
| **Ctrl + A** | Select all (multiple mode) |

### Keyboard Navigation

Keyboard navigation is enabled by default in the ListBox. No additional configuration is required — users can navigate items using the keyboard shortcuts listed in the table above.

---

## Screen Reader Support

### Label Association

Provide clear labels for screen reader users:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'JavaScript', id: '1' },
    { text: 'TypeScript', id: '2' }
  ];

  return (
    <div>
      <label htmlFor="framework-select">
        Select your preferred framework:
      </label>
      <ListBoxComponent 
        id="framework-select"
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        aria-labelledby="framework-select"
      />
    </div>
  );
}

export default App;
```

### Semantic HTML

Use proper semantic structure:

```tsx
function App() {
  const data = [
    { text: 'Beginner', id: '1' },
    { text: 'Intermediate', id: '2' },
    { text: 'Advanced', id: '3' }
  ];

  return (
    <form>
      <fieldset>
        <legend>Your Experience Level</legend>
        <ListBoxComponent 
          dataSource={data}
          fields={{ text: 'text', value: 'id' }}
        />
      </fieldset>
    </form>
  );
}

export default App;
```

### Test with Screen Reader

Common screen readers:
- **NVDA** (Windows, free)
- **JAWS** (Windows, commercial)
- **VoiceOver** (Mac/iOS, built-in)
- **TalkBack** (Android, built-in)

---

## Color and Contrast

### Sufficient Color Contrast

Ensure text has sufficient contrast:

```css
/* WCAG AA Standard: 4.5:1 minimum for normal text */

/* Good contrast */
.e-listbox .e-list-item {
  color: #1a1a1a;        /* Very dark gray on white = 18.5:1 */
  background-color: #ffffff;
}

/* Selected state - also good contrast */
.e-listbox .e-list-item.e-selected {
  color: #ffffff;        /* White on dark blue = 5.3:1 */
  background-color: #1976d2;
}

/* Avoid: Low contrast */
/* BAD: color: #999999 on #e8e8e8 = 2.1:1 (too low) */
```

### Don't Rely on Color Alone

Add visual indicators beyond color:

```tsx
const itemTemplate = (props) => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      {props.status === 'active' && (
        <>
          <span style={{ color: '#4caf50' }}>●</span>
          <span>(Active)</span>
        </>
      )}
      {props.status === 'inactive' && (
        <>
          <span style={{ color: '#999' }}>●</span>
          <span>(Inactive)</span>
        </>
      )}
      <span>{props.text}</span>
    </div>
  );
}
```

### Dark Mode Support

Ensure contrast in both light and dark modes:

```css
@media (prefers-color-scheme: light) {
  .e-listbox .e-list-item {
    color: #1a1a1a;
    background-color: #ffffff;
  }
}

@media (prefers-color-scheme: dark) {
  .e-listbox .e-list-item {
    color: #ffffff;
    background-color: #2d2d2d;
  }
}
```

---

## RTL Support

### Enable Right-to-Left Layout

For languages like Arabic, Hebrew, Persian:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const data = [
    { text: 'جافا سكريبت', id: '1' },
    { text: 'React', id: '2' },
    { text: 'Vue', id: '3' }
  ];

  return (
    <div dir="rtl" lang="ar">
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
        enableRtl={true}
      />
    </div>
  );
}

export default App;
```

### CSS for RTL

Syncfusion handles most RTL styling, but you can customize:

```css
/* RTL specific styling */
[dir="rtl"] .e-listbox {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .e-listbox .e-list-item {
  text-align: right;
  padding-right: 16px;
  padding-left: 16px;
}
```

---

## Focus Management

### Visible Focus Indicator

Ensure keyboard users can see focus:

```css
.e-listbox .e-list-item:focus {
  outline: 3px solid #1976d2;
  outline-offset: -2px;
}

.e-listbox .e-list-item:focus:not(:focus-visible) {
  outline: none;
}

.e-listbox .e-list-item:focus-visible {
  outline: 3px solid #1976d2;
  outline-offset: -2px;
}
```

### Focus Trap

Keep focus within a modal dialog using a native `onKeyDown` wrapper:

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';
import { useRef } from 'react';

function Modal() {
  const containerRef = useRef();

  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      const focusable = containerRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        last.focus();
        e.preventDefault();
      } else if (!e.shiftKey && document.activeElement === last) {
        first.focus();
        e.preventDefault();
      }
    }
  };

  return (
    <div role="dialog" ref={containerRef} onKeyDown={handleKeyDown}>
      <ListBoxComponent 
        dataSource={data}
        fields={{ text: 'text', value: 'id' }}
      />
    </div>
  );
}

export default Modal;
```

---

## Testing for Accessibility

### Automated Testing

Use accessibility testing tools:

```tsx
// Using axe-core
import { axe, toHaveNoViolations } from 'jest-axe';

test('ListBox should not have accessibility violations', async () => {
  const { container } = render(
    <ListBoxComponent dataSource={data} />
  );
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] Tab navigation works smoothly
- [ ] Focus indicator is visible at all times
- [ ] Text is readable with color alone removed
- [ ] Contrast ratio meets WCAG AA (4.5:1)
- [ ] Screen reader announces correctly
- [ ] Keyboard shortcuts work as expected
- [ ] Zoom to 200% still works
- [ ] RTL mode works (if applicable)
- [ ] All items are reachable by keyboard
- [ ] No keyboard traps

### Browser Testing

Test across browsers and devices:
- Chrome + ChromeVox
- Firefox + NVDA
- Safari + VoiceOver
- Mobile browsers with built-in screen readers

---

## Common Patterns

### Accessible Form with ListBox

```tsx
import { ListBoxComponent } from '@syncfusion/ej2-react-dropdowns';

function App() {
  const [selected, setSelected] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selected) {
      alert('Please select an option');
      return;
    }
    // Submit form
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="skills">Select your skills:</label>
        <ListBoxComponent 
          id="skills"
          dataSource={data}
          selectionSettings={{ mode: 'Multiple' }}
          change={(e) => setSelected(e.value)}
          aria-required="true"
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

export default App;
```

### Accessible Error Feedback

```tsx
function App() {
  const [error, setError] = useState(null);

  const handleValidation = (value) => {
    if (!value) {
      setError('Selection is required');
    } else {
      setError(null);
    }
  };

  return (
    <div>
      <label htmlFor="select">Choose an option:</label>
      <ListBoxComponent 
        id="select"
        dataSource={data}
        change={(e) => handleValidation(e.value)}
        aria-invalid={!!error}
        aria-describedby={error ? 'error-message' : undefined}
      />
      {error && (
        <div id="error-message" role="alert" style={{ color: '#d32f2f' }}>
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
```

---

## Troubleshooting

### Screen reader not announcing items
- Check ARIA roles are correct
- Ensure `aria-label` is provided
- Test with multiple screen readers
- Verify JavaScript is enabled

### Focus indicators not visible
- Check CSS `outline` property isn't removed
- Use `:focus-visible` for better UX
- Ensure sufficient contrast for focus outline
- Test with keyboard navigation

### Keyboard navigation not working
- Keyboard navigation is built-in — no extra prop is required
- Check for JavaScript errors in the console
- Ensure the ListBox has focus (click or Tab to it)
- Test in different browsers

### Color contrast issues
- Use contrast checker: WebAIM Contrast Checker
- Test with color blindness simulator
- Increase font size for better readability
- Add text indicators beyond colors
