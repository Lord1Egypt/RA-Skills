---
name: globalization-rtl
description: Enable internationalization, multi-language support, and RTL layouts in Chat-UI.
---

# Globalization and RTL

## Table of Contents
- [Localization](#localization)
- [Supported Languages](#supported-languages)
- [RTL Support](#rtl-support)
- [Locale Strings](#locale-strings)
- [Custom Localization](#custom-localization)

## Localization

### Set Language/Locale

Configure Chat-UI for different languages:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            {/* English (default) */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                locale="en"
            />

            {/* German */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                locale="de"
            />

            {/* Arabic */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                locale="ar"
            />

            {/* Spanish */}
            <ChatUIComponent 
                user={{ id: "user1", user: "Albert" }}
                locale="es"
            />
        </>
    );
}
```

## Supported Languages

| Locale | Language | Code |
|--------|----------|------|
| English | English | `en` |
| German | Deutsch | `de` |
| Spanish | Español | `es` |
| French | Français | `fr` |
| Arabic | العربية | `ar` |
| Portuguese | Português | `pt` |
| Russian | Русский | `ru` |
| Chinese Simplified | 简体中文 | `zh` |
| Japanese | 日本語 | `ja` |

## RTL Support

### Enable Right-to-Left Layout

Enable RTL for languages like Arabic and Hebrew:

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            {/* Arabic with RTL */}
            <ChatUIComponent 
                user={{ id: "user1", user: "أحمد" }}
                locale="ar"
                enableRtl={true}
            />

            {/* Hebrew with RTL */}
            <ChatUIComponent 
                user={{ id: "user1", user: "דויד" }}
                locale="he"
                enableRtl={true}
            />

            {/* Persian with RTL */}
            <ChatUIComponent 
                user={{ id: "user1", user: "علی" }}
                locale="fa"
                enableRtl={true}
            />
        </>
    );
}
```

### RTL Styling

```css
/* RTL layout adjustments */
.e-chat-ui[dir="rtl"] {
    direction: rtl;
    text-align: right;
}

.e-chat-ui[dir="rtl"] .e-input-group {
    direction: rtl;
}

.e-chat-ui[dir="rtl"] .e-send-button {
    margin-left: 0;
    margin-right: 8px;
}
```

## Locale Strings

### Typing Indicator Text

The typing indicator uses localized strings based on user count:

| Key | Default (English) | Count |
|-----|------------------|-------|
| `oneUserTyping` | `{0} is typing` | 1 user |
| `twoUserTyping` | `{0} and {1} are typing` | 2 users |
| `threeUserTyping` | `{0}, {1}, and {2} other are typing` | 3+ users (shows 2 + count) |
| `multipleUsersTyping` | `{0}, {1}, and {2} others are typing` | 3+ users |

### Typing Examples by Locale

```tsx
// English
"{0} is typing"          → "Albert is typing"
"{0} and {1} are typing" → "Albert and Michale are typing"

// German
"{0} schreibt"           → "Albert schreibt"
"{0} und {1} schreiben"  → "Albert und Michale schreiben"

// Arabic (RTL)
"يكتب {0}"              → "يكتب Albert"
"يكتب {0} و {1}"         → "يكتب Albert و Michale"
```

## Custom Localization

### Add Custom Locale

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

// Define custom locale
const customLocale = {
    'oneUserTyping': '{0} est en train d\'écrire',
    'twoUserTyping': '{0} et {1} écrivent',
    'threeUserTyping': '{0}, {1}, et {2} autre écrit',
    'multipleUsersTyping': '{0}, {1}, et {2} autres écrivent'
};

function App() {
    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "Albert" }}
            locale="fr"  // French locale
        />
    );
}
```

## Complete Example

### Multi-Language Chat Application

```tsx
import { ChatUIComponent, MessagesDirective, MessageDirective, UserModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [selectedLocale, setSelectedLocale] = useState('en');
    const [enableRtl, setEnableRtl] = useState(false);

    const currentUser: UserModel = {
        id: "user1",
        user: selectedLocale === 'ar' ? 'أحمد' : 'Albert'
    };

    const typingUsers = selectedLocale === 'ar' 
        ? [{ id: "user2", user: 'محمد' }]
        : [{ id: "user2", user: 'Support' }];

    const localeMessages = {
        en: {
            headerText: 'Support Chat',
            placeholder: 'Type your message...'
        },
        de: {
            headerText: 'Support-Chat',
            placeholder: 'Geben Sie Ihre Nachricht ein...'
        },
        ar: {
            headerText: 'دردشة الدعم',
            placeholder: 'اكتب رسالتك...'
        },
        es: {
            headerText: 'Chat de Soporte',
            placeholder: 'Escribe tu mensaje...'
        }
    };

    const messages = localeMessages[selectedLocale] || localeMessages.en;

    return (
        <div style={{ padding: '20px' }}>
            {/* Language Selector */}
            <div style={{ marginBottom: '20px' }}>
                <label>
                    Language:
                    <select 
                        value={selectedLocale}
                        onChange={(e) => {
                            setSelectedLocale(e.target.value);
                            setEnableRtl(e.target.value === 'ar');
                        }}
                    >
                        <option value="en">English</option>
                        <option value="de">Deutsch</option>
                        <option value="es">Español</option>
                        <option value="ar">العربية</option>
                    </select>
                </label>
            </div>

            {/* Chat Component */}
            <ChatUIComponent 
                user={currentUser}
                headerText={messages.headerText}
                placeholder={messages.placeholder}
                locale={selectedLocale}
                enableRtl={enableRtl}
                typingUsers={typingUsers}
                height="500px"
            >
                <MessagesDirective>
                    <MessageDirective 
                        text={selectedLocale === 'ar' ? 'مرحبا بك في الدعم!' : 'Welcome to support!'}
                        author={{ id: "user2", user: selectedLocale === 'ar' ? 'الدعم' : 'Support' }}
                    />
                </MessagesDirective>
            </ChatUIComponent>
        </div>
    );
}

export default App;
```

## Language Detection

### Auto-Detect User Language

```tsx
import { ChatUIComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [locale, setLocale] = useState('en');
    const [rtlEnabled, setRtlEnabled] = useState(false);

    useEffect(() => {
        // Get browser language
        const browserLang = navigator.language.split('-')[0];
        
        // Map to supported locales
        const supportedLocales = {
            'en': 'en',
            'de': 'de',
            'es': 'es',
            'ar': 'ar',
            'fr': 'fr',
            'pt': 'pt'
        };

        const detectedLocale = supportedLocales[browserLang] || 'en';
        setLocale(detectedLocale);

        // Enable RTL for specific locales
        const rtlLocales = ['ar', 'he', 'fa'];
        setRtlEnabled(rtlLocales.includes(detectedLocale));
    }, []);

    return (
        <ChatUIComponent 
            user={{ id: "user1", user: "User" }}
            locale={locale}
            enableRtl={rtlEnabled}
        />
    );
}
```

## Responsive RTL Layout

### CSS for RTL Responsiveness

```css
/* Base styles */
.e-chat-ui {
    direction: ltr;
}

/* RTL adjustments */
.e-chat-ui[dir="rtl"] {
    direction: rtl;
}

.e-chat-ui[dir="rtl"] .e-chat-header {
    padding-right: 16px;
    padding-left: 8px;
}

.e-chat-ui[dir="rtl"] .e-message-right {
    margin-right: 0;
    margin-left: auto;
}

.e-chat-ui[dir="rtl"] .e-message-left {
    margin-left: 0;
    margin-right: auto;
}

.e-chat-ui[dir="rtl"] .e-send-button {
    order: -1;
}

/* Mobile adjustments */
@media (max-width: 480px) {
    .e-chat-ui[dir="rtl"] {
        font-size: 14px;
    }
    
    .e-chat-ui[dir="rtl"] .e-message-bubble {
        max-width: 85%;
    }
}
```

## Best Practices

1. **Detect user language** from browser settings
2. **Support RTL automatically** for RTL locales
3. **Test with real native speakers** when localizing
4. **Keep text labels concise** for different languages
5. **Handle text expansion** (RTL text often needs more space)
6. **Use Unicode properly** for special characters
7. **Test on mobile** for RTL layouts
8. **Provide language selector** for user preference

## Supported RTL Languages

- Arabic (ar)
- Hebrew (he)
- Persian/Farsi (fa)
- Urdu (ur)
