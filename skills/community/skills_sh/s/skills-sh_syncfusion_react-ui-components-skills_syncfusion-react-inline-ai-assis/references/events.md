# Events

## Table of Contents
- [Overview](#overview)
- [created Event](#created-event)
- [promptRequest Event](#promptrequest-event)
- [open Event](#open-event)
- [close Event](#close-event)
- [Event Handler Patterns](#event-handler-patterns)
- [Complete Examples](#complete-examples)

## Overview

The Inline AI Assist component provides several lifecycle and interaction events that you can hook into to implement custom logic. These events are triggered at different points in the component's lifecycle and user interactions.

## created Event

Triggered when the component finishes rendering and initialization.

### When It Fires

After all DOM elements are created, CSS applied, and component is ready for interaction.

### Event Signature

```tsx
type CreatedEventHandler = () => void;
```

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const handleCreated = () => {
        console.log('Inline AI Assist component is ready');
        // Initialize third-party libraries
        // Set up analytics tracking
        // Fetch initial data
    };

    return (
        <InlineAIAssistComponent created={handleCreated} />
    );
};

export default App;
```

### Use Cases

1. **Initialize analytics:** Track component load
2. **Set up listeners:** Attach to parent elements
3. **Load saved state:** Restore user preferences
4. **Validate setup:** Confirm AI service connection

### Example: Initialize with Data

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleCreated = () => {
        // Load user's saved prompts
        loadSavedPrompts().then(prompts => {
            console.log('Prompts loaded:', prompts.length);
        });

        // Initialize AI service
        initializeAIService();

        // Set focus to input
        const inputElement = document.querySelector('.e-aiassist-input');
        if (inputElement) {
            (inputElement as HTMLElement).focus();
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            created={handleCreated}
        />
    );
};
```

## promptRequest Event

Triggered when the user submits a prompt (clicks send or presses Enter).

### When It Fires

After user enters text and triggers send action (built-in send button or Enter key).

### Event Arguments

```tsx
interface InlinePromptRequestEventArgs {
    prompt: string;              // The user's prompt text
    cancel: boolean;             // Set to true to cancel the request
}
```

### Basic Usage

```tsx
import { InlineAIAssistComponent, InlinePromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        console.log('User prompt:', args.prompt);

        // Simulate AI processing
        setTimeout(() => {
            const response = 'AI-generated response';
            assistRef.current?.addResponse(response);
        }, 1000);
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Use Cases

1. **Send to AI service:** Forward prompt to OpenAI, Gemini, etc.
2. **Validate prompt:** Check for content policies
3. **Add context:** Augment prompt with additional data
4. **Track analytics:** Log user queries
5. **Cancel request:** Block certain prompts

### Example: Validation and Context

```tsx
const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
    // Validate prompt content
    if (args.prompt.length < 5) {
        args.cancel = true;
        showNotification('Prompt must be at least 5 characters');
        return;
    }

    // Add context to prompt
    const context = 'Context information...';
    const enrichedPrompt = `${context}\n\nUser request: ${args.prompt}`;

    // Send to AI service
    callAIService(enrichedPrompt).then(response => {
        assistRef.current?.addResponse(response);
    });
};
```

### Example: Implement Prompt History

```tsx
const App: React.FC = () => {
    const [promptHistory, setPromptHistory] = React.useState<string[]>([]);
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        // Add to history
        setPromptHistory(prev => [args.prompt, ...prev]);

        // Save to database
        savePromptToDatabase(args.prompt);

        // Process with AI
        processWithAI(args.prompt).then(response => {
            assistRef.current?.addResponse(response);
        });
    };

    return (
        <div>
            <InlineAIAssistComponent
                ref={assistRef}
                promptRequest={handlePromptRequest}
            />
            <div>
                <h3>History</h3>
                {promptHistory.map((p, i) => (
                    <p key={i}>{p}</p>
                ))}
            </div>
        </div>
    );
};
```

## open Event

Triggered when the component popup opens.

### When It Fires

When the popup is opened (via user interaction, programmatic call, or component initialization).

### Event Arguments

```tsx
import { OpenEventArgs } from '@syncfusion/ej2-popups';

interface OpenEventArgs {
    name: 'open';
    element: HTMLElement;        // The popup element
}
```

### Basic Usage

```tsx
import { InlineAIAssistComponent, OpenEventArgs } from '@syncfusion/ej2-popups';
import React from 'react';

const App: React.FC = () => {
    const handlePopupOpen = (args: OpenEventArgs) => {
        console.log('Popup opened');
        // Focus input when popup opens
        const input = args.element?.querySelector('textarea');
        if (input) {
            (input as HTMLElement).focus();
        }
    };

    return (
        <InlineAIAssistComponent open={handlePopupOpen} />
    );
};

export default App;
```

### Use Cases

1. **Focus input:** Set focus to prompt field
2. **Track analytics:** Log popup open events
3. **Initialize data:** Load suggestions when popup opens
4. **Adjust layout:** Reposition if needed

### Example: Load Suggestions on Open

```tsx
const handlePopupOpen = async (args: OpenEventArgs) => {
    // Load recent prompts
    const suggestions = await loadSuggestions();
    console.log('Suggestions loaded:', suggestions);

    // Track analytics
    trackEvent('assist_popup_opened');

    // Announce for accessibility
    announceToScreenReader('AI Assist popup opened');
};
```

## close Event

Triggered when the component popup closes.

### When It Fires

When the popup is closed (user clicks outside, presses Escape, or programmatic call).

### Event Arguments

```tsx
import { CloseEventArgs } from '@syncfusion/ej2-popups';

interface CloseEventArgs {
    name: 'close';
    element: HTMLElement;        // The popup element
}
```

### Basic Usage

```tsx
import { InlineAIAssistComponent, CloseEventArgs } from '@syncfusion/ej2-popups';
import React from 'react';

const App: React.FC = () => {
    const handlePopupClose = (args: CloseEventArgs) => {
        console.log('Popup closed');
        // Clean up any pending operations
    };

    return (
        <InlineAIAssistComponent close={handlePopupClose} />
    );
};

export default App;
```

### Use Cases

1. **Cleanup:** Clear temporary data
2. **Analytics:** Track popup close events
3. **Save state:** Persist any unsaved changes
4. **Reset UI:** Clear highlights or selections

## Event Handler Patterns

### Pattern 1: Multiple Event Handlers

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleCreated = () => {
        console.log('Component ready');
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        console.log('Prompt submitted:', args.prompt);
    };

    const handlePopupOpen = (args: OpenEventArgs) => {
        console.log('Popup opened');
    };

    const handlePopupClose = (args: CloseEventArgs) => {
        console.log('Popup closed');
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            created={handleCreated}
            promptRequest={handlePromptRequest}
            open={handlePopupOpen}
            close={handlePopupClose}
        />
    );
};
```

### Pattern 2: Event Aggregation

```tsx
const handleComponentEvent = (eventType: string, eventData?: any) => {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] Event: ${eventType}`, eventData);

    // Send to analytics
    trackEvent(eventType, eventData);
};

const inlineAiAssistProps = {
    created: () => handleComponentEvent('created'),
    promptRequest: (args: InlinePromptRequestEventArgs) =>
        handleComponentEvent('promptRequest', { prompt: args.prompt }),
    open: () => handleComponentEvent('open'),
    close: () => handleComponentEvent('close')
};

<InlineAIAssistComponent {...inlineAiAssistProps} />
```

### Pattern 3: Conditional Logic

```tsx
const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
    // Cancel if user not authenticated
    if (!isAuthenticated()) {
        args.cancel = true;
        showLoginDialog();
        return;
    }

    // Process normally
    processPrompt(args.prompt);
};
```

## Complete Examples

### Example 1: Content Generation Workflow

```tsx
const ContentGenerator: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [isProcessing, setIsProcessing] = React.useState(false);

    const handleCreated = () => {
        console.log('Content Generator initialized');
        initializeTheme();
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        setIsProcessing(true);

        // Send prompt to API
        generateContent(args.prompt)
            .then(response => {
                assistRef.current?.addResponse(response);
            })
            .catch(error => {
                assistRef.current?.addResponse(`Error: ${error.message}`);
            })
            .finally(() => {
                setIsProcessing(false);
            });
    };

    const handlePopupOpen = () => {
        // Focus input
        const input = document.querySelector('.e-aiassist-input') as HTMLElement;
        input?.focus();
    };

    const handlePopupClose = () => {
        console.log('Content generator closed');
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            created={handleCreated}
            promptRequest={handlePromptRequest}
            open={handlePopupOpen}
            close={handlePopupClose}
        />
    );
};
```

### Example 2: Analytics and Monitoring

```tsx
const MonitoredAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const startTimeRef = React.useRef<number>(0);

    const handleCreated = () => {
        analytics.log('assist_created', { timestamp: Date.now() });
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        startTimeRef.current = Date.now();
        analytics.log('prompt_submitted', {
            promptLength: args.prompt.length,
            timestamp: Date.now()
        });

        processPrompt(args.prompt).then(response => {
            const duration = Date.now() - startTimeRef.current;
            assistRef.current?.addResponse(response);
            analytics.log('response_generated', {
                duration,
                responseLength: response.length
            });
        });
    };

    const handlePopupOpen = () => {
        analytics.log('popup_opened', { timestamp: Date.now() });
    };

    const handlePopupClose = () => {
        analytics.log('popup_closed', { timestamp: Date.now() });
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            created={handleCreated}
            promptRequest={handlePromptRequest}
            open={handlePopupOpen}
            close={handlePopupClose}
        />
    );
};
```

### Example 3: Multi-Language Support

```tsx
const MultiLanguageAssistant: React.FC = () => {
    const [language, setLanguage] = React.useState('en');
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleCreated = () => {
        // Load localized strings
        loadLocalization(language);
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        // Add language context to prompt
        const enhancedPrompt = `Language: ${language}\n\n${args.prompt}`;
        
        callAI(enhancedPrompt).then(response => {
            assistRef.current?.addResponse(response);
        });
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            created={handleCreated}
            promptRequest={handlePromptRequest}
        />
    );
};
```

## Best Practices

1. **Error Handling:** Wrap event handlers in try-catch
2. **Async Operations:** Use async/await for API calls
3. **Cleanup:** Remove listeners on component unmount
4. **Logging:** Track important events for debugging
5. **Performance:** Keep event handlers lightweight
6. **User Feedback:** Show loading states during processing
7. **Analytics:** Log user interactions for insights
8. **Accessibility:** Announce major events to screen readers
