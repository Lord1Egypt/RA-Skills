# Conversation Management

## Table of Contents
- [Prompt-Response Collection](#prompt-response-collection)
- [Initializing Pre-Configured Data](#initializing-pre-configured-data)
- [Accessing Conversation History](#accessing-conversation-history)
- [Adding Responses](#adding-responses)
- [PromptModel Data Structure](#promptmodel-data-structure)
- [Markdown Response Rendering](#markdown-response-rendering)
- [Dynamic Content](#dynamic-content)

## Prompt-Response Collection

### Overview

The AI AssistView component automatically maintains a collection of prompts and responses during a session. The `prompts` property stores all user interactions:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        // The component automatically adds the prompt to prompts collection
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response text');
        }, 1000);
    };

    const displayHistory = () => {
        // Access the conversation history
        const conversation = assistInstance.current?.prompts;
        console.log('Total exchanges:', conversation?.length);
        conversation?.forEach((item, index) => {
            console.log(`[${index}] User: ${item.prompt}`);
            console.log(`[${index}] AI: ${item.response}`);
        });
    };

    return (
        <div>
            <button onClick={displayHistory}>Show History</button>
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

## Initializing Pre-Configured Data

### Using the prompts Property

Initialize the component with existing conversation data using the `prompts` property:

```tsx
import { AIAssistViewComponent, PromptModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const preConfiguredPrompts: PromptModel[] = [
        {
            prompt: "What is React?",
            response: "React is a JavaScript library for building user interfaces with components."
        },
        {
            prompt: "How do I use hooks?",
            response: "Hooks let you use state and React features without writing class components."
        }
    ];

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            prompts={preConfiguredPrompts}
        />
    );
}

export default App;
```

### Complete Pre-Configured Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, PromptModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const initialConversation: PromptModel[] = [
        {
            prompt: "What is AI?",
            response: "<div>AI stands for Artificial Intelligence, enabling machines to mimic human intelligence.</div>"
        },
        {
            prompt: "What can AI do?",
            response: "<div>AI can perform tasks like learning, problem-solving, and decision-making.</div>"
        }
    ];

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        // Handle new user prompts
        const found = initialConversation.find(item => item.prompt === args.prompt);
        
        setTimeout(() => {
            assistInstance.current?.addPromptResponse(
                found ? found.response : 'Default response'
            );
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            prompts={initialConversation}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Accessing Conversation History

### Get All Prompts and Responses

Access the complete conversation history:

```tsx
const getConversationSummary = () => {
    const prompts = assistInstance.current?.prompts;
    
    if (!prompts) return;
    
    // Get conversation statistics
    console.log('Total exchanges:', prompts.length);
    console.log('First prompt:', prompts[0]?.prompt);
    console.log('Last response:', prompts[prompts.length - 1]?.response);
};
```

### Filter Conversation Data

Find specific prompts or responses:

```tsx
const findResponseAbout = (topic: string) => {
    const prompts = assistInstance.current?.prompts;
    const matching = prompts?.filter(item => 
        item.prompt.includes(topic) || item.response.includes(topic)
    );
    return matching;
};
```

### Export Conversation

Save conversation to file or database:

```tsx
const exportConversation = () => {
    const prompts = assistInstance.current?.prompts;
    const json = JSON.stringify(prompts, null, 2);
    
    // Save to localStorage
    localStorage.setItem('conversation', json);
    
    // Or download as file
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'conversation.json';
    link.click();
};
```

## Adding Responses

### Add Response as String

Append a simple text response to the last prompt:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    setTimeout(() => {
        // Add response as plain string
        assistInstance.current?.addPromptResponse('Simple text response');
    }, 1000);
};
```

### Add Response as Object

Add a complete prompt-response pair as an object:

```tsx
const addCompleteExchange = () => {
    assistInstance.current?.addPromptResponse({
        prompt: "What is React?",
        response: "React is a JavaScript library for building user interfaces."
    });
};
```

### Add HTML Response

Include HTML formatting in responses:

```tsx
const handlePromptRequest = (args: PromptRequestEventArgs) => {
    const htmlResponse = `
        <div class="response-content">
            <h3>Response Title</h3>
            <p>This is a formatted response with <strong>bold text</strong>.</p>
            <ul>
                <li>Point 1</li>
                <li>Point 2</li>
            </ul>
        </div>
    `;
    assistInstance.current?.addPromptResponse(htmlResponse);
};
```

## PromptModel Data Structure

### Properties

The `PromptModel` interface contains:

```tsx
interface PromptModel {
    prompt: string;           // User's question or input
    response: string;         // AI's response (HTML or plain text)
    suggestions?: string[];   // Optional follow-up suggestions
    output?: any;            // Optional additional data
    index?: number;          // Position in conversation
}
```

### Complete Example

```tsx
const advancedPrompt: PromptModel = {
    prompt: "What is React?",
    response: "<div><strong>React</strong> is a JavaScript library...</div>",
    suggestions: [
        "How to use React?",
        "React best practices?",
        "React vs Vue?"
    ],
    output: {
        confidence: 0.95,
        source: "knowledge_base"
    }
};

assistInstance.current?.addPromptResponse(advancedPrompt);
```

## Markdown Response Rendering

### Enable Markdown Parsing

Use the `marked` library to render markdown as HTML:

```bash
npm install marked --save
```

### Parse and Display Markdown

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import { marked } from 'marked';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        const markdownResponse = `
## Topic Title

This is **bold** and this is *italic*.

- Bullet point 1
- Bullet point 2

\`\`\`javascript
const code = "example";
\`\`\`
        `;

        setTimeout(() => {
            // Convert markdown to HTML
            const htmlResponse = marked.parse(markdownResponse);
            assistInstance.current?.addPromptResponse(htmlResponse);
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

## Dynamic Content

### Streaming Responses

Display responses character-by-character for typing effect:

```tsx
const streamResponse = async (text: string) => {
    let displayText = '';
    
    for (let i = 0; i < text.length; i++) {
        displayText += text[i];
        
        // Update every 10 characters
        if (i % 10 === 0 || i === text.length - 1) {
            const htmlResponse = marked.parse(displayText);
            assistInstance.current?.addPromptResponse(
                htmlResponse, 
                i === text.length - 1  // Mark as final when complete
            );
        }
        
        // Add delay for streaming effect
        await new Promise(resolve => setTimeout(resolve, 15));
    }
};
```

### Dynamic Response Update

Add progressive content to responses:

```tsx
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    // Initial response
    assistInstance.current?.addPromptResponse('Thinking...');
    
    // Simulate processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Update with actual content
    const fullResponse = 'This is the complete response after processing.';
    assistInstance.current?.addPromptResponse(fullResponse);
};
```

### Conversation Persistence

Save and restore conversations:

```tsx
const saveConversation = () => {
    const data = {
        timestamp: new Date().toISOString(),
        prompts: assistInstance.current?.prompts
    };
    localStorage.setItem('savedChat', JSON.stringify(data));
};

const loadConversation = () => {
    const saved = localStorage.getItem('savedChat');
    if (saved) {
        const data = JSON.parse(saved);
        assistInstance.current.prompts = data.prompts;
    }
};

const clearConversation = () => {
    assistInstance.current.prompts = [];
    localStorage.removeItem('savedChat');
};
```

## Best Practices

**Use HTML responses for rich content**: Better formatting and structure  
**Enable markdown parsing**: For AI-generated formatted responses  
**Stream long responses**: Provides better UX for lengthy content  
**Manage conversation size**: Archive old conversations to reduce memory  
**Validate response data**: Ensure HTML is safe (XSS prevention)  
**Backup conversations**: Save to localStorage or backend regularly
