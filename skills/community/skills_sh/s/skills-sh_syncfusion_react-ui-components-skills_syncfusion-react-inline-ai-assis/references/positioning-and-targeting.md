# Positioning and Targeting

## Table of Contents
- [Overview](#overview)
- [relateTo Property](#relateto-property)
- [target Property](#target-property)
- [responseMode Property](#responsemode-property)
- [Practical Positioning Examples](#practical-positioning-examples)

## Overview

The Inline AI Assist component can be positioned in three ways:

1. **Default:** Positioned relative to viewport (no specific positioning)
2. **relateTo:** Positioned relative to a specific DOM element (buttons, text fields, etc.)
3. **target:** Appended to a specific container element

The `responseMode` property controls how AI responses are displayed: inline (replaces content) or popup (floating window).

## relateTo Property

The `relateTo` property positions the component popup relative to a specific DOM element. This is useful for attaching the AI assistant to buttons, text areas, or other UI elements.

### Accepts Two Types of Values

**1. CSS Selector String**
```tsx
<InlineAIAssistComponent relateTo="#button-id" />
<InlineAIAssistComponent relateTo=".trigger-button" />
<InlineAIAssistComponent relateTo="[data-role='assist']" />
```

**2. HTMLElement Reference**
```tsx
const targetElement = document.getElementById('summarize-btn');
<InlineAIAssistComponent relateTo={targetElement} />
```

### Practical Example: Attach to Button

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const handleSummarizeClick = () => {
        // Logic for summarize action
    };

    return (
        <div>
            <button 
                id="summarize-btn" 
                className="e-btn e-primary"
                onClick={handleSummarizeClick}
            >
                Summarize Text
            </button>
            
            <InlineAIAssistComponent
                id="inlineAssist"
                relateTo="#summarize-btn"
                popupWidth="500px"
            />
        </div>
    );
};

export default App;
```

### Example: Multiple Trigger Points

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [activeTarget, setActiveTarget] = React.useState<string>('#summarize');

    return (
        <div>
            <button id="summarize" onClick={() => setActiveTarget('#summarize')}>
                Summarize
            </button>
            <button id="expand" onClick={() => setActiveTarget('#expand')}>
                Expand
            </button>
            <button id="rephrase" onClick={() => setActiveTarget('#rephrase')}>
                Rephrase
            </button>
            
            <InlineAIAssistComponent
                ref={assistRef}
                relateTo={activeTarget}
            />
        </div>
    );
};
```

## target Property

The `target` property specifies where the component should be appended in the DOM. This is different from `relateTo` which positions relative to an element but doesn't change the DOM parent.

### Accepts Two Types of Values

**1. CSS Selector String**
```tsx
<InlineAIAssistComponent target="#container" />
<InlineAIAssistComponent target=".app-wrapper" />
```

**2. HTMLElement Reference**
```tsx
const container = document.querySelector('.main-content');
<InlineAIAssistComponent target={container} />
```

### Example: Append to Container

```tsx
const App: React.FC = () => {
    return (
        <div className="main-app">
            <div className="toolbar">
                <button>Edit</button>
            </div>
            
            {/* Component will be appended here */}
            <div id="assist-container" className="assist-area"></div>
            
            <InlineAIAssistComponent
                target="#assist-container"
                popupWidth="100%"
            />
        </div>
    );
};
```

## responseMode Property

The `responseMode` property controls how AI responses are displayed to the user.

### Mode: "Popup" (Default)

Responses appear in a floating popup window:

```tsx
<InlineAIAssistComponent responseMode="Popup" popupWidth="400px" />
```

**Characteristics:**
- Response shows in overlay popup
- User can accept/reject response
- Popup can be positioned and sized
- Original content remains visible behind popup

**Best for:**
- Non-destructive operations (preview before accepting)
- Long responses that need space
- Comparing original and modified content

### Mode: "Inline"

Responses replace content directly in-place:

```tsx
<InlineAIAssistComponent responseMode="Inline" />
```

**Characteristics:**
- Response replaces original content immediately
- No separate popup window
- Faster workflow (no popup interaction)
- Content is replaced, not compared

**Best for:**
- Quick edits and corrections
- Grammar/spelling fixes
- Content transformations where preview not needed

### Example: Toggle Response Modes

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React, { useState } from 'react';

const App: React.FC = () => {
    const [responseMode, setResponseMode] = useState<'Popup' | 'Inline'>('Popup');

    const toggleMode = () => {
        setResponseMode(responseMode === 'Popup' ? 'Inline' : 'Popup');
    };

    return (
        <div>
            <button onClick={toggleMode} className="e-btn">
                Mode: {responseMode}
            </button>
            
            <InlineAIAssistComponent
                responseMode={responseMode}
                popupWidth="500px"
            />
        </div>
    );
};

export default App;
```

## Practical Positioning Examples

### Example 1: Text Editor with AI Assist

Position Inline AI Assist relative to a text editor:

```tsx
const TextEditor: React.FC = () => {
    const editorRef = React.useRef<HTMLDivElement>(null);
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleShowAssist = () => {
        assistRef.current?.showPopup();
    };

    return (
        <div className="editor-container">
            <div className="editor-toolbar">
                <button 
                    className="e-btn e-icon-btn" 
                    id="ai-assist-btn"
                    onClick={handleShowAssist}
                    title="Open AI Assistant"
                >
                    <span className="e-icons">✨</span>
                </button>
            </div>
            
            <div 
                ref={editorRef}
                contentEditable={true}
                className="editor-content"
            >
                Edit your text here...
            </div>
            
            <InlineAIAssistComponent
                ref={assistRef}
                relateTo="#ai-assist-btn"
                responseMode="Popup"
                popupWidth="450px"
            />
        </div>
    );
};
```

### Example 2: Form Field Enhancement

Add AI assist to form fields:

```tsx
const Form: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handleGenerateContent = () => {
        assistRef.current?.showPopup();
    };

    return (
        <form>
            <div className="form-group">
                <label>Description</label>
                <textarea 
                    id="description-field"
                    placeholder="Enter product description..."
                />
                <button 
                    type="button"
                    id="generate-btn"
                    className="e-btn e-small"
                    onClick={handleGenerateContent}
                >
                    Generate with AI
                </button>
            </div>
            
            <InlineAIAssistComponent
                ref={assistRef}
                relateTo="#generate-btn"
                popupWidth="500px"
            />
        </form>
    );
};
```

### Example 3: Floating Assist for Any Content

Position assist independently and control manually:

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [showAssist, setShowAssist] = useState(false);

    const handleShowAssist = (e: React.MouseEvent) => {
        setShowAssist(true);
        assistRef.current?.showPopup({
            x: e.clientX,
            y: e.clientY
        });
    };

    return (
        <div 
            onContextMenu={(e) => {
                e.preventDefault();
                handleShowAssist(e);
            }}
        >
            Right-click anywhere for AI assist...
            
            {showAssist && (
                <InlineAIAssistComponent
                    ref={assistRef}
                    responseMode="Popup"
                    popupWidth="400px"
                />
            )}
        </div>
    );
};
```

### Example 4: Full-Screen Content Assist

Target entire application area:

```tsx
const FullScreenAssist: React.FC = () => {
    return (
        <div className="app-container">
            <div id="app-content">
                {/* Your main content */}
            </div>
            
            <InlineAIAssistComponent
                target="#app-content"
                responseMode="Popup"
                popupWidth="80vw"
                popupHeight="80vh"
            />
        </div>
    );
};
```

## Best Practices

1. **Use `relateTo` for button/trigger:** Position near the interaction point
2. **Use `target` for layouts:** When you need specific DOM nesting
3. **Choose `Popup` mode for:** Non-destructive operations, previewing changes
4. **Choose `Inline` mode for:** Quick, destructive transformations
5. **Set appropriate dimensions:** Match popup size to content type
6. **Store ref:** Use React ref to control popup programmatically
7. **Handle multiple instances:** Different assist components for different areas

## Performance Considerations

- Avoid creating many instances; reuse with dynamic `relateTo`
- Use `target` to maintain DOM structure efficiency
- Consider `Inline` mode for faster interactions
- Lazy-load assist component if only occasionally used
