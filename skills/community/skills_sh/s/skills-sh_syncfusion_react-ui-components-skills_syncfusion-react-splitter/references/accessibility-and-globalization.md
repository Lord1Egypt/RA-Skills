# Accessibility and Globalization

## Table of Contents
- [WCAG Compliance](#wcag-compliance)
- [Keyboard Navigation](#keyboard-navigation)
- [ARIA Attributes](#aria-attributes)
- [Screen Reader Support](#screen-reader-support)
- [RTL Support](#rtl-support)
- [Internationalization](#internationalization)
- [Focus Management](#focus-management)

## WCAG Compliance

The Splitter component follows WCAG 2.1 Level AA guidelines for accessibility.

### Guidelines Met

**Perceivable:**
- Sufficient color contrast (text vs background)
- Non-color-dependent indicators (icons, text labels)
- Resizable text and components

**Operable:**
- Keyboard accessible (no mouse required)
- Adjustable timing (no time limits)
- Seizure prevention (no flashing)

**Understandable:**
- Clear navigation patterns
- Consistent component behavior
- Error prevention and recovery

**Robust:**
- Valid HTML structure
- ARIA attributes
- Assistive technology compatibility

### Accessibility Properties

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function WCAGCompliantSplitter() {
  return (
    <div role='main' aria-label='Main Content Area'>
      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px' }}
        aria-label='Two-panel layout splitter'
      >
        <PanesDirective>
          <PaneDirective 
            size='250px'
            aria-label='Navigation sidebar'
          >
            <nav style={{ padding: '20px' }}>
              <h2>Navigation</h2>
              <ul role='navigation'>
                <li><a href='#home'>Home</a></li>
                <li><a href='#about'>About</a></li>
                <li><a href='#contact'>Contact</a></li>
              </ul>
            </nav>
          </PaneDirective>

          <PaneDirective 
            size='300px'
            aria-label='Main content area'
          >
            <article style={{ padding: '20px' }}>
              <h2>Content</h2>
              <p>Main article content here</p>
            </article>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default WCAGCompliantSplitter;
```

## Keyboard Navigation

Users can navigate and operate the splitter without a mouse.

### Keyboard Shortcuts

| Key | Action | Notes |
|-----|--------|-------|
| `Tab` | Move focus to splitter | Focuses separator bar |
| `Enter` / `Space` | Toggle collapse (if collapsible) | When separator focused |
| `Arrow Left` | Decrease left pane, increase right | In horizontal layout |
| `Arrow Right` | Increase left pane, decrease right | In horizontal layout |
| `Arrow Up` | Decrease top pane, increase bottom | In vertical layout |
| `Arrow Down` | Increase top pane, decrease bottom | In vertical layout |

### Example: Full Keyboard Navigation

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function KeyboardNavigableSplitter() {
  const splitterRef = React.useRef<SplitterComponent>(null);

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (!splitterRef.current) return;

    // Get current sizes
    const panes = splitterRef.current.panes;
    if (!panes || panes.length < 2) return;

    const leftSize = parseInt(panes[0].size || '0');
    const rightSize = parseInt(panes[1].size || '0');
    const step = 20; // Pixel increment

    switch(event.key) {
      case 'ArrowLeft':
        event.preventDefault();
        panes[0].size = `${Math.max(100, leftSize - step)}px`;
        panes[1].size = `${rightSize + step}px`;
        splitterRef.current.refresh();
        break;

      case 'ArrowRight':
        event.preventDefault();
        panes[0].size = `${leftSize + step}px`;
        panes[1].size = `${Math.max(100, rightSize - step)}px`;
        splitterRef.current.refresh();
        break;
    }
  };

  return (
    <div onKeyDown={handleKeyDown} tabIndex={0}>
      <p><em>Tab to focus, then use Arrow keys to resize</em></p>
      
      <SplitterComponent 
        ref={splitterRef}
        orientation='Horizontal'
        style={{ height: '300px' }}
      >
        <PanesDirective>
          <PaneDirective size='200px'>
            <div style={{ padding: '20px' }}>
              <h3>Left Panel</h3>
            </div>
          </PaneDirective>
          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>Right Panel</h3>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default KeyboardNavigableSplitter;
```

## ARIA Attributes

Use ARIA attributes to provide semantic meaning for assistive technologies.

### Important ARIA Attributes

```tsx
<SplitterComponent
  aria-label='Main layout splitter'
  aria-orientation='horizontal'
  role='separator'
>
  <PanesDirective>
    <PaneDirective 
      size='250px'
      aria-label='Left navigation pane'
      aria-expanded={!isCollapsed}
    >
      {/* Content */}
    </PaneDirective>

    <PaneDirective 
      size='300px'
      aria-label='Main content pane'
      aria-live='polite'
    >
      {/* Content */}
    </PaneDirective>
  </PanesDirective>
</SplitterComponent>
```

### ARIA Property Descriptions

| Attribute | Value | Purpose |
|-----------|-------|---------|
| `aria-label` | string | Human-readable label |
| `aria-orientation` | horizontal/vertical | Layout direction |
| `role` | separator | Component type |
| `aria-expanded` | true/false | Pane collapsed state |
| `aria-live` | polite/assertive | Content changes announcement |
| `aria-controls` | id | Controls relationship |

## Screen Reader Support

Ensure content is announced properly to screen reader users.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function ScreenReaderFriendly() {
  const [expandedPane, setExpandedPane] = React.useState<number | null>(null);

  const handleBeforeCollapse = (args: any) => {
    setExpandedPane(args.paneIndex);
  };

  return (
    <div>
      <h1>Document with Accessible Splitter</h1>
      
      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px' }}
        beforeCollapse={handleBeforeCollapse}
      >
        <PanesDirective>
          <PaneDirective 
            size='250px'
            collapsible={true}
            aria-label='Navigation Panel'
            role='navigation'
          >
            <nav>
              <h2>Navigation</h2>
              <ul>
                <li><a href='#section1'>Section 1</a></li>
                <li><a href='#section2'>Section 2</a></li>
              </ul>
            </nav>
          </PaneDirective>

          <PaneDirective 
            size='300px'
            aria-label='Main Content'
            role='main'
            aria-live='polite'
          >
            <main>
              <h2>Main Content</h2>
              <p>Content updated dynamically</p>
              {expandedPane !== null && (
                <p>Panel {expandedPane} was collapsed</p>
              )}
            </main>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default ScreenReaderFriendly;
```

### Best Practices

1. **Use semantic HTML** - `<nav>`, `<main>`, `<article>`, `<aside>`
2. **Provide clear labels** - Use aria-label for non-obvious components
3. **Announce changes** - Use aria-live for dynamic updates
4. **Maintain headings hierarchy** - H1 → H2 → H3 structure
5. **Link related items** - Use aria-controls for associations

## RTL Support

Enable Right-to-Left language support for Arabic, Hebrew, and other RTL languages.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function RTLSplitter() {
  const [isRTL, setIsRTL] = React.useState(false);

  return (
    <div style={{ direction: isRTL ? 'rtl' : 'ltr' }}>
      <button onClick={() => setIsRTL(!isRTL)}>
        Toggle RTL: {isRTL ? 'Arabic' : 'English'}
      </button>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px', marginTop: '20px' }}
        enableRtl={isRTL}
      >
        <PanesDirective>
          <PaneDirective size='250px'>
            <div style={{ padding: '20px' }}>
              <h3>{isRTL ? 'الشريط الجانبي' : 'Sidebar'}</h3>
              <p>{isRTL ? 'محتوى اللغة العربية' : 'English content'}</p>
            </div>
          </PaneDirective>

          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>{isRTL ? 'المحتوى الرئيسي' : 'Main Content'}</h3>
              <p>{isRTL ? 'يتم عرض هذا النص من اليمين إلى اليسار' : 'Text flows left to right'}</p>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default RTLSplitter;
```

### RTL Features

- Separator position automatically adjusted
- Text alignment reversed
- Icon mirroring (if applicable)
- Navigation direction reversed
- Collapse/expand icons mirrored

## Internationalization

Support multiple languages in the splitter interface.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

const translations = {
  en: {
    sidebar: 'Navigation',
    content: 'Main Content',
    placeholder: 'Select an item'
  },
  es: {
    sidebar: 'Navegación',
    content: 'Contenido Principal',
    placeholder: 'Selecciona un elemento'
  },
  fr: {
    sidebar: 'Navigation',
    content: 'Contenu Principal',
    placeholder: 'Sélectionnez un élément'
  }
};

function InternationalizedSplitter() {
  const [lang, setLang] = React.useState('en');
  const t = translations[lang as keyof typeof translations];

  return (
    <div>
      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        <option value='en'>English</option>
        <option value='es'>Español</option>
        <option value='fr'>Français</option>
      </select>

      <SplitterComponent 
        orientation='Horizontal'
        style={{ height: '400px', marginTop: '10px' }}
        lang={lang}
      >
        <PanesDirective>
          <PaneDirective size='250px'>
            <div style={{ padding: '20px' }}>
              <h3>{t.sidebar}</h3>
              <p>{t.placeholder}</p>
            </div>
          </PaneDirective>

          <PaneDirective size='300px'>
            <div style={{ padding: '20px' }}>
              <h3>{t.content}</h3>
            </div>
          </PaneDirective>
        </PanesDirective>
      </SplitterComponent>
    </div>
  );
}

export default InternationalizedSplitter;
```

## Focus Management

Properly manage focus for keyboard navigation.

```tsx
import { PaneDirective, PanesDirective, SplitterComponent } from '@syncfusion/ej2-react-layouts';
import * as React from 'react';

function FocusManagement() {
  const splitterRef = React.useRef<SplitterComponent>(null);
  const sidebarRef = React.useRef<HTMLDivElement>(null);
  const contentRef = React.useRef<HTMLDivElement>(null);

  const handleFocusNext = () => {
    contentRef.current?.focus();
  };

  const handleFocusPrev = () => {
    sidebarRef.current?.focus();
  };

  return (
    <SplitterComponent 
      ref={splitterRef}
      orientation='Horizontal'
      style={{ height: '400px' }}
    >
      <PanesDirective>
        <PaneDirective size='250px'>
          <div 
            ref={sidebarRef}
            tabIndex={0}
            style={{ padding: '20px', outline: 'none' }}
            onKeyDown={(e) => {
              if (e.key === 'Tab' && !e.shiftKey) {
                e.preventDefault();
                handleFocusNext();
              }
            }}
          >
            <h3>Sidebar</h3>
            <p>Focused element</p>
          </div>
        </PaneDirective>

        <PaneDirective size='300px'>
          <div 
            ref={contentRef}
            tabIndex={0}
            style={{ padding: '20px', outline: 'none' }}
            onKeyDown={(e) => {
              if (e.key === 'Tab' && e.shiftKey) {
                e.preventDefault();
                handleFocusPrev();
              }
            }}
          >
            <h3>Content</h3>
            <p>Tab navigation</p>
          </div>
        </PaneDirective>
      </PanesDirective>
    </SplitterComponent>
  );
}

export default FocusManagement;
```

### Focus Best Practices

1. **Maintain logical tab order** - Use tabIndex appropriately
2. **Show focus indicators** - Visible outline or highlight
3. **Skip links** - Allow jumping to main content
4. **Focus trapping** - Keep focus within modal splitters
5. **Restore focus** - Return focus after collapsing panes

## Checklist for Accessible Splitter

- [ ] ARIA labels provided for all panes
- [ ] Keyboard navigation fully functional
- [ ] Color contrast meets WCAG AA
- [ ] Screen reader tested
- [ ] RTL support enabled
- [ ] Focus management implemented
- [ ] Error messages clear and accessible
- [ ] Sufficient target size (44x44px minimum)
- [ ] Tested with assistive technologies
