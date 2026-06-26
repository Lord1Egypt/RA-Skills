# Project & Preview — Knowledge

This is supplementary knowledge for the yino-ai skill. Load this when the user's task involves multiple related generations and you want to organize them with a project and visual preview.

## When to suggest a project

**Upfront** — the user's task clearly involves multiple related generations:
- Music video: storyboard images + video clips per shot
- Style exploration: multiple style variations of the same subject
- Product shots: multiple angles or settings
- Any task producing 3+ generations that tell a story together

Suggest: "Would you like me to create a project so you can preview all the results together?"

**Retroactive** — you've already generated several related items without a project. Suggest: "I've generated a few related pieces — want me to organize them into a project?" Then create a project and assign existing generations to it.

## Workflow

### Starting with a project

1. **Create project** → `POST /api/agent/projects` with a title
2. **Generate with project_id** → pass `project_id` and `comment` (short label, max 100 chars) when submitting to model endpoints
3. **Build preview early** → `PUT /api/agent/projects/:id/preview` with blocks referencing the generations (even before they complete — the preview shows loading state for in-progress generations)
4. **Share preview_url** → the response includes a `preview_url`, share it in chat
5. **Poll by project** → `GET /api/agent/generations/status?project_id=xxx` to check all generations at once
6. **Append new blocks** → as more generations are created, use `PATCH /api/agent/projects/:id/preview` with `{"append": [...]}` to add new blocks without resending everything

### Retroactive: assign existing generations to a project

Use `PATCH /api/agent/generations/:id` to assign existing generations:

```bash
curl -X PATCH "${YINO_API_BASE_URL}/api/agent/generations/<gen_id>" \
  -H "Authorization: Bearer $YINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "proj_xxx"}'
```

You can also update `comment` in the same call: `{"project_id": "proj_xxx", "comment": "Shot 1"}`

## Preview blocks

Preview is a linear document made of three block types:

- **markdown** — text content (use sparingly; text explanations belong in chat)
- **media** — a single image/video/audio, either by `generationId` or external `url`
- **group** — container for child blocks, nestable up to 3 levels

### Key rules

- Every block must have an `id` — a short semantic name you choose (max 50 chars, e.g. `"shot-1"`, `"storyboard"`)
- `title` (max 50 chars) and `comment` (max 100 chars) are optional on every block
- Second-level groups render as **cards in a responsive grid**
- At the deepest level (L3), media children render as **tabs with icons** (🖼️ image, ▶️ video, 🔊 audio)
- When a group contains sub-groups, children render as a **responsive grid**
- Maximum nesting: 3 levels deep. 2 levels is usually enough.

### Example: Storyboard

```json
{
  "blocks": [
    {
      "type": "media",
      "id": "final-mv",
      "title": "Final MV",
      "comment": "Complete music video, 3:24",
      "generationId": "gen-final"
    },
    {
      "type": "group",
      "id": "storyboard",
      "title": "Storyboard",
      "comment": "12 shots, Shunji Iwai style",
      "children": [
        {
          "type": "group",
          "id": "shot-1",
          "title": "Shot 1 - Rain street",
          "children": [
            { "type": "media", "id": "shot-1-img", "generationId": "gen-img-001" },
            { "type": "media", "id": "shot-1-vid", "generationId": "gen-vid-001" }
          ]
        },
        {
          "type": "group",
          "id": "shot-2",
          "title": "Shot 2 - Window",
          "children": [
            { "type": "media", "id": "shot-2-img", "generationId": "gen-img-002" },
            { "type": "media", "id": "shot-2-vid", "generationId": "gen-vid-002" }
          ]
        }
      ]
    }
  ]
}
```

Each shot group renders as cards in a grid — image and video side by side.

### Example: Style comparison

```json
{
  "blocks": [
    {
      "type": "group",
      "id": "style-options",
      "title": "Style Options",
      "comment": "3 directions for your album cover",
      "children": [
        { "type": "media", "id": "style-a", "title": "A. Minimalist", "generationId": "gen-001" },
        { "type": "media", "id": "style-b", "title": "B. Retro", "generationId": "gen-002" },
        { "type": "media", "id": "style-c", "title": "C. Abstract", "generationId": "gen-003" }
      ]
    }
  ]
}
```

## Updating preview

Three update modes:

**PATCH `update`** — modify specific blocks in place by id (works recursively on nested blocks):

```bash
curl -X PATCH "${YINO_API_BASE_URL}/api/agent/projects/<project_id>/preview" \
  -H "Authorization: Bearer $YINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"update": [{"id": "shot-1-img", "generationId": "gen-new-001"}]}'
```

**PATCH `append`** — add new blocks to the end:

```bash
curl -X PATCH "${YINO_API_BASE_URL}/api/agent/projects/<project_id>/preview" \
  -H "Authorization: Bearer $YINO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"append": [{"type": "media", "id": "shot-3-img", "generationId": "gen-003"}]}'
```

Both can be combined in one request: `{"update": [...], "append": [...]}`. Updates apply first, then appends.

**PUT (full replacement)** — for restructuring layout or building from scratch. Send the complete blocks array.

**Strategy:**
- Use `update` to swap a generationId after re-generating, or tweak titles/comments
- Use `append` to add new shots as they're created
- Use `PUT` only when reorganizing the entire layout
- All three save context window tokens compared to resending the full blocks array

**Early preview:** You can register generations to the preview as soon as they're created — even before they finish processing. The preview shows a loading spinner for in-progress generations and updates automatically. This lets users watch progress in real time.

## Comment best practices

Generation `comment` (max 100 chars) is a short label that appears in status polling responses. Keep it concise — it's carried in every poll response and counts against the agent's context window.

Good: `"Shot 3 - Rain street close-up"`
Bad: `"This is the third shot in the sequence showing a close-up of rain drops on a glass window in a dimly lit street scene inspired by Shunji Iwai's cinematography"`
