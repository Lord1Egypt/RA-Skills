# Accessibility & Best Practices

## Table of Contents
- [WCAG Compliance](#wcag-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [Focus Management](#focus-management)
- [Color Contrast](#color-contrast)
- [Best Practices](#best-practices)

---

## WCAG Compliance

### WCAG 2.1 Accessibility Levels

The Syncfusion Sidebar component supports WCAG 2.1 Level AA compliance:

- **Level A**: Basic accessibility support
- **Level AA**: Enhanced accessibility (recommended)
- **Level AAA**: Advanced accessibility features

### Accessibility Guidelines

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function AccessibleSidebar() {
  const sidebarRef = useRef(null);

  // WCAG 2.1 compliant implementation
  return (
    <div>
      {/* 1. Semantic HTML */}
      <button
        aria-label="Open navigation menu"
        aria-controls="sidebar"
        onClick={() => sidebarRef.current?.toggle()}
      >
        ☰ Menu
      </button>

      {/* 2. Proper ARIA attributes */}
      <SidebarComponent
        ref={sidebarRef}
        id="sidebar"
        type="Over"
        width="280px"
        role="navigation"
        aria-label="Main Navigation"
      >
        <nav aria-label="Navigation links">
          <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </SidebarComponent>
    </div>
  );
}

export default AccessibleSidebar;
```

---

## Keyboard Navigation

### Standard Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Tab** | Move focus to next focusable element |
| **Shift + Tab** | Move focus to previous focusable element |
| **Enter** | Activate button/link |
| **Space** | Toggle sidebar open/close |
| **Escape** | Close sidebar |
| **Arrow Down** | Move focus to next item in list |
| **Arrow Up** | Move focus to previous item in list |

### Implementation

```jsx
import React, { useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function KeyboardAccessibleSidebar() {
  const sidebarRef = useRef(null);
  const toggleBtnRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (!sidebarRef.current) return;

      // Spacebar or Enter to toggle
      if (event.key === ' ' || event.key === 'Enter') {
        if (document.activeElement === toggleBtnRef.current) {
          event.preventDefault();
          sidebarRef.current.toggle();
        }
      }

      // Escape to close
      if (event.key === 'Escape') {
        if (sidebarRef.current.element.classList.contains('e-open')) {
          sidebarRef.current.hide();
          toggleBtnRef.current?.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div>
      <button
        ref={toggleBtnRef}
        aria-label="Toggle navigation menu"
        aria-controls="sidebar"
        aria-expanded={sidebarRef.current?.element?.classList.contains('e-open') || false}
      >
        ☰ Menu
      </button>

      <SidebarComponent
        ref={sidebarRef}
        id="sidebar"
        type="Over"
        width="280px"
        role="navigation"
      >
        <nav>
          <a href="#home" tabIndex="0">Home</a>
          <a href="#products" tabIndex="0">Products</a>
          <a href="#services" tabIndex="0">Services</a>
        </nav>
      </SidebarComponent>
    </div>
  );
}

export default KeyboardAccessibleSidebar;
```

### Keyboard Focus Trap (Modal Pattern)

When sidebar is open as a modal, keep focus within sidebar:

```jsx
import React, { useRef, useEffect } from 'react';

function FocusTrapSidebar() {
  const sidebarRef = useRef(null);

  useEffect(() => {
    const sidebar = sidebarRef.current?.element;
    if (!sidebar) return;

    const focusableElements = sidebar.querySelectorAll(
      'a, button, input, select, textarea, [tabindex]'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    const handleKeyDown = (e) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        // Shift + Tab on first element -> go to last
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        // Tab on last element -> go to first
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    sidebar.addEventListener('keydown', handleKeyDown);
    return () => sidebar.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      role="dialog"
      aria-modal="true"
    >
      {/* Content */}
    </SidebarComponent>
  );
}

export default FocusTrapSidebar;
```

---

## ARIA Attributes

### Essential ARIA Attributes

```jsx
<SidebarComponent
  // Identifies role
  role="navigation"
  
  // Descriptive label
  aria-label="Main Navigation"
  
  // Related button
  aria-controls="toggle-button"
  
  // Current expanded state
  aria-expanded={isOpen}
  
  // Modal state
  aria-modal="true"
  
  // Hidden from screen readers
  aria-hidden={!isOpen}
/>
```

### Complete ARIA Example

```jsx
import React, { useState, useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function ARIACompliantSidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const sidebarRef = useRef(null);
  const toggleRef = useRef(null);

  const handleChange = (args) => {
    const nowOpen = args.element.classList.contains('e-open');
    setIsOpen(nowOpen);
    
    // Update toggle button aria-expanded
    if (toggleRef.current) {
      toggleRef.current.setAttribute('aria-expanded', nowOpen);
    }
  };

  return (
    <div>
      <button
        ref={toggleRef}
        id="sidebar-toggle"
        aria-label="Open navigation menu"
        aria-controls="main-sidebar"
        aria-expanded={isOpen}
        onClick={() => sidebarRef.current?.toggle()}
      >
        ☰ Menu
      </button>

      <SidebarComponent
        ref={sidebarRef}
        id="main-sidebar"
        role="navigation"
        aria-label="Primary Navigation"
        aria-expanded={isOpen}
        type="Over"
        width="280px"
        change={handleChange}
      >
        <nav aria-label="Menu Items">
          <ul role="menubar">
            <li role="none">
              <a href="#home" role="menuitem">
                Home
              </a>
            </li>
            <li role="none">
              <a href="#products" role="menuitem">
                Products
              </a>
            </li>
            <li role="none">
              <a href="#services" role="menuitem">
                Services
              </a>
            </li>
          </ul>
        </nav>
      </SidebarComponent>
    </div>
  );
}

export default ARIACompliantSidebar;
```

---

## Screen Reader Support

### Screen Reader Friendly Content

```jsx
function ScreenReaderOptimizedSidebar() {
  return (
    <SidebarComponent
      type="Over"
      role="navigation"
      aria-label="Application Navigation"
    >
      {/* Skip link for screen reader users */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <nav>
        <h2 className="sr-only">Navigation Menu</h2>
        <ul>
          <li>
            <a href="#home" aria-current="page">
              Home <span className="sr-only">(current page)</span>
            </a>
          </li>
          <li>
            <a href="#about">About Us</a>
          </li>
          <li>
            <a href="#contact">Contact</a>
          </li>
        </ul>
      </nav>
    </SidebarComponent>
  );
}
```

### CSS for Screen Reader Content

```css
/* Hide visually but keep for screen readers */
.sr-only,
.skip-link {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Make skip link visible on focus */
.skip-link:focus {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  padding: 1rem;
  background-color: #000;
  color: #fff;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
}
```

---

## Focus Management

### Initial Focus

Automatically focus first interactive element when sidebar opens:

```jsx
import React, { useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function FocusManagementSidebar() {
  const sidebarRef = useRef(null);
  const firstLinkRef = useRef(null);

  useEffect(() => {
    const sidebar = sidebarRef.current?.element;
    if (!sidebar) return;

    const handleOpened = () => {
      // Focus first interactive element
      setTimeout(() => {
        firstLinkRef.current?.focus();
      }, 100);
    };

    sidebar.addEventListener('opened', handleOpened);
    return () => sidebar.removeEventListener('opened', handleOpened);
  }, []);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      role="dialog"
      aria-modal="true"
    >
      <nav>
        <a ref={firstLinkRef} href="#home">Home</a>
        <a href="#about">About</a>
      </nav>
    </SidebarComponent>
  );
}

export default FocusManagementSidebar;
```

### Restore Focus on Close

Return focus to trigger button when sidebar closes:

```jsx
function RestoreFocusSidebar() {
  const sidebarRef = useRef(null);
  const toggleRef = useRef(null);

  useEffect(() => {
    const sidebar = sidebarRef.current?.element;
    if (!sidebar) return;

    const handleClosed = () => {
      // Return focus to toggle button
      setTimeout(() => {
        toggleRef.current?.focus();
      }, 100);
    };

    sidebar.addEventListener('closed', handleClosed);
    return () => sidebar.removeEventListener('closed', handleClosed);
  }, []);

  return (
    <>
      <button
        ref={toggleRef}
        onClick={() => sidebarRef.current?.toggle()}
      >
        Menu
      </button>
      <SidebarComponent ref={sidebarRef} type="Over">
        {/* Content */}
      </SidebarComponent>
    </>
  );
}
```

---

## Color Contrast

### WCAG Contrast Ratios

- **Normal text**: Minimum 4.5:1
- **Large text (18pt+)**: Minimum 3:1
- **UI components**: Minimum 3:1

### Compliant Color Scheme

```css
/* Light theme with good contrast */
.accessible-sidebar-light {
  background-color: #ffffff;  /* White */
  color: #333333;             /* Dark gray (contrast ratio 12.63:1) */
}

.accessible-sidebar-light a {
  color: #0056b3;             /* Blue (contrast ratio 8.59:1) */
}

.accessible-sidebar-light a:visited {
  color: #7030a0;             /* Purple (contrast ratio 8.41:1) */
}

/* Dark theme with good contrast */
.accessible-sidebar-dark {
  background-color: #1a1a1a;  /* Very dark gray */
  color: #e0e0e0;             /* Light gray (contrast ratio 12.04:1) */
}

.accessible-sidebar-dark a {
  color: #4a90e2;             /* Light blue (contrast ratio 8.32:1) */
}

.accessible-sidebar-dark a:visited {
  color: #b89ed6;             /* Light purple (contrast ratio 7.99:1) */
}
```

### Check Contrast Tools

- [WebAIM Contrast Checker](url)
- [Accessible Colors Tool](url)

---

## Best Practices

### 1. Semantic HTML

```jsx
<SidebarComponent role="navigation">
  <nav>
    <ul>
      <li><a href="/home">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</SidebarComponent>
```

### 2. Meaningful Labels

```jsx
// Good
<button aria-label="Open navigation menu">☰</button>

// Bad
<button>Menu</button>
```

### 3. Visible Focus Indicators

```css
/* Always provide visible focus state */
a:focus,
button:focus {
  outline: 2px solid #0056b3;
  outline-offset: 2px;
}
```

### 4. Alternative Text

```jsx
<SidebarComponent type="Over">
  <img src="logo.svg" alt="Company Logo" />
  <img src="icon.svg" alt="" aria-hidden="true" /> {/* Decorative */}
</SidebarComponent>
```

### 5. Test with Assistive Technology

```bash
# Screen readers to test with:
# - NVDA (free, Windows)
# - JAWS (commercial, Windows)
# - VoiceOver (built-in, macOS/iOS)
# - TalkBack (built-in, Android)

# Keyboard navigation test:
# - Tab through all elements
# - Use arrow keys in lists
# - Test Escape key
# - Test Enter/Space
```

### 6. Accessibility Checklist

```jsx
function AccessibilityChecklist() {
  const checks = [
    '✓ Semantic HTML (nav, button, etc)',
    '✓ ARIA labels and roles',
    '✓ Keyboard navigation (Tab, Arrow, Escape)',
    '✓ Focus management (visible focus, initial focus)',
    '✓ Screen reader support (alt text, labels)',
    '✓ Color contrast (4.5:1 minimum)',
    '✓ Sufficient touch target size (44x44px)',
    '✓ No keyboard traps',
    '✓ No auto-playing content',
    '✓ Tested with screen readers'
  ];

  return (
    <div>
      <h3>Accessibility Checklist</h3>
      <ul>
        {checks.map((check, i) => <li key={i}>{check}</li>)}
      </ul>
    </div>
  );
}
```

### 7. Complete Accessible Example

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function FullyAccessibleSidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const sidebarRef = useRef(null);
  const toggleRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        sidebarRef.current?.hide();
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  const handleToggle = () => {
    sidebarRef.current?.toggle();
    setIsOpen(!isOpen);
  };

  return (
    <div>
      <header>
        <ButtonComponent
          ref={toggleRef}
          id="sidebar-toggle"
          cssClass="menu-button"
          onClick={handleToggle}
          aria-label="Toggle navigation menu"
          aria-controls="main-sidebar"
          aria-expanded={isOpen}
        >
          ☰ <span>Menu</span>
        </ButtonComponent>
        <h1>Application</h1>
      </header>

      <SidebarComponent
        ref={sidebarRef}
        id="main-sidebar"
        type="Over"
        width="280px"
        role="navigation"
        aria-label="Main Navigation"
        aria-expanded={isOpen}
        change={(args) => {
          const nowOpen = args.element.classList.contains('e-open');
          setIsOpen(nowOpen);
          if (toggleRef.current) {
            toggleRef.current.setAttribute('aria-expanded', nowOpen);
          }
        }}
        showBackdrop={true}
        closeOnDocumentClick={true}
      >
        <nav aria-label="Navigation links">
          <ul role="menubar">
            <li role="none">
              <a href="#home" role="menuitem" tabIndex="0">
                🏠 Home
              </a>
            </li>
            <li role="none">
              <a href="#products" role="menuitem" tabIndex="0">
                📦 Products
              </a>
            </li>
            <li role="none">
              <a href="#contact" role="menuitem" tabIndex="0">
                📧 Contact
              </a>
            </li>
          </ul>
        </nav>
      </SidebarComponent>

      <main id="main-content">
        <h2>Welcome</h2>
        <p>Press ESC to close the sidebar or click outside.</p>
      </main>
    </div>
  );
}

export default FullyAccessibleSidebar;
```

---

**Resources:**
- [WCAG 2.1 Guidelines](url)
- [ARIA Authoring Practices](url)
- [WebAIM](url)
- [Accessible Components](url)
