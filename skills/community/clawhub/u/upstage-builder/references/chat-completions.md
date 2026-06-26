<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Chat Completions API

## 1. Chat Completions API

Generate conversational responses using Solar LLM models.

### Endpoint

```
POST https://api.upstage.ai/v1/chat/completions
```

### Available Models

| Model Alias          | Currently Points To | Description                                                |
| -------------------- | ------------------- | ---------------------------------------------------------- |
| `solar-pro3`         | `solar-pro3-260126` | Latest flagship model (102B MoE, 12B active, 128K context) |
| `solar-pro2`         | `solar-pro2-251215` | Previous generation flagship (31B, 65K context)            |
| `solar-mini`         | `solar-mini-250422` | Lightweight, fast model (10.7B, 32K context)               |
| `syn-pro`            | `syn-pro-251021`    | Synthetic data optimized (no function calling)             |
| `solar-pro2-nightly` | -                   | Experimental nightly (not for production)                  |
| `solar-mini-nightly` | -                   | Experimental nightly (not for production)                  |

### Request Body (JSON)

| Parameter             | Type          | Required | Description                                                                                                                                                            |
| --------------------- | ------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model`               | string        | Yes      | Model name: `solar-pro3`, `solar-pro2`, `solar-mini`, or `syn-pro`                                                                                                     |
| `messages`            | array         | Yes      | Array of message objects with `role` and `content`                                                                                                                     |
| `max_tokens`          | integer       | No       | Maximum tokens to generate                                                                                                                                             |
| `temperature`         | float         | No       | Sampling temperature (0-2). Default: 0.8 for solar-pro3, 0.7 for other models                                                                                          |
| `top_p`               | float         | No       | Nucleus sampling (0-1). Default: 0.95 for solar-pro3, 1.0 for other models                                                                                             |
| `stream`              | boolean       | No       | Enable streaming. Default: false                                                                                                                                       |
| `frequency_penalty`   | float         | No       | Penalty for token frequency (-2 to 2). Default: 1.1                                                                                                                    |
| `presence_penalty`    | float         | No       | Penalty for token presence (-2 to 2). Default: 0.0                                                                                                                     |
| `reasoning_effort`    | string        | No       | Reasoning level: `minimal`, `low`, `medium`, `high`. Default: `minimal`. See notes below                                                                               |
| `tools`               | array         | No       | Function definitions for function calling (max 128 functions)                                                                                                          |
| `tool_choice`         | string/object | No       | Tool selection: `none`, `auto`, `required`, or specific function                                                                                                       |
| `parallel_tool_calls` | boolean       | No       | Enable parallel function calls (solar-pro3 only). Default: true                                                                                                        |
| `response_format`     | object        | No       | For structured outputs (all solar models: solar-pro3, solar-pro2, solar-mini, solar-pro2-nightly, solar-mini-nightly): `{"type": "json_schema", "json_schema": {...}}` |
| `prompt_cache_key`    | string        | No       | Unique key for prompt caching                                                                                                                                          |

### Reasoning Effort

#### Solar Pro 3

`solar-pro3` introduces a dynamic reasoning budget. The budget is dynamically adjusted based on the remaining context window.

| Value    | Reasoning | Ratio | Max Budget | Min Budget | Description                               |
| -------- | --------- | ----- | ---------- | ---------- | ----------------------------------------- |
| `high`   | ON        | 60%   | 32,768     | 8,192      | Maximum reasoning, best for complex tasks |
| `medium` | ON        | 30%   | 16,384     | 4,096      | Balanced reasoning (default)              |
| `low`    | OFF       | -     | -          | -          | No reasoning, fastest response            |

#### Solar Pro 2

For `solar-pro2` and `solar-pro2-nightly`, reasoning is disabled by default (`minimal`). To enable reasoning, set `reasoning_effort` to `high`.

| Value     | Reasoning | Description            |
| --------- | --------- | ---------------------- |
| `high`    | ON        | Enable reasoning       |
| `medium`  | ON        | Treated as `high`      |
| `low`     | OFF       | Treated as `minimal`   |
| `minimal` | OFF       | No reasoning (default) |

**Notes:**

- `solar-mini` and `syn-pro` do not support reasoning. The `reasoning_effort` parameter is ignored for these models.

**Reasoning Budget Calculation (solar-pro3):**

The reasoning budget limits how many tokens the model can consume for reasoning. It is dynamically adjusted:

```
budget = min(max_budget, max(min_budget, ratio * remaining_context))
remaining_context = context_length - input_tokens (or max_tokens if set)
```

### Message Object

**Standard Message:**

```json
{
  "role": "system" | "user" | "assistant",
  "content": "message text"
}
```

**Tool Response Message (for function calling):**

```json
{
  "tool_call_id": "call_abc123",
  "role": "tool",
  "name": "function_name",
  "content": "function_response_json_string"
}
```

When responding to a function call, you must include `tool_call_id` (matching the id from the model's tool_call) and `name` (the function name).

### Example Request

```bash
curl -X POST https://api.upstage.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "solar-pro3",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ],
    "max_tokens": 200,
    "temperature": 0.8
  }'
```

### Example Response (Non-streaming)

```json
{
  "id": "e1a90437-df41-45cd-acc6-a7bacbdd2a86",
  "object": "chat.completion",
  "created": 1723911735,
  "model": "solar-pro3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 8,
    "total_tokens": 33
  }
}
```

### Example Response (With Reasoning)

When `reasoning_effort` is set to `high` or `medium` for solar-pro3, the response includes a `reasoning` field showing the model's thought process:

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1747209370,
  "model": "solar-pro3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning": "The user wants to calculate 15% of 80.\n1. Convert 15% to decimal: 15/100 = 0.15\n2. Multiply: 0.15 × 80 = 12\nThe answer is 12.",
        "content": "15% of 80 is **12**."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 37,
    "completion_tokens": 133,
    "total_tokens": 170,
    "completion_tokens_details": {
      "reasoning_tokens": 45
    }
  }
}
```

**Reasoning Response Fields:**

- `message.reasoning`: The model's internal chain-of-thought reasoning (only present when reasoning is enabled)
- `completion_tokens_details.reasoning_tokens`: Number of tokens consumed by the reasoning process (included in `completion_tokens` total)

### Python Example

```python
import requests

response = requests.post(
    "https://api.upstage.ai/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "solar-pro3",
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }
)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

### OpenAI SDK Compatible

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

response = client.chat.completions.create(
    model="solar-pro3",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Parameter Tips

| Use Case                | Recommended Settings                            |
| ----------------------- | ----------------------------------------------- |
| Complex reasoning tasks | `reasoning_effort: "high"`, `temperature: 0.7`  |
| Fast simple responses   | `reasoning_effort: "low"`, `max_tokens: 200`    |
| Creative writing        | `temperature: 1.2`, `top_p: 0.95`               |
| Consistent outputs      | `temperature: 0.3`, `frequency_penalty: 1.5`    |
| Function calling        | `tools: [...]`, `tool_choice: "auto"`           |
| Structured JSON output  | `response_format: {"type": "json_schema", ...}` |
| Long conversations      | `prompt_cache_key: "unique_session_id"`         |

### Prompt Caching

Prompt caching allows you to reuse previously processed prompts, reducing latency and costs for repeated or similar requests.

**How it works:**

- Set a unique `prompt_cache_key` for each conversation session or context
- When the same key is used, the model can reuse cached prompt processing
- Best suited for multi-turn conversations or repeated prompts with the same prefix

**Best practices:**

- Use a consistent, unique key per user session (e.g., hashed user ID + session ID)
- Keep the cached portion (system prompt, context) at the beginning of messages
- Varying content should come after the cached prefix

### Function Calling

Function calling enables your model to interact with external services such as APIs, databases, or custom functions. The model generates function signatures in JSON format based on your tool definitions.

#### Tool Definition Schema

```json
{
  "type": "function",
  "function": {
    "name": "function_name",
    "description": "Description of what the function does",
    "parameters": {
      "type": "object",
      "properties": {
        "param1": {
          "type": "string",
          "description": "Parameter description"
        },
        "param2": {
          "type": "string",
          "enum": ["option1", "option2"]
        }
      },
      "required": ["param1"]
    }
  }
}
```

**Function Name Rules:**

- Allowed characters: `a-z`, `A-Z`, `0-9`, underscore (`_`), and hyphen (`-`)
- Maximum length: 64 characters
- Pattern: `^[a-zA-Z0-9_-]+$`

#### tool_choice Options

| Value                                                         | Description                                       |
| ------------------------------------------------------------- | ------------------------------------------------- |
| `"none"`                                                      | Model will not call any function                  |
| `"auto"`                                                      | Model decides whether to call functions (default) |
| `"required"`                                                  | Model must call at least one function             |
| `{"type": "function", "function": {"name": "function_name"}}` | Force specific function                           |

#### Parallel Tool Calls (solar-pro3 only)

When `parallel_tool_calls=True` (default), the model may return multiple tool calls in a single response for independent operations (e.g., fetching weather for multiple cities simultaneously).

#### Complete Function Calling Example

```python
from openai import OpenAI
import json

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

# Step 1: Define your function
def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    # In production, call actual weather API
    weather_data = {
        "seoul": {"temperature": "10", "condition": "cloudy"},
        "san francisco": {"temperature": "18", "condition": "sunny"},
        "paris": {"temperature": "15", "condition": "rainy"}
    }
    city = location.lower()
    if city in weather_data:
        return json.dumps({"location": location, **weather_data[city], "unit": unit})
    return json.dumps({"location": location, "temperature": "unknown"})

# Step 2: Define tools for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. Seoul, San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Step 3: Initial request
messages = [{"role": "user", "content": "What's the weather in Seoul and Paris?"}]

response = client.chat.completions.create(
    model="solar-pro3",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    parallel_tool_calls=True  # Enable parallel calls
)

# Step 4: Process tool calls
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

if tool_calls:
    messages.append(response_message)

    # Execute each function call
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Call the actual function
        function_response = get_current_weather(
            location=function_args.get("location"),
            unit=function_args.get("unit", "celsius")
        )

        # Append function result to messages
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response
        })

    # Step 5: Get final response with function results
    final_response = client.chat.completions.create(
        model="solar-pro3",
        messages=messages
    )
    print(final_response.choices[0].message.content)
```

#### Function Calling Response Structure

When the model decides to call functions, the response includes `tool_calls`:

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\": \"Seoul\", \"unit\": \"celsius\"}"
            }
          },
          {
            "id": "call_def456",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\": \"Paris\", \"unit\": \"celsius\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

### Structured Outputs

Generate JSON responses conforming to a specified schema using `response_format`.

#### Schema Requirements

- Supported types: `string`, `number`, `boolean`, `integer`, `object`, `array`
- All fields must be in the `required` array
- Maximum nesting depth: 3 levels
- `strict` must be `true`
- `additionalProperties` must be `false`
- Recursive schemas are not supported
- Definitions for subschemas (`$ref` to local definitions) are not supported

#### Structured Output Example

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

response = client.chat.completions.create(
    model="solar-pro3",
    messages=[
        {"role": "user", "content": "Extract menu items from: Coffee $5, Sandwich $8, Salad $7"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "menu_extraction",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "price": {"type": "number"}
                            },
                            "required": ["name", "price"],
                            "additionalProperties": False
                        }
                    },
                    "total_items": {"type": "integer"}
                },
                "required": ["items", "total_items"],
                "additionalProperties": False
            }
        }
    }
)

import json
result = json.loads(response.choices[0].message.content)
print(result)
# {"items": [{"name": "Coffee", "price": 5}, {"name": "Sandwich", "price": 8}, {"name": "Salad", "price": 7}], "total_items": 3}
```

### Streaming Response

When `stream=True`, the response is sent as Server-Sent Events (SSE).

#### Streaming Response Structure

Each chunk is a `chat.completion.chunk` object:

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion.chunk",
  "created": 1723911735,
  "model": "solar-pro3",
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": "Hello"
      },
      "finish_reason": null
    }
  ]
}
```

Key differences from non-streaming:

- Object type: `chat.completion.chunk` (not `chat.completion`)
- Uses `delta` instead of `message`
- `delta.content` contains incremental text
- Final chunk has `finish_reason: "stop"` and empty `delta`

#### Streaming Example

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

stream = client.chat.completions.create(
    model="solar-pro3",
    messages=[{"role": "user", "content": "Tell me a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

