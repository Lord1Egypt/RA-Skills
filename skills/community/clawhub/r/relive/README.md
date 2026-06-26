# Re:live — chat again with someone you love · AI digital twin cloning skill for OpenClaw

![Re:live — chat again with someone you love](logo.png)

## One-Minute Quick Start

Missing someone important and want to chat, voice-call, or video with them? Just:

1. **Prepare chat logs** — JSON exported from QQ or WhatsApp, or have the user describe identity, personality, common phrases, and how they address people. After upload, export to `storage/{user_id}_{target_id}/chat.md`; personality analysis goes to `storage/{user_id}_{target_id}/profile.md`. For **voice cloning**, put reference audio in `storage/{user_id}_{target_id}/voice_profile/` and **must** ask the user for the transcript of that audio, saved as **`corresponding.txt`** in the same directory. **Reference image** (optional): create `reference_image_url.txt` under the character directory with one line containing the public URL of the first-frame image for video mode.
2. **Upload and initialize** — Call `init` + `upload` APIs. Put the API calls in a JSON file, then run `python main.py <file_path>` to execute.
3. **Start conversation** — Call `get_context` to get the prompt, `synthesize` to generate replies.

If you don’t want to read the rest, that’s fine — your OpenClaw will help you get it done.

---

## Installation and Voice Models (Required Before Voice Output)

To use **voice cloning** (`output_mode: "voice"`), you must complete the following environment and model setup. You can skip this section if you only use text or video mode.

### 1. Install Python Dependencies

In this skill’s root directory (`workspace/skills/relive/`). **Recommended: use a virtual environment** (see commands in the code block below); then run the following:

```bash
# Create and activate a virtual environment (Python 3.10/3.10+ recommended)
# Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS:
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Dependencies include `torch`, `torchaudio`, `librosa`, `modelscope`, `rank_bm25`, etc. Python 3.10 is recommended; install CUDA as needed for faster inference. **Using a virtual environment is recommended** to avoid conflicts with system or other projects; when running `main.py` for voice later, activate the same venv first.

**If `.venv` is not created:** On Windows, `python` may be the Store stub (`WindowsApps\python.exe`) and does nothing. Install Python from [python.org](https://www.python.org/downloads/) (or use Anaconda), then run `python -m venv .venv` again, or use the full path to your Python, e.g. `"C:\Python310\python.exe" -m venv .venv`.

### 2. Prepare CosyVoice Code

This skill uses **CosyVoice3** for zero-shot voice synthesis. Clone the CosyVoice repo under this skill’s `models/voice/`:

```bash
# Run from skill root directory
mkdir -p models/voice
cd models/voice
git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git
# If submodules fail, enter the repo and run:
# cd CosyVoice && git submodule update --init --recursive
```

Resulting layout: `workspace/skills/relive/models/voice/CosyVoice/` (containing `cosyvoice`, `third_party/Matcha-TTS`, etc.).

### 3. Download Voice Models and Resources

Create and run a download script in the skill root, or run in Python (after `pip install modelscope`):

**Option A: Huggingface**

```bash
cd workspace/skills/relive
python -c "
from huggingface_hub import snapshot_download
from pathlib import Path
root = Path('models/pretrained_models')
root.mkdir(parents=True, exist_ok=True)
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir=str(root / 'Fun-CosyVoice3-0.5B'))
snapshot_download('FunAudioLLM/CosyVoice-ttsfrd', local_dir=str(root / 'CosyVoice-ttsfrd'))
print('Done.')
"
```

**Option A: Modelscope (recommended in China)**

```bash
cd workspace/skills/relive   # or your skill root path
python -c "
from modelscope import snapshot_download
from pathlib import Path
root = Path('models/pretrained_models')
root.mkdir(parents=True, exist_ok=True)
print('Downloading Fun-CosyVoice3-0.5B...')
snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512', local_dir=str(root / 'Fun-CosyVoice3-0.5B'))
print('Downloading CosyVoice-ttsfrd...')
snapshot_download('iic/CosyVoice-ttsfrd', local_dir=str(root / 'CosyVoice-ttsfrd'))
print('Done.')
"
```

You should then have:
- `models/pretrained_models/Fun-CosyVoice3-0.5B/` (main model; used by `voice.model_dir` in `config/settings.yaml`, default path is already set)
- `models/pretrained_models/CosyVoice-ttsfrd/` (text front-end; optionally install its whl for better text normalization, otherwise wetext is used)

### 4. Verify Configuration

Ensure voice-related settings in `config/settings.yaml` match the paths above, e.g.:

```yaml
voice:
  model_dir: models/pretrained_models/Fun-CosyVoice3-0.5B
  voice_profile_path: storage/{user_id}_{target_id}/voice_profile
```

If voice still does not generate, see "Troubleshooting → Voice not generating" below and confirm steps 1–3 are done.

---

## Getting Started

### How to Run

All skill invocations run from **this skill’s root directory** (`workspace/skills/relive/`):

```bash
python main.py message.json
```

Put a single API call in a JSON file and run `python main.py <file_path>`. Examples: `python main.py init.json`, `python main.py upload.json`, `python main.py export_md.json`, `python main.py get_context.json`, `python main.py synthesize.json`, `python main.py video_wait.json`.

### 1. Initialize a Character

```json
{
  "type": "init",
  "user_id": "default",
  "target_id": "Martha"
}
```

This creates the needed directories under `storage/default_Martha/`, including `source/`, `voice_profile/`, etc.

### 2. Upload Chat Logs

```json
{
  "type": "upload",
  "user_id": "default",
  "target_id": "Martha",
  "file_path": "/path/to/chat.json",
  "file_type": "json",
  "self_name": "Jonas",
  "target_name": "Martha"
}
```

| Parameter    | Required | Description                    |
|-------------|----------|--------------------------------|
| `file_path` | ✅       | Path to chat log file          |
| `file_type` | ✅       | Currently only `json`          |
| `self_name` | ✅       | Your name (to distinguish sides) |
| `target_name` | ✅     | The other person’s name       |

### 3. Export Chat Logs to Markdown (for personality analysis)

```json
{
  "type": "export_md",
  "user_id": "default",
  "target_id": "Martha"
}
```

Output: `storage/{user_id}_{target_id}/chat.md`, for LLM personality analysis.

### 4. Analyze Personality and Save

Based on the exported `storage/{user_id}_{target_id}/chat.md` from step 3, analyze the target’s personality. If the file is large, split the markdown, analyze each part, then merge results and save to `storage/{user_id}_{target_id}/profile.md`.

**After creating or first using a character**: Add the character to the workspace root **`USER.md`** (e.g. add a "Re:Live characters" section and append something like `- **Re:Live characters:** Martha, Ulrich`). The main Agent can then read the character list from USER.md without asking again.

### 5. Get Conversation Context

When the user’s message needs history (e.g. "Do you remember our May Day plans?") or when you need history to start a topic, call:

```json
{
  "type": "get_context",
  "user_id": "default",
  "target_id": "Martha",
  "content": "What have you been up to lately?"
}
```

Returns a system prompt with profile and dual-track RAG memory for the LLM. If the current message does not need history, you can reply using only `profile.md` and current context without calling this.

### 6. Generate Reply (optional voice/video)

```json
{
  "type": "synthesize",
  "user_id": "default",
  "target_id": "Martha",
  "content": "Working on the project proposal, presenting next week",
  "user_message": "What have you been up to lately?",
  "output_mode": "voice"
}
```
(Voice mode requires the reference audio transcript in `voice_profile/corresponding.txt`, or pass the `prompt_text` parameter.)

| Parameter        | Required | Description |
|------------------|----------|-------------|
| `user_id`        | ✅       | User ID, same as init/upload |
| `target_id`      | ✅       | Character ID |
| `content`        | ✅       | AI reply text to synthesize (passed to TTS in voice/video mode) |
| `user_message`   | ✅       | User’s message for this turn; written to runtime log and RAG index |
| `output_mode`    | No       | `text` (default), `voice`, `video` |
| `prompt_text`    | One of two for voice | Transcript of reference audio; can also be set in `voice_profile/corresponding.txt`; must match audio content. |

`output_mode` options: `text` (text only), `voice` (voice), `video` (video). **Video and voice use the same entry point**; set `output_mode` to `"video"`. Optional `reference_image_url` or `reference_image_url.txt` under the character directory; optional `video_wait: true` to wait synchronously for video completion.

---

## Preparing Chat Logs

Example chat log files (QQ and WhatsApp formats) are in the **`chatlog_examples/`** folder: `chatlog_example_qq.json` and `chatlog_example_whatsapp.json`. Use them as reference when preparing your own exports.

### Supported Formats

| Platform   | Export tool | File format |
|-----------|-------------|-------------|
| QQ        | [qq-chat-exporter](https://github.com/shuakami/qq-chat-exporter) | JSON |
| WhatsApp  | [WhatsApp-Chat-Exporter](https://github.com/KnugiHK/WhatsApp-Chat-Exporter) | JSON |

### QQ Format Example

```json
{
  "messages": [
    {
      "time": "2019-04-01 13:23:36",
      "sender": {"name": "Deer"},
      "content": {"text": "Message content"}
    }
  ]
}
```

Full example: [chatlog_example_qq.json](chatlog_examples/chatlog_example_qq.json)

### WhatsApp Format Example

```json
{
  "chat_id@s.whatsapp.net": {
    "name": "John",
    "messages": {
      "1": {
        "from_me": false,
        "timestamp": 1699123200,
        "data": "Message content",
        "sender": "John"
      }
    }
  }
}
```

Full example: [chatlog_example_whatsapp.json](chatlog_examples/chatlog_example_whatsapp.json)

---

## Integration with Main Agent (/relive command)

In the main Agent (e.g. OpenClaw), implement:

- **`/relive:<character_id>`** (e.g. `/relive:meihan`): Enter relive mode; all subsequent dialogue uses this skill and is persisted under `storage/{user_id}_{target_id}/`; each turn is indexed for RAG.
- **`/relive:end`**: Exit relive mode, clear current relive character; dialogue no longer goes through the relive skill.

The main Agent must **persist** the "current relive character" in the session (e.g. `current_relive_target = "meihan"`). Until the user types `/relive:end`, use this skill’s `get_context` + generate + `synthesize` flow and write to runtime log and vector store.

**When entering a character**: Before each conversation with that character, **always read** that character’s **`profile.md`** (`storage/{user_id}_{target_id}/profile.md`) as the personality and style basis and inject it into the main Agent’s system or context.

See the "Command protocol" section in `SKILL.md` for details.

---

## Advanced Features

### Voice Synthesis

For voice output you need:

1. **Voice samples**: Put reference audio (`.wav` / `.mp3` / `.m4a`) for the target in `storage/{user_id}_{target_id}/voice_profile/`, at least one file.
2. **Transcript for reference audio**: Must match the audio for voice cloning alignment. Either: (1) create **`corresponding.txt`** under `voice_profile/` with the transcript, or (2) pass **`prompt_text`** when calling `synthesize`. When creating a character, if the user provides reference audio, ask for the transcript and save it to `corresponding.txt`.
3. Set `output_mode: "voice"`.

If the above are not met, output falls back to text and the response includes `voice_skip_reason`. Complete the **"Installation and Voice Models"** section above before using voice.

### Video Generation

Video uses the same entry as voice: set `output_mode: "video"` in synthesize to use the video generation API (e.g. Seedance). Reference image is a **URL**: pass `reference_image_url` or put it in `reference_image_url.txt` under the character directory. After a successful `video_task_id` is returned, you can run the auto-generated `video_wait.json` (`python main.py video_wait.json`) to poll and download to that character’s `cache/`. For synchronous video link, pass `video_wait: true` in the synthesize request.

**Configuration**: In `config/settings.yaml` set `video_generation` (including `model_id` for the inference endpoint) and set `ARK_API_KEY`. The request’s `model` must be the **inference endpoint ID** (created in the Volc Engine console), not the model name. See [Volc Engine: Create inference endpoint](https://www.volcengine.com/docs/82379/1099522).

#### Poll and Download Video (video_generation_wait)

The **`type` in the JSON must be `video_generation_wait`** (the code dispatches by this). The conventional filename is `video_wait.json`. After synthesize returns `video_task_id`, create or use the auto-generated `video_wait.json`:

```json
{
  "type": "video_generation_wait",
  "user_id": "default",
  "target_id": "Martha",
  "task_id": "paste video_task_id from synthesize response here",
  "poll_interval_seconds": 5,
  "poll_timeout_seconds": 600
}
```

Run: `python main.py video_wait.json`. On success, video is saved to `storage/{user_id}_{target_id}/cache/{task_id}.mp4` and the response includes `video_path` and `video_url`; on timeout or failure `success` is false with `error`.

---

## File Structure

```
storage/{user_id}_{target_id}/
├── source/                  # Original chat logs (written by upload, read-only)
├── chat.md                  # Exported chat Markdown (export_md), for personality analysis
├── chat_meta.json           # Metadata (self_name/target_name)
├── profile.md               # Personality profile (written after LLM analysis); must read when entering character
├── reference_image_url.txt  # Optional: one line, first-frame image URL for output_mode: video
├── voice_profile/           # Reference audio (.wav/.mp3/.m4a) + corresponding.txt (required, audio transcript)
├── runtime/                 # Dialogue log, including conversation.jsonl (appended on each synthesize)
├── vector_db/               # Dual-track BM25: source_index (real history), runtime_index (saved simulated dialogue)
└── cache/                   # Generated artifacts: .wav for voice, .mp4 for video (video_wait download)
```

---

## Core Modules (Implementation Reference)

| Module | Description |
|--------|-------------|
| **main.py** | Skill entry; receives JSON messages and dispatches by `type` to handlers |
| **core/orchestrator.py** | Multimodal orchestration; Text → Voice → Video pipeline |
| **core/importer/** | Chat log parsing (QQ/WhatsApp JSON, etc.) |
| **core/memory/** | Dual-track RAG: dual_rag.py, vector_store.py; BM25 term matching, no embedding |
| **core/engines/** | llm_engine, voice_engine (CosyVoice3), video_gen_engine (video API, e.g. Seedance) |

---

## API Summary

| type | Description | Required parameters |
|------|-------------|---------------------|
| `init` | Initialize storage directories | `user_id`, `target_id` |
| `upload` | Upload chat logs | `user_id`, `target_id`, `file_path`, `file_type`, `self_name`, `target_name` |
| `export_md` | Export chat logs to Markdown | `user_id`, `target_id` |
| `get_context` | Get conversation context (incl. RAG memory) | `user_id`, `target_id`, `content` |
| `synthesize` | Generate reply and persist (text/voice/video same entry, distinguished by `output_mode`) | `user_id`, `target_id`, `content`, `user_message` |
| `video_generation_wait` | Poll video task until done and download to character cache/ | `user_id`, `target_id`, `task_id` |

**upload**: `self_name` / `target_name` must **exactly match** sender names in the chat log.  
**synthesize**: `output_mode` can be `text` (default), `voice`, `video`. Optional `reference_image_url` (first-frame URL); if not passed, read from `reference_image_url.txt` under the character directory. Optional `video_wait: true` to poll within the call until video is done and return `video_url`. After video success, `video_wait.json` is auto-generated; run `python main.py video_wait.json` to download to `storage/{user_id}_{target_id}/cache/{task_id}.mp4`.

---

## Where RAG Searches

RAG is **dual-track**. Each `get_context` uses the current user input to search both stores below and injects results into the system prompt as "relevant memory":

| Source | Index path | Original data |
|--------|------------|----------------|
| **Real history** | `storage/{user_id}_{target_id}/vector_db/source_index/` | **Raw files**: `*.json` / `*.csv` / `*.txt` under `storage/{user_id}_{target_id}/source/` (chat logs uploaded via `upload`). After upload, `index_source_data` parses and writes to the index above. |
| **Saved simulated dialogue** | `storage/{user_id}_{target_id}/vector_db/runtime_index/` | Each `synthesize` appends the turn to `runtime/conversation.jsonl` and `index_runtime_data` writes to the index above. |

---

## Notes

- **Privacy**: User data is isolated per character and used only for the current clone task.
- **Ethics**: Do not use for deception, forgery, or other misuse.

---

The above content is for academic use only and is intended to demonstrate technical capabilities. Some examples are sourced from the internet. If any content infringes your rights, please contact us to request removal.

## Troubleshooting

### .venv folder not created
On Windows, if `python -m venv .venv` produces no output and no `.venv` folder appears, `python` is likely the **Windows Store stub** (check with `where python` — if it shows `WindowsApps\python.exe`, that is the stub). Install a real Python from [python.org](https://www.python.org/downloads/) (recommended 3.10), ensure “Add Python to PATH” is checked, open a **new** terminal, then run `python -m venv .venv` again. Alternatively use the full path to your Python executable: `"C:\Python310\python.exe" -m venv .venv`.

### Messages not attributed correctly
Check that `self_name` and `target_name` exactly match the names in the chat log (case, spaces, nicknames must match).

### Format recognition failed
Ensure the file is JSON and contains a `messages` array (QQ) or the WhatsApp nested structure.

### Voice not generating

1. **Environment and models**: Complete **"Installation and Voice Models"** above: `pip install -r requirements.txt`, put CosyVoice repo under `models/voice/CosyVoice`, and download Fun-CosyVoice3-0.5B and CosyVoice-ttsfrd to `models/pretrained_models/`.
2. **Voice samples and transcript**: Check that `storage/{user_id}_{target_id}/voice_profile/` has reference audio (.wav/.mp3/.m4a) and that `corresponding.txt` (or `prompt_text` passed to synthesize) is set correctly and matches the audio.
3. **Execution timeout in OpenClaw**: When running this skill through OpenClaw’s `exec`, long CosyVoice3 synthesis can be killed by the default timeout. In `npm/node_modules/openclaw/dist/auth-profiles-*.js`, increase `DEFAULT_EXEC_TIMEOUT_MS` (e.g. from `5e3` to `180e3`) so that long voice synthesis jobs are not terminated prematurely.

### Video not generating
Confirm `ARK_API_KEY` is set and `config/settings.yaml` has `video_generation.enabled` true.

### Video API returns 404
The request’s `model` must be the **inference endpoint ID** (created in the Volc Engine console), not the model name. Create an inference endpoint in the [Volc Engine console](https://console.volcengine.com/ark), deploy the video model, and set its ID in `config/settings.yaml` under `video_generation.model_id`.
