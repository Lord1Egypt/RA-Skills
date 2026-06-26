````markdown
# Internationalization (i18n) and RTL Support

## Table of Contents
- [Overview](#overview)
- [locale Property](#locale-property)
- [enableRtl Property](#enablertl-property)
- [Combining locale and enableRtl](#combining-locale-and-enablertl)
- [Available Locales](#available-locales)
- [Custom Localization](#custom-localization)
- [Complete Examples](#complete-examples)

## Overview

The Inline AI Assist component supports internationalization (i18n) and right-to-left (RTL) text direction for building global applications. Two key properties enable this:

1. **locale** - Sets the language and regional formatting
2. **enableRtl** - Enables right-to-left text direction

These properties ensure your AI assistant can serve users worldwide with proper localization and text directionality.

## locale Property

The `locale` property sets the language and cultural formatting for the component's UI text, date formats, and number formats.

### Property Details

**Type:** `string`  
**Default:** `'en-US'`  
**Component Property:** `locale`

### Supported Locale Codes

Locale codes follow the BCP 47 format: `language-REGION` (e.g., `en-US`, `fr-FR`, `ar-SA`)

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            locale="fr-FR"
            placeholder="Demandez à l'IA..."
        />
    );
};

export default App;
```

### What Gets Localized

When you set the `locale` property, the following UI elements adapt:

1. **UI Text:**
   - Button labels (Send, Cancel, Accept, Reject)
   - Placeholder text
   - Error messages
   - Tooltips

2. **Date/Time Formatting:**
   - Timestamps in response headers
   - Date displays in metadata

3. **Number Formatting:**
   - Character counts
   - Token counts
   - Progress indicators

### Setting Up Localization

#### Step 1: Install Localization Package

```bash
npm install @syncfusion/ej2-locale --save
```

#### Step 2: Import Locale Data

```tsx
import { L10n, loadCldr } from '@syncfusion/ej2-base';
import * as numberingSystems from 'cldr-data/supplemental/numberingSystems.json';
import * as gregorian from 'cldr-data/main/fr-FR/ca-gregorian.json';
import * as numbers from 'cldr-data/main/fr-FR/numbers.json';
import * as timeZoneNames from 'cldr-data/main/fr-FR/timeZoneNames.json';

// Load CLDR data
loadCldr(numberingSystems, gregorian, numbers, timeZoneNames);
```

#### Step 3: Define Localized Strings

```tsx
// French localization
L10n.load({
    'fr-FR': {
        'inline-ai-assist': {
            'placeholder': 'Demandez quelque chose à l\'IA...',
            'send': 'Envoyer',
            'cancel': 'Annuler',
            'accept': 'Accepter',
            'reject': 'Rejeter',
            'generating': 'Génération en cours...',
            'error': 'Une erreur s\'est produite'
        }
    }
});
```

#### Step 4: Apply Locale to Component

```tsx
const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            locale="fr-FR"
        />
    );
};
```

### Complete Localization Example

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import { L10n } from '@syncfusion/ej2-base';
import React from 'react';

// Define Spanish localization
L10n.load({
    'es-ES': {
        'inline-ai-assist': {
            'placeholder': 'Pregunta algo a la IA...',
            'send': 'Enviar',
            'cancel': 'Cancelar',
            'accept': 'Aceptar',
            'reject': 'Rechazar',
            'regenerate': 'Regenerar',
            'copy': 'Copiar',
            'generating': 'Generando respuesta...',
            'error': 'Se produjo un error',
            'noResponse': 'No se recibió respuesta'
        }
    }
});

const SpanishAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = (args: any) => {
        setTimeout(() => {
            assistRef.current?.addResponse('Esta es una respuesta de la IA.');
        }, 1000);
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            locale="es-ES"
            promptRequest={handlePromptRequest}
        />
    );
};

export default SpanishAssistant;
```

## enableRtl Property

The `enableRtl` property enables right-to-left text direction for languages like Arabic, Hebrew, Persian, and Urdu.

### Property Details

**Type:** `boolean`  
**Default:** `false`  
**Component Property:** `enableRtl`

### When to Use

Enable RTL when your application serves:
- Arabic (ar)
- Hebrew (he)
- Persian/Farsi (fa)
- Urdu (ur)
- Other RTL languages

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            enableRtl={true}
            placeholder="اسأل الذكاء الاصطناعي..."
        />
    );
};

export default App;
```

### What Changes with RTL

When `enableRtl` is enabled:

1. **Layout Direction:**
   - Component layout flips horizontally
   - Buttons move from right to left
   - Text alignment changes to right

2. **UI Elements:**
   - Input fields align text to the right
   - Icons and buttons reposition to the left
   - Popup menus open from right to left

3. **Scroll Behavior:**
   - Scrollbars appear on the left side
   - Scroll direction adjusts accordingly

### RTL Example (Arabic)

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import { L10n } from '@syncfusion/ej2-base';
import React from 'react';

// Arabic localization
L10n.load({
    'ar-SA': {
        'inline-ai-assist': {
            'placeholder': 'اسأل الذكاء الاصطناعي...',
            'send': 'إرسال',
            'cancel': 'إلغاء',
            'accept': 'قبول',
            'reject': 'رفض',
            'generating': 'جارٍ الإنشاء...',
            'error': 'حدث خطأ'
        }
    }
});

const ArabicAssistant: React.FC = () => {
    return (
        <div dir="rtl"> {/* Set RTL on container */}
            <InlineAIAssistComponent
                locale="ar-SA"
                enableRtl={true}
            />
        </div>
    );
};

export default ArabicAssistant;
```

### RTL Example (Hebrew)

```tsx
// Hebrew localization
L10n.load({
    'he-IL': {
        'inline-ai-assist': {
            'placeholder': 'שאל את הבינה המלאכותית...',
            'send': 'שלח',
            'cancel': 'ביטול',
            'accept': 'אשר',
            'reject': 'דחה',
            'generating': 'מייצר תשובה...',
            'error': 'אירעה שגיאה'
        }
    }
});

const HebrewAssistant: React.FC = () => {
    return (
        <InlineAIAssistComponent
            locale="he-IL"
            enableRtl={true}
        />
    );
};
```

## Combining locale and enableRtl

For RTL languages, you typically use both properties together:

### Complete RTL Setup

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import { L10n } from '@syncfusion/ej2-base';
import React from 'react';

const RTLAssistant: React.FC = () => {
    // Setup Arabic localization
    React.useEffect(() => {
        L10n.load({
            'ar-SA': {
                'inline-ai-assist': {
                    'placeholder': 'اسأل الذكاء الاصطناعي...',
                    'send': 'إرسال',
                    'cancel': 'إلغاء',
                    'accept': 'قبول',
                    'reject': 'رفض'
                }
            }
        });
    }, []);

    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = (args: any) => {
        // Call Arabic AI service
        callArabicAI(args.prompt).then(response => {
            assistRef.current?.addResponse(response);
        });
    };

    return (
        <div dir="rtl" style={{ fontFamily: 'Arial, sans-serif' }}>
            <h2>مساعد الذكاء الاصطناعي</h2>
            
            <InlineAIAssistComponent
                ref={assistRef}
                locale="ar-SA"
                enableRtl={true}
                promptRequest={handlePromptRequest}
                popupWidth="500px"
            />
        </div>
    );
};

export default RTLAssistant;
```

## Available Locales

### Common Locales

| Locale Code | Language | Region | RTL Required |
|-------------|----------|--------|--------------|
| `en-US` | English | United States | No |
| `en-GB` | English | United Kingdom | No |
| `es-ES` | Spanish | Spain | No |
| `es-MX` | Spanish | Mexico | No |
| `fr-FR` | French | France | No |
| `de-DE` | German | Germany | No |
| `it-IT` | Italian | Italy | No |
| `pt-BR` | Portuguese | Brazil | No |
| `pt-PT` | Portuguese | Portugal | No |
| `ru-RU` | Russian | Russia | No |
| `ja-JP` | Japanese | Japan | No |
| `ko-KR` | Korean | South Korea | No |
| `zh-CN` | Chinese | China (Simplified) | No |
| `zh-TW` | Chinese | Taiwan (Traditional) | No |
| `ar-SA` | Arabic | Saudi Arabia | Yes |
| `ar-AE` | Arabic | UAE | Yes |
| `he-IL` | Hebrew | Israel | Yes |
| `fa-IR` | Persian | Iran | Yes |
| `ur-PK` | Urdu | Pakistan | Yes |
| `hi-IN` | Hindi | India | No |
| `bn-BD` | Bengali | Bangladesh | No |
| `tr-TR` | Turkish | Turkey | No |
| `pl-PL` | Polish | Poland | No |
| `nl-NL` | Dutch | Netherlands | No |
| `sv-SE` | Swedish | Sweden | No |
| `da-DK` | Danish | Denmark | No |
| `fi-FI` | Finnish | Finland | No |
| `no-NO` | Norwegian | Norway | No |

## Custom Localization

### Creating Custom Locale Strings

Define custom localization for any language:

```tsx
import { L10n } from '@syncfusion/ej2-base';

// Define custom locale
L10n.load({
    'custom-LANG': {
        'inline-ai-assist': {
            // Prompt input
            'placeholder': 'Your placeholder text',
            
            // Actions
            'send': 'Send',
            'cancel': 'Cancel',
            'accept': 'Accept',
            'reject': 'Reject',
            'regenerate': 'Regenerate',
            'copy': 'Copy',
            'share': 'Share',
            
            // Status messages
            'generating': 'Generating...',
            'loading': 'Loading...',
            'processing': 'Processing...',
            
            // Error messages
            'error': 'An error occurred',
            'noResponse': 'No response received',
            'networkError': 'Network error',
            'timeout': 'Request timed out',
            
            // Tooltips
            'sendTooltip': 'Send prompt',
            'cancelTooltip': 'Cancel request',
            'acceptTooltip': 'Accept response',
            'rejectTooltip': 'Reject response'
        }
    }
});
```

### Multi-Language Application

Support multiple languages with language selector:

```tsx
const MultiLanguageAssistant: React.FC = () => {
    const [currentLocale, setCurrentLocale] = React.useState('en-US');
    const [isRtl, setIsRtl] = React.useState(false);
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    // RTL languages
    const rtlLanguages = ['ar-SA', 'he-IL', 'fa-IR', 'ur-PK'];

    // Setup localizations
    React.useEffect(() => {
        L10n.load({
            'en-US': {
                'inline-ai-assist': {
                    'placeholder': 'Ask AI anything...',
                    'send': 'Send',
                    'cancel': 'Cancel',
                    'accept': 'Accept',
                    'reject': 'Reject'
                }
            },
            'es-ES': {
                'inline-ai-assist': {
                    'placeholder': 'Pregunta algo...',
                    'send': 'Enviar',
                    'cancel': 'Cancelar',
                    'accept': 'Aceptar',
                    'reject': 'Rechazar'
                }
            },
            'ar-SA': {
                'inline-ai-assist': {
                    'placeholder': 'اسأل الذكاء الاصطناعي...',
                    'send': 'إرسال',
                    'cancel': 'إلغاء',
                    'accept': 'قبول',
                    'reject': 'رفض'
                }
            },
            'fr-FR': {
                'inline-ai-assist': {
                    'placeholder': 'Demandez à l\'IA...',
                    'send': 'Envoyer',
                    'cancel': 'Annuler',
                    'accept': 'Accepter',
                    'reject': 'Rejeter'
                }
            }
        });
    }, []);

    const handleLanguageChange = (locale: string) => {
        setCurrentLocale(locale);
        setIsRtl(rtlLanguages.includes(locale));
    };

    return (
        <div dir={isRtl ? 'rtl' : 'ltr'}>
            <div className="language-selector">
                <label>Language:</label>
                <select 
                    value={currentLocale}
                    onChange={(e) => handleLanguageChange(e.target.value)}
                    className="e-input"
                >
                    <option value="en-US">🇺🇸 English</option>
                    <option value="es-ES">🇪🇸 Español</option>
                    <option value="fr-FR">🇫🇷 Français</option>
                    <option value="ar-SA">🇸🇦 العربية</option>
                </select>
            </div>
            
            <InlineAIAssistComponent
                ref={assistRef}
                locale={currentLocale}
                enableRtl={isRtl}
            />
        </div>
    );
};
```

## Complete Examples

### Example 1: Multi-Region Support

```tsx
const GlobalAssistant: React.FC = () => {
    const [region, setRegion] = React.useState<'us' | 'eu' | 'asia' | 'mena'>('us');
    
    const regionSettings = {
        us: { locale: 'en-US', rtl: false },
        eu: { locale: 'de-DE', rtl: false },
        asia: { locale: 'ja-JP', rtl: false },
        mena: { locale: 'ar-SA', rtl: true }
    };

    const currentSettings = regionSettings[region];

    React.useEffect(() => {
        // Load all regional localizations
        L10n.load({
            'en-US': { /* English strings */ },
            'de-DE': { /* German strings */ },
            'ja-JP': { /* Japanese strings */ },
            'ar-SA': { /* Arabic strings */ }
        });
    }, []);

    return (
        <div dir={currentSettings.rtl ? 'rtl' : 'ltr'}>
            <div className="region-selector">
                <button onClick={() => setRegion('us')}>🇺🇸 Americas</button>
                <button onClick={() => setRegion('eu')}>🇪🇺 Europe</button>
                <button onClick={() => setRegion('asia')}>🌏 Asia</button>
                <button onClick={() => setRegion('mena')}>🌍 MENA</button>
            </div>
            
            <InlineAIAssistComponent
                locale={currentSettings.locale}
                enableRtl={currentSettings.rtl}
            />
        </div>
    );
};
```

### Example 2: Browser Language Detection

```tsx
const AutoLocaleAssistant: React.FC = () => {
    const [locale, setLocale] = React.useState('en-US');
    const [enableRtl, setEnableRtl] = React.useState(false);

    React.useEffect(() => {
        // Detect browser language
        const browserLang = navigator.language || navigator.languages[0];
        
        // Map to supported locale
        const supportedLocales: Record<string, string> = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'ar': 'ar-SA',
            'he': 'he-IL',
            'ja': 'ja-JP',
            'zh': 'zh-CN'
        };

        const lang = browserLang.split('-')[0];
        const detectedLocale = supportedLocales[lang] || 'en-US';
        
        setLocale(detectedLocale);
        setEnableRtl(['ar-SA', 'he-IL', 'fa-IR'].includes(detectedLocale));
    }, []);

    return (
        <InlineAIAssistComponent
            locale={locale}
            enableRtl={enableRtl}
        />
    );
};
```

### Example 3: User Preference Storage

```tsx
const PersistentLocaleAssistant: React.FC = () => {
    const [locale, setLocale] = React.useState<string>(() => {
        // Load from localStorage
        return localStorage.getItem('preferredLocale') || 'en-US';
    });

    const [enableRtl, setEnableRtl] = React.useState<boolean>(() => {
        return localStorage.getItem('preferredRtl') === 'true';
    });

    const handleLocaleChange = (newLocale: string) => {
        const isRtl = ['ar-SA', 'he-IL', 'fa-IR', 'ur-PK'].includes(newLocale);
        
        setLocale(newLocale);
        setEnableRtl(isRtl);
        
        // Persist to localStorage
        localStorage.setItem('preferredLocale', newLocale);
        localStorage.setItem('preferredRtl', isRtl.toString());
    };

    return (
        <div>
            <select 
                value={locale}
                onChange={(e) => handleLocaleChange(e.target.value)}
            >
                <option value="en-US">English (US)</option>
                <option value="es-ES">Español</option>
                <option value="fr-FR">Français</option>
                <option value="ar-SA">العربية</option>
            </select>
            
            <InlineAIAssistComponent
                locale={locale}
                enableRtl={enableRtl}
            />
        </div>
    );
};
```

## Best Practices

### Localization Best Practices

1. **Provide Complete Translations:**
   - Translate all UI text, not just partial strings
   - Include tooltips, error messages, and help text

2. **Test with Native Speakers:**
   - Verify translations are culturally appropriate
   - Check for proper grammar and context

3. **Consider Text Expansion:**
   - Some languages require more space (German, Finnish)
   - Design UI to accommodate text length variations

4. **Use Standard Locale Codes:**
   - Follow BCP 47 format (language-REGION)
   - Be consistent across your application

5. **Date and Number Formatting:**
   - Use locale-aware formatting libraries
   - Consider regional preferences (12/24 hour, date order)

### RTL Best Practices

1. **Test UI Layout:**
   - Verify all elements flip correctly
   - Check alignment and spacing

2. **Icons and Images:**
   - Some icons may need mirroring (arrows, directional icons)
   - Logos usually don't need flipping

3. **Mixed Content:**
   - Handle mixed LTR/RTL content gracefully
   - Properly mark content directionality

4. **Input Handling:**
   - Ensure proper text cursor behavior
   - Test copy/paste functionality

5. **Accessibility:**
   - Verify screen reader compatibility
   - Test keyboard navigation

### General i18n Guidelines

1. **Avoid Hardcoded Text:**
   - Use L10n for all user-facing text
   - Don't concatenate translated strings

2. **Context Matters:**
   - Same word may need different translations in different contexts
   - Provide context comments for translators

3. **Pluralization:**
   - Handle plural forms correctly (some languages have multiple plural forms)
   - Use ICU message format when needed

4. **Cultural Sensitivity:**
   - Be aware of cultural differences in colors, symbols
   - Test with users from target locales

5. **Performance:**
   - Load only required locale data
   - Consider lazy loading for large applications

---

````