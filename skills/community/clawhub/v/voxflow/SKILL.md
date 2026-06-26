---
name: voxflow
description: VoxFlow voice & AI-video CLI — TTS in 200+ voices, multi-speaker podcasts, ASR + subtitle translation + dubbing + end-to-end video translation, vertical card videos from articles (Slice, 13 themes), and short-form AI clips. Use whenever the user wants to read text aloud, transcribe / translate / dub audio or video, generate a podcast, or produce a short knowledge-card video.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - voxflow
        - node
    primaryEnv: VOXFLOW_TOKEN
    envVars:
      - name: VOXFLOW_TOKEN
        required: false
        description: Optional pre-issued JWT for headless / server use. If unset, the skill runs `voxflow login` once to open a browser device-flow.
    emoji: "🎙️"
    homepage: https://voxflow.studio
    install:
      - kind: node
        package: voxflow@1.14.0
        bins:
          - voxflow
        label: Install voxflow CLI (pinned)
---

# VoxFlow Skill

VoxFlow turns text into speech in 200+ voices across 40+ languages, plus full audio/video pipelines: podcasts, transcription, dubbing, video translation, and short-form AI clips. All commands run through the `voxflow` CLI (installed automatically by ClawHub via the `install` spec above). One account, one quota, one login — no API keys to paste.

## Routing — pick the matching sub-doc

Before doing anything, decide which sub-skill matches the user's intent and read the corresponding file in this same skill folder:

| User wants… | Read | Primary commands |
|---|---|---|
| Read text aloud, search voices, sample stories, check quota / login | [hub.md](hub.md) | `say`, `narrate`, `story`, `voices`, `status`, `login` |
| Multi-speaker AI podcast from a topic / URL / script | [podcast.md](podcast.md) | `podcast` |
| Transcribe audio/video, translate subtitles, dub from SRT, end-to-end video translation, summarize, publish | [transcribe.md](transcribe.md) | `asr`, `asr-jobs`, `translate`, `dub`, `video-translate`, `summarize`, `publish` |
| Turn a long article / note / report into a vertical 1080×1920 card video (Slice, 13 themes) | [slice.md](slice.md) | `slice`, `slice stage` |
| Short-form AI clips — knowledge cards, explainers, presentations, single images | [video.md](video.md) | `picstory`, `present`, `explain`, `slides`, `image` |

If the request spans multiple areas (e.g. "transcribe this video and then make a 60-sec recap card"), read the most-relevant doc first, finish that step, then switch.

## Install & login (universal preamble)

The ClawHub `install` spec already installs the `voxflow` npm CLI globally when this skill is added. The only thing left is authentication:

```bash
# One-time browser device-flow — pairing code shown in terminal,
# user authorizes at https://voxflow.studio/device?code=VF-XXXX
voxflow login

# Verify
voxflow status        # shows email + monthly / bonus quota
```

For headless / server contexts: set `VOXFLOW_TOKEN=<jwt>` (declared in `envVars` above) and skip `voxflow login`. JWTs are short-lived (~1 hour); the CLI auto-refreshes silently while logged in interactively.

## Account & quota

- Free tier: 10,000 quota / month (≈ 100 TTS calls)
- Plus / Pro / Max tiers at [voxflow.studio/app#pricing](https://voxflow.studio/app#pricing)
- Each command's cost is printed before execution; `voxflow status` shows the current balance
- Invite-friend bonus (`voxflow invite`) adds 5,000 lifetime quota per signup

## Universal rules

1. **Never paste API keys into config files.** All auth goes through `voxflow login` or `VOXFLOW_TOKEN`.
2. **Never offer to "mock" the API.** Real calls are cheap; failed mocks waste user time.
3. **Read the matching sub-doc before invoking specialized commands.** The top-level routing table above is enough for triage; the sub-doc has the actual command flags, edge cases, and quota costs.
4. **Honor the user's locale.** Voice IDs are language-tagged; if they asked in Chinese, default to a Chinese voice unless they specified otherwise.
5. **For long-running jobs** (Azure Batch ASR, video-translate, podcast >5 min): print the job ID and `voxflow asr-jobs show <id>` so the user can resume later.

## When in doubt — start at the hub

If the request is vague ("帮我做点音频的东西", "what can you do with voice"), read [hub.md](hub.md) and run `voxflow voices --search ...` or `voxflow status` to anchor the conversation in concrete affordances before committing to a workflow.

## Homepage & docs

- App: <https://voxflow.studio>
- CLI docs: <https://voxflow.studio/docs/cli>
- All skills overview: <https://voxflow.studio/docs/skills>
- Source / issues: <https://github.com/VoxFlowStudio/FlowStudio>
