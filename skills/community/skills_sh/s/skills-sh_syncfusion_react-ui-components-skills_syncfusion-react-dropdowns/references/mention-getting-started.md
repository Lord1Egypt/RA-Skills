# Getting Started with Syncfusion React Mention

## Installation

Install the Syncfusion React Dropdowns package:

```bash
npm install @syncfusion/ej2-react-dropdowns --save
```

## CSS Theme Imports

Add these imports in your `src/App.css`:

```css
@import "../node_modules/@syncfusion/ej2-base/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-buttons/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-popups/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-list/styles/tailwind3.css";
@import "../node_modules/@syncfusion/ej2-react-dropdowns/styles/tailwind3.css";
```

Then import `App.css` in `src/App.tsx`:

```tsx
import './App.css';
```

## Basic Setup

The `MentionComponent` needs a `target` prop pointing to an editable element (a `contenteditable` div or similar). The component listens for the trigger character in that element and shows a popup.

**Functional component:**

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

function App() {
  const mentionTarget: string = '#mentionElement';

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label>Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent target={mentionTarget} />
    </div>
  );
}

export default App;
```

**Class component:**

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';
import './App.css';

export default class App extends React.Component<{}, {}> {
  private mentionTarget: string = '#mentionElement';

  public render() {
    return (
      <div id="mention_default">
        <table>
          <tr>
            <td>
              <label>Comments</label>
              <div id="mentionElement" placeholder="Type @ and tag user"></div>
            </td>
          </tr>
        </table>
        <MentionComponent target={this.mentionTarget} />
      </div>
    );
  }
}
```

## Binding a Data Source

Pass an array of strings or objects via the `dataSource` prop. For objects, also set `fields` to map the `text` field.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: string[] = ['Selma Rose', 'Garth', 'Robert', 'William', 'Joseph'];

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
      <MentionComponent target={mentionTarget} dataSource={userData} />
    </div>
  );
}

export default App;
```

## Target Element Styling

Style the target editable element so it is visible to users:

```css
#mentionElement {
  min-height: 100px;
  border: 1px solid #d7d7d7;
  border-radius: 4px;
  padding: 8px;
  font-size: 14px;
  width: 600px;
}
```

## Display Mention Character

By default, `showMentionChar` is `false` and the trigger character is not included in the inserted text. Enable it to include the trigger character in the output. Use `mentionChar` to change the trigger character.

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import * as React from 'react';

function App() {
  const mentionTarget: string = '#mentionElement';
  const userData: string[] = ['Selma Rose', 'Garth', 'Robert', 'William', 'Joseph'];
  const mentionCharacter: string = '#';

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type # and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={userData}
        showMentionChar={true}
        mentionChar={mentionCharacter}
      />
    </div>
  );
}

export default App;
```

> **Default:** `mentionChar` is `@` and `showMentionChar` is `false`.

## Running the Application

```bash
npm run dev
```

## Gotchas

- The `target` must point to an **existing DOM element** when the `MentionComponent` mounts. Use a valid CSS selector string (e.g., `'#mentionElement'`) or pass an `HTMLElement` reference.
- The target element should be editable (`contenteditable="true"` or a text input). The component listens for keyboard input in the target.
- Import the `MentionComponent` from `@syncfusion/ej2-react-dropdowns`—not from any other sub-package.
