# Response Settings

## Table of Contents
- [Overview](#overview)
- [Built-in Response Items](#built-in-response-items)
- [Response Item Properties](#response-item-properties)
- [Adding Custom Response Items](#adding-custom-response-items)
- [Grouping Response Items](#grouping-response-items)
- [Handling Response Selection](#handling-response-selection)
- [Complete Examples](#complete-examples)

## Overview

Response settings control what actions users can take on AI-generated responses. By default, responses show "Accept" and "Reject" actions, but you can customize these with additional actions like "Edit", "Save", "Copy", or domain-specific actions.

Response items are configured through the `responseSettings` property using the `ResponseSettingsModel` interface.

## Built-in Response Items

The component includes two built-in response items by default:

| Item | Label | Action | Purpose |
|------|-------|--------|---------|
| `accept` | Accept | Accepts the response | Confirms use of AI-generated content |
| `reject` | Reject | Discards the response | Rejects the current response |

These appear automatically in the response popup when a response is generated.

### Default Behavior

```tsx
// These items appear automatically
<InlineAIAssistComponent />

// Built-in items always present:
// - Accept button
// - Reject button
```

## Response Item Properties

Each custom response item supports these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the response item |
| `label` | string | Yes | Display text shown in response popup |
| `iconCss` | string | No | CSS class for icon display |
| `disabled` | boolean | No | Disable item (default: false) |
| `tooltip` | string | No | Tooltip text on hover |
| `groupBy` | string | No | Group name for organization |

## Adding Custom Response Items

Use the `responseSettings` property to add custom items alongside built-in items:

### Basic Custom Items

```tsx
import { InlineAIAssistComponent, ResponseSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const responseSettings: ResponseSettingsModel = {
        items: [
            {
                id: 'edit',
                label: 'Edit'
            },
            {
                id: 'copy',
                label: 'Copy'
            }
        ]
    };

    return (
        <InlineAIAssistComponent responseSettings={responseSettings} />
    );
};

export default App;
```

The built-in "Accept" and "Reject" items will be added automatically along with your custom items.

### Custom Items with Icons

```tsx
const responseSettings: ResponseSettingsModel = {
    items: [
        {
            id: 'save-as-draft',
            label: 'Save as Draft',
            iconCss: 'e-icons e-save'
        },
        {
            id: 'publish',
            label: 'Publish',
            iconCss: 'e-icons e-upload'
        },
        {
            id: 'regenerate',
            label: 'Regenerate',
            iconCss: 'e-icons e-refresh'
        },
        {
            id: 'copy-clipboard',
            label: 'Copy',
            iconCss: 'e-icons e-copy'
        }
    ]
};
```

### Conditional Response Items

Enable/disable items based on application state:

```tsx
const App: React.FC = () => {
    const [canPublish, setCanPublish] = React.useState(false);

    const responseSettings: ResponseSettingsModel = {
        items: [
            {
                id: 'save-draft',
                label: 'Save as Draft',
                disabled: false
            },
            {
                id: 'publish',
                label: 'Publish',
                disabled: !canPublish  // Disable until validation passes
            }
        ]
    };

    return (
        <InlineAIAssistComponent responseSettings={responseSettings} />
    );
};
```

## Grouping Response Items

Use `groupBy` to organize response items into logical sections:

```tsx
const responseSettings: ResponseSettingsModel = {
    items: [
        {
            id: 'save-draft',
            label: 'Save as Draft',
            groupBy: 'Save'
        },
        {
            id: 'save-template',
            label: 'Save as Template',
            groupBy: 'Save'
        },
        {
            id: 'share-email',
            label: 'Share via Email',
            groupBy: 'Share'
        },
        {
            id: 'share-social',
            label: 'Share on Social',
            groupBy: 'Share'
        },
        {
            id: 'export-pdf',
            label: 'Export as PDF',
            groupBy: 'Export'
        },
        {
            id: 'export-word',
            label: 'Export as Word',
            groupBy: 'Export'
        }
    ]
};
```

The popup will display group headers automatically, organizing items visually.

## Handling Response Selection

Detect when a response item is selected using the `itemSelect` event:

### Basic Event Handler

```tsx
import { ResponseItemSelectEventArgs } from '@syncfusion/ej2-react-interactive-chat';

const handleResponseItemSelect = (args: ResponseItemSelectEventArgs) => {
    console.log('Selected item:', args.command.id);
    console.log('Item label:', args.command.label);
};

const responseSettings: ResponseSettingsModel = {
    items: [
        { id: 'save', label: 'Save' },
        { id: 'copy', label: 'Copy' }
    ],
    itemSelect: handleResponseItemSelect
};

<InlineAIAssistComponent responseSettings={responseSettings} />
```

### Advanced Event Handler with Logic

```tsx
const handleResponseItemSelect = (args: ResponseItemSelectEventArgs) => {
    const itemId = args.command.id;
    const assistRef = useRef<InlineAIAssistComponent>(null);

    // Get the latest response
    const lastResponse = assistRef.current?.prompts?.[
        assistRef.current.prompts.length - 1
    ]?.response;

    switch (itemId) {
        case 'accept':
            console.log('Response accepted');
            saveContentToDatabase(lastResponse);
            break;
        case 'reject':
            console.log('Response rejected');
            assistRef.current?.hidePopup();
            break;
        case 'copy':
            navigator.clipboard.writeText(lastResponse);
            showNotification('Copied to clipboard');
            break;
        case 'edit':
            openEditorMode(lastResponse);
            break;
        default:
            console.log('Unknown action:', itemId);
    }
};
```

### Handling Built-in Items

```tsx
const handleResponseItemSelect = (args: ResponseItemSelectEventArgs) => {
    if (args.command.label === 'Accept') {
        // Handle accept
        if (editableRef.current) {
            editableRef.current.innerHTML = lastResponse;
        }
    } else if (args.command.label === 'Reject') {
        // Handle reject - close popup
        assistRef.current?.hidePopup();
    }
};
```

## Complete Examples

### Example 1: Content Publishing Workflow

```tsx
const ContentPublisher: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const responseSettings: ResponseSettingsModel = {
        items: [
            {
                id: 'save-draft',
                label: 'Save as Draft',
                iconCss: 'e-icons e-save'
            },
            {
                id: 'schedule',
                label: 'Schedule Publish',
                iconCss: 'e-icons e-calendar'
            },
            {
                id: 'publish-now',
                label: 'Publish Now',
                iconCss: 'e-icons e-upload'
            }
        ],
        itemSelect: (args) => {
            const response = assistRef.current?.prompts?.[
                assistRef.current.prompts.length - 1
            ]?.response;

            switch (args.command.id) {
                case 'save-draft':
                    saveAsDraft(response);
                    break;
                case 'schedule':
                    openScheduleDialog(response);
                    break;
                case 'publish-now':
                    publishContent(response);
                    break;
            }
        }
    };

    const handlePromptRequest = () => {
        setTimeout(() => {
            const generatedContent = 'AI-generated content here...';
            assistRef.current?.addResponse(generatedContent);
        }, 1000);
    };

    return (
        <div className="content-publisher">
            <textarea placeholder="Your content..." />
            <InlineAIAssistComponent
                ref={assistRef}
                responseSettings={responseSettings}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
};
```

### Example 2: Code Review Assistant

```tsx
const CodeReviewAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const responseSettings: ResponseSettingsModel = {
        items: [
            {
                id: 'apply-suggestion',
                label: 'Apply Suggestion',
                iconCss: 'e-icons e-check',
                groupBy: 'Action'
            },
            {
                id: 'copy-suggestion',
                label: 'Copy',
                iconCss: 'e-icons e-copy',
                groupBy: 'Action'
            },
            {
                id: 'ask-more',
                label: 'Ask More Details',
                iconCss: 'e-icons e-chat',
                groupBy: 'Action'
            },
            {
                id: 'view-docs',
                label: 'View Documentation',
                iconCss: 'e-icons e-help',
                groupBy: 'Learn'
            }
        ],
        itemSelect: (args) => {
            switch (args.command.id) {
                case 'apply-suggestion':
                    applyCodeChange(getLastResponse());
                    break;
                case 'copy-suggestion':
                    copyToClipboard(getLastResponse());
                    break;
                case 'ask-more':
                    assistRef.current?.showPopup();
                    break;
                case 'view-docs':
                    openDocumentation();
                    break;
            }
        }
    };

    return (
        <pre>
            {`// Your code here`}
            <InlineAIAssistComponent
                ref={assistRef}
                responseSettings={responseSettings}
            />
        </pre>
    );
};
```

### Example 3: Writing Assistant with Feedback

```tsx
const WritingAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [feedback, setFeedback] = React.useState<string[]>([]);

    const responseSettings: ResponseSettingsModel = {
        items: [
            {
                id: 'use-suggestion',
                label: 'Use This',
                iconCss: 'e-icons e-check'
            },
            {
                id: 'mark-helpful',
                label: 'Mark Helpful',
                iconCss: 'e-icons e-thumb-up'
            },
            {
                id: 'not-helpful',
                label: 'Not Helpful',
                iconCss: 'e-icons e-thumb-down'
            },
            {
                id: 'explain',
                label: 'Explain Why',
                iconCss: 'e-icons e-info'
            }
        ],
        itemSelect: (args) => {
            const response = getLastResponse();
            const timestamp = new Date().toLocaleTimeString();

            switch (args.command.id) {
                case 'use-suggestion':
                    insertContent(response);
                    break;
                case 'mark-helpful':
                    recordFeedback('helpful', response);
                    break;
                case 'not-helpful':
                    recordFeedback('not-helpful', response);
                    break;
                case 'explain':
                    assistRef.current?.executePrompt(
                        'Explain your previous suggestion'
                    );
                    break;
            }
        }
    };

    return (
        <div className="writing-assistant">
            <textarea id="content" placeholder="Write your content..." />
            <InlineAIAssistComponent
                ref={assistRef}
                responseSettings={responseSettings}
            />
        </div>
    );
};
```

## Best Practices

1. **Descriptive Labels:** Use action verbs ("Save as Draft" not "Draft")
2. **Consistent Icons:** Use Syncfusion icon set for visual consistency
3. **Logical Grouping:** Organize related actions (Save, Share, Export)
4. **Feedback Loop:** Track which items users select for analytics
5. **Conditional Items:** Disable items that aren't applicable
6. **Clear Intent:** Each item should have a clear, distinct action
7. **Tooltips:** Add tooltips for ambiguous actions
8. **Error Handling:** Handle edge cases where response is unavailable
9. **Workflow Support:** Design items to support your content workflow
