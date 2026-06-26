---
name: ui-audio
description: Play audio and expose controls with useAudio hook
---

# useAudio

Creates `<audio>` element, tracks its state and exposes playback controls.

## Usage

```jsx
import {useAudio} from 'react-use';

const Demo = () => {
  const [audio, state, controls, ref] = useAudio({
    src: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
    autoPlay: true,
  });

  return (
    <div>
      {audio}
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
const [audio, state, controls, ref] = useAudio(props);
const [audio, state, controls] = useAudio(<audio {...props}/>);
```

- **`audio`**: React's `<audio>` element that you have to insert in your render tree
- **`state`**: object tracking audio state with properties:
  - `buffered`: array of buffered time ranges
  - `time`: current playback time
  - `duration`: total duration
  - `paused`: whether audio is paused
  - `muted`: whether audio is muted
  - `volume`: volume level (0-1)
  - `playing`: whether audio is playing (affected by network buffering)
- **`controls`**: object with methods:
  - `play()`: start playback
  - `pause()`: pause playback
  - `mute()`: mute audio
  - `unmute()`: unmute audio
  - `volume(volume: number)`: set volume (0-1)
  - `seek(time: number)`: seek to specific time
- **`ref`**: React reference to HTML `<audio>` element

## Key Points

- Returns React element that must be rendered
- Provides comprehensive state tracking
- Full playback control API
- `playing` state accounts for network buffering

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useAudio.md
-->
