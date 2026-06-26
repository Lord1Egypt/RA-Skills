# Speech Recognition Features

## Table of Contents
- [Retrieving Transcripts](#retrieving-transcripts)
- [Setting Language](#setting-language)
- [Allowing Interim Results](#allowing-interim-results)
- [Managing Listening State](#managing-listening-state)
- [Real-Time Speech Processing](#real-time-speech-processing)
- [Multi-Language Support](#multi-language-support)

## Retrieving Transcripts

The `transcript` property allows you to access the text generated from spoken input. You can retrieve and display the transcribed text in your application.

### Basic Transcript Retrieval

```tsx
import { SpeechToTextComponent, TextAreaComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function TranscriptDemo() {
  const [transcript, setTranscript] = useState('');

  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    // Update state with the latest transcript
    setTranscript(args.transcript);
  };

  return (
    <div>
      <SpeechToTextComponent 
        transcriptChanged={handleTranscriptChanged}
      />
      <TextAreaComponent
        value={transcript}
        placeholder="Transcribed text appears here..."
        rows={5}
      />
    </div>
  );
}

export default TranscriptDemo;
```

### Accessing Transcript from Component Ref

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function DirectTranscriptAccess() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  const getTranscript = () => {
    const currentTranscript = speechRef.current?.transcript;
    console.log('Current transcript:', currentTranscript);
  };

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
      <button onClick={getTranscript}>Get Transcript</button>
    </div>
  );
}
```

### Pre-filling Transcript

You can initialize the component with existing transcript text:

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function PreFilledTranscript() {
  const initialText = 'Hello, this is a pre-filled transcript.';

  return (
    <div>
      <SpeechToTextComponent 
        transcript={initialText}
      />
    </div>
  );
}
```

## Setting Language

The `lang` property specifies the language for speech recognition. This determines how the speech engine interprets spoken words.

### Supported Languages

Common language codes:
- `en-US` - English (US)
- `en-GB` - English (UK)
- `fr-FR` - French
- `de-DE` - German
- `es-ES` - Spanish
- `it-IT` - Italian
- `ja-JP` - Japanese
- `zh-CN` - Chinese (Simplified)
- `zh-TW` - Chinese (Traditional)
- `pt-BR` - Portuguese (Brazil)
- `ru-RU` - Russian

### Setting a Specific Language

```tsx
import { SpeechToTextComponent, TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function LanguageDemo() {
  const [transcript, setTranscript] = useState('');

  return (
    <div>
      <h3>French Speech Recognition</h3>
      <SpeechToTextComponent 
        lang="fr-FR"
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
      />
      <TextAreaComponent
        value={transcript}
        placeholder="Parlez en français..."
      />
    </div>
  );
}

export default LanguageDemo;
```

### Language Selection Dropdown

```tsx
import { SpeechToTextComponent, TextAreaComponent, DropDownListComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function LanguageSelector() {
  const [language, setLanguage] = useState('en-US');
  const [transcript, setTranscript] = useState('');

  const languages = [
    { text: 'English (US)', value: 'en-US' },
    { text: 'English (UK)', value: 'en-GB' },
    { text: 'French', value: 'fr-FR' },
    { text: 'Spanish', value: 'es-ES' },
    { text: 'German', value: 'de-DE' },
    { text: 'Japanese', value: 'ja-JP' }
  ];

  return (
    <div>
      <div>
        <label>Select Language:</label>
        <DropDownListComponent
          dataSource={languages}
          fields={{ text: 'text', value: 'value' }}
          value={language}
          change={(e: any) => setLanguage(e.value)}
        />
      </div>
      
      <SpeechToTextComponent 
        lang={language}
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
      />
      <TextAreaComponent
        value={transcript}
        placeholder="Your speech will appear here..."
      />
    </div>
  );
}

export default LanguageSelector;
```

## Allowing Interim Results

The `allowInterimResults` property controls whether the component displays results in real-time as the user speaks or waits for the final result.

### What are Interim Results?

- **Interim Results (true):** Text updates continuously while speaking (default)
- **Final Results (false):** Text updates only after speech recognition completes

### Real-Time Results (Default)

```tsx
import { SpeechToTextComponent, TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function RealTimeDemo() {
  const [transcript, setTranscript] = useState('');

  return (
    <div>
      <h3>Real-Time Transcription</h3>
      <p>Text updates as you speak:</p>
      <SpeechToTextComponent 
        allowInterimResults={true}  // Default
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
      />
      <TextAreaComponent
        value={transcript}
        rows={5}
        placeholder="Real-time transcript..."
      />
    </div>
  );
}

export default RealTimeDemo;
```

### Final Results Only

```tsx
import { SpeechToTextComponent, TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function FinalResultsDemo() {
  const [transcript, setTranscript] = useState('');

  return (
    <div>
      <h3>Final Results Only</h3>
      <p>Text updates after you stop speaking:</p>
      <SpeechToTextComponent 
        allowInterimResults={false}
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
      />
      <TextAreaComponent
        value={transcript}
        rows={5}
        placeholder="Final transcript will appear here..."
      />
    </div>
  );
}

export default FinalResultsDemo;
```

## Managing Listening State

The `listeningState` property indicates the current status of the component. It helps you understand whether the component is waiting for input, actively listening, or has stopped. Import the `SpeechToTextState` enum to work with state values in a type-safe way.

### SpeechToTextState Enum

| Enum Value | String | Description |
|------------|--------|-------------|
| `SpeechToTextState.Inactive` | `'Inactive'` | Component is idle, not listening |
| `SpeechToTextState.Listening` | `'Listening'` | Component is actively capturing audio |
| `SpeechToTextState.Stopped` | `'Stopped'` | Speech recognition has ended |

### Reading listeningState via Event Args

The `listeningState` is provided in `StartListeningEventArgs` and `StopListeningEventArgs` so you can read the exact state at the time each event fires:

```tsx
import { SpeechToTextComponent, StartListeningEventArgs, StopListeningEventArgs, SpeechToTextState } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function ListeningStateDemo() {
  const [currentState, setCurrentState] = useState<SpeechToTextState>(SpeechToTextState.Inactive);

  const handleStart = (args: StartListeningEventArgs) => {
    setCurrentState(args.listeningState); // SpeechToTextState.Listening
  };

  const handleStop = (args: StopListeningEventArgs) => {
    setCurrentState(args.listeningState); // SpeechToTextState.Stopped
  };

  const stateLabels: Record<SpeechToTextState, string> = {
    [SpeechToTextState.Inactive]: '⏸️ Inactive',
    [SpeechToTextState.Listening]: '🎤 Listening',
    [SpeechToTextState.Stopped]: '⏹️ Stopped',
  };

  return (
    <div>
      <div style={{
        padding: '10px',
        margin: '10px 0',
        backgroundColor: currentState === SpeechToTextState.Listening ? '#ffeb3b' : '#e8f5e9',
        borderRadius: '4px'
      }}>
        Status: {stateLabels[currentState]}
      </div>

      <SpeechToTextComponent
        onStart={handleStart}
        onStop={handleStop}
      />
    </div>
  );
}

export default ListeningStateDemo;
```

### Reading listeningState from a Ref

You can also read the current `listeningState` directly from the component ref at any time:

```tsx
import { SpeechToTextComponent, SpeechToTextState } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function ReadStateFromRef() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  const checkState = () => {
    const state = speechRef.current?.listeningState;
    if (state === SpeechToTextState.Listening) {
      console.log('Currently listening — stopping now.');
      speechRef.current?.stopListening();
    } else if (state === SpeechToTextState.Inactive) {
      console.log('Idle — starting now.');
      speechRef.current?.startListening();
    }
  };

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
      <button onClick={checkState}>Toggle Listening</button>
    </div>
  );
}

export default ReadStateFromRef;
```

## Real-Time Speech Processing

Process transcribed text in real-time as the user speaks:

```tsx
import { SpeechToTextComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function RealtimeProcessing() {
  const [transcript, setTranscript] = useState('');
  const [wordCount, setWordCount] = useState(0);
  const [letterCount, setLetterCount] = useState(0);

  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    const text = args.transcript;
    setTranscript(text);
    
    // Count words
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    setWordCount(words.length);
    
    // Count letters
    setLetterCount(text.replace(/\s/g, '').length);
  };

  return (
    <div style={{ padding: '20px' }}>
      <SpeechToTextComponent 
        transcriptChanged={handleTranscriptChanged}
      />
      
      <div style={{ marginTop: '20px' }}>
        <p>Transcript: {transcript}</p>
        <p>Words: {wordCount}</p>
        <p>Letters: {letterCount}</p>
      </div>
    </div>
  );
}

export default RealtimeProcessing;
```

## Multi-Language Support

Implement a multi-language voice interface:

```tsx
import { SpeechToTextComponent, TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function MultiLanguageVoiceApp() {
  const [language, setLanguage] = useState('en-US');
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);

  const languages = {
    'en-US': 'English (US)',
    'fr-FR': 'French',
    'es-ES': 'Spanish',
    'de-DE': 'German',
    'ja-JP': 'Japanese'
  };

  const handleStart = () => {
    setIsListening(true);
  };

  const handleStop = () => {
    setIsListening(false);
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h2>Multi-Language Voice Input</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <label>Select Language: </label>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          style={{ padding: '8px', fontSize: '16px' }}
        >
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>{name}</option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <p>{isListening ? '🎤 Listening...' : 'Click to start speaking'}</p>
        <SpeechToTextComponent 
          lang={language}
          onStart={handleStart}
          onStop={handleStop}
          transcriptChanged={(args: any) => setTranscript(args.transcript)}
        />
      </div>

      <div>
        <p>Transcribed Text:</p>
        <TextAreaComponent
          value={transcript}
          readOnly={false}
          rows={5}
          placeholder="Your speech appears here..."
        />
      </div>
    </div>
  );
}

export default MultiLanguageVoiceApp;
```

## Common Patterns

### Pattern: Clear Transcript Button

```tsx
const [transcript, setTranscript] = useState('');

const clearTranscript = () => {
  setTranscript('');
};

return (
  <div>
    <SpeechToTextComponent 
      transcript={transcript}
      transcriptChanged={(args: any) => setTranscript(args.transcript)}
    />
    <button onClick={clearTranscript}>Clear</button>
  </div>
);
```

### Pattern: Copy to Clipboard

```tsx
const copyToClipboard = async () => {
  await navigator.clipboard.writeText(transcript);
  alert('Copied to clipboard!');
};

return (
  <div>
    <SpeechToTextComponent 
      transcriptChanged={(args: any) => setTranscript(args.transcript)}
    />
    <button onClick={copyToClipboard}>Copy Transcript</button>
  </div>
);
```

## Troubleshooting

### No transcript appearing
- Check microphone is working
- Verify `allowInterimResults` setting
- Ensure microphone permissions are granted
- Check browser console for errors

### Wrong language recognized
- Verify `lang` property is set to correct language code
- Test with your microphone and audio
- Try a different accent or speech pace

