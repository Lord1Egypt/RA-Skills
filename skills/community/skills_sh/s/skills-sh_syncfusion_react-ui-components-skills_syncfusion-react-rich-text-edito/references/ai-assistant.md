# AI Assistant in Syncfusion React Rich Text Editor

## Table of Contents
- [Overview](#overview)
- [Integrating the AI Assistant](#integrating-the-ai-assistant)
- [AI Commands and Prompts](#ai-commands-and-prompts)
- [Handling Responses](#handling-responses)
- [Customizing the AI Toolbar](#customizing-the-ai-toolbar)
- [Popup Dimensions](#popup-dimensions)
- [Using Public Methods](#using-public-methods)

## Overview

The AI Assistant in the Rich Text Editor provides integrated AI capabilities for simplified content creation, editing, and enhancement. It includes an AssistView presented inside a pop-up interface, a dropdown of predefined prompts, and dedicated toolbar options for initiating AI interactions.

## Integrating the AI Assistant

To enable the AI Assistant:

1. Add the `AIAssistant` service to the **Inject** array
2. Include `AICommands` and `AIQuery` in the `toolbarSettings.items` property
3. Configure the `aiAssistantSettings` with your AI backend endpoint

### Installation

```bash
npm install @syncfusion/ej2-react-richtexteditor
```

### Importing Styles

The Rich Text Editor AI Assistant requires additional style references for proper rendering. Add the following to your **src/App.css**:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-richtexteditor/styles/tailwind3.css';

/* Required for AI Assistant */
@import '../node_modules/@syncfusion/ej2-interactive-chat/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css';
```

### Basic Setup with Functional Component

```tsx
import { HtmlEditor, Image, Inject, Link, QuickToolbar, RichTextEditorComponent, Toolbar, AIAssistant, AIAssistantSettingsModel, ToolbarSettingsModel } from '@syncfusion/ej2-react-richtexteditor';
import * as React from 'react';

function App() {
    const editor = React.createRef<RichTextEditorComponent>();
    const toolbarSettings: ToolbarSettingsModel = { items: ['AICommands', 'AIQuery'] };
    const aiAssistantSettings: AIAssistantSettingsModel = {
        popupWidth: '600px',
        popupMaxHeight: '400px'
    };

    return (
        <RichTextEditorComponent
            ref={editor}
            toolbarSettings={toolbarSettings}
            aiAssistantSettings={aiAssistantSettings}
        >
            <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar, AIAssistant]} />
        </RichTextEditorComponent>
    );
}

export default App;
```

## AI Commands and Prompts

The `AICommands` toolbar item opens a menu containing predefined prompts. You can customize the commands and add preloaded prompts and suggestions using the `aiAssistantSettings`.

### Adding Custom Commands

```tsx
function App() {
    const toolbarSettings: ToolbarSettingsModel = { items: ['AICommands', 'AIQuery'] };
    const aiAssistantSettings: AIAssistantSettingsModel = {
        commands: [
            { text: 'Rewrite', prompt: 'Rewrite the content to be more refined.' },
            { text: 'Elaborate', prompt: 'Expand on the following content with more detail and explanation:' },
            {
                text: 'Change Tone',
                items: [
                    { text: 'Professional', prompt: 'Rewrite the following content in a professional tone:' },
                    { text: 'Casual', prompt: 'Rewrite the following content in a casual, conversational tone:' },
                    { text: 'Direct', prompt: 'Rewrite the following content to be more direct and to the point:' },
                ],
            },
        ]
    };

    return (
        <RichTextEditorComponent toolbarSettings={toolbarSettings} aiAssistantSettings={aiAssistantSettings}>
            <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar, AIAssistant]} />
        </RichTextEditorComponent>
    );
}
```

### Preloading Prompts and Suggestions

```tsx
const aiAssistantSettings: AIAssistantSettingsModel = {
    prompts: [
        {
            prompt: 'What is Essential Studio?',
            response: 'Essential Studio is a software toolkit by Syncfusion that offers a variety of UI controls, frameworks, and libraries for developing applications on web, desktop, and mobile platforms.'
        }
    ],
    suggestions: [
        'What are the popular components of Essential Studio?',
        'Which web frameworks are supported by Essential Studio?'
    ]
};
```

## Handling Responses

**Security Warning**
 
The Rich Text Editor does not handle or send requests to AI provider endpoints. All AI interactions must be processed at the application layer (preferably in the backend).
 
Ensure that:
 
* AI inputs are validated and moderated on the backend.
* API keys and secrets are never exposed in request bodies or client-side code.
* All requests to AI services are securely routed and managed through backend systems.

Executing a prompt triggers the `aiAssistantPromptRequest` event. You can handle streaming or non-streaming responses using the `addAIPromptResponse` method.

### Handling Streaming Responses

```tsx
const onPromptRequest = async (args: AIAssistantPromptRequestArgs) => {
    const response = await fetch('/api/ai/stream', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: args.prompt + args.text }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error);
    }

    const stream = response.body.pipeThrough(new TextDecoderStream());
    let fullText = '';

    for await (const chunk of stream as unknown as AsyncIterable<string>) {
        fullText += chunk;
        editor.current?.addAIPromptResponse(fullText, false);
    }

    editor.current?.addAIPromptResponse(fullText, true);
};
```

### Handling Non-Streaming Responses

```tsx
const onPromptRequest = async (args: AIAssistantPromptRequestArgs) => {    
    const response = await fetch('/api/ai/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: args.prompt + args.text }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.text();
    editor.current?.addAIPromptResponse(data, true);
};
```

## Customizing the AI Toolbar

Configure the toolbar items displayed in the Header, Prompt, and Response sections using the toolbar settings properties.

### Available Toolbar Items

| Toolbar | Items |
|---------|-------|
| **Header** | `AIcommands` – Opens AI command options<br>`Close` – Closes the AI Assistant popup<br>`Clear` – Clear conversations |
| **Prompt** | `Edit` – Modify the prompt text<br>`Copy` – Copy prompt to clipboard |
| **Response** | `Regenerate` – Produce new response<br>`Copy` – Copy AI response<br>`\|` – Visual separator<br>`Insert` – Insert response into editor |

### Customizing Toolbar Configuration

```tsx
const aiAssistantSettings: AIAssistantSettingsModel = {
    headerToolbarSettings: ['AIcommands', 'Clear', 'Close'],
    promptToolbarSettings: ['Edit', 'Copy'],
    responseToolbarSettings: ['Regenerate', 'Copy', '|', 'Insert'],
    prompts: [
        {
            prompt: 'What is Essential Studio?',
            response: 'Essential Studio is a software toolkit by Syncfusion...'
        }
    ]
};

<RichTextEditorComponent aiAssistantSettings={aiAssistantSettings}>
    <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar, AIAssistant]} />
</RichTextEditorComponent>
```

## Popup Dimensions

Customize the width and maximum height of the AI Assistant popup to fit your editor layout.

```tsx
const aiAssistantSettings: AIAssistantSettingsModel = {
    popupWidth: '600px',      // or use numbers for pixels: 600
    popupMaxHeight: '500px'   // or use numbers for pixels: 500
};

<RichTextEditorComponent aiAssistantSettings={aiAssistantSettings}>
    <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar, AIAssistant]} />
</RichTextEditorComponent>
```

## Using Public Methods

Manage the AI Assistant programmatically using public methods.

### Available Methods

| Method | Description |
|--------|-------------|
| `getAIPromptHistory()` | Get conversation history |
| `executeAIPrompt(prompt: string)` | Send a prompt to the AI Assistant |
| `addAIPromptResponse(response: string, isFinalUpdate?: boolean)` | Add response to AI Assistant |
| `showAIAssistantPopup()` | Show the AI Assistant popup |
| `hideAIAssistantPopup()` | Hide the AI Assistant popup |
| `clearAIPromptHistory()` | Clear all conversation history |

### Proofread Use Case Example

```tsx
function App() {
    const editor = React.createRef<RichTextEditorComponent>();
    const toolbarSettings = { items: ['AICommands', 'AIQuery'] };
    
    const onPromptRequest = () => {
        setTimeout(() => {
            const aiResponse = 'Dear Valued Customer, We are writing to inform you that there has been a recent change to our policies...';
            editor.current?.addAIPromptResponse(aiResponse, false);
            editor.current?.addAIPromptResponse(aiResponse, true);
        }, 300);
    };

    const reviewContent = () => {
        editor.current?.showAIAssistantPopup();
        editor.current?.executeAIPrompt('Proof read the editor content.');
    };

    return (
        <div>
            <RichTextEditorComponent
                ref={editor}
                toolbarSettings={toolbarSettings}
                aiAssistantPromptRequest={onPromptRequest}
            >
                <p>Your content here...</p>
                <Inject services={[Toolbar, Image, Link, HtmlEditor, QuickToolbar, AIAssistant]} />
            </RichTextEditorComponent>
            <br />
            <button className="e-btn e-primary" onClick={reviewContent}>
                <span className="e-icons e-btn-icon e-check-large"></span>Proof read
            </button>
        </div>
    );
}

export default App;
```

### Saving Conversation History

```tsx
const onSaveBtnClick = () => {
    const promptHistory = editor.current?.getAIPromptHistory();
    console.log(promptHistory);
    // Handle DB Post and save history to the DB
};

<button className="e-btn e-primary" onClick={onSaveBtnClick}>
    <span className="e-icons e-save"></span>Save
</button>
```
