# Customization in Syncfusion React Mention

## Table of Contents
- [Show or Hide Mention Character](#show-or-hide-mention-character)
- [Suffix Text After Selection](#suffix-text-after-selection)
- [Popup Height and Width](#popup-height-and-width)
- [Custom Trigger Character](#custom-trigger-character)
- [Leading Space Requirement](#leading-space-requirement)
- [CSS Class Customization](#css-class-customization)
- [Highlight Matched Characters](#highlight-matched-characters)
- [Ignore Accent and Case](#ignore-accent-and-case)
- [Z-Index for Popup](#z-index-for-popup)
- [RTL Support](#rtl-support)

## Show or Hide Mention Character

By default, `showMentionChar` is `false`—the trigger character (`@`) is not included in the inserted text. Set it to `true` to include it:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Name: 'Selma Rose', EmailId: 'selma@gmail.com' },
    { Name: 'Maria', EmailId: 'maria@gmail.com' },
    { Name: 'Russo kay', EmailId: 'russo@gmail.com' },
    { Name: 'Robert', EmailId: 'robert@gmail.com' },
    { Name: 'Garth', EmailId: 'garth@gmail.com' },
  ];
  const fields: Object = { text: 'Name' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      {/* Inserted text will include "@" before the name */}
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
        showMentionChar={true}
      />
    </div>
  );
}

export default App;
```

## Suffix Text After Selection

Use `suffixText` to append a custom string after the selected mention text. Common values:
- `'&nbsp;'` — non-breaking space (keeps cursor after the mention)
- `'\n'` — newline

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Country: 'Australia', Code: 'AU' },
    { Country: 'Bermuda', Code: 'BM' },
    { Country: 'Canada', Code: 'CA' },
    { Country: 'Cameroon', Code: 'CM' },
    { Country: 'Denmark', Code: 'DK' },
  ];
  const fields: Object = { text: 'Country' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag country"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
        showMentionChar={true}
        suffixText="&nbsp;"
      />
    </div>
  );
}

export default App;
```

## Popup Height and Width

Control the popup dimensions with `popupHeight` and `popupWidth`. Both accept strings with CSS units or numbers (treated as pixels).

Defaults: `popupHeight='300px'`, `popupWidth='auto'`.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const sportsData: { [key: string]: Object }[] = [
    { ID: 'game1', Game: 'Badminton' },
    { ID: 'game2', Game: 'Football' },
    { ID: 'game3', Game: 'Tennis' },
    { ID: 'game4', Game: 'Hockey' },
    { ID: 'game5', Game: 'Basketball' },
    { ID: 'game6', Game: 'Cricket' },
  ];
  const fields: Object = { text: 'Game' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag sport"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={sportsData}
        fields={fields}
        popupHeight="200px"
        popupWidth="250px"
      />
    </div>
  );
}

export default App;
```

## Custom Trigger Character

Change the trigger character with `mentionChar`. Default is `@`. Any single character is valid.

```tsx
{/* Trigger with '#' for hashtags */}
<MentionComponent
  target={mentionTarget}
  dataSource={tagsData}
  fields={{ text: 'Tag' }}
  mentionChar="#"
  showMentionChar={true}
/>
```

## Leading Space Requirement

The `requireLeadingSpace` property controls whether a space must precede the trigger character. Default: `true`.

Set to `false` to allow the mention at the start of a line or directly after another character:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: { [key: string]: Object }[] = [
    { Name: 'Selma Rose', EmailId: 'selma@gmail.com' },
    { Name: 'Maria', EmailId: 'maria@gmail.com' },
    { Name: 'Russo kay', EmailId: 'russo@gmail.com' },
  ];
  const fields: Object = { text: 'Name' };

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      {/* Can trigger @mention without a preceding space */}
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        fields={fields}
        requireLeadingSpace={false}
      />
    </div>
  );
}

export default App;
```

## CSS Class Customization

Use `cssClass` to apply one or more custom CSS classes to the Mention component (affects the popup element):

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  cssClass="my-mention-popup"
/>
```

```css
.my-mention-popup .e-list-item {
  padding: 6px 12px;
}
```

## Highlight Matched Characters

Set `highlight={true}` to bold or highlight the typed characters within suggestion list items:

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  highlight={true}
/>
```

## Ignore Accent and Case

- `ignoreAccent={true}` — treats accented characters the same as their base characters (e.g., `é` matches `e`)
- `ignoreCase={true}` — case-insensitive filtering (default: `true`)

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  ignoreAccent={true}
  ignoreCase={true}
/>
```

## Z-Index for Popup

Set `zIndex` to control the popup stacking order. Default: `1000`. Increase this when the popup renders beneath a modal or other overlay.

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  zIndex={9999}
/>
```

## RTL Support

Enable right-to-left layout for the popup with `enableRtl={true}`:

```tsx
<MentionComponent
  target={mentionTarget}
  dataSource={userData}
  fields={fields}
  enableRtl={true}
/>
```
