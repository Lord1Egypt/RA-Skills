# Volcengine API Parameters Reference

Complete reference for all API parameters available on Volcano Engine platform. Based on official API documentation.

## Chat API Parameters

Endpoint: `POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`

### Request Parameters

| Parameter | Type | Required | Description | Default | Constraints |
|-----------|------|----------|-------------|---------|-------------|
| `model` | string | Yes | Model ID to use for completion | - | Must be a valid Model ID from available models |
| `messages` | array | Yes | Array of message objects | - | At least one message required |
| `temperature` | number | No | Sampling temperature (0.0 to 2.0) | 0.7 | Higher = more random, lower = more focused |
| `top_p` | number | No | Nucleus sampling parameter (0.0 to 1.0) | 0.9 | Alternative to temperature sampling |
| `max_tokens` | integer | No | Maximum tokens to generate | Model-specific | Must be ≤ model's max output tokens |
| `stream` | boolean | No | Whether to stream responses | false | Enable for real-time output |
| `stop` | string/array | No | Stop sequences | null | Up to 4 sequences |
| `presence_penalty` | number | No | Penalize new tokens based on presence (-2.0 to 2.0) | 0.0 | Positive values penalize repetition |
| `frequency_penalty` | number | No | Penalize new tokens based on frequency (-2.0 to 2.0) | 0.0 | Positive values penalize repetition |
| `logit_bias` | map | No | Modify likelihood of specified tokens | null | Token ID to bias mapping |
| `user` | string | No | User identifier for abuse monitoring | null | - |
| `tools` | array | No | Tools available to the model | null | Function calling tools |
| `tool_choice` | string/object | No | Tool selection control | "auto" | "none", "auto", or specific tool |
| `response_format` | object | No | Response format specification | null | e.g., {"type": "json_object"} |
| `seed` | integer | No | Random seed for reproducibility | null | - |

### Message Object Structure

Each message object has the following structure:

```json
{
  "role": "system|user|assistant|tool",
  "content": "string or array",
  "name": "string (optional)",
  "tool_calls": "array (optional, assistant only)",
  "tool_call_id": "string (optional, tool only)"
}
```

#### Content Types

1. **Text Content** (string):
```json
{"role": "user", "content": "Hello, world!"}
```

2. **Multimodal Content** (array of objects):
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Describe this image"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
  ]
}
```

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | string | Unique completion ID |
| `object` | string | Always "chat.completion" |
| `created` | integer | Unix timestamp of creation |
| `model` | string | Model used for completion |
| `choices` | array | Array of completion choices |
| `usage` | object | Token usage statistics |
| `system_fingerprint` | string | System fingerprint for debugging |

#### Choice Object

```json
{
  "index": 0,
  "message": {
    "role": "assistant",
    "content": "Response text here",
    "tool_calls": []  // Optional
  },
  "finish_reason": "stop|length|tool_calls|content_filter",
  "logprobs": null  // Currently not supported
}
```

#### Usage Object

```json
{
  "prompt_tokens": 100,
  "completion_tokens": 50,
  "total_tokens": 150,
  "completion_tokens_details": {
    "reasoning_tokens": 20  // For reasoning models only
  }
}
```

## Responses API Parameters

Endpoint: `GET https://ark.cn-beijing.volces.com/api/v3/responses/{response_id}`

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `response_id` | string | Yes | ID of the response to retrieve | 

### Response Parameters

Similar to Chat API response but includes additional metadata for asynchronous responses.

## Files API Parameters

### Upload File

Endpoint: `POST https://ark.cn-beijing.volces.com/api/v3/files`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | File to upload (multipart/form-data) |
| `purpose` | string | Yes | File purpose ("fine-tune", "assistants", etc.) |

### List Files

Endpoint: `GET https://ark.cn-beijing.volces.com/api/v3/files`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `purpose` | string | No | Filter by purpose |
| `limit` | integer | No | Number of files to return (1-100) | 20 |
| `after` | string | No | Cursor for pagination |

## Common Parameter Details

### Temperature and Top-p

- **Temperature**: Controls randomness. Lower values make output more deterministic.
- **Top-p**: Controls diversity via nucleus sampling. Use either temperature or top-p, not both.

### Max Tokens

Maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length.

### Stop Sequences

Up to 4 sequences where the API will stop generating further tokens.

### Streaming

When enabled, the API returns Server-Sent Events (SSE) stream. Each chunk has the structure:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1694268190,
  "model": "doubao-seed-1-8-251228",
  "choices": [
    {
      "index": 0,
      "delta": {"content": "Hello"},
      "finish_reason": null
    }
  ]
}
```

## Examples

### Basic Chat Request

```json
{
  "model": "doubao-seed-2-0-pro-260215",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 500
}
```

### Streaming Request

```json
{
  "model": "doubao-seed-2-0-pro-260215",
  "messages": [{"role": "user", "content": "Tell me a story"}],
  "stream": true,
  "max_tokens": 1000
}
```

### Function Calling Request

```json
{
  "model": "doubao-seed-2-0-pro-260215",
  "messages": [{"role": "user", "content": "What's the weather in Beijing?"}],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
          },
          "required": ["location"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

### Multimodal Request

```json
{
  "model": "doubao-seed-2-0-pro-260215",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What's in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
          }
        }
      ]
    }
  ]
}
```

## Parameter Constraints

### Model-Specific Limits

| Model | Max Context | Max Output | Image Support | Streaming |
|-------|-------------|------------|---------------|-----------|
| Doubao Seed 2.0 Pro | 256,000 | 12,800 | Yes | Yes |
| Doubao Seed 2.0 Lite | 256,000 | 12,800 | Yes | Yes |
| GLM-4 7B | 200,000 | 8,192 | Yes | Yes |
| Kimi K2.5 | 256,000 | 32,768 | Yes | Yes |
| DeepSeek V3.2 | 128,000 | 8,192 | Yes | Yes |

### Rate Limits

- **RPM (Requests Per Minute)**: Varies by tier (Free: 100, Basic: 1000)
- **TPM (Tokens Per Minute)**: Model-specific limits
- **IPM (Images Per Minute)**: For multimodal requests

### File Upload Limits

- Maximum file size: 512MB
- Supported formats: `.jsonl`, `.txt`, `.pdf`, `.docx`, etc.
- Processing time: Varies by file size

## Error Handling

See [Error Codes Reference](../configuration.md#error-handling) for complete error handling information.

## Notes

1. **Parameter Compatibility**: Some parameters may not be supported by all models
2. **Default Values**: When not specified, API uses sensible defaults
3. **Region Variations**: Parameters may have different constraints in different regions
4. **Versioning**: API parameters may change with new API versions

---

*Based on Volcano Engine API Reference (2026-04-15)*  
*For the most up-to-date information, refer to official documentation.*