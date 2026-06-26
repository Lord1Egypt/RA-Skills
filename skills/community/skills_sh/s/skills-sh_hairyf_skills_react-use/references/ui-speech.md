---
name: ui-speech
description: Synthesize speech from text string with useSpeech hook
---

# useSpeech

React UI hook that synthesizes human voice that speaks a given string.

## Usage

```jsx
import {useSpeech} from 'react-use';

const voices = window.speechSynthesis.getVoices();

const Demo = () => {
  const state = useSpeech('Hello world!', { rate: 0.8, pitch: 0.5, voice: voices[0] });

  return (
    <pre>
      {JSON.stringify(state, null, 2)}
    </pre>  
  );
};
```

## Reference

```ts
const state = useSpeech(text: string, options?: SpeechOptions);
```

Options:
- `rate`: `number` - speech rate (0.1 to 10)
- `pitch`: `number` - speech pitch (0 to 2)
- `volume`: `number` - speech volume (0 to 1)
- `voice`: `SpeechSynthesisVoice` - voice to use

Returns state object with speech synthesis status.

## Key Points

- Uses Web Speech API
- Supports voice selection and speech parameters
- Useful for accessibility and text-to-speech features

<!--
Source references:
- https://github.com/streamich/react-use/blob/master/docs/useSpeech.md
-->
