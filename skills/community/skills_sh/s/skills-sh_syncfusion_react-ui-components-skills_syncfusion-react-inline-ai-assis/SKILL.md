---
name: syncfusion-react-inline-ai-assist
description: Implement the Syncfusion React Inline AI Assist component. Use this skill to add inline AI suggestions, integrate AI services such as OpenAI, Gemini, Lite-LLM, or Ollama, configure command and response actions, customize toolbars, handle events, and support real-time prompt-response workflows in React.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React Syncfusion React Inline AI Assist Component

## Component Overview

The Inline AI Assist component provides intelligent text processing capabilities for your React applications. It enables AI-powered suggestions, content generation, and interactive prompt-response workflows with support for multiple AI service integrations.

### Key Capabilities

- **Multi-AI Service Integration**: Connect to OpenAI, Google Gemini, Lite-LLM, and Ollama for flexible AI backend options
- **Real-Time Response Streaming**: Enable `enableStreaming` for progressive response updates during content generation
- **Command & Response Actions**: Configure predefined commands for quick AI tasks and custom response actions
- **Inline Toolbar**: Add custom toolbar items with icons, buttons, and separators for enhanced user interactions
- **Inline & Popup Modes**: Display AI responses inline with existing content or in a floating popup window
- **Flexible Template Customization**: Customize prompt input and response display using string, function, or JSX templates
- **Internationalization (i18n) & RTL**: Support for multiple languages and right-to-left text direction
- **Event Handling**: Lifecycle events including `created`, `promptRequest`, `open`, and `close` for precise control
- **Public Methods**: Programmatic access with `addResponse()`, `executePrompt()`, `showPopup()`, and more
- **Prompt History**: Track prompt-response conversations with persistent history management
- **Accessibility & Theming**: Compatible with Material, Bootstrap, Fluent, and Tailwind CSS themes

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm
- CSS theme imports (Material, Bootstrap, Fluent, Tailwind)
- Component rendering
- Custom styling with `cssClass` property
- Running your first example

### Template Customization
📄 **Read:** [references/template-customization.md](references/template-customization.md)
- `editorTemplate` property: Customize prompt input area
- `responseTemplate` property: Customize response display
- String templates, function templates, JSX.Element templates
- Rich text editor integration
- Voice input integration
- Code syntax highlighting
- Markdown rendering

### Internationalization (i18n) and RTL
📄 **Read:** [references/internationalization.md](references/internationalization.md)
- `locale` property: Set language and regional formatting
- `enableRtl` property: Enable right-to-left text direction
- Available locale codes and setup
- Arabic, Hebrew, Persian support
- Multi-language applications
- Browser language detection
- Custom localization strings

### Positioning and Targeting
📄 **Read:** [references/positioning-and-targeting.md](references/positioning-and-targeting.md)
- `relateTo` property: Position relative to DOM elements
- `target` property: Specify where to append the component
- `responseMode` property: Inline vs Popup display modes
- Practical positioning scenarios

### Command Settings
📄 **Read:** [references/command-settings.md](references/command-settings.md)
- Configure command items for quick actions
- Command properties: id, label, iconCss, disabled, prompt, tooltip
- Group commands with `groupBy` property
- Handle `itemSelect` events
- Set popup dimensions

### Response Settings
📄 **Read:** [references/response-settings.md](references/response-settings.md)
- Built-in response items (accept, reject)
- Adding custom response actions
- Response item properties and configuration
- Group response items with `groupBy`
- Handle response `itemSelect` events

### Inline Toolbar Customization
📄 **Read:** [references/inline-toolbar.md](references/inline-toolbar.md)
- Configure toolbar items (buttons, separators, inputs)
- Built-in items and custom items
- Item properties: text, iconCss, type, visible, disabled, align
- Tab key navigation with `tabIndex`
- Custom item templates
- Toolbar positioning: Inline vs Bottom
- `itemClick` event handling with complete event args

### Events
📄 **Read:** [references/events.md](references/events.md)
- `created` event: Component render complete
- `promptRequest` event: Prompt submitted by user
- `open` event: Popup opened
- `close` event: Popup closed
- Event handler patterns and examples

### Methods
📄 **Read:** [references/methods.md](references/methods.md)
- `addResponse(response)`: Add AI response to component
- `executePrompt(prompt)`: Execute prompt dynamically
- `showPopup(coordinates)`: Open the popup
- `hidePopup()`: Close the popup
- `showCommandPopup()`: Show command actions
- `hideCommandPopup()`: Hide command actions

### AI Service Integrations
📄 **Read:** [references/ai-integrations.md](references/ai-integrations.md)
- `enableStreaming` property: Real-time response streaming
- OpenAI API integration with streaming
- Google Gemini AI integration with streaming
- Lite-LLM service integration
- Ollama local LLM integration with streaming
- API credential setup
- Prompt handling and response streaming
- Performance optimization and error handling

## Quick Start

```jsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

function App() {
    const assistRef = React.useRef(null);

    const handlePromptRequest = () => {
        // Simulate AI response
        setTimeout(() => {
            const response = 'Your AI-generated response here';
            assistRef.current?.addResponse(response);
        }, 1000);
    };

    const handleShowPopup = () => {
        assistRef.current?.showPopup();
    };

    return (
        <div>
            <button onClick={handleShowPopup} className="e-btn e-primary">
                Ask AI
            </button>
            <InlineAIAssistComponent
                id="inlineAssist"
                ref={assistRef}
                relateTo="button"
                promptRequest={handlePromptRequest}
                popupWidth="500px"
            />
        </div>
    );
}

export default App;
```

## Common Patterns

### Pattern 1: AI-Assisted Text Editing
Combine the component with a contentEditable div to enable AI-powered suggestions while editing:

```jsx
const handleResponseItemSelect = (args) => {
    if (args.command.label === 'Accept') {
        const lastResponse = assistRef.current.prompts?.[assistRef.current.prompts.length - 1]?.response;
        if (lastResponse && editableRef.current) {
            editableRef.current.innerHTML = lastResponse;
        }
    }
};

<InlineAIAssistComponent
    responseSettings={{
        itemSelect: handleResponseItemSelect
    }}
/>
```

### Pattern 2: Command-Based Actions
Set up predefined commands for common AI tasks:

```jsx
const commandSettings = {
    commands: [
        { id: 'summarize', label: 'Summarize', iconCss: 'e-icons e-compress', prompt: 'Summarize this text' },
        { id: 'expand', label: 'Expand', iconCss: 'e-icons e-expand', prompt: 'Expand this text' },
        { id: 'fix', label: 'Fix Grammar', iconCss: 'e-icons e-check-box', prompt: 'Fix grammar and spelling' }
    ]
};

<InlineAIAssistComponent commandSettings={commandSettings} />
```

### Pattern 3: Custom Toolbar Actions
Add custom toolbar items to trigger component methods:

```jsx
const handleToolbarItemClick = (args) => {
    if (args.item.id === 'customAction') {
        assistRef.current?.executePrompt('User-defined prompt');
    }
};

const inlineToolbarSettings = {
    items: [
        { id: 'customAction', text: 'Custom', iconCss: 'e-icons e-settings' }
    ],
    itemClick: handleToolbarItemClick
};
```

### Pattern 4: Response Display Modes
Switch between inline editing and popup responses:

```jsx
// Inline mode: Response appears inline
<InlineAIAssistComponent responseMode="Inline" />

// Popup mode: Response in floating popup
<InlineAIAssistComponent responseMode="Popup" popupWidth="400px" />
```

### Pattern 5: Lifecycle Management
Use events to coordinate component state:

```jsx
const handleCreated = () => {
    console.log('Component initialized');
};

const handlePromptRequest = (args) => {
    console.log('Prompt submitted:', args.prompt);
};

<InlineAIAssistComponent
    created={handleCreated}
    promptRequest={handlePromptRequest}
    open={() => console.log('Popup opened')}
    close={() => console.log('Popup closed')}
/>
```

## Key Configuration Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `editorTemplate` | string \| function \| JSX.Element | '' | Custom prompt input template |
| `responseTemplate` | string \| function \| JSX.Element | '' | Custom response display template |
| `enableStreaming` | boolean | false | Enable real-time response streaming |
| `locale` | string | 'en-US' | Language and regional formatting |
| `enableRtl` | boolean | false | Enable right-to-left text direction |
| `enablePersistence` | boolean | false | Persist component state across reloads |
| `cssClass` | string | '' | Custom CSS classes for styling |
| `relateTo` | string \| HTMLElement | - | Position component relative to element |
| `target` | string \| HTMLElement | 'body' | Specify append target |
| `responseMode` | string | 'Popup' | 'Inline' or 'Popup' |
| `popupWidth` | string \| number | '400px' | Popup width (CSS value) |
| `popupHeight` | string \| number | 'auto' | Popup height |
| `zIndex` | number | 1000 | Popup z-index |
| `placeholder` | string | 'Ask or generate AI content..' | Prompt textarea placeholder |
| `prompt` | string | '' | Default prompt text |
| `prompts` | array | [] | Prompt-response collection |
| `commandSettings` | CommandSettingsModel | null | Command configuration |
| `responseSettings` | ResponseSettingsModel | null | Response action configuration |
| `inlineToolbarSettings` | InlineToolbarSettingsModel | null | Toolbar customization |


**For complete examples and advanced scenarios, explore individual reference files above.**
