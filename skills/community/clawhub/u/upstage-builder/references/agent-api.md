<!-- Source: https://console.upstage.ai/api/docs/for-agents/raw -->
# Agent API

## 9. Agent API

Agents are reusable, multi-step workflows (e.g., Parse, Classify, Extract) designed to run complex document processing tasks. Create and configure Agents in [Upstage Studio](https://studio.upstage.ai), then execute them via the API.

> **Prerequisite:** Agent API requires creating and configuring an Agent in [Upstage Studio](https://studio.upstage.ai) before making API calls. There is no API for agent creation — the Studio UI is mandatory. Create your agent workflow (e.g., Parse → Classify → Extract), save it, and copy the Agent ID from the Code panel.

**Base URL:** `https://api.upstage.ai/v2` (Note: Agents use v2, not v1)

The Agent API follows the [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses) format and is compatible with the OpenAI SDK.

### 9.1 Files API (Agent)

Upload, list, retrieve, and delete files used by Agents.

#### Upload File

```
POST https://api.upstage.ai/v2/files
```

**Request Body (multipart/form-data):**

| Parameter | Type   | Required | Description                        |
| --------- | ------ | -------- | ---------------------------------- |
| `file`    | file   | Yes      | The document file to upload        |
| `purpose` | string | No       | File purpose. Default: `user_data` |

**curl:**

```bash
curl -X POST https://api.upstage.ai/v2/files \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf" \
  -F "purpose=user_data"
```

**Python (OpenAI SDK):**

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v2"
)

with open("document.pdf", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="user_data"
    )

print(file.model_dump())
```

**Response:**

```json
{
  "id": "file-abc123",
  "object": "file",
  "bytes": 17408,
  "created_at": 1756368389,
  "expires_at": null,
  "filename": "document.pdf",
  "purpose": "user_data"
}
```

#### Retrieve File

```
GET https://api.upstage.ai/v2/files/{file_id}
```

#### List Files

```
GET https://api.upstage.ai/v2/files
```

#### Delete File

```
DELETE https://api.upstage.ai/v2/files/{file_id}
```

### 9.2 Jobs API (Agent)

Execute Agents and retrieve results.

#### Create Job

```
POST https://api.upstage.ai/v2/responses
```

**Request Body (JSON):**

| Parameter | Type   | Required | Description                                                               |
| --------- | ------ | -------- | ------------------------------------------------------------------------- |
| `model`   | string | Yes      | Agent ID (e.g., `agt_BxcRatEWzVYH2yRNtyWynn`). Obtain from Upstage Studio |
| `input`   | array  | Yes      | Array of input messages with file references                              |
| `include` | array  | No       | Output scope: `["last"]` for final step only, `["all"]` for all steps     |

**Input Message Format:**

```json
{
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_file",
          "file_id": "file-abc123"
        }
      ]
    }
  ]
}
```

**curl:**

```bash
curl -X POST https://api.upstage.ai/v2/responses \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agt_BxcRatEWzVYH2yRNtyWynn",
    "include": ["last"],
    "input": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_file",
            "file_id": "file-abc123"
          }
        ]
      }
    ]
  }'
```

**Python (OpenAI SDK):**

```python
from openai import OpenAI
from time import sleep
import json

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.upstage.ai/v2"
)

# Upload file
with open("document.pdf", "rb") as f:
    file = client.files.create(file=f, purpose="user_data")

# Create a job
resp = client.responses.create(
    model="agt_BxcRatEWzVYH2yRNtyWynn",
    include=["last"],
    input=[
        {
            "role": "user",
            "content": [{"type": "input_file", "file_id": file.id}]
        }
    ],
)

# Poll until the job completes
while resp.status in {"queued", "in_progress"}:
    sleep(2)
    resp = client.responses.retrieve(resp.id, include=["last"])

# Read the final output
if resp.status == "completed":
    print(json.loads(resp.output_text))
```

#### Retrieve Job

```
GET https://api.upstage.ai/v2/responses/{job_id}
```

| Query Parameter | Type  | Description                                                      |
| --------------- | ----- | ---------------------------------------------------------------- |
| `include[]`     | array | `last` (default) for final step only, `all` for all step results |

**curl:**

```bash
curl https://api.upstage.ai/v2/responses/{JOB_ID}?include[]=last \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Python:**

```python
response = client.responses.retrieve(
    job_id,
    include=["all"]
)
print(response.model_dump())
```

#### Job Response Format

```json
{
  "id": "job_7yMqwGy3rfh6Pwo7MdseMo",
  "object": "response",
  "created_at": 1767613535,
  "status": "completed",
  "model": "agt_BxcRatEWzVYH2yRNtyWynn",
  "output": [
    {
      "id": "fb543069-1a45-4fde-94de-2383995d7339",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "model": "step_2_extract",
      "content": [
        {
          "type": "output_text",
          "text": "{\"key\": \"value\"}",
          "annotations": [],
          "additional_values": "{...}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "total_tokens": 0
  }
}
```

**Response Fields:**

| Field                                  | Type   | Description                                                                               |
| -------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| `id`                                   | string | Job ID                                                                                    |
| `status`                               | string | `queued`, `in_progress`, `completed`, or `failed`                                         |
| `output`                               | array  | Array of step results (filtered by `include` parameter)                                   |
| `output[].model`                       | string | Step name (e.g., `step_1_parse`, `step_2_extract`)                                        |
| `output[].content[].text`              | string | Main result text (matches the corresponding standalone API)                               |
| `output[].content[].additional_values` | string | Stringified JSON with extra data (e.g., confidence, locations). Parse with `json.loads()` |

#### Accessing Results via `output_text`

For quick access to the final result, use `include=["last"]` and read `response.output_text`:

```python
response = client.responses.retrieve(job_id, include=["last"])
print(response.output_text)
```

---

