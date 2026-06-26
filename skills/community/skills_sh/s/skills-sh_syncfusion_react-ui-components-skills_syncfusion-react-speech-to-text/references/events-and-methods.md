# Events and Methods

## Table of Contents
- [Event Handlers](#event-handlers)
- [Event Arguments](#event-arguments)
- [Error Types](#error-types)
- [Methods](#methods)
  - [startListening()](#startlistening-method)
  - [stopListening()](#stoplistening-method)
  - [destroy()](#destroy-method)
- [Programmatic Control](#programmatic-control)
- [Event Workflows](#event-workflows)
- [Error Handling](#error-handling)

## Event Handlers

The SpeechToText component provides five main events for handling different stages of speech recognition.

### Available Events

| Event | Fires | Description |
|-------|-------|-------------|
| `created` | After component initialization | Component is ready to use |
| `onStart` | When listening begins | Speech recognition started |
| `onStop` | When listening ends | Speech recognition stopped |
| `onError` | When an error occurs | Error during recognition |
| `transcriptChanged` | During recognition | Transcript text changes |

### Basic Event Handling

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';

function EventHandlingDemo() {
  const handleCreated = () => {
    console.log('✓ Component initialized');
  };

  const handleStart = (args: any) => {
    console.log('🎤 Started listening');
  };

  const handleStop = (args: any) => {
    console.log('⏹️ Stopped listening');
  };

  const handleError = (args: any) => {
    console.error('❌ Error:', args.error);
  };

  const handleTranscriptChanged = (args: any) => {
    console.log('📝 Transcript:', args.transcript);
  };

  return (
    <SpeechToTextComponent
      created={handleCreated}
      onStart={handleStart}
      onStop={handleStop}
      onError={handleError}
      transcriptChanged={handleTranscriptChanged}
    />
  );
}

export default EventHandlingDemo;
```

## Event Arguments

Each event provides specific data through its arguments object.

### TranscriptChangedEventArgs

Contains transcript information during speech recognition:

| Property | Type | Description |
|----------|------|-------------|
| `transcript` | `string` | The transcribed text captured from the speech input. |
| `isInterimResult` | `boolean` | `true` if the result is interim (still processing); `false` if it is the final result. Determined by the `allowInterimResults` property. |
| `event` | `Event` | The native browser event associated with the transcript update. |
| `name` | `string` | Name of the event (`'transcriptChanged'`). |

Usage:

```tsx
import { SpeechToTextComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';

function TranscriptEventDemo() {
  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    if (args.isInterimResult) {
      console.log('[Interim] transcript:', args.transcript);
    } else {
      console.log('[Final] transcript:', args.transcript);
    }
  };

  return (
    <SpeechToTextComponent 
      transcriptChanged={handleTranscriptChanged}
    />
  );
}
```

### StartListeningEventArgs

Contains information when listening starts:

| Property | Type | Description |
|----------|------|-------------|
| `cancel` | `boolean` | Set to `true` to prevent listening from starting. Useful for conditional validation before recognition begins. |
| `event` | `Event` | The native browser event associated with the start listening action. |
| `isInteracted` | `boolean` | `true` if triggered by user interaction (button click); `false` if triggered programmatically via `startListening()`. |
| `listeningState` | `SpeechToTextState` | The current state of the component when listening starts. |
| `name` | `string` | Name of the event (`'onStart'`). |

Usage:

```tsx
import { SpeechToTextComponent, StartListeningEventArgs, SpeechToTextState } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function StartEventDemo() {
  const [isListening, setIsListening] = useState(false);

  const handleStart = (args: StartListeningEventArgs) => {
    console.log('Triggered by user?', args.isInteracted);
    console.log('Current state:', args.listeningState); // SpeechToTextState.Listening
    setIsListening(true);
  };

  return (
    <div>
      <SpeechToTextComponent onStart={handleStart} />
      {isListening && <p>🎤 Currently listening...</p>}
    </div>
  );
}
```

### Cancelling Listening on Start

Use `cancel` to conditionally prevent listening from starting:

```tsx
import { SpeechToTextComponent, StartListeningEventArgs } from '@syncfusion/ej2-react-inputs';

function ConditionalListeningDemo() {
  const [isFormValid, setIsFormValid] = useState(true);

  const handleStart = (args: StartListeningEventArgs) => {
    if (!isFormValid) {
      args.cancel = true; // Prevent listening from starting
      console.log('Listening cancelled: form is not valid.');
    }
  };

  return (
    <div>
      <label>
        <input type="checkbox" checked={isFormValid} onChange={e => setIsFormValid(e.target.checked)} />
        Form is valid
      </label>
      <SpeechToTextComponent onStart={handleStart} />
    </div>
  );
}
```

### StopListeningEventArgs

Contains information when listening stops:

| Property | Type | Description |
|----------|------|-------------|
| `event` | `Event` | The native browser event associated with the stop listening action. |
| `isInteracted` | `boolean` | `true` if triggered by user interaction (button click); `false` if triggered programmatically via `stopListening()`. |
| `listeningState` | `SpeechToTextState` | The current state of the component when listening stops. |
| `name` | `string` | Name of the event (`'onStop'`). |

Usage:

```tsx
import { SpeechToTextComponent, StopListeningEventArgs, SpeechToTextState } from '@syncfusion/ej2-react-inputs';

function StopEventDemo() {
  const handleStop = (args: StopListeningEventArgs) => {
    console.log('Listening stopped');
    console.log('Triggered by user?', args.isInteracted);
    console.log('Current state:', args.listeningState); // SpeechToTextState.Stopped
  };

  return (
    <SpeechToTextComponent onStop={handleStop} />
  );
}
```

### ErrorEventArgs

Contains error information:

| Property | Type | Description |
|----------|------|-------------|
| `error` | `string` | Error code describing the type of error (e.g., `'audio-capture'`, `'not-allowed'`). |
| `errorMessage` | `string` | A human-readable message providing further details about the error for user-facing display or logging. |
| `event` | `Event` | The native browser event data provided when the error is triggered. |
| `name` | `string` | Name of the event (`'onError'`). |

## Error Types

The component can report various error types through the `onError` event.

### Common Error Types

| Error | Meaning | Solution |
|-------|---------|----------|
| `no-speech` | No speech detected | Speak louder/clearer |
| `audio-capture` | Microphone unavailable | Check microphone connection |
| `network` | Network error | Check internet connection |
| `not-allowed` | Microphone permission denied | Allow microphone access |
| `service-not-allowed` | Service blocked | Check browser settings |
| `bad-grammar` | Grammar error | N/A (browser API) |
| `aborted` | Recognition aborted | User or system interrupted |

### Error Handling Pattern

```tsx
import { SpeechToTextComponent, ErrorEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function ErrorHandlingDemo() {
  const [error, setError] = useState('');

  const handleError = (args: ErrorEventArgs) => {
    const errorMessages: { [key: string]: string } = {
      'no-speech': '🔇 No speech detected. Please try again.',
      'audio-capture': '🎙️ Microphone not found. Check your device.',
      'network': '🌐 Network error. Check your connection.',
      'not-allowed': '🔒 Microphone permission denied. Allow access in settings.',
      'service-not-allowed': '⛔ Service not allowed in this context.',
      'aborted': '⏹️ Speech recognition was interrupted.'
    };

    // args.errorMessage provides a human-readable description from the component
    const message = errorMessages[args.error] || args.errorMessage || `Error: ${args.error}`;
    setError(message);

    // Auto-clear error after 5 seconds
    setTimeout(() => setError(''), 5000);
  };

  return (
    <div>
      <SpeechToTextComponent onError={handleError} />
      {error && (
        <div style={{
          padding: '10px',
          marginTop: '10px',
          backgroundColor: '#ffebee',
          borderLeft: '4px solid #f44336',
          color: '#c62828'
        }}>
          {error}
        </div>
      )}
    </div>
  );
}

export default ErrorHandlingDemo;
```

## Methods

The component provides two main methods for programmatic control.

### startListening() Method

Programmatically start speech recognition without user clicking the button.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function ProgrammaticStartDemo() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  const startRecording = () => {
    speechRef.current?.startListening();
  };

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
      <button onClick={startRecording} style={{ marginTop: '10px' }}>
        Start Recording
      </button>
    </div>
  );
}

export default ProgrammaticStartDemo;
```

### stopListening() Method

Programmatically stop speech recognition.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function ProgrammaticStopDemo() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  const stopRecording = () => {
    speechRef.current?.stopListening();
  };

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
      <button onClick={stopRecording} style={{ marginTop: '10px' }}>
        Stop Recording
      </button>
    </div>
  );
}

export default ProgrammaticStopDemo;
```

### destroy() Method

Destroys the SpeechToText component instance and releases all associated resources. Call this during component unmount in dynamic UIs to prevent memory leaks.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useRef, useEffect } from 'react';

function DestroyDemo() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  useEffect(() => {
    // Cleanup: destroy the component when the parent unmounts
    return () => {
      speechRef.current?.destroy();
    };
  }, []);

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
    </div>
  );
}

export default DestroyDemo;
```

> **Note:** After calling `destroy()`, the component instance is no longer usable. Do not call `startListening()` or `stopListening()` on a destroyed instance.

## Programmatic Control

Full programmatic control over speech recognition:

```tsx
import { SpeechToTextComponent, TextAreaComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useRef, useState } from 'react';

function FullControlDemo() {
  const speechRef = useRef<SpeechToTextComponent>(null);
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleStart = () => {
    setIsListening(true);
  };

  const handleStop = () => {
    setIsListening(false);
  };

  const handleTranscript = (args: TranscriptChangedEventArgs) => {
    setTranscript(args.transcript);
  };

  const toggleListening = () => {
    if (isListening) {
      speechRef.current?.stopListening();
    } else {
      speechRef.current?.startListening();
    }
  };

  const clearTranscript = () => {
    setTranscript('');
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <SpeechToTextComponent
          ref={speechRef}
          onStart={handleStart}
          onStop={handleStop}
          transcriptChanged={handleTranscript}
        />
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button onClick={toggleListening} style={{ padding: '10px 20px' }}>
          {isListening ? '⏹️ Stop' : '🎤 Start'}
        </button>
        <button onClick={clearTranscript} style={{ padding: '10px 20px' }}>
          Clear
        </button>
      </div>

      <TextAreaComponent
        value={transcript}
        rows={5}
        placeholder="Transcript will appear here..."
      />
    </div>
  );
}

export default FullControlDemo;
```

## Event Workflows

### Workflow 1: Simple Recording

```tsx
const handleStart = () => console.log('Recording started');
const handleStop = () => console.log('Recording stopped');
const handleTranscript = (args: any) => console.log('Text:', args.transcript);

return (
  <SpeechToTextComponent
    onStart={handleStart}
    onStop={handleStop}
    transcriptChanged={handleTranscript}
  />
);
```

Sequence:
1. User clicks button → `onStart` fires
2. User speaks → `transcriptChanged` fires repeatedly
3. User stops → `onStop` fires

### Workflow 2: Form Submission with Voice

```tsx
import { useState, useRef } from 'react';

function FormWithVoice() {
  const [formData, setFormData] = useState({ name: '', email: '', message: '' });
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFieldTranscript = (field: string, args: any) => {
    setFormData(prev => ({ ...prev, [field]: args.transcript }));
  };

  const handleSubmit = async () => {
    setIsProcessing(true);
    try {
      // Submit form
      console.log('Submitting:', formData);
      // await submitForm(formData);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <SpeechToTextComponent 
        transcriptChanged={(args) => handleFieldTranscript('name', args)}
      />
      <SpeechToTextComponent 
        transcriptChanged={(args) => handleFieldTranscript('email', args)}
      />
      <SpeechToTextComponent 
        transcriptChanged={(args) => handleFieldTranscript('message', args)}
      />
      <button onClick={handleSubmit} disabled={isProcessing}>
        Submit
      </button>
    </div>
  );
}
```

## Error Handling

### Comprehensive Error Handling

```tsx
import { SpeechToTextComponent, ErrorEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function RobustErrorHandling() {
  const [state, setState] = useState({
    error: '',
    isListening: false,
    retryCount: 0,
    maxRetries: 3
  });

  const handleError = (args: ErrorEventArgs) => {
    setState(prev => ({
      ...prev,
      error: args.errorMessage || args.error, // errorMessage is human-readable; error is the code
      retryCount: prev.retryCount + 1
    }));
  };

  const handleStart = () => {
    setState(prev => ({
      ...prev,
      error: '',
      isListening: true,
      retryCount: 0
    }));
  };

  const handleStop = () => {
    setState(prev => ({ ...prev, isListening: false }));
  };

  const canRetry = state.retryCount < state.maxRetries;

  return (
    <div style={{ padding: '20px' }}>
      <SpeechToTextComponent
        onStart={handleStart}
        onStop={handleStop}
        onError={handleError}
      />

      {state.isListening && (
        <p style={{ color: 'green' }}>🎤 Listening...</p>
      )}

      {state.error && (
        <div style={{
          padding: '10px',
          marginTop: '10px',
          backgroundColor: '#ffebee',
          borderLeft: '4px solid #f44336',
          color: '#c62828'
        }}>
          <p>Error: {state.error}</p>
          <p>Attempt {state.retryCount} of {state.maxRetries}</p>
          {canRetry && <p>Retrying...</p>}
          {!canRetry && <p>Max retries exceeded. Please try again later.</p>}
        </div>
      )}
    </div>
  );
}

export default RobustErrorHandling;
```

## Troubleshooting

### Method not found error
- Ensure ref is properly created with `useRef<SpeechToTextComponent>(null)`
- Check that component is rendered before calling methods

### Events not firing
- Verify event handlers are properly bound
- Check browser console for errors

### Microphone permission issues
- Handle `not-allowed` error gracefully
- Provide clear instructions to user

