---
name: syncfusion-react-speech-to-text
description: Implement the Syncfusion React SpeechToText component. Use this skill to convert speech to text, manage microphone input, control listening states, process speech events, customize UI, support accessible voice-enabled forms, and handle globalization and security in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion React SpeechToText Component

## Component Overview

The SpeechToText component enables users to convert spoken words into text using the Web Speech API. This skill helps you implement, customize, and troubleshoot speech recognition in React applications. The main component that captures audio from the user's microphone and converts speech to text in real-time using browser APIs.

## Key Capabilities

- Real-time speech recognition
- Multiple language support
- Customizable button and tooltip
- Event-driven architecture
- Programmatic control via methods
- Accessibility support (ARIA labels, keyboard navigation)
- Localization support
- Error handling and recovery

## Documentation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via npm
- Package installation and setup
- Basic component implementation
- CSS imports and theme selection
- First working example
- TypeScript configuration
- Disabling the component (`disabled` property)

### Speech Recognition Features
📄 **Read:** [references/speech-recognition-features.md](references/speech-recognition-features.md)
- Retrieving transcripts in real-time
- Setting language for recognition
- Managing interim results
- Listening state management with `SpeechToTextState` enum (Inactive, Listening, Stopped)
- Reading `listeningState` from event args and component ref
- Handling speech-to-text conversion
- Real-time vs final results

### Button and Tooltip Customization
📄 **Read:** [references/button-and-tooltip-customization.md](references/button-and-tooltip-customization.md)
- Customizing button content and icons
- Icon positioning and styling
- Controlling tooltip visibility (`showTooltip` property)
- Tooltip configuration and placement (all 12 `TooltipPosition` values)
- CSS class styling (e-primary, e-success, etc.)
- Button appearance modes
- Responsive button design

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event handling (created, onStart, onStop, onError, transcriptChanged)
- Correct event argument interfaces (StartListeningEventArgs, StopListeningEventArgs, ErrorEventArgs, TranscriptChangedEventArgs)
- `cancel` property to prevent listening start
- `isInteracted` to distinguish user vs programmatic triggers
- `errorMessage` for human-readable error details
- `isInterimResult` for interim vs final transcript results
- startListening(), stopListening(), and destroy() methods
- Ref-based component control
- Programmatic listening management

### Globalization and Localization
📄 **Read:** [references/globalization-and-localization.md](references/globalization-and-localization.md)
- Localization with L10n.load()
- Available locale strings and translations
- Language-specific error messages
- RTL support for right-to-left languages
- Accessibility labels and ARIA attributes
- `htmlAttributes` for custom HTML/ARIA attributes on the button element
- Multi-language interface support

### Troubleshooting and Security
📄 **Read:** [references/troubleshooting-and-security.md](references/troubleshooting-and-security.md)
- Common issues and solutions
- Browser compatibility matrix
- Microphone permission handling
- Security considerations and best practices
- Privacy and data transmission
- Performance optimization
- Offline fallback strategies

## Quick Start Example

```tsx
import { SpeechToTextComponent, TextAreaComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function VoiceNoteApp() {
  const [transcript, setTranscript] = useState('');

  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    setTranscript(args.transcript);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Voice Note Recorder</h2>
      
      {/* SpeechToText component with microphone button */}
      <SpeechToTextComponent 
        id="speechToText"
        transcriptChanged={handleTranscriptChanged}
      />
      
      {/* Display transcribed text */}
      <TextAreaComponent
        id="noteArea"
        value={transcript}
        resizeMode="None"
        rows={5}
        cols={50}
        placeholder="Your voice will appear here..."
      />
    </div>
  );
}

export default VoiceNoteApp;
```

## Common Patterns

### Pattern 1: Voice Form Input

```tsx
import { SpeechToTextComponent, TextBoxComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function VoiceForm() {
  const [formData, setFormData] = useState({
    name: '',
    message: ''
  });

  const handleNameTranscript = (args: any) => {
    setFormData(prev => ({ ...prev, name: args.transcript }));
  };

  const handleMessageTranscript = (args: any) => {
    setFormData(prev => ({ ...prev, message: args.transcript }));
  };

  return (
    <div>
      <label>Name (speak):</label>
      <SpeechToTextComponent transcriptChanged={handleNameTranscript} />
      <TextBoxComponent value={formData.name} />
      
      <label>Message (speak):</label>
      <SpeechToTextComponent transcriptChanged={handleMessageTranscript} />
      <TextBoxComponent value={formData.message} />
    </div>
  );
}
```

### Pattern 2: Programmatic Control

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useRef } from 'react';

function VoiceControlApp() {
  const speechRef = useRef<SpeechToTextComponent>(null);

  const startVoiceInput = () => {
    speechRef.current?.startListening();
  };

  const stopVoiceInput = () => {
    speechRef.current?.stopListening();
  };

  return (
    <div>
      <SpeechToTextComponent ref={speechRef} />
      <button onClick={startVoiceInput}>Start Recording</button>
      <button onClick={stopVoiceInput}>Stop Recording</button>
    </div>
  );
}
```

### Pattern 3: Error Handling

```tsx
import { SpeechToTextComponent, ErrorEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function VoiceWithErrorHandling() {
  const [error, setError] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleError = (args: ErrorEventArgs) => {
    // args.errorMessage is the human-readable description; args.error is the error code
    setError(args.errorMessage || `Error: ${args.error}`);
  };

  const handleStart = () => {
    setIsListening(true);
    setError('');
  };

  const handleStop = () => {
    setIsListening(false);
  };

  return (
    <div>
      <SpeechToTextComponent 
        onError={handleError}
        onStart={handleStart}
        onStop={handleStop}
      />
      {isListening && <p>🎤 Listening...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}
```

## Key Props

| Prop | Type | Description |
|------|------|-------------|
| `lang` | string | Language for speech recognition (e.g., 'en-US', 'fr-FR') |
| `transcript` | string | Current transcribed text |
| `allowInterimResults` | boolean | Show real-time results (default: true) |
| `listeningState` | SpeechToTextState | Current listening state (Inactive, Listening, Stopped) |
| `buttonSettings` | ButtonSettingsModel | Customize button appearance and content |
| `tooltipSettings` | TooltipSettingsModel | Configure tooltip display |
| `showTooltip` | boolean | Whether to display the tooltip on hover (default: true) |
| `cssClass` | string | Apply CSS classes for styling |
| `disabled` | boolean | Disable all component interaction (default: false) |
| `htmlAttributes` | { [key: string]: string } | Additional HTML attributes (ARIA, data-*, etc.) for the root button element |
| `locale` | string | Localization language code |
| `enableRtl` | boolean | Enable right-to-left layout |
| `enablePersistence` | boolean | Persist component state between page reloads via localStorage |

## Event Handlers

| Event | Args | Description |
|-------|------|-------------|
| `created` | - | Fired when component is initialized |
| `onStart` | StartListeningEventArgs | Fired when speech recognition begins. Args: `cancel`, `event`, `isInteracted`, `listeningState`, `name` |
| `onStop` | StopListeningEventArgs | Fired when speech recognition ends. Args: `event`, `isInteracted`, `listeningState`, `name` |
| `onError` | ErrorEventArgs | Fired when an error occurs. Args: `error`, `errorMessage`, `event`, `name` |
| `transcriptChanged` | TranscriptChangedEventArgs | Fired when transcription updates. Args: `transcript`, `isInterimResult`, `event`, `name` |

## Methods

| Method | Description |
|--------|-------------|
| `startListening()` | Begin speech recognition programmatically |
| `stopListening()` | Stop speech recognition programmatically |
| `destroy()` | Destroy the component instance and release all resources |

## Troubleshooting

### Microphone permission denied
**Solution:** Check browser permissions settings and allow microphone access in security settings

### Speech not recognized
**Solution:** Check microphone volume, speak clearly, verify correct language setting

### Component not rendering
**Solution:** Ensure CSS imports are included and license key is registered

### Browser not supported
**Solution:** Check if browser supports Web Speech API (Chrome, Edge, Safari support it)

## Related Components

- **TextArea:** For displaying transcribed text
- **TextBox:** For input fields with voice capabilities
- **Button:** For custom voice control buttons
- **Tooltip:** For contextual help on voice features

