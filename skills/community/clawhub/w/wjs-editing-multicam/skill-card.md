## Description:

Use when the user has 2+ recordings of the same event with `.sync.json` sidecars and wants them combined into a single MP4 with audio-energy-driven camera switching and optional picture-in-picture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and video-editing agents use this skill to generate edit decisions and render synced multicamera recordings into MP4 outputs with hard cuts or picture-in-picture. It is suited to events with multiple camera angles and synced sidecars where audio energy is an acceptable switching signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or untrusted edit-plan JSON can drive FFmpeg rendering without sufficient validation.

Mitigation: Use EDL files generated from trusted media, or validate input paths, time ranges, camera indexes, and bounds before rendering.

Risk: The render scripts overwrite the chosen output path.

Mitigation: Keep backups and choose an output path that does not replace important media or project files.

Risk: Audio-energy switching is a proxy and may choose a poor source when a microphone is clipped, noisy, or quiet.

Mitigation: Review a short sample render and override the audio source or edit segments before committing to a full render.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-editing-multicam)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include EDL JSON and MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local FFmpeg-based rendering and requires original camera media plus optional `.sync.json` sidecars.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
