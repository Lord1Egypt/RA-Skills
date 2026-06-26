# Getting Started with React SpeechToText Component

## Installation

The SpeechToText component requires the Syncfusion React inputs package. Install it using npm:

```bash
npm install @syncfusion/ej2-react-inputs --save
```

## Project Setup

### Using Vite (Recommended)

Vite provides faster development and optimized builds for React applications.

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm run dev
```

Install the Syncfusion package:

```bash
npm install @syncfusion/ej2-react-inputs --save
```

### TypeScript Configuration

For TypeScript projects, ensure your `tsconfig.json` includes:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "jsx": "react-jsx",
    "skipLibCheck": true,
    "esModuleInterop": true
  }
}
```

## Basic Implementation

### Minimal Example (Functional Component)

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function App() {
  return (
    <div>
      <h1>Speech to Text</h1>
      <SpeechToTextComponent id="speechToText" />
    </div>
  );
}

export default App;
```

### Minimal Example (Class Component)

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { Component } from 'react';
import '@syncfusion/ej2-react-inputs/styles/material.css';

export default class App extends Component {
  public render() {
    return (
      <div>
        <h1>Speech to Text</h1>
        <SpeechToTextComponent id="speechToText" />
      </div>
    );
  }
}
```

## CSS Imports and Theme Selection

### Available Themes

Syncfusion provides multiple built-in themes:

- **Material** (default)
- **Bootstrap** 
- **Fluent**
- **Fabric**
- **Tailwind**
- **Bootstrap 5**

### Importing CSS

```tsx
// Material theme (default)
import '@syncfusion/ej2-react-inputs/styles/material.css';

// Bootstrap theme
import '@syncfusion/ej2-react-inputs/styles/bootstrap.css';

// Fluent theme
import '@syncfusion/ej2-react-inputs/styles/fluent.css';

// Include icon font CSS for button icons
import '@syncfusion/ej2-icons/styles/material.css';
```

### Using Multiple Themes

If you need icon support or additional styling:

```tsx
import '@syncfusion/ej2-base/styles/material.css';
import '@syncfusion/ej2-buttons/styles/material.css';
import '@syncfusion/ej2-popups/styles/material.css';
import '@syncfusion/ej2-react-inputs/styles/material.css';
import '@syncfusion/ej2-icons/styles/material.css';
```

## First Working Example

Here's a complete example with text display:

```tsx
import { SpeechToTextComponent, TextAreaComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';
import '@syncfusion/ej2-react-inputs/styles/material.css';

function VoiceApp() {
  const [transcript, setTranscript] = useState('');

  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    setTranscript(args.transcript);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>Speech to Text Demo</h2>
      
      {/* Speech to Text Component */}
      <div style={{ marginBottom: '20px' }}>
        <p>Click the microphone button to start speaking:</p>
        <SpeechToTextComponent 
          id="speechToText"
          transcriptChanged={handleTranscriptChanged}
        />
      </div>

      {/* Display transcribed text */}
      <div>
        <p>Transcribed Text:</p>
        <TextAreaComponent
          id="transcriptArea"
          value={transcript}
          readOnly={false}
          rows={5}
          cols={50}
          placeholder="Your speech will appear here..."
        />
      </div>
    </div>
  );
}

export default VoiceApp;
```

## Disabling the Component

Use the `disabled` property to prevent all user interaction with the component. When `true`, clicking the microphone button has no effect and `startListening()` / `stopListening()` calls are ignored.

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function DisabledDemo() {
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = async () => {
    setIsProcessing(true);
    // Simulate async operation
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsProcessing(false);
  };

  return (
    <div>
      {/* Disable voice input while form is being submitted */}
      <SpeechToTextComponent disabled={isProcessing} />
      <button onClick={handleSubmit} disabled={isProcessing}>
        {isProcessing ? 'Submitting...' : 'Submit'}
      </button>
    </div>
  );
}

export default DisabledDemo;
```

> **Note:** The `disabled` property defaults to `false`. It is useful for preventing user interaction during loading states, form submission, or when the feature should be temporarily unavailable.

## Handling Events

The component supports multiple events that fire during the speech recognition process:

```tsx
import { SpeechToTextComponent, TranscriptChangedEventArgs } from '@syncfusion/ej2-react-inputs';

function EventDemo() {
  const handleCreated = () => {
    console.log('Component initialized');
  };

  const handleStart = (args: any) => {
    console.log('Speech recognition started');
  };

  const handleStop = (args: any) => {
    console.log('Speech recognition stopped');
  };

  const handleError = (args: any) => {
    console.error('Error:', args.error);
  };

  const handleTranscriptChanged = (args: TranscriptChangedEventArgs) => {
    console.log('Transcript:', args.transcript);
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

export default EventDemo;
```

## License Registration

For production use, register your Syncfusion license key in your main App component:

```tsx
import { registerLicense } from '@syncfusion/ej2-base';

// Register your license key
registerLicense('YOUR_LICENSE_KEY_HERE');

function App() {
  return <SpeechToTextComponent id="speechToText" />;
}

export default App;
```

## Development Server

Start the development server:

**Vite:**
```bash
npm run dev
```

**Create React App:**
```bash
npm start
```

The application will be available at `http://localhost:5173` (Vite) or `http://localhost:3000` (CRA).

## Verification

Once the app is running, you should see:
1. A microphone button displayed on the page
2. The ability to click the button to start speaking
3. Text appearing as you speak (or after you finish, depending on settings)

If the microphone button doesn't appear, check:
- CSS imports are included
- Browser supports Web Speech API
- Microphone permissions are granted
