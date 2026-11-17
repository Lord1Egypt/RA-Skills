## Description:

Given a topic or prepared voiceover, Video Creation helps an agent generate a short-video package with copy, storyboard scenes, avatar narration, AI-generated video segments, and local MP4 assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn a topic or prepared voiceover into a short vertical video with a plan, script, storyboard, TTS audio, avatar narration, AI b-roll, and local MP4 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends scripts, generated audio, and video prompts to Chanjing services.

Mitigation: Use only non-sensitive inputs and install the skill only when the Chanjing data flow is acceptable for the intended content.

Risk: The workflow downloads remote media URLs and processes generated files locally with ffmpeg.

Mitigation: Run the skill in a contained environment and use a dedicated output directory before opening or reusing generated files.

Risk: Generated outputs may inherit demographic or cultural defaults from the skill templates.

Mitigation: Review and override demographic, cultural, and visual-prompt defaults before using the skill for general-purpose or public content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyuting214/skills/video-creation)
- [Chanjing Open API](https://open-api.chanjing.cc)
- [Skill README](artifact/README.md)
- [Render rules](artifact/templates/render_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, JSON workflow data, shell commands, and local media/result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHANJING_APP_ID, CHANJING_SECRET_KEY, ffmpeg, and ffprobe; writes generated media and workflow_result.json to a local output directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
