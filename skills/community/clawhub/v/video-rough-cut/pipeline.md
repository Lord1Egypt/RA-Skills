# Current Rough-Cut Pipeline

This skill reflects the current B-Roll Studio rough-cut implementation.

## What the pipeline does

1. Extract source metadata
2. Transcribe speech with Whisper
3. Analyze audio energy and breath / pause events
4. Detect head/tail clutter
5. Merge cut decisions into kept segments
6. Optionally stabilize video
7. Analyze brightness and clamp over-bright footage
8. Optionally auto-center subject
9. Optionally apply beauty
10. Encode final output

## Practical defaults

- pause removal: on
- breath removal: on
- head/tail trimming: on
- stabilization: on
- auto-centering: on
- brightness adjustment: on
- beauty: `light`
- denoise: off

## Important behavioral notes

- This is a **rough cut**, not a final edit.
- The system tries to remove `321走 / 试音 / 收镜头动作` as clutter.
- Head/tail trimming is intentionally conservative around正文.
- Audio denoise is off by default because strong denoise made speech sound闷.
- Brightness logic is no longer "only brighten"; very bright footage can be
  slightly darkened back to a natural range.

## What to tell users

If a user says:

- "正文也被裁了"
  Explain that head/tail trimming needs review or rerun.

- "尾巴收镜头还在"
  Explain that the issue belongs to head/tail clutter detection, not pause removal.

- "画面很亮"
  Explain that brightness correction should stay enabled and be rerun.

- "声音发闷"
  Explain that denoise should remain off unless the source noise is severe.
