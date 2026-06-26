# AI Service Integrations

## Table of Contents
- [Overview](#overview)
- [Streaming Responses (enableStreaming)](#streaming-responses-enablestreaming)
- [OpenAI Integration](#openai-integration)
- [Google Gemini Integration](#google-gemini-integration)
- [Lite-LLM Integration](#lite-llm-integration)
- [Ollama Local LLM Integration](#ollama-local-llm-integration)
- [Integration Patterns](#integration-patterns)
- [Complete Examples](#complete-examples)

## Overview

The Inline AI Assist component is designed to work with various AI services. You handle the AI service integration yourself by:

1. **Listening to `promptRequest` event** - User submits a prompt
2. **Calling your AI service** - Send prompt to OpenAI, Gemini, or other service
3. **Adding response** - Use `addResponse()` method to display result

This gives you complete flexibility to use any AI service you prefer.

## Streaming Responses (enableStreaming)

The `enableStreaming` property enables real-time streaming of AI responses, providing a better user experience by displaying content as it's generated rather than waiting for the complete response.

### Property Details

**Type:** `boolean`  
**Default:** `false`  
**Component Property:** `enableStreaming`

### When to Use Streaming

✅ **Enable streaming when:**
- Working with LLMs that support streaming (OpenAI, Gemini, etc.)
- Responses are typically long (> 100 words)
- User experience is priority (immediate feedback)
- Building chat-like interfaces

❌ **Don't enable streaming when:**
- AI service doesn't support streaming
- Responses are short and fast (< 1 second)
- You need complete response for post-processing
- Bandwidth is limited

### Basic Usage

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    return (
        <InlineAIAssistComponent
            enableStreaming={true}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### How Streaming Works

When `enableStreaming` is enabled:

1. **Component Behavior Changes:**
   - Response area updates incrementally as text arrives
   - No need to wait for complete response
   - Better perceived performance

2. **Your Implementation:**
   - Call `addResponse()` multiple times with cumulative text
   - Each call updates the displayed response
   - Component handles the UI updates automatically

3. **User Experience:**
   - Text appears character-by-character or word-by-word
   - Immediate feedback that processing started
   - Natural chat-like interaction

### Streaming with OpenAI

```tsx
import { InlineAIAssistComponent, InlinePromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import OpenAI from 'openai';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const openai = new OpenAI({
        apiKey: process.env.REACT_APP_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true
    });

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            let fullResponse = '';

            const stream = await openai.chat.completions.create({
                model: 'gpt-4',
                messages: [{ role: 'user', content: args.prompt }],
                stream: true  // Enable streaming
            });

            // Process each chunk as it arrives
            for await (const chunk of stream) {
                const content = chunk.choices[0]?.delta?.content || '';
                fullResponse += content;
                
                // Update response incrementally
                assistRef.current?.addResponse(fullResponse);
            }
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            enableStreaming={true}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Streaming with Google Gemini

```tsx
import { InlineAIAssistComponent, InlinePromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import { GoogleGenerativeAI } from '@google/generative-ai';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const genAI = new GoogleGenerativeAI(process.env.REACT_APP_GEMINI_API_KEY!);
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            let fullResponse = '';

            // Generate content with streaming
            const result = await model.generateContentStream(args.prompt);

            // Process each chunk
            for await (const chunk of result.stream) {
                const chunkText = chunk.text();
                fullResponse += chunkText;
                
                // Update response incrementally
                assistRef.current?.addResponse(fullResponse);
            }
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            enableStreaming={true}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Streaming with Ollama

```tsx
import { InlineAIAssistComponent, InlinePromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const OLLAMA_API_URL = 'http://localhost:11434/api/generate';

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const response = await fetch(OLLAMA_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'llama2',
                    prompt: args.prompt,
                    stream: true  // Enable streaming
                })
            });

            const reader = response.body?.getReader();
            const decoder = new TextDecoder();
            let fullResponse = '';

            while (true) {
                const { done, value } = await reader!.read();
                if (done) break;

                const chunk = decoder.decode(value);
                
                // Parse JSON chunk
                try {
                    const json = JSON.parse(chunk);
                    fullResponse += json.response;
                    
                    // Update response incrementally
                    assistRef.current?.addResponse(fullResponse);
                } catch (e) {
                    // Skip malformed JSON chunks
                    console.warn('Skipping chunk:', chunk);
                }
            }
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            enableStreaming={true}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Advanced Streaming with Progress Indicator

Show visual feedback during streaming:

```tsx
const StreamingAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [isStreaming, setIsStreaming] = React.useState(false);
    const [streamProgress, setStreamProgress] = React.useState(0);

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        setIsStreaming(true);
        setStreamProgress(0);
        
        try {
            let fullResponse = '';
            let chunkCount = 0;

            const stream = await openai.chat.completions.create({
                model: 'gpt-4',
                messages: [{ role: 'user', content: args.prompt }],
                stream: true
            });

            for await (const chunk of stream) {
                const content = chunk.choices[0]?.delta?.content || '';
                fullResponse += content;
                chunkCount++;
                
                // Update progress
                setStreamProgress(chunkCount);
                
                // Update response
                assistRef.current?.addResponse(fullResponse);
            }
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        } finally {
            setIsStreaming(false);
        }
    };

    return (
        <div>
            {isStreaming && (
                <div className="streaming-indicator">
                    <span className="spinner"></span>
                    Streaming... ({streamProgress} chunks received)
                </div>
            )}
            
            <InlineAIAssistComponent
                ref={assistRef}
                enableStreaming={true}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
};
```

### Streaming with Error Recovery

Implement robust error handling for streaming:

```tsx
const RobustStreamingAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [retryCount, setRetryCount] = React.useState(0);
    const MAX_RETRIES = 3;

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        let attempt = 0;
        
        while (attempt < MAX_RETRIES) {
            try {
                let fullResponse = '';
                
                const stream = await openai.chat.completions.create({
                    model: 'gpt-4',
                    messages: [{ role: 'user', content: args.prompt }],
                    stream: true,
                    stream_options: { include_usage: true }
                });

                for await (const chunk of stream) {
                    const content = chunk.choices[0]?.delta?.content || '';
                    fullResponse += content;
                    assistRef.current?.addResponse(fullResponse);
                }
                
                // Success - break retry loop
                setRetryCount(0);
                break;
                
            } catch (error) {
                attempt++;
                setRetryCount(attempt);
                
                if (attempt >= MAX_RETRIES) {
                    assistRef.current?.addResponse(
                        `Failed after ${MAX_RETRIES} attempts. Error: ${error.message}`
                    );
                    break;
                }
                
                // Wait before retrying (exponential backoff)
                await new Promise(resolve => 
                    setTimeout(resolve, Math.pow(2, attempt) * 1000)
                );
            }
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            enableStreaming={true}
            promptRequest={handlePromptRequest}
        />
    );
};
```

### Performance Considerations

#### Throttling Updates

For very fast streams, throttle UI updates to improve performance:

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    let fullResponse = '';
    let lastUpdateTime = Date.now();
    const UPDATE_INTERVAL_MS = 50; // Update every 50ms

    const stream = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: args.prompt }],
        stream: true
    });

    for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || '';
        fullResponse += content;
        
        // Throttle updates
        const now = Date.now();
        if (now - lastUpdateTime >= UPDATE_INTERVAL_MS) {
            assistRef.current?.addResponse(fullResponse);
            lastUpdateTime = now;
        }
    }
    
    // Final update to ensure complete response
    assistRef.current?.addResponse(fullResponse);
};
```

#### Buffer Chunks

Buffer small chunks to reduce update frequency:

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    let fullResponse = '';
    let buffer = '';
    const BUFFER_SIZE = 10; // Words

    const stream = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: args.prompt }],
        stream: true
    });

    for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content || '';
        buffer += content;
        
        // Update when buffer reaches threshold
        if (buffer.split(' ').length >= BUFFER_SIZE) {
            fullResponse += buffer;
            assistRef.current?.addResponse(fullResponse);
            buffer = '';
        }
    }
    
    // Flush remaining buffer
    if (buffer) {
        fullResponse += buffer;
        assistRef.current?.addResponse(fullResponse);
    }
};
```

### Streaming Best Practices

1. **Always Handle Errors:**
   - Wrap streaming logic in try-catch
   - Provide meaningful error messages
   - Implement retry logic for transient failures

2. **Performance:**
   - Throttle UI updates for very fast streams
   - Buffer small chunks to reduce render frequency
   - Consider debouncing for large responses

3. **User Experience:**
   - Show streaming indicator/spinner
   - Allow users to cancel streaming
   - Display progress information

4. **Testing:**
   - Test with slow network conditions
   - Test error scenarios (network failure, API errors)
   - Verify complete response accuracy

5. **Resource Management:**
   - Clean up streams on component unmount
   - Cancel ongoing requests when new prompt submitted
   - Monitor memory usage with long responses

6. **Security:**
   - Validate and sanitize streamed content
   - Implement rate limiting
   - Monitor for malicious content

### Comparison: Streaming vs Non-Streaming

| Aspect | Streaming (`enableStreaming: true`) | Non-Streaming (`enableStreaming: false`) |
|--------|-------------------------------------|------------------------------------------|
| **User Experience** | Immediate feedback, word-by-word | Wait for complete response |
| **Perceived Speed** | Feels faster, progressive | May feel slower, all-at-once |
| **Implementation** | Call `addResponse()` multiple times | Call `addResponse()` once |
| **Error Handling** | Must handle partial responses | Simpler error handling |
| **Performance** | More UI updates | Single UI update |
| **Best For** | Long responses, chat interfaces | Short responses, fast APIs |
| **Network Usage** | Continuous connection | Single request-response |

### Migration from Non-Streaming to Streaming

If you have existing non-streaming code:

**Before (Non-Streaming):**
```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    const response = await callAI(args.prompt);
    assistRef.current?.addResponse(response);
};
```

**After (Streaming):**
```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    let fullResponse = '';
    const stream = await callAIStreaming(args.prompt);
    
    for await (const chunk of stream) {
        fullResponse += chunk;
        assistRef.current?.addResponse(fullResponse); // Called multiple times
    }
};

// Enable streaming in component
<InlineAIAssistComponent enableStreaming={true} {...props} />
```

## OpenAI Integration

### Setup: Get API Key

1. Sign up at [openai.com](https://platform.openai.com)
2. Create API key in [API keys page](https://platform.openai.com/api-keys)
3. Store securely (use environment variables, not hardcoded)

### Install OpenAI Package

```bash
npm install openai
```

### Basic Implementation

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import OpenAI from 'openai';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const openai = new OpenAI({
        apiKey: process.env.REACT_APP_OPENAI_API_KEY,
        dangerouslyAllowBrowser: true  // Only for development!
    });

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const message = await openai.chat.completions.create({
                model: 'gpt-4',
                messages: [
                    { role: 'user', content: args.prompt }
                ]
            });

            const response = message.choices[0].message.content || '';
            assistRef.current?.addResponse(response);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Advanced: Streaming Responses

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    try {
        let fullResponse = '';

        const stream = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{ role: 'user', content: args.prompt }],
            stream: true
        });

        for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content || '';
            fullResponse += content;
            // Update response incrementally
            assistRef.current?.addResponse(fullResponse);
        }
    } catch (error) {
        assistRef.current?.addResponse(`Error: ${error.message}`);
    }
};
```

### With Context History

```tsx
const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [conversationHistory, setConversationHistory] = React.useState<any[]>([]);

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            // Build message history
            const messages = [
                ...conversationHistory,
                { role: 'user', content: args.prompt }
            ];

            const response = await openai.chat.completions.create({
                model: 'gpt-4',
                messages
            });

            const assistantMessage = response.choices[0].message.content || '';
            
            // Add to history
            setConversationHistory([
                ...messages,
                { role: 'assistant', content: assistantMessage }
            ]);

            assistRef.current?.addResponse(assistantMessage);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};
```

## Google Gemini Integration

### Setup: Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click "Create API Key"
3. Store securely in environment variables

### Install Gemini Package

```bash
npm install @google/generative-ai
```

### Basic Implementation

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import { GoogleGenerativeAI } from '@google/generative-ai';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const genAI = new GoogleGenerativeAI(process.env.REACT_APP_GEMINI_API_KEY!);
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const result = await model.generateContent(args.prompt);
            const response = result.response.text();
            assistRef.current?.addResponse(response);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### With Safety Settings

```tsx
const model = genAI.getGenerativeModel({
    model: 'gemini-pro',
    safetySettings: [
        {
            category: HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
    ]
});

const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    try {
        const result = await model.generateContent({
            contents: [{
                role: 'user',
                parts: [{ text: args.prompt }]
            }]
        });

        const response = result.response.text();
        assistRef.current?.addResponse(response);
    } catch (error) {
        assistRef.current?.addResponse(`Error: ${error.message}`);
    }
};
```

### With Vision (Image Analysis)

```tsx
const model = genAI.getGenerativeModel({ model: 'gemini-pro-vision' });

const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    try {
        // If image available
        const imagePart = {
            inlineData: {
                data: imageBase64,
                mimeType: 'image/jpeg'
            }
        };

        const result = await model.generateContent([
            args.prompt,
            imagePart
        ]);

        const response = result.response.text();
        assistRef.current?.addResponse(response);
    } catch (error) {
        assistRef.current?.addResponse(`Error: ${error.message}`);
    }
};
```

## Lite-LLM Integration

### Setup

Lite-LLM is a library that provides a unified interface to multiple LLM providers.

```bash
npm install litellm
```

### Basic Implementation

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import { LiteLLM } from 'litellm';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const llm = new LiteLLM({
        apiKey: process.env.REACT_APP_LITELLM_API_KEY
    });

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const response = await llm.completion({
                model: 'gpt-3.5-turbo',
                messages: [
                    { role: 'user', content: args.prompt }
                ]
            });

            assistRef.current?.addResponse(response.choices[0].message.content);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Multiple Provider Support

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    const providers = ['openai', 'azure', 'anthropic'];
    
    for (const provider of providers) {
        try {
            const response = await llm.completion({
                model: `${provider}/gpt-3.5-turbo`,
                messages: [{ role: 'user', content: args.prompt }]
            });

            assistRef.current?.addResponse(response.choices[0].message.content);
            break;  // Success, exit loop
        } catch (error) {
            console.error(`${provider} failed, trying next...`);
            continue;
        }
    }
};
```

## Ollama Local LLM Integration

### Setup

Ollama runs LLMs locally on your machine. Download from [ollama.ai](https://ollama.ai)

```bash
# Install Ollama, then pull a model
ollama pull llama2
ollama serve  # Start Ollama server (default: http://localhost:11434)
```

### Basic Implementation

```tsx
import { InlineAIAssistComponent } from '@syncfusion/ej2-react-interactive-chat';
import React from 'react';

const App: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const OLLAMA_API_URL = 'http://localhost:11434/api/generate';

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const response = await fetch(OLLAMA_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    model: 'llama2',
                    prompt: args.prompt,
                    stream: false
                })
            });

            const data = await response.json();
            assistRef.current?.addResponse(data.response);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};

export default App;
```

### Streaming Response

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    try {
        const response = await fetch(OLLAMA_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'llama2',
                prompt: args.prompt,
                stream: true
            })
        });

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';

        while (true) {
            const { done, value } = await reader!.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const json = JSON.parse(chunk);
            fullResponse += json.response;

            // Update incrementally
            assistRef.current?.addResponse(fullResponse);
        }
    } catch (error) {
        assistRef.current?.addResponse(`Error: ${error.message}`);
    }
};
```

## Integration Patterns

### Pattern 1: Error Handling with Fallback

```tsx
const callAIService = async (prompt: string): Promise<string> => {
    try {
        // Try primary service
        return await openai.chat.completions.create({ ... });
    } catch (error) {
        console.error('OpenAI failed, trying Gemini...');
        try {
            // Try fallback service
            return await gemini.generateContent(prompt);
        } catch (fallbackError) {
            throw new Error('All AI services failed');
        }
    }
};

const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
    callAIService(args.prompt)
        .then(response => assistRef.current?.addResponse(response))
        .catch(error => assistRef.current?.addResponse(`Error: ${error.message}`));
};
```

### Pattern 2: Loading State Management

```tsx
const App: React.FC = () => {
    const [isLoading, setIsLoading] = React.useState(false);

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        setIsLoading(true);
        try {
            const response = await callAI(args.prompt);
            assistRef.current?.addResponse(response);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            {isLoading && <p>Processing...</p>}
            <InlineAIAssistComponent promptRequest={handlePromptRequest} />
        </div>
    );
};
```

### Pattern 3: Token Limit Management

```tsx
const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
    const maxTokens = 1000;
    const estimatedTokens = args.prompt.split(' ').length * 1.3;

    if (estimatedTokens > maxTokens) {
        assistRef.current?.addResponse(
            'Prompt too long. Please reduce and try again.'
        );
        return;
    }

    const response = await callAI(args.prompt);
    assistRef.current?.addResponse(response);
};
```

## Complete Examples

### Example 1: Multi-Service Provider

```tsx
const MultiServiceAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [service, setService] = React.useState<'openai' | 'gemini' | 'ollama'>('openai');

    const callService = async (prompt: string) => {
        switch (service) {
            case 'openai':
                return await openai.chat.completions.create({ ... });
            case 'gemini':
                return await gemini.generateContent(prompt);
            case 'ollama':
                return await fetch('http://localhost:11434/api/generate', { ... });
            default:
                throw new Error('Unknown service');
        }
    };

    const handlePromptRequest = (args: InlinePromptRequestEventArgs) => {
        callService(args.prompt)
            .then(response => assistRef.current?.addResponse(response))
            .catch(error => assistRef.current?.addResponse(`Error: ${error.message}`));
    };

    return (
        <div>
            <select value={service} onChange={(e) => setService(e.target.value as any)}>
                <option>openai</option>
                <option>gemini</option>
                <option>ollama</option>
            </select>
            <InlineAIAssistComponent
                ref={assistRef}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
};
```

### Example 2: Backend API Integration

```tsx
const BackendIntegration: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        try {
            const response = await fetch('/api/ai/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: args.prompt })
            });

            const data = await response.json();
            assistRef.current?.addResponse(data.response);
        } catch (error) {
            assistRef.current?.addResponse(`Error: ${error.message}`);
        }
    };

    return (
        <InlineAIAssistComponent
            ref={assistRef}
            promptRequest={handlePromptRequest}
        />
    );
};
```

### Example 3: Context-Aware Responses

```tsx
const ContextAwareAssistant: React.FC = () => {
    const assistRef = React.useRef<InlineAIAssistComponent>(null);
    const [context, setContext] = React.useState<string>('');

    const handlePromptRequest = async (args: InlinePromptRequestEventArgs) => {
        const enrichedPrompt = `
            Context: ${context}
            
            User Request: ${args.prompt}
        `;

        const response = await openai.chat.completions.create({
            model: 'gpt-4',
            messages: [{ role: 'user', content: enrichedPrompt }]
        });

        assistRef.current?.addResponse(response.choices[0].message.content || '');
    };

    return (
        <div>
            <textarea
                placeholder="Provide context..."
                onChange={(e) => setContext(e.target.value)}
            />
            <InlineAIAssistComponent
                ref={assistRef}
                promptRequest={handlePromptRequest}
            />
        </div>
    );
};
```

## Best Practices

1. **Security:** Never hardcode API keys; use environment variables
2. **Error Handling:** Always catch and display user-friendly errors
3. **Rate Limiting:** Implement rate limiting to avoid API quota exhaustion
4. **Caching:** Cache responses for identical prompts
5. **Timeouts:** Set reasonable timeouts for API calls
6. **Monitoring:** Log all API calls for debugging
7. **Cost Management:** Track token usage and costs
8. **User Feedback:** Show loading states during processing
9. **Retry Logic:** Implement exponential backoff for failed requests
10. **Privacy:** Don't send sensitive data to external services
