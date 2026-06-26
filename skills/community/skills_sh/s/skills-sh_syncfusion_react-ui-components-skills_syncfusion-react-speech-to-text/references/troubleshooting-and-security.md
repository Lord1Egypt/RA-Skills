# Troubleshooting and Security

## Table of Contents
- [Common Issues and Solutions](#common-issues-and-solutions)
- [Browser Compatibility](#browser-compatibility)
- [Microphone Permission Handling](#microphone-permission-handling)
- [Security Considerations](#security-considerations)
- [Privacy and Data Handling](#privacy-and-data-handling)
- [Performance Optimization](#performance-optimization)
- [Offline Fallbacks](#offline-fallbacks)

## Common Issues and Solutions

### Issue: Component doesn't render

**Problem:** SpeechToText component not showing on page

**Solutions:**
1. Check CSS imports
```tsx
import '@syncfusion/ej2-react-inputs/styles/material.css';
import '@syncfusion/ej2-icons/styles/material.css';
```

2. Verify component is imported
```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
```

3. Check license key if in production
```tsx
import { registerLicense } from '@syncfusion/ej2-base';
registerLicense('YOUR_LICENSE_KEY');
```

4. Check browser console for errors using DevTools

### Issue: Microphone button not working

**Problem:** Button doesn't respond to clicks

**Solutions:**
1. Check microphone permissions (see [Microphone Permission Handling](#microphone-permission-handling))
2. Verify browser supports Web Speech API
3. Check for JavaScript errors in console
4. Try refreshing the page

### Issue: Speech not being recognized

**Problem:** Component listens but doesn't transcribe text

**Solutions:**
1. **Check microphone volume** - Speak louder
2. **Verify language setting** - Ensure correct language code
```tsx
<SpeechToTextComponent lang="en-US" />  // en-US, not just "en"
```

3. **Check microphone quality** - Test microphone with browser settings
4. **Speak clearly and pause** - Avoid overlapping words
5. **Verify browser support** - Check browser compatibility matrix

### Issue: Transcript not updating

**Problem:** `transcriptChanged` event not firing

**Solutions:**
1. Verify event handler is properly bound
```tsx
const handleTranscript = (args: TranscriptChangedEventArgs) => {
  console.log(args.transcript);
};

<SpeechToTextComponent transcriptChanged={handleTranscript} />
```

2. Check if component is in listening state
3. Enable interim results
```tsx
<SpeechToTextComponent allowInterimResults={true} />
```

### Issue: Intermittent recognition failures

**Problem:** Works sometimes, fails other times

**Solutions:**
1. Check network connectivity (required for browser APIs)
2. Verify microphone is detected
```tsx
const handleError = (args: ErrorEventArgs) => {
  if (args.error === 'audio-capture') {
    console.log('Microphone not found');
  }
};
```

3. Add retry logic
```tsx
let retryCount = 0;
const maxRetries = 3;

const handleError = (args: ErrorEventArgs) => {
  if (retryCount < maxRetries) {
    retryCount++;
    speechRef.current?.startListening();
  }
};
```

### Issue: Slow performance or lag

**Problem:** Component feels sluggish or updates are delayed

**Solutions:**
1. Disable interim results if not needed
```tsx
<SpeechToTextComponent allowInterimResults={false} />
```

2. Use debouncing for transcript updates
```tsx
const debounce = (func: Function, delay: number) => {
  let timeoutId: any;
  return (...args: any[]) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

const debouncedUpdate = debounce((text: string) => {
  setTranscript(text);
}, 300);
```

3. Optimize component re-renders using React.memo

## Browser Compatibility

### Supported Browsers

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Fully Supported | Best support, recommended |
| Edge | ✅ Fully Supported | Good support |
| Firefox | ⚠️ Limited | Basic support, may require flags |
| Safari | ✅ Supported | iOS 14.5+ supported |
| Opera | ✅ Supported | Based on Chromium |
| IE 11 | ❌ Not Supported | Not supported |

### Checking Browser Support

```tsx
import { SpeechToTextComponent } from '@syncfusion/ej2-react-inputs';
import { useState, useEffect } from 'react';

function BrowserCheckDemo() {
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || 
                           (window as any).webkitSpeechRecognition;
    setIsSupported(!!SpeechRecognition);
  }, []);

  if (!isSupported) {
    return (
      <div style={{ padding: '20px', backgroundColor: '#ffebee', color: '#c62828' }}>
        Your browser does not support the Speech Recognition API.
        Please use Chrome, Edge, or Safari.
      </div>
    );
  }

  return <SpeechToTextComponent />;
}

export default BrowserCheckDemo;
```

### Graceful Degradation

```tsx
function FallbackDemo() {
  const [isSupported, setIsSupported] = useState(true);

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || 
                           (window as any).webkitSpeechRecognition;
    setIsSupported(!!SpeechRecognition);
  }, []);

  if (!isSupported) {
    return (
      <div>
        <p>Speech recognition not supported. Please use text input:</p>
        <input type="text" placeholder="Enter text manually" />
      </div>
    );
  }

  return <SpeechToTextComponent />;
}

export default FallbackDemo;
```

## Microphone Permission Handling

### Requesting Permissions

Modern browsers require explicit user permission to access the microphone.

```tsx
import { SpeechToTextComponent, ErrorEventArgs } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function MicrophonePermissionDemo() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  const handleError = (args: ErrorEventArgs) => {
    if (args.error === 'not-allowed') {
      setHasPermission(false);
    }
  };

  const handleStart = () => {
    setHasPermission(true);
  };

  return (
    <div>
      <SpeechToTextComponent
        onStart={handleStart}
        onError={handleError}
      />

      {hasPermission === false && (
        <div style={{
          padding: '10px',
          marginTop: '10px',
          backgroundColor: '#ffebee',
          borderLeft: '4px solid #f44336'
        }}>
          <p>🔒 Microphone permission denied</p>
          <p>To use voice input, please:</p>
          <ol>
            <li>Click the lock icon in the address bar</li>
            <li>Allow microphone access</li>
            <li>Refresh the page</li>
          </ol>
        </div>
      )}
    </div>
  );
}

export default MicrophonePermissionDemo;
```

### Checking Permissions at Startup

```tsx
import { useEffect, useState } from 'react';

function CheckMicrophonePermission() {
  const [permission, setPermission] = useState<'granted' | 'denied' | 'prompt' | null>(null);

  useEffect(() => {
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions.query({ name: 'microphone' })
        .then(permissionStatus => {
          setPermission(permissionStatus.state as any);
        });
    }
  }, []);

  return (
    <div>
      Microphone Permission: {permission || 'Checking...'}
    </div>
  );
}
```

## Security Considerations

### 1. HTTPS Requirement

Speech recognition requires secure context (HTTPS):

```tsx
// ✅ Works
// https://example.com

// ❌ Doesn't work
// http://example.com  (except localhost for development)
```

**Solution:** Always use HTTPS in production

```tsx
if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
  // Redirect to HTTPS or show warning
  console.warn('Speech recognition requires HTTPS');
}
```

### 2. Content Security Policy (CSP)

Ensure your CSP allows Web Speech API:

```tsx
// In your HTML head:
// <meta http-equiv="Content-Security-Policy" 
//       content="default-src 'self'; ...">
```

### 3. Third-Party Data Processing

Audio is sent to third-party servers for processing:

```tsx
// Inform users
function SecureVoiceApp() {
  return (
    <div>
      <p>⚠️ Your voice data will be processed by Google's servers for transcription.</p>
      <SpeechToTextComponent />
    </div>
  );
}
```

### 4. Input Sanitization

Always sanitize transcript before using:

```tsx
import { TextAreaComponent } from '@syncfusion/ej2-react-inputs';
import { useState } from 'react';

function SanitizedTranscript() {
  const [transcript, setTranscript] = useState('');

  const sanitizeText = (text: string): string => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  };

  const handleTranscript = (args: any) => {
    setTranscript(sanitizeText(args.transcript));
  };

  return (
    <div>
      <SpeechToTextComponent transcriptChanged={handleTranscript} />
      <TextAreaComponent value={transcript} />
    </div>
  );
}
```

## Privacy and Data Handling

### 1. Inform Users

Clearly communicate data usage:

```tsx
function PrivacyNotice() {
  return (
    <div style={{ backgroundColor: '#e3f2fd', padding: '10px', marginBottom: '10px' }}>
      <strong>Privacy Notice:</strong>
      <p>Your voice input will be sent to external servers for speech-to-text processing.
         By using this feature, you agree to their privacy policies.</p>
    </div>
  );
}
```

### 2. User Consent

Implement consent mechanism:

```tsx
import { useState } from 'react';

function ConsentRequiredDemo() {
  const [hasConsent, setHasConsent] = useState(false);

  if (!hasConsent) {
    return (
      <div style={{ padding: '20px', border: '1px solid #ddd' }}>
        <p>This app uses voice recognition which sends audio to external servers.</p>
        <button onClick={() => setHasConsent(true)}>I Agree</button>
        <button>Cancel</button>
      </div>
    );
  }

  return <SpeechToTextComponent />;
}
```

### 3. Data Minimization

Don't store voice data longer than needed:

```tsx
import { useState } from 'react';

function DataMinimization() {
  const [transcript, setTranscript] = useState('');

  const clearData = () => {
    setTranscript('');
  };

  const downloadTranscript = () => {
    const element = document.createElement('a');
    element.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(transcript);
    element.download = 'transcript.txt';
    element.click();
  };

  return (
    <div>
      <SpeechToTextComponent 
        transcriptChanged={(args: any) => setTranscript(args.transcript)}
      />
      <button onClick={clearData}>Clear Data</button>
      <button onClick={downloadTranscript}>Download</button>
    </div>
  );
}
```

## Performance Optimization

### 1. Lazy Loading

Load component only when needed:

```tsx
import { lazy, Suspense } from 'react';

const SpeechComponent = lazy(() => 
  import('./SpeechToTextComponent').then(m => ({ 
    default: m.SpeechToTextComponent 
  }))
);

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SpeechComponent />
    </Suspense>
  );
}
```

### 2. Memoization

Prevent unnecessary re-renders:

```tsx
import { memo } from 'react';

const OptimizedSpeech = memo(({ onTranscript }: any) => (
  <SpeechToTextComponent transcriptChanged={onTranscript} />
));
```

### 3. Optimize Transcript Updates

```tsx
const handleTranscript = (args: TranscriptChangedEventArgs) => {
  // Only update state on final results (isInterimResult is false when result is final)
  if (!args.isInterimResult) {
    setFinalTranscript(args.transcript);
  }
};

return (
  <SpeechToTextComponent 
    allowInterimResults={false}
    transcriptChanged={handleTranscript}
  />
);
```

## Offline Fallbacks

### 1. Detect Offline Status

```tsx
import { useEffect, useState } from 'react';

function OfflineAwareApp() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (!isOnline) {
    return (
      <div style={{ padding: '20px', backgroundColor: '#fff3e0' }}>
        🌐 You are offline. Speech recognition is not available.
      </div>
    );
  }

  return <SpeechToTextComponent />;
}
```

### 2. Text Input Fallback

```tsx
import { useState } from 'react';

function VoiceWithFallback() {
  const [useVoice, setUseVoice] = useState(true);
  const [transcript, setTranscript] = useState('');

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <input 
          type="radio" 
          name="input"
          checked={useVoice}
          onChange={() => setUseVoice(true)}
        />
        <label>Voice Input</label>
        
        <input 
          type="radio" 
          name="input"
          checked={!useVoice}
          onChange={() => setUseVoice(false)}
        />
        <label>Text Input</label>
      </div>

      {useVoice ? (
        <SpeechToTextComponent 
          transcriptChanged={(args: any) => setTranscript(args.transcript)}
        />
      ) : (
        <input 
          type="text"
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          placeholder="Enter text..."
        />
      )}
    </div>
  );
}
```

### 3. Cache Transcripts

```tsx
import { useState, useEffect } from 'react';

function CachedTranscripts() {
  const [transcripts, setTranscripts] = useState<string[]>([]);

  const saveTranscript = (text: string) => {
    setTranscripts(prev => [...prev, text]);
    localStorage.setItem('transcripts', JSON.stringify([...transcripts, text]));
  };

  useEffect(() => {
    const cached = localStorage.getItem('transcripts');
    if (cached) {
      setTranscripts(JSON.parse(cached));
    }
  }, []);

  return (
    <div>
      <SpeechToTextComponent 
        transcriptChanged={(args: any) => saveTranscript(args.transcript)}
      />
      <h3>Saved Transcripts:</h3>
      <ul>
        {transcripts.map((t, i) => <li key={i}>{t}</li>)}
      </ul>
    </div>
  );
}
```

## Best Practices Summary

✅ **Do:**
- Use HTTPS in production
- Inform users about data handling
- Test on multiple browsers
- Implement error handling
- Provide text input fallback
- Sanitize all user input
- Request microphone permission

❌ **Don't:**
- Use HTTP for speech features
- Store voice data unnecessarily
- Ignore browser compatibility
- Proceed without error handling
- Forget accessibility features
- Process untrusted data

