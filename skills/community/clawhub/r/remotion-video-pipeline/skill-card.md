## Description:

Use this skill to produce a Remotion short video through an audio-driven pipeline: script to audio to SRT to timeline to scenes.json to render to CapCut handoff, with human gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to run a repeatable Remotion knowledge or explainer short-video workflow with narration, subtitles, scene timing, and a CapCut handoff. It helps agents preserve script approvals and audio-derived timing before rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chosen TTS or STT tools may require API keys or separate trust review.

Mitigation: Review those tools separately, keep API keys outside the skill, and avoid logging or echoing credentials.

Risk: Timeline, audio, or asset files may be overwritten during production.

Mitigation: Confirm before overwriting existing scenes.json, audio, SRT, asset, or composition files.

Risk: SRT timestamps can drift from the final audio and cause visual timing issues.

Mitigation: Use the final audio as the master timeline, generate SRT from that audio, and preview alignment before full rendering.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON timeline data and checklist-style handoff instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scripts, storyboards, SRT-derived timing guidance, scenes.json timeline data, Remotion handoff guidance, and CapCut checklist text.]

## Skill Version(s):

0.1.0 (source: changelog, released 2026-06-11; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
