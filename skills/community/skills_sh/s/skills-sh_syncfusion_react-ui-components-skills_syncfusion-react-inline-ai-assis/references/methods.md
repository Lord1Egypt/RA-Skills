# Methods

## Table of Contents
- [Overview](#overview)
- [addResponse Method](#addresponse-method)
- [executePrompt Method](#executeprompt-method)
- [showPopup Method](#showpopup-method)
- [hidePopup Method](#hidepopup-method)
- [showCommandPopup Method](#showcommandpopup-method)
- [hideCommandPopup Method](#hidecommandpopup-method)
- [Method Patterns](#method-patterns)
- [Complete Examples](#complete-examples)

## Overview

The Inline AI Assist component exposes several public methods to programmatically control its behavior. These methods allow you to add responses, execute prompts, show/hide popups, and manage command actions without user interaction.

To use methods, you must store a reference to the component using `React.useRef`:

```tsx
const assistRef = React.useRef<InlineAIAssistComponent>(null);

<InlineAIAssistComponent ref={assistRef} />

// Later, call methods
assistRef.current?.addResponse('AI response');
```

## addResponse Method

Programmatically add an AI response to the component.

### Signature

```tsx
addResponse(response: string): void
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `response` | string | The AI-generated response text |

### When to Use

- Integrate custom AI services (OpenAI, Gemini, Lite-LLM)
- Add responses from backend APIs
- Simulate AI responses for testing
- Process responses before displaying

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleAddResponse = () => {
        const response = 'This is an AI-generated response';
        assistRef.current?.addResponse(response);
    };

    return (
        <div>
            <button onClick={handleAddResponse}>Add Response</button>
            <InlineAIAssistComponent ref={assistRef} />
        </div>
    );
};

export default App;
```

### Example: Add Response on Prompt

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = () => {
        // Simulate AI processing
        setTimeout(() => {
            const response = 'AI has processed your request';
            assistRef.current?.addResponse(response);
        }, 1500);
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};
```

### Example: Add Formatted Response

```tsx
const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
    callAIAPI(args.prompt).then(result => {
        // Format response
        const formatted = `
            <strong>Summary:</strong>
            ${result.summary}
            
            <strong>Details:</strong>
            ${result.details}
        `;
        assistRef.current?.addResponse(formatted);
    });
};
```

## executePrompt Method

Programmatically execute a prompt, which triggers the `promptRequest` event.

### Signature

```tsx
executePrompt(prompt: string): void
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | The prompt text to execute |

### When to Use

- Trigger preset prompts programmatically
- Execute command/action prompts automatically
- Create keyboard shortcuts for common prompts
- Implement batch prompt processing

### Basic Usage

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleSummarize = () => {
        assistRef.current?.executePrompt('Please summarize this text in 2-3 sentences');
    };

    return (
        <div>
            <button onClick={handleSummarize}>Summarize</button>
            <InlineAIAssistComponent ref={assistRef} />
        </div>
    );
};
```

### Example: Preset Prompts

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const promptPresets = {
        summarize: 'Summarize this content',
        expand: 'Expand with more details',
        simplify: 'Simplify this text',
        checkGrammar: 'Check grammar and spelling'
    };

    const handlePresetPrompt = (preset: keyof typeof promptPresets) => {
        assistRef.current?.executePrompt(promptPresets[preset]);
    };

    return (
        <div>
            <button onClick={() => handlePresetPrompt('summarize')}>Summarize</button>
            <button onClick={() => handlePresetPrompt('expand')}>Expand</button>
            <button onClick={() => handlePresetPrompt('simplify')}>Simplify</button>
            <button onClick={() => handlePresetPrompt('checkGrammar')}>Fix Grammar</button>
            <InlineAIAssistComponent ref={assistRef} />
        </div>
    );
};
```

### Example: Keyboard Shortcut

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    React.useEffect(() => {
        const handleKeyPress = (e: KeyboardEvent) => {
            // Ctrl+Alt+S for summarize
            if (e.ctrlKey && e.altKey && e.code === 'KeyS') {
                e.preventDefault();
                assistRef.current?.executePrompt('Summarize this text');
            }
            // Ctrl+Alt+E for expand
            if (e.ctrlKey && e.altKey && e.code === 'KeyE') {
                e.preventDefault();
                assistRef.current?.executePrompt('Expand this text with more details');
            }
        };

        window.addEventListener('keydown', handleKeyPress);
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, []);

    return <InlineAIAssistComponent ref={assistRef} />;
};
```

## showPopup Method

Open the component popup, optionally at specific coordinates.

### Signature

```tsx
showPopup(x: number, y: number): void
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `x` | number (optional) | x coordinates for popup position |
| `y` | number (optional) | y coordinates for popup position |

### When to Use

- Open popup on button click
- Position popup at mouse coordinates
- Show assist on context menu
- Trigger from keyboard shortcuts

### Basic Usage

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleShowAssist = () => {
        assistRef.current?.showPopup();
    };

    return (
        <div>
            <button onClick={handleShowAssist}>Open AI Assist</button>
            <InlineAIAssistComponent ref={assistRef} />
        </div>
    );
};
```

### Example: Position at Coordinates

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleContextMenu = (e: React.MouseEvent) => {
        e.preventDefault();
        assistRef.current?.showPopup(e.clientX, e.clientY);
    };

    return (
        <textarea onContextMenu={handleContextMenu}>
            Right-click anywhere...
        </textarea>
    );
};
```

### Example: Show Near Button

```tsx
const handleShowNearButton = (buttonElement: HTMLElement) => {
    const rect = buttonElement.getBoundingClientRect();
    assistRef.current?.showPopup(rect.left, rect.bottom + 10);
};
```

## hidePopup Method

Close the component popup.

### Signature

```tsx
hidePopup(): void
```

### When to Use

- Close popup after user action
- Hide popup on ESC key
- Close when operation completes
- Programmatic flow control

### Basic Usage

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleAcceptResponse = () => {
        // Accept response logic
        assistRef.current?.hidePopup();
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            responseSettings={{
                itemSelect: () => handleAcceptResponse()
            }}
        />
    );
};
```

### Example: Close After Timeout

```tsx
const handlePromptRequest = () => {
    setTimeout(() => {
        const response = 'Processing complete';
        assistRef.current?.addResponse(response);

        // Auto-close after 3 seconds
        setTimeout(() => {
            assistRef.current?.hidePopup();
        }, 3000);
    }, 1000);
};
```

## showCommandPopup Method

Open the command action popup (if commands are configured).

### Signature

```tsx
showCommandPopup(): void
```

### Requirements

- Must be called when component popup is already open
- Requires commands configured via `commandSettings`

### When to Use

- Show command menu programmatically
- Alternative to clicking command button
- Implement custom command triggers

### Basic Usage

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleShowCommands = () => {
        // First ensure popup is open
        assistRef.current?.showPopup();

        // Then show command popup
        setTimeout(() => {
            assistRef.current?.showCommandPopup();
        }, 100);
    };

    const commandSettings = {
        commands: [
            { id: 'summarize', label: 'Summarize', prompt: 'Summarize this' }
        ]
    };

    return (
        <div>
            <button onClick={handleShowCommands}>Show Commands</button>
            <InlineAIAssistComponent
                ref={assistRef}
                commandSettings={commandSettings}
            />
        </div>
    );
};
```

## hideCommandPopup Method

Close the command action popup.

### Signature

```tsx
hideCommandPopup(): void
```

### When to Use

- Close command menu after selection
- Hide menu programmatically
- Flow control in event handlers

### Basic Usage

```tsx
const handleCommandSelect = (args: CommandItemSelectEventArgs) => {
    console.log('Command selected:', args.command.id);
    assistRef.current?.hideCommandPopup();
};
```

## Method Patterns

### Pattern 1: Full Workflow

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleWorkflow = async () => {
        // 1. Show popup
        assistRef.current?.showPopup();

        // 2. Execute preset prompt
        assistRef.current?.executePrompt('Analyze this content');

        // 3. In promptRequest handler, add response (automatic)
        // 4. User accepts response
        // 5. Close popup
        setTimeout(() => {
            assistRef.current?.hidePopup();
        }, 3000);
    };

    return (
        <button onClick={handleWorkflow}>Start Workflow</button>
    );
};
```

### Pattern 2: Method Chaining

```tsx
const performAssistAction = (assistRef: React.RefObject<InlineAIAssistComponent>) => {
    assistRef.current?.showPopup();
    setTimeout(() => {
        assistRef.current?.executePrompt('Your prompt');
    }, 200);
};
```

### Pattern 3: Conditional Method Calls

```tsx
const handleUserInteraction = (action: string) => {
    switch (action) {
        case 'open':
            assistRef.current?.showPopup();
            break;
        case 'close':
            assistRef.current?.hidePopup();
            break;
        case 'execute':
            assistRef.current?.executePrompt('User prompt');
            break;
        case 'showCommands':
            assistRef.current?.showCommandPopup();
            break;
        default:
            break;
    }
};
```

## Complete Examples

### Example 1: Text Editor Integration

```tsx
const TextEditor: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const editorRef = React.useRef<HTMLDivElement>(null);

    const handleSummarize = () => {
        const selectedText = window.getSelection()?.toString();
        if (selectedText) {
            assistRef.current?.showPopup();
            assistRef.current?.executePrompt(`Summarize: ${selectedText}`);
        }
    };

    const handleAddResponse = (response: string) => {
        if (editorRef.current) {
            editorRef.current.innerHTML = response;
        }
        assistRef.current?.hidePopup();
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        processWithAI(args.prompt).then(response => {
            assistRef.current?.addResponse(response);
        });
    };

    return (
        <div>
            <button onClick={handleSummarize}>Summarize Selection</button>
            <div
                ref={editorRef}
                contentEditable
                className="editor"
            >
                Your text here...
            </div>
            <InlineAIAssistComponent
                ref={assistRef}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
};
```

### Example 2: Multi-Step Prompt Workflow

```tsx
const PromptWorkflow: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [step, setStep] = React.useState(0);

    const prompts = [
        'Analyze this content',
        'Identify key points',
        'Generate summary'
    ];

    const handleNextStep = () => {
        if (step < prompts.length) {
            assistRef.current?.executePrompt(prompts[step]);
            setStep(step + 1);
        } else {
            assistRef.current?.hidePopup();
            setStep(0);
        }
    };

    React.useEffect(() => {
        if (step === 0) {
            assistRef.current?.showPopup();
        }
    }, []);

    return (
        <div>
            <InlineAIAssistComponent
                ref={assistRef}
                responseSettings={{
                    itemSelect: () => handleNextStep()
                }}
            />
        </div>
    );
};
```

### Example 3: Batch Processing

```tsx
const BatchAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [items, setItems] = React.useState<string[]>([]);

    const processBatch = async (batch: string[]) => {
        for (const item of batch) {
            assistRef.current?.showPopup();
            assistRef.current?.executePrompt(`Process: ${item}`);

            // Wait for response
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
        assistRef.current?.hidePopup();
    };

    return (
        <button onClick={() => processBatch(['Item 1', 'Item 2', 'Item 3'])}>
            Process Batch
        </button>
    );
};
```

## Best Practices

1. **Check Refs:** Always verify `assistRef.current` exists before calling methods
2. **Async Operations:** Wrap methods in setTimeout if immediate execution fails
3. **User Feedback:** Show loading states while processing
4. **Error Handling:** Wrap method calls in try-catch blocks
5. **Performance:** Avoid calling methods excessively in loops
6. **Cleanup:** Remove listeners and clear refs on component unmount
7. **Documentation:** Comment method sequences for maintainability
