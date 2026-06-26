# AI Integration Setup

## Table of Contents
- [AI Service Overview](#ai-service-overview)
- [Azure OpenAI Setup](#azure-openai-setup)
- [API Credentials Configuration](#api-credentials-configuration)
- [Real-Time Prompt Processing](#real-time-prompt-processing)
- [Stream Response Handling](#stream-response-handling)
- [Markdown Response Parsing](#markdown-response-parsing)
- [Error Handling](#error-handling)
- [Rate Limiting and Optimization](#rate-limiting-and-optimization)
- [Security Considerations](#security-considerations)

## AI Service Overview

The AI AssistView can integrate with various AI services:
- **Azure OpenAI**: Microsoft's hosted OpenAI service
- **OpenAI**: Direct API access to GPT models
- **Google Gemini**: Google's advanced AI model
- **Anthropic Claude**: Constitutional AI models
- **Custom APIs**: Any REST-based AI service

## Azure OpenAI Setup

### Prerequisites

1. Azure account with OpenAI resource created
2. API key and endpoint from Azure portal
3. Deployed model (e.g., gpt-4, gpt-3.5-turbo)
4. API version (e.g., 2024-02-01)

### Getting Azure OpenAI Credentials

```tsx
// Log into Azure Portal → Azure OpenAI → Resource
// Under "Keys and endpoint":
const azureOpenAIApiKey = 'Your_API_Key_Here';
const azureOpenAIEndpoint = 'https://your-resource.openai.azure.com/';
const azureOpenAIApiVersion = '2024-02-01';
const azureDeploymentName = 'gpt-35-turbo'; // or your deployment
```

## API Credentials Configuration

### Secure Credential Management

**Never expose API keys in client-side code in production!**

```tsx
// ❌ WRONG - Exposes API key
const apiKey = 'sk-abc123...'; // DANGEROUS!

// ✅ CORRECT - Use environment variables
const apiKey = process.env.REACT_APP_OPENAI_KEY;

// ✅ BETTER - Use backend proxy
const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ prompt: userPrompt })
});
```

### Environment Variable Setup

Create `.env.local` file:

```
REACT_APP_OPENAI_API_KEY=your_key_here
REACT_APP_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
REACT_APP_OPENAI_DEPLOYMENT=gpt-35-turbo
```

Access in React:

```tsx
const apiKey = process.env.REACT_APP_OPENAI_API_KEY;
const endpoint = process.env.REACT_APP_OPENAI_ENDPOINT;
```

## Real-Time Prompt Processing

### Basic Prompt-Response Flow

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        try {
            // Call AI service with user prompt
            const response = await fetch(
                `${process.env.REACT_APP_OPENAI_ENDPOINT}/openai/deployments/${process.env.REACT_APP_OPENAI_DEPLOYMENT}/chat/completions?api-version=${process.env.REACT_APP_OPENAI_API_VERSION}`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'api-key': process.env.REACT_APP_OPENAI_API_KEY!
                    },
                    body: JSON.stringify({
                        messages: [{ role: 'user', content: args.prompt }],
                        temperature: 0.7,
                        max_tokens: 500
                    })
                }
            );

            const data = await response.json();
            const aiResponse = data.choices[0].message.content;
            
            // Display response
            assistInstance.current?.addPromptResponse(aiResponse);
            
        } catch (error) {
            assistInstance.current?.addPromptResponse('Error: Unable to process request');
            console.error('AI API error:', error);
        }
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
        />
    );
}

export default App;
```

## Stream Response Handling

### Streaming Responses from AI

Enable real-time typing effect:

```tsx
import { marked } from 'marked';

const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        const response = await fetch(
            `${endpoint}/openai/deployments/${deployment}/chat/completions?api-version=${apiVersion}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'api-key': apiKey
                },
                body: JSON.stringify({
                    messages: [{ role: 'user', content: args.prompt }],
                    stream: true  // Enable streaming
                })
            }
        );

        const reader = response.body.getReader();
        let fullResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            // Decode and parse streaming chunks
            const chunk = new TextDecoder().decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        const content = data.choices[0].delta?.content;
                        
                        if (content) {
                            fullResponse += content;
                            
                            // Update UI with partial response
                            const htmlResponse = marked.parse(fullResponse);
                            assistInstance.current?.addPromptResponse(
                                htmlResponse,
                                false  // Not final yet
                            );
                        }
                    } catch (e) {
                        // Handle parse errors silently
                    }
                }
            }
        }

        // Mark as final when complete
        assistInstance.current?.addPromptResponse(
            marked.parse(fullResponse),
            true  // Final response
        );

    } catch (error) {
        assistInstance.current?.addPromptResponse('Error streaming response');
        console.error('Streaming error:', error);
    }
};
```

## Markdown Response Parsing

### Install and Configure Marked

```bash
npm install marked --save
```

### Convert Markdown to HTML

```tsx
import { marked } from 'marked';

const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        const response = await getAIResponse(args.prompt);
        
        // Response is markdown from AI
        const htmlResponse = marked.parse(response);
        
        // Display formatted HTML
        assistInstance.current?.addPromptResponse(htmlResponse);
        
    } catch (error) {
        console.error('Error:', error);
    }
};
```

### Markdown to HTML Example

```tsx
const markdownText = `
## Response Title

This is **bold** and this is *italic*.

- Bullet point 1
- Bullet point 2

\`\`\`javascript
const example = "code block";
\`\`\`

[Link](https://example.com)
`;

const htmlResponse = marked.parse(markdownText);
// Displays formatted HTML with headings, lists, code blocks, etc.
```

## Error Handling

### Comprehensive Error Handling

```tsx
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    try {
        // Validate input
        if (!args.prompt?.trim()) {
            assistInstance.current?.addPromptResponse('Please enter a prompt');
            return;
        }

        // Show loading state
        assistInstance.current?.addPromptResponse('Processing...');

        // Call AI service
        const response = await fetch(aiEndpoint, {
            method: 'POST',
            headers: { 'api-key': apiKey },
            body: JSON.stringify({ messages: [{ role: 'user', content: args.prompt }] })
        });

        // Handle HTTP errors
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Authentication failed');
            } else if (response.status === 429) {
                throw new Error('Rate limit exceeded. Please try again later');
            } else {
                throw new Error(`API error: ${response.statusText}`);
            }
        }

        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        assistInstance.current?.addPromptResponse(aiResponse);

    } catch (error: any) {
        // Show user-friendly error message
        const errorMessage = error instanceof Error 
            ? error.message 
            : 'An unexpected error occurred';
        
        assistInstance.current?.addPromptResponse(
            `<div class="error-message">⚠️ ${errorMessage}</div>`
        );
        
        // Log for debugging
        console.error('Prompt handling error:', error);
    }
};
```

### API-Specific Error Handling

```tsx
const handleAzureOpenAIError = (response: Response, data: any) => {
    if (data.error?.code === 'AuthenticationFailed') {
        return 'Invalid API key. Please check your credentials.';
    } else if (data.error?.code === 'DeploymentNotFound') {
        return 'Model deployment not found. Check deployment name.';
    } else if (data.error?.code === 'RequestTooLarge') {
        return 'Prompt is too long. Please make it shorter.';
    } else if (response.status === 429) {
        return 'Too many requests. Please wait a moment.';
    } else {
        return `Error: ${data.error?.message || 'Unknown error'}`;
    }
};
```

## Rate Limiting and Optimization

### Implement Request Throttling

```tsx
import { useRef } from 'react';

function App() {
    const lastRequestTime = useRef<number>(0);
    const requestDelay = 500; // Minimum 500ms between requests

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        const now = Date.now();
        
        // Throttle requests
        if (now - lastRequestTime.current < requestDelay) {
            assistInstance.current?.addPromptResponse('Please wait before sending another prompt');
            return;
        }
        
        lastRequestTime.current = now;
        
        // Process prompt
        try {
            const response = await getAIResponse(args.prompt);
            assistInstance.current?.addPromptResponse(response);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            promptRequest={handlePromptRequest}
        />
    );
}
```

### Token Optimization

```tsx
// Limit response length to reduce token usage
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    const response = await fetch(aiEndpoint, {
        method: 'POST',
        headers: { 'api-key': apiKey },
        body: JSON.stringify({
            messages: [{ role: 'user', content: args.prompt }],
            max_tokens: 300,  // Limit response length
            temperature: 0.7  // Control creativity
        })
    });

    // ... handle response
};
```

## Security Considerations

### Backend Proxy Pattern (Recommended)

```tsx
// Client-side: Call your backend
const handlePromptRequest = async (args: PromptRequestEventArgs) => {
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: args.prompt })
    });
    
    const data = await response.json();
    assistInstance.current?.addPromptResponse(data.response);
};

// Server-side (Node.js/Express):
app.post('/api/chat', async (req, res) => {
    const { prompt } = req.body;
    
    // API key stays on server
    const response = await fetch('https://api.openai.com/...', {
        headers: { 'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` },
        body: JSON.stringify({ messages: [{ role: 'user', content: prompt }] })
    });
    
    const data = await response.json();
    res.json({ response: data.choices[0].message.content });
});
```

### Input Validation

```tsx
const validatePrompt = (prompt: string): boolean => {
    // Check length
    if (prompt.length > 2000) return false;
    
    // Check for malicious patterns
    if (prompt.includes('<script>')) return false;
    if (prompt.includes('javascript:')) return false;
    
    // Check for injection attempts
    if (prompt.toLowerCase().includes('ignore previous')) return false;
    
    return true;
};

const handlePromptRequest = (args: PromptRequestEventArgs) => {
    if (!validatePrompt(args.prompt)) {
        assistInstance.current?.addPromptResponse('Invalid prompt');
        return;
    }
    
    // Safe to process
    processPrompt(args.prompt);
};
```

## Complete Integration Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import { marked } from 'marked';
import React, { useRef } from 'react';

function App() {
    const assistInstance = useRef<AIAssistViewComponent>(null);

    const handlePromptRequest = async (args: PromptRequestEventArgs) => {
        if (!args.prompt?.trim()) {
            assistInstance.current?.addPromptResponse('Please enter a prompt');
            return;
        }

        try {
            // Show loading
            assistInstance.current?.addPromptResponse('Processing your request...');

            // Call backend API (not direct AI API)
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: args.prompt })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            
            // Parse and display response
            const htmlResponse = marked.parse(data.response);
            assistInstance.current?.addPromptResponse(htmlResponse);

        } catch (error) {
            assistInstance.current?.addPromptResponse(
                '⚠️ Error processing request. Please try again.'
            );
            console.error('Error:', error);
        }
    };

    return (
        <AIAssistViewComponent 
            id="aiAssistView"
            ref={assistInstance}
            promptRequest={handlePromptRequest}
            prompt="Ask me anything!"
            promptSuggestions={[
                'What can you help with?',
                'Tell me about AI',
                'How do I get started?'
            ]}
        />
    );
}

export default App;
```

## Best Practices Summary

✅ **Use backend proxy for API credentials**  
✅ **Implement request throttling**  
✅ **Parse responses as markdown**  
✅ **Handle all error cases gracefully**  
✅ **Validate user input**  
✅ **Implement streaming for long responses**  
✅ **Log errors for debugging**  
✅ **Show loading states**  
✅ **Optimize token usage**  
✅ **Use environment variables for configuration**
