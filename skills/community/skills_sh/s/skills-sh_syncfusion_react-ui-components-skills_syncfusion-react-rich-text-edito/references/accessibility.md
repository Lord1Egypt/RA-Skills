# Accessibility & Globalization in Syncfusion React Rich Text Editor

## Table of Contents
- [WCAG Compliance](#wcag-compliance)
- [Keyboard Support](#keyboard-support)
- [Globalization and Localization](#globalization-and-localization)
- [RTL Support](#rtl-support)
- [Style Encapsulation](#style-encapsulation)

## WCAG Compliance

The Syncfusion RTE follows WAI-ARIA 1.2 and WCAG 2.1 Level AA accessibility standards:
- Proper ARIA roles (`role="textbox"`, `aria-label`, `aria-multiline`)
- Focus management: keyboard users can navigate the toolbar and editor content
- Color contrast ratios meet WCAG AA requirements in all built-in themes
- Screen reader compatible — tested with NVDA, JAWS, and VoiceOver

No additional configuration is required for basic WCAG compliance.

## Keyboard Support

The RTE provides comprehensive keyboard shortcuts for formatting and navigation.

### Content Formatting Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + B` | Toggle bold |
| `Ctrl + I` | Toggle italic |
| `Ctrl + U` | Toggle underline |
| `Ctrl + Shift + S` | Toggle strikethrough |
| `Ctrl + \` | Clear formatting |
| `Ctrl + L` | Align left |
| `Ctrl + E` | Align center |
| `Ctrl + R` | Align right |
| `Ctrl + J` | Justify |

### Editor Navigation

| Shortcut | Action |
|---|---|
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + A` | Select all |
| `Ctrl + K` | Insert/edit hyperlink |
| `F10` | Focus toolbar |
| `Escape` | Exit toolbar focus, return to content |
| `Tab` | Move to next toolbar item |
| `Shift + Tab` | Move to previous toolbar item |

### Customizing Keyboard Shortcuts

Override default shortcuts or add new ones via `formatter`:

```tsx
import { IHtmlFormatterModel } from '@syncfusion/ej2-react-richtexteditor';

const customShortcut = {
  keyConfig: {
    bold: 'ctrl+alt+b',     // override Bold shortcut
    italic: 'ctrl+alt+i',  // override Italic shortcut
  }
};

<RichTextEditorComponent formatter={customShortcut}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

## Globalization and Localization

### Localization (translating UI strings)

Load locale strings to translate toolbar tooltips, dialog labels, and messages:

```tsx
import { L10n } from '@syncfusion/ej2-base';

L10n.load({
  'de': {
    'richtexteditor': {
      'alignments': 'Ausrichtungen',
      'justifyLeft': 'Links ausrichten',
      'justifyCenter': 'Mitte',
      'justifyRight': 'Rechts ausrichten',
      'justifyFull': 'Rechtfertigen',
      'fontName': 'Schriftart Name',
      'fontSize': 'Schriftgröße',
      // ... other strings
    }
  }
});

<RichTextEditorComponent locale="de">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### Number and Date Formatting

For number/date formatting within the editor content, use Syncfusion's `Internationalization` utility:

```tsx
import { Internationalization } from '@syncfusion/ej2-base';
const intl = new Internationalization();
const formattedDate = intl.formatDate(new Date(), { skeleton: 'yMd', locale: 'fr' });
```

## RTL Support

Enable right-to-left text direction for Arabic, Hebrew, or other RTL languages:

```tsx
<RichTextEditorComponent enableRtl={true} locale="ar">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

RTL mode flips:
- Toolbar item ordering (right to left)
- Text direction in the editor content area
- Dialog and popup positions

**RTL for the whole app** — set it globally:

```tsx
import { enableRtl } from '@syncfusion/ej2-base';
enableRtl(true);
```

## Style Encapsulation

Style encapsulation prevents the host page's CSS from affecting editor content and prevents editor styles from leaking out. Uses ShadowDOM internally.

```tsx
<RichTextEditorComponent enableHtmlSanitizer={true}>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

For IFrame mode, content isolation is automatic since the editor renders in its own `<iframe>` document. See `editor-modes.md` for IFrame configuration.

**When style conflicts occur:**
- Use IFrame mode (`iframeSettings.enable: true`) for strongest isolation
- Add `e-rte-content` class to your output container when rendering retrieved HTML outside the editor — this applies the correct content styles (see `editor-value.md` for the required CSS)
