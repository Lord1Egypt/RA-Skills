# Command Settings

## Table of Contents
- [Overview](#overview)
- [Command Item Properties](#command-item-properties)
- [Configuring Commands](#configuring-commands)
- [Grouping Commands](#grouping-commands)
- [Handling Command Selection](#handling-command-selection)
- [Popup Dimensions](#popup-dimensions)
- [Complete Examples](#complete-examples)

## Overview

Commands provide quick-access actions for users to trigger predefined AI prompts. When a user clicks the command icon in the inline assistant, a popup menu displays all configured commands. Selecting a command executes the associated prompt automatically.

Commands are configured through the `commandSettings` property using the `CommandSettingsModel` interface.

## Command Item Properties

Each command item in the `commands` array supports these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the command |
| `label` | string | Yes | Display text shown in command popup |
| `prompt` | string | Yes | AI prompt to execute when selected |
| `iconCss` | string | No | CSS class for icon display |
| `disabled` | boolean | No | Disable command (default: false) |
| `tooltip` | string | No | Tooltip text on hover |
| `groupBy` | string | No | Group name for command organization |

## Configuring Commands

### Basic Command Configuration

```tsx
import { InlineAIAssistComponent, CommandSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const commandSettings: CommandSettingsModel = {
        commands: [
            {
                id: 'summarize',
                label: 'Summarize',
                prompt: 'Please summarize this text in 2-3 sentences'
            },
            {
                id: 'expand',
                label: 'Expand',
                prompt: 'Please expand this text with more details and examples'
            },
            {
                id: 'simplify',
                label: 'Simplify',
                prompt: 'Rewrite this text in simpler, easier-to-understand language'
            }
        ]
    };

    return (
        <InlineAIAssistComponent commandSettings={commandSettings} />
    );
};

export default App;
```

### Adding Icons to Commands

Use Syncfusion icon CSS classes for consistency:

```tsx
const commandSettings: CommandSettingsModel = {
    commands: [
        {
            id: 'summarize',
            label: 'Summarize',
            iconCss: 'e-icons e-compress',
            prompt: 'Summarize this text concisely'
        },
        {
            id: 'translate',
            label: 'Translate to Spanish',
            iconCss: 'e-icons e-globe',
            prompt: 'Translate this text to Spanish'
        },
        {
            id: 'tone-formal',
            label: 'Formal Tone',
            iconCss: 'e-icons e-style',
            prompt: 'Rewrite this text in a formal, professional tone'
        },
        {
            id: 'tone-casual',
            label: 'Casual Tone',
            iconCss: 'e-icons e-chat',
            prompt: 'Rewrite this text in a casual, conversational tone'
        }
    ]
};
```

### Disabling Commands Conditionally

```tsx
const App: React.FC = () => {
    const [hasSelectedText, setHasSelectedText] = React.useState(false);

    const commandSettings: CommandSettingsModel = {
        commands: [
            {
                id: 'summarize',
                label: 'Summarize',
                prompt: 'Summarize: ',
                disabled: !hasSelectedText
            },
            {
                id: 'expand',
                label: 'Expand',
                prompt: 'Expand: ',
                disabled: !hasSelectedText
            }
        ]
    };

    const handleTextSelect = () => {
        setHasSelectedText(true);
    };

    return (
        <div>
            <textarea onSelect={handleTextSelect} />
            <InlineAIAssistComponent commandSettings={commandSettings} />
        </div>
    );
};
```

## Grouping Commands

Use the `groupBy` property to organize commands into logical groups. The popup displays group headers automatically.

```tsx
const commandSettings: CommandSettingsModel = {
    commands: [
        // Content Generation group
        {
            id: 'generate-title',
            label: 'Generate Title',
            groupBy: 'Generate',
            prompt: 'Generate a catchy title for this content'
        },
        {
            id: 'generate-summary',
            label: 'Generate Summary',
            groupBy: 'Generate',
            prompt: 'Generate a summary for this content'
        },
        // Content Refinement group
        {
            id: 'fix-grammar',
            label: 'Fix Grammar',
            groupBy: 'Refinement',
            prompt: 'Fix all grammar and spelling errors'
        },
        {
            id: 'improve-clarity',
            label: 'Improve Clarity',
            groupBy: 'Refinement',
            prompt: 'Improve the clarity and readability of this text'
        },
        // Transformation group
        {
            id: 'to-bullet-points',
            label: 'Convert to Bullet Points',
            groupBy: 'Transform',
            prompt: 'Convert this text to a bulleted list'
        },
        {
            id: 'to-paragraph',
            label: 'Convert to Paragraph',
            groupBy: 'Transform',
            prompt: 'Convert this list to paragraph format'
        }
    ]
};
```

## Handling Command Selection

Detect when a command is selected using the `itemSelect` event:

### Basic Event Handler

```tsx
import { CommandItemSelectEventArgs } from '@syncfusion/ej2-react-interactive-chat';

const handleCommandSelect = (args: CommandItemSelectEventArgs) => {
    console.log('Selected command ID:', args.command.id);
    console.log('Command label:', args.command.label);
    console.log('Prompt:', args.command.prompt);
};

const commandSettings: CommandSettingsModel = {
    commands: [
        { id: 'cmd1', label: 'Command 1', prompt: 'Prompt 1' }
    ],
    itemSelect: handleCommandSelect
};

<InlineAIAssistComponent commandSettings={commandSettings} />
```

### Advanced Event Handler with Logging

```tsx
const handleCommandSelect = (args: CommandItemSelectEventArgs) => {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] Command executed: ${args.command.label}`);
    
    // Log to analytics
    trackAnalytics('command_selected', {
        commandId: args.command.id,
        label: args.command.label
    });
    
    // Show notification
    showNotification(`Executing: ${args.command.label}`);
};
```

### Conditional Logic Based on Selected Command

```tsx
const handleCommandSelect = (args: CommandItemSelectEventArgs) => {
    switch (args.command.id) {
        case 'summarize':
            console.log('User requested summary');
            break;
        case 'expand':
            console.log('User requested expansion');
            break;
        case 'fix-grammar':
            console.log('User requested grammar check');
            break;
        default:
            console.log('Unknown command');
    }
};
```

## Popup Dimensions

Control the command popup size using `popupWidth` and `popupHeight`:

```tsx
const commandSettings: CommandSettingsModel = {
    popupWidth: '300px',      // CSS value or number (px)
    popupHeight: '400px',     // CSS value or number (px)
    commands: [
        { id: 'cmd1', label: 'Command 1', prompt: 'Prompt 1' }
    ]
};

<InlineAIAssistComponent commandSettings={commandSettings} />
```

### Responsive Dimensions

```tsx
const getCommandPopupWidth = () => {
    return window.innerWidth < 600 ? '250px' : '350px';
};

const commandSettings: CommandSettingsModel = {
    popupWidth: getCommandPopupWidth(),
    commands: [...]
};
```

## Complete Examples

### Example 1: Content Editor with Writing Commands

```tsx
const ContentEditor: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const commandSettings: CommandSettingsModel = {
        commands: [
            {
                id: 'enhance-writing',
                label: 'Enhance Writing',
                iconCss: 'e-icons e-edit',
                prompt: 'Improve the writing quality, clarity, and engagement'
            },
            {
                id: 'check-tone',
                label: 'Check Tone',
                iconCss: 'e-icons e-comment',
                prompt: 'Analyze the tone and suggest improvements for professionalism'
            },
            {
                id: 'plagiarism-check',
                label: 'Check Plagiarism',
                iconCss: 'e-icons e-search',
                prompt: 'Check for plagiarism and suggest unique alternatives'
            }
        ],
        popupWidth: '280px',
        itemSelect: (args) => {
            console.log('Writing command selected:', args.command.label);
        }
    };

    return (
        <div className="editor">
            <textarea id="content-area" placeholder="Write your content..." />
            <InlineAIAssistComponent
                ref={assistRef}
                commandSettings={commandSettings}
            />
        </div>
    );
};
```

### Example 2: Code Assistant with Development Commands

```tsx
const CodeAssistant: React.FC = () => {
    const commandSettings: CommandSettingsModel = {
        commands: [
            {
                id: 'explain',
                label: 'Explain Code',
                iconCss: 'e-icons e-help',
                prompt: 'Explain what this code does in simple terms',
                groupBy: 'Understanding'
            },
            {
                id: 'optimize',
                label: 'Optimize',
                iconCss: 'e-icons e-speed',
                prompt: 'Optimize this code for better performance',
                groupBy: 'Optimization'
            },
            {
                id: 'add-comments',
                label: 'Add Comments',
                iconCss: 'e-icons e-note',
                prompt: 'Add helpful comments to explain the code',
                groupBy: 'Documentation'
            },
            {
                id: 'find-bugs',
                label: 'Find Bugs',
                iconCss: 'e-icons e-bug',
                prompt: 'Identify potential bugs and issues in this code',
                groupBy: 'Quality'
            }
        ],
        popupWidth: '320px',
        popupHeight: '350px'
    };

    return (
        <pre id="code-editor">
            {`function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i < items.length; i++) {
        total = total + items[i].price;
    }
    return total;
}`}
            <InlineAIAssistComponent commandSettings={commandSettings} />
        </pre>
    );
};
```

### Example 3: E-Commerce with Product Commands

```tsx
const ProductManager: React.FC = () => {
    const commandSettings: CommandSettingsModel = {
        commands: [
            {
                id: 'improve-description',
                label: 'Improve Description',
                prompt: 'Make this product description more compelling and SEO-friendly',
                groupBy: 'SEO'
            },
            {
                id: 'generate-keywords',
                label: 'Generate Keywords',
                prompt: 'Generate relevant keywords for this product',
                groupBy: 'SEO'
            },
            {
                id: 'create-catchy-title',
                label: 'Create Title',
                prompt: 'Create a catchy, keyword-rich product title',
                groupBy: 'Content'
            },
            {
                id: 'write-benefits',
                label: 'Write Benefits',
                prompt: 'Write compelling customer benefits for this product',
                groupBy: 'Content'
            }
        ],
        itemSelect: (args) => {
            console.log('Product optimization command:', args.command.id);
        }
    };

    return (
        <div className="product-editor">
            <textarea placeholder="Product description..." />
            <InlineAIAssistComponent commandSettings={commandSettings} />
        </div>
    );
};
```

## Best Practices

1. **Descriptive Labels:** Use clear, action-oriented labels ("Fix Grammar" vs "Grammar")
2. **Logical Grouping:** Organize related commands by category (Content, Optimization, Quality)
3. **Consistent Icons:** Use Syncfusion icon set for visual consistency
4. **Context-Aware:** Enable/disable commands based on selected content
5. **Detailed Prompts:** Include specific instructions in the prompt string
6. **Popup Sizing:** Set dimensions based on typical command count (5-15 commands fits 250px width)
7. **Error Handling:** Track command selections for analytics and debugging
