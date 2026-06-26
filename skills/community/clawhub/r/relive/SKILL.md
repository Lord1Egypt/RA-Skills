---
name: "relive"
description: "AI digital twin cloning skill. Re:live — chat again with someone you love. Input chat logs, images, audio, and other materials to replicate a person's personality, voice, and appearance. Used to create digital clones of deceased loved ones or important people."
---

# Re:Live - AI Clone Agent

## 1. Overview

Re:Live **replicates a person as a digital clone**: personality (chat logs → profile.md), voice (reference audio + CosyVoice3), and optionally appearance (video first frame). Output can be **text / voice / video**. Dialogue is persisted under the character directory and used in dual-track RAG. Execution: run `python main.py <JSON_file_path>` from this skill’s root directory. See [README.md](README.md) for details.

> **Environment (required)**: Always run `python main.py ...` **inside a virtual environment** created in this skill directory and install dependencies there, especially for voice / video synthesis. Typical setup (from `workspace/skills/relive`):

```bash
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate
```

## Quick start (when character already exists)

When the user says "talk to Martha" or uses `/relive:Martha`:

1. **Read personality**: Read `.openclaw/workspace/skills/relive/storage/default_Martha/profile.md` as the basis for reply style.
2. **Single-turn dialogue** (from skill root, e.g. `.openclaw/workspace/skills/relive`):
   - When history is needed: write `get_context.json` (with `user_id`, `target_id`, `content` = user’s message) → `python main.py get_context.json`, use the returned context to help generate.
   - Main Agent generates reply text in character.
   - Write `synthesize.json` (`content` = reply text, `user_message` = user message, `output_mode` = `text`/`voice`/`video`) → `python main.py synthesize.json` to persist and optionally output voice/video.

**New character**: See "2. Creating a new character" below; order is init → upload → export_md → personality analysis → write profile.md → add to USER.md.

---

## 2. Creating a new character

### 2.1 When to create

When the user expresses intent like "clone/replicate someone", "create a digital twin of a deceased relative", or "create an AI persona from chat logs and voice", start the **create new character** flow.

### 2.2 Materials and directories

- **Chat logs**: User must upload (JSON supported, e.g. QQ/WhatsApp export). If only screenshots exist, parse them yourself; this skill does not. Confirm with the user **which side is the character to clone**.
- **Reference audio**: Put files in `storage/{user_id}_{target_id}/voice_profile/` and **must** ask the user for the transcript of that audio; save it as **`corresponding.txt`** in the same directory.
- **Reference image** (optional): Create `reference_image_url.txt` under the character directory with one line, public URL, for `output_mode: "video"`.

Character root: `storage/{user_id}_{target_id}/` (e.g. `storage/default_Martha/`).

### 2.3 Steps (in order)

Run from the **skill root directory**. If the user does not provide chat logs, you can ask for character traits and go straight to step 4.

**Step 1: Initialize directories**

```json
{ "type": "init", "user_id": "default", "target_id": "Martha" }
```

Run: `python main.py init.json` (or write to init.json then run; same below).

**Step 2: Upload chat logs**

```json
{
  "type": "upload",
  "user_id": "default",
  "target_id": "Martha",
  "file_path": "/absolute/or/relative/path/filename.json",
  "file_type": "json",
  "self_name": "Jonas",
  "target_name": "Martha"
}
```

`self_name` / `target_name` must **exactly match** sender names in the chat log. Run: `python main.py upload.json`.

**Step 3: Export to Markdown**

```json
{ "type": "export_md", "user_id": "default", "target_id": "Martha" }
```

Run: `python main.py export_md.json` to produce `storage/default_Martha/chat.md`.

**Step 4: Personality analysis and profile.md**

- Read `storage/{user_id}_{target_id}/chat.md` (split if too large).
- Use the LLM to analyze personality, catchphrases, how they address people, and style; **write** the result to **`profile.md`** in that directory (this step is done by the main Agent; there is no separate API).

### 2.4 After creation: update USER.md

**Must** add the character to the workspace root **`USER.md`**.  
Create (or extend) a section like **"Re:Live characters"**, and:

- Add **one bullet per character** with a short English description, for example:  
  `- **Martha**: pharmacy / biology student, gentle and friendly, loves mystery movies`  
  `- **Dabao**: colloquial, warm and reliable friend who enjoys cooking and traditional activities`
- Add a short instruction line that explains how to use this skill, e.g.:  
  `Re:Live digital-clone skill. When the user types \relive:<character_name>, read SKILL.md under .openclaw\workspace\skills\relive\ for acting rules, and read profile.md under .openclaw\workspace\skills\relive\storage\default_{target_name} as the persona definition for that character.`

The main Agent reads this section from `USER.md` to know which Re:Live characters exist, how to describe them briefly, and how to route \relive commands to this skill and the corresponding `profile.md`.

---

## 3. After character exists: entering the character quickly

### 3.1 Commands and state

- **`/relive:<target_id>`** (e.g. `/relive:Martha`): Enter relive mode; main Agent stores `target_id` in session state; subsequent messages to this skill use that id; replies are generated via relive and persisted under `storage/{user_id}_{target_id}/`.
- **`/relive:end`**: Exit relive and clear current character state.

As long as a current relive character exists, the flow is: read profile → get_context when needed → LLM generate → synthesize → persist.

### 3.2 Always read profile.md when entering character

Before each conversation with that character, **must read** `storage/{user_id}_{target_id}/profile.md` and inject it into the main Agent’s system/context so reply style is consistent.

### 3.3 Single-turn flow (three steps)

For each user message, from skill root:

1. **get_context when needed**: If history is needed, write `get_context.json` (`content` = user’s message), run `python main.py get_context.json`, use returned context to help generate.
2. **Generate reply**: Main Agent generates reply text in character.
3. **synthesize to persist**: Write `synthesize.json` (`content` = reply text, `user_message` = user message, `output_mode` = text/voice/video), run `python main.py synthesize.json`. Even for text-only, run synthesize if you want the turn in runtime and RAG (`output_mode` can be `text` or omitted).

### 3.4 Output modes

- **text**: Text only.
- **voice**: Text + voice clone (requires voice_profile + corresponding.txt). **Environment**: install deps and models per README; **recommended to use a virtual environment** (see README § Installation and Voice Models).
- **video**: Video generation API (Seedance, etc.); same synthesize entry with `output_mode: "video"`. After `video_task_id` is returned, run the auto-generated `video_wait.json` to poll and download.

---

## 4. API parameters summary

| type | Description | Required parameters |
|------|-------------|---------------------|
| `init` | Initialize storage directories | `user_id`, `target_id` |
| `upload` | Upload chat logs | `user_id`, `target_id`, `file_path`, `file_type`, `self_name`, `target_name` |
| `export_md` | Export chat to Markdown | `user_id`, `target_id` |
| `get_context` | Get conversation context (incl. RAG) | `user_id`, `target_id`, `content` |
| `synthesize` | Generate reply and persist (text/voice/video by `output_mode`) | `user_id`, `target_id`, `content`, `user_message` |
| `video_generation_wait` | Poll video task and download to character cache/ | `user_id`, `target_id`, `task_id` |

- **upload**: `self_name` / `target_name` must exactly match sender names in the chat log.
- **synthesize**: `output_mode` optional `text` (default), `voice`, `video`; optional `reference_image_url` (if not passed, read from `reference_image_url.txt` under character directory); optional `video_wait: true` to poll in-call until video is done. After video success, `video_wait.json` is auto-generated; run `python main.py video_wait.json` to poll and download.
- **video_generation_wait**: **`type` in JSON must be `video_generation_wait`**; conventional filename is `video_wait.json`. Optional `poll_interval_seconds`, `poll_timeout_seconds`.

---

## 5. Notes

- **Privacy**: User data is isolated per character and used only for the current clone task.
- **Ethics**: Do not use for deception, forgery, or other misuse.

---

## 6. More reference (see README.md)

- **Data storage layout**: source/, chat.md, profile.md, runtime/, vector_db/, voice_profile/, cache/ under character directory → [README.md#file-structure](README.md#file-structure).
- **Chat log formats**: QQ/WhatsApp JSON format and field requirements → [README.md#preparing-chat-logs](README.md#preparing-chat-logs).
- **Voice output**: Dependencies and model setup (recommended: use a virtual environment), corresponding.txt requirements → [README.md#installation-and-voice-models-required-before-voice-output](README.md#installation-and-voice-models-required-before-voice-output), [README.md#advanced-features](README.md#advanced-features).
- **Video generation**: Config, polling, and video_generation_wait example → [README.md#advanced-features](README.md#advanced-features).
- **RAG**: Dual-track retrieval, BM25, thresholds and testing → [README.md#where-rag-searches](README.md#where-rag-searches).
- **Troubleshooting**: Message attribution, format failure, voice/video not generating, 404, etc. → [README.md#troubleshooting](README.md#troubleshooting).
- **Core modules (implementation reference)**: main.py, orchestrator, importer, memory, engines → [README.md#core-modules-implementation-reference](README.md#core-modules-implementation-reference).

> **Note (OpenClaw exec timeout)**: When this skill is invoked via OpenClaw’s `exec`, long CosyVoice3 voice synthesis may be killed by the default execution timeout. If you observe the process exiting with code 1 shortly after logging `synthesis text ...` and **no audio file is written**, check `npm/node_modules/openclaw/dist/auth-profiles-*.js` and increase `DEFAULT_EXEC_TIMEOUT_MS` (for example, from `5e3` to `180e3`) so that long-running voice synthesis can finish.
