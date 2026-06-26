# Accessibility and Localization

## Table of Contents

- [Accessibility](#accessibility)
- [Localization](#localization)
- [Best Practices](#best-practices)
- [Advanced Patterns](#advanced-patterns)

## Accessibility

### WCAG Compliance

Image Editor supports WCAG 2.1 Level AA standards:

```tsx
const imageEditor = (
  <ImageEditorComponent
    // Accessibility built-in
    ariaLabel="Image editing workspace"
    role="application"
  />
);
```

### Keyboard Navigation

#### Default Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Navigate controls |
| Shift+Tab | Reverse navigation |
| Enter | Confirm action |
| Escape | Close dialog |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Ctrl+O | Open |
| Ctrl+S | Save |
| Delete | Remove selected |
| Arrow Keys | Move annotations |

### Custom Keyboard Shortcuts

```tsx
const handleKeyDown = (e: KeyboardEvent): void => {
  if (e.altKey) {
    switch (e.key) {
      case 'c':
        e.preventDefault();
        imgObj.crop();
        break;
      case 't':
        e.preventDefault();
        openTextDialog();
        break;
      case 'r':
        e.preventDefault();
        imgObj.rotate(90);
        break;
      case 'f':
        e.preventDefault();
        imgObj.flip('Horizontal');
        break;
    }
  }
};

document.addEventListener('keydown', handleKeyDown);
```

### Screen Reader Support

```tsx
function announceAction(message: string): void {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  announcement.textContent = message;
  
  document.body.appendChild(announcement);
  
  setTimeout(() => announcement.remove(), 3000);
}

// Usage
const handleCrop = (): void => {
  imgObj.crop();
  announceAction('Image cropped successfully');
};
```

### Semantic HTML

```tsx
const ImageEditorContainer = (): JSX.Element => {
  return (
    <article className="image-editor-container">
      <header>
        <h1>Image Editor</h1>
        <p>Edit and enhance your images</p>
      </header>
      
      <main>
        <ImageEditorComponent />
      </main>
      
      <footer>
        <p>Status: Ready</p>
      </footer>
    </article>
  );
};
```

### Color Contrast

```tsx
const accessibleTheme = {
  buttonBackground: '#0056B3',
  buttonText: '#FFFFFF',
  tooltipBackground: '#333333',
  tooltipText: '#FFFFFF',
  borderColor: '#000000'
};

const imageEditor = (
  <ImageEditorComponent
    theme={accessibleTheme}
  />
);
```

## Localization

### Supported Locales

The Image Editor supports 120+ locales. Common ones:

```tsx
// English (default)
<ImageEditorComponent />

// Español
<ImageEditorComponent locale="es" />

// Français
<ImageEditorComponent locale="fr" />

// Deutsch
<ImageEditorComponent locale="de" />

// 日本語
<ImageEditorComponent locale="ja" />

// 中文
<ImageEditorComponent locale="zh" />

// हिन्दी
<ImageEditorComponent locale="hi" />
```

### Locale-Specific Setup

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Register custom locale
L10n.load({
  'es': {
    'imageeditor': {
      'Open': 'Abrir',
      'Save': 'Guardar',
      'Undo': 'Deshacer',
      'Redo': 'Rehacer',
      'Crop': 'Recortar',
      'Rotate': 'Girar',
      'Text': 'Texto',
      'Filters': 'Filtros'
    }
  }
});

const imageEditor = (
  <ImageEditorComponent locale="es" />
);
```

### Custom Localization

```tsx
interface LocalizationStrings {
  [locale: string]: {
    [key: string]: string;
  };
}

const customLocales: LocalizationStrings = {
  'en': {
    'Open': 'Open Image',
    'Save': 'Save Image',
    'Crop': 'Crop Selection',
    'Rotate': 'Rotate Image'
  },
  'es': {
    'Open': 'Abrir Imagen',
    'Save': 'Guardar Imagen',
    'Crop': 'Recortar Selección',
    'Rotate': 'Girar Imagen'
  },
  'fr': {
    'Open': 'Ouvrir Image',
    'Save': 'Enregistrer Image',
    'Crop': 'Recadrer Sélection',
    'Rotate': 'Tourner Image'
  }
};

L10n.load(customLocales);

const imageEditor = (
  <ImageEditorComponent locale="fr" />
);
```

### RTL (Right-to-Left) Support

```tsx
// Hebrew
<ImageEditorComponent locale="he" enableRtl={true} />

// Arabic
<ImageEditorComponent locale="ar" enableRtl={true} />

// Urdu
<ImageEditorComponent locale="ur" enableRtl={true} />
```

## Best Practices

### Multi-Language UI

```tsx
const LanguageSelector = (): JSX.Element => {
  const [language, setLanguage] = useState('en');
  
  return (
    <>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
        <option value="ja">日本語</option>
        <option value="zh">中文</option>
      </select>
      
      <ImageEditorComponent locale={language} />
    </>
  );
};
```

### Accessible Tooltips

```tsx
function createAccessibleTooltip(text: string, target: HTMLElement): void {
  const tooltip = document.createElement('div');
  tooltip.setAttribute('role', 'tooltip');
  tooltip.setAttribute('aria-label', text);
  tooltip.className = 'accessible-tooltip';
  tooltip.textContent = text;
  
  target.addEventListener('mouseenter', () => {
    target.parentElement?.appendChild(tooltip);
  });
  
  target.addEventListener('mouseleave', () => {
    tooltip.remove();
  });
}
```

### Language-Aware Date/Time

```tsx
interface LocalDateTimeOptions {
  locale: string;
}

function formatDateTime(date: Date, options: LocalDateTimeOptions): string {
  return date.toLocaleString(options.locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

// Usage
console.log(formatDateTime(new Date(), { locale: 'es' }));
// Output: "15 de enero de 2024, 14:30"
```

## Advanced Patterns

### Dynamic Localization

```tsx
class LocalizationManager {
  private currentLocale: string = 'en';
  private locales: LocalizationStrings = {};
  
  setLocale(locale: string): void {
    this.currentLocale = locale;
    this.applyLocale();
  }
  
  private applyLocale(): void {
    L10n.load(this.locales);
    // Trigger UI update
    window.location.reload();
  }
  
  registerLocale(locale: string, strings: Record<string, string>): void {
    this.locales[locale] = strings;
  }
  
  getTranslation(key: string): string {
    return this.locales[this.currentLocale]?.[key] ?? key;
  }
}

const localizationManager = new LocalizationManager();
```

### Detect User Locale

```tsx
function detectUserLocale(): string {
  // Check browser language
  const browserLang = navigator.language.split('-')[0];
  
  // Supported locales
  const supportedLocales = ['en', 'es', 'fr', 'de', 'ja', 'zh', 'hi'];
  
  // Return supported locale or default to English
  return supportedLocales.includes(browserLang) ? browserLang : 'en';
}

const userLocale = detectUserLocale();
const imageEditor = (
  <ImageEditorComponent locale={userLocale} />
);
```

### Accessibility Audit

```tsx
class AccessibilityAudit {
  checkKeyboardNavigation(): boolean {
    // Verify all controls are keyboard accessible
    return document.querySelectorAll('[tabindex="-1"]').length === 0;
  }
  
  checkContrast(): boolean {
    // Verify sufficient color contrast
    const elements = document.querySelectorAll('button, [role="button"]');
    // Implementation would check computed styles
    return elements.length > 0;
  }
  
  checkAriaLabels(): boolean {
    // Verify all interactive elements have labels
    const interactive = document.querySelectorAll('button, [role="button"], input');
    let labeled = 0;
    
    interactive.forEach(element => {
      if (element.getAttribute('aria-label') || 
          element.getAttribute('aria-labelledby') ||
          element.textContent?.trim()) {
        labeled++;
      }
    });
    
    return labeled === interactive.length;
  }
  
  runFullAudit(): void {
    console.log({
      keyboardNavigation: this.checkKeyboardNavigation(),
      colorContrast: this.checkContrast(),
      ariaLabels: this.checkAriaLabels()
    });
  }
}

const audit = new AccessibilityAudit();
audit.runFullAudit();
```

### Language-Specific Features

```tsx
interface LanguageFeatures {
  locale: string;
  dateFormat: string;
  timeFormat: string;
  currencySymbol: string;
  numberSeparator: string;
}

const languageFeatures: Record<string, LanguageFeatures> = {
  'en': {
    locale: 'en-US',
    dateFormat: 'MM/DD/YYYY',
    timeFormat: '12-hour',
    currencySymbol: '$',
    numberSeparator: ','
  },
  'de': {
    locale: 'de-DE',
    dateFormat: 'DD.MM.YYYY',
    timeFormat: '24-hour',
    currencySymbol: '€',
    numberSeparator: '.'
  },
  'ja': {
    locale: 'ja-JP',
    dateFormat: 'YYYY年MM月DD日',
    timeFormat: '24-hour',
    currencySymbol: '¥',
    numberSeparator: ','
  }
};

function getLanguageFeatures(locale: string): LanguageFeatures {
  return languageFeatures[locale] || languageFeatures['en'];
}
```

### Focus Management

```tsx
class AccessibleFocusManager {
  private focusableElements: HTMLElement[] = [];
  
  initialize(): void {
    const selector = 'button, [href], input, [tabindex]:not([tabindex="-1"])';
    this.focusableElements = Array.from(document.querySelectorAll(selector));
  }
  
  focusFirst(): void {
    this.focusableElements[0]?.focus();
  }
  
  focusNext(current: HTMLElement): void {
    const index = this.focusableElements.indexOf(current);
    if (index < this.focusableElements.length - 1) {
      this.focusableElements[index + 1]?.focus();
    }
  }
  
  focusPrevious(current: HTMLElement): void {
    const index = this.focusableElements.indexOf(current);
    if (index > 0) {
      this.focusableElements[index - 1]?.focus();
    }
  }
}

const focusManager = new AccessibleFocusManager();
focusManager.initialize();
```
