---
name: video-intent-studio
description: Guide staged text-to-video generation from a rough user idea to ranked video type options, parameter tuning, prompt preview, and final Volcengine Ark video generation via bundled helper scripts. Use when a user wants help deciding video style, duration, ratio, motion, or prompt wording before generating a video, and when a reusable multi-turn workflow with simple state tracking is needed.
---

# Video Intent Studio

Follow a user-led workflow for video generation. Do not choose the final prompt for the user. Suggest options, keep the current prompt transparent, and ask for confirmation before generation.

## Core behavior

- Respond in the user's language. Default to Chinese if the user is writing in Chinese.
- Keep the workflow layered: intent -> ranked video types -> parameter tuning -> prompt confirmation -> generation.
- Present 3 to 5 options at the type-selection step. Keep the option set stable and only reorder by relevance.
- Show the current prompt preview whenever parameters change.
- Let the user revise or exit at every stage.
- Keep a simple state object in memory or scratch space:

```python
state = {
    "user_input": "",
    "selected_type": None,
    "params": {
        "duration": 8,
        "ratio": "16:9",
        "motion": "medium",
        "style": "original",
        "brightness": "normal",
        "subtitle": "off",
        "dream_filter": "off",
    },
    "final_prompt": "",
    "stage": "init",
}
```

## Skill directory and script paths

When this `SKILL.md` is loaded, resolve the skill directory from the absolute path of this file.

- Suggestion and prompt builder:
  - `<skill-dir>/scripts/video_agent_backend.py`
- Final generator:
  - `<skill-dir>/scripts/generate_ark_video.py`
- Type catalog and defaults:
  - `<skill-dir>/references/video-types.md`
- Usage walkthrough and examples:
  - `<skill-dir>/references/usage-guide.md`

Use absolute paths when running the scripts.

## Recommended workflow

1. Capture the user's raw idea.
   - Keep the original wording in state as `user_input`.
   - Do not rewrite it into a final prompt yet.

2. Rank video types.
   - Run:

```bash
python "<skill-dir>/scripts/video_agent_backend.py" suggest --input "user idea"
```

   - Present the top 3 to 5 results as numbered options.
   - For each option, include:
     - type name
     - one-sentence use case
     - default duration and ratio
     - short reason why it matches

3. After the user chooses a type, build a prompt preview.
   - Run:

```bash
python "<skill-dir>/scripts/video_agent_backend.py" build ^
  --input "user idea" ^
  --type cinematic-story
```

   - Show:
     - current prompt preview
     - current parameter summary
     - a short numbered list of tunable options

4. If the user adjusts settings, rerun `build` with explicit parameters.
   - Supported parameters:
     - `--duration 5|8|10|12`
     - `--ratio 9:16|16:9|1:1|4:3`
     - `--motion light|medium|strong`
     - `--style realistic|anime|cinematic|original`
     - `--brightness moody|normal|bright`
     - `--subtitle off|on`
     - `--dream-filter off|on`
     - `--notes "extra user constraint"`

5. Before generation, show the final prompt and ask for confirmation.
   - Use a short confirmation question such as:
     - "Final prompt and parameters are ready. Generate now?"

6. After explicit confirmation, generate the video.
   - Run:

```bash
python "<skill-dir>/scripts/generate_ark_video.py" ^
  --prompt "final prompt text" ^
  --output "C:\path\to\result.mp4"
```

7. Report success or failure clearly.
   - On success, give the downloaded file path and task id if available.
   - On failure, bucket the issue into one of:
     - API key or auth problem
     - network or polling problem
     - task failed remotely
     - response did not include a downloadable video URL

## Important implementation notes

- The bundled generator script intentionally mirrors the existing HTTP + polling pattern already used in this workspace.
- The current API request sends a text prompt payload only. Duration, ratio, motion, style, and other controls are encoded into the prompt text unless you later extend the API payload.
- The generator script reads credentials from environment variables first:
  - `ARK_API_KEY`
  - `VOLCENGINE_ARK_API_KEY`
- Optional environment variables:
  - `ARK_VIDEO_MODEL`
  - `ARK_VIDEO_TASKS_URL`

## Conversation rules

- Do not skip the type-selection step unless the user explicitly says they already know the type.
- Do not ask broad open-ended questions if a numbered choice is possible.
- If the user says "more realistic", "more cinematic", "shorter", "vertical", or similar, treat that as a parameter update and keep moving.
- If the user says "generate", "go", or "就这样生成", show the final prompt once and ask for one explicit confirmation unless they already confirmed in the same message.

## When to read references

- Read [references/video-types.md](references/video-types.md) when you need the fixed type list, defaults, or category-specific prompt leads.
- Read [references/usage-guide.md](references/usage-guide.md) when you need example conversations, sample commands, or the user-facing tutorial flow.
