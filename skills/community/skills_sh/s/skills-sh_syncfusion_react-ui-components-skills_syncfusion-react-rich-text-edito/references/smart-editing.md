# Smart Editing Features in Syncfusion React Rich Text Editor

## Table of Contents
- [Emoji Picker](#emoji-picker)
- [Slash Menu](#slash-menu)
- [Mentions](#mentions)
- [Mail Merge](#mail-merge)

## Emoji Picker

Inject `EmojiPicker` and add `'EmojiPicker'` to toolbar items. Opens a categorized emoji panel with a search box.

```tsx
import {
  HtmlEditor, Inject, Link, Image,
  QuickToolbar, RichTextEditorComponent, Toolbar, EmojiPicker
} from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'EmojiPicker', '|', 'Undo', 'Redo']
};

function App() {
  return (
    <RichTextEditorComponent toolbarSettings={toolbarSettings}>
      <Inject services={[Toolbar, HtmlEditor, EmojiPicker]} />
    </RichTextEditorComponent>
  );
}
```

### Customizing Emoji Sets

Override the default emoji categories and icons via `emojiPickerSettings.iconsSet`:

```tsx
const emojiPickerSettings: EmojiSettingsModel = {
  iconsSet: [
    {
      name: 'Smilies & People',
      code: '1F600',
      iconCss: 'e-emoji',
      icons: [
        { code: '1F600', desc: 'Grinning face' },
        { code: '1F603', desc: 'Grinning face with big eyes' },
        { code: '1F604', desc: 'Grinning face with smiling eyes' },
        { code: '1F602', desc: 'Face with tears of joy' },
      ]
    },
    {
      name: 'Animals & Nature',
      code: '1F435',
      iconCss: 'e-animals',
      icons: [
        { code: '1F436', desc: 'Dog face' },
        { code: '1F431', desc: 'Cat face' },
        { code: '1F430', desc: 'Rabbit face' },
      ]
    }
  ]
};

<RichTextEditorComponent
  toolbarSettings={toolbarSettings}
  emojiPickerSettings={emojiPickerSettings}
>
  <Inject services={[Toolbar, HtmlEditor, EmojiPicker]} />
</RichTextEditorComponent>
```

## Slash Menu

Inject `SlashMenu` to enable a command menu triggered by typing `/` anywhere in the editor content. It shows a list of format/insertion actions the user can apply.

```tsx
import { SlashMenu } from '@syncfusion/ej2-react-richtexteditor';

function App() {
  return (
    <RichTextEditorComponent>
      <Inject services={[Toolbar, HtmlEditor, SlashMenu]} />
    </RichTextEditorComponent>
  );
}
```

You can also add `'SlashMenu'` to the toolbar items to trigger it via a button.

### Customizing Slash Menu Items

Use `slashMenuSettings.items` to define which actions appear:

```tsx
const slashMenuSettings: SlashMenuSettingsModel = {
  enable: true,
  items: [
    'Paragraph', 'Heading 1', 'Heading 2', 'Heading 3',
    'Heading 4', 'OrderedList', 'UnorderedList',
    'CodeBlock', 'Blockquote', 'Link', 'Image', 'Video', 'Audio',
    'Table', 'Emojis'
  ]
};

<RichTextEditorComponent slashMenuSettings={slashMenuSettings}>
  <Inject services={[Toolbar, HtmlEditor, SlashMenu, Image, Link, Table, EmojiPicker]} />
</RichTextEditorComponent>
```

## Mentions

Inject the `Mention` module from `@syncfusion/ej2-react-dropdowns` to enable `@mention` functionality inside the editor. The mention component works alongside the RTE.

```bash
npm install @syncfusion/ej2-react-dropdowns
```

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { RichTextEditorComponent, Inject, Toolbar, HtmlEditor } from '@syncfusion/ej2-react-richtexteditor';

const mentionData = [
  { name: 'Selma Rose', value: 'selma' },
  { name: 'Russo Kay', value: 'russo' },
  { name: 'Camden Kate', value: 'camden' },
];

function App() {
  return (
    <div>
      <RichTextEditorComponent id="mention-rte" placeholder="Type @ to mention...">
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>
      <MentionComponent
        target="#mention-rte_rte-edit-view"
        dataSource={mentionData}
        fields={{ text: 'name', value: 'value' }}
        popupWidth="250px"
        itemTemplate='<span>${name}</span>'
        displayTemplate='<span class="mention">@${name}</span>'
      />
    </div>
  );
}
```

> Target the RTE's editable area via `#{rteId}_rte-edit-view`.

## Mail Merge

Mail merge lets you insert dynamic field placeholders (like `{{FirstName}}`) into the editor content and later replace them with actual data values.

```tsx
import { RichTextEditorComponent, Inject, Toolbar, HtmlEditor, QuickToolbar } from '@syncfusion/ej2-react-richtexteditor';

const toolbarSettings: ToolbarSettingsModel = {
  items: ['Bold', 'Italic', '|', 'Undo', 'Redo']
};

// Example: Insert merge fields programmatically
function insertMergeField(rteRef: React.RefObject<RichTextEditorComponent>, field: string) {
  rteRef.current?.executeCommand('insertHTML', `<span class="merge-field">{{${field}}}</span>&nbsp;`);
}

function App() {
  const rteRef = useRef<RichTextEditorComponent>(null);

  return (
    <>
      <button onClick={() => insertMergeField(rteRef, 'FirstName')}>Insert FirstName</button>
      <button onClick={() => insertMergeField(rteRef, 'LastName')}>Insert LastName</button>
      <RichTextEditorComponent ref={rteRef} toolbarSettings={toolbarSettings}>
        <Inject services={[Toolbar, HtmlEditor]} />
      </RichTextEditorComponent>
    </>
  );
}
```

For dedicated mail merge support with a field picker UI, see `docs/smart-editing/mail-merge.md` in the documentation folder.
