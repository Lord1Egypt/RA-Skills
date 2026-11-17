---
name: wiro-n8n
description: Generate video, images, speech, music, 3D and LLM output with Wiro AI inside n8n workflows through the Wiro AI community node @wiro-ai/n8n-nodes-wiro, including install, the Wiro AI API credential, picking a model and its inputs, task outputs, errors and cost control. Use when the user builds an n8n workflow or automation with Wiro, asks about the Wiro AI node or @wiro-ai/n8n-nodes-wiro, or wants media or LLM output generated in n8n.
---

# Wiro AI in n8n

The npm package `@wiro-ai/n8n-nodes-wiro` adds one n8n node, **Wiro AI**, that runs any model in the Wiro AI catalog. Pick a model and its inputs load into the node with their defaults. A run starts a task on Wiro, waits for it to finish and returns the output files, or the reply of a text model. The node can also be used as a tool by an n8n AI Agent.

## When to use

- The user builds or edits an n8n workflow that generates video, images, speech, music or 3D models, or chats with an LLM, through Wiro.
- The user wants to install or set up the Wiro AI node, or a Wiro AI node stopped with an error.
- For Wiro calls from code or from an agent outside n8n, use the `wiro-ai` skill (see the end).

## Install

On self-hosted n8n, as an Owner or Admin:

1. Go to **Settings > Community Nodes** and select **Install**.
2. Enter `@wiro-ai/n8n-nodes-wiro`, accept the risk notice and select **Install**.

For a manual install (for example inside a Docker container), run this in `~/.n8n/nodes`, then restart n8n:

```bash
npm install @wiro-ai/n8n-nodes-wiro
```

Other install methods: https://docs.n8n.io/integrations/community-nodes/installation/

Requirements: n8n 1.85.0 or later.

## Credentials

1. The user creates a project at https://wiro.ai/panel/project/new.
2. In n8n they open **Credentials > Add new > Wiro AI API** and fill in:

| Field | What to enter |
| --- | --- |
| API Key | The project's API key |
| API Secret | The project's API secret, only when the project uses signature authentication. Leave it empty otherwise |

With a secret, the node signs every request with HMAC-SHA256, so the secret itself is not sent. n8n tests the key when the credential is saved. See https://wiro.ai/docs/authentication.

Keys stay in the n8n credential:

- The user types the key and secret into the credential form. Never ask for them in chat.
- Never put a key or secret in node fields, expressions, Code nodes, workflow JSON or exported files. An exported workflow refers to its credential by ID and name only.

## How the node runs

| Resource | Operation | What it does |
| --- | --- | --- |
| Model | Run | Runs a model with the inputs and returns its outputs |
| Task | Get | Reads a task by its ID, with its status and outputs |
| Task | Wait | Waits until a task finishes, then returns its outputs |

- **Model:** pick it from the searchable list, paste its wiro.ai link (`https://wiro.ai/models/pruna/p-image`) or enter it as `owner/model` (`pruna/p-image`). Browse models at https://wiro.ai/models.
- **Inputs:** the inputs of the chosen model load with their defaults. Required inputs are always shown; advanced ones start hidden and are added with **Add input to send**. Inputs left out use the model's defaults.
- Files go in as URLs. Pass public URLs, or map one from an earlier node, for example `{{ $json.url }}`. An input that takes several files says so in its name; separate the URLs with commas.
- **Wait for Completion** is on by default: the node waits for the task and returns its outputs. Turned off, the node returns `taskId` at once; read the task later with **Task > Get** or **Task > Wait**.
- **Max Wait Time (Minutes)** is 20 by default, up to 120. A task still running after it comes back with `status: "running"`.
- The node runs once for each incoming item and links each result to its item, so ten items start ten paid tasks. Put a Limit node in front of it when you only want one run.

Output fields:

| Field | What it holds |
| --- | --- |
| `taskId` | The ID of the Wiro task |
| `status` | `queued`, `running`, `completed`, `failed` or `cancelled` |
| `model` | The model, as `owner/model` |
| `url` | The first output file |
| `urls` | Every output file |
| `text` | The reply of a text model |
| `costUsd` | What the task cost, in US dollars |
| `elapsedSeconds` | How long the task ran |

Run a new model once and look at its output before you map fields downstream.

## Workflow sketch: prompt to image

1. **Trigger:** a Manual Trigger while testing; later a Schedule Trigger, Form Trigger or Webhook.
2. **Wiro AI node, Model > Run:** model `openai/gpt-5-mini`, input **Prompt** asking for one image prompt. Its reply is in `text`.
3. **Wiro AI node, Model > Run:** model `pruna/p-image`, input **Prompt** mapped to `{{ $json.text }}`, **Aspect Ratio** `16:9`. Tell the user the expected cost before the first run.
4. **Next step:** `{{ $json.url }}` is the image link. Post it with a Slack or email node, or fetch the file with an HTTP Request node (response format File) and upload it to storage.

When you write workflow JSON (for example through the n8n API), the node type is `@wiro-ai/n8n-nodes-wiro.wiro` with `typeVersion` 1. The model is a resource locator, and the inputs go under `inputs.value`, keyed by the model's input IDs:

```json
{
  "name": "Create the image",
  "type": "@wiro-ai/n8n-nodes-wiro.wiro",
  "typeVersion": 1,
  "position": [520, 0],
  "parameters": {
    "resource": "model",
    "operation": "run",
    "model": { "__rl": true, "mode": "id", "value": "pruna/p-image" },
    "inputs": {
      "mappingMode": "defineBelow",
      "value": { "prompt": "={{ $json.text }}", "aspectRatio": "16:9" },
      "matchingColumns": [],
      "schema": []
    }
  },
  "credentials": { "wiroAiApi": { "id": "YOUR_CREDENTIAL_ID", "name": "YOUR_CREDENTIAL_NAME" } }
}
```

The keys of `inputs.value` are the model's input IDs, the `id` of each parameter that `POST /Tool/Detail` returns (see https://wiro.ai/docs/model-parameters). The node shows them as labels; to see the IDs, set the node up once in the editor and copy it as JSON.

## Errors and retries

- A task that fails or is cancelled stops the node with an n8n error that says what happened. To handle it in its own branch, set the node's **On Error** setting to **Continue (using error output)**.
- Do not turn on **Retry On Fail** for Model > Run: every retry starts a new paid task.
- A task still running after **Max Wait Time** is not an error: it comes back with `status: "running"`. Read it with **Task > Wait** and the same `taskId`; never run Model > Run again to retry it.
- Messages such as "This model needs a file" or "This model is not available" come from Wiro before a task starts. Fix the input or the model and run the node again.

## Money rules

- Each run is billed to the wallet of the project's workspace, including test runs in the editor.
- Before you run a Wiro AI node, or turn on a workflow that runs one, tell the user the model, the settings and the expected cost per run (https://wiro.ai/product/pricing). The `costUsd` field shows what a finished task cost.
- Count the runs a workflow can make. Loop Over Items, a sub-workflow run once per item, an AI Agent calling the node as a tool, a Schedule Trigger and a public Webhook or form all add paid runs. Say how many and what they cost, cap the list (for example with a Limit node), and ask before large batches.
- While building, pin the node's output after one good run, so later test runs reuse it instead of starting new tasks.
- After an error, a timeout or a stopped execution, never run the same paid step again on your own: the task may still be running, and a second run bills a second job. Look the task up by its `taskId` with Task > Get first.
- Stopping an n8n execution does not stop the Wiro task.

## More

- REST API and MCP server for any Wiro model, from code or an agent: `npx skills add wiroai/Wiro-Plugin --skill wiro-ai`
- n8n integration docs: https://wiro.ai/docs/n8n-wiro-integration
- Model catalog: https://wiro.ai/models
- Pricing: https://wiro.ai/product/pricing
- Package: https://www.npmjs.com/package/@wiro-ai/n8n-nodes-wiro
- Source: https://github.com/wiroai/n8n-nodes-wiro
