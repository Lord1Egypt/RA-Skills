````markdown
# Template Customization

## Table of Contents
- [Overview](#overview)
- [editorTemplate Property](#editortemplate-property)
- [responseTemplate Property](#responsetemplate-property)
- [Template Context Objects](#template-context-objects)
- [Complete Examples](#complete-examples)

## Overview

The Inline AI Assist component provides two powerful template properties for complete UI customization:

1. **editorTemplate** - Customize the prompt input area
2. **responseTemplate** - Customize how AI responses are rendered

Both properties accept three types of values:
- **String template** - HTML string with placeholders
- **Function template** - Function that returns HTML/JSX
- **JSX.Element** - React component for full control

## editorTemplate Property

The `editorTemplate` property allows you to completely customize the prompt input area. By default, the component renders a standard textarea, but you can replace it with any custom editor UI.

### Type Signature

```tsx
editorTemplate: string | function | JSX.Element
```

### Default Value

```tsx
editorTemplate: ''  // Uses built-in textarea editor
```

### When to Use

- Replace textarea with rich text editor
- Add custom input controls (voice input, file attachments)
- Integrate third-party editor components (Monaco, CodeMirror)
- Add custom toolbars or formatting options
- Implement specialized input interfaces

### String Template

Use a string template with HTML markup:

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const editorTemplate = `
        <div class="custom-editor">
            <textarea 
                class="e-input custom-prompt-area" 
                placeholder="Enter your prompt here..."
                rows="4"
            ></textarea>
            <div class="editor-footer">
                <span class="char-count">0 characters</span>
            </div>
        </div>
    `;

    return (
        <InlineAIAssistComponent
            editorTemplate={editorTemplate}
        />
    );
};

export default App;
```

### Function Template

Use a function that returns HTML or JSX:

```tsx
const App: React.FC = () => {
    const editorTemplate = () => {
        return (
            <div className="custom-editor-wrapper">
                <label htmlFor="prompt-input">Your AI Prompt:</label>
                <textarea
                    id="prompt-input"
                    className="e-input"
                    placeholder="Ask AI anything..."
                    rows={5}
                    style={{
                        width: '100%',
                        padding: '10px',
                        fontSize: '14px',
                        borderRadius: '4px'
                    }}
                />
                <div className="editor-hints">
                    <small>💡 Tip: Be specific for better results</small>
                </div>
            </div>
        );
    };

    return (
        <InlineAIAssistComponent
            editorTemplate={editorTemplate}
        />
    );
};
```

### JSX.Element Template

Use a React component for maximum flexibility:

```tsx
const CustomEditor: React.FC = () => {
    const [charCount, setCharCount] = React.useState(0);
    const [showHints, setShowHints] = React.useState(true);

    const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setCharCount(e.target.value.length);
    };

    return (
        <div className="advanced-editor">
            <div className="editor-header">
                <button 
                    className="e-btn e-small"
                    onClick={() => setShowHints(!showHints)}
                >
                    {showHints ? 'Hide' : 'Show'} Hints
                </button>
            </div>
            
            {showHints && (
                <div className="hints-panel">
                    <p>🎯 Quick tips:</p>
                    <ul>
                        <li>Be clear and specific</li>
                        <li>Provide context when needed</li>
                        <li>Ask follow-up questions</li>
                    </ul>
                </div>
            )}
            
            <textarea
                className="e-input prompt-textarea"
                placeholder="Enter your AI prompt..."
                onChange={handleTextChange}
                rows={6}
            />
            
            <div className="editor-footer">
                <span className="char-count">{charCount} characters</span>
                <span className="word-count">
                    {charCount > 0 ? Math.ceil(charCount / 5) : 0} words (est.)
                </span>
            </div>
        </div>
    );
};

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            editorTemplate={<CustomEditor />}
        />
    );
};
```

### Rich Text Editor Integration

Integrate a rich text editor like Draft.js or Quill:

```tsx
import { Editor } from 'react-draft-wysiwyg';
import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';

const RichTextEditor: React.FC = () => {
    const [editorState, setEditorState] = React.useState(
        EditorState.createEmpty()
    );

    return (
        <div className="rich-editor-wrapper">
            <Editor
                editorState={editorState}
                onEditorStateChange={setEditorState}
                toolbar={{
                    options: ['inline', 'list', 'emoji'],
                    inline: {
                        options: ['bold', 'italic', 'underline']
                    }
                }}
                placeholder="Enter your prompt with formatting..."
            />
        </div>
    );
};

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            editorTemplate={<RichTextEditor />}
        />
    );
};
```

### Voice Input Integration

Add voice input capability to the editor:

```tsx
const VoiceEnabledEditor: React.FC = () => {
    const [text, setText] = React.useState('');
    const [isListening, setIsListening] = React.useState(false);

    const startVoiceInput = () => {
        if (!('webkitSpeechRecognition' in window)) {
            alert('Voice input not supported');
            return;
        }

        const recognition = new (window as any).webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => setIsListening(true);
        recognition.onend = () => setIsListening(false);

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setText(prev => prev + ' ' + transcript);
        };

        recognition.start();
    };

    return (
        <div className="voice-editor">
            <div className="editor-controls">
                <button 
                    className={`e-btn ${isListening ? 'e-danger' : 'e-primary'}`}
                    onClick={startVoiceInput}
                >
                    <span className="e-icons e-microphone"></span>
                    {isListening ? 'Listening...' : 'Voice Input'}
                </button>
            </div>
            
            <textarea
                className="e-input"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type or use voice input..."
                rows={5}
            />
        </div>
    );
};

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            editorTemplate={<VoiceEnabledEditor />}
        />
    );
};
```

## responseTemplate Property

The `responseTemplate` property allows you to customize how AI-generated responses are displayed. By default, responses are rendered as plain text or markdown, but you can create custom layouts, styling, and interactive elements.

### Type Signature

```tsx
responseTemplate: string | function | JSX.Element
```

### Default Value

```tsx
responseTemplate: ''  // Uses built-in response renderer
```

### When to Use

- Custom response styling and layout
- Add interactive elements (copy, share, rate buttons)
- Format responses with custom rendering (code highlighting, tables)
- Show response metadata (tokens used, processing time)
- Implement response animations or transitions

### Template Context

When using a function template for `responseTemplate`, you receive a context object with response data:

```tsx
interface ResponseTemplateContext {
    response: string;          // The AI-generated response text
    prompt: string;            // The original user prompt
    index: number;             // Index in prompts array
}
```

### String Template

Use HTML string with inline styling:

```tsx
const App: React.FC = () => {
    const responseTemplate = `
        <div class="custom-response-card">
            <div class="response-header">
                <span class="response-icon">🤖</span>
                <strong>AI Response</strong>
            </div>
            <div class="response-body">
                \${response}
            </div>
            <div class="response-footer">
                <button class="e-btn e-small">Copy</button>
                <button class="e-btn e-small">Share</button>
            </div>
        </div>
    `;

    return (
        <InlineAIAssistComponent
            responseTemplate={responseTemplate}
        />
    );
};
```

### Function Template with Context

Use a function to access response data:

```tsx
const App: React.FC = () => {
    const responseTemplate = (context: any) => {
        const { response, prompt, index } = context;
        
        return (
            <div className="response-container">
                <div className="response-metadata">
                    <span className="response-number">Response #{index + 1}</span>
                    <span className="prompt-preview">
                        Prompt: {prompt.substring(0, 50)}...
                    </span>
                </div>
                
                <div className="response-content">
                    {response}
                </div>
                
                <div className="response-actions">
                    <button 
                        className="e-btn e-small"
                        onClick={() => navigator.clipboard.writeText(response)}
                    >
                        📋 Copy
                    </button>
                </div>
            </div>
        );
    };

    return (
        <InlineAIAssistComponent
            responseTemplate={responseTemplate}
        />
    );
};
```

### JSX.Element with Rich Formatting

Create a fully interactive response component:

```tsx
interface ResponseProps {
    response: string;
    prompt: string;
    index: number;
}

const CustomResponseCard: React.FC<ResponseProps> = ({ response, prompt, index }) => {
    const [isCopied, setIsCopied] = React.useState(false);
    const [rating, setRating] = React.useState<number | null>(null);

    const handleCopy = () => {
        navigator.clipboard.writeText(response);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
    };

    const handleRate = (stars: number) => {
        setRating(stars);
        // Send rating to analytics
        console.log(`Response #${index} rated ${stars} stars`);
    };

    return (
        <div className="response-card">
            <div className="response-header">
                <div className="header-left">
                    <span className="ai-icon">✨</span>
                    <h4>AI Assistant</h4>
                </div>
                <div className="header-right">
                    <span className="response-id">#{index + 1}</span>
                </div>
            </div>
            
            <div className="response-prompt">
                <strong>You asked:</strong>
                <p>{prompt}</p>
            </div>
            
            <div className="response-body">
                <div dangerouslySetInnerHTML={{ __html: response }} />
            </div>
            
            <div className="response-footer">
                <div className="footer-actions">
                    <button 
                        className={`e-btn e-small ${isCopied ? 'e-success' : ''}`}
                        onClick={handleCopy}
                    >
                        {isCopied ? '✓ Copied' : '📋 Copy'}
                    </button>
                    <button className="e-btn e-small">
                        🔄 Regenerate
                    </button>
                    <button className="e-btn e-small">
                        📤 Share
                    </button>
                </div>
                
                <div className="footer-rating">
                    <span>Rate this response:</span>
                    {[1, 2, 3, 4, 5].map(star => (
                        <button
                            key={star}
                            className="star-button"
                            onClick={() => handleRate(star)}
                        >
                            {star <= (rating || 0) ? '⭐' : '☆'}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const responseTemplate = (context: any) => (
        <CustomResponseCard
            response={context.response}
            prompt={context.prompt}
            index={context.index}
        />
    );

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            responseTemplate={responseTemplate}
        />
    );
};
```

### Code Syntax Highlighting

Format code responses with syntax highlighting:

```tsx
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';

const CodeResponseTemplate: React.FC<{ response: string }> = ({ response }) => {
    const [highlightedCode, setHighlightedCode] = React.useState('');

    React.useEffect(() => {
        // Detect code blocks and highlight
        const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
        const highlighted = response.replace(codeBlockRegex, (match, lang, code) => {
            const language = lang || 'javascript';
            const highlightedCode = Prism.highlight(
                code,
                Prism.languages[language],
                language
            );
            return `<pre class="language-${language}"><code>${highlightedCode}</code></pre>`;
        });
        setHighlightedCode(highlighted);
    }, [response]);

    return (
        <div className="code-response">
            <div dangerouslySetInnerHTML={{ __html: highlightedCode }} />
        </div>
    );
};

const App: React.FC = () => {
    const responseTemplate = (context: any) => (
        <CodeResponseTemplate response={context.response} />
    );

    return (
        <InlineAIAssistComponent
            responseTemplate={responseTemplate}
        />
    );
};
```

### Markdown Rendering

Render markdown responses with a markdown parser:

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const MarkdownResponseTemplate: React.FC<{ response: string; prompt: string }> = ({ 
    response, 
    prompt 
}) => {
    return (
        <div className="markdown-response">
            <div className="response-context">
                <small>In response to: "{prompt}"</small>
            </div>
            
            <div className="markdown-content">
                <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                        // Custom component renderers
                        h1: ({node, ...props}) => (
                            <h1 style={{ color: '#2563eb' }} {...props} />
                        ),
                        code: ({node, inline, ...props}) => (
                            inline 
                                ? <code className="inline-code" {...props} />
                                : <code className="code-block" {...props} />
                        ),
                        table: ({node, ...props}) => (
                            <div className="table-wrapper">
                                <table className="e-table" {...props} />
                            </div>
                        )
                    }}
                >
                    {response}
                </ReactMarkdown>
            </div>
        </div>
    );
};

const App: React.FC = () => {
    const responseTemplate = (context: any) => (
        <MarkdownResponseTemplate 
            response={context.response}
            prompt={context.prompt}
        />
    );

    return (
        <InlineAIAssistComponent
            responseTemplate={responseTemplate}
        />
    );
};
```

## Template Context Objects

### EditorTemplate Context

The `editorTemplate` doesn't receive context by default, but you can access the component instance via ref:

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const editorTemplate = () => {
        const handleSubmit = () => {
            const textarea = document.querySelector('.custom-prompt') as HTMLTextAreaElement;
            if (textarea && textarea.value) {
                assistRef.current?.executePrompt(textarea.value);
            }
        };

        return (
            <div>
                <textarea className="custom-prompt e-input" />
                <button onClick={handleSubmit}>Submit</button>
            </div>
        );
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            editorTemplate={editorTemplate}
        />
    );
};
```

### ResponseTemplate Context Properties

```tsx
interface ResponseTemplateContext {
    response: string;    // AI-generated response text
    prompt: string;      // Original user prompt
    index: number;       // Position in prompts array (0-based)
}
```

Example accessing all context properties:

```tsx
const responseTemplate = (context: ResponseTemplateContext) => {
    const { response, prompt, index } = context;
    
    return (
        <div className="detailed-response">
            <div className="metadata">
                <span>Response {index + 1}</span>
                <span>{new Date().toLocaleTimeString()}</span>
            </div>
            <div className="user-prompt">
                <strong>Your question:</strong> {prompt}
            </div>
            <div className="ai-response">
                <strong>AI answer:</strong> {response}
            </div>
        </div>
    );
};
```

## Complete Examples

### Example 1: Full Custom UI Workflow

```tsx
const FullCustomAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [promptText, setPromptText] = React.useState('');

    // Custom editor template
    const editorTemplate = () => (
        <div className="custom-editor-panel">
            <div className="editor-toolbar">
                <button className="e-btn e-small" title="Bold">
                    <strong>B</strong>
                </button>
                <button className="e-btn e-small" title="Italic">
                    <em>I</em>
                </button>
            </div>
            
            <textarea
                className="e-input editor-textarea"
                value={promptText}
                onChange={(e) => setPromptText(e.target.value)}
                placeholder="Type your AI prompt here..."
                rows={6}
            />
            
            <div className="editor-footer">
                <span className="char-count">{promptText.length}/1000</span>
                <button 
                    className="e-btn e-primary"
                    onClick={() => assistRef.current?.executePrompt(promptText)}
                    disabled={!promptText.trim()}
                >
                    Generate Response
                </button>
            </div>
        </div>
    );

    // Custom response template
    const responseTemplate = (context: any) => {
        const { response, prompt, index } = context;
        
        return (
            <div className="custom-response-panel">
                <div className="response-header">
                    <span className="badge">Response #{index + 1}</span>
                    <span className="timestamp">
                        {new Date().toLocaleString()}
                    </span>
                </div>
                
                <div className="original-prompt">
                    <label>Your prompt:</label>
                    <p>{prompt}</p>
                </div>
                
                <div className="ai-response">
                    <label>AI generated:</label>
                    <div className="response-text">{response}</div>
                </div>
                
                <div className="response-actions">
                    <button 
                        className="e-btn e-small e-outline"
                        onClick={() => {
                            navigator.clipboard.writeText(response);
                            alert('Copied!');
                        }}
                    >
                        Copy Response
                    </button>
                    <button 
                        className="e-btn e-small e-outline"
                        onClick={() => assistRef.current?.executePrompt(`Improve this: ${response}`)}
                    >
                        Improve
                    </button>
                </div>
            </div>
        );
    };

    const handlePromptRequest = (args: any) => {
        // Simulate AI processing
        setTimeout(() => {
            const response = `AI response to: "${args.prompt}"`;
            assistRef.current?.addResponse(response);
        }, 1500);
    };

    return (
        <div className="full-custom-assistant">
            <h2>AI Writing Assistant</h2>
            
            <InlineAIAssistComponent
                ref={assistRef}
                editorTemplate={editorTemplate}
                responseTemplate={responseTemplate}
                promptRequest={handlePromptRequest}
                popupWidth="600px"
            />
        </div>
    );
};
```

### Example 2: Content Editor Integration

```tsx
const ContentEditorWithAI: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [editorContent, setEditorContent] = React.useState('');

    const editorTemplate = () => (
        <div className="prompt-panel">
            <h4>What would you like to generate?</h4>
            <select className="e-input" style={{ marginBottom: '10px' }}>
                <option>Generate blog post</option>
                <option>Summarize text</option>
                <option>Expand content</option>
                <option>Rewrite for SEO</option>
            </select>
            
            <textarea
                className="e-input"
                placeholder="Provide context or instructions..."
                rows={4}
            />
        </div>
    );

    const responseTemplate = (context: any) => (
        <div className="content-response">
            <div className="response-preview">
                <h4>Generated Content:</h4>
                <div className="preview-box">
                    {context.response}
                </div>
            </div>
            
            <div className="response-options">
                <button 
                    className="e-btn e-success"
                    onClick={() => {
                        setEditorContent(context.response);
                        assistRef.current?.hidePopup();
                    }}
                >
                    ✓ Use This Content
                </button>
                <button className="e-btn e-outline">
                    🔄 Regenerate
                </button>
                <button className="e-btn e-outline">
                    ✎ Edit First
                </button>
            </div>
        </div>
    );

    return (
        <div className="content-editor">
            <div className="editor-toolbar">
                <button 
                    className="e-btn e-primary"
                    onClick={() => assistRef.current?.showPopup()}
                >
                    ✨ AI Generate
                </button>
            </div>
            
            <div
                className="editor-area"
                contentEditable
                dangerouslySetInnerHTML={{ __html: editorContent }}
            />
            
            <InlineAIAssistComponent
                ref={assistRef}
                editorTemplate={editorTemplate}
                responseTemplate={responseTemplate}
                responseMode="Popup"
                popupWidth="700px"
                popupHeight="500px"
            />
        </div>
    );
};
```

### Example 3: Code Assistant

```tsx
const CodeAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const editorTemplate = () => (
        <div className="code-prompt-panel">
            <label>Code Operation:</label>
            <div className="operation-buttons">
                <button className="e-btn e-small">Explain</button>
                <button className="e-btn e-small">Optimize</button>
                <button className="e-btn e-small">Debug</button>
                <button className="e-btn e-small">Add Comments</button>
            </div>
            
            <label>Selected Code:</label>
            <pre className="code-preview">
                <code>{/* Show selected code here */}</code>
            </pre>
            
            <label>Additional Instructions:</label>
            <textarea className="e-input" rows={3} />
        </div>
    );

    const responseTemplate = (context: any) => {
        const hasCode = context.response.includes('```');
        
        return (
            <div className="code-response">
                <div className="response-tabs">
                    <button className="tab active">Result</button>
                    <button className="tab">Explanation</button>
                    <button className="tab">Diff</button>
                </div>
                
                <div className="code-result">
                    {hasCode ? (
                        <pre className="language-javascript">
                            <code>{context.response}</code>
                        </pre>
                    ) : (
                        <p>{context.response}</p>
                    )}
                </div>
                
                <div className="code-actions">
                    <button className="e-btn e-success">Apply Changes</button>
                    <button className="e-btn e-outline">Copy Code</button>
                    <button className="e-btn e-outline">Ask Follow-up</button>
                </div>
            </div>
        );
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            editorTemplate={editorTemplate}
            responseTemplate={responseTemplate}
        />
    );
};
```

## Best Practices

### EditorTemplate Best Practices

1. **Maintain Input Element:** Ensure your custom editor has a way to capture user input
2. **Accessibility:** Include proper labels and ARIA attributes
3. **Focus Management:** Auto-focus the input when template renders
4. **Validation:** Implement input validation for length, format, etc.
5. **User Feedback:** Show character/word counts, validation errors
6. **Submit Method:** Provide clear way to submit (button, Enter key, etc.)
7. **Responsive:** Ensure template works on mobile devices

### ResponseTemplate Best Practices

1. **Consistent Styling:** Match your application's design system
2. **Loading States:** Show loading indicator while generating response
3. **Error Handling:** Gracefully display error messages
4. **Accessibility:** Use semantic HTML and proper ARIA labels
5. **Interactive Elements:** Add copy, share, rate functionality
6. **Performance:** Avoid heavy computations in template rendering
7. **Sanitization:** Sanitize HTML content to prevent XSS attacks
8. **Markdown Support:** Consider using markdown parser for formatted responses

### General Template Guidelines

1. **Keep It Simple:** Don't overcomplicate the UI
2. **Test Thoroughly:** Verify templates with various input/output sizes
3. **CSS Scoping:** Use specific class names to avoid CSS conflicts
4. **State Management:** Handle component state properly in React templates
5. **Event Handling:** Properly bind and cleanup event listeners
6. **Mobile-First:** Design templates to work on all screen sizes
7. **Theme Integration:** Use Syncfusion's CSS variables for consistency

## Styling Custom Templates

### Example CSS for Custom Editor

```css
.custom-editor-panel {
    padding: 15px;
    background: #f9fafb;
    border-radius: 8px;
}

.editor-toolbar {
    display: flex;
    gap: 5px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e5e7eb;
}

.editor-textarea {
    width: 100%;
    min-height: 120px;
    padding: 10px;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-family: inherit;
    resize: vertical;
}

.editor-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.char-count {
    font-size: 12px;
    color: #6b7280;
}
```

### Example CSS for Custom Response

```css
.custom-response-panel {
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.response-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #e5e7eb;
}

.badge {
    background: #3b82f6;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}

.response-text {
    padding: 15px;
    background: #f9fafb;
    border-left: 3px solid #3b82f6;
    border-radius: 4px;
    line-height: 1.6;
}

.response-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #e5e7eb;
}
```

---

````