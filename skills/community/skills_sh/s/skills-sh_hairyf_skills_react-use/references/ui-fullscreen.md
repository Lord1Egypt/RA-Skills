---
name: ui-fullscreen
description: Display element or video full-screen with useFullscreen hook
---

# useFullscreen

Display an element full-screen, optional fallback for fullscreen video on iOS.

## Usage

```jsx
import {useFullscreen, useToggle} from 'react-use';

const Demo = () => {
  const ref = useRef(null)
  const [show, toggle] = useToggle(false);
  const isFullscreen = useFullscreen(ref, show, {onClose: () => toggle(false)});

  return (
    <div ref={ref} style={{backgroundColor: 'white'}}>
      <div>{isFullscreen ? 'Fullscreen' : 'Not fullscreen'}</div>
      <button onClick={() => toggle()}>Toggle</button>
      <video src="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4" autoPlay />
    </div>
  );
};
```

## Reference

```ts
useFullscreen(ref, show, {onClose})
```

- **`ref`**: `RefObject<HTMLElement>` - reference to element to make fullscreen
- **`show`**: `boolean` - whether to show fullscreen
- **`onClose`**: `() => void` - optional callback when fullscreen is closed
- Returns: `boolean` - whether element is currently fullscreen

## Key Points

- Controls fullscreen state of an element
- Supports iOS video fullscreen fallback
- Provides callback for fullscreen close events
- Useful for media players and immersive experiences

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useFullscreen.md
-->
