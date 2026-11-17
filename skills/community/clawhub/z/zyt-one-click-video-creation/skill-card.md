## Description:

Generates a complete short-form video from a topic or spoken script, including copy, storyboard scenes, digital-human narration, AI video shots, and local ffmpeg assembly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and developers use this skill to turn a topic or finished spoken script into a publishable vertical short video. It is suited to workflows that need agent-generated planning, narration text, storyboard prompts, Chanjing TTS and digital-human video calls, AI B-roll generation, and local mp4 assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and stores Chanjing account credentials locally and allows the API host to be overridden.

Mitigation: Run it only in a trusted runtime, protect ~/.chanjing/credentials.json with owner-only permissions, and leave CHANJING_API_BASE unset or pinned to the official HTTPS Chanjing API host.

Risk: Workflow scripts, generated audio, or private media may be sent to the Chanjing service during video creation.

Mitigation: Do not include sensitive unpublished scripts or private media unless the user is comfortable sending that material to the Chanjing service.

Risk: Default persona and ethnicity rules can affect demographic representation in generated video scenes.

Mitigation: Review and adjust the persona, digital-human selection, and visual prompt constraints when demographic neutrality or a specific representation goal matters.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)
- [ClawHub skill page](https://clawhub.ai/zuoyuting214/skills/zyt-one-click-video-creation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance, JSON workflow data, shell commands, and local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Render runs can write final_one_click.mp4, workflow_result.json, and intermediate work files in the selected output directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
