# Speech Capabilities

## Table of Contents
- [Speech-to-Text Overview](#speech-to-text-overview)
- [Enabling Speech Recognition](#enabling-speech-recognition)
- [Language Configuration](#language-configuration)
- [Interim Results](#interim-results)
- [Button Customization](#button-customization)
- [Speech-to-Text Events](#speech-to-text-events)
- [Text-to-Speech Setup](#text-to-speech-setup)
- [Text-to-Speech Toolbar Integration](#text-to-speech-toolbar-integration)
- [Browser Compatibility](#browser-compatibility)

## Speech-to-Text Overview

The AI AssistView integrates the Web Speech API for voice input, allowing users to speak prompts instead of typing.

### Prerequisites

- Syncfusion AI AssistView component
- Browser with Web Speech API support
- Microphone permission granted

## Enabling Speech Recognition

### Basic Setup

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs, SpeechToTextSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const speechToTextSettings: SpeechToTextSettingsModel = {
        enable: true
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse('Response');
        }, 1000);
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            speechToTextSettings={speechToTextSettings}
        />
    );
}

export default App;
```

### Microphone Button

When enabled, a microphone button appears in the toolbar to trigger voice input.

## Language Configuration

### Setting Recognition Language

Configure the `lang` property to specify which language to recognize (default uses browser language):

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    lang: 'en-US'  // English - United States
};
```

### Common Language Codes

```tsx
// English
'en-US'      // United States
'en-GB'      // Great Britain
'en-AU'      // Australia

// Spanish
'es-ES'      // Spain
'es-MX'      // Mexico

// French
'fr-FR'      // France
'fr-CA'      // Canada

// German
'de-DE'      // Germany

// Mandarin Chinese
'zh-CN'      // Simplified Chinese
'zh-TW'      // Traditional Chinese

// Japanese
'ja-JP'      // Japan

// Arabic
'ar-SA'      // Saudi Arabia
'ar-AE'      // UAE
```

### Multiple Language Support

```tsx
const [selectedLang, setSelectedLang] = React.useState('en-US');

const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    lang: selectedLang
};

return (
    <div>
        <select onChange={(e) => setSelectedLang(e.target.value)}>
            <option value="en-US">English</option>
            <option value="es-ES">Spanish</option>
            <option value="fr-FR">French</option>
        </select>
        <AIAssistViewComponent 
            id="aiAssistView"
            speechToTextSettings={speechToTextSettings}
        />
    </div>
);
```

## Interim Results

### Enable Real-Time Transcription

Show partial transcription while user is still speaking:

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    lang: 'en-US',
    allowInterimResults: true  // Show partial results
};
```

### Without Interim Results (Default)

Only final results are displayed after user stops speaking:

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    allowInterimResults: false  // Only final results
};
```

## Button Customization

### Customize Button Text and Icons

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    buttonSettings: {
        content: 'Start Recording',           // Text when idle
        stopContent: 'Stop Recording',        // Text while recording
        iconCss: 'e-icons e-microphone',      // Icon when idle
        stopIconCss: 'e-icons e-microphone-off'  // Icon while recording
    }
};

<AIAssistViewComponent 
    id="aiAssistView"
    speechToTextSettings={speechToTextSettings}
/>
```

### Custom Button Labels

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    buttonSettings: {
        content: '🎙️ Speak Now',
        stopContent: '⏹️ Stop Speaking'
    }
};
```

## Speech-to-Text Events

### Handle Speech Lifecycle Events

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    onStart: (args: any) => {
        console.log('Speech recognition started');
        // Show recording indicator
    },
    onStop: (args: any) => {
        console.log('Speech recognition stopped');
        // Hide recording indicator
    },
    transcriptChanged: (args: any) => {
        console.log('Transcript updated:', args.text);
        // Update UI with partial transcript
    },
    onError: (args: any) => {
        console.log('Speech error:', args.error);
        // Show error message
    }
};
```

### Complete Event Implementation

```tsx
import { AIAssistViewComponent, SpeechToTextSettingsModel } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const [isRecording, setIsRecording] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [error, setError] = useState('');

    const speechToTextSettings: SpeechToTextSettingsModel = {
        enable: true,
        lang: 'en-US',
        allowInterimResults: true,
        onStart: () => {
            setIsRecording(true);
            setError('');
        },
        onStop: () => {
            setIsRecording(false);
        },
        transcriptChanged: (args: any) => {
            const text = args.text || args.transcript || '';
            setTranscript(text);
        },
        onError: (args: any) => {
            setError(args.error || 'Speech recognition error');
            setIsRecording(false);
        }
    };

    return (
        <div>
            <div className="speech-status">
                {isRecording && <span className="recording-indicator">🔴 Recording...</span>}
                {error && <span className="error-message">⚠️ {error}</span>}
            </div>
            <div className="transcript-display">
                {transcript || 'Waiting for speech...'}
            </div>
            <AIAssistViewComponent 
                id="aiAssistView"
                speechToTextSettings={speechToTextSettings}
            />
        </div>
    );
}

export default App;
```

## Text-to-Speech Setup

### Enable Response Audio

Add Text-to-Speech button to response toolbar:

```tsx
import { AIAssistViewComponent, ResponseToolbarSettingsModel, ToolbarItemClickedEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const responseToolbarSettings: ResponseToolbarSettingsModel = {
        items: [
            { type: 'Button', iconCss: 'e-icons e-audio', tooltip: 'Read Aloud' }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            if (args.item.iconCss === 'e-icons e-audio') {
                speakResponse(args.dataIndex);
            }
        }
    };

    const speakResponse = (index: number) => {
        const response = assistInstance.current?.prompts[index].response;
        if (response) {
            // Extract plain text from HTML response
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = response;
            const text = tempDiv.textContent || '';
            
            // Use Web Speech API
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            speechSynthesis.speak(utterance);
        }
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            responseToolbarSettings={responseToolbarSettings}
        />
    );
}

export default App;
```

## Text-to-Speech Toolbar Integration

### Add Audio Controls to Response Toolbar

```tsx
import { marked } from 'marked';

const responseToolbarSettings: ResponseToolbarSettingsModel = {
    items: [
        { type: 'Button', iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' },
        { type: 'Button', iconCss: 'e-icons e-audio', tooltip: 'Read Aloud' },
        { type: 'Button', iconCss: 'e-icons e-assist-like', tooltip: 'Like' }
    ],
    itemClicked: (args: ToolbarItemClickedEventArgs) => {
        const response = assistInstance.current?.prompts[args.dataIndex].response;
        
        switch (args.item.iconCss) {
            case 'e-icons e-audio':
                readResponseAloud(response);
                break;
            case 'e-icons e-assist-copy':
                navigator.clipboard.writeText(response);
                break;
        }
    }
};

const readResponseAloud = (htmlResponse: string) => {
    // Extract plain text
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlResponse;
    const plainText = tempDiv.textContent || '';
    
    // Speak
    const utterance = new SpeechSynthesisUtterance(plainText);
    utterance.rate = 1.0;        // Speed
    utterance.pitch = 1.0;       // Pitch
    utterance.volume = 1.0;      // Volume
    
    speechSynthesis.speak(utterance);
};
```

### Play/Pause Toggle

```tsx
let currentUtterance: SpeechSynthesisUtterance | null = null;

const handleAudioClick = (response: string) => {
    if (currentUtterance && speechSynthesis.speaking) {
        // Stop playing
        speechSynthesis.cancel();
        currentUtterance = null;
    } else {
        // Start playing
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = response;
        const text = tempDiv.textContent || '';
        
        currentUtterance = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(currentUtterance);
    }
};
```

## Tooltip Configuration

### Customize Microphone Button Tooltips

```tsx
const speechToTextSettings: SpeechToTextSettingsModel = {
    enable: true,
    tooltipSettings: {
        content: 'Click to start listening',
        stopContent: 'Click to stop listening',
        position: 'TopCenter'  // Tooltip position
    }
};
```

## Complete Speech Example

```tsx
import { 
    AIAssistViewComponent, 
    PromptRequestEventArgs,
    SpeechToTextSettingsModel,
    ResponseToolbarSettingsModel,
    ToolbarItemClickedEventArgs
} from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef, useState } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);
    const [recordingStatus, setRecordingStatus] = useState('Ready');
    let currentUtterance: SpeechSynthesisUtterance | null = null;

    const speechToTextSettings: SpeechToTextSettingsModel = {
        enable: true,
        lang: 'en-US',
        allowInterimResults: true,
        buttonSettings: {
            content: '🎙️ Speak',
            stopContent: '⏹️ Stop'
        },
        onStart: () => setRecordingStatus('Recording...'),
        onStop: () => setRecordingStatus('Processing...'),
        transcriptChanged: (args: any) => {
            console.log('Transcript:', args.text);
        },
        onError: (args: any) => {
            setRecordingStatus(`Error: ${args.error}`);
        }
    };

    const responseToolbarSettings: ResponseToolbarSettingsModel = {
        items: [
            { iconCss: 'e-icons e-audio', tooltip: 'Read Aloud' },
            { iconCss: 'e-icons e-assist-copy', tooltip: 'Copy' }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            const response = assistInstance.current?.prompts[args.dataIndex].response;
            
            if (args.item.iconCss === 'e-icons e-audio') {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = response;
                const text = tempDiv.textContent || '';
                
                if (currentUtterance && speechSynthesis.speaking) {
                    speechSynthesis.cancel();
                    currentUtterance = null;
                } else {
                    currentUtterance = new SpeechSynthesisUtterance(text);
                    speechSynthesis.speak(currentUtterance);
                }
            }
        }
    };

    const handlePromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            assistInstance.current?.addPromptResponse(
                'Response to: ' + args.prompt
            );
            setRecordingStatus('Ready');
        }, 1000);
    };

    return (
        <div>
            <div className="status-bar">
                Status: <span className="status-text">{recordingStatus}</span>
            </div>
            <AIAssistViewComponent 
                id="aiAssistView"
                ref={assistInstance}
                promptRequest={handlePromptRequest}
                speechToTextSettings={speechToTextSettings}
                responseToolbarSettings={responseToolbarSettings}
            />
        </div>
    );
}

export default App;
```

## Browser Compatibility

### Supported Browsers

| Browser | Speech-to-Text | Text-to-Speech |
|---------|----------------|-----------------|
| Chrome  | ✅ Yes | ✅ Yes |
| Edge    | ✅ Yes | ✅ Yes |
| Firefox | ⚠️ Limited | ✅ Yes |
| Safari  | ⚠️ Limited | ✅ Yes |
| Opera   | ✅ Yes | ✅ Yes |

### Feature Detection

```tsx
// Check if Speech Recognition is available
const isSpeechRecognitionAvailable = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

// Check if Speech Synthesis is available
const isSpeechSynthesisAvailable = 'speechSynthesis' in window;

if (!isSpeechRecognitionAvailable) {
    console.log('Speech-to-Text not supported');
}

if (!isSpeechSynthesisAvailable) {
    console.log('Text-to-Speech not supported');
}
```

## Best Practices

**Request microphone permission**: Ask users first before enabling  
**Show feedback during recording**: Visual indicators for recording state  
**Support language switching**: Allow users to change recognition language  
**Validate transcript**: Don't process incomplete or erroneous transcripts  
**Handle errors gracefully**: Show user-friendly error messages  
**Provide fallback**: Allow typing if voice input fails  
**Optimize audio playback**: Use appropriate speech rate and volume  
**Test browser compatibility**: Check supported browsers before deployment
