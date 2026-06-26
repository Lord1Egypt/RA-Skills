---
name: yino-ai
description: >
  Generate images and videos using yino.ai.
  Use when user wants to generate images (Seedream), generate videos (Veo),
  or any media generation task.
triggers:
  - generate image
  - generate video
  - text to image
  - image to video
  - yino
  - seedream
  - veo
tools:
  - bash
  - http
requires:
  env:
    - YINO_API_KEY
---

# yino.ai Media API

## How to Call

Use whatever HTTP tool you have — curl, Python requests, Node fetch, or built-in HTTP.
These APIs are designed for agents: errors include explanations and doc links, and batch mode reduces round trips.

## Preflight

1. `echo $YINO_API_KEY` — must be set. Get one at https://yino.ai/settings (API Keys section).
2. `echo ${YINO_API_BASE_URL:-https://yino.ai}` — defaults to production. Set `YINO_API_BASE_URL=http://localhost:3000` for local dev.

If either fails, stop and tell the user.

## Auth

Every request needs: `Authorization: Bearer $YINO_API_KEY`

## Step 1: Discover Capabilities

**Always start here.** Don't assume model names or parameters — discover them:

```bash
curl "${YINO_API_BASE_URL:-https://yino.ai}/api/agent/capabilities" \
  -H "Authorization: Bearer $YINO_API_KEY"
```

This returns all available models and tools with their endpoints, tags, and doc links. Models change over time — always discover first.

Each capability includes a `doc` field (e.g. `/docs/models/seedream-4-5.mdx`). **Fetch the doc to learn input parameters before calling any endpoint:**

```bash
curl "${YINO_API_BASE_URL:-https://yino.ai}{doc_field_value}"
```

**Doc URL convention:** Any URL ending in `.mdx` returns raw Markdown — the same content humans see on the website, but readable by you directly. Each doc starts with a breadcrumb (e.g. `> [docs](/docs) / [models](/docs/models) / seedream-4-5`) with links you can follow to navigate to parent pages or sibling docs.

## Step 2: Key Patterns

**Projects:** A project groups related generations and enables visual preview pages. Use projects in two situations:

1. **Upfront** — the user's task clearly involves multiple related generations (storyboard, style exploration, multi-shot video). Suggest: "Would you like me to create a project so you can preview all the results together?"
2. **Retroactive** — you've already generated several related items without a project. Suggest: "I've generated a few related pieces — want me to organize them into a project?" Then create a project and use `PATCH /api/agent/generations/:id` with `project_id` to assign existing generations to it.

After creating a project, immediately share the project link with the user: `${YINO_API_BASE_URL}/projects/{project_id}` — they can open it to watch progress and browse results as you generate.

Read `references/project-preview.md` for project workflow, preview block types, incremental update strategies, and examples.

**Async + Polling:** Model endpoints return `task_id`(s), not results. Poll with `sleep` + exponential backoff to balance between polling too frequently and waiting too long.

```bash
curl "${YINO_API_BASE_URL}/api/agent/generations/status?ids=id1,id2" \
  -H "Authorization: Bearer $YINO_API_KEY"
```

Each generation has `status` (pending → processing → done / failed) and `output.url` when done.

**Polling tips:**
- Poll manually one call at a time. Use `sleep` between polls with exponential backoff — do NOT write automated loop scripts, they block your execution environment and prevent you from doing useful work in between.
- While waiting, do useful work: if you have multiple batches in flight, check another batch, update the project preview with results that are already done, or inform the user of progress.
- Tell the user the current status between polls.

**Batch mode:** When you have multiple items, always use batch. One request with 10 items beats 10 separate requests. Wrap inputs in `{"items": [...]}` (up to 20).

**File upload:** When you need to provide a file (image, audio), upload it first:

```bash
curl -X POST "${YINO_API_BASE_URL}/api/agent/upload" \
  -H "Authorization: Bearer $YINO_API_KEY" \
  -F "file=@path/to/file"
```

Returns a URL you can pass to other endpoints. Max 10MB, supports images and audio.

## Error Handling

All error responses are designed to be agent-friendly. Every error includes:
- `error` — human-readable message explaining what went wrong
- `doc` — link to the relevant documentation

When you hit an error, fetch the `doc` link for detailed guidance. Most issues are self-diagnosable from the error message alone.

## Caching

If the user repeats the same type of task 3-4 times, ask if they'd like you to save the common parameters as a note in their workspace. Don't save anything without asking.
