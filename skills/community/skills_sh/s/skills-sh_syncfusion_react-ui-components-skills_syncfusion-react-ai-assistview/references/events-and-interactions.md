# Events and Interactions

## Table of Contents
- [Component Lifecycle Events](#component-lifecycle-events)
- [Prompt Request Event](#prompt-request-event)
- [Prompt Changed Event](#prompt-changed-event)
- [Event Data Structures](#event-data-structures)
- [Custom Event Workflows](#custom-event-workflows)
- [AI Service Integration via Events](#ai-service-integration-via-events)

## Component Lifecycle Events

### Created Event

The `created` event triggers when the AI AssistView component finishes rendering:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const handleCreated = () => {
        console.log('Component initialized and ready to use');
        // Initialize other features, load data, etc.
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            created={handleCreated}
        />
    );
}

export default App;
```

### Use Cases for Created Event

```tsx
const handleCreated = () => {
    // Load saved conversations
    const saved = localStorage.getItem('conversation');
    if (saved) {
        assistInstance.current.prompts = JSON.parse(saved);
    }
    
    // Initialize third-party libraries
    // Load user preferences
    // Set up event listeners
    // Track component creation for analytics
};
```

## Prompt Request Event

### Overview

The `promptRequest` event fires when a user submits a prompt. This is the primary event for handling user input:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        console.log('User prompt:', args.prompt);
        console.log('Event args:', args);
        
        // Process the prompt
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
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

### Event Data (PromptRequestEventArgs)

The `PromptRequestEventArgs` interface provides comprehensive information about the prompt submission:

```tsx
interface PromptRequestEventArgs {
    attachedFiles: FileInfo[];           // Files attached with the prompt
    cancel: boolean;                     // Set to true to cancel the prompt
    name: string;                        // Event name ('promptRequest')
    prompt: string;                      // The user's input text
    promptSuggestions: string[];         // Current prompt suggestions
    responseToolbarItems: ToolbarItemModel[];  // Toolbar items for response
}
```

### Accessing All Event Properties

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // User's prompt text
    console.log('Prompt:', args.prompt);
    
    // Attached files (if any)
    console.log('Files:', args.attachedFiles);
    if (args.attachedFiles && args.attachedFiles.length > 0) {
        args.attachedFiles.forEach(file => {
            console.log(`- ${file.name} (${file.size} bytes)`);
        });
    }
    
    // Event name
    console.log('Event name:', args.name);  // 'promptRequest'
    
    // Current suggestions
    console.log('Suggestions:', args.promptSuggestions);
    
    // Response toolbar items
    console.log('Response toolbar:', args.responseToolbarItems);
};
```

### Canceling Prompt Submission

Use the `cancel` property to prevent prompt processing:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // Validate prompt
    if (!args.prompt || args.prompt.trim().length === 0) {
        args.cancel = true;
        alert('Please enter a prompt');
        return;
    }
    
    if (args.prompt.length < 3) {
        args.cancel = true;
        alert('Prompt is too short');
        return;
    }
    
    if (args.prompt.length > 1000) {
        args.cancel = true;
        alert('Prompt is too long (max 1000 characters)');
        return;
    }
    
    // Check for inappropriate content
    const bannedWords = ['spam', 'abuse'];
    if (bannedWords.some(word => args.prompt.toLowerCase().includes(word))) {
        args.cancel = true;
        alert('Prompt contains inappropriate content');
        return;
    }
    
    // If validation passes, process normally
    processPrompt(args.prompt);
};
```

### Modifying Prompt Suggestions Dynamically

Update suggestions based on the prompt:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const prompt = args.prompt.toLowerCase();
    
    // Modify suggestions based on prompt content
    if (prompt.includes('code')) {
        args.promptSuggestions = [
            'Show me code examples',
            'Explain this code',
            'Debug this code'
        ];
    } else if (prompt.includes('help')) {
        args.promptSuggestions = [
            'How do I get started?',
            'Show documentation',
            'Contact support'
        ];
    }
    
    // Process the prompt
    setTimeout(() => {
        assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
    }, 1000);
};
```

### Customizing Response Toolbar Dynamically

Modify toolbar items for the response based on prompt content:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // Default toolbar items
    const defaultItems = [
        { iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
        { iconCss: 'e-icons e-assist-like', tooltip: 'Like' },
        { iconCss: 'e-icons e-assist-dislike', tooltip: 'Dislike' }
    ];
    
    // Add code-specific tools if prompt is about code
    if (args.prompt.toLowerCase().includes('code')) {
        args.responseToolbarItems = [
            ...defaultItems,
            { iconCss: 'e-icons e-download', tooltip: 'Download Code' },
            { iconCss: 'e-icons e-play', tooltip: 'Run Code' }
        ];
    } else {
        args.responseToolbarItems = defaultItems;
    }
    
    // Process prompt
    processPrompt(args.prompt);
};
```

### Working with Attached Files

Access and validate attached files:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, FileInfo } from '@syncfusion/ej2-react-interactive-chat';

const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const files: FileInfo[] = args.attachedFiles || [];
    
    if (files.length === 0) {
        // No files attached
        processTextOnlyPrompt(args.prompt);
        return;
    }
    
    // Validate file types
    const allowedTypes = ['image/png', 'image/jpeg', 'application/pdf'];
    const invalidFiles = files.filter(f => !allowedTypes.includes(f.type));
    
    if (invalidFiles.length > 0) {
        args.cancel = true;
        alert(`Invalid file types: ${invalidFiles.map(f => f.name).join(', ')}`);
        return;
    }
    
    // Validate file sizes
    const maxSize = 5 * 1024 * 1024; // 5 MB
    const oversizedFiles = files.filter(f => f.size > maxSize);
    
    if (oversizedFiles.length > 0) {
        args.cancel = true;
        alert(`Files too large: ${oversizedFiles.map(f => f.name).join(', ')}`);
        return;
    }
    
    // Process prompt with files
    processPromptWithFiles(args.prompt, files);
};
```

### Complete Example with All Properties

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        console.log('=== Prompt Request Event ===');
        console.log('Event name:', args.name);
        console.log('Prompt text:', args.prompt);
        console.log('Files attached:', args.attachedFiles?.length || 0);
        console.log('Current suggestions:', args.promptSuggestions);
        console.log('Response toolbar items:', args.responseToolbarItems?.length || 0);
        
        // Validation
        if (args.prompt.length > 1000) {
            args.cancel = true;
            assistInstance.current?.addPromptResponse('⚠️ Prompt too long');
            return;
        }
        
        // Check for files
        if (args.attachedFiles && args.attachedFiles.length > 0) {
            const fileNames = args.attachedFiles.map(f => f.name).join(', ');
            console.log('Processing with files:', fileNames);
        }
        
        // Modify suggestions for next interaction
        if (args.prompt.toLowerCase().includes('help')) {
            args.promptSuggestions = [
                'Documentation',
                'Examples',
                'Support'
            ];
        }
        
        // Customize response toolbar
        args.responseToolbarItems = [
            { iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
            { iconCss: 'e-icons e-refresh', tooltip: 'Regenerate' }
        ];
        
        // Process prompt
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            enableAttachments={true}
        />
    );
}

export default App;
```

### Practical Examples

**Handle Different Prompt Types:**

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const prompt = args.prompt.toLowerCase();
    
    let response = '';
    
    if (prompt.includes('hello')) {
        response = 'Hello! How can I help you?';
    } else if (prompt.includes('help')) {
        response = 'I can assist with various tasks. What do you need?';
    } else if (prompt.includes('bye')) {
        response = 'Goodbye! Have a great day!';
    } else {
        response = 'I received your prompt: ' + args.prompt;
    }
    
    assistInstance.current?.addPromptResponse(response);
};
```

**Validate Before Processing:**

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // Validate prompt
    if (!args.prompt || args.prompt.trim().length === 0) {
        assistInstance.current?.addPromptResponse('Please enter a prompt');
        return;
    }
    
    if (args.prompt.length > 1000) {
        assistInstance.current?.addPromptResponse('Prompt is too long');
        return;
    }
    
    // Safe to process
    processPrompt(args.prompt);
};
```

## Prompt Changed Event

### Overview

The `promptChanged` event fires whenever the prompt text is modified (as user types). It provides detailed information about the change through `PromptChangedEventArgs`.

**Type:** `EmitType<PromptChangedEventArgs>`

```tsx
import { AIAssistViewComponent, PromptChangedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptChanged = (args: PromptChangedEventArgs) => {
        console.log('Current value:', args.value);
        console.log('Previous value:', args.previousValue);
        console.log('Text area element:', args.element);
        console.log('DOM event:', args.event);
        console.log('Event name:', args.name);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptChanged={handlePromptChanged}
        />
    );
}

export default App;
```

### PromptChangedEventArgs Properties

The event arguments provide comprehensive information about the change:

```tsx
interface PromptChangedEventArgs {
    element: HTMLElement;      // The HTML element of the text area container
    event: Event;              // The underlying DOM event that triggered the change
    name: string;              // Event name ('promptChanged')
    previousValue: string;     // The prompt text before the change
    value: string;             // The current prompt text after the change
}
```

### Accessing Event Properties

```tsx
const handlePromptChanged = (args: PromptChangedEventArgs) => {
    // Current text
    const currentText = args.value;
    console.log('Current:', currentText);
    
    // Previous text
    const previousText = args.previousValue;
    console.log('Previous:', previousText);
    
    // Calculate what changed
    const added = currentText.length - previousText.length;
    console.log(`Characters ${added > 0 ? 'added' : 'removed'}:`, Math.abs(added));
    
    // Access the DOM element
    const textArea = args.element;
    console.log('Element:', textArea);
    
    // Access the original event
    const domEvent = args.event;
    console.log('Event type:', domEvent.type);
};
```

### Use Cases

**Real-time Character Count:**

```tsx
import { AIAssistViewComponent, PromptChangedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

function App() {
    const [charCount, setCharCount] = useState(0);
    const [wordCount, setWordCount] = useState(0);

    const handlePromptChanged = (args: PromptChangedEventArgs) => {
        const text = args.value;
        setCharCount(text.length);
        setWordCount(text.trim().split(/\s+/).filter(Boolean).length);
    };

    return (
        <div>
            <div className="stats-bar">
                <span>Characters: {charCount}/1000</span>
                <span>Words: {wordCount}</span>
            </div>
            <AIAssistViewComponent 
                id="aiAssistView"
                promptChanged={handlePromptChanged}
            />
        </div>
    );
}
```

**Detect Specific Keywords:**

```tsx
const handlePromptChanged = (args: PromptChangedEventArgs) => {
    const text = args.value.toLowerCase();
    const previousText = args.previousValue.toLowerCase();
    
    // Check if user typed a command
    if (text.startsWith('/') && !previousText.startsWith('/')) {
        console.log('Command mode activated');
        showCommandSuggestions();
    }
    
    // Detect @mentions
    const mentions = text.match(/@\w+/g);
    if (mentions) {
        console.log('Mentions detected:', mentions);
        showMentionSuggestions(mentions);
    }
};
```

**Auto-Save Draft:**

```tsx
import { AIAssistViewComponent, PromptChangedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const draftTimeoutRef = useRef<NodeJS.Timeout>();

    const handlePromptChanged = (args: PromptChangedEventArgs) => {
        // Clear previous timeout
        if (draftTimeoutRef.current) {
            clearTimeout(draftTimeoutRef.current);
        }
        
        // Save draft after 2 seconds of no typing
        draftTimeoutRef.current = setTimeout(() => {
            localStorage.setItem('promptDraft', args.value);
            console.log('Draft saved:', args.value);
        }, 2000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            promptChanged={handlePromptChanged}
        />
    );
}
```

**Validate Input in Real-Time:**

```tsx
import React, { useState } from 'react';

function App() {
    const [validationMessage, setValidationMessage] = useState('');

    const handlePromptChanged = (args: PromptChangedEventArgs) => {
        const text = args.value;
        
        // Validation rules
        if (text.length > 1000) {
            setValidationMessage('⚠️ Prompt is too long (max 1000 characters)');
        } else if (text.length > 0 && text.length < 3) {
            setValidationMessage('⚠️ Prompt is too short (min 3 characters)');
        } else if (text.includes('<script>')) {
            setValidationMessage('⚠️ Invalid characters detected');
        } else {
            setValidationMessage('');
        }
    };

    return (
        <div>
            {validationMessage && (
                <div className="validation-message">{validationMessage}</div>
            )}
            <AIAssistViewComponent 
                id="aiAssistView"
                promptChanged={handlePromptChanged}
            />
        </div>
    );
}
```

**Track Typing Speed:**

```tsx
function App() {
    const lastChangeTimeRef = useRef<number>(Date.now());
    const [typingSpeed, setTypingSpeed] = useState(0);

    const handlePromptChanged = (args: PromptChangedEventArgs) => {
        const now = Date.now();
        const timeDiff = now - lastChangeTimeRef.current;
        
        if (timeDiff > 0) {
            const charsAdded = Math.abs(args.value.length - args.previousValue.length);
            const speed = (charsAdded / timeDiff) * 1000 * 60; // chars per minute
            setTypingSpeed(Math.round(speed));
        }
        
        lastChangeTimeRef.current = now;
    };

    return (
        <div>
            <div>Typing speed: {typingSpeed} CPM</div>
            <AIAssistViewComponent 
                id="aiAssistView"
                promptChanged={handlePromptChanged}
            />
        </div>
    );
}
```

**Compare Previous and Current:**

```tsx
const handlePromptChanged = (args: PromptChangedEventArgs) => {
    const current = args.value;
    const previous = args.previousValue;
    
    // Detect what changed
    if (current.length > previous.length) {
        const added = current.slice(previous.length);
        console.log('Added:', added);
    } else if (current.length < previous.length) {
        console.log('Characters removed:', previous.length - current.length);
    }
    
    // Detect specific actions
    if (previous && !current) {
        console.log('Text cleared');
    }
    
    if (!previous && current) {
        console.log('Started typing');
    }
};
```

## Event Data Structures

### PromptRequestEventArgs Interface

```tsx
interface PromptRequestEventArgs {
    prompt: string;           // User's prompt text
    isInteraction?: boolean;  // User-triggered vs programmatic
    [key: string]: any;       // Other properties
}
```

### Working with Event Arguments

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    // Access prompt text
    const userInput = args.prompt;
    
    // Check if it's a user interaction
    const isUserTriggered = args.isInteraction !== false;
    
    // Access additional properties if available
    Object.keys(args).forEach(key => {
        console.log(`${key}: ${args[key]}`);
    });
};
```

## Custom Event Workflows

### Multi-Step Workflow

```tsx
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        // Step 1: Validate
        if (!validatePrompt(args.prompt)) {
            assistInstance.current?.addPromptResponse('Invalid prompt');
            return;
        }
        
        // Step 2: Sanitize
        const cleanPrompt = sanitizeInput(args.prompt);
        
        // Step 3: Process
        const result = await processWithAI(cleanPrompt);
        
        // Step 4: Format response
        const formattedResponse = formatResponse(result);
        
        // Step 5: Display
        assistInstance.current?.addPromptResponse(formattedResponse);
        
        // Step 6: Log for analytics
        logInteraction(args.prompt, formattedResponse);
        
    } catch (error) {
        console.error('Error processing prompt:', error);
        assistInstance.current?.addPromptResponse('An error occurred. Please try again.');
    }
};
```

### Conditional Workflow Based on Prompt Type

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const prompt = args.prompt;
    
    if (prompt.startsWith('/')) {
        // Command handling
        handleCommand(prompt);
    } else if (prompt.includes('@')) {
        // Mention handling
        handleMention(prompt);
    } else if (prompt.includes('?')) {
        // Question handling
        handleQuestion(prompt);
    } else {
        // Regular prompt
        handleRegularPrompt(prompt);
    }
};
```

## AI Service Integration via Events

### Basic AI Integration

```tsx
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        // Show loading state
        assistInstance.current?.addPromptResponse('Processing...');
        
        // Call AI service
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY'
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: args.prompt }],
                temperature: 0.7
            })
        });
        
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        // Display response
        assistInstance.current?.addPromptResponse(aiResponse);
        
    } catch (error) {
        assistInstance.current?.addPromptResponse('Error: ' + error.message);
    }
};
```

### Streaming Response from AI

```tsx
import { marked } from 'marked';

const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_KEY'
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: args.prompt }],
                stream: true
            })
        });
        
        const reader = response.body.getReader();
        let fullResponse = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = new TextDecoder().decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        const content = data.choices[0].delta.content;
                        
                        if (content) {
                            fullResponse += content;
                            // Update UI with partial response
                            const htmlResponse = marked.parse(fullResponse);
                            assistInstance.current?.addPromptResponse(htmlResponse);
                        }
                    } catch (e) {
                        // Ignore parse errors
                    }
                }
            }
        }
        
    } catch (error) {
        assistInstance.current?.addPromptResponse('Error: ' + error.message);
    }
};
```

### Error Handling in Events

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    try {
        // Validate input
        if (!args.prompt?.trim()) {
            throw new Error('Prompt cannot be empty');
        }
        
        // Process prompt
        processPrompt(args.prompt);
        
    } catch (error: any) {
        // Show user-friendly error
        const errorMessage = error.message || 'An unexpected error occurred';
        assistInstance.current?.addPromptResponse(
            `<div class="error-message">${errorMessage}</div>`
        );
        
        // Log error for debugging
        console.error('Prompt handling error:', error);
    }
};
```

## Stop Responding Event

### stopRespondingClick Event

The `stopRespondingClick` event triggers when users click the "Stop Responding" button during an active prompt request. This is essential for canceling long-running AI operations.

**Type:** `EmitType<StopRespondingEventArgs>`

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, StopRespondingEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const abortControllerRef = useRef<AbortController | null>(null);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        setIsProcessing(true);
        
        // Create abort controller for cancellation
        abortControllerRef.current = new AbortController();
        
        try {
            const response = await fetch('https://api.example.com/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: args.prompt }),
                signal: abortControllerRef.current.signal  // Pass abort signal
            });
            
            const data = await response.json();
            assistInstance.current?.addPromptResponse(data.response);
            
        } catch (error: any) {
            if (error.name === 'AbortError') {
                assistInstance.current?.addPromptResponse(
                    '<div class="cancelled-message">⚠️ Response cancelled by user</div>'
                );
            } else {
                assistInstance.current?.addPromptResponse('Error: ' + error.message);
            }
        } finally {
            setIsProcessing(false);
            abortControllerRef.current = null;
        }
    };

    const handleStopResponding = (args: StopRespondingEventArgs) => {
        console.log('Stop responding clicked');
        console.log('Prompt being cancelled:', args.prompt);
        console.log('Data index:', args.dataIndex);
        
        // Cancel the ongoing request
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        
        setIsProcessing(false);
    };

    return (
        <div>
            <div className="status">
                {isProcessing && <span>⏳ Processing...</span>}
            </div>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                stopRespondingClick={handleStopResponding}
            />
        </div>
    );
}

export default App;
```

### StopRespondingEventArgs Properties

The event arguments provide context about the cancelled operation:

```tsx
interface StopRespondingEventArgs {
    dataIndex: number;    // Index of the prompt in the prompts array
    event: Event;         // Original DOM event
    name: string;         // Event name ('stopRespondingClick')
    prompt: string;       // The prompt text that was being processed
}
```

### Accessing Event Properties

```tsx
const handleStopResponding = (args: StopRespondingEventArgs) => {
    // Get the prompt being cancelled
    const cancelledPrompt = args.prompt;
    console.log('Cancelling prompt:', cancelledPrompt);
    
    // Get the position in conversation
    const promptIndex = args.dataIndex;
    console.log('Prompt index:', promptIndex);
    
    // Access the original DOM event if needed
    const domEvent = args.event;
    console.log('Event type:', domEvent.type);
    
    // Event name
    console.log('Event name:', args.name);  // 'stopRespondingClick'
};
```

### Streaming Response Cancellation

Cancel streaming responses character-by-character:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, StopRespondingEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import { marked } from 'marked';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [isStreaming, setIsStreaming] = useState(false);
    const streamAbortRef = useRef<AbortController | null>(null);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        setIsStreaming(true);
        streamAbortRef.current = new AbortController();
        
        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_KEY'
                },
                body: JSON.stringify({
                    model: 'gpt-3.5-turbo',
                    messages: [{ role: 'user', content: args.prompt }],
                    stream: true
                }),
                signal: streamAbortRef.current.signal
            });

            const reader = response.body?.getReader();
            let fullResponse = '';

            while (reader && !streamAbortRef.current.signal.aborted) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = new TextDecoder().decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ') && !streamAbortRef.current.signal.aborted) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            const content = data.choices[0].delta?.content;
                            
                            if (content) {
                                fullResponse += content;
                                const htmlResponse = marked.parse(fullResponse);
                                assistInstance.current?.addPromptResponse(htmlResponse);
                            }
                        } catch (e) {
                            // Ignore parse errors
                        }
                    }
                }
            }

        } catch (error: any) {
            if (error.name === 'AbortError') {
                console.log('Streaming cancelled');
            }
        } finally {
            setIsStreaming(false);
            streamAbortRef.current = null;
        }
    };

    const handleStopResponding = (args: StopRespondingEventArgs) => {
        console.log('Stopping stream for:', args.prompt);
        
        if (streamAbortRef.current) {
            streamAbortRef.current.abort();
        }
        
        setIsStreaming(false);
        
        // Add cancellation message
        assistInstance.current?.addPromptResponse(
            '<div class="info-message">🛑 Response generation stopped</div>'
        );
    };

    return (
        <div>
            <div className="streaming-indicator">
                {isStreaming && <span className="pulse">● Generating response...</span>}
            </div>
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                stopRespondingClick={handleStopResponding}
            />
        </div>
    );
}

export default App;
```

### Cleanup on Stop

Perform cleanup operations when user cancels:

```tsx
const handleStopResponding = (args: StopRespondingEventArgs) => {
    // Abort API request
    if (abortControllerRef.current) {
        abortControllerRef.current.abort();
    }
    
    // Clear any pending timers
    if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
    }
    
    // Reset loading states
    setIsProcessing(false);
    setProgress(0);
    
    // Log cancellation for analytics
    logEvent('response_cancelled', {
        prompt: args.prompt,
        index: args.dataIndex,
        timestamp: new Date().toISOString()
    });
    
    // Notify user
    showNotification('Response generation cancelled');
};
```

### With Progress Tracking

Track progress and cancel at any point:

```tsx
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [progress, setProgress] = useState(0);
    const shouldContinueRef = useRef(true);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        shouldContinueRef.current = true;
        setProgress(0);
        
        // Simulate long operation
        for (let i = 0; i <= 100 && shouldContinueRef.current; i += 10) {
            setProgress(i);
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        if (shouldContinueRef.current) {
            assistInstance.current?.addPromptResponse('Processing complete!');
            setProgress(0);
        }
    };

    const handleStopResponding = (args: StopRespondingEventArgs) => {
        shouldContinueRef.current = false;
        setProgress(0);
        
        assistInstance.current?.addPromptResponse(
            `<div>Cancelled at ${progress}% progress</div>`
        );
    };

    return (
        <div>
            {progress > 0 && (
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }}>
                        {progress}%
                    </div>
                </div>
            )}
            
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                stopRespondingClick={handleStopResponding}
            />
        </div>
    );
}
```

### Multiple Request Management

Handle cancellation when multiple requests are in flight:

```tsx
function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const activeRequestsRef = useRef<Map<number, AbortController>>(new Map());

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        const requestId = Date.now();
        const abortController = new AbortController();
        
        // Track this request
        activeRequestsRef.current.set(requestId, abortController);
        
        try {
            const response = await fetch('https://api.example.com/chat', {
                method: 'POST',
                body: JSON.stringify({ prompt: args.prompt }),
                signal: abortController.signal
            });
            
            const data = await response.json();
            assistInstance.current?.addPromptResponse(data.response);
            
        } catch (error: any) {
            if (error.name !== 'AbortError') {
                console.error('Request error:', error);
            }
        } finally {
            // Remove from active requests
            activeRequestsRef.current.delete(requestId);
        }
    };

    const handleStopResponding = (args: StopRespondingEventArgs) => {
        // Cancel all active requests
        activeRequestsRef.current.forEach((controller, requestId) => {
            controller.abort();
            console.log(`Cancelled request ${requestId}`);
        });
        
        // Clear the map
        activeRequestsRef.current.clear();
        
        assistInstance.current?.addPromptResponse(
            '<div>All pending requests cancelled</div>'
        );
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            stopRespondingClick={handleStopResponding}
        />
    );
}
```

### Best Practices for Stop Responding

✅ **Always implement AbortController** for fetch requests  
✅ **Clear all timers and intervals** when stopping  
✅ **Update UI state** to reflect cancellation  
✅ **Provide user feedback** about cancellation  
✅ **Log cancellation events** for debugging and analytics  
✅ **Clean up resources** (streams, connections, etc.)  
✅ **Handle partial responses** gracefully  
✅ **Test cancellation scenarios** thoroughly

## Complete Event Integration Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleCreated = () => {
        console.log('Component ready');
        loadSavedConversation();
    };

    const handlePromptChanged = () => {
        // Update UI based on prompt changes
        const currentPrompt = assistInstance.current?.prompt || '';
        console.log('Current text:', currentPrompt);
    };

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        if (isProcessing) return;
        
        setIsProcessing(true);
        try {
            const response = await processUserPrompt(args.prompt);
            assistInstance.current?.addPromptResponse(response);
        } catch (error) {
            assistInstance.current?.addPromptResponse('Error processing request');
        } finally {
            setIsProcessing(false);
        }
    };

    const loadSavedConversation = () => {
        const saved = localStorage.getItem('conversation');
        if (saved) {
            assistInstance.current.prompts = JSON.parse(saved);
        }
    };

    const processUserPrompt = async (prompt: string): Promise<string> => {
        // Implement your logic here
        return 'Response to: ' + prompt;
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            created={handleCreated}
            promptChanged={handlePromptChanged}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Best Practices

**Always validate prompts**: Check for empty, null, or malicious input  
**Handle errors gracefully**: Provide user-friendly error messages  
**Use async/await**: For AI service calls and async operations  
**Optimize performance**: Debounce rapid event triggers if needed  
**Log interactions**: Track prompts and responses for debugging  
**Implement proper state management**: For complex workflows
