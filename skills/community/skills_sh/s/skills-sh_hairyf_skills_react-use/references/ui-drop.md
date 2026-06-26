---
name: ui-drop
description: Track file, link and copy-paste drops with useDrop and useDropArea hooks
---

# useDrop and useDropArea

Triggers on file, link drop and copy-paste.

`useDrop` tracks events for the whole page, `useDropArea` tracks drop events for a specific element.

## Usage

`useDrop`:

```jsx
import {useDrop} from 'react-use';

const Demo = () => {
  const state = useDrop({
    onFiles: files => console.log('files', files),
    onUri: uri => console.log('uri', uri),
    onText: text => console.log('text', text),
  });

  return (
    <div>
      Drop something on the page.
    </div>
  );
};
```

`useDropArea`:

```jsx
import {useDropArea} from 'react-use';

const Demo = () => {
  const [bond, state] = useDropArea({
    onFiles: files => console.log('files', files),
    onUri: uri => console.log('uri', uri),
    onText: text => console.log('text', text),
  });

  return (
    <div {...bond}>
      Drop something here.
    </div>
  );
};
```

## Reference

```ts
const state = useDrop({
  onFiles?: (files: File[]) => void,
  onUri?: (uri: string) => void,
  onText?: (text: string) => void,
});

const [bond, state] = useDropArea({
  onFiles?: (files: File[]) => void,
  onUri?: (uri: string) => void,
  onText?: (text: string) => void,
});
```

- **`onFiles`**: callback when files are dropped
- **`onUri`**: callback when URI/link is dropped
- **`onText`**: callback when text is pasted or dropped
- **`bond`**: object with event handlers to spread on element (for `useDropArea`)

## Key Points

- `useDrop` works for entire page
- `useDropArea` works for specific element (use `bond` props)
- Handles files, URIs, and text
- Useful for drag-and-drop file uploads

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useDrop.md
-->
