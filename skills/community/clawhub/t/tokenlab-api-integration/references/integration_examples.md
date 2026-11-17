# TokenLab integration examples

These are shape examples, not model-availability truth. Discover a live model and read its detail contract before every non-chat integration or before binding a long-lived agent route.

## Environment

```bash
export TOKENLAB_API_KEY='sk-...'
export TOKENLAB_API_BASE='https://api.tokenlab.sh'
```

Never paste the real key into source, browser code, logs, screenshots, or query strings unless an official SDK protocol specifically requires a query key and the request stays server-side.

## Shared JavaScript client

The JavaScript examples below reuse this client. Errors retain HTTP status, request ID and retry timing; callers decide whether a read can be retried. A failed or timed-out create must not be submitted again automatically.

```javascript
const apiBase = process.env.TOKENLAB_API_BASE ?? 'https://api.tokenlab.sh';
const apiKey = process.env.TOKENLAB_API_KEY;
const controller = new AbortController();

function retryAfterSeconds(value) {
  if (typeof value !== 'number' && typeof value !== 'string') return undefined;
  if (typeof value === 'string' && value.trim() === '') return undefined;
  const seconds = Number(value);
  if (Number.isFinite(seconds) && seconds >= 0) return seconds;
  if (typeof value !== 'string' || /^-?\d/.test(value)) return undefined;
  const date = Date.parse(value);
  return Number.isFinite(date) ? Math.max(0, Math.ceil((date - Date.now()) / 1000)) : undefined;
}

async function tokenlabRequest(path, init = {}, signal) {
  const url = new URL(path, `${apiBase}/`);
  if (url.origin !== new URL(apiBase).origin || url.username || url.password) {
    throw new Error('TokenLab requests and poll URLs must stay on the configured API origin');
  }
  const response = await fetch(url, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
      ...(init.body ? { 'Content-Type': 'application/json' } : {}),
      ...init.headers,
    },
    signal,
  });
  const text = await response.text();
  let body;
  let parseError;
  try {
    body = text ? JSON.parse(text) : null;
  } catch (cause) {
    parseError = cause;
  }
  if (!response.ok || parseError) {
    const error = new Error(body?.error?.message ?? `TokenLab HTTP ${response.status}${parseError ? ' (non-JSON response)' : ''}`, { cause: parseError });
    error.status = response.status;
    error.code = body?.error?.code;
    error.retryable = body?.error?.retryable ?? body?.retryable ??
      ([408, 425, 429].includes(response.status) || response.status >= 500);
    error.retryAfterHeader = response.headers.get('retry-after');
    error.retryAfter = retryAfterSeconds(error.retryAfterHeader) ??
      retryAfterSeconds(body?.error?.retry_after ?? body?.retry_after);
    error.requestId = response.headers.get('x-request-id') ?? body?.error?.request_id ?? body?.request_id;
    error.details = body ?? text.slice(0, 4000);
    throw error;
  }
  return body;
}
```

## Discover and inspect a model

### JavaScript

Use the shared client above. Media operation details are separate from chat protocol eligibility.

```javascript
const listing = await tokenlabRequest('/v1/models?category=video', {}, controller.signal);
const selected = listing.data[0];
if (!selected) throw new Error('No public video model is currently available');
const detail = await tokenlabRequest(`/v1/models/${encodeURIComponent(selected.id)}`, {}, controller.signal);
console.log(detail.id, detail.tokenlab?.accepted_request_formats,
  detail.tokenlab?.request_format_details ?? detail.tokenlab?.public_contract);
```

### Python

```python
import os
import requests

API_BASE = os.getenv("TOKENLAB_API_BASE", "https://api.tokenlab.sh")
API_KEY = os.getenv("TOKENLAB_API_KEY")
HEADERS = {"Accept": "application/json"}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"

listing = requests.get(
    f"{API_BASE}/v1/models",
    params={"category": "image"},
    headers=HEADERS,
    timeout=30,
)
listing.raise_for_status()
models = listing.json()["data"]
if not models:
    raise RuntimeError("No public image model is currently available")

model_id = models[0]["id"]
detail = requests.get(
    f"{API_BASE}/v1/models/{model_id}",
    headers=HEADERS,
    timeout=30,
)
detail.raise_for_status()
extension = detail.json()["tokenlab"]
print(extension.get("request_format_details") or extension.get("public_contract"))
```

## Native protocol examples

### OpenAI Responses

Use only when the detail contract contains `openai_responses`.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["TOKENLAB_API_KEY"],
    base_url="https://api.tokenlab.sh/v1",
    timeout=120.0,
)

response = client.responses.create(
    model="<model-id-from-live-detail>",
    input="Explain this repository in three bullets.",
)
print(response.output_text)
```

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.TOKENLAB_API_KEY,
  baseURL: 'https://api.tokenlab.sh/v1',
  timeout: 120_000,
});

const response = await client.responses.create({
  model: '<model-id-from-live-detail>',
  input: 'Explain this repository in three bullets.',
});
console.log(response.output_text);
```

### Anthropic Messages

Use only when the detail contract contains `anthropic_messages`. The SDK base URL has no `/v1` suffix.

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["TOKENLAB_API_KEY"],
    base_url="https://api.tokenlab.sh",
    timeout=120.0,
)

message = client.messages.create(
    model="<model-id-from-live-detail>",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
print("".join(block.text for block in message.content if block.type == "text"))
```

### Gemini `generateContent`

Use only when the detail contract contains `gemini_generate_content`. Keep native `contents`, `parts`, tools, files, and cached-content fields on this route.

```bash
curl --fail-with-body \
  -X POST 'https://api.tokenlab.sh/v1beta/models/<model-id>:generateContent' \
  -H "Authorization: Bearer $TOKENLAB_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{
      "role": "user",
      "parts": [{"text": "Explain this image"}]
    }]
  }'
```

### OpenAI Chat Completions compatibility

```javascript
const completion = await client.chat.completions.create({
  model: '<model-id-whose-detail-declares-openai_chat_completions>',
  messages: [{ role: 'user', content: 'Hello' }],
});
console.log(completion.choices[0]?.message?.content);
```

## Poll raw HTTP tasks

Reuse the shared client above. Pass the raw create response so its returned `poll_url` is preserved; a task ID alone also works for the generic task endpoint. A terminal `failed` response is a finished failure, and a wait timeout retains the latest state for another poll.

```javascript
const TERMINAL = new Set(['completed', 'failed', 'succeeded', 'cancelled', 'canceled', 'expired']);

function abortableDelay(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal.aborted) return reject(signal.reason);
    const finish = () => {
      signal.removeEventListener('abort', abort);
      resolve();
    };
    const timer = setTimeout(finish, ms);
    const abort = () => {
      clearTimeout(timer);
      signal.removeEventListener('abort', abort);
      reject(signal.reason);
    };
    signal.addEventListener('abort', abort, { once: true });
  });
}

async function waitForTokenLabTask(task, {
  signal,
  timeoutMs = 15 * 60_000,
  pollIntervalMs = 5_000,
} = {}) {
  const submitted = typeof task === 'string' ? { id: task } : task;
  const id = submitted?.task_id ?? submitted?.id;
  const pollUrl = submitted?.poll_url ??
    (typeof id === 'string' && id ? `/v1/tasks/${encodeURIComponent(id)}` : undefined);
  const timeout = AbortSignal.timeout(timeoutMs);
  const combined = signal ? AbortSignal.any([signal, timeout]) : timeout;
  let latest = submitted;
  try {
    combined.throwIfAborted();
    if (TERMINAL.has(String(latest?.status ?? '').toLowerCase())) return latest;
    if (typeof pollUrl !== 'string' || !pollUrl) throw new Error('Async response has no poll URL or task id');
    while (true) {
      latest = await tokenlabRequest(pollUrl, { method: 'GET' }, combined);
      const status = String(latest.status ?? '').toLowerCase();
      if (!status) throw new Error('Task response has no status');
      if (TERMINAL.has(status)) return latest;
      await abortableDelay(pollIntervalMs, combined);
    }
  } catch (error) {
    if (timeout.aborted && !signal?.aborted) {
      return { timed_out: true, terminal: false, latest };
    }
    throw error;
  }
}
```

## Multimedia: handle sync and async image delivery

Raw HTTP image results have top-level task fields when asynchronous. The `delivery` object belongs to MCP tool results, not the raw HTTP response. Use the client and polling helper above together with this example.

```javascript
const created = await tokenlabRequest('/v1/images/generations', {
  method: 'POST',
  body: JSON.stringify({
    model: '<live-image-model-id>',
    prompt: 'A paper-cut mountain landscape at dawn',
  }),
}, controller.signal);

if (created.task_id || created.poll_url || created.status) {
  const result = await waitForTokenLabTask(created, { signal: controller.signal });
  console.log(result);
} else {
  console.log(created);
}
```

## Async submit and wait

Video, music, and 3D create endpoints are asynchronous. Replace only the endpoint and request fields defined by the chosen model detail/OpenAPI. Keep the returned poll URL when passing the response to the helper.

```javascript
const submitted = await tokenlabRequest('/v1/videos/generations', {
  method: 'POST',
  body: JSON.stringify({
    model: '<live-video-model-id>',
    prompt: 'A slow tracking shot through a glass greenhouse after rain',
  }),
}, controller.signal);

const result = await waitForTokenLabTask(submitted, { signal: controller.signal });
console.log(result);
```

Python polling with an overall deadline:

```python
import os
import time
import requests
from urllib.parse import quote, urljoin, urlsplit

API_BASE = os.getenv("TOKENLAB_API_BASE", "https://api.tokenlab.sh")
HEADERS = {
    "Authorization": f"Bearer {os.environ['TOKENLAB_API_KEY']}",
    "Content-Type": "application/json",
}
TERMINAL = {"completed", "failed", "succeeded", "cancelled", "canceled", "expired"}

def wait_for_task(task: dict | str, timeout_seconds: float = 900, interval_seconds: float = 5):
    submitted = {"id": task} if isinstance(task, str) else task
    latest = submitted
    if str(latest.get("status", "")).lower() in TERMINAL:
        return latest
    task_id = submitted.get("task_id") or submitted.get("id")
    poll_url = submitted.get("poll_url") or (
        f"/v1/tasks/{quote(task_id, safe='')}" if isinstance(task_id, str) and task_id else None
    )
    if not poll_url:
        raise ValueError("Async response has no poll URL or task id")
    url = urljoin(f"{API_BASE}/", poll_url)
    base, target = urlsplit(API_BASE), urlsplit(url)
    base_port = base.port or (443 if base.scheme == "https" else 80)
    target_port = target.port or (443 if target.scheme == "https" else 80)
    if (target.scheme, target.hostname, target_port) != (base.scheme, base.hostname, base_port) or target.username or target.password:
        raise ValueError("Poll URL must stay on the configured API origin")
    deadline = time.monotonic() + timeout_seconds
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return {"timed_out": True, "terminal": False, "latest": latest}
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=min(30, remaining),
        )
        response.raise_for_status()
        latest = response.json()
        status = str(latest.get("status", "")).lower()
        if not status:
            raise RuntimeError("Task response has no status")
        if status in TERMINAL:
            return latest
        time.sleep(min(interval_seconds, max(0, deadline - time.monotonic())))
```

## Multipart audio and files

```python
with open("audio.wav", "rb") as audio:
    response = requests.post(
        f"{API_BASE}/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {os.environ['TOKENLAB_API_KEY']}"},
        data={"model": "<live-stt-model-id>"},
        files={"file": ("audio.wav", audio, "audio/wav")},
        timeout=120,
    )
response.raise_for_status()
print(response.json()["text"])
```

Validate the local path, MIME type, and byte size before opening a model-selected file. Do not let untrusted model output choose arbitrary host paths.

## Go base client

```go
client := &http.Client{Timeout: 120 * time.Second}
req, err := http.NewRequestWithContext(ctx, http.MethodGet,
    "https://api.tokenlab.sh/v1/models?category=embedding", nil)
if err != nil { return err }
req.Header.Set("Authorization", "Bearer "+os.Getenv("TOKENLAB_API_KEY"))
req.Header.Set("Accept", "application/json")
resp, err := client.Do(req)
if err != nil { return err }
defer resp.Body.Close()
```

Always use `NewRequestWithContext` so caller cancellation propagates.

## PHP base request

```php
<?php
$ch = curl_init('https://api.tokenlab.sh/v1/models?category=rerank');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTPHEADER => [
        'Accept: application/json',
        'Authorization: Bearer ' . getenv('TOKENLAB_API_KEY'),
    ],
]);
$body = curl_exec($ch);
if ($body === false) {
    throw new RuntimeException(curl_error($ch));
}
$status = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);
if ($status < 200 || $status >= 300) {
    throw new RuntimeException("TokenLab HTTP $status: $body");
}
$models = json_decode($body, true, flags: JSON_THROW_ON_ERROR);
```

## Structured error recovery

Do not implement an unbounded catch-and-retry loop. A safe policy is:

```text
401/403          -> stop; fix credential or permission
400 invalid      -> fix only fields named by the current public contract
404 model/task   -> rediscover or verify ownership; do not retry blindly
402 balance      -> stop or ask before selecting a cheaper model
429              -> bounded retry using Retry-After
5xx retryable    -> bounded same-request retry; preserve payload semantics
model_not_found  -> use explicit did_you_mean/suggestions or rediscover
```

Success means the requested semantic result was delivered: text/tool calls preserved for LLM endpoints, a valid media result or terminal task for generation, an embedding vector with the expected dimension, or a transcript for STT. HTTP 200 alone is not sufficient when the client silently changed the request or returned a nonterminal task.

## System One decisions

Discover `/v1/models?category=decision` and inspect the selected model first. This example uses `jev-1.13` only when its current contract declares `/v1/systemone`. Reuse the shared JavaScript client above.

```javascript
const decision = await tokenlabRequest('/v1/systemone', {
  method: 'POST',
  body: JSON.stringify({
    model: 'jev-1.13',
    state: { ticket: 'I was charged twice. Please refund the duplicate payment.' },
    questions: {
      refund_requested: { type: 'noul', instructions: 'Is a refund explicitly requested?' },
      department: {
        type: 'choice', instructions: 'Which team should handle the ticket?',
        criteria: { billing: 'Charges and refunds', technical: 'Software issues', other: 'Neither category fits' },
      },
      urgency: {
        type: 'score', instructions: 'How urgent is the ticket?',
        criteria: ['Routine enquiry', 'Money affected', 'Immediate safety emergency'],
      },
    },
  }),
}, controller.signal);
console.log(decision.answers, decision.usage);
```

The result is synchronous JSON. Noul is a probability; Choice is a category; Score is a position on ordered levels and may be fractional. Read any returned probabilities and confidence alongside the result. Missing confidence does not mean certainty. A refund request is not refund eligibility or authorization; keep action permissions, exact arithmetic, thresholds, and escalation in application code. No Chat, streaming, or Batch fields belong in this request.
