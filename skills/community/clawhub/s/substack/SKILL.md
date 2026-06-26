---
name: substack
description: Publish, edit, and manage Substack posts for the Alternative Partners publication (alternativepartners.substack.com) via the internal REST API. Use this skill when asked to post to Substack, update or edit an existing Substack post, save a draft, check a post's ID, or do any Substack publishing operation — even if the user just says "push this to Substack", "update the post", or "edit that Substack".
---

# Substack Skill

Manages publishing and editing for the Alternative Partners Substack publication via the internal REST API. No Playwright, no browser — pure `requests` with a session cookie.

## Auth

This skill requires a `connect.sid` session cookie from Substack. Store it securely and provide it as the `SUBSTACK_SID` environment variable (or equivalent in your secrets manager).

This is the `connect.sid` cookie. Valid for months unless you sign out of Substack in Chrome. To rotate: sign out of Substack → sign back in → open DevTools → copy `substack.sid` cookie value → update your secrets store.

The publisher module at `publishers/substack.py` handles auth automatically. Always use it rather than calling the API directly.

---

## API Endpoints (alternativepartners.substack.com)

| Action | Method | Endpoint |
|--------|--------|----------|
| Create draft | `POST` | `/api/v1/drafts` |
| Publish draft | `POST` | `/api/v1/drafts/{id}/publish` |
| Update existing post | `PUT` | `/api/v1/drafts/{id}` |
| Fetch post by slug | `GET` | `/api/v1/posts/{slug}` |
| List posts | `GET` | `/api/v1/posts?limit=N` |

**Key discovery (2026-03-20):** `PUT /api/v1/drafts/{id}` works on already-published posts too — it edits them in place. The post ID is the same as the draft ID used to create it.

**Does NOT exist:** `PUT /api/v1/posts/{id}` returns 404. Always use the `/drafts/{id}` endpoint even for published posts.

---

## Body Format

Substack uses ProseMirror JSON for post bodies. The publisher converts plain text → ProseMirror automatically.

**Input format:** Plain text with double-newline paragraph breaks.
**Output format (internal):** ProseMirror `doc` object, serialized as a JSON string and passed as `draft_body`.

```python
def _build_prosemirror_doc(body: str) -> dict:
    paragraphs = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
    return {
        "type": "doc",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": p}]}
            for p in paragraphs
        ]
    }
```

Limitation: This produces plain paragraphs only. Bold, headers, lists, links require richer ProseMirror nodes — not yet implemented.

---

## Common Operations

### 1. Publish a new post

```python
from publishers.substack import publish_substack

url = publish_substack(
    title="Your Post Title",
    body="First paragraph.\n\nSecond paragraph.",
    publish=True   # False = save as draft only
)
```

Or via CLI from the pipeline directory:
```bash
cd ~/Documents/Codex/Content/ap-content-pipeline
python3 publishers/substack.py "Title Here" "Body paragraph one.\n\nParagraph two."
```

### 2. Update / edit an existing post

Need the numeric post ID. Get it by fetching the post:
```bash
curl -s -b "substack.sid=$SUBSTACK_SID" \
  "https://alternativepartners.substack.com/api/v1/posts/{slug}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('id:', d.get('id'))"
```

Then update:
```python
from publishers.substack import update_substack

url = update_substack(
    post_id=191631753,
    title="Updated Title",
    body="New body content.\n\nSecond paragraph."
)
```

### 3. Get a post's ID from its slug

The slug is the last segment of the Substack URL:
`https://alternativepartners.substack.com/p/the-revops-ai-reality-check-nobodys`
→ slug = `the-revops-ai-reality-check-nobodys`

```bash
curl -s -b "substack.sid=$SUBSTACK_SID" \
  "https://alternativepartners.substack.com/api/v1/posts/THE-SLUG-HERE" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id'))"
```

### 4. Save as draft without publishing

```python
url = publish_substack(title, body, publish=False)
# Returns: https://alternativepartners.substack.com/publish/post/{id}
```

---

## Email Blast Behavior

`publish` endpoint is called with `{"send_email": False}` — posts go live on the web but do **not** trigger a subscriber email blast. This is intentional for automated/pipeline posts.

To send an email blast, Benjamin needs to manually click "Send" in the Substack editor UI. Do not change `send_email` to `True` without explicit confirmation.

---

## Pipeline Integration

The AP Content Pipeline at `~/Documents/Codex/Content/ap-content-pipeline/` handles end-to-end publishing including veto window, soft-veto Slack notification, and scheduling. For single one-off posts, call the publisher directly. For managed pipeline runs, use `publish_runner.py`.

The pipeline also has a `research_gate.py` that runs a web search competitive sweep + LLM differentiation analysis before drafting. Posts in `idea_inbox.json` with `research_status: "pending"` will be researched before drafting. Requires a search API key configured in your environment.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | Cookie expired | Rotate: sign out/in of Substack in Chrome, grab new `substack.sid`, update your secrets store |
| `PUT /api/v1/posts/...` → 404 | Wrong endpoint | Use `/api/v1/drafts/{id}` for updates, not `/api/v1/posts/{id}` |
| `POST /api/v1/drafts/{id}/publish` fails | Post already published | That's OK — post is already live, return the known URL |
| Body renders as one giant paragraph | Missing double-newlines | Input body must use `\n\n` between paragraphs |
| `substack.sid` not found | Cookie env var not set | Ensure `SUBSTACK_SID` is set in your environment before running |
