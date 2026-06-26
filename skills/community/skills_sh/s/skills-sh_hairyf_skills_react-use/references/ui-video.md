---
name: ui-video
description: Play video, track state, and expose controls with useVideo hook
---

# useVideo

Creates `<video>` element, tracks its state and exposes playback controls.

## Usage

```jsx
import {useVideo} from 'react-use';

const Demo = () => {
  const [video, state, controls, ref] = useVideo(
    <video src="http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4" autoPlay />
  );

  return (
    <div>
      {video}
      <pre>{JSON.stringify(state, null, 2)}</pre>
      <button onClick={controls.pause}>Pause</button>
      <button onClick={controls.play}>Play</button>
      <br/>
      <button onClick={controls.mute}>Mute</button>
      <button onClick={controls.unmute}>Un-mute</button>
      <br/>
      <button onClick={() => controls.volume(.1)}>Volume: 10%</button>
      <button onClick={() => controls.volume(.5)}>Volume: 50%</button>
      <button onClick={() => controls.volume(1)}>Volume: 100%</button>
      <br/>
      <button onClick={() => controls.seek(state.time - 5)}>-5 sec</button>
      <button onClick={() => controls.seek(state.time + 5)}>+5 sec</button>
    </div>
  );
};
```

## Reference

```jsx
const [video, state, controls, ref] = useVideo(props);
const [video, state, controls, ref] = useVideo(<video {...props}/>);
```

- **`video`**: React's `<video>` element that you have to insert in your render tree
- **`state`**: object tracking video state with properties:
  - `buffered`: array of buffered time ranges
  - `time`: current playback time
  - `duration`: total duration
  - `paused`: whether video is paused
  - `muted`: whether video is muted
  - `volume`: volume level (0-1)
- **`controls`**: object with methods:
  - `play()`: start playback
  - `pause()`: pause playback
  - `mute()`: mute video
  - `unmute()`: unmute video
  - `volume(volume: number)`: set volume (0-1)
  - `seek(time: number)`: seek to specific time
- **`ref`**: React reference to HTML `<video>` element

## Key Points

- Returns React element that must be rendered
- Provides comprehensive state tracking
- Full playback control API
- Similar API to `useAudio`

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useVideo.md
-->
