---
name: robin
description: "Save and review notes, quotes, articles, links, images, and video references in a personal commonplace book. Use when the user wants to file something to remember, organize knowledge by topic, resurface saved items, or review prior entries."
license: MIT
compatibility: "Requires Python 3.11+ and local filesystem access. Optional: a scheduler for periodic review."
metadata:
  category: personal
---

# Robin — Personal Knowledge Curation Skill

Robin is a digital commonplace book. The user gives content to the AI agent, and the agent uses Robin to store it in topic-organized Markdown files and resurface it later for review.

## Storage Model

- the Robin state directory stores:
  - `robin-config.json`
  - optionally `robin-review-index.json`
  - `topics/` for topic-organized Markdown files
  - `media/` for copied image assets

Recommended default state directory:

- `<agent-workspace>/data/robin/`

Typical host examples:

- Hermes: `~/.hermes/data/robin/`
- OpenClaw: `~/.openclaw/workspace/data/robin/`

Robin does not guess host layout. The caller must provide the Robin state directory explicitly.

## Host Requirements

The host agent must be able to:

- read and write local files
- run bundled Python scripts
- pass CLI arguments or environment variables to Robin
- schedule periodic review if review automation is desired

## Setup Contract

The host agent is responsible for first-run setup.

On setup, the agent should:

1. choose a state directory, usually `<agent-workspace>/data/robin/`
2. create the state directory if it does not exist
3. create `robin-config.json` in that directory if it does not exist
4. ensure the state directory contains `topics/` and `media/`
5. optionally create `robin-review-index.json`; if it is missing, Robin starts with an empty index and writes the file when review state is saved
6. ask the user how often scheduled recall should happen and when it should run
7. verify setup with a quick check by running `python3 scripts/doctor.py --state-dir <state-dir> --json`
8. optionally run the full integration check with `python3 scripts/selftest.py`

Example `robin-config.json`:

```json
{
  "topics_dir": "topics",
  "media_dir": "media",
  "min_items_before_review": 30,
  "review_cooldown_days": 60
}
```

Robin does not need a separate content-root path. Topic files and copied media live inside the state directory under `topics/` and `media/`.

`robin-config.json` itself is required, but it may be an empty JSON object (`{}`). All fields inside it are optional. Robin defaults to:

- `topics_dir`: `topics`
- `media_dir`: `media`
- `min_items_before_review`: `30`
- `review_cooldown_days`: `60`

Optional example `robin-review-index.json`:

```json
{
  "items": {}
}
```

## Runtime Contract

Robin accepts both:

- `--state-dir /path/to/data/robin`
- `ROBIN_STATE_DIR=/path/to/data/robin`

Precedence:

1. `--state-dir`
2. `ROBIN_STATE_DIR`
3. otherwise fail

If neither is provided, Robin exits with:

```text
Robin state directory is not configured. Pass --state-dir or set ROBIN_STATE_DIR.
```

Default runnable path:

- agents can run the repo-local scripts directly without installing the package:
  - `python3 scripts/add_entry.py`
  - `python3 scripts/doctor.py`
  - `python3 scripts/entries.py`
  - `python3 scripts/review.py`
  - `python3 scripts/reindex.py`
  - `python3 scripts/search.py`
  - `python3 scripts/selftest.py`
  - `python3 scripts/topics.py`

No `pip install -e .` or manual path setup is required for this repo-local script path.

Optional installed path for advanced users:

- if the user explicitly wants installed entry points and the agent runs `pip install -e .`, Robin also exposes:
  - `robin-add`
  - `robin-doctor`
  - `robin-entries`
  - `robin-review`
  - `robin-reindex`
  - `robin-search`
  - `robin-topics`

For advanced manual setup details and shell examples, see [docs/guide.md](docs/guide.md).

## Selftest

After setup or after a Robin upgrade, the agent can run:

```bash
python3 scripts/selftest.py
```

By default, this uses a temporary state directory and does not touch the user's real Robin library. It verifies setup, doctor, entries, add, search, review, rating, duplicate rejection, override, and reindex behavior against the documented JSON contracts.

For a non-destructive check of a real state directory, run:

```bash
python3 scripts/selftest.py --state-dir <state-dir>
```

That mode checks only that `robin-config.json`, `topics/`, `media/`, `topics.py --json`, and `doctor.py --json` work for the supplied state directory.

## Agent Responsibilities

When using Robin, the agent is responsible for:

- choosing the topic
- deciding whether the entry is `text`, `image`, or `video`
- generating a useful `description` for every entry
- generating `creator`, `published_at`, and `summary` for every media entry
- refusing to store media if the required metadata is missing
- passing only supported media forms to Robin:
  - local image file paths for image entries or text entry attachments
  - `http(s)` URLs for videos
  - never uploaded or local video files
- passing `--state-dir` or `ROBIN_STATE_DIR` on every Robin invocation

Robin is responsible for:

- persisting the entry and copied image assets
- preserving stable ids
- resurfacing the stored text, media reference, and metadata later
- maintaining review state
- returning a clear error instead of storing incomplete or unsupported media entries

## Safety Boundary

Robin is a storage and retrieval skill, not a code-editing skill.

Normal Robin use may:

- write to the configured state directory
- update the review index
- copy accepted image assets into the media directory

Normal Robin use must not:

- modify Robin's source code
- modify Robin's docs
- change packaging or tests
- change the skill implementation unless the user explicitly asks to edit Robin itself

If the agent notices a Robin bug while using the skill, it should report the issue to the user instead of patching Robin unless the user explicitly asks for a fix.

## Filing

1. The user sends content to the AI agent.
2. The agent lists existing topics with `python3 scripts/topics.py --state-dir <state-dir> --json`.
3. The agent chooses a topic by name when there is a clear match.
4. If topic names alone are ambiguous, the agent should inspect relevant topic files or use host search for more context.
5. If two existing topics are still both plausible, the agent asks the user to choose.
6. If no existing topic fits, the agent suggests a new reusable topic name and files the item there.
7. `add_entry.py` checks deterministic duplicates before saving; the agent uses `--allow-duplicate` only when the user intentionally wants another copy.
8. For explicit `image` or `video` entries, the agent must also supply `creator`, `published_at`, and `summary`. If any are missing, Robin rejects the entry.

### Topic Strategy

- List existing topics with `python3 scripts/topics.py --state-dir <state-dir> --json` before filing.
- Prefer reusing an existing topic over creating a near-duplicate.
- Prefer durable, reusable topics such as `quotes`, `wisdom`, `poetry`, or `talks`; avoid one-off topics named after a single entry.
- Create a new topic only when no existing topic clearly fits.
- If two existing topics are both plausible, ask the user to choose instead of guessing.
- Topic filenames are generated from topic names as lowercase slugs with non-alphanumeric characters normalized to dashes.

### Content Policy

- `add_entry.py` blocks deterministic duplicates by default when an existing entry has the same source URL, same media reference, or same normalized body text.
- If the user intentionally wants another copy, pass `--allow-duplicate`.
- If the item is a near-duplicate with meaningful differences, file it only when the difference is worth preserving and explain that in `description`.
- Robin has no hard body-size limit, but the agent should summarize very long articles/transcripts unless the user explicitly wants the full text stored.
- `description` is required context for every entry: why this item matters and how to recognize it later.
- `summary` is required only for media entries: what the media itself contains.
- `note` is optional agent commentary for extra curation, reminders, or connections to other entries.
- Pass tags on the CLI as one comma-separated string, for example `--tags "writing,clarity"`. Robin stores them as a frontmatter list.

### Entry-Type Rules

- `text`
  - requires: `topic`, `content`, `description`
  - optional: local image attachment with `--media-path`, `source`, `note`, `tags`
  - behavior: when `--media-path` is provided, Robin copies the image into `media/<topic-slug>/`, sets `media_source`, keeps `entry_type` as `text`, and does not require `creator`, `published_at`, or `summary`
  - rejection: text entries do not accept `--media-url`
- `image`
  - requires: `topic`, local image file path, `description`, `creator`, `published_at`, `summary`
  - optional: `content`, `source`, `note`, `tags`
  - behavior: Robin copies the image into `media/<topic-slug>/` under the state directory and creates that subdirectory automatically
- `video`
  - requires: `topic`, video URL, `description`, `creator`, `published_at`, `summary`
  - optional: `content`, `source`, `note`, `tags`
  - behavior: Robin stores the URL only
  - rejection: local or uploaded video files are always rejected; if the user cannot provide a shareable `http(s)` URL, save a normal `text` entry with the local path/context and tell the user Robin did not store the video file itself

### Failure Rules

Robin rejects the add operation if:

- a text entry is missing `content`
- a media entry is missing `description`, `creator`, `published_at`, or `summary`
- an image entry is missing a local file path
- an image path does not exist or is not a supported image type
- a video entry is missing a valid `http(s)` URL
- a local or uploaded video file is supplied
- the serialized entry would contain a standalone `***` line, which Robin reserves as its internal entry separator

When the add operation fails, the agent should pass the returned error back to the user instead of pretending the item was stored.

## Review Mode

Review is host-triggered. Robin itself does not run a scheduler.

During setup, the agent should ask the user what recall cadence they want. If the host supports scheduling, the agent should usually configure a daily or weekly recall trigger at the user's preferred time. Otherwise, the agent should expose active review as an on-demand action.

If the host scheduler supports skill metadata, scheduled recall jobs should load the `robin` skill. If it does not, the cron prompt must explicitly follow this Review Mode section.

Scheduled recall means Robin resurfaces an item for learning. It is not an active review session, and cron or scheduled recall messages must not ask the user to reply with a bare `1`-`5` rating because the agent may not know that a later numeric reply refers to Robin.

Default recall text output:

```text
📚 Robin Recall

Topic: <topic>
Type: <entry_type>
Source: <source if present, else media_source if present, else "Not provided">
Creator: <creator if present, else "Not provided">
Saved on: <date_added>

Description:
<description if present, else "Not provided">

Body:
<body if present, else "Not provided">
```

Review behavior:

1. Wait until `len(items) >= min_items_before_review`
2. Prefer unrated items first
3. Then lower-rated items
4. Then least frequently surfaced items
5. Skip items surfaced within `review_cooldown_days`
6. Surface the chosen entry, including media metadata when present
7. Scheduled recall is the default: `python3 scripts/review.py --state-dir <state-dir>` increments `times_surfaced`, sets `last_surfaced`, and keeps `_awaiting_rating` as `false`
8. Active review is explicit: `python3 scripts/review.py --state-dir <state-dir> --active-review` increments `times_surfaced`, sets `last_surfaced`, and marks `_awaiting_rating` as `true`
9. If `_awaiting_rating` is `true`, rating only overwrites the rating and clears `_awaiting_rating` back to `false`

If the agent calls `--rate` directly on an item that was not surfaced first, Robin still sets `last_surfaced`, increments `times_surfaced`, and leaves `_awaiting_rating` as `false`.

Preferred rating flow:

- Use `python3 scripts/review.py --state-dir <state-dir> --active-review --json` to surface an item in a live active-review session.
- After the user rates that surfaced item, call `python3 scripts/review.py --state-dir <state-dir> --rate <id> <rating> --json`.
- Use direct `--rate` without a prior surface only for manual corrections or when the user explicitly names an existing entry id.
- Do not request ratings in scheduled recall messages. Only rate during active review sessions or when the user explicitly names a Robin item id.

## Search Guidance

When the host supports file indexing, Robin topic files should be part of the host agent's searchable corpus.

Use host/global search for:

- broad semantic retrieval across the user's workspace
- natural-language recall where Robin may or may not be the relevant source

Use `robin-search` for:

- Robin-specific lookup tasks
- filtering by topic or tags
- returning stable Robin ids and metadata
- deterministic JSON output for Robin entries
- fallback when host indexing is unavailable or stale

`robin-search` can combine filters. If both `--topic` and `--tags` are provided, Robin first narrows to the topic and then applies the tag filter within that topic.

## Commands

Default repo-local commands for agents:

- `python3 scripts/add_entry.py`
- `python3 scripts/doctor.py`
- `python3 scripts/entries.py`
- `python3 scripts/review.py`
- `python3 scripts/reindex.py`
- `python3 scripts/search.py`
- `python3 scripts/selftest.py`
- `python3 scripts/topics.py`

Optional installed entry points for advanced users:

- `robin-add`
- `robin-doctor`
- `robin-entries`
- `robin-review`
- `robin-reindex`
- `robin-search`
- `robin-topics`

All Robin commands accept:

- `--state-dir`

Agents should use `--json` whenever they need to parse command output. Without `--json`, Robin prints human-readable text for interactive use; that text is not a stable machine contract.

CLI flags by command:

- `add_entry.py`: `--state-dir`, `--topic`, `--entry-type text|image|video`, `--content`, `--description`, `--source`, `--media-path`, `--media-url`, `--creator`, `--published-at`, `--summary`, `--note`, `--tags`, `--allow-duplicate`, `--json`
- `doctor.py`: `--state-dir`, `--json`
- `entries.py`: `--state-dir`, `--delete ID`, `--move ID --topic TOPIC`, `--json`
- `review.py`: `--state-dir`, `--status`, `--active-review`, `--rate ID RATING`, `--json`
- `search.py`: `--state-dir`, optional positional `query` string, `--topic`, `--tags`, `--json`
- `selftest.py`: optional `--state-dir` for non-destructive setup checks, `--keep-temp`
- `topics.py`: `--state-dir`, `--json`
- `reindex.py`: `--state-dir`, `--json`

Examples:

The examples below use the repo-local `python3 scripts/*.py` path. The installed `robin-*` commands are equivalent aliases if the package has been installed.

- `python3 scripts/add_entry.py --state-dir /path/to/data/robin --topic "reasoning" --content "..." --description "..."`
- `python3 scripts/add_entry.py --state-dir /path/to/data/robin --topic "writing" --content "..." --description "..." --note "Useful for later review."`
- `python3 scripts/add_entry.py --state-dir /path/to/data/robin --topic "writing" --content "Write as if speaking to a smart friend." --description "A reminder to keep prose conversational and clear." --source "https://example.com/article" --json`
- `python3 scripts/add_entry.py --state-dir /path/to/data/robin --topic "reasoning" --content "The map is not the territory." --description "A reminder that abstractions are not reality itself." --tags "thinking,quotes"`
- `python3 scripts/add_entry.py --state-dir /path/to/data/robin --topic "wisdom" --content "Filed this screenshot to wisdom." --description "A text note with a local screenshot attached for later context." --media-path ~/Downloads/screenshot.png --json`
- `python3 scripts/review.py --state-dir /path/to/data/robin`
- `python3 scripts/review.py --state-dir /path/to/data/robin --json`
- `python3 scripts/review.py --state-dir /path/to/data/robin --active-review --json`
- `python3 scripts/review.py --state-dir /path/to/data/robin --status --json`
- `python3 scripts/review.py --state-dir /path/to/data/robin --rate 20260408-a1f3c9 5`
- `python3 scripts/review.py --state-dir /path/to/data/robin --rate 20260408-a1f3c9 5 --json`
- `python3 scripts/search.py --state-dir /path/to/data/robin "clear thinking" --json`
- `python3 scripts/search.py --state-dir /path/to/data/robin --topic "AI Reasoning" --json`
- `python3 scripts/search.py --state-dir /path/to/data/robin --tags "writing,clarity" --json`
- `python3 scripts/search.py --state-dir /path/to/data/robin --topic "AI Reasoning" --tags "clarity" --json`
- `python3 scripts/topics.py --state-dir /path/to/data/robin --json`
- `python3 scripts/selftest.py`
- `python3 scripts/selftest.py --state-dir /path/to/data/robin`
- `python3 scripts/reindex.py --state-dir /path/to/data/robin`
- `python3 scripts/reindex.py --state-dir /path/to/data/robin --json`

Use `python3 scripts/reindex.py --state-dir <state-dir>` after manual edits to topic files, when rebuilding review state from existing markdown, or when importing legacy entries and wanting the review index rebuilt from disk.

## JSON Contract

Add success shape includes:

- `id`
- `topic`
- `filename` (topic file basename only, for example `quotes.md`)
- `entry_type`
- `media_source`
- `description`

Review success payload:

- `{"status": "ok", "id": "...", "topic": "...", "date_added": "YYYY-MM-DD", "entry_type": "text|image|video", "media_kind": "image|video|\"\"", "media_source": "...|\"\"", "source": "...|\"\"", "description": "...", "creator": "...|\"\"", "published_at": "...|\"\"", "summary": "...|\"\"", "tags": [...], "body": "...", "rating": 1|2|3|4|5|null, "times_surfaced": N}`

Review rate success payload:

- `{"id": "...", "topic": "...", "date": "YYYY-MM-DD", "rating": 1|2|3|4|5, "last_surfaced": "ISO-8601 timestamp", "times_surfaced": N, "_awaiting_rating": false}`

Search success payload:

- `{"count": N, "entries": [{"id": "...", "topic": "...", "date_added": "YYYY-MM-DD", "entry_type": "text|image|video", "media_kind": "image|video|\"\"", "media_source": "...|\"\"", "source": "...|\"\"", "description": "...", "creator": "...|\"\"", "published_at": "...|\"\"", "summary": "...|\"\"", "tags": [...], "body": "...", "rating": 1|2|3|4|5|null}]}`

Topics success payload:

- `[{"topic": "...", "filename": "...", "entries": N, "rated": N, "unrated": N}]`

Reindex success payload:

- `{"entries_found": N, "items_indexed": N, "rated": N, "unrated": N}`

Review skip payloads:

- `{"status": "skip", "reason": "not_enough_items", "total_items": N, "min_items_before_review": N}`
- `{"status": "skip", "reason": "no_eligible_items"}`

Review status payload:

- `{"total_items": N, "rated": N, "unrated": N, "min_items_before_review": N, "ready": true|false}`

Failure shape:

- `{"error": "..."}`

Exit status on failure:

- `1`

## Topic File Format

Entries are separated by `***`. Each entry is a frontmatter block followed by a blank line and then the body text.

Text entries may omit `entry_type`; omitted `entry_type` is parsed as `text`.

```text
id: 20260408-a1f3c9
date_added: 2026-04-08
entry_type: image
media_kind: image
media_source: media/poetry/20260408-a1f3c9.png
description: A photographed poem excerpt worth revisiting.
creator: Mary Oliver
published_at: 1986
summary: An excerpt about attention and observation.
tags: [poetry]

Opening lines from the photographed page.
```

Topic filename: lowercase topic slug with non-alphanumeric characters normalized to dashes.

Frontmatter parsing rules:

- keys are matched case-insensitively
- a blank line must separate frontmatter from body
- body starts at the first blank line

## Review Index Schema

```json
{
  "items": {
    "20260408-a1f3c9": {
      "id": "20260408-a1f3c9",
      "topic": "quotes",
      "date": "2026-04-08",
      "rating": null,
      "last_surfaced": null,
      "times_surfaced": 0,
      "_awaiting_rating": false
    }
  }
}
```

Review settings such as `min_items_before_review` and `review_cooldown_days` live only in `robin-config.json`.

`_awaiting_rating` is an internal review-state flag. It is `true` only after Robin surfaces an item with `--active-review` and becomes `false` again after that surface is rated. Scheduled recall leaves it `false`.

## Pitfalls

- Do not use `---` as an entry separator. Use `***`.
- Do not put a standalone `***` line inside entry body content. Robin reserves that exact line as its internal entry separator and rejects it on add.
- Uploaded or local video files are rejected. Ask for a shareable `http(s)` video URL, or save a normal `text` entry that records the local path/context without storing the video file.
- A blank line is required after frontmatter.
- Keep `id` stable when manually editing entries.
- If `robin-config.json` contains invalid JSON, Robin exits with an error; recreate it as `{}` or with the supported config fields.
- If `robin-review-index.json` is missing, Robin can rebuild review state as entries are used. If it is corrupted, back it up or recreate it as `{"items": {}}`, then run `python3 scripts/reindex.py --state-dir <state-dir> --json` to rebuild from topic files.
- If library health is uncertain, run `python3 scripts/doctor.py --state-dir <state-dir> --json` for a read-only diagnostic report.
- Use `python3 scripts/entries.py --state-dir <state-dir> --move <id> --topic <topic>` to move entries and `python3 scripts/entries.py --state-dir <state-dir> --delete <id>` to delete entries. Delete keeps copied media files.
- Manual topic-file edits must keep valid frontmatter, include a blank line before the body, and avoid standalone `***` lines in body content. Numbered lists are safe after the blank line.
- Telegram: Sending GIFs via `MEDIA:/path/file.gif` converts them to static photos. To preserve animation, GIFs must be sent as documents, not photos. The gateway may require a document wrapper or alternate approach for animated GIF delivery.

### Image Filing from Telegram / Chat Platforms

When a user sends an image to file to Robin via a messaging platform:

1. Telegram images arrive in `~/.hermes/image_cache/` with a name like `img_<hash>.jpg`
2. For an image-first entry, use `--entry-type image` and pass `--media-path`; this requires `creator`, `published_at`, and `summary`
3. For a text note with an attached image, keep `--entry-type text` and pass `--media-path`; Robin copies the image and sets `media_source` without requiring media metadata
4. After `add_entry.py` returns, verify `media_source` is populated in the JSON output

**Important**: Saying "Filed!" after running `add_entry.py` is premature if an expected image attachment is missing. Always check the returned JSON `media_source` field.

### Bulk Import Workflow

When filing many items at once (e.g. a batch of quotes):
1. Batch `add_entry.py` calls together when practical; each call performs deterministic duplicate checks before saving.
2. Use `--allow-duplicate` only for entries the user intentionally wants saved as another copy.
3. Prefer the CLI over manual Markdown edits. If manually editing topic files, validate that each entry has frontmatter, a blank line, body text, and no standalone `***` line.
4. If a topic file has a frontmatter parse error, `add_entry.py` and `search.py` can fail globally until the file is fixed.
