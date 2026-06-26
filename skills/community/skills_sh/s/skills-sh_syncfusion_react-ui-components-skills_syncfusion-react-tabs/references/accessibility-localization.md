# Accessibility & Localization

## Table of Contents
- [Accessibility Standards](#accessibility-standards)
- [Keyboard Navigation](#keyboard-navigation)
- [Screen Reader Support](#screen-reader-support)
- [Localization Setup](#localization-setup)
- [Language Examples](#language-examples)
- [RTL Support](#rtl-support)

## Accessibility Standards

The Tab component meets comprehensive accessibility requirements:

| Standard | Status | Details |
|----------|--------|---------|
| **WCAG 2.2** | ✓ Full Support | Web Content Accessibility Guidelines Level AA |
| **Section 508** | ✓ Full Support | U.S. Federal accessibility requirement |
| **Screen Readers** | ✓ Full Support | Compatible with JAWS, NVDA, VoiceOver |
| **Keyboard Navigation** | ✓ Full Support | Full keyboard access without mouse |
| **Color Contrast** | ✓ Full Support | Meets WCAG contrast requirements |
| **RTL Languages** | ✓ Full Support | Right-to-left layout support |

## Keyboard Navigation

The Tab component supports full keyboard navigation following WAI-ARIA Tab Pattern standards.

### Keyboard Shortcuts

| Key | Action | Notes |
|-----|--------|-------|
| <kbd>Left Arrow</kbd> | Move to previous tab | First tab has no previous |
| <kbd>Right Arrow</kbd> | Move to next tab | Last tab has no next |
| <kbd>Home</kbd> | Jump to first tab | Useful for long tab lists |
| <kbd>End</kbd> | Jump to last tab | Useful for long tab lists |
| <kbd>Enter</kbd> or <kbd>Space</kbd> | Activate focused tab | Selects tab if not already active |
| <kbd>Tab</kbd> | Move focus to next element | Moves focus away from tabs |
| <kbd>Shift + Tab</kbd> | Move focus to previous element | Moves focus away from tabs |
| <kbd>Escape</kbd> | Close popup (if open) | Only for popup overflow mode |
| <kbd>Shift + F10</kbd> | Open popup | For popup overflow mode |
| <kbd>Delete</kbd> | Delete/close tab | Only if close button enabled |

### Keyboard Navigation Example

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function AccessibleTab() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Keyboard Navigation Example</h1>
      <p>
        Focus on the tab headers and try these keys:
        <ul>
          <li><kbd>←</kbd> / <kbd>→</kbd> - Navigate between tabs</li>
          <li><kbd>Home</kbd> - Jump to first tab</li>
          <li><kbd>End</kbd> - Jump to last tab</li>
          <li><kbd>Enter</kbd> - Activate focused tab</li>
        </ul>
      </p>

      <TabComponent>
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Dashboard' }}
            content="Dashboard content - Use arrow keys to navigate"
          />
          <TabItemDirective 
            header={{ text: 'Analytics' }}
            content="Analytics content"
          />
          <TabItemDirective 
            header={{ text: 'Reports' }}
            content="Reports content"
          />
          <TabItemDirective 
            header={{ text: 'Settings' }}
            content="Settings content"
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Keyboard Focus Management

The Tab component manages focus automatically:

1. Tab header receives focus first
2. Arrow keys navigate between headers
3. Activating tab keeps focus on header
4. Tab key moves focus out of component
5. Shift + Tab moves focus backward

## Screen Reader Support

Screen readers like JAWS, NVDA, and VoiceOver automatically announce:

- **Tab list structure**: "Tablist, 4 tabs"
- **Tab position**: "Tab 2 of 4"
- **Tab state**: "Selected" or "Not selected"
- **Tab content**: Associated panel content
- **Disabled state**: If tab is disabled

### Example: Screen Reader Announcement

```
Screen reader announces:
"Tablist, 4 tabs, horizontal"
"Home tab, selected, currently active tab panel displayed"
"Use arrow keys to navigate between tabs"
```

### Testing Screen Reader Support

1. **Windows NVDA**:
   - Download: https://www.nvaccess.org/
   - Use Num+Plus to start reading
   - Test with Firefox or Chrome

2. **macOS VoiceOver**:
   - Enable: System Preferences > Accessibility > VoiceOver
   - Start reading: VO (Control+Option) + Right Arrow
   - Test with Safari or Chrome

3. **Windows JAWS**:
   - Professional screen reader
   - Works with all major browsers
   - Announces tab structure automatically

## Localization Setup

The Tab component supports localization for close button tooltip text.

### L10n Class Setup

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { L10n } from '@syncfusion/ej2-base';

export default function LocalizedTab() {
  // Set up localization for French
  L10n.load({
    'fr-FR': {
      'tab': {
        'closeButtonTitle': 'Fermer'
      }
    }
  });

  return (
    <TabComponent 
      locale="fr-FR"
      showCloseButton={true}
    >
      <TabItemsDirective>
        <TabItemDirective 
          header={{ text: 'Accueil' }}
          content="Contenu d'accueil"
        />
        <TabItemDirective 
          header={{ text: 'Profil' }}
          content="Contenu du profil"
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### Locale Property

Set tab language using the `locale` property:

```jsx
<TabComponent locale="es-ES">
  {/* Spanish tabs */}
</TabComponent>

<TabComponent locale="de-DE">
  {/* German tabs */}
</TabComponent>

<TabComponent locale="ja-JP">
  {/* Japanese tabs */}
</TabComponent>
```

## Language Examples

### English (default)

```jsx
<TabComponent locale="en-US" showCloseButton={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Home' }} content="Welcome" />
  </TabItemsDirective>
</TabComponent>
```

Close button tooltip: "Close"

### French

```jsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'fr-FR': {
    'tab': {
      'closeButtonTitle': 'Fermer'
    }
  }
});

<TabComponent locale="fr-FR" showCloseButton={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Accueil' }} content="Bienvenue" />
  </TabItemsDirective>
</TabComponent>
```

Close button tooltip: "Fermer" (French for Close)

### Spanish

```jsx
L10n.load({
  'es-ES': {
    'tab': {
      'closeButtonTitle': 'Cerrar'
    }
  }
});

<TabComponent locale="es-ES" showCloseButton={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Inicio' }} content="Bienvenido" />
  </TabItemsDirective>
</TabComponent>
```

### German

```jsx
L10n.load({
  'de-DE': {
    'tab': {
      'closeButtonTitle': 'Schließen'
    }
  }
});

<TabComponent locale="de-DE" showCloseButton={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Startseite' }} content="Willkommen" />
  </TabItemsDirective>
</TabComponent>
```

### Japanese

```jsx
L10n.load({
  'ja-JP': {
    'tab': {
      'closeButtonTitle': '閉じる'
    }
  }
});

<TabComponent locale="ja-JP" showCloseButton={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'ホーム' }} content="ようこそ" />
  </TabItemsDirective>
</TabComponent>
```

## RTL Support

RTL (Right-to-Left) support for languages like Arabic and Hebrew.

### Enable RTL

```jsx
<TabComponent enableRtl={true}>
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'الرئيسية' }} content="محتوى الرئيسية" />
    <TabItemDirective header={{ text: 'الملف الشخصي' }} content="محتوى الملف الشخصي" />
  </TabItemsDirective>
</TabComponent>
```

### RTL with Localization

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { L10n } from '@syncfusion/ej2-base';

export default function ArabicTab() {
  // Set up Arabic localization
  L10n.load({
    'ar-AE': {
      'tab': {
        'closeButtonTitle': 'إغلاق'
      }
    }
  });

  return (
    <TabComponent 
      locale="ar-AE"
      enableRtl={true}
      showCloseButton={true}
    >
      <TabItemsDirective>
        <TabItemDirective 
          header={{ text: 'الرئيسية' }}
          content="محتوى الرئيسية - رحبا بك"
        />
        <TabItemDirective 
          header={{ text: 'الملف الشخصي' }}
          content="معلومات ملفك الشخصي"
        />
        <TabItemDirective 
          header={{ text: 'الإعدادات' }}
          content="إعدادات التطبيق"
        />
      </TabItemsDirective>
    </TabComponent>
  );
}
```

### RTL Layout Changes

When RTL is enabled:

- Tabs appear right-aligned instead of left-aligned
- Navigation arrows reverse direction
- Content flows right-to-left
- Close buttons align to left
- Vertical tabs on right side (instead of left)

## Complete Accessible Example

```jsx
import React from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { L10n } from '@syncfusion/ej2-base';

export default function AccessibleLocalizedTab() {
  // Setup multilingual support
  L10n.load({
    'fr-FR': { 'tab': { 'closeButtonTitle': 'Fermer' } },
    'es-ES': { 'tab': { 'closeButtonTitle': 'Cerrar' } },
    'de-DE': { 'tab': { 'closeButtonTitle': 'Schließen' } }
  });

  const [language, setLanguage] = React.useState('en-US');
  const [rtl, setRtl] = React.useState(false);

  return (
    <div style={{ padding: '20px' }}>
      <h1>Accessible and Localized Tab Component</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <label>
          Language:
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="en-US">English</option>
            <option value="fr-FR">Français</option>
            <option value="es-ES">Español</option>
            <option value="de-DE">Deutsch</option>
          </select>
        </label>
        
        <label style={{ marginLeft: '20px' }}>
          <input 
            type="checkbox" 
            checked={rtl}
            onChange={(e) => setRtl(e.target.checked)}
          />
          Right-to-Left (RTL)
        </label>
      </div>

      <TabComponent 
        locale={language}
        enableRtl={rtl}
        showCloseButton={true}
        aria-label="Content Navigation Tabs"
      >
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: language === 'fr-FR' ? 'Accueil' : 'Home' }}
            content="Welcome content with full accessibility"
          />
          <TabItemDirective 
            header={{ text: language === 'fr-FR' ? 'À propos' : 'About' }}
            content="About us information"
          />
          <TabItemDirective 
            header={{ text: language === 'fr-FR' ? 'Contact' : 'Contact' }}
            content="Contact information"
          />
        </TabItemsDirective>
      </TabComponent>

      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
        <h3>Accessibility Features</h3>
        <ul>
          <li>✓ Full WCAG 2.2 compliance</li>
          <li>✓ ARIA attributes for screen readers</li>
          <li>✓ Keyboard navigation (arrows, Home, End)</li>
          <li>✓ Multiple language support</li>
          <li>✓ RTL language support</li>
          <li>✓ High contrast colors</li>
        </ul>
      </div>
    </div>
  );
}
```

## Testing Accessibility

1. **Keyboard Only**: Use the application without mouse
2. **Screen Reader**: Test with NVDA or similar
3. **Color Contrast**: Check with WebAIM Contrast Checker
4. **Tab Order**: Verify logical navigation flow
5. **Focus Indicators**: Ensure visible focus outline
6. **Language Support**: Test all localized versions
7. **RTL Layout**: Verify right-to-left rendering

## Best Practices

1. **Always provide text labels**: Never rely on icons alone
2. **Test with actual assistive technologies**: Don't assume compliance
3. **Use semantic HTML**: Leverage ARIA roles properly
4. **Maintain keyboard accessibility**: Don't require mouse/touch
5. **Provide language options**: Support international users
6. **Test on real devices**: Mobile keyboard support varies
7. **Color is not the only indicator**: Use icons, text, and styling combinations
