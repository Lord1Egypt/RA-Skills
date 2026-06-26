# Templating System

## Table of Contents
- [Template Architecture](#template-architecture)
- [Banner Template](#banner-template)
- [Prompt Item Template](#prompt-item-template)
- [Response Item Template](#response-item-template)
- [Suggestion Item Template](#suggestion-item-template)
- [Footer Template](#footer-template)
- [Template Context Data](#template-context-data)
- [HTML and CSS in Templates](#html-and-css-in-templates)
- [Dynamic Rendering](#dynamic-rendering)

## Template Architecture

The AI AssistView provides five template customization points:

1. **bannerTemplate**: Welcome/intro content at top
2. **promptItemTemplate**: User message display
3. **responseItemTemplate**: AI response display
4. **promptSuggestionItemTemplate**: Suggestion item styling
5. **footerTemplate**: Custom prompt input area

## Banner Template

### Basic Banner

Display welcome content at the top of the conversation:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const bannerTemplate = `
        <div class="banner-content">
            <div class="e-icons e-assistview-icon"></div>
            <h3>Welcome to AI Assistant</h3>
            <p>Your everyday AI companion for assistance</p>
        </div>
    `;

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            bannerTemplate={bannerTemplate}
        />
    );
}

export default App;
```

### Banner with Styling

```tsx
const bannerTemplate = `
    <div class="banner-content" style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px;">
        <h2>🤖 AI Assistant</h2>
        <p>How can I help you today?</p>
        <small>Powered by Advanced AI</small>
    </div>
`;
```

## Prompt Item Template

### Custom User Message Display

Customize how user prompts appear:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const promptItemTemplate = (props: any) => {
        return (
            <div className="custom-prompt">
                <div className="prompt-header">
                    <span className="e-icons e-user"></span>
                    <strong>You</strong>
                    <span className="time">Just now</span>
                </div>
                <div className="prompt-content">
                    {props.prompt}
                </div>
            </div>
        );
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            promptItemTemplate={promptItemTemplate}
        />
    );
}

export default App;
```

### Template with Badges

```tsx
const promptItemTemplate = (props: any) => {
    const wordCount = props.prompt.split(' ').length;
    return (
        <div className="custom-prompt">
            <div className="prompt-header">
                <strong>User</strong>
                <span className="badge">{wordCount} words</span>
            </div>
            <div className="prompt-content">
                {props.prompt}
            </div>
        </div>
    );
};
```

## Response Item Template

### Custom AI Response Display

Customize how AI responses appear:

```tsx
const responseItemTemplate = (props: any) => {
    return (
        <div className="custom-response">
            <div className="response-header">
                <span className="e-icons e-assistview-icon"></span>
                <strong>AI Assistant</strong>
            </div>
            <div className="assist-response-content" dangerouslySetInnerHTML={{ __html: props.response }}>
            </div>
            <div className="response-footer">
                <small>Response generated</small>
            </div>
        </div>
    );
};

<AIAssistViewComponent 
    id="aiAssistView"
    responseItemTemplate={responseItemTemplate}
/>
```

### Response with Rating

```tsx
const responseItemTemplate = (props: any) => {
    return (
        <div className="custom-response">
            <div className="response-content" dangerouslySetInnerHTML={{ __html: props.response }}></div>
            <div className="response-rating">
                <span>Was this helpful?</span>
                <span className="e-icons e-like"></span>
                <span className="e-icons e-dislike"></span>
            </div>
        </div>
    );
};
```

## Suggestion Item Template

### Custom Suggestion Display

Customize how suggestions are styled:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const suggestions = [
        "What is React?",
        "How to use hooks?",
        "Best practices"
    ];

    const promptSuggestionItemTemplate = (props: any) => {
        return (
            <div className="custom-suggestion">
                <span className="e-icons e-circle-info"></span>
                <div className="suggestion-text">
                    {props.promptSuggestion}
                </div>
            </div>
        );
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            promptSuggestions={suggestions}
            promptSuggestionItemTemplate={promptSuggestionItemTemplate}
        />
    );
}

export default App;
```

### Suggestion with Icons

```tsx
const getSuggestionIcon = (text: string) => {
    if (text.includes('?')) return '❓';
    if (text.includes('how')) return '📚';
    if (text.includes('best')) return '⭐';
    return '💡';
};

const promptSuggestionItemTemplate = (props: any) => {
    return (
        <div className="custom-suggestion">
            <span className="icon">{getSuggestionIcon(props.promptSuggestion)}</span>
            <span className="text">{props.promptSuggestion}</span>
        </div>
    );
};
```

## Footer Template

### Custom Prompt Input Area

Replace default footer with custom content:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const textAreaRef = useRef<HTMLTextAreaElement>(null);

    const footerTemplate = () => {
        return (
            <div className="custom-footer">
                <textarea 
                    ref={textAreaRef}
                    className="e-input" 
                    rows={3} 
                    placeholder="Enter your message here..."
                    onKeyPress={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            handleSend();
                        }
                    }}
                />
                <div className="footer-actions">
                    <button className="e-btn e-primary" onClick={handleSend}>
                        Send
                    </button>
                    <button className="e-btn" onClick={handleClear}>
                        Clear
                    </button>
                </div>
            </div>
        );
    };

    const handleSend = () => {
        if (textAreaRef.current?.value) {
            assistInstance.current?.executePrompt(textAreaRef.current.value);
            textAreaRef.current.value = '';
        }
    };

    const handleClear = () => {
        if (textAreaRef.current) {
            textAreaRef.current.value = '';
        }
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            footerTemplate={footerTemplate}
        />
    );
}

export default App;
```

### Footer with Character Counter

```tsx
const [charCount, setCharCount] = React.useState(0);

const footerTemplate = () => {
    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setCharCount(e.target.value.length);
    };

    return (
        <div className="custom-footer">
            <textarea 
                ref={textAreaRef}
                className="e-input" 
                rows={3} 
                placeholder="Message..."
                onChange={handleTextChange}
            />
            <div className="char-counter">
                {charCount}/1000 characters
            </div>
            <button className="e-btn e-primary" onClick={handleSend}>
                Send
            </button>
        </div>
    );
};
```

## Template Context Data

### Available Props for Templates

```tsx
// Prompt Item
interface PromptItemProps {
    prompt: string;           // User's message
    toolbarItems?: any[];     // Available toolbar actions
    index?: number;           // Position in conversation
}

// Response Item
interface ResponseItemProps {
    response: string;         // AI's response (HTML)
    prompt: string;          // Original prompt
    toolbarItems?: any[];     // Available toolbar actions
    index?: number;           // Position in conversation
    output?: any;            // Additional data
}

// Suggestion Item
interface SuggestionItemProps {
    promptSuggestion: string; // Suggestion text
    index?: number;           // Position in suggestions list
}
```

### Accessing Context in Templates

```tsx
const responseItemTemplate = (props: any) => {
    console.log('Response index:', props.index);
    console.log('Original prompt:', props.prompt);
    console.log('Available tools:', props.toolbarItems);
    
    return (
        <div>
            <h4>Response #{props.index}</h4>
            <div dangerouslySetInnerHTML={{ __html: props.response }}></div>
        </div>
    );
};
```

## HTML and CSS in Templates

### Inline Styles

```tsx
const bannerTemplate = `
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        <h2 style="margin: 0 0 10px 0;">Welcome</h2>
        <p style="margin: 0; opacity: 0.9;">How can I assist you?</p>
    </div>
`;
```

### External CSS Classes

```tsx
<style>{`
    .banner-custom {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 8px;
        text-align: center;
    }
    
    .prompt-custom {
        background: #f0f0f0;
        padding: 12px;
        border-radius: 6px;
        margin: 8px 0;
    }
    
    .response-custom {
        background: white;
        padding: 12px;
        border-left: 3px solid #667eea;
        margin: 8px 0;
    }
`}</style>

<AIAssistViewComponent 
    id="aiAssistView"
    bannerTemplate='<div class="banner-custom">Welcome</div>'
/>
```

## Dynamic Rendering

### Conditional Content

```tsx
const responseItemTemplate = (props: any) => {
    const isLongResponse = props.response.length > 500;
    const isCodeResponse = props.response.includes('<code>');
    
    return (
        <div className="custom-response">
            {isCodeResponse && <span className="badge">Code</span>}
            {isLongResponse && <span className="badge">Long Response</span>}
            <div dangerouslySetInnerHTML={{ __html: props.response }}></div>
        </div>
    );
};
```

### Timestamp Integration

```tsx
const promptItemTemplate = (props: any) => {
    const timestamp = new Date().toLocaleTimeString();
    
    return (
        <div className="prompt-with-time">
            <div className="prompt-header">
                <strong>You</strong>
                <small className="time">{timestamp}</small>
            </div>
            <div className="prompt-text">{props.prompt}</div>
        </div>
    );
};
```

## Complete Templating Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const styles = `
        <style>
            .banner { background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 8px; }
            .prompt-item { background: #f0f0f0; padding: 12px; border-radius: 6px; margin: 8px 0; }
            .response-item { background: white; padding: 12px; border-left: 3px solid #667eea; margin: 8px 0; }
            .suggestion-item { padding: 8px; margin: 4px 0; cursor: pointer; border-radius: 4px; }
            .suggestion-item:hover { background: #e8e8e8; }
        </style>
    `;

    const bannerTemplate = '<div class="banner"><h3>AI Assistant</h3><p>Your helper</p></div>';

    const promptItemTemplate = (props: any) => `
        <div class="prompt-item">
            <strong>You:</strong> ${props.prompt}
        </div>
    `;

    const responseItemTemplate = (props: any) => `
        <div class="response-item">
            <strong>AI:</strong> ${props.response}
        </div>
    `;

    const suggestionTemplate = (props: any) => `
        <div class="suggestion-item">
            💡 ${props.promptSuggestion}
        </div>
    `;

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <>
            {styles}
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                bannerTemplate={bannerTemplate}
                promptItemTemplate={promptItemTemplate}
                responseItemTemplate={responseItemTemplate}
                promptSuggestionItemTemplate={suggestionTemplate}
            />
        </>
    );
}

export default App;
```

## Best Practices

**Keep templates simple**: Avoid complex logic in templates  
**Use semantic HTML**: Proper structure for accessibility  
**Style consistently**: Maintain design coherence  
**Provide fallbacks**: Default content if template fails  
**Performance**: Minimize template rendering overhead  
**Security**: Sanitize user content in templates to prevent XSS
