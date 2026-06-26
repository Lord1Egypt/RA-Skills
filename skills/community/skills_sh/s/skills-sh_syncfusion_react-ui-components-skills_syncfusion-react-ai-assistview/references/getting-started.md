# Getting Started with AI AssistView

## Table of Contents
- [Installing Syncfusion Packages](#installing-syncfusion-packages)
- [Adding Component to Application](#adding-component-to-application)
- [CSS Theme Configuration](#css-theme-configuration)
- [Basic Example](#basic-example)
- [TypeScript Support](#typescript-support)

## Installing Syncfusion Packages

The AI AssistView component is distributed as part of the `@syncfusion/ej2-react-interactive-chat` package. Install it along with required package:

```bash
npm install @syncfusion/ej2-react-interactive-chat --save
```

### For AI Integration (Optional)

If integrating with AI services, install the markdown parser:

```bash
npm install marked --save
```

## Adding Component to Application

### Basic Component Import

In your `src/App.tsx` or `src/App.jsx`:

```tsx
import { AIAssistViewComponent } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';

function App() {
    return (
        <AIAssistViewComponent id="aiAssistView"></AIAssistViewComponent>
    );
}

export default App;
```

### With Handler Function

Add event handlers for more functionality:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';

function App() {
    const assistInstance = React.useRef<AIAssistViewComponent>(null);
    
    const onPromptRequest = (args: PromptRequestEventArgs) => {
        // Handle user prompt submission
        console.log('User prompt:', args.prompt);
        
        // Add response after delay
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response to: ' + args.prompt);
        }, 1000);
    };
  
    return (
        <AIAssistViewComponent 
            id="aiAssistView" 
            ref={assistInstance}
            promptRequest={onPromptRequest}
        />
    );
}

export default App;
```

## CSS Theme Configuration

### Add Theme to Application

Import the required CSS files in your `src/App.css` or `src/main.tsx`:

```css
/* Material Theme (Recommended) */
@import '@syncfusion/ej2-base/styles/material.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/material.css';
```

### Available Theme Options

Replace `material` with any of these options:

```css
/* Bootstrap 5 Theme */
@import '@syncfusion/ej2-base/styles/bootstrap5.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/bootstrap5.css';

/* Tailwind CSS Theme */
@import '@syncfusion/ej2-base/styles/tailwind.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/tailwind.css';

/* Fluent Theme */
@import '@syncfusion/ej2-base/styles/fluent.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/fluent.css';

/* Bootstrap Theme */
@import '@syncfusion/ej2-base/styles/bootstrap.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/bootstrap.css';

/* High Contrast Theme */
@import '@syncfusion/ej2-base/styles/highcontrast.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/highcontrast.css';
```

### In main.tsx or index.tsx

```tsx
import './App.css'
import App from './App.tsx'
import React from 'react'
import ReactDOM from 'react-dom/client'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Basic Example

Create a complete working application in `src/App.tsx`:

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';
import './App.css';

function App() {
    const assistInstance = React.useRef<AIAssistViewComponent>(null);
    
    const onPromptRequest = (args: PromptRequestEventArgs) => {
        // Simulate AI response with delay
        setTimeout(() => {
            const response = `You asked: "${args.prompt}". This is a simulated response.`;
            assistInstance.current?.addPromptResponse(response);
        }, 1000);
    };

    return (
        <div className="app-container">
            <h1>AI Chat Assistant</h1>
            <AIAssistViewComponent
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={onPromptRequest}
                prompt="How can I assist you today?"
                promptSuggestions={[
                    'What is React?',
                    'How to use AI AssistView?',
                    'Tell me about Syncfusion'
                ]}
            />
        </div>
    );
}

export default App;
```

### Add Styling to src/App.css

```css
@import '@syncfusion/ej2-base/styles/material.css';
@import '@syncfusion/ej2-react-interactive-chat/styles/material.css';

.app-container {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 20px;
    box-sizing: border-box;
}

.app-container h1 {
    margin: 0 0 20px 0;
    font-size: 24px;
}

#aiAssistView {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}
```

## TypeScript Support

### Full TypeScript Example

```tsx
import { 
    AIAssistViewComponent, 
    PromptRequestEventArgs,
    PromptModel 
} from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';
import './App.css';

const App: React.FC = () => {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    
    const initialPrompts: PromptModel[] = [
        {
            prompt: "What is React?",
            response: "React is a JavaScript library for building user interfaces."
        }
    ];

    const handlePromptRequest = (args: PromptRequestEventArgs): void => {
        setTimeout(() => {
            const response: string = `Response to: ${args.prompt}`;
            assistInstance.current?.addPromptResponse(response);
        }, 1000);
    };

    return (
        <AIAssistViewComponent
            id="aiAssistView"
            ref={assistInstance}
            prompts={initialPrompts}
            promptRequest={handlePromptRequest}
            prompt="How can I help?"
            promptSuggestions={['Help', 'About', 'Guide']}
        />
    );
};

export default App;
```

### Rendering to DOM

In `src/main.tsx`:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

In `index.html`:

```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Chat Assistant</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
</body>
</html>
```

## Common Setup Issues

**Issue**: CSS not loading  
**Solution**: Ensure CSS imports are before your custom styles, reload browser cache

**Issue**: Component not rendering  
**Solution**: Verify the container element exists and has proper dimensions

**Issue**: TypeScript errors  
**Solution**: Install type definitions: `npm install --save-dev @types/react`
