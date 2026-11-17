---
name: socialkit-youtube-pipeline
description: Runs the end-to-end YouTube video workflow (research, script, visuals, assembly, metadata, upload) and stops at three mandatory human approval checkpoints. Use when the user wants to make, produce or publish a YouTube video or Short from an idea, topic or source material, or asks where a video project stands.
license: MIT
metadata:
  author: Ahmad Hussain
  platform: youtube
  requires: socialkit-social-core socialkit-youtube-research socialkit-youtube-script socialkit-youtube-visuals socialkit-youtube-assemble socialkit-youtube-metadata socialkit-youtube-upload
---

# YouTube pipeline

Orchestrates the youtube-* skills. Each step below names the skill to follow. Script
paths are relative to the directory of the skill that owns them. Apply socialkit-social-core to
all content.

The three checkpoints are mandatory. YouTube's inauthentic content policy removes
monetization from channels that publish mass-produced or repetitive content without
meaningful human input, so a person must review the script, the packaging and the
final upload. See [policy notes](references/policy.md).

## Steps

1. **Brief.** Ask for topic, audience, target length (Short or long-form), language,
   and whether any realistic AI-generated voice, people or footage will be used.
2. **Project folder.** Pick a short slug and run
   `node scripts/state.mjs --init --dir yt-<slug> --slug <slug>`.
   All later files go in `yt-<slug>/`.
3. **Research (optional).** Follow socialkit-youtube-research. Output: `research.md`.
4. **Script.** Follow socialkit-youtube-script. Output: `script.md`.
5. **Checkpoint 1: script.** Stop. Show the script. Ask the user to run, in their own
   terminal: `node scripts/state.mjs --dir yt-<slug> --approve script`.
   Then run `node scripts/state.mjs --dir yt-<slug> --verify script`. Continue only
   when it exits 0.
6. **Visuals.** Follow socialkit-youtube-visuals. Output: `shot-list.json`; the user supplies
   or approves every asset.
7. **Assembly.** Follow socialkit-youtube-assemble. Output: `output/video.mp4`.
8. **Metadata.** Follow socialkit-youtube-metadata. Output: `metadata.json` and a thumbnail.
9. **Checkpoint 2: metadata.** Stop. Show title, description, tags and thumbnail. Ask the
   user to run `node scripts/state.mjs --dir yt-<slug> --approve metadata`, then verify.
10. **Upload plan.** Follow socialkit-youtube-upload to write `upload-plan.json` (private by
    default; schedule and synthetic-media flags as the user decides).
11. **Checkpoint 3: upload.** Stop. Ask the user to watch `output/video.mp4` and run
    `node scripts/state.mjs --dir yt-<slug> --approve upload`, then verify.
12. **Upload.** Follow socialkit-youtube-upload. Report the video URL, privacy and any warnings.

Check progress at any time with `node scripts/state.mjs --dir yt-<slug> --status`.

## Rules

- Never run `--approve` yourself, never edit `state.json`, never fake terminal input.
- Any edit to an approved file invalidates that approval. Re-request it; do not revert
  files to make verification pass without telling the user.
- Do not batch-produce videos. One project, one set of approvals.

## Output contract

At the end, report: project folder, checkpoint status, video URL, Studio URL, privacy
status, scheduled time, synthetic-media disclosure, and warnings, as a short list.

## Failure handling

- `APPROVAL_NEEDS_TERMINAL`: the approve command was run without a terminal. Ask the
  user to run it themselves.
- Verification fails: say which file changed and ask whether to re-approve.
- Any step's script exits non-zero: show its error and hint, fix inputs if the cause is
  clear, otherwise ask the user. Do not skip the step.
