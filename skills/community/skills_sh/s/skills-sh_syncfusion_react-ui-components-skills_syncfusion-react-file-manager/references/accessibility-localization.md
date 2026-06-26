# Accessibility and Localization

Ensure WCAG compliance, keyboard navigation, and support for 50+ languages with RTL layouts.

## Table of Contents

1. [Keyboard Navigation](#keyboard-navigation)
2. [Screen Reader Support](#screen-reader-support)
3. [Internationalization (i18n)](#internationalization-i18n)
4. [Right-to-Left (RTL) Layout](#right-to-left-rtl-layout)
5. [Complete Example](#complete-example)

## Keyboard Navigation

### Built-in Keyboard Shortcuts

File Manager supports standard keyboard shortcuts:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function AccessibleFileManager() {
  return (
    <FileManagerComponent
      allowMultiSelection={true}
      ajaxSettings={{
        url: "url",
        getImageUrl: "url",
        uploadUrl: "url",
        downloadUrl: "url"
      }}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default AccessibleFileManager;
```

**Keyboard Shortcuts:**
- `Arrow Up/Down` - Navigate files
- `Arrow Left/Right` - Expand/collapse folders
- `Space` - Toggle file selection
- `Ctrl+A` - Select all
- `Ctrl+C` - Copy
- `Ctrl+X` - Cut
- `Ctrl+V` - Paste
- `Delete` - Delete selected
- `Enter` - Open file/folder
- `F2` - Rename
- `Tab` - Focus navigation

### Manage Focus

```tsx
const handleFileSelection = (args) => {
  // Focus indicator automatically shown on keyboard navigation
  console.log('File selected:', args.fileDetails);
};

<FileManagerComponent
  fileSelect={handleFileSelection}
  ajaxSettings={{...}}
  allowMultiSelection={true}
>
  <Inject services={[DetailsView, NavigationPane, Toolbar]} />
</FileManagerComponent>
```

## Screen Reader Support

### ARIA Attributes

File Manager automatically includes ARIA attributes:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function ScreenReaderAccessible() {
  return (
    <div role="application" aria-label="File Manager">
      <FileManagerComponent
        ajaxSettings={{...}}
        cssClass="accessible-fm"
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default ScreenReaderAccessible;
```

**ARIA Support Includes:**
- `role="application"` on main container
- `aria-label` on component sections
- `aria-selected` on file items
- `aria-expanded` on folder items
- `aria-disabled` on disabled buttons
- Alt text on icons and images

### Test with Screen Reader

```tsx
import React, { useRef } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function ScreenReaderTest() {
  const fileManagerRef = useRef(null);

  const handleCreated = () => {
    console.log('File Manager created - ready for screen readers');
    
    // Announce to screen reader
    const ariaLive = document.querySelector('[aria-live="polite"]');
    if (ariaLive) {
      ariaLive.textContent = 'File Manager loaded. Use arrow keys to navigate.';
    }
  };

  return (
    <>
      <div aria-live="polite" aria-atomic="true" className="sr-only"></div>
      <FileManagerComponent
        ref={fileManagerRef}
        created={handleCreated}
        ajaxSettings={{...}}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </>
  );
}

export default ScreenReaderTest;
```

## Internationalization (i18n)

### Supported Locales

File Manager supports 50+ languages:

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function LocalizedFileManager() {
  return (
    <FileManagerComponent
      locale="es" // Spanish
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default LocalizedFileManager;
```

**Supported Languages:**
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)
- Vietnamese (vi)
- Thai (th)
- Polish (pl)
- Dutch (nl)
- Swedish (sv)
- And 32+ more...

### Dynamic Locale Switching

```tsx
import React, { useState } from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

function DynamicLocale() {
  const [locale, setLocale] = useState('en');

  return (
    <>
      <select onChange={(e) => setLocale(e.target.value)} value={locale}>
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        <option value="de">German</option>
        <option value="ja">Japanese</option>
        <option value="ar">Arabic</option>
      </select>

      <FileManagerComponent
        locale={locale}
        ajaxSettings={{...}}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </>
  );
}

export default DynamicLocale;
```

### Custom Localization

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Register custom localization
L10n.load({
  'es': {
    'filemanager': {
      'NewFolder': 'Carpeta Nueva',
      'Upload': 'Subir',
      'Delete': 'Eliminar',
      'Rename': 'Renombrar',
      'Download': 'Descargar',
      'Cut': 'Cortar',
      'Copy': 'Copiar',
      'Paste': 'Pegar',
      'Details': 'Detalles',
      'GridView': 'Vista de Cuadrícula'
    }
  }
});

function CustomLocalizedFileManager() {
  return (
    <FileManagerComponent
      locale="es"
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default CustomLocalizedFileManager;
```

## Right-to-Left (RTL) Layout

### Enable RTL

```tsx
import React from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';

function RTLFileManager() {
  return (
    <FileManagerComponent
      enableRtl={true}
      locale="ar" // Arabic
      ajaxSettings={{...}}
    >
      <Inject services={[DetailsView, NavigationPane, Toolbar]} />
    </FileManagerComponent>
  );
}

export default RTLFileManager;
```

### RTL with Custom Styling

```tsx
import React from 'react';
import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';
import './rtl-styles.css';

function RTLCustom() {
  return (
    <div dir="rtl">
      <FileManagerComponent
        enableRtl={true}
        locale="ar"
        cssClass="rtl-file-manager"
        ajaxSettings={{...}}
      >
        <Inject services={[DetailsView, NavigationPane, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
}

export default RTLCustom;
```

**CSS for RTL:**

```css
/* rtl-styles.css */
.rtl-file-manager {
  direction: rtl;
}

.rtl-file-manager .e-toolbar {
  direction: rtl;
  text-align: right;
}

.rtl-file-manager .e-navigationpane {
  border-left: 1px solid #d3d3d3;
  border-right: none;
}
```

## Complete Example

```tsx
import React, { useState } from 'react';
import { FileManagerComponent, Inject, DetailsView, NavigationPane, Toolbar } from '@syncfusion/ej2-react-filemanager';
import { L10n } from '@syncfusion/ej2-base';
import '@syncfusion/ej2-react-filemanager/styles/material.css';

// Register custom translations
L10n.load({
  'es': {
    'filemanager': {
      'NewFolder': 'Nueva Carpeta',
      'Upload': 'Subir Archivo',
      'Delete': 'Eliminar',
      'Rename': 'Renombrar'
    }
  },
  'ar': {
    'filemanager': {
      'NewFolder': 'مجلد جديد',
      'Upload': 'تحميل',
      'Delete': 'حذف',
      'Rename': 'إعادة تسمية'
    }
  }
});

function AccessibleAndLocalizedFileManager() {
  const [locale, setLocale] = useState('en');
  const [enableRtl, setEnableRtl] = useState(false);

  const handleLocaleChange = (newLocale) => {
    setLocale(newLocale);
    setEnableRtl(newLocale === 'ar');
  };

  return (
    <div>
      <select onChange={(e) => handleLocaleChange(e.target.value)} value={locale}>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="ar">العربية</option>
        <option value="fr">Français</option>
        <option value="de">Deutsch</option>
      </select>

      <div dir={enableRtl ? 'rtl' : 'ltr'}>
        <FileManagerComponent
          locale={locale}
          enableRtl={enableRtl}
          allowMultiSelection={true}
          created={() => {
            // Announce to screen reader
            const ariaLive = document.querySelector('[aria-live]');
            if (ariaLive) {
              ariaLive.textContent = `File Manager loaded in ${locale} locale`;
            }
          }}
          ajaxSettings={{
            url: "url",
            getImageUrl: "url",
            uploadUrl: "url",
            downloadUrl: "url"
          }}
          height="700px"
        >
          <Inject services={[DetailsView, NavigationPane, Toolbar]} />
        </FileManagerComponent>
      </div>

      <div aria-live="polite" aria-atomic="true" className="sr-only"></div>
    </div>
  );
}

export default AccessibleAndLocalizedFileManager;
```

## WCAG Compliance

### Checklist

- ✅ Keyboard accessible (arrow keys, space, enter)
- ✅ Screen reader compatible (ARIA labels)
- ✅ Focus indicators visible
- ✅ Color contrast >= 4.5:1
- ✅ Localization support (50+ languages)
- ✅ RTL layout support
- ✅ Responsive design

### Testing

```tsx
// Test keyboard navigation
const testKeyboardNavigation = () => {
  // Arrow keys should navigate files
  // Tab should move focus between sections
  // Enter should open/select
  console.log('Test keyboard navigation manually');
};

// Test screen reader
const testScreenReader = () => {
  // Use NVDA (Windows), JAWS, or VoiceOver (Mac)
  // Verify all UI elements are announced
  console.log('Test with screen reader');
};

// Test color contrast
const testColorContrast = () => {
  // Use WCAG color contrast analyzer
  console.log('Verify 4.5:1 ratio for text');
};
```

## Common Patterns

### Language Selector

```tsx
const languages = [
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Español' },
  { code: 'fr', label: 'Français' },
  { code: 'de', label: 'Deutsch' },
  { code: 'ar', label: 'العربية' }
];

<select onChange={(e) => setLocale(e.target.value)}>
  {languages.map(lang => (
    <option key={lang.code} value={lang.code}>{lang.label}</option>
  ))}
</select>
```

### Accessibility Announcements

```tsx
const announce = (message) => {
  const ariaLive = document.querySelector('[aria-live="polite"]');
  if (ariaLive) {
    ariaLive.textContent = message;
  }
};

const handleFileOpen = (args) => {
  announce(`Opened: ${args.fileDetails[0].name}`);
};
```

## Next Steps

- **Views:** UI configuration in [views-and-navigation.md](views-and-navigation.md)
- **Advanced:** Performance in [advanced-features.md](advanced-features.md)
- **Getting Started:** Installation in [getting-started.md](getting-started.md)
