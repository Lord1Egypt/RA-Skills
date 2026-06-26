````markdown
# Mentions and Labels

## Table of Contents
- [Overview](#overview)
- [Mention Feature (`users`)](#mention-feature-users)
- [Label Feature (`labelSettings`)](#label-feature-labelsettings)
- [Content Models for Mention and Label](#content-models-for-mention-and-label)
- [Complete Example](#complete-example)

## Overview

The BlockEditor supports two special inline content types:

| Feature | Trigger | Prop | Content Type |
|---|---|---|---|
| **Mention** | `@` | `users` | `ContentType.Mention` |
| **Label** | Configurable (default `$`) | `labelSettings` | `ContentType.Label` |

Both features insert structured inline content into a block's `content` array using `ContentType.Mention` or `ContentType.Label` along with a typed `properties` object.

---

## Mention Feature (`users`)

### `users` Prop

**Type:** `UserModel[]`  
**Default:** `[]`

Provide a list of users to enable the `@mention` feature. When the user types `@` in the editor, a popup appears listing the available users.

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="block-editor"
            users={[
                {
                    id: 'user1',
                    user: 'Alice Johnson',
                    avatarUrl: 'https://example.com/alice.png',
                    avatarBgColor: '#4caf50'
                },
                {
                    id: 'user2',
                    user: 'Bob Smith',
                    avatarBgColor: '#2196f3'
                },
                {
                    id: 'user3',
                    user: 'Carol White',
                    avatarBgColor: '#ff9800',
                    cssClass: 'admin-user'
                }
            ]}
        />
    );
}

export default App;
```

### `UserModel` Interface

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier for the user. Used in `IMentionContentSettings.userId`. |
| `user` | `string` | Display name of the user shown in the mention popup. |
| `avatarUrl` | `string` | URL of the user's avatar image. |
| `avatarBgColor` | `string` | Background color for the user's avatar (used when no `avatarUrl` is provided). |
| `cssClass` | `string` | CSS class applied to the user's block element. |

---

## Label Feature (`labelSettings`)

### `labelSettings` Prop

**Type:** `LabelSettingsModel`  
**Default:** `{}`

Configure available labels and the trigger character for the label picker.

```tsx
import { BlockEditorComponent } from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    return (
        <BlockEditorComponent
            id="block-editor"
            labelSettings={{
                triggerChar: '$',
                items: [
                    { id: 'label1', text: 'Important', labelColor: '#e53935' },
                    { id: 'label2', text: 'Review', labelColor: '#1e88e5' },
                    { id: 'label3', text: 'Approved', labelColor: '#43a047', iconCss: 'e-icons e-check' },
                    { id: 'label4', text: 'Bug', labelColor: '#fb8c00', groupBy: 'Issues' },
                    { id: 'label5', text: 'Feature', labelColor: '#8e24aa', groupBy: 'Issues' }
                ]
            }}
        />
    );
}

export default App;
```

### `LabelSettingsModel` Interface

| Property | Type | Default | Description |
|---|---|---|---|
| `items` | `LabelItemModel[]` | — | Array of label items available for selection. |
| `triggerChar` | `string` | `'$'` | Character that triggers the label picker popup. |

### `LabelItemModel` Interface

| Property | Type | Description |
|---|---|---|
| `id` | `string` | Unique identifier for the label. Used in `ILabelContentSettings.labelId`. |
| `text` | `string` | Display text for the label. |
| `labelColor` | `string` | Color of the label for visual distinction (e.g., `'#ff0000'`). |
| `iconCss` | `string` | CSS class for the label's icon. |
| `groupBy` | `string` | Group header for categorizing labels in the picker popup. |

---

## Content Models for Mention and Label

When a mention or label is inserted into a block's `content` array, each item uses the `ContentModel` structure with a typed `properties` object.

### `IMentionContentSettings`

Used with `contentType: ContentType.Mention`.

| Property | Type | Description |
|---|---|---|
| `userId` | `string` | The ID of the user being mentioned. Must match a `UserModel.id` from the `users` prop. |

### `ILabelContentSettings`

Used with `contentType: ContentType.Label`.

| Property | Type | Description |
|---|---|---|
| `labelId` | `string` | The ID of the label item being referenced. Must match a `LabelItemModel.id` from `labelSettings.items`. |

### Inline Content Array Examples

```tsx
import { BlockModel, ContentType } from '@syncfusion/ej2-react-blockeditor';

// Block with a mention embedded in text
const blockWithMention: BlockModel = {
    id: 'block-1',
    blockType: 'Paragraph',
    content: [
        { contentType: ContentType.Text, content: 'Hello ' },
        {
            contentType: ContentType.Mention,
            content: '@Alice Johnson',       // display text
            properties: { userId: 'user1' } // IMentionContentSettings
        },
        { contentType: ContentType.Text, content: ', please review this.' }
    ]
};

// Block with a label embedded in text
const blockWithLabel: BlockModel = {
    id: 'block-2',
    blockType: 'Paragraph',
    content: [
        { contentType: ContentType.Text, content: 'Status: ' },
        {
            contentType: ContentType.Label,
            content: 'Important',            // display text
            properties: { labelId: 'label1' } // ILabelContentSettings
        }
    ]
};
```

> ⚠️ `ContentType.Mention` and `ContentType.Label` are valid enum values. Do **not** use `ContentType.Code`, `ContentType.Image`, or `ContentType.Embed` — these do not exist in the API.

---

## Complete Example

```tsx
import {
    BlockEditorComponent,
    BlockModel,
    ContentType,
    UserModel,
    LabelSettingsModel
} from '@syncfusion/ej2-react-blockeditor';
import * as React from 'react';

function App() {
    const users: UserModel[] = [
        { id: 'user1', user: 'Alice Johnson', avatarUrl: 'https://example.com/alice.png', avatarBgColor: '#4caf50' },
        { id: 'user2', user: 'Bob Smith', avatarBgColor: '#2196f3' },
        { id: 'user3', user: 'Carol White', avatarBgColor: '#ff9800' }
    ];

    const labelSettings: LabelSettingsModel = {
        triggerChar: '$',
        items: [
            { id: 'label1', text: 'Important', labelColor: '#e53935' },
            { id: 'label2', text: 'Review', labelColor: '#1e88e5' },
            { id: 'label3', text: 'Approved', labelColor: '#43a047' }
        ]
    };

    const initialBlocks: BlockModel[] = [
        {
            id: 'block-1',
            blockType: 'Heading',
            properties: { level: 1 },
            content: [{ contentType: ContentType.Text, content: 'Project Notes' }]
        },
        {
            id: 'block-2',
            blockType: 'Paragraph',
            content: [
                { contentType: ContentType.Text, content: 'Assigned to ' },
                {
                    contentType: ContentType.Mention,
                    content: '@Alice Johnson',
                    properties: { userId: 'user1' }
                },
                { contentType: ContentType.Text, content: ' — status: ' },
                {
                    contentType: ContentType.Label,
                    content: 'Review',
                    properties: { labelId: 'label2' }
                }
            ]
        },
        {
            id: 'block-3',
            blockType: 'Paragraph',
            content: [
                { contentType: ContentType.Text, content: 'Type @ to mention a user, or $ to add a label.' }
            ]
        }
    ];

    return (
        <BlockEditorComponent
            id="block-editor"
            blocks={initialBlocks}
            users={users}
            labelSettings={labelSettings}
        />
    );
}

export default App;
```

### Summary

| Task | How |
|---|---|
| Enable mentions | Pass `users={UserModel[]}` to the component |
| Enable labels | Pass `labelSettings={{ triggerChar, items }}` |
| Trigger mention popup | Type `@` in the editor |
| Trigger label popup | Type the `triggerChar` (default `$`) |
| Reference a mention in block data | `contentType: ContentType.Mention`, `properties: { userId }` |
| Reference a label in block data | `contentType: ContentType.Label`, `properties: { labelId }` |
````
