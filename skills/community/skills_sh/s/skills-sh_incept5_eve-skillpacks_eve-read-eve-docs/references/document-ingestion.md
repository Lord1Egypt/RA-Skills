# Document Ingestion Pipeline

## Use When
- You need to wire end-to-end document processing: file upload through agent analysis to structured output.
- You need to configure the ingest agentpack or customize its processing behavior.
- You need to understand how media files (audio, video) are transcribed by agents.
- You need to understand how Slack file uploads reach agent workspaces.
- You need to connect ingestion to workflows, events, or org docs output.

## Load Next
- `references/ingest.md` for API endpoints, CLI flags, callback notifications, and CORS details.
- `references/events.md` for `system.doc.ingest` event payload and trigger syntax.
- `references/pipelines-workflows.md` for workflow trigger wiring.
- `references/jobs.md` for resource refs, hydration, and job lifecycle.
- `references/object-store-filesystem.md` for org bucket storage and presigned URL patterns.

## Ask If Missing
- Confirm the target project ID and whether a processing workflow is already configured.
- Confirm whether the input is CLI-driven, API-driven, or chat-driven (Slack file upload).
- Confirm whether media processing (audio/video transcription) is required.
- Confirm the desired output format and destination (org docs path, job result, callback).

## Pipeline Overview

Document ingestion is a composable flow: **file in -> event -> agent processes -> structured output**.

```
Input Channels              Platform Spine              Agent Processing
─────────────              ──────────────              ────────────────
eve ingest <file>    ─┐
POST /ingest API     ─┤    Ingest Record (audit)
Slack file upload    ─┘    Object Store (S3/MinIO)
                           system.doc.ingest event
                                    │
                           Workflow trigger match
                                    │
                           Job created ──── resource_refs: ingest://{id}
                                    │
                           Worker hydrates ingest:// into workspace
                                    │
                           Agent reads .eve/resources/
                           Processes file (text / PDF / audio / video)
                           Writes output (org docs, json-result)
```

Three input channels feed into a single processing spine. The agent receives files in a uniform workspace layout regardless of how the file arrived.

## Ingest Record Lifecycle

Each ingestion creates an immutable audit record (`ingest_xxx`).

**Statuses:** `pending` -> `processing` -> `done` | `failed`

- `pending`: Record created, presigned upload URL issued, waiting for file upload and confirm.
- `processing`: Upload confirmed, `system.doc.ingest` event emitted, workflow job running.
- `done`: Processing job completed successfully. `completed_at` set.
- `failed`: Processing job failed. `error_message` and `completed_at` set.

Confirm is idempotent -- calling it on a `processing` or `done` record returns current state without duplicate events or jobs.

## The `ingest://` URI Scheme

Ingest files are referenced via `ingest://` URIs in resource refs, alongside `org_docs://` and `job_attachments://`.

**Format:** `ingest:/{ingest_id}/{encoded_file_name}`

```json
{
  "uri": "ingest:/ingest_abc123/quarterly-report.pdf",
  "label": "Ingested document",
  "required": true,
  "mime_type": "application/pdf",
  "metadata": {
    "title": "Q4 Board Deck",
    "description": "Quarterly board presentation",
    "instructions": "Extract key financials and action items"
  }
}
```

The worker resolves `ingest://` URIs by downloading from object store key `ingest/{ingestId}/{fileName}` and writing to `.eve/resources/`. The resource index (`.eve/resources/index.json`) includes `mime_type` and `metadata` so agents know file types and submitter context without guessing from extensions.

## Workflow Trigger Wiring

Confirming an upload emits `system.doc.ingest`. Match it in a workflow trigger:

```yaml
workflows:
  process-document:
    trigger:
      system:
        event: doc.ingest
    steps:
      - agent:
          prompt: "Process the ingested document using your doc-processor skill."
```

The trigger matcher strips the `system.` prefix, so `system.doc.ingest` matches `event: doc.ingest`.

**Reliability**: doc.ingest workflow triggers fire reliably end-to-end. Pack
workflows are merged into the repo manifest before sync (no competing manifest
rows), `eve event emit --type doc.ingest --source system` auto-prefixes to the
canonical `system.doc.ingest` event type, and `eve workflow run --input` wraps
payloads correctly for the workflow invoke schema. If a doc.ingest event does
not match, `eve event show <event-id>` now shows the per-trigger evaluation
breakdown — see `events.md`.

The orchestrator interpolates event payload fields into workflow resource refs:

```yaml
resource_refs:
  - uri: "ingest://${event.payload.ingest_id}/${event.payload.file_name}"
    label: "Ingested document"
    required: true
```

## Ingest Agentpack

The `ingest-agentpack` provides a self-contained agent pack for document ingestion. Import it with a single `x-eve.packs` entry -- no boilerplate workflow or prompt authoring required.

### Pack Structure

```
ingest-agentpack/
├── eve/
│   ├── pack.yaml          # Pack manifest (id: doc-ingest)
│   ├── agents.yaml        # doc_processor agent definition
│   ├── workflows.yaml     # process-document workflow with doc.ingest trigger
│   └── x-eve.yaml         # Harness profiles (ingest, ingest-fast)
└── skills/
    └── doc-processor/
        └── SKILL.md        # Processing instructions for text, PDF, audio, video
```

### Import in Manifest

```yaml
x-eve:
  packs:
    - source: github:eve-horizon/ingest-agentpack
      ref: <40-char-sha>
```

Sync the pack into the project:

```bash
eve agents sync --project proj_xxx
```

This registers the `doc_processor` agent, the `process-document` workflow (with `doc.ingest` trigger), and harness profiles.

### Harness Profiles

| Profile | Harness | Model | Reasoning | Use Case |
|---------|---------|-------|-----------|----------|
| `ingest` | mclaude | opus-4.6 | medium | Quality-first (default) |
| `ingest-fast` | mclaude | sonnet-4.6 | low | Speed/cost optimization |

### Customize via Manifest Overlay

Override the agent's profile in the app manifest:

```yaml
x-eve:
  agents:
    doc_processor:
      harness_profile: ingest-fast
```

### Agent Behavior

The `doc_processor` agent:
1. Reads `.eve/resources/index.json` to find the ingested file, its MIME type, and submitter context.
2. Selects processing strategy based on MIME type (text, document, audio, video).
3. Runs tools if needed (whisper-cli for audio, ffmpeg + whisper-cli for video).
4. Writes structured analysis with summary, key facts, entities, and action items.
5. Emits a `json-result` block so output is retrievable via `eve job result`.

## Media Processing

Agent containers include `ffmpeg` and `whisper-cli` (whisper.cpp v1.8.1, CPU, `ggml-small.en` model) for audio and video transcription.

### Audio Files

Supported MIME types: `audio/mpeg`, `audio/wav`, `audio/mp4`, `audio/ogg`, `audio/flac`, `audio/opus`, `audio/aac`, `audio/amr`, `audio/x-ms-wma`.

Agent runs:
```bash
whisper-cli -m /opt/whisper/models/ggml-small.en.bin -f <file> -ovtt
```

Produces a `.vtt` transcript the agent reads and summarizes.

### Video Files

Supported MIME types: `video/mp4`, `video/x-matroska`, `video/quicktime`, `video/x-msvideo`, `video/webm`, `video/x-ms-wmv`, `video/x-flv`, `video/x-m4v`, `video/mpeg`, `video/3gpp`.

Agent runs:
```bash
ffmpeg -i <file> -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav
whisper-cli -m /opt/whisper/models/ggml-small.en.bin -f /tmp/audio.wav -ovtt
```

### PDF and Text

Claude reads PDFs natively via multimodal input -- no conversion tools needed. The `mime_type` field in the resource index tells the agent the file type. Text formats (markdown, JSON, YAML, CSV, HTML, XML) are read directly.

### Performance

| Input Duration | Approx. Transcription Time (CPU) |
|---------------|----------------------------------|
| 10 seconds | ~5 seconds |
| 1 minute | ~30 seconds |
| 10 minutes | ~5 minutes |
| 60 minutes | ~30 minutes |

Files over ~30 minutes may approach job timeouts. Use async polling (`eve ingest show`) rather than short `eve job wait` timeouts for long media.

### Tool Availability

Tools are installed in both `worker` and `agent-runtime` Docker images:
- **Worker**: `media` stage provides ffmpeg + whisper-cli; `full` and `production` stages inherit it.
- **Agent-runtime**: Tools installed in the `production` stage.
- **Model path**: `/opt/whisper/models/ggml-small.en.bin` (~150 MB, English-only).

If tools are unavailable, the agent reports what it can determine from the raw file and notes the limitation.

## Chat File Materialization

Slack file uploads are automatically downloaded, stored in Eve, and staged for agents. This bridges chat to the ingestion workspace pattern.

### Flow

```
Slack message + file attachment
       │
  Gateway (async phase)
  1. Download file via Slack bot token
  2. Upload to S3 via presigned URL
  3. Replace Slack URL with eve-storage:// ref
       │
  Routing (chat/route -> job)
  Files flow through in job metadata.files
       │
  Worker (workspace provisioning)
  4. Detect metadata.files with eve-storage:// URLs
  5. Download via presigned URL -> .eve/attachments/
  6. Write .eve/attachments/index.json
       │
  Agent reads .eve/attachments/index.json
```

### Agent Workspace Layout

Files land at `.eve/attachments/{file_id}-{sanitized_filename}` with an index at `.eve/attachments/index.json`:

```json
{
  "files": [
    {
      "id": "F019ABC123",
      "name": "product-spec-v2.pdf",
      "path": ".eve/attachments/F019ABC123-product-spec-v2.pdf",
      "mimetype": "application/pdf",
      "size": 245760,
      "source_provider": "slack"
    }
  ]
}
```

### Limits

| Limit | Value |
|-------|-------|
| Max files per message | 10 |
| Max file size | 50 MB |
| Max total per message | 100 MB |

Files exceeding limits are skipped (warning logged). The message text still routes normally.

### Distinction from Ingest Pipeline

Chat file materialization and the ingest pipeline are separate paths:
- **Chat files** arrive via Slack, land at `.eve/attachments/`, and the chat-routed agent sees them alongside the message.
- **Ingest files** arrive via `eve ingest` or the API, land at `.eve/resources/` via `ingest://` hydration, and a dedicated processing workflow handles them.

Both use presigned URLs and avoid proxying binary data through the API.

## CLI Quick Reference

```bash
# Upload and process a file
eve ingest <file> --project proj_xxx \
  [--title "..."] [--description "..."] \
  [--instructions "..."] [--tags t1,t2] \
  [--mime-type <type>] [--json]

# List ingest records
eve ingest list [--status pending|processing|done|failed] [--json]

# Show record with download URL
eve ingest show <ingest_id> [--json]
```

The CLI auto-infers MIME type from file extension (covers text, documents, images, audio, video formats). Override with `--mime-type` for edge cases. Source channel defaults to `cli`.

## Integration Points

| Primitive | Role in Ingestion |
|-----------|-------------------|
| **Object Store** | Presigned upload/download. Files stored at `ingest/{id}/{filename}` in org bucket. |
| **Events** | `system.doc.ingest` emitted on confirm. Carries full payload (file metadata, submitter context). |
| **Workflows** | Trigger on `doc.ingest` event. Create processing job with `ingest://` resource ref. |
| **Resource Hydration** | Worker resolves `ingest://` URIs, downloads from S3, writes to `.eve/resources/`. |
| **Resource Index** | `.eve/resources/index.json` includes `mime_type` and `metadata` from the ingest event. |
| **Org Docs** | Agent writes structured output via `eve docs write`. |
| **Job Result** | Agent emits `json-result` block. Retrieve via `eve job result <job-id>`. |
| **Callbacks** | Optional `callback_url` on ingest record. Platform POSTs status on completion. |

## Key Constraints

- **API never proxies binary data.** All file transfer uses presigned S3 URLs.
- **Ingest records are mostly immutable.** Only lifecycle fields (`status`, `event_id`, `job_id`, `error_message`, `completed_at`) update after creation.
- **Max file size: 500 MB** for ingest API uploads.
- **Whisper model: English-only** (`ggml-small.en`). Multilingual support requires swapping the model file.
- **Single agent per ingest job.** Multi-agent triage routing is not yet implemented.
- **Confirm is idempotent.** Repeated confirm calls return current state without duplicate events.
