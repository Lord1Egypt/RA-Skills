# SplitButton Accessibility

## Table of Contents
- [WCAG 2.1 Compliance](#wcag-21-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [Focus Management](#focus-management)
- [Color Contrast](#color-contrast)
- [Accessible Templates](#accessible-templates)
- [Testing for Accessibility](#testing-for-accessibility)
- [Best Practices](#best-practices)

## WCAG 2.1 Compliance

The SplitButton component is designed to meet WCAG 2.1 Level AA accessibility standards.

### Compliance Checklist

- ✓ Keyboard operable (WCAG 2.1.1 - Level A)
- ✓ Perceivable text labels (WCAG 1.4.3 - Level AA)
- ✓ Sufficient color contrast (WCAG 1.4.11 - Level AA)
- ✓ Focus visibility (WCAG 2.4.7 - Level AA)
- ✓ ARIA support (WCAG 4.1.2 - Level A)
- ✓ Navigation consistency (WCAG 3.2.3 - Level AA)

### WCAG Compliance Example

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function WCAGCompliantButton() {
  const items = [
    { text: 'Save', iconCss: 'e-icons e-save' },
    { text: 'Save As', iconCss: 'e-icons e-save-as' },
    { text: 'Save All', iconCss: 'e-icons e-save-all' }
  ];

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      title="Save options (Keyboard: Alt+S)"
      role="button"
      aria-label="Save document options"
      aria-haspopup="menu"
    >
      Save
    </SplitButtonComponent>
  );
}

export default WCAGCompliantButton;
```

## Keyboard Navigation

Users should be able to fully operate the SplitButton using only a keyboard.

### Keyboard Support

| Key | Action |
|-----|--------|
| `Tab` | Move focus to SplitButton |
| `Space` or `Enter` | Open dropdown menu or trigger primary action |
| `Arrow Down` | Move to next menu item |
| `Arrow Up` | Move to previous menu item |
| `Home` | Move to first menu item |
| `End` | Move to last menu item |
| `Space` or `Enter` | Select focused menu item |
| `Escape` | Close dropdown menu |

### Keyboard Navigation Implementation

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef } from 'react';

function KeyboardAccessibleButton() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      // Open dropdown or trigger primary action
      console.log('Space/Enter pressed');
    }
    
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      // Move to next item
      console.log('Arrow down pressed');
    }
    
    if (e.key === 'Escape') {
      e.preventDefault();
      // Close dropdown
      splitBtnRef.current?.hide();
    }
  };

  const items = [
    { text: 'Save', title: 'Ctrl+S' },
    { text: 'Save As', title: 'Ctrl+Shift+S' }
  ];

  return (
    <div>
      <label htmlFor="save-button">File Actions</label>
      <SplitButtonComponent
        ref={splitBtnRef}
        id="save-button"
        items={items}
        cssClass="e-primary"
        onKeyDown={handleKeyDown}
        tabIndex={0}
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default KeyboardAccessibleButton;
```

### Testing Keyboard Navigation

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function KeyboardNavigationTest() {
  const items = [
    { text: 'Save' },
    { text: 'Save As' },
    { text: 'Save All' }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h2>Keyboard Navigation Test</h2>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        Instructions:
        <ol>
          <li>Press <kbd>Tab</kbd> to focus the button</li>
          <li>Press <kbd>Space</kbd> or <kbd>Enter</kbd> to open dropdown</li>
          <li>Press <kbd>↑</kbd> or <kbd>↓</kbd> to navigate items</li>
          <li>Press <kbd>Enter</kbd> to select</li>
          <li>Press <kbd>Esc</kbd> to close</li>
        </ol>
      </p>
      
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        tabIndex={0}
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default KeyboardNavigationTest;
```

## ARIA Attributes

Use ARIA (Accessible Rich Internet Applications) attributes to communicate component state to assistive technologies.

### Essential ARIA Attributes

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ARIAAttributes() {
  const items = [
    { text: 'Save', id: 'save-item' },
    { text: 'Save As', id: 'save-as-item' },
    { text: 'Save All', id: 'save-all-item' }
  ];

  return (
    <SplitButtonComponent
      id="save-splitbutton"
      items={items}
      cssClass="e-primary"
      role="button"                              // Identifies as button
      aria-label="Save document options"        // Screen reader label
      aria-haspopup="menu"                      // Has dropdown menu
      aria-expanded={false}                     // Menu is initially closed
      aria-controls="save-menu"                 // Links to menu container
      tabIndex={0}                              // Include in tab order
    >
      Save
    </SplitButtonComponent>
  );
}

export default ARIAAttributes;
```

### Dynamic ARIA States

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function DynamicARIA() {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState('');

  const items = [
    { text: 'Option 1' },
    { text: 'Option 2' },
    { text: 'Option 3' }
  ];

  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleSelect = (args: any) => {
    setSelectedItem(args.item.text);
  };

  return (
    <SplitButtonComponent
      items={items}
      cssClass="e-primary"
      role="button"
      aria-label="Choose action"
      aria-haspopup="menu"
      aria-expanded={isOpen}
      aria-activedescendant={selectedItem ? `item-${selectedItem}` : undefined}
      open={handleOpen}
      close={handleClose}
      select={handleSelect}
    >
      Actions
    </SplitButtonComponent>
  );
}

export default DynamicARIA;
```

### ARIA Best Practices

| ARIA Attribute | Purpose | Example |
|---|---|---|
| `role` | Define component role | `role="button"` |
| `aria-label` | Provide accessible name | `aria-label="Save options"` |
| `aria-labelledby` | Link to external label | `aria-labelledby="label-id"` |
| `aria-describedby` | Link to description | `aria-describedby="desc-id"` |
| `aria-haspopup` | Indicate popup menu | `aria-haspopup="menu"` |
| `aria-expanded` | Indicate popup state | `aria-expanded={isOpen}` |
| `aria-disabled` | Indicate disabled state | `aria-disabled={disabled}` |
| `aria-hidden` | Hide decorative elements | `aria-hidden={true}` |

## Screen Reader Support

Ensure SplitButton is properly announced by screen readers like NVDA and JAWS.

### Screen Reader Compatible Structure

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ScreenReaderFriendly() {
  const items = [
    { 
      text: 'Save', 
      iconCss: 'e-icons e-save',
      title: 'Save current document' 
    },
    { 
      text: 'Save As', 
      iconCss: 'e-icons e-save-as',
      title: 'Save with new name' 
    },
    { 
      text: 'Save All', 
      iconCss: 'e-icons e-save-all',
      title: 'Save all open documents' 
    }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div role="menuitem">
        {props.iconCss && (
          <i 
            className={props.iconCss} 
            aria-hidden="true"
            style={{ marginRight: '8px' }}
          />
        )}
        <span>{props.text}</span>
        {props.title && (
          <span className="sr-only">({props.title})</span>
        )}
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
      aria-label="File save options"
      aria-haspopup="menu"
    >
      Save
    </SplitButtonComponent>
  );
}

export default ScreenReaderFriendly;
```

### Screen Reader Testing

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function ScreenReaderTest() {
  const items = [
    { text: 'Print', iconCss: 'e-icons e-print' },
    { text: 'Email', iconCss: 'e-icons e-mail' },
    { text: 'Save', iconCss: 'e-icons e-save' }
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>Screen Reader Test</h1>
      <p>
        Enable your screen reader and navigate with Tab key. 
        The button should announce: "Save document options, menu button"
      </p>
      
      <SplitButtonComponent
        items={items}
        cssClass="e-primary"
        aria-label="Save document options"
        aria-haspopup="menu"
      >
        Save
      </SplitButtonComponent>
    </div>
  );
}

export default ScreenReaderTest;
```

## Focus Management

Proper focus management ensures users can navigate and understand where they are.

### Focus Indicators

```css
/* Ensure visible focus indicator */
.e-split-button:focus,
.e-split-button:focus-visible {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* High contrast focus indicator */
@media (prefers-contrast: more) {
  .e-split-button:focus {
    outline: 3px solid #000;
    outline-offset: 3px;
  }
}
```

### Focus Management Example

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef, useCallback } from 'react';

function FocusManagement() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleFocus = () => {
    console.log('SplitButton focused');
  };

  const handleBlur = () => {
    console.log('SplitButton blurred');
  };

  const handleEscapeKey = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      // Return focus to button after closing menu
      splitBtnRef.current?.element?.focus();
    }
  }, []);

  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  return (
    <div ref={containerRef}>
      <label htmlFor="main-button">Select action:</label>
      <SplitButtonComponent
        ref={splitBtnRef}
        id="main-button"
        items={items}
        cssClass="e-primary"
        onFocus={handleFocus}
        onBlur={handleBlur}
        onKeyDown={handleEscapeKey}
        tabIndex={0}
      >
        Action
      </SplitButtonComponent>
    </div>
  );
}

export default FocusManagement;
```

### Focus Trap in Menu

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useRef } from 'react';

function FocusTrap() {
  const splitBtnRef = useRef<SplitButtonComponent>(null);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab') {
      // Trap focus within open menu
      console.log('Tab pressed - focus trapped within menu');
    }
  };

  const items = [
    { text: 'Option 1' },
    { text: 'Option 2' },
    { text: 'Option 3' }
  ];

  return (
    <SplitButtonComponent
      ref={splitBtnRef}
      items={items}
      cssClass="e-primary"
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      Menu
    </SplitButtonComponent>
  );
}

export default FocusTrap;
```

## Color Contrast

Ensure sufficient color contrast between text and background for visibility.

### Contrast Ratio Requirements

| Level | Minimum Ratio | Example |
|-------|---|---|
| WCAG AA (Normal) | 4.5:1 | Black text on white background |
| WCAG AAA (Normal) | 7:1 | Black text on light gray background |
| WCAG AA (Large) | 3:1 | Large white text on blue background |
| WCAG AAA (Large) | 4.5:1 | Large white text on dark blue background |

### High Contrast Mode

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function HighContrastButton() {
  const items = [{ text: 'Option 1' }, { text: 'Option 2' }];

  // Check for high contrast preference
  const isHighContrast = window.matchMedia('(prefers-contrast: more)').matches;

  return (
    <SplitButtonComponent
      items={items}
      cssClass={isHighContrast ? 'e-highcontrast' : 'e-primary'}
    >
      Button
    </SplitButtonComponent>
  );
}

export default HighContrastButton;
```

### Contrast Validation

```css
/* Verify contrast ratios */

/* ✓ Good: Black text on white (21:1) */
.good-contrast {
  color: #000000;
  background: #ffffff;
}

/* ✓ Good: White text on dark blue (8.6:1) */
.good-contrast-blue {
  color: #ffffff;
  background: #0033cc;
}

/* ✗ Bad: Gray text on light gray (2.1:1) */
.bad-contrast {
  color: #999999;
  background: #f0f0f0;
}
```

## Accessible Templates

Create custom templates that maintain accessibility.

### Accessible Item Template

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';

function AccessibleItemTemplate() {
  const items = [
    { 
      id: 'save',
      text: 'Save',
      icon: '💾',
      description: 'Save to current location'
    },
    { 
      id: 'save-as',
      text: 'Save As',
      icon: '🗂️',
      description: 'Save with new name'
    },
    { 
      id: 'save-all',
      text: 'Save All',
      icon: '📦',
      description: 'Save all open files'
    }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div
        role="menuitem"
        id={`menuitem-${props.id}`}
        aria-label={`${props.text}: ${props.description}`}
      >
        <span aria-hidden="true" style={{ marginRight: '8px' }}>
          {props.icon}
        </span>
        <div>
          <div style={{ fontWeight: 600 }}>{props.text}</div>
          <small style={{ color: '#666' }}>{props.description}</small>
        </div>
      </div>
    );
  };

  return (
    <SplitButtonComponent
      items={items}
      itemTemplate={itemTemplate}
      cssClass="e-primary"
      role="button"
      aria-label="Save options"
      aria-haspopup="menu"
    >
      Save
    </SplitButtonComponent>
  );
}

export default AccessibleItemTemplate;
```

## Testing for Accessibility

### Automated Testing

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('SplitButton Accessibility', () => {
  test('should not have accessibility violations', async () => {
    const { container } = render(
      <SplitButtonComponent
        items={[{ text: 'Option 1' }, { text: 'Option 2' }]}
        cssClass="e-primary"
        aria-label="Test button"
        aria-haspopup="menu"
      >
        Button
      </SplitButtonComponent>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Manual Testing Checklist

- [ ] Keyboard navigation works completely
- [ ] Tab order is logical
- [ ] Focus is visible at all times
- [ ] ARIA labels are descriptive
- [ ] Color contrast meets WCAG AA standards
- [ ] Screen reader announces component correctly
- [ ] Icons have proper aria-hidden or labels
- [ ] Disabled state is properly communicated
- [ ] Menu closes with Escape key
- [ ] Focus returns to button after menu closes

## Best Practices

### Complete Accessible Example

```tsx
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { useState } from 'react';

function AccessibleSplitButton() {
  const [isOpen, setIsOpen] = useState(false);

  const items = [
    { 
      text: 'Save',
      iconCss: 'e-icons e-save',
      title: 'Save current document (Ctrl+S)'
    },
    { 
      text: 'Save As',
      iconCss: 'e-icons e-save-as',
      title: 'Save with new name (Ctrl+Shift+S)'
    },
    { 
      text: 'Save All',
      iconCss: 'e-icons e-save-all',
      title: 'Save all open documents'
    }
  ];

  const itemTemplate = (props: any) => {
    return (
      <div role="menuitem" style={{ display: 'flex', gap: '8px' }}>
        <i 
          className={props.iconCss} 
          aria-hidden="true"
        />
        <div>
          <div>{props.text}</div>
          <small className="sr-only">{props.title}</small>
        </div>
      </div>
    );
  };

  return (
    <section aria-label="File operations">
      <SplitButtonComponent
        items={items}
        itemTemplate={itemTemplate}
        cssClass="e-primary"
        role="button"
        aria-label="Save document - dropdown menu available"
        aria-haspopup="menu"
        aria-expanded={isOpen}
        open={() => setIsOpen(true)}
        close={() => setIsOpen(false)}
        tabIndex={0}
      >
        Save
      </SplitButtonComponent>
    </section>
  );
}

export default AccessibleSplitButton;
```

### Accessibility Rules

1. **Always provide labels** - Use `aria-label` or visual label
2. **Keyboard support** - All functionality accessible via keyboard
3. **Focus management** - Focus always visible and logical
4. **Color not only indicator** - Don't rely on color alone
5. **ARIA when needed** - Use ARIA for complex interactions
6. **Test regularly** - Include accessibility in QA process
7. **Semantic HTML** - Use proper HTML elements and roles

## Next Steps

- **Features** → Read [splitbutton-features.md](splitbutton-features.md) for feature examples
- **Customization** → Read [customization.md](customization.md) for styling
- **Getting Started** → Read [getting-started.md](getting-started.md) for setup
