# Rich Text Editor Properties

## Table of Contents
- [Core Properties](#core-properties)
- [Toolbar Properties](#toolbar-properties)
- [Editor Mode & Behavior](#editor-mode--behavior)
- [Value & Content Properties](#value--content-properties)
- [Media Insert Properties](#media-insert-properties)
- [Font, Color & Format Properties](#font-color--format-properties)
- [Paste & Clipboard Properties](#paste--clipboard-properties)
- [Table Properties](#table-properties)
- [AI Assistant Properties](#ai-assistant-properties)
- [Slash Menu Properties](#slash-menu-properties)
- [Import / Export Properties](#import--export-properties)
- [Miscellaneous Properties](#miscellaneous-properties)

---

## Core Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `height` | `string \| number` | `'auto'` | Height of the editor |
| `width` | `string \| number` | `'100%'` | Width of the editor |
| `enabled` | `boolean` | `true` | Enable/disable the editor |
| `readonly` | `boolean` | `false` | Makes the editor read-only |
| `placeholder` | `string` | `''` | Placeholder text when empty |
| `cssClass` | `string` | `null` | Additional CSS class(es) on the root element |
| `htmlAttributes` | `{[key: string]: string}` | `{}` | Extra HTML attributes on the root element |
| `locale` | `string` | `''` | Override locale (default: `'en-US'`) |
| `showTooltip` | `boolean` | `true` | Show/hide toolbar tooltips |

```tsx
<RichTextEditorComponent
  height={450}
  width="100%"
  placeholder="Start typing here..."
  readonly={false}
  cssClass="my-custom-editor"
>
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

---

## Toolbar Properties

### Important Enum Imports

When working with toolbar and editor configurations, you may need to import specific enums:

```tsx
import {
  ToolbarType,        // For toolbarSettings.type
  EditorMode,         // For editorMode property
  SaveFormat,         // For insertImageSettings.saveFormat
  // ... other enums as needed
} from '@syncfusion/ej2-react-richtexteditor';
```

### `toolbarSettings: ToolbarSettingsModel`

Controls the main toolbar appearance and content.

| Property | Type | Description |
|---|---|---|
| `enable` | `boolean` | Show/hide the toolbar |
| `enableFloating` | `boolean` | Sticky floating toolbar on scroll |
| `items` | `(string \| ToolbarItems)[]` | Toolbar buttons (use `'|'` for separator) |
| `position` | `'Top' \| 'Bottom'` | Toolbar position |
| `type` | `ToolbarType` | Toolbar overflow behavior (`ToolbarType.Expand` \| `ToolbarType.MultiRow` \| `ToolbarType.Scrollable`) |

**Important:** The `type` property requires the `ToolbarType` enum, not a string literal. Import it from `@syncfusion/ej2-react-richtexteditor`.

```tsx
import { ToolbarType } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = {
  enable: true,
  enableFloating: true,
  position: 'Top',
  type: ToolbarType.Expand, // Use enum, not string
  items: [
    'Bold', 'Italic', 'Underline', '|',
    'Formats', 'Alignments', '|',
    'OrderedList', 'UnorderedList', '|',
    'CreateLink', 'Image', 'Table', '|',
    'Undo', 'Redo'
  ]
};
```

### `quickToolbarSettings: QuickToolbarSettingsModel`
Inline toolbar that appears when selecting images, links, or tables.

### `floatingToolbarOffset: number`
Pixel offset from the top of the page for the floating toolbar. Default: `0`.

---

## Editor Mode & Behavior

### `editorMode: EditorMode`
Sets the editing mode. Default: `'HTML'`.

**Available modes:**
- `'HTML'` — WYSIWYG HTML editor
- `'Markdown'` — Markdown textarea with preview support

**Note:** Can be used as a string literal or `EditorMode` enum.

```tsx
import { EditorMode } from '@syncfusion/ej2-react-richtexteditor';

// Using string literal (both work)
<RichTextEditorComponent editorMode="Markdown">
  <Inject services={[Toolbar, MarkdownEditor]} />
</RichTextEditorComponent>

// Using enum
<RichTextEditorComponent editorMode={EditorMode.Markdown}>
  <Inject services={[Toolbar, MarkdownEditor]} />
</RichTextEditorComponent>
```

### `iframeSettings: IFrameSettingsModel`
Enables iFrame mode for full CSS isolation.

| Property | Type | Description |
|---|---|---|
| `enable` | `boolean` | Render editor in an `<iframe>` |
| `resources` | `{styles: string[]; scripts: string[]}` | External CSS/JS to inject into iframe |
| `attributes` | `object` | Attributes for the iframe body |
| `sandbox` | `string[]` | Sandbox flags |

```tsx
const iframeSettings: IFrameSettingsModel = {
  enable: true,
  resources: {
    styles: ['url']
  }
};
```

### `inlineMode: InlineModeModel`
Enables inline editing (toolbar appears on selection rather than always visible).

```tsx
const inlineMode: InlineModeModel = { enable: true, onSelection: true };
```

### `enterKey: EnterKey`
Controls what tag is inserted when `Enter` is pressed.

- `'P'` (default) — inserts `<p><br></p>`
- `'DIV'` — inserts `<div>`
- `'BR'` — inserts `<br>`

```tsx
<RichTextEditorComponent enterKey="BR">
  <Inject services={[Toolbar, HtmlEditor]} />
</RichTextEditorComponent>
```

### `enableTabKey: boolean`
Allows the Tab key to insert a tab character in the editor. Default: `false`.

### `enableResize: boolean`
Adds a resize handle to the bottom-right of the editor. Default: `false`.

### `enableRtl: boolean`
Renders the editor in right-to-left direction. Default: `false`.

### `enablePersistence: boolean`
Persists the editor value across page reloads using localStorage. Default: `false`.

---

## Value & Content Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `value` | `string` | `null` | HTML or Markdown content |
| `valueTemplate` | `string \| function` | — | Custom template for rendering value |
| `maxLength` | `number` | `-1` | Max characters (`-1` = unlimited) |
| `showCharCount` | `boolean` | `false` | Display character count |
| `saveInterval` | `number` | `10000` | Auto-save idle delay in ms |
| `autoSaveOnIdle` | `boolean` | `false` | Enable auto-save on idle |
| `enableHtmlEncode` | `boolean` | `false` | Store/retrieve HTML as encoded string |
| `enableXhtml` | `boolean` | `false` | XHTML validation mode |
| `enableHtmlSanitizer` | `boolean` | `true` | XSS sanitization (disable only if you trust input) |
| `saveUrl` | `string` | `''` | Server URL to POST editor content |

```tsx
<RichTextEditorComponent
  value="<p>Hello</p>"
  maxLength={1000}
  showCharCount={true}
  saveInterval={3000}
  autoSaveOnIdle={true}
>
  <Inject services={[Toolbar, HtmlEditor, Count]} />
</RichTextEditorComponent>
```

---

## Media Insert Properties

### `insertImageSettings: ImageSettingsModel`

| Property | Default | Description |
|---|---|---|
| `allowedTypes` | `['.jpeg','.jpg','.png']` | Permitted image formats |
| `display` | `'inline'` | `'inline'` or `'block'` |
| `saveFormat` | `SaveFormat` | `SaveFormat.Blob` or `SaveFormat.Base64` (enum) |
| `saveUrl` | — | Upload endpoint URL |
| `removeUrl` | — | Delete endpoint URL |
| `path` | — | Base path for uploaded images |
| `resize` | `boolean` | Allow image resize |
| `minWidth` | `number \| string` | Minimum image width |
| `maxWidth` | `number \| string` | Maximum image width |
| `minHeight` | `number \| string` | Minimum image height |
| `maxHeight` | `number \| string` | Maximum image height |

```tsx
import { SaveFormat } from '@syncfusion/ej2-react-richtexteditor';

const insertImageSettings: ImageSettingsModel = {
  saveUrl: 'url',
  path: 'url',
  allowedTypes: ['.jpeg', '.jpg', '.png', '.gif', '.webp'],
  saveFormat: SaveFormat.Blob,  // Use enum
  resize: true,
  minWidth: 20,
  maxWidth: 1000
};
```

### `insertVideoSettings: VideoSettingsModel`

Similar to image settings with additional `layoutOption` (`'Inline'` or `'Break'`).

### `insertAudioSettings: AudioSettingsModel`

Similar to video settings. Default `maxFileSize`: 30 MB.

### `fileManagerSettings: FileManagerSettingsModel`
Configures a server-side file browser for image management. Key property: `enable: true` + `ajaxSettings` with API endpoints.

---

## Font, Color & Format Properties

### `fontFamily: FontFamilyModel`
```tsx
const fontFamily: FontFamilyModel = {
  default: 'Segoe UI',
  width: '65px',
  items: [
    { text: 'Segoe UI', value: 'Segoe UI' },
    { text: 'Arial', value: 'Arial' },
    { text: 'Courier New', value: 'Courier New, monospace' },
    { text: 'Georgia', value: 'Georgia, serif' }
  ]
};
```

### `fontSize: FontSizeModel`
```tsx
const fontSize: FontSizeModel = {
  default: '10pt',
  width: '35px',
  items: [
    { text: '8', value: '8pt' },
    { text: '10', value: '10pt' },
    { text: '12', value: '12pt' },
    { text: '14', value: '14pt' },
    { text: '18', value: '18pt' }
  ]
};
```

### `fontColor: FontColorModel`
Controls the font color palette. Key sub-properties: `columns`, `modeSwitcher`, `showRecentColors`, `colorCode`.

### `backgroundColor: BackgroundColorModel`
Controls the text highlight color palette. Same structure as `fontColor`.

### `format: FormatModel`
Defines paragraph format options (Paragraph, Heading 1–6, etc.).

### `lineHeight: LineHeightModel`
Defines line-height options available in the toolbar dropdown.

### `numberFormatList: NumberFormatListModel`
Defines ordered list style options (decimal, upper-roman, etc.).

### `bulletFormatList: BulletFormatListModel`
Defines unordered list style options (disc, circle, square).

### `formatPainterSettings: FormatPainterSettingsModel`
Controls which formats the Format Painter can copy/deny.

```tsx
const formatPainterSettings: FormatPainterSettingsModel = {
  allowedFormats: 'b; em; strong; span; p; div; h1; h2; h3;',
  deniedFormats: null
};
```

### `codeBlockSettings: CodeBlockSettingsModel`
Configures languages available in the Code Block toolbar dropdown.

```tsx
const codeBlockSettings: CodeBlockSettingsModel = {
  defaultLanguage: 'javascript',
  languages: [
    { language: 'javascript', label: 'JavaScript' },
    { language: 'typescript', label: 'TypeScript' },
    { language: 'python', label: 'Python' }
  ]
};
```

## Paste & Clipboard Properties

### `pasteCleanupSettings: PasteCleanupSettingsModel`

| Property | Default | Description |
|---|---|---|
| `prompt` | `false` | Show dialog asking how to paste |
| `plainText` | `false` | Strip all formatting on paste |
| `keepFormat` | `true` | Keep source formatting |
| `deniedTags` | `[]` | HTML tags to strip (array of tag names) |
| `deniedAttrs` | `[]` | Attributes to strip (array of attribute names) |
| `allowedStyleProps` | `[]` | CSS properties to preserve (array of CSS property names) |

**Security Best Practices:**
Always use `deniedTags` and `deniedAttrs` to prevent XSS attacks. Common dangerous elements to block:

```tsx
const pasteCleanupSettings: PasteCleanupSettingsModel = {
  prompt: true,
  keepFormat: true,
  // Security: Block dangerous tags
  deniedTags: ['script', 'iframe', 'embed', 'object', 'applet'],
  // Security: Strip potentially dangerous attributes
  deniedAttrs: ['onerror', 'onload', 'onclick', 'onmouseover', 'style', 'class', 'id'],
  // Allow only safe CSS properties
  allowedStyleProps: ['color', 'font-size', 'font-weight', 'font-style', 'text-align', 'background-color']
};
```

### `enableClipboardCleanup: boolean`
When `true`, copy/cut operations remove unwanted inline styles. Default: `true`.

### `enableAutoUrl: boolean`
When `true`, URLs are accepted as-is without prefixing `https://`. Default: `false`.

---

## Table Properties

### `tableSettings: TableSettingsModel`

| Property | Description |
|---|---|
| `width` | Default table width |
| `minWidth` | Minimum table width |
| `maxWidth` | Maximum table width |
| `resize` | Allow column/row resizing |
| `styles` | Quick style presets |

---

## AI Assistant Properties

### `aiAssistantSettings: AIAssistantSettingsModel`

Configures the AI Assistant functionality in the Rich Text Editor. Allows customization of AI commands, popup appearance, toolbars, prompts, suggestions, and banner templates.

**Type:** `AIAssistantSettingsModel`

**Default:**
```ts
{
  commands: DEFAULT_AI_COMMANDS,
  popupWidth: '600px',
  popupMaxHeight: '400px',
  placeholder: 'Ask AI to rewrite or generate content.',
  headerToolbarSettings: ['AIcommands', 'Close'],
  promptToolbarSettings: ['Edit', 'Copy'],
  responseToolbarSettings: ['Regenerate', 'Copy', '|', 'Insert'],
  prompts: [],
  suggestions: [],
  bannerTemplate: '',
  maxPromptHistory: 20
}
```

| Property | Type | Default | Description |
|---|---|---|---|
| `commands` | `AICommands[]` | Predefined commands | Defines AI command groups with text and prompt. Supports nested items for submenus |
| `popupWidth` | `string \| number` | `'600px'` | Sets the width of the AI Assistant popup |
| `popupMaxHeight` | `string \| number` | `'400px'` | Sets the maximum height of the AI Assistant popup |
| `placeholder` | `string` | `'Ask AI to rewrite or generate content.'` | Placeholder text for the AI input textarea |
| `headerToolbarSettings` | `(AssitantHeaderToolbarItems \| IAIAssistantToolbarItem)[]` | `['AIcommands', 'Close']` | Configures toolbar items in the header section |
| `promptToolbarSettings` | `(AssistantPromptToolbarItems \| IAIAssistantToolbarItem)[]` | `['Edit', 'Copy']` | Configures toolbar items for the prompt input section |
| `responseToolbarSettings` | `(AssistantResponseToolbarItems \| IAIAssistantToolbarItem)[]` | `['Regenerate', 'Copy', '\|', 'Insert']` | Configures toolbar items for the AI response section |
| `prompts` | `PromptModel[]` | `[]` | Defines predefined prompt-response pairs for preloading conversations |
| `suggestions` | `string[]` | `[]` | Provides suggestion prompts to guide users |
| `bannerTemplate` | `string \| Function` | `''` | Template for rendering the AI Assistant banner |
| `maxPromptHistory` | `number` | `20` | Maximum number of prompts stored in history |

**Toolbar Item Types:**

- **AssitantHeaderToolbarItems**: `'Close' | 'AIcommands' | 'Clear'`
- **AssistantPromptToolbarItems**: `'Edit' | 'Copy'`
- **AssistantResponseToolbarItems**: `'Regenerate' | 'Copy' | 'Insert' | '|'`

---

#### Custom AI Commands

Use the `commands` property to define custom AI command groups with nested items:

```tsx
const aiAssistantSettings: AIAssistantSettingsModel = {
  commands: [
    { text: 'Rewrite', prompt: 'Rewrite the content to be more refined.' },
    { text: 'Elaborate', prompt: 'Expand on the following content with more detail and explanation:' },
    {
      text: 'Change Tone',
      items: [
        { text: 'Professional', prompt: 'Rewrite the following content in a professional tone:' },
        { text: 'Casual', prompt: 'Rewrite the following content in a casual, conversational tone:' },
        { text: 'Direct', prompt: 'Rewrite the following content to be more direct and to the point:' }
      ]
    }
  ]
};

<RichTextEditorComponent aiAssistantSettings={aiAssistantSettings}>
  <Inject services={[Toolbar, HtmlEditor, AIAssistant]} />
</RichTextEditorComponent>
```

---

#### PromptModel Structure

For preloading conversations with prompt-response pairs:

```ts
interface PromptModel {
  /**
   * Specifies the prompt text.
   * Represents the text used for prompting user input.
   */
  prompt?: string;

  /**
   * Specifies the response associated with the prompt.
   * Represents the text that provides the response to the prompt.
   */
  response?: string;

  /**
   * Indicates if the response is considered helpful.
   * Represents the state of whether the generated response is useful or not.
   */
  isResponseHelpful?: boolean | null;
}
```

**⚠️ Important:** 
- **All properties are optional** in the TypeScript interface
- Use `prompt` property for the prompt text (NOT `text`)
- Use `response` property for preloaded AI responses
- `isResponseHelpful` tracks user feedback on AI responses

---

#### Preloading Prompts and Suggestions

```tsx
const aiAssistantSettings: AIAssistantSettingsModel = {
  // Preloaded prompt-response pairs (conversation history)
  prompts: [
    {
      prompt: 'What is Essential Studio?',
      response: 'Essential Studio is a software toolkit by Syncfusion that offers a variety of UI controls, frameworks, and libraries for developing applications on web, desktop, and mobile platforms.'
    },
    {
      prompt: 'Summarize the key features',
      response: 'Key features include comprehensive UI controls, cross-platform support, excellent performance, and extensive documentation.'
    }
  ],
  
  // Suggestion prompts (quick access buttons)
  suggestions: [
    'What are the popular components of Essential Studio?',
    'Which web frameworks are supported by Essential Studio?',
    'Explain the licensing model'
  ],
  
  popupWidth: '700px',
  popupMaxHeight: '500px',
  maxPromptHistory: 15
};

<RichTextEditorComponent aiAssistantSettings={aiAssistantSettings}>
  <Inject services={[Toolbar, HtmlEditor, AIAssistant]} />
</RichTextEditorComponent>
```

---

#### Complete Configuration Example

```tsx
import { RichTextEditorComponent, Inject, Toolbar, HtmlEditor, AIAssistant } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  const toolbarSettings: ToolbarSettingsModel = {
    items: ['AICommands', 'AIQuery', '|', 'Bold', 'Italic', 'Underline']
  };

  const aiAssistantSettings: AIAssistantSettingsModel = {
    // Popup dimensions
    popupWidth: '650px',
    popupMaxHeight: '450px',
    placeholder: 'Ask AI to help with your content...',
    
    // Custom AI commands with nested menus
    commands: [
      { text: 'Rewrite', prompt: 'Rewrite the content to be more refined.' },
      { text: 'Elaborate', prompt: 'Expand on the following content:' },
      {
        text: 'Change Tone',
        items: [
          { text: 'Professional', prompt: 'Make this professional:' },
          { text: 'Casual', prompt: 'Make this casual:' }
        ]
      }
    ],
    
    // Preloaded conversations
    prompts: [
      {
        prompt: 'Summarize this document',
        response: 'This document provides an overview of...'
      }
    ],
    
    // Quick suggestions
    suggestions: ['Summarize', 'Fix grammar', 'Make shorter'],
    
    // Toolbar customization
    headerToolbarSettings: ['AIcommands', 'Clear', 'Close'],
    promptToolbarSettings: ['Edit', 'Copy'],
    responseToolbarSettings: ['Regenerate', 'Copy', '|', 'Insert'],
    
    // History management
    maxPromptHistory: 25
  };

  return (
    <RichTextEditorComponent
      toolbarSettings={toolbarSettings}
      aiAssistantSettings={aiAssistantSettings}
    >
      <Inject services={[Toolbar, HtmlEditor, AIAssistant]} />
    </RichTextEditorComponent>
  );
}
```

---

#### Handling AI Responses

See [references/ai-assistant.md](./ai-assistant.md) for complete documentation on:
- Handling streaming and non-streaming AI responses
- Using the `aiAssistantPromptRequest` event
- Public methods: `executeAIPrompt`, `addAIPromptResponse`, `getAIPromptHistory`, `clearAIPromptHistory`
- Showing/hiding the AI Assistant popup programmatically

---

## Slash Menu Properties

### `slashMenuSettings: SlashMenuSettingsModel`

Configures the slash menu settings for the Rich Text Editor. This feature enables a quick-access popup menu triggered by typing `/`, allowing users to insert elements like headings, lists, media, and custom commands.

**Type:** `SlashMenuSettingsModel`

**Default:**
```ts
{
  enable: false,
  items: [
    'Paragraph',
    'Heading 1',
    'Heading 2',
    'Heading 3',
    'Heading 4',
    'OrderedList',
    'UnorderedList',
    'CodeBlock',
    'Blockquote'
  ],
  popupWidth: '300px',
  popupHeight: '320px'
}
```

| Property | Type | Default | Description |
|---|---|---|---|
| `enable` | `boolean` | `false` | Specifies whether to enable or disable the slash menu in the editor |
| `items` | `(SlashMenuItems \| ISlashMenuItem)[]` | Built-in items | Defines the list of items displayed in the slash menu |
| `popupWidth` | `string \| number` | `'300px'` | Specifies the width of the slash menu popup |
| `popupHeight` | `string \| number` | `'320px'` | Specifies the height of the slash menu popup |

**Predefined SlashMenuItems:**
```ts
'Heading 1' | 'Heading 2' | 'Heading 3' | 'Heading 4' |
'Paragraph' | 'Blockquote' | 'OrderedList' | 'UnorderedList' |
'Table' | 'Image' | 'Audio' | 'Video' |
'CodeBlock' | 'Emojipicker' | 'Link'
```

**⚠️ Common Mistakes:**
- ❌ Use `'Emojipicker'` NOT `'Emojis'` or `'EmojiPicker'`
- ✅ Item names are case-sensitive and must match exactly

**Custom Item Structure (ISlashMenuItem):**
- `text`: Display text of the menu item
- `command`: Command to execute when selected
- `iconCss`: Icon CSS class for the menu item
- `description` (optional): Additional information about the item
- `type`: Category/group of the menu item

**Example:**
```tsx
const slashMenuSettings: SlashMenuSettingsModel = {
  enable: true,
  items: [
    'Paragraph',
    'Heading 1',
    'Heading 2',
    'OrderedList',
    'UnorderedList',
    'CodeBlock',
    'Emojipicker',  // Correct: 'Emojipicker' not 'Emojis'
    'Image',
    'Table',
    'Link'
  ],
  popupWidth: '400px',
  popupHeight: '350px'
};

<RichTextEditorComponent slashMenuSettings={slashMenuSettings}>
  <Inject services={[Toolbar, HtmlEditor, SlashMenu]} />
</RichTextEditorComponent>
```

---

## Import / Export Properties

### `importWord: ImportWordModel`
```tsx
const importWord: ImportWordModel = {
  serviceUrl: 'url'
};
```

### `exportWord: ExportWordModel`
```tsx
const exportWord: ExportWordModel = {
  serviceUrl: 'url',
  fileName: 'Document.docx',
  stylesheet: null
};
```

### `exportPdf: ExportPdfModel`
```tsx
const exportPdf: ExportPdfModel = {
  serviceUrl: 'url',
  fileName: 'Document.pdf',
  stylesheet: null
};
```

---

## Miscellaneous Properties

| Property | Type | Default | Description |
|---|---|---|---|
| `undoRedoSteps` | `number` | `30` | Number of undo/redo steps stored |
| `undoRedoTimer` | `number` | `300` | Interval (ms) after which undo history clears |
| `enableMarkdownAutoFormat` | `boolean` | `true` | Auto-convert Markdown syntax while typing |
| `slashMenuSettings` | `SlashMenuSettingsModel` | — | Configure slash menu items |
| `emojiPickerSettings` | `EmojiSettingsModel` | — | Configure emoji picker categories |
| `keyConfig` | `{[key: string]: string}` | `null` | Override default keyboard shortcuts |
| `formatter` | `IFormatter` | `null` | Custom formatter for key code actions |
