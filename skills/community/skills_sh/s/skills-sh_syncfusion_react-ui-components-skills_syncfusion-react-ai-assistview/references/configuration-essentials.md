# Configuration Essentials

## Prompt Text and Placeholder

### Setting Default Prompt Text

Use the `prompt` property to set initial or default text in the prompt input area:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            prompt="What tools can help me prioritize tasks?"
        />
    );
}

export default App;
```

### Setting Placeholder Text

The `promptPlaceholder` property defines the placeholder text displayed when the input is empty. Default is "Type prompt for assistance...":

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    promptPlaceholder="Ask me anything..."
/>
```

## Prompt Suggestions Configuration

### Basic Suggestions

The `promptSuggestions` property provides users with helpful suggestions as starting prompts:

```tsx
const suggestions = [
    "Best practices for writing clean code?",
    "How to optimize code editor?",
    "Tips for better performance?"
];

<AIAssistViewComponent 
    id="aiAssistView"
    promptSuggestions={suggestions}
/>
```

### Customizing Suggestions Header

Add a header label above suggestions using `promptSuggestionsHeader`:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    promptSuggestions={suggestions}
    promptSuggestionsHeader="Suggested Prompts"
/>
```

### Handling Suggestion Selection

When users click a suggestion, it triggers the `promptRequest` event:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // args.prompt contains the suggestion text
    console.log('Selected suggestion:', args.prompt);
};

<AIAssistViewComponent 
    id="aiAssistView"
    promptSuggestions={suggestions}
    promptRequest={handlePromptRequest}
/>
```

## Avatar Customization

### User Avatar (promptIconCss)

Customize the icon that appears with user prompts using CSS classes:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    promptIconCss="e-icons e-user"
/>
```

### AI Response Avatar (responseIconCss)

Customize the icon that appears with AI responses. Default is `e-assistview-icon`:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    promptIconCss="e-icons e-user"
    responseIconCss="e-icons e-bullet-4"
/>
```

### Available Icon Classes

Common Syncfusion icon classes:
- `e-user` - User profile icon
- `e-bot` - Robot/bot icon
- `e-comment-show` - Comment icon
- `e-circle-info` - Info icon
- `e-assistview-icon` - Default AI icon
- `e-bullet-4` - Bullet point
- Custom CSS class for custom SVG/image icons

### Custom Avatar Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const onPromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response text');
        }, 1000);
    };

    return (
        <>
            <style>{`
                .custom-user-icon::before {
                    content: '👤';
                    font-size: 18px;
                }
                .custom-ai-icon::before {
                    content: '🤖';
                    font-size: 18px;
                }
            `}</style>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={onPromptRequest}
                promptIconCss="custom-user-icon"
                responseIconCss="custom-ai-icon"
            />
        </>
    );
}

export default App;
```

## Clear Button Visibility

### Enable Clear Button

The `showClearButton` property controls whether a clear button appears in the prompt input area. Default is `false`:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    showClearButton={true}
/>
```

### Clear Button Behavior

When clicked, the clear button only clears the current prompt text, NOT the conversation history:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
        }, 1000);
    };

    const clearConversation = () => {
        // Manually clear all prompts/responses
        if (assistInstance.current) {
            assistInstance.current.prompts = [];
        }
    };

    return (
        <div>
            <button onClick={clearConversation}>Clear All</button>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                showClearButton={true}
            />
        </div>
    );
}

export default App;
```

## Scroll to Bottom Functionality

### Enable Scroll Button

The `enableScrollToBottom` property controls the scroll-to-bottom indicator. Default is `true`:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    enableScrollToBottom={true}
/>
```

### When It Appears

A floating scroll-to-bottom button appears when:
- User scrolls away from the bottom of the conversation
- New responses are added while user is viewing earlier messages

Clicking the button smoothly scrolls to the latest response.

### Disable Auto-Scroll

If you want to hide the scroll button but keep scrolling behavior:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    enableScrollToBottom={false}
/>
```

## Component Sizing and Layout

### Setting Component Dimensions

Control the size of the AI AssistView component using `height` and `width` properties:

**Type:** `string | number`  
**Default:** `height='100%'`, `width='100%'`

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            height="600px"
            width="800px"
        />
    );
}

export default App;
```

### Height Options

```tsx
// Fixed pixel height
height="500px"

// Percentage height (relative to container)
height="100%"

// Viewport height
height="80vh"

// Numeric value (interpreted as pixels)
height={600}
```

### Width Options

```tsx
// Fixed pixel width
width="1000px"

// Percentage width (relative to container)
width="100%"

// Numeric value (interpreted as pixels)
width={800}

// Auto width
width="auto"
```

### Responsive Sizing

Make the component responsive to different screen sizes:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState, useEffect } from 'react';

function App() {
    const [dimensions, setDimensions] = useState({
        height: '600px',
        width: '100%'
    });

    useEffect(() => {
        const updateDimensions = () => {
            if (window.innerWidth < 768) {
                // Mobile
                setDimensions({ height: '100vh', width: '100%' });
            } else if (window.innerWidth < 1024) {
                // Tablet
                setDimensions({ height: '70vh', width: '90%' });
            } else {
                // Desktop
                setDimensions({ height: '600px', width: '800px' });
            }
        };

        updateDimensions();
        window.addEventListener('resize', updateDimensions);
        
        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            height={dimensions.height}
            width={dimensions.width}
        />
    );
}

export default App;
```

### Full Viewport Layout

Make the component fill the entire viewport:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    height="100vh"
    width="100%"
/>
```

### Within a Container

Size relative to a parent container:

```tsx
function App() {
    return (
        <div style={{ height: '800px', width: '1200px', padding: '20px' }}>
            <AIAssistViewComponent 
                id="aiAssistView"
                height="100%"
                width="100%"
            />
        </div>
    );
}
```

## Custom CSS Classes

### cssClass Property

Apply custom CSS classes to the component root element for additional styling:

**Type:** `string`  
**Default:** `''`

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <>
            <style>{`
                .custom-ai-chat {
                    border: 2px solid #667eea;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }
                
                .custom-ai-chat .e-toolbar {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                
                .custom-ai-chat .e-prompt-input {
                    font-size: 16px;
                    padding: 12px;
                }
            `}</style>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                cssClass="custom-ai-chat"
            />
        </>
    );
}

export default App;
```

### Multiple CSS Classes

Apply multiple classes separated by spaces:

```tsx
<AIAssistViewComponent 
    id="aiAssistView"
    cssClass="custom-theme dark-mode elevated-card"
/>
```

### Theme Customization with cssClass

Create custom themes:

```tsx
<style>{`
    /* Light theme */
    .theme-light {
        background-color: #ffffff;
        color: #333333;
    }
    
    .theme-light .e-prompt-area {
        background-color: #f5f5f5;
    }
    
    /* Dark theme */
    .theme-dark {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .theme-dark .e-prompt-area {
        background-color: #2d2d2d;
    }
    
    .theme-dark .e-prompt-input {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    /* Accent colors */
    .accent-blue .e-toolbar {
        background-color: #2196F3;
    }
    
    .accent-purple .e-toolbar {
        background-color: #9C27B0;
    }
    
    .accent-green .e-toolbar {
        background-color: #4CAF50;
    }
`}</style>

function App() {
    const [theme, setTheme] = useState('theme-light accent-blue');
    
    return (
        <div>
            <select onChange={(e) => setTheme(e.target.value)}>
                <option value="theme-light accent-blue">Light Blue</option>
                <option value="theme-dark accent-purple">Dark Purple</option>
                <option value="theme-light accent-green">Light Green</option>
            </select>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                cssClass={theme}
            />
        </div>
    );
}
```

### Spacing and Layout Adjustments

```tsx
<style>{`
    .compact-layout {
        font-size: 14px;
    }
    
    .compact-layout .e-prompt-item,
    .compact-layout .e-response-item {
        padding: 8px;
        margin: 4px 0;
    }
    
    .spacious-layout {
        font-size: 16px;
    }
    
    .spacious-layout .e-prompt-item,
    .spacious-layout .e-response-item {
        padding: 16px;
        margin: 12px 0;
    }
`}</style>

<AIAssistViewComponent 
    id="aiAssistView"
    cssClass="spacious-layout"
/>
```

### Brand-Specific Styling

```tsx
<style>{`
    .company-branded {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --text-color: #2C3E50;
    }
    
    .company-branded .e-toolbar {
        background-color: var(--primary-color);
        color: white;
    }
    
    .company-branded .e-btn-primary {
        background-color: var(--secondary-color);
        border-color: var(--secondary-color);
    }
    
    .company-branded .e-response-item {
        border-left: 3px solid var(--primary-color);
    }
`}</style>

<AIAssistViewComponent 
    id="aiAssistView"
    cssClass="company-branded"
/>
```

### Combining with Syncfusion Themes

```tsx
// Import Syncfusion theme
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-react-interactive-chat/styles/material.css';

<AIAssistViewComponent 
    id="aiAssistView"
    cssClass="custom-enhancements"  // Add your custom styles on top
/>
```

## Header Visibility Control

### showHeader Property

Control whether the header is displayed in the component:

**Type:** `boolean`  
**Default:** `true`

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            showHeader={false}  // Hide the header
        />
    );
}

export default App;
```

### When to Hide Header

Hide the header when:
- Embedding in a dashboard with its own title
- Creating a minimalist chat interface
- Component is in a modal or sidebar
- You want maximum space for conversation

```tsx
function MinimalistChat() {
    return (
        <div className="chat-container">
            <h2 className="custom-title">AI Assistant</h2>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                showHeader={false}
                height="calc(100vh - 80px)"
            />
        </div>
    );
}
```

### Dynamic Header Toggle

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [headerVisible, setHeaderVisible] = useState(true);

    return (
        <div>
            <button onClick={() => setHeaderVisible(!headerVisible)}>
                {headerVisible ? 'Hide Header' : 'Show Header'}
            </button>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                showHeader={headerVisible}
            />
        </div>
    );
}

export default App;
```

## Component Instance Management via Refs

### Using useRef to Access Component

Use React's `useRef` hook to access the component instance and call methods:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        // Access component methods and properties
        console.log('Current prompts:', assistInstance.current?.prompts);
        
        assistInstance.current?.addPromptResponse('Response');
    };

    const executeCustomPrompt = () => {
        // Programmatically execute a prompt
        assistInstance.current?.executePrompt('Custom prompt text');
    };

    return (
        <div>
            <button onClick={executeCustomPrompt}>Execute Prompt</button>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
}

export default App;
```

## Complete Configuration Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const prompts = [
        "What is AI?",
        "How to optimize code?",
        "Best practices?"
    ];

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            let response = 'Default response';
            if (args.prompt.includes('AI')) {
                response = 'AI stands for Artificial Intelligence.';
            }
            assistInstance.current?.addPromptResponse(response);
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            prompt="How can I help you?"
            promptPlaceholder="Enter your question here..."
            promptSuggestions={prompts}
            promptSuggestionsHeader="Try asking about:"
            promptIconCss="e-icons e-user"
            responseIconCss="e-icons e-assistview-icon"
            showClearButton={true}
            enableScrollToBottom={true}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Globalization and Localization

### Locale Property

The `locale` property sets the culture and language for the component. It overrides the global culture setting.

**Type:** `string`  
**Default:** `'en-US'` (English - United States)

```tsx
import { AIAssistViewComponent, L10n } from '@syncfusion/ej2-react-interactive-chat';
import { loadCldr, setCulture, setCurrencyCode } from '@syncfusion/ej2-base';
import React from 'react';

// Load culture data (required for non-English locales)
// import numberingSystems from 'cldr-data/supplemental/numberingSystems.json';
// import gregorian from 'cldr-data/main/de/ca-gregorian.json';
// import numbers from 'cldr-data/main/de/numbers.json';
// import timeZoneNames from 'cldr-data/main/de/timeZoneNames.json';

// loadCldr(numberingSystems, gregorian, numbers, timeZoneNames);

// Set localized text
L10n.load({
    'de': {
        'aiassistview': {
            'placeholder': 'Geben Sie Ihre Nachricht ein...',
            'send': 'Senden',
            'clear': 'Löschen',
            'copy': 'Kopieren',
            'like': 'Gefällt mir',
            'dislike': 'Gefällt mir nicht'
        }
    }
});

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            locale="de"  // German locale
        />
    );
}

export default App;
```

### Common Locale Values

```tsx
locale="en-US"  // English - United States (default)
locale="en-GB"  // English - United Kingdom
locale="de-DE"  // German - Germany
locale="fr-FR"  // French - France
locale="es-ES"  // Spanish - Spain
locale="it-IT"  // Italian - Italy
locale="ja-JP"  // Japanese - Japan
locale="zh-CN"  // Chinese - Simplified
locale="zh-TW"  // Chinese - Traditional
locale="ko-KR"  // Korean - Korea
locale="pt-BR"  // Portuguese - Brazil
locale="ar-SA"  // Arabic - Saudi Arabia
locale="ru-RU"  // Russian - Russia
```

### Spanish Localization Example

```tsx
import { AIAssistViewComponent, L10n } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

L10n.load({
    'es': {
        'aiassistview': {
            'placeholder': 'Escribe tu mensaje aquí...',
            'send': 'Enviar',
            'clear': 'Borrar',
            'copy': 'Copiar',
            'like': 'Me gusta',
            'dislike': 'No me gusta',
            'promptSuggestionsHeader': 'Sugerencias'
        }
    }
});

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            locale="es"
            promptPlaceholder="Escribe tu pregunta..."
            promptSuggestionsHeader="Prueba preguntar:"
            promptSuggestions={[
                '¿Qué puedes hacer?',
                'Ayúdame con algo',
                '¿Cómo empiezo?'
            ]}
        />
    );
}

export default App;
```

### Dynamic Locale Switching

```tsx
import { AIAssistViewComponent, L10n } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

// Load multiple locales
L10n.load({
    'en': {
        'aiassistview': {
            'placeholder': 'Type your message...',
            'send': 'Send'
        }
    },
    'fr': {
        'aiassistview': {
            'placeholder': 'Tapez votre message...',
            'send': 'Envoyer'
        }
    },
    'de': {
        'aiassistview': {
            'placeholder': 'Geben Sie Ihre Nachricht ein...',
            'send': 'Senden'
        }
    }
});

function App() {
    const [currentLocale, setCurrentLocale] = useState('en');

    return (
        <div>
            <select value={currentLocale} onChange={(e) => setCurrentLocale(e.target.value)}>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
            </select>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                locale={currentLocale}
            />
        </div>
    );
}

export default App;
```

## Right-to-Left (RTL) Support

### enableRtl Property

Enable right-to-left rendering for RTL languages (Arabic, Hebrew, etc.):

**Type:** `boolean`  
**Default:** `false`

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            enableRtl={true}
            locale="ar-SA"  // Arabic locale
            promptPlaceholder="اكتب رسالتك هنا..."
        />
    );
}

export default App;
```

### Arabic Language Example

```tsx
import { AIAssistViewComponent, L10n } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

L10n.load({
    'ar': {
        'aiassistview': {
            'placeholder': 'اكتب رسالتك...',
            'send': 'إرسال',
            'clear': 'مسح',
            'copy': 'نسخ',
            'like': 'إعجاب',
            'dislike': 'عدم إعجاب'
        }
    }
});

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            enableRtl={true}
            locale="ar"
            promptSuggestions={[
                'ماذا يمكنك أن تفعل؟',
                'ساعدني في شيء ما',
                'كيف أبدأ؟'
            ]}
        />
    );
}

export default App;
```

### Hebrew Language Example

```tsx
L10n.load({
    'he': {
        'aiassistview': {
            'placeholder': 'הקלד את ההודעה שלך...',
            'send': 'שלח',
            'clear': 'נקה',
            'copy': 'העתק'
        }
    }
});

<AIAssistViewComponent 
    id="aiAssistView"
    enableRtl={true}
    locale="he"
/>
```

### Dynamic RTL Toggle

```tsx
import React, { useState } from 'react';

function App() {
    const [isRtl, setIsRtl] = useState(false);
    const [locale, setLocale] = useState('en');

    const toggleRtl = () => {
        if (!isRtl) {
            setIsRtl(true);
            setLocale('ar');
        } else {
            setIsRtl(false);
            setLocale('en');
        }
    };

    return (
        <div>
            <button onClick={toggleRtl}>
                {isRtl ? 'Switch to LTR (English)' : 'Switch to RTL (Arabic)'}
            </button>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                enableRtl={isRtl}
                locale={locale}
            />
        </div>
    );
}
```

## State Persistence

### enablePersistence Property

Enable automatic persistence of component state across browser sessions:

**Type:** `boolean`  
**Default:** `false`

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            enablePersistence={true}  // Automatically saves and restores state
        />
    );
}

export default App;
```

### What Gets Persisted

When `enablePersistence` is enabled, the following state is automatically saved:
- Conversation history (prompts and responses)
- Current prompt text
- Active view index
- Component settings and preferences

### Persistence Key

The component uses the `id` property as the persistence key. Different IDs will have separate persisted states:

```tsx
// Chat 1 - has its own persisted state
<AIAssistViewComponent 
    id="chat-support"
    enablePersistence={true}
/>

// Chat 2 - has separate persisted state
<AIAssistViewComponent 
    id="chat-assistant"
    enablePersistence={true}
/>
```

### Manual State Persistence

For more control, implement custom persistence:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useEffect } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    // Load persisted state on mount
    useEffect(() => {
        const savedState = localStorage.getItem('ai-chat-state');
        if (savedState && assistInstance.current) {
            const state = JSON.parse(savedState);
            assistInstance.current.prompts = state.prompts || [];
        }
    }, []);

    // Save state on every prompt
    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
            
            // Save state
            const state = {
                prompts: assistInstance.current?.prompts,
                timestamp: new Date().toISOString()
            };
            localStorage.setItem('ai-chat-state', JSON.stringify(state));
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

### Clear Persisted State

```tsx
const clearPersistedData = () => {
    // Clear component's persisted data
    localStorage.removeItem('aiAssistView');  // Uses component ID as key
    
    // Or clear all localStorage
    localStorage.clear();
    
    // Reload to apply
    window.location.reload();
};

<button onClick={clearPersistedData}>Clear Saved Data</button>
```

### Persistence with Session Storage

Use sessionStorage instead of localStorage for session-only persistence:

```tsx
import React, { useRef, useEffect } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    useEffect(() => {
        // Load from sessionStorage (cleared when browser closes)
        const saved = sessionStorage.getItem('chat-session');
        if (saved && assistInstance.current) {
            assistInstance.current.prompts = JSON.parse(saved);
        }
        
        // Save on page unload
        const handleUnload = () => {
            const prompts = assistInstance.current?.prompts;
            sessionStorage.setItem('chat-session', JSON.stringify(prompts));
        };
        
        window.addEventListener('beforeunload', handleUnload);
        return () => window.removeEventListener('beforeunload', handleUnload);
    }, []);

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
        />
    );
}
```

### Combining All Globalization Features

```tsx
import { AIAssistViewComponent, L10n } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

L10n.load({
    'ar': {
        'aiassistview': {
            'placeholder': 'اكتب رسالتك...',
            'send': 'إرسال'
        }
    },
    'he': {
        'aiassistview': {
            'placeholder': 'הקלד הודעה...',
            'send': 'שלח'
        }
    },
    'en': {
        'aiassistview': {
            'placeholder': 'Type message...',
            'send': 'Send'
        }
    }
});

function App() {
    const [config, setConfig] = useState({
        locale: 'en',
        enableRtl: false,
        enablePersistence: true
    });

    const changeLanguage = (lang: string) => {
        const rtlLanguages = ['ar', 'he'];
        setConfig({
            ...config,
            locale: lang,
            enableRtl: rtlLanguages.includes(lang)
        });
    };

    return (
        <div>
            <select onChange={(e) => changeLanguage(e.target.value)} value={config.locale}>
                <option value="en">English</option>
                <option value="ar">العربية (Arabic)</option>
                <option value="he">עברית (Hebrew)</option>
            </select>
            
            <label>
                <input 
                    type="checkbox" 
                    checked={config.enablePersistence}
                    onChange={(e) => setConfig({...config, enablePersistence: e.target.checked})}
                />
                Save conversation history
            </label>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                locale={config.locale}
                enableRtl={config.enableRtl}
                enablePersistence={config.enablePersistence}
            />
        </div>
    );
}

export default App;
```

## Configuration Best Practices

**Use meaningful default prompts**: Set prompt text that guides users  
**Provide clear suggestions**: Help users understand what they can ask  
**Consistent avatars**: Use recognizable icons for user and AI  
**Show clear buttons**: Help users manage conversation state  
**Enable scroll feedback**: Especially for long conversations  
**Use refs effectively**: For advanced state management and method calls
