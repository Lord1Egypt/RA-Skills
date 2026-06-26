# Globalization and Localization

## Table of Contents
- [Localization Basics](#localization-basics)
- [Available Locale Strings](#available-locale-strings)
- [Implementing Localization](#implementing-localization)
- [Language Switching](#language-switching)
- [RTL Support](#rtl-support)
- [Accessibility Labels](#accessibility-labels)
- [Custom HTML Attributes](#custom-html-attributes)
- [Multi-Language Examples](#multi-language-examples)

## Localization Basics

The SpeechToText component supports localization through the `L10n.load()` method, which allows you to translate component strings for different languages and cultures.

### Default Locale

The component uses `en-US` (English - United States) by default.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function DefaultLocaleDemo() {
  return (
    <SpeechToTextComponent 
      id="speechToText"
      // Default locale is en-US
    />
  );
}
```

### Setting Component Locale

Use the `locale` property to set a specific locale:

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function CustomLocaleDemo() {
  return (
    <div>
      {/* German locale */}
      <SpeechToTextComponent locale="de" />
      
      {/* French locale */}
      <SpeechToTextComponent locale="fr" />
      
      {/* Spanish locale */}
      <SpeechToTextComponent locale="es" />
    </div>
  );
}
```

## Available Locale Strings

The following strings can be localized:

| Key | English Default | Purpose |
|-----|-----------------|---------|
| `abortedError` | "Speech recognition was aborted." | Shown when recognition is aborted |
| `audioCaptureError` | "No microphone detected. Ensure your microphone is connected." | Microphone not found |
| `defaultError` | "An unknown error occurred." | Generic error message |
| `networkError` | "Network error occurred. Check your internet connection." | Network connectivity issue |
| `noSpeechError` | "No speech detected. Please speak into the microphone." | User didn't speak |
| `notAllowedError` | "Microphone access denied. Allow microphone permissions." | Permission denied |
| `serviceNotAllowedError` | "Speech recognition service is not allowed in this context." | Service blocked |
| `unsupportedBrowserError` | "The browser does not support the SpeechRecognition API." | Browser not supported |
| `startAriaLabel` | "Press to start speaking and transcribe your words" | Accessibility label for start |
| `stopAriaLabel` | "Press to stop speaking and end transcription" | Accessibility label for stop |
| `startTooltipText` | "Start listening" | Tooltip when not listening |
| `stopTooltipText` | "Stop listening" | Tooltip when listening |

## Implementing Localization

### Basic Localization

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function LocalizationDemo() {
  // Load German translations
  L10n.load({
    'de': {
      'speech-to-text': {
        'startTooltipText': 'Zum Starten klicken',
        'stopTooltipText': 'Zum Stoppen klicken',
        'noSpeechError': 'Keine Sprache erkannt. Bitte sprechen Sie in das Mikrofon.'
      }
    }
  });

  return (
    <SpeechToTextComponent locale="de" />
  );
}

export default LocalizationDemo;
```

### Complete Language Translation

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function FullGermanTranslation() {
  L10n.load({
    'de': {
      'speech-to-text': {
        'abortedError': 'Die Spracherkennung wurde abgebrochen.',
        'audioCaptureError': 'Kein Mikrofon erkannt. Stellen Sie sicher, dass Ihr Mikrofon angeschlossen ist.',
        'defaultError': 'Ein unbekannter Fehler ist aufgetreten.',
        'networkError': 'Netzwerkfehler aufgetreten. Überprüfen Sie Ihre Internetverbindung.',
        'noSpeechError': 'Keine Sprache erkannt. Bitte sprechen Sie in das Mikrofon.',
        'notAllowedError': 'Mikrofonzugriff verweigert. Erlauben Sie Mikrofonberechtigungen.',
        'serviceNotAllowedError': 'Der Spracherkennungsdienst ist in diesem Kontext nicht erlaubt.',
        'unsupportedBrowserError': 'Der Browser unterstützt die SpeechRecognition API nicht.',
        'startAriaLabel': 'Drücken Sie, um zu sprechen und Ihre Worte zu transkribieren',
        'stopAriaLabel': 'Drücken Sie, um das Sprechen zu beenden und die Transkription zu stoppen',
        'startTooltipText': 'Zuhören starten',
        'stopTooltipText': 'Zuhören beenden'
      }
    }
  });

  return (
    <SpeechToTextComponent locale="de" />
  );
}

export default FullGermanTranslation;
```

## Language Switching

Implement dynamic language switching:

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import { useState } from 'react';

function LanguageSwitcher() {
  const [selectedLanguage, setSelectedLanguage] = useState('en');

  // Load translations for all supported languages
  L10n.load({
    'de': {
      'speech-to-text': {
        'startTooltipText': 'Zuhören starten',
        'stopTooltipText': 'Zuhören beenden',
        'noSpeechError': 'Keine Sprache erkannt.'
      }
    },
    'fr': {
      'speech-to-text': {
        'startTooltipText': 'Commencer à écouter',
        'stopTooltipText': 'Arrêter d\'écouter',
        'noSpeechError': 'Aucune parole détectée.'
      }
    },
    'es': {
      'speech-to-text': {
        'startTooltipText': 'Comenzar a escuchar',
        'stopTooltipText': 'Dejar de escuchar',
        'noSpeechError': 'No se detectó voz.'
      }
    }
  });

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <label>Select Language: </label>
        <select 
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
        >
          <option value="en">English</option>
          <option value="de">Deutsch</option>
          <option value="fr">Français</option>
          <option value="es">Español</option>
        </select>
      </div>

      <SpeechToTextComponent 
        locale={selectedLanguage}
        key={selectedLanguage}  // Force re-render on language change
      />
    </div>
  );
}

export default LanguageSwitcher;
```

## RTL Support

Enable Right-to-Left (RTL) layout for languages like Arabic, Hebrew, and Persian.

### Enabling RTL

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function RTLDemo() {
  return (
    <SpeechToTextComponent 
      enableRtl={true}
      locale="ar"  // Arabic locale
    />
  );
}

export default RTLDemo;
```

### RTL with Arabic Translations

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function ArabicRTL() {
  L10n.load({
    'ar': {
      'speech-to-text': {
        'startTooltipText': 'اضغط للبدء في التحدث',
        'stopTooltipText': 'اضغط للتوقف عن التحدث',
        'noSpeechError': 'لم يتم الكشف عن كلام. يرجى التحدث في الميكروفون.',
        'audioCaptureError': 'لم يتم الكشف عن ميكروفون.',
        'notAllowedError': 'تم رفض الوصول إلى الميكروفون.'
      }
    }
  });

  return (
    <div dir="rtl" style={{ padding: '20px' }}>
      <SpeechToTextComponent 
        enableRtl={true}
        locale="ar"
      />
    </div>
  );
}

export default ArabicRTL;
```

### RTL with Hebrew

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function HebrewRTL() {
  L10n.load({
    'he': {
      'speech-to-text': {
        'startTooltipText': 'לחץ כדי להתחיל לדבר',
        'stopTooltipText': 'לחץ כדי להפסיק לדבר',
        'noSpeechError': 'לא זוהה דיבור. אנא דברו למיקרופון.'
      }
    }
  });

  return (
    <div dir="rtl">
      <SpeechToTextComponent 
        enableRtl={true}
        locale="he"
      />
    </div>
  );
}

export default HebrewRTL;
```

## Accessibility Labels

Use ARIA labels for screen reader support via `L10n` locale strings:

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function AccessibleLocalization() {
  L10n.load({
    'en': {
      'speech-to-text': {
        'startAriaLabel': 'Activate voice input. Press to start recording your message.',
        'stopAriaLabel': 'Deactivate voice input. Press to stop recording your message.',
        'startTooltipText': 'Click to start voice input',
        'stopTooltipText': 'Click to stop voice input'
      }
    }
  });

  return (
    <SpeechToTextComponent locale="en" />
  );
}

export default AccessibleLocalization;
```

## Custom HTML Attributes

Use `htmlAttributes` to add arbitrary HTML attributes (ARIA attributes, data attributes, test IDs, etc.) directly to the root button element of the SpeechToText component.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function HtmlAttributesDemo() {
  return (
    <SpeechToTextComponent
      htmlAttributes={{
        'aria-label': 'Start voice input for the name field',
        'aria-describedby': 'voice-hint',
        'data-testid': 'voice-btn-name',
        'role': 'button'
      }}
    />
  );
}

export default HtmlAttributesDemo;
```

### Using htmlAttributes for Accessibility in Forms

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function AccessibleVoiceForm() {
  return (
    <form>
      <div>
        <label id="name-label" htmlFor="name-voice">Full Name (voice input)</label>
        <SpeechToTextComponent
          id="name-voice"
          htmlAttributes={{
            'aria-labelledby': 'name-label',
            'aria-required': 'true',
            'data-field': 'fullName'
          }}
        />
        <span id="voice-hint" style={{ fontSize: '12px', color: '#666' }}>
          Click the microphone and speak your full name.
        </span>
      </div>
    </form>
  );
}

export default AccessibleVoiceForm;
```

## Multi-Language Examples

### Example 1: Global Application

```tsx
import { SpeechToTextComponent, TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import { useState } from 'react';

function GlobalApp() {
  const [language, setLanguage] = useState('en');
  const [transcript, setTranscript] = useState('');

  // Load all supported languages
  L10n.load({
    'en': {
      'speech-to-text': {
        'startTooltipText': 'Start listening',
        'stopTooltipText': 'Stop listening',
        'noSpeechError': 'No speech detected. Please speak into the microphone.'
      }
    },
    'de': {
      'speech-to-text': {
        'startTooltipText': 'Zuhören starten',
        'stopTooltipText': 'Zuhören beenden',
        'noSpeechError': 'Keine Sprache erkannt. Bitte sprechen Sie in das Mikrofon.'
      }
    },
    'fr': {
      'speech-to-text': {
        'startTooltipText': 'Commencer à écouter',
        'stopTooltipText': 'Arrêter d\'écouter',
        'noSpeechError': 'Aucune parole détectée. Veuillez parler au microphone.'
      }
    },
    'es': {
      'speech-to-text': {
        'startTooltipText': 'Comenzar a escuchar',
        'stopTooltipText': 'Dejar de escuchar',
        'noSpeechError': 'No se detectó voz. Por favor, hable en el micrófono.'
      }
    },
    'ja': {
      'speech-to-text': {
        'startTooltipText': 'リッスニングを開始',
        'stopTooltipText': 'リッスニングを停止',
        'noSpeechError': '音声が検出されていません。マイクに向かって話してください。'
      }
    }
  });

  const languages = {
    en: 'English',
    de: 'Deutsch',
    fr: 'Français',
    es: 'Español',
    ja: '日本語'
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h2>Multi-Language Voice Input</h2>

      <div style={{ marginBottom: '20px' }}>
        <label>Language: </label>
        <select 
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>{name}</option>
          ))}
        </select>
      </div>

      <SpeechToTextComponent
        locale={language}
        lang={language === 'ja' ? 'ja-JP' : language}
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
        key={language}
      />

      <div style={{ marginTop: '20px' }}>
        <p>Transcript:</p>
        <TextAreaComponent
          value={transcript}
          rows={5}
          placeholder="Your speech will appear here..."
        />
      </div>
    </div>
  );
}

export default GlobalApp;
```

### Example 2: Region-Specific App

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';

function RegionalApp() {
  const userRegion = 'de'; // Could come from user settings

  L10n.load({
    'de': {
      'speech-to-text': {
        'startTooltipText': 'Zum Starten klicken',
        'stopTooltipText': 'Zum Stoppen klicken',
        'noSpeechError': 'Keine Sprache erkannt.'
      }
    }
  });

  return (
    <div>
      <h1>German Voice Input</h1>
      <SpeechToTextComponent 
        locale={userRegion}
        lang={`${userRegion}-DE`}
        enableRtl={false}
      />
    </div>
  );
}

export default RegionalApp;
```

### Example 3: Bilingual Interface

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { L10n } from '@syncfusion/ej2-base';
import { useState } from 'react';

function BilingualApp() {
  const [activeLanguage, setActiveLanguage] = useState('en');

  L10n.load({
    'en': {
      'speech-to-text': {
        'startTooltipText': 'Click to start',
        'stopTooltipText': 'Click to stop'
      }
    },
    'es': {
      'speech-to-text': {
        'startTooltipText': 'Haga clic para comenzar',
        'stopTooltipText': 'Haga clic para detener'
      }
    }
  });

  return (
    <div style={{ display: 'flex', gap: '40px', padding: '20px' }}>
      <div>
        <h3>English</h3>
        <SpeechToTextComponent 
          locale="en"
          lang="en-US"
        />
      </div>
      <div>
        <h3>Español</h3>
        <SpeechToTextComponent 
          locale="es"
          lang="es-ES"
        />
      </div>
    </div>
  );
}

export default BilingualApp;
```

## Troubleshooting

### Translations not appearing
- Ensure `L10n.load()` is called before component renders
- Check locale code matches (e.g., 'de' not 'de-DE' for L10n)
- Verify key names match exactly

### RTL not working
- Set `enableRtl={true}` on component
- Wrap in `<div dir="rtl">` for proper layout
- Load RTL-appropriate translations

### Language switching not updating
- Use `key` prop to force component re-render: `key={language}`
- Ensure locale property updates when language changes

