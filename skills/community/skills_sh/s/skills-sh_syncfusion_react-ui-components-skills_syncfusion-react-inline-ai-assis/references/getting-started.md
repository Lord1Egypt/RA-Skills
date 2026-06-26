# Getting Started with Inline AI Assist

## Table of Contents
- [Installation](#installation)
- [CSS Theme Setup](#css-theme-setup)
- [Basic Component Rendering](#basic-component-rendering)
- [Running Your Application](#running-your-application)
- [Common Setup Issues](#common-setup-issues)

## Installation

### Install Syncfusion Package

Install the interactive chat package that contains Inline AI Assist:

```bash
npm install @syncfusion/ej2-react-interactive-chat --save
```

This single command installs all required dependencies automatically.

## CSS Theme Setup

Import the required CSS theme files in your main `src/App.css` or `src/index.css`. Choose one of the available themes:

### Material Theme (Recommended for most apps)
```css
@import "../node_modules/@syncfusion/ej2-base/styles/material.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/material.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/material.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/material.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/material.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/material.css";
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/material.css";
```

### Bootstrap Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/bootstrap.css";
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/bootstrap.css";
```

### Fluent Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/fluent.css";
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/fluent.css";
```

### Tailwind Theme
```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-inputs/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-navigations/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-buttons/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-popups/styles/tailwind.css";
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/tailwind.css";
```

> **Tip:** Only import one theme. Importing multiple themes can cause CSS conflicts. All components automatically inherit the active theme.

## Basic Component Rendering

### Minimal Example (JavaScript)

Create a functional component and render Inline AI Assist:

```jsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';
import ReactDOM from 'react-dom';

function App() {
    return (
        <InlineAIAssistComponent id="inlineAiAssist"></InlineAIAssistComponent>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
```

### Minimal Example (TypeScript)

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';
import ReactDOM from 'react-dom';

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent id="inlineAiAssist"></InlineAIAssistComponent>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));
```

### With Event Handlers

```tsx
import { InlineAIAssistComponent, InlinePromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        console.log('User prompt:', args.prompt);
        
        // Simulate AI processing
        setTimeout(() => {
            const aiResponse = 'Your AI-generated response';
            assistRef.current?.addResponse(aiResponse);
        }, 1000);
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

## Running Your Application

After setup, start the development server:

```bash
npm start
```

The app opens automatically at `http://localhost:3000`. You should see the Inline AI Assist component ready to use.

### Verify Installation

Once running, check that:
1. ✅ Component renders without errors in browser console
2. ✅ Styles are applied correctly (buttons, inputs have proper styling)
3. ✅ Component is interactive (can type in prompt field)

## Custom Styling with cssClass

The `cssClass` property allows you to apply custom CSS classes to the root element of the Inline AI Assist component for styling customization.

### Property Details

**Type:** `string`  
**Default:** `''`  
**Component Property:** `cssClass`

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            cssClass="custom-ai-assist"
        />
    );
};

export default App;
```

### Applying Multiple Classes

Use space-separated class names for multiple custom classes:

```tsx
<InlineAIAssistComponent
    cssClass="custom-theme dark-mode elevated"
/>
```

### Example: Custom Theme Colors

**CSS (in your App.css or styles.css):**
```css
/* Custom blue theme */
.blue-theme .e-aiassist-input {
    border-color: #2563eb;
    background-color: #eff6ff;
}

.blue-theme .e-btn.e-primary {
    background-color: #2563eb;
    border-color: #2563eb;
}

.blue-theme .e-btn.e-primary:hover {
    background-color: #1d4ed8;
}

.blue-theme .e-popup {
    border: 2px solid #2563eb;
    border-radius: 12px;
}
```

**Component:**
```tsx
<InlineAIAssistComponent
    cssClass="blue-theme"
    popupWidth="500px"
/>
```

### Example: Dark Mode Styling

```css
/* Dark mode styles */
.dark-mode-assist {
    --bg-color: #1f2937;
    --text-color: #f9fafb;
    --border-color: #374151;
}

.dark-mode-assist .e-aiassist-input {
    background-color: var(--bg-color);
    color: var(--text-color);
    border-color: var(--border-color);
}

.dark-mode-assist .e-popup {
    background-color: var(--bg-color);
    color: var(--text-color);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.dark-mode-assist .e-btn {
    background-color: #374151;
    color: var(--text-color);
    border-color: var(--border-color);
}
```

**Component:**
```tsx
<InlineAIAssistComponent
    cssClass="dark-mode-assist"
/>
```

### Example: Compact Size Variant

```css
/* Compact size */
.compact-assist .e-aiassist-input {
    padding: 8px 12px;
    font-size: 13px;
    min-height: 80px;
}

.compact-assist .e-btn {
    padding: 6px 14px;
    font-size: 12px;
}

.compact-assist .e-popup {
    max-width: 350px;
}
```

**Component:**
```tsx
<InlineAIAssistComponent
    cssClass="compact-assist"
    popupWidth="350px"
/>
```

### Example: Elevated Card Style

```css
/* Elevated card effect */
.elevated-assist {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-radius: 12px;
    padding: 20px;
    background: white;
}

.elevated-assist .e-popup {
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    border-radius: 16px;
    border: 1px solid #e5e7eb;
}

.elevated-assist .e-aiassist-input {
    border-radius: 8px;
    border: 2px solid #e5e7eb;
    transition: border-color 0.2s ease;
}

.elevated-assist .e-aiassist-input:focus {
    border-color: #3b82f6;
    outline: none;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

**Component:**
```tsx
<InlineAIAssistComponent
    cssClass="elevated-assist"
/>
```

### Best Practices for cssClass

1. **Use Specific Class Names:** Avoid generic names that might conflict with other styles
   ```tsx
   // Good
   cssClass="my-app-ai-assist"
   
   // Avoid
   cssClass="container"
   ```

2. **CSS Specificity:** Your custom classes should be specific enough to override default styles
   ```css
   /* Good - specific selector */
   .my-app-ai-assist .e-aiassist-input {
       /* styles */
   }
   
   /* May not work - too generic */
   .e-aiassist-input {
       /* styles */
   }
   ```

3. **Use CSS Variables:** For flexible theming across your app
   ```css
   .custom-theme {
       --primary-color: #3b82f6;
       --secondary-color: #8b5cf6;
       --border-radius: 8px;
   }
   
   .custom-theme .e-btn.e-primary {
       background-color: var(--primary-color);
   }
   ```

4. **Test Across Themes:** If using multiple Syncfusion themes, test your custom CSS with each
   ```tsx
   // Test with Material, Bootstrap, Fluent, etc.
   <InlineAIAssistComponent cssClass="custom-theme" />
   ```

5. **Maintain Accessibility:** Ensure custom colors meet WCAG contrast requirements
   ```css
   /* Ensure sufficient contrast */
   .custom-theme .e-btn {
       background-color: #2563eb; /* Blue */
       color: #ffffff; /* White - good contrast */
   }
   ```

### Common Customization Scenarios

#### Scenario 1: Match Brand Colors

```css
.brand-ai-assist {
    --brand-primary: #ff6b35;
    --brand-secondary: #004e89;
}

.brand-ai-assist .e-btn.e-primary {
    background-color: var(--brand-primary);
    border-color: var(--brand-primary);
}

.brand-ai-assist .e-popup {
    border-top: 4px solid var(--brand-primary);
}
```

#### Scenario 2: Responsive Sizing

```css
.responsive-assist .e-popup {
    width: 90vw;
    max-width: 600px;
}

@media (max-width: 768px) {
    .responsive-assist .e-popup {
        width: 95vw;
    }
    
    .responsive-assist .e-aiassist-input {
        font-size: 16px; /* Prevents zoom on mobile */
    }
}
```

#### Scenario 3: Animation Effects

```css
.animated-assist .e-popup {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Complete Example: Full Custom Theme

**CSS:**
```css
/* Custom professional theme */
.professional-ai-assist {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.professional-ai-assist .e-aiassist-input {
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 15px;
    line-height: 1.5;
    transition: all 0.2s ease;
    background: #ffffff;
}

.professional-ai-assist .e-aiassist-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.professional-ai-assist .e-popup {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
                0 10px 10px -5px rgba(0, 0, 0, 0.04);
    overflow: hidden;
}

.professional-ai-assist .e-btn.e-primary {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    letter-spacing: 0.3px;
    transition: transform 0.2s ease;
}

.professional-ai-assist .e-btn.e-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}
```

**Component:**
```tsx
const ProfessionalAssistant: React.FC = () => {
    return (
        <div className="app-container">
            <h2>AI Writing Assistant</h2>
            
            <InlineAIAssistComponent
                cssClass="professional-ai-assist"
                placeholder="Describe what you'd like to create..."
                popupWidth="600px"
            />
        </div>
    );
};
```

## Common Setup Issues

### Issue: CSS Not Applied (Components Look Unstyled)
**Solution:** Verify CSS imports are in the correct file (App.css or index.css) and the import path matches your node_modules location:
```css
/* Make sure path is correct */
@import "../node_modules/@syncfusion/ej2-react-interactive-chat/styles/material.css";
```

### Issue: Module Not Found Error
**Solution:** Ensure the package is installed:
```bash
npm install @syncfusion/ej2-react-interactive-chat --save
npm install  # Reinstall if needed
```

### Issue: Port 3000 Already in Use
**Solution:** Specify a different port:
```bash
PORT=3001 npm start
```

### Issue: React Version Compatibility
The component requires React 16.8+. Check your React version:
```bash
npm list react
```

### Issue: Custom Styles Not Applying
**Solution:** Check CSS specificity and ensure your custom CSS is loaded after Syncfusion's CSS:
```tsx
// In index.tsx or App.tsx
import '@syncfusion/ej2-react-interactive-chat/styles/material.css';  // First
import './App.css';  // Then your custom CSS
```
