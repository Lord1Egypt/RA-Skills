## Description:

A Chinese-language Sparki skill for tightening and polishing talking-head, interview, tutorial, and presenter videos through upload, prompt-driven editing, status polling, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to guide an agent through Sparki-based editing of local talking-head or presenter videos, including upload, edit project creation, status checks, and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected video files are uploaded to Sparki for remote processing.

Mitigation: Use the skill only with videos the user is comfortable sending to Sparki, and confirm local file paths before upload.

Risk: API credentials can be saved in local OpenClaw configuration.

Mitigation: Prefer the SPARKI_API_KEY environment variable and avoid persisting credentials unless the user explicitly wants saved setup.

Risk: The skill may steer agents toward remote Sparki processing for simple or unrelated video tasks.

Mitigation: Use it for talking-head or presenter editing requests and reassess whether a local or simpler tool is more appropriate for unrelated tasks.

Risk: Downloaded results write to local output paths.

Mitigation: Review the output path before download and keep writes within the intended workspace or user-approved destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/talking-head-editor-zh)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload link](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON status data and downloaded video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPARKI_API_KEY; uploads mp4 or mov files to Sparki; default downloads are written under ~/.openclaw/workspace/sparki/videos unless an output path is provided.]

## Skill Version(s):

1.0.12 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
