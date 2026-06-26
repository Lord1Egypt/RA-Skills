# Methods and APIs

## Public Methods Overview

The AI AssistView component provides several public methods for programmatic interaction:

1. **addPromptResponse()**: Add response to conversation
2. **executePrompt()**: Execute prompt dynamically
3. **scrollToBottom()**: Scroll to latest message
4. **Advanced property access**: Direct state manipulation

## Adding Prompt Response

### addPromptResponse with String

Append a text response to the last prompt:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            // Add simple string response
            assistInstance.current?.addPromptResponse('This is the response text');
        }, 1000);
    };

    const addCustomResponse = () => {
        assistInstance.current?.addPromptResponse('Custom response added');
    };

    return (
        <div>
            <button onClick={addCustomResponse}>Add Response</button>
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

### addPromptResponse with Object

Add complete prompt-response pair:

```tsx
const addCompleteExchange = () => {
    assistInstance.current?.addPromptResponse({
        prompt: "What is React?",
        response: "React is a JavaScript library for building UIs with components.",
        suggestions: [
            "How to use React?",
            "React hooks?"
        ]
    });
};
```

### Add HTML Response

Include formatted content:

```tsx
const addFormattedResponse = () => {
    const htmlResponse = `
        <div class="response-content">
            <h4>Topic</h4>
            <p>This is a <strong>formatted</strong> response.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            <p>Additional information here.</p>
        </div>
    `;
    
    assistInstance.current?.addPromptResponse(htmlResponse);
};
```

### Response with Markdown

```tsx
import { marked } from 'marked';

const addMarkdownResponse = () => {
    const markdownText = `
## Response Header

This is **bold** and *italic* text.

- Bullet 1
- Bullet 2

\`\`\`javascript
const example = "code";
\`\`\`
    `;
    
    const htmlResponse = marked.parse(markdownText);
    assistInstance.current?.addPromptResponse(htmlResponse);
};
```

## Executing Prompts

### executePrompt Method

Execute a prompt programmatically, triggering the promptRequest event:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        console.log('Prompt executed:', args.prompt);
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    const executeCustomPrompt = () => {
        // Programmatically execute a prompt
        assistInstance.current?.executePrompt('What is artificial intelligence?');
    };

    const executePredefinedPrompt = () => {
        const questions = [
            'What is React?',
            'How to use hooks?',
            'Best practices?'
        ];
        const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
        assistInstance.current?.executePrompt(randomQuestion);
    };

    return (
        <div>
            <button onClick={executeCustomPrompt}>Execute Custom</button>
            <button onClick={executePredefinedPrompt}>Execute Random</button>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
}

export default app;
```

## Scrolling Methods

### Scroll to Bottom

```tsx
const scrollToLatestMessage = () => {
    assistInstance.current?.scrollToBottom();
};

// Or use in event handler
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    setTimeout(() => {
        assistInstance.current?.addPromptResponse('Response');
        assistInstance.current?.scrollToBottom();  // Ensure latest visible
    }, 1000);
};
```

### Auto-Scroll Implementation

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        // Stream response
        let response = '';
        for (let i = 0; i < 100; i++) {
            response += `Word ${i} `;
            
            if (i % 10 === 0) {
                assistInstance.current?.addPromptResponse(response);
                assistInstance.current?.scrollToBottom();  // Keep in view
            }
            
            await new Promise(resolve => setTimeout(resolve, 50));
        }
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

## Accessing Component Properties

### Accessing Prompts Collection

```tsx
const viewConversationHistory = () => {
    const prompts = assistInstance.current?.prompts;
    
    if (prompts) {
        console.log('Total exchanges:', prompts.length);
        prompts.forEach((item, index) => {
            console.log(`[${index}] Q: ${item.prompt}`);
            console.log(`[${index}] A: ${item.response}`);
        });
    }
};

const getLastExchange = () => {
    const prompts = assistInstance.current?.prompts;
    if (prompts && prompts.length > 0) {
        const last = prompts[prompts.length - 1];
        return {
            prompt: last.prompt,
            response: last.response
        };
    }
};
```

### Modifying Prompts Collection

```tsx
const clearConversation = () => {
    if (assistInstance.current) {
        assistInstance.current.prompts = [];
    }
};

const removeLastExchange = () => {
    const prompts = assistInstance.current?.prompts;
    if (prompts && prompts.length > 0) {
        prompts.pop();
        // Update component
        assistInstance.current.prompts = [...prompts];
    }
};

const replaceConversation = (newPrompts: any[]) => {
    if (assistInstance.current) {
        assistInstance.current.prompts = newPrompts;
    }
};
```

### Getting Current Prompt Text

```tsx
const getCurrentPromptText = (): string => {
    // Access the current prompt in input area
    const promptInput = document.querySelector('.e-prompt-input') as HTMLTextAreaElement;
    return promptInput?.value || '';
};

const setCurrentPromptText = (text: string) => {
    const promptInput = document.querySelector('.e-prompt-input') as HTMLTextAreaElement;
    if (promptInput) {
        promptInput.value = text;
    }
};
```

## Advanced Component Control

### Reset Component State

```tsx
const resetComponent = () => {
    const assistInstance = assistInstance.current;
    if (assistInstance) {
        // Clear all prompts
        assistInstance.prompts = [];
        
        // Reset prompt text
        setCurrentPromptText('');
        
        // Reset suggestions if needed
        assistInstance.promptSuggestions = [];
        
        // Reset active view
        assistInstance.activeView = 0;
    }
};
```

### Export Conversation

```tsx
const exportConversation = () => {
    const prompts = assistInstance.current?.prompts;
    if (!prompts) return;
    
    const data = {
        timestamp: new Date().toISOString(),
        exchanges: prompts.map(item => ({
            prompt: item.prompt,
            response: item.response,
            timestamp: new Date().toISOString()
        }))
    };
    
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `conversation-${Date.now()}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
};
```

### Import Conversation

```tsx
const importConversation = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target?.result as string);
            assistInstance.current?.prompts = data.exchanges;
        } catch (error) {
            console.error('Failed to import conversation:', error);
        }
    };
    reader.readAsText(file);
};
```

## Common Patterns

### Conversation Auto-Save

```tsx
const saveConversationLocally = () => {
    const prompts = assistInstance.current?.prompts;
    localStorage.setItem('aiConversation', JSON.stringify(prompts));
};

const loadConversationLocally = () => {
    const saved = localStorage.getItem('aiConversation');
    if (saved) {
        assistInstance.current.prompts = JSON.parse(saved);
    }
};

// Auto-save on every response
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    setTimeout(() => {
        assistInstance.current?.addPromptResponse('Response');
        saveConversationLocally();  // Auto-save
    }, 1000);
};
```

### Conversation Search

```tsx
const searchConversation = (query: string) => {
    const prompts = assistInstance.current?.prompts || [];
    const results = prompts.filter(item =>
        item.prompt.toLowerCase().includes(query.toLowerCase()) ||
        item.response.toLowerCase().includes(query.toLowerCase())
    );
    return results;
};

const highlightSearchResults = (query: string) => {
    const results = searchConversation(query);
    console.log(`Found ${results.length} matches for "${query}"`);
    results.forEach((result, index) => {
        console.log(`Match ${index + 1}:`, result);
    });
};
```

### Conversation Statistics

```tsx
const getConversationStats = () => {
    const prompts = assistInstance.current?.prompts || [];
    
    const stats = {
        totalExchanges: prompts.length,
        totalPromptWords: prompts.reduce((sum, item) => sum + item.prompt.split(' ').length, 0),
        totalResponseWords: prompts.reduce((sum, item) => {
            const div = document.createElement('div');
            div.innerHTML = item.response;
            return sum + (div.textContent || '').split(' ').length;
        }, 0),
        averagePromptLength: 0,
        averageResponseLength: 0
    };
    
    if (stats.totalExchanges > 0) {
        stats.averagePromptLength = stats.totalPromptWords / stats.totalExchanges;
        stats.averageResponseLength = stats.totalResponseWords / stats.totalExchanges;
    }
    
    return stats;
};
```

### Rate Limiting with Methods

```tsx
let lastExecuteTime = 0;
const MIN_INTERVAL = 500;  // 500ms between prompts

const executePromptSafe = (prompt: string) => {
    const now = Date.now();
    
    if (now - lastExecuteTime < MIN_INTERVAL) {
        console.warn('Please wait before executing next prompt');
        return false;
    }
    
    lastExecuteTime = now;
    assistInstance.current?.executePrompt(prompt);
    return true;
};
```

## Complete Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [stats, setStats] = useState({ exchanges: 0, lastTime: '' });

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            const response = `Processed: "${args.prompt}"`;
            assistInstance.current?.addPromptResponse(response);
            assistInstance.current?.scrollToBottom();
            
            // Update stats
            const prompts = assistInstance.current?.prompts || [];
            setStats({
                exchanges: prompts.length,
                lastTime: new Date().toLocaleTimeString()
            });
        }, 1000);
    };

    const actions = {
        clear: () => {
            assistInstance.current.prompts = [];
            setStats({ exchanges: 0, lastTime: '' });
        },
        execute: () => {
            assistInstance.current?.executePrompt('Sample automated prompt');
        },
        export: () => {
            const data = assistInstance.current?.prompts;
            console.log('Exported:', data);
        }
    };

    return (
        <div>
            <div className="controls">
                <button onClick={actions.clear}>Clear</button>
                <button onClick={actions.execute}>Execute Sample</button>
                <button onClick={actions.export}>Export</button>
            </div>
            <div className="stats">
                Exchanges: {stats.exchanges} | Last: {stats.lastTime}
            </div>
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

## Best Practices

**Always check for null/undefined**: Use optional chaining (?)  
**Validate before adding**: Check prompt/response content  
**Use methods for state changes**: Avoid direct prop manipulation  
**Implement error handling**: Try-catch for edge cases  
**Performance**: Debounce frequent method calls  
**Save state**: Backup conversations regularly  
**Test edge cases**: Empty responses, very long text, etc.
